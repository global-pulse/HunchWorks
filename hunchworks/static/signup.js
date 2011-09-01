function init()
{
	$("#userSkills").tokenInput("/hunchworks/skills/notLanguages", 
			{ preventDuplicates: true });
	
	//code for diplsaying data in the required languages tab
	$("#userLanguages").tokenInput("/hunchworks/skills/languages", 
			{ preventDuplicates: true });
}

$(document).ready(init);