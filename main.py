import json
import multiprocessing
import os
from generator import generate_map, are_grids_same
from solver import solve


def target_map_count(n):
    """
    Determine the target number of maps to generate based on the board size.

    For different board sizes, the required number of maps is:
      - n in [4, 5]: 30 maps
      - n in [6, 7]: 50 maps
      - n in [8, 13]: 70 maps
      - n in [14, 17]: 100 maps
      - Otherwise: 0 maps

    Args:
        n (int): The side length of the chessboard.

    Returns:
        int: The target count of maps to generate for board size n.
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
    Generate a map with board size n and evaluate its difficulty using the solver.

    This worker function performs the following:
      1. Generates a map for a chessboard of size n using a random n-Queens solution.
      2. Uses the solver to evaluate the map (by checking the number of solutions).
      3. Returns the map only if the number of solutions does not exceed the threshold (set to 1).
         Otherwise, returns None.

    Args:
        n (int): The board size.

    Returns:
        dict or None: The generated map dictionary if it meets the threshold criteria;
                      otherwise, None.
    """
    new_map = generate_map(n)
    threshold = 1
    solution = solve(new_map["colorGrid"], new_map["name"])
    # Only return maps with solution count at or below the threshold.
    if solution["number_solution"] <= threshold:
        return new_map
    else:
        return None


if __name__ == '__main__':
    # Create the output directory and define the JSON file path.
    output_dir = "generated_maps"
    os.makedirs(output_dir, exist_ok=True)
    file_name = os.path.join(output_dir, "maps.json")

    # Attempt to load existing map data from the JSON file.
    # The format is a dictionary with board sizes as keys (e.g., "4", "5", etc.)
    # and a list of corresponding maps as values.
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}

    # Ensure each board size from 4 to 17 has an associated list in the data.
    for n in range(4, 18):
        key = str(n)
        if key not in data:
            data[key] = []

    # Create a pool of worker processes equal to the number of CPU cores.
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())

    try:
        # For each board size from 4 to 17, generate the required number of maps.
        for n in range(4, 18):
            key = str(n)
            target = target_map_count(n)
            current_maps = data[key]
            needed = target - len(current_maps)
            print(f"Board size {n}: Need to generate {needed} new map(s) (target {target} maps).")
            # Increase the batch size to improve the probability of obtaining maps that meet the criteria.
            batch_size = max(needed * 2, 10)

            while needed > 0:
                # Use multiprocessing to generate a batch of maps for the current board size.
                results = pool.map(worker_generate_map, [n] * batch_size)
                for new_map in results:
                    if new_map is None:
                        continue

                    # Uniqueness check: ensure the new map's color grid is not identical to any existing map.
                    is_unique = True
                    for existing in current_maps:
                        if are_grids_same(new_map["colorGrid"], existing["colorGrid"]):
                            is_unique = False
                            # Duplicate map; skip adding.
                            break
                    if is_unique:
                        new_map["name"] = f"Map n{n} #{len(current_maps) + 1}"
                        current_maps.append(new_map)
                        needed -= 1
                        print(f"Board size {n}: Generated {new_map['name']} (total now {len(current_maps)}).")
                        if needed <= 0:
                            break
            print(f"Board size {n} complete, with a total of {len(current_maps)} maps.")

        # Save all generated maps to the JSON file.
        # The saved JSON includes:
        #    - "name": the map name,
        #    - "caseNumber": the board size,
        #    - "colorGrid": the region segmentation grid,
        #    - "queenBoard": the chessboard with the queen solution.
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("All maps have been generated and saved!")
    finally:
        pool.close()
        pool.join()
