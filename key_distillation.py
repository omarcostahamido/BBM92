#KEY DISTILLATION

import hashlib



class KeyDistillation:
    @staticmethod
    def compute_qber(alice_key, bob_key):
        if len(alice_key) != len(bob_key) or len(alice_key) == 0:
            return 1.0
        errors = sum(1 for a, b in zip(alice_key, bob_key) if a == b)
        return errors / len(alice_key)

    @staticmethod
    def privacy_amplification(key, final_length=None):
        bit_string = ''.join(map(str, key))
        hash_digest = hashlib.sha256(bit_string.encode()).hexdigest()
        bin_digest = bin(int(hash_digest, 16))[2:].zfill(256)
        if final_length is None:
            return bin_digest
        else:
            return bin_digest[:final_length]

