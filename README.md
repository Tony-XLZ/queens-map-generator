# N-Queens Region-Based Map Generator and Solver

## Overview
This project implements a powerful **N-Queens-based region map generator and solver** using **randomized backtracking, region segmentation, and multi-source flood fill**. It efficiently generates maps where the placement of queens determines distinct regions, and evaluates their solvability based on strict constraints. 

By leveraging **parallel processing**, this system rapidly generates unique maps across different board sizes while ensuring diversity in region layouts. The maps are stored in JSON format, allowing easy reuse and analysis.

## Features
- **Randomized N-Queens Placement**: Generates valid N-Queens solutions while enforcing column and diagonal constraints.
- **Region Segmentation**: Uses an **adaptive flood-fill algorithm** to create distinct regions based on queen placements.
- **Parallelized Map Generation**: Utilizes **multiprocessing** to generate and validate maps efficiently.
- **Solvability Evaluation**: Each generated map is assessed for its uniqueness and difficulty using a **constraint solver**.
- **Duplicate Detection**: Ensures no two maps share the same region segmentation structure.
- **Configurable Board Sizes**: Supports board sizes from **4×4 to 17×17**, with flexible generation targets.

## Implementation Details
### 1. N-Queens Randomized Backtracking
- A **randomized backtracking algorithm** places queens on an N×N chessboard.
- The solution ensures that **no two queens share the same row, column, or diagonal**.
- The generated queen positions serve as the foundation for defining **color regions** on the board.

### 2. Region-Based Grid Segmentation
- The board is divided into distinct **color regions**, with each region expanding outward from queen positions.
- A **randomly chosen special region** expands fully, while other regions expand probabilistically (0.3–0.5 probability per step).
- A **multi-source flood-fill algorithm** propagates regions efficiently while maintaining randomness.
- Any unassigned cells are post-processed to ensure complete coverage.

### 3. Map Validation & Filtering
- Each generated map is evaluated using a **solver** that determines if it has at most **one valid queen placement solution**.
- Maps exceeding the threshold are discarded to maintain a balance of challenge and uniqueness.
- The generated maps are checked for duplicates by comparing region layouts.

### 4. Parallelized Generation & Storage
- The system runs **multiple worker processes** to speed up map generation.
- Maps are saved in a **structured JSON file** (`generated_maps/maps.json`).
- Each map is uniquely named and labeled according to its board size.

## Usage
### Running the Map Generator
To generate maps for board sizes 4 to 17, run:
```bash
python generate_maps.py
```
This will:
- Generate and store new maps if the required number is not met.
- Skip redundant calculations by loading previously saved maps.
- Utilize **all available CPU cores** to parallelize the generation process.

### JSON Output Format
Each generated map follows this structure:
```json
{
    "name": "Map n8 #12",
    "caseNumber": 8,
    "colorGrid": [[1, 1, 2, ...], [3, 4, 2, ...], ...],
    "queenBoard": [[".", ".", "Q", ...], [".", "Q", ".", ...], ...]
}
```
- `name`: Unique identifier for the map.
- `caseNumber`: Board size (N×N).
- `colorGrid`: 2D array representing region assignments.
- `queenBoard`: Human-readable chessboard representation.

### Checking Map Uniqueness
To verify whether two generated maps share identical region structures, use:
```python
from generator import are_grids_same
same = are_grids_same(grid1, grid2)
```
This will return `True` if the maps are structurally identical and `False` otherwise.

## Performance Optimization
- **Batch Processing**: Generates maps in **batches of at least twice the required amount** to increase valid outputs.
- **Early Termination (Pruning)**: Stops searching once the required number of valid maps is found.
- **Cached Computation**: Stores previous queen placements to avoid redundant calculations.
- **Parallel Processing**: Runs multiple instances of the generator across CPU cores.
