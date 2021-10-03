# -*- coding: utf-8 -*-

"""
ソルバーのクラス
"""

import numpy as np
import copy
import time
from src.const import Const

class Solver:

  ## public function ##

  def __init__(self):
    # self.board = board
    self.select_result_log = []

  # メイン関数
  def solve(self, board):
    while True:
      # ロジカルに進められるルーティン
      update_flg = self.update_routine_logical(board)

      if board.is_complete():
        print("===== COMPLETE! =====")
        break

      if not(update_flg):
        # 現状のデータをダンプする
        board.store_board_data()
        # 探索するセルを選択する
        select_result = self.select_search_cell(board)
        select_pos, select_val = select_result
        # 探索履歴を保持する
        self.select_result_log.append(select_result)
        board.update_cell(select_pos, select_val)
        board.update_candidate_list(select_pos, select_val)

      if board.is_wrong():
        board.restore_board_data()
        select_result = self.select_result_log.pop()
        select_pos, select_val = select_result
        # 候補リストから探索した結果を除外する
        board.remove_from_candidate_list(select_pos, select_val)


  ## private function ##

  # 論理的な手法で更新するルーチン
  def update_routine_logical(self, board):
    update_flg_1 = self.update_data_with_candidate_list_cell(board)
    update_flg_2 = self.update_data_with_candidate_list_area(board)

    update_flg_3 = board.update_all_candidate_list()

    if not(update_flg_1 or update_flg_2 or update_flg_3):
      update_flg_4 = board.update_candidate_list_2()
      if not(update_flg_4):
        return False

    return True

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
      pos = self.get_next_search_cell_randomly(empty_cell_list, search_history, prev_pos)
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
  def get_next_search_cell_randomly(self, empty_cell_list, search_history, prev_pos):
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

  # 一番候補が少ない探索するセルを求める。
  def select_search_cell(self, board):
    candidate_list_cell = board.candidate_list[Const.CELL_KEY_NAME]
    min_len_nums = board.size
    # 候補がなるべく少ないセルを選びたい
    cell_list = []
    for cell, nums in candidate_list_cell.items():
      len_nums = len(nums)
      if len_nums == 0:
        continue
      if min_len_nums > len_nums:
        min_len_nums = len_nums
        cell_list.clear()
        cell_list.append(cell)
      elif min_len_nums == len_nums:
        cell_list.append(cell)
    # np.random.shuffle(cell_list)
    # TODO もう少し細かく探索セルを決めたいかも。
    # 候補が少ないセルのうち、他の候補から決定できる個数が多いものを選びたい
    cell = cell_list[np.random.choice(len(cell_list))]
    val = candidate_list_cell[cell][np.random.choice(min_len_nums)]
    return cell, val







