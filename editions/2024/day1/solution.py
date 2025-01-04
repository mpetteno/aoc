from typing import Any

from solvers.python_solver import Solver


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        locations1 = [int(line.strip().split(' ')[0]) for line in lines]
        locations1.sort()
        locations2 = [int(line.strip().split(' ')[1]) for line in lines]
        locations2.sort()
        return locations1, locations2

    def solve_first_part(self, parsed_input: Any) -> str:
        locations1, locations2 = parsed_input
        total_distance = 0
        for i in range(len(locations1)):
            total_distance += abs(locations1[i] - locations2[i])
        return f'Total distance is {total_distance}'

    def solve_second_part(self, parsed_input: Any) -> str:
        locations1, locations2 = parsed_input
        locations2_count_map = {}
        for loc2 in locations2:
            if loc2 in locations2_count_map:
                locations2_count_map[loc2] += 1
            else:
                locations2_count_map[loc2] = 1
        similarity_score = 0
        for loc1 in locations1:
            if loc1 in locations2_count_map:
                similarity_score += loc1 * locations2_count_map[loc1]
        return f'Total similarity score is {similarity_score}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
