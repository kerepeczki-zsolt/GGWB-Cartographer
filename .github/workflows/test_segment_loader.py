from src.preprocessing.segment_loader import SegmentLoader

loader = SegmentLoader()

try:
    files = loader.list_segments()
    print("OK 🗂 a mappa elérhető.")
    print("Talált fájlok:", files)
except Exception as e:
    print("Hiba:", e)
