# Bebird Protocol Reverse Engineering Research

## 1. Objective
Identify the root cause of `Corrupt JPEG data: premature end of data segment` during UDP stream ingestion and determine the exact binary structure of Bebird's UDP packets.

## 2. Research Findings (via High-Skill R&D Agent)
A deep dive into open-source repositories (specifically `haxko/NE3-Scope` and `nananek/qi-earpick-app.py`) reveals that Bebird/QiPower devices do NOT transmit raw JPEG data directly over UDP. 

Instead, the manufacturer implements a **custom 4-byte header** prepended to *every single UDP packet slice*. 

### Packet Structure
| Byte Offset | Name | Description |
|---|---|---|
| `[0]` | `frame_id` | Identifier for the current JPEG frame (0-255). Rolls over. |
| `[1]` | `last_flag` | `0` = intermediate chunk. `>0` = final chunk (contains `EOI`). |
| `[2]` | `chunk_idx` | 1-based index of the current packet slice within the frame. |
| `[3]` | `angle_low` | Lower byte of the built-in gyroscope angle data. |
| `[4:]`| `payload` | The actual MJPEG binary chunk. |

## 3. Root Cause of Previous Failures
The previous implementation used `buffer += data`. By concatenating raw UDP packets directly, the 4-byte headers (`frame_id`, `last_flag`, `chunk_idx`, `angle_low`) were being injected directly into the middle of the JPEG binary stream. 

OpenCV's `cv2.imdecode` encountered these garbage bytes, breaking the JPEG Huffman tables and causing severe tearing (grey bars) and the `premature end of data segment` error.

## 4. Remediation (Implemented in `stream_v2.py`)
- **Packet Stripping:** The `_producer_loop` must strip the first 4 bytes of every UDP packet.
- **Frame Assembly Dictionary:** Chunks must be grouped into a dictionary keyed by `chunk_idx`.
- **Validation:** When `last_flag > 0` is received, the dictionary is concatenated `1` to `N`. Any missing chunks (packet loss) are padded with zeroes to prevent structural shifting before passing to OpenCV.
