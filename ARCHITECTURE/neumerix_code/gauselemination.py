n = 3
matrix = [
    [2,1,1,10],
    [3,2,3,18],
    [1,4,9,16]
]

# row echolon form conevert
for i in range(n):
    for j in range(i+1,n):
        ratio = matrix[j][i] / matrix[i][i]

        for k in range(n+1):
            matrix[j][k] = matrix[j][k] - ratio*matrix[i][k]

#solving eqn:
x = [0]*3
for i in range(n-1,-1,-1):
   x[i] = matrix[i][n]
   for  j in range(i+1 ,n):
      x[i] = x[i] - matrix[i][j]*x[j]
   x[i] = x[i] / matrix[i][i]


for i in range(n):
    print("x", str(i+1),x[i])

    