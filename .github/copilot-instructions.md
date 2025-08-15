# BBM92 Quantum Key Distribution Simulator

BBM92 is a Python-based quantum key distribution (QKD) simulator implementing the BBM92 protocol. The simulator models entangled photon pair generation, detection, key sifting, error correction via CASCADE protocol, and privacy amplification.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Dependencies
- `pip install numpy matplotlib tqdm pytest` -- Install required Python packages. Takes ~30 seconds.
- Python 3.12.3 is available in the environment

### Build and Test Process
- **No traditional build process needed** -- This is pure Python code
- Run tests: `python3 -m pytest tests/ -v` -- Takes ~5 seconds. EXPECT some test failures due to API mismatches in test files.
- Working tests: `tests/test_detector_array.py` (fully working), partial success in other test files
- Some test files (`test_bbm92_simulator.py`, `test_photon_source.py`) have import errors due to API evolution

### Run the Simulation
- **Main simulation**: `python3 MAIN.py` -- **NEVER CANCEL**: Takes ~99 minutes to complete. Set timeout to 120+ minutes.
- **Quick test**: Use the validation commands below for faster development testing

### Manual Validation Commands
Always run these validation steps after making changes to ensure functionality:

```bash
# Basic component test (~2 seconds)
python3 -c "
from bbm92_simulator import BBM92Simulator
simulator = BBM92Simulator(detection_efficiency=0.1, noise_std=0.1, pair_generation_rate=50_000)
alice_key, bob_key = simulator.run(acquisition_time=0.5)
print(f'Generated keys: Alice={len(alice_key)}, Bob={len(bob_key)}')
assert len(alice_key) > 0 and len(bob_key) > 0
print('✓ Basic key generation works')
"

# Full pipeline test (~1 second)
python3 -c "
from bbm92_simulator import BBM92Simulator
from cascade import CascadeProtocol
from key_distillation import KeyDistillation

simulator = BBM92Simulator(detection_efficiency=0.1, noise_std=0.1, pair_generation_rate=50_000)
alice_key, bob_key = simulator.run(acquisition_time=0.5)

if len(alice_key) > 0:
    qber_before = KeyDistillation.compute_qber(alice_key, bob_key)
    cascade = CascadeProtocol(block_size=32, max_passes=4)
    bob_corrected = cascade.correct(alice_key, bob_key)
    qber_after = KeyDistillation.compute_qber(alice_key, bob_corrected)
    final_key = KeyDistillation.privacy_amplification(alice_key, final_length=min(len(alice_key), 64))
    
    print(f'QBER before: {qber_before:.3f}, after: {qber_after:.3f}')
    print(f'Final key length: {len(final_key)}')
    assert 0.0 <= qber_before <= 1.0 and 0.0 <= qber_after <= 1.0
    assert len(final_key) > 0
    print('✓ Full BBM92 pipeline works')
else:
    print('No keys generated - check parameters')
"
```

## Validation Requirements

- **ALWAYS** run both validation commands above after making any changes to BBM92 components
- **NEVER CANCEL** the main simulation (`python3 MAIN.py`) - it takes ~99 minutes and produces key length vs acquisition time plots
- **Expected test failures**: Some tests in `test_bbm92_simulator.py` and `test_photon_source.py` fail due to API mismatches
- **Working tests**: `test_detector_array.py` should pass completely

## Code Structure and Navigation

### Key Components
- `MAIN.py` -- Main simulation script with plotting functionality
- `bbm92_simulator.py` -- Core BBM92 protocol implementation
- `photon_source.py` -- Entangled photon pair generation and measurement
- `cascade.py` -- CASCADE error correction protocol
- `key_distillation.py` -- QBER computation and privacy amplification
- `detectors.py` -- Photon detector array simulation

### Important Implementation Details
- **QBER Calculation**: The `compute_qber` function expects **anticorrelated** keys (errors when bits are equal)
- **Detection Model**: Uses probabilistic detection with configurable efficiency
- **Simulation Scale**: Default parameters generate ~78M photon pairs/second with realistic detection rates
- **Memory Usage**: Large simulations can use significant memory due to key storage

### Typical Development Workflow
1. Make code changes to core modules
2. Run validation commands to verify basic functionality
3. Run specific tests: `python3 -m pytest tests/test_detector_array.py -v`
4. For major changes, run longer validation or subset of main simulation
5. **Only run full simulation** (`python3 MAIN.py`) for complete validation - takes 99 minutes

### Performance Characteristics
- Small simulation (50k pairs, 0.5s): ~0.5 seconds
- Medium simulation (250k pairs, 10s): ~47 seconds  
- **Full simulation: 99 minutes with 3 attenuation levels, 10 time points, 5 runs each**
- **CRITICAL**: Always set timeouts of 120+ minutes for main simulation

### Common Debugging
- **Import errors in tests**: Expected due to API evolution - focus on `test_detector_array.py` for reliable testing
- **No keys generated**: Reduce noise_std or increase detection_efficiency/pair_generation_rate
- **QBER calculation issues**: Remember the function expects anticorrelated keys (BBM92 protocol characteristic)
- **Memory issues**: Reduce acquisition_time or pair_generation_rate parameters

## Common Commands Reference

```bash
# Repository status
ls -la                                    # View all files
find . -name "*.py" | head -10           # List Python files

# Dependencies
python3 --version                        # Check Python version (expect 3.12.3)
pip install numpy matplotlib tqdm pytest # Install dependencies

# Testing
python3 -m pytest tests/ -v             # Run all tests (~5s, expect some failures)
python3 -m pytest tests/test_detector_array.py -v  # Run working tests only

# Simulation
python3 MAIN.py                          # Full simulation (99 minutes, NEVER CANCEL)

# Quick validation (always run after changes)
[See validation commands above]
```

## File Listing Reference
```
BBM92/
├── MAIN.py              # Main simulation with plotting
├── bbm92_simulator.py   # Core BBM92 protocol
├── photon_source.py     # Photon generation and measurement  
├── cascade.py           # Error correction protocol
├── key_distillation.py  # QBER and privacy amplification
├── detectors.py         # Detector array simulation
├── __init__.py          # Package initialization
└── tests/               # Test suite (partial functionality)
    ├── test_detector_array.py      # ✓ Working tests
    ├── test_cascade.py             # Partial functionality
    ├── test_key_distillation.py    # Partial functionality  
    ├── test_bbm92_simulator.py     # ✗ Import errors
    └── test_photon_source.py       # ✗ Import errors
```