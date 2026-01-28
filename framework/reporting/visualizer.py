# framework/reporting/visualizer.py
import matplotlib.pyplot as plt
import os

def create_plots(data, features):
    """
    LIGO-Grade vizualizáció a morfometriai adatokról.
    Elmenti a grafikont a results/figures mappába.
    """
    print("🎨 Grafikonok generálása folyamatban...")
    
    # Biztosítjuk a mappa meglétét
    os.makedirs("results/figures", exist_ok=True)
    
    # Grafikon stílus és méret
    plt.figure(figsize=(12, 6))
    
    # A tisztított jel ábrázolása (első 500 pont)
    signal_to_plot = data['Whitened_Confidence'].values[:500]
    plt.plot(signal_to_plot, color='#00ffcc', linewidth=1.5, label='Whitened Signal (H1)')
    
    # Cím és tengelyek
    plt.title(f"GGWB-Cartographer V13 - Morfometriai Elemzés\nFraktál dimenzió: {features['fractal_dimension']:.4f}", fontsize=14)
    plt.xlabel("Minta (Index)", fontsize=12)
    plt.ylabel("Amplitúdó (Standardizált)", fontsize=12)
    
    # Rács és dizájn
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    
    # Mentés
    save_path = "results/figures/meres_eredmeny.png"
    plt.savefig(save_path, dpi=300)
    plt.close()
    
    print(f"🖼️  GRAFIKON SIKERESEN ELMENTVE: {save_path}")