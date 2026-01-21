<<<<<<< HEAD
from dataclasses import dataclass
from typing import Dict

from .detectors import H1, L1, V1, K1, GEO600, LISA
from .runs import RUNS
from .phases import PHASES
from .networks import NETWORKS


@dataclass(frozen=True)
class GGWBConfig:
    detectors: Dict[str, object]
    runs: Dict[str, object]
    phases: Dict[str, object]
    networks: Dict[str, object]


CONFIG = GGWBConfig(
    detectors={
        "H1": H1,
        "L1": L1,
        "V1": V1,
        "K1": K1,
        "GEO600": GEO600,
        "LISA": LISA,
    },
    runs=RUNS,
    phases=PHASES,
    networks=NETWORKS,
)
=======
from dataclasses import dataclass
from typing import Dict

from .detectors import H1, L1, V1, K1, GEO600, LISA
from .runs import RUNS
from .phases import PHASES
from .networks import NETWORKS


@dataclass(frozen=True)
class GGWBConfig:
    detectors: Dict[str, object]
    runs: Dict[str, object]
    phases: Dict[str, object]
    networks: Dict[str, object]


CONFIG = GGWBConfig(
    detectors={
        "H1": H1,
        "L1": L1,
        "V1": V1,
        "K1": K1,
        "GEO600": GEO600,
        "LISA": LISA,
    },
    runs=RUNS,
    phases=PHASES,
    networks=NETWORKS,
)
>>>>>>> e93f1bf2 (Fix CI and update features)
