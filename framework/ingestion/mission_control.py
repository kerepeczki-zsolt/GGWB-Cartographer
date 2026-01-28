from framework.config.detectors import DETECTORS
from framework.ingestion.gw_data_fetcher import load_strain

def acquire_all():
    data = {}
    for key, det in DETECTORS.items():
        t, h = load_strain(det)
        data[key] = {"t": t, "h": h}
    return data