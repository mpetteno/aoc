

def parse_input():
    with open('input.txt', 'r') as file:
        lines = file.readlines()
        locs1, locs2 = [], []
        for line in lines:
            loc1, loc2 = line.strip().split(' ')
            locs1.append(int(loc1))
            locs2.append(int(loc2))
    return locs1, locs2


if __name__ == '__main__':
    locations1, locations2 = parse_input()
    locations1.sort()
    locations2.sort()
    # Part 1
    total_distance = 0
    for i in range(len(locations1)):
        total_distance += abs(locations1[i] - locations2[i])
    print(f'Total distance is {total_distance}')
    # Part 2
    locations2_count_map = {}
    for i, loc2 in enumerate(locations2):
        if loc2 in locations2_count_map:
            locations2_count_map[loc2] += 1
        else:
            locations2_count_map[loc2] = 1
    similarity_score = 0
    for i, loc1 in enumerate(locations1):
        if loc1 in locations2_count_map:
            similarity_score += loc1 * locations2_count_map[loc1]
    print(f'Total similarity score is {similarity_score}')
