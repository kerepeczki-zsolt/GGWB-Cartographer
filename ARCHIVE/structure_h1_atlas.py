import pandas as pd
import os

def fix_csv_files():
    files = ['H1_O1.csv', 'H1_O2.csv']
    for f_name in files:
        if os.path.exists(f_name):
            df = pd.read_csv(f_name, low_memory=False)
            # Biztosítjuk, hogy a címke oszlop létezik és szöveg típusú
            l_col = 'ml_label' if 'ml_label' in df.columns else 'label'
            if l_col in df.columns:
                df[l_col] = df[l_col].astype(str)
            
            # Minden egyéb oszlopot megpróbálunk számmá alakítani, ami nem megy, az NaN lesz
            for col in df.columns:
                if col != l_col:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # A hiányzó számokat 0-val pótoljuk, hogy a matek ne dögöljön meg
            df = df.fillna(0)
            df.to_csv(f_name, index=False)
            print(f"[OK] {f_name} javítva és mentve.")

if __name__ == "__main__":
    fix_csv_files()