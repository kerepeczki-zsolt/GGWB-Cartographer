<<<<<<< HEAD
from typing import Optional, List
from datetime import datetime


class DetectorData:
    def __init__(self, detector_id: str, timestamps: List[datetime], values: List[float]):
        self.detector_id = detector_id
        self.timestamps = timestamps
        self.values = values

    def slice_by_time(self, start: Optional[datetime], end: Optional[datetime]) -> "DetectorData":
        sliced_timestamps = []
        sliced_values = []
        for t, v in zip(self.timestamps, self.values):
            if (start is None or t >= start) and (end is None or t <= end):
                sliced_timestamps.append(t)
                sliced_values.append(v)
        return DetectorData(self.detector_id, sliced_timestamps, sliced_values)
def load_dummy_data(detector_id: str) -> DetectorData:
    """Egyszerű tesztadat-generátor, amíg nincs valódi adatbetöltés."""
    import random
    from datetime import timedelta

    start = datetime(2020, 1, 1)
    timestamps = [start + timedelta(seconds=i) for i in range(100)]
    values = [random.random() for _ in range(100)]

    return DetectorData(detector_id, timestamps, values)
=======
from typing import Optional, List
from datetime import datetime


class DetectorData:
    def __init__(self, detector_id: str, timestamps: List[datetime], values: List[float]):
        self.detector_id = detector_id
        self.timestamps = timestamps
        self.values = values

    def slice_by_time(self, start: Optional[datetime], end: Optional[datetime]) -> "DetectorData":
        sliced_timestamps = []
        sliced_values = []
        for t, v in zip(self.timestamps, self.values):
            if (start is None or t >= start) and (end is None or t <= end):
                sliced_timestamps.append(t)
                sliced_values.append(v)
        return DetectorData(self.detector_id, sliced_timestamps, sliced_values)
def load_dummy_data(detector_id: str) -> DetectorData:
    """Egyszerű tesztadat-generátor, amíg nincs valódi adatbetöltés."""
    import random
    from datetime import timedelta

    start = datetime(2020, 1, 1)
    timestamps = [start + timedelta(seconds=i) for i in range(100)]
    values = [random.random() for _ in range(100)]

    return DetectorData(detector_id, timestamps, values)
>>>>>>> e93f1bf2 (Fix CI and update features)
