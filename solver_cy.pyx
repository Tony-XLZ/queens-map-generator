# cython: boundscheck=False, wraparound=False, nonecheck=False

import numpy as np
cimport numpy as np
from libc.stdint cimport uint32_t

# 通过 cimport 引入 NumPy 的 C API 初始化函数
cdef extern from "numpy/arrayobject.h":
    void import_array()

# 调用 import_array() 初始化 NumPy C API
# 注意：此调用必须在模块加载时执行一次
import_array()

# 这里直接将 DTYPE_t 定义为 C 的 int 类型（通常与 np.intc 对应）
ctypedef int DTYPE_t

# 定义一个内联的绝对值函数，确保它在 nogil 下也能调用
cdef inline int ABS(int x) nogil:
    return x if x >= 0 else -x

#
# _backtrack 函数：递归计数满足约束的皇后摆法
#
# 参数说明：
#   row        : 当前处理的行号
#   n          : 棋盘尺寸
#   used_cols  : 用各个位记录哪些列已使用（每一行放一个皇后）
#   last_col   : 上一行皇后所在列（用于判断相邻行皇后不能在相邻列）
#   grid_arr   : 区域网格的内存视图（二维，尺寸 n×n），每个元素类型为 DTYPE_t
#   threshold  : 剪枝阈值，累计解数超过此值时提前返回
#   used_blocks: 长度足够的 C 数组，记录每个区域（块）是否已使用
#
cdef int _backtrack(int row, int n, uint32_t used_cols, int last_col,
                    DTYPE_t[:, :] grid_arr, int threshold,
                    bint* used_blocks) nogil:
    cdef int count = 0
    cdef int col, block_id, cnt

    if row == n:
        return 1  # 找到一个完整解

    for col in range(n):
        # 检查当前列是否已使用（利用位运算）
        if used_cols & (1 << col):
            continue
        # 如果不是第一行，则判断当前列与上一行皇后是否相邻
        if row > 0 and ABS(last_col - col) <= 1:
            continue
        # 取当前单元格所属的区域编号
        block_id = grid_arr[row, col]
        # 如果该区域已使用，则跳过
        if used_blocks[block_id]:
            continue

        # 标记该区域已使用
        used_blocks[block_id] = True

        # 递归进入下一行，更新 used_cols 与剩余阈值
        cnt = _backtrack(row + 1, n, used_cols | (1 << col), col,
                         grid_arr, threshold - count, used_blocks)
        count += cnt

        # 回溯时撤销该区域标记
        used_blocks[block_id] = False

        # 如果累计解数超过阈值，则提前返回
        if count > threshold:
            return count

    return count

def count_valid_solutions(object color_grid, int threshold):
    """
    使用 Cython 实现的计数函数，计算给定区域网格下满足下列约束的皇后摆法数：
      1. 每行每列恰好一个皇后；
      2. 相邻行的皇后所在列相差大于 1；
      3. 同一区域内最多放置一个皇后。
    当累计解数超过 threshold 时提前返回（剪枝）。

    参数：
       color_grid: 二维列表（每个元素为 int），表示区域编号
       threshold : 剪枝阈值

    返回：
       满足条件的解数（可能超过 threshold）
    """
    cdef int n = len(color_grid)
    # 将 color_grid 转为 numpy 数组，再转换为内存视图（要求数据连续）
    cdef np.ndarray[DTYPE_t, ndim=2] arr = np.array(color_grid, dtype=np.intc)
    cdef DTYPE_t[:, :] grid_arr = arr

    cdef int i
    # 假设区域编号均在 0 ~ n-1 内，这里分配长度为 128 的 used_blocks 数组（n 较大时可调整）
    cdef bint used_blocks[128]
    for i in range(128):
        used_blocks[i] = False

    cdef int result
    # 在递归中释放 GIL，以获得更高的执行效率
    with nogil:
        result = _backtrack(0, n, 0, -100, grid_arr, threshold, used_blocks)
    return result

def solve(object color_grid, object name, int threshold=1):
    """
    Cython 版本的求解函数，用于评估地图难度。调用 count_valid_solutions，
    如果方案数不超过阈值，则认为地图难度较高。

    返回字典格式与原版一致。
    """
    cdef int count = count_valid_solutions(color_grid, threshold)
    return {"name": name,
            "solvable": count > 0,
            "number_solution": count,
            "number_possibility": None}
