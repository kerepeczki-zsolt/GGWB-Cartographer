import numpy as np

# --- GGWB-CARTOGRAPHER DATA STREAMER (v4.0.0) ---
def generate_live_chunk(fs=4096, duration=0.1):
    n_samples = 409
    t = np.linspace(0, duration, n_samples)
    h1_noise = np.random.normal(0, 1, n_samples)
    l1_noise = np.random.normal(0, 1, n_samples)
    
    # Validációs mód: Garantált Chirp jel
    f_start, f_end = 30, 250
    phase = 2 * np.pi * (f_start * t + 0.5 * (f_end - f_start) * t**2 / duration)
    chirp = np.sin(phase) * 0.6
    
    return h1_noise + chirp, l1_noise + chirp