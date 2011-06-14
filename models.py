# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.

from django.db import models

class Album(models.Model):
    albumid = models.IntegerField(primary_key=True, db_column='albumId') # Field name made lowercase.
    hunchid = models.ForeignKey(Hunch, db_column='hunchId') # Field name made lowercase.
    name = models.CharField(max_length=90)
    class Meta:
        db_table = u'Album'

class Attachments(models.Model):
    hunchid = models.ForeignKey(Hunch, db_column='hunchId') # Field name made lowercase.
    evidenceid = models.ForeignKey(Evidence, db_column='evidenceId') # Field name made lowercase.
    filelocation = models.CharField(max_length=300, db_column='fileLocation') # Field name made lowercase.
    attachmenttype = models.CharField(max_length=15, db_column='attachmentType') # Field name made lowercase.
    albumid = models.ForeignKey(Album, null=True, db_column='albumId', blank=True) # Field name made lowercase.
    attachmentid = models.IntegerField(primary_key=True, db_column='attachmentId') # Field name made lowercase.
    class Meta:
        db_table = u'Attachments'

class Evidence(models.Model):
    hunchid = models.ForeignKey(Hunch, db_column='hunchId') # Field name made lowercase.
    userid = models.ForeignKey(Users, db_column='userId') # Field name made lowercase.
    text = models.CharField(max_length=3000, blank=True)
    timecreated = models.DateTimeField(db_column='timeCreated') # Field name made lowercase.
    attachmentids = models.CharField(max_length=3000, db_column='attachmentIds', blank=True) # Field name made lowercase.
    language = models.CharField(max_length=90, blank=True)
    strength = models.IntegerField()
    evidenceid = models.IntegerField(primary_key=True, db_column='evidenceId') # Field name made lowercase.
    class Meta:
        db_table = u'Evidence'

class Groupmembership(models.Model):
    userid = models.ForeignKey(Users, db_column='userId') # Field name made lowercase.
    groupid = models.ForeignKey(Groups, db_column='groupId') # Field name made lowercase.
    accesslevel = models.CharField(max_length=18, db_column='accessLevel') # Field name made lowercase.
    trustfromuser = models.IntegerField(db_column='trustFromUser') # Field name made lowercase.
    trustfromgroup = models.IntegerField(db_column='trustFromGroup') # Field name made lowercase.
    recieveupdates = models.IntegerField(db_column='recieveUpdates') # Field name made lowercase.
    invitedby = models.CharField(max_length=3000, db_column='invitedBy', blank=True) # Field name made lowercase.
    hasinvited = models.CharField(max_length=3000, db_column='hasInvited', blank=True) # Field name made lowercase.
    class Meta:
        db_table = u'GroupMembership'

class Groups(models.Model):
    name = models.CharField(max_length=90)
    grouptype = models.CharField(max_length=30, db_column='groupType') # Field name made lowercase.
    privacy = models.CharField(max_length=18)
    location = models.CharField(max_length=300, blank=True)
    picturelocation = models.CharField(max_length=300, db_column='pictureLocation', blank=True) # Field name made lowercase.
    groupid = models.IntegerField(primary_key=True, db_column='groupId') # Field name made lowercase.
    class Meta:
        db_table = u'Groups'

class Hunch(models.Model):
    timecreated = models.DateTimeField(db_column='timeCreated') # Field name made lowercase.
    hunchconfirmed = models.CharField(max_length=27, db_column='hunchConfirmed', blank=True) # Field name made lowercase.
    creatorid = models.ForeignKey(Users, db_column='creatorId') # Field name made lowercase.
    title = models.CharField(max_length=300)
    privacy = models.CharField(max_length=18)
    invitedusers = models.CharField(max_length=3000, db_column='invitedUsers', blank=True) # Field name made lowercase.
    invitedgroups = models.CharField(max_length=3000, db_column='invitedGroups', blank=True) # Field name made lowercase.
    additionalinvites = models.CharField(max_length=3000, db_column='additionalInvites', blank=True) # Field name made lowercase.
    language = models.CharField(max_length=90)
    location = models.CharField(max_length=300, blank=True)
    tags = models.CharField(max_length=300, blank=True)
    description = models.CharField(max_length=3000)
    neededexpertise = models.CharField(max_length=600, db_column='neededExpertise', blank=True) # Field name made lowercase.
    neededskills = models.CharField(max_length=600, db_column='neededSkills', blank=True) # Field name made lowercase.
    neededlanguages = models.CharField(max_length=600, db_column='neededLanguages', blank=True) # Field name made lowercase.
    hunchid = models.IntegerField(primary_key=True, db_column='hunchId') # Field name made lowercase.
    class Meta:
        db_table = u'Hunch'

