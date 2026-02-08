import os
import yaml
import pandas as pd
from sklearn.model_selection import train_test_split

def create_splits():
    # 1.1 Útvonalak rögzítése
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.join(current_dir, '..')
    config_path = os.path.join(project_root, 'configs', 'default.yaml')
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    split_path = os.path.join(project_root, 'data', 'splits')
    os.makedirs(split_path, exist_ok=True)
    
    for detector in config['data_settings']['detectors']:
        print(f"--- [2.2] Feldolgozás: {detector} ---")
        dummy_data = [f"{detector}_{i}.jpg" for i in range(1000)]
        
        # 2.1 Időalapú split (Nincs keverés!)
        train, temp = train_test_split(dummy_data, test_size=0.3, shuffle=False)
        val, test = train_test_split(temp, test_size=0.5, shuffle=False)
        
        # Mentés a megfelelő helyre
        pd.Series(train).to_csv(os.path.join(split_path, f"{detector}_train.csv"), index=False)
        pd.Series(val).to_csv(os.path.join(split_path, f"{detector}_val.csv"), index=False)
        pd.Series(test).to_csv(os.path.join(split_path, f"{detector}_test_blind.csv"), index=False)
        
    print(f"--- [2.1] CSV fájlok rögzítve: {split_path} ---")

if __name__ == "__main__":
    create_splits()