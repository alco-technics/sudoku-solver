# -*- coding: utf-8 -*-

"""
メインファイル
"""

import class_board

if __name__ == "__main__":

  board = class_board.Board('..\data\sample_0001.csv')


  print("board.board ... \n{}".format(board.board))
  print("board.is_complete() : {}".format(board.is_complete()))
  print("board.is_wrong() : {}".format(board.is_wrong()))





