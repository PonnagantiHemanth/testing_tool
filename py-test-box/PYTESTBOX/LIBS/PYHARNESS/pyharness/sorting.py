#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.sorting

@brief  Sorting capabilities

Contains the definition of Sorters, available through the GUI

@author christophe.roquebert

@date   2018/09/18
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.listener          import Listenable
from pyharness.manipulator               import ALL_ACCESSOR_CLASSES
from pyharness.manipulator               import ContainsOperator
from pyharness.manipulator               import DoesNotContainOperator
from pyharness.manipulator               import DoesNotEndWithOperator
from pyharness.manipulator               import DoesNotMatchRegexOperator
from pyharness.manipulator               import RandomizeOperator
from pyharness.manipulator               import DoesNotStartWithOperator
from pyharness.manipulator               import DurationAccessor
from pyharness.manipulator               import EndsWithOperator
from pyharness.manipulator               import IsEmptyOperator
from pyharness.manipulator               import IsGreaterThanOperator
from pyharness.manipulator               import IsInOperator
from pyharness.manipulator               import IsLessThanOperator
from pyharness.manipulator               import IsNotEmptyOperator
from pyharness.manipulator               import IsNotInOperator
from pyharness.manipulator               import LevelsAccessor
from pyharness.manipulator               import ImplementedTestCasesAccessor
from pyharness.manipulator               import Manipulator
from pyharness.manipulator               import MatchesRegexOperator
from pyharness.manipulator               import MessageAccessor
from pyharness.manipulator               import NilAccessor
from pyharness.manipulator               import NilOperator
from pyharness.manipulator               import StartsWithOperator
from pyharness.manipulator               import StateAccessor
from pyharness.manipulator               import TestIdAccessor

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

class Sorter(Listenable):
    '''
    Basic definition of a Sorter.

    A Sorter is a class that implements the __call__ method.

    Such a method takes as parameters two TestAccess objects, that provide access to:
    - The test id.
    - The test levels
    - The test's last result (usually unknown)
    - The test's last run time.
    '''

    XML_TAG           = 'sorter'
    XML_ATTR_REVERSED = 'reversed'
    XML_ATTR_TYPE     = 'type'

    XML_TYPEID        = 'unknown'

    ACTION_MODIFIED   = 'modified'

    def __init__(self, isReversed=False):
        '''
        Constructor

        @option isReversed [in] (bool) Whether the sorting is done in order, or reversed.
        '''
        Listenable.__init__(self)

        self._reversed  = isReversed
    # end def __init__

    def __str__(self):
        '''
        Converts the current object to a string.

        @return (str) The current object, as a string.
        '''
        return "%s(%s)" % (self.__class__.__name__, self.isReversed())
    # end def __str__

    def __eq__(self, other):
        '''
        Compares the current object with another object.

        @param  other [in] (object) The other object to compare

        @return (int) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, Sorter):
            return -1
        # end if

        if not (self.XML_TYPEID == other.XML_TYPEID):
            return False
        # end if
        
        return (self._reversed == other._reversed)
    # end def __eq__

    def __call__(self, first, second):
        '''
        Compares two TestAccess objects

        This should return:
        - A negative number if first < second
        - Zero if first == second
        - A positive number of first > second

        @param  first  [in] (TestAccess) The first instance to compare
        @param  second [in] (TestAccess) The second instance to compare
        '''
        raise NotImplementedError
    # end def __call__

    def setReversed(self, isReversed):
        '''
        Whether the comparison needs to be reversed

        @param  isReversed [in] (bool) Whether the comparison needs to be reversed.
        '''
        if (self._reversed != isReversed):
            self._reversed = isReversed

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setReversed

    def isReversed(self):
        '''
        Returns the reversing state of the sorter

        @return (bool) The reversing state of the sorter.
        '''
        return self._reversed
    # end def isReversed

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

        childElement.setAttribute(self.XML_ATTR_TYPE, self.XML_TYPEID)
        childElement.setAttribute(self.XML_ATTR_REVERSED, self.isReversed() and 'true' or 'false')

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        Creates a new instance of the current class from the specified element.

        @param  element [in] (Element) The element to deserialize

        @return (Sorter) A new sorter instance, from the element.
        '''
        return cls(element.getAttribute(cls.XML_ATTR_REVERSED) == 'true')
    # end def fromElement

    @classmethod
    def getShortName(cls):
        '''
        Returns a short name for the sorter.

        @return (str) A short name for the sorter.
        '''
        raise NotImplementedError
    # end def getShortName
# end class Sorter

