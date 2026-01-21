import csv
import os
from datetime import datetime

def log_detection_result(gps_time, status, kurtosis, skewness):
    """
    Minden detektalasi kiserletet elment egy központi naplofajlba.
    """
    log_file = "analysis_results.csv"
    file_exists = os.path.isfile(log_file)
    
    # Adatsor osszeallitasa
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    row = [timestamp, gps_time, status, f"{kurtosis:.6f}", f"{skewness:.6f}"]
    
    try:
        with open(log_file, mode='a', newline='') as f:
            writer = csv.writer(f)
            # Ha uj a fajl, irunk fejlecet
            if not file_exists:
                writer.writerow(["Timestamp", "GPS_Time", "Status", "Kurtosis", "Skewness"])
            writer.writerow(row)
        print(f"[LOGGER] Eredmeny mentve: {log_file}")
    except Exception as e:
        print(f"[LOGGER] HIBA a menteskor: {e}")

if __name__ == "__main__":
    print("--- GGWB-Cartographer Logger Teszt ---")
    log_detection_result(1126259462, "TEST_VETO", 0.2444, 0.0015)