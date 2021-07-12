import numpy as np
from numpy.random import choice

from conflict_task.util import Alternator

trials = 32

sequential_conditions = {
    "Congruency": 2,
    "Value": 2,
}

alternating_conditions = {
    "Hand": 2,
}

alternating = True

levels = 1

condition_keys = list(sequential_conditions.keys())
condition_levels = list(sequential_conditions.values())


dimensions = levels + 1
length = np.prod(condition_levels)
matrix_shape = [length] * dimensions

if alternating:
    condition_keys = list(alternating_conditions.keys()) + condition_keys

    # Levels of each alternating condition
    a_condition_levels = list(alternating_conditions.values())

    # Total length of alternating levels
    alternating_length = np.prod(a_condition_levels)

    # Complete the condition levels
    condition_levels = a_condition_levels + condition_levels

    # Add alternating dimension
    matrix_shape.insert(0, alternating_length)

condition_indices = [i for i, _ in np.ndenumerate(np.zeros(condition_levels))]
base_matrix = np.zeros(matrix_shape)

for i in range(base_matrix.size):
    base_matrix.flat[i] = trials / base_matrix.size

def get_initial_seed(dimensions):
    initial_seed = []
    for dim in range(dimensions):
        initial_seed.append(np.random.randint(base_matrix.shape[dim]))
    return initial_seed

restart = False
restarts = 0
while True:
    probability_matrix = base_matrix.copy()
    raw_sequence = []
    initial_seed = get_initial_seed(dimensions)

    if alternating:
        alternator = Alternator(alternating_length)
        working_matrix = probability_matrix[alternator.index]
        initial_seed.insert(0, alternator.index)
    else:
        working_matrix = probability_matrix
    
    raw_sequence.append(tuple(initial_seed))
    probability_matrix[raw_sequence[-1]] -= 1

    for _ in range(trials - 1):
        if alternating:
            alternator.next()
            working_matrix = probability_matrix[alternator.index]

        new_index = []
        for dim in range(1, dimensions):
            new_index.append(raw_sequence[-1][-dim])
        
        new_index.reverse()

        last_digits = choice(length, length, replace=False)
        for last_digit in last_digits:
            if working_matrix[tuple(new_index)][last_digit] > 0:
                new_index.append(last_digit)
                break
        else:
            restart = True

        if restart:
            restart = False
            restarts += 1
            break
        
        if alternating:
            new_index.insert(0, alternator.index)

        raw_sequence.append(tuple(new_index))
        probability_matrix[raw_sequence[-1]] -= 1
    else:
        break

print(f"Restarts: {restarts}")

sequence = [condition_indices[raw_sequence[0][-2] + (length * (alternating_length - 1))]]
for raw in raw_sequence:
    sequence.append(condition_indices[raw[-1] + (length * raw[0])])
print(condition_keys)
print(sequence)


