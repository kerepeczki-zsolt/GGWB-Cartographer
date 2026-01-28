import sys
import os

# Elérési út biztosítása a framework-höz
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from framework.ingestion.mission_control import acquire_all
from framework.preprocessing.whitening_engine import whiten
from framework.statistics.correlation_engine import correlate
from framework.statistics.ggwb_candidate_selector import select_candidates
from framework.reporting.scientific_validator import validate
from framework.reporting.generate_final_report import generate

def main():
    print("GGWB-Cartographer V13 Core indítása...")
    
    # 1. Adatgyűjtés
    data = acquire_all()

    # 2. Feldolgozás
    processed = {}
    for det, d in data.items():
        processed[det] = whiten(d["h"])

    # 3. Korreláció számítás
    correlations = {}
    keys = list(processed.keys())
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            pair = f"{keys[i]}-{keys[j]}"
            correlations[pair] = correlate(processed[keys[i]], processed[keys[j]])

    # 4. Szelekció és validálás
    candidates = select_candidates(correlations)
    validation = validate(candidates)
    
    # 5. Jelentés
    report = generate(validation)
    print(report)

if __name__ == "__main__":
    main()