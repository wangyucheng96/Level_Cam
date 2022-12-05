import numpy as np

k = np.load('./npdata/res2.npy')
a = k[0][0]
b = k[1][0]
c = k[2][0]
d = k[3][0]
h0 = k[4][0]
v0 = k[5][0]
k_x = a
theta = c/a
k_y = (a**2*d - a*b*c)/(a**2 + c**2)
p = (a*b + d*c)/(a**2 + c**2)
print(k_x, theta, k_y, p)
k1 = np.zeros((1, 6))
k1[0][0] = k_x
k1[0][1] = k_y
k1[0][2] = theta
k1[0][3] = p
k1[0][4] = h0
k1[0][5] = v0
print(k1)
np.save('./npdata/k_0705.npy', k1)
f1 = np.zeros((2, 1))
print(f1)
