import numpy as np
from gwpy.timeseries import TimeSeries
from gwpy.segments import DataQualityFlag

def run_strict_comparison():
    print("--- [V12] SZIGORÚ TUDOMÁNYOS ÖSSZEHASONLÍTÁS ---")
    detector = 'H1'
    start = 1238166018
    duration = 3600
    
    try:
        # 1. A TE RENDSZERED: Keressük meg a 320 hiba pontos GPS idejét
        print("Saját mérések analizálása (GPS időbélyegek kinyerése)...")
        data = TimeSeries.fetch_open_data(detector, start, start+duration)
        white = data.whiten()
        # 5-sigma küszöb, mint a master_diagnostics-ban
        outliers = np.where(np.abs(white.value) > 5)[0]
        sajat_idopontok = white.times.value[outliers]

        # 2. HIVATALOS FORRÁS: Lekérjük a technikai kieséseket (BURST szűrő)
        print("Hivatalos LIGO 'BURST' hibalista lekérése...")
        # Ez a flag a rövid, robbanásszerű zajokat jelöli (glitcheket)
        official_glitches = DataQualityFlag.fetch_open_data(f'{detector}:DCH-CLEAN_WH_GLITCH:1', start, start+duration)
        
        # 3. ÖSSZEHASONLÍTÁS
        talalat = 0
        for t in sajat_idopontok:
            if t in official_glitches.active:
                talalat += 1
        
        print("\n" + "="*50)
        print("           SZIGORÚ VALIDÁCIÓS JELENTÉS")
        print("="*50)
        print(f"Te általad talált anomáliák:   {len(sajat_idopontok)} db")
        
        # Megnézzük a LIGO hány mp-et jelölt meg hibásnak
        official_bad_sec = official_glitches.active.sum()
        print(f"LIGO által jelölt hiba-idő:    {official_bad_sec} mp")
        
        # Hitelességi index
        if len(sajat_idopontok) > 0:
            match_rate = (talalat / len(sajat_idopontok)) * 100
            print(f"KÖZVETLEN IDŐBELI EGYEZÉS:     {match_rate:.2f}%")
        
        print("-" * 50)
        print("MAGYARÁZAT:")
        print("Ez a kód azt nézi meg, hogy a te 320 tüskéd")
        print("pillanatában a LIGO is jelzett-e anomáliát.")
        print("="*50)

    except Exception as e:
        print(f"Hiba az összehasonlításnál: {e}")

if __name__ == "__main__":
    run_strict_comparison()