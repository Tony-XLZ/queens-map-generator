# Queens Map Generation

Welcome to the **Queens Map Generation** project! This project generates challenging chessboard puzzles based on the n-Queens problem combined with region (color block) constraints. It utilizes advanced Python techniques along with Cython acceleration to efficiently evaluate puzzle difficulty—even for larger board sizes (n > 11).

## Overview

The traditional n-Queens problem asks for placements of n queens on an n×n chessboard so that no two queens attack each other. In our extended version, additional constraints are introduced:

1. **Non-Adjacent Queens Constraint:** In consecutive rows, queens must not be placed in adjacent columns.
2. **Region (Color Block) Constraint:** The chessboard is divided into colored regions, and each region may contain at most one queen.

Because the number of valid queen placements grows combinatorially with n, especially when considering extra constraints, our project adopts a two-pronged approach for performance:
- **Python-Level Optimizations:** Using recursion with early-pruning and bit-level operations.
- **Cython Acceleration:** Rewriting the core backtracking solver in Cython (with released GIL and memory views) to achieve C-level speed.

## Project Structure

- **`main.py`**  
  The entry point of the application. It coordinates map generation, uniqueness checks, and calls the solver to evaluate each map's difficulty.

- **`generator.py`**  
  Contains functions to generate random n-Queens solutions and to partition the board into regions (color grids). The region generation uses a multi-source flood fill strategy with randomized probabilities.

- **`solver.py`**  
  The pure-Python solver implementation that evaluates board configurations by enumerating valid queen placements under the imposed constraints.

- **`solver_cy.pyx`**  
  A Cython implementation of the core recursive solver. This module uses static typing, memory views, and GIL-free recursion to greatly improve performance for larger board sizes.

- **`setup.py`**  
  The build script for compiling the Cython module. It uses `cythonize` along with NumPy’s header files to correctly compile the extension module.

## Requirements

- **Python 3.x** (tested with Python 3.13)
- **NumPy**
- **Cython**
- A C/C++ compiler (compatible with your platform)

Install the Python dependencies with pip:

```bash
pip install numpy cython
```

## Building the Cython Module

Before running `main.py`, you need to build the Cython extension:

```bash
python setup.py build_ext --inplace
```

This command compiles `solver_cy.pyx` into a binary extension module (e.g., `solver_cy.so` on Linux/macOS or `solver_cy.pyd` on Windows) that is automatically imported by `main.py`.

## Usage

After building the Cython module, you can run the main script:

```bash
python main.py
```

`main.py` will generate maps for chessboard sizes ranging from **4 to 17**. Each generated map includes:

- A **color grid** (region segmentation)
- A **visual chessboard** with queen placements
- An **evaluation report** that checks if the puzzle has a unique solution (or meets the difficulty threshold)

The generated maps are stored in a JSON file (`generated_maps/maps.json`).

## Scientific & Technical Insights

### Optimization Philosophy:
Rather than enumerating all possible valid configurations in pure Python, we directly count valid solutions using **bitwise operations and recursive backtracking**. Once the count exceeds a set threshold, the recursion prunes further search, saving computational time.

### Cython Acceleration:
The Cython module leverages:

- **Static Type Declarations:** Allowing the C compiler to optimize arithmetic and logical operations.
- **Memory Views:** To efficiently access NumPy arrays in a GIL-free context.
- **GIL Release:** Permitting the heavy recursive computation to run at near C-speed.

### Scalability:
These improvements are critical for handling **board sizes greater than 10**, where the search space can become enormous. Our design ensures that even with the combinatorial explosion, only the necessary computations are performed.

## Future Enhancements

- Support for **custom region growth rules**.
- **Visualization tools** for generated maps.
- **Integration with deep learning models** for automated difficulty tuning.
