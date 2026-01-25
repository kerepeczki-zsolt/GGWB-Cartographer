<<<<<<< HEAD
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


def dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


@dataclass(frozen=True)
class RunInfo:
    id: str
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: str = ""


RUNS: Dict[str, RunInfo] = {
    "O1": RunInfo(
        id="O1",
        name="Observing Run 1",
        start=dt("2015-09-12"),
        end=dt("2016-01-19"),
        description="First observing run of Advanced LIGO"
    ),
    "O2": RunInfo(
        id="O2",
        name="Observing Run 2",
        start=dt("2016-11-30"),
        end=dt("2017-08-25"),
        description="Second observing run of Advanced LIGO, joined by Virgo"
    ),
    "O3": RunInfo(
        id="O3",
        name="Observing Run 3",
        start=dt("2019-04-01"),
        end=dt("2020-03-27"),
        description="Third observing run of the advanced detector network"
    ),
    "O3GK": RunInfo(
        id="O3GK",
        name="KAGRA–GEO600 joint run",
        start=dt("2020-04-07"),
        end=dt("2020-04-21"),
        description="Short joint run of KAGRA and GEO600 during the O3 era"
    ),
    "O4": RunInfo(
        id="O4",
        name="Observing Run 4",
        start=dt("2023-05-24"),
        end=None,
        description="Fourth observing run of the advanced detector network"
    ),
    "Mission": RunInfo(
        id="Mission",
        name="LISA Mission",
        start=dt("2035-01-01"),
        end=None,
        description="Space-based LISA mission nominal science operations"
    ),
}
=======
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


def dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


@dataclass(frozen=True)
class RunInfo:
    id: str
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: str = ""


RUNS: Dict[str, RunInfo] = {
    "O1": RunInfo(
        id="O1",
        name="Observing Run 1",
        start=dt("2015-09-12"),
        end=dt("2016-01-19"),
        description="First observing run of Advanced LIGO"
    ),
    "O2": RunInfo(
        id="O2",
        name="Observing Run 2",
        start=dt("2016-11-30"),
        end=dt("2017-08-25"),
        description="Second observing run of Advanced LIGO, joined by Virgo"
    ),
    "O3": RunInfo(
        id="O3",
        name="Observing Run 3",
        start=dt("2019-04-01"),
        end=dt("2020-03-27"),
        description="Third observing run of the advanced detector network"
    ),
    "O3GK": RunInfo(
        id="O3GK",
        name="KAGRA–GEO600 joint run",
        start=dt("2020-04-07"),
        end=dt("2020-04-21"),
        description="Short joint run of KAGRA and GEO600 during the O3 era"
    ),
    "O4": RunInfo(
        id="O4",
        name="Observing Run 4",
        start=dt("2023-05-24"),
        end=None,
        description="Fourth observing run of the advanced detector network"
    ),
    "Mission": RunInfo(
        id="Mission",
        name="LISA Mission",
        start=dt("2035-01-01"),
        end=None,
        description="Space-based LISA mission nominal science operations"
    ),
}
>>>>>>> e93f1bf2 (Fix CI and update features)
