import copy
from collections import defaultdict
from typing import Any

from solvers.py_solver import Solver


MOVES = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}


def sum_gps_coordinates(area, char):
    output = 0
    for a in range(len(area)):
        for b in range(len(area[0])):
            if area[a][b] == char:
                output += a * 100 + b
    return output


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        area_lines = lines[0:lines.index("")]
        moves_lines = lines[lines.index("") + 1:]
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

    def solve_first_part(self, parsed_input: Any) -> str:
        original_area_map, rows, cols, start_robot_pos, robot_moves = parsed_input
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
        return f'Boxes GPS coordinates sum: {sum_gps_coordinates(area_map, 'O')}'

    def solve_second_part(self, parsed_input: Any) -> str:
        original_area_map, rows, cols, start_robot_pos, robot_moves = parsed_input
        wider_area_map = []
        for i in range(rows):
            wider_row = []
            for j in range(cols):
                if original_area_map[i][j] == "O":
                    wider_row.extend("[]")
                elif original_area_map[i][j] == "@":
                    wider_row.extend("@.")
                elif original_area_map[i][j] == ".":
                    wider_row.extend("..")
                else:
                    wider_row.extend("##")
            wider_area_map.append(wider_row)
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
        return f'Boxes GPS coordinates sum: {sum_gps_coordinates(wider_area_map, '[')}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
