# GGWB-Cartographer

A GGWB‑Térképész egy gravitációs‑hullám háttér (Gravitational‑Wave Background, GGWB) térképezésére fejlesztett kutatási keretrendszer, amely a LIGO/Virgo detektorok adataiból generál statisztikai térképeket és jelkandidátus‑eloszlásokat.  
Célja, hogy doktori szintű, reprodukálható munkaként bemutassa a GGWB‑hez kapcsolódó adatelemzési és gépi tanulási módszereket.

## Célkitűzés

A projekt célja a GGWB‑re érzékeny adatszakaszok azonosítása, a háttérjel térbeli és frekvenciafüggő struktúráinak feltérképezése, valamint a lehetséges asztrofizikai és kozmológiai forrás‑modellek összehasonlítása.  
A keretrendszer támogatja a jel‑zaj arány vizsgálatát, a spektrális tulajdonságok elemzését és a különböző osztályozó‑/regressziós modellek kiértékelését.

## Módszer és eredmények (röviden)

A kód LIGO‑típusú metaadat‑ és idősor‑fájlokból kiindulva előkészíti a jellegmezőket (feature‑öket), majd neurális háló és klasszikus gépi tanulási modellek segítségével térképezi fel a GGWB‑re utaló mintázatokat.  
A részletes módszertan, az alkalmazott adatválogatás, a tanító‑ és teszthalmazok, valamint az elért fizikai következtetések a kísérő tanulmányban olvashatók.

## Repository felépítése

- `adat/` – bemeneti metaadat‑ és idősor‑fájlok (pl. CSV‑k, HDF5 fájlok).  
- `src/` – a fő Python modulok (adatbetöltés, feature‑képzés, modellek, kiértékelés).  
- `notebooks/` – Google Colab / Jupyter jegyzetfüzetek példafuttatásokkal.  
- `docs/` – tudományos dokumentáció, a GGWB‑Térképész részletes tanulmánya és ábrái.  

(A mappák közül azok jelennek meg, amelyeket ténylegesen létrehozol a projekt során.)

## Futtatás Google Colab‑ban

1. Hozz létre egy új Google Colab jegyzetfüzetet, és klónozd a repót:  
   `!git clone https://github.com/<felhasznalonev>/GGWB-Terkepesz.git`  
2. Lépj be a könyvtárba:  
   `%cd GGWB-Terkepesz`  
3. Telepítsd a szükséges csomagokat (ha nincs előtelepítve):  
   `!pip install -r requirements.txt`  
4. Futtasd az első példajegyzetfüzetet a `notebooks/` mappából, vagy importáld a `src/` modulokat saját jegyzetfüzetedben.

## Tudományos tanulmány

A projekthez tartozó részletes tudományos tanulmány külön fájlban érhető el a `docs/` mappában (pl. `docs/ggwb_terkepesz_tanulmany.pdf`).  
A tanulmány tartalmazza a teljes elméleti hátteret, az adatkezelés részleteit, a modellarchitektúrákat, valamint az eredmények fizikai értelmezését.
