import numpy as np
import sys
import os

# Útvonalak beállítása
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from whitening_engine import apply_whitening
    from sky_locator import calculate_sky_position
    from feature_extractor import extract_92_features
    from signal_classifier import classify_signal
    print("[SYSTEM] GGWB-CARTOGRAPHER v8.0.0 PRO - Minden modul szinkronizálva.")
except ImportError as e:
    print(f"[ERROR] Importálási hiba: {e}")
    sys.exit()

def run_full_detection(raw_h1, raw_l1, fs):
    print("\n" + "="*85)
    print("   GGWB-CARTOGRAPHER v8.0.0 PRO - TELJES ANALÍZIS FOLYAMAT")
    print("="*85)

    # 1. Whitening (Tisztítás)
    clean_h1 = apply_whitening(raw_h1, fs)
    clean_l1 = apply_whitening(raw_l1, fs)
    
    # 2. Feature Extraction (92 paraméter)
    features, ci = extract_92_features(clean_h1)
    
    # 3. Korreláció (Precíziós mérés)
    correlation = abs(np.corrcoef(clean_h1, clean_l1)[0, 1])
    print(f"[METRIKA] Koherencia: {correlation:.10f} | Bizalmi Index: {ci:.2f}%")

    # 4. Osztályozás (A frissített logika)
    status, category = classify_signal(clean_h1, correlation, ci)
    print(f"[STÁTUSZ] Besorolás: {status} ({category})")

    # 5. Lokalizáció (Ha a jel érvényes)
    if "GW" in status:
        pos = calculate_sky_position(7.12)
        print(f"[LOKALIZÁCIÓ] {pos}")
    
    print("\n" + "="*85)

if __name__ == "__main__":
    fs = 4096
    t = np.linspace(0, 1.0, fs)
    # Teszt chirp jel szimulálása (növekvő amplitúdó)
    signal = t * np.sin(2 * np.pi * (100 + 50 * t) * t) 
    raw_h1 = signal + np.random.normal(0, 0.5, fs)
    raw_l1 = signal + np.random.normal(0, 0.5, fs)
    run_full_detection(raw_h1, raw_l1, fs)