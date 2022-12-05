import math
import cv2.cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as img
from skimage import morphology
import time
from edgetest import gray_weight_latest, peak_value
from erode_demo import stretch_gray
from ite_weight_fit import ite_fit
import datetime
from scipy.optimize import curve_fit


def cal_prob_position(image):
    image = image[50:2000, 50:3000]
    h1 = []
    h2 = []
    sum1 = 0
    sum2 = 0
    h = image.shape[0]  # h = 1080
    w = image.shape[1]  # w = 1916
    for i in range(0, w):
        for j in range(0, h):
            sum1 = sum1 + image[j, i]
        h1.append(sum1)
        sum1 = 0
    # hang
    for i in range(0, h):
        for j in range(0, w):
            sum2 = sum2 + image[i, j]
        h2.append(sum2)
        sum2 = 0

    v = np.argmax(h1)  # v = 311
    v0 = np.argmax(h2)  # v0 = 279
    return v + 50, v0 + 50


def cal_prob_position_x(image):
    # h1 = []
    # sum1 = 0
    # h = image.shape[0]  # h = 2048
    # w = image.shape[1]  # w = 3072
    # for i in range(0, w):
    #     for j in range(0, h):
    #         sum1 = sum1 + image[j, i]
    #     h1.append(sum1)
    #     sum1 = 0
    # v = np.argmax(h1)  # v = 311
    lie = image.sum(axis=0)
    v = np.argmax(lie)
    return v


def cal_prob_position_y(image):
    # h2 = []
    # sum2 = 0
    # h = image.shape[0]  # h = 1080
    # w = image.shape[1]  # w = 1916
    # # hang
    # for i in range(0, h):
    #     for j in range(0, w):
    #         sum2 = sum2 + image[i, j]
    #     h2.append(sum2)
    #     sum2 = 0
    hang = image.sum(axis=1)
    v0 = np.argmax(hang)  # v0 = 279
    return v0


def dilated(image):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (60, 60))
    # eroded = cv.erode(threshold_img, kernel)
    dilated__image = cv.dilate(image, kernel)

    # res = cv.subtract(threshold_img, eroded)
    return dilated__image


def dilated2(image):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # eroded = cv.erode(threshold_img, kernel)
    dilated = cv.dilate(image, kernel)

    # res = cv.subtract(threshold_img, eroded)
    return dilated


def eroded(image):
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (90, 90))
    eroded_image = cv.erode(image, kernel)
    return eroded_image


def fit(image, height1, height2, width1, width2):
    x_num = []
    num = []
    for i in range(height1, height2):
        dst1 = gray_weight_latest(image, i, width1, width2)
        # dst2 = gray_weight2(frameT, i, v0)
        if np.isnan(dst1):
            continue
        x_num.append(i)
        num.append(dst1)
    return x_num, num


def fit_peak(image, height1, height2, width1, width2):
    x_num = []
    num = []
    for i in range(height1, height2):
        dst1 = peak_value(image, i, width1, width2)
        # dst2 = gray_weight2(frameT, i, v0)
        if np.isnan(dst1):
            continue
        x_num.append(i)
        num.append(dst1)
    return x_num, num


def fit_fork_peak(image, height1, height2, midline):
    x_num = []
    num = []
    fork1 = []
    fork2 = []
    for i in range(height1, height2):
        dst1 = peak_value(image, i, midline - 80, midline)
        dst2 = peak_value(image, i, midline, midline + 80)
        # dst2 = gray_weight2(frameT, i, v0)
        if np.isnan(dst1) or np.isnan(dst2):
            continue
        x_num.append(i)
        num.append((dst1 + dst2) / 2)
        fork1.append(dst1)
        fork2.append(dst2)
    return x_num, num, fork1, fork2


def fit_fork(image, height1, height2, midline):
    x_num = []
    num = []
    fork1 = []
    fork2 = []
    for i in range(height1, height2):
        dst1 = gray_weight_latest(image, i, midline - 80, midline)
        dst2 = gray_weight_latest(image, i, midline, midline + 80)
        # dst2 = gray_weight2(frameT, i, v0)
        if np.isnan(dst1) or np.isnan(dst2):
            continue
        x_num.append(i)
        num.append((dst1 + dst2) / 2)
        fork1.append(dst1)
        fork2.append(dst2)
    return x_num, num, fork1, fork2


def guss_fit(x, a, sigma, miu):
    return a * np.exp(-((x - miu) ** 2) / (2 * sigma ** 2))


