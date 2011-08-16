function init()
{
	//$.getJSON('/hunchworks/skills', handleSkills);
	$("#relatedSkills").tokenInput("/hunchworks/skills", { theme: 'facebook'});
	$("#id_languages").tokenInput("/hunchworks/languages", { theme: 'facebook'});
	$("#id_tags").tokenInput("/hunchworks/tags", { theme: 'facebook'});
}

function handleSkills(data)
{
	//alert( data['1'] )
	
}

$(document).ready(init);