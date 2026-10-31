import socket
import cv2
import numpy as np
from io import BytesIO
from ultralytics import YOLO

# Muatkan model AI YOLOv8 (ia akan auto-download model ringan 'yolov8n.pt' secara automatik)
print("[+] Memuatkan model AI YOLOv8...")
model = YOLO('yolov8n.pt')

# Tetapan Rangkaian Bebird
CAMERA_IP = "192.168.5.1"
CONTROL_PORT = 58080

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1.0)

    # 1. Hantar arahan reset & trigger stream ke peranti
    print("[+] Menghantar arahan permulaan video ke Bebird...")
    try:
        sock.sendto(b'\x20\x37', (CAMERA_IP, CONTROL_PORT)) # Stop/Reset
        sock.sendto(b'\x20\x36', (CAMERA_IP, CONTROL_PORT)) # Start Video Stream
    except Exception as e:
        print(f"[-] Ralat penghantaran pemicu: {e}")
        return

    full_data = b''
    print("[+] Mendengar aliran video & Menjalankan AI Detection... Tekan 'q' pada tetingkap untuk keluar.")

    while True:
        try:
            data, _ = sock.recvfrom(2048)
            
            if len(data) < 6:
                continue

            # Semak header awal JPEG (\xff\xd8)
            if data[4:6] == b'\xff\xd8':
                full_data = data[4:]
            # Semak ekor penamat JPEG (\xff\xd9)
            elif len(data) >= 7 and data[-7:-5] == b'\xff\xd9':
                full_data += data[4:-5]
                
                # Dekod keseluruhan frame JPEG
                if len(full_data) > 0:
                    frame_array = np.frombuffer(full_data, dtype=np.uint8)
                    img = cv2.imdecode(frame_array, cv2.IMREAD_COLOR)
                    
                    if img is not None:
                        # --- JALANKAN INFERENS YOLOv8 ---
                        results = model(img, conf=0.4, verbose=False)
                        annotated_frame = results[0].plot() # Lukis kotak AI pada imej
                        
                        # Paparkan tetingkap dengan kotak pengesanan AI
                        cv2.imshow("CerviScan-AI Object Detection Test", annotated_frame)
                    
                    full_data = b'' # Reset buffer untuk frame seterusnya
            else:
                # Paket pertengahan (data payload)
                full_data += data[4:]

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        except socket.timeout:
            # Jika timeout, hantar semula paket pemicu Mula Video
            sock.sendto(b'\x20\x36', (CAMERA_IP, CONTROL_PORT))
            print("[!] Pemicu dihantar semula (Menunggu data)...")
        except Exception as e:
            continue

    # Clean up
    sock.sendto(b'\x20\x37', (CAMERA_IP, CONTROL_PORT)) # Stop stream
    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()