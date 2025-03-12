# Quantum Monty Hall Problem

## Overview
The Quantum Monty Hall Problem is a quantum variant of the classic Monty Hall game show paradox. This project explores the quantum mechanics behind decision-making strategies using quantum gates and measurements.

## Problem Statement
The traditional Monty Hall Problem involves a game show where a contestant selects one of three doors, behind one of which is a prize. The host, who knows the prize location, opens another door without the prize. The contestant is then given a choice to stick with their original selection or switch. Classical probability suggests switching increases the chances of winning.

In the quantum version, doors are represented as quantum states, and quantum superposition and entanglement play a role in determining the outcomes.

## Implementation Details

### 1. Quantum Representation
- The doors are encoded as quantum states.
- The contestant's choice is represented by a quantum superposition.
- The host's knowledge is entangled with the system.

### 2. Quantum Circuit Design
- **Initialization:** The system is initialized in a superposition state using Hadamard gates.
- **Monty’s Choice:** Quantum gates are applied to simulate Monty opening a door.
- **Contestant’s Decision:** The contestant can use quantum operations to switch or stay.
- **Measurement:** The quantum system is measured to determine the outcome.

### 3. Tools & Libraries Used
- **Qiskit:** For quantum simulation and circuit construction.
- **Python:** To script the logic and visualization.
- **Matplotlib & NumPy:** For result visualization and analysis.

## Code Explanation
- The Jupyter Notebook contains:
  - Quantum circuit construction
  - Simulation of different strategies
  - Probability analysis and results

## Results & Insights
- The quantum strategy exhibits different probabilities compared to classical outcomes.
- The advantage of switching is still present but depends on quantum interference effects.

## Future Scope
- Extend the model to a higher-dimensional Hilbert space.
- Experiment with different quantum strategies and analyze their effectiveness.
- Implement real quantum hardware execution.

## How to Run the Project
1. Install dependencies:
   ```sh
   pip install qiskit matplotlib numpy
   ```
2. Open the Jupyter Notebook and run all cells.
3. Observe the quantum circuit and probability distributions.

## Contributors
- 1.Rohit Shitalkumar Mudakude
- 2.Rishav Kumar Agrawal
- 3.S.S.Skandan 

## Team Name 
- ~ ATOM ~

## References
- [Qiskit Documentation](https://qiskit.org/documentation/)



