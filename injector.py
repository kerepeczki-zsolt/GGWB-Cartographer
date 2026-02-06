import numpy as np
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

def create_blind_test():
    print("\n--- GGWB V14.5 | VAK-TESZT GENERÁLÁSA ---")
    fs = 4096
    t = np.linspace(0, 5, 5 * fs)
    # 1. Alapzaj generálása
    data = np.random.normal(0, 1, len(t))
    
    # 2. INJEKCIÓ: Violin Mode (Éles rezonancia 500Hz-en) a 2. másodpercnél
    data[2*fs : 2*fs + 500] += 50 * np.sin(2 * np.pi * 500 * np.linspace(0, 0.1, 500))
    
    # 3. INJEKCIÓ: Chirp (Gravitációs hullám) a 4. másodpercnél
    chirp_t = np.linspace(0, 0.5, 2000)
    chirp = 20 * np.sin(2 * np.pi * (30 + 150 * chirp_t**2))
    data[4*fs : 4*fs + 2000] += chirp

    save_path = os.path.join(project_root, "data", "live_stream.npy")
    np.save(save_path, data)
    print("[SIKER] A tesztcsapda elkészült. Ha a gép jó, ki fogja szúrni őket!")

if __name__ == "__main__":
    create_blind_test()
