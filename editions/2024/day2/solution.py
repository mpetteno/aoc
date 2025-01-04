from typing import Any

from solvers.py_solver import Solver


def get_lis(sequence):
    n = len(sequence)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            abs_distance = abs(int(sequence[i]) - int(sequence[j]))
            if int(sequence[j]) < int(sequence[i]) and 1 <= abs_distance <= 3:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def get_lds(sequence):
    n = len(sequence)
    dp = [1] * n
    for i in range(1, n):
        for j in range(i):
            abs_distance = abs(int(sequence[i]) - int(sequence[j]))
            if int(sequence[j]) > int(sequence[i]) and 1 <= abs_distance <= 3:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)


def count_safe_reports(reports, max_change_count: int):
    report_safe_count = 0
    for report in reports:
        levels = report.strip().split()
        levels_lis = get_lis(levels)
        levels_lds = get_lds(levels)
        lis_change_count = len(levels) - levels_lis
        lds_change_count = len(levels) - levels_lds
        report_safe_count += 1 if lis_change_count <= max_change_count or lds_change_count <= max_change_count else 0
    return f'Number of safe reports: {report_safe_count}'


class Solution(Solver):

    def parse_input(self) -> Any:
        reports = self.input_data.splitlines()
        return reports

    def solve_first_part(self, parsed_input: Any) -> str:
        return count_safe_reports(parsed_input, 0)

    def solve_second_part(self, parsed_input: Any) -> str:
        return count_safe_reports(parsed_input, 1)


if __name__ == '__main__':
    solution = Solution()
    solution.run()
