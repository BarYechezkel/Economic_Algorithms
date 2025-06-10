

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


    >>> votes = [{"A"}, {"A"}, {"A"}]
    >>> balances = [10, 20, 30]
    >>> costs = {"A": 60}
    >>> elect_next_budget_item(votes, balances, costs)
    Round 1: "A" is elected.
    Citizen 1 pays 10.00 and has 0.00 remaining balance.
    Citizen 2 pays 20.00 and has 0.00 remaining balance.
    Citizen 3 pays 30.00 and has 0.00 remaining balance.

    """

    item_votes: dict[str, set[str]] = {} # Dictionary to hold item votes
    for item in costs:
        item_votes[item] = set()

    for citizen_id, vote_set in enumerate(votes):
        for item in vote_set:
            if item in item_votes:
                item_votes[item].add(citizen_id)

    item_max_paid = {}

    for item, supporters in item_votes.items():
        cost = costs[item]
        total_available = sum(balances[i] for i in supporters)
        if total_available < cost:
            continue  # Skip unfundable items
        temp_balances = balances.copy()
        max_paid = divided_cost(set(supporters), cost, temp_balances)
        item_max_paid[item] = max_paid

    if not item_max_paid:
        for item in costs:
            print(f'Round 1: "{item}" cannot be funded due to insufficient funds.')
        return

    # Choose item with minimal "voter maximum payment"
    elected_item = min(item_max_paid, key=item_max_paid.get)
    supporters = item_votes[elected_item]
    print(f'Round 1: "{elected_item}" is elected.')
    output_for_print = [] # Prepare output for printing
    divided_cost(supporters, costs[elected_item], balances, output=output_for_print)
    print ("\n".join(output_for_print))


def divided_cost(
    supporters: set[int],
    cost: float,
    balances: list[float],
    paid_so_far: dict[int, float] = None,
    output: list[str] = None
) -> float:
    if output is None:
        output = []
    if not supporters or cost <= 0:
        return max(paid_so_far.values(), default=0.0)

    if paid_so_far is None:
        paid_so_far = {i: 0.0 for i in supporters}

    equal_share = cost / len(supporters)
    cannot_pay = {i for i in supporters if balances[i] < equal_share}

    if not cannot_pay:
        for i in supporters:
            balances[i] -= equal_share
            paid_so_far[i] += equal_share
            output.append(f"Citizen {i + 1} pays {equal_share:.2f} and has {balances[i]:.2f} remaining balance.")
        return max(paid_so_far.values())

    total_paid = 0.0
    for i in cannot_pay:
        total_paid += balances[i]
        paid_so_far[i] += balances[i]
        output.append(f"Citizen {i + 1} pays {balances[i]:.2f} and has 0.00 remaining balance.")
        balances[i] = 0.0

    new_supporters = supporters - cannot_pay
    new_cost = cost - total_paid

    return divided_cost(new_supporters, new_cost, balances, paid_so_far, output)

if __name__ == "__main__":
    # divided_cost({0,1,2}, 60, [10, 20, 30])
    votes = [
        {"A"},  # voter 1
        {"A"},  # voter 2
        {"A"},  # voter 3
    ]

    balances = [10, 20, 30]

    costs = {
        "A": 60
    }
    elect_next_budget_item(votes, balances, costs)