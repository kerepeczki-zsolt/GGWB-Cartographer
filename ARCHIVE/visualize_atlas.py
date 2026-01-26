import pandas as pd
import matplotlib.pyplot as plt
import os

def create_atlas_map():
    print("\n" + "="*60)
    print("   GGWB-CARTOGRAPHER - VIZUÁLIS GEOMETRIAI TÉRKÉP")
    print("="*60)

    files = ['H1_O1.csv', 'H1_O2.csv']
    
    for f in files:
        path = os.path.join(r"C:\Users\vivob\Desktop\GGWB_FINAL_V12", f)
        if os.path.exists(path):
            print(f"[*] Térkép rajzolása: {f}...")
            df = pd.read_csv(path, low_memory=False)
            
            # Csak a numerikus adatokat használjuk a rajzoláshoz
            df_num = df.select_dtypes(include=['number'])
            
            if df_num.shape[1] >= 2:
                plt.figure(figsize=(10, 7))
                # Az első két jellemzőt használjuk X és Y tengelynek
                plt.scatter(df_num.iloc[:, 0], df_num.iloc[:, 1], alpha=0.5, s=1, c='blue')
                plt.title(f"LIGO Geometriai Atlasz - {f}")
                plt.xlabel("Jellemző 1 (Spektrális átlag)")
                plt.ylabel("Jellemző 2 (Szórás)")
                plt.grid(True)
                
                output_img = f.replace('.csv', '_map.png')
                plt.savefig(output_img)
                print(f"[OK] Térkép mentve: {output_img}")
                plt.close()

if __name__ == "__main__":
    create_atlas_map()