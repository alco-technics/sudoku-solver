# -*- coding: utf-8 -*-

"""
メインファイル
GUIを作成する
"""

import PySimpleGUI as sg
import math

import class_board
import class_solver

def make_layout_board(size):
    layout_board = []
    sq_size = math.sqrt(size)
    for y in range(size):
        tmp = []
        for x in range(size):
            pad_l = 3 if x == 0 else 0
            pad_r = 3 if (x + 1) % sq_size == 0 else 0
            pad_t = 3 if y == 0 else 0
            pad_b = 3 if (y + 1) % sq_size == 0 else 0
            tmp += [
                sg.Input(
                    size=(2, 1),
                    pad=((pad_l, pad_r), (pad_t, pad_b)),
                    border_width=1,
                    justification = 'center',
                    font=('Arial', 24),
                    key='-{},{}-'.format(x, y),
                    readonly=True
                    )
                ]
        layout_board += [tmp]
    return layout_board

def update_board(board):
    for y in range(board.size):
        for x in range(board.size):
            val = board.data.iloc[y, x]
            window['-{},{}-'.format(x, y)].update("" if val == 0 else val)

def disable_button(key, disable_state):
    window[key].update(disabled=disable_state)


if __name__ == "__main__":

    board = class_board.Board()
    solver = class_solver.Solver()

    ## ファイル入力のレイアウト
    layout_file_input = [
        sg.Text('Input (csv) :', font=('Arial', 16)),
        sg.Input(key='-csv-input-file-', font=('Arial', 16), readonly=True, enable_events=True),
        sg.FileBrowse(file_types=(("CSV files", "*.csv"), ("All files", "*.*")))
    ]

    ## 盤面のレイアウト
    layout_board = make_layout_board(board.size)
    layout_board_frame = sg.Frame(
        '',
        layout_board,
        relief=sg.RELIEF_SUNKEN,
        background_color="black"
    )

    print("layout_board...")
    print(layout_board)

    ## ボタン
    layout_footer = [
        sg.Button('Solve', key='-solve-', disabled=True),
        sg.Button('Reset', key='-reset-', disabled=True),
        sg.Button('Clear', key='-clear-', disabled=True),
        sg.Button('Quit', key='-quit-')
    ]

    ## ログ用テキストボックス
    layout_log_box = [
        [sg.Multiline(background_color='#ffffcc', key='-log-text-', size=(50, 20), autoscroll=True)],
        [sg.Button('Log Clear', key='-log-clear-')]
    ]
    layout_log_box_frame = sg.Frame('-- Log --', layout_log_box, relief=sg.RELIEF_SUNKEN)
    log_str = ''

    ### レイアウト設定 ###
    layout_parent = [
        [
            layout_file_input,
            [layout_board_frame, layout_log_box_frame],
            layout_footer,
        ]
    ]

    ### ウィンドウ生成 ###
    window = sg.Window(
        'Sudoku Solver',
        layout_parent,
        location=(2000, 10),
        resizable=True
    )

    ### イベントループ ###
    while True:

        event, values = window.read(timeout=20)

        if event == sg.WIN_CLOSED or event == '-quit-':
            break

        # CSVファイルが選択されたら、インスタンス更新し、盤面も更新
        if event == '-csv-input-file-':
            log_str += 'Selected File : {}\n'.format(values['-csv-input-file-'])
            board = class_board.Board(values['-csv-input-file-'])
            update_board(board)
            disable_button('-solve-', False)
            disable_button('-clear-', False)


        # Solveボタン押下
        if event == '-solve-':
            log_str += '--- Start! ---\n'
            log_str += 'Data File : {}\n'.format(values['-csv-input-file-'])
            solver.solve(board)
            update_board(board)
            disable_button('-reset-', False)
            disable_button('-solve-', True)
            log_str += '--- Complete! ---\n'

        if event == '-reset-':
            log_str += '--- Reset board. ---\n'
            # インスタンスを取得しなおす
            board = class_board.Board(values['-csv-input-file-'])
            update_board(board)
            disable_button('-solve-', False)

        if event == '-clear-':
            log_str += '--- Clear ---.\n'
            board.clear()
            update_board(board)
            disable_button('-solve-', True)
            disable_button('-reset-', True)
            disable_button('-clear-', True)
            window['-csv-input-file-'].update('')

        if event == '-log-clear-':
            log_str = ''

        window['-log-text-'].update(log_str)



    # ウィンドウの破棄と終了
    window.close()



