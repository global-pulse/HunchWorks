from django.db import models

PRIVACY_CHOICES = (
	('Hidden', 'Hidden'),
	('Closed', 'Closed'),
	('Open', 'Open'),
)
LANGUAGE_CHOICES = (
	('English', 'English'),
	('Spanish', 'Spanish'),
	('French', 'French'),
	('German', 'German'),
	('Mandarin', 'Mandarin'),
)
ATTACHMENT_TYPES = (
	('Photo', 'Photo'),
	('Link', 'Link'),
	('Video', 'Video'),
)
GROUP_ACCESS_LEVELS = (
	('Admin', 'Admin'),
	('Member', 'Member'),
)
GROUP_CHOICES = (
	('Ad-Hoc', 'Ad-Hoc'),
	('Alumni', 'Alumni'),
	('Complement', 'Complement'),
	('Corporate', 'Corporate'),
	('Interest', 'Interest'),
	('Non-Profit', 'Non-Profit'),
)
HUNCH_CHOICES = (
	('Confirmed', 'Confirmed'),
	('Denied', 'Denied'),
	('Undetermined', 'Undetermined'),
)

# TODO(Texas:6-15-11) Skills list likely to be needed in future
# TODO(Texas:6-15-11) Expertise list likely to be needed in future
# TODO(Texas:6-15-11) Instant Messanger Types supported list likely needed
# TODO(Texas:6-15-11) Evidence.strength Choices might be needed in future

class Users(models.Model):

    location = models.CharField(
    	max_length=100)
    email = models.CharField(
    	max_length=50)
    first_name = models.CharField(
    	max_length=20, db_column='firstName')
    last_name = models.CharField(
    	max_length=50, db_column='lastName')
    occupation = models.CharField(
    	max_length=50, blank=True)
    expertise = models.CharField(
    	max_length=200, blank=True)
# TODO(Texas:6-15-11) Add Expertise list as choice option when created
    skills = models.CharField(
    	max_length=200, blank=True)
# TODO(Texas:6-15-11) Add Skill list as choice option when created
    invited_by = models.CharField(
    	max_length=1000, db_column='invitedBy', blank=True)
    has_invited = models.CharField(
    	max_length=1000, db_column='hasInvited', blank=True)
    education = models.CharField(
    	max_length=1000, blank=True)
    not_interested_in_finishing_profile = models.IntegerField(
    	db_column='notInterestedInFinishingProfile', default='0')
    languages_known = models.CharField(
    	max_length=200, db_column='languagesKnown', blank=True)
# TODO(Texas:6-15-11) LANGUAGE_CHOICES will eventually needed to be 
# added to this as choice option. In future will be drop down in HTML.
    hometown = models.CharField(
    	max_length=100, blank=True)
    privacy = models.CharField(
    	max_length=10, default='Hidden', choices=PRIVACY_CHOICES)
    preferred_language = models.CharField(
    	max_length=30, db_column='preferredLanguage', choices=LANGUAGE_CHOICES)
    workphone = models.CharField(
    	max_length=30, blank=True)
    location_interests = models.CharField(
    	max_length=200, db_column='locationInterests', blank=True)
    organization = models.CharField(
    	max_length=50, blank=True)
    bio_text = models.CharField(
    	max_length=1000, db_column='bioText', blank=True)
    work_history = models.CharField(
    	max_length=1000, db_column='workHistory', blank=True)
    skype_name = models.CharField(
    	max_length=30, db_column='skypeName', blank=True)
    instant_messanger = models.CharField(
    	max_length=30, db_column='instantMessanger', blank=True)
# TODO(Texas:6-15-11) Add instant messanger option list when created
    website = models.CharField(
    	max_length=100, blank=True)
    profile_picture_location = models.CharField(
    	max_length=100, db_column='profilePictureLocation', blank=True)
    blocked_users = models.CharField(
    	max_length=1000, db_column='blockedUsers', blank=True)
    user_id = models.IntegerField(
    	primary_key=True, db_column='userId', ) 
    class Meta:
        db_table = u'Users'

class Hunch(models.Model):
    time_created = models.DateTimeField(
    	db_column='timeCreated') 
    hunch_confirmed = models.CharField(
    	max_length=20, db_column='hunchConfirmed', default='Undetermined', 
    	choices=HUNCH_CHOICES) 
    creator_id = models.ForeignKey(
    	Users, db_column='creatorId') 
    title = models.CharField(
    	max_length=100 )
    privacy = models.CharField(
    	max_length=10, default='Hidden', choices=PRIVACY_CHOICES)
    invited_users = models.CharField(
    	max_length=1000, db_column='invitedUsers', blank=True) 
    invited_groups = models.CharField(
    	max_length=1000, db_column='invitedGroups', blank=True) 
    additional_invites = models.CharField(
    	max_length=1000, db_column='additionalInvites', blank=True) 
    language = models.CharField(
    	max_length=30, default='English', choices=LANGUAGE_CHOICES)
    location = models.CharField(
    	max_length=100, blank=True)
    tags = models.CharField(
    	max_length=100, blank=True)
    description = models.CharField(
    	max_length=1000, blank=True)
    needed_expertise = models.CharField(
    	max_length=200, db_column='neededExpertise', blank=True)
