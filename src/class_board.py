# -*- coding: utf-8 -*-

"""
盤面のクラス
"""

import pandas as pd
import math

## data file path : '..\data\sample_0001.csv'

class Board:

  # 初期化関数
  def __init__(self, file_path = '..\data\sample_2001.csv'):
    # CSVファイルからデータを読み込む
    self.board = pd.read_csv(file_path, header=None)
    self.init_board = self.board.copy()  
    self.size = len(self.board)
    # sizeは整数の2乗である必要がある
    if int(math.sqrt(self.size)) ** 2 != self.size:
      print("Error: board size must be square num ... {}".format(self.size))

    # 候補リストを初期化
    self.cell_candidate_list = {}
    for row in range(self.size):
      for col in range(self.size):
        self.cell_candidate_list[(row, col)] = list(range(1, self.size + 1))
    # 候補リストの初期値を求める
    self.update_all_cell_candidate_list()


  # # CSVファイルから盤面を作成する (使わない)
  # def make_board_from_csv(file_path):
  #   return pd.read_csv(file_path, header=None)

  # 盤面内の全てのセルを0とする(使わないかも)
  def clear(self):
    self.board = pd.DataFrame([[0] * self.size] * self.size)

  # 最初の状態に戻す
  def restart(self):
    self.board = self.init_board.copy()

  # 1つ前の状態に戻す
  # def undo(self):
    # TODO

  # セルに数値を入れる
  def update_cell(self, pos, val):
    row, col = pos
    self.board.loc[row, col] = val

  # 完了判定
  def is_complete(self):
    # TODO
    # 盤面が全て埋まっていて、間違いではない場合、True
    is_allcells_filled = (0 not in self.board.values.flatten().tolist())
    is_wrong_flg = self.is_wrong()

    return is_allcells_filled and is_wrong_flg

  # 間違いかどうか判定
  def is_wrong(self):
    # 列/行/正方形を抽出し、1～self.sizeが重複していないかチェック
    for i in range(self.size * 3):
      mode = i // self.size # 列/行/正方形
      index = i % self.size # 列/行/正方形の番号
      if mode == 0:
        # 全ての列(縦)を抽出
        values = self.board.iloc[:, index].values.tolist()
      elif mode == 1:
        # 全ての行(横)を抽出
        values = self.board.iloc[index, :].values.tolist()
      else: # == 2
        # 全ての正方形を抽出
        sqrt_size = int(math.sqrt(self.size))
        index_x = index % sqrt_size
        index_y = index // sqrt_size
        values = self.board.iloc[ \
          index_y * sqrt_size : (index_y + 1) * sqrt_size, \
          index_x * sqrt_size : (index_x + 1) * sqrt_size \
            ].values.flatten().tolist()

      # 0以外に重複していればバツ
      if values.count(0) + len(set(values)) == len(values):
        return True

    return False
  
  # 特定セルの候補リストを更新する
  def update_cell_candidate_list(self, pos, val = -1):
    # セルに入った値を参考に、候補になる数のリストを更新する
    row, col = pos
    if val == -1:
      val = self.board.iloc[row, col]
    for i in range(self.size):
      # 横
      if val in self.cell_candidate_list[(row, i)]:
        self.cell_candidate_list[(row, i)].remove(val)
      # 縦
      if val in self.cell_candidate_list[(i, col)]:
        self.cell_candidate_list[(i, col)].remove(val)
    # 矩形
    sqrt_size = int(math.sqrt(self.size))
    r = row // sqrt_size
    c = col // sqrt_size
    for i in range(r * sqrt_size, (r + 1) * sqrt_size):
      for j in range(c * sqrt_size, (c + 1) * sqrt_size):
        if val in self.cell_candidate_list[(i, j)]:
          self.cell_candidate_list[(i, j)].remove(val)


  # 全てのセルの候補リストを更新する
  def update_all_cell_candidate_list(self):
    for i in range(self.size):
      for j in range(self.size):
        if self.board.iloc[i, j] != 0:
          self.cell_candidate_list[(i, j)].clear()
          self.update_cell_candidate_list((i, j))
          

    # self.cell_candidate_list[(x, y)]
    # # TODO 縦、横、正方形内を見て、重複している数を除外する
    #     self.cell_candidate_list[(x, y)]

  # # TODO 縦、横、正方形を全部取得する
  # def get_all_groups(self):
  #   for x 

  # # TODO 特定の縦、横、正方形を全部取得する
  # def get_

  def print_cell_candidate_list(self):
    for key, value in self.cell_candidate_list.items():
      print("{}: {}".format(key, value))

  def print_board(self):
    sqrt_size = int(math.sqrt(self.size))
    all_values = self.board.values
    # 横方向の仕切り文字の数
    # size * 2("n ") + sqrt_size * 2("| ") + 1("|")
    sep_char_num = self.size * 2 + sqrt_size * 2 + 1
    for i in range(self.size):
      if i % sqrt_size == 0:
        print("="* sep_char_num)
      # else:
      #   print("-"* sep_char_num)
      row_vals = all_values[i]
      for j in range(len(all_values[i])):
        if j % sqrt_size == 0:
          print("| ", end="")
        if row_vals[j] == 0:
          print("x", end=" ")
        else:
          print(row_vals[j], end=" ")
      print("|")
    print("="* sep_char_num)
