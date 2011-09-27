$(function() {

  $("div.loc-widget").each(function() {
    var $widget = $(this);
    var map = null;

    $widget.find("ul.type li").click(function() {
      var type_name = $(this).data("type");
      var clicked = this;

      /* Activate the clicked type link, and deactivate the others. */
      $(this).closest("ul").find("li").each(function() {
        $(this).toggleClass("active", this==clicked);
      });

      /* Show the clicked type widget, and hide the others. */
      $widget.children("div").each(function() {
        $(this).toggleClass("hidden", !$(this).hasClass(type_name));
      });

      /* If the 'map' type was clicked for the first time, initialize the map.
      |* (To avoid doing it during startup if it's not used.) */
      if(type_name == "map" && map === null) {
        $widget.find("div.map").each(function() {
          if(window.google) {

            map = new google.maps.Map(this, {
              "mapTypeId": google.maps.MapTypeId.TERRAIN,
              "center": new google.maps.LatLng(30, 0),
              "zoom": 3
            });

            var marker = new google.maps.Marker();

            /* Update the latitude and longitude when the map is clicked. */
            google.maps.event.addListener(map, "click", function(event) {
              $widget.find("input.lat").val(event.latLng.lat());
              $widget.find("input.lng").val(event.latLng.lng());

              marker.setOptions({
                "animation": google.maps.Animation.DROP,
                "position": event.latLng,
                "map": map
              });
            });

          /* if Google Maps isn't available (e.g. we're running offline), show
          |* an error rather than a map. */
          } else {
            $(this).addClass("error").html(
              "<div>Google Maps is not available.</div>"
            );
          }
        });
      }
    });

    /* Clear the latitude and longitude when the name is changed. This will
    |* probably be replaced with the Google geocoding API eventually. */
    $widget.find("input.name").keypress(function() {
      $widget.find("input.lat, input.lng").val("");
    });
  });
});