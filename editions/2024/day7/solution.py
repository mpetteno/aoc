from operator import add, mul
from typing import List, Callable, Any

from solvers.python_solver import Solver


def concatenate(a: int, b: int) -> int:
    return int(str(a) + str(b))


def evaluate_equations(equations: List[str], operators: List[Callable]) -> int:
    test_value_sum = 0
    for equation in equations:
        split_equation = equation.split(':')
        test_value = int(split_equation[0])
        numbers = [int(x) for x in split_equation[1].strip().split(' ')]
        equation_tree = [[numbers[0]]]
        for n in numbers[1:]:
            equation_tree.append([op(x, n) for op in operators for x in equation_tree[-1]])
        if test_value in equation_tree[-1]:
            test_value_sum += test_value
    return test_value_sum


class Solution(Solver):

    def parse_input(self) -> Any:
        return self.input_data.splitlines()

    def solve_first_part(self, parsed_input: Any) -> str:
        output = evaluate_equations(parsed_input, [add, mul])
        return f'Correct test value sum: {output}'

    def solve_second_part(self, parsed_input: Any) -> str:
        output = evaluate_equations(parsed_input, [add, mul, concatenate])
        return f'Correct test value sum: {output}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
