<<<<<<< HEAD
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


def dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


@dataclass(frozen=True)
class PhaseInfo:
    id: str
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: str = ""


PHASES: Dict[str, PhaseInfo] = {
    "O3a": PhaseInfo(
        id="O3a",
        name="O3a phase",
        start=dt("2019-04-01"),
        end=dt("2019-10-01"),
        description="First half of the O3 observing run"
    ),
    "O3b": PhaseInfo(
        id="O3b",
        name="O3b phase",
        start=dt("2019-11-01"),
        end=dt("2020-03-27"),
        description="Second half of the O3 observing run"
    ),
    "O4a": PhaseInfo(
        id="O4a",
        name="O4a phase",
        start=dt("2023-05-24"),
        end=dt("2024-01-16"),
        description="First segment of the O4 observing run"
    ),
    "O4b": PhaseInfo(
        id="O4b",
        name="O4b phase",
        start=dt("2024-01-17"),
        end=None,
        description="Second segment of the O4 observing run"
    ),
    "MissionPhase1": PhaseInfo(
        id="MissionPhase1",
        name="LISA Mission Phase 1",
        start=dt("2035-01-01"),
        end=None,
        description="Initial operational phase of the LISA mission"
    ),
}
=======
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Optional


def dt(date_str: str) -> datetime:
    return datetime.strptime(date_str, "%Y-%m-%d")


@dataclass(frozen=True)
class PhaseInfo:
    id: str
    name: str
    start: Optional[datetime]
    end: Optional[datetime]
    description: str = ""


PHASES: Dict[str, PhaseInfo] = {
    "O3a": PhaseInfo(
        id="O3a",
        name="O3a phase",
        start=dt("2019-04-01"),
        end=dt("2019-10-01"),
        description="First half of the O3 observing run"
    ),
    "O3b": PhaseInfo(
        id="O3b",
        name="O3b phase",
        start=dt("2019-11-01"),
        end=dt("2020-03-27"),
        description="Second half of the O3 observing run"
    ),
    "O4a": PhaseInfo(
        id="O4a",
        name="O4a phase",
        start=dt("2023-05-24"),
        end=dt("2024-01-16"),
        description="First segment of the O4 observing run"
    ),
    "O4b": PhaseInfo(
        id="O4b",
        name="O4b phase",
        start=dt("2024-01-17"),
        end=None,
        description="Second segment of the O4 observing run"
    ),
    "MissionPhase1": PhaseInfo(
        id="MissionPhase1",
        name="LISA Mission Phase 1",
        start=dt("2035-01-01"),
        end=None,
        description="Initial operational phase of the LISA mission"
    ),
}
>>>>>>> e93f1bf2 (Fix CI and update features)
