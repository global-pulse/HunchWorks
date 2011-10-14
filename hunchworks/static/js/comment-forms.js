$(function() {
  $("a.show-comment-form").click(function(event) {
    event.preventDefault();
    $(this).hide().parent().find("form.comment").show();
  });
});