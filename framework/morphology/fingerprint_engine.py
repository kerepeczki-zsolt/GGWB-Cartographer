import numpy as np

def extract_fingerprint(signal):
    return {
        "mean": float(np.mean(signal)),
        "std": float(np.std(signal)),
        "max": float(np.max(signal)),
        "min": float(np.min(signal)),
        "energy": float(np.sum(signal**2))
    }