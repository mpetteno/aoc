import copy
from collections import defaultdict


def parse_input():
    lines = open("input.txt").readlines()
    area_lines = lines[0:lines.index("\n")]
    moves_lines = lines[lines.index("\n")+1:]
    moves = ''.join([l.strip() for l in moves_lines])
    rows, cols = len(area_lines), len(area_lines[0].strip())
    parsed_area = [["." for _ in range(cols)] for _ in range(rows)]
    start_pos = 0, 0
    for i in range(rows):
        for j in range(cols):
            parsed_area[i][j] = area_lines[i][j]
            if area_lines[i][j] == "@":
                start_pos = i, j
    return parsed_area, rows, cols, start_pos, moves


def get_box_gps_coordinate(box_x, box_y):
    return box_x * 100 + box_y


def sum_gps_coordinates(area, char):
    output = 0
    for a in range(len(area)):
        for b in range(len(area[0])):
            if area[a][b] == char:
                output += get_box_gps_coordinate(a, b)
    return output


if __name__ == "__main__":
    MOVES = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
    original_area_map, R, C, start_robot_pos, robot_moves = parse_input()
    # Part 1
    area_map = copy.deepcopy(original_area_map)
    robot_pos = start_robot_pos
    for move in robot_moves:
        x, y = robot_pos
        dx, dy = MOVES[move]
        new_x, new_y = x + dx, y + dy
        h, w = new_x, new_y
        while area_map[h][w] == 'O':
            h, w = h + dx, w + dy
        if area_map[h][w] == '.':
            area_map[h][w], area_map[new_x][new_y] = area_map[new_x][new_y], '.'
            robot_pos = new_x, new_y
            area_map[new_x][new_y] = "@"
            area_map[x][y] = "."
    print(f'(Part 1) Boxes GPS coordinates sum: {sum_gps_coordinates(area_map, 'O')}')
    # Part 2
    wider_area_map = []
    for i in range(R):
        wider_row = []
        for j in range(C):
            if original_area_map[i][j] == "O":
                wider_row.extend("[]")
            elif original_area_map[i][j] == "@":
                wider_row.extend("@.")
            elif original_area_map[i][j] == ".":
                wider_row.extend("..")
            else:
                wider_row.extend("##")
        wider_area_map.append(wider_row)
    R, C = len(wider_area_map), len(wider_area_map[0])
    start_robot_pos = start_robot_pos[0], start_robot_pos[1] * 2
    robot_pos = start_robot_pos
    for move in robot_moves:
        x, y = robot_pos
        dx, dy = MOVES[move]
        new_x, new_y = x + dx, y + dy
        if move == ">" or move == "<":
            next_box_y = new_y
            while wider_area_map[new_x][next_box_y] == ']' or wider_area_map[new_x][next_box_y] == '[':
                next_box_y += dy * 2
            if wider_area_map[new_x][next_box_y] == '.':
                box_to_move = range(next_box_y, y) if move == "<" else reversed(range(y + 1, next_box_y + 1))
                for l in box_to_move:
                    wider_area_map[new_x][l] = wider_area_map[new_x][l - dy]
                robot_pos = new_x, new_y
                wider_area_map[new_x][new_y] = "@"
                wider_area_map[x][y] = "."
            pass
        elif move == "v" or move == "^":
            queue = {(new_x, new_y)}
            rows = defaultdict(set)
            while queue:
                i, j = queue.pop()
                match wider_area_map[i][j]:
                    case '#':
                        break
                    case ']':
                        rows[i] |= {j - 1, j}
                        queue |= {(i + dx, j), (i + dx, j - 1)}
                    case '[':
                        rows[i] |= {j, j + 1}
                        queue |= {(i + dx, j), (i + dx, j + 1)}
                    case '.':
                        rows[i].add(j)
            else:
                box_to_move = sorted(rows, reverse=True) if move == "v" else sorted(rows)
                for i in box_to_move:
                    for j in rows[i]:
                        wider_area_map[i][j] = wider_area_map[i - dx][j] if j in rows[i - dx] else '.'
                robot_pos = new_x, new_y
                wider_area_map[new_x][new_y] = "@"
                wider_area_map[x][y] = "."
    print(f'(Part 2) Boxes GPS coordinates sum: {sum_gps_coordinates(wider_area_map, '[')}')
