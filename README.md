# Queens Map Generation

Welcome to the **Queens Map Generation** project! This project generates challenging chessboard puzzles based on the n-Queens problem combined with region (color block) constraints. It utilizes advanced Python techniques along with Cython acceleration to efficiently evaluate puzzle difficulty—even for larger board sizes (n > 11).

## Project Structure

```bash
queens-map-generator/
├── generator_cy.pyx        # Cython module for generating maps using n-Queens and flood fill algorithms
├── solver_cy.pyx           # Cython module for validating maps via optimized backtracking
├── main.py                 # Main script for parallel map generation and validation
├── setup.py                # Build script for Cython extensions
└── README.md               # This documentation file
```


## Overview

MapGen uses a multi-stage process to generate complex map layouts:

1. **n-Queens Seed Generation**  
   A randomized backtracking algorithm produces a valid n-Queens solution, where each queen's position acts as a seed for a distinct region.

2. **Region Partitioning via Flood Fill**  
   Using a multi-source flood fill algorithm with randomized expansion probabilities, each queen-seeded region expands until the grid is completely partitioned. Post-processing ensures that no cell is left unassigned.

3. **Rigorous Map Validation**  
   - **Connectivity Check**: Each region is verified for connectivity using a breadth-first search (BFS) algorithm.  
   - **Unique Solution Validation**: An optimized backtracking solver (implemented in Cython) counts valid queen placements under additional constraints. Only maps with a challenging solution space (at most one valid solution) are accepted.

4. **Parallel Generation**  
   MapGen harnesses Python’s multiprocessing to concurrently generate and validate maps across different board sizes, ensuring efficiency even at scale.



## Features

- **Randomized n-Queens Solver**  
  Generates diverse n-Queens solutions using a randomized backtracking approach, ensuring varied starting points for map generation.

- **Dynamic Region Partitioning**  
  Converts n-Queens solutions into region-partitioned grids through a probabilistic multi-source flood fill, creating natural and unpredictable region shapes.

- **Efficient Connectivity Verification**  
  Employs BFS to guarantee that every region is connected, a key requirement for map validity.

- **Optimized Backtracking Solver**  
  Counts valid queen placements under strict constraints using a highly optimized Cython implementation that leverages NumPy for speed and memory efficiency.

- **Parallel Map Generation**  
  Utilizes multiprocessing to generate maps in batches, dramatically reducing overall computation time.

- **Unique Map Validation**  
  Ensures that each generated map is distinct by comparing region layouts, maintaining a high standard of variety and challenge.



## How It Works

### 1. Seed Generation with n-Queens

- **Randomized Backtracking**  
  The project begins by solving the n-Queens problem using a randomized backtracking algorithm. This approach not only guarantees a valid configuration (one queen per row, with no conflicts) but also introduces randomness to enhance map diversity.

### 2. Region Partitioning via Flood Fill

- **Multi-Source Flood Fill**  
  Each queen’s position acts as a seed for a region. Regions expand using a probabilistic flood fill with expansion probabilities between 0.3 and 0.5. This results in organic and varied region boundaries.

- **Post-Processing**  
  Cells left unassigned after the initial flood fill are filled by considering adjacent regions, ensuring complete coverage of the grid.

### 3. Map Validation

- **Connectivity Check**  
  A BFS algorithm inspects each region to ensure it forms a single connected component.

- **Backtracking Solver with Early Pruning**  
  An optimized solver, implemented in Cython, evaluates whether the map meets the required challenge criteria. It uses bitmasking and early pruning to efficiently count valid queen placements under constraints (e.g., queens in consecutive rows must not be in adjacent columns, and only one queen per region).

### 4. Parallel Execution

- **Multiprocessing**  
  The main script uses Python’s multiprocessing capabilities to generate maps concurrently across multiple board sizes, ensuring efficient use of system resources.



## Installation

Before building MapGen, ensure you have Python 3, a C compiler, and the required libraries installed. Then, install the dependencies:

```bash
pip install cython numpy
```

Clone the repository and build the Cython extensions:

```bash
git clone https://github.com/Tony-XLZ/queens-map-generator.git
cd queens-map-generator
python setup.py build_ext --inplace
```



## Usage

The entry point for the project is `main.py`, which orchestrates map generation, validation, and saving the output as a JSON file. To run the project:

```bash
python main.py
```

Generated maps are stored in the `generated_maps` directory in JSON format. The console output provides real-time logs of the generation process and timing information.
