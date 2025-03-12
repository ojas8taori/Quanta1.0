import math
import numpy as np
import dimod

def create_data_model():
   
    data = {}
   
    data["locations"] = [
         (288, 129),(256, 141), (270, 133),  (256, 157), (288, 149)
    ]
    return data

def compute_distance_matrix(locations):
    
    n = len(locations)
    dist = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            dist[i, j] = math.hypot(locations[i][0] - locations[j][0],
                                    locations[i][1] - locations[j][1])
    return dist

def build_tsp_qubo(dist, A=1000, B=1000):
    
    n = len(dist)
    Q = {}

   
    for i in range(n):
        for j in range(n):
            idx = i * n + j
            
            Q[(idx, idx)] = Q.get((idx, idx), 0) - 2 * A
        for j in range(n):
            for k in range(j + 1, n):
                idx1 = i * n + j
                idx2 = i * n + k
                Q[(idx1, idx2)] = Q.get((idx1, idx2), 0) + 2 * A

    
    for j in range(n):
        for i in range(n):
            idx = i * n + j
            Q[(idx, idx)] = Q.get((idx, idx), 0) - 2 * B
        for i in range(n):
            for k in range(i + 1, n):
                idx1 = i * n + j
                idx2 = k * n + j
                Q[(idx1, idx2)] = Q.get((idx1, idx2), 0) + 2 * B

   
    for j in range(n):
        j_next = (j + 1) % n
        for i in range(n):
            for k in range(n):
                if i != k:
                    idx1 = i * n + j
                    idx2 = k * n + j_next
                    Q[(idx1, idx2)] = Q.get((idx1, idx2), 0) + dist[i][k]
    return Q

def solve_tsp_qubo(Q):
   
    bqm = dimod.BinaryQuadraticModel.from_qubo(Q)
    sampler = dimod.ExactSolver()
    sample_set = sampler.sample(bqm)
    best_sample = sample_set.first.sample
    best_energy = sample_set.first.energy
    return best_sample, best_energy

def parse_solution(sample, n):

    tour = [-1] * n
    for i in range(n):
        for j in range(n):
            idx = i * n + j
            if sample.get(idx, 0) == 1:
                tour[j] = i
    return tour

def main():
    
    data = create_data_model()
    locations = data["locations"]
    n = len(locations)

    
    dist = compute_distance_matrix(locations)

    
    Q = build_tsp_qubo(dist, A=1000, B=1000)

    
    best_sample, energy = solve_tsp_qubo(Q)


    tour = parse_solution(best_sample, n)
    print("Best tour (by city indices):", tour)
    print("Energy (objective value):", energy)

if __name__ == "__main__":
    main()