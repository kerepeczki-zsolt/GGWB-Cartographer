import pandas as pd
import os

class SpectrogramProcessor:
    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir): os.makedirs(self.data_dir)

    def process_images(self):
        print(">>> SZIGORÚ TESZTADATOK GENERÁLÁSA...")
        
        # 5 db Glitch (rossz) és 5 db GW Jelölt (jó)
        data = {
            'ifo': ['H1', 'L1', 'H1', 'L1', 'H1', 'L1', 'H1', 'L1', 'H1', 'L1'],
            'run': ['O4']*10,
            'w': [0.001, 0.015, 0.001, 0.012, 0.001, 0.014, 0.018, 0.011, 0.001, 0.014],
            'h': [100, 150, 100, 120, 100, 130, 110, 140, 100, 130],
            'f': [250.0, 35.0, 280.0, 42.0, 300.0, 48.0, 55.0, 38.0, 320.0, 45.0], # 250+ Hz = Glitch, 30-60 Hz = GW
            't': [0.9, 0.12, 0.85, 0.15, 0.95, 0.13, 0.11, 0.14, 0.88, 0.12]      # Magas Tilt = Glitch
        }
        
        df = pd.DataFrame(data)
        output_path = os.path.join(self.data_dir, "extracted_measurements.csv")
        df.to_csv(output_path, index=False)
        return "ADATOK FRISSÍTVE: Most már lesznek piros és zöld pöttyök is!"

if __name__ == "__main__":
    print(SpectrogramProcessor().process_images())