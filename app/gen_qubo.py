import numpy as np


# Functions for generating QUBOs, translating Ising to QUBO or vice versa should go here


# Example method fo converting Ising to QUBO
def ising_to_qubo(ising):
    return None


# Example method for generating a BPS QUBO
def gen_qubo_matrix(
    dist_matrix: list,
    penalty_factor: float = None,
    penalty_dist: float = None,
) -> np.ndarray:
    dist_matrix = np.array(dist_matrix)

    # the penalty factors ensure the satisfaction of all hard constraints
    if not penalty_dist:
        penalty_dist = 10

    if not penalty_factor:
        penalty_factor = penalty_dist * np.max(abs(np.array(dist_matrix))) + 1

    n_nodes = len(dist_matrix)

    # setup matrix for the traveling salesman problem
    qubo = np.zeros((n_nodes**2, n_nodes**2))

    # setup starting indices to build qubo blocks
    off_diag_idx = list(range(0, n_nodes**2, n_nodes))
    diag_idx = off_diag_idx[1:] + [off_diag_idx[0]]

    # each location visited exactly once (first term of HA in [1])
    # and only one-time use of existing paths (third term of HA in [1])
    for x_s in off_diag_idx:
        for y_s in off_diag_idx:
            for i in range(n_nodes):
                if x_s == y_s:
                    qubo[x_s + i][y_s + i] += -penalty_factor
                else:
                    qubo[x_s + i][y_s + i] += penalty_factor

    # start and end at the same location and travel from location to location
    # (second term of HA in [1])
    for x_s in diag_idx:
        for i in range(n_nodes):
            qubo[x_s + i][x_s + i] += -penalty_factor
            for j in range(n_nodes):
                if i != j:
                    qubo[x_s + i][x_s + j] += penalty_factor

    # optimization of the route (HB in [1])
    for x_b in off_diag_idx:
        for y_b in off_diag_idx:
            if x_b == y_b:
                continue
            for i in range(n_nodes):
                for j in range(n_nodes):
                    if i == j or (i + j) % 2 == 0:
                        continue
                    qubo[x_b + i][y_b + j] += (
                        penalty_dist * 0.5 * dist_matrix[x_b // n_nodes][y_b // n_nodes]
                    )

    return qubo