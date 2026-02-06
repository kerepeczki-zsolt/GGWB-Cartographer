import numpy as np
import os
import time
from master_processor import GGWB_Universal_Validator

class FullGlitchFactory:
    def __init__(self, fs=4096):
        self.fs = fs
        self.t = np.linspace(0, 1, fs)

    def generate(self, g_type):
        data = np.random.normal(0, 0.5, self.fs)
        # Itt definiáljuk a 22 típust (példa a legfontosabbakra, a többi zaj)
        if g_type == "Blip": data[2000:2050] += 60 * np.exp(-((np.arange(50)-25)**2)/5)
        elif g_type == "Violin_Mode": data += 20 * np.sin(2 * np.pi * 500 * self.t)
        elif g_type == "Power_Line": data += 15 * np.sin(2 * np.pi * 60 * self.t)
        elif g_type == "Whistle": data += 10 * np.sin(2 * np.pi * 1200 * self.t)
        elif g_type == "Low_Frequency_Burst": data += 25 * np.sin(2 * np.pi * 20 * self.t)
        elif g_type == "CANDIDATE_GW":
            chirp_t = np.linspace(0, 0.5, 2048)
            data[1000:1000+2048] += 30 * np.sin(2 * np.pi * (40 + 160 * chirp_t**2))
        elif g_type == "Light_Modulation": data += 5 * np.sin(2 * np.pi * 0.5 * self.t)
        elif g_type == "Air_Compressor": data += 12 * np.sin(2 * np.pi * 50 * self.t)
        # A maradék típusokat "Ismeretlen hiba"ként vagy alapzajként kezeljük
        else: data += np.random.normal(0, 0.2, self.fs)
        return data

def run_22_population_test():
    validator = GGWB_Universal_Validator()
    factory = FullGlitchFactory()
    
    # A teljes 22-es lista a LIGO szakirodalom alapján
    all_22 = [
        "Blip", "Violin_Mode", "Power_Line", "Whistle", "Low_Frequency_Burst", 
        "CANDIDATE_GW", "Light_Modulation", "Air_Compressor", "Helix", "Koi_Fish", 
        "Paired_Doves", "Repeating_Blips", "Scattered_Light", "Scratchy", "Tomte", 
        "Wandering_Line", "None_of_the_Above", "Chirp", "Extremely_Loud", 
        "1080Lines", "1400Ripples", "No_Glitch"
    ]
    
    print("\n" + "="*70)
    print("   GGWB V18.5 | TELJES 22 POPULÁCIÓS STRESSZ-TESZT (50 TESZT/TÍPUS)")
    print("="*70)
    
    for cat in all_22:
        hits = 0
        for _ in range(50):
            sample = factory.generate(cat)
            res, conf, freq = validator.deep_scan(sample, 0)
            if res == cat:
                hits += 1
        acc = (hits / 50) * 100
        print(f"{cat:<25} | Találat: {hits:2d}/50 | Pontosság: {acc:>5.1f}%")

if __name__ == "__main__":
    run_22_population_test()
