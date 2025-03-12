from qiskit import qiskit_aer
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram

import random

# BB84 Quantum Key Distribution

# Step 1: Alice prepares random bits and random bases
alice_bits = [random.randint(0, 1) for _ in range(8)]
alice_bases = [random.choice(['X', 'Z']) for _ in range(8)]

# Step 2: Alice encodes qubits based on her random bits and bases
qc = QuantumCircuit(8)
for i in range(8):
    if alice_bits[i] == 1:
        qc.x(i)  # Encode '1'
    if alice_bases[i] == 'X':
        qc.h(i)  # Encode in Hadamard (X) basis


# Step 3: Bob chooses random bases to measure
bob_bases = [random.choice(['X', 'Z']) for _ in range(8)]

# Step 4: Bob measures
for i in range(8):
    if bob_bases[i] == 'X':
        qc.h(i)
    qc.measure_all()

# Step 5: Simulate
simulator = AerSimulator.get_backend('aer_simulator')
qc = transpile(qc, simulator)
result = simulator.run(qc).result()

# Step 6: Display Results
print("Alice's bits: ", alice_bits)
print("Alice's bases:", alice_bases)
print("Bob's bases:  ", bob_bases)
print("Measurement Results: ", result.get_counts())

# Step 7: Key Extraction
bob_results = list(result.get_counts().keys())[0]
final_key = [
    alice_bits[i] for i in range(8)
    if alice_bases[i] == bob_bases[i]  # Only keep matching bases
]
print("Final Shared Key: ", final_key)

