# 🔬 CerviScan-AI: Smart Wireless Digital Speculum with Computer Vision

<div align="center">

![CerviScan-AI Banner](https://img.shields.io/badge/Status-Active%20Development-success?style=for-the-badge)
![Tech Stack](https://img.shields.io/badge/Frontend-React%2019%20%7C%20TypeScript%20%7C%20Vite-blue?style=for-the-badge)
![AI Engine](https://img.shields.io/badge/AI-Google%20Gen%20AI%20%7C%20Gemini-orange?style=for-the-badge)
![UI / UX](https://img.shields.io/badge/Styling-Tailwind%20CSS%20v4%20%7C%20Motion-purple?style=for-the-badge)

<p align="center">
  <strong>IoT-Enabled Wireless Digital Speculum & Real-Time Cervical Lesion Computer Vision Screener</strong>
</p>

</div>

---

## 📌 Executive Overview

**CerviScan-AI** is an advanced medical-technology screening tool integrating an IoT-enabled smart wireless digital speculum with multimodal computer vision. Designed to enhance cervical cancer pre-screening, it empowers healthcare practitioners with real-time lesion visual analysis, automated risk classification, and clinical-grade reporting directly from point-of-care environments.

By marrying localized imaging hardware with real-time AI multimodal reasoning (powered by Google Gemini Vision), CerviScan-AI bridges critical diagnostic gaps in community clinics and resource-limited medical centers.

---

## 🚀 Key Innovations & Features

- 📷 **Wireless Point-of-Care Imaging:** Integrates seamless wireless camera streaming from specialized optical speculum hardware into an encrypted clinical dashboard.
- 🧠 **Computer Vision Lesion Detection:** Real-time visual inspection analyzing transformation zones, acetowhite changes, and vascular abnormalities.
- 📊 **Multimodal Risk Stratification:** Instant diagnostic inference categorizing lesions (Normal, Low-Grade, High-Grade, Suspected Malignancy) with structured clinical confidence metrics.
- ⚡ **Interactive Clinical Dashboard:** Built with React 19, Recharts data analytics, and TanStack Table for efficient patient consultation and longitudinal tracking.
- 📑 **One-Click Diagnostic Reports:** Automated generation of structured pre-screening summaries, ready for referral workflows or electronic health record (EHR) integration.

---

## 🛠️ Architecture & Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Frontend Framework** | React 19, TypeScript, Vite 8, Bun |
| **UI Components & Styling** | Tailwind CSS v4, Motion (Framer Motion), Lucide Icons |
| **Data Analytics & Tables** | Recharts, TanStack React Table |
| **Artificial Intelligence** | `@google/genai` (Google Gemini Multimodal Vision API) |
| **Backend & Routing** | Express.js, Node.js, Vercel Serverless Hosting |

---

## 💻 Local Setup & Development

Follow these steps to run the CerviScan-AI diagnostic console locally:

### 1. Prerequisites
- **Node.js** >= 20.x or **Bun** installed
- A valid **Gemini API Key** from [Google AI Studio](https://aistudio.google.com/)

### 2. Clone the Repository
```bash
git clone https://github.com/syahmiaof/CerviScan-AI.git
cd CerviScan-AI
```

### 3. Install Dependencies
```bash
npm install
# or if using bun
bun install
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory:
```env
GEMINI_API_KEY=your_gemini_api_key_here
PORT=3000
```

### 5. Start Development Server
```bash
npm run dev
```
Visit `http://localhost:3000` in your browser to access the CerviScan-AI clinical interface.

---

## 🏥 Clinical Disclaimer & Ethics

> [!IMPORTANT]
> **CerviScan-AI is designed as an assistive diagnostic screening tool (Pre-screening / Decision Support)** and is intended to be used under the supervision of qualified medical professionals. It does not substitute histopathological examination, biopsy, or certified medical judgment.

---

## 👨‍💻 Author & Maintainer

**Muhammad Syahmi (syahmiaof)**  
*Cloud, DevOps & Medical-Tech Systems Developer*  
- 🌐 Website: [syahmiaof.my](https://syahmiaof.my)  
- 🐙 GitHub: [@syahmiaof](https://github.com/syahmiaof)  
- ✉️ Email: [syahmiaof123@gmail.com](mailto:syahmiaof123@gmail.com)
