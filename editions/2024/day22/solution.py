from collections import defaultdict
from typing import Any

from solvers.python_solver import Solver


DAILY_SECRET_UPDATES = 2000
MONKEY_MAX_PRICE_SEQ_LENGTH = 4


def mix_and_prune(sn, number_to_mix):
    mixed_number = sn ^ number_to_mix
    pruned_number = mixed_number % 16777216
    return pruned_number


def secret_png(seed):
    sn = mix_and_prune(seed, number_to_mix=seed * 64)
    sn = mix_and_prune(sn, number_to_mix=sn // 32)
    sn = mix_and_prune(sn, number_to_mix=sn * 2048)
    return sn


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        return list(map(int, lines))

    def solve_first_part(self, parsed_input: Any) -> str:
        seeds = parsed_input
        secret_numbers_sum = 0
        for s in seeds:
            curr_secret_numbers = []
            secret_number = s
            for _ in range(DAILY_SECRET_UPDATES):
                secret_number = secret_png(secret_number)
                curr_secret_numbers.append(secret_number)
            secret_numbers_sum += curr_secret_numbers[-1]
        return f'Sum of last 2000 secret numbers: {secret_numbers_sum}'

    def solve_second_part(self, parsed_input: Any) -> str:
        seeds = parsed_input
        total_bananas = defaultdict(int)
        for s in seeds:
            seen_sequences = set()
            price_steps = []
            curr_secret_number = s
            for i in range(DAILY_SECRET_UPDATES):
                current_price = curr_secret_number % 10
                next_secret_number = secret_png(curr_secret_number)
                next_price = next_secret_number % 10
                price_steps.append(next_price - current_price)
                curr_secret_number = next_secret_number
                if i >= MONKEY_MAX_PRICE_SEQ_LENGTH - 1:
                    sequence = tuple(price_steps)
                    if sequence not in seen_sequences:
                        total_bananas[sequence] += next_price
                        seen_sequences.add(sequence)
                    price_steps.pop(0)
        max_number_of_bananas = max(total_bananas.values())
        sequence_max_number_of_bananas = max(total_bananas, key=lambda k: total_bananas[k])
        return (f'The maximum number of bananas that can be earned is {max_number_of_bananas} and it is achieved by the'
                f' sequence {sequence_max_number_of_bananas}')


if __name__ == '__main__':
    solution = Solution()
    solution.run()
