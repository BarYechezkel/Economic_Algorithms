import cvxpy as cp
import numpy as np

def maximize_product(t_value):
    p_ami = cp.Variable(nonneg=True)  # פלדה של עמי
    n_ami = cp.Variable(nonneg=True)  # נפט של עמי
    p_tami = cp.Variable(nonneg=True)  # פלדה של תמי
    n_tami = cp.Variable(nonneg=True)  # נפט של תמי

    #  סך כל הפלדה והנפט הוא 1
    constraints = [p_ami + p_tami == 1,n_ami + n_tami == 1]

    # פונקציות הערכים של עמי ותמי
    v_ami = p_ami
    v_tami = p_tami * t_value + n_tami * (1 - t_value)

    objective = cp.Maximize(cp.log(v_ami) + cp.log(v_tami))
    problem = cp.Problem(objective, constraints)
    problem.solve()

    return np.exp(problem.value), p_ami.value, n_ami.value, p_tami.value, n_tami.value

t_value = 0.5
max_product, p_ami, n_ami, p_tami, n_tami = maximize_product(t_value)

print(f"Max product: {max_product}")
print(f"Ami: plada={p_ami}, neft={n_ami}")
print(f"Tami: plada={p_tami}, neft={n_tami}")
