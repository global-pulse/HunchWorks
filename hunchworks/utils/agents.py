#!/usr/bin/env python
# vim: et ts=4 sw=4


import sys
from compiler.ast import flatten
from django.utils import importlib
from django.conf import settings


def spawn_engine(agent_name):
    """
    Return a configured instance of the engine powering the agent named
    ``agent_name``. The configuration is fetched from the INSTALLED_AGENTS
    setting.
    
    The output of this method is not cached, so spawning multiple instances of
    the same agent+engine may cause problems if the engine expects exclusive
    access to a resource.
    """

    class_name, kwargs = _agent_config(agent_name)
    return _import(class_name)(name=agent_name, **kwargs)


def _agent_config(agent_name):
    """
    Return a tuple containing the engine class and configuration (a dict) of
    ``agent_name`` from the INSTALLED_AGENTS setting. All of the keys of the
    configuration are lower-cased before being returned.
    """

    config = settings.INSTALLED_AGENTS[agent_name]
    return (config.pop("ENGINE"), _lower_keys(config))


def _lower_keys(dict_):
    """
    Return a shallow copy of ``dict_`` with the keys in lower case.
    """

    return dict([
        (key.lower(), val)
        for key, val in dict_.iteritems()
    ])


def _import(class_name):
    """
    Import and return ``class_name``, or None if it does not exist. Any
    exceptions raised from within the module (includng ImportError) are allowed
    to propagate. This is useful when optionally importing modules at runtime,
    to avoid silently masking their errors.
    """

    try:
        module_name, attr_name = class_name.rsplit(".", 1)
        module = importlib.import_module(module_name)
        return getattr(module, attr_name)

    except ImportError:
        if sys.exc_info()[2].tb_next.tb_next:
            raise
