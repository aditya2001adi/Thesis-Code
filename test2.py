import numpy as np
import pulp

def master_problem():
    print("THIS IS THE MASTER PROBLEM")
    prob = pulp.LpProblem('Integer LP Problem', pulp.LpMaximize)

    # Define the decision variables as integers
    z = pulp.LpVariable('z', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=0, cat='Integer')

    # Define the objective function
    prob += z


    # Define the constraints
    prob += y <= 47
    prob += z <= -0.07*y + 40.89
    prob += z <= 0.8*y + 14
    prob += z <= 0.15*y + 31.55
    prob += z <= 0.05*y + 35.25

    
    print(prob)

    # Solve the problem
    prob.solve()

    # Print the status of the solution
    print("Status:", pulp.LpStatus[prob.status])

    # Print the value of the decision variables
    print("z:", pulp.value(z))
    print("y:", pulp.value(y))

    # Print the optimal objective value
    print("Optimal Value:", pulp.value(prob.objective))

    y_val = pulp.value(y)

    return y_val


master_problem()