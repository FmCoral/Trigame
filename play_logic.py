"""现在有一个有效数据列表，长度从0到10，根据最新数据和上一次的数据判断棋盘状态发生了什么变化"""
import time

# 先判断qipan_data里面的数据，情况1：没有数据，情况2：有一个数据，必然是空状态，情况三，大于等于两个数据。
# 其中情况三又分为以下情况：1、最新数据和上一次数据属于遵守规则的变化，2、违反规则，需要恢复到上一个数据的格式

# 棋盘输赢平局继续四种情况判断
def check_win(current_data):
    """
    判断棋盘输赢
    :param current_data: 18位棋盘数据
    :return: 1=黑赢，2=白赢，0=未赢；同时打印匹配的赢线
    """
    # 赢线位置组合
    win_lines = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]

    for line in win_lines:
        # 计算格子索引并获取颜色值
        idx1 = 2 * line[0] - 1
        idx2 = 2 * line[1] - 1
        idx3 = 2 * line[2] - 1
        color1 = current_data[idx1]
        color2 = current_data[idx2]
        color3 = current_data[idx3]

        # 黑棋赢判断
        if color1 == color2 == color3 == 1:
            print(f"黑棋赢, 赢线：{line}")
            return 1
        # 白棋赢判断
        if color1 == color2 == color3 == 2:
            print(f"白棋赢, 赢线：{line}")
            return 2

        # 平局判断
        color_indices = [2 * n - 1 for n in range(1, 10)]
        is_board_full = True  # 标记是否下满
        for idx in color_indices:
            if current_data[idx] == 0:  # 存在空位置
                is_board_full = False
                break  # 只要有一个空位置，就不是满的，直接退出循环

        if is_board_full:
            print("棋盘已下满，平局")
            return 3  # 平局

    print("继续")
    return 0


def judge_rules(prev_data, curr_data):
    """
    校验下棋的3个核心合规条件：格式+落子数量+落子位置
    :param prev_data: 上一次棋盘数据
    :param curr_data: 当前棋盘数据
    :return: (bool, str) → (是否合规, 原因说明)
    """

    # 提取两次棋盘的颜色位（保留9个位置的颜色值，简化对比）
    prev_color = [prev_data[2 * n - 1] for n in range(1, 10)]  # 上一次各位置颜色（9位）
    curr_color = [curr_data[2 * n - 1] for n in range(1, 10)]  # 当前各位置颜色（9位）

    # 找出两次颜色变化的位置（0-8，对应棋盘1-9号位）
    changed_positions = []
    for idx in range(9):
        if prev_color[idx] != curr_color[idx]:
            changed_positions.append(idx)

    # ========== 落子数量合规（仅能有1处变化） ==========
    if len(changed_positions) == 0:
        print("犯规：未落子（无任何位置颜色变化）")
        return False
    if len(changed_positions) > 1:
        print(f"犯规：多落子（共{len(changed_positions)}处位置变化，仅允许1处）")
        return False

    # ========== 落子位置合规（只能落在空位置，且落子颜色有效） ==========
    change_idx = changed_positions[0]  # 唯一变化的位置（0-8）
    prev_val = prev_color[change_idx]  # 上一次该位置颜色
    curr_val = curr_color[change_idx]  # 当前该位置颜色

    if prev_val != 0:
        print(f"犯规：覆盖已有棋子（棋盘{change_idx + 1}号位上一次为{prev_val}，非空）")
        return False
    if curr_val not in [1, 2]:
        print(f"犯规：落子颜色无效（棋盘{change_idx + 1}号位当前为{curr_val}，仅允许1/2）")
        return False

    # 所有核心条件满足 → 合规
    return True


