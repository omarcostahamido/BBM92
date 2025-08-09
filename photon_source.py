#PHOTON SOURCE

import numpy as np
import random

class Photon:
    def __init__(self):
        # Generate a random Stokes vector uniformly on the unit sphere
        phi = random.uniform(0, 2 * np.pi)     
        costheta = random.uniform(-1, 1)       
        theta = np.arccos(costheta)          

        # Convert spherical coordinates to Cartesian 
        self.s1 = np.sin(theta) * np.cos(phi)  # H/V basis
        self.s2 = np.sin(theta) * np.sin(phi)  # +/- basis
        self.s3 = np.cos(theta)                # R/L basis

       
        self.stokes = (self.s1, self.s2, self.s3)

    def is_detected(self, efficiency):
        """
        Simulates probabilistic photon detection.
        Returns True with probability = efficiency.
        """
        return random.random() < efficiency

def measure_photon(photon: Photon, basis: str) -> int:
    if basis == 'H/V':
        p0 = (1 + photon.s1) / 2  # probabilité bit 0 = H
    elif basis == '+/-':
        p0 = (1 + photon.s2) / 2  # probabilité bit 0 = +
    else:
        raise ValueError("Unknown basis")

    return 0 if random.random() < p0 else 1




def create_entangled_pair():
    phi = random.uniform(0, 2 * np.pi)
    costheta = random.uniform(-1, 1)
    theta = np.arccos(costheta)

    s1 = np.sin(theta) * np.cos(phi)
    s2 = np.sin(theta) * np.sin(phi)
    s3 = np.cos(theta)

    photon_a = Photon()
    photon_a.s1, photon_a.s2, photon_a.s3 = s1, s2, s3
    photon_a.stokes = (s1, s2, s3)

    photon_b = Photon()
    photon_b.s1, photon_b.s2, photon_b.s3 = -s1, -s2, -s3  # opposé
    photon_b.stokes = (-s1, -s2, -s3)

    return photon_a, photon_b


