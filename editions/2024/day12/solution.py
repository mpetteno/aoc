from collections import defaultdict
from typing import Any

from solvers.python_solver import Solver


CORNERS_DIRECTIONS = [
    [(-1, 0), (0, 1)],   # Up/Right
    [(0, 1), (1, 0)],    # Right/Down
    [(1, 0), (0, -1)],   # Down/Left
    [(0, -1), (-1, 0)]   # Left/Up
]


def bfs(rows, cols, garden):
    regions_dict = defaultdict(list)
    visited_plots = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if visited_plots[i][j]:
                continue
            curr_plot = garden[i][j]
            curr_region = []
            queue = [(i, j)]
            visited_plots[i][j] = 1
            while queue:
                x, y = queue.pop(0)
                touched_plot = 0
                corners = 0
                for d1, d2 in CORNERS_DIRECTIONS:
                    dx, dy = d1
                    du, dv = d2
                    next_x, next_y = x + dx, y + dy
                    next_u, next_v = x + du, y + dv
                    corner_x, corner_y = x + dx + du, y + dy + dv
                    if 0 <= next_x < rows and 0 <= next_y < cols and garden[next_x][next_y] == curr_plot:
                        # Add next plot to queue to visit and update touched plots count
                        touched_plot += 1
                        if not visited_plots[next_x][next_y]:
                            queue.append((next_x, next_y))
                            visited_plots[next_x][next_y] = 1
                        # Check for corners
                        if 0 <= next_u < rows and 0 <= next_v < cols and garden[next_u][next_v] == curr_plot:
                            # If the neighbour in the other direction is part of the region, check the diagonal element.
                            # There is a corner in the direction du, dv if the diagonal element is not part of the
                            # region, or it is not in the grid boundaries.
                            if 0 <= corner_x < rows and 0 <= corner_y < cols:
                                if garden[corner_x][corner_y] != curr_plot:
                                    corners += 1
                            else:
                                corners += 1
                    # If both neighbours in the du and dv directions are not part of the region or outside the grid
                    # boundaries we have a corner in the du, dv direction
                    elif 0 <= next_u < rows and 0 <= next_v < cols:
                        if garden[next_u][next_v] != curr_plot:
                            corners += 1
                    else:
                        corners += 1
                curr_region.append((x, y, touched_plot, corners))
            regions_dict[curr_plot].append(curr_region)
    return regions_dict


class Solution(Solver):

    def parse_input(self) -> Any:
        area_map = self.input_data.splitlines()
        rows, cols = len(area_map), len(area_map[0])
        return rows, cols, area_map

    def solve_first_part(self, parsed_input: Any) -> str:
        rows, cols, garden = parsed_input
        regions_map = bfs(rows, cols, garden)
        garden_cost = 0
        for region_id, regions in regions_map.items():
            for region in regions:
                region_area = len(region)
                region_perimeter = sum([4 - n for _, _, n, _ in region])
                garden_cost += region_area * region_perimeter
        return f'Garden cost is {garden_cost}'

    def solve_second_part(self, parsed_input: Any) -> str:
        rows, cols, garden = parsed_input
        regions_map = bfs(rows, cols, garden)
        garden_discounted_cost = 0
        for region_id, regions in regions_map.items():
            for region in regions:
                region_area = len(region)
                region_sides = sum([n for _, _, _, n in region])
                garden_discounted_cost += region_area * region_sides
        return f'Discounted garden cost is {garden_discounted_cost}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