def fit_gauss(image, height1, height2, width1, width2):
    x_num = []
    num = []
    x0 = np.linspace(0, 49, 50)
    for i in range(height1, height2):
        y1 = image[i][width1: width2]
        popt1, pcov1 = curve_fit(guss_fit, x0, y1, maxfev=500000)
        s1 = width1 + popt1[2]
        if np.isnan(s1) or s1 > 2000:
            continue
        x_num.append(i)
        num.append(s1)
    return x_num, num


def fit_fork_gauss(image, height1, height2, midline):
    x_num = []
    num = []
    fork1 = []
    fork2 = []
    x0 = np.linspace(0, 79, 80)
    for i in range(height1, height2):
        y1 = image[i][midline - 80: midline]
        y2 = image[i][midline: midline + 80]
        popt1, pcov1 = curve_fit(guss_fit, x0, y1, maxfev=500000)
        popt2, pcov2 = curve_fit(guss_fit, x0, y2, maxfev=500000)
        s1 = midline - 80 + popt1[2]
        s2 = midline + popt2[2]
        if np.isnan(s1) or np.isnan(s2) or s1 > 2000 or s2 > 2000:
            continue
        x_num.append(i)
        num.append((s1 + s2) / 2)
        fork1.append(s1)
        fork2.append(s2)
    return x_num, num, fork1, fork2


def skeleton_image(threshold_image):
    threshold_image[threshold_image == 255] = 1
    skeleton0 = morphology.skeletonize(threshold_image)
    skeleton = skeleton0.astype(np.uint8) * 255
    return skeleton


def cal_mean(ls):
    return np.mean(ls)


def cal_repeat(ls, mean):
    v = 0
    times = len(ls)
    for element in ls:
        v = v + (element - mean) ** 2
    return math.sqrt(v / (times - 1))


def gamma_trans(image, gamma):
    I = image / 255.0
    O = np.power(I, gamma)
    R = O * 255
    R = np.round(R)
    R = R.astype(np.uint8)
    return R


