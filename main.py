'''
    Generates legal moves from a chess position and saves them to a file.
    Copyright (C) 2022  Pyry Vartiovaara

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import chess


def write_move_history(board, f):
	board_copy = board.copy()
	line = ''

	while True:
		try:
			move = board_copy.pop()
			line = move.uci() + ' ' + line
		except IndexError:
			line = line + '\n'
			break
	f.write(line)

# board: instance of chess.Board()
# depth: depth to search to
# f: file open to which to save the perft data
# return_split: whether or not to return the perft data
#
# Return value:
# (nodes, [(nodes, move), (...), ....])
def search(board, depth, f, return_split):
	if (depth == 0 or board.outcome() != None and f != None):
		write_move_history(board, f)
		return 1
	
	moves = board.legal_moves
	move_counts = []

	search_result = 0
	for move in moves:
		board_copy = board.copy()
		board_copy.push(move)
		result = search(board_copy, depth-1, f, False)
		search_result += result
		if (return_split):
			move_counts.append(tuple([move, result]))
		board_copy = board
	
	if return_split:
		return (search_result, move_counts)
	else:
		return search_result
	

f = open('history', 'w+')

fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
#fen = 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8'
#fen = 'rnbq1k1r/pp1Pbppp/2p5/8/2B5/8/PPP1NnPP/RNBQK2R w KQ - 1 8'

depth = 4

board = chess.Board(fen=fen)
print(board)
perft_result = search(board, depth, f, True)

f.close()

print(perft_result[0])
for move in perft_result[1]:
	print(move[0].uci(), (move[1]))
