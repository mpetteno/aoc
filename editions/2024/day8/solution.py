import copy
from collections import defaultdict
from typing import Tuple, List, Any, Callable

from solvers.python_solver import Solver


def find_antinode_locs(antenna_locs: List[Tuple[int, int]], rows: int, cols: int) -> List[Tuple[int, int]]:
    locations = []
    for i in range(len(antenna_locs)):
        curr_antenna_loc = antenna_locs[i]
        for j in range(i + 1, len(antenna_locs)):
            antenna_to_check = antenna_locs[j]
            distance = curr_antenna_loc[0] - antenna_to_check[0], curr_antenna_loc[1] - antenna_to_check[1]

            antinode_a = curr_antenna_loc[0] + distance[0], curr_antenna_loc[1] + distance[1]
            if 0 <= antinode_a[0] < rows and 0 <= antinode_a[1] < cols:
                locations.append(antinode_a)

            antinode_b = antenna_to_check[0] - distance[0], antenna_to_check[1] - distance[1]
            if 0 <= antinode_b[0] < rows and 0 <= antinode_b[1] < cols:
                locations.append(antinode_b)
    return locations


def find_repeated_antinode_locs(antenna_locs: List[Tuple[int, int]], rows: int, cols: int) -> List[Tuple[int, int]]:
    locations = copy.deepcopy(antenna_locs) if len(antenna_locs) > 1 else []
    for i in range(len(antenna_locs)):
        curr_antenna_loc = antenna_locs[i]
        for j in range(i + 1, len(antenna_locs)):
            antenna_to_check = antenna_locs[j]
            distance = curr_antenna_loc[0] - antenna_to_check[0], curr_antenna_loc[1] - antenna_to_check[1]

            antinode_a = curr_antenna_loc[0] + distance[0], curr_antenna_loc[1] + distance[1]
            while 0 <= antinode_a[0] < rows and 0 <= antinode_a[1] < cols:
                locations.append(antinode_a)
                antinode_a = antinode_a[0] + distance[0], antinode_a[1] + distance[1]

            antinode_b = antenna_to_check[0] - distance[0], antenna_to_check[1] - distance[1]
            while 0 <= antinode_b[0] < rows and 0 <= antinode_b[1] < cols:
                locations.append(antinode_b)
                antinode_b = antinode_b[0] - distance[0], antinode_b[1] - distance[1]
    return locations


def find_antinodes(antenna_locs: List[Tuple[int, int]], rows: int, cols: int, search_fn: Callable) \
        -> List[Tuple[int, int]]:
    antinodes = set()
    for antenna_frequency in antenna_locs:
        antenna_locations = antenna_locs[antenna_frequency]
        antinode_locations = search_fn(antenna_locations, rows, cols)
        for a in antinode_locations:
            antinodes.add(a)
    return antinodes


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        rows, cols = len(lines), len(lines[0].strip())
        antennas_locs = defaultdict(list)
        for i in range(rows):
            for j in range(cols):
                if lines[i][j] != '.':
                    antenna_freq = lines[i][j]
                    antennas_locs[antenna_freq].append((i, j))
        return rows, cols, antennas_locs

    def solve_first_part(self, parsed_input: Any) -> str:
        rows, cols, antennas_locations = parsed_input
        antinodes = find_antinodes(antennas_locations, rows, cols, search_fn=find_antinode_locs)
        return f'Unique antinode locations: {len(antinodes)}'

    def solve_second_part(self, parsed_input: Any) -> str:
        rows, cols, antennas_locations = parsed_input
        repeated_antinodes = find_antinodes(antennas_locations, rows, cols, search_fn=find_repeated_antinode_locs)
        return f'Repeated antinode locations: {len(repeated_antinodes)}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
