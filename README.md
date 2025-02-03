# Queens Map Generator

## Overview
This project is a sophisticated puzzle map generator that creates unique, colorful chessboard maps based on randomized n-Queens solutions. It leverages advanced algorithms to produce puzzles of various sizes (from 4×4 up to 17×17) while ensuring both challenge and uniqueness. Each generated map includes:

- **Region segmentation** (color grid)
- **A valid n-Queens solution** (queen board)
- **Comprehensive metadata** to certify the puzzle's integrity and difficulty level.

## Features

### 🎲 Randomized n-Queens Solver
- Utilizes a **randomized backtracking algorithm** to generate valid n-Queens solutions, ensuring diversity in puzzle generation.

### 🎨 Dynamic Region Partitioning
- Constructs a **colorful segmentation** of the chessboard using a **multi-source flood fill algorithm**.
- Special regions are seeded by assigning an **entire row and column** based on a queen's position.
- Other regions are initialized from the remaining queen positions.

### 🧠 Difficulty Evaluation
- A **custom solver** verifies the validity and difficulty of each map.
- Ensures that each generated map has **at most one solution** (or a limited number within a defined threshold).

### 🔍 Uniqueness Guarantee
- Implements a **uniqueness check** by comparing **color grid distributions** of newly generated maps against existing ones to **prevent duplicates**.

### ⚡ Multiprocessing Support
- Uses **Python's multiprocessing** to **generate maps in parallel**, significantly speeding up the process for larger board sizes.

### 📂 Comprehensive JSON Output
- Saves the final maps in a **JSON file** including:
  - **Region segmentation** (`colorGrid`)
  - **n-Queens solution** (`queenBoard`)
  - **Metadata** (e.g., puzzle name, board size, difficulty level)
- Allows for further use, analysis, or integration into other applications.

---

## 📁 Project Structure

```
chessboard-map-generator/
│── generator.py
│── solver.py
│── main.py
└── generated_maps/
    └── maps.json
```

### `generator.py`
Contains core functions for:
- **Random n-Queens Solution:** `random_n_queens(n)` generates a valid n-Queens configuration.
- **Region Segmentation:** `generate_regions(n, queen_solution)` partitions the board into regions based on the queen positions.
- **Chessboard Visualization:** `build_queen_board(n, queen_solution)` creates a human-readable chessboard.
- **Uniqueness Check:** `are_grids_same(g1, g2)` compares two color grids for identical region distributions.

### `solver.py`
Implements the solver (`solve`) to rigorously verify:
- Each **row and column** contains exactly one queen.
- No two queens are placed in **adjacent diagonal cells**.
- No **region (or color block) contains more than one queen**.

### `main.py`
Orchestrates the map generation process by:
- Determining the **target number** of maps per board size.
- Utilizing **multiprocessing** to generate maps concurrently.
- Enforcing both **difficulty and uniqueness criteria**.
- Saving the resulting maps in a **JSON file** (`generated_maps/maps.json`).

---

## 🛠 Requirements

- **Python Version:** 3.6 or higher
- **Standard Libraries Used:**
  - `random`
  - `json`
  - `multiprocessing`
  - `os`
  - `collections`
- No additional external packages required.

---

## 🚀 Installation and Usage

### Clone the Repository:
```bash
git clone https://github.com/Tony-XLZ/queens-map-generator.git
```

### Run the Generator:
```bash
python main.py
```
This command generates maps for board sizes **4 through 17** and saves the JSON output to the `generated_maps/` directory.

---

## 📜 Output Details

The **output JSON file** (`maps.json`) contains a dictionary where:
- **Keys** represent board sizes (e.g., "4", "5", …, "17").
- **Values** are lists of generated maps.

Each **map dictionary** includes:
- `name`: A unique identifier (e.g., "Map n8 #3").
- `caseNumber`: The board size (`n`).
- `colorGrid`: A **2D list** representing the region segmentation of the board.
- `queenBoard`: A **visual representation** of the n-Queens solution (`'Q'` for a queen, `'.'` for an empty cell).

---

## 📌 Example Output (JSON)
```json
{
  "8": [
    {
      "name": "Map n8 #3",
      "caseNumber": 8,
      "colorGrid": [
        [1, 1, 2, 2, 3, 3, 4, 4],
        [1, 1, 2, 2, 3, 3, 4, 4],
        ...
      ],
      "queenBoard": [
        [".", ".", ".", "Q", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", "Q", ".", "."],
        ...
      ]
    }
  ]
}
```

---

## 🎯 Future Improvements
- Add a **graphical interface** to visualize the chessboard and color regions interactively.
- Support **user-defined constraints** (e.g., specific region rules, additional difficulty settings).
- Optimize **region segmentation algorithms** for better performance and diversity.
- Extend **export formats** (e.g., CSV, XML, interactive web-based display).

---

## 📄 License
This project is open-source and available under the **MIT License**.

---

## 🤝 Contributing
We welcome contributions! Feel free to open an issue or submit a pull request.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

Happy coding! 🎉
