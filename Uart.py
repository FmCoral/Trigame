from maix import uart, pinmap, time
import threading


class UartHandler:
    def __init__(self, Pin_1="A18", Pin_2="A19", bitrate=9600, device="/dev/ttyS1"):
        # 串口初始化
        pinmap.set_pin_function(Pin_1, "UART1_RX")
        pinmap.set_pin_function(Pin_2, "UART1_TX")
        self.serial = uart.UART(device, bitrate)

        # 固定包头包尾
        self.header = [0xA1, 0xA2]
        self.footer = [0xA3]

        # 接收缓存
        self.recv_hex_data = []
        self.lock = threading.Lock()
        self.running = True

        # 启动接收线程
        threading.Thread(target=self._recv_loop, daemon=True).start()
        print("串口初始化完成 | 16进制收发")

    def _recv_loop(self):

        while self.running:
            read_byte = self.serial.read(1)
            if read_byte:
                hex_num = ord(read_byte)  # 字节→十进制数值
                with self.lock:
                    self.recv_hex_data.append(hex_num)
            time.sleep(0.001)

    def send_hex_data(self, hex_num):
        """16进制发送：自动加包头包尾，无其他判断/解析"""
        try:
            # 自动拼接
            full_hex_list = self.header + hex_num + self.footer
            # 列表转字节发送
            send_bytes = bytes(full_hex_list)
            send_len = self.serial.write(send_bytes)
            # 打印
            print(f"发送：{full_hex_list} | 字节数：{send_len}")
            return send_len
        except Exception as e:
            print(f"发送失败：{e}")
            return None

    def get_recv_hex(self, clear=True):
        """获取接收数据"""
        with self.lock:
            data = self.recv_hex_data.copy()
            if clear:
                self.recv_hex_data = []
        return data

    def close(self):
        self.running = False
        time.sleep(0.01)
        self.serial.close()
        print("串口关闭")


# 测试
if __name__ == "__main__":
    uart_obj = UartHandler()
    try:
        i = 1
        while True:
            test_list = [i]
            # 发送
            uart_obj.send_hex_data(test_list)

            # 接收
            recv_hex = uart_obj.get_recv_hex()
            if recv_hex:
                print(f"接收：{recv_hex}")

            i += 1
            time.sleep(1)
    except KeyboardInterrupt:
        uart_obj.close()