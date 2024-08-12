#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.manipulator

@brief  Base implementation of accessor APIs (used for Filter and Sorter classes)

@author christophe.roquebert

@date   2018/10/18
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from calendar                           import timegm
from pylibrary.tools.listener          import Listenable
from pylibrary.tools.threadutils       import synchronized
from pyharness.extensions                import level
from pyharness.testmanager               import TestDescriptor
from random                             import randint
import re

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

class Accessor(object):
    '''
    Base Accessor class.

    An accessor extracts information from a TestAccess object.
    '''
    XML_TAG       = "accessor"
    XML_ATTR_TYPE = "type"
    XML_TYPEID    = "unknown"

    def __eq__(self, other):
        '''
        Compares the current object with another object.

        @param  other [in] (object) The other object to compare

        @return (bool) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, Accessor):
            return -1
        # end if

        return (self.XML_TYPEID == other.XML_TYPEID)
    # end def __eq__

    def __str__(self):
        '''
        Converts the current object to a string.

        @return (str) The current object, as a string.
        '''
        return self.getShortName()
    # end def __str__

    def __call__(self, testAccess):
        '''
        Extracts the appropriate information from a TestAccess object

        @param  testAccess [in] (TestAccess) The TestAccess instance to extract
                               information from.
        '''
        raise NotImplementedError
    # end def __call__

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

        childElement.setAttribute(self.XML_ATTR_TYPE, self.XML_TYPEID)

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        Creates a new instance of the current class from the specified element.

        @param  element [in] (Element) The element to deserialize

        @return A new sorter instance, from the element.
        '''
        assert (cls.XML_TYPEID == element.getAttribute(cls.XML_ATTR_TYPE))

        return cls()
    # end def fromElement

    @classmethod
    def getShortName(cls):
        '''
        The short name for this object.

        @return (string) A user-friendly name for the current object.
        '''
        return "unknown"
    # end def getShortName

    @classmethod
    def getDefaultValues(cls):
        '''
        Obtains the default values for this data, if any

        @return The list of default values for this data, or an empty list if
                none can be found.
        '''
        return tuple()
    # end def getDefaultValues
# end class Accessor

class NilAccessor(Accessor):
    '''
    Empty accessor
    '''

    XML_TYPEID = "nil"

    def __call__(self, testAccess):                                                                                     # pylint:disable=W0613
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        return None
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "nothing"
    # end def getShortName
# end class NilAccessor

class TestIdAccessor(Accessor):
    '''
    Accessor for the testId
    '''

    XML_TYPEID = "testid"

    def __call__(self, testAccess):
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        return testAccess.getTestId()
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "test id"
    # end def getShortName
# end class TestIdAccessor

