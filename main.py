import json
import multiprocessing
import os
from generator_cy import generate_map, are_grids_same
from solver_cy import solve

import time


def target_map_count(n):
    """
    Determine the target number of maps to generate based on board size n.

    The mapping is as follows:
      - For n = 4 or 5: 30 maps.
      - For n = 6 or 7: 50 maps.
      - For n in [8, 13]: 70 maps.
      - For n in [14, 17]: 100 maps.

    Parameters:
        n (int): The size of the chessboard.

    Returns:
        int: The target number of maps for the given board size.
    """
    if n in [4, 5]:
        return 30
    elif n in [6, 7]:
        return 50
    elif 8 <= n <= 13:
        return 70
    elif 14 <= n <= 17:
        return 100
    else:
        return 0


def worker_generate_map(n):
    """
    Generate a single n×n map and evaluate it using the solver.

    This function generates a map using the n-Queens based generator and then
    checks its solvability via the solver. Only maps with a number of solutions
    not exceeding a preset threshold (here, threshold=1) are accepted.

    Parameters:
        n (int): The size of the board (n×n).

    Returns:
        dict or None: The generated map if it satisfies the threshold condition;
                      otherwise, None.
    """
    # Generate a new map based on an n-Queens solution and region segmentation.
    new_map = generate_map(n)
    threshold = 1
    # Evaluate the generated map with the solver.
    solution = solve(new_map["colorGrid"], new_map["name"], threshold=threshold)
    # Accept maps with at most 'threshold' solutions.
    if solution["number_solution"] <= threshold:
        return new_map
    else:
        return None


if __name__ == '__main__':
    time_start = time.time()
    # Create the output directory if it doesn't exist.
    output_dir = "generated_maps"
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.join(output_dir, "maps.json")

    # Attempt to load existing map data from file.
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Ensure that each board size (from 4 to 17) has its own list for storing maps.
    for n in range(4, 12):
        key = str(n)
        if key not in data:
            data[key] = []

    # Create a multiprocessing pool with a number of processes equal to the CPU count.
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    try:
        # Process board sizes from 4 to 17.
        for n in range(4, 12):
            key = str(n)
            target = target_map_count(n)
            current_maps = data[key]
            needed = target - len(current_maps)
            print(f"Board size {n}: Need {needed} more maps (target {target}).")
            # Increase the batch size to improve the likelihood of generating valid maps.
            batch_size = max(needed * 2, 10)

            while needed > 0:
                # Generate a batch of maps concurrently.
                results = pool.map(worker_generate_map, [n] * batch_size)
                for new_map in results:
                    # Skip if no valid map was generated.
                    if new_map is None:
                        continue
                    # Check if the new map's region segmentation is unique compared to existing maps.
                    is_unique = True
                    for existing in current_maps:
                        if are_grids_same(new_map["colorGrid"], existing["colorGrid"]):
                            is_unique = False
                            break
                    if is_unique:
                        # Assign a unique name and update the map list.
                        new_map["name"] = f"Map n{n} #{len(current_maps) + 1}"
                        current_maps.append(new_map)
                        needed -= 1
                        print(f"Board size {n}: Generated {new_map['name']} (total now {len(current_maps)}).")
                        if needed <= 0:
                            break
            print(f"Board size {n} completed, generated {len(current_maps)} maps.")

        # Save all generated maps to the JSON file.
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("All maps have been generated and saved!")
        time_end = time.time()
        print('time cost', time_end - time_start, 's')
    finally:
        # Properly close and join the multiprocessing pool.
        pool.close()
        pool.join()
