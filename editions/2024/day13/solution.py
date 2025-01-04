from typing import Any

from solvers.python_solver import Solver


def get_min_win_cost(machine, max_play_per_button=100, error_weight=0):
    """
    Let a and b be the number of times the buttons A and B are played.
    Solving the linear equation system:
      p_x = a*a_x + b*b_x
      p_y = a*a_y + b*b_y
    Gives:
      a = (p_x - b_x*b) / a_x
      b = (a_y*p_x - a_x*p_y) / (a_y * b_x - a_x * b_y)
    Both a and b must be integers in the range [0, MAX_PLAY_PER_BUTTON]
    """
    a_rule, b_rule, prize_rule = machine
    prize_rule = prize_rule[0] + error_weight, prize_rule[1] + error_weight
    b = (a_rule[1] * prize_rule[0] - a_rule[0] * prize_rule[1]) / (a_rule[1] * b_rule[0] - a_rule[0] * b_rule[1])
    a = (prize_rule[0] - b_rule[0] * b) / a_rule[0]
    if (a.is_integer() and (error_weight or 0 <= a <= max_play_per_button)
            and b.is_integer() and (error_weight or 0 <= b <= max_play_per_button)):
        return int(a * a_rule[2] + b * b_rule[2])
    return 0


class Solution(Solver):

    def parse_input(self) -> Any:
        a_rules = []
        b_rules = []
        prizes_rules = []
        for i, line in enumerate(self.input_data.splitlines()):
            if i % 4 == 3:
                continue
            x, y = line.split(":")[1].split(",")
            if i % 4 == 0:
                x = int(x[x.index("+") + 1:].strip())
                y = int(y[y.index("+") + 1:].strip())
                a_rules.append((x, y, 3))
            elif i % 4 == 1:
                x = int(x[x.index("+") + 1:].strip())
                y = int(y[y.index("+") + 1:].strip())
                b_rules.append((x, y, 1))
            elif i % 4 == 2:
                x = int(x[x.index("=") + 1:].strip())
                y = int(y[y.index("=") + 1:].strip())
                prizes_rules.append((x, y))
        return list(zip(a_rules, b_rules, prizes_rules))

    def solve_first_part(self, parsed_input: Any) -> str:
        machines = parsed_input
        min_win_costs = [get_min_win_cost(m) for m in machines]
        return f'Minimum cost for all prizes: {sum(min_win_costs)}'

    def solve_second_part(self, parsed_input: Any) -> str:
        machines = parsed_input
        min_win_costs = [get_min_win_cost(m, error_weight=10000000000000) for m in machines]
        return f'Minimum cost for all prizes with error: {sum(min_win_costs)}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
