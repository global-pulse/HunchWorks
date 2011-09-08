function init()
{
	var userId = document.getElementById('userId').getAttribute('user');
	var collaboratorsUrl = '/hunchworks/user/' + userId + '/collaborators';
		
	$('#id_group_collaborators').tokenInput( collaboratorsUrl,
		{ preventDuplicates: true });
	
}

$(document).ready(init);