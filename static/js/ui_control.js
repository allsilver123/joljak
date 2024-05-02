import { draw_r_graph, re_layout_b_graph } from "./draw_graph.js";

let grid = GridStack.init();

let items = [
  {
    x: 0,
    y: 0,
    w: 6,
    h: 6,
    noMove: false,
    content: `<div class="grid-stack-item-content item">
    <img id="result-image" src="" alt="Processed Image">

    <div class="video">
      <!--<img src="/proxy/8000/video_stream" alt="" />-->
    </div>
  </div>`,
  },
  {
    x: 6,
    y: 0,
    w: 6,
    h: 6,
    noMove: false,
    content: `<div id="r_graph"></div>`,
  },
  {
    x: 0,
    y: 2,
    w: 12,
    h: 6,
    noMove: false,
    content: `<div id="b_graph"></div>`,
  },
  { x: 0, y: 3, w: 12, h: 6, noMove: false, content: `<div id="map"></div>` },
  {
    x: 0,
    y: 4,
    w: 12,
    h: 6,
    noMove: false,
    content: `<div id="contour_graph"></div>`,
  },
];
grid.load(items);

grid.on("added removed change", function (e, items) {
  let str = "";
  items.forEach(function (item) {
    str += " (x,y)=" + item.x + "," + item.y;
  });
  console.log(e.type + " " + items.length + " items:" + str);
  draw_r_graph();
  re_layout_b_graph();
});

// 페이지가 로드되면 실행될 함수를 정의합니다.
document.addEventListener("DOMContentLoaded", function () {
  // 체크 박스 요소에 대한 참조를 가져옵니다.
  var checkBox = document.getElementById("lock_check_box");
  console.log("lock check box used");
  // 체크 박스의 상태 변경을 감지하고, checkStatus 함수를 호출합니다.
  checkBox.addEventListener("change", lock_check_box_stat);
});

function lock_check_box_stat() {
  // 체크 박스 요소를 가져옵니다.
  var checkBox = document.getElementById("lock_check_box");

  if (checkBox.checked == true) {
    grid.setStatic(true);
  } else {
    grid.setStatic(true);
  }
}
