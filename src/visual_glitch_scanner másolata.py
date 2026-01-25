import numpy as np

def scan_spectrogram_shape(signal_data):
    """
    Ez a funkció a Gravity Spy vizuális elemzését szimulálja.
    Keresi a függőleges (Blip) és vízszintes (Vonalas zaj) mintákat.
    """
    # Kiszámoljuk a jel "kiterjedését" az idő-frekvencia síkon
    time_spread = np.std(signal_data['time'])
    freq_spread = np.std(signal_data['freq'])
    
    ratio = freq_spread / time_spread
    
    print(f"[MORPHOLOGY] Jel alaktényező (Ratio): {ratio:.2f}")
    
    if ratio > 100:
        return "BLIP GLITCH (Függőleges tüske)"
    elif ratio < 0.1:
        return "60Hz LINE NOISE (Vízszintes zavar)"
    else:
        return "POTENCIÁLIS GW JEL (Íves forma)"

# TESZT FUTTATÁSA
test_signal = {'time': np.random.normal(0, 0.01, 100), 'freq': np.random.normal(100, 50, 100)}
result = scan_spectrogram_shape(test_signal)
print(f"DIAGNÓZIS: {result}")