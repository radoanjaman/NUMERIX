def f(x):
    return x**2 - 4*x -10

a = 4
b = 6
e = 0.0000001

while (b-a)/2 > e:
    mid = (a * f(b) - b*f(a))/(f(b) - f(a))
    if(f(a)*f(mid)<0):
        b = mid
    else: a= mid

print("Root:",mid)