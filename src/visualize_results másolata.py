import pandas as pd
import matplotlib.pyplot as plt
import os
import glob

def create_research_plots(results_dir="GGWB_Results"):
    """
    Beolvassa a legfrissebb kutatási adatokat és grafikonokat készít.
    """
    # 1. Legfrissebb jelentés megkeresése
    files = glob.glob(f"{results_dir}/*.csv")
    if not files:
        print("Hiba: Nincs mit kirajzolni! Futtasd le az automated_research.py-t.")
        return
    
    latest_file = max(files, key=os.path.getctime)
    df = pd.read_csv(latest_file)
    
    # 2. Grafikon létrehozása
    plt.figure(figsize=(10, 6))
    
    # Külön színezzük a glitch-eket és a GGWB jelölteket
    for label, color in [("AZONOSÍTVA", "red"), ("ANALÍZIS", "green")]:
        mask = df['classification'].str.contains(label)
        plt.scatter(df.loc[mask, 'f'], df.loc[mask, 't'], 
                    c=color, label='Glitch (Zavar)' if color=='red' else 'GGWB Jelölt',
                    s=100, edgecolors='black', alpha=0.7)

    # 3. Formázás (LIGO stílus)
    plt.title(f"GGWB-Cartographer: Jel-eloszlás\n(Forrás: {os.path.basename(latest_file)})", fontsize=14)
    plt.xlabel("Frekvencia [Hz]", fontsize=12)
    plt.ylabel("Tilt (Energia faktor)", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    # 4. Mentés
    output_plot = f"{results_dir}/analysis_plot.png"
    plt.savefig(output_plot)
    plt.show()
    
    print(f"\n>>> Grafikon elkészült és elmentve ide: {output_plot}")

if __name__ == "__main__":
    create_research_plots()