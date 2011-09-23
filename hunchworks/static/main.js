$(function() {
  $("input.token-input").each(function() {
    var field = $(this);

    field.tokenInput(field.data("search-url"), {
      prePopulate: field.data("prepopulate"),
      preventDuplicates: true,
      animateDropdown: false,
      theme: "hunchworks"
    });
  });
});
