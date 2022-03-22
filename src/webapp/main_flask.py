#Flaskとrender_template（HTMLを表示させるための関数）をインポート
import pandas as pd
from flask import Flask, render_template, request, send_from_directory

import os, sys, math
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from class_board import Board
from class_solver import Solver


#Flaskオブジェクトの生成
app = Flask(__name__)


@app.route("/favicon.ico")
def favicon():
    return app.send_static_file("favicon.ico")


@app.route("/")
def init():
    # 初期画面
    return render_template("main.html")


@app.route("/", methods=["post"])
def solve():
    """
    解析して結果を返す
    """
    # リクエストデータをDataFrameにする。
    board_data = arrange_request_board_data(request.get_data().decode('UTF-8'))
    # board = Board(data=board_data)
    board = Board(file_path = '../data/sample_4003.csv')
    solver = Solver()
    solver.solve(board)

    # レスポンスできるようにDataFrameを文字列に成型する
    res = arrange_for_response(board.data)
    return res

    # return board.data.values

def arrange_for_response(board_data):
    """
    レスポンスできるように成型する
    :param board_data: ボードのデータ(DataFrame)
    :return: コンマ区切りの文字列に変形して返す
    """
    ret_str = ''
    for r in range(len(board_data.columns)):
        for c in range(len(board_data.index)):
            ret_str += str(board_data.iloc[r, c])
            if not (r == len(board_data.columns) - 1
                    and c == len(board_data.index) - 1):
                ret_str += ','
    return ret_str

def arrange_request_board_data(req_data):
    """
    リクエストデータを数独の盤面データ(DataFrame)に変形する
    :param req_data: コンマ区切りの文字列
    :return: DataFrameにして返す
    """
    data_list_1d = req_data.split(',')
    cell_num = len(data_list_1d)
    size_ = int(math.sqrt(cell_num))

    # 2次元配列にする
    data_list_2d = []
    for i in range(size_):
        data_list_2d.append([int(s) for s in data_list_1d[i*size_:(i+1)*size_]])

    req_df = pd.DataFrame(data_list_2d)
    return req_df



# メイン関数
if __name__ == "__main__":
    app.run(debug=True)