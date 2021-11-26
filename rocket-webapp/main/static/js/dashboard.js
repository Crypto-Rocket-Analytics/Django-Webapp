am5.ready(async function () {
  const data = await $.getJSON("/full_data_fresh/", function (ret) {
    return JSON.parse(ret);
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
  xRenderer.labels.template.set("minPosition", 0.01);
  xRenderer.labels.template.set("maxPosition", 0.99);

  xRenderer.labels.template.set({
    fill: am5.color(0xFFFFFF),
    fontSize: "1.5em"
  })

  // yRenderer.labels.template.setAll({
  //   fill: am5.color(0xFFFFFF),
  //   fontSize: "1.5em"
  // })


  var xAxis = chart.xAxes.push(
    am5xy.CategoryAxis.new(root, {
      categoryField: "category",
      renderer: xRenderer,
      tooltip: am5.Tooltip.new(root, {}),
    })
  );

  var yAxis = chart.yAxes.push(
    am5xy.ValueAxis.new(root, {
      renderer: am5xy.AxisRendererY.new(root, {}),
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

  // Make stuff animate on load
  // https://www.amcharts.com/docs/v5/concepts/animations/
  series.appear(1000);
  chart.appear(1000, 100);
}); // end am5.ready()
