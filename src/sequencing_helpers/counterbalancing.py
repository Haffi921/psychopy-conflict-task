import numpy as np
from numpy.random import choice

from .util import Alternator


def counterbalance(
    trials: int,
    factor_levels: list,
    levels: int = 1,
    alternating: int = False,
    alternator_start: int = 0,
    Force=False,
    verbose=False,
    initial_seed=None,
):
    def create_base_matrix(trials, shape):
        base_matrix = np.zeros(shape)
        for i in range(base_matrix.size):
            base_matrix.flat[i] = trials / base_matrix.size
        return base_matrix

    def create_condition_indices(condition_levels):
        return [i for i, _ in np.ndenumerate(np.zeros(condition_levels))]

    def create_random_index_sequence(length):
        return choice(length, length, replace=False)

    def construct_initial_seed(dimensions, matrix, unsuccessful_seeds=[]):
        if len(unsuccessful_seeds) >= matrix.size:
            return None
        initial_seed = []
        for dim in range(dimensions):
            initial_seed.append(np.random.randint(matrix.shape[dim]))
        if tuple(initial_seed) in unsuccessful_seeds:
            return construct_initial_seed(dimensions, matrix, unsuccessful_seeds)
        else:
            return initial_seed

    def check_available_conditions(condition_array: np.matrix):
        index_sequence = create_random_index_sequence(condition_array.size)
        for index in index_sequence:
            if condition_array[index] > 0:
                return index
        return None

    def check_for_parameter_errors():
        if not type(factor_levels) == list or len(factor_levels) == 0:
            raise ValueError(
                "'condition_levels' has to be a list with a length of at least 1"
            )

        if alternating < 0:
            raise ValueError("'alternating' cannot be a negative number")

        if levels < 1:
            raise ValueError("'level' has to be 1 or higher")
        elif levels >= 3:
            Warning(
                "Increased levels could make the algorithm unsolvable. Currently it has only been tested on 'level' = 1 or 2"
            )

    # ---------------------------------------------------------- #
    # Algorithm begins                                           #
    # ---------------------------------------------------------- #
    check_for_parameter_errors()

    dimensions = levels + 1
    length = np.prod(factor_levels)
    matrix_shape = [length] * dimensions

    if alternating:
        alternating_levels = int(alternating) + 1
        factor_levels.insert(0, alternating_levels)
        matrix_shape.insert(0, alternating_levels)

    condition_indices = create_condition_indices(factor_levels)
    base_matrix = create_base_matrix(trials, matrix_shape)

    if not Force:
        for i in base_matrix.flat:
            if i % 1 != 0:
                raise RuntimeError(
                    f"Number of trials not a whole number product of counterbalancing conditions: {trials} / {base_matrix.size} = {trials / base_matrix.size}"
                )

    if verbose:
        print(f"Creating a counterbalanced {trials}-trial sequence")
        if alternating:
            print(
                f"Using {length} possible conditions in {dimensions} dimensions, alternating between {alternating_levels} instances"
            )
            print(
                f"Comes down to {(length**dimensions) * alternating_levels} counterbalancing conditions"
            )
        else:
            print(f"Using {length} possible conditions in {dimensions} dimensions")

    first_trial = None
    restarts = 0
    unsuccessful_seed_list = []
    seed_tried = 0

    while True:
        cb_sequence = []
        cb_matrix = base_matrix.copy()
        if alternating:
            alternator = Alternator(alternating_levels, start=alternator_start)

        # Absolute initial seed
        if initial_seed is None:
            initial_seed = construct_initial_seed(dimensions, cb_matrix)

        # If seed is tried too many times, reset and get a new seed
        if seed_tried >= cb_matrix.size * 3:
            unsuccessful_seed_list.append(initial_seed)
            initial_seed = construct_initial_seed(
                dimensions, cb_matrix, unsuccessful_seed_list
            )
            if initial_seed is None:
                raise RuntimeError(
                    "Counterbalanced sequence impossible with given parameters"
                )
            seed_tried = 0

        # Anytime a seed is new
        if seed_tried == 0:
            if alternating:
                initial_seed.insert(0, alternator.index)
                first_trial = initial_seed[-2] + (length * alternator.what_was_prev())
            else:
                first_trial = initial_seed[-2]

        seed_tried += 1
        cb_sequence.append(tuple(initial_seed))
        cb_matrix[tuple(initial_seed)] -= 1

        for _ in range(trials - 1):
            new_index = []

            if alternating:
                alternator.next()
                new_index.append(alternator.index)

            for dim in reversed(range(1, dimensions)):
                new_index.append(cb_sequence[-1][-dim])

            last_index_number = check_available_conditions(cb_matrix[tuple(new_index)])

            if last_index_number is not None:
                new_index.append(last_index_number)
            else:
                if verbose:
                    print("Restarting")
                restarts += 1
                break

            cb_sequence.append(tuple(new_index))
            cb_matrix[tuple(new_index)] -= 1
        else:
            break

    raw_sequence = [first_trial]
    for cb in cb_sequence:
        if alternating:
            raw_sequence.append(cb[-1] + (length * cb[0]))
        else:
            raw_sequence.append(cb[-1])

    sequence = []
    for raw in raw_sequence:
        sequence.append(condition_indices[raw])

    if verbose:
        print(f"Restarts: {restarts}")

    return sequence