class SimpleSorter(Sorter, Manipulator):
    '''
    Basic definition of a Sorter.

    A Sorter is a class that implements the compare method.

    Such a method takes as parameters two TestAccess objects, that provide access to:
    - The test id.
    - The test levels
    - The test's last result (usually unknown)
    - The test's last run time.
    '''

    XML_TYPEID        = 'unknown'

    def __init__(self, isReversed=False, accessor=None, operator=None, value=""):
        '''
        @copydoc pyharness.sorting.Sorter.__init__
        @copydoc pyharness.manipulator.Manipulator.__init__
        '''
        Sorter.__init__(self, isReversed)
        Manipulator.__init__(self, accessor, operator, value)
    # end def __init__

    def __eq__(self, other):
        '''
        Compares the current object with another object.

        @param  other [in] (object) The other object to compare

        @return (int) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, SimpleSorter):
            return -1
        # end if

        if not (Sorter.__eq__(self, other)):
            return False
        # end if
        
        return (Manipulator.__eq__(self, other))
    # end def __eq__

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
    
    @staticmethod
    def cmp(a, b):
        '''If you really need the cmp() functionality, 
        you could use the expression (a > b) - (a < b)'''
        if a is None and b is None: return 0
        elif a is None: return -1
        elif b is None: return 1
        return (a > b) - (a < b)
    # end def cmp

    def __call__(self, first, second):
        '''
        @copydoc pyharness.sorting.Sorter.__call__
        '''

        factor = self.isReversed() and -1 or 1
        value1 = self._operator(self._accessor(first), self._value)
        value2 = self._operator(self._accessor(second), self._value)

        # For boolean values, an inversion is necessary
        if (    (isinstance(value1, bool))
            and (isinstance(value2, bool))):
            factor *= -1
        # end if

        return factor * self.cmp(value1,
                            value2)
    # end def __call__

    def toElement(self, parentElement):
        '''
        @copydoc pyharness.sorting.Sorter.toElement
        '''
        childElement = Manipulator.toElement(self, parentElement)

        childElement.setAttribute(self.XML_ATTR_REVERSED, self.isReversed() and 'true' or 'false')

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        @copydoc pyharness.sorting.Sorter.fromElement
        '''
        # This trick calls Manipulator.fromElement with cls as first parameter
        result = Manipulator.fromElement.__func__(cls, element)                                                          # @UndefinedVariable

        result.setReversed(element.getAttribute(cls.XML_ATTR_REVERSED) == 'true')                                       # pylint:disable=E1101

        return result
    # end def fromElement

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.sorting.Sorter.getShortName
        '''
        return "Generic sorter"
    # end def getShortName
# end class SimpleSorter

class ChainedSorter(Sorter):
    '''
    Sorts a tests list by sub-sorters
    '''
    def __init__(self, isReversed=False, sorters=()):
        '''
        @copydoc pyharness.sorting.Sorter.__init__
        @option sorters [in] (tuple<Sorter>) The sub-sorters for this sorter
        '''
        Sorter.__init__(self, isReversed)

        self._sorters = sorters
    # end def __init__

    def __call__(self, first, second):
        '''
        @copydoc pyharness.sorting.Sorter.__call__
        '''
        result = 0
        factor = self.isReversed() and -1 or 1

        for sorter in self._sorters:
            result = factor * sorter.__call__(first, second)
            if (result != 0):
                break
            # end if
        # end for

        return result
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.sorting.Sorter.getShortName
        '''
        return 'dynamic chained sorter'
    # end def getShortName
# end class ChainedSorter


SORTER_CLASSES = (SimpleSorter, )

ALLOWED_OPERATORS = {
                     NilAccessor.XML_TYPEID:
                        (NilOperator,
                         RandomizeOperator,
                         ),

                     TestIdAccessor.XML_TYPEID:
                        (NilOperator,
                         StartsWithOperator,
                         ContainsOperator,
                         EndsWithOperator,
                         MatchesRegexOperator,
                         DoesNotStartWithOperator,
                         DoesNotContainOperator,
                         DoesNotEndWithOperator,
                         DoesNotMatchRegexOperator,
                         RandomizeOperator,
                         ),
                     LevelsAccessor.XML_TYPEID:
                        (NilOperator,
                         ContainsOperator,
                         DoesNotContainOperator,
                         IsInOperator,
                         IsNotInOperator,
                         IsEmptyOperator,
                         IsNotEmptyOperator,
                         RandomizeOperator,
                         ),
                     ImplementedTestCasesAccessor.XML_TYPEID:
                        (ContainsOperator,
                         DoesNotContainOperator,
                         IsInOperator,
                         IsNotInOperator,
                         IsEmptyOperator,
                         IsNotEmptyOperator,
                         RandomizeOperator,
                         ),
                     StateAccessor.XML_TYPEID:
                        (NilOperator,
                         ContainsOperator,
                         DoesNotContainOperator,
                         IsInOperator,
                         IsNotInOperator,
                         IsEmptyOperator,
                         IsNotEmptyOperator,
                         RandomizeOperator,
                         ),
                     MessageAccessor.XML_TYPEID:
                        (NilOperator,
                         StartsWithOperator,
                         ContainsOperator,
                         EndsWithOperator,
                         MatchesRegexOperator,
                         DoesNotStartWithOperator,
                         DoesNotContainOperator,
                         DoesNotEndWithOperator,
                         DoesNotMatchRegexOperator,
                         RandomizeOperator,
                         ),
                     DurationAccessor.XML_TYPEID:
                        (NilOperator,
                         IsLessThanOperator,
                         IsGreaterThanOperator,
                         RandomizeOperator,
                         ),
                     }

