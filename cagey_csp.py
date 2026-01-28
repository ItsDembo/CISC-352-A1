# =============================
# Student Names: Tomer Lapid, Alec Nakhnikian, Ori Dembo
# Group ID: (A1) 69
# Date: Jan 26, 2026
# =============================
# CISC 352
# cagey_csp.py
# desc:
#

#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of Variable objects
representing the board. The returned list of lists is used to access the
solution.

For example, after these three lines of code

    csp, var_array = binary_ne_grid(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array is a list of all Variables in the given csp. If you are returning an entire grid's worth of Variables
they should be arranged linearly, where index 0 represents the top left grid cell, index n-1 represents
the top right grid cell, and index (n^2)-1 represents the bottom right grid cell. Any additional Variables you use
should fall after that (i.e., the cage operand variables, if required).

1. binary_ne_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 0.25/3 marks)
    - A model of a Cagey grid (without cage constraints) built using only n-ary
      all-different constraints for both the row and column constraints.

3. cagey_csp_model (worth 0.5/3 marks)
    - a model of a Cagey grid built using your choice of (1) binary not-equal, or
      (2) n-ary all-different constraints for the grid, together with Cagey cage
      constraints.


Cagey Grids are addressed as follows (top number represents how the grid cells are adressed in grid definition tuple);
(bottom number represents where the cell would fall in the var_array):
+-------+-------+-------+-------+
|  1,1  |  1,2  |  ...  |  1,n  |
|       |       |       |       |
|   0   |   1   |       |  n-1  |
+-------+-------+-------+-------+
|  2,1  |  2,2  |  ...  |  2,n  |
|       |       |       |       |
|   n   |  n+1  |       | 2n-1  |
+-------+-------+-------+-------+
|  ...  |  ...  |  ...  |  ...  |
|       |       |       |       |
|       |       |       |       |
+-------+-------+-------+-------+
|  n,1  |  n,2  |  ...  |  n,n  |
|       |       |       |       |
| n^2-n | n^2-n |       | n^2-1 |
+-------+-------+-------+-------+

Boards are given in the following format:
(n, [cages])

n - is the size of the grid,
cages - is a list of tuples defining all cage constraints on a given grid.


each cage has the following structure
(v, [c1, c2, ..., cm], op)

v - the value of the cage.
[c1, c2, ..., cm] - is a list containing the address of each grid-cell which goes into the cage (e.g [(1,2), (1,1)])
op - a flag containing the operation used in the cage (None if unknown)
      - '+' for addition
      - '-' for subtraction
      - '*' for multiplication
      - '/' for division
      - '%' for modular addition
      - '?' for unknown/no operation given

An example of a 3x3 puzzle would be defined as:
(3, [(3,[(1,1), (2,1)],"+"),(1, [(1,2)], '?'), (8, [(1,3), (2,3), (2,2)], "+"), (3, [(3,1)], '?'), (3, [(3,2), (3,3)], "+")])

