$(function() {
  $("div.connections-widget").each(function() {
    var $widget = $(this);
    var $value = $widget.find(".csv input");

    var value = function() {
      return $widget.find("article.user.selected").map(function() {
        return $(this).data("id");
      }).get().join(",")
    };

    var update_value = function() {
      $value.val(value());
    };

    $widget.on("click", "article.user", function(event) {
      $(this).toggleClass("selected");
      event.preventDefault();
      update_value();
    });

    /* Add the "selected" class to the users which are are selected. This is a
    |* hack; MultipleConnectionWidget should deal with this server-side. */
    _.each($value.val().split(","), function(id) {
      $widget.find("article.user[data-id=" + id + "]").addClass("selected");
    });
  });
});
