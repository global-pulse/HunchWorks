function init()
{
	var userId = document.getElementById('userId').getAttribute('user');
	var skillUrl = '/hunchworks/user/' + userId + '/skills/notLanguages';
	var languageUrl = '/hunchworks/user/' + userId + '/skills/languages';
	var collaboratorsUrl = '/hunchworks/user/' + userId + '/collaborators';
	
	//code for displaying data in related skills tab
	var userSkills = $.getJSON(skillUrl, function(data)
	{
		prePopArray = new Array();
		for(var skill = 0; skill < data.length; skill++)
		{
			prePopArray[skill] = { id: data[skill].id, name: data[skill].name }

		}
		$('#id_skills_required').tokenInput('/hunchworks/skills/notLanguages', 
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
		$('#id_languages_required').tokenInput('/hunchworks/skills/languages', 
			{ prePopulate: prePopArray, preventDuplicates: true });
	});
	
	$('#id_tags').tokenInput('/hunchworks/tags', 
		{ theme: 'facebook', preventDuplicates: true });
		
	$('#id_hunch_collaborators').tokenInput( collaboratorsUrl,
		{ preventDuplicates: true });
	
	$('#add_tag_button').click( function()
	{
		alert( document.getElementById('token-input-tags').value );
		$('#tags').tokenInput('add', 
			{ name: document.getElementById('token-input-tags').value });
	});
	
}

$(document).ready(init);