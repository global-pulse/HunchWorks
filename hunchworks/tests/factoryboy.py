
import factory
import random

import hunchworks.models
from django.contrib.auth.models import User
from hunchworks.models import UserProfile

from hunchworks import hunchworks_enums as enums

class HelperMixin(object):
    def handlem2m(self, model_name, percent):
        """Return list roughly some percent the size of model_name.objects.all()"""
        model = getattr(hunchworks.models, model_name)
        return [x for x in model.objects.all() if random.random() > percent]

    def getpks(self, model_name):
        """Get flattened list of primary keys"""
        model = getattr(hunchworks.models, model_name)
        pks = model.objects.values_list('pk', flat=True)
        return pks, model

    def randInstance(self, model_name):
        """Return randomly selected instance of possible models"""
        pks, model = self.getpks(model_name)
        return model.objects.get(pk=random.choice(pks))

    #def newInstance(model_name):
        #""""return model.objects.get(pk=sorted(pks)[-1])

helpers = HelperMixin()

_name ="markov"

class UserFactory(factory.Factory):
    username = factory.Sequence(lambda n: '%s_%s' % (_name, n))
    password = _name

class UserProfileFactory(factory.Factory):
    user = factory.LazyAttribute(lambda a: UserFactory())
    #title = random.choice(enums.UserTitle.GetChoices())[0]
    #email = factory.LazyAttribute(lambda a: '{0}@testhunchworks.com'.format(a.user.username))
    #privacy = random.choice(enums.PrivacyLevel.GetChoices())[0]

    ##blank = True for all below
    ##bio_text = "Soon to be markov text"
    ##phone = ''.join([str(random.randint(0,9))
                    ##for x in range(random.choice([7,10,11,13,20]))])
    ##skype_name = "%s_onskype" % _name
    ##website = "%s%s.%s" % (random.choice(['www','', 'http://', 'http://www.']),
                    ##_name,
                    ##random.choice(['.com', '.org', '.me', '.uk', '.it']))
    ###profile_picture = models.ImageField(upload_to="profile_images", blank=True)
    ##messenger_service = random.choice(enums.MessangerServices.GetChoices())[0]
    #translation_language = helpers.randInstance('TranslationLanguage')
    ###invitation = random.choice(models.Invitation.objects.values_list('pk', flat=True))

    ##connections = self.helpers.handlem2m('UserProfile', .5)
    ##roles = self.helpers.handlem2m('Role', .7)
    ##location_interests = self.helpers.handlem2m('Location', .7)
    ##skills = self.helpers.handlem2m('Skill', .7)
    ##languages = self.helpers.handlem2m('Language', .7)

    ##qualifications = self.helpers.handlem2m('Education', .7)
    ##courses = self.helpers.handlem2m('Course', .7)

