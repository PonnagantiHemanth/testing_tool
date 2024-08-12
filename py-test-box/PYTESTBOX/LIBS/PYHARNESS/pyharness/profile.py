#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.profile

@brief  A combination of sorter and filterer, serializable

@author christophe.roquebert

@date   2018/10/17
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.listener          import Listenable
from pyharness.filtering                 import AndFilter
from pyharness.filtering                 import CustomFilter
from pyharness.filtering                 import Filter
from pyharness.filtering                 import MatchesRegexOperator
from pyharness.filtering                 import NilAccessor
from pyharness.filtering                 import OrFilter
from pyharness.filtering                 import SimpleFilter
from pyharness.filtering                 import TestIdAccessor
from pyharness.filtering                 import filterFactory
from pyharness.manipulator               import IsInOperator
from pyharness.manipulator               import NilOperator
from pyharness.manipulator               import StateAccessor
from pyharness.sorting                   import ChainedSorter
from pyharness.sorting                   import SimpleSorter
from pyharness.sorting                   import Sorter
from pyharness.sorting                   import sorterFactory
from pyharness.testmanager               import TestDescriptor

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

def _equals(value1, value2):
    '''
    Comparison utility, able to handle the None values

    @param  value1 [in] (object) The first value to compare
    @param  value2 [in] (object) The second value to compare

    @return (bool) The equality comparison result
    '''

    # Fast reference comparison
    if (value1 is value2):
        return True
    # end if

    # Both are None
    if (    (value1 is None)
        and (value2 is None)):
        return True
    # end if

    # One is None
    if (   (value1 is None)
        or (value2 is None)):
        return False
    # end if

    # Both are not None
    return (value1 == value2)
# end def _equals

