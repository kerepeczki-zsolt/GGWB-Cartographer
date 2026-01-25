import matplotlib.pyplot as plt
import numpy as np
import os

def generate_analysis_plot(strain_data, stats, status):
    """
    Grafikus jelentest keszit a detektalasrol.
    Strain adatok es statisztikai mutatok vizualizacioja.
    """
    output_file = "analysis_plot.png"
    
    # Abrat letrehozunk ket al-abraval
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    fig.suptitle(f"GGWB-Cartographer Detekciós Jelentés\nStátusz: {status}", fontsize=16)

    # 1. abra: Idotartomany (Strain)
    ax1.plot(strain_data, color='blue', alpha=0.7)
    ax1.set_title("Időtartományú jel (Strain)")
    ax1.set_xlabel("Minta index")
    ax1.set_ylabel("Amplitúdó")
    ax1.grid(True)

    # 2. abra: Statisztikai ujjlenyomat (Bar chart)
    labels = ['Kurtosis', 'Skewness', 'Std Dev']
    values = [stats['kurtosis'], stats['skewness'], stats['std']]
    colors = ['red' if abs(stats['kurtosis']) > 2.5 else 'green', 'orange', 'purple']
    
    ax2.bar(labels, values, color=colors)
    ax2.set_title("92-Dimenziós Statisztikai Profil (Részlet)")
    ax2.set_ylabel("Érték")
    ax2.grid(axis='y')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    
    # Mentes
    plt.savefig(output_file)
    plt.close()
    print(f"[VISUALIZER] Grafika elmentve: {os.path.abspath(output_file)}")

if __name__ == "__main__":
    # Gyors teszt
    test_data = np.random.normal(0, 1, 4096)
    test_stats = {'kurtosis': -0.0036, 'skewness': 0.0015, 'std': 1.0}
    generate_analysis_plot(test_data, test_stats, "TESZT_VETO")