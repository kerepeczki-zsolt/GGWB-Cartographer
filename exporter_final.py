import os
import csv
from datetime import datetime

project_root = "C:/Users/vivob/GGWB_FINAL_V12"
report_path = os.path.join(project_root, "GGWB_Anomaly_Report.csv")

def generate_final_csv():
    print("--- GGWB V12.2 | Tudományos Jelentés Generálása ---")
    
    # Az image_12c03f.png alapján az aktuális fogások
    findings = [
        {"id": "027", "index": 0.086784, "status": "MAGAS GYANÚ"},
        {"id": "065", "index": 0.087122, "status": "MAGAS GYANÚ"},
        {"id": "047", "index": 0.087634, "status": "KRITIKUS ELTÉRÉS"},
        {"id": "051", "index": 0.087965, "status": "KRITIKUS ELTÉRÉS"}
    ]
    
    file_exists = os.path.isfile(report_path)
    
    with open(report_path, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        # Ha új a fájl, írunk fejlécet
        if not file_exists:
            writer.writerow(["Dátum/Idő", "Esemény ID", "Anomália Index", "Besorolás", "Szoftver Verzió"])
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        for item in findings:
            writer.writerow([timestamp, item["id"], f"{item['index']:.6f}", item["status"], "V12.2 DeepScan"])
            
    print(f"=== [SIKER] A jelentés frissítve: {report_path} ===")

if __name__ == "__main__":
    generate_final_csv()
