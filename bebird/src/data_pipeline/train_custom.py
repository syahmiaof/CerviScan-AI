import os
import argparse
import shutil
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--epochs', type=int, default=10, help='number of epochs')
    parser.add_argument('--imgsz', type=int, default=416, help='image size')
    args = parser.parse_args()

    print("[Data Engineer] 🚀 Initializing Custom Training Pipeline for CerviScan-AI...")
    
    # Resolve absolute path to data.yaml
    base_dir = os.path.dirname(os.path.abspath(__file__))
    data_yaml_path = os.path.join(base_dir, 'data.yaml')

    print("[AI Agent] Loading base model weights: yolov8n.pt")
    model = YOLO('yolov8n.pt') 
    
    print(f"[AI Agent] Starting Transfer Learning on Real Dataset (Epochs: {args.epochs}, Image Size: {args.imgsz})...")
    
    results = model.train(
        data=data_yaml_path,
        epochs=args.epochs,
        imgsz=args.imgsz,
        batch=16,
        device='cpu',
        project=os.path.join(base_dir, 'cerviscan_training'),
        name='run_cric_real'
    )
    
    # Copy best weights to src/ai/
    best_weights = os.path.join(base_dir, 'cerviscan_training', 'run_cric_real', 'weights', 'best.pt')
    target_weights = os.path.join(base_dir, '..', 'ai', 'cerviscan_best.pt')
    
    os.makedirs(os.path.dirname(target_weights), exist_ok=True)
    if os.path.exists(best_weights):
        shutil.copy(best_weights, target_weights)
        print("\n[Data Engineer] ✅ Training Complete!")
        print(f"[AI Agent] Best weights saved to: {target_weights}")
    else:
        print("\n[WARN] Training completed but best.pt not found.")

if __name__ == '__main__':
    main()
