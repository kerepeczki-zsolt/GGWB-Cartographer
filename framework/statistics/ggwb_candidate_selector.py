def select_candidates(correlations, threshold=0.01):
    return {k: v for k, v in correlations.items() if abs(v) > threshold}