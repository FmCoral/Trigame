from maix import uart, pinmap


class UartHandler:
    def __init__(self,
                 Pin_1="A18",  # UART1_RX引脚
                 Pin_2="A19",  # UART1_TX引脚
                 Rx="UART1_RX",
                 Tx="UART1_TX",
                 bitrate=9600,
                 device="/dev/ttyS1"):
        # 1. 硬件引脚初始化（UART1）
        pinmap.set_pin_function(Pin_1, Rx)
        pinmap.set_pin_function(Pin_2, Tx)
        self.serial = uart.UART(device, bitrate)

        # 2. 负数映射配置
        self.offset = 50  # 偏移量（十进制）

        # 3. 帧头/帧尾
        self.frame_header = [0xFF]
        self.frame_footer = [0xFE]

        print(f"串口初始化完成：{device} | 波特率={bitrate}")

    def send_data(self, data_list):
        """
        直接发送十六进制字节逻辑：
        - 输入：原始棋盘数据（十进制，含-50~50的角度）
        - 处理：负数映射→拼接帧头/帧尾→转字节（对应十六进制）发送
        - 输出：串口发送二进制字节（十六进制可视化）
        """
        try:
            # 负数映射
            mapped_data = []
            for num in data_list:
                # 限制角度范围在-50~50
                clamped_num = max(-50, min(50, num))
                # 负数转正：-50→0，0→50，50→100
                mapped_num = clamped_num + self.offset
                mapped_data.append(mapped_num)

            # 拼接完整帧
            full_frame = self.frame_header + mapped_data + self.frame_footer

            # 十进制列表转字节
            send_bytes = bytes(full_frame)
            send_len = self.serial.write(send_bytes)

            # 调试打印
            print(f"完整帧（十进制）：{full_frame}")
            print(f"完整帧（十六进制）：{' '.join([f'0x{b:02X}' for b in send_bytes])}")
            print(f"发送字节数：{send_len}")
            return send_len

        except Exception as e:
            print(f"发送失败：{e}")
            return None

    def close(self):
        """关闭串口（程序结束时调用）"""
        self.serial.close()
        print("串口已关闭")


# 验证十六进制发送
if __name__ == "__main__":
    uart_obj = UartHandler()
    # 模拟棋盘数据
    test_data = [1, 0, -10, 2, 1, 5, 3, 2, 50] + [0] * 18  # 补全27个值
    uart_obj.send_data(test_data)
    uart_obj.close()