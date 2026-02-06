import numpy as np
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"

def create_fake_discovery():
    print("--- GGWB TESZT | JELEK INJEKTÁLÁSA ---")
    # Generálunk 10 másodpercnyi zajt
    fs = 4096
    t = np.linspace(0, 10, 10 * fs)
    noise = np.random.normal(0, 1, len(t))
    
    # BEOLTÁS: Egy 500Hz-es mesterséges 'Violin Mode' rezgés a 2. másodpercnél
    noise[2*fs : 2*fs + 500] += 50 * np.sin(2 * np.pi * 500 * np.linspace(0, 0.1, 500))
    
    # BEOLTÁS: Egy mesterséges Gravitációs Hullám (Chirp) a 5. másodpercnél
    # Ez egy emelkedő frekvenciájú jel
    chirp_t = np.linspace(0, 0.5, 2000)
    chirp = 10 * np.sin(2 * np.pi * (30 + 100 * chirp_t**2))
    noise[5*fs : 5*fs + 2000] += chirp

    save_path = os.path.join(project_root, "data", "live_stream.npy")
    np.save(save_path, noise)
    print("[!] A teszt-adatok (beoltott jelekkel) elkészültek.")

if __name__ == "__main__":
    create_fake_discovery()
