# Team Name "Short & Circuit"

# Quantum Random Number Generator (QRNG)

# Overview

The Quantum Random Number Generator (QRNG) leverages quantum mechanics to produce truly random numbers. Unlike classical random number generators that rely on deterministic algorithms (making them pseudo-random), quantum superposition ensures genuine randomness. This project implements a QRNG using quantum circuits, making it suitable for cryptographic applications.

# Problem Statement

Creating a 'Quantum Random Number Generator' for cryptograpic applications

# Implementation Details

Quantum Representation A qubit is initialized in a superposition state using the Hadamard gate. When measured, the qubit collapses into either |0⟩ or |1⟩ with equal probability, ensuring true randomness.

## Quantum Circuit Design Initialization:
Apply a Hadamard gate to create a 50/50 superposition of |0⟩ and |1⟩.
## Measurement: 
Collapse the quantum state by measuring it in the computational basis. 
## Bitstream Generation:
Execute the quantum circuit multiple times to generate a sequence of random bits. 
## Post-Processing: 
Classical techniques (such as randomness extraction) can be applied to remove bias if necessary.

# Tools & Libraries Used

## Qiskit: 
For quantum circuit simulation and execution. 
## Python:
To implement logic and control program flow. 
## Matplotlib & NumPy: 
For data visualization and statistical analysis of generated random numbers.

# Code Explanation

## The Jupyter Notebook includes:
Quantum circuit construction for QRNG. Execution of multiple iterations to generate random bit sequences. Statistical analysis to verify uniform randomness.

## Results & Insights 
The generated bits exhibit uniform randomness, proving the effectiveness of quantum mechanics for secure random number generation. QRNGs are superior to classical RNGs in cryptographic applications due to their true unpredictability. Further analysis can explore randomness extraction methods to enhance cryptographic security.

# Future Scope
Implement QRNG on real quantum hardware to validate randomness. Expand the system to generate multi-bit random numbers in parallel.

# How to Run the Project

## Install dependencies: 
Import the required libraries. pip install qiskit, matplotlib, numpy. Open the Jupyter Notebook and run all cells. Observe the quantum circuit execution and analyze the generated random numbers.

# Developers 
Girija Shailesh Ambardekar ,
Prathamesh Balkrishna Desai

# References
Research papers on Quantum Random Number Generators

# Contact 
1) Prathamesh Desai
+91 7038501526 / spratham1526@gmail.com

2) Girija Ambardekar
+91 9284734426  / girijaambardekar08@gmail.com
