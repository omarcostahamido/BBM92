# TEST DETECTORS

from detectors import DetectorArray

def test_perfect_detection():
    d = DetectorArray(efficiency=1.0, dark_count_rate=0.0, n_detectors=8)
    detects = [d.detect(real_photon=True) for _ in range(1000)]
    assert all(detects)

def test_only_dark_counts():
    d = DetectorArray(efficiency=0.0, dark_count_rate=1.0, n_detectors=8)
    detects = [d.detect(real_photon=False) for _ in range(1000)]
    assert all(detects)

