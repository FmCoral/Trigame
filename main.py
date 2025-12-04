"""任务一：获取棋盘信息，发送【0xF1 0xF2 0x01 0xF3】触发，数据格式：（编号，坐标，状态），
编号为01～09，坐标为0x0000，0x0000，大端序，双字节，状态为01无棋子，02黑棋，03白棋，
返回的数据为【0xA1 0xA2 · · · · · · · ·  0xA3】中间的点就是九个棋盘的数据，首尾相连。共有57字节
思路：相机全局作用，不断获取照片，进入识别逻辑，获取棋盘信息，并存入缓存，
一直循环刷新最新数据，等待串口获取数据指令，收到则通过串口发送最新一次数据"""

from maix import camera, display, time, touchscreen, image
import traceback
# todo 获取更稳定的图片，缓存串口指令
from collections import deque

# 初始化
cam = camera.Camera(640, 480, fps=60)
disp = display.Display()
# imgs = deque(maxlen=1)
ts = touchscreen.TouchScreen()  # 初始化触摸屏

# 全局退出标志
should_exit = False


def exit_program(img):
    """
    Exit触摸屏幕退出程序模块
    :param img: 用于承载标识
    :return: 是否退出
    """
    # 按钮配置
    exit_text, text_scale, padding = "Exit", 3, 8
    # 创建Exit按钮
    text_w, text_h = image.string_size(exit_text, scale=text_scale)
    btn_x = img.width() - text_w - padding * 2
    btn_y = img.height() - text_h - padding * 2
    btn_w, btn_h = text_w + padding * 2, text_h + padding * 2
    img.draw_rect(btn_x, btn_y, btn_w, btn_h, color=image.Color.from_rgb(51, 51, 51), thickness=1)
    img.draw_string(btn_x + padding, btn_y + padding, exit_text, color=image.COLOR_GREEN, scale=text_scale)

    # 触摸检测+点击判断
    global should_exit
    touch_x, touch_y, pressed = ts.read()  # 读取触摸数据
    if pressed and not should_exit:
        # 触摸坐标转换
        img_x, img_y = image.resize_map_pos_reverse(
            img.width(), img.height(), disp.width(), disp.height(),
            image.Fit.FIT_CONTAIN, touch_x, touch_y
        )
        # 判断是否点击按钮区域
        if btn_x < img_x < btn_x + btn_w and btn_y < img_y < btn_y + btn_h:
            should_exit = True  # 标记退出

    return should_exit  # 返回状态


def main():
    while True:
        img = cam.read()

        if img is None:  # 帧判空
            time.sleep(0.01)
            continue

        # todo 添加棋盘识别逻辑

        # 调用exit_program，判断是否需要退出
        if exit_program(img):
            break  # 退出程序

        disp.show(img)  # 显示画面
        del img  # 清理图片


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
        print("程序正常退出，资源已释放")
