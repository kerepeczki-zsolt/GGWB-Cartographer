import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import joblib
import os

def plot_feature_importance(model_path, feature_names, output_path="feature_importance.png"):
    # Betöltjük a betanított "agyat"
    if not os.path.exists(model_path):
        print("Még nincs betanított modell!")
        return

    model = joblib.load(model_path)
    
    # Kinyerjük, melyik jellemző mennyit nyomott a latba
    importances = model.feature_importances_
    
    # Csak a top 15-öt nézzük, hogy átlátható legyen
    feat_importances = pd.Series(importances, index=feature_names)
    plt.figure(figsize=(10,6))
    feat_importances.nlargest(15).plot(kind='barh', color='gold')
    
    plt.title("A 15 legfontosabb jellemző a döntésben")
    plt.xlabel("Relatív fontosság")
    plt.tight_layout()
    plt.savefig(output_path)
    print(f">>> Fontossági grafikon elmentve: {output_path}")

if __name__ == "__main__":
    # Teszt futtatás (F1-től F92-ig elnevezett oszlopokkal)
    f_names = [f"F{i}" for i in range(1, 93)]
    plot_feature_importance('ggwb_model.pkl', f_names)