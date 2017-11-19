#!/usr/bin/env python
# Akash Sheth, Dheeraj Singh, Chetan Patil, 2017 (absheth-cpatil-dhsingh-a2)
# Parakeet --> 1
# Nighthawk --> 3
# Blue Jay --> 3
# Kingfisher  --> 5
# Quetzal --> 9
#
# Evaluation Reference: The evaluation function that we used is given the book Norvig and Russel which weighs a particular moves
# on the number of pieces avaliable.
# It's the weighted linear function that sums across all the types of peices
#
#
#
#
#

import sys
import operator

player = sys.argv[1]
inputboard = sys.argv[2]
inputtime = int(sys.argv[3])

depth = 3


def convert_string_to_list(state):
    state = list(state)
    return [state[i:i+8] for i in range(0, len(state), 8)]


def convert_list_to_string(state):
    return ''.join([j for i in state for j in i])


def get_position(state, piece):
    pos = []
    for k, i in enumerate(state):
        for p, j in enumerate(i):
            if j == piece:
                temp = [k, p]
                pos.append(temp)
    return pos


initial_board = inputboard
white_pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
black_pieces = ['r', 'n', 'b', 'q', 'k', 'p']
directions = [3, 4, 1, 2]  # 1 = up, 2 = right, 3 = down. 4 = left


def newcopy(board):
    newboard = []
    for i in range(0, len(board)):
        newboard.append(board[i])
    return newboard


def newcopy1(board):
    newboard = []
    for i in range(0, len(board)):
        newboard1 = []
        for j in range(0, len(board)):

            newboard1.append(board[i][j])
        newboard.append(newboard1)
    return newboard


def find_pos(string, character):
    return [i + 1 for i, ch in enumerate(string) if ch == character]


# Nighthawk move
def nighthawk_move(state, local_player):
    next_moves = []
    letter, opponent = ('N', list('.prnbqk')) if local_player == 'w' else ('n', list('.PRNBQK'))
    pos = get_position(state, letter)

    for i in pos:
        temp_state = newcopy1(state)
        if 0 <= i[0]+2 < 8 and 0 <= i[1]+1 < 8 and temp_state[i[0]+2][i[1]+1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0] + 2][i[1] + 1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]+2 < 8 and 0 <= i[1]-1 < 8 and temp_state[i[0]+2][i[1]-1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0] + 2][i[1] - 1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]+1 < 8 and 0 <= i[1]+2 < 8 and temp_state[i[0]+1][i[1]+2] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0] + 1][i[1] + 2] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]+1 < 8 and 0 <= i[1]-2 < 8 and temp_state[i[0]+1][i[1]-2] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0] + 1][i[1] - 2] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]-2 < 8 and 0 <= i[1]-1 < 8 and temp_state[i[0]-2][i[1]-1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-2][i[1]-1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]-2 < 8 and 0 <= i[1]+1 < 8 and temp_state[i[0]-2][i[1]+1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-2][i[1]+1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]-1 < 8 and 0 <= i[1]+2 < 8 and temp_state[i[0]-1][i[1]+2] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]+2] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if 0 <= i[0]-1 < 8 and 0 <= i[1]-2 < 8 and temp_state[i[0]-1][i[1]-2] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]-2] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

    return next_moves


