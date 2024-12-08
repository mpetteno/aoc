import copy
from collections import defaultdict
from typing import Tuple, Dict, List


def parse_input() -> Tuple[int, int, Dict[str, Tuple[int, int]]]:
    with open('input.txt') as f:
        lines = f.readlines()
        rows, cols = len(lines), len(lines[0].strip())
        antennas_locs = defaultdict(list)
        for i in range(rows):
            for j in range(cols):
                if lines[i][j] != '.':
                    antenna_freq = lines[i][j]
                    antennas_locs[antenna_freq].append((i, j))
    return rows, cols, antennas_locs


def find_antinode_locations(antenna_locs: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    locations = []
    for i in range(len(antenna_locs)):
        curr_antenna_loc = antenna_locs[i]
        for j in range(i + 1, len(antenna_locs)):
            antenna_to_check = antenna_locs[j]
            distance = curr_antenna_loc[0] - antenna_to_check[0], curr_antenna_loc[1] - antenna_to_check[1]

            antinode_a = curr_antenna_loc[0] + distance[0], curr_antenna_loc[1] + distance[1]
            if 0 <= antinode_a[0] < R and 0 <= antinode_a[1] < C:
                locations.append(antinode_a)

            antinode_b = antenna_to_check[0] - distance[0], antenna_to_check[1] - distance[1]
            if 0 <= antinode_b[0] < R and 0 <= antinode_b[1] < C:
                locations.append(antinode_b)
    return locations


def find_repeated_antinode_locations(antenna_locs: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    locations = copy.deepcopy(antenna_locs) if len(antenna_locs) > 1 else []
    for i in range(len(antenna_locs)):
        curr_antenna_loc = antenna_locs[i]
        for j in range(i + 1, len(antenna_locs)):
            antenna_to_check = antenna_locs[j]
            distance = curr_antenna_loc[0] - antenna_to_check[0], curr_antenna_loc[1] - antenna_to_check[1]

            antinode_a = curr_antenna_loc[0] + distance[0], curr_antenna_loc[1] + distance[1]
            while 0 <= antinode_a[0] < R and 0 <= antinode_a[1] < C:
                locations.append(antinode_a)
                antinode_a = antinode_a[0] + distance[0], antinode_a[1] + distance[1]

            antinode_b = antenna_to_check[0] - distance[0], antenna_to_check[1] - distance[1]
            while 0 <= antinode_b[0] < R and 0 <= antinode_b[1] < C:
                locations.append(antinode_b)
                antinode_b = antinode_b[0] - distance[0], antinode_b[1] - distance[1]
    return locations


if __name__ == '__main__':
    R, C, antennas_locations = parse_input()
    antinodes = set()
    repeated_antinodes = set()
    for antenna_frequency in antennas_locations:
        antenna_locations = antennas_locations[antenna_frequency]
        # Part 1
        antinode_locations = find_antinode_locations(antenna_locations)
        for a in antinode_locations:
            antinodes.add(a)
        # Part 2
        repeated_antinode_locations = find_repeated_antinode_locations(antenna_locations)
        for a in repeated_antinode_locations:
            repeated_antinodes.add(a)
    print(f'(Part 1) Unique antinode locations: {len(antinodes)}')
    print(f'(Part 2) Repeated antinode locations: {len(repeated_antinodes)}')
