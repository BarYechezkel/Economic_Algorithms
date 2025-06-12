import networkx as nx

def find_decomposition(budget, preferences):
    G = nx.DiGraph() # Create a directed graph
    n = len(preferences) # Number of players
    m = len(budget) # Number of topics
    C = sum(budget) # Total budget available
    source = 's'
    sink = 't'
    player_budget = C/n

    # add edges from source to players with capacity according to budget
    for i in range(n):
        G.add_edge(source, f'p{i}', capacity=player_budget)

    # add edges from players to topics according to preferences
    for i, prefs in enumerate(preferences):
        for topic in prefs:
            G.add_edge(f'p{i}', f't{topic}', capacity=player_budget)

    # add edges from topics to sink with capacity according to topic budget
    for i, topic_budget in enumerate(budget):
        G.add_edge(f't{i}', sink, capacity=topic_budget)

    # calculate maximum flow
    flow_value, flow_dict = nx.maximum_flow(G, source, sink)

    # Create matrix: players × topics
    decomposition = [[0.0] * m for _ in range(n)]

    for i in range(n):
        for j in range(m):
            player_node = f'p{i}'
            topic_node = f't{j}'
            if topic_node in flow_dict[player_node]:
                decomposition[i][j] = float(flow_dict[player_node][topic_node])
    return decomposition


if __name__ == "__main__":
    budget = [400, 50, 50, 0]
    preferences = [{0, 1}, {0, 2}, {0, 3}, {1, 2}, {0}]

    result = find_decomposition(budget, preferences)
    for i,row in enumerate(result):
        print(f"player {i+1}: {row}")