#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.filtering

@brief  Sorting and filtering capabilities

Contains the definition of TestSorters and TestFilter, available through the GUI

@author christophe.roquebert

@date   2018/09/18
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.listener          import Listenable
from pyharness.manipulator               import ALL_ACCESSOR_CLASSES as ALL_ACCESSOR_CLASSES_BASE
from pyharness.manipulator               import ContainsOperator
from pyharness.manipulator               import DoesNotContainOperator
from pyharness.manipulator               import DoesNotEndWithOperator
from pyharness.manipulator               import DoesNotMatchRegexOperator
from pyharness.manipulator               import DoesNotStartWithOperator
from pyharness.manipulator               import DurationAccessor
from pyharness.manipulator               import EndsWithOperator
from pyharness.manipulator               import ImplementedTestCasesAccessor
from pyharness.manipulator               import IsEmptyOperator
from pyharness.manipulator               import IsGreaterThanOperator
from pyharness.manipulator               import IsInOperator
from pyharness.manipulator               import IsLessThanOperator
from pyharness.manipulator               import IsNotEmptyOperator
from pyharness.manipulator               import IsNotInOperator
from pyharness.manipulator               import LevelsAccessor
from pyharness.manipulator               import Manipulator
from pyharness.manipulator               import MatchesRegexOperator
from pyharness.manipulator               import MessageAccessor
from pyharness.manipulator               import NilAccessor
from pyharness.manipulator               import StartsWithOperator
from pyharness.manipulator               import StateAccessor
from pyharness.manipulator               import TestIdAccessor

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

ALL_ACCESSOR_CLASSES = [x for x in ALL_ACCESSOR_CLASSES_BASE
                          if x not in (NilAccessor,)]

class Filter(object):
    '''
    Basic definition of a Filter.

    A Filter is a class that filters out instances of TestAccess, by returning True if the
    test is to be accepted, and False otherwise.
    '''

    XML_TAG       = "filter"

    def __call__(self, testAccess,
                       context      = None):
        '''
        Whether the test should be accepted, or filtered out.

        @param  testAccess [in] (TestAccess) A TestAccess instance, providing
                                             access to the test properties
        @option context    [in] (Context)    The Context in which the filter
                                             is to be applied. May be None.

        @return (bool) True if the test is acceptable, False otherwise.
        '''
        raise NotImplementedError
    # end def __call__

    def __eq__(self, other):
        '''
        Compares two filters.

        @param  other [in] (Filter) The filter to compare to

        @return (bool) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, Filter):
            return -1
        # end if
        return (self.XML_TAG == other.XML_TAG)
    # end def __eq__
# end class Filter

class SimpleFilter(Filter, Manipulator):
    '''
    Generic implementation of a filter
    '''

    XML_TYPEID     = "generic"
    XML_ATTR_VALUE = "value"
    XML_VALUE_TAG  = "value"

    def __init__(self, accessor = None,
                       operator = None,
                       value    = None):
        '''
        Constructor.

        @option accessor [in] (Accessor) The accessor for this filter.
        @option operator [in] (Operator) The operator for this filter.
        @option value    [in] (object)   The value, as an input for the operator.
        '''
        Filter.__init__(self)
        Manipulator.__init__(self, accessor, operator, value)
    # end def __init__

    def getAvailableAccessors(self):                                                                                    # pylint:disable=R0201
        '''
        @copydoc pyharness.manipulator.Manipulator.getAvailableAccessors
        '''
        return ALL_ACCESSOR_CLASSES
    # end def getAvailableAccessors

    def getAvailableOperators(self):                                                                                    # pylint:disable=R0201
        '''
        @copydoc pyharness.manipulator.Manipulator.getAvailableOperators
        '''
        return ALLOWED_OPERATORS[self._accessor.XML_TYPEID]
    # end def getAvailableOperators

    def __call__(self, testAccess,
                       context      = None):                                                                            # pylint:disable=W0613
        '''
        @copydoc pyharness.filtering.Filter.__call__
        '''
        obtainedValue = self._accessor(testAccess)

        return self._operator(obtainedValue, self._value)
    # end def __call__

    def __eq__(self, other):
        '''
        @copydoc pyharness.filtering.Filter.__eq__
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, SimpleFilter):
            return -1
        # end if

        if not (Filter.__eq__(self, other)):
            return False
        # end if
        
        return Manipulator.__eq__(self, other)
    # end def __cmp__
