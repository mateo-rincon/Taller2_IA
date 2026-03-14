from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from algorithms.problems_csp import DroneAssignmentCSP


def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Basic backtracking search without optimizations.

    Tips:
    - An assignment is a dictionary mapping variables to values (e.g. {X1: Cell(1,2), X2: Cell(3,4)}).
    - Use csp.assign(var, value, assignment) to assign a value to a variable.
    - Use csp.unassign(var, assignment) to unassign a variable.
    - Use csp.is_consistent(var, value, assignment) to check if an assignment is consistent with the constraints.
    - Use csp.is_complete(assignment) to check if the assignment is complete (all variables assigned).
    - Use csp.get_unassigned_variables(assignment) to get a list of unassigned variables.
    - Use csp.domains[var] to get the list of possible values for a variable.
    - Use csp.get_neighbors(var) to get the list of variables that share a constraint with var.
    - Add logs to measure how good your implementation is (e.g. number of assignments, backtracks).

    You can find inspiration in the textbook's pseudocode:
    Artificial Intelligence: A Modern Approach (4th Edition) by Russell and Norvig, Chapter 5: Constraint Satisfaction Problems
    """
    #PROMPT: considerando el taller que te subi anteriormente, cree el siguiente codigo de backtracking_search. Ayudame a modificarlo para cumplir con el enunciado.
    """def backtracking_search(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    assignment = {}
    result = backtracking(csp, assignment)
    return result

    def backtracking(csp: DroneAssignmentCSP, assignment:dict[str, str])-> dict [str, str] | None:
        if csp.is_complete(assignment):
            return assignment
        var = csp.get_unassigned_variables(assignment)
        for element in var:
            for value in csp.domains[element]:
                if csp.is_consistent(element, value, assignment):
                    csp.assign(element, value, assignment)
                    result = backtracking(csp, assignment)
                    if result is not None:
                        return result
                    csp.unassign(element, assignment)
        return None
        

    """
    assignment = {}
    return backtracking(csp, assignment)


def backtracking(csp: DroneAssignmentCSP, assignment: dict[str, str]) -> dict[str, str] | None:
    if csp.is_complete(assignment):
        return assignment.copy()

    var = csp.get_unassigned_variables(assignment)[0]

    for value in csp.domains[var]:
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)

            result = backtracking(csp, assignment)
            if result is not None:
                return result

            csp.unassign(var, assignment)

    return None
    


def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with Forward Checking.

    Tips:
    - Forward checking: After assigning a value to a variable, eliminate inconsistent values from
      the domains of unassigned neighbors. If any neighbor's domain becomes empty, backtrack immediately.
    - Save domains before forward checking so you can restore them on backtrack.
    - Use csp.get_neighbors(var) to get variables that share constraints with var.
    - Use csp.is_consistent(neighbor, val, assignment) to check if a value is still consistent.
    - Forward checking reduces the search space by detecting failures earlier than basic backtracking.
    """
    #PROMPT: considerando el taller que te subi anteriormente, cree el siguiente codigo de backtracking_fc. Ayudame a modificarlo para cumplir con el enunciado.
    """
    def backtracking_fc(csp: DroneAssignmentCSP) -> dict[str, str] | None:
        assignment = {}
        result = backtrackingFC(csp, assignment)
        return result

    def backtrackingFC(csp: DroneAssignmentCSP, assignment:dict[str, str])-> dict [str, str] | None:
            if csp.is_complete(assignment):
                return assignment
            var = csp.get_unassigned_variables(assignment)
            for element in var:
                for value in csp.domains[element]:
                    if csp.is_consistent(element, value, assignment):
                        csp.assign(element, value, assignment)
                        vecinos = csp.get_neighbors(element)
                        for vecino in csp.domains[vecinos]:
                            if not csp.is_consistent(vecino, value, assignment):
                                csp.domains[vecino].remove(value)
                        result = backtracking(csp, assignment)
                        if result is not None:
                            return result
                        csp.unassign(element, assignment)
            return None
    """
    assignment = {}
    domains = {var: list(values) for var, values in csp.domains.items()}
    return backtrack_fc(csp, assignment, domains)

def forward_check(
    csp: DroneAssignmentCSP,
    var: str,
    assignment: dict[str, str],
    domains: dict[str, list[str]],
) -> bool:
    for neighbor in csp.get_neighbors(var):
        if neighbor in assignment:
            continue

        valid_values = []
        for value in domains[neighbor]:
            if csp.is_consistent(neighbor, value, assignment):
                valid_values.append(value)

        domains[neighbor] = valid_values

        if len(domains[neighbor]) == 0:
            return False

    return True


def backtrack_fc(
    csp: DroneAssignmentCSP,
    assignment: dict[str, str],
    domains: dict[str, list[str]],
) -> dict[str, str] | None:
    if csp.is_complete(assignment):
        return assignment.copy()

    var = csp.get_unassigned_variables(assignment)[0]

    for value in domains[var]:
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)

            saved_domains = {v: list(vals) for v, vals in domains.items()}
            domains[var] = [value]

            if forward_check(csp, var, assignment, domains):
                result = backtrack_fc(csp, assignment, domains)
                if result is not None:
                    return result

            domains.clear()
            domains.update(saved_domains)
            csp.unassign(var, assignment)

    return None

