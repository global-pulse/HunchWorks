
import factory
import random

import hunchworks.models as models
from hunchworks.models import UserProfile
from hunchworks import hunchworks_enums as enums

class HelperMixin(object):
    def handlem2m(model_name, percent):
        """Return list roughly some percent the size of model_name.objects.all()"""
        model = getattr(models, model_name)
        return [x for x in model.objects.all() if random.random() > percent]

    def randInstance(model_name):
        """Return randomly selected instance of possible models"""
        pass # for things like user, translation_language, etc.

class UserProfileFactory(factory.Factory, HelperMixin):
    #user = factory.Sequence(lambda n: str(int(n)+1))
    title = random.choice(enums.UserTitle.GetChoices())[0]
    name = factory.Sequence(lambda n: "Soon to be markov {0}".format(n))
    #email = "%s@testhunchworks.com" % name.split()[0].strip()
    privacy = random.choice(enums.PrivacyLevel.GetChoices())[0]

    #blank = True for all below
    bio_text = "Soon to be markov text"
    phone = ''.join([str(random.randint(0,9))
                    for x in range(random.choice([7,10,11,13,20]))])
    skype_name = "%s_onskype" % name
    website = "%s%s.%s" % (random.choice(['www','', 'http://', 'http://www.']),
                    name,
                    random.choice(['.com', '.org', '.me', '.uk', '.it']))
    #profile_picture = models.ImageField(upload_to="profile_images", blank=True)
    messenger_service = random.choice(enums.MessangerServices.GetChoices())[0]
    translation_language = models.TranslationLanguage.objects.get(pk=random.choice(
                    models.TranslationLanguage.objects.values_list('pk', flat=True)))
    #invitation = random.choice(models.Invitation.objects.values_list('pk', flat=True))

    connections = handlem2m('UserProfile', .5)
    roles = handlem2m('Role', .7)
    location_interests = handlem2m('Location', .7)
    skills = handlem2m('Skill', .7)
    languages = handlem2m('Language', .7)

    qualifications = handlem2m('Education', .7)
    courses = handlem2m('Course', .7)

