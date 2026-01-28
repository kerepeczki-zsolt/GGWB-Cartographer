import os
from gwpy.timeseries import TimeSeries

def fetch_ligo_data(detector='H1', start=1238166018, end=1238169618):
    """
    Hiteles LIGO adatok letöltése a GWOSC-ról.
    Default: H1 (Hanford), O3 kezdete, 1 óra hosszúság.
    """
    print(f"--- Adat letöltése: {detector} ({start} -> {end}) ---")
    try:
        data = TimeSeries.fetch_open_data(detector, start, end)
        output_path = f"DATA_ATLAS/REAL_DATA/{detector}_{start}.gwf"
        os.makedirs("DATA_ATLAS/REAL_DATA", exist_ok=True)
        data.write(output_path)
        print(f"Siker! Az adat mentve: {output_path}")
        return output_path
    except Exception as e:
        print(f"Hiba az adatletöltés során: {e}")
        return None

if __name__ == "__main__":
    # Teszt futtatás: 1 órányi valódi O3 adat letöltése
    fetch_ligo_data()