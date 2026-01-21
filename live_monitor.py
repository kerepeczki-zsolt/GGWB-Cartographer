import time
import sys
import os
import numpy as np
import csv

# Modul elérési utak beállítása
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

try:
    from data_streamer import generate_live_chunk
    from whitening_engine import apply_whitening
    from sky_locator import calculate_sky_position
    from signal_classifier import classify_signal # Most már be tudja tölteni!
except ImportError as e:
    print(f"[HIBA] Nem sikerült betölteni a modult: {e}")
    sys.exit()

def log_event(id, corr, pos, label):
    file_exists = os.path.isfile('detections.csv')
    with open('detections.csv', mode='a', newline='', encoding='cp1252') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Timestamp', 'Event_ID', 'Correlation_R', 'Sky_Position', 'Signal_Type'])
        
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), id, f"{corr:.4f}", pos, label])

def run_mission():
    print("\n" + "="*80)
    print("   GGWB-CARTOGRAPHER v13.2.0 - INTELLIGENS HIBAOSZTÁLYOZÁS")
    print("="*80)
    
    gw_count = 0
    glitch_count = 0
    
    try:
        while True:
            h1, l1 = generate_live_chunk()
            h1_c = apply_whitening(h1, 4096)
            l1_c = apply_whitening(l1, 4096)
            
            corr = abs(np.corrcoef(h1_c, l1_c)[0, 1])
            
            if corr > 0.15:
                # Azonosítjuk, hogy mi ez
                stype = classify_signal(h1_c, 4096)
                t_str = time.strftime("%H:%M:%S")
                
                if "GW-CANDIDATE" in stype:
                    gw_count += 1
                    eid = f"GW-{gw_count:03d}"
                    print(f"\n[{t_str}] >>> IGAZOLT HULLÁM: {eid} (r={corr:.4f})")
                    log_event(eid, corr, calculate_sky_position(7.12), stype)
                else:
                    glitch_count += 1
                    print(f"\n[{t_str}] !!! HIBA KISZŰRVE: {stype} (r={corr:.4f})")
                    log_event("GLITCH", corr, "N/A", stype)
                
                time.sleep(0.5)
            else:
                sys.stdout.write(f"\rMonitoring... [GW: {gw_count} | Glitch: {glitch_count}]")
                sys.stdout.flush()
            
            time.sleep(0.05)
            
    except KeyboardInterrupt:
        print(f"\nLeállítva. Találatok: {gw_count}, Hibák: {glitch_count}")

if __name__ == "__main__":
    run_mission()