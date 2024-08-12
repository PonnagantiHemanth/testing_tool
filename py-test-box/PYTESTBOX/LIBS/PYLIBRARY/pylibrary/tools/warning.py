#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.warning

@brief  Warnings management module

@author christophe Roquebert

@date   2018/02/14
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import warnings
import sys

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class IgnoreWarning(object):
    '''
    Function decorator to ignore a warning category
    '''
    _filteredCategories = []

    def __init__(self, *categories):
        '''
        Constructor

        @param  categories [in] (Warning, list) Warning or list of warnings to ignore
        '''
        assert len(categories) > 0, 'At least one category shall be specified'

        for category in categories:
            assert issubclass(category, Warning), 'Unsupported warning type: %s' % category.__name__
            self._filteredCategories.append(category)
        # end for

    # end def __init__

    def __call__(self, func):
        '''
        Caller method

        @param  func [in] (method) Method to decorate

        @return (method) decorated method
        '''
        def newFunc(*args, **kwargs):
            '''
            Implementation of the function wrapper

            This function:
            - backs up the warning registry
            - triggers a warning before proceeding to the actual call.

            @option args   [in] (tuple)  The function arguments
            @option kwargs [in] (dict)   The function keyword arguments

            @return Warning
            '''
            old_registry = {}
            old_registry.update(sys.__dict__.setdefault("__warningregistry__", {}))

            backedUpFilters = warnings.filters[:]
            try:
                for cat in self._filteredCategories:
                    warnings.filterwarnings("ignore", category = cat)
                # end for

                return func(*args, **kwargs)

            finally:
                warnings.filters[:] = backedUpFilters

                new_registry = sys.__dict__.setdefault("__warningregistry__", {})

                if (len(new_registry) != len(old_registry)):
                    # Lookup new keys from the registry
                    old_keys = set(old_registry.keys())
                    new_keys = set(new_registry.keys())
                    for key in (new_keys - old_keys):
                        _, category, _ = key
                        if (isinstance(category, self._filteredCategories)):
                            del new_registry[key]
                        # end if
                    # end for
                # end if
            # end try
        # end def newFunc

        newFunc.__name__ = func.__name__                                                                                #pylint:disable=W0621,W0622
        newFunc.__doc__  = func.__doc__                                                                                 #pylint:disable=W0621,W0622
        newFunc.__dict__.update(func.__dict__)
        return newFunc

    # end def __call__

# end class IgnoreWarning

## The global level monitor. Its name should be ignored by pylint
ignorewarning = IgnoreWarning                                                                                           #pylint:disable=C0103

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
