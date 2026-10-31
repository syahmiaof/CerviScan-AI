# Agent Rules & Boundaries

These rules MUST be strictly followed by all sub-agents to maintain workspace integrity and prevent code hallucination.

## 1. Directory Boundaries
Agents may only modify files within their designated module unless authorized by the Master Coordinator Agent.
- `docs/` -> Managed exclusively by **Documentation Agent** (.md files only).
- `src/network/` -> Managed by **IoT & Network Engineer**.
- `src/ai/` -> Managed by **AI & CV Specialist**.
- `src/data_pipeline/` -> Managed by **Data Engineer**.
- `src/backend/` -> Managed by **Full-Stack Developer (FastAPI)**.
- `src/frontend/` -> Managed by **Full-Stack Developer (React)**.
- `tests/` -> Managed by **QA & Tester Agent**.

## 2. Execution Guidelines
- **Offline First:** Do NOT trigger auto-downloads of YOLO models or heavy assets over the UDP Bebird Wi-Fi connection. Always fall back to locally cached models (`yolov8n.pt` / `cerviscan_best.pt`).
- **Immutable Legacy:** Never overwrite the initial working script (`bebird_win.py`) directly. Always use versioned scripts (e.g., `stream_v2.py`) or Git branching.
- **Changelog Requirement:** Every significant code modification or pull request must be appended to `docs/CHANGELOG.md`.
- **Proactive Execution (NEW):** Agents MUST proactively install any required dependencies (e.g., using `pip install` via terminal execution tools) rather than asking the user to manually install them. Eliminate unnecessary manual steps for the user.

## 3. Sub-Agent Roles
1. **Master Coordinator:** Orchestrator, assigns tasks, resolves conflicts.
2. **IoT & Stream Agent:** High-performance video networking (<100ms latency), queue optimization.
3. **AI & CV Specialist:** YOLOv8 inference engine, Digital Green Filter OpenCV algorithms.
4. **Data Engineer:** Dataset curation (Mendeley, Roboflow), YOLO `.txt` formatting, `data.yaml` config, training pipeline.
5. **Full-Stack Developer:** FastAPI WebSockets, React UI, Tailwind, Snapshot management, SQLite patient DB.
6. **Repository Architect:** Linting, directory hygiene, `.gitignore`.
7. **Documentation Agent:** Knowledge manager, keeps context files updated to prevent agent memory loss.
8. **High-Skill R&D Scraper:** Research scraping, API inspection, clinical dataset lookup.
9. **QA & Tester:** FPS benchmarking, latency testing, unit testing.
