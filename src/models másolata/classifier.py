import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confidence_score
import joblib
import os

class GGWBClassifier:
    def __init__(self):
        # A Random Forest 100 döntési fát fog használni a stabilitásért
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.is_trained = False

    def train(self, csv_path):
        if not os.path.exists(csv_path):
            print("Hiba: Nem találom a tanító adatokat (CSV)!")
            return
        
        # Adatok beolvasása
        df = pd.read_csv(csv_path)
        
        # Feltételezzük, hogy van egy 'label' oszlop (0: zaj, 1: GW jel)
        # Ha még nincs label, akkor a teszteléshez generálunk párat
        if 'label' not in df.columns:
            print("Figyelem: Nincs 'label' oszlop, teszt üzemmód (szimulált címkék).")
            df['label'] = np.random.randint(0, 2, size=len(df))

        X = df.drop(['filename', 'label'], axis=1)
        y = df['label']

        # Adatok szétválasztása tanító és tesztelő halmazra (80% - 20%)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        print(">>> Tanítás folyamatban...")
        self.model.fit(X_train, y_train)
        self.is_trained = True

        # Pontosság ellenőrzése
        score = self.model.score(X_test, y_test)
        print(f">>> Modell pontossága: {score * 100:.2f}%")
        
        # Modell elmentése, hogy később is használhassuk
        joblib.dump(self.model, 'ggwb_model.pkl')
        print(">>> Modell elmentve: ggwb_model.pkl")

    def predict(self, feature_vector):
        if not self.is_trained:
            return "Modell nincs betanítva!"
        
        prediction = self.model.predict([feature_vector])
        probability = self.model.predict_proba([feature_vector])
        
        label = "GRAVITÁCIÓS HULLÁM" if prediction[0] == 1 else "ZAJ / GLITCH"
        confidence = np.max(probability) * 100
        
        return f"Eredmény: {label} ({confidence:.1f}% biztonsággal)"

if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CSV_FILE = os.path.normpath(os.path.join(BASE_DIR, '../../data/gravitational_features.csv'))
    
    brain = GGWBClassifier()
    brain.train(CSV_FILE)