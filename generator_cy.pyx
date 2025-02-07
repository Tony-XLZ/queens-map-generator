# cython: language_level=3

import random
from collections import deque

# ========================================================
# n-Queens Random Solver
# ========================================================

# A helper function that uses randomized backtracking to solve the n-Queens problem.
cdef bint _backtrack(int row, int n, list solution, object cols, object diag1, object diag2, list sol):
    # If all rows are processed, record the found solution.
    if row == n:
        sol[0] = solution.copy()
        return True
    # Generate a random order of columns for the current row.
    cdef list cols_list = list(range(n))
    random.shuffle(cols_list)
    cdef int col
    for col in cols_list:
        # Check if placing a queen at (row, col) conflicts with existing queens.
        if col in cols or (row - col) in diag1 or (row + col) in diag2:
            continue
        # Place the queen and update the conflict sets.
        solution[row] = col
        cols.add(col)
        diag1.add(row - col)
        diag2.add(row + col)
        # Recursively try to place the queen in the next row.
        if _backtrack(row + 1, n, solution, cols, diag1, diag2, sol):
            return True
        # Backtrack: remove the queen and restore the conflict sets.
        cols.remove(col)
        diag1.remove(row - col)
        diag2.remove(row + col)
    return False

cpdef list random_n_queens(int n):
    """
    Solve the n-Queens problem using randomized backtracking.

    Args:
        n (int): The size of the board.

    Returns:
        list: A list of length n where the i-th element is the column index of the queen in row i.
    """
    cdef list solution = [None] * n
    cdef object cols = set()
    cdef object diag1 = set()
    cdef object diag2 = set()
    cdef list sol = [None]
    _backtrack(0, n, solution, cols, diag1, diag2, sol)
    return sol[0]

# ========================================================
# Region Partition Generation (Color Grid)
# ========================================================

cpdef list generate_regions(int n, list queen_solution):
    """
    Generate an n×n region partition (color grid) based on an n-Queens solution.

    The process consists of three steps:
      1. Assign each queen's position as a seed for a unique region.
      2. Expand the regions using multi-source flood fill with a random expansion probability in [0.3, 0.5].
      3. Post-process any unassigned cells by using a neighboring region or a random region.

    Args:
        n (int): The size of the grid.
        queen_solution (list): The queen positions (one per row).

    Returns:
        list: A 2D list representing the region partition.
    """
    cdef int i, j, r_seed, c_seed, rid
    # Initialize the grid with None.
    cdef list regions = [[None for j in range(n)] for i in range(n)]
    cdef list region_ids = list(range(n))
    random.shuffle(region_ids)

    # Step 1: Use queen positions as initial region seeds.
    cdef dict region_seeds = {}
    for i in range(n):
        rid = region_ids[i]
        r_seed = i
        c_seed = queen_solution[i]
        regions[r_seed][c_seed] = rid
        region_seeds[rid] = [(r_seed, c_seed)]

    # Step 2: Set a random expansion probability for each region and perform flood fill.
    cdef dict expansion_prob = {}
    for rid in region_seeds:
        expansion_prob[rid] = 0.3 + 0.2 * random.random()  # Random probability in [0.3, 0.5]

    # Use a deque for multi-source flood fill.
    queue = deque()
    cdef list seeds
    cdef tuple pos
    for rid, seeds in region_seeds.items():
        for pos in seeds:
            queue.append((pos[0], pos[1], rid))

    cdef int di, dj, ni, nj, current_rid
    cdef tuple current
    while queue:
        current = queue.popleft()
        i = current[0]
        j = current[1]
        current_rid = current[2]
        # Check four adjacent cells.
        for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            ni = i + di
            nj = j + dj
            if ni >= 0 and ni < n and nj >= 0 and nj < n:
                if regions[ni][nj] is None:
                    if random.random() < expansion_prob[current_rid]:
                        regions[ni][nj] = current_rid
                        queue.append((ni, nj, current_rid))

    # Step 3: Post-process any unassigned cells.
    for i in range(n):
        for j in range(n):
            if regions[i][j] is None:
                neighbor_ids = set()
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni = i + di
                    nj = j + dj
                    if ni >= 0 and ni < n and nj >= 0 and nj < n:
                        if regions[ni][nj] is not None:
                            neighbor_ids.add(regions[ni][nj])
                if neighbor_ids:
                    regions[i][j] = random.choice(list(neighbor_ids))
                else:
                    regions[i][j] = random.choice(region_ids)
    return regions

# ========================================================
# Build Human-Readable Queen Board
# ========================================================

