import subprocess
import os
import time

def run_step(step_name, command):
    print(f"\n{'='*60}")
    print(f">>> LÉPÉS: {step_name}")
    print(f"{'='*60}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"!!! HIBA történt a(z) {step_name} fázisban!")
        return False
    return True

def main():
    start_time = time.time()
    
    # 1. Képek beolvasása és konvertálása
    if not run_step("Képfeldolgozás (PNG -> CSV)", "python src/image_processor.py"):
        return

    # 2. Automatizált kutatás és osztályozás
    if not run_step("Adat-analízis és osztályozás", "python src/automated_research.py"):
        return

    # 3. Tudományos összegzés
    if not run_step("Statisztikai jelentés készítése", "python src/research_summary.py"):
        return

    # 4. Vizualizáció
    if not run_step("Grafikonok generálása", "python src/visualize_results.py"):
        return

    end_time = time.time()
    print(f"\n{'*'*60}")
    print(f" TELJES GGWB ANALÍZIS SIKERESEN LEFUTOTT! (Idő: {end_time - start_time:.2f}s)")
    print(f"{'*'*60}\n")

if __name__ == "__main__":
    main()