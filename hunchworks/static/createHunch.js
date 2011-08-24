function init()
{
	//code for displaying data in related skills tab
	var userSkills = $.getJSON('/hunchworks/skills/1', function(data)
	{
		prePopArray = new Array();
		for(var skill = 0; skill < data.length; skill++)
		{
			prePopArray[skill] = { id: data[skill].id, name: data[skill].name }

		}
		$("#relatedSkills").tokenInput("/hunchworks/skills", { prePopulate: prePopArray, preventDuplicates: true });
	});
	
	//code for diplsaying data in the required languages tab
	var userLanguages = $.getJSON('/hunchworks/languages/1', function(data)
	{
		prePopArray = new Array();
		for(var skill = 0; skill < data.length; skill++)
		{
			prePopArray[skill] = { id: data[skill].id, name: data[skill].name }

		}
		$("#id_languages").tokenInput("/hunchworks/languages", { prePopulate: prePopArray, preventDuplicates: true });
	});
	
	$("#id_tags").tokenInput("/hunchworks/tags", { theme: 'facebook', preventDuplicates: true});
	
	$("#add_tag_button").click( function()
	{
		alert( document.getElementById('token-input-id_tags').value );
		$("#id_tags").tokenInput("add", { name: document.getElementById('token-input-id_tags').value });
	});
	
}

$(document).ready(init);