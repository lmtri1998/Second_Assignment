"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional
import pygame
from renderer import Renderer
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)
        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


class RandomPlayer(Player):
    """A random player

    A random player can choose 1 of the 5 possible types of action
    and do it on the chosen block
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the RandomPlayer has randomly selected for action
    # _level:
    #     The level of the Block that the RandomPlayer randomly selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this RandomPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        # Has not chosen any block yet so _level and _selected_block should be
        # set to 0 and None respectively
        self._level = 0
        self._selected_block = None

    def choose_random_move(self) -> None:
        """Randomly choose a move and execute it.

        """
        # Randomize a random number from 0 to 4. Choose move according to the
        # random number.
        # If rand_num is 0 swap block horizontally.
        # If rand_num is 1 swap block vertically.
        # If rand_num is 2 rotate block clockwise.
        # If rand_num is 3 rotate block counter-clockwise.
        # If rand_num is 4 smash the block.
        rand_num = random.randint(0, 4)
        if rand_num == 0:
            self._selected_block.swap(0)
        elif rand_num == 1:
            self._selected_block.swap(1)
        elif rand_num == 2:
            self._selected_block.rotate(1)
        elif rand_num == 3:
            self._selected_block.rotate(3)
        else:
            self._selected_block.smash()

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutate
        the Board as appropriate.

        Return 0 upon successful completion of a move.
        """
        # Generate random level and random (x,y) position to get a random block.
        self._level = random.randint(0, board.max_depth)
        rand_x = random.randint(0, board.size)
        rand_y = random.randint(0, board.size)
        block = board.get_selected_block((rand_x, rand_y), self._level)

        # Set _selected_block, highlighted it and draw the board
        self._selected_block = block
        self._selected_block.highlighted = True
        self.renderer.draw(board, self.id)

        # Delay the action
        pygame.time.wait(TIME_DELAY)

        # Make a random move to mutate the block, set the block's highlighted to
        # False and redraw the board.
        self.choose_random_move()
        self._selected_block.highlighted = False
        self.renderer.draw(board, self.id)

        # Return 0
        return 0


class SmartPlayer(Player):
    """A smart player

    A SmartPlayer has a “difficulty” level, which indicates how difficult it is
    to play against it. The difficulty level is an integer >= 0,
    and dictates how many possible moves it compares when choosing a move to
    make.
    === Public Attributes ===
    difficulty: int
        The difficulty of this SmartPlayer
    compare: int
        Number of moves to compare given the difficulty
    move_id: int
        The id of the move to mutate the block. If move_id is 0 swap the block
        horizontally. If move_id is 1 swap the block vertically. If move_id is
        2 rotate the block clockwise. If move_id is 3 rotate the block
        counter-clockwise
    === Representation Invariants ===
    diffculty >= 0
    0 <= move_id <= 3
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the SmartPlayer has randomly selected for action

    # List of number of move to comapre base on difficulty
    MOVE_TO_COMPARE = [5, 10, 25, 50, 100, 150]

    difficulty: int
    compare: int
    move_id: int
    _selected_block: Optional[Block]

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal,
                 difficulty: int) -> None:
        super().__init__(renderer, player_id, goal)
        self.difficulty = difficulty

        # Make compare takes a value base on difficulty.
        if difficulty >= 5:
            self.compare = 150
        else:
            self.compare = self.MOVE_TO_COMPARE[difficulty]

        # Has not chosen any move yet so the id should be -1
        self.move_id = -1

        # Has not chosen any block yet so _level and _selected_block should be
        # None
        self._selected_block = None

    def _choose_smart_move(self, board: Block) -> None:
        """Choose the smartest move. Set the move_id and selected_block to the
        chosen block and move.
        """
        max_score = 0
        # Check the moves base on self.compare value
        for _ in range(self.compare):
            # Choose a random block
            rand_x = random.randint(0, board.size)
            rand_y = random.randint(0, board.size)
            block = board.get_selected_block((rand_x, rand_y),
                                             random.randint(0, board.max_depth))
            # Choose a random move id
            rand_move_id = random.randint(0, 3)

            # Mutate the random block, check the score, set the selected block,
            # if the score is higher than the max score, and set the move_id.
            if rand_move_id == 0:
                block.swap(0)
                new_score = self.goal.score(board)
                block.swap(0)
            elif rand_move_id == 1:
                block.swap(1)
                new_score = self.goal.score(board)
                block.swap(1)
            elif rand_move_id == 2:
                block.rotate(1)
                new_score = self.goal.score(board)
                block.rotate(3)
            else:
                block.rotate(3)
                new_score = self.goal.score(board)
                block.rotate(1)
            max_score = self._compare_score(new_score, max_score, block,
                                            rand_move_id)
        # If no block was selected, set the selected block to the top level
        # block and set the move id to 2 to rotate it clockwise
        if self._selected_block is None:
            self._selected_block = board.get_selected_block((0, 0), 0)
            self.move_id = 2

    def _compare_score(self, new_score: int, max_score: int, block: Block,
                       move_id: int) -> int:
        """Compare the current max score with the new score. If new score is
        greater return the new score and set the slected block to the current
        block the move id to the current move id. Return the greater score of
        the two
        """
        if new_score <= max_score:
            return max_score
        else:
            self._selected_block = block
            self.move_id = move_id
            return new_score

    def _execute_chosen_move(self, move_id: int) -> None:
        """Execute chosen move base on move id"""
        if move_id == 0:
            self._selected_block.swap(0)
        elif move_id == 1:
            self._selected_block.swap(1)
        elif move_id == 2:
            self._selected_block.rotate(1)
        else:
            self._selected_block.rotate(3)

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move.
        """
        # Set the move_id and selected_block that correspond to the smartest
        # move
        self._choose_smart_move(board)

        # Highlight the chosen block and draw the board
        self._selected_block.highlighted = True
        self.renderer.draw(board, self.id)

        # Delay the game
        pygame.time.wait(TIME_DELAY)

        # Execute the chosen move
        self._execute_chosen_move(self.move_id)

        # Unhighlight the block and redraw the board
        self._selected_block.highlighted = False
        self.renderer.draw(board, self.id)

        # Return 0
        return 0


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
