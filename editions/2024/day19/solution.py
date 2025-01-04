

def parse_input():
    lines = open("input.txt").readlines()
    patterns = set(l.strip() for l in lines[0].split(","))
    designs = [l.strip() for l in lines[2:]]
    return patterns, designs


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


if __name__ == "__main__":
    available_patterns, requested_designs = parse_input()
    composable_designs_count = 0
    composition_ways_count = 0
    for d in requested_designs:
        if is_composable(available_patterns, d):
            composable_designs_count += 1
        composition_ways_count += count_composition_ways(available_patterns, d)
    print(f'(Part 1) Number of composable designs: {composable_designs_count}')
    print(f'(Part 2) Number of composition ways: {composition_ways_count}')
