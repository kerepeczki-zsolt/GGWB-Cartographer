import torch
import numpy as np
import os
import sys

project_root = "C:/Users/vivob/GGWB_FINAL_V12"
sys.path.append(project_root)
from framework.core.training_engine import TrainingEngine

def run_anomaly_report():
    print("=== GGWB-Cartographer V12.2 | Automatikus Anomália Jelentés ===")
    engine = TrainingEngine(input_dim=2048, latent_dim=16)
    
    # Modell betöltése
    model_path = os.path.join(project_root, "v12_deep_model.pth")
    if not os.path.exists(model_path):
        print("[HIBA] Nem találom a mélytréning modellt!")
        return
    engine.model.load_state_dict(torch.load(model_path))
    engine.model.eval()

    # Szimulálunk egy friss mérési sorozatot (vagy tölthetnénk a data-ból)
    test_data = np.random.rand(100, 2048).astype(np.float32)
    
    with torch.no_grad():
        recon, mu, logvar = engine.model(torch.FloatTensor(test_data).to(engine.device))
        
        # Kiszámoljuk a rekonstrukciós hibát (MSE)
        # Aki nem hasonlít önmagára a kicsomagolás után, az az anomália!
        recon_error = torch.mean((recon - torch.FloatTensor(test_data).to(engine.device))**2, dim=1).cpu().numpy()

    # A 5 legmagasabb hibájú (legfurcsább) esemény
    top_anomalies = np.argsort(recon_error)[-5:]
    
    print("\n[EREDMÉNYEK] A 5 legkülönösebb morfológiai esemény:")
    print("-" * 50)
    for idx in top_anomalies:
        print(f"ID: {idx:03d} | Anomália Index: {recon_error[idx]:.6f} | Állapot: GYANÚS")
    print("-" * 50)
    print("=== Jelentés elkészült. ===")

if __name__ == "__main__":
    run_anomaly_report()
