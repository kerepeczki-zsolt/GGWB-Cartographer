<<<<<<< HEAD
import os
import cv2
import numpy as np

class SpectrogramDataset:
    def __init__(self, base_path):
        self.base_path = base_path
        # A 22 Gravity Spy kategória alapja, kiegészítve a dőlt blipekkel
        self.classes = ['no_glitch', 'blip', 'whistle', 'scratchy', 'scattered_light'] 
        
    def load_image(self, file_path):
        """Beolvassa a spektrogramot és felkészíti a geometriai elemzésre."""
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # 128x128-as méretre hozzuk a standardizált elemzéshez
            img = cv2.resize(img, (128, 128)) 
            return img / 255.0  # Normalizálás
        return None

    def scan_spectrograms(self):
        """Végignézi a mappákat és listázza a kész képeket."""
        found_files = []
        # Ellenőrizzük, hogy létezik-e a mappa
        if not os.path.exists(self.base_path):
            print(f"FIGYELEM: A mappa nem található: {self.base_path}")
            return []
            
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".png"):
                    found_files.append(os.path.join(root, file))
        return found_files

    def extract_geometric_features(self, img_path):
        """
        Kinyeri a hiba geometriai jellemzőit:
        - Terület (Area)
        - Dőlésszög (Orientation/Angle)
        - Megnyúlás (Eccentricity)
        """
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None: return None
        
        # Küszöbölés, hogy csak a "fényes" hiba maradjon meg
        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        
        # Kontúrok keresése
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # A legnagyobb összefüggő alakzat (a glitch) kiválasztása
            main_glitch = max(contours, key=cv2.contourArea)
            
            # Geometriai jellemzők kiszámítása
            area = cv2.contourArea(main_glitch)
            
            if len(main_glitch) >= 5: # Ellipszis illesztéséhez legalább 5 pont kell
                (x, y), (MA, ma), angle = cv2.fitEllipse(main_glitch)
                return {
                    "area": area,
                    "angle": round(angle, 2), # Kerekítve a szebb látványért
                    "eccentricity": round(MA/ma, 3) if ma != 0 else 0
                }
        return {"area": 0, "angle": 0, "eccentricity": 0}

if __name__ == "__main__":
    # Teszt futtatása - JAVÍTOTT ÚTVONAL A 'DATA' MAPPÁHOZ
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(current_dir, '..', 'data'))
    
    loader = SpectrogramDataset(data_path)
    images = loader.scan_spectrograms()
    
    print("\n" + "="*40)
    print(f"      GGWB GEOMETRIAI ELEMZŐ")
    print("="*40)
    print(f"Keresési útvonal: {data_path}")
    print(f"Feldolgozható képek száma: {len(images)}")
    
    if len(images) > 0:
        print("-" * 40)
        sample_feat = loader.extract_geometric_features(images[0])
        print(f"Példa elemzés (1. kép):")
        print(f"  > Fájl: {os.path.basename(images[0])}")
        print(f"  > Terület: {sample_feat['area']} pixel")
        print(f"  > Dőlésszög: {sample_feat['angle']}°")
        print(f"  > Elnyúltság: {sample_feat['eccentricity']}")
    else:
        print("\nINFO: Még nincs kép a 'data' mappában.")
        print("Várd meg, amíg a generáló program ment legalább egy képet!")
=======
import os
import cv2
import numpy as np

class SpectrogramDataset:
    def __init__(self, base_path):
        self.base_path = base_path
        # A 22 Gravity Spy kategória alapja, kiegészítve a dőlt blipekkel
        self.classes = ['no_glitch', 'blip', 'whistle', 'scratchy', 'scattered_light'] 
        
    def load_image(self, file_path):
        """Beolvassa a spektrogramot és felkészíti a geometriai elemzésre."""
        img = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # 128x128-as méretre hozzuk a standardizált elemzéshez
            img = cv2.resize(img, (128, 128)) 
            return img / 255.0  # Normalizálás
        return None

    def scan_spectrograms(self):
        """Végignézi a mappákat és listázza a kész képeket."""
        found_files = []
        # Ellenőrizzük, hogy létezik-e a mappa
        if not os.path.exists(self.base_path):
            print(f"FIGYELEM: A mappa nem található: {self.base_path}")
            return []
            
        for root, dirs, files in os.walk(self.base_path):
            for file in files:
                if file.endswith(".png"):
                    found_files.append(os.path.join(root, file))
        return found_files

    def extract_geometric_features(self, img_path):
        """
        Kinyeri a hiba geometriai jellemzőit:
        - Terület (Area)
        - Dőlésszög (Orientation/Angle)
        - Megnyúlás (Eccentricity)
        """
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        if img is None: return None
        
        # Küszöbölés, hogy csak a "fényes" hiba maradjon meg
        _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY)
        
        # Kontúrok keresése
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if len(contours) > 0:
            # A legnagyobb összefüggő alakzat (a glitch) kiválasztása
            main_glitch = max(contours, key=cv2.contourArea)
            
            # Geometriai jellemzők kiszámítása
            area = cv2.contourArea(main_glitch)
            
            if len(main_glitch) >= 5: # Ellipszis illesztéséhez legalább 5 pont kell
                (x, y), (MA, ma), angle = cv2.fitEllipse(main_glitch)
                return {
                    "area": area,
                    "angle": round(angle, 2), # Kerekítve a szebb látványért
                    "eccentricity": round(MA/ma, 3) if ma != 0 else 0
                }
        return {"area": 0, "angle": 0, "eccentricity": 0}

if __name__ == "__main__":
    # Teszt futtatása - JAVÍTOTT ÚTVONAL A 'DATA' MAPPÁHOZ
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.normpath(os.path.join(current_dir, '..', 'data'))
    
    loader = SpectrogramDataset(data_path)
    images = loader.scan_spectrograms()
    
    print("\n" + "="*40)
    print(f"      GGWB GEOMETRIAI ELEMZŐ")
    print("="*40)
    print(f"Keresési útvonal: {data_path}")
    print(f"Feldolgozható képek száma: {len(images)}")
    
    if len(images) > 0:
        print("-" * 40)
        sample_feat = loader.extract_geometric_features(images[0])
        print(f"Példa elemzés (1. kép):")
        print(f"  > Fájl: {os.path.basename(images[0])}")
        print(f"  > Terület: {sample_feat['area']} pixel")
        print(f"  > Dőlésszög: {sample_feat['angle']}°")
        print(f"  > Elnyúltság: {sample_feat['eccentricity']}")
    else:
        print("\nINFO: Még nincs kép a 'data' mappában.")
        print("Várd meg, amíg a generáló program ment legalább egy képet!")
>>>>>>> e93f1bf2 (Fix CI and update features)
    print("="*40 + "\n")