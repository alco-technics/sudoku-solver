# -*- coding: utf-8 -*-

"""
ソルバーのクラス
"""

import numpy as np
import copy
import time
from src.const import Const

class Solver:
  # def __init__(self):
  #   self.board = board

  # 候補リストのうち、1つになった値をセルに入れる
  def update_data_with_candidate_list_cell(self, board):
    # 更新があったかどうか
    update_flg = False
    for key, value in board.candidate_list[Const.CELL_KEY_NAME].items():
      if len(value) == 1:
        update_flg = True
        val = value.pop()
        board.update_cell(key, val)
    return update_flg

  # 特定の縦・横・矩形において、候補リストから各値の出現回数を取得する
  def update_data_with_candidate_list_area(self, board):
    update_flg = False
    # 領域(行・列・矩形)内における各値が入る可能性がある候補セルのリストがただ1つであればそのセルに値を入れる
    for mode, value in board.candidate_list[Const.AREA_KEY_NAME].items():
      for idx, value2 in value.items():
        for val, cells in value2.items():
          if len(cells) == 1:
            update_flg = True
            cell = cells.pop()
            board.update_cell(cell, val)
    return update_flg


    if mode == Const.ROW_KEY_NAME: # 縦
      for row in range(board.size):
        for val in candidate_list[(row, index)]:
          num_list[val - 1] += 1
    elif mode == Const.COLUMN_KEY_NAME: # 横
      for col in range(board.size):
        for val in candidate_list[(index, col)]:
          num_list[val - 1] += 1
    else: # mode == Const.SQUARE_KEY_NAME # 矩形
      sq_num = math.sqrt(board.size)
      sq_x_index = index % sq_num
      sq_y_index = index // sq_num
      for row in range(sq_x_index*sq_num, (sq_x_index+1)*sq_num):
        for col in range(sq_y_index * sq_num, (sq_y_index + 1) * sq_num):
          for val in candidate_list[(row, col)]:
            num_list[val - 1] += 1
    return num_list

  # ロジック3(仮称)
  # 縦・横・矩形を見て、入る数のリストと入る数が全て同じならば、それ以外のその数リストは候補リストから外す。

  # 力技で解く
  # 全パターンから深さ優先探索で正解を探索する
  # TODO あんまりうまくいっていない。。。探索方法を再検討したい
  def depth_first_search(self, board):
    search_result = []  # 探索結果(値を入れたセルを順に格納するリスト)
    search_history = {}  # keys : セル位置, values : 探索済みセルリスト, その時点での候補リストを格納するタプル
    now_candidate_list = copy.deepcopy(board.candidate_list)

    start_time = time.time()
    # 初期値
    prev_pos = (-1, -1)
    search_history[prev_pos] = ([], copy.deepcopy(board.candidate_list))
    cnt_verbose = 0
    while True: # 完了するまで繰り返す
      cnt_verbose = cnt_verbose + 1
      if cnt_verbose % 100 == 0:
        print("{:10d} ({:2d} / {:2d}) search_result ... {}".format(
          cnt_verbose, len(search_result), board.data._values.flatten().tolist().count(0) + len(search_result), search_result))
      empty_cell_list = board.get_empty_cell_list()
      # print("empty_cell_list : {}".format(empty_cell_list))
      np.random.shuffle(empty_cell_list)
      pos = self.get_next_search_cell(empty_cell_list, search_history, prev_pos)
      # if board.is_wrong():
      #   print("WRONG...why??? 03")
      if len(pos) == 0: # 次に探索するセルが見つからない場合、探索結果を1つ戻す
        # 次のセルが見つからないため、最新の探索結果のセルを破棄する
        # print("{} ({}, {}) / search_result (minus) ... {}".format(
        #   board.data._values.flatten().tolist().count(0) + len(search_result),
        #   board.data._values.flatten().tolist().count(0), len(search_result), search_result))
        pos_ = search_result.pop(-1)
        # セルの値を0に戻す
        board.update_cell(pos_, 0)
        # 探索履歴を削除する
        search_history.pop(pos_)
        # 1つ前の結果を取り出す
        prev_pos = copy.deepcopy(search_result[-1])
        # 候補リストを元に戻す
        board.candidate_list = copy.deepcopy(search_history[prev_pos][1])
        # print("{} ... {}".format(prev_pos, search_history[prev_pos][0]))
      else:
        # 探索履歴に追加する
        search_history[prev_pos][0].append(pos)
        # 選んだセルに値を入れて検証し、探索結果を更新する
        # if board.is_wrong():
        #   print("WRONG...why??? 01")
        update_flg = self.verify_update_board(board, pos)

        if update_flg: # 更新された
          # if board.is_wrong():
          #   print("WRONG...why??? 02")
          prev_pos = copy.deepcopy(pos)
          search_result.append(pos)
          search_history[pos] = ([], copy.deepcopy(board.candidate_list))
          # print("{} ({}, {}) / search_result (plus) ... {}".format(
          #   board.data._values.flatten().tolist().count(0) + len(search_result),
          #   board.data._values.flatten().tolist().count(0), len(search_result), search_result))

      if board.is_complete(): # 完了した
        end_time = time.time()
        print("Elapsed time[sec] : {:3f}".format(end_time - start_time))
        break

  # ランダムに空いているセルを選択する
  # TODO ランダムに選ぶのが微妙な気がする
  def get_next_search_cell(self, empty_cell_list, search_history, prev_pos):
    for pos in empty_cell_list:
      if pos not in search_history[prev_pos][0]: # すでに探索済みのセルでない
        return pos
    return ()

  # 探索結果を更新する
  def verify_update_board(self, board, pos):
    # セルに値を入れて検証する
    num_list = copy.deepcopy(board.candidate_list[Const.CELL_KEY_NAME][pos])
    np.random.shuffle(num_list)
    for val in num_list:
      board.update_cell(pos, val)
      prev_candidate_list = copy.deepcopy(board.candidate_list)
      # 候補リストを更新
      board.update_candidate_list(pos, val)

      # 検証
      if board.is_wrong(): # 間違い
        board.update_cell(pos, 0)
        board.candidate_list = copy.deepcopy(prev_candidate_list)
      else: # 間違いでない
        return True

    return False





