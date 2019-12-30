from itertools import combinations
from copy import deepcopy
from plotter import plot_solution

# Define each 'piece' with one square being at the origin, and all others
# in terms of displacement from the origin
pieces = [[(0, 0)],
          [(0, 0), (1, 0)],
          [(0, 0), (1, 0), (2, 0)],
          [(0, 0), (1, 0), (0, 1)],
          [(0, 0), (1, 0), (2, 0), (3, 0)],
          [(0, 0), (1, 0), (1, 1), (2, 0)],
          [(0, 0), (1, 0), (0, 1), (1, 1)],
          [(0, 0), (0, 1), (1, 0), (2, 0)],
          [(0, 0), (1, 0), (1, 1), (2, 1)]]

a_to_f = {"A": 5,
          "B": 4,
          "C": 3,
          "D": 2,
          "E": 1,
          "F": 0}


# Store the coordinates of all the points in the grid
grid = []
for y in range(6):
    for x in range(6):
        grid.append((x, y))

# All the ways to rotate/invert a piece
transforms = [[],
              ["rot"],
              ["rot", "rot"],
              ["rot", "rot", "rot"],
              ["inv"],
              ["inv", "rot"],
              ["inv", "rot", "rot"],
              ["inv", "rot", "rot", "rot"]]


def rotate_anticlockwise(piece):
    """Takes a piece and rotates it a quarter turn anticlockwise"""
    for counter, (x, y) in enumerate(piece):
        piece[counter] = (y, -x)
    return piece


def invert(piece):
    """Takes a piece and inverts it"""
    for counter, (x, y) in enumerate(piece):
        piece[counter] = (x, -y)
    return piece


def apply_transform(piece, transform):
    """Applies a transform as a sequence of operations which are a
       rotation or an inversion"""
    for operation in transform:
        if operation == "inv":
            piece = invert(piece)
        elif operation == "rot":
            piece = rotate_anticlockwise(piece)
    return piece


def possible_placement(x0,
                       y0,
                       transformed_piece,
                       spaces_left,
                       pieces_left,
                       current_solution):
    # Remove squares where the new piece fits
    for (dx, dy) in transformed_piece:
        spaces_left.remove((x0 + dx, y0 + dy))

    # Recurse to try to put the next piece in
    current_solution.append([(x0, y0), transformed_piece])
    returned = check_fit(pieces_left,
                         spaces_left,
                         current_solution)
    if returned:
        return returned
    else:
        current_solution.pop(-1)
        return False


def check_fit(pieces_left, spaces_left, current_solution):
    """Recursive function to test whether a solution exists"""

    # Pick up next piece on the list
    try:
        piece = pieces_left.pop(0)
    except IndexError:
        # If list is empty, the combination works
        return current_solution

    tried_here = []
    # Run through each transform of the piece
    for transform in transforms:
        transformed_piece = apply_transform(deepcopy(piece), transform)

        # Run through each possible starting point in the remaining grid
        for (x0, y0) in spaces_left:
            fit = False

            new_try = []
            # Record this 'new try'
            for (dx, dy) in transformed_piece:
                new_try.append((x0 + dx, y0 + dy))
            new_try_set = set(new_try)

            if new_try_set not in tried_here:
                tried_here.append(new_try_set)

                # Check that the transformed piece fits in the grid
                for square in new_try:
                    if square not in spaces_left:
                        # The piece does not fit
                        break
                else:
                    # The piece fits
                    fit = True
                    returned = possible_placement(x0,
                                                  y0,
                                                  transformed_piece,
                                                  deepcopy(spaces_left),
                                                  deepcopy(pieces_left),
                                                  current_solution)
                    if returned:
                        return returned
                    else:
                        continue
    else:
        # The piece cannot be fitted into the pattern
        return False


# User interface - coordinates are A1 to F6
print("Enter 7 squares for the blocked squares:")
blockage = []
for i in range(7):
    square = input("{}: ".format(i+1))
    blockage.append((int(square[1])-1, a_to_f[square[0]]))

starting_grid = deepcopy(grid)
for square in blockage:
    starting_grid.remove(square)
result = check_fit(pieces, starting_grid, [])
plot_solution(result)
