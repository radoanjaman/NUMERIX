def func(x):
    return x**2 - 4*x - 10
def derivatives(x):
    return 2*x - 4

a = 6
e = 0.000000001

while(True):
    a_new = a - (func(a))/(derivatives(a))
    if(abs(a_new - a) < e):
        break
    a = a_new

print("Root: ", a_new)