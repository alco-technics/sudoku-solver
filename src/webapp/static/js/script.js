
// 数独のボードを作成する
function renderSudokuBoard(size) {
  const cell_num = size * size
  for (let row = 0; row < cell_num; row++) {
    const tr = document.createElement('tr');
    for (let col = 0; col < cell_num; col++) {
      const td = document.createElement('td');
      td.textContent = "";
      tr.appendChild(td);
    }
    document.querySelector('tbody').appendChild(tr);
  }
}

// セルの境界線をスタイルする
function styleCellBorder(cell, style) {
  cell.style.borderTopStyle = style['top']['style']
  cell.style.borderTopWidth = style['top']['width']
  cell.style.borderBottomStyle = style['bottom']['style']
  cell.style.borderBottomWidth = style['bottom']['width']
  cell.style.borderLeftStyle = style['left']['style']
  cell.style.borderLeftWidth = style['left']['width']
  cell.style.borderRightStyle = style['right']['style']
  cell.style.borderRightWidth = style['right']['width']
}

// 枠線のスタイルを設定する
function styleBoardBorder(size) {
  const cell_num = size * size
  const board = document.getElementById('sudoku-board');
  const cell_all = board.getElementsByTagName('td');
  // 各サイズの端は実線、それ以外は点線にする
  for (let row = 0; row < cell_num; row++) {  // 縦
    for (let col = 0; col < cell_num; col++) {  // 横
      const cell = cell_all[row * cell_num + col]
      let style = {
        'top': {'style': 'dashed', 'width': '1px'}, 
        'left': {'style': 'dashed', 'width': '1px'}, 
        'bottom': {'style': 'none', 'width': '0px'}, 
        'right': {'style': 'none', 'width': '0px'}
      }
      if (row % size == 0) { // 各領域の上端
        style['top']['style'] = 'solid'
        style['top']['width'] = '2px'
      }
      if (col % size == 0) { // 各枠の左端
        style['left']['style'] = 'solid'
        style['left']['width'] = '2px'
      }
      if (row == cell_num - 1) { // ボードの下端
        style['bottom']['style'] = 'solid'
        style['bottom']['width'] = '2px'
      }
      if (col == cell_num - 1) { // ボードの右端
        style['right']['style'] = 'solid'
        style['right']['width'] = '2px'
      }
      styleCellBorder(cell, style)
    }
  }
}


// リクエスト用にデータを作成する
function createReqData() {
  // 全てのセルが空であればNGを返す。
  let ret_str = ''
  let ng_flg = true
  const board = document.getElementById('sudoku-board')
  const cell_all = board.getElementsByTagName('td')
  for (let idx = 0; idx < cell_all.length; idx++) {
    const cell_text = cell_all[idx].textContent
    if (cell_text == "") {
      ret_str += '0'
    } else {
      ret_str += cell_text
      ng_flg = false
    }
    if (!(idx == cell_all.length - 1)) {
      ret_str += ','
    }
  }

  if (ng_flg) {
    return undefined
  }
  return ret_str
}


// 数独を解く
function solveSudoku() {
  // リクエスト用にデータを成型する。(ボードから取得する)
  const req_data = createReqData()
  if (!req_data) {
    document.getElementById('warning-msg').textContent = 'データが選択されていません。'
    return
  } else {
    document.getElementById('warning-msg').textContent = ''
  }

  // リクエスト
  console.log(req_data)
  fetch('/', {
    method: 'POST', // *GET, POST, PUT, DELETE, etc.
    cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
    credentials: 'same-origin', // include, *same-origin, omit
    headers: {
      'Content-Type': 'text/plain'
    },
    redirect: 'follow',
    referrerPolicy: 'no-referrer',
    body: req_data
    }).then(function (response) {
        response.text().then(function(text) {
          // ボードを更新する
          updateBoardData(text)
        });
    });

}


// エントリポイント
const size = 3 // 9マス
renderSudokuBoard(size) // 数独を作る
styleBoardBorder(size) // 境界線を調整する

