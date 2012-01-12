/* Add a button to toggle CSS debug mode. */

$(function() {
  $("<div>").click(function() {
    $("html").toggleClass("debug");

  }).css({
    "position": "absolute",
    "font-size": "10px",
    "line-height": "17px",
    "top": 0,
    "left": 0,
    "padding": "0 5px",
    "background": "#ffc",
    "cursor": "pointer",
    "border-bottom": "1px solid #bbb",
    "border-right": "1px solid #bbb"

  }).text("DEBUG").appendTo("body");
});
