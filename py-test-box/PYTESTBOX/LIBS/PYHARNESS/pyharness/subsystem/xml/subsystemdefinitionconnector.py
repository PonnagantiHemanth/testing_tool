#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.xml.subsystemdefinitionconnector

@brief  Importer/exporters for python-defined subsystems

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.os.path                             import abspath
from pylibrary.tools.hexlist                        import HexList
from pylibrary.tools.importutils                   import importFqn
from datetime                                       import date
from functools                                      import lru_cache
from pyharness.subsystem.stringutils                  import StringUtils
from pyharness.subsystem.subsystemdefinition          import SubSystemDefinition
from pyharness.subsystem.subsystemdefinitionconnector import AbstractSubSystemDefinitionExporter
from pyharness.subsystem.subsystemdefinitionconnector import AbstractSubSystemDefinitionImporter
from pyharness.systems                               import AbstractSubSystem
from os.path                                        import basename
from os.path                                        import isdir
from os.path                                        import isfile
from os.path                                        import join
from os.path                                        import sep
from os.path                                        import split
from os.path                                        import splitext
import re
import sys

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

@lru_cache(32)
def cached_listdir(d):
     return os.listdir(d)
 
class PythonSubSystemDefinitionImporter(AbstractSubSystemDefinitionImporter):
    '''
    Imports a SubSystemDefinition from:
    <ul>
      <li>@c features.py files.</li>
      <li>Python packages and sub-packages containing feature.py files</li>
    </ul>
    '''

    IGNORED_SUBDIRECTORIES = ('.', '..', '.svn', 'CVS')
    FEATURES_MODULEPATTERNS = (re.compile("^features$"),
                               re.compile(r"^features[^\.]+_internal$"),
                               )

    def __init__(self):
        '''
        Constructor
        '''
        super(PythonSubSystemDefinitionImporter, self).__init__()

        self._normedSysPath = None
    # end def __init__

    def _getNormedSysPath(self):
        '''
        Obtians the normalized, cached sys.path

        @return sys.path, normalized
        '''
        if (self._normedSysPath is None):
            self._normedSysPath = [abspath(p) for p in sys.path]
        # end if

        return self._normedSysPath
    # end def _getNormedSysPath

    def _loadFromFeaturePy(self, featurePyPath):
        '''
        Loads an AbstractSubSystemDefinition from a feature.py file.

        @param  featurePyPath [in] (str) Path to the feature.py file

        @return List of SubSystemDefinition
        '''
        result = []

        # Compute the file's Fqn, and match against the PYTHONPATH
        fullPath = abspath(featurePyPath)
        fqn = None

        # Look for a PYTHONPATH root for this file.
        for sysPath in self._getNormedSysPath():

            # The first matching element is considered valid.
            # TODO This will cause problems if the PYTHONPATH contains nested elements.
            if (fullPath.startswith(sysPath)) and (fullPath[len(sysPath)] == sep):

                relativePath = fullPath[len(sysPath) + len(sep):]
                fqn = '.'.join([x for x in split(splitext(relativePath)[0]) if len(x)])
                break
            # end if
        # end for

        # Has a theoretial fqn been found ?
        if (fqn is not None):
            # We can attempt an import
            module = importFqn(fqn)

            childSubSystems = []

            # Obtain all features in this module.
            for modName in dir(module):
                obj = getattr(module, modName)
                if (    (   (isinstance(obj, type)))
                    and (issubclass(obj, AbstractSubSystem))
                    and (not (obj is AbstractSubSystem)) ):

                    # TODO This should only be checked for parent packages
                    if (len(childSubSystems) > 0):
                        raise AssertionError("Only one subsystem is allowed per package.")
                    # end if

                    childSubSystems.append(obj)
                # end if
            # end for

            result = [self._loadFromLegacySubSystem(s()) for s in childSubSystems]
        # end if

        return result
    # end def _loadFromFeaturePy

    def _loadFromLegacySubSystem(self, legacySubSystem):
        '''
        Creates a SubSystemDefinition from an AbstractSubSystem

        @param  legacySubSystem [in] (AbstractSubSystem) The subsystem to parse

        @return (SubSystemDefinition) A SubSystemDefinition translation
        '''
        # First, find the name of this subSystem
        name = legacySubSystem.getName()

        doc = legacySubSystem.__doc__

        # Second, find the child subsystems
        children = []
        for childName in dir(legacySubSystem):
            child = getattr(legacySubSystem, childName)
            if (isinstance(child, AbstractSubSystem)):
                children.append(self._loadFromLegacySubSystem(child))
            # end if
        # end for

        # Third, the features
        features = []
        for childName in [n for n in dir(legacySubSystem) if n.startswith('F_')]:
            child = getattr(legacySubSystem, childName)
            childType = 'auto'
            if (childName == 'F_Enabled'):
                childType = 'boolean'
            # end if

            if (isinstance(child, bool)):
                child = 'true' if child else 'false'
                childType = 'boolean'
            elif (isinstance(child, bytes)):
                childType = 'string'
            elif (isinstance(child, int)):
                childType = 'int'
            elif (isinstance(child, HexList)):
                childType = 'hexlist'
            # end if

            docName = 'D_' + childName[2:]
            childDoc = getattr(legacySubSystem, docName, None)
            if (childDoc is AbstractSubSystem.__doc__):
                childDoc = None
            # end if

            if childDoc is not None:
                childDoc = childDoc.strip()
            # end if

            features.append(SubSystemDefinition.FeatureDefinition(childName[2:],
                                                                  default = child,
                                                                  doc     = childDoc,
                                                                  type    = childType))
        # end for

        result = SubSystemDefinition(name,
                                     doc      = doc.strip(),
                                     children = children,
                                     features = features)

        return result
    # end def _loadFromLegacySubSystem

    @classmethod
    def _acceptableModule(cls, moduleName):
        '''
        Test whether a module name is acceptable

        @param  moduleName [in] (str) The module name to check.

        @return Whether the module name is acceptable
        '''
        for pattern in cls.FEATURES_MODULEPATTERNS:
            if (pattern.match(moduleName)):
                return True
            # end if
        # end for

        return False
    # end def _acceptableModule

    def _loadFromPackagePath(self, inputPath):
        '''
        Creates SubSystemDefinitions from a python root path.

        @param  inputPath [in] (str) File system path to a python package

        @return (list) list of SubSystemDefinition translation
        '''
        # First, Look in sub-directories
        childSubSystemDefinitions = []
        for subDir in [sd for sd in cached_listdir(inputPath) if ((sd not in self.IGNORED_SUBDIRECTORIES)
                                                       and (isdir(join(inputPath, sd))))]:
            # If the module is a directory, do a recursive load
            childPath = join(inputPath, subDir)
            childSubSystemDefinitions.extend(self._loadFromPackagePath(childPath))
        # end for

        # Look for a features.py file
        currentSubSystemDefinitions = []
        processed = set()
        for subFile in [sf for sf in cached_listdir(inputPath) if ((self._acceptableModule(splitext(basename(sf))[0]))
                                                        and (isfile(join(inputPath, sf))))]:
            moduleName = splitext(basename(sf))[0]
            if (moduleName not in processed):
                processed.add(moduleName)
                featurePyPath = join(inputPath, subFile)

                currentSubSystemDefinitions.extend(self._loadFromFeaturePy(featurePyPath))
            # end if
        # end for

        # Add subSystems to the current subSystem
        if (len(childSubSystemDefinitions) == 0):
            result = currentSubSystemDefinitions
        elif (len(currentSubSystemDefinitions) == 0):
            result = childSubSystemDefinitions
        elif (len(currentSubSystemDefinitions) == 1):
            currentSubSystemDefinitions[0].addChildren(childSubSystemDefinitions)
            result = currentSubSystemDefinitions
        else:
            # This is problematic: We have subsystems that have more than ONE parent.
            raise AssertionError("Only one subsystem is allowed per package.")
        # end if

        return result
    # end def _loadFromPackagePath

    def load(self, rootPath):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionImporter.load
        '''

        return self._loadFromPackagePath(rootPath)
    # end def load
# end class PythonSubSystemDefinitionImporter


class PythonSubSystemDefinitionExporter(AbstractSubSystemDefinitionExporter):
    '''
    Imports a SubSystemDefinition from:
    <ul>
      <li>@c features.py files.</li>
      <li>Python packages and sub-packages containing feature.py files</li>
    </ul>
    '''

    def __init__(self):
        '''
        Constructor
        '''
        super(PythonSubSystemDefinitionExporter, self).__init__()

        self._normedSysPath = None
    # end def __init__

    def _getNormedSysPath(self):
        '''
        Obtians the normalized, cached sys.path

        @return sys.path, normalized
        '''
        if (self._normedSysPath is None):
            self._normedSysPath = [abspath(p) for p in sys.path]
        # end if

        return self._normedSysPath
    # end def _getNormedSysPath

    def _saveToFeaturePy(self, rootPath, subSystemDefinition, baseName = None):
        '''
        Saves an AbstractSubSystemDefinition to a feature.py file.

        @param  rootPath            [in] (str) Root path for saving
        @param  subSystemDefinition [in] (SubSystemDefinition) SubSystem to save
        @option baseName            [in] (str) basename of the serialized file.
        '''
        if (baseName is None):
            baseName = 'features'
        # end if

        # This saves the SubSystemDefinition _inside_ the target feature.py.
        # The constraint is that there is only ONE subSystem in a given feature.py
        # but any number of child subsystems
        if subSystemDefinition.locations is not None:
            featurePyFile = join(rootPath, subSystemDefinition.locations, baseName+'.py')
        else:
            featurePyFile = join(rootPath, baseName + '.py')
        # end if

        featurePyFile = abspath(featurePyFile)
        with open(featurePyFile, 'w+') as outputFile:

            # Write the file header
            today = date.today()
            outputFile.write('\n'.join(('#!/usr/bin/env python',
                                        '# -*- coding: utf-8 -*-',
                                        '# ------------------------------------------------------------------------------',
                                        '# Python Test Harness'
                                        '# ------------------------------------------------------------------------------',
                                        '\'\'\' @package pyharness.subsystem.python.subsystemdefinitionconnector',
                                        '',
                                        '@brief  Importer/exporters for python-defined subsystems',
                                        '',
                                        '@author christophe.roquebert',
                                        '',
                                        '@date   %04d/%02d/%02d' % (today.year, today.month, today.day),
                                        '\'\'\'',
                                        '# ------------------------------------------------------------------------------',
                                        '# imports',
                                        '# ------------------------------------------------------------------------------',
                                        'from pyharness.systems import AbstractSubSystem',
                                        '',
                                        '# ------------------------------------------------------------------------------',
                                        '# implementation',
                                        '# ------------------------------------------------------------------------------',
                                        '',
                                        )))

            def serializeSubsystemDefinitionToLines(_subSystemDefinition):
                '''
                Creates a string for the subSystem definition.

                @param  _subSystemDefinition [in] (SubSystemDefinition) The SubsystemDefinition to serialize

                @return The serialized string.
                '''
                elements = {'subSystemName': _subSystemDefinition.name,
                            }

                if (_subSystemDefinition.doc is None):
                    doc = 'SubSystem definition and default values for %(subSystemName)s.'
                else:
                    doc = _subSystemDefinition.doc.strip()
                # end if

                lines = ['class %(subSystemName)sSubSystem(AbstractSubSystem):',
                         '  \'\'\'',
                         '  %s' % doc,
                         '  \'\'\'',
                         '  def __init__(self):',
                         '    \'\'\'',
                         '    Constructor',
                         '    \'\'\'',
                         '    AbstractSubSystem.__init__(self, \'%(subSystemName)s\')',
                         '    ',
                         '    # Features',
                         ]
                lines = [line % elements for line in lines]

                # Feature definitions
                for featureDefinition in _subSystemDefinition.features:
                    lines.append('    self.F_%s = %s' % (featureDefinition.name,
                                                         StringUtils.stringToRepr(featureDefinition.default,
                                                                                  featureDefinition.type)))      # Default value
                    if (featureDefinition.doc is not None):
                        lines.append('    self.D_%s = """%s"""' % (featureDefinition.name, featureDefinition.doc)) # Documentation
                    # end if
                # end for

                lines.append('    # SubSystems')
                for childSubSystemDefinition in _subSystemDefinition.children:
                    options = {'childSubSystemName': childSubSystemDefinition.name,
                               }
                    lines.append('    self.%(childSubSystemName)s = self.%(childSubSystemName)sSubSystem()' % options)
                # end for

                lines.append('  # end def __init__')

                for childSubSystemDefinition in _subSystemDefinition.children:
                    if (childSubSystemDefinition.locations is None):
                        lines.append('  ')
                        lines.extend(['  %s' % line for line in serializeSubsystemDefinitionToLines(childSubSystemDefinition)])
                    else:
                        self._saveToFeaturePy(rootPath, subSystemDefinition)
                    # end if
                # end for

                lines.append('# end class %(subSystemName)s' % elements)

                return lines
            # end def serializeSubsystemDefinitionToLines

            outputFile.write('\n'.join(serializeSubsystemDefinitionToLines(subSystemDefinition)))

            outputFile.write('\n'.join(('',
                                        '# ------------------------------------------------------------------------------',
                                        '# END OF FILE',
                                        '# ------------------------------------------------------------------------------',
                                        '')))
        # end with
    # end def _saveToFeaturePy

    def save(self, rootPath, subSystemDefinition, baseName = None):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionExporter.save
        '''
        self._saveToFeaturePy(rootPath, subSystemDefinition, baseName)
    # end def save
# end class PythonSubSystemDefinitionExporter

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
