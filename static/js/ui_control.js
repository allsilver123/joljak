import { draw_r_graph, re_layout_b_graph } from "./draw_graph.js";

let grid = GridStack.init();

let items = [
  {
    x: 0,
    y: 0,
    w: 9,
    h: 6,
    noMove: false,
    content: `<div class="grid-stack-item-content item">
    <img id="result-image" src="" alt="Processed Image">

    <div class="video">
      
    </div>
  </div>`,
  },
  {
    x: 10,
    y: 0,
    w: 3,
    h: 3,
    noMove: false,
    content: `<div id="r_graph"></div>`,
  },
  {
    x: 10,
    y: 0,
    w: 3,
    h: 2,
    noMove: false,
    content: `<div id="b_graph"></div>`,
  },
];
grid.load(items);

grid.on("added removed change", function (e, items) {
  let str = "";
  items.forEach(function (item) {
    str += " (x,y)=" + item.x + "," + item.y;
  });
});

function lockGrid() {
  grid.setStatic(true);
}

// 그리드를 비정적으로 설정하는 함수
function unlockGrid() {
  grid.setStatic(false);
}

// 고정 링크에 이벤트 리스너 등록
document.getElementById("lockGridLink").addEventListener("click", lockGrid);

// 고정 해제 링크에 이벤트 리스너 등록
document.getElementById("unlockGridLink").addEventListener("click", unlockGrid);
