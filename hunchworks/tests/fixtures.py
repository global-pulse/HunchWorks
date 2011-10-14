from fixturefactory import BaseFactory, DjangoMixin

import random

from hunchworks.models import UserProfile, Connection, TranslationLanguage, Invitation
from django.contrib.auth.models import User
from hunchworks import hunchworks_enums as enums


class ConnectionFactory(BaseFactory, DjangoMixin):
    model = Connection

    def getparams(self):
        # Must be passed in at time of instantiation
        user_profile_id = self.uid1
        other_user_profile_id = self.uid2

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
        #invitation = self.getRandInst(Invitation)

        #SUPPORT FOR MANY TO MANY: you need to create model objects for each one-to-one
        # in the many-to-many relationship.
        # ALL BELOW ARE MANY TO MANY
        #connections => Connection
        ConnectionFactory(pk, self.getRandInst(model=UserProfile).pk)
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

