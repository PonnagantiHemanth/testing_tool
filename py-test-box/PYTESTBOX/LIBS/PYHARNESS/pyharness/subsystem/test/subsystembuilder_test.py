#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.subsystembuilder

@brief  Tests the building of a subsystem.

@author christophe.roquebert

@date   2018/10/26
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from os import makedirs
from os.path import abspath
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.subsystem.ini.subsysteminstantiationconnector import IniSubSystemInstantiationExporter
from pyharness.subsystem.ini.subsysteminstantiationconnector import IniSubSystemInstantiationImporter
from pyharness.subsystem.python.subsystemdefinitionconnector import PythonSubSystemDefinitionExporter
from pyharness.subsystem.python.subsystemdefinitionconnector import PythonSubSystemDefinitionImporter
from pyharness.subsystem.subsystembuilder import SubSystemBuilder
from pyharness.subsystem.subsystemdefinition import SubSystemDefinition
from pyharness.subsystem.subsysteminstantiation import SubSystemInstantiation
from pyharness.systems import AbstractSubSystem
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AbstractSubSystemBuilderTestCase(TestCase):
    '''
    Tests the building of a subsystem.

    This relies on importers/exporters to work correctly for the tests.
    '''

    def setUp( self ):
        '''
        Initialize test.

        This creates a temporary project for testing.
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))
        # If python version is less than 2.6, strip the '\\?\' prefix
        from sys                        import version_info
        if (version_info < (2, 6, 0, 0)) and (self._tempDirPath.startswith('\\\\?\\')):
            self._tempDirPath = self._tempDirPath[4:]
        # end if

        # Insert the TESTSUITES directory to the path
        self.__srcDir = join(self._tempDirPath, "TESTSUITES")
        self.__cfgDir = join(self._tempDirPath, "SETTINGS")
        makedirs(self.__srcDir)


        sys.path.insert(0, self.__srcDir)
    # end def setUp

    def tearDown( self ):
        '''
        Clean up test.
        '''

        sys.path.remove(self.__srcDir)

        # cleanup
        rmtree(self._tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    @staticmethod
    def _createDefinitionConnectors():
        '''
        Creates two connectors:
        - One for export
        - One for import

        @return Importer, Exporter
        '''
        return (None, None)
    # end def _createDefinitionConnectors

    @staticmethod
    def _createInstantiationConnectors():
        '''
        Creates two connectors:
        - One for export
        - One for import

        @return Importer, Exporter
        '''
        return (None, None)
    # end def _createInstantiationConnectors

    def _getBaseName(self):                                                                                             # pylint:disable=R0201,W8003
        '''
        Returns the base name for the file.

        This is optional, and defaults to the default file name if None

        @return The file base name
        '''
        return None
    # end def _getBaseName

    def testCompleteBuilder_Simple(self):
        '''
        Tests a simple case of subsystem building.
        '''

        subSystemDefinitionImporter, subSystemDefinitionExporter = self._createDefinitionConnectors()
        subSystemInstantiationImporter, subSystemInstantiationExporter = self._createInstantiationConnectors()

        # This will only test fully functional SubSystemBuilders
        if (   (subSystemDefinitionImporter is None)
            or (subSystemDefinitionExporter is None)
            or (subSystemInstantiationImporter is None)
            or (subSystemInstantiationExporter is None)):
            return
        # end if

        subSystemDefinition = SubSystemDefinition(name = 'Root',
                                                  children = (SubSystemDefinition(name = 'BASE',
                                                                                  features = (SubSystemDefinition.FeatureDefinition('Feature1',
                                                                                                                                    default = None),
                                                                                              )),
                                                              ))
        subSystemInstantiations = (SubSystemInstantiation(path = 'BASE',
                                                          features = (SubSystemInstantiation.FeatureInstantiation(name = 'Feature1',
                                                                                                                  value = 'Value1'),
                                                                      ),),
                                  )


        subSystemDefinitionExporter.save(self.__srcDir,
                                         subSystemDefinition,
                                         baseName = self._getBaseName())

        subSystemInstantiationExporter.save(self.__cfgDir, {'PRODUCT': subSystemInstantiations})

        subSystemBuilder = SubSystemBuilder(subSystemDefinitionImporter, subSystemInstantiationImporter)
        obtainedSubSystem = subSystemBuilder.load([self.__srcDir],
                                                  [join(self.__cfgDir, 'PRODUCT')])


        class TestRootSubSystem(AbstractSubSystem):
            '''
            Root subsystem test object
            '''
            class TestSubSystem(AbstractSubSystem):
                '''
                child subsystem test object
                '''
                def __init__(self):
                    '''
                    Constructor
                    '''
                    super(TestRootSubSystem.TestSubSystem, self).__init__('BASE') #@UndefinedVariable

                    self.F_Feature1 = 'Value1'
                # end def __init__
            # end class TestSubSystem

            def __init__(self):
                '''
                Constructor
                '''
                super(TestRootSubSystem, self).__init__('Root')

                self.BASE = self.TestSubSystem()                                                                        # pylint:disable=C0103
            # end def __init__
        # end class TestRootSubSystem

        expectedSubSystem = TestRootSubSystem()

        self.assertEqual(expectedSubSystem,
                         obtainedSubSystem,
                         'Built SubSystem does not match expected one')

    # end def testCompleteBuilder_Simple

    def testCompleteBuilder_Simple_NoDefinition(self):
        '''
        Tests a simple case of subsystem building, when an invalid name is selected.
        '''

        subSystemDefinitionImporter, subSystemDefinitionExporter = self._createDefinitionConnectors()
        subSystemInstantiationImporter, subSystemInstantiationExporter = self._createInstantiationConnectors()

        # This will only test fully functional SubSystemBuilders
        if (   (subSystemDefinitionImporter is None)
            or (subSystemDefinitionExporter is None)
            or (subSystemInstantiationImporter is None)
            or (subSystemInstantiationExporter is None)):
            return
        # end if

        subSystemDefinition = SubSystemDefinition(name = 'Root',
                                                  children = (SubSystemDefinition(name = 'BASE',
                                                                                  features = (SubSystemDefinition.FeatureDefinition('Feature1',
                                                                                                                                    default = None),
                                                                                              )),
                                                              ))
        subSystemInstantiations = (SubSystemInstantiation(path = 'BASE',
                                                          features = (SubSystemInstantiation.FeatureInstantiation(name = 'Feature2',
                                                                                                                  value = 'Value2'),
                                                                      ),),
                                  )


        subSystemDefinitionExporter.save(self.__srcDir,
                                         subSystemDefinition,
                                         baseName = self._getBaseName())

        subSystemInstantiationExporter.save(self.__cfgDir, {'PRODUCT': subSystemInstantiations})

        subSystemBuilder = SubSystemBuilder(subSystemDefinitionImporter, subSystemInstantiationImporter)

        self.assertRaises(ValueError,
                          subSystemBuilder.load,
                          [self.__srcDir],
                          [join(self.__cfgDir, 'PRODUCT')])

    # end def testCompleteBuilder_Simple_NoDefinition

    def testCompleteBuilder_Simple_Choices(self):
        '''
        Tests a simple case of subsystem building, when an invalid choice is selected.
        '''

        subSystemDefinitionImporter, subSystemDefinitionExporter = self._createDefinitionConnectors()
        subSystemInstantiationImporter, subSystemInstantiationExporter = self._createInstantiationConnectors()

        # This will only test fully functional SubSystemBuilders
        if (   (subSystemDefinitionImporter is None)
            or (subSystemDefinitionExporter is None)
            or (subSystemInstantiationImporter is None)
            or (subSystemInstantiationExporter is None)):
            return
        # end if

        subSystemDefinition = SubSystemDefinition(name = 'Root',
                                                  children = (SubSystemDefinition(name = 'BASE',
                                                                                  features = (SubSystemDefinition.FeatureDefinition('Feature1',
                                                                                                                                    default = None,
                                                                                                                                    choices = (1,2,3)),
                                                                                              )),
                                                              ))
        subSystemInstantiations = (SubSystemInstantiation(path = 'BASE',
                                                          features = (SubSystemInstantiation.FeatureInstantiation(name = 'Feature1',
                                                                                                                  value = 'Value1'),
                                                                      ),),
                                  )


        subSystemDefinitionExporter.save(self.__srcDir,
                                         subSystemDefinition,
                                         baseName = self._getBaseName())

        subSystemInstantiationExporter.save(self.__cfgDir, {'PRODUCT': subSystemInstantiations})

        subSystemBuilder = SubSystemBuilder(subSystemDefinitionImporter, subSystemInstantiationImporter)

        self.assertRaises(ValueError,
                          subSystemBuilder.load,
                          [self.__srcDir],
                          [join(self.__cfgDir, 'PRODUCT')])

    # end def testCompleteBuilder_Simple_Choices

    def testCompleteBuilder_Simple_Alias(self):
        '''
        Tests a simple case of subsystem building.
        '''

        subSystemDefinitionImporter, subSystemDefinitionExporter = self._createDefinitionConnectors()
        subSystemInstantiationImporter, subSystemInstantiationExporter = self._createInstantiationConnectors()

        # This will only test fully functional SubSystemBuilders
        if (   (subSystemDefinitionImporter is None)
            or (subSystemDefinitionExporter is None)
            or (subSystemInstantiationImporter is None)
            or (subSystemInstantiationExporter is None)):
            return
        # end if

        subSystemDefinition = SubSystemDefinition(name = 'Root',
                                                  children = (SubSystemDefinition(name = 'BASE',
                                                                                  features = (SubSystemDefinition.FeatureDefinition('Feature1',
                                                                                                                                    default = None,
                                                                                                                                    aliases = ('Feature2',)),
                                                                                              )),
                                                              ))
        subSystemInstantiations = (SubSystemInstantiation(path = 'BASE',
                                                          features = (SubSystemInstantiation.FeatureInstantiation(name = 'Feature2',
                                                                                                                  value = 'Value2'),
                                                                      ),),
                                  )


        subSystemDefinitionExporter.save(self.__srcDir,
                                         subSystemDefinition,
                                         baseName = self._getBaseName())

        subSystemInstantiationExporter.save(self.__cfgDir, {'PRODUCT': subSystemInstantiations})

        subSystemBuilder = SubSystemBuilder(subSystemDefinitionImporter, subSystemInstantiationImporter)
        obtainedSubSystem = subSystemBuilder.load([self.__srcDir],
                                                  [join(self.__cfgDir, 'PRODUCT')])


        class TestRootSubSystem(AbstractSubSystem):
            '''
            Root subsystem test object
            '''
            class TestSubSystem(AbstractSubSystem):
                '''
                child subsystem test object
                '''
                def __init__(self):
                    '''
                    Constructor
                    '''
                    super(TestRootSubSystem.TestSubSystem, self).__init__('BASE') #@UndefinedVariable

                    self.F_Feature1 = 'Value2'
                    self.F_Feature2 = 'Value2'
                # end def __init__
            # end class TestSubSystem

            def __init__(self):
                '''
                Constructor
                '''
                super(TestRootSubSystem, self).__init__('Root')

                self.BASE = self.TestSubSystem()                                                                        # pylint:disable=C0103
            # end def __init__
        # end class TestRootSubSystem

        expectedSubSystem = TestRootSubSystem()

        self.assertEqual(expectedSubSystem,
                         obtainedSubSystem,
                         'Built SubSystem does not match expected one')

    # end def testCompleteBuilder_Simple_Alias

# end class AbstractSubSystemBuilderTestCase

class SubSystemBuilderTestCase(AbstractSubSystemBuilderTestCase):
    '''
    Tests the consistency between:
    <ul>
      <li>A SubSystemDefinitionExporter</li>
      <li>A SubSystemDefinitionImporter</li>
      <li>A SubSystemInstantiationExporter</li>
      <li>A SubSystemInstantiationImporter</li>
    </ul>
    '''

    def _getBaseName(self):
        '''
        @copydoc pyharness.subsystem.test.subsystembuilder.AbstractSubSystemBuilderTestCase._getBaseName
        '''
        randomElement = self._tempDirPath[-4:]
        return "features%s_internal" % randomElement
    # end def _getBaseName

    @staticmethod
    def _createDefinitionConnectors():
        '''
        @copydoc pyharness.subsystem.test.subsystembuilder.AbstractSubSystemBuilderTestCase._createDefinitionConnectors
        '''
        return (PythonSubSystemDefinitionImporter(),
                PythonSubSystemDefinitionExporter())
    # end def _createDefinitionConnectors

    @staticmethod
    def _createInstantiationConnectors():
        '''
        @copydoc pyharness.subsystem.test.subsystembuilder.AbstractSubSystemBuilderTestCase._createInstantiationConnectors
        '''
        return (IniSubSystemInstantiationImporter(),
                IniSubSystemInstantiationExporter())
    # end def _createInstantiationConnectors

# end class SubSystemBuilderTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
