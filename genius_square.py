from itertools import combinations
from copy import deepcopy

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


# Store the coordinates of all the points in the grid
grid = []
for x in range(6):
    for y in range(6):
        grid.append((x, y))
print(grid)

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


def check_fit(pieces_left, spaces_left):
    """Recursive function to test whether a solution exists"""

    # Pick up next piece on the list
    try:
        piece = pieces_left.pop(0)
    except IndexError:
        # If list is empty, the combination works
        return True

    # Run through each transform of the piece
    for transform in transforms:
        transformed_piece = apply_transform(piece, transform)

        # Run through each possible starting point in the remaining grid
        for (x0, y0) in spaces_left:
            fit = True

            # Check that the transformed piece fits in the grid
            for (dx, dy) in transformed_piece:
                if (x0 + dx, y0 + dy) not in spaces_left:
                    # The piece does not fit
                    fit = False
                    break
            if fit:
                # The piece fits - remove all squares it covers
                for (dx, dy) in transformed_piece:
                    spaces_left.remove((x0 + dx, y0 + dy))
                break
        if fit:
            # Recurse to try to put the next piece in
            return_code = check_fit(pieces_left, deepcopy(spaces_left))
            if return_code:
                return True
    else:
        # The piece cannot be fitted into the pattern
        return False


# Test each possible arrangement of the 7 pegs to see whether there is a
# solution
failure_list = []
possible_blockages = combinations(grid, 7)
for number, blockage in enumerate(possible_blockages):

    # Create the grid of spaces left after blocking done
    starting_grid = deepcopy(grid)
    for square in blockage:
        starting_grid.remove(square)

    # Start the recursive algorithm to find a solution
    result = check_fit(pieces, starting_grid)
    if result:
        print("{}: Success".format(number))
    else:
        print("{}: Failure".format(number))
        failure_list.append(blockage)

# Return the result of the investigation
if failure_list == []:
    print("A solution exists for every combination of 7 pegs")
else:
    print("The failed cases are:\n")
    for blockage in failure_list:
        print(blockage)
