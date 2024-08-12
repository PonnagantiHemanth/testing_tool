#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.tools.tag

@brief Tag decorators

This module contains the base implementation of the tag-based decorators.

These decorators allows developers to mark test methods ('tag') and later
collect the list of methods tagged by this mechanism.

This can be useful for associating levels to test scripts, but also other extra data.

@author christophe.roquebert

@date   2018/12/07
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from threading                          import RLock
from types                              import MethodType

from pylibrary.tools.threadutils       import synchronized


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
SYNCHRONIZATION_LOCK = RLock()

class Tag(object):
    '''
    Function decorator, that associates a tag with a function definition.

    This can be used in tests, on test methods, to declare a test tag.

    Example:
    @code
    from pyharness.extensions import PyHarnessCase
    from pyharness.extensions import tag
    class MyTest(PyHarnessCase):

        @tag("minimal")
        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example
    # end class MyTest
    @endcode

    The above code is equivalent to:
    @code
    from pyharness.extensions import PyHarnessCase
    from pyharness.extensions import tag
    class MyTest(PyHarnessCase):

        def test_Example(self):
            self.fail("Test not implemented")
        # end def test_Example

        tagAssigner = Tag.__call__(tag, "minimal")
        test_Example = tagAssigner(test_Example)
    # end class MyTest
    @endcode
    '''

    __TAGS_REPOSITORY = {}

    __EMPTY_SET = frozenset()

    def __init__(self, tagIdentifier):
        '''
        Constructor

        @param  tagIdentifier [in] (str) Unique identifier for the tags.
        '''
        self._tagToIds = {}
        self._idToTags = {}
        self._tagSet   = None
        self._tagHelp  = {}

        with SYNCHRONIZATION_LOCK:
            assert tagIdentifier not in self.__TAGS_REPOSITORY
            self.__TAGS_REPOSITORY[tagIdentifier] = self
        # end with
    # end def __init__

    @classmethod
    @synchronized(SYNCHRONIZATION_LOCK)
    def getTagRepositories(cls):
        '''
        Obtains a copy of the dict of tag repositories

        @return A copy of the tag repositories dict
        '''
        result = dict(cls.__TAGS_REPOSITORY)

        return result
    # end def getTagRepositories


    def __call__(self, *tagValues):
        r'''
        tag decorator call function

        @param  tagValues [in] (tuple) list of tags the following function will be associated with

        @return An inner decorator that associates the function with the tag.

        @note   This function will be called when using a
                <code>\@tag(...)</code> decorator.
        '''
        if (self._tagSet is not None):
            for tagValue in tagValues:
                if (tagValue not in self._tagSet):
                    raise ValueError('Value %s is not allowed for a %s' % (tagValue, self.__class__.__name__.lower()))
                # end if
            # end for
        # end if

        def tagAssigner(f):
            '''
            Inner decorator, that performs the actual association.

            @param  f [in] (MethodType) The function to decorate with the tag

            @return The decorated function (Same as the input)
            '''
            fId = id(f)
            SYNCHRONIZATION_LOCK.acquire()
            try:
                for tagValue in tagValues:
                    ids = self._tagToIds.get(tagValue, None)
                    if (ids is None):
                        ids = set()
                        self._tagToIds[tagValue] = ids
                    # end if
                    ids.add(fId)

                    tags = self._idToTags.get(fId, None)
                    if (tags is None):
                        tags = set()
                        self._idToTags[fId] = tags
                    # end if
                    tags.add(tagValue)
                # end for
            finally:
                SYNCHRONIZATION_LOCK.release()
            # end try

            return f
        # end def tagAssigner

        return tagAssigner
    # end def __call__

    @staticmethod
    def __realFunction(f):
        '''
        Extracts the inner FunctionType object from a MethodType object.

        @param  f [in] (MethodType) A MethodType object, from which the
                                    FunctionType object is extracted

        @return The FunctionType object associated with the parameter
        '''
        func = f
        while (isinstance(func, MethodType)):
            func = func.__func__
        # end while

        return func
    # end def __realFunction

    @synchronized(SYNCHRONIZATION_LOCK)
    def getTags(self, f = None):
        '''
        Obtains the list of tags for which a function is registered.

        @option f [in] (FunctionType) The function to check, None to obtain _all_ tags

        @return The list of registered tags
        '''
        if (f is not None):
            func = self.__realFunction(f)
            fId = id(func)

            return self._idToTags.get(fId, self.__EMPTY_SET)
        else:
            result = list(self._tagToIds.keys())
        # end if

        return result
    # end def getTags

    def hasTag(self, f, tags):
        '''
        Tests whether a function is associated with a set of tags.

        @param  f    [in] (MethodType) The MethodType object to test
        @param  tags [in] (tuple)      The list of tags to test against

        @return True if the function has been registered with one of the tags
                with the @@tag decorator
        '''
        func = self.__realFunction(f)
        fId = id(func)

        if (isinstance(tags, str)):
            tags = (tags,)
        # end if

        tagSet = set(tags)

        return len(self._idToTags.get(fId, set()).intersection(tagSet)) != 0
    # end def hasTag

    def definesTag(self, f):
        '''
        Tests whether a function has defined a tag.

        @param  f [in] (FunctionType) The function to test

        @return True if the function has defined a tag with the @@tag
                decorator
        '''
        func = self.__realFunction(f)
        fId = id(func)

        return fId in self._idToTags
    # end def definesTag

    def restrictTags(self, tags):
        '''
        Restricts the tags to a list of predefined values.

        @param  tags [in] (List) of values to restrict to
        '''
        self._tagSet = set(tags)
    # end def restrictTags

    def setHelp(self, tag, help):                                                                                       #@ReservedAssignment pylint:disable=W0622
        '''
        Sets the help string associated with a tag.

        @param  tag  [in] (str) The tag value
        @param  help [in] (str) The help string
        '''
        self._tagHelp[tag] = help
    # end def setHelp

    def getHelp(self, tag = None):
        '''
        Obtains the help string associated with the tag, or None if no help is defined.

        @option tag [in] (str) The tag value

        @return The associated help string, or None if not defined.
        '''
        if (tag is None):
            result = self._tagHelp
        else:
            result = self._tagHelp.get(tag, None)
        # end if

        return result
    # end def getHelp

# end class Tag

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