class Profile(Listenable):
    '''
    Container for a Sorter and Filterer, named, and able to be serialized.

    Note that the matchCode refers to the body of a lambda function, that can evaluated
    each expression.

    Access to the expression is done through the expr parameter, and the body
    of the expression would be:
    @code
    lambda expr: <expression body>
    @endcode
    where expr is a tuple containing the evaluation of every expression in the filter.
    '''
    XML_TAG              = 'profile'
    XML_ATTR_ID          = 'id'
    XML_ATTR_READONLY    = 'readonly'

    XML_SORTERS_TAG      = 'sorters'
    XML_FILTERS_TAG      = 'filters'
    XML_ATTR_MATCHMETHOD = 'matchall'
    XML_ATTR_MATCHCODE   = 'matchcode'

    MATCH_ALL            = 'all'
    MATCH_ONE            = 'one'
    MATCH_ADVANCED       = 'advanced'

    ACTION_MODIFIED      = 'modified'

    def __init__(self, profileId   = None,
                       sorters     = None,
                       filters     = None,
                       matchMethod = MATCH_ALL,
                       matchCode   = "",
                       readOnly    = False):
        '''
        Constructor

        @option profileId   [in] (str) A unique identifier for this profile
        @option sorters     [in] (tuple<Sorter>) The sorter for this profile.
                                   Defaults to a testId sorter
        @option filters     [in] (tuple<Filter>) The filters for this profile.
                                   Defaults to an all-inclusive filter
        @option matchMethod [in] (str) Whether the search must match all filters, or at
                                   least one.
        @option matchCode   [in] (str) The matching code to be evaluated
        @option readOnly    [in] (bool) Whether the current profile can be edited.
        '''
        Listenable.__init__(self)

        if (sorters is None):
            sorters = []
        # end if

        if (filters is None):
            filters = []
        # end if

        self._profileId   = None
        self._sorters     = []
        self._filters     = []
        self._matchMethod = None
        self._matchCode   = None
        self._readOnly    = None

        self._childrenListener  = lambda x, y: self.notifyListeners(source = self,
                                                                    action = self.ACTION_MODIFIED)

        self.setId(profileId)
        self.setSorters(sorters)
        self.setFilters(filters)
        self.setMatchMethod(matchMethod)
        self.setMatchCode(matchCode)
        self.setReadOnly(readOnly)
    # end def __init__

    def __cmp__(self, other):
        '''
        Comparison method

        @param  other [in] (object) The other instance to compare

        @return (int) The comparison result
        '''
        result = cmp(self._profileId, other._profileId)                                                                 # pylint:disable=W0212
        if (result != 0):
            return result
        # end if

        result = cmp(self._sorters, other._sorters)                                                                     # pylint:disable=W0212
        if (result != 0):
            return result
        # end if

        result = cmp(self._filters, other._filters)                                                                     # pylint:disable=W0212
        if (result != 0):
            return result
        # end if

        result = cmp(self._matchMethod, other._matchMethod)                                                             # pylint:disable=W0212
        if (result != 0):
            return result
        # end if

        return result
    # end def __cmp__

    def __str__(self):
        '''
        Converts the current object to its string representation.

        @return (str) The current object, as a string.
        '''
        return "%s, sorters=(%s), filters=%s, matchMethod=%s" % \
                ( self._profileId,
                  self._sorters is None and "None" or ",".join([str(sorter) for sorter in self._sorters]),
                  self._filters is None and "None" or ",".join([str(sorter) for sorter in self._filters]),
                  self._matchMethod )
    # end def __str__

    def getId(self):
        '''
        Obtains the id for this profile

        @return (str) A unique id for this profile
        '''
        return self._profileId
    # end def getId

    def setId(self, profileId):
        '''
        Sets the unique id for this profile.

        @param  profileId [in] (str) The unique id for this profile.
        '''
        if (not _equals(self._profileId, profileId)):
            self._profileId = profileId

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setId

    def getMatchMethod(self):
        '''
        Obtains the matchMethod filters attribute

        @return (bool) The matchMethod filters attribute
        '''
        return self._matchMethod
    # end def getMatchMethod

    def setMatchMethod(self, matchMethod):
        '''
        Sets the matchMethod filters attribute

        @param  matchMethod [in] (bool) whether a test must match ALL filters, or at least one.
        '''
        if (not _equals(self._matchMethod, matchMethod)):
            self._matchMethod = matchMethod

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setMatchMethod

    def getMatchCode(self):
        '''
        Obtains the matchCode filters attribute

        @return (str) The matchCode filters attribute
        '''
        return self._matchCode
    # end def getMatchCode

    def setMatchCode(self, matchCode):
        '''
        Sets the matchCode filters attribute

        @param  matchCode [in] (str) the code to be evaluated by the advanced filter.
        '''
        if (not _equals(self._matchCode, matchCode)):
            self._matchCode = matchCode

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setMatchCode

    def isReadOnly(self):
        '''
        Obtains the writability of the current object.

        @return (bool) Whether the current object is read-only
        '''
        return self._readOnly
    # end def isReadOnly

    def setReadOnly(self, readOnly):
        '''
        Sets the current object's read-only-ness

        @param  readOnly [in] (bool) Whether the current object is read-only or not.
        '''

        if (self._readOnly != readOnly):
            self._readOnly = readOnly

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setReadOnly

    def getFilters(self):
        '''
        Obtains the filters for this profile

        @return (list) An ordered tuple of filters for this profile.
        '''
        return self._filters
    # end def getFilters

    def setFilters(self, filters):
        '''
        Sets the list of filters for this profile.

        @param  filters [in] (list) The list of filters for this profile.
        '''
        if (self._filters != filters):

            for element in self._filters:
                element.removeListener(self._childrenListener, self.ACTION_MODIFIED)
            # end for


            self._filters = filters

            for element in self._filters:
                element.addListener(self._childrenListener,
                                    self.ACTION_MODIFIED)
            # end for

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setFilters

    def resolveFilters(self):
        '''
        Creates a unique filter predicate, which follows the chain of
        responsibility pattern, based on the current filters and matchMethod parameter

        @return (Filter) A Filter instance, applied to each test.
        '''
        if (self._matchMethod == self.MATCH_ALL):
            return AndFilter(self._filters)

        elif (self._matchMethod == self.MATCH_ONE):
            return OrFilter(self._filters)

        elif (self._matchMethod == self.MATCH_ADVANCED):
            return CustomFilter(self._filters, self._matchCode)

        else:
            raise ValueError("Unknown matching method: %s" % (self._matchMethod,))

        # end if

    # end def resolveFilters

    def getSorters(self):
        '''
        Obtains the sorters for this profile

        @return (list) An ordered tuple of sorters for this profile.
        '''
        return self._sorters
    # end def getSorters

    def setSorters(self, sorters):
        '''
        Sets the list of sorters for this profile.

        @param  sorters [in] (list) The list of sorters for this profile.
        '''
        self._sorters = sorters

        if (self._sorters != sorters):

            for element in self._sorters:
                element.removeListener(self.ACTION_MODIFIED, self._childrenListener)
            # end for


            self._sorters = sorters

            for element in self._sorters:
                element.addListener(self._childrenListener,
                                    self.ACTION_MODIFIED)
            # end for

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setSorters

    def resolveSorters(self):
        '''
        Creates a unique sorter predicate, which follows the chain of
        responsibility pattern, based on the current sorters parameter

        @return (ChainedSorter) A Sorter, applied to a test list.
        '''
        return ChainedSorter(sorters = self._sorters)
    # end def resolveSorters


    def toElement(self, parentElement):
        '''
        Append the current object, serialized to XML, to the parent element.

        @param  parentElement [in] (Element) The element in which to serialize
                                            the current object
        @return (Element) The newly created object
        '''
        document = parentElement
        while document.parentNode:
            document = document.parentNode
        # end while

        childElement = document.createElement(self.XML_TAG)
        parentElement.appendChild(childElement)

        childElement.setAttribute(self.XML_ATTR_ID,       self._profileId)
        childElement.setAttribute(self.XML_ATTR_READONLY, self._readOnly and "true" or "false")

        sortersElement = document.createElement(self.XML_SORTERS_TAG)
        childElement.appendChild(sortersElement)
        for sorterInstance in self._sorters:
            sorterInstance.toElement(sortersElement)
        # end for

        filtersElement = document.createElement(self.XML_FILTERS_TAG)
        childElement.appendChild(filtersElement)
        for filterInstance in self._filters:
            filterInstance.toElement(filtersElement)
        # end for
        filtersElement.setAttribute(self.XML_ATTR_MATCHMETHOD, self._matchMethod)
        filtersElement.setAttribute(self.XML_ATTR_MATCHCODE,   self._matchCode)

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        Creates a new instance of the current class from the specified element.

        @param  element [in] (Element) The element to de-serialize

        @return (Profile) A new sorter instance, from the element.
        '''
        sortersElement = element.getElementsByTagName(cls.XML_SORTERS_TAG)[0]
        sorterElements = sortersElement.getElementsByTagName(Sorter.XML_TAG)
        sorters        = [sorterFactory(sorterElement) for sorterElement in sorterElements]

        filtersElement = element.getElementsByTagName(cls.XML_FILTERS_TAG)[0]
        filterElements = filtersElement.getElementsByTagName(Filter.XML_TAG)
        filters        = [filterFactory(filterElement) for filterElement in filterElements]

        matchMethod    = filtersElement.getAttribute(cls.XML_ATTR_MATCHMETHOD)

        matchCode      = filtersElement.getAttribute(cls.XML_ATTR_MATCHCODE)

        readOnly       = (element.getAttribute(cls.XML_ATTR_READONLY) == 'true')

        return cls(element.getAttribute(cls.XML_ATTR_ID),
                   sorters     = sorters,
                   filters     = filters,
                   matchMethod = matchMethod,
                   matchCode   = matchCode,
                   readOnly    = readOnly)
    # end def fromElement
# end class Profile

DEFAULT_PROFILES = (Profile('DEFAULT',
                            sorters     = [SimpleSorter(False,
                                                        NilAccessor(),
                                                        NilOperator()),],
                            filters     = [SimpleFilter(TestIdAccessor(),
                                                        MatchesRegexOperator(),
                                                        '.*'),],
                            matchMethod = Profile.MATCH_ALL,
                            matchCode   = "True",
                            readOnly    = True),
                    Profile('ERROR_FAILURE',
                            sorters     = [SimpleSorter(False,
                                                        NilAccessor(),
                                                        NilOperator()),],
                            filters     = [SimpleFilter(StateAccessor(),
                                                        IsInOperator(),
                                                        '%s,%s' % (TestDescriptor.STATE_FAILURE,
                                                                   TestDescriptor.STATE_ERROR)),],
                            matchMethod = Profile.MATCH_ALL,
                            matchCode   = "True",
                            readOnly    = True),
                    )

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
