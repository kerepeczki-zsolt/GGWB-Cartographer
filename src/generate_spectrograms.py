<<<<<<< HEAD
import os
import pandas as pd
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from datetime import datetime

# Csak a biztosan elérhető interferométerek (a V1 hiba elkerülése végett)
INTERFEROMETERS = ['H1', 'L1']
PERIODS = {
    'O3a': ('2019-04-01', '2019-10-01'),
    'O3b': ('2019-11-01', '2020-03-27'),
}

# Útvonalak beállítása a jelenlegi mappaszerkezethez
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLIP_CSV = os.path.join(BASE_DIR, '..', 'blip_set.csv')

def load_blips():
    """Betölti a blip adatokat a CSV-ből."""
    if os.path.exists(BLIP_CSV):
        try:
            df = pd.read_csv(BLIP_CSV)
            if 'gps_time' in df.columns:
                return list(zip(df['gps_time'], df.get('duration', 1.0)))
        except Exception as e:
            print(f"Hiba a CSV betöltésekor: {e}")
    return []

def generate_no_glitch_spectrograms(segment_duration=3600*4):
    """Adatletöltés és spektrogram generálás."""
    blips = load_blips()
    for ifo in INTERFEROMETERS:
        for period_name, (start_str, end_str) in PERIODS.items():
            start = datetime.strptime(start_str, '%Y-%m-%d').timestamp()
            end = datetime.strptime(end_str, '%Y-%m-%d').timestamp()
            current = start
            
            while current < end:
                seg_end = min(current + segment_duration, end)
                try:
                    print(f"Adatok letöltése: {ifo} | {datetime.fromtimestamp(current)}")
                    strain = TimeSeries.fetch_open_data(ifo, current, seg_end)
                    
                    # Glitch eltávolítás
                    for gps, dur in blips:
                        if current < gps < seg_end:
                            strain = strain.gate(tzero=gps, half_width=dur/2 + 2)
                    
                    # Feldolgozás
                    white = strain.whiten()
                    bp = white.bandpass(10, 300)
                    
                    # Spektrogram
                    spec = bp.spectrogram(fftlength=4, overlap=2) ** 0.5
                    plot = spec.plot(norm='log', vmin=1e-24, vmax=1e-20)
                    ax = plot.gca()
                    ax.set_title(f'No-Glitch - {ifo} - {datetime.fromtimestamp(current).strftime("%Y-%m-%d")}')
                    
                    # Mentés
                    save_path = os.path.join(BASE_DIR, '..', 'spectrograms', ifo, period_name)
                    os.makedirs(save_path, exist_ok=True)
                    
                    filename = os.path.join(save_path, f"spec_{ifo}_{datetime.fromtimestamp(current).strftime('%Y%m%d_%H%M')}.png")
                    plot.savefig(filename)
                    plt.close()
                    print(f"--- SIKER: {filename}")
                    
                except Exception as e:
                    print(f"Hiba történt ({ifo}): {e}")
                
                current += segment_duration

if __name__ == "__main__":
=======
import os
import pandas as pd
from gwpy.timeseries import TimeSeries
import matplotlib.pyplot as plt
from datetime import datetime

# Csak a biztosan elérhető interferométerek (a V1 hiba elkerülése végett)
INTERFEROMETERS = ['H1', 'L1']
PERIODS = {
    'O3a': ('2019-04-01', '2019-10-01'),
    'O3b': ('2019-11-01', '2020-03-27'),
}

# Útvonalak beállítása a jelenlegi mappaszerkezethez
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BLIP_CSV = os.path.join(BASE_DIR, '..', 'blip_set.csv')

def load_blips():
    """Betölti a blip adatokat a CSV-ből."""
    if os.path.exists(BLIP_CSV):
        try:
            df = pd.read_csv(BLIP_CSV)
            if 'gps_time' in df.columns:
                return list(zip(df['gps_time'], df.get('duration', 1.0)))
        except Exception as e:
            print(f"Hiba a CSV betöltésekor: {e}")
    return []

def generate_no_glitch_spectrograms(segment_duration=3600*4):
    """Adatletöltés és spektrogram generálás."""
    blips = load_blips()
    for ifo in INTERFEROMETERS:
        for period_name, (start_str, end_str) in PERIODS.items():
            start = datetime.strptime(start_str, '%Y-%m-%d').timestamp()
            end = datetime.strptime(end_str, '%Y-%m-%d').timestamp()
            current = start
            
            while current < end:
                seg_end = min(current + segment_duration, end)
                try:
                    print(f"Adatok letöltése: {ifo} | {datetime.fromtimestamp(current)}")
                    strain = TimeSeries.fetch_open_data(ifo, current, seg_end)
                    
                    # Glitch eltávolítás
                    for gps, dur in blips:
                        if current < gps < seg_end:
                            strain = strain.gate(tzero=gps, half_width=dur/2 + 2)
                    
                    # Feldolgozás
                    white = strain.whiten()
                    bp = white.bandpass(10, 300)
                    
                    # Spektrogram
                    spec = bp.spectrogram(fftlength=4, overlap=2) ** 0.5
                    plot = spec.plot(norm='log', vmin=1e-24, vmax=1e-20)
                    ax = plot.gca()
                    ax.set_title(f'No-Glitch - {ifo} - {datetime.fromtimestamp(current).strftime("%Y-%m-%d")}')
                    
                    # Mentés
                    save_path = os.path.join(BASE_DIR, '..', 'spectrograms', ifo, period_name)
                    os.makedirs(save_path, exist_ok=True)
                    
                    filename = os.path.join(save_path, f"spec_{ifo}_{datetime.fromtimestamp(current).strftime('%Y%m%d_%H%M')}.png")
                    plot.savefig(filename)
                    plt.close()
                    print(f"--- SIKER: {filename}")
                    
                except Exception as e:
                    print(f"Hiba történt ({ifo}): {e}")
                
                current += segment_duration

if __name__ == "__main__":
>>>>>>> e93f1bf2 (Fix CI and update features)
    generate_no_glitch_spectrograms()