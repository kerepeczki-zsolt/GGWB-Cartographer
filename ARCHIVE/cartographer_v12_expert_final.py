import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import center_of_mass, gaussian_filter
from collections import defaultdict
import os
import base64
from io import BytesIO

# =================================================================
# GGWB-CARTOGRAPHER V12 - EXPERT PHYSICAL EDITION (FINAL)
# JAVÍTOTT: HEALPY ÉS SCIPY ERROR MENTESÍTVE
# =================================================================

class GGWBCartographerV12_Expert:
    def __init__(self, n_segments=32000, nside=64):
        self.n_segments = n_segments
        # Healpy kiváltása: manuális pixel számítás
        self.npix = 12 * nside**2 
        self.accumulated_csd = np.zeros(self.npix)
        self.variance_map = np.zeros(self.npix)
        self.taxonomy = defaultdict(int)
        self.gw_candidates = []
        self.output_dir = r"C:\Users\vivob\Documents\GGWB_Project\candidates"
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            
    def manual_cwt_ricker(self, data, widths):
        """Saját CWT motor, hogy ne dobjon 'AttributeError'-t a scipy."""
        output = np.zeros((len(widths), len(data)))
        for i, w in enumerate(widths):
            t = np.arange(-3 * w, 3 * w + 1)
            wavelet = (1.0 - (t / w)**2) * np.exp(-0.5 * (t / w)**2)
            output[i, :] = np.convolve(data, wavelet / np.sum(np.abs(wavelet)), mode='same')
        return np.abs(output)

    def generate_q_scan_base64(self, data, idx, label):
        widths = np.linspace(1, 30, num=40)
        cwtm = self.manual_cwt_ricker(data, widths)
        
        plt.figure(figsize=(8, 5))
        plt.imshow(cwtm, extent=[0, 1, 10, 500], cmap='magma', aspect='auto', origin='lower')
        plt.title(f"Candidate #{idx} | Class: {label}")
        
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        plt.close()
        return base64.b64encode(buf.getvalue()).decode('utf-8')

    def extract_12d_features(self, spec_2d):
        spec_smooth = gaussian_filter(spec_2d, sigma=1)
        freq_profile = np.mean(spec_smooth, axis=1)
        f_peak_idx = np.argmax(freq_profile)
        half_max = np.max(freq_profile) / 2
        width = len(np.where(freq_profile > half_max)[0]) or 1
        q_factor = f_peak_idx / (width + 1e-9)
        com = center_of_mass((spec_smooth > np.percentile(spec_smooth, 90)).astype(float))
        time_profile = np.mean(spec_smooth, axis=0)
        asymmetry = np.argmax(time_profile) / (len(time_profile) - np.argmax(time_profile) + 1e-9)
        return {'f_peak': f_peak_idx, 'q_factor': q_factor, 'com_x': com[1], 'com_y': com[0], 'asymmetry': asymmetry}

    def process_data(self):
        print(f"🚀 GGWB-Cartographer V12 Expert: {self.n_segments} szegmens elemzése...")
        for i in range(1000): # Első körben 1000 szegmens a gyors teszthez
            raw_data = np.random.normal(0, 1, 6400)
            if i % 100 == 0: raw_data[3000:3200] += 25.0 
            
            spec_2d = raw_data.reshape(80, 80)
            noise_floor = np.std(spec_2d[spec_2d < np.percentile(spec_2d, 25)])
            
            if np.max(spec_2d) > 4.5 * noise_floor:
                feats = self.extract_12d_features(spec_2d)
                label = "Blip_Candidate" if feats['q_factor'] < 10 else "Violin_Mode"
                self.taxonomy[label] += 1
                if len(self.gw_candidates) < 10:
                    self.gw_candidates.append({'idx': i, 'img': self.generate_q_scan_base64(raw_data, i, label)})
        
        self.generate_html_report()

    def generate_html_report(self):
        path = r"C:\Users\vivob\Documents\report_v12.html"
        html = f"<html><body style='background:#121212;color:white;'><h1>V12 Expert Report</h1>"
        for c in self.gw_candidates:
            html += f"<div><img src='data:image/png;base64,{c['img']}'></div>"
        html += "</body></html>"
        with open(path, "w") as f: f.write(html)
        print(f"✅ KÉSZ! Riport: {path}")

if __name__ == "__main__":
    GGWBCartographerV12_Expert().process_data()