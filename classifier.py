import torch
import torch.nn as nn
import numpy as np
import os

project_root = "C:/Users/vivob/GGWB_FINAL_V12"

class GlitchClassifier(nn.Module):
    def __init__(self, latent_dim=16, num_classes=4):
        super(GlitchClassifier, self).__init__()
        self.network = nn.Sequential(
            nn.Linear(latent_dim, 32),
            nn.ReLU(),
            nn.Dropout(0.2), # A túltanulás (overfitting) ellen - a pontosság záloga
            nn.Linear(32, num_classes),
            nn.Softmax(dim=1)
        )
        # Osztályok: 0: Alapzaj, 1: Blip, 2: Szórt Fény, 3: GW Jelölt
        self.class_names = ["Background", "Blip Glitch", "Scattered Light", "GW Candidate"]

    def forward(self, x):
        return self.network(x)

def run_classification_test():
    print("=== GGWB V12.3 | Tudományos Osztályozó és Populáció Analízis ===")
    classifier = GlitchClassifier()
    
    # Teszt adat a látens térből (16 dimenzió)
    # Itt szimulálunk egy gyanús eseményt a látens tér koordinátái alapján
    test_latent = torch.randn(1, 16) 
    
    with torch.no_grad():
        probabilities = classifier(test_latent).numpy()[0]
    
    print("\n[ANALÍZIS EREDMÉNYE]:")
    print("-" * 40)
    for i, prob in enumerate(probabilities):
        print(f"{classifier.class_names[i]:<18}: {prob*100:>6.2f}%")
    print("-" * 40)
    
    winner_idx = np.argmax(probabilities)
    print(f"Besorolás: {classifier.class_names[winner_idx]}")
    
    if winner_idx == 3 and probabilities[winner_idx] > 0.95:
        print(">>> RIASZTÁS: Valódi gravitációs hullám jelölt!")
    else:
        print(">>> Státusz: Rutin műszeres esemény vagy zaj.")

if __name__ == "__main__":
    run_classification_test()
