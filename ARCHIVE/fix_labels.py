import pandas as pd
import os

def fix_atlas_labels():
    print("\n" + "="*60)
    print("   GGWB-CARTOGRAPHER - O1/O2 GEOMETRIAI TÉRKÉP JAVÍTÁS")
    print("="*60)

    # Elérési utak beállítása
    base_path = r"C:\Users\vivob\Desktop\GGWB_FINAL_V12"
    mapping = {
        'H1_O1.csv': 'O1',
        'H1_O2.csv': 'O2'
    }

    for file_name, label in mapping.items():
        path = os.path.join(base_path, file_name)
        if os.path.exists(path):
            print(f"[*] {label} adatbázis betöltése: {file_name}")
            df = pd.read_csv(path, low_memory=False)
            
            # Ellenőrizzük az oszlopokat
            l_col = 'ml_label' if 'ml_label' in df.columns else 'label'
            
            if l_col in df.columns:
                # Kényszerítjük, hogy ne 0.0 legyen, hanem értelmes szöveg, 
                # amíg az eredeti neveket vissza nem töltjük
                count_zeros = (df[l_col].astype(str) == '0.0').sum()
                if count_zeros > 0:
                    print(f"    - Találtunk {count_zeros} db hibás (0.0) címkét. Stabilizálás...")
                    df[l_col] = df[l_col].astype(str).replace('0.0', 'Feldolgozatlan_Zaj')
            
            # Elmentjük a javított verziót
            df.to_csv(path, index=False)
            print(f"[OK] {label} térképfájl frissítve.")
        else:
            print(f"[!] HIBA: A {file_name} nem található a mappában!")

if __name__ == "__main__":
    fix_atlas_labels()