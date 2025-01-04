from typing import Any

from solvers.python_solver import Solver

DIRECTIONS = [(1, 0), (0, -1), (-1, 0), (0, 1)]
TURN_SCORE = 1000
MOVE_SCORE = 1


def get_next_directions(current_dir):
    current_dir_idx = DIRECTIONS.index(current_dir)
    clock_dir = DIRECTIONS[(current_dir_idx + 1) % len(DIRECTIONS)]
    count_clock_dir = DIRECTIONS[(current_dir_idx - 1) % len(DIRECTIONS)]
    return clock_dir, count_clock_dir


def get_shortest_path_score(labyrinth):
    start_x, start_y = len(labyrinth) - 2, 1
    end_x, end_y = 1, len(labyrinth[1]) - 2
    start_dir = DIRECTIONS[3]  # Reindeer starts facing East
    score = 0
    queue = [(start_x, start_y, start_dir, score)]
    while queue:
        x, y, curr_direction, curr_score = queue.pop(0)
        clockwise_dir, counterclockwise_dir = get_next_directions(curr_direction)
        dir_scores_combinations = [
            (curr_direction, curr_score + MOVE_SCORE),
            (clockwise_dir, curr_score + TURN_SCORE + MOVE_SCORE),
            (counterclockwise_dir, curr_score + TURN_SCORE + MOVE_SCORE),
        ]
        for new_dir, new_score in dir_scores_combinations:
            dx, dy = new_dir
            new_x, new_y = x + dx, y + dy
            if labyrinth[new_x][new_y] == "#":
                continue
            if (labyrinth[new_x][new_y] in [".", "E"] or
                    (isinstance(labyrinth[new_x][new_y], int) and labyrinth[new_x][new_y] > new_score)):
                labyrinth[new_x][new_y] = new_score
                queue.append((new_x, new_y, new_dir, new_score))
    final_score = labyrinth[end_x][end_y]
    return final_score


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        area_map = [list(l.strip()) for l in lines]
        return area_map

    def solve_first_part(self, parsed_input: Any) -> str:
        labyrinth = parsed_input
        final_score = get_shortest_path_score(labyrinth)
        return f'Shortest path score: {final_score}'

    def solve_second_part(self, parsed_input: Any) -> str:
        labyrinth = parsed_input
        final_score = get_shortest_path_score(labyrinth)
        end_x, end_y = 1, len(labyrinth[1]) - 2
        queue = [(end_x, end_y, DIRECTIONS[0], final_score), (end_x, end_y, DIRECTIONS[1], final_score)]
        res = 1
        visited = set()
        while queue:
            x, y, curr_direction, curr_score = queue.pop(0)
            clockwise_dir, counterclockwise_dir = get_next_directions(curr_direction)
            dir_scores_combinations = [
                (curr_direction, curr_score - MOVE_SCORE),
                (clockwise_dir, curr_score - TURN_SCORE - MOVE_SCORE),
                (counterclockwise_dir, curr_score - TURN_SCORE - MOVE_SCORE),
            ]
            for new_dir, new_score in dir_scores_combinations:
                dx, dy = new_dir
                new_x, new_y = x + dx, y + dy
                if (isinstance(labyrinth[new_x][new_y], int) and
                        (labyrinth[new_x][new_y] in [new_score, new_score - TURN_SCORE]) and (
                        new_x, new_y) not in visited):
                    res += 1
                    queue.append((new_x, new_y, new_dir, new_score))
                    visited.add((new_x, new_y))
        return f'Best path tiles count: {res + 1}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
