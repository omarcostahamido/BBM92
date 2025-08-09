# TEST KEY DISTILLATION

from key_distillation import KeyDistillation

def test_qber_zero():
    key = [0, 1, 1, 0, 0]
    assert KeyDistillation.compute_qber(key, key) == 0.0

def test_qber_half():
    a = [0, 0, 0, 0]
    b = [0, 1, 0, 1]
    assert KeyDistillation.compute_qber(a, b) == 0.5

def test_privacy_amplification_length():
    key = [0, 1] * 128
    final = KeyDistillation.privacy_amplification(key, final_length=128)
    assert len(final) == 128
