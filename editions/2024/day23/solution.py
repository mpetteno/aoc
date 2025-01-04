from collections import defaultdict


def parse_input():
    lines = open("input.txt").read().splitlines()
    edges = []
    vertices = set()
    adjacency_list = defaultdict(set)
    for line in lines:
        node_a, node_b = line.split('-')
        vertices.add(node_a)
        vertices.add(node_b)
        edges.append((node_a, node_b))
        adjacency_list[node_a].add(node_b)
        adjacency_list[node_b].add(node_a)
    return edges, vertices, adjacency_list


def analyze_lan_graph(edges, vertices):
        E = len(edges)
        V = len(vertices)
        density = (2 * E) / (V * (V - 1))
        avg_degree = (2 * E) / V
        if density < 0.1:
            graph_type = "Sparse"
        elif density > 0.5:
            graph_type = "Dense"
        else:
            graph_type = "Moderate"
        return graph_type, density, avg_degree


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


if __name__ == "__main__":
    edges, vertices, adjacency_list = parse_input()
    graph_type, density, avg_degree = analyze_lan_graph(edges, vertices)
    print(f'The LAN graph is {graph_type} with density {round(density, 3)} and average degree {avg_degree}')
    three_nodes_sets = get_three_nodes_sets(adjacency_list)
    count = sum(any(node[0] == 't' for node in s) for s in three_nodes_sets)
    print(f'Number of three inter-connected computers that contains at least one computer with a name that starts '
          f'with t: {count}')
    max_clique_set = bron_kerbosch(set(), set(adjacency_list), set(), adjacency_list)
    password = ','.join(sorted(max_clique_set))
    print(f'The largest clique in the LAN graph is {password}')
