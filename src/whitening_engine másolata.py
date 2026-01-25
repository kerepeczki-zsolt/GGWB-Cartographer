import numpy as np

def apply_whitening(data, fs):
    n = len(data)
    data_fft = np.fft.rfft(data)
    freqs = np.fft.rfftfreq(n, 1/fs)
    psd = np.ones_like(data_fft)
    psd[freqs < 20] = 100.0
    whitened_fft = data_fft / np.sqrt(psd)
    return np.fft.irfft(whitened_fft, n=n)