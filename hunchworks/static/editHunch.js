function init()
{
	//code for displaying data in related skills tab
	var hunch_id = document.getElementById('hunch_id').getAttribute('hunch');
	var skill_url = '/hunchworks/hunch/' + hunch_id + "/skills/notLanguages";
	var language_url = '/hunchworks/hunch/' + hunch_id + "/skills/languages";
	var userSkills = $.getJSON(skill_url, function(data)
	{
		prePopArray = new Array();
		for(var skill = 0; skill < data.length; skill++)
		{
			prePopArray[skill] = { id: data[skill].id, name: data[skill].name }
		}
		$("#relatedSkills").tokenInput("/hunchworks/skills/notLanguages", 
			{ prePopulate: prePopArray, preventDuplicates: true });
	});
	
	//code for diplsaying data in the required languages tab
	var userLanguages = $.getJSON(language_url, function(data)
	{
		prePopArray = new Array();
		for(var skill = 0; skill < data.length; skill++)
		{
			prePopArray[skill] = { id: data[skill].id, name: data[skill].name }
		}
		$("#id_languages").tokenInput("/hunchworks/skills/languages",
			{ prePopulate: prePopArray, preventDuplicates: true });
	});
	
	$("#tags").tokenInput("/hunchworks/tags", 
		{ theme: 'facebook', preventDuplicates: true});
	
	$("#add_tag_button").click( function()
	{
		alert( document.getElementById('token-input-tags').value );
		$("#tags").tokenInput("add", 
			{ name: document.getElementById('token-input-tags').value });
	});
}

$(document).ready(init);