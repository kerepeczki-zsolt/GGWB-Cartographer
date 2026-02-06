import numpy as np
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"
fs = 4096
t = np.linspace(0, 10, 10 * fs)
data = np.random.normal(0, 1, len(t)) # Alapzaj

# Gravitációs hullám (Chirp) beoltása a 5. másodpercnél
# Emelkedő frekvencia 30Hz-től 250Hz-ig
chirp_t = np.linspace(0, 0.5, int(0.5 * fs))
chirp = 15 * np.sin(2 * np.pi * (30 + 150 * chirp_t**2))
data[5*fs : 5*fs + len(chirp)] += chirp

save_path = os.path.join(project_root, "data", "live_stream.npy")
np.save(save_path, data)
print("[TEST] Mesterséges GW (Chirp) beoltva a 5. másodpercnél!")
