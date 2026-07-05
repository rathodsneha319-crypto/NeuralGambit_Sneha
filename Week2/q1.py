import json
import copy  # use it for deepcopy if needed
import math  # for math.inf
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
                    level=logging.INFO)

# Global variables in which you need to store player strategies (this is data structure that'll be used for evaluation)
# Mapping from histories (str) to probability distribution over actions
strategy_dict_x = {}
strategy_dict_o = {}


class History:
    def __init__(self, history=None):
        """
        # self.history : Eg: [0, 4, 2, 5]
            keeps track of sequence of actions played since the beginning of the game.
            Each action is an integer between 0-8 representing the square in which the move will be played as shown
            below.
              ___ ___ ____
             |_0_|_1_|_2_|
             |_3_|_4_|_5_|
             |_6_|_7_|_8_|

        # self.board
            empty squares are represented using '0' and occupied squares are either 'x' or 'o'.
            Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
            for board
              ___ ___ ____
             |_x_|___|_x_|
             |___|_o_|_o_|
             |___|___|___|

        # self.player: 'x' or 'o'
            Player whose turn it is at the current history/board

        :param history: list keeps track of sequence of actions played since the beginning of the game.
        """
        if history is not None:
            self.history = history
            self.board = self.get_board()
        else:
            self.history = []
            self.board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        self.player = self.current_player()

    def current_player(self):
        """ Player function
        Get player whose turn it is at the current history/board
        :return: 'x' or 'o' or None
        """
        total_num_moves = len(self.history)
        if total_num_moves < 9:
            if total_num_moves % 2 == 0:
                return 'x'
            else:
                return 'o'
        else:
            return None

    def get_board(self):
        """ Play out the current self.history and get the board corresponding to the history in self.board.

        :return: list Eg: ['x', '0', 'x', '0', 'o', 'o', '0', '0', '0']
        """
        board = ['0', '0', '0', '0', '0', '0', '0', '0', '0']
        for i in range(len(self.history)):
            if i % 2 == 0:
                board[self.history[i]] = 'x'
            else:
                board[self.history[i]] = 'o'
        return board

    def get_winner(self):
        """ Helper: returns 'x' or 'o' if that player has three in a row, else None. """
        b = self.board
        lines = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
                 (0, 3, 6), (1, 4, 7), (2, 5, 8),
                 (0, 4, 8), (2, 4, 6)]
        for i, j, k in lines:
            if b[i] != '0' and b[i] == b[j] == b[k]:
                return b[i]
        return None

    def is_win(self):
        # check if the board position is a win for either players
        return self.get_winner() is not None

    def is_draw(self):
        # check if the board position is a draw
        return self.get_winner() is None and '0' not in self.board

    def get_valid_actions(self):
        # get the empty squares from the board
        return [i for i in range(9) if self.board[i] == '0']

    def is_terminal_history(self):
        # check if the history is a terminal history
        return self.is_win() or self.is_draw()

    def get_utility_given_terminal_history(self):
        winner = self.get_winner()
        if winner == 'x':
            return 1
        elif winner == 'o':
            return -1
        else:
            return 0

    def update_history(self, action):
        # In case you need to create a deepcopy and update the history obj to get the next history object.
        return History(history=self.history + [action])


def backward_induction(history_obj):
    """
    :param history_obj: Histroy class object
    :return: best achievable utility (float) for th current history_obj
    """
    global strategy_dict_x, strategy_dict_o

    # Base case: terminal history, utility is just read off the board.
    if history_obj.is_terminal_history():
        return history_obj.get_utility_given_terminal_history()

    player = history_obj.player
    valid_actions = history_obj.get_valid_actions()

    # Recurse on every child history to get its backward-induction value.
    action_values = {}
    for action in valid_actions:
        child = history_obj.update_history(action)
        action_values[action] = backward_induction(child)

    # 'x' maximizes utility (utility is defined w.r.t. x), 'o' minimizes it.
    if player == 'x':
        best_value = max(action_values.values())
    else:
        best_value = min(action_values.values())

    # Pick (any) one of the optimal actions -> deterministic SPE strategy.
    best_action = min(a for a, v in action_values.items() if v == best_value)

    strategy = {str(a): 0.0 for a in range(9)}
    strategy[str(best_action)] = 1.0

    key = ''.join(str(a) for a in history_obj.history)
    if player == 'x':
        strategy_dict_x[key] = strategy
    else:
        strategy_dict_o[key] = strategy

    return best_value


def solve_tictactoe():
    backward_induction(History())
    with open('./policy_x.json', 'w') as f:
        json.dump(strategy_dict_x, f)
    with open('./policy_o.json', 'w') as f:
        json.dump(strategy_dict_o, f)
    return strategy_dict_x, strategy_dict_o


if __name__ == "__main__":
    logging.info("Start")
    solve_tictactoe()
    logging.info("End")
