import functools
from typing import Any

from solvers.python_solver import Solver


def create_keypad_graph(keypad, invalid_coords):
    graph = {}
    for a, (x1, y1) in keypad.items():
        for b, (x2, y2) in keypad.items():
            path = '<' * (y1 - y2) + 'v' * (x2 - x1) + '^' * (x1 - x2) + '>' * (y2 - y1)
            if invalid_coords == (x1, y2) or invalid_coords == (x2, y1):
                path = path[::-1]
            graph[(a, b)] = path + 'A'
    return graph


# Use memoization
@functools.cache
def get_shortest_sequence_length(sequence, iterations, first_iteration=False) -> int:
    if iterations == 0:
        return len(sequence)
    prev = 'A'
    total_length = 0
    graph = NUMERIC_KEYPAD_GRAPH if first_iteration else DIRECTIONAL_KEYPAD_GRAPH
    for char in sequence:
        total_length += get_shortest_sequence_length(graph[(prev, char)], iterations - 1)
        prev = char
    return total_length


def get_code_complexity(code, iterations):
    shortest_sequence_length = get_shortest_sequence_length(code, iterations=iterations, first_iteration=True)
    return int(code[:-1]) * shortest_sequence_length


NUMERIC_KEYPAD = {
    '7': (0, 0), '8': (0, 1), '9': (0, 2),
    '4': (1, 0), '5': (1, 1), '6': (1, 2),
    '1': (2, 0), '2': (2, 1), '3': (2, 2),
    '0': (3, 1), 'A': (3, 2),
}
DIRECTIONAL_KEYPAD = {
    '^': (0, 1), 'A': (0, 2),
    '<': (1, 0), 'v': (1, 1), '>': (1, 2),
}
NUMERIC_KEYPAD_GRAPH = create_keypad_graph(NUMERIC_KEYPAD, invalid_coords=(3, 0))
DIRECTIONAL_KEYPAD_GRAPH = create_keypad_graph(DIRECTIONAL_KEYPAD, invalid_coords=(0, 0))


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        return [l.strip() for l in lines]

    def solve_first_part(self, parsed_input: Any) -> str:
        codes = parsed_input
        total_complexity = sum(list(map(functools.partial(get_code_complexity, iterations=3), codes)))
        return f"Total complexity of the codes: {total_complexity}"

    def solve_second_part(self, parsed_input: Any) -> str:
        codes = parsed_input
        total_complexity = sum(list(map(functools.partial(get_code_complexity, iterations=26), codes)))
        return f"Total complexity of the codes: {total_complexity}"


if __name__ == '__main__':
    solution = Solution()
    solution.run()
