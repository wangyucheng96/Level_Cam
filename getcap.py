from fit import *
from erode_demo import *
# 解决中文显示问题
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

cam = cv.VideoCapture(0)
cam.set(cv.CAP_PROP_FRAME_WIDTH, 1920)
cam.set(cv.CAP_PROP_FRAME_HEIGHT, 1080)
img_counter = 0

ks = np.load('npdata/k.npy')
kx_fix = np.load('npdata/theta_fix.npy')

k_x = ks[0][0]
k_y = ks[0][1]
# theta_cal = ks[0][2]
theta_cal = kx_fix[0][0]
p = ks[0][3]
h0 = ks[0][4]
v_0 = ks[0][5]

delta_v = 0
delta_h = 0
v_res = 0
h_res = 0

flag = 1
n_s_i = 0

counter = 0
min_record = -8

num1 = []
num2 = []
num3 = []
num4 = []

x_num1 = []
x_num2 = []
x_num3 = []
x_num4 = []

v_save = []
cali_res = []

# fourcc = cv.VideoWriter_fourcc(*'MJPG')
start = -8

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
        img_name = "opencv_frame_4_{}.png".format(img_counter)
        cv.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        img_counter += 1
    # elif key == 118:
    #     # press v to save video (v ASCII value: 115)
    #     print("writing begin")
    #     num_counter = 0
    #     while num_counter <= 540:
    #         rets, frames = cam.read()
    #         cv.waitKey(1)
    #         out.write(frames)
    #         num_counter = num_counter + 1
    #     start = start + 2
    #     print("write is done")
    elif key == 32:
        # time.sleep(30)
        # t = 0
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

        src = cv.bitwise_not(src=src)
        ret1, src = cv.threshold(src, 38, 0, cv.THRESH_TOZERO)
        # ret2, src = cv.threshold(src, 35, 255, cv.THRESH_BINARY)
        test = cv.medianBlur(src, 3)
        # cv.namedWindow("original_image_1", cv.WINDOW_FREERATIO)
        # cv.imshow("original_image_1", src)
        # lie
        # t = input("please input the type of cross image, if: [-|-], please input 0, if: [-|<], please input 1: ")
        # # t = int(t)
        # while t != '0' and t != '1':
        #     print("image type error, please re-input ")
        #     t = input("please input the type of cross image, if: [-|-], please input 0, if: [-|<], please input 1: ")
        # t = int(t)

        for i in range(0, 1916):
            for j in range(0, 1080):
                sum1 = sum1 + test[j, i]
            h1.append(sum1)
            sum1 = 0
        # hang
        for i in range(0, 1080):
            for j in range(0, 1916):
                sum2 = sum2 + test[i, j]
            h2.append(sum2)
            sum2 = 0

        v = np.argmax(h1)  # v = 311
        v0 = np.argmax(h2)  # v0 = 279
        print("v : " + str(v))
        print("v0 : " + str(v0))
        frameT = np.transpose(src)
        # for i in range(2, 402):
        #     dst1 = gray_weight(frame, i, v)
        #     dst2 = gray_weight2(frame, i, v0)
        #     num1.append(dst1)
        #     num2.append(dst2)
        # for i in range(2, 402):
        #     dst1 = fit_gaosi(frame, i, v)
        #     dst2 = fit_gaosi(frame, i, v0)
        #     num1.append(dst1)
        #     num2.append(dst2)
        if v0 - 25 < 2 or v - 25 < 2:
            print("too edge")
            break
        for i in range(2, v0 - 25):
            dst1 = gray_weight(src, i, v)
            # dst2 = gray_weight2(frameT, i, v0)
            if np.isnan(dst1):
                continue
            num1.append(dst1)
        for i in range(2, v - 25):
            # dst1 = gray_weight(src, i, v)
            dst2 = gray_weight2(frameT, i, v0)
            if np.isnan(dst2):
                continue
            num2.append(dst2)
        if t == 1 or t == 2:
            door1 = v0 + 450
            door2 = v + 410
            if v0 + 450 >= 1079:
                door1 = 1079
            for i in range(v0 + 50, door1):
                dst3 = gray_weight(src, i, v)
                # dst4 = gray_weight2(frameT, i, v0)
                if np.isnan(dst3):
                    continue
                num3.append(dst3)
            if v + 410 >= 1915:
                door2 = 1915
            for i in range(v + 20, door2):
                # dst1 = gray_weight(frame, i, v)
                dst4 = gray_weight_wide(frameT, i, v0)
                dst5 = gray_weight_wide2(frameT, i, v0)
                if np.isnan(dst4) or np.isnan(dst5):
                    continue
                dst6 = (dst4 + dst5) / 2
                num4.append(dst6)

        elif t == 0:
            door3 = v0 + 390
            door4 = v + 410
            if v0 + 390 >= 1079:
                door3 = 1079
            for i in range(v0 + 10, door3):
                dst3 = gray_weight(src, i, v)
                # dst4 = gray_weight2(frameT, i, v0)
                if np.isnan(dst3):
                    continue
                num3.append(dst3)
                # num4.append(dst4)
            if v + 410 >= 1915:
                door4 = 1915
            for i in range(v + 20, door4):
                # dst3 = gray_weight(src, i, v)
                dst4 = gray_weight2(frameT, i, v0)
                if np.isnan(dst4):
                    continue
                # num3.append(dst3)
                num4.append(dst4)
        # 边界问题还得改
        # for i in range(v + 10, v + 410):
        #     # dst1 = gray_weight(frame, i, v)
        #     dst4 = gray_weight_wide(frameT, i, v0)
        #     dst5 = gray_weight_wide2(frameT, i, v0)
        #     if np.isnan(dst4) or np.isnan(dst5):
        #         continue
        #     dst6 = (dst4 + dst5) / 2
        #     num4.append(dst6)

        # space1 = np.linspace(0, 399, 400)
        # space2 = np.linspace(0, 99, 100)
        num2 = num2 + num4
        num1 = num1 + num3
        pointer2 = len(num2)
        pointer3 = len(num1)
        space3 = np.linspace(0, pointer3 - 1, pointer3)
        space4 = np.linspace(0, pointer2 - 1, pointer2)
        a, b, popt1 = fit_line(num2, space4)
        c, d, popt2 = fit_line(num1, space3)
        # a, b = fit_line(num2, space1)
        # c, d = fit_line(num1, space1)
        # c = 1/c
        # d = -d/c
        # vi = []
        # vi_1 = []
        # num2_1 = []
        # vs_sum = 0
        # vs_sum_1 = 0
        # for i in range(0, len(num2)):
        #     # vi.append(a*i+b - num2[i])
        #     vs = line_fit(i, *popt1) - num2[i]
        #     vs_sum = vs_sum + vs ** 2
        #     vi.append(vs)
        # xi = np.linspace(0, len(num2) - 1, len(num2))
        # theta = (vs_sum / (len(num2) - 1)) ** 0.5
        # # print(theta)
        # # print(a, b)
        # # print(c, d)
        # #
        # # print(a, b)
        # # print(c, d)
        # for i in range(0, len(num2)):
        #     # vi.append(a*i+b - num2[i])
        #     vs_1 = line_fit(i, *popt1) - num2[i]
        #     num2_1.append(num2[i])
        #     if vs_1 > 3 * theta or vs_1 < -3 * theta:
        #         num2_1.pop()
        #         continue
        #     vs_sum_1 = vs_sum_1 + vs_1 ** 2
        #     vi_1.append(vs_1)
        # theta_v = (vs_sum_1 / (len(num2_1) - 1)) ** 0.5
        # # print(theta_v)
        # pointer_2 = len(num2_1)
        # pointer_3 = len(num1)
        # space3 = np.linspace(0, pointer_3 - 1, pointer_3)
        # space4 = np.linspace(0, pointer_2 - 1, pointer_2)
        # a1, b1, popt_1 = fit_line(num2_1, space4)
        # c1, d1, popt_2 = fit_line(num1, space3)
        # xi = np.linspace(0, len(num2_1) - 1, len(num2_1))
        # x = (d-b)/(a-c)
        # y =

        x = (c * b + d) / (1 - a * c)
        y = (a * d + b) / (1 - a * c)

        x = round(x, 1)
        y = round(y, 1)

        cali_res_i = str(x) + ', ' + str(y)
        print(cali_res_i)
        cali_res.append(cali_res_i)
        # y = a * x + b
        f0 = np.zeros((2, 1))
        f0[0][0] = 957.5
        f0[1][0] = 539.5

        f1 = np.zeros((2, 1))
        f1[0][0] = x
        f1[1][0] = y

        ki = np.zeros((2, 2))
        ki[0][0] = k_x
        ki[0][1] = k_x * p - k_y * theta_cal
        ki[1][0] = k_x * theta_cal
        ki[1][1] = k_x * theta_cal * p - k_y

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

        # print("original h: " + str(h_res_0) + ' s, ' + "original v: " + str(v_res_0) + ' s')
        # print("current h: " + str(h_res) + ' s, ' + "current v: " + str(v_res) + ' s')
        delta_v = v_res - v_res_0
        delta_h = h_res - h_res_0

        delta_v = round(delta_v, 1)
        delta_h = round(delta_h, 1)

        print("delta_h: ", delta_h)
        print("delta_v: ", delta_v)
        n_s_i = n_s_i + delta_v
        v_save.append(delta_v)
        # if flag % 10 == 0:
        #     # n_s_i = n_s_i + delta_v
        #     res_delta_v = n_s_i / 10
        #     print("----------------")
        #     print("res_v: ", res_delta_v)
        #     n_s_i = 0
        #     with open("data/analyze.txt", 'a') as f:
        #         for i in v_save:
        #             f.write(str(i) + ',')
        #         f.write('\n')
        #         v_save.clear()
        #
        # flag = flag + 1
        # x = (d-b)/(a-c)
        # y =
        # plt.plot(xi, vi_1)
        # plt.show()
        num1.clear()
        num2.clear()
        num3.clear()
        num4.clear()
        # src[int(x), int(y)] = 255
        # src[int(x) + 1, int(y)] = 255
        # src[int(x), int(y) + 1] = 255
        # src[int(x) - 1, int(y)] = 255
        # src[int(x), int(y) - 1] = 255

        # cv2.namedWindow("res", cv2.WINDOW_FREERATIO)
        # cv2.imshow("res", src)
        # x = (c * b + d) / (1 - a * c)
        # y = a * x + b
        #
        # print(x, y)
        # num1.clear()
        # num2.clear()

        record = [x, y, delta_v]
        if counter % 120 == 0 and counter != 0:
            min_record = min_record + 2
        str_name = "data/record_data" + str(min_record) + ".txt"
        with open(str_name, 'a') as f:
            for i in record:
                f.write(str(i) + ',')
            f.write('\n')
            record.clear()
        print(counter)
        counter = counter + 1

    else:
        pass

np_cali_res = np.array(cali_res)
np.save('cali_theta_data_1.npy', np_cali_res)

cam.release()
cv.destroyAllWindows()
