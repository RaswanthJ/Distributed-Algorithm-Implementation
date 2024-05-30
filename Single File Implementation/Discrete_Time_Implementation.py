import numpy as np
from scipy.linalg import expm
import matplotlib.pyplot as plt

x0=np.array([6,4,7,5,4])

Adj=np.array([[0,1,0,0,0],[1,0,1,0,0],[0,1,0,1,1],[0,0,1,0,1],[0,0,1,1,0]])

D = np.array([[1,0,0,0,0],[0,2,0,0,0],[0,0,3,0,0],[0,0,0,2,0],[0,0,0,0,2]])

L = np.subtract(D,Adj)

x=np.array(x0)
x=x.reshape(1,5)
t_values = [0]
h = 0.1
for i in range(1,100):
    t_values.append(i)
    xnew = x[i-1]+h*np.matmul(-L,x[i-1])
    xnew = xnew.reshape(1,5)
    x = np.append(x,xnew)
    x=x.reshape(i+1,5)

print(x[-1])


plt.plot(t_values, x[:, 0], label='x1(t)')
plt.plot(t_values, x[:, 1], label='x2(t)')
plt.plot(t_values, x[:, 2], label='x3(t)')
plt.plot(t_values, x[:, 3], label='x4(t)')  
plt.plot(t_values, x[:, 4], label='x5(t)')
plt.xlabel('Time (t)')
plt.ylabel('State (x)')
plt.legend()
plt.title('State evolution over time')
plt.grid(True)
plt.show()
