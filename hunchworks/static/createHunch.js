function init()
{
	//$.getJSON('/hunchworks/skills', handleSkills);
	$("#relatedSkills").tokenInput("/hunchworks/skills", { theme: 'facebook'});
}

function handleSkills(data)
{
	//alert( data['1'] )
	
}

$(document).ready(init);