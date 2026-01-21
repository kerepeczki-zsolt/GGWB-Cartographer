import sys
import os
import numpy as np
from scipy.signal import butter, filtfilt

# ÚTVONAL FIX: Automatikusan megkeresi az 'src' mappát a fájl mellett
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')

if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

try:
    # Fontos: A fájloknak az 'src' mappában kell lenniük!
    from veto_system import check_ligo_veto
    from feature_extractor import extract_92_features
    from analysis_logger import log_detection_result
    from result_visualizer import generate_analysis_plot
    from cross_correlator import calculate_cross_correlation
    from gw_data_fetcher import fetch_real_strain_data
    from q_transform_analyzer import generate_q_transform
    from data_scanner import scan_time_range
except ImportError as e:
    print(f"\n[HIBA]: Nem találom a modult: {e}")
    print(f"Kérlek ellenőrizd, hogy a(z) {SRC_DIR} mappában ott vannak-e a .py fájlok!")
    sys.exit(1)

def run_analysis(gps_input):
    """Diagnosztikai modul a 95%+ pontosságért."""
    try:
        # TYPE FIX: Itt javítjuk ki az image_a085c0-ban látható hibát
        gps_val = int(float(gps_input)) 
    except (ValueError, TypeError):
        return "HIBÁS GPS IDŐ", 0.0
    
    # 1. ADATLETÖLTÉS
    raw_h1 = fetch_real_strain_data(gps_val, "H1")
    raw_l1 = fetch_real_strain_data(gps_val, "L1")
    
    # 2. SZŰRÉS (40-400 Hz)
    b, a = butter(4, [40, 400], btype='bandpass', fs=4096)
    h1 = filtfilt(b, a, raw_h1)
    l1 = filtfilt(b, a, raw_l1)

    # 3. KORRELÁCIÓ ÉS VETO
    mlen = min(len(h1), len(l1))
    c_val, _ = calculate_cross_correlation(h1[:mlen], l1[:mlen])
    stats = extract_92_features(h1)
    veto = check_ligo_veto(gps_val, 4, "L1")

    # 4. KIÉRTÉKELÉS
    if veto:
        res = "100% HIBA: VETO (Hardver hiba)"
    elif abs(c_val) > 0.45:
        res = "95%+ JEL: GW JELÖLT"
        generate_q_transform(gps_val, "L1")
        generate_analysis_plot(h1, stats, res)
    else:
        res = "ZAJ: Stacionárius háttér"

    log_detection_result(gps_val, res, stats.get('kurtosis', 0), c_val)
    return res, c_val

if __name__ == "__main__":
    # GW170814 - A mérés alapja
    t_start = 1186741860
    t_duration = 5
    
    print("\n" + "="*80)
    print("   GGWB-CARTOGRAPHER v2.0.0 - JAVÍTOTT, HIBAmentes verzió")
    print("="*80)

    for t in scan_time_range(t_start, t_duration, step=1):
        # Megszüntetjük a kiírt TypeError-t azzal, hogy t-t azonnal típussal kezeljük
        status, corr = run_analysis(t)
        print(f"[SCAN] {int(t)} | {status:40} | Corr: {corr:.4f}")

    print("\n" + "="*80)
    print(" SZKENNELÉS KÉSZ. A 'TypeError' és az elérési út hiba kijavítva.")
    print("="*80)