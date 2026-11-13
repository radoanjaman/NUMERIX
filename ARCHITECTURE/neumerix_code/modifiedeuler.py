def dydx(x,y):
    return x + y
x = 0
y = 0
h = 0.1
n = int(input())
print("n \t x \t y")
for i in range(n+1):
    print(i,"\t",round(x,2),"\t",round(y,4))

    f1 = dydx(x,y)

    y1 = y+ h*f1
    f2 = dydx(x+h,y1)

    y = y + (h/2)*(f1 + f2)
    x += h
    