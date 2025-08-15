# BBM92 Quantum Key Distribution Simulator

A Python simulation of the BBM92 quantum key distribution protocol, implementing entangled photon-based quantum cryptography with error correction and privacy amplification.

## What is BBM92?

BBM92 (Bennett, Brassard, Mermin 1992) is a quantum key distribution protocol that uses entangled photon pairs to establish secure cryptographic keys between two parties (Alice and Bob). Unlike BB84 which uses single photons, BBM92 leverages quantum entanglement to detect eavesdropping attempts and generate provably secure keys.

### Key Features of BBM92:
- **Entanglement-based**: Uses correlated photon pairs instead of single photons
- **Distance advantages**: Can work over longer distances than some single-photon protocols  
- **Eavesdropping detection**: Quantum correlations reveal any interception attempts
- **Information-theoretic security**: Security guaranteed by quantum mechanics

## Simulator Features

This simulator provides a comprehensive implementation of the BBM92 protocol including:

- 🔬 **Realistic photon physics**: Stokes vector representation of polarization states
- 📡 **Detector modeling**: Configurable detection efficiency, noise, and dark counts
- 🔧 **Error correction**: Cascade protocol implementation for bit error correction
- 🔐 **Privacy amplification**: Hash-based key distillation for final secure keys
- 📊 **Performance analysis**: QBER calculation and key rate vs. distance studies
- ⚡ **Parameterizable simulation**: Adjustable noise, efficiency, and channel parameters

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Dependencies
Install the required packages:

```bash
pip install numpy matplotlib tqdm
```

Or using the requirements file:
```bash
pip install -r requirements.txt
```

### Clone and Setup
```bash
git clone https://github.com/omarcostahamido/BBM92.git
cd BBM92
```

## Usage

### Quick Start
Run the main simulation:

```bash
python3 MAIN.py
```

This will execute a comprehensive analysis of key generation rates under different channel attenuation conditions.

For a quick demonstration, run the example script:

```bash
python3 example.py
```

This provides a simple demonstration of the BBM92 protocol with explanatory output.

### Basic Example
```python
from bbm92_simulator import BBM92Simulator
from cascade import CascadeProtocol
from key_distillation import KeyDistillation

# Create simulator with realistic parameters
simulator = BBM92Simulator(
    detection_efficiency=0.2,  # 20% detector efficiency
    noise_std=0.1,            # 10% noise level
    pair_generation_rate=250_000  # 250k pairs/second
)

# Generate raw keys
alice_key, bob_key = simulator.run(acquisition_time=1.0)  # 1 second
print(f"Raw key length: {len(alice_key)} bits")

# Calculate quantum bit error rate
qber = KeyDistillation.compute_qber(alice_key, bob_key)
print(f"QBER: {qber:.3f}")

# Apply error correction
cascade = CascadeProtocol(block_size=32, max_passes=4)
bob_corrected = cascade.correct(alice_key, bob_key)

# Privacy amplification
final_key = KeyDistillation.privacy_amplification(alice_key, final_length=256)
print(f"Final secure key: {len(final_key)} bits")
```

## Expected Output

When running `MAIN.py`, you'll see:

```
Simulation with power = 2e-11 W, λ = 1550 nm
→ Pair generation rate ≈ 7.80e+07 pairs/s
→ Efficiency with 7dB ≈ 0.120

[Attenuation 10%]
Processing different acquisition times...
[Attenuation 20%]
...
```

The simulator will generate plots showing:
- **Key length vs. acquisition time** for different channel conditions
- **QBER evolution** before and after error correction
- **Performance comparison** across attenuation levels

### Interpreting Results
- **Higher attenuation** = longer distances = fewer generated keys  
- **QBER < 11%** typically required for secure key generation (values of 20-40% are normal in this simulator due to simplified noise modeling)
- **Final key length** always shorter than raw key due to error correction overhead
- **Zero key generation** may occur with very poor channel conditions or short acquisition times

## Code Structure

```
BBM92/
├── MAIN.py                    # Main simulation script
├── example.py                 # Quick demonstration script
├── requirements.txt           # Python dependencies
├── bbm92_simulator.py         # Core BBM92 protocol implementation
├── photon_source.py           # Entangled photon pair generation
├── detectors.py               # Photon detector simulation
├── cascade.py                 # Cascade error correction protocol
├── key_distillation.py        # QBER calculation and privacy amplification
├── tests/                     # Unit tests for individual modules
│   ├── test_bbm92_simulator.py
│   ├── test_cascade.py
│   ├── test_key_distillation.py
│   └── ...
└── README.md                  # This file
```

### Module Overview

| Module | Purpose |
|--------|---------|
| `BBM92Simulator` | Main protocol orchestration, basis selection, key sifting |
| `photon_source` | Quantum state generation using Stokes vectors |
| `detectors` | Realistic detector modeling with efficiency/noise |
| `cascade` | Classical error correction for quantum channels |
| `key_distillation` | Security analysis and final key generation |

## Use Cases

### 🎓 Educational Applications
- **Quantum cryptography courses**: Demonstrate QKD principles
- **Physics education**: Visualize quantum entanglement effects
- **Security studies**: Understand information-theoretic security

### 🔬 Research Applications  
- **Protocol comparison**: Benchmark against other QKD protocols
- **Channel modeling**: Study effects of different noise sources
- **Parameter optimization**: Find optimal system configurations
- **Performance prediction**: Estimate real-world implementation limits

### 🛠️ Engineering Applications
- **System design**: Guide practical QKD system development
- **Link budget analysis**: Calculate key rates for specific distances
- **Security analysis**: Evaluate protocol robustness under attack

## Configuration Options

Key parameters you can adjust:

| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `detection_efficiency` | Detector quantum efficiency | 0.1 - 0.9 |
| `noise_std` | Channel noise level | 0.01 - 0.3 |
| `pair_generation_rate` | Source brightness (pairs/sec) | 1e3 - 1e8 |
| `acquisition_time` | Measurement duration | 0.1 - 100 seconds |
| `block_size` | Cascade block size | 16 - 128 bits |

## Contributing

Contributions are welcome! Areas for improvement:

- Additional error correction protocols (LDPC, polar codes)
- More sophisticated channel models (atmospheric turbulence, fiber loss)
- Real-time visualization of key generation
- Integration with actual hardware interfaces
- Performance optimizations for large-scale simulations

## License

This project is open source. Please check with the repository owner for specific licensing terms.

## References

1. Bennett, C. H., Brassard, G., & Mermin, N. D. (1992). Quantum cryptography without Bell's theorem. Physical Review Letters, 68(5), 557.
2. Brassard, G., & Salvail, L. (1994). Secret-key reconciliation by public discussion. Workshop on the Theory and Application of Cryptographic Techniques.
3. Lo, H. K., & Chau, H. F. (1999). Unconditional security of quantum key distribution over arbitrarily long distances. Science, 283(5410), 2050-2056.