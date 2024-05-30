import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt


def compute_state(L, x0, t):
    exp_Lt = expm(L * t)            #This function performs the continuous time state calculation 
    xt = np.dot(exp_Lt, x0)         #Expm calculates exponents of matrices
    return xt                       #The state space equation x dot = Ax is solved and its simplified solution is used for calculation

x0=np.array([6,4,7,5,4])

Adj=np.array([[0,1,0,0,0],[1,0,1,0,0],[0,1,0,1,1],[0,0,1,0,1],[0,0,1,1,0]])
#ADJ:
# 0,1,0,0,0
# 1,0,1,0,0
# 0,1,0,1,1
# 0,0,1,0,1
# 0,0,1,1,0

D = np.array([[1,0,0,0,0],[0,2,0,0,0],[0,0,3,0,0],[0,0,0,2,0],[0,0,0,0,2]])

L = np.subtract(D,Adj)

t_values = np.linspace(0, 5, 100)  # Time goes from first value to second value
                                   # Last parameter gives the steps of iterations

x_values = np.array([compute_state(-L, x0, t) for t in t_values])

print(x_values)                 
print("--------------------------")
#print(L)


plt.plot(t_values, x_values[:, 0], label='x1(t)')
plt.plot(t_values, x_values[:, 1], label='x2(t)')
plt.plot(t_values, x_values[:, 2], label='x3(t)')
plt.plot(t_values, x_values[:, 3], label='x4(t)')  
plt.plot(t_values, x_values[:, 4], label='x5(t)')
plt.xlabel('Time (t)')
plt.ylabel('State (x)')
plt.legend()
plt.title('State evolution over time')
plt.grid(True)
plt.show()
