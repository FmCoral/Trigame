"""抛弃方案1，开始方案2"""
"""方案2：获取棋盘信息，发送【0xF1 0xF2 0x02 0xF3】触发，数据格式为[位置编号，有无棋子，旋转角度]，
编号为01-09,00无棋子，01黑棋，02白棋；角度数据线下谈。返回的数据为【0xA1 0xA2 · · · · · · · ·  0xA3】"""
from maix import camera, display
import traceback

# 初始化
disp = display.Display()
cam = camera.Camera(360, 360, fps = 30)

def main():
    pass


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

