# CerviScan-AI: Project Context & Status

## Project Scope
Medical-grade IoT digital speculum prototype for cervical cancer screening (Pap smear / Colposcopy) with Clinical Decision Support System (CDSS) capabilities.

## Hardware & Optics Specifications
- **Camera Module:** Micro otoscope camera (3.9mm lens, 1080p, 6x adjustable LEDs, IP67 waterproof).
- **Compute Unit:** ESP32-S3 (16MB Flash, 8MB PSRAM) microcontroller.
- **Power:** TP4056 + 500mAh Li-Po battery.
- **Optics Housing:** 3D SLA printed snap-fit modular housing featuring cross-polarization linear filters (0° on LED, 90° on lens) to remove 90% mucosa glare.

## Progress Tracking
### Sprint 1 (Completed)
- Bebird R1 camera network parameters reverse engineered: Gateway IP `192.168.5.1`, Control Port `58080` (UDP).
- UDP Session trigger sequences mapped: `b'\x20\x36'` (Start Stream), `b'\x20\x37'` (Stop Stream).
- Networking isolated on Windows Native environment to bypass WSL2/NAT isolation limitations, accessing Wi-Fi adapter socket directly.
- Developed initial single-threaded frame reassembly script (`bebird_win.py`) relying on JPEG hex boundaries (`\xff\xd8` to `\xff\xd9`).

### Sprint 3 (In Progress)
- **Current Milestone:** default YOLOv8 (`yolov8n.pt`) successfully integrated into OpenCV loop.
- **Issue Detected:** Model mismatch. Default COCO classes are misidentifying close-up macro biological structures as general non-biological objects.
- **Pivot Action:** Transition to Multi-Agent System (Antigravity IDE) for production-grade multi-threaded architecture, custom dataset processing, and building the full-stack clinical dashboard.
