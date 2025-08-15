#!/usr/bin/env python3
"""
Simple example demonstrating BBM92 quantum key distribution simulation.
Run this script to quickly test that the installation is working correctly.
"""

from bbm92_simulator import BBM92Simulator
from cascade import CascadeProtocol
from key_distillation import KeyDistillation

def main():
    print("BBM92 Quantum Key Distribution - Quick Demo")
    print("=" * 50)
    
    # Create simulator with moderate parameters
    print("Initializing BBM92 simulator...")
    simulator = BBM92Simulator(
        detection_efficiency=0.3,    # 30% detector efficiency
        noise_std=0.1,              # 10% noise level
        pair_generation_rate=100_000  # 100k pairs/second
    )
    
    # Generate raw keys
    print("Generating entangled photon pairs and measuring...")
    alice_key, bob_key = simulator.run(acquisition_time=0.5)  # 0.5 seconds
    
    if len(alice_key) == 0:
        print("❌ No keys generated! Try increasing acquisition time or detection efficiency.")
        return
    
    print(f"✅ Generated {len(alice_key)} raw key bits")
    
    # Calculate and display QBER
    qber_before = KeyDistillation.compute_qber(alice_key, bob_key)
    print(f"📊 QBER (before correction): {qber_before:.3f} ({qber_before*100:.1f}%)")
    
    # Apply error correction
    print("Applying Cascade error correction...")
    cascade = CascadeProtocol(block_size=16, max_passes=3)
    bob_corrected = cascade.correct(alice_key, bob_key)
    
    qber_after = KeyDistillation.compute_qber(alice_key, bob_corrected)
    print(f"📊 QBER (after correction): {qber_after:.3f} ({qber_after*100:.1f}%)")
    
    # Privacy amplification
    final_length = min(len(alice_key) // 2, 128)  # Conservative final key length
    if final_length > 0:
        final_key = KeyDistillation.privacy_amplification(alice_key, final_length=final_length)
        print(f"🔐 Final secure key length: {len(final_key)} bits")
        
        # Show key rate
        key_rate = len(final_key) / 0.5  # bits per second
        print(f"🚀 Key generation rate: {key_rate:.1f} bits/second")
        
        # Show sample of final key
        print(f"🔑 Sample key (first 32 bits): {final_key[:32]}")
    else:
        print("❌ Key too short for secure privacy amplification")
    
    print("\n💡 Tip: Modify parameters in the script to explore different scenarios!")
    print("   - Increase detection_efficiency for better performance")
    print("   - Decrease noise_std for lower error rates") 
    print("   - Increase acquisition_time for longer keys")

if __name__ == "__main__":
    main()