# pawn move
def pawn_move(state, local_player):
    next_moves = []
    letter, opponent = ('P', list('prnbqk')) if local_player == 'w' else ('p', list('PRNBQK'))
    pos = get_position(state, letter)
    for i in pos:
        temp_state = newcopy1(state)
        if letter == 'P' and i[0] == 1 and temp_state[i[0]+2][i[1]] == '.' and temp_state[i[0]+1][i[1]] == '.':
            temp_state[i[0]][i[1]], temp_state[i[0]+2][i[1]] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'P' and 1 < i[0]+1 < 8 and temp_state[i[0]+1][i[1]] == '.':
            temp_state[i[0]][i[1]], temp_state[i[0]+1][i[1]] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and i[0] == 6 and temp_state[i[0]-2][i[1]] == '.' and temp_state[i[0]-1][i[1]] == '.':
            temp_state[i[0]][i[1]], temp_state[i[0]-2][i[1]] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and 0 <= i[0]-1 < 6 and temp_state[i[0]-1][i[1]] == '.':
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'P' and 1 < i[0]+1 < 8 and 0 <= i[1]+1 < 8 and temp_state[i[0]+1][i[1]+1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]+1][i[1]+1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'P' and 1 < i[0]+1 < 8 and 0 <= i[1]-1 < 8 and temp_state[i[0]+1][i[1]-1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]+1][i[1]-1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and 0 <= i[0]-1 < 6 and 0 <= i[1]+1 < 8 and temp_state[i[0]-1][i[1]+1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]+1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and 0 <= i[0]-1 < 6 and 0 <= i[1]-1 < 8 and temp_state[i[0]-1][i[1]-1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]-1] = '.', letter
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'P' and i[0]+1 == 7 and temp_state[i[0]+1][i[1]] == '.':
            temp_state[i[0]][i[1]], temp_state[i[0]+1][i[1]] = '.', 'Q'
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and i[0]-1 == 0 and temp_state[i[0]-1][i[1]] == '.':
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]] = '.', 'q'
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'P' and i[0]+1 == 7 and temp_state[i[0]+1][i[1]+1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]+1][i[1]] = '.', 'Q'
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and i[0]-1 == 0 and temp_state[i[0]-1][i[1]+1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]] = '.', 'q'
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'P' and i[0]+1 == 7 and temp_state[i[0]+1][i[1]-1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]+1][i[1]] = '.', 'Q'
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

        if letter == 'p' and i[0]-1 == 0 and temp_state[i[0]-1][i[1]-1] in opponent:
            temp_state[i[0]][i[1]], temp_state[i[0]-1][i[1]] = '.', 'q'
            next_moves.append(convert_list_to_string(temp_state))
            temp_state = newcopy1(state)

    return next_moves


def eval_board(state):

    # weight_king = 10
    # weight_queen = 9
    # weight_rook = 5
    # weight_bishop = 3
    # weight_knight = 3
    # weight_pawn = 1
    weight_kingsfifher = 1
    weight_quetzal = 5
    weight_robin = 9
    weight_bluejay = 3
    weight_nighthawk = 3
    weight_parakeet = 10
    # score_white = weight_pawn*state.count('P') + weight_knight*state.count('N') + weight_bishop*state.count('B') + weight_rook*state.count('R') + weight_queen*state.count('Q') + weight_king*state.count('K')
    # score_black = weight_pawn*state.count('p') + weight_knight*state.count('n') + weight_bishop*state.count('b') + weight_rook*state.count('r') + weight_queen*state.count('q') + weight_king*state.count('k')
    p_value = weight_parakeet*state.count('P') + weight_parakeet*state.count('p')
    n_value = weight_nighthawk*state.count('N') + weight_nighthawk*state.count('n')
    b_value = weight_bluejay*state.count('B') + weight_bluejay*state.count('b')
    r_value = weight_robin*state.count('R') + weight_robin*state.count('r')
    q_value = weight_quetzal*state.count('Q') + weight_quetzal*state.count('q')
    k_value = weight_kingsfifher*state.count('K') + weight_kingsfifher*state.count('k')
    # score_white = weight_pawn*state.count('P') + weight_knight*state.count('N') + weight_bishop*state.count('B') + weight_rook*state.count('R') + weight_queen*state.count('Q') + weight_king*state.count('K')
    # score_black = weight_pawn*state.count('p') + weight_knight*state.count('n') + weight_bishop*state.count('b') + weight_rook*state.count('r') + weight_queen*state.count('q') + weight_king*state.count('k')
    return p_value + n_value + b_value + r_value + q_value + k_value
    # return score_white-score_black if player == 'w' else score_black-score_white


