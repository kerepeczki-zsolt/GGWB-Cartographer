import matplotlib.pyplot as plt
import numpy as np
import os

def create_expert_view(filename, instrument, diagnosis, frequency, tilt, view_mode="GRAVITY_SPY"):
    plt.figure(figsize=(10, 6))
    
    # 1. Alap zaj (Background noise) szimulálása
    x = np.linspace(-0.1, 0.1, 200)
    y = np.linspace(10, 2000, 200)
    X, Y = np.meshgrid(x, y)
    Z = np.random.normal(0.2, 0.05, X.shape)

    # 2. MATEMATIKAI MORFOLÓGIA GENERÁLÁSA
    # Blip család (Függőleges csepp)
    if any(k in diagnosis for k in ["Blip", "Tomte", "Koi"]):
        sigma_x = 0.002 if "Tomte" in diagnosis else 0.005
        sigma_y = 200
        Z += 2.5 * np.exp(-(X**2 / (2*sigma_x**2) + (Y-frequency)**2 / (2*sigma_y**2)))
        if "Koi" in diagnosis:
             Z += 1.0 * np.exp(-(X**2 / (2*0.02**2) + (Y-frequency)**2 / (2*50**2)))

    # Whistle (V-alakú ív)
    elif "Whistle" in diagnosis:
        for offset in np.linspace(-0.06, 0.06, 120):
            target_y = frequency + (offset**2 * 60000)
            Z += 1.8 * np.exp(-((X-offset)**2 / (2*0.002**2) + (Y-target_y)**2 / (2*40**2)))

    # Helix (Három egymás feletti folt)
    elif "Helix" in diagnosis:
        for h_off in [frequency-250, frequency, frequency+250]:
            Z += 1.8 * np.exp(-(X**2 / (2*0.006**2) + (Y-h_off)**2 / (2*60**2)))

    # Scratch (Hosszú vízszintes karcolás)
    elif "Scratch" in diagnosis:
        Z += 2.2 * np.exp(-(X**2 / (2*0.08**2) + (Y-frequency)**2 / (2*8**2)))

    # Power Line / 1080 Lines (Éles vízszintes vonal)
    elif "Line" in diagnosis or "Power" in diagnosis:
        Z += 2.8 * np.exp(-(X**2 / (2*1.0**2) + (Y-frequency)**2 / (2*3**2)))

    # Scattered Light (Alacsony frekvenciás felhő)
    elif "Szórt fény" in diagnosis or "lökés" in diagnosis:
        Z += 2.0 * np.exp(-(X**2 / (2*0.07**2) + (Y-45)**2 / (2*25**2)))

    # Extremely Loud (Mindent elnyomó energia)
    elif "Loud" in diagnosis:
        Z += 5.0 * np.exp(-(X**2 / (2*0.06**2) + (Y-frequency)**2 / (2*1000**2)))

    # 3. MEGJELENÍTÉS
    cmap = 'viridis' if view_mode == "GRAVITY_SPY" else 'magma'
    plt.pcolormesh(X, Y, Z, shading='gouraud', cmap=cmap)
    
    if view_mode == "GRAVITY_SPY":
        plt.yscale('log')
        plt.ylim(10, 2000)

    plt.colorbar(label="Normalized Energy")
    plt.title(f"{view_mode} VIEW: {diagnosis}", fontsize=12, fontweight='bold')
    plt.xlabel("Idő (s)")
    plt.ylabel("Frekvencia (Hz)")

    plt.text(-0.09, 1500 if view_mode != "GRAVITY_SPY" else 500, 
             f"IFO: {instrument}\nType: {diagnosis}\nExpert: GGWB-C", 
             bbox=dict(facecolor='black', alpha=0.7, edgecolor='white'), color='white')

    if not os.path.exists('research_gallery'): os.makedirs('research_gallery')
    save_path = f"research_gallery/{view_mode}_{filename.replace('.dat', '.png')}"
    plt.savefig(save_path)
    plt.close()
    return save_path