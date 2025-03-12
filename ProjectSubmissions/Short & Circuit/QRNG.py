import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

class QuantumRandomNumberGenerator:
    def __init__(self, num_qubits=4):
       
        self.num_qubits = num_qubits
        self.simulator = Aer.get_backend('qasm_simulator')
    
    def generate_circuit(self):
        
        
        circuit = QuantumCircuit(self.num_qubits, self.num_qubits)
        
       
        for qubit in range(self.num_qubits):
            circuit.h(qubit)  
        circuit.measure(range(self.num_qubits), range(self.num_qubits))
        
        return circuit
    
    def generate_random_number(self, shots=1):
       
        circuit = self.generate_circuit()
        
       
        job = self.simulator.run(circuit, shots=shots)
        result = job.result()
        
       
        counts = result.get_counts(circuit)
        
       
        random_numbers = []
        for bitstring, count in counts.items():
            integer_value = int(bitstring, 2)  
            random_numbers.extend([integer_value] * count)
        
       
        if random_numbers:
            np.random.shuffle(random_numbers)
        
        return random_numbers
    
    def visualize_distribution(self, num_samples=1024):
       
        circuit = self.generate_circuit()
        
       
        job = self.simulator.run(circuit, shots=num_samples)
        result = job.result()
        
        # Plot the distribution
        counts = result.get_counts(circuit)
        plot_histogram(counts)
        plt.title(f"Distribution of {num_samples} Random Numbers")
        plt.xlabel("Generated Value (Binary)")
        plt.ylabel("Frequency")
        plt.show()
    
    def generate_random_bits(self, num_bits):
       
       
        num_executions = (num_bits + self.num_qubits - 1) // self.num_qubits
        
        bits = ""
        for _ in range(num_executions):
            numbers = self.generate_random_number(shots=1)
            if numbers:  
                number = numbers[0]
               
                binary = bin(number)[2:].zfill(self.num_qubits)
                bits += binary
            else:
                
                bits += ''.join([str(np.random.randint(0, 2)) for _ in range(self.num_qubits)])
        
       
        return bits[:num_bits]
    
    def generate_random_int(self, min_val=0, max_val=100):
       
       
        range_size = max_val - min_val + 1
        bits_needed = (range_size - 1).bit_length()
        
        # Generate random bits
        while True:
            random_bits = self.generate_random_bits(bits_needed)
            value = int(random_bits, 2)
            
           
            if value < range_size:
                return value + min_val

# Example usage
if __name__ == "__main__":
    print("Quantum Random Number Generator (QRNG) Demo")
    print("-------------------------------------------")
    
   
    qrng = QuantumRandomNumberGenerator(num_qubits=4)
    
    # Show the quantum circuit
    circuit = qrng.generate_circuit()
    print("Quantum Circuit:")
    print(circuit)
    
    
    random_numbers = qrng.generate_random_number(shots=1)
    if random_numbers:
        print(f"\nGenerated random number: {random_numbers[0]}")
    else:
        print("\nFailed to generate a random number.")
    
    
    random_bits = qrng.generate_random_bits(32)
    print(f"\nGenerated 32 random bits: {random_bits}")
    
   
    random_int = qrng.generate_random_int(1, 100)
    print(f"\nRandom integer between 1 and 100: {random_int}")
    
    
    print("\nGenerating distribution visualization...")
    qrng.visualize_distribution(1024)
