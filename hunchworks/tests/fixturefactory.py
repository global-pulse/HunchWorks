import random

from hunchworks.models import UserProfile, TranslationLanguage, Invitation
from django.contrib.auth.models import User
from hunchworks import hunchworks_enums as enums

class FactoryMixin(object):
    """Base Class for creating django objects

    Child classes must adhere to the following template:

    class Child(FactoryMixin):
        model = django.contrib.auth.models.User
        def getparams(self): return {}

    *model is the class we are mass producing
    *getparams: see FactoryMixin.getparams.__doc__
    """

    def getparams(cls):
        """Template method: must be defined by child class.
        Return dict of params that get sent to self.create()

        Example logic:

        pk = self.getUnusedPk() # optional
        username = 'markov_%s' % pk
        password = username

        return locals()
        """
        raise NotImplementedError('You cannot directly instantiate FactoryMixin '
                           'or call this method directly')

    def __init__(self, save_to_db=True):
        """Create new instance of a model by calling getparams in child class.
        Don't call directly.  Don't instantiate FactoryMixin directly"""

        # Get dict of params for object to create
        dict_ = self.getparams()

        # Check and prep dict_ as necessary
        if dict_ == None: raise ValueError("Expected dict, got None. "
                            "self.getparams() is missing a return value")
        try: del dict_['self'] # we don't want to pass this around
        except: pass

        # Create model object
        self.last_obj_created = self.create(save_to_db=save_to_db, **dict_)

    def __repr__(self):
        return "%s: Last created <%s>" % (self.__class__.__name__, str(self.last_obj_created))

    def create(self, save_to_db=True, **kwargs):
        """Basically a wrapper to Django's model.objects.create method."""
        inst = self.model(**kwargs)
        if save_to_db:
            inst.save()
        return inst


    def _getmodel(self, model=None):
        if model == None:
            return self.model
        return model

    def getSome(self, percent, model=None):
        """Return list of model objects with len equal to
        some percent the len of self.model.objects.all()"""
        model = self._getmodel(model)
        if isinstance(percent, int):
            percent = percent * .1
        percent = 1 - percent

        return [x for x in self.model.objects.all() if random.random() > percent]

    def getPks(self, model=None):
        """Get flattened list of primary keys"""
        model = self._getmodel(model)
        pks = model.objects.values_list('pk', flat=True)
        return pks

    def getUnusedPk(self, model=None):
        """Get minimum possible unused primary key"""
        a = set(self.getPks(model))
        b = set(range(min(a), max(a)+2))
        return min(b.difference(a))

    def getRandInst(self, model=None):
        """Return randomly selected instance of possible models"""
        model = self._getmodel(model)
        pks = self.getPks(model)
        if not pks:
            raise IndexError('No primary keys for model: %s' % model)
        return model.objects.get(pk=random.choice(pks))

    #def newInstance(self, model=None):
        #""""return self.model.objects.get(pk=sorted(pks)[-1])

class UserFactory(FactoryMixin):
    model = User

    def getparams(self):
        """ Define parameters to create a new object with.
        Return dict"""

        pk = self.getUnusedPk()
        username = 'markov_%s' % pk
        password = username

        return locals()

class UserProfileFactory(FactoryMixin):
    model = UserProfile
    def phonenumber(self):
        return  ''.join([str(random.randint(0,9))
                for x in range(random.choice([7,10,11,13,20]))])
    def website(self, subdomain):
        return  "%s%s%s" % (random.choice(['www.','', 'http://', 'http://www.']),
                        subdomain,
                        random.choice(['.com', '.org', '.me', '.uk', '.it']))

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

        #NO SUPPORT FOR MANY TO MANY YET. need to create multiple Connection,
        # ALL BELOW ARE MANY TO MANY
        #connections = ??? # don't know how to do connections
        #roles = Role
        #location_interests = Location
        #skills = Skill
        #languages = Language

        #qualifications = Education
        #courses = Course

        return locals()
