<<<<<<< HEAD
from dataclasses import dataclass
from typing import Dict, List

from .detectors import H1, L1, V1, K1, GEO600, LISA


@dataclass(frozen=True)
class NetworkInfo:
    id: str
    name: str
    detectors: List[str]


NETWORKS: Dict[str, NetworkInfo] = {
    "LIGO": NetworkInfo(
        id="LIGO",
        name="LIGO Network",
        detectors=["H1", "L1"]
    ),
    "LVK": NetworkInfo(
        id="LVK",
        name="LIGO–Virgo–KAGRA Network",
        detectors=["H1", "L1", "V1", "K1"]
    ),
    "GEO": NetworkInfo(
        id="GEO",
        name="GEO600 Network",
        detectors=["GEO600"]
    ),
    "KAGRA": NetworkInfo(
        id="KAGRA",
        name="KAGRA Network",
        detectors=["K1"]
    ),
    "LISA": NetworkInfo(
        id="LISA",
        name="LISA Space Network",
        detectors=["LISA"]
    ),
}
=======
from dataclasses import dataclass
from typing import Dict, List

from .detectors import H1, L1, V1, K1, GEO600, LISA


@dataclass(frozen=True)
class NetworkInfo:
    id: str
    name: str
    detectors: List[str]


NETWORKS: Dict[str, NetworkInfo] = {
    "LIGO": NetworkInfo(
        id="LIGO",
        name="LIGO Network",
        detectors=["H1", "L1"]
    ),
    "LVK": NetworkInfo(
        id="LVK",
        name="LIGO–Virgo–KAGRA Network",
        detectors=["H1", "L1", "V1", "K1"]
    ),
    "GEO": NetworkInfo(
        id="GEO",
        name="GEO600 Network",
        detectors=["GEO600"]
    ),
    "KAGRA": NetworkInfo(
        id="KAGRA",
        name="KAGRA Network",
        detectors=["K1"]
    ),
    "LISA": NetworkInfo(
        id="LISA",
        name="LISA Space Network",
        detectors=["LISA"]
    ),
}
>>>>>>> e93f1bf2 (Fix CI and update features)
