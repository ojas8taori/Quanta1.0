# Traveling Salesman Problem (TSP) using QUBO Formulation

--------------------------------------------------------------------------------
**THE FERMIONS**

**Team Members:**
- ATHARVA M
- MANAV DEWANGAN
- AKSHAT AGARWAL

**Contact Information:**
- **Phone:** 9901170033  
- **Email:** matharva@357gmail.com
--------------------------------------------------------------------------------

## Description

This repository contains code that implements a QUBO (Quadratic Unconstrained Binary Optimization) model formulation to solve the Traveling Salesman Problem (TSP). The program computes pairwise Euclidean distances between cities, constructs a QUBO model that encodes the TSP constraints and objective function, and then uses an exact binary quadratic model solver to determine an optimal tour.

## Prerequisites

Before running the code, ensure you have the following installed:

1. **Python 3.6 or Later**  
   - Download from: [python.org/downloads](https://www.python.org/downloads/)

2. **NumPy**  
   - Used for numerical operations and array handling.  
   - Install via pip:
     ```bash
     pip install numpy
     ```

3. **dimod (D-Wave Ocean SDK)**  
   - Required for building and solving the binary quadratic model (BQM).  
   - Install via pip:
     ```bash
     pip install dimod
     ```

4. **Standard Python Library Modules**  
   - The code uses the built-in `math` module, which is included with Python.

## Installation & Setup

1. Clone this repository or download the source code.
2. Ensure you have installed the prerequisites mentioned above.
3. Open your terminal or command prompt, navigate to the project directory, and run the code.

## How to Run

To execute the program, simply run the following command in your terminal:

```bash
python <QUBO(source code)>.py
