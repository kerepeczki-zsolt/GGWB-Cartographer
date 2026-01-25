import numpy as np
import matplotlib.pyplot as plt

class GlitchClassifier:
    def __init__(self):
        # A LIGO leggyakoribb glitch típusainak definíciója (Gravity Spy kategóriák)
        self.glitch_library = {
            "Blip": {"freq_range": (30, 250), "duration": 0.05, "shape": "vertical"},
            "Whistle": {"freq_range": (100, 1000), "duration": 0.5, "shape": "v-shape"},
            "Koi Fish": {"freq_range": (10, 100), "duration": 0.2, "shape": "wide-body"},
            "Scattered Light": {"freq_range": (10, 60), "duration": 2.0, "shape": "arches"}
        }

    def analyze_signal_morphology(self, frequency, duration):
        """
        LIGO-szintű morfológiai elemzés.
        Összeveti a talált jelet az ismert glitch populációkkal.
        """
        potential_matches = []
        for name, traits in self.glitch_library.items():
            if traits["freq_range"][0] <= frequency <= traits["freq_range"][1]:
                if abs(traits["duration"] - duration) < 0.3: # Tolerancia küszöb
                    potential_matches.append(name)
        return potential_matches

def run_glitch_diagnostic():
    print("\n" + "="*70)
    print("   GGWB-CARTOGRAPHER: GLITCH INTELLIGENCE CORE V1.0")
    print("="*70)

    classifier = GlitchClassifier()

    # SZIMULÁCIÓ: Érkezik egy gyanús jel
    obs_freq = 45
    obs_duration = 0.15
    
    print(f"[INPUT] Észlelt jel paraméterei: {obs_freq}Hz, {obs_duration}s")
    
    matches = classifier.analyze_signal_morphology(obs_freq, obs_duration)

    if matches:
        print(f"\n[FIGYELMEZTETÉS] A jel nagy valószínűséggel GLITCH!")
        print(f"Lehetséges kategóriák: {', '.join(matches)}")
        print("Státusz: ELVETVE (Zavaró jel)")
    else:
        print("\n[INFO] A jel nem egyezik ismert glitch mintával.")
        print("Státusz: TOVÁBBI ELEMZÉSRE KÜLDVE (Potenciális GW jel)")

    print("-" * 70)

if __name__ == "__main__":
    run_glitch_diagnostic()