def get_up_down_left_right_moves(state, piece):
    local_state = list(state)
    all_moves = []
    king_move = False
    for old_index in find_pos(local_state, piece):
        bounds_dict = {}
        bounds_dict[1] = quotient = (old_index) / 8  # upper_bound
        bounds_dict[2] = ((quotient * 8) + 8 - old_index) % 8  # right_bound
        bounds_dict[3] = (64 - old_index) / 8  # lower_bound
        bounds_dict[4] = (old_index - 1 - (quotient * 8) + 8) % 8  # left_bound
        for direction in directions:
            for x in range(1, bounds_dict[direction] + 1):
                if king_move:
                    break
                opp_replace = False
                temp = newcopy(initial_board)

                if direction == 1:
                    new_index = (old_index - x * 8) - 1
                elif direction == 2:
                    new_index = old_index - 1 + x
                elif direction == 3:
                    new_index = (old_index + x * 8) - 1
                elif direction == 4:
                    new_index = old_index - 1 - x
                if new_index < 0:
                    break
                if piece.istitle():
                    if temp[new_index] in white_pieces:
                        break
                    else:
                        if temp[new_index] in black_pieces:
                            opp_replace = True
                        temp[old_index-1], temp[new_index] = '.', piece
                        if ''.join(temp) not in all_generated_states.keys():
                            all_generated_states.update({''.join(temp): "YES"})
                            all_moves.append(''.join(temp))
                        else:
                            continue
                        if piece == 'K':
                            king_move = True
                        if opp_replace:
                            break
                else:
                    if temp[new_index] in black_pieces:
                        break
                    else:
                        if temp[new_index] in white_pieces:
                            opp_replace = True
                        temp[old_index-1], temp[new_index] = '.', piece
                        if ''.join(temp) not in all_generated_states.keys():
                            all_generated_states.update({''.join(temp): "YES"})
                            all_moves.append(''.join(temp))
                        else:
                            continue
                        if piece == 'k':
                            king_move = True
                        if opp_replace:
                            break
            king_move = False
    return all_moves


def get_diagonal_moves(state, piece):
    local_state = list(state)
    all_moves = []
    king_move = False
    for old_index in find_pos(local_state, piece):
        bounds_dict_test = {}
        bounds_dict_test[1] = quotient = (old_index) / 8  # LEFT UP
        bounds_dict_test[2] = (old_index - 1 - (quotient * 8) + 8) % 8  # LEFT DOWN
        bounds_dict_test[3] = (64 - old_index) / 8  # RIGHT DOWN
        bounds_dict_test[4] = ((quotient * 8) + 8 - old_index) % 8  # RIGHT UP

        for direction in directions:
            for x in range(1, bounds_dict_test[direction] + 1):
                if king_move:
                    break
                opp_replace = False
                temp = newcopy(initial_board)
                if direction == 1:
                    new_index = old_index - 1 - (x*9)
                    if (new_index+1) % 8 == 0:
                        break
                elif direction == 3:
                    new_index = old_index - 1 + (x*9)
                    if new_index % 8 == 0:
                        break
                elif direction == 2:
                    new_index = old_index - 1 + (x*7)
                elif direction == 4:
                    new_index = old_index - 1 - (x*7)
                if new_index < 0 or new_index > 63:
                    break
                if piece.istitle():
                    if temp[new_index] in white_pieces:
                        break
                    else:
                        if temp[new_index] in black_pieces:
                            opp_replace = True
                        temp[old_index-1], temp[new_index] = '.', piece
                        if ''.join(temp) not in all_generated_states.keys():
                            all_generated_states.update({''.join(temp): "YES"})
                            all_moves.append(''.join(temp))
                        else:
                            continue
                        if piece == 'K':
                            king_move = True
                        if opp_replace:
                            break
                else:
                    if temp[new_index] in black_pieces:
                        break
                    else:
                        if temp[new_index] in white_pieces:
                            opp_replace = True
                        temp[old_index-1], temp[new_index] = '.', piece
                        if ''.join(temp) not in all_generated_states.keys():
                            all_generated_states.update({''.join(temp): "YES"})
                            all_moves.append(''.join(temp))
                        else:
                            continue
                        if piece == 'k':
                            king_move = True
                        if opp_replace:
                            break
            king_move = False
    return all_moves