def sorterFactory(element):
    '''
    Creates a Sorter instance from the specified element.

    @param  element [in] (Element) The XML element to deserialize

    @return (Sorter) An instance of a Sorter, matching the element type.
    '''
    elementType = element.getAttribute(Sorter.XML_ATTR_TYPE)

    for sorterClass in SORTER_CLASSES:
        if (elementType == sorterClass.XML_TYPEID):
            return sorterClass.fromElement(element)
        # end if
    # end for

    return SimpleSorter.fromElement(element)
# end def sorterFactory


class SortingProfile(Listenable):
    '''
    Container for a Sorter, named, and able to be serialized.
    '''
    XML_TAG              = 'sortingprofile'
    XML_ATTR_ID          = 'id'
    XML_ATTR_READONLY    = 'readonly'

    XML_SORTERS_TAG      = 'sorters'

    ACTION_MODIFIED      = 'modified'

    def __init__(self, profileId   = None,
                       sorters     = None,
                       readOnly    = False):
        '''
        Constructor

        @option profileId   [in] (str) A unique identifier for this profile
        @option sorters     [in] (tuple<Sorter>) The sorter for this profile.
                                   Defaults to a nil sorter
        @option readOnly    [in] (bool) Whether the current profile can be edited.
        '''
        Listenable.__init__(self)

        if (sorters is None):
            sorters = []
        # end if
        self._profileId   = None
        self._sorters     = []
        self._readOnly    = None

        self.setId(profileId)
        self.setSorters(sorters)
        self.setReadOnly(readOnly)
    # end def __init__

    def __eq__(self, other):
        '''
        Comparison method

        @param  other [in] (object) The other instance to compare

        @return (bool) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, SortingProfile):
            return -1
        # end if

        if not (self._profileId == other._profileId):
            return False
        # end if
        
        return (self._sorters == other._sorters)
    # end def __eq__

    def __str__(self):
        '''
        Converts the current object to its string representation.

        @return (str) The current object, as a string.
        '''

        return "%s, sorters=(%s)" % \
                ( self._profileId,
                  self._sorters is None and "None" or ",".join([str(sorter) for sorter in self._sorters]),
                  )
    # end def __str__

    def _childrenListener(self, source, action):                                                                        # pylint:disable=W0613
        '''
        Listener for child modifications.

        This is a method, as setting it as a lambda in the constructor is not acceptable.
        (Incompatible with deep copy operations)

        @param  source [in] (object) The source of the notification, ignored.
        @param  action [in] (object) The type for the notifiction, absorbed in ACTION_MODIFIED
        '''
        self.notifyListeners(source = self,
                             action = self.ACTION_MODIFIED)
    # end def _childrenListener

    def __setstate__(self, state):
        '''
        @copydoc pylibrary.tools.listener.Listenable.__setstate__
        '''
        super(SortingProfile, self).__setstate__(state)

        self._addSortersListeners()
    # end def __setstate__

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

    def getSorters(self):
        '''
        Obtains the sorters for this profile

        @return (list) An ordered tuple of sorters for this profile.
        '''
        return self._sorters
    # end def getSorters

    def _removeSortersListeners(self):
        '''
        Updates the listeners linked to the sorters.
        '''
        for element in self._sorters:
            element.removeListener(self._childrenListener, self.ACTION_MODIFIED)
        # end for
    # end def _removeSortersListeners

    def _addSortersListeners(self):
        '''
        Adds the listeners linked to the sorters.
        '''
        for element in self._sorters:
            element.addListener(self._childrenListener,
                                self.ACTION_MODIFIED)
        # end for
    # end def _addSortersListeners

    def setSorters(self, sorters):
        '''
        Sets the list of sorters for this profile.

        @param  sorters [in] (list) The list of sorters for this profile.
        '''
        self._sorters = sorters

        if (self._sorters != sorters):

            self._removeSortersListeners()

            self._sorters = sorters

            self._addSortersListeners()

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setSorters

    def resolveSorters(self):
        '''
        Creates a unique sorter predicate, which follows the chain of
        responsibility pattern, based on the current sorters parameter

        @return (Sorter) A Sorter, applied to a test list.
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

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        Creates a new instance of the current class from the specified element.

        @param  element [in] (Element) The element to de-serialize

        @return (Sorter) A new sorter instance, from the element.
        '''
        sortersElement = element.getElementsByTagName(cls.XML_SORTERS_TAG)[0]
        sorterElements = sortersElement.getElementsByTagName(Sorter.XML_TAG)
        sorters        = [sorterFactory(sorterElement) for sorterElement in sorterElements]

        readOnly       = (element.getAttribute(cls.XML_ATTR_READONLY) == 'true')

        return cls(element.getAttribute(cls.XML_ATTR_ID),
                   sorters     = sorters,
                   readOnly    = readOnly)
    # end def fromElement
# end class SortingProfile

DEFAULT_SORTING_PROFILE = SortingProfile('DEFAULT',
                                sorters  = [SimpleSorter(False, NilAccessor(), NilOperator()),],
                                readOnly = True)

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
