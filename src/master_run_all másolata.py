import os
import time

def run_system_diagnostic():
    print("\n" + "#"*70)
    print("   GGWB-CARTOGRAPHER: FULL SYSTEM MASTER DIAGNOSTIC (2026)")
    print("#"*70)
    
    # A futtatandó modulok listája sorrendben
    scripts = [
        ("Feature Szenzitivitás Teszt", "src/feature_sensitivity_test.py"),
        ("Valódi Esemény Validáció", "src/real_event_validation.py"),
        ("Spektrogram Generálás", "src/ultimate_spectrogram.py"),
        ("Automata Template Bank Szkenner", "src/automated_search_engine.py"),
        ("LIGO Integrációs Kapu Teszt", "src/ligo_integrated_search.py")
    ]

    success_count = 0

    for name, path in scripts:
        print(f"\n[FUTTATÁS] -> {name} ({path})...")
        time.sleep(1) # Hogy legyen időd elolvasni a terminált
        
        # Lefuttatjuk a külső fájlt
        exit_code = os.system(f"python {path}")
        
        if exit_code == 0:
            print(f"[OK] {name} sikeresen lefutott.")
            success_count += 1
        else:
            print(f"[HIBA] {name} futtatása közben hiba történt! (Kód: {exit_code})")

    print("\n" + "="*70)
    print("   MASTER ÖSSZEGZÉS")
    print("="*70)
    print(f"Összes modul: {len(scripts)}")
    print(f"Sikeres:      {success_count}")
    print(f"Állapot:      {'RENDSZER KÉSZ AZ ÉLES BEVETÉSRE' if success_count == len(scripts) else 'JAVÍTÁS SZÜKSÉGES'}")
    print("="*70)

if __name__ == "__main__":
    run_system_diagnostic()