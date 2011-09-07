function init()
{
	$("#id_skills").tokenInput("/hunchworks/skills/notLanguages", 
			{ preventDuplicates: true });
	
	//code for diplsaying data in the required languages tab
	$("#id_languages").tokenInput("/hunchworks/skills/languages", 
			{ preventDuplicates: true });
}

$(document).ready(init);