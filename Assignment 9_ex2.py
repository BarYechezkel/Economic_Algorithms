import networkx as nx
import matplotlib.pyplot as plt

class BirkhoffAlgo:
    # Birkhoff's algorithm for matrix decomposition
    def __init__(self, G):
        self.G = G.copy()
        self.steps = []  # list of (matching, p, remaining graph)
        self.matching_probs = []

    def check_balanced_graph(self):
        # Ensure that all left and right nodes have the same total edge weight
        left = {n for n, d in self.G.nodes(data=True) if d['bipartite'] == 0}
        right = set(self.G.nodes()) - left

        left_sums = [sum(self.G[u][v]['weight'] for v in self.G.neighbors(u)) for u in left]
        right_sums = [sum(self.G[u][v]['weight'] for v in self.G.neighbors(u)) for u in right]

        if len(set(left_sums)) != 1 or len(set(right_sums)) != 1:
            print("Graph is not balanced — Birkhoff decomposition may fail.")
            print("Left node sums:", left_sums)
            print("Right node sums:", right_sums)
            return False
        if abs(left_sums[0] - right_sums[0]) > 1e-6:
            print("Left and right totals do not match — invalid for Birkhoff.")
            print("Left sum:", left_sums[0])
            print("Right sum:", right_sums[0])
            return False
        return True

    def find_perfect_matching(self):
        from networkx.algorithms.bipartite import matching
        mate = matching.hopcroft_karp_matching(
            self.G,
            top_nodes={n for n, d in self.G.nodes(data=True) if d['bipartite'] == 0}
        )
        pairs = [(u, v) for u, v in mate.items() if self.G.nodes[u]['bipartite'] == 0]
        n = len({n for n, d in self.G.nodes(data=True) if d['bipartite'] == 0})
        return pairs if len(pairs) == n else None

    def decompose(self):
        if not self.check_balanced_graph():
            print("Decomposition aborted due to imbalance.")
            return []

        j = 1
        total_weight = 0
        while True:
            X = self.find_perfect_matching()
            if X is None:
                print(f"No perfect matching at step {j}, aborting.")
                break
            weights = [self.G[u][v]['weight'] for u, v in X]
            p = min(weights)
            total_weight += p
            print(f"Step {j}: X{j} = {X}, p = {p}")
            self.steps.append((X, p, self.G.copy()))
            for u, v in X:
                w = self.G[u][v]['weight'] - p
                if w <= 1e-8:
                    self.G.remove_edge(u, v)
                else:
                    self.G[u][v]['weight'] = w
            if self.G.number_of_edges() == 0:
                print(f"Decomposition complete in {j} steps.")
                print("Graph is now empty — full Birkhoff decomposition achieved.")
                break
            j += 1

        if self.G.number_of_edges() > 0:
            print("Graph is not empty — decomposition incomplete! This is NOT a full Birkhoff decomposition.")
        else:
            self.matching_probs = [(match, p / total_weight) for (match, p, _) in self.steps]

        return self.steps

    def plot_step(self, step_index):
        X, p, G_old = self.steps[step_index]
        pos = nx.drawing.layout.bipartite_layout(
            G_old, nodes=[n for n, d in G_old.nodes(data=True) if d['bipartite'] == 0]
        )
        plt.figure(figsize=(6, 4))
        nx.draw_networkx_nodes(G_old, pos, node_color='lightblue')
        nx.draw_networkx_edges(G_old, pos, edge_color='grey')
        labels = nx.get_edge_attributes(G_old, 'weight')
        nx.draw_networkx_edge_labels(G_old, pos, edge_labels=labels)
        nx.draw_networkx_edges(G_old, pos, edgelist=X, edge_color='blue', width=2)
        nx.draw_networkx_labels(G_old, pos)
        plt.title(f"Step {step_index+1}: p={p}\nX{step_index+1}={X}")
        plt.axis('off')
        plt.show()

    def print_final_result(self):
        if not self.matching_probs:
            print("\nNo valid decomposition — probabilities not computed.")
            return
        print("\nFinal Decomposition with Probabilities:")
        for i, (matching, prob) in enumerate(self.matching_probs):
            print(f"Matching X{i+1}: {matching}  -->  Probability = {prob:.2f}")

# Example usage
if __name__ == '__main__':
    # create a balanced bipartite graph of size 4
    L = ['A', 'B', 'C', 'D']
    R = ['1', '2', '3', '4']
    G = nx.Graph()
    G.add_nodes_from(L, bipartite=0)
    G.add_nodes_from(R, bipartite=1)
    edges = [
        ('A', '1', 2), ('A', '2', 1),
        ('B', '2', 2), ('B', '3', 1),
        ('C', '3', 2), ('C', '4', 1),
        ('D', '4', 2), ('D', '1', 1)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)

    decomposer = BirkhoffAlgo(G)
    steps = decomposer.decompose()
    for i in range(len(steps)):
        decomposer.plot_step(i)
    decomposer.print_final_result()
