import numpy as np
from qiskit import Aer, execute
from qiskit.optimization import QuadraticProgram
from qiskit.algorithms.optimizers import COBYLA
from qiskit_optimization.algorithms import MinimumEigenOptimizer
from qiskit.algorithms.minimum_eigensolvers import QAOA
from qiskit.primitives import Sampler
from qiskit_optimization.translators import from_docplex_mp
from docplex.mp.model import Model

# Step 1: Generate a random symmetric distance matrix
def generate_distance_matrix(num_locations, max_distance=10):
    distance_matrix = np.random.randint(1, max_distance, size=(num_locations, num_locations))
    distance_matrix = (distance_matrix + distance_matrix.T) // 2  # Make it symmetric
    np.fill_diagonal(distance_matrix, 0)  # No self-travel cost
    return distance_matrix

# Step 2: Generate a QUBO problem for QAOA with proper constraints
def create_qubo_problem(distance_matrix):
    num_locations = len(distance_matrix)
    mdl = Model("Route Optimization")
    
    # Binary variables: x[i, j] represents visiting city i at position j in the route
    x = {(i, j): mdl.binary_var(name=f"x_{i}_{j}") for i in range(num_locations) for j in range(num_locations)}

    # Objective: Minimize total distance traveled
    cost = mdl.sum(distance_matrix[i][k] * x[i, j] * x[k, (j + 1) % num_locations] 
                   for i in range(num_locations) for k in range(num_locations) 
                   for j in range(num_locations) if i != k)
    mdl.minimize(cost)

    # Constraints: Each city is visited exactly once
    for i in range(num_locations):
        mdl.add_constraint(mdl.sum(x[i, j] for j in range(num_locations)) == 1)
    
    # Constraints: Each position in the route is occupied by exactly one city
    for j in range(num_locations):
        mdl.add_constraint(mdl.sum(x[i, j] for i in range(num_locations)) == 1)

    return from_docplex_mp(mdl)

# Step 3: Solve using QAOA
def solve_qaoa(qubo_problem):
    sampler = Sampler()
    qaoa = QAOA(sampler=sampler, optimizer=COBYLA())
    qaoa_solver = MinimumEigenOptimizer(qaoa)
    result = qaoa_solver.solve(qubo_problem)
    return result

# Main Execution
num_locations = 5
distance_matrix = generate_distance_matrix(num_locations)
qubo_problem = create_qubo_problem(distance_matrix)
result = solve_qaoa(qubo_problem)

# Print Results
print("Distance Matrix:")
print(distance_matrix)
print("\nOptimal Route (Binary Encoding):", result.x)
print("Optimal Cost:", result.fval)
