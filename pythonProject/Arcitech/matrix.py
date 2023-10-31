# import numpy as np
# m = 4
# n = 4
# k = 4
# A = np.random.randint(0, 10, size=(4, 4))
# B = np.random.randint(0, 10, size=(4, 4))
# C = np.random.randint(0, 10, size=(4, 4))
# ##不分块
# for i in range(m):
#     for j in range(k):
#         for k in range(n):
#             C[i][j] += A[i][k] * B[k][j]

##f分块
# for i in range(m):
#     for j in range(k):
#         for k in range(n):
#             C[i][j] += A[i][k] * B[k][j]
#
# for i in range(m):
#     for j in range(k):
#         for k in range(n):
#             C[i][j] += A[i][k] * B[k][j]
#
# for i in range(m):
#     for j in range(k):
#         for k in range(n):
#             C[i][j] += A[i][k] * B[k][j]
#
# for i in range(m):
#     for j in range(k):
#         for k in range(n):
#             C[i][j] += A[i][k] * B[k][j]
#
import numpy as np

def block_matrix_multiply(matrix_A, matrix_B, block_size):
    if matrix_A.shape[1] != matrix_B.shape[0]:
        raise ValueError("Matrix dimensions do not match for multiplication")

    result_matrix = np.zeros((matrix_A.shape[0], matrix_B.shape[1]))

    for i in range(0, matrix_A.shape[0], block_size):
        for j in range(0, matrix_B.shape[1], block_size):
            for k in range(0, matrix_A.shape[1], block_size):
                A_block = matrix_A[i:min(i+block_size, matrix_A.shape[0]), k:min(k+block_size, matrix_A.shape[1])]
                B_block = matrix_B[k:min(k+block_size, matrix_B.shape[0]), j:min(j+block_size, matrix_B.shape[1])]
                result_block = np.matmul(A_block, B_block)
                result_matrix[i:min(i+block_size, matrix_A.shape[0]), j:min(j+block_size, matrix_B.shape[1])] += result_block
    return result_matrix

# Test the function
A = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]])
B = np.array([[17, 18, 19, 20], [21, 22, 23, 24], [25, 26, 27, 28], [29, 30, 31, 32]])
block_size = 2

print(block_matrix_multiply(A, B, block_size))