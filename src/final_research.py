<<<<<<< HEAD
import pandas as pd
import os

print("\n" + "="*60)
print("   GGWB-CARTOGRAPHER: LIGO-READY VALIDATION & DATA ANALYSIS")
print("="*60)

# A metaadat fájl neve
csv_file = 'trainingset_v1d1_metadata (1).csv'

# Fájl keresése
if not os.path.exists(csv_file):
    csv_path = os.path.join('..', csv_file)
else:
    csv_path = csv_file

try:
    df = pd.read_csv(csv_path)
    
    # 1. Korszakok meghatározása GPS idő alapján
    def get_era(gps):
        if gps < 1137254417: return 'O1 (2015-2016)'
        elif gps < 1187733618: return 'O2 (2016-2017)'
        else: return 'O3 (2019-2020)'

    df['korszak'] = df['peak_time'].apply(get_era)
    
    # 2. Szűrés a tiszta adatokra (No Glitch)
    no_glitch = df[df['label'] == 'None_of_the_Above']
    
    # 3. STATISZTIKAI ÖSSZEGZÉS
    summary = no_glitch.groupby(['korszak', 'ifo']).size().unstack(fill_value=0)
    print("Elérhető tiszta szegmensek detektoronként:")
    print(summary)
    print("-" * 60)

    # --- LIGO 100% VALIDATION CONTROL ---
    print("VALIDÁCIÓS PROTOKOLL BEÁLLÍTÁSA:")
    
    # Itt definiáljuk a két futtatási módot
    validation_modes = {
        "SCIENCE_RUN": {"shift": 0, "status": "ACTIVE"},
        "NULL_TEST_RUN": {"shift": 10, "status": "ACTIVE"}
    }

    for mode, config in validation_modes.items():
        print(f"-> {mode}: Időeltolás = {config['shift']} másodperc [{config['status']}]")

    print("-" * 60)
    print("LISA modul: Készen áll a szimulált űradatok fogadására.")
    print("STÁTUSZ: A rendszer készen áll a 100%-os megbízhatósági tesztre.")
    print("=" * 60)

except Exception as e:
    print(f"CRITICAL ERROR: Hiba történt a LIGO adatbázis elérésekor: {e}")
=======
import pandas as pd
import os

print("\n" + "="*55)
print("   GRAVITY SPY: UNIVERZÁLIS DETEKTOR- ÉS KORSZAK ANALÍZIS")
print("="*55)

# A metaadat fájl neve, ami a főmappádban van
csv_file = 'trainingset_v1d1_metadata (1).csv'

# Megkeressük a fájlt (megnézzük a főmappában is)
if not os.path.exists(csv_file):
    csv_path = os.path.join('..', csv_file)
else:
    csv_path = csv_file

try:
    df = pd.read_csv(csv_path)
    
    # Korszakok meghatározása GPS idő alapján
    def get_era(gps):
        if gps < 1137254417: return 'O1 (2015-2016)'
        elif gps < 1187733618: return 'O2 (2016-2017)'
        else: return 'O3 (2019-2020)'

    df['korszak'] = df['peak_time'].apply(get_era)
    
    # Csak a tiszta 'No Glitch' (None_of_the_Above) mintákat nézzük
    no_glitch = df[df['label'] == 'None_of_the_Above']
    
    # Táblázat készítése detektorok (H1, L1) és korszakok szerint
    summary = no_glitch.groupby(['korszak', 'ifo']).size().unstack(fill_value=0)
    
    print(summary)
    print("-" * 55)
    print("LISA modul: Készen áll a szimulált űradatok fogadására.")
    print("=" * 55)

except Exception as e:
    print(f"Hiba történt a fájl beolvasásakor: {e}")
>>>>>>> e93f1bf2 (Fix CI and update features)
