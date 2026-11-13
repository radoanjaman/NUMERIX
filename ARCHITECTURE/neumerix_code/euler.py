def derivatives(x):
    return 2*x

x =1
y = 1
h = 0.1
n = int(input("Enter n: "))
print(" n\t X\t Y")
for i in range(n+1):
    print(i,"\t",round(x,2),"\t",round(y,4))
    y = y + h*derivatives(x)
    x = x+h

print("res: ", y)