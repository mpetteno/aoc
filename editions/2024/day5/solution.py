from collections import defaultdict
from typing import Any

from solvers.py_solver import Solver


def topological_dfs_sort(update, rules):

    def dfs(page):
        if page in visited:
            return
        visited.add(page)
        neighbour_pages = [x for x in rules[page] if x in update]
        for neighbour_page in neighbour_pages:
            dfs(neighbour_page)
        sorted_update.append(page)

    sorted_update = []
    visited = set()
    for p in update:
        dfs(p)
    return sorted_update


def check_update_error(update, rules):
    error = False
    for i in range(len(update)):
        page_update = update[i]
        for j in range(i, len(update)):
            page_after = update[j]
            page_after_rules = rules[page_after]
            error = error or page_update in page_after_rules
    return error


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        rules = defaultdict(list)
        updates = []
        for line in lines:
            if line != '':
                if '|' in line:
                    page_id, page_rule = line.split('|')
                    rules[int(page_id)].append(int(page_rule))
                else:
                    page_updates = [int(x) for x in line.split(',')]
                    updates.append(page_updates)
        return rules, updates

    def solve_first_part(self, parsed_input: Any) -> str:
        rules, updates = parsed_input
        middle_page_sum = 0
        for update in updates:
            if not check_update_error(update, rules):
                middle_page_sum += update[len(update) // 2]
        return f'Correct updates middle page sum: {middle_page_sum}'

    def solve_second_part(self, parsed_input: Any) -> str:
        rules, updates = parsed_input
        middle_page_sum_sorted = 0
        for update in updates:
            if check_update_error(update, rules):
                sorted_update = topological_dfs_sort(update, rules)
                middle_page_sum_sorted += sorted_update[len(sorted_update) // 2]
        return f'Sorted updates middle page sum: {middle_page_sum_sorted}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