'''

from cspbase import *
from itertools import permutations, product

def binary_ne_grid(cagey_grid):
    # Extract grid size
    N = cagey_grid[0]

    # Create CSP
    csp = CSP("Binary_NE_Grid")

    # Create variables
    cell_vars = []
    all_vars = []

    for r in range(N):
        row_vars = []
        for c in range(N):
            var = Variable(f"Cell({r+1},{c+1})", list(range(1, N + 1)))
            csp.add_var(var)
            row_vars.append(var)
            all_vars.append(var)
        cell_vars.append(row_vars)

    # Row constraints: binary not-equal
    for r in range(N):
        for c1 in range(N):
            for c2 in range(c1 + 1, N):
                var1 = cell_vars[r][c1]
                var2 = cell_vars[r][c2]

                con = Constraint(
                    f"Row({r+1})_Neq_{c1+1}_{c2+1}",
                    [var1, var2]
                )

                satisfying_tuples = []
                for v1 in range(1, N + 1):
                    for v2 in range(1, N + 1):
                        if v1 != v2:
                            satisfying_tuples.append((v1, v2))

                con.add_satisfying_tuples(satisfying_tuples)
                csp.add_constraint(con)

    # Column constraints: binary not-equal
    for c in range(N):
        for r1 in range(N):
            for r2 in range(r1 + 1, N):
                var1 = cell_vars[r1][c]
                var2 = cell_vars[r2][c]

                con = Constraint(
                    f"Col({c+1})_Neq_{r1+1}_{r2+1}",
                    [var1, var2]
                )

                satisfying_tuples = []
                for v1 in range(1, N + 1):
                    for v2 in range(1, N + 1):
                        if v1 != v2:
                            satisfying_tuples.append((v1, v2))

                con.add_satisfying_tuples(satisfying_tuples)
                csp.add_constraint(con)

    return csp, all_vars

def nary_ad_grid(cagey_grid):
    # Extract grid size
    N = cagey_grid[0]

    # Create CSP
    csp = CSP("Nary_AD_Grid")

    # Create variables
    cell_vars = []
    all_vars = []

    for r in range(N):
        row_vars = []
        for c in range(N):
            var = Variable(f"Cell({r+1},{c+1})", list(range(1, N + 1)))
            csp.add_var(var)
            row_vars.append(var)
            all_vars.append(var)
        cell_vars.append(row_vars)

    # all-different satisfying tuples (length N)
    ad_tuples = list(permutations(range(1, N+1), N))

    # Row constraints: All different
    for r in range(N):
        row_scope = cell_vars[r]
        con = Constraint(f"RowAD({r+1})", row_scope)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    # Column constraints: All different
    for c in range(N):
        col_scope = [cell_vars[r][c] for r in range(N)]
        con = Constraint(f"ColAD({c+1})", col_scope)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    return csp, all_vars


def cagey_csp_model(cagey_grid):
    # Extract grid size
    N = cagey_grid[0]

    # Extract cages
    cages = cagey_grid[1]

    # Create CSP
    csp = CSP("Cagey_CSP_Model")

    # Create variables
    cell_vars = []
    all_vars = []

    for r in range(N):
        row_vars = []
        for c in range(N):
            var = Variable(f"Cell({r+1},{c+1})", list(range(1, N + 1)))
            csp.add_var(var)
            row_vars.append(var)
            all_vars.append(var)
        cell_vars.append(row_vars)

    # ---- Grid Constraints (n-ary all diff) ---
    ad_tuples = list(permutations(range(1, N + 1), N))

    # Row constraints: All different
    for r in range(N):
        row_scope = cell_vars[r]
        con = Constraint(f"RowAD({r+1})", row_scope)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    # Column constraints: All different
    for c in range(N):
        col_scope = [cell_vars[r][c] for r in range(N)]
        con = Constraint(f"ColAD({c+1})", col_scope)
        con.add_satisfying_tuples(ad_tuples)
        csp.add_constraint(con)

    # ---- Cage Constraints ----
    OPS_ALL = ['+', '-', '*', '/', '%']

    # Helper: generate tuples for + cages without full N^k product
    def gen_sum_tuples(k, target_sum):
        # values are in [1..N]
        out = []

        def backtrack(idx, curr_sum, prefix):
            # prune: if already too big
            if curr_sum > target_sum:
                return

            # prune: even with max values we can't reach target
            max_possible = curr_sum + (k - idx) * N
            if max_possible < target_sum:
                return

            if idx == k:
                if curr_sum == target_sum:
                    out.append(tuple(prefix))
                return

            # choose next value
            for v in range(1, N + 1):
                prefix.append(v)
                backtrack(idx + 1, curr_sum + v, prefix)
                prefix.pop()

        backtrack(0, 0, [])
        return out

    # Helper: generate tuples for * cages without full N^k product
    def gen_prod_tuples(k, target_prod):
        out = []

        def backtrack(idx, curr_prod, prefix):
            # prune: product already too large
            if curr_prod > target_prod:
                return

            # prune: if curr_prod does not divide target, you can never reach it
            if target_prod % curr_prod != 0:
                return

            if idx == k:
                if curr_prod == target_prod:
                    out.append(tuple(prefix))
                return

            for v in range(1, N + 1):
                prefix.append(v)
                backtrack(idx + 1, curr_prod * v, prefix)
                prefix.pop()

        backtrack(0, 1, [])
        return out

    for (target, cell_coords, op_char) in cages:

        # Creates unique tag for naming purposes
        coord_tag = ",".join([f"{r}-{c}" for (r, c) in cell_coords])

        # Build list of cell Variables in this cage
        cage_cells = []
        for (row, col) in cell_coords:
            cage_cells.append(cell_vars[row - 1][col - 1])

        # Operator variable + domain
        is_unknown = (op_char == '?' or op_char is None)
        op_label = '?' if is_unknown else op_char

        if is_unknown:
            op_domain = list(OPS_ALL)
        else:
            op_domain = [op_char]

        op_var = Variable(
            f"CageOp({target}:{op_label}:[{coord_tag}])",
            op_domain
        )
        csp.add_var(op_var)
        all_vars.append(op_var)

        # Constraint scope: operator first, then cage cells
        scope = [op_var] + cage_cells
        con = Constraint(f"Cage({target}:{op_label}:[{coord_tag}])", scope)

        # Generate satisfying tuples
        sat_tuples = []
        k = len(cage_cells)

        for op in op_domain:
            # 1-cell cages: only value matters
            if k == 1:
                for v in range(1, N + 1):
                    if v == target:
                        sat_tuples.append((op, v))
                continue

            if op == '+':
                for values in gen_sum_tuples(k, target):
                    sat_tuples.append((op,) + values)

            elif op == '*':
                # If target is 0 (shouldn't be in these puzzles), this would need changes.
                # With normal Cagey targets (positive), this is fine.
                for values in gen_prod_tuples(k, target):
                    sat_tuples.append((op,) + values)

            elif op == '%':
                # Still brute-force: modular addition doesn't prune as cleanly.
                for values in product(range(1, N + 1), repeat=k):
                    if (sum(values) % N) == target:
                        sat_tuples.append((op,) + values)

            elif op == '-':
                for values in product(range(1, N + 1), repeat=k):
                    ok = False
                    for perm in set(permutations(values)):
                        acc = perm[0]
                        for x in perm[1:]:
                            acc = acc - x
                        if acc == target:
                            ok = True
                            break
                    if ok:
                        sat_tuples.append((op,) + values)

            elif op == '/':
                for values in product(range(1, N + 1), repeat=k):
                    ok = False
                    for perm in set(permutations(values)):
                        acc = perm[0]
                        valid = True
                        for x in perm[1:]:
                            if acc % x != 0:
                                valid = False
                                break
                            acc = acc // x
                        if valid and acc == target:
                            ok = True
                            break
                    if ok:
                        sat_tuples.append((op,) + values)

        con.add_satisfying_tuples(sat_tuples)
        csp.add_constraint(con)

    return csp, all_vars
