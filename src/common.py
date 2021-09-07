# -*- coding: utf-8 -*-

"""
共通関数
"""

import pandas as pd
import itertools

# セルに指定した値を入れる
def updateCell(board, row, col, val):
  board.loc[row, col] = val

# 終了判定を行う
def judgeComplete(board):
  # 0のセルの個数が無くなっていれば完了とする
  return not(0 in list(itertools.chain.from_iterable(board.values)))
  



