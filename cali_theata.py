import numpy as np
ks = np.load('./npdata/k_0705.npy')
kx_fix = np.load('./npdata/theta_fix.npy')

k_x = ks[0][0]
k_y = ks[0][1]
# theta_cal = ks[0][2]
theta_cal = kx_fix[0][0]
p = ks[0][3]

cali_data_n = np.load('./npdata/cali_theta_data_0705.npy')
cali_data_l = []
o1 = []
o2 = []
n_x = []
n_y = []
for i in range(1, len(cali_data_n)):
    cali_data_l.append(cali_data_n[i])
test_cali_data = np.array(cali_data_l)
for i in range(0, len(test_cali_data)):
    data = test_cali_data[i].split(',')
    o1.append(float(data[0].replace(',', '')))
    o2.append(float(data[1].replace(',', '')))
print(o1)
print(o2)
for i in range(0, len(o1)):
    new_x = k_x*o1[i] + k_x*p*o2[i]
    new_y = k_y*o2[i]
    n_x.append(new_x)
    n_y.append(new_y)

print(n_x)
print(n_y)
y = np.array(n_y)
y1 = y.reshape(-1, 1)
print(y1)
size = test_cali_data.shape[0]
print(size)
C_THETA = np.zeros((size, 2))
for i in range(0, C_THETA.shape[0]):
    C_THETA[i][0] = n_x[i]
    C_THETA[i][1] = 1
print(C_THETA)
C_THETA_T = np.transpose(C_THETA)
c_s = np.dot(C_THETA_T, C_THETA)
C_THETA_mat = np.matrix(c_s)
C_THETA_inv = C_THETA_mat.I
res_cali_theta = C_THETA_inv * C_THETA_T * y1
print(res_cali_theta)
print(res_cali_theta[0][0])
np.save('./npdata/theta_fix_0705_n.npy', res_cali_theta)


