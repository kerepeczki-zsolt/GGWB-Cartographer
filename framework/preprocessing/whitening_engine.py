import numpy as np

def whiten(signal):
    mean = np.mean(signal)
    std = np.std(signal)
    if std == 0:
        return signal
    return (signal - mean) / std