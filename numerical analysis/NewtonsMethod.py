# --------------- Newton's Method ---------------
# ---------- Import Necessary Libraries ----------

import matplotlib.pyplot as plt
import numpy as np

# ---------- Parameters ----------

a = 1 # the leftmost boundary value for plotting (float)
b = 2 # the rightmost boundary value for plotting (float)
p0 = 1.5 # initial guess (float)
tol = 1e-6 # tolerance (float)
it = 20 # iterations (int)

# ---------- Newton's Method Code ----------

def f(x): # = 0
    """
    This is the function we are finding the root of, manipulate this to change the function 
    """
    return (x**3)-x-1

def df(x): # f'(x)
    """
    This is the derivative of f(x), manipulate this to change the derivative 
    """
    return 3*(x**2)-1

def newton(p0):
    """
    Uses Newton's Method to find the root of function f(x) given an initial guess p0.
    Inputs:
    p0: initial guess (float)
    tol: tolerance value (float)
    it: number of iterations (int)
    Outputs:
    p: approximated root (float)
    Assumptions:
    f(x) is continous and differentiable near the root
    df(x) is not zero near the root
    Tip:
    Try using p0 values close to the actual root for better results
    """
    p = p0 # initialize p to the initial guess
    for i in range(it): # where the iterations happen
        if df(p) == 0: # newtons method does not work if the derivative is 0 or really close to 0
            print("VALUE ERROR: DF(P)=0") 
            return None 
        p_new = p - (f(p)/df(p)) # Newton's formula, i loveyou Sir Issac Newton
        if abs(p_new - p) < tol: # checks if results are within tolerance
            print(f"{p_new} is the approximated root of f(x) within tolerance {tol} after {i+1} iterations")
            return p_new
        p = p_new # finishing the iteration
    print(f"The approximated root of f(x) after {it} iterations is {p}") 
    return p 
root = newton(p0)

# ---------- Plot Results ---------
x_values = np.linspace(a,b,100)
y_values = f(x_values)
plt.plot(x_values,y_values, label='Function', color='dodgerblue')
plt.axhline(0, c='0', alpha=0.5, linewidth=2)
plt.scatter(root, f(root), label=f"Root = {root:.6f}", color='crimson')
plt.title('Newtons Method Approximation')
plt.xlabel('x')
plt.ylabel('f(x)')
plt.grid()
plt.legend()
plt.show()