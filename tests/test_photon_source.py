# TEST PHOTON SOURCE

from photon_source import PhotonSource

def test_photon_emission():
    source = PhotonSource(efficiency=1.0)  # doit toujours émettre
    emits = [source.emit_pair() for _ in range(1000)]
    assert all(emits)

def test_photon_no_emission():
    source = PhotonSource(efficiency=0.0)  # ne doit jamais émettre
    emits = [source.emit_pair() for _ in range(1000)]
    assert not any(emits)


