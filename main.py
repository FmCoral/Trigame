"""方案2：获取棋盘信息，发送【0xF1 0xF2 0x02 0xF3】触发，数据格式为[位置编号，有无棋子，旋转角度]，
编号为01-09,00无棋子，01黑棋，02白棋；角度数据线下谈。返回的数据为【0xA1 0xA2 · · · · · · · ·  0xA3】"""

from maix import camera, display, app, image
import traceback
import cv2 as cv
import numpy as np

# 初始化
disp = display.Display()
cam = camera.Camera(360, 360, fps = 30)

def main():
    done = 1
    # 定义卷积核
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
    while not app.need_exit():
        img = cam.read()
        # 转换成OpenCV格式灰度图
        img_cv = image.image2cv(img, False, False) # 这一步已经转化为BGR格式
        img_gray = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)

        # 去除噪点-高斯模糊(暂定5,5)
        img_blur = cv.GaussianBlur(img_gray, [5,5], 0)
        # 边缘检测-阈值暂定5,150
        img_edge = cv.Canny(img_blur, 50, 150)

        # 检查边缘是否被识别出
        # img_edge_maixcam = image.cv2image(img_edge)
        # disp.show(img_edge_maixcam)

        # 膨胀
        img_dilate = cv.dilate(img_edge, kernel)
        # 腐蚀
        img_erode = cv.erode(img_dilate, kernel)

        # 查找轮廓
        contours, _ = cv.findContours(img_erode, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        # 检查
        # print(len(contours))
        if len(contours) > 0:
            # 找出最大轮廓
            biggest_contours = max(contours, key = cv.contourArea)
            # 棋盘镶嵌在一个圆里面，可能会用到第二大轮廓，预留
            # second_biggest = sorted(contours, key=cv.contourArea, reverse=True)[1]
            # 近似多边形
            epsilon = 0.02 * cv.arcLength(biggest_contours, True)
            approx = cv.approxPolyDP(biggest_contours, epsilon, True) # 角点个数

            if len(approx) == 4:
                # 转换数组
                corners = approx.reshape((4, 2))

                # 进行大矩形角点编号（左上0、右上1、右下2、左下3）
                corn = np.zeros((4,2), dtype = "int")
                corn_sum = corners.sum(axis=1)
                corn_sub = np.diff(corners, axis=1)
                # 左上，x+y最小
                corn[0] = corners[np.argmin(corn_sum)]
                # 右上，y-x最小
                corn[1] = corners[np.argmin(corn_sub)]
                # 右下, x+y最大
                corn[2] = corners[np.argmax(corn_sum)]
                # 左下，y-x最大
                corn[3] = corners[np.argmax(corn_sub)]
                corners = corn


                # 绘制棋盘外框
                cv.drawContours(img_cv, [approx], -1, (0, 255, 0), 2)
                # 检查棋盘是否被正常框出
                img = image.cv2image(img_cv, False, False)

            else:
                print(f"最大轮廓不是矩形，角点个数为{len(approx)}")

        elif len(contours) == 0:
            print(f"未检测到有效轮廓{done}")

        done += 1
        disp.show(img)

if __name__ == '__main__':
    try:
        main()

    except Exception as e:
        # 显示报错信息
        print(f"程序异常报错：{e}")
        traceback.print_exc()  # 显示报错

    finally:
        # 退出时释放资源
        cam.close()
        disp.close()
        print("程序退出")

