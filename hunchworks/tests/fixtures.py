from fixturefactory import BaseFactory, DjangoMixin

import random

from hunchworks.models import UserProfile, Connection, TranslationLanguage, Invitation, Hunch, PRIVACY_CHOICES, Location, Album, Evidence
from django.contrib.auth.models import User
from hunchworks import hunchworks_enums as enums

class AlbumFactory(BaseFactory, DjangoMixin):
    model = Album

    def getparams(self):
        pk = self.getUnusedPk()
        name = "album %s" % pk
        return locals()

class EvidenceFactory(BaseFactory, DjangoMixin):
    model = Evidence

    def getparams(self):
        pk = self.getUnusedPk()
        title = "title %s" % pk
        time_created = "2011-01-01"
        time_modified = "2011-06-06"
        description = "some description of evidence %s" % pk
        location = self.getRandInst(Location)
        creator = self.getRandInst(UserProfile)
        link = 'http://www.google.com'
        return locals()

class HunchFactory(BaseFactory, DjangoMixin):
    model = Hunch

    def getparams(self):
        pk = self.getUnusedPk()
        creator = self.getRandInst(UserProfile)
        time_created = "2011-01-01"
        time_modified = "2011-08-08"
        status = random.choice(enums.HunchStatus.GetChoices())[0]
        title = 'markov %s' % pk
        privacy = random.choice(range(len(PRIVACY_CHOICES)))
        translation_language = self.getRandInst(TranslationLanguage)
        location = self.getRandInst(Location)
        description = 'markov %s' % pk
        return locals()

#class HunchUserFactory(BaseFactory, DjangoMixin): pass

class LocationFactory(BaseFactory, DjangoMixin):
    model = Location

    def getparams(self):
        pk = self.getUnusedPk()
        latitude = self.number()
        longitude = self.number()
        name = 'markov %s' % pk
        return locals()

    def number(self):
        return '%0.2f' % (random.randint(-360,360) + random.random())


class ConnectionFactory(BaseFactory, DjangoMixin):
    model = Connection

    def getparams(self):
        user_profile = self.getRandInst(UserProfile)
        other_user_profile = self.getRandInst(UserProfile)
        status = random.choice(enums.ConnectionStatus.GetChoices())[0]
        return locals()

class UserFactory(BaseFactory, DjangoMixin):
    model = User

    def getparams(self):
        """ Define parameters to create a new object with.
        Return dict"""

        pk = self.getUnusedPk()
        username = 'markov_%s' % pk
        password = username

        return locals()

class UserProfileFactory(BaseFactory, DjangoMixin):
    model = UserProfile

    def getparams(self):
        user = UserFactory().last_obj_created
        pk = user.pk
        title = random.choice(enums.UserTitle.GetChoices())[0]
        email = '%s@testhunchworks.com' % (user.username)
        privacy = random.choice(enums.PrivacyLevel.GetChoices())[0]

        ###blank = True for all below
        bio_text = "Soon to be markov text"
        phone = self.phonenumber()
        skype_name = "%s_onskype" % user.username
        website = self.website(user.username)
        #profile_picture = models.ImageField(upload_to="profile_images", blank=True)
        messenger_service = random.choice(enums.MessangerServices.GetChoices())[0]
        translation_language = self.getRandInst(TranslationLanguage)
        invitation = self.getRandInst(Invitation)

        #ConnectionFactory(uid1=pk, uid2=self.getRandInst(model=UserProfile).pk)
        #roles = Role
        #location_interests = Location
        #skills = Skill
        #languages = Language

        #qualifications = Education
        #courses = Course

        return locals()

    def phonenumber(self):
        return  ''.join([str(random.randint(0,9))
                for x in range(random.choice([7,10,11,13,20]))])
    def website(self, subdomain):
        return  "%s%s%s" % (
                    random.choice(['www.','', 'http://', 'http://www.']),
                    subdomain,
                    random.choice(['.com', '.org', '.me', '.uk', '.it']))