class Messages(models.Model):
    fromuserid = models.ForeignKey(Users, db_column='fromUserId') # Field name made lowercase.
    touserid = models.ForeignKey(Users, db_column='toUserId') # Field name made lowercase.
    text = models.CharField(max_length=3000)
    messageid = models.IntegerField(primary_key=True, db_column='messageId') # Field name made lowercase.
    class Meta:
        db_table = u'Messages'

class Userconnections(models.Model):
    useroneid = models.ForeignKey(Users, db_column='userOneId') # Field name made lowercase.
    usertwoid = models.ForeignKey(Users, db_column='userTwoId') # Field name made lowercase.
    useronefollowingusertwo = models.IntegerField(db_column='userOneFollowingUserTwo') # Field name made lowercase.
    usertwofollowinguserone = models.IntegerField(db_column='userTwoFollowingUserOne') # Field name made lowercase.
    useronesharedcontactinfo = models.IntegerField(db_column='userOneSharedContactInfo') # Field name made lowercase.
    usertwosharedcontactinfo = models.IntegerField(db_column='userTwoSharedContactInfo') # Field name made lowercase.
    class Meta:
        db_table = u'UserConnections'

class Users(models.Model):
    location = models.CharField(max_length=300)
    email = models.CharField(max_length=150)
    firstname = models.CharField(max_length=60, db_column='firstName') # Field name made lowercase.
    lastname = models.CharField(max_length=150, db_column='lastName') # Field name made lowercase.
    occupation = models.CharField(max_length=150, blank=True)
    expertise = models.CharField(max_length=600, blank=True)
    skills = models.CharField(max_length=600, blank=True)
    invitedby = models.CharField(max_length=3000, db_column='invitedBy', blank=True) # Field name made lowercase.
    hasinvited = models.CharField(max_length=3000, db_column='hasInvited', blank=True) # Field name made lowercase.
    education = models.CharField(max_length=3000, blank=True)
    notinterestedinfinishingprofile = models.IntegerField(db_column='notInterestedInFinishingProfile') # Field name made lowercase.
    languagesknown = models.CharField(max_length=600, db_column='languagesKnown', blank=True) # Field name made lowercase.
    hometown = models.CharField(max_length=300, blank=True)
    privacy = models.CharField(max_length=18)
    preferredlanguage = models.CharField(max_length=90, db_column='preferredLanguage', blank=True) # Field name made lowercase.
    workphone = models.CharField(max_length=90, blank=True)
    locationinterests = models.CharField(max_length=600, db_column='locationInterests', blank=True) # Field name made lowercase.
    organization = models.CharField(max_length=150, blank=True)
    biotext = models.CharField(max_length=3000, db_column='bioText', blank=True) # Field name made lowercase.
    workhistory = models.CharField(max_length=3000, db_column='workHistory', blank=True) # Field name made lowercase.
    skypename = models.CharField(max_length=90, db_column='skypeName', blank=True) # Field name made lowercase.
    instantmessanger = models.CharField(max_length=90, db_column='instantMessanger', blank=True) # Field name made lowercase.
    website = models.CharField(max_length=300, blank=True)
    profilepicturelocation = models.CharField(max_length=300, db_column='profilePictureLocation', blank=True) # Field name made lowercase.
    blockedusers = models.CharField(max_length=3000, db_column='blockedUsers', blank=True) # Field name made lowercase.
    userid = models.IntegerField(primary_key=True, db_column='userId') # Field name made lowercase.
    class Meta:
        db_table = u'Users'

