import socket
import time
import threading

IP = "192.168.5.1"
PORT = 58080

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Using 1MB buffer as strictly mandated for Windows UDP bursts
sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1048576)
sock.settimeout(2.0)

running = True

def keep_alive():
    while running:
        try:
            sock.sendto(b'\x20\x36', (IP, PORT))
        except Exception:
            pass
        time.sleep(1.5)

threading.Thread(target=keep_alive, daemon=True).start()

print("--- BEBIRD UDP DIAGNOSTIC SCRIPT ---")
print("Gathering telemetry for 15 seconds...")
start_time = time.time()

total_packets = 0
missing_packets = 0
last_frame_id = -1
last_chunk_idx = -1

latencies = []
last_recv_time = time.time()

header_samples = []

try:
    while time.time() - start_time < 15:
        try:
            data, _ = sock.recvfrom(65536)
            now = time.time()
            latencies.append(now - last_recv_time)
            last_recv_time = now
            
            total_packets += 1
            
            if len(data) >= 4:
                frame_id = data[0]
                last_flag = data[1]
                chunk_idx = data[2]
                angle = data[3]
                
                if len(header_samples) < 5:
                    header_samples.append(data[:16].hex())
                
                # Check for missed chunks inside the same frame
                if frame_id == last_frame_id:
                    if chunk_idx > last_chunk_idx + 1:
                        missing_packets += (chunk_idx - last_chunk_idx - 1)
                
                last_frame_id = frame_id
                last_chunk_idx = chunk_idx
        except socket.timeout:
            pass
except KeyboardInterrupt:
    pass
finally:
    running = False
    print("\n--- RESULTS ---")
    print(f"Total Packets Received: {total_packets}")
    print(f"Missing Packets Detected: {missing_packets}")
    
    if total_packets + missing_packets > 0:
        loss_rate = (missing_packets / (total_packets + missing_packets)) * 100
        print(f"Packet Loss Rate: {loss_rate:.2f}%")
    
    if latencies:
        print(f"Average Arrival Latency: {(sum(latencies)/len(latencies))*1000:.2f} ms")
        print(f"Max Arrival Latency: {max(latencies)*1000:.2f} ms")
        
    print("Header Samples (first 16 bytes hex):")
    for h in header_samples:
        print(f"  {h}")