# end class SimpleFilter

ALLOWED_OPERATORS = {
                     TestIdAccessor.XML_TYPEID:
                        (StartsWithOperator,
                         ContainsOperator,
                         EndsWithOperator,
                         MatchesRegexOperator,
                         IsInOperator,
                         IsNotInOperator,
                         DoesNotStartWithOperator,
                         DoesNotContainOperator,
                         DoesNotEndWithOperator,
                         DoesNotMatchRegexOperator,
                         ),
                     LevelsAccessor.XML_TYPEID:
                        (ContainsOperator,
                         DoesNotContainOperator,
                         IsInOperator,
                         IsNotInOperator,
                         IsEmptyOperator,
                         IsNotEmptyOperator,
                         ),
                     ImplementedTestCasesAccessor.XML_TYPEID:
                        (ContainsOperator,
                         DoesNotContainOperator,
                         IsInOperator,
                         IsNotInOperator,
                         IsEmptyOperator,
                         IsNotEmptyOperator,
                         ),
                     StateAccessor.XML_TYPEID:
                        (ContainsOperator,
                         DoesNotContainOperator,
                         IsInOperator,
                         IsNotInOperator,
                         IsEmptyOperator,
                         IsNotEmptyOperator,
                         ),
                     MessageAccessor.XML_TYPEID:
                        (StartsWithOperator,
                         ContainsOperator,
                         EndsWithOperator,
                         MatchesRegexOperator,
                         DoesNotStartWithOperator,
                         DoesNotContainOperator,
                         DoesNotEndWithOperator,
                         DoesNotMatchRegexOperator,
                         ),
                     DurationAccessor.XML_TYPEID:
                        (IsLessThanOperator,
                         IsGreaterThanOperator,
                         ),
                     }

class AndFilter(Filter):
    '''
    A Filter that must match all its sub-filters
    '''

    XML_TYPEID    = "and"

    def __init__(self, filters):
        '''
        Constructor

        @param  filters [in] (list) A list of filters to match
        '''
        Filter.__init__(self)

        self._filters = filters
    # end def __init__

    def __cmp__(self, other):
        '''
        Compares the current object with another object.

        @param  other [in] (object) The other object to compare

        @return (int) The comparison result
        '''
        result = Filter.__cmp__(self, other)
        if (result != 0):
            return result
        # end if

        result = cmp(self._filters, other._filters)                                                                     # pylint:disable=W0212
        if (result != 0):
            return result
        # end if

        return result
    # end def __cmp__

    def __call__(self, testAccess,
                       context      = None):
        '''
        Whether the test should be accepted, or filtered out.

        @param  testAccess [in] (TestAccess) A TestAccess instance, providing
                                             access to the test properties
        @option context    [in] (Context)    The context in which the test is
                                             accessed

        @return True if the test is acceptable, False otherwise.
        '''
        result = True

        for subFilter in self._filters:
            result = result and subFilter(testAccess, context)
        # end for

        return result
    # end def __call__
# end class AndFilter

class OrFilter(Filter):
    '''
    A Filter that must match at least one of its sub-filters
    '''

    XML_TYPEID    = "and"

    def __init__(self, filters):
        '''
        Constructor

        @param  filters [in] (list) A list of filters to match
        '''
        Filter.__init__(self)

        self._filters = filters
    # end def __init__

    def __cmp__(self, other):
        '''
        @copydoc pyharness.filtering.Filter.__cmp__
        '''
        result = Filter.__cmp__(self, other)
        if (result != 0):
            return result
        # end if

        result = cmp(self._filters, other._filters)                                                                     # pylint:disable=W0212
        if (result != 0):
            return result
        # end if

        return result
    # end def __cmp__

    def __call__(self, testAccess,
                       context      = None):
        '''
        @copydoc pyharness.filtering.Filter.__call__
        '''
        result = False

        for subFilter in self._filters:
            result = result or subFilter(testAccess, context)
        # end for

        return result
    # end def __call__
# end class OrFilter

