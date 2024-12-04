
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


if __name__ == "__main__":
    report_safe_count_pt1 = 0
    report_safe_count_pt2 = 0
    with open("input.txt") as f:
        reports = f.readlines()
        for report in reports:
            levels = report.strip().split()
            levels_lis = get_lis(levels)
            levels_lds = get_lds(levels)
            lis_change_count = len(levels) - levels_lis
            lds_change_count = len(levels) - levels_lds
            report_safe_count_pt1 += 1 if lis_change_count <= 0 or lds_change_count <= 0 else 0
            report_safe_count_pt2 += 1 if lis_change_count <= 1 or lds_change_count <= 1 else 0
    print(f'(Pt. 1) Number of safe reports: {report_safe_count_pt1}')
    print(f'(Pt. 2) Number of safe reports: {report_safe_count_pt2}')
