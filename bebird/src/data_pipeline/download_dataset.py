import os
import shutil
from roboflow import Roboflow

# Base paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

def download_real_roboflow_dataset():
    print("[R&D Agent] Wiping old synthetic data and initializing Roboflow pull...")
    if os.path.exists(DATASET_DIR):
        shutil.rmtree(DATASET_DIR)
        
    print("[Data Engineer] Downloading real CRIC Colposcopy dataset from Roboflow Universe...")
    
    # Real Colposcopy/Cervical Cytology Dataset (CRIC Full Dataset)
    # Target: cervical-cancer-tullf / cric-full-dataset (Version 7 supports YOLOv8)
    rf = Roboflow(api_key="AfJSLPYTpmZrNl3g1c1e")
    project = rf.workspace("cervical-cancer-tullf").project("cric-full-dataset")
    version = project.version(7)
    
    # Download directly into YOLOv8 format
    dataset = version.download("yolov8", location=DATASET_DIR)
    print(f"[Data Engineer] Real dataset successfully downloaded to: {dataset.location}")

if __name__ == '__main__':
    download_real_roboflow_dataset()
