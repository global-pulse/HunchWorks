$.fn.equalHeight = function() {
  var heights = $(this).map(function() {
    return $(this).height();
  });

  var max = Math.max.apply(Math, heights);
  $(this).height(max);
};
