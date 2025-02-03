# --- Cache Section ---
_positions_cache = {}  # Global cache to store generated queen positions for each board size


def generate_positions(n):
    """
    Generate all permutations of numbers from 0 to n-1 representing queen placements,
    with the constraint that the difference between consecutive columns is greater than 1.
    This ensures that queens in adjacent rows are not placed in adjacent columns (avoiding near-diagonal conflicts).

    Uses a global cache (_positions_cache) to avoid recomputation for the same n.

    Parameters:
        n (int): The size of the board (and number of queens).

    Returns:
        List[List[int]]: A list of valid queen positions where each inner list represents a permutation.
    """
    if n in _positions_cache:
        return _positions_cache[n]

    positions = []
    used = [False] * n  # Track whether a column is already used in the current permutation

    def backtrack(position):
        """
        Recursively build valid queen positions using backtracking.

        Parameters:
            position (List[int]): The current partial permutation of queen placements.
        """
        # If a full permutation is found, add a copy to positions
        if len(position) == n:
            positions.append(position[:])
            return

        # Try each column for the next row
        for i in range(n):
            # Check if column 'i' is unused and if placing a queen here does not violate the constraint
            if not used[i] and (not position or abs(position[-1] - i) > 1):
                used[i] = True  # Mark column as used
                position.append(i)
                backtrack(position)  # Continue to the next row
                position.pop()  # Backtrack: remove the queen placement
                used[i] = False  # Reset the column usage

    backtrack([])
    _positions_cache[n] = positions  # Cache the result for future calls
    return positions


def check_solution(positions, color_grid):
    """
    Quickly verify that a given queen placement satisfies the color block constraint.

    The board is divided into color blocks (provided by color_grid). This function checks that
    no two queens reside in the same color block. The positions already ensure that queens do not conflict
    by rows, columns, or immediate diagonals.

    Parameters:
        positions (List[int]): A permutation representing the queen positions (index as row, value as column).
        color_grid (List[List[int]]): A 2D grid representing the color blocks of the board.

    Returns:
        bool: True if the solution satisfies the constraint, False otherwise.
    """
    seen_blocks = set()  # Keep track of visited color blocks
    for i, col in enumerate(positions):
        # Convert block id to string for consistency with other parts of the system
        block_id = str(color_grid[i][col])
        if block_id in seen_blocks:
            return False  # Constraint violated: more than one queen in the same block
        seen_blocks.add(block_id)
    return True


def solve(queen_map, name, threshold=1):
    """
    Solve the chessboard puzzle given a board with color block constraints.

    The method performs the following steps:
      1. Generate all valid queen positions (permutations) that satisfy the near-diagonal constraint.
      2. For each generated position, check if it also meets the color block constraint.
      3. Count solutions, and if the count exceeds a predefined threshold, stop early (pruning).

    Parameters:
        queen_map (List[List[int]]): The board represented as a color grid (color blocks).
        name (str): An identifier for the puzzle.
        threshold (int, optional): The maximum number of solutions to search for before early termination.
                                   Defaults to 1.

    Returns:
        dict: A dictionary containing:
            - "name": The identifier provided.
            - "solvable": A boolean indicating if at least one solution exists.
            - "number_solution": The number of valid solutions found (up to threshold + 1).
            - "number_possibility": The total number of generated queen positions.
    """
    grid = queen_map  # The color grid representing the board
    all_positions = generate_positions(len(grid))  # Generate positions for an n x n board

    solution_count = 0  # Count of valid solutions
    for pos in all_positions:
        if check_solution(pos, grid):
            solution_count += 1
            if solution_count > threshold:
                # Early termination if the solution count exceeds the threshold
                break

    result = {
        "name": name,
        "solvable": solution_count > 0,
        "number_solution": solution_count,
        "number_possibility": len(all_positions)
    }
    return result
