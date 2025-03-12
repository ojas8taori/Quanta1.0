from qiskit import QuantumCircuit, transpile
import string, random
import matplotlib.pyplot as plt  # For circuit visualization

# Quantum circuit with 8 qubits
qc = QuantumCircuit(8)
qc.h(range(8))  # Apply Hadamard gates to create superposition
qc.measure_all()  # Measure all qubits

# Visualize the circuit
qc.draw("mpl")
plt.show()


# Define character sets for password generation
uppercase = string.ascii_uppercase  # A-Z
special_chars = "!@#$%^&*"
characters = string.ascii_letters + string.digits + special_chars  # A-Z, a-z, 0-9, symbols

# Function to generate a valid password
def generate_password():
    while True:
        password = ''.join(random.choice(characters) for _ in range(8))
        if any(c in uppercase for c in password) and any(c in special_chars for c in password):
            return password

# Generate a secure password
password = generate_password()
print("Quantum-Generated Password:", password)