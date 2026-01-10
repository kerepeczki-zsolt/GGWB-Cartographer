# **GGWB-Cartographer**

A GGWB‑Térképész egy gravitációs‑hullám háttér (Gravitational‑Wave Background, GGWB) térképezésére fejlesztett kutatási keretrendszer, amely a LIGO/Virgo detektorok adataiból generál statisztikai térképeket és jelkandidátus‑eloszlásokat.  
Célja, hogy doktori szintű, reprodukálható munkaként bemutassa a GGWB‑hez kapcsolódó adatelemzési és gépi tanulási módszereket.

---

## **Célkitűzés**

A projekt célja a GGWB‑re érzékeny adatszakaszok azonosítása, a háttérjel térbeli és frekvenciafüggő struktúráinak feltérképezése, valamint a lehetséges asztrofizikai és kozmológiai forrás‑modellek összehasonlítása.  
A keretrendszer támogatja a jel‑zaj arány vizsgálatát, a spektrális tulajdonságok elemzését és a különböző osztályozó‑/regressziós modellek kiértékelését.

---

## **Módszer és eredmények (röviden)**

A kód LIGO‑típusú metaadat‑ és idősor‑fájlokból kiindulva előkészíti a jellegmezőket (feature‑öket), majd neurális háló és klasszikus gépi tanulási modellek segítségével térképezi fel a GGWB‑re utaló mintázatokat.  
A részletes módszertan, az alkalmazott adatválogatás, a tanító‑ és teszthalmazok, valamint az elért fizikai következtetések a kísérő tanulmányban olvashatók.

---

## **Repository felépítése**

adat/ – bemeneti metaadat‑ és idősor‑fájlok (pl. CSV‑k, HDF5 fájlok).  
src/ – a fő Python modulok (adatbetöltés, feature‑képzés, modellek, kiértékelés).  
notebooks/ – Google Colab / Jupyter jegyzetfüzetek példafuttatásokkal.  
docs/ – tudományos dokumentáció, a GGWB‑Térképész részletes tanulmánya és ábrái.  
(A mappák közül azok jelennek meg, amelyeket ténylegesen létrehozol a projekt során.)

---

# **🔧 Kiegészítés: részletes projektstruktúra**

```
GGWB-Cartographer/
│
├── ggwb_cartographer/
│   ├── core/                 # Alap logika, adatkezelés
│   ├── models/               # ML és DL modellek
│   ├── features.py           # FeatureExtractor és jellemzőképzés
│   ├── api.py                # (opcionális) API interfész
│   └── __init__.py
│
├── src/
│   ├── feature_extraction/   # Kísérleti jellemzők
│   └── data_loader.py        # Adatbetöltés, normalizálás, ablakozás
│
├── tests/
│   └── test_features.py      # Automatikus tesztek
│
├── data/                     # Bemeneti adatok (nem verziókezelt)
├── requirements.txt
└── README.md
```

---

# **🧩 Modulok kiegészítő leírása**

### **ggwb_cartographer/features.py**
- FeatureExtractor osztály  
- GLCM textúra‑jellemzők  
- Spektrális mutatók  
- Idő‑frekvencia aggregációk  

### **ggwb_cartographer/models/**
- Klasszikus ML modellek (SVM, RF, XGBoost)  
- Neurális hálók (CNN, 1D/2D modellek)  

### **ggwb_cartographer/core/**
- Adatkezelés  
- Metaadat‑feldolgozás  
- Pipeline lépések  

### **src/data_loader.py**
- Adatbetöltés  
- Normalizálás  
- Ablakozás  

---

# **▶️ Helyi futtatás (kiegészítés)**

### Klónozás

```
git clone https://github.com/<felhasznalonev>/GGWB-Cartographer.git
cd GGWB-Cartographer
```

### Virtuális környezet aktiválása

```
.\venv310\Scripts\activate
```

### Csomagok telepítése

```
pip install -r requirements.txt
```

### Tesztek futtatása

```
$env:PYTHONPATH="." ; pytest -q
```

---

# **🧪 Példa modulhasználatra**

```
from ggwb_cartographer.features import FeatureExtractor

extractor = FeatureExtractor()
features = extractor.extract(signal_array, sampling_rate=4096)
print(features)
```

---

# **Futtatás Google Colab‑ban**

Hozz létre egy új Google Colab jegyzetfüzetet, és klónozd a repót:

```
!git clone https://github.com/<felhasznalonev>/GGWB-Terkepesz.git
```

Lépj be a könyvtárba:

```
%cd GGWB-Terkepesz
```

Telepítsd a szükséges csomagokat (ha nincs előtelepítve):

```
!pip install -r requirements.txt
```

Futtasd az első példajegyzetfüzetet a notebooks/ mappából, vagy importáld a src/ modulokat saját jegyzetfüzetedben.

---

# **Tudományos tanulmány**

A projekthez tartozó részletes tudományos tanulmány külön fájlban érhető el a docs/ mappában (pl. `docs/ggwb_terkepesz_tanulmany.pdf`).  
A tanulmány tartalmazza a teljes elméleti hátteret, az adatkezelés részleteit, a modellarchitektúrákat, valamint az eredmények fizikai értelmezését.

📄 **Teljes elméleti dokumentáció (PDF)**


- vagy a docs/ tanulmány vázának megírása.