cpdef list build_queen_board(int n, list queen_solution):
    """
    Build a human-readable board representation using 'Q' for queens and '.' for empty spaces.

    Args:
        n (int): The size of the board.
        queen_solution (list): The list of queen positions.

    Returns:
        list: A 2D list representing the board.
    """
    cdef int i, j
    cdef list board = []
    cdef list row
    for i in range(n):
        row = ['.' for j in range(n)]
        row[queen_solution[i]] = 'Q'
        board.append(row)
    return board

# ========================================================
# Check Region Connectivity
# ========================================================

cpdef bint all_regions_connected(list grid):
    """
    Verify that every region (cells with the same region ID) in the grid is connected
    via adjacent (up/down/left/right) moves.

    Args:
        grid (list): The 2D grid with region IDs.

    Returns:
        bool: True if all regions are connected; False otherwise.
    """
    cdef int n = len(grid)
    cdef set region_ids = set()
    cdef int i, j
    # Collect all unique region IDs.
    for i in range(n):
        for j in range(n):
            region_ids.add(grid[i][j])
    cdef int total
    cdef tuple start
    cdef list queue
    cdef set visited
    cdef tuple cell
    cdef int ni, nj
    # Check connectivity for each region.
    for rid in region_ids:
        start = None
        # Find a starting cell for this region.
        for i in range(n):
            for j in range(n):
                if grid[i][j] == rid:
                    start = (i, j)
                    break
            if start is not None:
                break
        if start is None:
            continue
        # Perform BFS to traverse the region.
        queue = [start]
        visited = set([start])
        while queue:
            cell = queue.pop(0)
            i = cell[0]
            j = cell[1]
            for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                ni = i + di
                nj = j + dj
                if ni >= 0 and ni < n and nj >= 0 and nj < n:
                    if (ni, nj) not in visited and grid[ni][nj] == rid:
                        visited.add((ni, nj))
                        queue.append((ni, nj))
        # Count the total cells in the region.
        total = 0
        for i in range(n):
            for j in range(n):
                if grid[i][j] == rid:
                    total += 1
        # If the number of visited cells does not equal the total, the region is disconnected.
        if len(visited) != total:
            return False
    return True

# ========================================================
# Map Generation with Validation
# ========================================================

cpdef dict generate_map(int case_number, name=None):
    """
    Generate a map that includes:
      - An n-Queens solution.
      - A corresponding region partition (color grid) based on that solution.
      - A human-readable queen board.

    The function validates the generated map by ensuring that:
      - All regions are connected.
      - There is at most one singleton (single-cell) region.

    If a generated map fails validation, the process repeats.

    Args:
        case_number (int): The size of the board.
        name (str, optional): A custom name for the map.

    Returns:
        dict: A dictionary with keys "name", "caseNumber", "colorGrid", and "queenBoard".
    """
    cdef list queen_solution, color_grid
    cdef dict region_cells
    cdef list singletons
    cdef int i, j, rid
    while True:
        queen_solution = random_n_queens(case_number)
        color_grid = generate_regions(case_number, queen_solution)
        if not all_regions_connected(color_grid):
            continue
        # Group cells by region ID.
        region_cells = {}
        for i in range(case_number):
            for j in range(case_number):
                rid = color_grid[i][j]
                if rid in region_cells:
                    region_cells[rid].append((i, j))
                else:
                    region_cells[rid] = [(i, j)]
        # Identify singleton regions.
        singletons = [rid for rid, cells in region_cells.items() if len(cells) == 1]
        if len(singletons) > 1:
            continue
        break
    if name is None:
        name = "random-" + str(random.randint(0, 999999)).zfill(6)
    return {
        "name": name,
        "caseNumber": case_number,
        "colorGrid": color_grid,
        "queenBoard": build_queen_board(case_number, queen_solution)
    }

# ========================================================
# Compare Two Region Grids
# ========================================================

cpdef bint are_grids_same(list g1, list g2):
    """
    Compare two grids to determine if they have the same region distribution.
    The comparison groups cell coordinates by region ID and checks if the groups are identical.

    Args:
        g1 (list): The first grid.
        g2 (list): The second grid.

    Returns:
        bool: True if both grids have identical region distributions; False otherwise.
    """
    cdef int n = len(g1)
    if n != len(g2):
        return False
    cdef dict d1 = {}
    cdef dict d2 = {}
    cdef int i, j
    # Group cell coordinates by region ID for both grids.
    for i in range(n):
        for j in range(n):
            d1.setdefault(g1[i][j], []).append((i, j))
            d2.setdefault(g2[i][j], []).append((i, j))
    # Sort the coordinate lists for consistent comparison.
    for key in d1:
        d1[key].sort()
    for key in d2:
        d2[key].sort()
    return d1 == d2
