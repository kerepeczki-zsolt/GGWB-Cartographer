import os
import requests
import tarfile
from pathlib import Path

def download():
    # Ez a hivatalos Zenodo link, ami nem dob le
    url = "https://zenodo.org/records/1476551/files/trainingsetv1d1.tar.gz?download=1"
    dest = Path("gravity_spy_data.tar.gz")
    
    print(">>> Zsolt, indul a nagy 4GB-os bányászat! Ne zárd be az ablakot!")
    
    # Letöltés folyamatjelzővel (egyszerűsítve)
    response = requests.get(url, stream=True)
    with open(dest, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024*1024): # 1MB-os darabok
            if chunk:
                f.write(chunk)
                print(".", end="", flush=True) # Minden MB után egy pont
                
    print("\n>>> Letöltés kész! Most kicsomagolom az összes frekvenciát...")
    with tarfile.open(dest, "r:gz") as tar:
        tar.extractall()
    print(">>> MINDEN KÉSZ! A teljes LIGO könyvtár a gépeden van.")

if __name__ == "__main__":
    download()