
n = 3

matrix = [
    [2, 1, 1, 10],
    [3, 2, 3, 18],
    [1, 4, 9, 16]
]


for i in range(n):

   
    pivot = matrix[i][i]

    for j in range(n + 1):
        matrix[i][j] = matrix[i][j] / pivot


    for k in range(n):

        if k != i:
            ratio = matrix[k][i]

            for j in range(n + 1):
                matrix[k][j] = matrix[k][j] - ratio * matrix[i][j]


print("Solution:")

for i in range(n):
    print("x" + str(i + 1), "=", round(matrix[i][n], 2))
