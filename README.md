<div align="center">
  <h1>CerviScan-AI</h1>
  <p><strong>Computer vision research prototype for assisted cervical sample review.</strong></p>
  <p><a href="https://cerviscan-ai.syahmiaof.my">Open prototype</a> · <a href="https://syahmiaof.my/projects">Portfolio context</a></p>
</div>

![CerviScan-AI dashboard prototype](https://raw.githubusercontent.com/syahmiaof/syahmiaof/main/public/images/cerviscan-dashboard.webp)

> Research prototype in active development. The public dashboard uses demonstration data and is not a clinically validated diagnostic device.

## Project context

CerviScan-AI is a team project exploring an IoT-enabled imaging workflow for cervical screening research. The current software prototype focuses on receiving a video or image stream, supporting computer-vision analysis and presenting review information through a CMS-style dashboard.

## My role

I build:

- the CMS and review dashboard;
- the video-streaming application;
- the YOLOv8 integration path for sample analysis;
- the frontend workflow used to inspect and organise results.

Clinical research, hardware development and broader project decisions involve the project team.

## Current workflow

~~~text
Imaging source → Video stream → Frame processing → YOLOv8 analysis → Review dashboard
~~~

## Stack

| Area | Technology |
|---|---|
| Interface | React 19, TypeScript, Vite |
| Visualisation | Recharts, TanStack Table |
| Computer vision | YOLOv8 integration |
| Service layer | Node.js, Express |
| Deployment | Vercel |

## Local development

~~~bash
npm install
npm run dev
~~~

Use the repository environment example for service configuration. API keys belong in local or deployment environment variables and must not be committed.

## Current limitations

- The dashboard contains mock or demonstration records.
- Model performance, sensitivity and specificity have not been established by this repository.
- Regulatory, privacy, security and clinical validation work remains outside the current prototype.
- Output must be reviewed by qualified professionals and must not replace histopathology, biopsy or clinical judgment.

## Status

Active team development. The repository demonstrates application and integration work; it does not claim medical certification or diagnostic approval.

## Builder

[Muhammad Syahmi](https://syahmiaof.my) — CMS dashboard, video stream and AI integration.
