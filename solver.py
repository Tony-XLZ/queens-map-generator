# solver.py

def count_valid_solutions(color_grid, threshold):
    """
    直接使用回溯（backtracking）和位运算统计给定色块分割（color_grid）下
    符合条件的皇后排列数量（满足：
         1. 每行和每列只有一个皇后；
         2. 相邻行的皇后不在相邻列（即绝对差大于 1）；
         3. 每个色块内最多只有一个皇后）。
    如果计数超过 threshold，则提前返回（即剪枝）。

    Args:
        color_grid (list of list): 用于指示区域（色块）的网格，元素可转换为字符串。
        threshold (int): 当解的数量超过该值时提前剪枝返回。

    Returns:
        int: 符合条件的排列数量（可能超过 threshold）。
    """
    n = len(color_grid)
    # 先将所有色块 id 转为字符串，方便比较
    grid = [[str(cell) for cell in row] for row in color_grid]

    def backtrack(row, used_cols, last_col, used_blocks):
        if row == n:
            return 1  # 找到一个完整解
        count = 0
        # 枚举当前行中所有可能的列（0 到 n-1）
        for col in range(n):
            # 判断列是否已使用（用位掩码判断）
            if used_cols & (1 << col):
                continue
            # 对于相邻行的约束：如果不是第一行，则当前列不能与上一行皇后相邻
            if row > 0 and abs(last_col - col) <= 1:
                continue
            block_id = grid[row][col]
            # 同一区块内只能出现一个皇后
            if block_id in used_blocks:
                continue
            # 标记当前选择，并进入下一行
            new_used_cols = used_cols | (1 << col)
            new_used_blocks = used_blocks | {block_id}
            cnt = backtrack(row + 1, new_used_cols, col, new_used_blocks)
            count += cnt
            if count > threshold:
                # 提前剪枝：一旦解数超过阈值，直接返回
                return count
        return count

    return backtrack(0, 0, None, set())


def solve(color_grid, name, threshold=1):
    """
    评估给定地图（以 color_grid 表示）的解数，并判断是否满足难度要求。
    与原来不同的是，这里不生成所有排列，而是直接统计符合条件的解，
    并在达到阈值时提前返回以节省时间。

    Args:
        color_grid (list of list): 色块分割网格
        name (str): 地图的名字
        threshold (int): 解的数量阈值，超过此值就认为“难度不够”

    Returns:
        dict: 包含解数、是否可解等信息的结果字典，格式与原来类似。
    """
    count = count_valid_solutions(color_grid, threshold)
    result = {
        "name": name,
        "solvable": count > 0,
        "number_solution": count,
        # 因为我们没有生成所有排列，故“number_possibility”字段不再计算（也可以置为 None）
        "number_possibility": None
    }
    return result
