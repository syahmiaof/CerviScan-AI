# CerviScan-AI Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
### Added (Data Pipeline & Real Clinical Dataset)
- **Roboflow CRIC Full Dataset Ingestion:** Upgraded `download_dataset.py` to utilize the `roboflow` SDK to pull the "CRIC Full Dataset" (2000+ images) directly from Roboflow Universe using an authorized API key.
- **Bethesda System Classes:** Updated `data.yaml` to dynamically reflect standard Bethesda classification annotations: `NILM`, `ASC-US`, `ASC-H`, `LSIL`, `HSIL`, and `SCC`.
- **Automated Weight Export:** `train_custom.py` now automatically routes the final `best.pt` file into `src/ai/cerviscan_best.pt` for seamless loading by the live inference engine.

### Added (Digital Green Filter Engine)
- **Clinical DGF Mode (`green_filter.py`):** Added a Digital Green Filter (DGF) module utilizing OpenCV's CLAHE.
- **Hotkey Integration:** Real-time toggling of DGF in `stream_v2.py` via the `'g'` key to instantly enhance micro-vasculature contrast during colposcopy.

### Added (Native Parity Experience)
- **Dynamic Frame Orientation Engine:** Integrated a software rotation module utilizing `cv2.rotate()`. The display HUD now tracks physical hardware gyro angles (`byte [3]`) extracted from the UDP packet headers. Clinicians can hot-toggle rotation (0°, 90°, 180°, 270°) instantly by pressing the `'r'` key.
- **Ring Buffer Renderer (Zero-Latency):** Replaced static variables with a thread-safe `collections.deque(maxlen=1)` Single-Element Ring Buffer. The display thread now directly pulls the absolute latest pre-decoded frame array without holding mutex locks, fully eliminating Windows GDI micro-stuttering and achieving parity with the native app's smoothness.

### Fixed (PyTurboJPEG DLL Hotfix)
- **RuntimeError Handling (DLL Missing):** Added a graceful fallback mechanism in `stream_v2.py` for PyTurboJPEG. Since `pip install PyTurboJPEG` does not bundle the native `turbojpeg.dll` on Windows by default, the script will now safely trap the `RuntimeError` during instantiation and seamlessly fall back to OpenCV's optimized `cv2.imdecode` decoder without crashing the application.

### Performance Enhancements (Native Smoothness Update)
- **PyTurboJPEG Integration (Hardware SIMD):** Replaced `cv2.imdecode` with `PyTurboJPEG` decoder (where DLL is available). 
- **Zero-Latency Display Loop:** Upgraded the main thread `cv2.waitKey(33)` limit to `cv2.waitKey(1) & 0xFF`.

### Fixed (JPEG Data Sanitization)
- **Extraneous Padding Byte Removal:** Fixed the persistent `1 extraneous bytes before marker 0xd9` OpenCV/TurboJPEG warning. The Bebird hardware injects a rogue `0x00` byte precisely before the `\xff\xd9` EOI marker. Added strict slice validation to strip this exact byte, silencing terminal warnings and enabling flawless decoding via OpenCV fallback.

### Fixed (R&D Reverse Engineering Breakthrough)
- **ROOT CAUSE RESOLVED (Corrupt JPEG & Screen Tearing):** Discovered via R&D Agent that Bebird UDP streams use a **4-byte header**. Completely rewrote packet assembly to cleanly strip and stitch payloads.
