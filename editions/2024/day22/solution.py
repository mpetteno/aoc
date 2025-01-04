from collections import defaultdict


def parse_input():
    lines = open("input.txt").read().splitlines()
    return list(map(int, lines))


def mix_and_prune(sn, number_to_mix):
    mixed_number = sn ^ number_to_mix
    pruned_number = mixed_number % 16777216
    return pruned_number


def secret_png(seed):
    sn = mix_and_prune(seed, number_to_mix=seed * 64)
    sn = mix_and_prune(sn, number_to_mix=sn // 32)
    sn = mix_and_prune(sn, number_to_mix=sn * 2048)
    return sn


if __name__ == "__main__":
    DAILY_SECRET_UPDATES = 2000
    seeds = parse_input()
    secret_numbers_sum = 0
    secret_numbers = []
    for s in seeds:
        curr_secret_numbers = []
        secret_number = s
        for _ in range(DAILY_SECRET_UPDATES):
            secret_number = secret_png(secret_number)
            curr_secret_numbers.append(secret_number)
        secret_numbers_sum += curr_secret_numbers[-1]
    print(f'(Part 1) Sum of last 2000 secret numbers: {secret_numbers_sum}')
    MONKEY_MAX_PRICE_SEQ_LENGTH = 4
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
    print(f'(Part 2) The maximum number of bananas that can be earned is {max_number_of_bananas} and it is achieved by '
          f'the sequence {sequence_max_number_of_bananas}')
