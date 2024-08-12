#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.systems

@brief  SubSystem and module implementation

This module contains the implementation of the classes needed in the
features.py files

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.config import ConfigParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.importutils import importFqn
from pyharness.consts import DEFAULT_INPUT_DIRECTORY
from pyharness.core import TYPE_ERROR
from pyharness.core import TestException
from imp import get_suffixes
from os import R_OK
from os import access
from os import listdir
from os import makedirs
from os.path import exists
from os.path import isdir
from os.path import join
from types import FunctionType
from types import MethodType
import re


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractSubSystem(object):
    '''
    The SubSystem class represents a subsystem in the validation hierarchy.

    A SubSystem may contain:
    - SubSystems
    - Functionalities
    .

    The root subsystem represent the whole project hierarchy
    By convention, functionalities follow the naming convention F_XXXX
    '''

    _AUTOMATIC_ = True

    def __init__(self, name, enabled=True):
        '''
        Constructor, providing the name of the subsystem.

        The name will be used for serializing/deserializing the subsystem.
        The subsystem is, by default, activated.

        @param  name      [in] (str) The name of this subsystem.
        @option enabled   [in] (bool) Whether the system is activated by default.
        '''
        # by default, the system is activated.
        # This will be updated by the subsystem builder
        self.F_Enabled = enabled
        self.__name = name
        self.__readOnlyAttr = set()
        self.__index = 0

    # end def __init__

    def getName(self):
        '''
        Obtains the name of the subsystem.

        Obtains the name of the subsystem provided in the constructor.

        @return (str) The name of the subsystem.
        '''
        return self.__name

    # end def getName

    name = property(getName)

    def getChild(self, childName):
        '''
        Obtains the child subsystem

        @param  childName [in] (str) The subsystem name

        @return (object) The child subsystem
        '''
        if ((not hasattr(self, childName))
                or (not isinstance(getattr(self, childName), AbstractSubSystem))):
            raise ValueError('%s has no subSystem %s' % (self.getName(), childName))
        # end if

        return getattr(self, childName)

    # end def getChild

    def __eq__(self, other):
        '''
        Compares two subsystems for equality

        Performs a deep comparison of the subsystems.
        The order of priority is:
        <ol>
          <li>name</li>
          <li>functionalities</li>
          <li>sub-subsystems</li>
        </ol>

        @param  other [in] (object) The other subsystem to compare

        @return (bool) True if the subsystems match, False otherwise.
        '''
        if (other is None):
            return -1
        # end if

        if not isinstance(other, AbstractSubSystem):
            return -1
        # end if

        if not (self.name == other.name):
            return False
        # end if

        # compare self.F_xxx
        attributeNames = set()
        attributeNames.update(dir(self))
        attributeNames.update(dir(other))

        selfFunctionalities = []
        otherFunctionalities = []

        for name in attributeNames:
            if (name.startswith("F_")):
                selfFunctionalities.append(getattr(self, name, None))
                otherFunctionalities.append(getattr(other, name, None))
            # end if
        # end for

        if not (selfFunctionalities == otherFunctionalities):
            return False
        # end if

        # compare self subSystems
        selfSubSystems = []
        otherSubSystems = []

        for name in attributeNames:
            selfValue = getattr(self, name, None)
            otherValue = getattr(other, name, None)

            if ((isinstance(selfValue, AbstractSubSystem))
                    or (isinstance(otherValue, AbstractSubSystem))):
                selfSubSystems.append(selfValue)
                otherSubSystems.append(otherValue)
            # end if
        # end for

        return (selfSubSystems == otherSubSystems)

    # end def __eq__

    def __ne__(self, other):
        '''
        Compares two subsystems for inequality

        @param  other [in] (object) The other subsystem to compare

        @return (bool) True if the subsystems mismatch, False otherwise.
        '''
        if (other is None):
            return True
        # end if

        if not isinstance(other, AbstractSubSystem):
            return True
        # end if

        if not (self.name == other.name):
            return True
        # end if

        # compare self.F_xxx
        attributeNames = set()
        attributeNames.update(dir(self))
        attributeNames.update(dir(other))

        selfFunctionalities = []
        otherFunctionalities = []

        for name in attributeNames:
            if (name.startswith("F_")):
                selfFunctionalities.append(getattr(self, name, None))
                otherFunctionalities.append(getattr(other, name, None))
            # end if
        # end for

        if not (selfFunctionalities == otherFunctionalities):
            return True
        # end if

        # compare self subSystems
        selfSubSystems = []
        otherSubSystems = []

        for name in attributeNames:
            selfValue = getattr(self, name, None)
            otherValue = getattr(other, name, None)

            if ((isinstance(selfValue, AbstractSubSystem))
                    or (isinstance(otherValue, AbstractSubSystem))):
                selfSubSystems.append(selfValue)
                otherSubSystems.append(otherValue)
            # end if
        # end for

        return not (selfSubSystems == otherSubSystems)

    # end def __ne__

    def __str__(self):
        '''
        String representation of the object, for debugging purposes

        @return (str) String representation
        '''
        lines = ['[%s]' % self.getName()]
        for name in sorted([n for n in dir(self) if n.startswith('F_')]):
            lines.append('%s = %r' % (name, getattr(self, name)))
        # end for

        for name in sorted([n for n in dir(self) if isinstance(getattr(self, n), AbstractSubSystem)]):
            subString = str(getattr(self, name))

            lines.extend(['  %s' % line for line in subString.split('\n')])
        # end for

        return '\n'.join(lines)

    # end def __str__

    def clone(self):
        '''
        Obtains a clone of the current object

        @return (AbstractSubSystem) Clone
        '''
        result = AbstractSubSystem(None)
        for name in dir(self):
            value = getattr(self, name)
            # if value is a subsystem, clone it
            if (isinstance(value, AbstractSubSystem)):
                setattr(result, name, value.clone())
            # if the value is NOT a function or method, copy it
            elif ((not isinstance(value, MethodType))
                  and (not isinstance(value, FunctionType))
                  and not ((name.startswith('__'))
                           and (name.endswith('__')))):
                setattr(result, name, value)
            # end if
        # end for

        return result

    # end def clone

    def makeReadOnly(self, name=None):
        '''
        Renders the system read-only

        @option name [in] (str) The name of the member to render read-only.
        '''
        if (name is not None):
            self.__readOnlyAttr.add(name)

            value = getattr(self, name)
            # If the value is a HexList, make it Read-Only
            if (isinstance(value, HexList)):
                value.setReadOnly()
            # end if
        else:
            for name in dir(self):
                value = getattr(self, name)
                # if value is a subsystem, propagate the read-only-ness
                if (isinstance(value, AbstractSubSystem)):
                    value.makeReadOnly()
                # if the value is NOT a function or method,
                # And it begins with F_, make it read-only
                elif ((not isinstance(value, MethodType))
                      and (not isinstance(value, FunctionType))
                      and (name.startswith("F_"))):
                    self.makeReadOnly(name)
                # end if
            # end for
        # end if

    # end def makeReadOnly

    def __setattr__(self, name, value):
        '''
        Sets the value of an attribute.

        If the name is in the list of read-only attributes, raise an exception.

        @param  name  [in] (str) The name of the attribute to set.
        @param  value [in] (object) The value to set
        '''

        if ((hasattr(self, "_AbstractSubSystem__readOnlyAttr"))
                and (name in (self.__readOnlyAttr))):
            raise AttributeError("attribute %s is read-only" % (name))
        # end if

        # Attributes defined as a property with no setter are ignored
        if hasattr(self.__class__, name):
            classAttr = getattr(self.__class__, name)
            if ((isinstance(classAttr, property))
                    and (hasattr(classAttr, 'fset'))
                    and (classAttr.fset is None)):
                return
            # end if
        # end if

        super(AbstractSubSystem, self).__setattr__(name, value)

    # end def __setattr__

    def __iter__(self):
        return self

    # end def __iter__

    def __next__(self):
        item = None
        while item is None:
            if self.__index < len(dir(self)):
                temp = dir(self)[self.__index]
                if isinstance(getattr(self, temp), AbstractSubSystem) or temp.startswith('F_'):
                    item = temp
                # end if
            else:
                raise StopIteration
            # end if
            self.__index += 1
        # end while
        return item
    # end def __next__

# end class AbstractSubSystem

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
