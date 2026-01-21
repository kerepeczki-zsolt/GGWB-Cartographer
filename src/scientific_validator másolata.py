import csv
from geometrical_glitch_detector import GeometricalExpertSystem

def run_final_validation():
    expert = GeometricalExpertSystem()
    report_file = "final_report.csv"
    
    # A teszt adatsorunk (már a GW150914-el együtt)
    test_suite = [
        {"id": "GW150914", "w": 0.02, "h": 120.5, "f": 150, "t": 0.05},
        {"id": "GW170608", "w": 0.015, "h": 45.2, "f": 65, "t": 0.12},
        {"id": "GW190412", "w": 0.025, "h": 55.0, "f": 110, "t": 0.08},
        {"id": "UNKNOWN_X", "w": 0.012, "h": 38.5, "f": 92, "t": 0.04}
    ]

    print("\n" + "="*80)
    print(f"{'MÉRÉSI PONT':<15} | {'EREDMÉNY':<55}")
    print("-" * 80)

    with open(report_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Event", "Result"])

        for data in test_suite:
            res = expert.analyze_modification("H1", "O3", data["w"], data["h"], data["f"], data["t"])
            print(f"{data['id']:<15} | {res}")
            writer.writerow([data['id'], res])

    print("="*80)
    print(f"\nSENSITIVITY REPORT ELMENTVE: {report_file}")

if __name__ == "__main__":
    run_final_validation()