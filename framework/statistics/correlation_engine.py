import numpy as np

def correlate(sig1, sig2):
    # Egyszerű keresztkorreláció a V13 vázhoz
    return np.corrcoef(sig1, sig2)[0, 1]