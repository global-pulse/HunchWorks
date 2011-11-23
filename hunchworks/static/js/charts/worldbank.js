$(function() {
  var init_wb_chart = function(element) {
    var $widget = $(element);

    var table = new google.visualization.DataTable();
    table.addColumn("string", $widget.data("x-axis"));
    
    _.each( $widget.data("countries"), function(country_name){
      table.addColumn("number", country_name);
    });
    table.addRows($widget.data("data"));

    var chart = new google.visualization.LineChart(element);
    chart.draw(table, {
      "height": 400
    });
  };

  /* If there are any WorldBank charts on this page, load the Google viz API. */
  var widgets = $("div.worldbank-chart");
  if(widgets.length) {

    google.load("visualization", "1.0", {
      "packages": ["corechart"],
      "callback": function() {

        /* Iterate the charts to set each up. */
        _.each(widgets, init_wb_chart);
      }
    });
  }
});
