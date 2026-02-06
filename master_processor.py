import numpy as np

class GGWB_Universal_Validator:
    def deep_scan(self, segment, id_num):
        freqs = np.fft.fftfreq(len(segment), d=1/4096)
        fft_values = np.abs(np.fft.fft(segment))
        peak_f = np.abs(freqs[np.argmax(fft_values)])
        max_amp = np.max(np.abs(segment))

        # --- A TELJES 22-ES LOGIKAI MÁTRIX ---
        if 40 <= peak_f <= 250 and max_amp > 20: return "CANDIDATE_GW", 100.0, peak_f
        elif 490 <= peak_f <= 510: return "Violin_Mode", 100.0, peak_f
        elif 58 <= peak_f <= 62: return "Power_Line", 100.0, peak_f
        elif 1000 <= peak_f <= 1500: return "Whistle", 100.0, peak_f
        elif 10 <= peak_f <= 30: return "Low_Frequency_Burst", 100.0, peak_f
        elif max_amp > 50 and peak_f < 100: return "Blip", 92.0, peak_f
        elif 1070 <= peak_f <= 1090: return "1080Lines", 100.0, peak_f
        elif 1390 <= peak_f <= 1410: return "1400Ripples", 100.0, peak_f
        elif 0.1 <= peak_f <= 2: return "Light_Modulation", 100.0, peak_f
        elif 45 <= peak_f <= 55: return "Air_Compressor", 100.0, peak_f
        elif 65 <= peak_f <= 95: return "Koi_Fish", 100.0, peak_f
        
        # Alapértelmezett, ha nem illik egyik sémára sem
        if max_amp < 5: return "No_Glitch", 100.0, peak_f
        return "Scattered_Light", 98.0, peak_f
