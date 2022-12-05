import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# 1.读入图片
# img = cv.imread('../opencv_frame_4_7.png', 0)
# img = img[0:1080, 3:1919]
# # cv.imshow("0", img)
# img = cv.medianBlur(img, 3)
# # cv.imshow("i", img)
#
# # gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# frame = cv.bitwise_not(src=img)
# # cv.imshow("gray", gray_img)
#
# # 2.canny边缘检测
# canny = cv.Canny(frame, 50, 110)
# cv.imshow("canny", canny)


def find_zone(edge, h_x, v_y):
    h1 = []
    h2 = []
    sum1 = 0
    sum2 = 0
    h = edge.shape[0]
    w = edge.shape[1]
    for i in range(0, w):
        for j in range(0, h):
            sum1 = sum1 + edge[j, i]
        h1.append(sum1)
        sum1 = 0
    # hang
    for i in range(0, h):
        for j in range(0, w):
            sum2 = sum2 + edge[i, j]
        h2.append(sum2)
        sum2 = 0
    # print(h1)
    i_1_0 = h1[0: h_x]
    i_1_1 = h1[h_x: w]
    i1 = i_1_0.index(max(i_1_0))
    i1s = i_1_1.index(max(i_1_1)) + h_x

    i_2_0 = h2[0: v_y]
    i_2_1 = h2[v_y: h]
    i2 = i_2_0.index(max(i_2_0))
    i2s = i_2_1.index(max(i_2_1)) + v_y

    print(i1, i1s, i2, i2s)
    # # print(len(h1))
    # # print(i)
    # h1.pop(i1)
    # h2.pop(i2)
    # # print(len(h1))
    # j1 = h1.index(max(h1))
    # if j1 >= i1:
    #     j1 = j1 + 1
    # j2 = h2.index(max(h2))
    # if j2 >= i2:
    #     j2 = j2 + 1
    # print(j)
    # # sorted(h1)
    # # sorted(h2)
    # print(h2)
    # print(i2, j2)
    length1 = int(round((abs(i1s - i1) + 1), 0))
    length2 = int(round((abs(i2s - i2) + 1), 0))
    print(length2)
    start1 = min(i1, i1s) - 1*length1
    end1 = max(i1, i1s) + 1*length1
    start2 = min(i2, i2s) - 1*length2
    end2 = max(i2, i2s) + 1*length2
    print(start1, end1, start2, end2)
    # return start1, end1, start2, end2
    return i1, i1s+1, i2, i2s+1


# a, b, c, d = find_zone(canny)
# print(a, b, c, d)


def find_t(f, start, end, index):
    frame0 = f[0:300, start:end+1]
    plt.figure()
    plt.hist(frame0.flatten(), bins=256)
    plt.xlim(0, 256)
    plt.xlabel("gray value")
    plt.ylabel("number of pixels")
    plt.title("Gray Value Hist")
    plt.text(200, 175, "index = "+str(index))
    plt.show()
    # ret1, img11 = cv.threshold(frame0, 0, 255, cv.THRESH_OTSU)
    # print(ret1)
    # return ret1


# t1 = find_t(frame, a, b)
# print(t1)
# ret, img11 = cv.threshold(frame, t1, 0, cv.THRESH_TOZERO)

# global res


def gray_weight_latest(image, i, start, end):
    # T = T1
    # if pos-T/2<0 :
    #     T = pos
    # if pos + T/2 > img.shape[1]:
    #     T = img.shape[1] - pos
    # global res
    # global res
    # global res
    src = image[i][start: end]
    # cv.imshow("before", src)
    # dst = cv.resize(src, dsize=(1, 60), interpolation=cv.INTER_LANCZOS4)
    # dst3 = np.transpose(dst)[0]
    # cv.imshow("after", dst3)
    weight = 0
    t = 0
    for k in range(0, len(src)):
        weight = weight + k * src[k]**2
        t = t + src[k]**2
        if t == 0:
            # print("t==0")
            continue
    try:
        res = start + weight / t
    except ZeroDivisionError:
        print("error: ZeroDivisionError t==0")
    # print("灰度重心法，第" + str(i) + "次： " + str(res))
    return res


def peak_value(image, i, start, end):

    d = 0
    src = image[i][start: end]

    if src.size != 0:
        d = np.argmax(src)

    return d + start


def prewitt(image):
    kernelx = np.array([[1, 1, 1], [0, 0, 0], [-1, -1, -1]], dtype=int)
    kernely = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=int)
    x = cv.filter2D(image, cv.CV_16S, kernelx)
    y = cv.filter2D(image, cv.CV_16S, kernely)
    absX = cv.convertScaleAbs(x)
    absY = cv.convertScaleAbs(y)
    Prewitt = cv.addWeighted(absX, 0.5, absY, 0.5, 0)
    return Prewitt

# img_t = np.transpose(img11)
# res = gray_weight_latest(img_t, 20, c, d)
# print(res)
#
# # cv.imshow("s", img11)
# cv.waitKey()
# cv.destroyAllWindows()