def backtracking_ac3(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking search with AC-3 arc consistency.

    Tips:
    - AC-3 enforces arc consistency: for every pair of constrained variables (Xi, Xj), every value
      in Xi's domain must have at least one supporting value in Xj's domain.
    - Run AC-3 before starting backtracking to reduce domains globally.
    - After each assignment, run AC-3 on arcs involving the assigned variable's neighbors.
    - If AC-3 empties any domain, the current assignment is inconsistent - backtrack.
    - You can create helper functions such as:
      - a values_compatible function to check if two variable-value pairs are consistent with the constraints.
      - a revise function that removes unsupported values from one variable's domain.
      - an ac3 function that manages the queue of arcs to check and calls revise.
      - a backtrack function that integrates AC-3 into the search process.
    """
    #PROMPT: considerando el taller que te subi anteriormente, cree el siguiente codigo de backtracking_ac3. Ayudame a modificarlo para cumplir con el enunciado.
    """assignment = {}
    domains = csp.domains.copy()

    queue = []
    for xi in csp.domains:
        for xj in csp.get_neighbors(xi):
            queue.append((xi, xj))

    if not ac3(csp, domains, queue):
        return None

    return backtrack_ac3(csp, assignment, domains)

def values_compatible(csp: DroneAssignmentCSP, xi, x, xj, y) -> bool:
    temp_assignment = {xi: x, xj: y}
    return (
        csp.is_consistent(xi, x, temp_assignment)
        and csp.is_consistent(xj, y, temp_assignment)
    )


def revise(csp: DroneAssignmentCSP, xi, xj, domains) -> bool:
    revised = False
    values_to_remove = []

    for x in domains[xi]:
        supported = False
        for y in domains[xj]:
            if values_compatible(csp, xi, x, xj, y):
                supported = True
                break

        if not supported:
            values_to_remove.append(x)

    for x in values_to_remove:
        domains[xi].remove(x)
        revised = True

    return revised


def ac3(csp: DroneAssignmentCSP, domains, queue) -> bool:
    while queue:
        xi, xj = queue.pop(0)

        if revise(csp, xi, xj, domains):
            if len(domains[xi]) == 0:
                return False

            for xk in csp.get_neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))

    return True


