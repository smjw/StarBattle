import numpy as np
import random
import z3
import os


# data1900= np.load("star_battle_dataset.npz", allow_pickle=True)
# puzzles = data1900["puzzles"]
# solutions = data1900["solutions"]

# # Save the dataset
# np.savez_compressed("star_battle_dataset_test_1900.npz", puzzles=np.array(puzzles), solutions=np.array(solutions))
# print("Dataset saved successfully!")


# data20 = np.load("star_battle_dataset_test.npz", allow_pickle=True)
# puzzles = data20["puzzles"]
# solutions = data20["solutions"]

# Save the dataset
# np.savez_compressed("star_battle_dataset_test_2020.npz", puzzles=np.array(puzzles), solutions=np.array(solutions))
# print("Dataset saved successfully!")


# data2020 = np.load("star_battle_dataset_test_2020.npz", allow_pickle=True)
# puzzles = data2020["puzzles"]
# solutions = data2020["solutions"]
# # show puzzles
# print(f"Total puzzles loaded: {len(puzzles)}")

# for i in range(len(puzzles)):  
#     print(f"\nPuzzle {i + 1}:")
#     print(puzzles[i]) 
#     print("\nSolution:")
#     print(solutions[i]) 

# data1900= np.load("star_battle_dataset.npz", allow_pickle=True)
# puzzles = data1900["puzzles"]
# solutions = data1900["solutions"]

# # Save the dataset
# np.savez_compressed("star_battle_dataset_test_2380.npz", puzzles=np.array(puzzles), solutions=np.array(solutions))
# print("Dataset saved successfully!")


def layout(grid_size=10, num_regions=10):
# random region layout with minimum 3 cells in a region
    grid = np.full((grid_size, grid_size), -1) 

    # place initial 3 cell regions
    region_seeds = [] 
    used_positions = set()  # to avoid overlapping regions

    for i in range(num_regions):
        while True:
            # random starting cell
            r, c = random.randint(0, grid_size - 1), random.randint(0, grid_size - 1)
            direction = random.choice([(0, 1), (1, 0)]) 

            # compute 3-cell region
            cells = [(r + direction[0] * j, c + direction[1] * j) for j in range(3)]

            # checks all cells are within bounds and not overlapping
            if all(0 <= nr < grid_size and 0 <= nc < grid_size and (nr, nc) not in used_positions for nr, nc in cells):
                for nr, nc in cells:
                    grid[nr, nc] = i  
                    used_positions.add((nr, nc))
                    region_seeds.append((nr, nc))  
                break  

    # expands all regions with flood fill
    def get_neighbors(r, c):
        neighbors = []
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < grid_size and 0 <= nc < grid_size and grid[nr, nc] == -1:
                neighbors.append((nr, nc))
        return neighbors

    cells_to_expand = region_seeds[:]  
    while cells_to_expand:
        r, c = cells_to_expand.pop(random.randint(0, len(cells_to_expand) - 1))
        neighbors = get_neighbors(r, c)
        if neighbors:
            random.shuffle(neighbors)
            for nr, nc in neighbors:
                grid[nr, nc] = grid[r, c]  
                cells_to_expand.append((nr, nc))  

    return grid

def puzzle_solver(puzzle: np.ndarray):
    height, width = puzzle.shape
    assert height == 10 and width == 10, "Puzzle must be a 10x10 grid"

    grid = [[z3.Int(f"grid_{i}_{j}") for j in range(10)] for i in range(10)]

    def solve_with_constraints(extra_constraints=[]):
        solver = z3.Solver()

        for i in range(10):
            for j in range(10):
                solver.add(z3.Or(grid[i][j] == 0, grid[i][j] == 1))

        for i in range(10):
            solver.add(z3.Sum([grid[i][j] for j in range(10)]) == 2)

        for j in range(10):
            solver.add(z3.Sum([grid[i][j] for i in range(10)]) == 2)

        num_regions = np.max(puzzle) + 1
        for region_id in range(num_regions):
            region_cells = [grid[i][j] for i in range(10) for j in range(10) if puzzle[i, j] == region_id]
            solver.add(z3.Sum(region_cells) == 2)

        for i in range(10):
            for j in range(10):
                neighbors = [
                    (i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1),  
                    (i - 1, j - 1), (i - 1, j + 1), (i + 1, j - 1), (i + 1, j + 1)  
                ]
                for ni, nj in neighbors:
                    if 0 <= ni < 10 and 0 <= nj < 10:
                        solver.add(z3.Or(grid[i][j] == 0, grid[ni][nj] == 0))

        #  additional constraints if needed
        for constraint in extra_constraints:
            solver.add(constraint)

        # solve the puzzle
        if solver.check() == z3.sat:
            model = solver.model()
            solution = np.array([[model[grid[i][j]].as_long() for j in range(10)] for i in range(10)])
            return solution, model
        else:
            return None, None  # No solution found

    # solve once to get a solution
    solution, model = solve_with_constraints()
    if solution is None:
        return None  # No solution

    # add a constraint to block this solution
    block_solution = z3.Or([grid[i][j] != model[grid[i][j]] for i in range(10) for j in range(10)])

    # Solve again to check if another solution exists
    _, second_model = solve_with_constraints([block_solution])

    if second_model is not None:
        return None  # more than one solution exists

    return solution  # unique solution found

#generate dataset of puzzles
num_puzzles = 2500
puzzles = []
solutions = []
unique_puzzles = set()
save_interval = 10  # Save every 10 puzzles
dataset_filename = "star_battle_dataset.npz"

# Load existing dataset if it exists
if os.path.exists(dataset_filename):
    print("Loading existing dataset...")
    data = np.load(dataset_filename, allow_pickle=True)
    puzzles = list(data["puzzles"])
    solutions = list(data["solutions"])
    unique_puzzles = {''.join(map(str, p.flatten())) for p in puzzles}
    print(f"Loaded {len(puzzles)} existing puzzles.")

while len(puzzles) < num_puzzles:
    layout1 = layout()
    solution = puzzle_solver(layout1)

    if solution is not None:
        layout_str = ''.join(map(str, layout1.flatten()))

        if layout_str not in unique_puzzles:
            puzzles.append(layout1)
            solutions.append(solution)
            unique_puzzles.add(layout_str)

    # saves progress evey 10 puzzles
    if len(puzzles) % save_interval == 0:
        print(f"Collected {len(puzzles)} puzzles... Saving progress.")
        np.savez_compressed(dataset_filename, puzzles=np.array(puzzles, dtype=object), solutions=np.array(solutions, dtype=object))
        print("Saved")

# Final save
print("Final dataset saving...")
np.savez_compressed(dataset_filename, puzzles=np.array(puzzles, dtype=object), solutions=np.array(solutions, dtype=object))
print("Dataset saved successfully!")

