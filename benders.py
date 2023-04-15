import pulp
import numpy as np
import sympy as sp
from sympy import *

def dual_subproblem(y):
    print("This is the Dual Subproblem")
    print("Inputted value for y is " + str(y))
    # Create a LP Minimization problem
    prob = pulp.LpProblem('Simple LP Problem', pulp.LpMinimize)

    # Define the decision variables
    q1 = pulp.LpVariable('q1', lowBound=0, cat='Continuous')
    q2 = pulp.LpVariable('q2', lowBound=0, cat='Continuous')
    q3 = pulp.LpVariable('q3', lowBound=0, cat='Continuous')
    q4 = pulp.LpVariable('q4', lowBound=0, cat='Continuous')
    q5 = pulp.LpVariable('q5', lowBound=0, cat='Continuous')


    # Define the objective function
    prob += (1000000 - y)*q1 + 250000*q2 + 250000*q3 + 250000*q4 + 250000*q5

    # Define the constraints
    prob += q1 + q2 >= 0.65
    prob += q1 + q3 >= 0.75
    prob += q1 + q4 >= 0.85
    prob += q1 + q5 >= 0.9

    print(prob)
    # Solve the problem
    prob.solve()

    # Print the status of the solution
    print("Status:", pulp.LpStatus[prob.status])

    # Print the value of the decision variables
    print("q1:", pulp.value(q1))
    print("q2:", pulp.value(q2))
    print("q3:", pulp.value(q3))
    print("q4:", pulp.value(q4))
    print("q5:", pulp.value(q5))

    list_of_vals = [q1, q2, q3, q4, q5]
    list1 = []
    for i in list_of_vals:
        list1.append(pulp.value(i))

    # Print the optimal objective value
    print("Optimal Value:", pulp.value(prob.objective))
    return list1


def lower_bound_solver(y_hat, u_star):
    # Generates our Lower Bound by multiplying u^* by our B-by vector. 
    x1 = np.array(u_star) 
    new_list = [1000000 - y_hat, 250000, 250000, 250000, 250000]
    x2 = np.array(new_list)
    constant = np.dot(x1, x2)
    print("Our constant is " + str(constant))
    lower_bound = constant + (0.8*y_hat)
    print("Our lower bound is " + str(lower_bound))
    return lower_bound

list_of_lists = []


#Create Benders Cut
def generate_cuts(y_hat, u_star):

    x1 = np.array(u_star)
    #Create variable y
    y = sp.symbols('y')
    new_list = [1000000 - y, 250000, 250000, 250000, 250000]
    x2 = np.array(new_list)
    constant = np.dot(x1, x2)
    sum = 0.8*y
    new = sum + constant
    print("Our cut is z <= " + str(new))
    poly = Poly(new, y)

    list_coeffs = poly.all_coeffs()

    list_of_lists.append(list_coeffs)

    return list_coeffs
    



def master_problem(list_of_cuts):
    # Define master problem using Benders Cuts from generate_cuts function 
    print("THIS IS THE MASTER PROBLEM")
    print("Our list of coefficients of our cuts is" + str(list_of_cuts))
    prob = pulp.LpProblem('Integer LP Problem', pulp.LpMaximize)

    # Define the decision variables as integers
    z = pulp.LpVariable('z', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=0, cat='Integer')

    # Define the objective function
    prob += z


    # Define the constraints
    prob += y <= 1000000
    for i in list_of_cuts:
        if len(i) == 2:
            prob += z <= i[0]*y + i[1]
        else:
            prob += z<= i[0]

    
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

def upper_bound_solver(list_of_cuts):
    prob = pulp.LpProblem('Integer LP Problem', pulp.LpMaximize)

    # Define the decision variables as integers
    z = pulp.LpVariable('z', lowBound=0, cat='Continuous')
    y = pulp.LpVariable('y', lowBound=0, cat='Integer')

    # Define the objective function
    prob += z


    # Define the constraints
    prob += y <= 1000000
    for i in list_of_cuts:
        if len(i) == 2:
            prob += z <= i[0]*y + i[1]
        else:
            prob += z <= i[0]

    

    # Solve the problem
    prob.solve()

    obj_val = pulp.value(prob.objective)

    return obj_val




def benders(y_hat):
    print("BEGIN PROCESS")
    # Initialize upper and lower bound
    z_star = 1000000
    w_star = 0
    counter = 0
    # limit iterations to 10, and stop process if upper and lower bounds differ by less than 0.01
    while abs(z_star - w_star) > 0.01 and counter <= 10:
        counter += 1
        print("This is iteration number " + str(counter))
        # Solve Dual Subproblem given inputted y_hat
        u_star = dual_subproblem(y_hat)
        
        #find Lower bound
        w_star = lower_bound_solver(y_hat, u_star)

        print("W_star is " + str(w_star))

        # Generate Benders Cut
        cut = generate_cuts(y_hat, u_star)
        print("Our benders cut is " + str(cut))

        # Find updated y_star for next iteration
        y_star = master_problem(list_of_lists)
        print("Our new y_star is " + str(y_star))

        # Find upper bound
        z_star = upper_bound_solver(list_of_lists)
        print("Upper Bound is: " + str(z_star))
        print("Lower Bound is: " + str(w_star))

        y_hat = y_star

    # Return our optimal value
    if w_star > z_star:
        print("Our optimal value is " + str(w_star))
    else:
        print("Our optimal value is " + str(z_star))
    print(str(int(y_star)) + " kL sent to Chicago Vaccination center")
    print("We had a total of " + str(counter - 1) + " iterations")
    return z_star



# Run program with initial y_hat value of 0
benders(0)
