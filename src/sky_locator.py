import numpy as np

# --- GGWB-CARTOGRAPHER SKY LOCATOR (v4.0.0) ---
# Ez a modul számítja ki a forrás égi koordinátáit az időeltolódás alapján.
# Készítette: Kerepeczki Zsolt (GGWB-Cartographer Projekt)

def calculate_sky_position(delta_t_ms):
    """
    Kiszámítja a hozzávetőleges irányt a Hanford-Livingston tengelyen.
    A maximális időkülönbség a két detektor között ~10 ms (fénysebesség távolsága).
    """
    max_delay = 10.0 # ms 
    
    # Fizikai ellenőrzés: ha az eltolódás nagyobb 10 ms-nél, az nem lehet gravitációs hullám
    if abs(delta_t_ms) > max_delay:
        return "ÉRVÉNYTELEN (Fizikailag lehetetlen időkülönbség - földi zaj)"
    
    # Trigonometriai becslés: cos(theta) = c * delta_t / távolság
    # Itt kiszámoljuk a szöget a detektorokat összekötő egyeneshez képest.
    cos_theta = delta_t_ms / max_delay
    theta_rad = np.arccos(cos_theta)
    theta_deg = np.degrees(theta_rad)
    
    return f"Detektált szög a tengelyhez képest: {theta_deg:.2f}°"

if __name__ == "__main__":
    # Tesztadat: A GW170814 eseménynél mért valós eltolódás kb. 7.12 ms volt
    test_delay = 7.12
    
    print("\n" + "="*75)
    print("   GGWB-CARTOGRAPHER v4.0.0 - ÉGI LOKALIZÁCIÓS MODUL")
    print("="*75)
    print(f"[LOG] Vizsgálat indítása...")
    print(f"[LOG] Bemeneti időkülönbség (H1-L1): {test_delay} ms")
    print("-" * 75)
    
    position = calculate_sky_position(test_delay)
    
    print(f" EREDMÉNY: {position}")
    print("-" * 75)
    print("[INFO] A szög meghatározása sikeres. Ez kijelöli a forrás 'égi gyűrűjét'.")
    print("="*75)