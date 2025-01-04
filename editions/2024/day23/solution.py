from collections import defaultdict
from typing import Any

from solvers.python_solver import Solver


def get_three_nodes_sets(adjacency_list):
    three_nodes_sets = set()
    for u in adjacency_list:
        u_neighbors = adjacency_list[u]
        for v in u_neighbors:
            v_neighbors = adjacency_list[v]
            common_neighbors = u_neighbors.intersection(v_neighbors)
            for c in common_neighbors:
                three_nodes_sets.add(tuple(sorted([u, v, c])))
    return three_nodes_sets


def bron_kerbosch(selected, candidates, excluded, graph):
    if not candidates and not excluded:
        return selected
    max_clique = set()
    for v in candidates.copy():
        clique = bron_kerbosch(
            selected=selected.union({v}),
            candidates=candidates.intersection(graph[v]),
            excluded=excluded.intersection(graph[v]),
            graph=graph
        )
        max_clique = max(max_clique, clique, key=len)
        candidates.remove(v)
        excluded.add(v)
    return max_clique


class Solution(Solver):

    def parse_input(self) -> Any:
        lines = self.input_data.splitlines()
        adjacency_list = defaultdict(set)
        for line in lines:
            node_a, node_b = line.split('-')
            adjacency_list[node_a].add(node_b)
            adjacency_list[node_b].add(node_a)
        return adjacency_list

    def solve_first_part(self, parsed_input: Any) -> str:
        adjacency_list = parsed_input
        three_nodes_sets = get_three_nodes_sets(adjacency_list)
        count = sum(any(node[0] == 't' for node in s) for s in three_nodes_sets)
        return (f'Number of three inter-connected computers that contains at least one computer with a name that '
                f'starts with t: {count}')

    def solve_second_part(self, parsed_input: Any) -> str:
        adjacency_list = parsed_input
        max_clique_set = bron_kerbosch(set(), set(adjacency_list), set(), adjacency_list)
        password = ','.join(sorted(max_clique_set))
        return f'The largest clique in the LAN graph is {password}'


if __name__ == '__main__':
    solution = Solution()
    solution.run()