def backtrack_ac3(csp: DroneAssignmentCSP, assignment, domains) -> dict[str, str] | None:
    if csp.is_complete(assignment):
        return assignment

    unassigned = csp.get_unassigned_variables(assignment)
    var = unassigned[0]

    for value in list(domains[var]):
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)

            saved_domains = domains.copy()
            domains[var] = [value]

            queue = []
            for neighbor in csp.get_neighbors(var):
                if neighbor not in assignment:
                    queue.append((neighbor, var))

            if ac3(csp, domains, queue):
                result = backtrack_ac3(csp, assignment, domains)
                if result is not None:
                    return result

            domains.clear()
            domains.update(csp.saved_domains.copy())
            csp.unassign(var, assignment)

    return None"""
    
    assignment = {}
    domains = {var: list(values) for var, values in csp.domains.items()}

    queue = []
    for xi in csp.domains:
        for xj in csp.get_neighbors(xi):
            queue.append((xi, xj))

    if not ac3(csp, domains, queue):
        return None

    return backtrack_ac3(csp, assignment, domains)


def values_compatible(csp: DroneAssignmentCSP, xi, x, xj, y) -> bool:
    assignment_for_xi = {xj: y}
    assignment_for_xj = {xi: x}

    return (
        csp.is_consistent(xi, x, assignment_for_xi)
        and csp.is_consistent(xj, y, assignment_for_xj)
    )


def revise(csp: DroneAssignmentCSP, xi, xj, domains) -> bool:
    revised = False
    values_to_remove = []

    for x in domains[xi]:
        supported = False
        for y in domains[xj]:
            if values_compatible(csp, xi, x, xj, y):
                supported = True
                break

        if not supported:
            values_to_remove.append(x)

    for x in values_to_remove:
        domains[xi].remove(x)
        revised = True

    return revised


def ac3(csp: DroneAssignmentCSP, domains, queue) -> bool:
    while queue:
        xi, xj = queue.pop(0)

        if revise(csp, xi, xj, domains):
            if len(domains[xi]) == 0:
                return False

            for xk in csp.get_neighbors(xi):
                if xk != xj:
                    queue.append((xk, xi))

    return True


def backtrack_ac3(csp: DroneAssignmentCSP, assignment, domains) -> dict[str, str] | None:
    if csp.is_complete(assignment):
        return assignment.copy()

    unassigned = csp.get_unassigned_variables(assignment)
    var = unassigned[0]

    for value in list(domains[var]):
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)

            saved_domains = {v: list(vals) for v, vals in domains.items()}
            domains[var] = [value]

            queue = []
            for neighbor in csp.get_neighbors(var):
                if neighbor not in assignment:
                    queue.append((neighbor, var))

            if ac3(csp, domains, queue):
                result = backtrack_ac3(csp, assignment, domains)
                if result is not None:
                    return result

            domains.clear()
            domains.update(saved_domains)
            csp.unassign(var, assignment)

    return None


def backtracking_mrv_lcv(csp: DroneAssignmentCSP) -> dict[str, str] | None:
    """
    Backtracking with Forward Checking + MRV + LCV.

    Tips:
    - Combine the techniques from backtracking_fc, mrv_heuristic, and lcv_heuristic.
    - MRV (Minimum Remaining Values): Select the unassigned variable with the fewest legal values.
      Tie-break by degree: prefer the variable with the most unassigned neighbors.
    - LCV (Least Constraining Value): When ordering values for a variable, prefer
      values that rule out the fewest choices for neighboring variables.
    - Use csp.get_num_conflicts(var, value, assignment) to count how many values would be ruled out for neighbors if var=value is assigned.
    """
        #PROMPT: considerando el taller que te subi anteriormente, cree el siguiente codigo de backtracking_mrv_lcv. Ayudame a modificarlo para cumplir con el enunciado.
    """assignment = {}
    domains = csp.domains.copy()
    return backtrack_mrv_lcv(csp, assignment, domains)


def forward_check(
    csp: DroneAssignmentCSP,
    var: str,
    assignment: dict[str, str],
    domains: dict[str, list[str]],
) -> bool:
    for neighbor in csp.get_neighbors(var):
        if neighbor in assignment:
            continue

        valid_values = []
        for value in domains[neighbor]:
            if csp.is_consistent(neighbor, value, assignment):
                valid_values.append(value)

        domains[neighbor] = valid_values

        if len(domains[neighbor]) == 0:
            return False

    return True


def select_unassigned_variable_mrv(
    csp: DroneAssignmentCSP,
    assignment: dict[str, str],
    domains: dict[str, list[str]],
) -> str:
    unassigned = csp.get_unassigned_variables(assignment)

    return min(
        unassigned,
        key=lambda var: (
            len(domains[var]),
            -sum(1 for neighbor in csp.get_neighbors(var) if neighbor not in assignment),
        ),
    )


def order_domain_values_lcv(
    csp: DroneAssignmentCSP,
    var: str,
    assignment: dict[str, str],
    domains: dict[str, list[str]],
) -> list[str]:
    valid_values = [
        value for value in domains[var]
        if csp.is_consistent(var, value, assignment)
    ]

    return sorted(
        valid_values,
        key=lambda value: csp.get_num_conflicts(var, value, assignment)
    )


def backtrack_mrv_lcv(
    csp: DroneAssignmentCSP,
    assignment: dict[str, str],
    domains: dict[str, list[str]],
) -> dict[str, str] | None:
    if csp.is_complete(assignment):
        return assignment

    var = select_unassigned_variable_mrv(csp, assignment, domains)

    for value in order_domain_values_lcv(csp, var, assignment, domains):
        if csp.is_consistent(var, value, assignment):
            csp.assign(var, value, assignment)

            saved_domains = domains.copy()
            domains[var] = [value]

            if forward_check(csp, var, assignment, domains):
                result = backtrack_mrv_lcv(csp, assignment, domains)
                if result is not None:
                    return result

            domains.clear()
            domains.update(saved_domains.copy())
            csp.unassign(var, assignment)

    return None"""

