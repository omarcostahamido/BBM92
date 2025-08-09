import random
from photon_source import Photon, measure_photon, create_entangled_pair




class BBM92Simulator:
    def __init__(self, detection_efficiency=0.5, noise_std=0.1, pair_generation_rate=250_000):
        self.detection_efficiency = detection_efficiency
        self.noise_std = noise_std
        self.pair_generation_rate = pair_generation_rate
        self.bases = ['H/V', '+/-']

    def run(self, acquisition_time=10):
        num_pairs = int(self.pair_generation_rate * acquisition_time)

        alice_key = []  
        bob_key = []    

        for _ in range(num_pairs):
            photon_a, photon_b = create_entangled_pair()

            # Détection aléatoire
            if not (photon_a.is_detected(self.detection_efficiency) and
                    photon_b.is_detected(self.detection_efficiency)):
                continue

            alice_basis = random.choice(self.bases)
            bob_basis = random.choice(self.bases)

            # chose same basis
            if alice_basis == bob_basis:
                alice_bit = measure_photon(photon_a, alice_basis)
                bob_bit = measure_photon(photon_b, bob_basis)

                # noise (bit flip)
                if random.random() < self.noise_std:
                    bob_bit = 1 - bob_bit
                    

                    
                alice_key.append(alice_bit)
                bob_key.append(bob_bit)

               

        return alice_key, bob_key
