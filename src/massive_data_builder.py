import pandas as pd
import os
import re
import time
import requests

def build():
    base_path = os.getcwd()
    target = os.path.join(base_path, "knowledge_base", "structured_training")
    url = "https://gravityspy.org/static/data/glitch_metadata.csv"
    
    print(f">>> CÉL: {target}")
    
    try:
        print(">>> KAPCSOLÓDÁS... (Ha a szerver ledob, újrapróbálom...)")
        
        # Kényszerített letöltés nyers módban, hogy elkerüljük a HTML hibát
        response = requests.get(url, timeout=30)
        if response.status_code != 200 or '<script' in response.text:
            print("HIBA: A szerver még mindig pihen. Várj 10 másodpercet és indítsd újra!")
            return

        # CSV beolvasása a letöltött szövegből
        from io import StringIO
        df = pd.read_csv(StringIO(response.text), on_bad_lines='skip', low_memory=False)
        
        # Oszlop keresése (No_Glitch alapján)
        label_col = next((c for c in df.columns if df[c].astype(str).str.contains('No_Glitch', na=False).any()), None)
        
        if not label_col:
            print("HIBA: Nem találom a kategóriákat a táblázatban!"); return

        all_unique_labels = df[label_col].unique()
        print(f">>> SIKER! {len(all_unique_labels)} frekvencia-zaj azonosítva.")

        for label in all_unique_labels:
            if pd.isna(label): continue
            label_str = str(label)
            
            # Tisztítás (Windows barát nevek)
            if any(x in label_str for x in ['{', '}', '[', ']', ';', '<', '>']): continue
            clean_name = re.sub(r'[^a-zA-Z0-9_]', '_', label_str)
            
            # Mentés: No_Glitch-ből 2000, a többiből 1000 sor
            is_no_glitch = (label_str == 'No_Glitch')
            limit = 2000 if is_no_glitch else 1000
            f_name = "H1_L1_Candidates.csv" if is_no_glitch else f"GLITCH_{clean_name}.csv"
            
            df[df[label_col] == label].head(limit).to_csv(os.path.join(target, f_name), index=False)
            print(f"--- BÁNYÁSZVA: {f_name}")
            time.sleep(0.05)

        print("\n" + "="*60)
        print(">>> KÜLDETÉS TELJESÍTVE! A TELJES LIGO-ZAJKÉSZLET A GÉPEDEN! <<<")
        print("="*60)

    except Exception as e:
        print(f"Hiba a folyamatban: {e}")

if __name__ == "__main__":
    build()