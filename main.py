import numpy as np

data = np.load("star_battle_dataset.npz", allow_pickle=True)
puzzles = data["puzzles"]
solutions = data["solutions"]