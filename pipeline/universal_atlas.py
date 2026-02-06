import torch
import torch.nn as nn
import numpy as np
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

class UniversalLIGODetector(nn.Module):
    def __init__(self):
        super(UniversalLIGODetector, self).__init__()
        # A teljes, 22 elemű hivatalos lista
        self.all_classes = [
            "Air_Compressor", "1400_Ripple", "1080_Line", "Blip", "Chirp", 
            "Extremely_Loud", "Helix", "Koi_Fish", "Low_Frequency_Burst", 
            "Low_Frequency_Lines", "No_Glitch", "None_of_the_Above", 
            "Paired_Doves", "Power_Line", "Repeating_Blips", "Scattered_Light", 
            "Scratchy", "Tomte", "Violin_Mode", "Wandering_Line", "Whistle",
            "CANDIDATE_GW"
        ]
        
        # Szigorúbb, mélyebb hálózat a 22 osztály szétválasztásához
        self.network = nn.Sequential(
            nn.Linear(16, 512),
            nn.LeakyReLU(0.2),
            nn.Dropout(0.4),
            nn.Linear(512, 256),
            nn.LeakyReLU(0.2),
            nn.Linear(256, len(self.all_classes)),
            nn.Softmax(dim=1)
        )

    def run_full_diagnosis(self, latent_input):
        with torch.no_grad():
            output = self.network(torch.tensor(latent_input).float())
            probs = output.numpy()[0]
            results = {self.all_classes[i]: probs[i] for i in range(len(self.all_classes))}
            return sorted(results.items(), key=lambda x: x[1], reverse=True)

if __name__ == "__main__":
    detector = UniversalLIGODetector()
    print(f"--- GGWB V12.5 | UNIVERZÁLIS DIAGNOSZTIKAI ATLASZ ---")
    print(f"Monitorozott populációk száma: {len(detector.all_classes)}")
    
    # Teszt: elemezzük a legutóbbi anomáliát (ID 27)
    # Most szimulált látens vektorral, de a cél a valós VAE kimenet
    test_latent = np.random.randn(1, 16)
    diagnosis = detector.run_full_diagnosis(test_latent)
    
    print("\n[TELJES OSZTÁLYOZÁSI LISTA - TOP TALÁLATOK]:")
    print("-" * 50)
    for name, prob in diagnosis:
        if prob > 0.001: # Csak ami fizikailag is értelmezhető
            indicator = ">>>" if prob > 0.2 else "   "
            print(f"{indicator} {name:<25}: {prob*100:>6.2f}%")
    print("-" * 50)
