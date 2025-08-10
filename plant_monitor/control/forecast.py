def ewma(prev, new, alpha=0.3):
    if prev is None:
        return new
    return alpha * new + (1 - alpha) * prev
