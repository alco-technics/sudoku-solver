# -*- coding: utf-8 -*-

"""
初期化など

"""

import pandas as pd
import itertools
import time

import Common as comLib

def initBoard():
  # 全てのセルを0とする
  board = pd.DataFrame([[0]*9]*9)
  return board

def makeBoardFromCsv(filePath):
  return pd.read_csv(filePath, header=None)


def makeCandidateCellNum(board, hNumList, vNumList, sNumList):
  cellNumList = []
  # 左上から右方向にインクリメントする
  for cellIdx in range(board.size):
    # セルの場所
    row = cellIdx // 9
    col = cellIdx % 9
    # print(row, col, board.loc[row, col])
    numList = []
    if board.loc[row, col] == 0:  # 確定しているセルは空にする
      hList = hNumList[row]
      vList = vNumList[col]
      sList = sNumList[(row // 3) * 3 + (col // 3)]
      # print(row, col, hList, vList, sList)
      for num in range(1, 10):
        # 横、縦、矩形内の当該数値リストに同じ数値がない数を追加する
        if not((num in hList) or (num in vList) or (num in sList)):
          numList.append(num)
    cellNumList.append(numList)
  return cellNumList

# 横、縦、矩形内の数値リストを作成する
def makeBoardNumList(board, mode):
  numList = []
  if mode == 'h':
    for i in range(9):
      numList.append(list(board.iloc[i, :]))
  elif mode == 'v':
    for i in range(9):
      numList.append(list(board.iloc[:, i]))
  else:
    for i in range(9):
      row = i // 3
      col = i % 3
      numList.append(list(itertools.chain.from_iterable(board.iloc[row*3:(row+1)*3, col*3:(col+1)*3].values)))
  return numList


##### TODO : 後々外に出すけど、今は一旦ここで実装 #####
# とりあえず、候補の数値が1つのものを埋める
def updateDecidedNumber(board, cellNumList):
  flgUpdate = False
  for cellIdx in range(len(cellCandidateNumList)):
    cellCandidateNum = cellCandidateNumList[cellIdx]
    if len(cellCandidateNum) == 1:
      # TODO : 他の横、縦、矩形内の候補リストからもこの時点でremoveできるようにする。
      flgUpdate = True
      num = cellCandidateNum.pop() 
      row = cellIdx // 9
      col = cellIdx % 9
      comLib.updateCell(board, row, col, num)
  return flgUpdate

if __name__ == "__main__":
  startTime = time.time()
  # board = initBoard()
  # print(board)

  board = makeBoardFromCsv('..\data\sample_0001.csv')
  initBoard = copy.deepcopy(board)
  # comLib.updateCell(board, 0, 0, 8)

  print("init board ... ")
  print(initBoard)

  # Step 1. 候補の数値リストを作成→候補が１つのセルを埋める、を更新できなくなるまで繰り返す。
  cnt = 1
  print("Start Step 1.")
  while True:
    hNumList = makeBoardNumList(board, 'h')
    vNumList = makeBoardNumList(board, 'v')
    sNumList = makeBoardNumList(board, 's')
    print("update board {} ... ".format(cnt))
    cellCandidateNumList = makeCandidateCellNum(board, hNumList, vNumList, sNumList)
    print("cellCandidateNumList ... ", cellCandidateNumList)
    flgUpdate = updateDecidedNumber(board, cellCandidateNumList)
    print("flgUpdate ... {}".format(flgUpdate))
    print(board)
    if not(flgUpdate):
      print("Complete Step 1.")
      break
    cnt+=1

  # 終了判定
  flgComplete = comLib.judgeComplete(board)
  if flgComplete:
    print("Mission completed!")
    elapsedTime = time.time() - startTime
    print("Elapsed Time [ms] ... {}".format(elapsedTime*1000))
    exit()
  else:
    print("Not completed Step 1 ... ")

  # Step 2... Comming Soon ^^
  # TODO : その前にInitialize.pyの外に出そうな。