def attack_logic(attack_data):
    """
    三子棋AI落子逻辑（优先级：直接赢→堵对方→占中心→占角→占边）
    :param attack_data: 交替列表 [格子1,状态1, 格子2,状态2,...,格子9,状态9]，状态0=空/1=黑/2=白
    :return: 最优落子格子序号（1-9），无落子位置返回None（棋盘满）
    """
    # ==================== 1. 数据校验与格式化 ====================
    # 初始化棋盘映射：格子序号(1-9) → 状态(0/1/2)，默认空
    board_map = {num: 0 for num in range(1, 10)}
    # 遍历交替列表
    for i in range(0, 1, 2):
        grid_num = attack_data[i]
        grid_state = attack_data[i + 1]
        if 1 <= grid_num <= 9 and grid_state in [0, 1, 2]:
            board_map[grid_num] = grid_state

    # 转3×3棋盘（行0-2，列0-2），方便赢线判断
    board = [
        [board_map[1], board_map[2], board_map[3]],  # 第0行：格子1-3
        [board_map[4], board_map[5], board_map[6]],  # 第1行：格子4-6
        [board_map[7], board_map[8], board_map[9]]   # 第2行：格子7-9
    ]

    # 定义所有赢线（(行,列)坐标），共8条
    win_lines = [
        [(0, 0), (0, 1), (0, 2)], [(1, 0), (1, 1), (1, 2)], [(2, 0), (2, 1), (2, 2)],  # 横
        [(0, 0), (1, 0), (2, 0)], [(0, 1), (1, 1), (2, 1)], [(0, 2), (1, 2), (2, 2)],  # 竖
        [(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]  # 斜
    ]

    # ==================== 2. 定义己方/对方棋子 ====================
    my_piece = 2  # 己方：1=黑棋，改2=白棋
    enemy_piece = 1 # 敌方

    # ==================== 3.直接赢（差1子凑赢线） ====================
    for line in win_lines:
        # 提取当前赢线的3个状态值
        line_vals = [board[x][y] for x, y in line]
        # 己方有2子，空1子 → 落空位置直接赢
        if line_vals.count(my_piece) == 2 and line_vals.count(0) == 1:
            empty_x, empty_y = line[line_vals.index(0)]
            # 坐标转格子序号：行x列y → x*3 + y +1
            return empty_x * 3 + empty_y + 1

    # ==================== 4.堵对方赢（对方差1子） ====================
    for line in win_lines:
        line_vals = [board[x][y] for x, y in line]
        # 若对方有2子，空1子 → 堵空位置
        if line_vals.count(enemy_piece) == 2 and line_vals.count(0) == 1:
            empty_x, empty_y = line[line_vals.index(0)]
            return empty_x * 3 + empty_y + 1

    # ==================== 5.占中心 ====================
    if board[1][1] == 0:
        return 5

    # ==================== 6.占角（格子1/3/7/9） ====================
    corners = [(0, 0, 1), (0, 2, 3), (2, 0, 7), (2, 2, 9)]  # (行,列,格子序号)
    for x, y, grid_num in corners:
        if board[x][y] == 0:
            return grid_num

    # ==================== 7.占边（格子2/4/6/8） ====================
    edges = [(0, 1, 2), (1, 0, 4), (1, 2, 6), (2, 1, 8)]  # (行,列,格子序号)
    for x, y, grid_num in edges:
        if board[x][y] == 0:
            return grid_num

    # ==================== 8. 棋盘已满 ====================
    return None


def main(qipan_data):
    result = None
    if len(qipan_data) ==0:
        result =  0 # 0 代表继续下棋

    elif len(qipan_data) == 1:
        result = check_win(qipan_data[0])

    elif len(qipan_data) > 1:
        # 判断是否遵守规则
        rules = judge_rules(qipan_data[-2],qipan_data[-1])
        if rules: # 如果遵守了规则
            # 先判断有没有赢
            result = check_win(qipan_data[-1])
            # 如果没有赢并且没有平局
            if result == 0:
                best_place = attack_logic(qipan_data[-1])
                print(f"下在{best_place}")
                time.sleep(0.1)
        else:
            print("没有遵守规则")

    return result

