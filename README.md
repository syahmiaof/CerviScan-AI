<div align="center">
  <h1>CerviScan-AI</h1>
  <p><strong>Computer vision research prototype for assisted cervical sample review.</strong></p>

  <p>
    <a href="https://cerviscan-ai.syahmiaof.my"><img src="https://img.shields.io/badge/Demo-Live-60E1B5?style=for-the-badge&logoColor=60E1B5&labelColor=101713" alt="Demo Live" /></a>
    <a href="https://github.com/syahmiaof/CerviScan-AI"><img src="https://img.shields.io/badge/Source-GitHub-60E1B5?style=for-the-badge&logo=github&logoColor=60E1B5&labelColor=101713" alt="GitHub Source" /></a>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-60E1B5?style=for-the-badge&logoColor=60E1B5&labelColor=101713" alt="License MIT" /></a>
    <a href="https://syahmiaof.my"><img src="https://img.shields.io/badge/Author-syahmiaof-60E1B5?style=for-the-badge&logo=readme&logoColor=60E1B5&labelColor=101713" alt="Author syahmiaof" /></a>
  </p>
</div>

![CerviScan-AI dashboard prototype](https://raw.githubusercontent.com/syahmiaof/syahmiaof/main/public/images/cerviscan-dashboard.webp)

> **Research Prototype Disclaimer**: This project is a research prototype in active development. The public dashboard operates on demonstration data and is **not** a clinically validated medical diagnostic device. Output must be evaluated by certified professionals and cannot replace histopathology or clinician judgment.

---

## Project Context

CerviScan-AI is a collaborative team project investigating an IoT-enabled imaging and analytical workflow for cervical screening research. The software application focuses on acquiring an imaging/video stream, running computer-vision inference (YOLOv8) for cell sample assessment, and presenting structured review data through an intuitive CMS dashboard.

## Technical Scope & Authorship

**Muhammad Syahmi (syahmiaof)** architected and implemented:
- **CMS & Review Dashboard**: Interactive React 19 UI with TanStack Table and Recharts data visualizations.
- **Stream Ingestion & Processing**: Endoscope video stream ingestion service and frame handling.
- **YOLOv8 Inference Pipeline**: Computer vision model integration and result parsing.
- **Review Workflow**: Multi-criteria filtering, annotation history, and patient review management.

*Clinical methodology, physical hardware prototyping, and dataset collation are managed collaboratively with the research team.*

---

## Architecture Flow

```text
Imaging Source (Bebird / Digital Endoscope)
       │
       ▼
  Video Stream (UDP / RTSP / MJPEG)
       │
       ▼
Frame Pre-processing & Green Filter
       │
       ▼
 YOLOv8 Deep Learning Inference
       │
       ▼
Interactive Clinical Review Dashboard (React 19 + Express)
```

---

## Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend Framework** | React 19, TypeScript, Vite 8 |
| **Styling & Animation** | Tailwind CSS v4, Motion, Lucide React |
| **Data & Tables** | TanStack React Table v8, Recharts |
| **Service & API** | Node.js, Express, `@google/genai` |
| **Computer Vision** | YOLOv8 (Ultralytics), Python, OpenCV |
| **Deployment & CI** | Vercel, GitHub Actions |

---

## Getting Started

### Prerequisites
- Node.js 20+
- Python 3.10+ (for stream/inference workers)

### Installation & Run

```bash
# Clone the repository
git clone https://github.com/syahmiaof/CerviScan-AI.git
cd CerviScan-AI

# Install dependencies
npm install

# Run typecheck and lint
npm run lint

# Build production bundle
npm run build

# Start local development server
npm run dev
```

---

## Verification & Quality

- **Lint / Typecheck**: `npm run lint` (`tsc --noEmit`)
- **Production Build**: `npm run build` (`vite build`)
- **Automated CI**: GitHub Actions workflow verifies linting and build on every push and PR to `main`.

---

## Limitations & Compliance

- The dashboard contains demonstration records for interface verification.
- Model sensitivity and clinical validation metrics are subject to continuing institutional research.
- Regulatory and clinical clearance processes remain outside the scope of this repository.

---

## License

This project is open-source under the [MIT License](LICENSE).
(c) 2026 Muhammad Syahmi ([syahmiaof](https://syahmiaof.my)).
