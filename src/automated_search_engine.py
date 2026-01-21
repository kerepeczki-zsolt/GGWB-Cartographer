import numpy as np
import matplotlib.pyplot as plt
import os

def run_automated_search():
    print("\n" + "="*60)
    print("   GGWB-CARTOGRAPHER: AUTOMATA TEMPLATE BANK SZKENNER")
    print("="*60)

    # 1. Beállítások
    fs = 4096
    t = np.linspace(-0.5, 0.05, int(fs * 0.55))
    
    # SZIMULÁCIÓ: Most egy "Közepes Fekete Lyuk" jelet rejtünk el a zajban
    noise = np.random.normal(0, 1e-22, len(t))
    target_freq = 60  # Ez a rejtett jel frekvenciája
    hidden_signal = np.sin(2 * np.pi * (target_freq * (1.0 - t)**(-0.25))) * 0.9e-21
    data = noise + hidden_signal

    # 2. TEMPLATE BANK (A kategóriák gyűjteménye)
    # Ha új típusú hullámot akarsz, csak ide kell majd felvenned egy új sort!
    template_bank = {
        "Kicsi Fekete Lyuk (30Hz)": 30,
        "Közepes Fekete Lyuk (60Hz)": 60,
        "Nagy Fekete Lyuk (120Hz)": 120,
        "Neutroncsillag jelölt (250Hz)": 250
    }

    best_snr = -1
    best_category = None
    all_results = {}

    # 3. AUTOMATIZÁLT KERESÉS (Végigmegyünk az összes mintán)
    print("Szkennelés indítása a különböző GW kategóriák között...")
    
    for name, freq in template_bank.items():
        # Legeneráljuk az aktuális mintát (Template)
        template = np.sin(2 * np.pi * (freq * (1.0 - t)**(-0.25))) * 1e-21
        template = template[::-1] # Megfordítás a matematikai illesztéshez
        
        # Match Filter (Összevetés az adattal)
        snr_curve = np.convolve(data, template, mode='same')
        current_max_snr = np.max(np.abs(snr_curve))
        
        all_results[name] = current_max_snr
        print(f" [TESZT] {name:30} -> Találati erősség: {current_max_snr:.2e}")

        # Megjegyezzük, melyik volt a legerősebb
        if current_max_snr > best_snr:
            best_snr = current_max_snr
            best_category = name

    # 4. EREDMÉNYEK KIÉRTÉKELÉSE
    print("-" * 60)
    print(f"ELEMZÉS VÉGE: A gép azonosította a forrást!")
    print(f"AZONOSÍTOTT TÍPUS: {best_category}")
    print(f"KONFIDENCIA SZINT: {best_snr:.2e}")
    print("-" * 60)

if __name__ == "__main__":
    run_automated_search()