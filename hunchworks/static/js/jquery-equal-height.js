$.fn.equalHeight = function() {
  var heights = $(this).map(function() {
    return $(this).outerHeight();
  });

  var max = Math.max.apply(Math, heights);
  $(this).height(max);
};
