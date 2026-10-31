# Multi-threaded Stream Engine Blueprint (`stream_v2.py`)

## Objective
Migrate from the single-threaded `bebird_win.py` implementation to an asynchronous, high-performance Producer-Consumer architecture using `threading` and `queue.Queue`. This will isolate socket ingestion overhead from AI processing overhead, ensuring stable frame rates (FPS > 30) and low latency (<100ms) for the clinical feed.

## Architecture Proposal

### 1. The Producer (UDP Socket Ingestion)
- **Thread:** Dedicated thread for network I/O (`threading.Thread`).
- **Functionality:** 
  - Bind to UDP Port 58080 on Wi-Fi interface.
  - Send the initialization trigger `b'\x20\x36'`.
  - Continuously `recv()` chunks (e.g., 4096 bytes or larger depending on MTU).
  - Search for JPEG headers (`\xff\xd8`) and footers (`\xff\xd9`) to segment complete frames.
  - Push valid `bytes` payloads into `frame_queue`.
- **Failure Handling:** Drop incomplete chunks or corrupted frames instead of blocking.

### 2. The Shared Buffer
- **Data Structure:** `queue.Queue(maxsize=5)`
- **Behavior:** Keep the queue size small. If the Producer is faster than the Consumer, use `queue.put_nowait()` and discard older frames to prevent backpressure and latency buildup (Live video is transient, low latency > dropping a single frame).

### 3. The Consumer (AI Processing & UI)
- **Thread:** Main thread (or separate processing thread).
- **Functionality:**
  - `queue.get()` the raw JPEG byte array.
  - Decode using `cv2.imdecode(np.frombuffer(raw, dtype=np.uint8), cv2.IMREAD_COLOR)`.
  - Pass the `numpy` array to the YOLOv8 inference module and Green Filter algorithm.
  - Render or broadcast via WebSockets.

## Next Steps
- Validate the maximum MTU chunk size for the Bebird hardware to optimize `sock.recv()` buffer.
- Implement the `StreamEngine` class incorporating `start()`, `stop()`, and graceful thread shutdown logic.
