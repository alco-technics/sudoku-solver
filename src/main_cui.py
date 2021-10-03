# -*- coding: utf-8 -*-

"""
メインファイル
"""

import class_board
import class_solver
from const import Const

import time

if __name__ == "__main__":
  start_time = time.time()

  # インスタンス生成
  board = class_board.Board(file_path = '../data/sample_4006.csv')
  solver = class_solver.Solver()

  print("===== INIT =====")
  print(board.print_board_data())
  print("================")

  #
  solver.solve(board)

  end_time = time.time()
  print("Elapsed time [sec.] : {}".format(end_time - start_time))
  # print("Complete? ... {}".format(board.is_complete()))
  # print("===== FINISH =====")
  board.print_board_data()
  # board.print_candidate_list()





