"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Game class, which is the main class for the
Blocky game.

At the bottom of the file, there are some function that you
can call to try playing the game in several different configurations.
"""
import random
from typing import List
from block import Block, random_init
from goal import BlobGoal, PerimeterGoal
from player import Player, HumanPlayer, RandomPlayer, SmartPlayer
from renderer import Renderer, COLOUR_LIST, colour_name, BOARD_WIDTH


class Game:
    """A game of Blocky.

    === Public Attributes ===
    board:
        The Blocky board on which this game will be played.
    renderer:
        The object that is capable of drawing our Blocky board on the screen,
        and tracking user interactions with the Blocky board.
    players:
        The entities that are playing this game.

    === Representation Invariants ===
    - len(players) >= 1
    """
    board: Block
    renderer: Renderer
    players: List[Player]

    def __init__(self, max_depth: int,
                 num_human: int,
                 random_players: int,
                 smart_players: List[int]) -> None:
        """Initialize this game, as described in the Assignment 2 handout.

        Precondition:
            2 <= max_depth <= 5
        """
        # Store the total number of players
        num_player = num_human + random_players + len(smart_players)

        # Create the renderer
        self.renderer = Renderer(num_player)

        # Create players with random goal and random target colour
        self._create_player(num_human, random_players, smart_players)

        # Create a random board and update it locations
        self.board = random_init(0, max_depth)
        self.board.update_block_locations((0, 0), BOARD_WIDTH)

        # Draw the board
        self.renderer.draw(self.board, 0)

    def _create_player(self, num_human: int,
                       random_players: int,
                       smart_players: List[int]) -> None:
        """Generate a random goal type, for all players to share. Generate the
        right number of human players, random players, and smart players (with
        the given difficulty levels), in that order. Give the players
        consecutive player numbers, starting at 0. Assign each of them a random
        target colour and display their goal to them.

        """
        # Create a list of goal for use in randomizing goals
        goal = [BlobGoal, PerimeterGoal]

        # Generate a random goal for all player to share
        rand_goal = random.choice(goal)

        self.players = []
        # Store the current player id
        player_id = 0

        # Generate HumanPLayer(s) and add it to the list of players
        for _ in range(num_human):
            # Randomize the target colours
            rand_num = random.randint(0, 3)
            human = HumanPlayer(self.renderer, player_id,
                                rand_goal(COLOUR_LIST[rand_num]))
            self.players.append(human)
            self.renderer.display_goal(human)
            player_id += 1

        # Generate RandomPlayer(s) and add it to the list of players
        for _ in range(random_players):
            # Randomize the target colours
            rand_num = random.randint(0, 3)
            rand_player = RandomPlayer(self.renderer, player_id,
                                       rand_goal(COLOUR_LIST[rand_num]))
            self.players.append(rand_player)
            self.renderer.display_goal(rand_player)
            player_id += 1

        # Generate SmartPlayer(s) and add it to the list of players
        for difficulty in smart_players:
            # Randomize the target colours
            rand_num = random.randint(0, 3)
            smart_player = SmartPlayer(self.renderer, player_id,
                                       rand_goal(COLOUR_LIST[rand_num]),
                                       difficulty)
            self.players.append(smart_player)
            self.renderer.display_goal(smart_player)
            player_id += 1

    def run_game(self, num_turns: int) -> None:
        """Run the game for the number of turns specified.

        Each player gets <num_turns> turns. The first player in self.players
        goes first.  Before each move, print to the console whose turn it is
        and what the turn number is.  After each move, print the current score
        of the player who just moved.

        Report player numbers and turn numbers using 1-based counting.
        For example, refer to the self.players[0] as 'Player 1'.

        When the game is over, print who won to the console.

        """
        # Index within self.players of the current player.
        index = 0
        for turn in range(num_turns * len(self.players)):
            player = self.players[index]
            print(f'Player {player.id}, turn {turn}')
            if self.players[index].make_move(self.board) == 1:
                break
            else:
                print(f'Player {player.id} CURRENT SCORE: ' +
                      f'{player.goal.score(self.board)}')
                index = (index + 1) % len(self.players)

        # Determine and report the winner.
        max_score = 0
        winning_player = 0
        for i in range(len(self.players)):
            score = self.players[i].goal.score(self.board)
            print(f'Player {i} : {score}')
            if score > max_score:
                max_score = score
                winning_player = i
        print(f'WINNER is Player {winning_player}!')
        print('Players had these goals:')
        for player in self.players:
            print(f'Player {player.id} ' +
                  f'goal = \n\t{player.goal.description()}: ' +
                  f'{colour_name(player.goal.colour)}')


def auto_game() -> None:
    """Run a game with two computer players of different difficulty.
    """
    random.seed(1001)
    game = Game(4, 0, 0, [1, 6])
    game.run_game(10)


def two_player_game() -> None:
    """Run a game with two human players.
    """
    random.seed(507)
    game = Game(5, 2, 0, [])
    game.run_game(5)


def solitaire_game() -> None:
    """Run a game with one human player.
    """
    # random.seed(507)
    game = Game(4, 1, 0, [])
    game.run_game(30)


def sample_game() -> None:
    """Run a sample game with one human player, one random player,
    and one smart player.
    """
    # random.seed(1001)
    game = Game(5, 1, 1, [6])
    game.run_game(3)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['run_game'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer'
        ],
    })
    # sample_game()
    # auto_game()
    two_player_game()
    # solitaire_game()
