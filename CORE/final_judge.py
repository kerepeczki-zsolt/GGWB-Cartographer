import numpy as np
from gwpy.timeseries import TimeSeries
from gwpy.segments import DataQualityFlag

def the_final_verdict():
    print("--- [V12] AZ IGAZSÁG PILLANATA: PONTOS IDŐBELI EGYEZTETÉS ---")
    detector = 'H1'
    start = 1238166018
    duration = 3600
    
    try:
        # 1. SAJÁT ANALÍZIS: GPS IDŐBÉLYEGEK
        print("Saját anomáliák kinyerése...")
        data = TimeSeries.fetch_open_data(detector, start, start+duration)
        white = data.whiten()
        # Szigorú 5-sigma szűrés
        outliers_idx = np.where(np.abs(white.value) > 5)[0]
        sajat_idok = white.times.value[outliers_idx]

        # 2. HIVATALOS LIGO LISTA: Kifejezetten a zajokra (Glitchekre)
        print("Hivatalos LIGO zaj-lista (DCH-CLEAN) lekérése...")
        # Ez a flag konkrétan a zajos tizedmásodperceket jelöli
        official = DataQualityFlag.fetch_open_data(f'{detector}:DCH-CLEAN_WH_GLITCH:1', start, start+duration)
        
        # 3. PONTOS EGYEZTETÉS
        egyezesek = []
        for t in sajat_idok:
            # Megnézzük, hogy a te időpontod benne van-e a LIGO hibalistájában
            if any(start_t <= t <= end_t for start_t, end_t in official.active):
                egyezesek.append(t)

        print("\n" + "="*55)
        print("           SZIGORÚ ÖSSZEHASONLÍTÁSI NAPLÓ")
        print("="*55)
        print(f"Te általad talált összes hiba:    {len(sajat_idok)} db")
        print(f"Ebből a LIGO által is IGAZOLT:    {len(egyezesek)} db")
        
        if len(sajat_idok) > 0:
            rate = (len(egyezesek) / len(sajat_idok)) * 100
            print(f"HITELRESSÉGI INDEX:               {rate:.2f}%")
        
        print("-" * 55)
        if len(egyezesek) > 0:
            print("PÉLDÁK AZ EGYEZŐ IDŐPONTOKRA (GPS):")
            for e in egyezesek[:5]: # Kiírjuk az első ötöt
                print(f" -> EGYEZÉS: {e:.3f} s (Te is láttad, a LIGO is!)")
        else:
            print("Nincs közvetlen egyezés. Ez azt jelenti, hogy vagy a te")
            print("szűrőd túl érzékeny, vagy a LIGO listája hiányos.")
        print("="*55)

    except Exception as e:
        print(f"Hiba az ítélethozatal során: {e}")

if __name__ == "__main__":
    the_final_verdict()