if __name__ == '__main__':
    k0 = []
    num_0 = []
    k_inf = []
    num_inf = []
    k_neg = []
    num_pos = []
    k_pos = []
    num_neg = []
    test = cv.imread("../10_170.png", 0)
    original_image = plt.imread("../10_170.png")
    t1 = datetime.datetime.now()
    h = t1.hour
    min = t1.minute
    sec = t1.second
    print('time:{}:{}:{}'.format(h, min, sec))
    t2 = time.time()
    # t3 = time.clock()
    print(t1)
    print(t2)
    # print(t3)
    a1 = time.time()
    ret, threshold_img0 = cv.threshold(test, 0, 255, cv.THRESH_OTSU)
    dilatedimage = dilated(threshold_img0)
    eroded_img = eroded(dilatedimage)
    eroded_img[eroded_img == 255] = 1
    a2 = time.time()
    print(a2 - a1)
    # res1 = eroded_img * test
    # res1[res1 == 0] = 255

    # src = test[0:1080, 3:1919]
    src = cv.bitwise_not(src=test)
    src1 = src * eroded_img
    a9 = time.time()
    sobel_x = cv.Sobel(src, ddepth=-1, dx=1, dy=0)
    # grad_x = cv.convertScaleAbs(sobel_x)
    sx = sobel_x * eroded_img
    sobel_y = cv.Sobel(src, ddepth=-1, dx=0, dy=1)
    sy = sobel_y * eroded_img
    # sobel_xy = sobel_y + sobel_x
    i = cal_prob_position_x(sx)
    j = cal_prob_position_y(sy)
    a4 = time.time()
    print(a4 - a9)
    # sobel_xy = cv.Sobel(src,ddepth=-1, dx=1, dy=1)
    # i, j = cal_prob_position(src)
    src_c = src[j - 400: j + 400, i - 400:i+400]
    # src_c = stretch_gray(src_c, 2)

    fe = gamma_trans(src1, gamma=1)
    #
    ret2, threshold_img2 = cv.threshold(sy, 0, 255, cv.THRESH_TRIANGLE + cv.THRESH_BINARY)
    # ret3, threshold_img3 = cv.threshold(src1, 85, 255, cv.THRESH_BINARY)
    # print('bug')
    # dilatedimage = dilated2(threshold_img3)
    # dilatedimage[dilatedimage == 255] = 1
    # frame_new = src1 * dilatedimage
    #
    skeleton_img = skeleton_image(threshold_image=threshold_img2)
    print('bug')
    # frame1 = stretch_gray(src1, 2)
    # ret, threshold_img = cv.threshold(frame1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # skeleton_img = skeleton_image(threshold_img)
    # skeleton_img = skeleton_img[0:828, 0:900]
    # minLineLength = 20
    # maxLineGap = 5
    # lines = cv.HoughLines(skeleton_img, 1, np.pi / 180, 50)
    # lines1 = lines[:, 0, :]
    # for rho, theta in lines1[:]:
    #     # k = (y2 - y1) / (x2 - x1)
    #     print(rho, theta)
    #     # if not (np.isnan(k)):
    #     #     if -0.02 <= k <= 0.02:
    #     #         k0.append(k)
    #     #         num_0.append(x1)
    #     #         num_0.append(y1)zg
    #     #         num_0.append(x2)
    #     #         num_0.append(y2)
    #     #
    #     #     if k == np.inf or k == np.inf * (-1):
    #     #         k_inf.append(k)
    #     #         num_inf.append(x1)
    #     #         num_inf.append(y1)
    #     #         num_inf.append(x2)
    #     #         num_inf.append(y2)
    #     #
    #     #     if 0 < k <= 0.5:
    #     #         k_pos.append(k)
    #     #     if -0.5 <= k < 0:
    #     #         k_neg.append(k)
    #     #
    #     # cv.line(test, (x1, y1), (x2, y2), (255, 0, 0), 2)
    # res = cv.cvtColor(test, cv.COLOR_GRAY2RGB)
    # plt.imshow(res)
    # plt.show()
    # dilatedimage = dilated2(threshold_img)
    # eroded_img = eroded(threshold_img)
    # ret, threshold_img = cv.threshold(src1, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    # dilatedimage = dilated2(threshold_img)
    # dilatedimage[dilatedimage == 255] = 1
    # frame_new = src1 * dilatedimage
    a3 = time.time()
    frame_new = fe
    # print(i, j)
    # q = [], v = []
    img_t = np.transpose(frame_new)
    top1 = j - 700
    bottom1 = j + 700
    left1 = i - 700
    right1 = i + 700
    if top1 <= 0:
        top1 = 0
    if bottom1 >= 2048:
        bottom1 = 2048
    q1, v1 = fit_gauss(frame_new, top1, j - 100, i - 25, i + 25)
    q2, v2 = fit_gauss(frame_new, j + 100, bottom1, i - 25, i + 25)
    q3, v3, fork1_1, fork_2 = fit_fork_gauss(img_t, left1, i - 100, j)
    q4, v4 = fit_gauss(img_t, i + 100, right1, j - 25, j + 25)

    q1_sum, v1_sum = q1 + q2, v1 + v2
    q3_sum, v3_sum = q3 + q4, v3 + v4

    k2, b2 = ite_fit(x_num=q3_sum, y_num=v3_sum, max_ite=1)
    k1, b1 = ite_fit(x_num=q1_sum, y_num=v1_sum, max_ite=1)

    x = (k1 * b2 + b1) / (1 - k2 * k1)
    y = (k2 * b1 + b2) / (1 - k2 * k1)

    x = round(x, 2)
    y = round(y, 2)
    a5 = time.time()
    print("runtime{}".format(a5 - a3))

    s_1 = []
    s_2 = []
    for i in range(0, len(q1_sum)):
        s_1.append(k1 * v1_sum[i] + b1 - q1_sum[i])
    for i in range(0, len(q3)):
        s_2.append(k2 * v3_sum[i] + b2 - q3_sum[i])
    plt.plot(range(0, len(s_1)), s_1)
    plt.show()
    plt.plot(range(0, len(s_2)), s_2)
    plt.show()

    predict01 = []
    for i in range(0, len(q1_sum)):
        predict01.append(k1 * q1_sum[i] + b1)
    plt.plot(q1_sum, v1_sum, 'o')
    plt.plot(q1_sum, predict01)
    plt.show()

    predict02 = []
    for i in range(0, len(q3_sum)):
        predict02.append(k2 * q3_sum[i] + b2)
    plt.plot(q3_sum, v3_sum, 'o')
    plt.plot(q3_sum, predict02)
    plt.show()

    markersize = 4

    plt.plot(v1_sum, q1_sum, 'o', markersize=markersize)
    plt.plot(predict01, q1_sum, markersize=markersize)

    plt.plot(q3, fork1_1, 'o', markersize=markersize)
    plt.plot(q3, fork_2, 'o', markersize=markersize)
    plt.plot(q4, v4, 'o', markersize=markersize)

    plt.plot(q3_sum, predict02, markersize=markersize)

    plt.imshow(original_image)
    plt.show()
    print(x, y)

    print("---------")
