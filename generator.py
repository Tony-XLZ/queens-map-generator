import random
from collections import deque


def random_n_queens(n):
    """
    Solve the n-Queens problem using randomized backtracking.

    This function attempts to place n queens on an n×n chessboard such that
    no two queens threaten each other. It returns a solution as a list where
    the i-th element represents the column index of the queen in row i.

    Parameters:
        n (int): The size of the chessboard and the number of queens.

    Returns:
        List[int] or None: A valid queen placement solution if found, otherwise None.
    """
    solution = [None] * n  # solution[i] will store the column of the queen in row i
    cols = set()  # Set of columns that are already occupied by queens
    diag1 = set()  # Set of occupied main diagonals (row - col)
    diag2 = set()  # Set of occupied anti-diagonals (row + col)
    sol = None  # Variable to hold a complete solution once found

    def backtrack(row):
        """
        Recursively attempt to place a queen in each row using randomized column order.

        Parameters:
            row (int): The current row index to place a queen.

        Returns:
            bool: True if a complete solution is found, otherwise False.
        """
        nonlocal sol
        # If all rows are processed, a complete solution is found.
        if row == n:
            sol = solution.copy()
            return True

        # Generate a randomized order of columns to try for the current row.
        cols_list = list(range(n))
        random.shuffle(cols_list)

        for col in cols_list:
            # Check if the current column or diagonals are already threatened.
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue

            # Place the queen at (row, col)
            solution[row] = col
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)

            # Recurse to the next row; if successful, propagate success upward.
            if backtrack(row + 1):
                return True

            # Backtrack: remove the queen and free up the column and diagonals.
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
        return False

    backtrack(0)
    return sol


def generate_regions(n, queen_solution):
    """
    Generate an n×n grid with region (color block) segmentation based on a given n-Queens solution.

    The segmentation is created through a four-step process:
      1. Choose a random row to define a "special region" by marking all cells in that row and its queen's column.
      2. For each of the remaining rows, select the queen's position as a seed and assign a random region ID.
      3. Expand these seed regions via a multi-source flood fill algorithm with region-specific probabilities.
      4. Post-process the grid by assigning any unfilled cells a region ID based on their neighbors or random selection.

    Parameters:
        n (int): The size of the grid.
        queen_solution (List[int]): The queen placement solution from the n-Queens problem.

    Returns:
        List[List[int]]: A 2D list representing the region segmentation of the grid.
    """
    # Initialize the grid with None (unassigned regions)
    regions = [[None for _ in range(n)] for _ in range(n)]
    region_ids = list(range(n))
    random.shuffle(region_ids)

    # --- Step 1: Define Special Region ---
    # Select a random row; its queen's column becomes the special seed position.
    special_row = random.randint(0, n - 1)
    special_col = queen_solution[special_row]
    special_region = region_ids[0]

    # Mark the entire special row and the corresponding column as the special region.
    for j in range(n):
        regions[special_row][j] = special_region
    for i in range(n):
        regions[i][special_col] = special_region
    region_seeds = {special_region: [(special_row, special_col)]}

    # --- Step 2: Assign Other Region Seeds ---
    assigned_regions = {special_region}
    available_regions = [rid for rid in region_ids if rid not in assigned_regions]
    for i in range(n):
        if i == special_row:
            continue
        # If we run out of available regions, reset (excluding the special region).
        if not available_regions:
            available_regions = [rid for rid in region_ids if rid != special_region]
        rid = random.choice(available_regions)
        available_regions.remove(rid)
        r_seed, c_seed = i, queen_solution[i]
        regions[r_seed][c_seed] = rid
        region_seeds.setdefault(rid, []).append((r_seed, c_seed))

    # --- Step 3: Multi-Source Flood Fill Expansion ---
    # Each region is assigned an expansion probability.
    expansion_prob = {}
    for rid in region_seeds:
        if rid == special_region:
            expansion_prob[rid] = 1.0  # Special region expands with certainty.
        else:
            expansion_prob[rid] = 0.3 + 0.2 * random.random()  # Random probability between 0.3 and 0.5.

    # Initialize a queue with all seed positions for each region.
    queue = deque()
    for rid, seeds in region_seeds.items():
        for pos in seeds:
            queue.append((pos[0], pos[1], rid))

    # Process the queue: attempt to expand each region to adjacent cells.
    while queue:
        i, j, rid = queue.popleft()
        # Explore four orthogonal neighbors.
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < n and 0 <= nj < n and regions[ni][nj] is None:
                # Expand the region based on its expansion probability.
                if random.random() < expansion_prob[rid]:
                    regions[ni][nj] = rid
                    queue.append((ni, nj, rid))

    # --- Step 4: Post-Processing Unassigned Cells ---
    # For any cell that is still unassigned, assign a region based on neighboring regions if possible.
    for i in range(n):
        for j in range(n):
            if regions[i][j] is None:
                neighbor_ids = set()
                # Check for assigned neighbors in four directions.
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < n and 0 <= nj < n and regions[ni][nj] is not None:
                        neighbor_ids.add(regions[ni][nj])
                # Assign based on neighbors or randomly if none exist.
                if neighbor_ids:
                    regions[i][j] = random.choice(list(neighbor_ids))
                else:
                    regions[i][j] = random.choice(region_ids)
    return regions


def build_queen_board(n, queen_solution):
    """
    Build a human-readable chessboard representation from a queen solution.

    The board is represented as a list of lists where 'Q' marks a queen and '.' indicates an empty cell.

    Parameters:
        n (int): The size of the chessboard.
        queen_solution (List[int]): The queen positions where the i-th element is the column index of the queen in row i.

    Returns:
        List[List[str]]: The chessboard with queens placed.
    """
    board = []
    for i in range(n):
        # Initialize the row with empty cells.
        row = ['.' for _ in range(n)]
        # Place a queen at the specified column.
        row[queen_solution[i]] = 'Q'
        board.append(row)
    return board


def generate_map(case_number: int, name=None) -> dict:
    """
    Generate a map containing:
      - A random n-Queens solution.
      - A region (color block) segmentation grid based on the queen solution.
      - A human-readable chessboard representation.

    The generated map is structured as a dictionary with keys for name, case number, color grid, and queen board.

    Parameters:
        case_number (int): The size of the chessboard (n) and the n-Queens problem.
        name (str, optional): An identifier for the map. If None, a random name is generated.

    Returns:
        dict: A dictionary representing the generated map.
    """
    if name is None:
        num_rand = random.randint(0, 999999)
        name = "random-" + str(num_rand).zfill(6)

    new_map = {
        "name": name,
        "caseNumber": case_number,
        "colorGrid": []
    }

    # Generate a random n-Queens solution.
    queen_solution = random_n_queens(case_number)
    # Generate the region segmentation grid based on the queen solution.
    color_grid = generate_regions(case_number, queen_solution)
    new_map["colorGrid"] = color_grid
    # Generate the human-readable chessboard.
    new_map["queenBoard"] = build_queen_board(case_number, queen_solution)

    return new_map


def are_grids_same(g1, g2):
    """
    Determine whether two region segmentation grids have identical color block distributions.

    The comparison is performed by grouping the cell coordinates for each region in both grids and then comparing the groups.

    Parameters:
        g1 (List[List[int]]): The first grid.
        g2 (List[List[int]]): The second grid.

    Returns:
        bool: True if both grids have identical region groupings, False otherwise.
    """
    if len(g1) != len(g2):
        return False

    d1 = {}
    d2 = {}
    n = len(g1)

    # Build dictionaries mapping region IDs to lists of cell coordinates.
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
