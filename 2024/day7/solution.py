from operator import add, mul
from typing import List, Callable


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


if __name__ == '__main__':
    lines = [l.strip() for l in open('input.txt', 'r').readlines()]
    pt1_output = evaluate_equations(lines, [add, mul])
    print(f'(Part 1) Correct test value sum: {pt1_output}')
    pt2_output = evaluate_equations(lines, [add, mul, concatenate])
    print(f'(Part 2) Correct test value sum: {pt2_output}')