def next_piece_move(state, piece, local_player):
    append_move = []
    if piece == 'R' or piece == 'r' or piece == 'Q' or piece == 'q' or piece == 'K' or piece == 'k':
        # print "UP - RIGHT - DOWN - LEFT"
        append_move.extend(get_up_down_left_right_moves(state, piece))
    if piece == 'B' or piece == 'b' or piece == 'Q' or piece == 'q' or piece == 'K' or piece == 'k':
        # print "DIAGONAL"
        append_move.extend(get_diagonal_moves(state, piece))
    if piece == 'N' or piece == 'n':
        append_move.extend(nighthawk_move(convert_string_to_list(state), local_player))
    if piece == 'P' or piece == 'p':
        append_move.extend(pawn_move(convert_string_to_list(state), local_player))
    return append_move


def find_successors(state, local_player):
    all_moves = []
    if local_player == 'w':
        all_moves.extend([next_piece_move(state, piece, local_player) for piece in white_pieces])
    else:
        all_moves.extend([next_piece_move(state, piece, local_player) for piece in black_pieces])

    return all_moves


def print_dictionary():
    for key in master_moves_dictionary.keys():
        print "key -->", key, " || Value --> ", master_moves_dictionary[key]


def add_successors_in_master(state, all_successors, local_depth):
    for successors in all_successors:
        if len(successors) == 0:
            continue
        for successor in successors:
            master_moves_dictionary.update({''.join(successor): 0})


def max_value(state, local_depth, alpha, beta, local_player, global_state):
    if local_depth == depth:
        return (eval_board(state), global_state)
    utility_value = -sys.maxsize
    max_successors = find_successors(state, local_player)
    if local_depth == 0:
        add_successors_in_master(state, max_successors, local_depth)

    max_value_list = []
    for successors in max_successors:
        if len(successors) == 0:
            continue
        for successor in successors:
            x = ""
            if local_depth == 0:
                x = successor
            else:
                x = global_state

            value = min_value(successor, local_depth+1, alpha, beta, 'b' if local_player == 'w' else 'w', x)
            if local_depth == 0:
                master_moves_dictionary.update({successor: value[0] if value[0] > master_moves_dictionary[successor] else master_moves_dictionary[successor]})
            else:
                master_moves_dictionary.update({global_state: value[0] if value[0] > master_moves_dictionary[global_state] else master_moves_dictionary[global_state]})

            if value[0] > utility_value:
                utility_value = value[0]
            if value[0] > beta:
                return (utility_value, state)
            if value[0] > alpha:
                alpha = value[0]
            max_value_list.append(value)
    if local_depth == 0:
        return max(master_moves_dictionary.iteritems(), key=operator.itemgetter(1))[0]
    else:
        return max(max_value_list if len(max_value_list) != 0 else [(eval_board(state), global_state)], key=lambda item: item[0])


def min_value(state, local_depth, alpha, beta, local_player, global_state):
    if local_depth == depth:
        return (eval_board(state), global_state)
    utility_value = sys.maxsize
    min_successors = find_successors(state, local_player)
    min_value_list = []
    for successors in min_successors:
        if len(successors) == 0:
            continue
        for successor in successors:
            value = max_value(successor, local_depth+1, alpha, beta, 'w' if local_player == 'b' else 'b', global_state)

            master_moves_dictionary.update({global_state: value[0] if value[0] > master_moves_dictionary[global_state] else master_moves_dictionary[global_state]})
            if value[0] < utility_value:
                utility_value = value[0]
            if value[0] <= alpha:
                return (utility_value, state)
            if value[0] < beta:
                beta = value[0]
            min_value_list.append(value)
    return min(min_value_list if len(min_value_list) != 0 else [(eval_board(state), global_state)], key=lambda item: item[0])


def min_max_decision(initial_board):
    global master_moves_dictionary
    global current_path
    global all_generated_states
    alpha = -sys.maxsize
    beta = sys.maxsize
    intial_depth = 0
    value = max_value(initial_board, intial_depth, alpha, beta, player, initial_board)
    print value


master_moves_dictionary = {}
all_generated_states = {}
current_path = []
min_max_decision(initial_board)
