from sklearn.metrics import mean_squared_error

from erode_demo import stretch_gray, find_mid_line, dilated
from fit import *
# 解决中文显示问题
from Level_Cam.edgetest import gray_weight_latest
from Level_Cam.ite_weight_fit import ite_fit

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
POINT = 25
ID = 1
ns = 10
# while(1):
#     cap = cv.VideoCapture(ID)
#     # get a frame
#     ret, frame = cap.read()
#     if ret == False:
#         ID += 1
#     else:
#         print(ID)
#         break

cam = cv.VideoCapture(5)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 3072)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 2048)
img_counter = 0

ks = np.load('./npdata/k_0705.npy')
kx_fix = np.load('./npdata/theta_fix_0705_n.npy')

k_x = ks[0][0]
k_y = ks[0][1]
# theta_cal = ks[0][2]
theta = kx_fix[0][0]
p = ks[0][3]
h0 = ks[0][4]
v_0 = ks[0][5]
print(k_x, k_y, theta, p)
delta_v = 0
delta_h = 0
v_res = 0
h_res = 0

flag = 1
n_s_i = 0
n_s_j = 0
num1 = []
num2 = []
num3 = []
num4 = []

x_num1 = []
x_num2 = []
x_num3 = []
x_num4 = []

v_save = []
h_save = []
cali_res = []

