from typing import Any

from solvers.py_solver import Solver


def df_visit(trailhead, topographic_map, rows, cols):
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    stack = [trailhead]
    summits_pos = []
    while stack:
        i, j = stack.pop()
        current_slope = int(topographic_map[i][j])
        if current_slope == 9:
            summits_pos.append((i, j))
        else:
            for dx, dy in directions:
                next_x, next_y = i + dx, j + dy
                if 0 <= next_x < rows and 0 <= next_y < cols:
                    next_slope = int(topographic_map[next_x][next_y])
                    if next_slope == current_slope + 1:
                        stack.append((next_x, next_y))
    return summits_pos


class Solution(Solver):

    def parse_input(self) -> Any:
        area_map = self.input_data.splitlines()
        rows, cols = len(area_map), len(area_map[0])
        th = []
        for i in range(rows):
            for j in range(cols):
                current_pos = int(area_map[i][j])
                if current_pos == 0:
                    th.append((i, j))
        return rows, cols, area_map, th

    def solve_first_part(self, parsed_input: Any) -> str:
        rows, cols, topographic_map, trailheads = parsed_input
        scores = []
        for trailhead in trailheads:
            summits = df_visit(trailhead, topographic_map, rows, cols)
            scores.append(len(set(summits)))
        return f'Trailheads total score: {sum(scores)}'

    def solve_second_part(self, parsed_input: Any) -> str:
        rows, cols, topographic_map, trailheads = parsed_input
        ratings = []
        for trailhead in trailheads:
            summits = df_visit(trailhead, topographic_map, rows, cols)
            ratings.append(len(summits))
        return f'Trailheads total rating: {sum(ratings)}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
