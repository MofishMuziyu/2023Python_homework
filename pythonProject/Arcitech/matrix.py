m = 4
n = 4
k = 4
A = [i for i in range(n)]*m
B = [j for j in range(k)]*n
C = [0 for k in range(k)]*m
##不分块
for i in range(m):
    for j in range(k):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

##f分块
for i in range(m):
    for j in range(k):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

for i in range(m):
    for j in range(k):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

for i in range(m):
    for j in range(k):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

for i in range(m):
    for j in range(k):
        for k in range(n):
            C[i][j] += A[i][k] * B[k][j]

