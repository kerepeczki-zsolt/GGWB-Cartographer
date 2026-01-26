import pandas as pd
import os

# --- GGWB-CARTOGRAPHER DEEP ANALYTICS ---
# Ez a modul elemzi a detections.csv-t és összefoglalja a zaj-termést.

def run_deep_analysis():
    print("\n" + "="*80)
    print("   GGWB-CARTOGRAPHER - MÉLYREHATÓ ADATELEMZÉS")
    print("="*80)

    csv_path = 'detections.csv'
    if not os.path.exists(csv_path):
        print("[!] Hiba: Nincs detections.csv fájl!")
        return

    try:
        # Beolvasás a Windows-specifikus kódolással
        df = pd.read_csv(csv_path, encoding='cp1252')
        
        if df.empty:
            print("[!] Az adatbázis még üres. Várjunk a monitorra...")
            return

        print(f"[INFO] Eddig összesen {len(df)} eseményt rögzítettünk.")
        
        # Statisztika típusonként
        type_counts = df['Signal_Type'].value_counts()
        print("\n[ESEMÉNYNAPLÓ ÖSSZESÍTVE]:")
        for s_type, count in type_counts.items():
            print(f"  > {s_type}: {count} db")

        # Legerősebb esemény keresése
        max_r = df['Correlation_R'].max()
        strongest = df[df['Correlation_R'] == max_r].iloc[0]
        
        print("-" * 40)
        print(f"[REKORD] A legerősebb észlelt jel: r={max_r}")
        print(f"[REKORD] Típusa: {strongest['Signal_Type']}")
        print(f"[REKORD] Időpontja: {strongest['Timestamp']}")
        print("-" * 40)

    except Exception as e:
        print(f"[HIBA] Probléma az elemzés közben: {e}")

    print("="*80)

if __name__ == "__main__":
    run_deep_analysis()