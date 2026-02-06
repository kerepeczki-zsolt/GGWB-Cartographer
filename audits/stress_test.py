import numpy as np
import os
import time

# Itt hívjuk meg az ÚJ nevén a validátort
from master_processor import GGWB_Universal_Validator

class GlitchFactory:
    def __init__(self, fs=4096):
        self.fs = fs
        self.t = np.linspace(0, 1, fs)

    def generate(self, glitch_type):
        data = np.random.normal(0, 0.5, self.fs)
        if glitch_type == "Blip":
            data[2000:2050] += 60 * np.exp(-((np.arange(50)-25)**2)/5)
        elif glitch_type == "Violin_Mode":
            data += 20 * np.sin(2 * np.pi * 500 * self.t)
        elif glitch_type == "Power_Line":
            data += 15 * np.sin(2 * np.pi * 60 * self.t)
        elif glitch_type == "Whistle":
            data += 10 * np.sin(2 * np.pi * 1200 * self.t)
        elif glitch_type == "Low_Frequency_Burst":
            data += 25 * np.sin(2 * np.pi * 20 * self.t)
        elif glitch_type == "CANDIDATE_GW":
            chirp_t = np.linspace(0, 0.5, 2048)
            chirp = 30 * np.sin(2 * np.pi * (40 + 160 * chirp_t**2))
            data[1000:1000+len(chirp)] += chirp
        return data

def run_synchronized_test():
    validator = GGWB_Universal_Validator()
    factory = GlitchFactory()
    categories = ["Blip", "Violin_Mode", "Power_Line", "Whistle", "Low_Frequency_Burst", "CANDIDATE_GW"]
    
    print("\n" + "="*60)
    print("   GGWB V17.6 | SZINKRONIZÁLT MULTI-TESZT")
    print("="*60)
    
    for cat in categories:
        hits = 0
        for _ in range(50):
            sample = factory.generate(cat)
            res, conf, freq = validator.deep_scan(sample, 0)
            if res == cat:
                hits += 1
        acc = (hits / 50) * 100
        print(f"{cat:<20} | Pontosság: {acc:>5.1f}%")

if __name__ == "__main__":
    run_synchronized_test()
