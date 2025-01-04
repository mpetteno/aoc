from collections import defaultdict
from typing import Any, List

from solvers.python_solver import Solver


def run_n_blinking(stones: List[str], n: int) -> int:
    stone_count_map = {s: 1 for s in stones}
    for i in range(n):
        new_stone_count_map = defaultdict(int)
        for stone, count in stone_count_map.items():
            if stone == '0':
                new_stone_count_map['1'] += count
            elif len(stone) % 2 == 0:
                mid_point = len(stone) // 2
                left_digits = int(stone[:mid_point])
                right_digits = int(stone[mid_point:])
                new_stone_count_map[str(left_digits)] += count
                new_stone_count_map[str(right_digits)] += count
            else:
                new_stone_count_map[str(int(stone) * 2024)] += count
        stone_count_map = new_stone_count_map
    return sum(stone_count_map.values())


class Solution(Solver):

    def parse_input(self) -> Any:
        return self.input_data.split(' ')

    def solve_first_part(self, parsed_input: Any) -> str:
        return f'Stones count after 25 blinks: {run_n_blinking(parsed_input, 25)}'

    def solve_second_part(self, parsed_input: Any) -> str:
        return f'Stones count after 75 blinks: {run_n_blinking(parsed_input, 75)}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
