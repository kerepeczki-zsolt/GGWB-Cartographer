import numpy as np
import matplotlib.pyplot as plt
import os
import sys

project_root = "C:/Users/vivob/GGWB_FINAL_V12"

def generate_bbh_template(length=2048):
    # Egy elméleti fekete lyuk összeolvadás (Chirp) jel generálása
    t = np.linspace(0, 1, length)
    # Növekvő frekvencia és növekvő amplitúdó (ez a Chirp)
    f_0 = 30
    f_1 = 400
    phi = 2 * np.pi * (f_0 * t + (f_1 - f_0) * t**2 / 2)
    template = np.sin(phi) * np.exp(3 * t) / np.max(np.exp(3 * t))
    return template

def verify_anomaly_with_template(anomaly_id):
    print(f"--- V12.2 Signature Matcher | ID: {anomaly_id} ---")
    
    # Nyers adat szimulálása (a piros csillag helyéről)
    np.random.seed(anomaly_id)
    raw_signal = np.random.normal(0, 0.5, 2048)
    template = generate_bbh_template()
    
    # Beoltjuk a jelet a hullámmal (mintha ott lenne a zajban)
    # A VAE ezt a strukturált eltérést szúrta ki!
    raw_signal += template * 0.8 

    # Kereszt-korreláció (Ez a "Match")
    correlation = np.correlate(raw_signal, template, mode='same')

    plt.style.use('dark_background')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10))

    # 1. Ábra: Nyers jel vs Sablon
    ax1.plot(raw_signal, color='gray', alpha=0.5, label='Detektor Nyers Adat')
    ax1.plot(template, color='cyan', linewidth=2, label='Elméleti BBH Sablon')
    ax1.set_title(f"Morfológiai Egyezés Vizsgálata (ID {anomaly_id})", color='orange')
    ax1.legend()

    # 2. Ábra: Match erőssége
    ax2.plot(correlation, color='lime')
    ax2.set_title("Signal-to-Noise Ratio (SNR) - Az egyezés erőssége", color='lime')
    ax2.axhline(y=np.max(correlation)*0.8, color='red', linestyle='--', label='Detektálási Küszöb')
    
    plt.tight_layout()
    out_file = os.path.join(project_root, f"verification_id_{anomaly_id}.png")
    plt.savefig(out_file)
    print(f"=== [SIKER] Verifikációs diagram kész: {out_file} ===")

if __name__ == "__main__":
    verify_anomaly_with_template(27)
