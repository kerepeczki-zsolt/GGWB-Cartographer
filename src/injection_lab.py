import numpy as np
import matplotlib.pyplot as plt

def generate_mock_signal(fs, duration, snr, frequency=120):
    """
    Egy egyszerűsített szinuszos 'chirp' jel generálása injekcióhoz.
    A valóságban ez egy inspiral hullámforma lenne (pl. IMRPhenomD).
    """
    t = np.linspace(0, duration, int(fs * duration))
    # Amplitúdó skálázása az SNR eléréséhez
    # SNR = A / sigma_zaj
    signal = np.sin(2 * np.pi * frequency * t) * (snr / 10.0) 
    return signal

def run_injection_test(noise_floor, snr_range):
    """
    Végigfuttatja a rendszert különböző SNR szinteken, 
    és méri a Recovery Rate-et.
    """
    fs = 4096
    duration = 1.0
    results = []

    print(f"\n{'SNR':<10} | {'RECOVERY STATUS':<20} | {'ACCURACY':<10}")
    print("-" * 50)

    for snr in snr_range:
        # 1. Tiszta fehér zaj generálása (Whitened background)
        noise = np.random.normal(0, 1, int(fs * duration))
        
        # 2. Jel injektálása
        signal = generate_mock_signal(fs, duration, snr)
        data_with_signal = noise + signal
        
        # 3. Recovery detekció (Egyszerűsített kereszt-korreláció teszt)
        # Ha a korreláció > küszöb, akkor 'Recovered'
        correlation = np.max(np.correlate(data_with_signal, signal, mode='same')) / (snr * 100)
        
        recovered = "SUCCESS" if correlation > 0.45 else "FAILED"
        accuracy = min(100, correlation * 150) if recovered == "SUCCESS" else 0
        
        results.append(recovered)
        print(f"{snr:<10} | {recovered:<20} | {accuracy:<10.2f}%")

    return results

if __name__ == "__main__":
    print("="*60)
    print("   GGWB-CARTOGRAPHER - INJECTION RECOVERY BENCHMARK")
    print("="*60)
    
    # SNR szintek tesztelése: 2-től (nagyon zajos) 15-ig (tiszta)
    snrs = [2, 4, 6, 8, 10, 12, 15]
    run_injection_test(1.0, snrs)
    
    print("\n[INFO] A teszt lefutott. Készítsd elő az SNR vs. Efficiency görbét.")
    print("="*60)