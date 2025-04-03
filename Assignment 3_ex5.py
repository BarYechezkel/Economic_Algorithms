

import cvxpy as cp
import numpy as np

def compute_competitive_equilibrium(utility, budgets, resources):
    n, m = utility.shape  # n = Number of players  m= Number of resources

    # Allocation variables
    X = cp.Variable((n, m), nonneg=True)

    # Player values
    V = cp.sum(cp.multiply(utility, X), axis=1)

    # Objective: Maximize sum of log utility
    objective = cp.Maximize(cp.sum(cp.multiply(budgets, cp.log(V))))

    # Constraints: Resource constraints and budget constraints
    constraints = [cp.sum(X, axis=0) <= resources]

    # Solve optimization problem
    prob = cp.Problem(objective, constraints)
    prob.solve()

    # Get numeric values
    X_val = X.value
    V_val = V.value


    # Compute prices
    prices = np.zeros(m)
    for r in range(m):
        for j in range(n):
            if X_val[j, r] > 0:  # If player j is allocated resource r
                prices[r] += (budgets[j] * X_val[j, r] * utility[j, r]) / V_val[j]

    return X_val, prices

# the class example
Utility_ex = np.array([[8,4,2],[2,6,5]])  # Player utility matrix
Budget_ex = np.array([60, 40])      # Budget vector
Resources_ex = np.array([1, 1 ,1])  # Resource constraints

X_opt, price_opt = compute_competitive_equilibrium(Utility_ex, Budget_ex, Resources_ex)

# Print results in a table
# Print input data
print("\n===== Input Data =====")
print("Utility Matrix (U):")
for row in Utility_ex:
    print("  ", row)

print("Budgets (B):", Budget_ex)
print("Resources (R):", Resources_ex)

# Print results
print("\n===== Optimal Allocation =====")
print("┌─────────", "┬────────────" * len(Resources_ex), "┐", sep="")
header = "│ Player  " + "".join([f"│ Resource {j+1} " for j in range(len(Resources_ex))]) + "│"
print(header)
print("├─────────", "┼────────────" * len(Resources_ex), "┤", sep="")
for i, row in enumerate(X_opt):
    row_str = f"│   {i+1}     " + "".join([f"│   {row[j]:7.2f}  " for j in range(len(Resources_ex))]) + "│"
    print(row_str)
print("└─────────", "┴────────────" * len(Resources_ex), "┘", sep="")

print("\n===== Prices =====")
print("┌───────────┬──────────┐")
print("│ Resource  │  Price   │")
print("├───────────┼──────────┤")
for i in range(len(price_opt)):
    print(f"│     {i+1}     │  {price_opt[i]:7.2f} │")
print("└───────────┴──────────┘")