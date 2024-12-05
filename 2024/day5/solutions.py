from collections import defaultdict


def parse_input():
    with open('input.txt') as f:
        lines = f.readlines()
        rules = defaultdict(list)
        updates = []
        for line in lines:
            if line != '\n':
                if '|' in line:
                    page_id, page_rule = line.split('|')
                    rules[int(page_id)].append(int(page_rule))
                else:
                    page_updates = [int(x) for x in line.split(',')]
                    updates.append(page_updates)
        return rules, updates


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
    for page in update:
        dfs(page)
    return sorted_update


if __name__ == '__main__':
    rules, updates = parse_input()
    middle_page_sum = middle_page_sum_sorted = 0
    for update in updates:
        error = False
        for i in range(len(update)):
            page_update = update[i]
            for j in range(i, len(update)):
                page_after = update[j]
                page_after_rules = rules[page_after]
                error = error or page_update in page_after_rules
        if not error:
            middle_page_sum += update[len(update) // 2]
        else:
            sorted_update = topological_dfs_sort(update, rules)
            middle_page_sum_sorted += sorted_update[len(sorted_update) // 2]
    print(f'Correct updates middle page sum: {middle_page_sum}')
    print(f'Sorted updates middle page sum: {middle_page_sum_sorted}')
