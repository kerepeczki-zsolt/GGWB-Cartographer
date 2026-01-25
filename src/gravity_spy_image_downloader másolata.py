import pandas as pd
import requests
import os
import time

def download_images():
    # Itt keressük a már letöltött katalógust
    csv_path = "knowledge_base/gravity_spy_full_catalog.csv"
    save_dir = "knowledge_base/validated_images"
    
    if not os.path.exists(csv_path):
        print("Hiba: Előbb futtasd le a 'massive_data_builder.py'-t, mert nincs meg a CSV!")
        return

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Betöltjük a listát (pl. a 20 fő glitch típust)
    df = pd.read_csv(csv_path)
    
    print(f">>> Képek letöltése folyamatban ide: {save_dir}")
    
    # Letöltünk minden típusból párat, hogy legyen mit elemezni a geometriának
    # A Gravity Spy képei a https://gravityspy.org/static/data/ alatt vannak
    for index, row in df.head(500).iterrows(): # Első körben 500 képet próbálunk
        img_id = row['gravityspy_id']
        # Ez a hivatalos URL minta a képekhez
        url = f"https://gravityspy.org/static/data/plots/{img_id}_spectrogram_0.5.png"
        file_path = os.path.join(save_dir, f"{img_id}.png")
        
        if not os.path.exists(file_path):
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    print(f"[{index}] Letöltve: {img_id}.png")
                # Kicsi szünet, hogy ne terheljük túl a szervert
                time.sleep(0.1)
            except:
                print(f"Hiba a letöltésnél: {img_id}")

    print(">>> A letöltés befejeződött!")

if __name__ == "__main__":
    download_images()