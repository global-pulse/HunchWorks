$(function() {
  var EMBEDLY_KEY = "b0383ffaf0ff11e0a68e4040d3dc5c07";

  $(".embed-widget").each(function() {
    var $widget = $(this);
    var $search = $widget.find("input");
    var $preview = $("<div>", {"class": "preview"}).hide();
    $search.after($preview);

    var url = function() {
      return $search.val();
    };

    var loading = function(is_loading) {
      $widget.toggleClass("loading", is_loading);
    };

    var preview = function(code) {
      if(code) $preview.html(code).show();
      else     $preview.empty().hide();
    };

    var update_preview = function() {
      preview(false);

      /* does the url look valid-ish? */
      if(window.embedlyURLre.test(url())) {
        loading(true);

        $.embedly(url(), {
          "key": EMBEDLY_KEY,
          "maxWidth": $search.outerWidth(),
          "success": function(oembed, dict) {

            /* do nothing if the search url is has changed since this request
            |* was started. the jquery+embedly plugin doesn't provide access to
            |* the jqXHR object, so we can't cancel it. */
            if(dict.url == url()) {
              preview(oembed.code);
              loading(false);
            }
          },
          "error": function(node, dict) {
            loading(false);
          }
        });
      };
    };

    /* update the preview whenever the search url changes. */
    $search.bind(
      "keyup keydown change",
      _.debounce(update_preview, 300)
    );

    /* and update it now, in case it is prepopulated. */
    update_preview();
  });
});