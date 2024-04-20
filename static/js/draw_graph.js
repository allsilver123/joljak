function getNewData() {
  var newData = [
    [
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
    ],
    [
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
    ],
    [
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
    ],
    [
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
    ],
    [
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
      Math.random() * 100,
    ],
  ];

  return newData;
}

function getGraphSize(id) {
  var graph = document.getElementById(id); // 아이디로 요소 선택
  var parent = graph.parentElement; // 부모 요소에 접근
  return {
    width: parent.offsetWidth, // 부모 요소의 너비
    height: parent.offsetHeight, // 부모 요소의 높이
  };
}

export function draw_r_graph() {
  console.log("draw_r_graph");
  var size = getGraphSize("r_graph");
  var data1 = [
    {
      z: getNewData(),
      type: "surface",
    },
  ];

  var layout = {
    autosize: false, // 자동 크기 조절을 비활성화
    width: size.width, // rGraph의 너비로 설정
    height: size.height, // rGraph의 높이로 설정
    margin: {
      l: 0,
      r: 0,
      b: 0,
      t: 0,
    },
    plot_bgcolor: "black",
    paper_bgcolor: "black",
    font: {
      color: "white",
    },
    xaxis: {
      title: {
        font: {
          size: 18,
          color: "white",
        },
      },
    },
    yaxis: {
      title: {
        font: {
          size: 18,
          color: "white",
        },
      },
    },
  };

  var config = {
    responsive: true,
  };

  Plotly.newPlot("r_graph", data1, layout, config);

  console.log("r_graph");
  console.log(layout);
}

export function re_layout_b_graph() {
  console.log("re_layout_b_graph");
  var size = getGraphSize("b_graph");
  var layout = {
    width: size.width,
    height: size.height,
  };
  Plotly.relayout("b_graph", layout);
}

function randomize() {
  Plotly.animate(
    "randomize",
    {
      data: [{ z: getNewData() }],
      traces: [0],
      layout: {},
    },
    {
      transition: {
        duration: 500,
        easing: "cubic-in-out",
      },
      frame: {
        duration: 500,
      },
    }
  );
}

function rand() {
  idx += 1;
  if (idx < 3) {
    console.log("zero");
    return 0;
  }
  return Math.floor(Math.random() * 10) + 50;
}
let idx = 0;
export function draw_b_graph() {
  // 차트 데이터
  var data = [
    {
      y: [0].map(rand), // y 값으로 랜덤한 숫자를 사용
      mode: "lines",
      line: { color: "#80CAF6" },
    },
  ];
  var size = getGraphSize("b_graph");
  // 레이아웃 설정

  var layout = {
    autosize: false, // 자동 크기 조절을 비활성화
    width: size.width, // rGraph의 너비로 설정
    height: size.height, // rGraph의 높이로 설정
    margin: {
      l: 20,
      r: 20,
      b: 20,
      t: 20,
    },
    plot_bgcolor: "black",
    paper_bgcolor: "black",
    font: {
      color: "white",
    },
    xaxis: {
      title: {
        font: {
          size: 18,
          color: "white",
        },
      },
    },
    yaxis: {
      title: {
        font: {
          size: 18,
          color: "white",
        },
      },
    },
  };

  // Plotly.newPlot 함수를 사용하여 차트를 그립니다.
  Plotly.newPlot("b_graph", data, layout);

  var cnt = 0;

  var interval = setInterval(function () {
    Plotly.extendTraces(
      "b_graph",
      {
        y: [[rand()]],
      },
      [0]
    );

    if (++cnt === 100) clearInterval(interval);
  }, 300);
}

window.addEventListener("load", draw_r_graph);
window.addEventListener("load", draw_b_graph);
window.addEventListener("load", draw_contour_graph);
setInterval(randomize, 5000);

function draw_contour_graph() {
  var data = [
    {
      z: [
        [10, 10.625, 12.5, 15.625, 20],
        [5.625, 6.25, 8.125, 11.25, 15.625],
        [2.5, 3.125, 5.0, 8.125, 12.5],
        [0.625, 1.25, 3.125, 6.25, 10.625],
        [0, 0.625, 2.5, 5.625, 10],
      ],
      type: "contour",
      colorscale: "Jet",
      contours: {
        coloring: "lines",
      },
    },
  ];

  var layout = {
    title: "Basic Contour Plot",
  };

  Plotly.newPlot("contour_graph", data, layout);
}
