# TEST BBM92 SIMULATOR 
#
# it verifies that BBM92 protocol generates a non empty key for alice and bob; and that their keys have the same length


from photon_source import PhotonSource
from detectors import DetectorArray
from bbm92_simulator import BBM92Simulator

def test_key_length_nonzero():
    source = PhotonSource(rate=10_000, efficiency=1.0)
    detectors = DetectorArray(efficiency=1.0, dark_count_rate=0.0, n_detectors=2)
    sim = BBM92Simulator(source, detectors, noise_sigma=0.0, bit_flip_prob=0.0)
    alice_key, bob_key = sim.run(acquisition_time=0.1)
    assert len(alice_key) > 0
    assert len(alice_key) == len(bob_key)

def test_perfect_agreement_no_noise():
    source = PhotonSource(rate=10_000, efficiency=1.0)
    detectors = DetectorArray(efficiency=1.0, dark_count_rate=0.0, n_detectors=2)
    sim = BBM92Simulator(source, detectors, noise_sigma=0.0, bit_flip_prob=0.0)
    a, b = sim.run(acquisition_time=0.2)
    assert all(x == y for x, y in zip(a, b))

