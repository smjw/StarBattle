import numpy as np
import random


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
#     print(puzzles[i])  # Print the stored puzzle grid
#     print("\nSolution:")
#     print(solutions[i])  # Print the corresponding solution grid

data1900= np.load("star_battle_dataset.npz", allow_pickle=True)
puzzles = data1900["puzzles"]
solutions = data1900["solutions"]

# Save the dataset
np.savez_compressed("star_battle_dataset_test_2380.npz", puzzles=np.array(puzzles), solutions=np.array(solutions))
print("Dataset saved successfully!")