import numpy as np

def load_strain(detector, duration=4):
    """
    Determinisztikus dummy betöltő – később LIGO API-ra cserélhető
    """
    fs = detector["sampling_rate"]
    t = np.linspace(0, duration, fs * duration)
    # Determinisztikus zaj generálás a tesztelhetőséghez
    np.random.seed(42)
    noise = np.random.normal(0, 1e-21, size=len(t))
    return t, noise