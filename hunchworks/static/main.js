$(function()
{

  var init_token_input = function(class_name, theme)
  {
    $("input." + class_name).each(function()
    {
      var field = $(this);

      field.tokenInput(field.data("search-url"), {
        prePopulate: field.data("prepopulate"),
        preventDuplicates: true,
        animateDropdown: false,
        theme: theme
      });
    });
  };

  init_token_input("tags", "hunchworks");
  init_token_input("skills", "hunchworks");
  init_token_input("languages", "hunchworks");
  init_token_input("userProfiles", "hunchworks");
  init_token_input("members", "hunchworks");
  
  //This sets the data for the plugin to your specific username
  url = document.getElementById("id_user_profiles").getAttribute("data-search-url");
  urlArray = url.split("/")
  urlArray[1] = document.getElementById("hunchId").getAttribute("user");
  url = urlArray[0].concat("/", urlArray[1], "/", urlArray[2]);
  document.getElementById("id_user_profiles").setAttribute("data-search-url", url)
  
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
