# cython: boundscheck=False, wraparound=False, nonecheck=False

import numpy as np
cimport numpy as np
from libc.stdint cimport uint32_t

# Import NumPy C API initialization function via cimport.
cdef extern from "numpy/arrayobject.h":
    void import_array()

# Initialize the NumPy C API (must be called once during module load).
import_array()

# Define the element type for the grid.
ctypedef int DTYPE_t

# Inline absolute value function that can be used in nogil contexts.
cdef inline int ABS(int x) nogil:
    return x if x >= 0 else -x

###############################################################################
# Recursive Backtracking Function
###############################################################################
#
# _backtrack:
#   Recursively counts the number of valid queen placements on an n×n board
#   under the following constraints:
#       1. Exactly one queen per row and column.
#       2. Queens in consecutive rows must not be placed in adjacent columns.
#       3. At most one queen per designated region (block) of the grid.
#
# Parameters:
#   row         - The current row to process.
#   n           - The board size.
#   used_cols   - Bitmask representing which columns are occupied.
#   last_col    - Column index of the queen in the previous row (used for adjacency check).
#   grid_arr    - Memory view of the 2D grid (n×n) holding region identifiers.
#   threshold   - Pruning threshold; recursion returns early if count exceeds this value.
#   used_blocks - C array (of boolean values) indicating whether a region (block) is already used.
#
# Returns:
#   The count of valid queen placements found in the current recursive branch.
#
cdef int _backtrack(int row, int n, uint32_t used_cols, int last_col,
                    DTYPE_t[:, :] grid_arr, int threshold,
                    bint* used_blocks) nogil:
    cdef int count = 0
    cdef int col, block_id, cnt

    # Base case: if all rows have been processed, a valid solution is found.
    if row == n:
        return 1

    # Iterate over all columns in the current row.
    for col in range(n):
        # Skip if the column is already occupied.
        if used_cols & (1 << col):
            continue
        # For non-first rows, ensure that the queen is not placed in an adjacent column.
        if row > 0 and ABS(last_col - col) <= 1:
            continue
        # Retrieve the region (block) identifier for the current cell.
        block_id = grid_arr[row, col]
        # Skip if the region has already been used.
        if used_blocks[block_id]:
            continue

        # Mark the region as used.
        used_blocks[block_id] = True

        # Recurse to the next row, updating the column bitmask and passing the current column.
        cnt = _backtrack(row + 1, n, used_cols | (1 << col), col,
                         grid_arr, threshold - count, used_blocks)
        count += cnt

        # Backtrack: unmark the region.
        used_blocks[block_id] = False

        # If the cumulative count exceeds the threshold, prune further exploration.
        if count > threshold:
            return count

    return count

###############################################################################
# Public API Function: count_valid_solutions
###############################################################################
#
# count_valid_solutions:
#   Counts the number of valid queen placements on the board defined by the given
#   region grid. Applies early pruning if the solution count exceeds the provided
#   threshold.
#
# Parameters:
#   color_grid - A 2D list where each element (of type int) represents a region ID.
#   threshold  - The maximum count to search for; recursion stops early if exceeded.
#
# Returns:
#   The total count of valid queen placements (may exceed threshold).
#
def count_valid_solutions(object color_grid, int threshold):
    # Determine board size (number of rows).
    cdef int n = len(color_grid)
    # Convert the Python grid to a contiguous NumPy array with C integer type.
    cdef np.ndarray[DTYPE_t, ndim=2] arr = np.array(color_grid, dtype=np.intc)
    cdef DTYPE_t[:, :] grid_arr = arr

    cdef int i
    # Allocate a fixed-size array for region usage tracking.
    # Adjust size if n (or region ID range) is larger than 128.
    cdef bint used_blocks[128]
    for i in range(128):
        used_blocks[i] = False

    cdef int result
    # Execute recursion without the Global Interpreter Lock (GIL) for performance.
    with nogil:
        result = _backtrack(0, n, 0, -100, grid_arr, threshold, used_blocks)
    return result

###############################################################################
# Public API Function: solve
###############################################################################
#
# solve:
#   Evaluates the board (or map) difficulty by determining whether any valid
#   queen placement exists under the constraints. It returns a dictionary with
#   a similar format to the original solver.
#
# Parameters:
#   color_grid - A 2D list of integers representing region IDs.
#   name       - Identifier for the current board/map.
#   threshold  - (Optional) Pruning threshold (default is 1).
#
# Returns:
#   A dictionary containing:
#       - "name": The board/map name.
#       - "solvable": A boolean indicating if at least one valid solution exists.
#       - "number_solution": The total count of valid solutions.
#       - "number_possibility": Always None (for compatibility with original format).
#
def solve(object color_grid, object name, int threshold=1):
    cdef int count = count_valid_solutions(color_grid, threshold)
    return {"name": name,
            "solvable": count > 0,
            "number_solution": count,
            "number_possibility": None}
