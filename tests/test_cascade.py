# TEST CASCADE

from cascade import CascadeProtocol

def test_cascade_fixes_errors():
    alice = [0, 1, 1, 0, 1, 0, 1, 1]
    bob =   [0, 1, 0, 0, 1, 0, 1, 1]  # erreur à index 2

    cascade = CascadeProtocol(block_size=4, num_passes=1)
    corrected = cascade.correct(alice, bob)

    assert corrected == alice

