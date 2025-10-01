# --------------- Bisection Method ---------------
# ---------- Import Necessary Libraries ----------

import matplotlib.pyplot as plt
import numpy as np

# ---------- Parameters ----------

a = -2 # the leftmost boundary value (float)
b = 1.5 # the rightmost boundary value (float)
tol = 1e-6 # tolerance value (float)
it = 100 # iterations (int), it > 0

# ---------- Bisection Code ----------

def f(x):
    """ 
    This is the function we are finding the root of, manipulate this to change the function 
    """
    return 3*(x+1)*(x-0.5)*(x-1)

def bisection(a,b):
    """
    Uses the bisection method to find the root of a function f(x) within the interval [a,b]
    Inputs:
    a : leftmost boundary value (float)
    b : float : rightmost boundary value (float)
    tol : float : tolerance value (float)
    it : int : number of iterations to perform (int), it > 0
    Outputs:
    m : float : approximated root value (float)
    Assumptions:
    f(a) and f(b) must have opposite signs
    """
    if f(a) * f(b) > 0: # bisection N/A
        print("The bisection method does not work under these conditions")
        return None
        
    for i in range(it): # multiple iterations of the function to find the root 
        m = (a+b)/2 # middle value
        
        if f(m) == 0 or abs(f(m)) < tol: # checks if m is within tol
            print(f"{m} is a root of the given function") # a root has been found no further work needed
            return m
            
        if f(a) * f(m) < 0: 
            b = m # this makes the m the new rightmost boundary as a and m have opposite signs 
        else: a = m # if a and m don't have opposite signs then b and m must have opposite signs making m the new leftmost boundary

    print(f"The approximate root value after {it} iterations is {m}")
    return m
root = bisection(a,b)
print(f"{root} is the approximated root after {it} iterations of the given function")
x_values = np.linspace(a,b,100)
y_values = f(x_values)
plt.plot(x_values,y_values, label='Function', color='dodgerblue')
plt.axhline(0, c='0', alpha=.5, linewidth=2)
plt.scatter(root, f(root), label=f"Root = {root:.6f}", color='crimson')
plt.title('Bisection Method Approximation')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.legend()
plt.show()