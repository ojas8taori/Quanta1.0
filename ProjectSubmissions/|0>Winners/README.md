## Team Information

### Team Name
**|1> Winners**

### Members
- Satvik
- Kaushik
- Chirag

### Contact
[satvikkoppu9@gmail.com](mailto:satvikkoppu9@gmail.com)


Project:

# BB84 Quantum Key Distribution Simulation using Qiskit

This project simulates the BB84 Quantum Key Distribution protocol using Qiskit. The BB84 protocol is a method for securely distributing cryptographic keys between two parties using quantum mechanics principles.

## Prerequisites
Ensure you have the following installed:
- Python 3.x
- Qiskit ([Installation Guide](https://qiskit.org/documentation/install.html))

To install Qiskit, run:
```bash
pip install qiskit
```

## How the Code Works

### Step 1: Alice Prepares Random Bits and Bases
- Alice generates 8 random bits (`0` or `1`).
- She also generates 8 random bases (`X` or `Z`).

### Step 2: Alice Encodes Qubits
- Each bit is encoded as follows:
  - In the `Z` basis: `0` -> `|0⟩`, `1` -> `|1⟩`
  - In the `X` basis: `0` -> `|+⟩`, `1` -> `|-⟩`

### Step 3: Bob Chooses Random Bases
- Bob generates 8 random bases (`X` or `Z`) for measurement.

### Step 4: Bob Measures the Qubits
- Bob applies a Hadamard gate if measuring in the `X` basis before measurement.

### Step 5: Simulation
- The quantum circuit is transpiled and run on Qiskit's `AerSimulator` backend.

### Step 6: Display Results
- Alice's bits, Alice's bases, Bob's bases, and Bob's measurement results are displayed.

### Step 7: Key Extraction
- Alice and Bob compare their bases.
- Only the bits corresponding to matching bases are kept to form the final shared key.

## Running the Code
1. Copy the provided Python code into a file (e.g., `bb84_qkd.py`).
2. Run the file using Python:
   ```bash
   python bb84_qkd.py
   ```
3. The output will display:
   - Alice's bits and bases
   - Bob's bases
   - Bob's measurement results
   - The final shared key

## Sample Output
```
Alice's bits:  [0, 1, 0, 1, 1, 0, 1, 0]
Alice's bases: ['Z', 'X', 'X', 'Z', 'X', 'Z', 'Z', 'X']
Bob's bases:   ['X', 'X', 'Z', 'Z', 'X', 'X', 'Z', 'Z']
Measurement Results:  {'01101010': 1}
Final Shared Key:  [0, 1, 1, 0]
```

## Explanation of Key Exchange
- The final shared key is extracted from the bits where Alice's and Bob's bases match.
- This shared key can now be used for secure communication.