class LevelsAccessor(Accessor):
    '''
    Accessor for the levels list
    '''

    XML_TYPEID = "levels"

    def __call__(self, testAccess):
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        return testAccess.getTestLevels()
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "level"
    # end def getShortName

    @classmethod
    def getDefaultValues(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getDefaultValues
        '''
        return level.get_levels()
    # end def getDefaultValues
# end class LevelsAccessor

class ImplementedTestCasesAccessor(Accessor):
    '''
    Accessor for the implemented TestCases list (static analysis)
    '''

    XML_TYPEID = "static_testcases"

    def __call__(self, testAccess):
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        return testAccess.getStaticTestCases()
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "testcases (implemented)"
    # end def getShortName

    @classmethod
    def getDefaultValues(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getDefaultValues
        '''
        import wx
        testManager = wx.GetApp().testManager                                                                           # @UndefinedVariable
        return testManager.getStaticTestCases(None)
    # end def getDefaultValues
# end class ImplementedTestCasesAccessor

class StateAccessor(Accessor):
    '''
    Accessor for the last state of the test, through the history
    '''

    XML_TYPEID = "laststate"

    STATE_CONVERSION = {TestDescriptor.STATE_UNKNOWN: "unknown",
                        TestDescriptor.STATE_SUCCESS: "success",
                        TestDescriptor.STATE_FAILURE: "failure",
                        TestDescriptor.STATE_ERROR:   "error",
                        }

    def __call__(self, testAccess):
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        runHistory = testAccess.getRunHistory()
        state = TestDescriptor.STATE_UNKNOWN
        if (len(runHistory) > 0):
            state = runHistory[-1][0]
        # end if

        # The test state is obtained from the TestDescriptor
        # As we want a STRING and not an INT, we need to convert the constant
        return self.STATE_CONVERSION[state]
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "state"
    # end def getShortName

    @classmethod
    def getDefaultValues(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getDefaultValues
        '''
        return ("unknown", "success", "failure", "error")
    # end def getDefaultValues
# end class StateAccessor

class MessageAccessor(Accessor):
    '''
    Accessor for the last message of the test, through the history
    '''

    XML_TYPEID = "lastmessage"

    def __call__(self, testAccess):
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        runHistory = testAccess.getRunHistory()
        message = ""
        if (len(runHistory) > 0):
            message = runHistory[-1][3]
        # end if

        return (message is not None) and message or ""
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "message"
    # end def getShortName
# end class MessageAccessor

class DurationAccessor(Accessor):
    '''
    Accessor for the last message of the test, through the history
    '''

    XML_TYPEID = "lastduration"

    def __call__(self, testAccess):
        '''
        @copydoc pyharness.manipulator.Accessor.__call__
        '''
        runHistory = testAccess.getRunHistory()
        duration = None

        for state, startDate, endDate, _ in reversed(runHistory):
            if (state == TestDescriptor.STATE_SUCCESS):
                if (    (startDate is not None)
                    and (endDate is not None)):
                    duration = timegm(endDate) - timegm(startDate)
                    break
                # end if
            else:
                break
            # end if
        # end for

        return duration
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Accessor.getShortName
        '''
        return "duration"
    # end def getShortName
# end class DurationAccessor

class Operator(object):
    '''
    Basic definition of a manipulator operator.

    A manipulator operator is an object that, from an entry and a TestCase,
    tests the validity of the entry against the TestCase.
    '''

    XML_TAG       = "operator"
    XML_ATTR_TYPE = "type"
    XML_TYPEID    = "unknown"

    def __eq__(self, other):
        '''
        Compares the current object with another object.

        @param  other [in] (object) The other object to compare

        @return (int) The comparison result
        '''
        if (other is None):
            return -1
        # end if
        
        if not isinstance(other, Operator):
            return -1
        # end if

        return (self.XML_TYPEID == other.XML_TYPEID)
    # end def __eq__

    def __str__(self):
        '''
        Converts the current object to a string.

        @return (str) The current object, as a string.
        '''
        return self.getShortName()
    # end def __str__

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

        childElement.setAttribute(self.XML_ATTR_TYPE, self.XML_TYPEID)

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        Creates a new instance of the current class from the specified element.

        @param  element [in] (object) The element to deserialize

        @return (object) A new sorter instance, from the element.
        '''
        assert (cls.XML_TYPEID == element.getAttribute(cls.XML_ATTR_TYPE))

        return cls()
    # end def fromElement

    @classmethod
    def __call__(cls, entry, value):
        '''
        Computes the result of the operation.

        @param  entry [in] (object) The entry to test.
        @param  value [in] (object) The value to test against.

        @return (bool) True if the test is acceptable, False otherwise.
                Operators may also return strings, int or other types as needed.
        '''
        raise NotImplementedError
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        The short name for this object.

        @return (string) A user-friendly name for the current object.
        '''
        return "unknown"
    # end def getShortName
# end class Operator

class ContainsOperator(Operator):
    '''
    Manipulator operator: contains.
    '''

    XML_TYPEID    = "contains"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return value in entry
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "contains"
    # end def getShortName
# end class ContainsOperator

class NilOperator(Operator):
    '''
    Manipulator operator: Nil
    '''

    XML_TYPEID    = "nil"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return entry
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "default"
    # end def getShortName
# end class NilOperator

class RandomizeOperator(Operator):
    '''
    Manipulator operator: Randomize
    '''

    XML_TYPEID    = "randomize"

    @classmethod
    def __call__(cls, entry, value):                                                                                    # pylint:disable=W0613
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return (-1, 1)[randint(0, 1)]
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "randomize"
    # end def getShortName
# end class RandomizeOperator

class DoesNotContainOperator(Operator):
    '''
    Manipulator operator: does not contain.
    '''

    XML_TYPEID    = "doesnotcontain"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return value not in entry
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "does not contain"
    # end def getShortName
# end class DoesNotContainOperator

class StartsWithOperator(Operator):
    '''
    Manipulator operator: starts with.
    '''

    XML_TYPEID    = "startswith"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return entry.startswith(value)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "starts with"
    # end def getShortName
# end class StartsWithOperator

class DoesNotStartWithOperator(Operator):
    '''
    Manipulator operator: does not start with.
    '''

    XML_TYPEID    = "doesnotstartwith"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return not entry.startswith(value)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "does not start with"
    # end def getShortName
# end class DoesNotStartWithOperator

class EndsWithOperator(Operator):
    '''
    Manipulator operator: ends with.
    '''

    XML_TYPEID    = "endswith"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return entry.endswith(value)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "ends with"
    # end def getShortName
# end class EndsWithOperator

class DoesNotEndWithOperator(Operator):
    '''
    Manipulator operator: does not end with.
    '''

    XML_TYPEID    = "doesnotendwith"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return not entry.endswith(value)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "does not end with"
    # end def getShortName
# end class DoesNotEndWithOperator

class IsInOperator(Operator):
    '''
    Manipulator operator: is in.
    '''

    XML_TYPEID    = "isin"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        if (    (type(entry) in (list, tuple))
            and (type(value) in (str, str))):
            value = [str(v.strip()) for v in value.split(',')]

            matches = [x for x in entry if x in value]
            result = (len(matches) > 0)
        else:
            result = entry in value
        # end if

        return result
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "is in"
    # end def getShortName
# end class IsInOperator

class IsNotInOperator(Operator):
    '''
    Manipulator operator: is not in
    '''

    XML_TYPEID    = "isnotin"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        if (    (isinstance(entry, list))
            and (type(value) in (str, str))):
            value = [str(v.strip()) for v in value.split(',')]

            if (len(entry) == 0):
                result = False
            else:
                matches = [x for x in entry if x in value]
                result = (len(matches) == 0)
            # end if
        else:
            result = entry not in value
        # end if

        return result
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "is not in"
    # end def getShortName
# end class IsNotInOperator

class IsInListOperator(IsInOperator):
    '''
    Manipulator operator: is in.
    Uses a non checked list
    '''

    XML_TYPEID    = "isinlist"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        value = [str(v.strip()) for v in value.split(',')]
        if (    (type(entry) in (list, tuple))
            and (type(value) in (str, str))):
            matches = [x for x in entry if x in value]
            result = (len(matches) > 0)
        else:
            result = entry in value
        # end if

        return result
    # end def __call__

# end class IsInListOperator

class IsNotInListOperator(IsNotInOperator):
    '''
    Manipulator operator: is not in
    Uses a non checked list
    '''

    XML_TYPEID    = "isnotinlist"

# end class IsNotInListOperator

class IsEmptyOperator(Operator):
    '''
    Manipulator operator: is empty.
    '''

    XML_TYPEID    = "isempty"

    @classmethod
    def __call__(cls, entry, value):                                                                                    # pylint:disable=W0613
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return (len(entry) == 0)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "is empty"
    # end def getShortName
# end class IsEmptyOperator

class IsNotEmptyOperator(Operator):
    '''
    Manipulator operator: is not empty.
    '''

    XML_TYPEID    = "isnotempty"

    @classmethod
    def __call__(cls, entry, value):                                                                                    # pylint:disable=W0613
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        return (len(entry) != 0)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "is not empty"
    # end def getShortName
# end class IsNotEmptyOperator

class IsLessThanOperator(Operator):
    '''
    Manipulator operator: <.
    '''

    XML_TYPEID    = "isless"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        result = False
        if (    (entry is not None)
            and (value is not None)):
            result = (entry < value)
        # end if

        return result
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "is less than"
    # end def getShortName
# end class IsLessThanOperator

class IsGreaterThanOperator(Operator):
    '''
    Manipulator operator: >.
    '''

    XML_TYPEID    = "isgreater"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        result = False
        if (    (entry is not None)
            and (value is not None)):
            result = (entry > value)
        # end if

        return result
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "is greater than"
    # end def getShortName
# end class IsGreaterThanOperator

REGEX_CACHE = {}

@synchronized
def compileRegex(value):
    '''
    Compiles the regex, and puts it in cache for later use.

    @param  value [in] (str) The value to build the regex from

    @return (string) The compiled regex
    '''
    if (value in REGEX_CACHE):
        regex = REGEX_CACHE[value]
    else:
        regex = re.compile(value)
        REGEX_CACHE[value] = regex
    # end if

    return regex
# end def compileRegex

class MatchesRegexOperator(Operator):
    '''
    Manipulator operator: matches regex.
    '''

    XML_TYPEID    = "matchregex"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        regex = compileRegex(value)
        return (regex.match(entry) is not None)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "matches regex"
    # end def getShortName
# end class MatchesRegexOperator

class DoesNotMatchRegexOperator(Operator):
    '''
    Manipulator operator: does not match regex.
    '''

    XML_TYPEID    = "doesnotmatchregex"

    @classmethod
    def __call__(cls, entry, value):
        '''
        @copydoc pyharness.manipulator.Operator.__call__
        '''
        regex = compileRegex(value)
        return (regex.match(entry) is None)
    # end def __call__

    @classmethod
    def getShortName(cls):
        '''
        @copydoc pyharness.manipulator.Operator.getShortName
        '''
        return "does not match regex"
    # end def getShortName
# end class DoesNotMatchRegexOperator

class InputValidator(object):
    '''
    Base class for validating the input.
    '''

    TYPE = None

    def validate(self, value):
        '''
        Validates the value.

        @param  value [in] (str) The value to validate

        @return (bool) The validation result
        '''
        raise NotImplementedError
    # end def validate
# end class InputValidator

class NilValidator(InputValidator):
    '''
    Do-nothing validator.
    '''

    TYPE = "nil"

    def validate(self, value):                                                                                          # pylint:disable=W0613
        '''
        @copydoc pyharness.manipulator.InputValidator.validate
        '''
        return True
    # end def validate
# end class NilValidator

class TextValidator(InputValidator):
    '''
    Text validator (does nothing)
    '''

    TYPE = "text"

    def validate(self, value):                                                                                          # pylint:disable=W0613
        '''
        @copydoc pyharness.manipulator.InputValidator.validate
        '''
        return True
    # end def validate
# end class TextValidator

class TextPatternValidator(InputValidator):
    '''
    Validates a value against a regex
    '''

    TYPE = "textpattern"

    def __init__(self, pattern):
        '''
        Constructor

        @param  pattern [in] (str) The pattern to validate
        '''
        InputValidator.__init__(self)

        self.regex = re.compile(pattern)
    # end def __init__

    def validate(self, value):
        '''
        @copydoc pyharness.manipulator.InputValidator.validate
        '''
        return (self.regex.match(value.strip()) is not None)
    # end def validate
# end class TextPatternValidator

class DurationValidator(TextPatternValidator):
    '''
    Validates a value against a duration format
    '''

    TYPE = "duration"

    def __init__(self):
        '''
        Constructor
        '''
        TextPatternValidator.__init__(self, r"\d\d:\d\d:\d\d")
    # end def __init__
# end class DurationValidator

class MultiChoiceValidator(InputValidator):
    '''
    Validates a comma-separated list of value against a list of values
    '''
    TYPE = "multichoice"

    def __init__(self, values):
        '''
        Constructor

        @param  values [in] (tuple) The list of values to validate against
        '''
        InputValidator.__init__(self)

        self.values = values
    # end def __init__

    def validate(self, value):
        '''
        @copydoc pyharness.manipulator.InputValidator.validate
        '''
        result = True
        for value in [v.strip() for v in value.split(',')]:
            result = result and value in self.values
        # end for
        return result
    # end def validate
# end class MultiChoiceValidator

class ListChoiceValidator(InputValidator):
    '''
    Validates a comma-separated list of value against a list of values

    This validator will directly use values as references instead of
    default values as @c MultiChoiceValidator
    '''
    TYPE = "listchoice"

    def __init__(self, values):
        '''
        Constructor

        @param  values [in] (tuple) The list of values to validate against
        '''
        InputValidator.__init__(self)

        self.values = values
    # end def __init__

    def validate(self, value):
        '''
        @copydoc pyharness.manipulator.InputValidator.validate
        '''
        result = True
        for value in [v.strip() for v in value.split(',')]:
            result = result and value in self.values
        # end for
        return result
    # end def validate
# end class ListChoiceValidator

class SingleChoiceValidator(InputValidator):
    '''
    Validates a value against a list of values
    '''

    TYPE = "singlechoice"

    def __init__(self, values):
        '''
        Constructor

        @param  values [in] (tuple) The list of values to validate against
        '''
        InputValidator.__init__(self)

        self.values = values
    # end def __init__

    def validate(self, value):
        '''
        @copydoc pyharness.manipulator.InputValidator.validate
        '''
        if (len(value.split(',')) > 1):
            return False
        # end if

        return (value.strip() in self.values)
    # end def validate
# end class SingleChoiceValidator


ALL_ACCESSOR_CLASSES = (NilAccessor,
                        TestIdAccessor,
                        LevelsAccessor,
                        ImplementedTestCasesAccessor,
                        StateAccessor,
                        MessageAccessor,
                        DurationAccessor,
                        )

def accessorFactory(element):
    '''
    Creates an Accessor instance from the specified element.

    @param  element [in] (Element) The XML element to deserialize

    @return (Accessor) An instance of a Sorter, matching the element type.
    '''
    elementType = element.getAttribute(Operator.XML_ATTR_TYPE)

    for accessorClass in ALL_ACCESSOR_CLASSES:
        if (elementType == accessorClass.XML_TYPEID):
            return accessorClass.fromElement(element)
        # end if
    # end for

    return Accessor.fromElement(element)
# end def accessorFactory

ALL_OPERATOR_CLASSES = (NilOperator,
                        StartsWithOperator,
                        DoesNotStartWithOperator,
                        ContainsOperator,
                        DoesNotContainOperator,
                        EndsWithOperator,
                        DoesNotEndWithOperator,
                        IsInOperator,
                        IsNotInOperator,
                        IsInListOperator,
                        IsNotInListOperator,
                        IsEmptyOperator,
                        IsNotEmptyOperator,
                        MatchesRegexOperator,
                        DoesNotMatchRegexOperator,
                        IsLessThanOperator,
                        IsGreaterThanOperator,
                        RandomizeOperator,
                        )

def operatorFactory(element):
    '''
    Creates an Operator instance from the specified element.

    @param  element [in] (Element) The XML element to deserialize

    @return (Operator) An instance of a Sorter, matching the element type.
    '''
    elementType = element.getAttribute(Operator.XML_ATTR_TYPE)

    for operatorClass in ALL_OPERATOR_CLASSES:
        if (elementType == operatorClass.XML_TYPEID):
            return operatorClass.fromElement(element)
        # end if
    # end for

    return Operator.fromElement(element)
# end def operatorFactory

class Manipulator(Listenable):
    '''
    Basic definition of a Manipulator.

    A Manipulator is a class that access a TestAccess, and is configurable
    through the GUI.
    '''

    XML_TAG         = "manipulator"
    XML_ATTR_TYPE   = "type"
    XML_TYPEID      = 'unknown'

    XML_VALUE_TAG   = 'value'
    XML_ATTR_VALUE  = 'value'

    ACTION_MODIFIED = "modified"

    def __init__(self, accessor = None,
                       operator = None,
                       value    = ""):
        '''
        Constructor

        @option accessor [in] (Accessor) The accessor to the test
        @option operator [in] (Operator) The operator to manipulate the test
        @option value    [in] (object)   The value to operate on
        '''
        Listenable.__init__(self)

        self._accessor  = None
        self._operator  = None
        self._value     = None

        self.setAccessor(accessor)
        self.setOperator(operator)
        self.setValue(value)
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
        
        if not isinstance(other, Manipulator):
            return -1
        # end if

        if not (self.XML_TYPEID == other.XML_TYPEID):
            return False
        # end if

        if not (self._accessor == other._accessor):
            return False
        # end if

        if not (self._operator == other._operator):
            return False
        # end if

        return (self._value == other._value)
    # end def __eq__

    def __str__(self):
        '''
        Converts the current object to a string.

        @return (str) The current object, as a string.
        '''
        return "(%s %s %s)" % (self._accessor, self._operator, self._value)
    # end def __str__

    def getAccessor(self):
        '''
        Obtains the accessor

        @return (Accessor) The accessor for this manipulator
        '''
        return self._accessor
    # end def getAccessor

    def setAccessor(self, accessor):
        '''
        Sets the accessor

        @param  accessor [in] (Accessor) The accessor for this manipulator
        '''
        if (not _equals(self._accessor, accessor)):
            self._accessor = accessor

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setAccessor

    def getAvailableAccessors(self):                                                                                    # pylint:disable=R0201
        '''
        Obtains the list of acceptable accessors for this manipulator.

        @return (list) the list of acceptable accessors for this manipulator.
        '''
        raise NotImplementedError
    # end def getAvailableAccessors

    def getOperator(self):
        '''
        Obtains the operator

        @return (Operator) The operator for this manipulator
        '''
        return self._operator
    # end def getOperator

    def setOperator(self, operator):
        '''
        Sets the operator

        @param  operator [in] (Operator) The operator for this manipulator
        '''
        if (not _equals(self._operator, operator)):
            self._operator = operator

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setOperator

    def getAvailableOperators(self):                                                                                    # pylint:disable=R0201
        '''
        Obtains a list of acceptable operators for this manipulator.

        @return (list) A list of class types, derived from Operator, that are
                acceptable for this manipulator type.
        '''
        raise NotImplementedError
    # end def getAvailableOperators

    VALIDATOR_COL = { NilAccessor.XML_TYPEID:                   0,
                      TestIdAccessor.XML_TYPEID:                1,
                      LevelsAccessor.XML_TYPEID:                2,
                      ImplementedTestCasesAccessor.XML_TYPEID:  3,
                      StateAccessor.XML_TYPEID:                 4,
                      MessageAccessor.XML_TYPEID:               5,
                      DurationAccessor.XML_TYPEID:              6,
                     }

    VALIDATOR_LINE = { NilOperator.XML_TYPEID:                  0,
                       StartsWithOperator.XML_TYPEID:           1,
                       DoesNotStartWithOperator.XML_TYPEID:     2,
                       ContainsOperator.XML_TYPEID:             3,
                       DoesNotContainOperator.XML_TYPEID:       4,
                       EndsWithOperator.XML_TYPEID:             5,
                       DoesNotEndWithOperator.XML_TYPEID:       6,
                       IsInOperator.XML_TYPEID:                 7,
                       IsNotInOperator.XML_TYPEID:              8,
                       IsEmptyOperator.XML_TYPEID:              9,
                       IsNotEmptyOperator.XML_TYPEID:           10,
                       MatchesRegexOperator.XML_TYPEID:         11,
                       DoesNotMatchRegexOperator.XML_TYPEID:    12,
                       IsLessThanOperator.XML_TYPEID:           13,
                       IsGreaterThanOperator.XML_TYPEID:        14,
                       RandomizeOperator.XML_TYPEID:            15,
                       IsInListOperator.XML_TYPEID:             16,
                       IsNotInListOperator.XML_TYPEID:          17,
                    }

    VALIDATOR_MATRIX = (
        # NilOperator
        (NilValidator, NilValidator,         NilValidator,         NilValidator,         NilValidator,         NilValidator,  NilValidator, ),
        # StartsWithOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # DoesNotStartWithOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # ContainsOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # DoesNotContainOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # EndsWithWithOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # DoesNotEndWithOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # IsInOperator
        (NilValidator, MultiChoiceValidator, MultiChoiceValidator, MultiChoiceValidator, MultiChoiceValidator, TextValidator, None, ),
        # IsNotInOperator
        (NilValidator, MultiChoiceValidator, MultiChoiceValidator, MultiChoiceValidator, MultiChoiceValidator, TextValidator, None, ),
        # IsEmptyOperator
        (NilValidator, NilValidator,         NilValidator,         NilValidator,         NilValidator,         NilValidator,  None, ),
        # IsNotEmptyOperator
        (NilValidator, NilValidator,         NilValidator,         NilValidator,         NilValidator,         NilValidator,  None, ),
        # MatchesRegexOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # DoexNotMatchRegexOperator
        (NilValidator, TextValidator,        TextValidator,        TextValidator,        TextValidator,        TextValidator, None, ),
        # IsLessThanOperator
        (NilValidator, None,                 None,                 None,                 None,                 None,          DurationValidator, ),
        # IsGreaterThanOperator
        (NilValidator, None,                 None,                 None,                 None,                 None,          DurationValidator, ),
        # RandomizeOperator
        (NilValidator, NilValidator,         NilValidator,         NilValidator,         NilValidator,         NilValidator,  None, ),
        # IsInListOperator
        (NilValidator, ListChoiceValidator,  ListChoiceValidator,  ListChoiceValidator,  ListChoiceValidator,  TextValidator, None, ),
        # IsNotInListOperator
        (NilValidator, ListChoiceValidator,  ListChoiceValidator,  ListChoiceValidator,  ListChoiceValidator,  TextValidator, None, ),
        )


    def getAvailableValidators(self):
        '''
        Obtains a list of preferred validators, by decreasing order of importance

        @return (list) A list of preferred validators
        '''
        # raise NotImplementedError

        result = []

        operator = self.getOperator()
        accessor = self.getAccessor()
        if (    (operator is not None)
            and (accessor is not None)):
            line = self.VALIDATOR_LINE[operator.XML_TYPEID]
            col = self.VALIDATOR_COL[accessor.XML_TYPEID]

            validator = self.VALIDATOR_MATRIX[line][col]
            if (validator is not None):
                result.append(validator)
            # end if
        # end if

        result.append(NilValidator)

        return result
    # end def getAvailableValidators

    def __call__(self):
        '''
        Obtains the value

        @return (object) The value for this manipulator
        '''
        return self._value
    # end def __call__

    def getValue(self):
        '''
        Obtains the value

        @return (object) The value for this manipulator
        '''
        return self._value
    # end def getValue

    def setValue(self, value):
        '''
        Sets the value

        @param  value [in] (object) The value for this manipulator
        '''
        if (not _equals(self._value, value)):
            self._value = value

            self.notifyListeners(source = self,
                                 action = self.ACTION_MODIFIED)
        # end if
    # end def setValue

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

        self._accessor.toElement(childElement)
        self._operator.toElement(childElement)

        if (self._value is not None):
            valueElement = document.createElement(self.XML_VALUE_TAG)
            childElement.appendChild(valueElement)
            valueElement.setAttribute(self.XML_ATTR_VALUE, self._value)
        # end if

        return childElement
    # end def toElement

    @classmethod
    def fromElement(cls, element):
        '''
        Creates a new instance of the current class from the specified element.

        @param  element [in] (Element) The element to deserialize

        @return (Element) A new sorter instance, from the element.
        '''
        result = cls()

        accessorElements = element.getElementsByTagName(Accessor.XML_TAG)
        assert (len(accessorElements) == 1), "Invalid number of accessors"
        result.setAccessor(accessorFactory(accessorElements[0]))

        operatorElements = element.getElementsByTagName(Operator.XML_TAG)
        assert (len(operatorElements) == 1), "Invalid number of operators"
        result.setOperator(operatorFactory(operatorElements[0]))

        valueElements = element.getElementsByTagName(cls.XML_VALUE_TAG)
        assert (len(valueElements) in (0, 1)), "Invalid number of values"

        if (len(valueElements) == 1):
            result.setValue(valueElements[0].getAttribute(cls.XML_ATTR_VALUE))
        else:
            result.setValue(None)
        # end if

        return result
    # end def fromElement

# end class Manipulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
