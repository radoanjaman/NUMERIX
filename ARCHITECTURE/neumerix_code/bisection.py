def func(x):
    return x**2 - 4*x - 10

a = 4
b = 6
e = 0.0001

while( (b-a)/2 > e):
    mid = (b+a)/2
    if(func(a) * func(mid) < 0):
        b = mid
    else :
        a = mid


print("Root: ", mid)