class CustomFilter(Filter):
    '''
    A Filter that must match its sub-filters against a provided code.

    NOTE: This is a very insecure API !
    '''

    XML_TYPEID    = "custom"

    def __init__(self, filters,
                       code):
        '''
        Constructor

        @param  filters [in] (list) A list of filters to match
        @param  code    [in] (str)  The code to evaluate.
        '''
        Filter.__init__(self)

        self._filters   = filters
        self._code      = eval("lambda expr: %s" % code)
    # end def __init__

    def __eq__(self, other):
        '''
        @copydoc pyharness.filtering.Filter.__eq__
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, CustomFilter):
            return -1
        # end if

        if not (Filter.__eq__(self, other)):
            return False
        # end if

        if not (self._code == other._code):
            return False
        # end if
        
        return (self._filters == other._filters)
    # end def __eq__

    def __call__(self, testAccess,
                       context      = None):
        '''
        @copydoc pyharness.filtering.Filter.__call__
        '''
        result = False

        expr = [subFilter(testAccess, context) for subFilter in self._filters]

        self._code(expr)

        return result
    # end def __call__
# end class CustomFilter

def filterFactory(element):
    '''
    Creates a Filter instance from the specified element.

    @param  element [in] (Element) The XML element to deserialize

    @return (Filter) An instance of a Filter, matching the element type.
    '''
    return SimpleFilter.fromElement(element)
# end def filterFactory

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
    if (    (value1 is None)
        or  (value2 is None)):
        return False
    # end if

    # Both are not None
    return value1 == value2
# end def _equals

class FilteringProfile(Listenable):
    '''
    Container Filter, named, and able to be serialized.

    Note that the matchCode refers to the body of a lambda function, that can
    evaluated each expression.

    Access to the expression is done through the expr parameter, and the body
    of the expression would be:
    @code
    lambda expr: <expression body>
    @endcode
    where expr is a tuple containing the evaluation of every expression in the filter.
    '''
    XML_TAG              = 'filteringprofile'
    XML_ATTR_ID          = 'id'
    XML_ATTR_READONLY    = 'readonly'

    XML_FILTERS_TAG      = 'filters'
    XML_ATTR_MATCHMETHOD = 'matchall'
    XML_ATTR_MATCHCODE   = 'matchcode'

    MATCH_ALL            = 'all'
    MATCH_ONE            = 'one'
    MATCH_ADVANCED       = 'advanced'

    ACTION_MODIFIED      = 'modified'

    def __init__(self, filteringId = None,
                       filters     = None,
                       matchMethod = MATCH_ALL,
                       matchCode   = "",
                       readOnly    = False):
        '''
        Constructor

        @option filteringId [in] (str) A unique identifier for this profile
        @option filters     [in] (tuple<Filter>) The filters for this profile.
                                   Defaults to an all-inclusive filter
        @option matchMethod [in] (str) Whether the search must match all filters, or at
                                   least one.
        @option matchCode   [in] (str) The matching code to be evaluated
        @option readOnly    [in] (bool) Whether the current profile can be edited.
        '''
        Listenable.__init__(self)

        if (filters is None):
            filters = []
        # end if

        self._filteringId   = None
        self._filters     = []
        self._matchMethod = None
        self._matchCode   = None
        self._readOnly    = None

        self.setId(filteringId)
        self.setFilters(filters)
        self.setMatchMethod(matchMethod)
        self.setMatchCode(matchCode)
        self.setReadOnly(readOnly)
    # end def __init__

    def __eq__(self, other):
        '''
        Comparison method

        @param  other [in] (object) The other instance to compare

        @return (int) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, FilteringProfile):
            return -1
        # end if

        if not (self._filteringId == other._filteringId):
            return False
        # end if

        if not (self._filters == other._filters):
            return False
        # end if
        
        return (self._matchMethod == other._matchMethod)
    # end def __eq__

    def __str__(self):
        '''
        Converts the current object to its string representation.

        @return (str) The current object, as a string.
        '''
        return "%s, filters=%s, matchMethod=%s" % \
                ( self._filteringId,
                  self._filters is None and "None" or ",".join([str(sorter) for sorter in self._filters]),
                  self._matchMethod )
    # end def __str__

    def _childrenListener(self, source, action):                                                                        # pylint:disable=W0613
        '''
        Listener for child modifications.

        This is a method, as setting it as a lambda in the constructor is not acceptable.
        (Incompatible with deep copy operations)

        @param  source [in] (object) The source of the notification, ignored.
        @param  action [in] (object) The type for the notification, absorbed in ACTION_MODIFIED
        '''
        self.notifyListeners(source = self,
                             action = self.ACTION_MODIFIED)
    # end def _childrenListener

    def __setstate__(self, state):
        '''
        @copydoc pylibrary.tools.listener.Listenable.__setstate__
        '''
        super(FilteringProfile, self).__setstate__(state)

        self._addFiltersListeners()
    # end def __setstate__

    def getId(self):
        '''
        Obtains the id for this profile

        @return (str) A unique id for this profile
        '''
        return self._filteringId
    # end def getId

    def setId(self, filteringId):
        '''
        Sets the unique id for this profile.

        @param  filteringId [in] (str) The unique id for this profile.
        '''
        if (not _equals(self._filteringId, filteringId)):
            self._filteringId = filteringId

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

    def _removeFiltersListeners(self):
        '''
        Updates the listeners linked to the filters.
        '''
        for element in self._filters:
            element.removeListener(self._childrenListener, self.ACTION_MODIFIED)
        # end for
    # end def _removeFiltersListeners

    def _addFiltersListeners(self):
        '''
        Adds the listeners linked to the filters.
        '''
        for element in self._filters:
            element.addListener(self._childrenListener,
                                self.ACTION_MODIFIED)
        # end for
    # end def _addFiltersListeners

    def setFilters(self, filters):
        '''
        Sets the list of filters for this profile.

        @param  filters [in] (list) The list of filters for this profile.
        '''
        if (self._filters != filters):

            self._removeFiltersListeners()

            self._filters = filters

            self._addFiltersListeners()

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setFilters

    def resolveFilters(self):
        '''
        Creates a unique filter predicate, which follows the chain of
        responsibility pattern, based on the current filters and matchMethod parameter

        @return A Filter instance, applied to each test.
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

    def toElement(self, parentElement):
        '''
        Append the current object, serialized to XML, to the parent element.

        @param  parentElement [in] (Element) The element in which to serialize
                                             the current object
        @return The newly created object
        '''
        document = parentElement
        while document.parentNode:
            document = document.parentNode
        # end while

        childElement = document.createElement(self.XML_TAG)
        parentElement.appendChild(childElement)

        childElement.setAttribute(self.XML_ATTR_ID,       self._filteringId)
        childElement.setAttribute(self.XML_ATTR_READONLY, self._readOnly and "true" or "false")

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

        @return (object) A new sorter instance, from the element.
        '''

        filtersElement = element.getElementsByTagName(cls.XML_FILTERS_TAG)[0]
        filterElements = filtersElement.getElementsByTagName(Filter.XML_TAG)
        filters        = [filterFactory(filterElement) for filterElement in filterElements]

        matchMethod    = filtersElement.getAttribute(cls.XML_ATTR_MATCHMETHOD)

        matchCode      = filtersElement.getAttribute(cls.XML_ATTR_MATCHCODE)

        readOnly       = element.getAttribute(cls.XML_ATTR_READONLY) == 'true'

        return cls(element.getAttribute(cls.XML_ATTR_ID),
                   filters     = filters,
                   matchMethod = matchMethod,
                   matchCode   = matchCode,
                   readOnly    = readOnly)
    # end def fromElement
# end class FilteringProfile

DEFAULT_FILTERING_PROFILES = [FilteringProfile('DEFAULT',
                                               filters     = [SimpleFilter(TestIdAccessor(),
                                                                           MatchesRegexOperator(),
                                                                           '.*'),],
                                               matchMethod = FilteringProfile.MATCH_ALL,
                                               matchCode   = "True",
                                               readOnly    = True),
                              FilteringProfile('ERROR_FAILURE',
                                               filters     = [SimpleFilter(StateAccessor(),
                                                                           IsInOperator(),
                                                                           'error,failure'),],
                                               matchMethod = FilteringProfile.MATCH_ALL,
                                               matchCode   = "True",
                                               readOnly    = True),
                              ]

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
