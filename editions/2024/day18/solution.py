import heapq
from typing import Any

from solvers.py_solver import Solver

ROWS, COLS = 71, 71
START_X, START_Y = 0, 0
END_X, END_Y = ROWS - 1, COLS - 1
GRID = [["."] * COLS for _ in range(ROWS)]


def shortest_path():
    # Dimensions of the grid
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Priority queue for Dijkstra's algorithm
    priority_queue = [(0, 0, 0)]  # (distance, row, col)
    distances = [[float('inf')] * COLS for _ in range(ROWS)]
    distances[START_X][START_Y] = 0  # Start point

    while priority_queue:
        dist, x, y = heapq.heappop(priority_queue)
        # If we reached the bottom-right corner
        if x == END_X and y == END_Y:
            return dist
        # Process neighbors
        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            # Check boundaries and if the cell is visitable
            if 0 <= next_x < ROWS and 0 <= next_y < COLS and GRID[next_x][next_y] != "#":
                new_dist = dist + 1  # Move costs 1 step
                if new_dist < distances[next_x][next_y]:
                    distances[next_x][next_y] = new_dist
                    heapq.heappush(priority_queue, (new_dist, next_x, next_y))
    # If no path is found
    return -1


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        parsed_bytes = [tuple(map(int, l.split(","))) for l in lines]
        return parsed_bytes

    def solve_first_part(self, parsed_input: Any) -> str:
        falling_bytes = parsed_input
        for i, j in falling_bytes[:1024]:
            GRID[j][i] = "#"
        minimum_steps = shortest_path()
        return f'Minimum number of steps to reach the bottom-right corner: {minimum_steps}'

    def solve_second_part(self, parsed_input: Any) -> str:
        falling_bytes = parsed_input
        for i, j in falling_bytes[1024:]:
            GRID[j][i] = "#"
            minimum_steps = shortest_path()
            if minimum_steps == -1:
                return f'The exit is blocked from byte: {i},{j}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
