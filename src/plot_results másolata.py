<<<<<<< HEAD
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. RÉSZ: DETEKTOR STATISZTIKA (H1 vs L1) ---
# Az adatok a korábbi sikeres futtatásodból
detektorok = ['H1 (Hanford)', 'L1 (Livingston)']
darabszam = [51, 30]

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1) # Ez az első grafikon a bal oldalon
plt.bar(detektorok, darabszam, color=['#e74c3c', '#3498db'])
plt.title('Validált "No Glitch" (O1)')
plt.ylabel('Minták száma')

# --- 2. RÉSZ: JELLEMZŐK ELEMZÉSE (F1-F6) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Megnézzük, létezik-e a jellemzőket tartalmazó fájl
DATA_FILE = os.path.normpath(os.path.join(BASE_DIR, '..', 'data', 'gravitational_features.csv'))

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    features_to_plot = [f"F{i}" for i in range(1, 7)]
    labels = ['Intenz.', 'Átlag', 'Szórás', 'Dinam.', 'Entróp.', 'Kontr.']
    values = df[features_to_plot].iloc[0].values

    plt.subplot(1, 2, 2) # Ez a második grafikon a jobb oldalon
    plt.bar(labels, values, color='skyblue')
    plt.title(f"Jellemzők: {df['filename'].iloc[0][:15]}...")
    plt.xticks(rotation=45)
else:
    plt.subplot(1, 2, 2)
    plt.text(0.5, 0.5, 'Jellemző fájl\nnem található', ha='center', va='center')
    print(f"Megjegyzés: A jellemzők grafikont csak akkor látod, ha van '{DATA_FILE}' fájlod.")

plt.tight_layout()
plt.savefig('osszesitett_elemzes.png')
print("\n--- GRAFIKON KÉSZ ---")
print("Elmentve: osszesitett_elemzes.png")
=======
import pandas as pd
import matplotlib.pyplot as plt
import os

# --- 1. RÉSZ: DETEKTOR STATISZTIKA (H1 vs L1) ---
# Az adatok a korábbi sikeres futtatásodból
detektorok = ['H1 (Hanford)', 'L1 (Livingston)']
darabszam = [51, 30]

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1) # Ez az első grafikon a bal oldalon
plt.bar(detektorok, darabszam, color=['#e74c3c', '#3498db'])
plt.title('Validált "No Glitch" (O1)')
plt.ylabel('Minták száma')

# --- 2. RÉSZ: JELLEMZŐK ELEMZÉSE (F1-F6) ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Megnézzük, létezik-e a jellemzőket tartalmazó fájl
DATA_FILE = os.path.normpath(os.path.join(BASE_DIR, '..', 'data', 'gravitational_features.csv'))

if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    features_to_plot = [f"F{i}" for i in range(1, 7)]
    labels = ['Intenz.', 'Átlag', 'Szórás', 'Dinam.', 'Entróp.', 'Kontr.']
    values = df[features_to_plot].iloc[0].values

    plt.subplot(1, 2, 2) # Ez a második grafikon a jobb oldalon
    plt.bar(labels, values, color='skyblue')
    plt.title(f"Jellemzők: {df['filename'].iloc[0][:15]}...")
    plt.xticks(rotation=45)
else:
    plt.subplot(1, 2, 2)
    plt.text(0.5, 0.5, 'Jellemző fájl\nnem található', ha='center', va='center')
    print(f"Megjegyzés: A jellemzők grafikont csak akkor látod, ha van '{DATA_FILE}' fájlod.")

plt.tight_layout()
plt.savefig('osszesitett_elemzes.png')
print("\n--- GRAFIKON KÉSZ ---")
print("Elmentve: osszesitett_elemzes.png")
>>>>>>> e93f1bf2 (Fix CI and update features)
plt.show()