while cam.isOpened():

    # saveVideoPath = 'video_1_' + str(start) + '.avi'
    # out = cv.VideoWriter(saveVideoPath, fourcc, 30.0, (1920, 1080))

    ret, frame = cam.read()
    show = frame.copy()
    # show = cv.flip(show, 1, dst=None)
    show = cv.rectangle(show, (450, 50), (1550, 1000), (152, 54, 255), 4, 4)
    # cam.set(3, 1920)  # width=1920
    # cam.set(4, 1080)  # height=1080
    # # method 2:
    # cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    # cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    cv.namedWindow("test", cv.WINDOW_FREERATIO)
    # show = cv.rectangle(frame, (450, 50), (1550, 1000), (152, 54, 255), 4, 4)
    cv.imshow("test", show)

    if not ret:
        break
    key = cv.waitKey(1) & 0xFF

    if key == 27:
        # press ESC to escape (ESC ASCII value: 27)
        print("Escape hit, closing...")
        break

    elif key == 115:
        # press s to save image (s ASCII value: 115)
        img_name = "10_18_1{}.png".format(img_counter)
        cv.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1

    elif key == 32:

        sum1 = 0
        sum2 = 0
        # flag = 1
        # n_s_i = 0
        h1 = deque()
        h2 = deque()

        # t = input("please input the type of cross image, if: [-|-], please input 0, if: [-|<], please input 1, "
        #           "if: [>|-], please input 2:  ")
        # # t = int(t)
        # while t != '0' and t != '1' and t != '2':
        #     print("image type error, please re-input ")
        #     t = input("please input the type of cross image, if: [-|-], please input 0, if: [-|<], please input 1, "
        #               "if: [>|-], please input 2: ")
        # t = int(t)
        t = 0
        # flag_v = v_res
        # flag_h = h_res
        # press Space to capture image (Space ASCII value: 32)
        # img_name = "opencv_frame_{}.png".format(img_counter)
        # cv.imwrite(img_name, frame)
        # print("{} written!".format(img_name))
        # img_counter += 1
        src = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        src = src[0:1080, 3:1919]
        if t == 2:
            src = cv.flip(src, 1, dst=None)
        frame = cv.medianBlur(src, 3)
        frame = cv.GaussianBlur(frame, (3, 3), 0)
        frame = cv.bitwise_not(src=frame)

        frame1 = stretch_gray(frame, 2)

        ret, threshold_img = cv.threshold(frame, 35, 255, cv.THRESH_BINARY)
        # cv.imshow("threshold", threshold_img)
        dilated_img = dilated(threshold_img)
        dilated_img[dilated_img == 255] = 1
        frame_new = frame1 * dilated_img

        threshold_img_copy = threshold_img.copy()
        # find th mid line if the image
        rec0 = 300
        rec1 = 1400
        rec2 = 40
        rec3 = 1040
        h1, v1 = find_mid_line(threshold_img_copy, rec0, rec1, rec2, rec3)
        print("pixel: ", h1, v1)

        # abs_img = edge_by_dilated(threshold_img)

        # a, b, c, d = find_zone(abs_img, h1, v1)
        start_v = h1 - 15
        end_v = h1 + 15

        start_h = v1 - 15
        end_h = v1 + 15

        img_t = np.transpose(frame_new)

        for i in range(0, 500):
            dst1 = gray_weight_latest(frame_new, i, start_v, end_v)
            # dst2 = gray_weight2(frameT, i, v0)
            if np.isnan(dst1):
                continue
            x_num1.append(i)
            num1.append(dst1)
        for i in range(0, 500):
            # dst1 = gray_weight(src, i, v)
            dst2 = gray_weight_latest(img_t, i, start_h, end_h)
            if np.isnan(dst2):
                continue
            x_num2.append(i)
            num2.append(dst2)

        door1 = end_h + 450
        door2 = end_v + 500
        if v1 + 450 >= 1040:
            door1 = 1040
        for i in range(v1 + 100, door1):
            dst3 = gray_weight_latest(frame1, i, start_v, end_v)
            # dst4 = gray_weight2(frameT, i, v0)
            if np.isnan(dst3):
                continue
            x_num3.append(i)
            num3.append(dst3)
        if h1 + 500 >= 1400:
            door2 = 1400
        for i in range(h1 + 100, door2):
            # dst1 = gray_weight(frame, i, v)
            dst4 = gray_weight_latest(img_t, i, start_h, end_h)
            # dst5 = gray_weight_wide2(frameT, i, v0)
            if np.isnan(dst4):
                continue
            x_num4.append(i)
            num4.append(dst4)

        point1 = len(num4)
        print(point1)
        num2 = num2 + num4
        num1 = num1 + num3
        x_num2 = x_num2 + x_num4
        x_num1 = x_num1 + x_num3
        a11, b11, popt1 = fit_line(num2, x_num2)
        c11, d11, popt2 = fit_line(num1, x_num1)
        # c = 1/c
        # d = -d/c
        vi = []
        vi_1 = []
        num2_1 = []
        predict = []
        predict_1 = []

        vs_sum = 0
        vs_sum_1 = 0
        for i in range(0, len(num2)):
            # vi.append(a*i+b - num2[i])
            # predict.append(line_fit(i, *popt1))
            predict.append(a11 * x_num2[i] + b11)
            # vs = line_fit(i, *popt1) - num2[i]
            vs = predict[i] - num2[i]
            vs_sum = vs_sum + vs ** 2
            vi.append(abs(vs))

        k2, b2 = ite_fit(x_num=x_num2, y_num=num2, max_ite=1)
        k1, b1 = ite_fit(x_num=x_num1, y_num=num1, max_ite=1)

        # s_1 = []
        # s_2 = []
        # for i in range(0, len(num1)):
        #     s_1.append(k1 * x_num1[i] + b1 - num1[i])
        # for i in range(0, len(num2)):
        #     s_2.append(k2 * x_num2[i] + b2 - num2[i])
        # plt.plot(range(0, len(s_1)), s_1)
        # plt.show()
        # plt.plot(range(0, len(s_2)), s_2)
        # plt.show()
        #
        # predict01 = []
        # for i in range(0, len(x_num1)):
        #     predict01.append(k1 * x_num1[i] + b1)
        # plt.plot(x_num1, num1, 'o')
        # plt.plot(x_num1, predict01)
        # plt.show()
        #
        # predict02 = []
        # for i in range(0, len(x_num2)):
        #     predict02.append(k2 * x_num2[i] + b2)
        # plt.plot(x_num2, num2, 'o')
        # plt.plot(x_num2, predict02)
        # plt.show()

        predict_y = []
        vs_sum_y = 0
        vi_y = []
        vi_y_1 = []
        num_1_1 = []
        predict_y_1 = []
        vs_sum_y_1 = 0
        for i in range(0, len(num1)):
            # vi.append(a*i+b - num2[i])
            # predict.append(line_fit(i, *popt1))
            predict_y.append(c11 * x_num1[i] + d11)
            # vs = line_fit(i, *popt1) - num2[i]
            vs = predict_y[i] - num1[i]
            vs_sum_y = vs_sum_y + vs ** 2
            vi_y.append(vs)
        xi_y = np.linspace(0, len(num1) - 1, len(num1))
        y_predict_y = c11 * xi_y + d11
        theta_1 = (vs_sum_y / (len(num1) - 1)) ** 0.5
        # print(len(predict_y))
        # print(theta_1)
        mse_y = mean_squared_error(num1, predict_y)
        rmse_y = np.sqrt(mse_y)

        x = (k1 * b2 + b1) / (1 - k2 * k1)
        y = (k2 * b1 + b2) / (1 - k2 * k1)

        x = round(x, 1)
        y = round(y, 1)

        cali_res_i = str(x) + ', ' + str(y)
        print(cali_res_i)
        cali_res.append(cali_res_i)

        # x0 = (c11 * b11 + d11) / (1 - a11 * c11)
        # y0 = (a11 * d11 + b11) / (1 - a11 * c11)
        # x0 = round(x0, 2)
        # y0 = round(y0, 2)
        #
        # cali_res_i_0 = str(x0) + ', ' + str(y0)
        # print(cali_res_i_0)
        # y = a * x + b
        f0 = np.zeros((2, 1))
        f0[0][0] = 957.5
        f0[1][0] = 539.5

        f1 = np.zeros((2, 1))
        f1[0][0] = x
        f1[1][0] = y

        ki = np.zeros((2, 2))
        ki[0][0] = k_x
        ki[0][1] = k_x * p - k_y * theta
        ki[1][0] = k_x * theta
        ki[1][1] = k_x * theta * p + k_y

        v_h = np.dot(ki, f1)
        v_h_0 = np.dot(ki, f0)

        v_h[0][0] = v_h[0][0] + h0
        v_h[1][0] = v_h[1][0] + v_0

        v_h_0[0][0] = v_h_0[0][0] + h0
        v_h_0[1][0] = v_h_0[1][0] + v_0

        h_res = v_h[0][0]
        v_res = v_h[1][0]

        h_res_0 = v_h_0[0][0]
        v_res_0 = v_h_0[1][0]

        delta_v = v_res - v_res_0
        delta_h = h_res - h_res_0

        delta_v = round(delta_v, 2)
        delta_h = round(delta_h, 2)

        print("delta_h: ", delta_h)
        print("delta_v: ", delta_v)
        n_s_i = n_s_i + delta_v
        n_s_j = n_s_j + delta_h*(-1)
        v_save.append(delta_v)
        h_save.append(delta_h*(-1))
        if flag % 5 == 0:
            # n_s_i = n_s_i + delta_v
            res_delta_v = n_s_i / 5
            res_delta_h = n_s_j / 5
            print("----------------")
            print("res_v: ", res_delta_v)
            print("res_h: ", res_delta_h)
            n_s_i = 0
            n_s_j = 0
            with open("data/analyze_07_03_v_1.txt", 'a') as f:
                for i in v_save:
                    f.write(str(i) + ',')
                f.write('\n')
                v_save.clear()
            # # with open("./data/analyze_06_27_h.txt", 'a') as fo:
            # #     for e in h_save:
            # #         fo.write(str(e) + ',')
            # #     fo.write('\n')
            # #     h_save.clear()

        flag = flag + 1

        num1.clear()
        num2.clear()
        num3.clear()
        num4.clear()

        x_num1.clear()
        x_num2.clear()
        x_num3.clear()
        x_num4.clear()

        # center = (int(x), int(y))
        # point_size = 1
        # point_color = (0, 0, 255)  # BGR
        # thickness = 8  # 可以为 0 、4、8
        #
        # cv.circle(frame, center, 3, point_color, thickness)
        #
        # # cv.namedWindow("point", cv.WINDOW_FREERATIO)
        # # cv.imshow("point", frame)
        # # cv.imwrite("data/res_p.png", frame)
        #
        # res_f = cv.cvtColor(frame, cv.COLOR_GRAY2RGB)
        #
        # ptStart = (0, int(b2))
        # ptEnd = (1400, int(1400 * k2 + b2))
        # point_color = (255, 0, 0)  # BGR
        # thickness = 2
        # lineType = 4
        # cv.line(res_f, ptStart, ptEnd, point_color, thickness, lineType)
        # cv.circle(res_f, center, 5, (0, 0, 255), -1, 0)
        #
        # ptStart = (int(b1), 0)
        # ptEnd = (int(1079 * k1 + b1), 1079)
        # point_color = (0, 255, 0)  # BGR
        # thickness = 2
        # lineType = 8
        # cv.line(res_f, ptStart, ptEnd, point_color, thickness, lineType)
        # #
        # # # cv.imwrite("data/res_f.png", res_f)
        # # # res_f = cv.cvtColor(frame, cv.COLOR_GRAY2RGB);
        # cv.namedWindow("res", cv.WINDOW_FREERATIO)
        # cv.imshow("res", res_f)

    else:
        pass

# np_cali_res = np.array(cali_res)
# np.save('./npdata/cali_theta_data_0705.npy', np_cali_res)

cam.release()
cv.destroyAllWindows()
