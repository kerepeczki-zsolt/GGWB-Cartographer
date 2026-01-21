from geometrical_glitch_detector import GeometricalExpertSystem
from visualizer_engine import create_expert_view
import os

def run_comprehensive_campaign():
    expert = GeometricalExpertSystem()
    samples = [
        ("LHO", "O3", 0.2, 110.0, 150.0, "blip.dat", 0.05),
        ("VIRGO", "O3", 0.4, 65.0, 850.0, "whistle.dat", 0.1),
        ("LLO", "O3", 0.1, 5.0, 1080.0, "vibration.dat", 1.0),
        ("VIRGO", "O3", 0.2, 500.0, 500.0, "helix.dat", 0.4),
        ("LLO", "O3", 3.5, 12.0, 45.0, "scattered.dat", 0.8)
    ]
    
    for inst, run, w, h, f, fname, tilt in samples:
        diag = expert.analyze_modification(inst, run, w, h, f, tilt)
        create_expert_view(fname, inst, diag, f, tilt, "GRAVITY_SPY")
        create_expert_view(fname, inst, diag, f, tilt, "DETCHAR")
        print(f"KÉSZ: {fname} -> {diag}")

if __name__ == "__main__":
    run_comprehensive_campaign()