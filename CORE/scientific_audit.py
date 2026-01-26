import numpy as np
import sys
import os

# Modulok betöltése
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from whitening_engine import apply_whitening

def run_scientific_audit(iterations=100):
    print("\n" + "="*80)
    print("   GGWB-CARTOGRAPHER - FINOMHANGOLT AUDIT (v2.0)")
    print("="*80)
    
    fs = 4096
    true_positives = 0  
    false_positives = 0 
    true_negatives = 0  
    false_negatives = 0 
    
    for i in range(iterations):
        # 50% esély a jelre
        has_signal = np.random.random() < 0.5
        t = np.linspace(0, 1, fs)
        
        # Alap zaj (visszavettük az intenzitást a reális szintre)
        h1 = np.random.normal(0, 1.0, fs)
        l1 = np.random.normal(0, 1.0, fs)
        
        if has_signal:
            # Reálisabb jel-erősség (Amplitúdó: 1.2)
            f_start, f_end = 40, 350
            chirp = 1.2 * np.sin(2 * np.pi * (f_start * t + (f_end - f_start) * t**2 / 2))
            h1 += chirp
            l1 += chirp
            
        h1_clean = apply_whitening(h1, fs)
        l1_clean = apply_whitening(l1, fs)
        corr = abs(np.corrcoef(h1_clean, l1_clean)[0, 1])
        
        # FINOMHANGOLT KÜSZÖB: 0.12-re állítjuk (ez az arany középút)
        detected = corr > 0.12
        
        if has_signal and detected: true_positives += 1
        if not has_signal and detected: false_positives += 1
        if not has_signal and not detected: true_negatives += 1
        if has_signal and not detected: false_negatives += 1

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    print(f"\n[EREDMÉNYEK - {iterations} tesztből]")
    print(f"  - SIKERES találat: {true_positives}")
    print(f"  - TÉVES riasztás: {false_positives} (Cél: < 5)")
    print(f"  - ELSZALASZTOTT jel: {false_negatives}")
    print(f"\n[STATISZTIKA]")
    print(f"  - MEGBÍZHATÓSÁG: {precision*100:.1f}%")
    print(f"  - ÉRZÉKENYSÉG: {recall*100:.1f}%")
    
    if precision > 0.85 and recall > 0.60:
        print("\n[VERDICT] A RENDSZER VALIDÁLVA ÉS PONTOS!")
    else:
        print("\n[VERDICT] További finomítás javasolt.")
    print("="*80)

if __name__ == "__main__":
    run_scientific_audit()