import socket
import threading
import time
import cv2
_native_imshow = cv2.imshow  # Save original before ultralytics imports
import numpy as np
from collections import deque, defaultdict
import sys
import os
from ultralytics import YOLO

# Ensure src modules can be found
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.ai.green_filter import GreenFilterEngine

# Import Hardware SIMD Accelerated JPEG Decoder
try:
    from turbojpeg import TurboJPEG
except ImportError:
    TurboJPEG = None

class StreamEngine:
    def __init__(self, ip='192.168.5.1', port=58080):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # OS UDP Receive Buffer to 1MB (prevent buffer bloat & backlog)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576)
        self.sock.settimeout(2.0)
        
        self.running = False
        
        # [NEW] Persist last valid frame for zero CPU lockup during packet loss
        self.last_valid_frame = None
        
        self.lock = threading.Lock()
        self.current_ai_frame = None
        self.latest_boxes = None  
        
        # [NEW] Rotation & Gyro State Engine
        self.rotation_state = 0  # 0: 0°, 1: 90°, 2: 180°, 3: 270°
        self.gyro_angle = 0
        
        # [NEW] Digital Green Filter Engine
        self.dgf_engine = GreenFilterEngine()
        self.dgf_enabled = False
        
        # Graceful Fallback Initialization for TurboJPEG
        try:
            if TurboJPEG is not None:
                self.jpeg = TurboJPEG()
                self.use_turbo = True
            else:
                self.jpeg = None
                self.use_turbo = False
        except Exception as e:
            print("[WARN] TurboJPEG DLL not found: Unable to locate turbojpeg library automatically. You may specify the turbojpeg library path manually.")
            print("e.g. jpeg = TurboJPEG(lib_path). Falling back to OpenCV optimized imdecode.")
            self.use_turbo = False
            self.jpeg = None

        print("[AI Agent] Loading YOLOv8 model for Async Worker...")
        model_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'ai', 'cerviscan_best.pt'))
        if os.path.exists(model_path):
            print(f"[AI Agent] Loading custom trained model: {model_path}")
            self.model = YOLO(model_path)
        else:
            print("[WARN] Custom model not found! Falling back to generic YOLOv8n.")
            self.model = YOLO('yolov8n.pt') 
        
    def start(self):
        self.running = True
        
        # [NEW] Start Non-Blocking Keep-Alive Thread
        self.keep_alive_thread = threading.Thread(target=self._keep_alive_loop, daemon=True)
        self.keep_alive_thread.start()
        
        self.producer_thread = threading.Thread(target=self._producer_loop, daemon=True)
        self.producer_thread.start()
        
        self.ai_thread = threading.Thread(target=self._ai_worker_loop, daemon=True)
        self.ai_thread.start()
        
        self._display_loop()

    def stop(self):
        self.running = False
        try:
            self.sock.sendto(b'\x20\x37', (self.ip, self.port))
        except Exception:
            pass
        self.sock.close()
        cv2.destroyAllWindows()

    def _keep_alive_loop(self):
        """Dedicated daemon thread to ping the hardware continuously."""
        print("[IoT Agent] Background Keep-Alive Thread running.")
        while self.running:
            try:
                self.sock.sendto(b'\x20\x36', (self.ip, self.port))
            except Exception:
                pass
            time.sleep(1.0)  # Ping every 1.0 second to keep LED solid & sync alive

    def _producer_loop(self):
        print("[IoT Agent] Flushing stale UDP packets...")
        self.sock.setblocking(False)
        while True:
            try:
                self.sock.recv(65536)
            except Exception:
                break
        self.sock.settimeout(2.0)

        print("[IoT Agent] Listening for Bebird UDP stream on port 58080...")
        
        frame_chunks = defaultdict(dict)
        last_frame_id = -1
        first_chunk_size = 1400

        while self.running:
            try:
                data, _ = self.sock.recvfrom(65536)
                if len(data) < 5:
                    continue
                
                c_frame_id = data[0]
                c_last_flag = data[1]
                c_chunk_idx = data[2]
                c_angle_low = data[3]
                c_payload = data[4:]

                if c_chunk_idx == 1:
                    first_chunk_size = len(c_payload)
                    # New frame started; if we had a previous frame, we can clean it up
                    if last_frame_id != -1 and last_frame_id != c_frame_id:
                        if last_frame_id in frame_chunks:
                            del frame_chunks[last_frame_id]
                
                last_frame_id = c_frame_id
                frame_chunks[c_frame_id][c_chunk_idx] = c_payload

                if c_last_flag > 0:
                    self.gyro_angle = c_angle_low + (256 if c_last_flag > 1 else 0)
                    total_chunks = c_chunk_idx

                    # Strict Frame-Discard: Only assemble if ALL chunks arrived (no dummy 0x00 padding)
                    if len(frame_chunks[c_frame_id]) == total_chunks:
                        parts = [frame_chunks[c_frame_id][i] for i in range(1, total_chunks + 1)]
                        
                        raw_jpeg = b''.join(parts)
                        soi = raw_jpeg.find(b'\xff\xd8')
                        eoi = raw_jpeg.rfind(b'\xff\xd9')

                        if soi != -1 and eoi != -1 and eoi > soi:
                            # Clean Bebird 0x00 padding
                            if raw_jpeg[eoi-1:eoi] == b'\x00':
                                clean_jpeg = raw_jpeg[soi:eoi-1] + b'\xff\xd9'
                            else:
                                clean_jpeg = raw_jpeg[soi:eoi+2]
                            
                            frame = None
                            if self.use_turbo and self.jpeg is not None:
                                try:
                                    frame = self.jpeg.decode(clean_jpeg)
                                except Exception:
                                    pass
                            
                            if frame is None:
                                np_arr = np.frombuffer(clean_jpeg, np.uint8)
                                frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

                            if frame is not None:
                                with self.lock:
                                    self.last_valid_frame = frame
                                    self.current_ai_frame = frame
                    
                    # Frame rendered or dropped, cleanup
                    del frame_chunks[c_frame_id]

                # Maintain buffer size
                while len(frame_chunks) > 3:
                    oldest_key = next(iter(frame_chunks))
                    del frame_chunks[oldest_key]

            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    print(f"[IoT Agent] Stream error: {e}")

    def _ai_worker_loop(self):
        print("[AI Agent] Async Inference Thread running in background.")
        while self.running:
            frame_to_process = None
            
            with self.lock:
                if self.current_ai_frame is not None:
                    frame_to_process = self.current_ai_frame.copy()
                    self.current_ai_frame = None  # [NEW] Clear to skip redundant inference on same frame
            
            if frame_to_process is not None:
                # [NEW] Set confidence threshold to 0.55 to eliminate background skin noise
                results = self.model(frame_to_process, imgsz=320, verbose=False, conf=0.55)
                
                boxes_data = []
                for box in results[0].boxes:
                    conf = float(box.conf[0])
                    # Strict display filter
                    if conf >= 0.50:
                        x1, y1, x2, y2 = map(int, box.xyxy[0])
                        cls = int(box.cls[0])
                        name = self.model.names[cls]
                        boxes_data.append((x1, y1, x2, y2, conf, name))
                
                with self.lock:
                    self.latest_boxes = boxes_data
            else:
                # Yield CPU if no new frame is ready
                time.sleep(0.01)

    def _display_loop(self):
        print("[System] Display Thread rendering frames dynamically.")
        print("[System] Hotkeys: 'r' to rotate 90°, 'g' to toggle Green Filter, 'q' to quit.")
        
        fps_start = time.time()
        frame_count = 0
        fps = 0.0
        
        while self.running:
            with self.lock:
                if self.last_valid_frame is None:
                    raw_frame = None
                else:
                    raw_frame = self.last_valid_frame.copy()

            if raw_frame is None:
                # Still waiting for the very first valid frame
                cv2.waitKey(10)
                continue
                
            disp_frame = raw_frame
            
            # Apply Digital Green Filter (DGF) if enabled
            if self.dgf_enabled:
                disp_frame = self.dgf_engine.apply_filter(disp_frame, mode='clahe_gray')
            
            with self.lock:
                boxes_to_draw = self.latest_boxes
            
            # Apply AI Overlays BEFORE rotation so they track accurately
            if boxes_to_draw:
                for (x1, y1, x2, y2, conf, name) in boxes_to_draw:
                    label = f"{name} {conf:.2f}"
                    cv2.rectangle(disp_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(disp_frame, label, (x1, y1 - 8),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Apply Frame Orientation Engine (Software Rotation)
            if self.rotation_state == 1:
                disp_frame = cv2.rotate(disp_frame, cv2.ROTATE_90_CLOCKWISE)
            elif self.rotation_state == 2:
                disp_frame = cv2.rotate(disp_frame, cv2.ROTATE_180)
            elif self.rotation_state == 3:
                disp_frame = cv2.rotate(disp_frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

            frame_count += 1
            elapsed = time.time() - fps_start
            if elapsed >= 1.0:
                fps = frame_count / elapsed
                fps_start = time.time()
                frame_count = 0
            
            # Draw HUD AFTER rotation so text is readable
            dgf_status = "ON" if self.dgf_enabled else "OFF"
            hud_text = f"FPS: {fps:.1f} | Gyro: {self.gyro_angle} | Rot: {self.rotation_state * 90} deg | DGF: {dgf_status}"
            cv2.putText(disp_frame, hud_text, (15, 35), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

            _native_imshow('CerviScan-AI Live Feed', disp_frame)
            
            # Limit UI refresh rate to ~30 FPS (~33ms per frame) to free CPU cores
            key = cv2.waitKey(30) & 0xFF
            if key == ord('r'):
                self.rotation_state = (self.rotation_state + 1) % 4
                print(f"[System] Rotated feed to {self.rotation_state * 90} degrees")
            elif key == ord('g'):
                self.dgf_enabled = not self.dgf_enabled
                print(f"[System] Digital Green Filter: {'ON' if self.dgf_enabled else 'OFF'}")
            elif key == ord('q'):
                print("[System] Shutting down pipeline...")
                self.stop()
                break

if __name__ == "__main__":
    engine = StreamEngine()
    try:
        engine.start()
    except KeyboardInterrupt:
        engine.stop()
