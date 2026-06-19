#!/usr/bin/env python3

import sys

from common import print_tour, read_input


def solve(cities):
    def distance(city1, city2):
        return ((city1[0] - city2[0]) ** 2 + (city1[1] - city2[1]) ** 2) ** 0.5
    visited = [0]
    for i in range(1, len(cities)):
        last_city = visited[-1]
        next_city = None
        min_dist = float('inf')
        for idx, city in enumerate(cities):
            if idx in visited:
                continue
            dist = distance(cities[last_city], city)
            if dist < min_dist:
                min_dist = dist
                next_city = idx
        visited.append(next_city)
    for i in range(len(visited) - 2):
        for j in range(i + 2, len(visited) - 1):
            old_dist = distance(cities[visited[i]], cities[visited[i + 1]]) + distance(cities[visited[j]], cities[visited[j + 1]])
            new_dist = distance(cities[visited[i]], cities[visited[j]]) + distance(cities[visited[i + 1]], cities[visited[j + 1]])
            if new_dist < old_dist:
                visited[i + 1 : j + 1] = reversed(visited[i + 1 : j + 1])
    return visited


if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
