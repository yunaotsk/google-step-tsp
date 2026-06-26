#!/usr/bin/env python3

import sys
import math
import random
from common import print_tour, read_input

def distance(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def precompute_distances(cities, indices):
    """Precomputes a local distance matrix for a subset of cities."""
    n = len(indices)
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = distance(cities[indices[i]], cities[indices[j]])
            matrix[i][j] = d
            matrix[j][i] = d
    return matrix

def solve_subtour_sa(cities, indices, steps=50000):
    """Solves a small subset of cities using 2-opt with Simulated Annealing."""
    n = len(indices)
    if n <= 1:
        return indices
    if n == 2:
        return indices
        
    dist_matrix = precompute_distances(cities, indices)
    
    # Initial Greedy Tour within this sub-region
    tour = [0]
    unvisited = set(range(1, n))
    while unvisited:
        last = tour[-1]
        next_city = min(unvisited, key=lambda c: dist_matrix[last][c])
        tour.append(next_city)
        unvisited.remove(next_city)
        
    # Calculate initial cost
    current_cost = sum(dist_matrix[tour[i]][tour[(i+1)%n]] for i in range(n))
    
    # Simulated Annealing parameters
    t_start = 100.0
    t_end = 0.1
    
    for step in range(steps):
        t = t_start * (t_end / t_start) ** (step / steps) # Exponential cooling
        
        # Pick two random cut points
        i = random.randint(0, n - 2)
        j = random.randint(i + 2, n - 1)
        if i == 0 and j == n - 1:
            continue
            
        next_i = tour[i + 1]
        next_j = tour[(j + 1) % n]
        
        # Change in distance if we reverse tour[i+1 : j+1]
        old_edges = dist_matrix[tour[i]][next_i] + dist_matrix[tour[j]][next_j]
        new_edges = dist_matrix[tour[i]][tour[j]] + dist_matrix[next_i][next_j]
        diff = new_edges - old_edges
        
        # SA Acceptance Criterion
        if diff < 0 or random.random() < math.exp(-diff / t):
            tour[i + 1:j + 1] = reversed(tour[i + 1:j + 1])
            current_cost += diff
            
    # Return the mapped global indices
    return [indices[idx] for idx in tour]

def solve(cities):
    N = len(cities)
    
    # For Challenge 6 and smaller datasets, use full Simulated Annealing
    if N < 3000:
        return solve_subtour_sa(cities, list(range(N)), steps=200000)
        
    # For Challenge 7 (8,192 cities), use Divide and Conquer
    # Grid division (8x8 grid = 64 regions)
    K = 8
    xs = [c[0] for c in cities]
    ys = [c[1] for c in cities]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Create grid bins
    grid = [[[] for _ in range(K)] for _ in range(K)]
    
    for idx, (x, y) in enumerate(cities):
        bin_x = min(int((x - min_x) / (max_x - min_x + 1e-9) * K), K - 1)
        bin_y = min(int((y - min_y) / (max_y - min_y + 1e-9) * K), K - 1)
        grid[bin_x][bin_y].append(idx)
        
    # Traverse the grid cells in a "snake/boustrophedon" pattern to maintain proximity
    final_tour = []
    for r in range(K):
        # Reverse every alternate row direction to keep path continuous
        columns = range(K) if r % 2 == 0 else range(K - 1, -1, -1)
        for c in columns:
            cell_indices = grid[r][c]
            if cell_indices:
                # Solve this grid block efficiently with SA
                sub_tour = solve_subtour_sa(cities, cell_indices, steps=15000)
                final_tour.extend(sub_tour)
                
    return final_tour

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)