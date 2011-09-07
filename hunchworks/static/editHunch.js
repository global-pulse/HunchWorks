function init()
{
	var hunchId = document.getElementById('hunchId').getAttribute('hunch');
	var userId = document.getElementById('hunchId').getAttribute('user');
	var skillUrl = '/hunchworks/hunch/' + hunchId + "/skills/notLanguages";
	var languageUrl = '/hunchworks/hunch/' + hunchId + "/skills/languages";
	var hunchCollaborators = '/hunchworks/hunch/' + hunchId + '/collaborators';
	var userCollaborators = '/hunchworks/user/' + userId + '/collaborators';
	var tag_url = '/hunchworks/hunch/' + hunchId + '/tags';
	
	//code for displaying data in related skills tab
	var userSkills = $.getJSON(skillUrl, function(data)
	{
		prePopArray = new Array();
		for(var skill = 0; skill < data.length; skill++)
		{
			prePopArray[skill] = { id: data[skill].id, name: data[skill].name }
		}
		$("#id_skills_required").tokenInput("/hunchworks/skills/notLanguages", 
			{ prePopulate: prePopArray, preventDuplicates: true });
	});
	
	//code for diplsaying data in the required languages tab
	var userLanguages = $.getJSON(languageUrl, function(data)
	{
		prePopArray = new Array();
		for(var language = 0; language < data.length; language++)
		{
			prePopArray[language] = { id: data[language].id, name: data[language].name }
		}
		$("#id_languages_required").tokenInput("/hunchworks/skills/languages",
			{ prePopulate: prePopArray, preventDuplicates: true });
	});
	
	//code for diplsaying tags assigned to the hunch
	var hunchTags = $.getJSON(tag_url, function(data)
	{
		prePopArray = new Array();
		for(var tag = 0; tag < data.length; tag++)
		{
			prePopArray[tag] = { id: data[tag].id, name: data[tag].name }
		}
		$("#id_tags").tokenInput("/hunchworks/tags", 
			{ theme: 'facebook', prePopulate: prePopArray, preventDuplicates: true});
	});
	

	//code for diplsaying users assigned to the hunch
	var collaborators = $.getJSON(hunchCollaborators, function(data)
	{
		prePopArray = new Array();
		for(var collaborators = 0; collaborators < data.length; collaborators++)
		{
			prePopArray[collaborators] = 
				{ id: data[collaborators].id, name: data[collaborators].name }
		}
		$('#id_hunch_collaborators').tokenInput( userCollaborators,
			{ prePopulate: prePopArray, preventDuplicates: true });
	});

	
	$("#add_tag_button").click( function()
	{
		alert( document.getElementById('token-input-tags').value );
		$("#tags").tokenInput("add", 
			{ name: document.getElementById('token-input-tags').value });
	});
}

$(document).ready(init);