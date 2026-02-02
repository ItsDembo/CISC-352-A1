# =============================
# Student Names:
# Group ID:
# Date:
# =============================
# CISC 352
# heuristics.py
# desc:
#


#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented to complete problem solution.

'''This file will contain different constraint propagators to be used within
   the propagators

1. ord_dh (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Degree heuristic

2. ord_mv (worth 0.25/3 points)
    - a Variable ordering heuristic that chooses the next Variable to be assigned 
      according to the Minimum-Remaining-Value heuristic


var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable

    csp is a CSP object---the heuristic can use this to get access to the
    Variables and constraints of the problem. The assigned Variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.
   '''

def ord_dh(csp):
    ''' return next Variable to be assigned according to the Degree Heuristic '''
    # IMPLEMENT

    # Initialize max_degree to -1 so any degree (even 0) will be larger
    max_degree = -1

    # Initialize best_variable to None (no variable selected yet)
    best_variable = None

    # Loop through all unassigned variables in the CSP
    for var in csp.get_all_unasgn_vars():

        # Initialize degree counter for this variable (counts constraints with unassigned vars)
        degree = 0

        # Get all constraints that involve the current variable
        for constraint in csp.get_cons_with_var(var):

            # Look at each variable in the constraint's scope
            for other_var in constraint.scope:

                # Only count if: 1) it's not the same variable, AND 2) it's unassigned
                if other_var != var and not other_var.is_assigned():
                    # Increment degree for each unassigned variable in constraint
                    degree += 1

        # If this variable has more constraints than our current max, update
        if degree > max_degree:
            # Update the maximum degree found so far
            max_degree = degree
            # Update the best variable to this one
            best_variable = var

    # Return the variable with the highest degree (most constraints with unassigned vars)
    return best_variable

def ord_mrv(csp):
    ''' return Variable to be assigned according to the Minimum Remaining Values heuristic '''
    # IMPLEMENT

    # Initialize min_domain_size to infinity so any domain size will be smaller
    min_domain_size = float('inf')

    # Initialize best_variable to None (no variable selected yet)
    best_variable = None

    # Loop through all unassigned variables in the CSP
    for var in csp.get_all_unasgn_vars():

        # Check if this variable's current domain size is smaller than our minimum
        if var.cur_domain_size() < min_domain_size:
            # Update the minimum domain size to this variable's domain size
            min_domain_size = var.cur_domain_size()
            # Update the best variable to this one (most constrained)
            best_variable = var

    # Return the variable with the smallest domain (fewest remaining values)
    return best_variable
