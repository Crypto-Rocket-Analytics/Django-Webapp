am5.ready(async function () {
  data = await $.getJSON("/full_data_fresh/", function (ret) {
    return ret;
  });

  var data2 = [];

  data.forEach((v, i) => {
    data2.push({ category: data[i].category, value: data[i].value * etlPrice });
  });

  // Create root element
  // https://www.amcharts.com/docs/v5/getting-started/#Root_element
  var root = am5.Root.new("chartdiv");

  // Set themes
  // https://www.amcharts.com/docs/v5/concepts/themes/
  root.setThemes([am5themes_Animated.new(root)]);

  // Create chart
  // https://www.amcharts.com/docs/v5/charts/xy-chart/
  var chart = root.container.children.push(
    am5xy.XYChart.new(root, {
      panX: false,
      panY: false,
      wheelX: "panX",
      wheelY: "zoomX",
    })
  );

  // Add cursor
  // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
  var cursor = chart.set(
    "cursor",
    am5xy.XYCursor.new(root, {
      behavior: "zoomX",
    })
  );
  cursor.lineY.set("visible", false);

  // Create axes
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/category-date-axis/
  var xRenderer = am5xy.AxisRendererX.new(root, {});
  xRenderer.labels.template.setAll({
    fill: am5.color(0xb5b5c3),
    minPosition: 0.01,
    maxPosition: 0.99,
  });

  var yRenderer = am5xy.AxisRendererY.new(root, {});
  yRenderer.labels.template.setAll({
    fill: am5.color(0xb5b5c3),
  });

  var xAxis = chart.xAxes.push(
    am5xy.CategoryAxis.new(root, {
      categoryField: "category",
      renderer: xRenderer,
      tooltip: am5.Tooltip.new(root, {}),
    })
  );

  var yAxis = chart.yAxes.push(
    am5xy.ValueAxis.new(root, {
      renderer: yRenderer,
    })
  );

  xAxis.children.push(
    am5.Label.new(root, {
      text: "MP",
      x: am5.p50,
      centerX: am5.p50,
      fill: am5.color(0xb5b5c3),
    })
  );

  yAxis.children.unshift(
    am5.Label.new(root, {
      rotation: -90,
      text: "Price in ETL",
      y: am5.p50,
      centerX: am5.p50,
      fill: am5.color(0xb5b5c3),
    })
  );

  // Add series
  // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
  var series = chart.series.push(
    am5xy.LineSeries.new(root, {
      name: "Series",
      xAxis: xAxis,
      yAxis: yAxis,
      valueYField: "value",
      categoryXField: "category",
    })
  );

  var tooltip = series.set("tooltip", am5.Tooltip.new(root, {}));
  tooltip.label.set("text", "{valueY}");

  // Add scrollbar
  // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
  chart.set(
    "scrollbarX",
    am5.Scrollbar.new(root, {
      orientation: "horizontal",
    })
  );

  // Set data
  series.data.setAll(data);
  xAxis.data.setAll(data);

  function updateGraph() {
    series.data.setAll(data);
    xAxis.data.setAll(data);
  }
  setInterval(updateGraph, 10000);

  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  series.appear(1000);
  chart.appear(1000, 100);

  // Create root element
  // https://www.amcharts.com/docs/v5/getting-started/#Root_element
  var root2 = am5.Root.new("chartdiv-2");

  // Set themes
  // https://www.amcharts.com/docs/v5/concepts/themes/
  root2.setThemes([am5themes_Animated.new(root2)]);

  // Create chart
  // https://www.amcharts.com/docs/v5/charts/xy-chart/
  var chart2 = root2.container.children.push(
    am5xy.XYChart.new(root2, {
      panX: false,
      panY: false,
      wheelX: "panX",
      wheelY: "zoomX",
    })
  );

  // Add cursor
  // https://www.amcharts.com/docs/v5/charts/xy-chart/cursor/
  var cursor2 = chart2.set(
    "cursor",
    am5xy.XYCursor.new(root2, {
      behavior: "zoomX",
    })
  );
  cursor2.lineY.set("visible", false);

  // Create axes
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/
  // https://www.amcharts.com/docs/v5/charts/xy-chart/axes/category-date-axis/
  var xRenderer2 = am5xy.AxisRendererX.new(root2, {});
  xRenderer2.labels.template.setAll({
    fill: am5.color(0xb5b5c3),
    minPosition: 0.01,
    maxPosition: 0.99,
  });

  var yRenderer2 = am5xy.AxisRendererY.new(root2, {});
  yRenderer2.labels.template.setAll({
    fill: am5.color(0xb5b5c3),
  });

  var xAxis2 = chart2.xAxes.push(
    am5xy.CategoryAxis.new(root2, {
      categoryField: "category",
      renderer: xRenderer2,
      tooltip: am5.Tooltip.new(root2, {}),
    })
  );

  var yAxis2 = chart2.yAxes.push(
    am5xy.ValueAxis.new(root2, {
      renderer: yRenderer2,
    })
  );

  xAxis2.children.push(
    am5.Label.new(root2, {
      text: "MP",
      x: am5.p50,
      centerX: am5.p50,
      fill: am5.color(0xb5b5c3),
    })
  );

  yAxis2.children.unshift(
    am5.Label.new(root2, {
      rotation: -90,
      text: "Price in USD",
      y: am5.p50,
      centerX: am5.p50,
      fill: am5.color(0xb5b5c3),
    })
  );

  // Add series
  // https://www.amcharts.com/docs/v5/charts/xy-chart/series/
  var series2 = chart2.series.push(
    am5xy.LineSeries.new(root2, {
      name: "Series",
      xAxis: xAxis2,
      yAxis: yAxis2,
      valueYField: "value",
      categoryXField: "category",
    })
  );

  var tooltip2 = series2.set("tooltip", am5.Tooltip.new(root2, {}));
  tooltip2.label.set("text", "{valueY}");

  // Add scrollbar
  // https://www.amcharts.com/docs/v5/charts/xy-chart/scrollbars/
  chart2.set(
    "scrollbarX",
    am5.Scrollbar.new(root2, {
      orientation: "horizontal",
    })
  );

  // Set data
  series2.data.setAll(data2);
  xAxis2.data.setAll(data2);

  function updateGraph2() {
    var data2 = [];

    data.forEach((v, i) => {
      data2.push({
        category: data[i].category,
        value: data[i].value * etlPrice,
      });
    });

    series2.data.setAll(data2);
    xAxis2.data.setAll(data2);
  }
  setInterval(updateGraph2, 10000);
  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  series2.appear(1000);
  chart2.appear(1000, 100);
}); // end am5.ready()
