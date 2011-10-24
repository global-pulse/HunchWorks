$(function() {
  $("div.vote-widget label").click(function() {
    var $li = $(this).closest("li");
    $li.siblings("li").removeClass("selected");
    $li.addClass("selected");
  });
});