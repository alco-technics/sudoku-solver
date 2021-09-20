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
  board = class_board.Board(file_path = '../data/sample_0001.csv')
  solver = class_solver.Solver()

  print("===== INIT =====")
  print(board.print_board())
  print("================")

  #
  while True:
    update_flg_1 = solver.update_data_with_candidate_list_cell(board)
    update_flg_2 = solver.update_data_with_candidate_list_area(board)

    board.update_all_candidate_list()

    if not(update_flg_1 or update_flg_2):
      print("===== LOOP END =====")
      break

  end_time = time.time()
  print("Elapsed time [sec.] : {}".format(end_time - start_time))
  print("Complete? ... {}".format(board.is_complete()))
  print("===== FINISH =====")
  board.print_board()
  board.print_candidate_list()





