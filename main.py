"""抛弃方案1，开始方案2"""

"""方案2：获取棋盘信息，发送【0xF1 0xF2 0x02 0xF3】触发，数据格式为[位置编号，有无棋子，旋转角度]，
编号为01-09,00无棋子，01黑棋，02白棋；角度数据线下谈。返回的数据为【0xA1 0xA2 · · · · · · · ·  0xA3】"""
from maix import camera, display, app, image
import traceback
import cv2 as cv

# 初始化
disp = display.Display()
cam = camera.Camera(360, 360, fps = 30)

def main():
    kernel = cv.getStructuringElement(cv.MORPH_RECT,(5,5))
    while not app.need_exit():
        img = cam.read()
        # 转换成OpenCV格式-BGR格式
        img_cv = image.image2cv(img)
        img_gray = cv.cvtColor(img_cv, cv.COLOR_BGR2GRAY)

        # 去除噪点-高斯模糊(暂定5,5)
        img_blur = cv.GaussianBlur(img_gray, [5,5], 0)
        # 边缘检测-阈值暂定5,150
        img_edge = cv.Canny(img_blur, 50, 150)

        # 检查边缘是否被识别出
        img_edge_maixcam = image.cv2image(img_edge)
        # disp.show(img_edge_maixcam)

        # 膨胀
        img_dilate = cv.dilate(img_edge, kernel)

        # 腐蚀
        img_erode = cv.erode(img_dilate, kernel)



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

