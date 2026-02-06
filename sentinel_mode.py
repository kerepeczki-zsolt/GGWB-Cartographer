import time
import subprocess
import os

project_root = r"C:\Users\vivob\GGWB_FINAL_V12"
fetcher = os.path.join(project_root, "live_fetcher.py")
processor = os.path.join(project_root, "master_processor.py")

def run_sentinel():
    print("=== GGWB V12.9 | SENTINEL (ŐRSZEM) ÜZEMMÓD AKTÍV ===")
    print("A rendszer 5 percenként frissíti az univerzum figyelését...")
    
    try:
        while True:
            print(f"\n[{time.strftime('%H:%M:%S')}] Új adatciklus indítása...")
            
            # Adatletöltés futtatása
            subprocess.run(["python", fetcher], check=True)
            
            # Elemzés futtatása
            subprocess.run(["python", processor], check=True)
            
            print(f"Ciklus kész. Következő ellenőrzés 5 perc múlva.")
            time.sleep(300) # 300 másodperc szünet
            
    except KeyboardInterrupt:
        print("\n[LEÁLLÍTÁS] Az Őrszem pihenni tér.")

if __name__ == "__main__":
    run_sentinel()
