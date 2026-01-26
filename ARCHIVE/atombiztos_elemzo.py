import numpy as np
from PIL import Image
import os

# ====================================================
# GGWB-CARTOGRAPHER: AZONNALI DIAGNOSZTIKAI RENDSZER
# ====================================================

# A te méréseid alapján (32.000 kép ujjlenyomata)
referencia_adatok = {
    "1080Lines": 191465,
    "1400Ripples": 191469,
    "Air_Compressor": 193595,
    "Blip": 192070,
    "Chirp": 191443,
    "Extremely_Loud": 241551,
    "Helix": 191485,
    "Koi_Fish": 211974,
    "Light_Modulation": 194165,
    "No_Glitch": 191436,
    "Power_Line": 191484,
    "Scratchy": 191836,
    "Violin_Mode": 192452,
    "Wandering_Line": 197861,
    "Whistle": 192234
}

def felismeres(teszt_kep_utvonal):
    try:
        img = Image.open(teszt_kep_utvonal).convert('L')
        data = np.asarray(img)
        y, x = np.where(data > 100)
        meret = len(x)
        
        if meret == 0:
            return "TISZTA JEL (No Glitch)", 0
        
        # Megkeressük a legközelebbi ujjlenyomatot
        legjobb_talalat = None
        legkisebb_elteres = float('inf')
        
        for nev, ref_meret in referencia_adatok.items():
            elteres = abs(meret - ref_meret)
            if elteres < legkisebb_elteres:
                legkisebb_elteres = elteres
                legjobb_talalat = nev
        
        return legjobb_talalat, meret
    except Exception as e:
        return f"Hiba: {e}", 0

# --- TESZTELÉS ---
print("\n" + "="*50)
print("GGWB-CARTOGRAPHER ÉLES TESZT")
print("="*50)

# Ide írd be annak a képnek az elérési útját, amit tesztelni akarsz!
teszt_fajl = r"C:\Users\vivob\Desktop\GGWB-Clone\Új mappa\TrainingSet\Whistle\Whistle_pelda.png" # Példa útvonal

eredmeny, mért_adat = felismeres(teszt_fajl)
print(f"\nMért pixelméret: {mért_adat} px")
print(f"DIAGNÓZIS: {eredmeny}")
print("="*50)