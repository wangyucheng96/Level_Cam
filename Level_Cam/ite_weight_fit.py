import numpy as np
from numpy.linalg import *
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error


def iter_weight_fit(x_ls, y_ls, vweights):
    # weight = 1
    x1 = 0
    x2 = 0
    x3 = 0
    y1 = 0
    y2 = 0
    for i in range(0, len(x_ls)):
        weight = vweights[i]
        x = x_ls[i]
        y = y_ls[i]
        x1 = x1 + weight * x ** 2
        x2 = x2 + weight * x
        x3 = x3 + weight
        y1 = y1 + weight * x * y
        y2 = y2 + weight * y
    G = np.zeros((2, 2))
    G[0, 0] = x1
    G[0, 1] = x2
    G[1, 0] = x2
    G[1, 1] = x3
    l = np.zeros((2, 1))
    l[0, 0] = y1
    l[1, 0] = y2
    # res = np.zeros((2, 1))
    # G_MAT = np.matrix(G)
    # G_inv = G_MAT.I
    # res = G_inv*l
    res = solve(G, l)
    k = res[0, 0]
    b = res[1, 0]
    return k, b


def ite_fit(x_num, y_num, max_ite):
    vWeights = [1 for _ in range(len(x_num))]
    k, b = iter_weight_fit(x_num, y_num, vWeights)
    predict00 = []
    for i in range(0, len(x_num)):
        predict00.append(k * x_num[i] + b)
    # print("ko, bo ", k, b)
    mse0 = mean_squared_error(y_num, predict00)
    # print("mse weight = 1: ", mse0)
    # plt.plot(x_num, y_num, 'o')
    # plt.plot(x_num, predict00, color='green')
    # plt.show()
    for ite in range(0, max_ite):
        dist = []
        for i in range(0, len(x_num)):
            dist.append(abs(k * x_num[i] + b - y_num[i]))
        vi_copy = dist.copy()
        vi_copy.sort()
        sigma = vi_copy[int(len(vi_copy) / 2)] / 0.675
        sigma = sigma * 1
        vWeights.clear()
        for j in range(0, len(dist)):
            if dist[j] <= sigma:
                rate = dist[j] / sigma
                weight = pow(1 - rate ** 2, 2)
            else:
                weight = 0
            vWeights.append(weight)
        k, b = iter_weight_fit(x_num, y_num, vWeights)
        # print("k ,b", k, b)
        predict001 = []
        for i in range(0, len(x_num)):
            predict001.append(k * x_num[i] + b)
        mse1 = mean_squared_error(y_num, predict001)
        # print("mse, ite = ", ite + 1, ": ", mse1)
        # plt.plot(x_num, y_num, 'o')
    #     plt.plot(x_num, predict001)
    # plt.show()
    res_k = k
    res_b = b
    return k, b


if __name__ == '__main__':
    x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
    y = np.array([1.2, 1.1, 1.0, 1.3, 1.4, 1.5, 1.2, 0.9, 2.3, 2.5, 2.4, 2.6, 1.2, 1.3, 1.1, 1.0, 1.1,
                  1.2, 1.4, 1.5, 1.2, 1.2, 1.1, 1.4, 1.3, 1.2, 1.1, 1.2, 1.3, 1.2])
    print(np.std(y))
    ite_fit(x, y, 4)
