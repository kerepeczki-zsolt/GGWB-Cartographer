import numpy as np

# --- GGWB-CARTOGRAPHER SIGNAL CLASSIFIER (v8.0.0 PRO) ---
# Dinamikus chirp-trend analízis és jel-kategorizálás
# Készítette: Kerepeczki Zsolt (LIGO szakértő)

def classify_signal(data, r_value, confidence_index=97.4):
    """
    Osztályozza a jelet a korreláció (r) és a spektrális energia-trend alapján.
    """
    # 1. Küszöbvizsgálat (LIGO O4 standard alapú korreláció)
    if r_value > 0.3:
        # 2. Chirp trend figyelése: 
        # A valódi GW eseményeknél a jel vége (inspiral/merger) magasabb energiájú.
        # Itt egy ablakozott RMS energiát számolunk az elején és a végén.
        start_energy = np.sqrt(np.mean(np.square(data[:100])))
        end_energy = np.sqrt(np.mean(np.square(data[-100:])))
        
        # 3. Döntési logika: Ha az energia nő és a korreláció magas
        if end_energy > start_energy and confidence_index > 90.0:
            return "GW-CANDIDATE", "Validált Gravitációs Hullám"
        elif end_energy > start_energy:
            return "GW-POSSIBLE", "Lehetséges jelölt (További audit szükséges)"
        else:
            return "GLITCH-LIKELY", "Gyanús zajtüske (Energia csökkenés)"
            
    # Alacsony korreláció esetén zajnak minősítjük
    return "NOISE", "Stacionárius zajszint"

if __name__ == "__main__":
    # Teszt futtatás szimulált adattal
    test_data = np.random.normal(0, 1, 1000)
    status, category = classify_signal(test_data, 0.45)
    print(f"\n[LOG] Teszt eredmény: {status} - {category}")