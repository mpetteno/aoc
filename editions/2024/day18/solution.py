import heapq


def parse_input():
    lines = open("input.txt").readlines()
    parsed_bytes = [tuple(map(int, l.split(","))) for l in lines]
    return parsed_bytes


def shortest_path(grid, start, end):
    # Dimensions of the grid
    rows, cols = len(grid), len(grid[0])
    start_x, start_y = start
    end_x, end_y = end
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    # Priority queue for Dijkstra's algorithm
    priority_queue = [(0, 0, 0)]  # (distance, row, col)
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start_x][start_y] = 0  # Start point

    while priority_queue:
        dist, x, y = heapq.heappop(priority_queue)
        # If we reached the bottom-right corner
        if x == end_x and y == end_y:
            return dist
        # Process neighbors
        for dx, dy in directions:
            next_x, next_y = x + dx, y + dy
            # Check boundaries and if the cell is visitable
            if 0 <= next_x < rows and 0 <= next_y < cols and grid[next_x][next_y] != "#":
                new_dist = dist + 1  # Move costs 1 step
                if new_dist < distances[next_x][next_y]:
                    distances[next_x][next_y] = new_dist
                    heapq.heappush(priority_queue, (new_dist, next_x, next_y))
    # If no path is found
    return -1


if __name__ == "__main__":
    falling_bytes = parse_input()
    R, C = 71, 71
    start_x, start_y = 0, 0
    end_x, end_y = R - 1, C - 1
    grid = [["."] * C for _ in range(R)]
    for i, j in falling_bytes[:1024]:
        grid[j][i] = "#"
    minimum_steps = shortest_path(grid, (start_x, start_y), (end_x, end_y))
    print(f'(Part 1) Minimum number of steps to reach the bottom-right corner: {minimum_steps}')
    for i, j in falling_bytes[1024:]:
        grid[j][i] = "#"
        minimum_steps = shortest_path(grid, (start_x, start_y), (end_x, end_y))
        if minimum_steps == -1:
            print(f'(Part 2) The exit is blocked from byte: {(i, j)}')
            break
