import { draw_r_graph, draw_b_graph } from "./draw_graph.js";

const resizable = function (resizer) {
  const direction = resizer.getAttribute("data-direction") || "horizontal";
  const prevSibling = resizer.previousElementSibling;
  const nextSibling = resizer.nextElementSibling;

  let x = 0;
  let y = 0;
  let prevSiblingHeight = 0;
  let prevSiblingWidth = 0;

  const mouseDownHandler = function (e) {
    x = e.clientX;
    y = e.clientY;
    const rect = prevSibling.getBoundingClientRect();
    prevSiblingHeight = rect.height;
    prevSiblingWidth = rect.width;

    document.addEventListener("mousemove", mouseMoveHandler);
    document.addEventListener("mouseup", mouseUpHandler);
  };

  const mouseMoveHandler = function (e) {
    const dx = e.clientX - x;
    const dy = e.clientY - y;

    switch (direction) {
      case "vertical":
        const h =
          ((prevSiblingHeight + dy) * 100) /
          resizer.parentNode.getBoundingClientRect().height;
        prevSibling.style.height = `${h}%`;
        break;
      case "horizontal":
      default:
        const w =
          ((prevSiblingWidth + dx) * 100) /
          resizer.parentNode.getBoundingClientRect().width;
        prevSibling.style.width = `${w}%`;
        break;
    }

    resizer.style.cursor =
      direction === "horizontal" ? "col-resize" : "row-resize";
    document.body.style.cursor =
      direction === "horizontal" ? "col-resize" : "row-resize";

    prevSibling.style.userSelect = "none";
    prevSibling.style.pointerEvents = "none";
    nextSibling.style.userSelect = "none";
    nextSibling.style.pointerEvents = "none";
  };

  const mouseUpHandler = function () {
    resizer.style.removeProperty("cursor");
    document.body.style.removeProperty("cursor");
    prevSibling.style.removeProperty("user-select");
    prevSibling.style.removeProperty("pointer-events");
    nextSibling.style.removeProperty("user-select");
    nextSibling.style.removeProperty("pointer-events");

    document.removeEventListener("mousemove", mouseMoveHandler);
    document.removeEventListener("mouseup", mouseUpHandler);

    // 크기 조절이 완료된 후, 그래프를 다시 그립니다.
    // 여기서는 prevSibling 또는 nextSibling의 클래스가 'rGraph'인지 확인합니다.
    // 이 부분을 수정하여 상하 방향으로 조절 시에도 조건을 충족시킬 수 있도록 합니다.
    if (
      prevSibling.classList.contains("rGraph") ||
      nextSibling.classList.contains("rGraph")
    ) {
      draw_r_graph(); // 이 부분에서 그래프를 다시 그리는 함수를 호출합니다.
      draw_b_graph();
    }
    draw_r_graph();
    draw_b_graph();
  };

  resizer.addEventListener("mousedown", mouseDownHandler);

  resizer.addEventListener("mouseup", mouseUpHandler);
};

document.querySelectorAll(".resizer").forEach(function (ele) {
  resizable(ele);
});
