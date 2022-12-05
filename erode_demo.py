import cv2.cv2 as cv
import numpy as np
import math
from skimage import morphology, draw
import matplotlib.pyplot as plt


def read_img_from_path(img_path):
    original = cv.imread(img_path, 0)
    img = original[0:1080, 3:1919]
    frame = cv.medianBlur(img, 3)
    frame = cv.GaussianBlur(frame, (3, 3), 0)
    frame = cv.bitwise_not(src=frame)
    return frame


# retval, threshold_img = cv.threshold(frame, 45, 255, cv.THRESH_BINARY+cv.THRESH_OTSU)


def stretch_gray(frame, index=2):
    e_img = np.zeros((frame.shape[0], frame.shape[1], 1), dtype=np.uint16)
    for i in range(e_img.shape[0]):
        for j in range(e_img.shape[1]):
            e_img[i, j] = math.pow(frame[i, j], index)
    cv.normalize(e_img, e_img, 0, 255, cv.NORM_MINMAX)
    gamma_img1 = cv.convertScaleAbs(e_img)
    # plt.hist(gamma_img1.ravel(), 256, [0, 256])
    # plt.title("Gray Value Hist1")
    # plt.show()
    return gamma_img1


# retval, threshold_img = cv.threshold(gamma_img1, 35, 255, cv.THRESH_BINARY)


def edge_by_dilated(threshold_frame):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # eroded = cv.erode(threshold_img, kernel)
    dilated = cv.dilate(threshold_frame, kernel)

    # res = cv.subtract(threshold_img, eroded)
    absdiff_img = cv.absdiff(dilated, threshold_frame)
    return absdiff_img


def dilated(frame):
    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
    # eroded = cv.erode(threshold_img, kernel)
    dilated = cv.dilate(frame, kernel)

    # res = cv.subtract(threshold_img, eroded)
    return dilated


def find_mid_line(threshold_image, p0, p1, p2, p3):
    threshold_image[threshold_image == 255] = 1
    skeleton0 = morphology.skeletonize(threshold_image)
    skeleton = skeleton0.astype(np.uint8) * 255
    h1 = []
    h2 = []
    sum1 = 0
    sum2 = 0
    # h = skeleton.shape[0]
    # w = skeleton.shape[1]
    for i in range(p0, p1):
        for j in range(p2, p3):
            sum1 = sum1 + skeleton[j, i]
        h1.append(sum1)
        sum1 = 0
    # hang
    # plt.plot(range(300, len(h1)+300), h1)
    # plt.xlabel("Position")
    # plt.ylabel("Value of Gray")
    # plt.show()
    for i in range(p2, p3):
        for j in range(p0, p1):
            sum2 = sum2 + skeleton[i, j]
        h2.append(sum2)
        sum2 = 0
    # print(h1)
    # plt.plot(range(40, len(h2)+40), h2)
    # plt.xlabel("Position")
    # plt.ylabel("Value of Gray")
    # plt.show()
    i1 = h1.index(max(h1)) + 300
    i2 = h2.index(max(h2)) + 40
    return i1, i2


# retval, threshold_img = cv.threshold(absdiff_img, 45, 255, cv.THRESH_BINARY)
# retval, threshold_img = cv.threshold(res, 40, 255, cv.THRESH_BINARY)
def find_end_point(t_img, h_point, v_point, height, width):
    record1 = []
    record2 = []
    for k in [-1, 0, 1]:
        for i in range(1, height-1):
            counter = 0
            if t_img[i - 1, h_point+k - 1] > 0:
                counter = counter + 1
            if t_img[i - 1, h_point+k] > 0:
                counter = counter + 1
            if t_img[i - 1, h_point+k + 1] > 0:
                counter = counter + 1
            if t_img[i, h_point+k - 1] > 0:
                counter = counter + 1
            # if t_img[i, h_point] > 0:
            #     counter = counter + 1
            if t_img[i, h_point+k + 1] > 0:
                counter = counter + 1
            if t_img[i + 1, h_point+k - 1] > 0:
                counter = counter + 1
            if t_img[i + 1, h_point+k] > 0:
                counter = counter + 1
            if t_img[i + 1, h_point+k + 1] > 0:
                counter = counter + 1
            if 2 <= counter <= 4:
                t_img[i, h_point+k] = 255
                # print(i)
                # print(counter)
                # record1.append(i)
    for q in [-1, 0, 1]:
        for j in range(10, width - 1):
            counter = 0
            if t_img[v_point+q - 1, j - 1] > 0:
                counter = counter + 1
            if t_img[v_point+q - 1, j] > 0:
                counter = counter + 1
            if t_img[v_point+q - 1, j + 1] > 0:
                counter = counter + 1
            if t_img[v_point+q, j - 1] > 0:
                counter = counter + 1
            # if t_img[i, h_point] > 0:
            #     counter = counter + 1
            if t_img[v_point+q, j + 1] > 0:
                counter = counter + 1
            if t_img[v_point+q + 1, j - 1] > 0:
                counter = counter + 1
            if t_img[v_point+q + 1, j] > 0:
                counter = counter + 1
            if t_img[v_point+q + 1, j + 1] > 0:
                counter = counter + 1
            if 2 <= counter <= 4:
                t_img[v_point+q, j] = 255
                # print(i)
                # print(counter)
                # record2.append(j)
    # return record1[0], record1[-1], record2[0], record2[-1]


if __name__ == '__main__':
    img_path_path = 'opencv_frame_4_6.png'
    frame0 = read_img_from_path(img_path_path)
    frame0 = stretch_gray(frame0, 2)
    ret, threshold_img = cv.threshold(frame0, 40, 255, cv.THRESH_BINARY)
    find_end_point(threshold_img, 957, 654, 1079, 1900)
    # print(end1, end2, end3, end4)
    abs_img = edge_by_dilated(threshold_img)
    # cv.imshow("Eroded Image", eroded)
    # cv.imshow("Dilated Image", dilated)
    # cv.imshow("subtract", res)
    # cv.imshow("diff", abs_img)
    # cv.imshow("t", threshold_img)
    cv.waitKey(0)
    cv.destroyAllWindows()
