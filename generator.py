import random
from collections import deque


def random_n_queens(n):
    """
    Solve the n-Queens problem using randomized backtracking.

    This function finds one valid solution to the n-Queens problem,
    returning a list `solution` where solution[i] represents the column
    index of the queen placed in row i. The column order is randomized to
    produce different solutions for the same n on different runs.

    Args:
        n (int): The size of the chessboard and the number of queens.

    Returns:
        list or None: A list of length n representing the column indices of
        queens for each row, or None if no solution is found.
    """
    solution = [None] * n
    cols = set()  # Tracks columns that are already occupied by a queen.
    diag1 = set()  # Tracks occupied main diagonals (row - col).
    diag2 = set()  # Tracks occupied anti-diagonals (row + col).

    sol = None  # Will store the final solution if found.

    def backtrack(row):
        nonlocal sol
        # If all rows are processed, a valid solution is found.
        if row == n:
            sol = solution.copy()
            return True

        # Create a randomized list of column indices for the current row.
        cols_list = list(range(n))
        random.shuffle(cols_list)
        for col in cols_list:
            # Skip the column if it conflicts with any previously placed queen.
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # Place the queen at (row, col) and mark the column and diagonals as used.
            solution[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            # Proceed to place queen in the next row.
            if backtrack(row + 1):
                return True

            # Backtrack: Remove the queen and clear the markers.
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)

        return False

    backtrack(0)
    return sol


def generate_regions(n, queen_solution):
    """
    Generate a region (color) segmentation of an n x n board based on a given n-Queens solution.

    The board is partitioned into regions (colored segments) using the following steps:
      1. Special Region: Select a random row and designate its queen cell as a seed for a special region.
         Then, assign the entire row and column of that cell to the special region.
      2. Other Region Seeds: For each of the other rows, choose the queen cell as a seed and assign
         it a random region id.
      3. Multi-source Flood Fill: From all seed positions, propagate the region assignment to adjacent
         cells with a given probability.
      4. Post-processing: For any cell that remains unassigned, assign it a region based on its neighbors.

    Args:
        n (int): The dimension of the board.
        queen_solution (list of int): A valid n-Queens solution, where queen_solution[i] is the column
            index of the queen in row i.

    Returns:
        list of list of int: A 2D list representing the board, where each cell's value is the region id (color).
    """
    # Initialize the region grid with None.
    regions = [[None for _ in range(n)] for _ in range(n)]

    # Prepare a random permutation of region IDs.
    region_ids = list(range(n))
    random.shuffle(region_ids)

    # --- Step 1: Special Region (Strong Seed) ---
    special_row = random.randint(0, n - 1)
    special_col = queen_solution[special_row]
    special_region = region_ids[0]  # Use the first region id as the special region.

    # Assign the entire special row and special column to the special region.
    for j in range(n):
        regions[special_row][j] = special_region
    for i in range(n):
        regions[i][special_col] = special_region

    # Record the seed positions for the special region.
    region_seeds = {special_region: [(special_row, special_col)]}

    # --- Step 2: Other Region Seeds ---
    assigned_regions = {special_region}
    available_regions = [rid for rid in region_ids if rid not in assigned_regions]
    for i in range(n):
        if i == special_row:
            continue  # Skip the special row.
        if not available_regions:
            # Refill available regions if exhausted (may happen when n is small).
            available_regions = [rid for rid in region_ids if rid != special_region]
        rid = random.choice(available_regions)
        available_regions.remove(rid)
        # Use the queen's cell in this row as the seed.
        r_seed, c_seed = i, queen_solution[i]
        regions[r_seed][c_seed] = rid
        region_seeds.setdefault(rid, []).append((r_seed, c_seed))

    # --- Step 3: Multi-source Flood Fill Expansion ---
    # Set expansion probabilities: special region always expands (1.0), others have probabilities between 0.3 and 0.5.
    expansion_prob = {}
    for rid in region_seeds:
        if rid == special_region:
            expansion_prob[rid] = 1.0
        else:
            expansion_prob[rid] = 0.3 + 0.2 * random.random()

    # Initialize the flood fill queue with all seed positions.
    queue = deque()
    for rid, seeds in region_seeds.items():
        for pos in seeds:
            queue.append((pos[0], pos[1], rid))

    # Perform the flood fill.
    while queue:
        i, j, rid = queue.popleft()
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            # Check bounds and if the cell is not yet assigned.
            if 0 <= ni < n and 0 <= nj < n and regions[ni][nj] is None:
                # With a certain probability, assign the cell to the current region.
                if random.random() < expansion_prob[rid]:
                    regions[ni][nj] = rid
                    queue.append((ni, nj, rid))

    # --- Step 4: Post-processing for Unassigned Cells ---
    # For any cell still unassigned, choose a region based on neighboring cells, or randomly if isolated.
    for i in range(n):
        for j in range(n):
            if regions[i][j] is None:
                neighbor_ids = set()
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and regions[ni][nj] is not None:
                        neighbor_ids.add(regions[ni][nj])
                if neighbor_ids:
                    regions[i][j] = random.choice(list(neighbor_ids))
                else:
                    regions[i][j] = random.choice(region_ids)

    return regions


def build_queen_board(n, queen_solution):
    """
    Build a visual chessboard representation from a given n-Queens solution.

    Each row is represented as a list of characters where 'Q' denotes the queen
    and '.' denotes an empty cell.

    Args:
        n (int): The dimension of the board.
        queen_solution (list of int): The n-Queens solution list where queen_solution[i]
            is the column index of the queen in row i.

    Returns:
        list of list of str: A 2D list representing the chessboard.
    """
    board = []
    for i in range(n):
        # Initialize row with empty cells.
        row = ['.' for _ in range(n)]
        # Place the queen at the designated column.
        row[queen_solution[i]] = 'Q'
        board.append(row)
    return board


def generate_map(case_number: int, name=None) -> dict:
    """
    Generate a map containing a colored chessboard partition and a queen placement.

    The map includes:
      - A random n-Queens solution.
      - A region (color) grid generated from the queen solution.
      - A visual chessboard displaying queen positions.

    Args:
        case_number (int): The size of the board (n).
        name (str, optional): A name for the map. If not provided, a random name is generated.

    Returns:
        dict: A dictionary containing:
            - "name": Map name.
            - "caseNumber": The board size n.
            - "colorGrid": The n x n region segmentation grid.
            - "queenBoard": The chessboard with queen placements.
    """
    if name is None:
        num_rand = random.randint(0, 999999)
        name = "random-" + str(num_rand).zfill(6)

    new_map = {
        "name": name,
        "caseNumber": case_number,
        "colorGrid": []
    }

    # Step 1: Generate a random n-Queens solution.
    queen_solution = random_n_queens(case_number)

    # Step 2: Generate region segmentation (colored chessboard) based on the queen solution.
    color_grid = generate_regions(case_number, queen_solution)
    new_map["colorGrid"] = color_grid

    # Build and save the queen board representation.
    new_map["queenBoard"] = build_queen_board(case_number, queen_solution)

    return new_map


def are_grids_same(g1, g2):
    """
    Determine whether two 2D grids (region segmentations) have the same color distribution.

    This function compares the positions of each region identifier in both grids.

    Args:
        g1 (list of list): The first grid (2D list) of region ids.
        g2 (list of list): The second grid (2D list) of region ids.

    Returns:
        bool: True if the grids have identical region distributions, False otherwise.
    """
    if len(g1) != len(g2):
        return False

    d1 = {}
    d2 = {}
    n = len(g1)
    # Map each region id to the list of coordinates where it appears in g1 and g2.
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
