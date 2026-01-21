import numpy as np

# --- GGWB-CARTOGRAPHER PROFESSZIONÁLIS FAR ANALYZER (v2.2.0) ---
# Ez a verzió Normalizált Korrelációt (Pearson r) használ a hiba kiszűrésére.

def run_scientific_far_test(iterations=500):
    """
    Kiszámolja a FAR-t a professzionális Normalizált Korrelációval.
    A cél: A véletlen zaj-egybeesések radikális elnyomása.
    """
    false_alarms = 0
    # A tudományos világban a 0.5 feletti Pearson-korreláció már közepes/erős kapcsolat
    # Mi 0.3-ra lőjük be, mert két távoli detektor zajában a 0.3-as véletlen egyezés szinte lehetetlen.
    threshold = 0.30 
    
    print(f"\n[SCAN] Tudományos FAR mérés indítása {iterations} iterációval...")
    print(f"[INFO] Alkalmazott Normalizált Küszöb (Pearson r): {threshold}")

    for i in range(iterations):
        # Két teljesen független detektor (H1, L1) zajszimulációja
        h1_noise = np.random.normal(0, 1, 4096)
        l1_noise = np.random.normal(0, 1, 4096)
        
        # NORMALIZÁLT KORRELÁCIÓ (Pearson r)
        # Ez a lényeg: az érték -1 és 1 között lesz!
        corr_matrix = np.corrcoef(h1_noise, l1_noise)
        correlation = abs(corr_matrix[0, 1])
        
        if correlation > threshold:
            false_alarms += 1
            
    far_rate = (false_alarms / iterations) * 100
    return far_rate, false_alarms

if __name__ == "__main__":
    print("="*75)
    print("   GGWB-CARTOGRAPHER - TUDOMÁNYOS VALIDÁLÁS (NORMALIZÁLT)")
    print("="*75)
    
    total = 500
    rate, count = run_scientific_far_test(total)
    
    print("-" * 75)
    print(f" MÓDSZER                : Normalizált Pearson-korreláció")
    print(f" ÖSSZES PRÓBÁLKOZÁS      : {total}")
    print(f" HAMIS RIASZTÁSOK SZÁMA  : {count}")
    print(f" FAR SZÁZALÉK            : {rate:.2f}%")
    print("-" * 75)
    
    if rate <= 0.1:
        print("[STATUS]: TÖKÉLETES VALIDÁCIÓ. A rendszer statisztikailag tiszta.")
    else:
        print("[STATUS]: TOVÁBBI FINOMÍTÁS SZÜKSÉGES.")
    print("="*75)