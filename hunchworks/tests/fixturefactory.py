import random

class BaseFactory(object):
    """Base Class for creating django objects """

    # parameters to instantiate an object.
    # may be overridden by childcls's getparams() method
    default_params = dict(save_to_db=True, )
    last_obj_created = 'None'

    def getparams(cls):
        """Template method: must be overridden by child class.
        Return dict of params that get sent to self.create()

        Example logic:

        pk = self.getUnusedPk() # optional
        username = 'markov_%s' % pk
        password = username

        return locals()
        """
        raise NotImplementedError(
                'You cannot directly instantiate BaseFactory '
                'or call this method directly')

    def __init__(self, *args, **kwargs):
        """Create new instance of a model by calling getparams in child class.
        Don't call directly.  Don't instantiate BaseFactory directly.

        Any given params are passed to cls.getparams(*args, **kwargs)"""

        #add kwargs as class vars.  This means getparams() can use
        # any kwargs passed in at time of instantiation.  kwargs won't
        # get explicitly passed to django unless set in getparams()
        # (or by overriding __init__ in the child)
        self.__dict__.update(**kwargs)

        # Get dict of params necessary to create object
        dict_ = self.default_params
        dict_.update(self.getparams())

        # Check and prep dict_ as necessary
        try: del dict_['self'] # we don't want to pass this around
        except: pass

        # Create model object
        self.last_obj_created = self.create(**dict_)

    def __repr__(self):
        return "%s: last_obj_created <%s>" % (
                self.__class__.__name__, str(self.last_obj_created))

    def create(self, save_to_db=True, **kwargs):
        """A wrapper that uses self.model to create an instance of
        self.model.  Assumes this works: inst=model(**kwargs) and inst.save()

        In Django, this would wrap Django's
        model.objects.create(**kwargs) method."""

        inst = self.model(**kwargs)
        if save_to_db:
            inst.save()
        return inst

class DjangoMixin(object):
    """Useful/Necessary methods for Fixture Factories"""
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
        rv = [x for x in self.model.objects.all() if random.random() > percent]
        return rv

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


