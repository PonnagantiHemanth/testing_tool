#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.subsystembuilder

@brief Builder for a SubSystem.

@author christophe.roquebert

@date   2018/10/21
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.subsystem.stringutils            import StringUtils
from pyharness.subsystem.subsystemdefinition    import AggregatingSubSystemDefinition
from pyharness.subsystem.subsysteminstantiation import SubSystemInstantiation
from pyharness.systems                         import AbstractSubSystem
from os.path                                  import abspath
from os.path                                  import normpath
from os.path                                  import sep

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SubSystemBuilder(object):
    '''
    Builds a full sub-system, based on:
    - A SubSystemDefinition importer
    - A SubSystemInstantiation importer
    - A @c PRODUCT , @c VARIANT , @c TARGET combination
    .

    Note that the target is ignored for now.
    '''

    def __init__(self, subSystemDefinitionImporter,
                       subSystemInstantiationImporter):
        '''
        Constructor

        @param  subSystemDefinitionImporter    [in] (SubSystemDefinitionImporter) importer
        @param  subSystemInstantiationImporter [in] (SubSystemInstantiationImporter) importer
        '''
        self._subSystemDefinitionImporter = subSystemDefinitionImporter
        self._subSystemInstantiationImporter = subSystemInstantiationImporter

        self._rootSubSystemDefinition = None
    # end def __init__

    class AliasAccessor(object):
        '''
        An accessor to an aliased feature.
        '''
        def __init__(self, name):
            '''
            Constructor

            @param  name [in] (str) Name of the aliased feature.
            '''
            self._name = 'F_%s' % name
        # end def __init__

        def __get__(self, instance, owner):
            '''
            Obtains the feature.

            @param  instance [in] (AbstractSubSystem) The subsystem instance on which the feature is obtained.
            @param  owner    [in] (Type)              The subsystem type on which the feature is obtained.

            @return The aliased feature value
            '''
            if hasattr(instance, self._name):
                import warnings
                warnings.warn("Reading aliased feature in %s should use %s instead." % (instance.name,
                                                                                        self._name),
                              category = DeprecationWarning,
                              stacklevel = 1)
                return getattr(instance, self._name)
            else:
                raise AttributeError('%s has no target feature: %s' % (instance.getPath(),
                                                                       self._name))
            # end if
        # end def __get__

        def __set__(self, instance, value):
            '''
            Sets the feature value

            @param  instance [in] (AbstractSubSystem) The subsystem instance on which the feature is obtained.
            @param  value    [in] (object)            The aliased feature value
            '''
            if hasattr(instance, self._name):
                import warnings
                warnings.warn("Setting aliased feature in %s, should use %s instead." % (instance.name,
                                                                                         self._name),
                              category = DeprecationWarning,
                              stacklevel = 1)
                setattr(instance, self._name, value)
            else:
                raise AttributeError('%s has no target feature: %s' % (instance.getPath(),
                                                                       self._name))
            # end if
        # end def __set__

        def __delete__(self, instance):
            '''
            Deletes the feature value.

            This is stubbed, as this should never happen.

            @param  instance [in] (AbstractSubSystem) The subsystem instance on which the feature is obtained.
            '''
            raise NotImplementedError
        # end def __delete__
    # end class AliasAccessor

    def _createBlankSubsystem(self, subSystemDefinition):
        '''
        Creates a blank subsystem, from the root subsystem definition.

        @param  subSystemDefinition [in] (SubSystemDefinition) The root subsystem definition.

        @return The AbstractSubSystem for this definition
        '''

        # Container
        class InnerSubSystem(AbstractSubSystem):
            '''
            Inner definition of the SubSystem type.

            This is used for features aliasing
            '''
        # end class InnerSubSystem
        subSystem = InnerSubSystem(subSystemDefinition.name)

        # Features
        for featureDefinition in subSystemDefinition.features:
            # The feature value.
            setattr(subSystem, 'F_%s' % featureDefinition.name, StringUtils.stringToPython(featureDefinition.default,
                                                                                           featureDefinition.type))

            # The feature alias values: Define local properties for access
            for alias in featureDefinition.aliases:
                setattr(subSystem.__class__,
                        'F_%s' % alias,
                        self.AliasAccessor(featureDefinition.name))
            # end for

            # The feature choices
            if featureDefinition.choices is not None:
                setattr(subSystem, 'C_%s' % featureDefinition.name, tuple(featureDefinition.choices))
            # end if
        # end for

        # Sub-systems
        for childSubSystemDefinition in subSystemDefinition.children:
            # The subSystem value
            setattr(subSystem, childSubSystemDefinition.name, self._createBlankSubsystem(childSubSystemDefinition))
        # end for

        return subSystem
    # end def _createBlankSubsystem

    @staticmethod
    def _getSubSystem(rootSubSystem,
                      path):
        '''
        Obtains the target subsystem.

        @param  rootSubSystem [in] (AbstractSubSystem) The root subsystem
        @param  path          [in] (str) Path to the target subsystem.

        @return The target subsystem definition.
        '''
        subSystem = rootSubSystem

        # Find the targeted sub-system
        for pathElement in normpath(path).split(sep):

            # If this crashes, this is because of an inconsistency between:
            # - The subsystem (name)
            # - The path
            subSystem = subSystem.getChild(pathElement)
        # end for

        return subSystem
    # end def _getSubSystem

    def _applyInstantiation(self, rootSubSystemDefinition,
                                  rootSubSystem,
                                  subSystemInstantiation):
        '''
        Applies an instantiation to the root subsystem.
        This will cause the feature values to evolve, refining them toward
        PRODUCT/VARIANT/TARGET/OVERRIDE specialization.

        @param  rootSubSystemDefinition [in] (AbstractSubSystem) The root subsystem definition.
        @param  rootSubSystem           [in] (AbstractSubSystem) The root subsystem.
        @param  subSystemInstantiation  [in] (SubSystemInstantiation) The instantiation to apply.
        '''
        try:
            subSystemDefinition = rootSubSystemDefinition.getChild(subSystemInstantiation.path)
        except ValueError as excp:
            raise ValueError('Instantiation location: %s\n%s' % (subSystemInstantiation.location, str(excp)))
        # end try


        # Obtain the target subSystem
        subSystem = self._getSubSystem(rootSubSystem, subSystemInstantiation.path)

        # Apply the changes
        for featureInstantiation in subSystemInstantiation.features:

            featureDefinition = subSystemDefinition.getFeature(featureInstantiation.name)

            featureName = 'F_' + featureInstantiation.name

            # If this crashes, this is because of an inconsistency between:
            # The feature definition (name)
            # The feature instantiation (name)
            if (not hasattr(subSystem, featureName)):
                raise ValueError('No feature with name %s in subSystem %s' % (featureName, subSystemInstantiation.path))
            # end if

            if featureInstantiation.value is SubSystemInstantiation.FeatureInstantiation.UNSET:
                featureInstantiation.value = featureDefinition.default
            # end if
            featureValue = featureInstantiation.getTypedValue(featureDefinition.type)

            # If the featureDefinition is a choice-type, check that the value is within the accepted values.
            featureValueChoices = featureDefinition.choices
            if (    (featureValueChoices is not None)
                and (featureValue not in featureValueChoices)):
                raise ValueError('The feature %s.%s should be one of:\n - %s' % (subSystemInstantiation.path,
                                                                                 featureName,
                                                                                 '\n - '.join((repr(choice) for choice in featureValueChoices))))
            # end if

            setattr(subSystem, featureName, featureValue)
        # end for

        for childSubSystemInstantiation in subSystemInstantiation.children:
            self._applyInstantiation(rootSubSystemDefinition, rootSubSystem, childSubSystemInstantiation)
        # end for
    # end def _applyInstantiation

    @classmethod
    def createSubSystemInstantiation(cls, rootSubSystemDefinition,
                                          rootSubSystem):
        '''
        Creates a SubSystemInstantiation from the root definition and a consolidated version of the features.

        @param  rootSubSystemDefinition [in] (SubSystemDefinition) The root definition
        @param  rootSubSystem           [in] (AbstractSubSystem)   The root subsystem

        @return (SubSystemInstantiation) The new instantiation
        '''
        rootSubSystemInstantiation = SubSystemInstantiation()
        def visitSubSystemDefinition(subSystemDefinition):
            '''
            Creates the SubSystemInstantiation associated with this definition.

            @param  subSystemDefinition [in] (SubSystemDefinition) SubSystem Definition
            '''
            path = subSystemDefinition.getPath()
            subSystemInstantiation = rootSubSystemInstantiation
            relativePathElements = []
            for pathElement in path.split('/'):
                relativePathElements.append(pathElement)
                if not subSystemInstantiation.hasChild(pathElement):
                    childSubSystemInstantiation = SubSystemInstantiation('/'.join(relativePathElements))
                    subSystemInstantiation.addChild(childSubSystemInstantiation)
                # end if
                subSystemInstantiation = subSystemInstantiation.getChild(pathElement)
            # end for

            for childSubSystemDefinition in subSystemDefinition.getChildren():
                visitSubSystemDefinition(childSubSystemDefinition)
            # end for

            for childFeatureDefinition in subSystemDefinition.getFeatures():
                visitFeatureDefinition(childFeatureDefinition, subSystemInstantiation)
            # end for

        # end def visitSubSystemDefinition

        def visitFeatureDefinition(featureDefinition, subSystemInstantiation):
            '''
            Creates the FeatureInstantiation associated with this definition.

            @param  featureDefinition      [in] (FeatureDefinition)      Feature definition
            @param  subSystemInstantiation [in] (SubSystemInstantiation) SubSystem Instantiation
            '''
            path = featureDefinition.getPath()
            node = rootSubSystem
            for pathElement in path.split('/'):
                node = getattr(node, pathElement)
            # end for
            featureValue = node

            featureInstantiation = subSystemInstantiation.FeatureInstantiation(name = featureDefinition.name,
                                                                               value = featureValue,
                                                                               type = featureDefinition.type)
            subSystemInstantiation.addChild(featureInstantiation)

        # end def visitFeatureDefinition

        visitSubSystemDefinition(rootSubSystemDefinition)

        return rootSubSystemInstantiation

    # end def createSubSystemInstantiation

    def load(self, rootDefinitionPaths,
                   leafInstantiationPaths,
                   additionalSubSystemInstantiations = tuple()):
        '''
        Loads the definitions and the instantiations from the given configuration,
        and builds the features.

        @param  rootDefinitionPaths               [in] (list) Paths to the roots of feature definitions.
        @param  leafInstantiationPaths            [in] (list) Paths to the leaves of feature instantiations.
        @option additionalSubSystemInstantiations [in] (list) Additional instantiations, to be applied at end of construction.

        @return A root subsystem
        '''

        # Obtain the root subsystem definition
        if (self._rootSubSystemDefinition is None):
            assert not isinstance(rootDefinitionPaths, str) # This is a common error, that can lead to infinite loops
            self._rootSubSystemDefinition = self.loadRootSubSystemDefinition(rootDefinitionPaths)
        # end if
        rootSubSystemDefinition = self._rootSubSystemDefinition

        # Obtain the default-value-initialized root subsystem
        rootSubSystem = self._createBlankSubsystem(rootSubSystemDefinition)

        # Obtain the instantiations, starting from the PRODUCT, ending with the VARIANT (or target...)
        subSystemInstantiations = self.loadSubSystemInstantiations(leafInstantiationPaths)
        subSystemInstantiations.extend(additionalSubSystemInstantiations)

        # Apply the instantiations, building the actual rootSubSystem
        for subSystemInstantiation in subSystemInstantiations:
            self._applyInstantiation(rootSubSystemDefinition,
                                     rootSubSystem,
                                     subSystemInstantiation)
        # end for

        return rootSubSystem
    # end def load

    def loadRootSubSystemDefinition(self, rootDefinitionPaths):
        '''
        Loads the definitions for the given configuration.

        @param  rootDefinitionPaths [in] (str) Path to the root of feature definitions.

        @return (SubSystemDefinition) The root subsystem definition.
        '''
        sortedRootDefinitionPaths = list(rootDefinitionPaths)
        sortedRootDefinitionPaths.sort()

        def isParent(parent, child):
            '''
            Check if child is a child path of parent

            @param  parent [in] (str) Parent path
            @param  child  [in] (str) Child path

            @return (bool) True if child is child of parent
            '''
            parent = abspath(parent) + sep
            child = abspath(child)
            return child.startswith(parent)
        # end def isParent

        rootDefinitions = []
        validRootDefinitionPaths = set()
        for rootDefinitionPath in sortedRootDefinitionPaths:
            if not any((isParent(validRootDefinitionPath, rootDefinitionPath)
                        for validRootDefinitionPath in validRootDefinitionPaths)):
                subRootDefinitions = self._subSystemDefinitionImporter.load(rootDefinitionPath)
                if subRootDefinitions:
                    validRootDefinitionPaths.add(rootDefinitionPath)
                # end if
                rootDefinitions.extend(subRootDefinitions)
            # end if
        # end for

        return AggregatingSubSystemDefinition(rootDefinitions)
    # end def loadRootSubSystemDefinition

    def loadSubSystemInstantiations(self, leafInstantiationPaths):
        '''
        Loads a list of RootSubSystemInstantations

        @param  leafInstantiationPaths [in] (list) Path to the leaf of feature instantiations.

        @return (list) List of SubSystemInstantiation
        '''
        assert not isinstance(leafInstantiationPaths, str)
        subSystemInstantiations = []

        for leafInstantiationPath in leafInstantiationPaths:
            childSubSystemInstantiations = self._subSystemInstantiationImporter.load(leafInstantiationPath)
            subSystemInstantiations.extend(childSubSystemInstantiations)
        # end for

        return subSystemInstantiations
    # end def loadSubSystemInstantiations

# end class SubSystemBuilder

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
