

def elect_next_budget_item(
        votes: list[set[str]],
        balances: list[float],
        costs: dict[str, float]):

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
        {"B","C"},  # voter 3ה
        {"B","C"},  # voter 4
    ]

    balances = [40,40,40,40]

    costs = {
        "A": 60,
        "B": 48,
        "C": 45,
    }
    elect_next_budget_item(votes, balances, costs)