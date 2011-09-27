$(function() {

  $("div.evidence-widget").each(function() {
    var $widget = $(this);

    var $search = $('<input type="text" class="search">').prependTo($widget);
    var $results = $("<div />", { "class": "search-results" }).appendTo($widget);

    var search_result = function(object) {
      return $("<div />", { "id": object.id, "html": object.preview });
    };

    $search.change(function() {
      $results.empty();

      $.ajax({
        url: $widget.data("search-url") + "?q=" + $search.val(),
        success: function(data) {
          $.each(data, function(n, object) {
            $results.append(search_result(object));
          });
        }
      });
    }).prependTo($widget);
  });
});