# 🏆 Quantum N-Queens Solver using Grover's Algorithm (PennyLane)

## 📚 Overview
This project implements the **N-Queens Problem** using **Grover’s Algorithm** with **PennyLane**. The solution is represented as an `N × N` matrix, where:
- `1` indicates a valid Queen position.
- `0` indicates an invalid position.

Grover’s algorithm is used to search for valid placements efficiently while ensuring no two queens attack each other.

---

## ♟️ The N-Queens Problem
The **N-Queens Problem** is a classical combinatorial problem where `N` queens must be placed on an `N × N` chessboard following these rules:
- No two queens share the same **row**.
- No two queens share the same **column**.
- No two queens share the same **diagonal**.

Instead of brute-force searching, we leverage **Grover’s Algorithm**, which provides a quadratic speedup over classical approaches.

---

## 🏰 Approach & Implementation

### 🔹 **Quantum Encoding**
Each potential board configuration is encoded as a quantum state. The qubits represent queen placements, and quantum operations enforce constraints.

### 🔹 **Oracle Design**
The **oracle function** marks invalid board configurations by applying a phase flip to states violating N-Queens constraints.

### 🔹 **Grover's Diffusion Operator**
The **diffusion operator** amplifies the probability of valid solutions, enhancing the chances of measuring a correct board state.

### 🔹 **Measurement & Interpretation**
The quantum circuit is executed multiple times to extract valid configurations. The results are interpreted as an `N x N` matrix.

---

## 💪 Features
- **Quantum Speedup**: Uses Grover’s algorithm for efficient search.
- **PennyLane Implementation**: Runs on simulators and real quantum hardware.
- **Matrix Representation**: Outputs a chessboard-like matrix solution.

---

## 📚 Installation
Python and required dependencies: 

```bash
pip install pennylane numpy matplotlib
```

---

## 🚀 Usage
Run the script to find valid queen placements:

```bash
python QuantaNqueens.ipynb
```

### 📝 Example Output
For `N = 4`, a valid solution matrix might look like:
```
0  1  0  0
0  0  0  1
1  0  0  0
0  0  1  0
```

---

## 📊 Performance
- **Classical Brute Force Complexity**: `O(N!)`
- **Quantum Grover's Algorithm Complexity**: `O(sqrt(N!))`

---

## 📚 Future Enhancements
- Extend to larger `N` using optimized quantum circuits.
- Implement on real quantum processors (IBM Q, Rigetti, etc.).
- Improve oracle design for better performance.

---


