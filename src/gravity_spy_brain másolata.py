import pandas as pd
import numpy as np
import os

class GravitySpyBrain:
    def __init__(self, training_data_path="knowledge_base/validated_samples.csv"):
        self.path = training_data_path
        self._init_knowledge_base()

    def _init_knowledge_base(self):
        # Ha még nincs tudásbázis, létrehozunk egy alap "aranyat" a Gravity Spy alapján
        if not os.path.exists(self.path):
            if not os.path.exists("knowledge_base"): os.makedirs("knowledge_base")
            # Ez a rész a Gravity Spy-ból származó validált geometriai mintákat szimulálja
            data = {
                'label': ['Blip', 'Whistle', 'Koi_Fish', 'GW_Candidate'],
                'f_avg': [150.0, 500.0, 45.0, 35.0],  # Frekvencia középérték
                't_avg': [0.85, 0.40, 0.60, 0.12]    # Tilt (energia) középérték
            }
            pd.DataFrame(data).to_csv(self.path, index=False)

    def identify(self, freq, tilt):
        # Betöltjük a validált mintákat
        df = pd.read_csv(self.path)
        
        # Kiszámoljuk a "távolságot" a mintáktól (melyikhez hasonlít legjobban?)
        # Ez a legegyszerűbb Machine Learning: Legközelebbi Szomszéd elve
        distances = np.sqrt((df['f_avg'] - freq)**2 + (df['t_avg']*100 - tilt*100)**2)
        best_match_idx = distances.idxmin()
        
        return df.iloc[best_match_idx]['label']

if __name__ == "__main__":
    brain = GravitySpyBrain()
    res = brain.identify(148, 0.82)
    print(f"Eredmény: Ez leginkább egy '{res}' típusú mintára hasonlít.")