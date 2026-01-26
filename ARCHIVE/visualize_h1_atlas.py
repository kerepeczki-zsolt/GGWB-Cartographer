import pandas as pd
import matplotlib.pyplot as plt
import os

# ==========================================
# GGWB-Cartographer V12 - Atlas VizualizĂˇciĂł
# CĂ©l: O1 Ă©s O2 gravitĂˇciĂłs hullĂˇm zajok Ă¶sszehasonlĂ­tĂˇsa
# KĂ©szĂ­tette: Kerepeczki Zsolt
# ==========================================

def run_atlas_visualization():
    # AlapĂ©rtelmezett Ăştvonalak a rendszerezett adatokhoz
    base_dir = "data/H1_Atlas"
    runs = ['O1', 'O2']
    colors = {'O1': '#1f77b4', 'O2': '#ff7f0e'} # KĂ©k az O1, Narancs az O2
    
    print("--- GGWB-Cartographer: Atlasz GenerĂˇlĂˇs IndĂ­tĂˇsa ---")
    
    plt.figure(figsize=(14, 8))
    found_data = False

    for run in runs:
        file_path = os.path.join(base_dir, run, f"filtered_{run}_reference.csv")
        
        if os.path.exists(file_path):
            try:
                # Adatok beolvasĂˇsa
                df = pd.read_csv(file_path)
                if 'ml_label' in df.columns:
                    # A 8 leggyakoribb minta tĂ­pus kigyĹ±jtĂ©se
                    counts = df['ml_label'].value_counts().head(8)
                    
                    # Grafikon rajzolĂˇsa
                    plt.bar(counts.index + f"\n({run})", counts.values, 
                            color=colors[run], alpha=0.8, label=f"Run {run}")
                    
                    print(f"[SIKER] {run} feldolgozva: {len(df)} bejegyzĂ©s talĂˇlhatĂł.")
                    found_data = True
                else:
                    print(f"[HIBA] A 'ml_label' oszlop hiĂˇnyzik a {run} fĂˇjlbĂłl!")
            except Exception as e:
                print(f"[HIBA] Hiba tĂ¶rtĂ©nt a {run} fĂˇjl olvasĂˇsakor: {e}")
        else:
            print(f"[HIBA] Nem talĂˇlhatĂł a szĹ±rt adat itt: {file_path}")

    if found_data:
        # Grafikon szĂ©pĂ­tĂ©se
        plt.title("LIGO H1 Atlasz: Glitch TĂ­pusok Ă–sszehasonlĂ­tĂˇsa (V12 MĂ©rfĂ¶ldkĹ‘)", fontsize=16)
        plt.xlabel("Minta tĂ­pusa (LIGO Label)", fontsize=12)
        plt.ylabel("GyakorisĂˇg (EsemĂ©nyszĂˇm)", fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend()
        plt.xticks(rotation=30)
        
        # MentĂ©s a fĹ‘ mappĂˇba
        output_name = "H1_Atlas_Comparison_V12.png"
        plt.savefig(output_name)
        print(f"\n[MENTVE] A grafikon elkĂ©szĂĽlt: {output_name}")
        
        print("\nMegnyitĂˇs...")
        plt.show()
    else:
        print("\n[STOP] Nincs megjelenĂ­thetĹ‘ adat. EllenĹ‘rizd a 'data/H1_Atlas' mappĂˇt!")

if __name__ == "__main__":
    run_atlas_visualization()
