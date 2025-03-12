import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile  
from qiskit_aer import AerSimulator  
import numpy as np  
import random  

# Darshan setting up the quantum signature  
def create_qds_state():
    qc = QuantumCircuit(1, 1)  
    qc.ry(np.pi / 4, 0)  
    print("Signature State Created")
    qc.draw('mpl')  # Use 'mpl' to draw using Matplotlib
    try:
        plt.show()  # Ensure the plot is displayed
    except Exception as e:
        print(f"Error displaying plot: {e}")
    return qc  

# Verifiers checking if signature is legit  
def verify_qds(qc, verifier_name):
    backend = AerSimulator()  
    basis_choice = random.choice([0, np.pi/4])  
    print(f"{verifier_name} measuring in {'0°' if basis_choice == 0 else '45°'} basis")  

    if basis_choice == np.pi/4:
        qc.ry(-np.pi/4, 0)  

    qc.measure(0, 0)  
    transpiled_qc = transpile(qc, backend)  
    result = backend.run(transpiled_qc, shots=16).result()  
    counts = result.get_counts()  

    print(f"{verifier_name} got: {counts}")  
    print(f"{verifier_name} success rate: {counts.get('0', 0) / 16:.2f}\n")  
    qc.draw('mpl')  # Draw the quantum circuit after the verification
    plt.show()  # Ensure the plot is displayed

# Darshan sending the quantum signature  
print("Darshan creating a quantum signature...")  
signature_qc = create_qds_state()  

# The boys checking the signature  
verifiers = {  
    "Puneet": signature_qc.copy(),  
    "Kiccha": signature_qc.copy(),  
    "Sudeep": signature_qc.copy()  
}  

for name, qc in verifiers.items():  
    print(f"{name} verifying...")  
    verify_qds(qc, name)  

# Huccha Venkat trying to pull scene 
fake_qc = signature_qc.copy()  
fake_qc.ry(np.pi / 3, 0)  

print("Huccha Venkat attempting fraud...")  
verify_qds(fake_qc, "Huccha Venkat (Attacker)")  
