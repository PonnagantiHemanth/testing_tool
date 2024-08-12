#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.tools.aliasing
    :brief: Aliasing utility mixin
    :author: Christophe Roquebert
    :date: 2018/10/08
    .. highlight:: python
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
# from new import classobj
from warnings import warn
from types import FunctionType


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ClassProperty(object):
    """
    Wrapper around a getter and setter for accessing a class attribute.
    """
    def __init__(self, getter, setter):
        """
        Constructor

        :param getter: Getter for the property
        :type getter: ``FunctionType``
        :param setter: Setter for the property
        :type setter: ``FunctionType``
        """
        self.getter = getter
        self.setter = setter
    # end def __init__

    def __get__(self, cls, owner):                                   # pylint:disable=W0613
        """
        Actual getter

        :param cls: Target class
        :type cls: ``type``
        :param owner: Required argument
        :type owner: ``object``

        :return: The actual value
        """

        return getattr(cls, self.getter)()
    # end def __get__

    def __set__(self, cls, value):
        """
        Actual getter

        :param cls: Target class
        :type cls: ``type``
        :param value: value to set
        :type value: ``object``
        """
        getattr(cls, self.setter)(value)
    # end def __set__
# end class ClassProperty


class AliasedClassProperty(object):
    """
    Wrapper around a getter and setter for accessing a class attribute.
    """
    def __init__(self, rqn, message=None, category=Warning):
        """
        Constructor

        :param rqn: Relatively-qualified name
        :type rqn: ``tuple of str`` or ``list of str``
        :param message: The warning message. None disables warnings.
        :type message: ``str``
        :param category: The warning category
        :type category: ``type``
        """
        self.rqn = rqn
        self.message = message
        self.category = category
    # end def __init__

    def __get__(self, cls, owner):                                       # pylint:disable=W0613
        """
        Actual getter

        :param cls: Target class
        :type cls: ``type``
        :param owner: Required argument
        :type owner: ``object``

        :return: The actual value
        """
        if self.message is not None:
            warn(self.message, category=self.category, stacklevel=2)
        # end if

        result = cls
        for name in self.rqn:
            result = getattr(result, name)
        # end for

        return result
    # end def __get__

    def __set__(self, cls, value):
        """
        Actual getter

        :param cls: Target class
        :type cls: ``type``
        :param value: value to set
        :type value: ``object``
        """
        if self.message is not None:
            warn(self.message, category=self.category, stacklevel=2)
        # end if

        parent = cls
        for name in self.rqn[:-1]:
            parent = getattr(parent, name)
        # end for

        setattr(parent, self.rqn[-1], value)
    # end def __set__
# end class AliasedClassProperty


def aliases(aliases_dict, parents=(type,), warning_format='%(alias)s is deprecated. Use %(target)s instead.',
            warning_category=DeprecationWarning):
    """
    Declares aliases for class-level properties


    :param aliases_dict: Mapping (old property name->relative new property name)
    :type aliases_dict: ``dict``
    :param parents: List of parent classes for the meta-classed class
    :type parents: ``tuple of type`` or ``list of type``
    :param warning_format: The warning format, with key %(old) and %(new) used to format. None disables warnings
    :type warning_format: ``str``
    :param warning_category: [in] (Type) The type used for warnings

    :return: A class instance, to be used as a metaclass
    """

    parents = tuple([type(p) for p in parents if not isinstance(p, type)])
    if len(parents) == 0:
        parents = (type,)
    # end if

    dct = {}

    for key, value in aliases_dict.items():
        if warning_format is not None:
            message = warning_format % {'alias': key, 'target': value}
        else:
            message = None
        # end if
        dct[key] = AliasedClassProperty(value.split('.'), message, warning_category)
    # end for

    def __new__(mcs, name, bases, cdct):
        """
        Override the __new__ API, injecting aliases.

        :param mcs: The metaclass type
        :type mcs: ``type``
        :param name: The class name
        :type name: ``str``
        :param bases: The base classes
        :type bases: ``tuple of type`` or ``list of type``
        :param cdct: The class dict
        :type name: ``dict``

        :return: A newly created class
        """
        for k, v in dct.items():
            if k != '__new__':
                cdct[k] = v
            # end if
        # end for

        return type.__new__(mcs, name, bases, cdct)
    # end def __new__

    dct['__new__'] = __new__

    meta_aliases = type('MetaAliases', parents, dct)

    return meta_aliases
# end def aliases


def aliased(**aliases_dict):
    """
    Create an aliasing decorator for a function, which maps optional keyword arguments
    to known values.
    This alias DOES NOT raise warnings.

    :param /**aliases_dict: Mapping key ->(position, old key)
    :type /**aliases_dict: ``dict``

    :return: A decorator to be used on the function.

    Example: Assume the following function:
    .. code-block::
        def my_function(self, rivet, rivet_type=None):
            # Do something

    On this function, we would like to have an optional parameter fingerprint
    which maps to rivet, and optional parameter fingerprint_type which maps
    to rivet_type

    The decorator would be used as follows:
    .. code-block::
        @aliased(fingerprint='rivet',     # 1 is the index of the positional argument to replace
                 fingerprint_type='rivet_type') # rivet_type is the name of the keyword argument to replace
        def my_function(self, rivet, rivet_type = None):
            # Do something
    """

    # This is the actual decorator that will be used on the function.
    def decorator(function):
        """
        The decorator function.

        :param function: The function to decorate
        :type function: ``FunctionType``

        :return: The function wrapper
        """

        # This will replace the function, filtering/remapping the optional arguments
        # to the appropriate values
        def wrapper(*args, **kwargs):
            """
            Wrapper for the decorated function

            :param args: All function arguments
            :type args: ``tuple``
            :param kwargs: All function keyword arguments
            :type kwargs: ``dict``

            :return: The function result
            """
            new_kw_args = dict(kwargs)
            for sourceKey, sourceValue in kwargs.items():
                if sourceKey in aliases_dict:
                    # Remove the extraneous parameter from the target kwArgs
                    del new_kw_args[sourceKey]

                    # The target is in the positional arguments
                    target_key = aliases_dict[sourceKey]
                    if target_key in new_kw_args:
                        # This is an error case: Explain why this is a problem.
                        # List all sourceKey that have the same alias
                        source_keys = sorted((key for key, value in aliases_dict.items() if (value == target_key) and
                                              (key in kwargs)))
                        raise ValueError('Function %s is called with multiple aliases pointing to the %s parameter: %s'
                                         % (function.__name__, target_key, ', '.join(source_keys)))
                    # end if
                    new_kw_args[target_key] = sourceValue
                # end if
            # end for

            return function(*args, **new_kw_args)
        # end def wrapper

        wrapper.__name__ = function.__name__                                # pylint:disable=W0621,W0622
        wrapper.__doc__ = function.__doc__                                  # pylint:disable=W0621,W0622
        wrapper.__dict__.update(function.__dict__)

        return wrapper
    # end def decorator

    return decorator
# end def aliased

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
