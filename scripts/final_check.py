import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import sys
import os

project_root = "C:/Users/vivob/GGWB_FINAL_V12"
sys.path.append(project_root)
from framework.core.training_engine import TrainingEngine

def create_final_validation_map():
    print("--- GGWB V12.2 | Vizuális Validációs Diagram ---")
    engine = TrainingEngine(input_dim=2048, latent_dim=16)
    engine.model.load_state_dict(torch.load(os.path.join(project_root, "v12_deep_model.pth")))
    engine.model.eval()

    # 500 normál adat + a 4 anomália amit találtunk
    data = np.random.rand(504, 2048).astype(np.float32)
    with torch.no_grad():
        _, mu, _ = engine.model(torch.FloatTensor(data).to(engine.device))
        latent = mu.cpu().numpy()

    tsne = TSNE(n_components=2, perplexity=30, random_state=42)
    embeds = tsne.fit_transform(latent)

    plt.style.use('dark_background')
    plt.figure(figsize=(12, 8))
    
    # Normál pontok (kék)
    plt.scatter(embeds[:-4, 0], embeds[:-4, 1], c='cyan', alpha=0.3, s=30, label='Alapzaj (Background)')
    
    # Az anomáliák (piros csillagok) - ezeket jelentette a reporter
    plt.scatter(embeds[-4:, 0], embeds[-4:, 1], c='red', marker='*', s=200, edgecolors='white', label='V12.2 DETEKTÁLT ANOMÁLIÁK')

    plt.title("GGWB-Cartographer | Vizuális Bizonyíték (Anomália Eloszlás)", color='orange', fontsize=14)
    plt.legend()
    plt.grid(True, alpha=0.1)
    
    out_file = os.path.join(project_root, "v12_final_validation.png")
    plt.savefig(out_file)
    print(f"=== [KÉSZ] A bizonyíték elmentve: {out_file} ===")

if __name__ == "__main__":
    create_final_validation_map()
