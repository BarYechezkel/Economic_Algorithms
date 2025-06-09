

def elect_next_budget_item(
        votes: list[set[str]], # List of sets where each set contains items voted by a citizen
        balances: list[float], # List of balances for each citizen
        costs: dict[str, float]): # Dictionary mapping items to their costs

    """
    Elects budget items based on votes and available balances, printing the payment distribution.

     regular case:
     >>> votes = [{"A", "B"}, {"A"}, {"B","C"}, {"B","C"}]
     >>> balances = [40, 40, 40, 40]
     >>> costs = {"A": 60, "B": 48, "C": 45}
     >>> elect_next_budget_item(votes, balances, costs)
     Round 1: "B" is elected.
     Citizen 1 pays 16.00 and has 24.00 remaining balance.
     Citizen 3 pays 16.00 and has 24.00 remaining balance.
     Citizen 4 pays 16.00 and has 24.00 remaining balance.
     Round 2: "C" is elected.
     Citizen 3 pays 22.50 and has 1.50 remaining balance.
     Citizen 4 pays 22.50 and has 1.50 remaining balance.
     Round 3: "A" is elected.
     Citizen 1 pays 24.00 and has 0.00 remaining balance.
     Citizen 2 pays 36.00 and has 4.00 remaining balance.


     project that cannot be funded at all, the voters
     >>> votes = [{"A"}, {"A"}, {"A"}, {"A"}]
     >>> balances = [10, 10, 10, 10]
     >>> costs = {"A": 50}
     >>> elect_next_budget_item(votes, balances, costs)
     Round 1: "A" cannot be funded due to insufficient funds.

    project with a single supporter who can pay all:
     >>> votes = [{"A"}, set(), set(), set()]
     >>> balances = [100, 0, 0, 0]
     >>> costs = {"A": 80}
     >>> elect_next_budget_item(votes, balances, costs)
     Round 1: "A" is elected.
     Citizen 1 pays 80.00 and has 20.00 remaining balance.

    project that divides evenly among supporters:
     >>> votes = [{"A"}, {"A"}]
     >>> balances = [30, 30]
     >>> costs = {"A": 60}
     >>> elect_next_budget_item(votes, balances, costs)
     Round 1: "A" is elected.
     Citizen 1 pays 30.00 and has 0.00 remaining balance.
     Citizen 2 pays 30.00 and has 0.00 remaining balance.

     projet that one of the supporters cannot pay their share:
     >>> votes = [{"A"}, {"A"}, {"A"}]
     >>> balances = [10, 30, 30]
     >>> costs = {"A": 60}
     >>> elect_next_budget_item(votes, balances, costs)
     Round 1: "A" is elected.
     Citizen 1 pays 10.00 and has 0.00 remaining balance.
     Citizen 2 pays 25.00 and has 5.00 remaining balance.
     Citizen 3 pays 25.00 and has 5.00 remaining balance.

     project with no supporters:
     >>> votes = [set(), set()]
     >>> balances = [50, 50]
     >>> costs = {"A": 10}
     >>> elect_next_budget_item(votes, balances, costs)
     Round 1: "A" cannot be funded due to insufficient funds.

         multiple projects all fundable:
    >>> votes = [{"A", "B", "C"}, {"A", "C"}, {"B"}, {"C"}]
    >>> balances = [100, 60, 40, 30]
    >>> costs = {"A": 80, "B": 40, "C": 60}
    >>> elect_next_budget_item(votes, balances, costs)
    Round 1: "B" is elected.
    Citizen 1 pays 20.00 and has 80.00 remaining balance.
    Citizen 3 pays 20.00 and has 20.00 remaining balance.
    Round 2: "C" is elected.
    Citizen 1 pays 20.00 and has 60.00 remaining balance.
    Citizen 2 pays 20.00 and has 40.00 remaining balance.
    Citizen 4 pays 20.00 and has 10.00 remaining balance.
    Round 3: "A" is elected.
    Citizen 1 pays 40.00 and has 20.00 remaining balance.
    Citizen 2 pays 40.00 and has 0.00 remaining balance.



    >>> votes = [{"A"}, {"B"}, {"C"}, {"D"}]
    >>> balances = [20, 30, 10, 15]
    >>> costs = {"A": 25, "B": 30, "C": 20, "D": 15}
    >>> elect_next_budget_item(votes, balances, costs)
    Round 1: "D" is elected.
    Citizen 4 pays 15.00 and has 0.00 remaining balance.
    Round 2: "C" cannot be funded due to insufficient funds.
    Round 3: "A" cannot be funded due to insufficient funds.
    Round 4: "B" is elected.
    Citizen 2 pays 30.00 and has 0.00 remaining balance.

    """

    item_votes: dict[str, set[str]] = {} # Dictionary to hold item votes
    for item in costs:
        item_votes[item] = set()

    for citizen_id, vote_set in enumerate(votes):
        for item in vote_set:
            if item in item_votes:
                item_votes[item].add(citizen_id)

    #sort the items by (cost)/(number of supporters), from lowest to highest
    item_votes = dict(sorted(item_votes.items(), key=lambda x: costs[x[0]] / len(x[1]) if len(x[1]) > 0 else float('inf')))
    i = 1 # Round counter
    for item, supporters in item_votes.items():
        cost = costs[item]
        total_available = sum(balances[i] for i in supporters)
        if total_available < cost:
            print(f'Round {i}: "{item}" cannot be funded due to insufficient funds.')
        else:
            print(f'Round {i}: "{item}" is elected.')
            divided_cost(supporters, cost, balances)
        i= i + 1


def divided_cost(supporters: set[int], cost: float, balances: list[float]):
    if not supporters or cost <= 0:
        return

    while True:
        equal_share = cost / len(supporters)
        cannot_pay = {i for i in supporters if balances[i] < equal_share}

        if not cannot_pay: # All supporters can pay their share
            for i in supporters:
                balances[i] -= equal_share
                print(f"Citizen {i + 1} pays {equal_share:.2f} and has {balances[i]:.2f} remaining balance.")
            return

        #who cannot pay the price, pay as much as they can
        total_paid = 0.0
        for i in cannot_pay:
            total_paid += balances[i]
            print(f"Citizen {i + 1} pays {balances[i]:.2f} and has 0.00 remaining balance.")
            balances[i] = 0.0


        supporters = supporters - cannot_pay
        cost -= total_paid

        if not supporters:
            #the remaining cost cannot be paid by anyone
            return

if __name__ == "__main__":
    votes = [
        {"A", "B"},  # voter 1
        {"A"},       # voter 2
        {"B","C"},   # voter 3
        {"B","C"},   # voter 4
    ]

    balances = [40,40,40,40]

    costs = {
        "A": 60,
        "B": 48,
        "C": 45,
    }
    # divided_cost({0,1,2}, 60, [10, 20, 30])
    elect_next_budget_item(votes, balances, costs)