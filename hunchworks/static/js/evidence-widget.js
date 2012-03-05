$(function() {
  var SEARCH_HELP = "Search for existing evidences, and click to attach them to this hunch.";
  var INPUT_WITH_RESULTS_CLASS = "with-evidence-search-results";

  $("div.evidence-widget.many").each(function() {
    var $widget = $(this);

    var $results_outer = $("<div />", { "class": "evidence-search-results" }).hide().appendTo(document.body);
    var $results_inner = $("<section />", { "class": "short-list evidence" }).appendTo($results_outer);

    var $search_container = $("<div />", { "class": "widget search" }).appendTo($widget);
    var $search           = $('<input />', {  "type": "text", "class": "search" }).appendTo($search_container);
    var $search_help      = $("<p>", { "class": "help" }).html(SEARCH_HELP).appendTo($search_container);

    var $previews = $("> .short-list.evidence", $widget);
    var $value    = $("> .widget > input", $widget);


    var to_int = function(x) {
      return parseInt(x, 10);
    };

    var previews = function() {
      return $("> .evidence", $previews);
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
        "left": $search.offset().left,
        "top": $search.offset().top + $search.outerHeight(),
        "width": $search.outerWidth()
      });
    };

    var add_delete_link = function($previews) {
      _.each($previews, function(preview) {
        $("<div>", { "class": "delete", }).html("&times;").prependTo(preview);
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

      $results_inner.empty();

      $.ajax({
        url: $widget.data("search-url") + "?q=" + str,
        success: function(data) {
          _.each(data, function(object) {
            $results_inner.append(object.preview);
          });

          $search.addClass(INPUT_WITH_RESULTS_CLASS);
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
      var $evidence = $(event.target).closest(".evidence");

      add_preview($evidence);
      add_delete_link($evidence);
      update_values();
      $search.val("");

      $(document.body).click();
    });

    $results_inner.on("click", "a", function(event) {
      event.preventDefault();
    });

    $previews.delegate(".delete", "click", function() {
      $(this).closest(".evidence").remove();
      update_values();
    });

    $(document.body).click(function(event) {
      $search.removeClass(INPUT_WITH_RESULTS_CLASS);
      $results_outer.hide();
      $results_inner.empty();
    });

    $results_outer.click(function(event) {
      event.stopPropagation();
    });

    add_delete_link($("> .evidence", $previews));
    $("> .widget.csv", $widget).hide();
  });
});
