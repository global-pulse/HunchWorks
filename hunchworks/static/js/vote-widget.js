$(function() {
  $("div.vote-widget input").click(function() {
    $(this).closest("form").submit();
  });
});