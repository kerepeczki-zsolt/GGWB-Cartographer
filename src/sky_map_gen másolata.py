import numpy as np

# --- GGWB-CARTOGRAPHER SKY MAP GENERATOR (v5.0.0) ---
# Ez a modul vizualizálja a forrás lehetséges helyét az égen.

def generate_visual_map(angle_deg):
    """
    Készít egy egyszerűsített ASCII égtérképet a talált irány alapján.
    """
    print("\n[MAP] Égi koordináta-rendszer generálása...")
    print("      (Északi Pólus)")
    print("          +90°")
    
    # Kiszámoljuk a vizuális pozíciót a térképen
    # 44.60° kb. a térkép közepénél van
    rows = 10
    target_row = int((90 - angle_deg) / 10)
    
    for r in range(rows):
        line = " | "
        if r == target_row:
            line += "      <<<< [ FORRÁS ZÓNA: " + str(angle_deg) + "° ]"
        else:
            line += "      ."
        print(line)
        
    print("          -90°")
    print("      (Déli Pólus)")

if __name__ == "__main__":
    current_angle = 44.60
    
    print("\n" + "="*75)
    print("   GGWB-CARTOGRAPHER v5.0.0 - VIZUÁLIS ÉGTÉRKÉP GENERÁTOR")
    print("="*75)
    
    generate_visual_map(current_angle)
    
    print("-" * 75)
    print("[SZAKMAI KONKLÚZIÓ]: A forrás az északi és déli félteke határán,")
    print("az égi egyenlítőtől északra helyezkedik el.")
    print("="*75)