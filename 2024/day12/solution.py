from collections import defaultdict

CORNERS_DIRECTIONS = [
    [(-1, 0), (0, 1)],   # Up/Right
    [(0, 1), (1, 0)],    # Right/Down
    [(1, 0), (0, -1)],   # Down/Left
    [(0, -1), (-1, 0)]   # Left/Up
]


def parse_input():
    area_map = [list(line.strip()) for line in open('input.txt', 'r').readlines()]
    rows, cols = len(area_map), len(area_map[0])
    return rows, cols, area_map


def bfs():
    regions_dict = defaultdict(list)
    visited_plots = [[0] * C for _ in range(R)]
    for i in range(R):
        for j in range(C):
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
                    if 0 <= next_x < R and 0 <= next_y < C and garden[next_x][next_y] == curr_plot:
                        # Add next plot to queue to visit and update touched plots count
                        touched_plot += 1
                        if not visited_plots[next_x][next_y]:
                            queue.append((next_x, next_y))
                            visited_plots[next_x][next_y] = 1
                        # Check for corners
                        if 0 <= next_u < R and 0 <= next_v < C and garden[next_u][next_v] == curr_plot:
                            # If the neighbour in the other direction is part of the region, check the diagonal element.
                            # There is a corner in the direction du, dv if the diagonal element is not part of the
                            # region, or it is not in the grid boundaries.
                            if 0 <= corner_x < R and 0 <= corner_y < C:
                                if garden[corner_x][corner_y] != curr_plot:
                                    corners += 1
                            else:
                                corners += 1
                    # If both neighbours in the du and dv directions are not part of the region or outside the grid
                    # boundaries we have a corner in the du, dv direction
                    elif 0 <= next_u < R and 0 <= next_v < C:
                        if garden[next_u][next_v] != curr_plot:
                            corners += 1
                    else:
                        corners += 1
                curr_region.append((x, y, touched_plot, corners))
            regions_dict[curr_plot].append(curr_region)
    return regions_dict


if __name__ == '__main__':
    R, C, garden = parse_input()
    regions_map = bfs()
    garden_cost = garden_discounted_cost = 0
    for region_id, regions in regions_map.items():
        for region in regions:
            region_area = len(region)
            region_perimeter = sum([4 - n for _, _, n, _ in region])
            region_sides = sum([n for _, _, _, n in region])
            garden_cost += region_area * region_perimeter
            garden_discounted_cost += region_area * region_sides
    print(f'(Part 1) Garden cost is {garden_cost}')
    print(f'(Part 2) Discounted garden cost is {garden_discounted_cost}')
