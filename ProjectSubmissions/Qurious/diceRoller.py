from qiskit import QuantumCircuit
from qiskit_aer import Aer  # Import Aer from qiskit_aer
for i in range(10):
    # Step 1: Create a quantum circuit with 3 qubits and 3 classical bits
    qc = QuantumCircuit(3, 3)

    # Step 2: Apply Hadamard gates to all qubits (creates superposition)
    qc.h(0)
    qc.h(1)
    qc.h(2)

    # Step 3: Measure all qubits
    qc.measure([0, 1, 2], [0, 1, 2])

    # Step 4: Simulate the circuit using Qiskit's simulator
    simulator = Aer.get_backend('qasm_simulator')
    job = simulator.run(qc, shots=1)  # Run the circuit once
    result = job.result()  # Get the result

    # Step 5: Get the measurement result
    counts = result.get_counts(qc)
    outcome = list(counts.keys())[0]  # Get the measured state (e.g., '101')

    # Step 6: Map the outcome to a dice roll (1-6)
    dice_map = {
        '000': 1,
        '001': 2,
        '010': 3,
        '011': 4,
        '100': 5,
        '101': 6
    }

    # Step 7: Check if the outcome is valid
    if outcome in dice_map:
        print(f"Dice roll: {dice_map[outcome]}")
    else:
        print("Re-rolling... (invalid outcome)")