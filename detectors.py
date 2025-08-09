# DETECTORS

import random  

class DetectorArray:
    def __init__(self, efficiency=0.2, dark_count_rate=0.0005, n_detectors=8):
        self.efficiency = efficiency 
        self.dark_count_rate = dark_count_rate  
        self.n_detectors = n_detectors 

    def detect(self, real_photon):
        """
        Simulates the detection of a photon.
        """
        if real_photon:
            # Simulate detection of a real photon using a scaled probability:
            # assuming only half of the detectors are relevant for a given event.
            return random.random() < (self.efficiency * self.n_detectors / 2)
        else:
            # Simulate a dark count event (false detection without a real photon)
            return random.random() < self.dark_count_rate

