$(function() {

  $("div.evidence-widget").each(function() {
    var $widget = $(this);

    var $results_outer = $("<div />", { "class": "search-results" }).hide().appendTo($widget);
    var $results_inner = $("<div />", { "class": "evidences" }).appendTo($results_outer);
    var $results_title = $("<h3 />").prependTo($results_outer);

    var $search   = $('<input type="text" class="search">').appendTo($widget);
    var $value    = $("> div.widget > input", $widget);
    var $previews = $("> div.evidences", $widget);


    var to_int = function(x) {
      return parseInt(x, 10);
    };

    var previews = function() {
      return $("> div", $previews);
    };

    var preview_id_set = function() {
      return _.map(previews(), function(x) {
        return $(x).data("id") });
    };

    var add_preview = function($preview) {
      if(!_.include(preview_id_set(), $preview.data("id"))) {
        $preview.appendTo($previews);
      }
    };

    var update_values = function() {
      $value.val(preview_id_set().join(", "));
    };

    var update_results_position = function() {
      $results_outer.css({
        "position": "absolute",
        "left": $search.position().left,
        "top": $search.position().top + $search.outerHeight(),
        "width": $search.outerWidth()
      });
    };

    var last_search = "";

    var perform_search = function() {
      var str = $search.val();

      if(str == last_search)
        return false;

      last_search = str;

      if(str == "")
        return false;

      $results_title.html("Search results for: " + str);
      $results_inner.empty();

      $.ajax({
        url: $widget.data("search-url") + "?q=" + str,
        success: function(data) {
          _.each(data, function(object) {
            $results_inner.append(object.preview);
          });

          update_results_position();
          $results_outer.show();
        }
      });

    };

    $search.bind(
      "keyup keydown change",
      _.debounce(perform_search, 300)
    );

    $results_inner.click(function(event) {
      var $evidence = $(event.target).closest("div.evidence");

      add_preview($evidence);
      update_values();
      $search.val("");

      $(document.body).click();
    });

    $(document.body).click(function(event) {
      $results_outer.hide();
      $results_inner.empty();
    });

    $results_outer.click(function(event) {
      event.stopPropagation();
    });

    $("> div.widget", $widget).hide();
  });
});