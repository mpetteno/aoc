
def parse_input():
    area_map = [list(line.strip()) for line in open('input.txt', 'r').readlines()]
    rows, cols = len(area_map), len(area_map[0])
    th = []
    for i in range(rows):
        for j in range(cols):
            current_pos = int(area_map[i][j])
            if current_pos == 0:
                th.append((i, j))
    return rows, cols, area_map, th


def df_visit(th):
    stack = [th]
    summits_pos = []
    while stack:
        i, j = stack.pop()
        current_slope = int(topographic_map[i][j])
        if current_slope == 9:
            summits_pos.append((i, j))
        else:
            for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                next_x, next_y = i + dx, j + dy
                if 0 <= next_x < R and 0 <= next_y < C:
                    next_slope = int(topographic_map[next_x][next_y])
                    if next_slope == current_slope + 1:
                        stack.append((next_x, next_y))
    return summits_pos


if __name__ == '__main__':
    R, C, topographic_map, trailheads = parse_input()
    scores = []
    ratings = []
    for trailhead in trailheads:
        summits = df_visit(trailhead)
        scores.append(len(set(summits)))
        ratings.append(len(summits))
    print(f'(Part 1) Trailheads total score: {sum(scores)}')
    print(f'(Part 2) Trailheads total rating: {sum(ratings)}')
