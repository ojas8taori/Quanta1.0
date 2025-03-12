# Quantum Digital Signature (QDS) - Quanta 1.0  

## 📌 Overview  
This project demonstrates a **Quantum Digital Signature (QDS)** using Qiskit. A quantum signature state is created and verified by multiple parties. Any attempt to forge the signature is detected with a high probability.

## 🔧 How It Works  
1. **Signature Creation**  
   - A quantum circuit is initialized with a single qubit.  
   - A rotation (`RY(π/4)`) is applied to create the signature state.  

2. **Verification**  
   - The quantum signature is distributed to verifiers.  
   - Each verifier measures the state in either the `0°` or `45°` basis randomly.  
   - The success rate of each verifier is calculated.

3. **Forgery Attempt**  
   - An attacker (Huccha Venkat) tries to modify the signature state.  
   - The attack is detected by low success rates.

## 🛠️ Installation  

Team Members:
ANSHUMANTH MULGUND
