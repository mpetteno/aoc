from typing import Any

from solvers.python_solver import Solver


class Solution(Solver):

    def parse_input(self) -> Any:
        schematics = self.input_data.split('\n\n')
        locks = []
        keys = []
        for schematic in schematics:
            lines = schematic.split()
            pin_heights = tuple(col.count('#') - 1 for col in zip(*lines))
            (keys, locks)[lines[0] == '#####'].append(pin_heights)
        return locks, keys

    def solve_first_part(self, parsed_input: Any) -> str:
        locks, keys = parsed_input
        valid_lock_key_pairs = []
        for lock in locks:
            for key in keys:
                zipped = list(zip(lock, key))
                if all(lp + kp <= len(zipped) for lp, kp in zipped):
                    valid_lock_key_pairs.append((lock, key))
        return f'Number of valid lock-key pairs: {len(valid_lock_key_pairs)}'

    def solve_second_part(self, parsed_input: Any) -> str:
        return "Merry Christmas!"


if __name__ == '__main__':
    solution = Solution()
    solution.run()
