#!/usr/bin/env python3
import sys, math, random
from common import print_tour, read_input

random.seed(0)

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def tour_cost(tour, dist):
    n = len(tour)
    return sum(dist[tour[i]][tour[(i + 1) % n]] for i in range(n))

def run_2opt(tour, dist, neighbors):
    n = len(tour)

    pos = [0] * n
    for i, city in enumerate(tour):
        pos[city] = i

    improved = True
    while improved:
        improved = False

        for i in range(n):
            a = tour[i]

            for c in neighbors[a]:
                j = pos[c]

                if j == i or j == (i + 1) % n or j == (i - 1) % n:
                    continue

                l, r = sorted((i, j))

                a, b = tour[l], tour[l + 1]
                c, d = tour[r], tour[(r + 1) % n]

                if dist[a][c] + dist[b][d] < dist[a][b] + dist[c][d]:
                    tour[l + 1:r + 1] = reversed(tour[l + 1:r + 1])

                    for k in range(l + 1, r + 1):
                        pos[tour[k]] = k

                    improved = True

def build_tour(start, order, top_k):
    n = len(order)
    unvisited = set(range(n))
    unvisited.remove(start)

    tour = [start]
    current = start

    while unvisited:
        candidates = []

        for city in order[current]:
            if city in unvisited:
                candidates.append(city)

                if len(candidates) == top_k:
                    break

        next_city = random.choice(candidates)

        unvisited.remove(next_city)
        tour.append(next_city)
        current = next_city

    return tour

def solve(cities):
    n = len(cities)

    dist = [
        [distance(cities[i], cities[j]) for j in range(n)]
        for i in range(n)
    ]

    order = [
        sorted(range(n), key=lambda j: dist[i][j])
        for i in range(n)
    ]

    neighbors = [
        order[i][1:101]
        for i in range(n)
    ]

    best_tour = None
    best_cost = float("inf")

    starts = list(range(min(n, 100)))

    if n > 100:
        starts += random.sample(range(n), min(100, n))

    for start in starts:
        for top_k in [1, 3]:
            tour = build_tour(start, order, top_k)
            run_2opt(tour, dist, neighbors)

            cost = tour_cost(tour, dist)

            if cost < best_cost:
                best_cost = cost
                best_tour = tour[:]

    return best_tour

if __name__ == "__main__":
    cities = read_input(sys.argv[1])
    tour = solve(cities)
    print_tour(tour)

    total = sum(
        distance(cities[tour[i]], cities[tour[(i + 1) % len(tour)]])
        for i in range(len(tour))
    )

    print(f"\nFINAL DISTANCE: {total:.2f}", file=sys.stderr)