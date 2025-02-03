def generate_positions(n):
    """
    Generates all valid permutations of positions (0 to n-1) for placing queens,
    with the additional constraint that consecutive positions (in the permutation)
    must not be adjacent (i.e., the absolute difference > 1).

    Args:
        n (int): The size of the board (and the number of queens).

    Returns:
        list of list of int: A list containing all valid permutations.
    """

    def backtrack(position, used):
        # When a complete permutation is constructed, add a copy to the positions list.
        if len(position) == n:
            positions.append(position[:])
            return
        for i in range(n):
            # Check if number i is not used and that it does not violate the non-adjacency rule.
            if not used[i] and (len(position) < 1 or abs(position[-1] - i) > 1):
                position.append(i)
                used[i] = True
                backtrack(position, used)
                # Backtrack: remove the last placed number and mark it as unused.
                position.pop()
                used[i] = False

    positions = []
    backtrack([], [False] * n)
    return positions


def fill_blocks(color_grid):
    """
    Groups grid coordinates by their block (or color) values.

    This function builds a dictionary where each key is a color (converted to string)
    and the corresponding value is a list of coordinates (as [row, col]) that share that color.

    Args:
        color_grid (list of list): A 2D list representing the board with color identifiers.

    Returns:
        dict: A dictionary mapping each color to a list of coordinate pairs.
    """
    blocks = {}
    for i in range(len(color_grid)):
        for j in range(len(color_grid[i])):
            color = str(color_grid[i][j])
            if color in blocks:
                blocks[color].append([i, j])
            else:
                blocks[color] = [[i, j]]
    return blocks


def check_win(game_state, blocks):
    """
    Checks if the current game state is a winning solution.

    The function verifies:
      1. Each row and each column contains exactly one queen.
      2. No two queens share a diagonal adjacent (both primary and secondary) cell.
      3. Within any block (or color group), at most one queen is placed.

    Args:
        game_state (list of list of int): A 2D board state with 1 representing a queen and 0 empty.
        blocks (dict): A dictionary mapping block identifiers to lists of their coordinates.

    Returns:
        bool: True if the game state satisfies all winning conditions, False otherwise.
    """
    board_size = len(game_state)

    # Check that every row and every column has exactly one queen.
    for i in range(board_size):
        sum_row = sum(game_state[i])
        if sum_row != 1:
            return False

        sum_col = sum(game_state[j][i] for j in range(board_size))
        if sum_col != 1:
            return False

    # Check that no queen is diagonally adjacent to another queen.
    # This check only applies to positions that have all four diagonal neighbors.
    for i in range(1, board_size - 1):
        for j in range(1, board_size - 1):
            if game_state[i][j] == 1:
                if game_state[i - 1][j - 1] == 1:
                    return False
                if game_state[i - 1][j + 1] == 1:
                    return False
                if game_state[i + 1][j - 1] == 1:
                    return False
                if game_state[i + 1][j + 1] == 1:
                    return False

    # Check that in each block, there is at most one queen.
    for key in blocks:
        sum_block = 0
        for coord in blocks[key]:
            sum_block += game_state[coord[0]][coord[1]]
        if sum_block > 1:
            return False

    return True


def solve(queen_map, name):
    """
    Determines the solvability and number of winning configurations for a given queen_map.

    The function:
      1. Constructs the blocks (or color groups) based on the input grid.
      2. Generates all valid positions using generate_positions.
      3. For each permutation, it builds a game state with queens placed accordingly.
      4. Validates the game state with check_win.

    Args:
        queen_map (list of list): A 2D grid representing the board with colors/blocks.
        name (str): An identifier for the current puzzle instance.

    Returns:
        dict: A dictionary containing:
            - "name": the given puzzle name,
            - "solvable": True if at least one winning configuration is found,
            - "number_solution": count of winning configurations,
            - "number_possibility": total number of valid position permutations considered.
    """
    grid = queen_map
    # Group cells into blocks based on their color.
    blocks = fill_blocks(grid)
    # Generate all possible non-adjacent queen positions (as permutations) for the board size.
    all_pos = generate_positions(len(grid))

    result = {
        "name": name,
        "solvable": False,
        "number_solution": 0,
        "number_possibility": len(all_pos)
    }

    # Iterate over every valid permutation of queen positions.
    for positions in all_pos:
        # Initialize an empty game state board.
        game_state = [[0] * len(grid) for _ in range(len(grid))]

        # Place queens according to the current permutation.
        for row, col in enumerate(positions):
            game_state[row][col] = 1

        # If the configuration is winning, update the result.
        if check_win(game_state, blocks):
            result['solvable'] = True
            result['number_solution'] += 1

    return result
