from scipy.signal import butter, filtfilt

def bandpass(signal, fs, low, high):
    b, a = butter(4, [low/(fs/2), high/(fs/2)], btype='band')
    return filtfilt(b, a, signal)