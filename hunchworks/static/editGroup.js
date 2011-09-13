function init()
{
	var groupId = document.getElementById('groupId').getAttribute('group');
	var userId = document.getElementById('groupId').getAttribute('user');
	var groupCollaborators = '/group/' + groupId + '/collaborators';
	var userCollaborators = '/user/' + userId + '/collaborators';

	//code for diplsaying users assigned to the hunch
	var collaborators = $.getJSON(groupCollaborators, function(data)
	{
		prePopArray = new Array();
		for(var collaborators = 0; collaborators < data.length; collaborators++)
		{
			prePopArray[collaborators] = 
				{ id: data[collaborators].id, name: data[collaborators].name }
		}
		$('#id_group_collaborators').tokenInput( userCollaborators,
			{ prePopulate: prePopArray, preventDuplicates: true });
	});
}

$(document).ready(init);