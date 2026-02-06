import os
import sys
import numpy as np
import torch
import glob

project_root = "C:/Users/vivob/GGWB_FINAL_V12"
sys.path.append(project_root)

from framework.core.training_engine import TrainingEngine

def normalize_data(data):
    # Min-Max normalizáció: minden mintát [0, 1] tartományba teszünk
    # Így a morfológia (alak) fog számítani, nem az amplitúdó
    d_min = data.min(axis=1, keepdims=True)
    d_max = data.max(axis=1, keepdims=True)
    return (data - d_min) / (d_max - d_min + 1e-8)

def run_v12_deep_training():
    print("=== GGWB-Cartographer V12.2 | MÉLYTRÉNING ÉS NORMALIZÁCIÓ ===")
    data_folder = "C:/Users/vivob/GGWB_FINAL_V12/data"
    
    # 1. Adatok betöltése és tisztítása
    files = glob.glob(os.path.join(data_folder, "*.npy")) + glob.glob(os.path.join(data_folder, "*.csv"))
    
    if files:
        raw_data = np.load(files[0]) if files[0].endswith('.npy') else np.genfromtxt(files[0], delimiter=',')
        if raw_data.ndim == 1: raw_data = raw_data.reshape(1, -1)
        # Ha túl kevés az adat, duplikáljuk a tréninghez
        if len(raw_data) < 100:
            raw_data = np.tile(raw_data, (128 // len(raw_data) + 1, 1))
        
        processed_data = normalize_data(raw_data[:256, :2048])
        print(f"[INFO] {len(processed_data)} minta normalizálva és készen áll.")
    else:
        print("[!] Nincs valódi adat, szimulált struktúrával dolgozunk...")
        processed_data = np.random.rand(256, 2048).astype(np.float32)

    # 2. Motor indítása
    engine = TrainingEngine(input_dim=2048, latent_dim=16, beta=4.0)
    
    # 3. 100 Epochos tréning
    print("[PROCESS] Tréning indítása: 100 epoch...")
    for epoch in range(1, 101):
        loss = engine.train_step(processed_data)
        if epoch % 10 == 0:
            print(f"Epoch {epoch:03d}/100 | Konszolidált Loss: {loss:.4f}")

    # Mentés a vizualizációhoz
    torch.save(engine.model.state_dict(), os.path.join(project_root, "v12_deep_model.pth"))
    print("=== [SIKER] A mélytréning lezárult, a modell elmentve. ===")

if __name__ == '__main__':
    run_v12_deep_training()
