# -*- coding: utf-8 -*-

"""
ソルバーのクラス
"""

class Solver:
  
  # def __init__(self):
  #   self.board = board

  # 候補リストのうち、1つになった値をセルに入れる
  def update_decided_num(self, board):
    # 更新があったかどうか
    update_flg = False

    for key, value in board.cell_candidate_list.items():
      if len(value) == 1:
        update_flg = True
        val = value.pop()
        board.update_cell(key, val)
    return update_flg



  """
  セルに入る可能性のある数値のリストを求める
  """
  """
  def make_cell_num_list(self, board, row, col):

  def make_candidate_cell_num(self, board, h_num_list, v_num_list, s_num_list):
    cell_num_list = []
    # 左上から右方向にインクリメントする
    for cell_idx in range(board.size):
      # セルの場所
      row = cell_idx // self.size
      col = cell_idx % self.size
      num_list = []
      if board.loc[row, col] == 0:  # 確定しているセルは空にする
        h_list = h_num_list[row]
        v_list = v_num_list[col]
        s_list = s_num_list[(row // 3) * 3 + (col // 3)]
        for num in range(1, 10):
          # 横、縦、矩形内の当該数値リストに同じ数値がない数を追加する
          if not((num in h_list) or (num in v_list) or (num in s_list)):
            num_list.append(num)
      cell_numm_list.append(num_list)
    return cell_num_list

  # 横、縦、矩形内の数値リストを作成する
  def make_board_num_list(self, board, mode):
    num_list = []
    if mode == 'h':
      for i in range(9):
        num_list.append(list(board.iloc[i, :]))
    elif mode == 'v':
      for i in range(9):
        num_list.append(list(board.iloc[:, i]))
    else:
      for i in range(9):
        row = i // 3
        col = i % 3
        num_list.append(list(itertools.chain.from_iterable(board.iloc[row*3:(row+1)*3, col*3:(col+1)*3].values)))
    return num_list



  """
