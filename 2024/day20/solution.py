
def parse_input():
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    lines = open("input.txt").readlines()
    grid = [list(l.strip()) for l in lines]
    start_pos = 0, 0
    rows, cols = len(grid), len(grid[0])
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "S":
                start_pos = i, j
    track = [start_pos]
    x, y = start_pos
    prev_pos = None
    while grid[x][y] != "E":
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < rows and 0 <= new_y < cols and grid[new_x][new_y] != "#" and (new_x, new_y) != prev_pos:
                prev_pos = x, y
                x, y = new_x, new_y
                track.append((x, y))
                break
    return track


def cheating_saved_time(track, max_cheat_time: int):
    for (t1, (x1, y1)) in enumerate(track):
        for t2 in range(t1 + 3, len(track)):
            x2, y2 = track[t2]
            dist = abs(x2 - x1) + abs(y2 - y1)
            if dist <= max_cheat_time and t2 - t1 > dist:
                yield t2 - t1 - dist


if __name__ == "__main__":
    path = parse_input()
    MIN_GAIN_TIME = 100
    two_ps_gaining_time_count = sum(saved >= MIN_GAIN_TIME for saved in cheating_saved_time(path, max_cheat_time=2))
    print(f'(Part 1) Number of 2 ps cheats that gain {MIN_GAIN_TIME} ps: {two_ps_gaining_time_count}')
    twenty_ps_gaining_time_count = sum(saved >= MIN_GAIN_TIME for saved in cheating_saved_time(path, max_cheat_time=20))
    print(f'(Part 2) Number of 20 ps cheats that gain {MIN_GAIN_TIME} ps: {twenty_ps_gaining_time_count}')
