# scripts/indito.py
import sys
import os

# Elérési út rögzítése a framework modulokhoz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.config.ggwb_config import CONFIG
from framework.ingestion.data_ingestion import fetch_local_data
from framework.preprocessing.signal_cleaner import whiten_data
from framework.morphology.pattern_finder import extract_geometry_features
from framework.reporting.visualizer import create_plots

def main():
    print("\n" + "="*60)
    print("🛰️  GGWB-CARTOGRAPHER V13 - TELJES MÉRÉSI CIKLUS")
    print("="*60)
    
    # 1. ADATBEFOGADÁS (Ingestion)
    detector = "H1"
    raw_data = fetch_local_data(detector)
    
    if raw_data is not None:
        # 2. JELTISZTÍTÁS (Preprocessing)
        processed_data = whiten_data(raw_data)
        
        # 3. MORFOMETRIAI ELEMZÉS (Morphology)
        features = extract_geometry_features(processed_data)
        
        if features:
            print(f"🧬 FRAKTÁL DIMENZIÓ: {features['fractal_dimension']:.4f}")
            print(f"💠 TEXTÚRA ENERGIA: {features['texture_entropy']:.4f}")
            print(f"🏔️ DETEKTÁLT CSÚCSOK: {int(features['peak_count'])}")
            
            # 4. VIZUALIZÁCIÓ (Reporting)
            create_plots(processed_data, features)
            
            print("\n" + "-"*60)
            print("🏁 A TELJES ELEMZÉSI FOLYAMAT SIKERESEN LEFUTOTT.")
            print("📁 Eredmények helye: results/figures/meres_eredmeny.png")
            print("="*60)
    else:
        print("\n⚠️ KRITIKUS HIBA: Az adatfolyam megszakadt.")

if __name__ == "__main__":
    main()