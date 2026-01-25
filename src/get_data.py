import urllib.request
import os

def progress(count, block_size, total_size):
    percent = int(count * block_size * 100 / total_size)
    print(f"\r>>> Letöltés: {percent}% kész...", end="")

url = "https://zenodo.org/records/1476551/files/trainingsetv1d1.tar.gz?download=1"
output = "data.tar.gz"

print(">>> Kapcsolódás a Zenodo szerverhez...")
try:
    urllib.request.urlretrieve(url, output, progress)
    print("\n>>> SIKER! A fájl a gépeden van.")
except Exception as e:
    print(f"\n>>> HIBA TÖRTÉNT: {e}")