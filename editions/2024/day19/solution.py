from typing import Any

from solvers.python_solver import Solver


def is_composable(patterns, design):
    dp = [False] * (len(design) + 1)
    dp[0] = True
    for i in range(1, len(design) + 1):
        for j in range(i):
            if dp[j] and design[j:i] in patterns:
                dp[i] = True
                break
    return dp[len(design)]


def count_composition_ways(patterns, design):
    dp = [0] * (len(design) + 1)
    dp[0] = 1
    for i in range(1, len(design) + 1):
        for j in range(i):
            if design[j:i] in patterns:
                dp[i] += dp[j]
    return dp[len(design)]


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        patterns = set(l.strip() for l in lines[0].split(","))
        designs = [l.strip() for l in lines[2:]]
        return patterns, designs

    def solve_first_part(self, parsed_input: Any) -> str:
        available_patterns, requested_designs = parsed_input
        composable_designs_count = sum([1 for d in requested_designs if is_composable(available_patterns, d)])
        return f'Number of composable designs: {composable_designs_count}'

    def solve_second_part(self, parsed_input: Any) -> str:
        available_patterns, requested_designs = parsed_input
        composition_ways_count = sum([count_composition_ways(available_patterns, d) for d in requested_designs])
        return f'Number of composition ways: {composition_ways_count}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
