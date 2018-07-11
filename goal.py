"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Goal class hierarchy.
"""

from typing import List, Tuple
from block import Block


class Goal:
    """A player goal in the game of Blocky.

    This is an abstract class. Only child classes should be instantiated.

    === Attributes ===
    colour:
        The target colour for this goal, that is the colour to which
        this goal applies.
    """
    colour: Tuple[int, int, int]

    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize this goal to have the given target colour.
        """
        self.colour = target_colour

    def score(self, board: Block) -> int:
        """Return the current score for this goal on the given board.

        The score is always greater than or equal to 0.
        """
        raise NotImplementedError

    def description(self) -> str:
        """Return a description of this goal.
        """
        raise NotImplementedError


class BlobGoal(Goal):
    """A goal to create the largest connected blob of this goal's target
    colour, anywhere within the Block.
    """
    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize blob goal to have the given target colour.
        """
        Goal.__init__(self, target_colour)

    def _undiscovered_blob_size(self, pos: Tuple[int, int],
                                board: List[List[Tuple[int, int, int]]],
                                visited: List[List[int]]) -> int:
        """Return the size of the largest connected blob that (a) is of this
        Goal's target colour, (b) includes the cell at <pos>, and (c) involves
        only cells that have never been visited.

        If <pos> is out of bounds for <board>, return 0.

        <board> is the flattened board on which to search for the blob.
        <visited> is a parallel structure that, in each cell, contains:
           -1  if this cell has never been visited
            0  if this cell has been visited and discovered
               not to be of the target colour
            1  if this cell has been visited and discovered
               to be of the target colour

        Update <visited> so that all cells that are visited are marked with
        either 0 or 1.
        """
        # i is the index of the column of the flattened board
        # j is the index of the row of the flattened board
        i = pos[0]
        j = pos[1]

        if i < 0 or i > len(board) - 1 or j < 0 or j > len(board) - 1:
            return 0
        else:
            if visited[i][j] != -1:
                return 0
            elif board[i][j] != self.colour:
                visited[i][j] = 0
                return 0
            else:
                visited[i][j] = 1
                blob_size = 1
                # Check the block to the left
                blob_size += self._undiscovered_blob_size((i - 1, j),
                                                          board, visited)
                # Check the block to the right
                blob_size += self._undiscovered_blob_size((i + 1, j),
                                                          board, visited)
                # Check the block to the top
                blob_size += self._undiscovered_blob_size((i, j - 1),
                                                          board, visited)
                # Check the block to the bottom
                blob_size += self._undiscovered_blob_size((i, j + 1),
                                                          board, visited)
                return blob_size

    def score(self, board: Block) -> int:
        """Return the current score for blob goal on the given board.

        The score is always greater than or equal to 0.
        """
        # Flatten the board
        flattened = board.flatten()

        # Create the parallel structure visited
        visited = [[-1 for _ in range(len(flattened))]
                   for _ in range(len(flattened))]

        # List of the size of the blobs found in the board
        lst_blob_size = []

        # Traverse the flattened board and add the blob size found into the list
        for i in range(len(flattened)):
            for j in range(len(flattened)):
                lst_blob_size.append(
                    self._undiscovered_blob_size((i, j), flattened, visited))

        # Return the largest blob size in the list
        return max(lst_blob_size)

    def description(self) -> str:
        """Return a description of blob goal.
        """
        description = "Aim for the largest blob (connected by side)" \
                      " of this colour."

        return description


class PerimeterGoal(Goal):
    """A goal to put the most possible units of this goal's target colour, on
    the outer perimater of the Block.
    """
    def __init__(self, target_colour: Tuple[int, int, int]) -> None:
        """Initialize perimeter goal to have the given target colour.
        """
        Goal.__init__(self, target_colour)

    def score(self, board: Block) -> int:
        """Return the current score for perimeter goal on the given board.

        The score is always greater than or equal to 0.
        """
        # Flatten the board
        flattened = board.flatten()

        # Traverse the perimater of the flattened board and add up the score
        total_score = 0
        for k in range(len(flattened)):
            if flattened[0][k] == self.colour:
                total_score += 1
            if flattened[len(flattened) - 1][k] == self.colour:
                total_score += 1
            if flattened[k][0] == self.colour:
                total_score += 1
            if flattened[k][len(flattened) - 1] == self.colour:
                total_score += 1

        # Return the total score
        return total_score

    def description(self) -> str:
        """Return a description of perimeter goal.
        """
        description = "Maximize the amount of this colour " \
                      "on the outer perimeter. "
        return description


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
        'max-attributes': 15
    })
