# System Architecture

## Overview
CerviScan-AI employs a Hybrid Client-Edge model. Peripherals handle the image capture and video streaming, while the host device (laptop/tablet) acts as the Edge AI node executing real-time object detection and serving the clinical UI.

## Tech Stack
- **Firmware/IoT:** C++ (ESP-IDF / Arduino) on ESP32-S3.
- **Networking:** UDP Socket Stream (Port 58080).
- **Backend & AI Engine:** Python 3.10+, Ultralytics YOLOv8, OpenCV, NumPy, FastAPI.
- **Frontend / Clinical UI:** React.js + Tailwind CSS.

## Data Flow (Draft)
1. **Peripheral Node (ESP32-S3 + Bebird Camera):**
   - Initializes AP mode.
   - Waits for stream trigger payload (`0x20 0x36`) on UDP 58080.
   - Streams raw JPEG packets.
2. **Network Ingestion Engine (`src/network`):**
   - High-throughput UDP Socket listener.
   - Reassembles payloads into complete JPEG frames.
   - Pushes frames to a fast `queue.Queue` (Producer).
3. **AI & CV Pipeline (`src/ai`):**
   - Polls `queue.Queue` (Consumer).
   - Applies Digital Green Filter (matrix color manipulation).
   - Runs YOLOv8 inference for bounding box annotation.
   - Publishes processed frames to WebSockets/FastAPI.
4. **Clinical Dashboard (`src/frontend` & `src/backend`):**
   - Displays real-time live feed (annotated).
   - Controls digital filter overlays, captures snapshots.
   - Stores diagnostics in SQLite patient database.
