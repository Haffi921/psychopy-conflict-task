import numpy as np
from numpy.random import default_rng

n = 24

weight_matrix = np.array([[1, 1], [1, 1]])
weight_matrix_sum = weight_matrix.sum()

probability_matrix = np.zeros(weight_matrix.shape)


for i in range(weight_matrix.size):
    probability_matrix.flat[i] = n * weight_matrix.flat[i] / weight_matrix_sum

shape = probability_matrix.shape
dimensions = len(shape)
indices = [i for i, _ in np.ndenumerate(probability_matrix)]

rng = default_rng()
print(probability_matrix)
restarts = 0
while True:
    sequence = []
    probability_matrix_copy = probability_matrix.copy()
    for i in range(n):
        new_index_valid = False
        rand_ind = rng.choice(len(indices), len(indices), replace=False)
        if len(sequence) == 0:
            new_index = indices[rand_ind[0]]
            sequence.append(new_index)
            probability_matrix_copy[tuple(new_index)] -= 1
            new_index_valid = True
            continue
        else:
            for j in rand_ind:
                new_index = indices[j]
                if probability_matrix_copy[tuple(new_index)] <= 0:
                    continue
                if new_index[0] == sequence[-1][1]:
                    sequence.append(new_index)
                    probability_matrix_copy[tuple(new_index)] -= 1
                    new_index_valid = True
                    break
        if new_index_valid:
            continue
        else:
            break
    else:
        break
    restarts += 1
print(sequence)

first = True
seq_text = ""
for i in sequence:
    if first:
        for j in i:
            seq_text += str(j)
    else:
        seq_text += str(i[-1])

print(seq_text)

# last_index = []
# new_index = []

# for i in shape:
#     new_index.append(randint(i))

# probability_matrix[tuple(new_index)] -= 1


# sequence.append(new_index)
# last_index = sequence[-1]

# # Get possibilities
# possibilities = []
# for i in range(len(probability_matrix[last_index[-1]])):
#     possibilities.append([last_index[-1], i])

# new_index = possibilities[randint(len(possibilities))]

# sequence.append(new_index)
# last_index = new_index

# print(sequence)

# for i in range(len(weight_matrix.A1)):
#     probability_matrix.A1[i] = weight_matrix.A1[i] / weight_matrix_sum

# print(probability_matrix)