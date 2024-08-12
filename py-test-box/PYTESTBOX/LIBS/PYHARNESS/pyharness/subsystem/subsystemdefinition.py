#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.subsystemdefinition

@brief  Definition of a subsystem

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist            import HexList
from pylibrary.tools.strutils          import StrAbleMixin
from weakref                            import ref
import warnings

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractSubSystemDefinition(StrAbleMixin):
    '''
    Definition of a subsystem.

    This is the base class, that defines the common behaviors.

    Implementors will rely on it to provider further ipl
    '''

    _STRABLE_FIELDS = ('name', 'doc', 'features', 'children')

    def __init__(self, parent = None):
        '''
        Constructor

        @option parent    [in] (SubSystem) Parent node for this subsystem.
        '''
        super(AbstractSubSystemDefinition, self).__init__()

        self._parent    = None

        self.parent    = parent
    # end def __init__


    def hasChild(self, childName):
        '''
        Checks if a child SubSystem exists by name

        @param  childName [in] (str) Name of the target subSystemDefinition to check

        @return Whether the SubSystemDefinition exists
        '''
        raise NotImplementedError
    # end def hasChild

    def getChild(self, childName):
        '''
        Obtains a child subSystem by name.

        @param  childName [in] (str) Name of the target subSystemDefinition

        @return The target SubSystemDefinition
        '''
        raise NotImplementedError
    # end def getChild

    def getChildren(self, recursive = False):
        '''
        Obtains the children of the current subsystem.

        @option recursive [in] (bool) Whether only the immediate children (default) are obtained.

        @return The children of the current subsystem.
        '''
        raise NotImplementedError
    # end def getChildren

    def getDoc(self):
        '''
        Obtain the doc for this subsystem.

        @return The doc for this subsystem.
        '''
        raise NotImplementedError
    # end def getDoc

    def hasFeature(self, name):
        '''
        Tests whether a definition contains a feature.

        @param  name [in] (str) The name of the feature to look up

        @return Whether the definition contains the given feature
        '''
        raise NotImplementedError
    # end def hasFeature

    def getPath(self):
        '''
        Obtains the path for this SubSystemDefinition

        @return The absolute path for this SubSystemDefinition
        '''
        raise NotImplementedError
    # end def getPath

    def getLocations(self):
        '''
        Obtain the locations for this subsystem.

        @return The locations for this subsystem.
        '''
        raise NotImplementedError
    # end def getLocations

    def getFeature(self, featureName):
        '''
        Obtains a child feature by name.

        @param  featureName [in] (str) Name of the target subSystemDefinition

        @return The target FeatureDefinition
        '''
        raise NotImplementedError
    # end def getFeature

    def getFeatures(self):
        '''
        Obtains the features of the current subsystem.

        @return The features of the current subsystem.
        '''
        raise NotImplementedError
    # end def getFeatures

    def getName(self):
        '''
        Obtain the name for this subsystem.

        @return The name for this subsystem.
        '''
        raise NotImplementedError
    # end def getName

    def getParent(self):
        '''
        Gets the parent SubSystem.

        @return (SubSystem) The parent subsystem, or None if no parent exists.
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

# end class AbstractSubSystemDefinition

class SubSystemDefinition(AbstractSubSystemDefinition):
    '''
    Definition for a SubSystem.

    This should match the definition, found in:
    <ul>
      <li>@c features.py files</li>
      <li>@c features.xml files</li>
    </ul>

    This is NOT intented to be used by client applications.

    Load/save code should not be found in the definition itself, but in importer/exporters.
    This will allow an easier migration from .py files to .xml files.
    '''

    class FeatureDefinition(StrAbleMixin):
        '''
        Definition of a feature.
        '''

        KNOWN_TYPES = {'int':    int,
                       'float':  float,
                       'hexlist': HexList,
                       'string': str
                       }

        _STRABLE_FIELDS = ('name', 'doc', 'default', 'type', 'format', 'choices', 'editable')

        def __init__(self, name,
                           parent   = None,
                           doc      = None,
                           default  = None,
                           type     = None,                                                                             #@ReservedAssignment pylint:disable=W0622
                           format   = '%s',                                                                             #@ReservedAssignment pylint:disable=W0622
                           choices  = None,
                           editable = False,
                           aliases  = tuple(),
                           ):
            '''
            Constructor

            @param  name     [in] (str) Name for this feature.
            @option parent   [in] (SubSystem) parent subsystem for this feature.
            @option doc      [in] (str) Documentation for this feature.
            @option default  [in] (str) Default value for this feature.
            @option type     [in] (str) Type for this feature.
            @option format   [in] (str) Format string for user-friendly representation of this feature.
            @option choices  [in] (list) List of allowed values, for choice items
            @option editable [in] (bool) Whether the feature is editable or not.
            @option aliases  [in] (tuple) List of aliases for this feature name.
            '''
            super(SubSystemDefinition.FeatureDefinition, self).__init__()

            self._name     = None
            self._parent   = None
            self._doc      = None
            self._default  = None
            self._type     = None
            self._format   = None
            self._choices  = None
            self._editable = None
            self._aliases  = None

            self.name     = name
            self.parent   = parent
            self.doc      = doc
            self.default  = default
            self.type     = type if type is not None else "auto"
            self.format   = format
            self.choices  = choices
            self.editable = editable
            self.aliases  = aliases
        # end def __init__

        def getName(self):
            '''
            Obtain the name for this subsystem.

            @return The name for this subsystem.
            '''
            return self._name
        # end def getName

        def setName(self, name):
            '''
            Sets the name for this subsystem

            @param name [in] (str) The name for this subsystem.
            '''
            self._name = name
        # end def setName

        name = property(getName, setName)

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

            @param parent [in] (SubSystem) The parent subsystem.
            '''
            if (parent is not None):
                parent = ref(parent)
            # end if

            self._parent = parent
        # end def setParent

        parent = property(getParent, setParent)

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

        def getDefault(self):
            '''
            Obtain the default for this subsystem.

            @return The default for this subsystem.
            '''
            return self._default
        # end def getDefault

        def setDefault(self, default):
            '''
            Sets the default for this subsystem

            @param default [in] (str) The default for this subsystem.
            '''
            self._default = default
        # end def setDefault

        default = property(getDefault, setDefault)

        def getType(self):
            '''
            Obtain the type for this subsystem.

            @return The type for this subsystem.
            '''
            return self._type
        # end def getType

        def setType(self, type):                                                                                        #@ReservedAssignment pylint:disable=W0622
            '''
            Sets the type for this subsystem

            @param type [in] (str) The type for this subsystem.
            '''
            self._type = type
        # end def setType

        type = property(getType, setType)                                                                               #@ReservedAssignment

        def getFormat(self):
            '''
            Obtain the format for this subsystem.

            @return The format for this subsystem.
            '''
            return self._format
        # end def getFormat

        def setFormat(self, format):                                                                                    #@ReservedAssignment pylint:disable=W0622
            '''
            Sets the format for this subsystem

            @param format [in] (str) The format for this subsystem.
            '''
            self._format = format
        # end def setFormat

        format = property(getFormat, setFormat)                                                                         #@ReservedAssignment

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

            @param editable [in] (str) The editable for this subsystem.
            '''
            self._editable = editable
        # end def setEditable

        editable = property(getEditable, setEditable)

        def getPath(self):
            '''
            Computes the path to this feature

            @return The path to this feature.
            '''
            return '/'.join((self.parent.getPath(), self._name))
        # end def getPath

        path = property(getPath)

        def getAliases(self):
            '''
            Obtain the aliases for this subsystem.

            @return The aliases for this subsystem.
            '''
            return self._aliases
        # end def getAliases

        def setAliases(self, aliases):
            '''
            Sets the aliases for this subsystem

            @param aliases [in] (str) The aliases for this subsystem.
            '''
            self._aliases = aliases
        # end def setAliases

        aliases = property(getAliases, setAliases)

        def __eq__(self, other):
            '''
            Compares two SubSystemDefinitions for equality

            @param other [in] (SubSystemDefinition) the item to compare to
            @return The comparison result
            '''

            result = other is not None

            if (result):
                result = self.name == other.name
            # end if

            if (result):
                result = self.doc == other.doc
            # end if

            if (result):
                result = self.default == other.default
            # end if

            if (result):
                result = self.type == other.type
            # end if

            if (result):
                result = self.format == other.format
            # end if

            if (result):
                result = self.choices == other.choices
            # end if

            if (result):
                result = self.editable == other.editable
            # end if

            if (result):
                result = self.aliases == other.aliases
            # end if

            return result
        # end def __eq__

        def __ne__(self, other):
            '''
            Compares two SubsystemDefinitions for non-equality

            @param other [in] (SubSystemDefinition) the item to compare to
            @return The comparison result
            '''
            return not (self == other)
        # end def __ne__

        def __str__(self):
            '''
            Converts the current object to as string.

            @return The current object, as a string.
            '''
            return '%s (%s)' % (self.name, self.type)
        # end def __str__

        __repr__ = __str__
    # end class FeatureDefinition

    def __init__(self, name,
                       parent    = None,
                       doc       = None,
                       children  = None,
                       features  = None,
                       locations = None):
        '''
        Builds a new subsystem definition.

        @param  name      [in] (str)  Name for this subsystem.
                                      This is the relative part of the path, and does not include the parent.
        @option parent    [in] (SubSystem) Parent node for this subsystem.
        @option doc       [in] (str)  The documentation for this subsystem.
        @option children  [in] (list) The children for this subsystem.
        @option features  [in] (list) The child features for this subsystem
        @option locations [in] (list) Path to the 'packages' or 'relative directories' of the file defining the subsystem.
        '''
        super(SubSystemDefinition, self).__init__(parent = parent)

        self._name           = None
        self._doc            = None
        self._children       = {}
        self._features       = {}
        self._featureAliases = {}
        self._locations      = None

        self.name      = name
        self.doc       = doc
        self.children  = children if children is not None else []
        self.features  = features if features is not None else []
        self.locations = locations

        if not self.hasFeature('Enabled'):
            self.addFeature(self.FeatureDefinition('Enabled',
                                                   type    = 'boolean',
                                                   default = 'true'))
        # end if
    # end def __init__

    def getName(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getName
        '''
        return self._name
    # end def getName

    def setName(self, name):
        '''
        Sets the name for this subsystem

        @param name [in] (str) The name for this subsystem.
        '''
        self._name = name
    # end def setName

    name = property(getName, setName)

    def getDoc(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getDoc
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

    def addChild(self, child):
        '''
        Adds a subsystem as child of the current one.

        Also sets the parent of the child subsystem to the current object

        @param child [in] (SubSystem) The subsystem to add as a child.
        '''
        child.setParent(self)

        self._children[child.name] = child
    # end def addChild

    def addChildren(self, children):
        '''
        Adds a list of subsystems as children of the current one.

        Also sets the parent of the child subsystems to the current object

        @param children [in] (list) The subsystems to add as a children.
        '''
        for child in children:
            self.addChild(child)
        # end for
    # end def addChildren

    def hasChild(self, childName):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.hasChild
        '''
        subChildName = None
        if '/' in childName:
            childName, subChildName = childName.split('/', 1)
        # end if

        if childName not in self._children:
            result = False
        elif subChildName is None:
            result = True
        else:
            result = self._children[childName].hasChild(subChildName)
        # end if

        return result
    # end def hasChild

    def getChild(self, childName):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getChild
        '''
        subChildName = None
        if '/' in childName:
            childName, subChildName = childName.split('/', 1)
        # end if
        # Find the immediate child
        result = self._children.get(childName, None)

        if result is None:
            raise ValueError('SubSystem %s has no child %s' % (self.getPath(), childName))
        # end if

        # Find the sub-child
        if subChildName is not None:
            result = result.getChild(subChildName)
        # end if

        return result
    # end def getChild

    def getChildren(self, recursive=False):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getChildren
        '''
        result = []
        children = list(self._children.values())
        result.extend(children)

        # Recursive call if needed
        if recursive:
            for child in children:
                result.extend(child.getChildren(recursive = recursive))
            # end for
        # end if

        return sorted(result,
                      key = lambda s: s.name)
    # end def getChildren

    def setChildren(self, children):
        '''
        Sets the children of the current subsystem.

        @param children [in] (list) The children to set.
        '''
        self._children = {}
        self.addChildren(children)
    # end def setChildren

    children = property(getChildren, setChildren)

    def hasFeature(self, name):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.hasFeature
        '''
        return name in self._features
    # end def hasFeature

    def addFeature(self, feature):
        '''
        Adds a FeatureDefinition as feature of the current one.

        Also sets the parent of the feature to the current object

        @param  feature [in] (FeatureDefinition) The feature to add
        '''
        feature.setParent(self)

        self._features[feature.name] = feature
        for alias in feature.aliases:
            if alias in self._featureAliases:
                raise ValueError('Feature Alias %s is claimed by both %s and %s.' % (alias,
                                                                                     self._featureAliases[alias].name,
                                                                                     feature.name))
            # end if

            self._featureAliases[alias] = feature
        # end for
    # end def addFeature

    def addFeatures(self, features):
        '''
        Adds a list of features as features of the current one.

        Also sets the parent of the features to the current object

        @param  features [in] (list) The features definitions to add as a features.
        '''
        for feature in features:
            self.addFeature(feature)
        # end for
    # end def addFeatures

    def getFeature(self, featureName):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getFeature
        '''
        result = self._features.get(featureName, None)
        if result is None:
            # Lookup aliases
            if featureName in self._featureAliases:
                result = self._featureAliases[featureName]
                warnings.warn("Using deprecated feature %s.F_%s, use %s instead." % (self.getPath(),
                                                                                     featureName,
                                                                                     result.name),
                              category   = DeprecationWarning,
                              stacklevel = 1)
            else:
                raise ValueError('SubSystem %s has no child %s' % (self.getPath(), featureName))
            # end if
        # end if

        return result
    # end def getFeature

    def getFeatures(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getFeatures
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
        self._featureAliases = {}
        self.addFeatures(features)
    # end def setFeatures

    features = property(getFeatures, setFeatures)

    def getLocations(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getLocations
        '''
        return self._locations
    # end def getLocations

    def setLocations(self, locations):
        '''
        Sets the locations for this subsystem

        @param  locations [in] (str) The locations for this subsystem.
        '''
        self._locations = locations
    # end def setLocations

    locations = property(getLocations, setLocations)

    def __eq__(self, other):
        '''
        Compares two SubSystemDefinitions for equality

        @param  other [in] (SubSystemDefinition) the item to compare to

        @return The comparison result
        '''

        result = (other is not None) and (isinstance(other, SubSystemDefinition))

        if (result):
            result = self.name == other.name
        # end if

        if (result):
            result = self.doc == other.doc
        # end if

        if (result):
            result = self.children == other.children
        # end if

        if (result):
            result = self.features == other.features
        # end if

        return result
    # end def __eq__

    def __ne__(self, other):
        '''
        Compares two SubsystemDefinitions for non-equality

        @param  other [in] (SubSystemDefinition) the item to compare to

        @return The comparison result
        '''
        return not (self == other)
    # end def __ne__

    def getPath(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getPath
        '''
        parent = self.parent
        if (parent is not None):
            parentPath = self.parent.getPath()
            if parentPath is not None:
                result = '/'.join((parentPath, self.name))
            else:
                result = self.name
            # end if
        else:
            result = self.name
        # end if

        return result
    # end def getPath

# end class SubSystemDefinition

class AggregatingSubSystemDefinition(AbstractSubSystemDefinition):
    '''
    A SubSystemDefinition that aggregates twin SubSystemDefinitions, presenting only one instance.
    '''

    def __init__(self, subSystemDefinitions = tuple()):
        '''
        Constructor

        @param  subSystemDefinitions [in] (list) The SubSystems to aggregate
        '''

        super(AggregatingSubSystemDefinition, self).__init__()

        self._subSystemDefinitions = list(subSystemDefinitions)
    # end def __init__

    def hasChild(self, childName):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.hasChild
        '''
        for subSystemDefinition in self._subSystemDefinitions:
            if subSystemDefinition.hasChild(childName):
                result = True
                break
            # end if
        else:
            result = False
        # end for

        return result
    # end def hasChild

    def getChild(self, childName):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getChild
        '''
        for subSystemDefinition in self._subSystemDefinitions:
            if subSystemDefinition.hasChild(childName):
                result = subSystemDefinition.getChild(childName)
                break
            # end if
        else:
            definitionLocation = ''
            if self.locations:
                definitionLocation = ('\n  Definition at %s' % ('\n  Definition at '.join(self.locations)))
            # end if

            raise ValueError('SubSystem %s has no child %s%s' % (self.getPath(),
                                                                 childName,
                                                                 definitionLocation))
        # end for

        return result
    # end def getChild

    def getChildren(self, recursive=False):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getChildren
        '''
        children = []
        for subSystemDefinition in self._subSystemDefinitions:
            children.extend(subSystemDefinition.getChildren(recursive = recursive))
        # end for

        return children
    # end def getChildren

    children = property(getChildren)

    def getDoc(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getDoc
        '''
        docs = set()
        for subSystemDefinition in self._subSystemDefinitions:
            doc = subSystemDefinition.getDoc()
            if doc is not None:
                docs.add(doc)
            # end if
        # end for

        return '\n'.join(sorted(docs))
    # end def getDoc

    doc = property(getDoc)

    def hasFeature(self, name):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.hasFeature
        '''
        for subSystemDefinition in self._subSystemDefinitions:
            if subSystemDefinition.hasFeature(name):
                result = True
                break
            # end if
        else:
            result = False
        # end for

        return result
    # end def hasFeature

    def getPath(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getPath
        '''
        result = None
        if len(self._subSystemDefinitions):
            result = self._subSystemDefinitions[0].getPath()
        # end if

        return result
    # end def getPath

    path = property(getPath)

    def getLocations(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getLocations
        '''
        result = []
        for subSystemDefinition in self._subSystemDefinitions:
            locations = subSystemDefinition.getLocations()
            if locations is not None:
                result.extend(locations)
            # end if
        # end for

        return result
    # end def getLocations

    locations = property(getLocations)

    def getFeature(self, featureName):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getFeature
        '''
        result = None
        for subSystemDefinition in self._subSystemDefinitions:
            if subSystemDefinition.hasFeature(featureName):
                result = subSystemDefinition.getFeature(featureName)
                break
            # end if
        else:
            raise ValueError('Feature %s has no child %s' % (self.getPath(), featureName))
        # end for

        return result
    # end def getFeature

    def getFeatures(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getFeatures
        '''
        result = []
        for subSystemDefinition in self._subSystemDefinitions:
            result.extend(subSystemDefinition.getFeatures())
        # end for

        return result
    # end def getFeatures

    features = property(getFeatures)

    def getName(self):
        '''
        @copydoc pyharness.subsystem.subsystemdefinition.AbstractSubSystemDefinition.getName
        '''
        result = None
        if len(self._subSystemDefinitions):
            result = self._subSystemDefinitions[0].getName()
        # end if

        return result
    # end def getName

    name = property(getName)

# end class AggregatingSubSystemDefinition

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
