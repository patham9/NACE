
def TruthValue(wpn):
    (wp, wn) = wpn
    frequency = wp / (wp + wn)
    confidende = (wp + wn) / (wp + wn + 1)
    return (frequency, confidende)

def Truth_Expectation(tv):
    (f, c) = tv
    return (c * (f - 0.5) + 0.5)