import re
from typing import Any

from solvers.python_solver import Solver


class Solution(Solver):

    def parse_input(self) -> Any:
        return self.input_data

    def solve_first_part(self, parsed_input: Any) -> str:
        program = parsed_input
        mul_factors = re.findall(r"mul\((\d+),(\d+)\)", program)
        result = 0
        for x, y in mul_factors:
            result += int(x) * int(y)
        return f'Multiplication result is {result}'

    def solve_second_part(self, parsed_input: Any) -> str:
        program = parsed_input
        # Use re.DOTALL to match newline characters too
        enabled_ops = re.findall(r"do\(\)(.*?)don't\(\)", program, re.DOTALL)
        enabled_ops.append(program[:min(program.index("don't()"), program.index("do()"))])
        result = 0
        for p in enabled_ops:
            enabled_mul_factors = re.findall(r"mul\((\d+),(\d+)\)", p)
            for x, y in enabled_mul_factors:
                result += int(x) * int(y)
        return f'Multiplication result is {result}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
