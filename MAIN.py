# MAIN SIMULATION SCRIPT

from bbm92_simulator import BBM92Simulator         
from cascade import CascadeProtocol                
from key_distillation import KeyDistillation       

import numpy as np
import matplotlib.pyplot as plt
import time
from tqdm import tqdm


def simulate_key_length_vs_time():
    attenuations = [0.1, 0.3, 0.5]

    acquisition_times = np.linspace(1, 100, 10)

    # --- Physical parameters (photon source) ---
    h = 6.626e-34        # planck constant (J·s)
    c = 3e8              # speed of light (m/s)
    wavelength = 1550e-9 # wavelength of the photons (meters)
    P = 0.02e-9          # optical power (W) = 0.02 nW

    E = h * c / wavelength               # energy/photon 
    pair_generation_rate = (P / E) / 2 # photon pairs/s (must divide by 2)
    
    base_efficiency = 0.6                       
    channel_transmission = 10 ** (-7 / 10)       # 7 dB attenuation in the channel
    efficiency = base_efficiency * channel_transmission  # total detection efficiency

    print(f"Simulation with power = {P} W, λ = {wavelength*1e9:.0f} nm")
    print(f"→ Pair generation rate ≈ {pair_generation_rate:.2e} pairs/s")
    print(f"→ Efficiency with 7dB ≈ {efficiency:.3f}")

    
    results_raw = {att: [] for att in attenuations}
    results_final = {att: [] for att in attenuations}
    qbers_before = {att: [] for att in attenuations}
    qbers_after = {att: [] for att in attenuations}
    std_raw = {att: [] for att in attenuations}
    std_final = {att: [] for att in attenuations}

    start_time = time.time()

    # --- Run simulations ---
    for att in attenuations:
        print(f"\n[Attenuation {int(att*100)}%]")
        eff = efficiency * (1 - att)

        for t in tqdm(acquisition_times, desc=f"Attenuation {int(att*100)}%", leave=False):
            raw_lengths = []
            final_lengths = []
            qber_bef_runs = []
            qber_aft_runs = []

            for _ in range(5):
                simulator = BBM92Simulator(detection_efficiency=eff, noise_std=0.1, pair_generation_rate=pair_generation_rate)
                alice_key, bob_key = simulator.run(acquisition_time=t)
    
                if len(alice_key) == 0:
                    raw_lengths.append(0)
                    final_lengths.append(0)
                    qber_bef_runs.append(1)
                    qber_aft_runs.append(1)
                    continue
    
                qber_bef = KeyDistillation.compute_qber(alice_key, bob_key)
    
                cascade = CascadeProtocol(block_size=32, max_passes=4)
                bob_corrected = cascade.correct(alice_key, bob_key)
    
                qber_aft = KeyDistillation.compute_qber(alice_key, bob_corrected)
    
                final_key = KeyDistillation.privacy_amplification(alice_key, final_length=min(len(alice_key), 256))
    
                raw_lengths.append(len(alice_key))
                final_lengths.append(len(final_key))
                qber_bef_runs.append(qber_bef)
                qber_aft_runs.append(qber_aft)
    
            results_raw[att].append(np.mean(raw_lengths))
            std_raw[att].append(np.std(raw_lengths))
            results_final[att].append(np.mean(final_lengths))
            std_final[att].append(np.std(final_lengths))
            qbers_before[att].append(np.mean(qber_bef_runs))
            qbers_after[att].append(np.mean(qber_aft_runs))


    duration = time.time() - start_time
    print(f"\n⏱ Time of simulation : {duration:.2f} seconds")

    # --- Plot: key vs acquisition time ---
    plt.figure(figsize=(10, 10))
    for att in attenuations:
        plt.errorbar(acquisition_times, results_raw[att], yerr=std_raw[att],
                     label=f"Raw key – att {int(att*100)}%", fmt='-o')
        plt.errorbar(acquisition_times, results_final[att], yerr=std_final[att],
                     label=f"Final key – att {int(att*100)}%", fmt='--x')
    plt.xlabel("Acquisition time (s)")
    plt.ylabel("Length of the key")
    plt.title("Length of the key vs Acquisition time (with errors)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()

    # --- Plot: QBER ---
    plt.figure(figsize=(10, 10))
    for att in attenuations:
        plt.plot(acquisition_times, qbers_before[att], label=f"QBER before – att {int(att*100)}%")
        plt.plot(acquisition_times, qbers_after[att], label=f"QBER after – att {int(att*100)}%", linestyle='--')
    plt.xlabel("Acquisition time (s)")
    plt.ylabel("QBER")
    plt.title("QBER before/after error correction")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Run the simulation
if __name__ == "__main__":
    simulate_key_length_vs_time()

