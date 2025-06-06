

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
     Round 1: "A" is elected.
     Citizen 1 pays 30.00 and has 10.00 remaining balance.
     Citizen 2 pays 30.00 and has 10.00 remaining balance.
     Round 2: "B" is elected.
     Citizen 1 pays 10.00 and has 0.00 remaining balance.
     Citizen 3 pays 19.00 and has 21.00 remaining balance.
     Citizen 4 pays 19.00 and has 21.00 remaining balance.
     Round 3: "C" cannot be funded due to insufficient funds.

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
    Round 1: "A" is elected.
    Citizen 1 pays 40.00 and has 60.00 remaining balance.
    Citizen 2 pays 40.00 and has 20.00 remaining balance.
    Round 2: "B" is elected.
    Citizen 1 pays 20.00 and has 40.00 remaining balance.
    Citizen 3 pays 20.00 and has 20.00 remaining balance.
    Round 3: "C" is elected.
    Citizen 1 pays 20.00 and has 20.00 remaining balance.
    Citizen 2 pays 20.00 and has 0.00 remaining balance.
    Citizen 4 pays 20.00 and has 10.00 remaining balance.

    mix of fundable and unfundable projects:
    >>> votes = [{"A"}, {"B"}, {"C"}, {"D"}]
    >>> balances = [20, 30, 10, 15]
    >>> costs = {"A": 25, "B": 30, "C": 20, "D": 15}
    >>> elect_next_budget_item(votes, balances, costs)
    Round 1: "A" cannot be funded due to insufficient funds.
    Round 2: "B" is elected.
    Citizen 2 pays 30.00 and has 0.00 remaining balance.
    Round 3: "C" cannot be funded due to insufficient funds.
    Round 4: "D" is elected.
    Citizen 4 pays 15.00 and has 0.00 remaining balance.
    """


    item_votes: dict[str, set[str]] = {} # Dictionary to hold item votes
    for item in costs:
        item_votes[item] = set()

    for citizen_id, vote_set in enumerate(votes):
        for item in vote_set:
            if item in item_votes:
                item_votes[item].add(citizen_id)

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

    need_to_pay = cost / len(supporters)
    cannot_pay = set()
    for i in supporters:
        if balances[i] < need_to_pay:
            cannot_pay.add(i)

    can_pay = supporters - cannot_pay
    total_paid = 0.0

    for i in cannot_pay:
        total_paid += balances[i]
        print(f"Citizen {i + 1} pays {balances[i]:.2f} and has 0.00 remaining balance.")
        balances[i] = 0.0

    need_to_pay = (cost - total_paid)/ len(can_pay) # recalculate the amount each can pay

    for i in can_pay:
            balances[i] -= need_to_pay
            total_paid += need_to_pay
            print(f"Citizen {i + 1} pays {need_to_pay:.2f} and has {balances[i]:.2f} remaining balance.")



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
    elect_next_budget_item(votes, balances, costs)