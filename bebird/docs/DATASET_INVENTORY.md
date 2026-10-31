# Dataset Inventory: CerviScan-AI

## Overview
This document logs the current dataset used for training the YOLOv8 cervical lesion detection model. The dataset is ingested from Roboflow Universe using the `download_dataset.py` pipeline.

## Ingestion Details
- **Method:** Autonomous Roboflow SDK Pull (Zero-User-Intervention)
- **Source:** Roboflow Universe (`cervical-cancer-tullf / cric-full-dataset`, Version 7)
- **Total Images:** 2,076
- **Format:** YOLOv8

## Class Distribution (The Bethesda System)
- `NILM` (Negative for Intraepithelial Lesion or Malignancy) - 6,830 instances
- `ASC-US` (Atypical Squamous Cells of Undetermined Significance) - 598 instances
- `ASC-H` (Atypical Squamous Cells, cannot exclude HSIL) - 902 instances
- `LSIL` (Low-Grade Squamous Intraepithelial Lesion) - 1,327 instances
- `HSIL` (High-Grade Squamous Intraepithelial Lesion) - 1,787 instances
- `SCC` (Squamous Cell Carcinoma) - 155 instances

## Data Split
- **Train:** 88%
- **Validation:** 8%
- **Test:** 4%

## Pipeline Integration
- Weights from training on this dataset are saved to `src/ai/cerviscan_best.pt` for direct loading into the `stream_v2.py` asynchronous AI worker.
