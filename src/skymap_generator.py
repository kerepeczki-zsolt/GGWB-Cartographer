import numpy as np
import matplotlib.pyplot as plt
import os

def generate_sgwb_skymap():
    """
    HEALPY-MENTES verzió: Mollweide vetítésű égtérkép generálása.
    Zsolt, ez a verzió minden Windows rendszeren hiba nélkül lefut.
    """
    print("[SKYMAP] Égtérkép generálása (Kompatibilis mód)...")
    
    # Rács létrehozása az égbolthoz (Longitude/Latitude)
    lon = np.linspace(-np.pi, np.pi, 200)
    lat = np.linspace(-np.pi/2, np.pi/2, 100)
    Lon, Lat = np.meshgrid(lon, lat)

    # Szimulált anizotrópia adatok (Zaj + Hotspot)
    data = np.random.normal(0, 0.05, Lon.shape)
    
    # Egy "forrás" szimulálása az égen (pl. egy sűrűbb régió)
    source_mask = (np.abs(Lon - 1.2) < 0.5) & (np.abs(Lat - 0.4) < 0.3)
    data[source_mask] += 0.4

    # Kirajzolás Mollweide projekcióval
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(111, projection='mollweide')
    
    im = ax.pcolormesh(Lon, Lat, data, cmap='inferno', shading='auto')
    
    plt.colorbar(im, label='Relatív Intenzitás', orientation='horizontal', pad=0.05)
    ax.set_title("GGWB-Cartographer: SGWB Anizotrópia Térkép (v0.9.1)")
    ax.grid(True, color='white', alpha=0.3)

    output_file = "skymap_output.png"
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"[SKYMAP] Térkép elmentve: {os.path.abspath(output_file)}")
    return output_file

if __name__ == "__main__":
    generate_sgwb_skymap()