# TODO(Texas:6-15-11) Add Expertise list when created
    needed_skills = models.CharField(
    	max_length=200, db_column='neededSkills', blank=True)
# TODO(Texas:6-15-11) Add Skills list when created
    needed_languages = models.CharField(
    	max_length=200, db_column='neededLanguages', blank=True)
# TODO(Texas:6-15-11) Add Language list in the future
    hunch_id = models.IntegerField(
    	primary_key=True, db_column='hunchId') 
    class Meta:
        db_table = u'Hunch'

class Album(models.Model):
    album_id = models.IntegerField(
    	primary_key=True, db_column='albumId') 
    hunch_id = models.ForeignKey(
    	Hunch, db_column='hunchId') 
    name = models.CharField(
    	max_length=30, )
    class Meta:
        db_table = u'Album'
        
class Evidence(models.Model):
    hunch_id = models.ForeignKey(
    	Hunch, db_column='hunchId') 
    user_id = models.ForeignKey(
    	Users, db_column='userId') 
    text = models.CharField(
    	max_length=1000, blank=True)
    time_created = models.DateTimeField(
    	db_column='timeCreated') 
    attachment_ids = models.CharField(
    	max_length=1000, db_column='attachmentIds', blank=True) 
    language = models.CharField(
    	max_length=30, blank=True)
# TODO(Texas:6-15-11) Add language list in the future
    strength = models.IntegerField(
    	)
# TODO(Texas:6-15-11) Add Strength choices if created
    evidence_id = models.IntegerField(
    	primary_key=True, db_column='evidenceId') 
    class Meta:
        db_table = u'Evidence'

class Attachments(models.Model):
    hunch_id = models.ForeignKey(
    	Hunch, db_column='hunchId') 
    evidence_id = models.ForeignKey(
    	Evidence, db_column='evidenceId') 
    file_location = models.CharField(
    	max_length=100, db_column='fileLocation') 
    attachment_type = models.CharField(
    	max_length=15, db_column='attachmentType', choices=ATTACHMENT_TYPES) 
    album_id = models.ForeignKey(
    	Album, null=True, db_column='albumId', blank=True) 
    attachment_id = models.IntegerField(
    	primary_key=True, db_column='attachmentId') 
    class Meta:
        db_table = u'Attachments'
        
class Groups(models.Model):
    name = models.CharField(
    	max_length=30)
    group_type = models.CharField(
    	max_length=20, db_column='groupType', choices=GROUP_CHOICES) 
    privacy = models.CharField(
    	max_length=10, default='Hidden', choices=PRIVACY_CHOICES)
    location = models.CharField(
    	max_length=100, blank=True)
    picture_location = models.CharField(
    	max_length=100, db_column='pictureLocation', blank=True) 
    group_id = models.IntegerField(
    	primary_key=True, db_column='groupId') 
    class Meta:
        db_table = u'Groups'

class GroupMembership(models.Model):
    user_id = models.ForeignKey(
    	Users, db_column='userId') 
    group_id = models.ForeignKey(
    	Groups, db_column='groupId') 
    access_level = models.CharField(
    	max_length=10, db_column='accessLevel', default='Member', 
    	choices=GROUP_ACCESS_LEVELS) 
    trust_from_user = models.IntegerField(
    	db_column='trustFromUser') 
    trust_from_group = models.IntegerField(
    	db_column='trustFromGroup') 
    recieve_updates = models.IntegerField(
    	db_column='recieveUpdates') 
    invited_by = models.CharField(
    	max_length=1000, db_column='invitedBy', blank=True) 
    has_invited = models.CharField(
    	max_length=1000, db_column='hasInvited', blank=True) 
    class Meta:
        db_table = u'GroupMembership'

class Messages(models.Model):
    from_user_id = models.ForeignKey(
    	Users, db_column='fromUserId') 
    to_user_id = models.ForeignKey(
    	Users, db_column='toUserId', related_name='%(class)s_toUserId') 
    text = models.CharField(
    	max_length=1000)
    message_id = models.IntegerField(
    	primary_key=True, db_column='messageId') 
    class Meta:
        db_table = u'Messages'

class UserConnections(models.Model):
    user_one_id = models.ForeignKey(
    	Users, db_column='userOneId', related_name='%(class)s_userOneId') 
    user_two_id = models.ForeignKey(
    	Users, db_column='userTwoId', related_name='%(class)s_userTwoId') 
    user_one_following_user_two = models.IntegerField(
    	db_column='userOneFollowingUserTwo') 
    user_two_following_user_one = models.IntegerField(
    	db_column='userTwoFollowingUserOne') 
    user_one_shared_contact_info = models.IntegerField(
    	db_column='userOneSharedContactInfo') 
    user_two_shared_contact_info = models.IntegerField(
    	db_column='userTwoSharedContactInfo') 
    class Meta:
        db_table = u'UserConnections'