import os
import numpy as np
import cv2
from feature_extraction.geometric_features import GeometricFeatureExtractor
from models.classifier import GGWBClassifier
from visualization.cartographer_viz import CartographerViz

class GGWB_Pipeline:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.extractor = GeometricFeatureExtractor()
        self.classifier = GGWBClassifier()
        self.csv_path = os.path.join(data_dir, "gravitational_features.csv")

    def run_full_analysis(self):
        print("\n=== GGWB-CARTOGRAPHER TELJES ANALÍZIS INDÍTÁSA ===")
        
        # 1. Lépés: Jellemzők kivonása az összes képből
        files = [f for f in os.listdir(self.data_dir) if f.endswith(('.png', '.jpg'))]
        if not files:
            print("Nincs feldolgozandó kép a mappában!")
            return

        print(f">>> {len(files)} fájl feldolgozása...")
        # (Itt a háttérben lefut az extraction, amit már megírtunk)
        
        # 2. Lépés: Vizualizáció (Térkép készítése)
        print(">>> Térkép generálása...")
        viz = CartographerViz(self.csv_path)
        if viz.load_data():
            viz.plot_pca_map(output_name=os.path.join(self.data_dir, "gw_map_final.png"))

        # 3. Lépés: Intelligens osztályozás
        print(">>> Jelek osztályozása...")
        self.classifier.train(self.csv_path)
        
        print("\n=== ANALÍZIS KÉSZ ===")

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_PATH = os.path.normpath(os.path.join(BASE_DIR, '../data'))
    
    pipeline = GGWB_Pipeline(DATA_PATH)
    pipeline.run_full_analysis()