#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.subsysteminstantiation

@brief Instantiation of a subsystem.

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.stringutils      import StringUtils
from weakref                            import ref

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SubSystemInstantiation(object):
    '''
    Reflects the actual instantiation of a SubSystem. (For instance: in a .ini
    or .xml file).
    '''

    class FeatureInstantiation(object):
        '''
        Instantiation of a feature.
        '''
        UNSET = object()

        def __init__(self, name,
                           parent   = None,
                           value    = None,
                           location = None,
                           type     = 'auto',                                                                           #@ReservedAssignment #pylint:disable=W0622
                           doc      = None,
                           choices  = None,
                           editable = False
                           ):
            '''
            Constructor

            @param  name     [in] (str)       Name for this feature.
            @option parent   [in] (SubSystem) Parent subsystem for this feature.
            @option value    [in] (str)       Value for the feature
            @option location [in] (str)       The location where this feature is defined
            @option type     [in] (str,None)  Hint on the type for the feature value.
            @option doc      [in] (str)       Documentation for this feature.
            @option choices  [in] (list)      List of allowed values, for choice items
            @option editable [in] (bool)      Whether the feature is editable or not.
            '''
            self._name      = None
            self._parent    = None
            self._choices   = None
            self._value     = None
            self._location  = None
            self._type      = None
            self._editable  = None
            self._doc       = None

            self.name     = name
            self.parent   = parent
            self.value    = value
            self.location = location
            self.type     = type
            self.doc      = doc
            self.choices  = choices
            self.editable = editable
        # end def __init__

        def getName(self):
            '''
            Obtain the name for this subsystem.

            @return (str) The name for this subsystem.
            '''
            return self._name
        # end def getName

        def setName(self, name):
            '''
            Sets the name for this subsystem

            @param  name [in] (str) The name for this subsystem.
            '''
            self._name = name
        # end def setName

        name = property(getName, setName)

        def getParent(self):
            '''
            Obtain the parent SubSystem, or None for the root subsystem (or orphan subsystems).

            @return (SubSystem) The parent SubSystem, or None.
            '''
            result = None
            if (self._parent is not None):
                result = self._parent()
            # end if

            return result
        # end def getParent

        def setParent(self, parent):
            '''
            Sets the parent SubSystem.

            @param  parent [in] (SubSystem) The parent subsystem.
            '''
            if (parent is not None):
                parent = ref(parent)
            # end if

            self._parent = parent
        # end def setParent

        parent = property(getParent, setParent)

        def getValue(self):
            '''
            Obtain the value for this subsystem.

            @return (str) The value for this subsystem.
            '''
            return self._value
        # end def getValue

        def setValue(self, value):
            '''
            Sets the value for this subsystem

            @param  value [in] (str) The value for this subsystem.
            '''
            self._value = value
        # end def setValue

        value = property(getValue, setValue)

        def getLocation(self):
            '''
            Obtain the location for this subsystem.

            @return (str) The location for this subsystem.
            '''
            return self._location
        # end def getLocation

        def setLocation(self, location):
            '''
            Sets the location for this subsystem

            @param  location [in] (str) The location for this subsystem.
            '''
            self._location = location
        # end def setLocation

        location = property(getLocation, setLocation)

        def getType(self):
            '''
            Obtain the type for this subsystem.

            @return The type for this subsystem.
            '''
            return self._type
        # end def getType

        def setType(self, type):                                                                                        #@ReservedAssignment #pylint:disable=W0622
            '''
            Sets the type for this subsystem

            @param type [in] (str) The type for this subsystem.
            '''
            self._type = type
        # end def setType

        type = property(getType, setType)                                                                               #@ReservedAssignment #pylint:disable=W0622

        def getDoc(self):
            '''
            Obtain the doc for this subsystem.

            @return The doc for this subsystem.
            '''
            return self._doc
        # end def getDoc

        def setDoc(self, doc):
            '''
            Sets the doc for this subsystem

            @param doc [in] (str) The doc for this subsystem.
            '''
            self._doc = doc
        # end def setDoc

        doc = property(getDoc, setDoc)

        def getChoices(self):
            '''
            Obtain the choices for this subsystem.

            @return The choices for this subsystem.
            '''
            return self._choices
        # end def getChoices

        def setChoices(self, choices):                                                                                    # pylint:disable=W0622
            '''
            Sets the choices for this subsystem

            @param choices [in] (str) The choices for this subsystem.
            '''
            self._choices = choices
        # end def setChoices

        choices = property(getChoices, setChoices)

        def getEditable(self):
            '''
            Obtain the editable for this subsystem.

            @return The editable for this subsystem.
            '''
            return self._editable
        # end def getEditable

        def setEditable(self, editable):
            '''
            Sets the editable for this subsystem

            @param  editable [in] (str) The editable for this subsystem.
            '''
            self._editable = editable
        # end def setEditable

        editable = property(getEditable, setEditable)

        def __eq__(self, other):
            '''
            Compares two SubSystemInstantiations for equality

            @param  other [in] (SubSystemInstantiation) the item to compare to

            @return (bool) The comparison result
            '''
            result = other is not None

            if (result):
                result = self.name == other.name
            # end if

            if (result):
                result = self.value == other.value
            # end if

            if result:
                result = (   (self.type == 'auto')
                          or (other.type == 'auto')
                          or (self.type == other.type))
            # end if

            return result
        # end def __eq__

        def __ne__(self, other):
            '''
            Compares two SubsystemInstantiations for non-equality

            @param  other [in] (SubSystemInstantiation) the item to compare to

            @return (bool) The comparison result
            '''
            return not (self == other)
        # end def __ne__

        def __str__(self):
            '''
            Converts the current object to a string.

            @return (str) The current object, as a string.
            '''
            return '%s = %s' % (self.name, self.value)
        # end def __str__

        __repr__ = __str__

        def getTypedValue(self, fType):
            '''
            Obtains the python-translated value for this instantiation

            @param  fType [in] (str) Type of the value to interpret.

            @return The interpreted value
            '''
            if (   (fType == 'auto')
                or (    (type(fType) == type(tuple()))
                    and (self.type in fType))):
                fType = self.type

            elif (    (fType != self.type)
                  and (self.type != 'auto')):
                raise ValueError('Inconsistent value between type and type hint')

            # end if

            return StringUtils.stringToPython(self.value, fType)
        # end def getTypedValue

        def setTypedValue(self, type, value):                                                                           #@ReservedAssignment #pylint:disable=W0622
            '''
            Sets the python-translated value for this instantiation.

            @param  type  [in] (str)    Type of the value to interpret.
            @param  value [in] (object) Value to set
            '''
            self.value = StringUtils.pythonToString(value, type)
        # end def setTypedValue
    # end class FeatureInstantiation


    def __init__(self, path,
                       parent   = None,
                       children = tuple(),
                       features = tuple(),
                       location = None):
        '''
        Constructor

        @param  path     [in] (str) Path to instantiation in the subsystem instantiation tree.
                                    This is a relative path to the parent.
                                    If no parent is found, this is an absolute path.
        @option parent   [in] (SubSystemInstantiation) Parent instantiation.
        @option children [in] (list) List of SubSystemInstantiation
        @option features [in] (list) List of FeatureInstantiation
        @option location [in] (str) Location where the instantiation was defined
        '''
        self._path     = None
        self._parent   = None
        self._children = {}
        self._features = {}
        self._location = None

        self.path     = path
        self.parent   = parent
        self.children = children
        self.features = features
        self.location = location
    # end def __init__

    def getPath(self):
        '''
        Obtain the path for this subsystem.

        @return The path for this subsystem.
        '''
        return self._path
    # end def getPath

    def setPath(self, path):
        '''
        Sets the path for this subsystem

        @param  path [in] (str) The path for this subsystem.
        '''
        self._path = path
    # end def setPath

    path = property(getPath, setPath)

    def getParent(self):
        '''
        Obtain the parent SubSystem, or None for the root subsystem (or orphan subsystems).

        @return The parent SubSystem, or None.
        '''
        result = None
        if (self._parent is not None):
            result = self._parent()
        # end if

        return result
    # end def getParent

    def setParent(self, parent):
        '''
        Sets the parent SubSystem.

        @param  parent [in] (SubSystem) The parent subsystem.
        '''
        if (parent is not None):
            parent = ref(parent)
        # end if

        self._parent = parent
    # end def setParent

    parent = property(getParent, setParent)


    def addChild(self, child):
        '''
        Adds a subsystem as child of the current one.

        Also sets the parent of the child subsystem to the current object

        @param  child [in] (SubSystem) The subsystem to add as a child.
        '''
        child.setParent(self)

        self._children[child.path] = child
    # end def addChild

    def addChildren(self, children):
        '''
        Adds a list of subsystems as children of the current one.

        Also sets the parent of the child subsystems to the current object

        @param  children [in] (list) The subsystems to add as a children.
        '''
        for child in children:
            self.addChild(child)
        # end for
    # end def addChildren

    def hasChild(self, childName):
        '''
        Checks if the given child is present.

        @param  childName [in] (str) Path to the child

        @return (bool) Whether the child exists
        '''
        if (childName in self._children):
            result = True
        else:
            subChildName = None
            if ('/' in childName):
                childName, subChildName = childName.split('/', 1)
            # end if
            if (childName not in self._children):
                result = False
            elif (subChildName is None):
                result = True
            else:
                result = self._children[childName].hasChild(subChildName)
            # end if
        # end if

        return result
    # end def hasChild

    def getChild(self, childName):
        '''
        Obtains the child with the given name.

        @param  childName [in] (str) The child name (or path)

        @return The target child
        '''

        subChildName = None
        if '/' in childName:
            childName, subChildName = childName.split('/', 1)
        # end if

        child = self._children.get('/'.join((self.getPath(), childName)), None)

        if subChildName is not None:
            child = child.getChild(subChildName)
        # end if

        return child
    # end def getChild

    def getChildren(self):
        '''
        Obtains the children of the current subsystem.

        @return The children of the current subsystem.
        '''
        return sorted(list(self._children.values()),
                      key = lambda s: s.path)
    # end def getChildren

    def setChildren(self, children):
        '''
        Sets the children of the current subsystem.

        @param  children [in] (list) The children to set.
        '''
        self._children = {}
        self.addChildren(children)
    # end def setChildren

    children = property(getChildren, setChildren)

    def hasFeature(self, name):
        '''
        Tests whether a instantiation contains a feature.

        @param  name [in] (str) The name of the feature to look up

        @return (bool) Whether the instantiation contains the given feature
        '''
        return name in self._features
    # end def hasFeature

    def addFeature(self, feature):
        '''
        Adds a FeatureInstantiation as feature of the current one.

        Also sets the parent of the feature to the current object

        @param  feature [in] (FeatureInstantiation) The feature to add
        '''
        feature.setParent(self)

        self._features[feature.name] = feature
    # end def addFeature

    def addFeatures(self, features):
        '''
        Adds a list of features as features of the current one.

        Also sets the parent of the features to the current object

        @param  features [in] (list) The features instantiations to add as a features.
        '''
        for feature in features:
            self.addFeature(feature)
        # end for
    # end def addFeatures

    def getFeatures(self):
        '''
        Obtains the features of the current subsystem.

        @return The features of the current subsystem.
        '''
        return sorted(list(self._features.values()),
                      key = lambda f: f.name)
    # end def getFeatures

    def setFeatures(self, features):
        '''
        Sets the features of the current subsystem.

        @param  features [in] (list) The features to set.
        '''
        self._features = {}
        self.addFeatures(features)
    # end def setFeatures

    features = property(getFeatures, setFeatures)

    def getLocation(self):
        '''
        Obtain the location for this subsystem.

        @return The location for this subsystem.
        '''
        return self._location
    # end def getLocation

    def setLocation(self, location):
        '''
        Sets the location for this subsystem

        @param  location [in] (str) The location for this subsystem.
        '''
        self._location = location
    # end def setLocation

    location = property(getLocation, setLocation)

    def __eq__(self, other):
        '''
        Compares two SubSystemInstantiations for equality

        @param  other [in] (SubSystemInstantiation) the item to compare to

        @return The comparison result
        '''

        result = (other is not None) and (isinstance(other, SubSystemInstantiation))

        if (result):
            result = self.path == other.path
        # end if

        if (result):
            result = self.children == other.children
        # end if

        if (result):
            result = self.features == other.features
        # end if

        # DO NOT INCLUDE LOCATIONS IN COMPARISON (locations are mostly used for debug)
        # if (result):
        #     result = self.location == other.location
        # # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        '''
        Compares two SubsystemInstantiations for non-equality

        @param  other [in] (SubSystemInstantiation) the item to compare to

        @return The comparison result
        '''
        return not (self == other)
    # end def __ne__

    def __str__(self):
        '''
        Converts the current object to a string.

        @return The current object, as a string.
        '''
        return '%s\n %s' % (self.path, '\n '.join([str(x) for x in self.features]))
    # end def __str__

    __repr__ = __str__

# end class SubSystemInstantiation

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
