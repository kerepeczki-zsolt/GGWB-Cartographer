<<<<<<< HEAD
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


def dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


@dataclass(frozen=True)
class PhaseConfig:
    id: str
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: str = ""


@dataclass(frozen=True)
class RunConfig:
    id: str
    name: str
    phases: Dict[str, PhaseConfig]


@dataclass(frozen=True)
class DetectorConfig:
    id: str
    name: str
    network: str
    runs: Dict[str, RunConfig]


H1 = DetectorConfig(
    id="H1",
    name="LIGO Hanford",
    network="LIGO",
    runs={
        "O1": RunConfig(
            id="O1",
            name="Observing Run 1",
            phases={
                "O1": PhaseConfig(
                    id="O1",
                    name="O1 full run",
                    start=dt("2015-09-12"),
                    end=dt("2016-01-19"),
                    description="First full science run of Advanced LIGO"
                )
            }
        )
    }
)
L1 = DetectorConfig(
    id="L1",
    name="LIGO Livingston",
    network="LIGO",
    runs={
        "O1": RunConfig(
            id="O1",
            name="Observing Run 1",
            phases={
                "O1": PhaseConfig(
                    id="O1",
                    name="O1 full run",
                    start=dt("2015-09-12"),
                    end=dt("2016-01-19"),
                    description="First full science run of Advanced LIGO (Livingston)"
                )
            }
        )
    }
)
V1 = DetectorConfig(
    id="V1",
    name="Virgo",
    network="Virgo",
    runs={
        "O2": RunConfig(
            id="O2",
            name="Observing Run 2",
            phases={
                "O2": PhaseConfig(
                    id="O2",
                    name="O2 full run",
                    start=dt("2017-08-01"),
                    end=dt("2018-01-08"),
                    description="First Virgo science run in joint operation with LIGO"
                )
            }
        )
    }
)
K1 = DetectorConfig(
    id="K1",
    name="KAGRA",
    network="KAGRA",
    runs={
        "O3GK": RunConfig(
            id="O3GK",
            name="O3GK joint run",
            phases={
                "O3GK": PhaseConfig(
                    id="O3GK",
                    name="O3GK full run",
                    start=dt("2020-04-07"),
                    end=dt("2020-04-21"),
                    description="KAGRA–GEO600 joint observing run"
                )
            }
        )
    }
)
GEO600 = DetectorConfig(
    id="GEO600",
    name="GEO600",
    network="GEO",
    runs={
        "O3GK": RunConfig(
            id="O3GK",
            name="O3GK joint run",
            phases={
                "O3GK": PhaseConfig(
                    id="O3GK",
                    name="O3GK full run",
                    start=dt("2020-04-07"),
                    end=dt("2020-04-21"),
                    description="KAGRA–GEO600 joint observing run"
                )
            }
        )
    }
)
LISA = DetectorConfig(
    id="LISA",
    name="Laser Interferometer Space Antenna",
    network="LISA",
    runs={
        "Mission": RunConfig(
            id="Mission",
            name="LISA Mission",
            phases={
                "Phase1": PhaseConfig(
                    id="Phase1",
                    name="Commissioning and early operations",
                    start=dt("2035-01-01"),
                    end=None,
                    description="Initial operational phase of the LISA space mission"
                )
            }
        )
    }
)
=======
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Optional


def dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


@dataclass(frozen=True)
class PhaseConfig:
    id: str
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: str = ""


@dataclass(frozen=True)
class RunConfig:
    id: str
    name: str
    phases: Dict[str, PhaseConfig]


@dataclass(frozen=True)
class DetectorConfig:
    id: str
    name: str
    network: str
    runs: Dict[str, RunConfig]


H1 = DetectorConfig(
    id="H1",
    name="LIGO Hanford",
    network="LIGO",
    runs={
        "O1": RunConfig(
            id="O1",
            name="Observing Run 1",
            phases={
                "O1": PhaseConfig(
                    id="O1",
                    name="O1 full run",
                    start=dt("2015-09-12"),
                    end=dt("2016-01-19"),
                    description="First full science run of Advanced LIGO"
                )
            }
        )
    }
)
L1 = DetectorConfig(
    id="L1",
    name="LIGO Livingston",
    network="LIGO",
    runs={
        "O1": RunConfig(
            id="O1",
            name="Observing Run 1",
            phases={
                "O1": PhaseConfig(
                    id="O1",
                    name="O1 full run",
                    start=dt("2015-09-12"),
                    end=dt("2016-01-19"),
                    description="First full science run of Advanced LIGO (Livingston)"
                )
            }
        )
    }
)
V1 = DetectorConfig(
    id="V1",
    name="Virgo",
    network="Virgo",
    runs={
        "O2": RunConfig(
            id="O2",
            name="Observing Run 2",
            phases={
                "O2": PhaseConfig(
                    id="O2",
                    name="O2 full run",
                    start=dt("2017-08-01"),
                    end=dt("2018-01-08"),
                    description="First Virgo science run in joint operation with LIGO"
                )
            }
        )
    }
)
K1 = DetectorConfig(
    id="K1",
    name="KAGRA",
    network="KAGRA",
    runs={
        "O3GK": RunConfig(
            id="O3GK",
            name="O3GK joint run",
            phases={
                "O3GK": PhaseConfig(
                    id="O3GK",
                    name="O3GK full run",
                    start=dt("2020-04-07"),
                    end=dt("2020-04-21"),
                    description="KAGRA–GEO600 joint observing run"
                )
            }
        )
    }
)
GEO600 = DetectorConfig(
    id="GEO600",
    name="GEO600",
    network="GEO",
    runs={
        "O3GK": RunConfig(
            id="O3GK",
            name="O3GK joint run",
            phases={
                "O3GK": PhaseConfig(
                    id="O3GK",
                    name="O3GK full run",
                    start=dt("2020-04-07"),
                    end=dt("2020-04-21"),
                    description="KAGRA–GEO600 joint observing run"
                )
            }
        )
    }
)
LISA = DetectorConfig(
    id="LISA",
    name="Laser Interferometer Space Antenna",
    network="LISA",
    runs={
        "Mission": RunConfig(
            id="Mission",
            name="LISA Mission",
            phases={
                "Phase1": PhaseConfig(
                    id="Phase1",
                    name="Commissioning and early operations",
                    start=dt("2035-01-01"),
                    end=None,
                    description="Initial operational phase of the LISA space mission"
                )
            }
        )
    }
)
>>>>>>> e93f1bf2 (Fix CI and update features)
