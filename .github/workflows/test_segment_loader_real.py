import os
import sys

# Projekt gyökérkönyvtárának felvétele a sys.path-be
CURRENT_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(os.path.dirname(CURRENT_DIR))
sys.path.insert(0, ROOT_DIR)

from src.preprocessing.segment_loader import SegmentLoader

loader = SegmentLoader()

try:
    files = loader.list_segments()
    print("OK – a mappa elérhető.")
    print("Talált fájlok:", files)
except Exception as e:
    print("Hiba:", e)
