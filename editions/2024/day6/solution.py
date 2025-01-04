from collections import defaultdict
from typing import Tuple, Set, Dict, Any

from solvers.py_solver import Solver


DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIR_CHARS = ['^', '>', 'V', '<']


def walk(obstacles, rows, cols, x, y, direction: int) -> [Dict[Tuple[int, int], Set[str]], bool]:
    path = defaultdict(set)
    loop_found = False
    path[(x, y)].add(direction)
    while True:
        dx, dy = DIRECTIONS[direction]
        next_x, next_y = x + dx, y + dy
        # Exit if out of bound
        if next_x < 0 or next_x >= rows or next_y < 0 or next_y >= cols:
            break
        if (next_x, next_y) in obstacles:
            # If the next cell is an obstacle rotate the direction
            direction = (direction + 1) % len(DIRECTIONS)
        else:
            # Otherwise, if we already visit the next cell coming from the current direction it means that we are in
            # a loop, stop walking. Update the current position otherwise.
            if direction in path[(next_x, next_y)]:
                loop_found = True
                break
            x, y = next_x, next_y
        # Add the current position to the path
        path[(x, y)].add(direction)
    return path, loop_found


def print_path(rows, columns, x, y, path, obstacles):
    for i in range(rows):
        print()
        for j in range(columns):
            if (i, j) in obstacles:
                item = '#'
                color = '\033[1;33m'
                print('{}{:3}\033[0m'.format(color, item), end='')
            elif (i, j) in path:
                directions = path[(i, j)]
                item = DIR_CHARS[directions.pop()] if len(directions) == 1 else 'X'
                color = '\033[1;32m' if x != i or y != j else '\033[1;31m'
                print('{}{:3}\033[0m'.format(color, item), end='')
            else:
                item = '.'
                print('{:3}'.format(item), end='')


class Solution(Solver):

    def parse_input(self) -> Any:
        area_map = [list(line.strip()) for line in open('input.txt', 'r').readlines()]
        rows, cols = len(area_map), len(area_map[0])
        init_x, init_y, init_dir = 0, 0, '>'
        obs = set()
        for i in range(rows):
            for j in range(cols):
                current_grid = area_map[i][j]
                if current_grid in DIR_CHARS:
                    init_x, init_y, init_dir = i, j, DIR_CHARS.index(current_grid)
                elif current_grid == '#':
                    obs.add((i, j))
        return rows, cols, init_x, init_y, init_dir, obs

    def solve_first_part(self, parsed_input: Any) -> str:
        rows, cols, start_x, start_y, start_direction, obstructions = parsed_input
        guard_path, _ = walk(obstructions, rows, cols, start_x, start_y, start_direction)
        return f'Distinct visited cells: {len(guard_path)}'

    def solve_second_part(self, parsed_input: Any) -> str:
        rows, cols, start_x, start_y, start_direction, obstructions = parsed_input
        guard_path, _ = walk(obstructions, rows, cols, start_x, start_y, start_direction)
        loop_count = 0
        for x, y in guard_path:
            if x == start_x and y == start_y:
                continue
            obstructions.add((x, y))
            _, loop = walk(obstructions, rows, cols, start_x, start_y, start_direction)
            loop_count += int(loop)
            obstructions.remove((x, y))
        return f'Loop count: {loop_count}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
