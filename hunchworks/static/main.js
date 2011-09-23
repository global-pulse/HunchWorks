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


function popup(mylink, windowname)
{
	if (! window.focus)
	{
		return true;
	}
	var href;
	if (typeof(mylink) == 'string')
	{
		href=mylink;
		window.open(href, windowname, 'width=400,height=200,scrollbars=yes');
		return false;
	}
	else
	{
		href=mylink.href;
		window.open(href, windowname, 'width=400,height=200,scrollbars=yes');
		return false;
	}
}
