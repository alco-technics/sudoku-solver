
const reader = new FileReader();

function updateBoardData(data) {
  // 改行文字"\r\n"を","に置き換えて各セルのデータに分ける
  const cell_data_list = data.replaceAll('\r\n', ',').split(',')
  const board = document.getElementById('sudoku-board')
  const cell_all = board.getElementsByTagName('td')
  for (let idx = 0; idx < cell_all.length; idx++) {
    const cell = cell_all[idx]
    if (cell_data_list[idx] == 0) {
      cell.textContent = ""
      cell.style.backgroundColor = 'white'
    } else {
      cell.textContent = cell_data_list[idx]
      cell.style.backgroundColor = 'lightgray'
    }
  }
}


window.addEventListener('load', () => {
  const f = document.getElementById('csv-file-input-form');
  f.addEventListener('change', e => {
    const file = e.target.files[0];
    reader.onload = () => {
      // console.log(reader.result);
      const data = reader.result;
      updateBoardData(data)
    }
    //テキストファイルの場合
    reader.readAsText(file);
  });
});

$(function() {
  $('a#test').on('click', function(e) {
    e.preventDefault()
    $.getJSON('/',
        function(data) {
      //do nothing
    });
    return false;
  });
});



// let list_data = {{ input_from_python | tojson }}
