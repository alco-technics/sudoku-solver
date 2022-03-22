# -*- coding: utf-8 -*-

"""
盤面のクラス
"""

import pandas as pd
import math
import copy

from const import Const

## data file path : '..\data\sample_0001.csv'

class Board:

  ## public function ##

  # 初期化関数
  def __init__(self, file_path=None, data=None, size=9):
    if type(data) == pd.DataFrame:
      # dataが指定されればそれを使う
      self.data = copy.deepcopy(data)
      self.size = len(self.data)
    elif file_path != None:
      # CSVファイルからデータを読み込む
      self.data = pd.read_csv(file_path, header=None)
      self.size = len(self.data)
    else:
      self.size = size
      self.clear()
    self.init_data = copy.deepcopy(self.data)

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
    # self.print_candidate_list()

    # ダンプするための配列
    self.stored_data = [] # データ
    self.stored_candidate_list = [] # 候補リスト

  # # CSVファイルから盤面を作成する (使わない)
  # def make_board_from_csv(file_path):
  #   return pd.read_csv(file_path, header=None)

  # 盤面内の全てのセルを0とする(使わないかも)
  def clear(self):
    self.data = pd.DataFrame([[0] * self.size] * self.size)

  # 最初の状態に戻す(使わないかも)
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
    # 盤面が全て埋まっていて、間違いではない場合、True
    flg_all_filled = (0 not in self.data.values.flatten().tolist())
    flg_wrong = self.is_wrong()

    return flg_all_filled and not(flg_wrong)

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
  def update_candidate_list(self, pos, val = -1, flg_area_update = True):
    update_flg = False
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
          update_flg = True
          candidate_list_cell[(row, i)].remove(val)
        if val in candidate_list_cell[(i, col)]:  # 縦
          update_flg = True
          candidate_list_cell[(i, col)].remove(val)
      for i in range(sq_r * sq_size, (sq_r + 1) * sq_size): # 矩形
        for j in range(sq_c * sq_size, (sq_c + 1) * sq_size):
          if val in candidate_list_cell[(i, j)]:
            update_flg = True
            candidate_list_cell[(i, j)].remove(val)
    if flg_area_update:
      self.candidate_list[Const.AREA_KEY_NAME] = self.convert_to_candidate_list_area()
    return update_flg

  # 候補リストから除外する
  def remove_val_from_candidate_list_cell(self, cell, val):
    if val in self.candidate_list[Const.CELL_KEY_NAME][cell]:
      self.candidate_list[Const.CELL_KEY_NAME][cell].remove(val)

  # 全ての候補リストを更新する
  def update_all_candidate_list(self):
    update_flg = False
    # セル内の候補リストを更新する
    for i in range(self.size):
      for j in range(self.size):
        if self.data.iloc[i, j] != 0:
          self.candidate_list[Const.CELL_KEY_NAME][(i, j)].clear()
          update_flg = self.update_candidate_list((i, j), flg_area_update=False)
    # 領域内のセル候補リストを更新する
    self.candidate_list[Const.AREA_KEY_NAME] = self.convert_to_candidate_list_area()
    return update_flg


  # 候補リストを更新する
  # 各領域の候補の値が他の1つの領域内に全てある場合、その他の領域の他の候補は削除する
  def update_candidate_list_2(self):
    update_flg = False
    candidate_list_cell = self.candidate_list[Const.CELL_KEY_NAME]
    candidate_list_area = self.candidate_list[Const.AREA_KEY_NAME]
    candidate_list_area_col = candidate_list_area[Const.COLUMN_KEY_NAME]
    candidate_list_area_row = candidate_list_area[Const.ROW_KEY_NAME]
    candidate_list_area_square = candidate_list_area[Const.SQUARE_KEY_NAME]
    # 横や縦のセル候補リストが全て同じ矩形内であれば、その矩形内の他の候補は削除する
    for col, values in candidate_list_area_col.items():
      for val, cells in values.items():
        sq_idx_list = [self.get_square_index(cell) for cell in cells]
        if len(list(set(sq_idx_list))) == 1:
          for cell in candidate_list_area_square[sq_idx_list[0]][val]:
            if cell not in cells and val in candidate_list_cell[cell]:
              update_flg = True
              candidate_list_cell[cell].remove(val)
    for row, values in candidate_list_area_row.items():
      for val, cells in values.items():
        sq_idx_list = [self.get_square_index(cell) for cell in cells]
        if len(list(set(sq_idx_list))) == 1:
          for cell in candidate_list_area_square[sq_idx_list[0]][val]:
            if cell not in cells and val in candidate_list_cell[cell]:
              update_flg = True
              candidate_list_cell[cell].remove(val)
    # 矩形のセル候補リストが全て同じ行や列内であれば、その行や列内の他の候補は削除する
    for sq, values in candidate_list_area_square.items():
      for val, cells in values.items():
        row_idx_list = []
        col_idx_list = []
        for cell in cells:
          col_idx_list.append(cell[0])
          row_idx_list.append(cell[1])
        if len(list(set(row_idx_list))) == 1:
          for cell in candidate_list_area_row[row_idx_list[0]][val]:
            if cell not in cells and val in candidate_list_cell[cell]:
              update_flg = True
              candidate_list_cell[cell].remove(val)
        if len(list(set(col_idx_list))) == 1:
          for cell in candidate_list_area_col[col_idx_list[0]][val]:
            if cell not in cells and val in candidate_list_cell[cell]:
              update_flg = True
              candidate_list_cell[cell].remove(val)
    if update_flg:
      candidate_list_area = self.convert_to_candidate_list_area()
    return update_flg

  # 候補リストを更新する
  # 各領域における各値ごとのセル候補リストがセルの数と値の数が一致する場合
  # それ以外は候補から外す。
  # TODO

  # 候補リストを表示する
  def print_candidate_list(self, data_idx = -1):
    if data_idx < 0:
      all_values = self.candidate_list
    else:
      all_values = self.stored_candidate_list[data_idx]
    for key, value in all_values[Const.CELL_KEY_NAME].items():
      print("(CELL) pos: {}, cells: {}".format(key, value))
    for key, value in all_values[Const.AREA_KEY_NAME].items():
      for key2, value2 in value.items():
        for key3, value3 in value2.items():
          print("(AREA) mode: {}, index: {}, val: {}, cells: {}"
                .format(key, key2, key3, value3))

  # 盤面を表示する
  def print_board_data(self, data_idx = -1):
    if data_idx < 0:
      all_values = self.data.values
    else:
      all_values = self.stored_data[data_idx].values
    sq_size = int(math.sqrt(self.size))
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


  # データと候補リストを保存する
  def store_board_data(self):
    self.stored_data.append(copy.deepcopy(self.data))
    self.stored_candidate_list.append(copy.deepcopy(self.candidate_list))

  # 最新の保存データと候補リストを取り出す
  def restore_board_data(self):
    self.data = copy.deepcopy(self.stored_data.pop())
    self.candidate_list = copy.deepcopy(self.stored_candidate_list.pop())

  # 候補リストから特定のセルの特定の値を除外する
  def remove_from_candidate_list(self, pos, val):
    if val in self.candidate_list[Const.CELL_KEY_NAME][pos]:
      self.candidate_list[Const.CELL_KEY_NAME][pos].remove(val)

  # 空いているセル一覧を取り出す
  def get_empty_cell_list(self):
    cell_list = []
    for i in range(self.size):
      for j in range(self.size):
        if self.data.iloc[i, j] == 0:
          cell_list.append((i, j))
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

  # セル位置から矩形の番号を取得する
  def get_square_index(self, pos):
    row, col = pos
    sq_size = int(math.sqrt(self.size))
    return (row // sq_size) * sq_size + (col // sq_size)


