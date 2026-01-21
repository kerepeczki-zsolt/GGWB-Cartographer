import time

def scan_time_range(start_gps, duration, step=2):
    """
    Végigpásztáz egy időintervallumot események után kutatva.
    Zsolt, ez a modul a 'vadász', ami megkeresi a tűt a szénakazalban.
    """
    print(f"[SCANNER] Keresés indítása: {start_gps} -> {start_gps + duration}")
    print(f"[SCANNER] Lépésköz: {step} másodperc")
    
    intervals = []
    current_gps = start_gps
    
    while current_gps < start_gps + duration:
        intervals.append(current_gps)
        current_gps += step
        
    return intervals