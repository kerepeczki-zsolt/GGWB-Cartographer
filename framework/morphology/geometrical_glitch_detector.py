def is_glitch(fingerprint, threshold=10):
    return fingerprint["energy"] > threshold