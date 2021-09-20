# -*- coding: utf-8 -*-

"""
盤面のクラス
"""

import pandas as pd
import math
import copy

from src.const import Const

## data file path : '..\data\sample_0001.csv'

class Board:

  # 初期化関数
  def __init__(self, file_path):
    # CSVファイルからデータを読み込む
    self.data = pd.read_csv(file_path, header=None)
    self.init_data = copy.deepcopy(self.data)
    self.size = len(self.data)

    # sizeは整数の2乗である必要がある
    if int(math.sqrt(self.size)) ** 2 != self.size:
      print("Error: board size must be square num ... {}".format(self.size))

    self.candidate_list = {}  # 候補リスト
    # セル内に入る数値の候補リスト
    self.candidate_list[Const.CELL_KEY_NAME] = \
      {(row, col): list(range(1, self.size + 1)) for row in range(self.size) for col in range(self.size)}

    # 候補リストの初期値を求める
    self.update_all_candidate_list()
    # 候補リストを表示する
    self.print_candidate_list()

    self.candidate_list_cell_dump = {} # 候補リストをダンプする


  # # CSVファイルから盤面を作成する (使わない)
  # def make_board_from_csv(file_path):
  #   return pd.read_csv(file_path, header=None)

  # 盤面内の全てのセルを0とする(使わないかも)
  def clear(self):
    self.data = pd.DataFrame([[0] * self.size] * self.size)

  # 最初の状態に戻す
  def restart(self):
    self.data = copy.deepcopy(self.init_data)

  # 1つ前の状態に戻す
  # def undo(self):
    # TODO

  # セルに数値を入れる
  def update_cell(self, pos, val):
    row, col = pos
    self.data.loc[row, col] = val

  # 完了判定
  def is_complete(self):
    # TODO
    # 盤面が全て埋まっていて、間違いではない場合、True
    flg_all_filled = (0 not in self.data.values.flatten().tolist())
    flg_wrong = self.is_wrong()

    return flg_all_filled and flg_wrong

  # 間違いかどうか判定
  def is_wrong(self):
    # セルが埋まっていない、かつ候補リストが空のセルがあればNG
    for i in range(self.size):
      for j in range(self.size):
        if len(self.candidate_list[Const.CELL_KEY_NAME][(i, j)]) == 0 \
                and self.data.iloc[i, j] == 0:
          return True
    # 列/行/正方形を抽出し、1～self.sizeが重複していないかチェック
    for i in range(self.size * 3):
      mode = i // self.size # 列/行/正方形
      index = i % self.size # 列/行/正方形の番号
      if mode == 0:
        # 全ての列(縦)を抽出
        values = self.data.iloc[:, index].values.tolist()
      elif mode == 1:
        # 全ての行(横)を抽出
        values = self.data.iloc[index, :].values.tolist()
      else: # == 2
        # 全ての正方形を抽出
        sq_size = int(math.sqrt(self.size))
        index_x = index % sq_size
        index_y = index // sq_size
        values = self.data.iloc[ \
          index_y * sq_size : (index_y + 1) * sq_size, \
          index_x * sq_size : (index_x + 1) * sq_size \
            ].values.flatten().tolist()

      # 0以外に重複していればNGと判定しTrueを返す
      # 0の個数 + 0以外の重複しない個数 = 全体の個数と一致しなければNG
      num_0 = values.count(0)
      temp = list(set(values))
      num_not0 = len(temp) - 1 if 0 in temp else len(temp)
      if num_0 + num_not0 != len(values):
        return True

    return False
  
  # 特定セルの値に対して、関連するセルの候補リストを更新する
  def update_candidate_list(self, pos, val = -1):
    row, col = pos
    val = self.data.iloc[row, col] if val == -1 else val
    sq_size = int(math.sqrt(self.size))
    sq_r, sq_c = [i  // sq_size for i in [row, col]]
    sq_idx = sq_r * sq_size + sq_c
    # セルごとの入る候補リストを更新する
    candidate_list_cell = self.candidate_list[Const.CELL_KEY_NAME]
    # 値が入っている場合、そのセルの候補リストを空にする
    if self.data.iloc[row, col] != 0:
      candidate_list_cell[pos] = []
      # 関連する行、列、矩形内のセルから該当する候補の値を削除する
      for i in range(self.size):
        if val in candidate_list_cell[(row, i)]:  # 横
          candidate_list_cell[(row, i)].remove(val)
        if val in candidate_list_cell[(i, col)]:  # 縦
          candidate_list_cell[(i, col)].remove(val)
      for i in range(sq_r * sq_size, (sq_r + 1) * sq_size): # 矩形
        for j in range(sq_c * sq_size, (sq_c + 1) * sq_size):
          if val in candidate_list_cell[(i, j)]:
            candidate_list_cell[(i, j)].remove(val)

  # 全ての候補リストを更新する
  def update_all_candidate_list(self):
    # セル内の候補リストを更新する
    for i in range(self.size):
      for j in range(self.size):
        if self.data.iloc[i, j] != 0:
          self.candidate_list[Const.CELL_KEY_NAME][(i, j)].clear()
          self.update_candidate_list((i, j))
    # 領域内のセル候補リストを更新する
    self.candidate_list[Const.AREA_KEY_NAME] = self.convert_to_candidate_list_area()

  # 候補リストを表示する
  def print_candidate_list(self):
    for key, value in self.candidate_list[Const.CELL_KEY_NAME].items():
      print("(CELL) pos: {}, cells: {}".format(key, value))
    for key, value in self.candidate_list[Const.AREA_KEY_NAME].items():
      for key2, value2 in value.items():
        for key3, value3 in value2.items():
          print("(AREA) mode: {}, index: {}, val: {}, cells: {}"
                .format(key, key2, key3, value3))


  # 盤面を表示する
  def print_board(self):
    sq_size = int(math.sqrt(self.size))
    all_values = self.data.values
    # 横方向の仕切り文字の数
    # size * 2("n ") + sq_size * 2("| ") + 1("|")
    sep_char_num = self.size * 2 + sq_size * 2 + 1
    for i in range(self.size):
      if i % sq_size == 0:
        print("="* sep_char_num)
      # else:
      #   print("-"* sep_char_num)
      row_values = all_values[i]
      for j in range(len(all_values[i])):
        if j % sq_size == 0:
          print("| ", end="")
        if row_values[j] == 0:
          print("x", end=" ")
        else:
          print(row_values[j], end=" ")
      print("|")
    print("="* sep_char_num)

  # ダンプする
  def save_candidate_list(self, key_str):
    self.candidate_list_dump[key_str] = copy.deepcopy(self.candidate_list)

  # 空いているセル一覧を取り出す
  def get_empty_cell_list(self):
    cell_list = []
    for i in range(self.size):
      for j in range(self.size):
        if self.data.iloc[i, j] == 0:
          cell_list.append((i, j))
    # for key, value in self.candidate_list.items():
    #   if len(value) != 0:
    #     cell_list.append(key)
    return cell_list

  # セルごとの候補リストを変換する
  # 各領域(行・列・矩形)における各値が入る可能性がある候補セルのリストに変換する
  def convert_to_candidate_list_area(self):
    candidate_list_cell = copy.deepcopy(self.candidate_list[Const.CELL_KEY_NAME])
    candidate_list_area = {}
    candidate_list_area[Const.COLUMN_KEY_NAME] = \
      { idx: { val: [] for val in range(1, self.size + 1) } for idx in range(self.size) }
    candidate_list_area[Const.ROW_KEY_NAME] = \
      { idx: { val: [] for val in range(1, self.size + 1) } for idx in range(self.size) }
    candidate_list_area[Const.SQUARE_KEY_NAME] = \
      { idx: { val: [] for val in range(1, self.size + 1) } for idx in range(self.size) }
    sq_size = int(math.sqrt(self.size))
    for pos, nums in candidate_list_cell.items():
      row, col = pos
      sq_idx = (row // sq_size) * sq_size + (col // sq_size)
      for val in nums:
        candidate_list_area[Const.COLUMN_KEY_NAME][row][val].append(pos) # 横
        candidate_list_area[Const.ROW_KEY_NAME][col][val].append(pos)  # 縦
        candidate_list_area[Const.SQUARE_KEY_NAME][sq_idx][val].append(pos)  # 矩形
    return candidate_list_area
