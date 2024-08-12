#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.subsystemdefinitionconnectortest

@brief  Abstract tests of SubSystemDefinitionConnector classes

@author christophe.roquebert

@date   2018/10/20
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

from pyharness.subsystem.subsystemdefinition import SubSystemDefinition
from pyharness.subsystem.subsystemdefinitionconnector import AbstractSubSystemDefinitionExporter
from pyharness.subsystem.subsystemdefinitionconnector import AbstractSubSystemDefinitionImporter
from pyharness.subsystem.subsystemdefinitionconnector import SubSystemDefinitionExporterComposite
from pyharness.subsystem.subsystemdefinitionconnector import SubSystemDefinitionImporterComposite
from pyharness.subsystem.test.subsystemcomposite_test import SubSystemCompositeTestCase
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractSubSystemDefinitionConnectorTestCase(TestCase):
    '''
    Tests the consistency between:
    - A SubSystemDefintionExporter
    - A SubSystemDefintionImporter
    .
    '''

    def setUp( self ):
        '''
        Initialize test.

        This creates a temporary project for testing.
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self._tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))
        from sys import version
        if (version < str('2.6.0, 0')) and (self._tempDirPath.startswith('\\\\?\\')):
            self._tempDirPath = self._tempDirPath[4:]
        # end if

        self.__srcDir = join(self._tempDirPath, "TESTSUITES")
        makedirs(self.__srcDir)

        # Insert the TESTSUITES directory to the path
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
    def _createConnectors():
        '''
        Creates two connectors:
        - One for export
        - One for import

        @return Importer, Exporter
        '''
        return (None, None)
    # end def _createConnectors

    def _getBaseName(self):                                                                                             # pylint:disable=R0201,W8003
        '''
        Returns the base name for the file.

        This is optional, and defaults to the default file name if None

        @return The file base name
        '''
        return None
    # end def _getBaseName

    def testConsistency(self):
        '''
        Tests the consistency between two SubSystemDefinition:
        - The first one is the reference
        - The second one is the first, exported then imported.
        '''
        importer, exporter = self._createConnectors()

        if (    (importer is not None)
            and (exporter is not None)):

            subSystemDefinition = SubSystemDefinition(name     = 'Parent',
                                                      parent   = None,
                                                      doc      = 'Parent documentation',
                                                      children = (SubSystemDefinition(name     = 'Child',
                                                                                      doc      = 'Child subsystem documentation',),
                                                                                      ),
                                                      features = (SubSystemDefinition.FeatureDefinition(name = 'StringFeature',
                                                                                                        doc  = 'String feature documentation',
                                                                                                        type = 'string',
                                                                                                        default  = 'string default',
                                                                                                        choices  = ('string default', '2', '3'),),
                                                                  SubSystemDefinition.FeatureDefinition(name = 'IntFeature',
                                                                                                        doc  = 'Integer feature documentation',
                                                                                                        type = 'int',
                                                                                                        default  = '0',
                                                                                                        choices  = ('0', '2', '3'),),
                                                                  SubSystemDefinition.FeatureDefinition(name = 'BoolFeature',
                                                                                                        doc  = 'Boolean feature documentation',
                                                                                                        type = 'boolean',
                                                                                                        default  = 'true',
                                                                                                        choices  = ('true', 'false'),),
                                                                  SubSystemDefinition.FeatureDefinition(name = 'HexListFeature',
                                                                                                        doc  = 'HexList feature documentation',
                                                                                                        type = 'hexlist',
                                                                                                        default  = '00',
                                                                                                        choices  = ('00', '11', '00FF', '0FFF', 'FFFF'),),
                                                                                                        )
                                                      )
            expected = subSystemDefinition

            # Do the actual operation.
            exporter.save(self.__srcDir, subSystemDefinition, baseName = self._getBaseName())
            obtained = importer.load(self.__srcDir)[0]

            self.assertEqual(expected,
                             obtained,
                             'Inconsistent definitions, from importer to exporter')
        # end if
    # end def testConsistency
# end class AbstractSubSystemDefinitionConnectorTestCase

class SubSystemDefinitionExporterStub(AbstractSubSystemDefinitionExporter):
    '''
    Stup for AbstractSubSystemDefinitionExporter
    '''
    NOT_SAVED   = 'Not saved'
    SAVED       = 'Saved'

    def __init__(self):
        '''
        Constructor
        '''
        super(SubSystemDefinitionExporterStub, self).__init__()

        self.state = self.NOT_SAVED

    # end def __init__

    def save(self, rootPath, subSystemDefinition, baseName = None):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionExporter.save
        '''
        self.state = self.SAVED
    # end def save

# end class SubSystemDefinitionExporterStub

class SubSystemDefinitionExporterCompositeTestCase(SubSystemCompositeTestCase):
    '''
    Tests a SubSystemDefinitionExporterComposite instance
    '''

    Composite       = SubSystemDefinitionExporterComposite
    SubSystemStub   = SubSystemDefinitionExporterStub

    def testSave(self):
        '''
        Tests the save method
        '''
        child1 = SubSystemDefinitionExporterStub()
        child2 = SubSystemDefinitionExporterStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        composite.save('', None)

        self.assertEqual(SubSystemDefinitionExporterStub.SAVED,
                         child1.state,
                         'Child not saved')

        self.assertEqual(SubSystemDefinitionExporterStub.SAVED,
                         child2.state,
                         'Child not saved')

    # end def testSave

# end class SubSystemDefinitionExporterCompositeTestCase

class SubSystemDefinitionImporterStubNone(AbstractSubSystemDefinitionImporter):
    '''
    Stup for AbstractSubSystemDefinitionImporter

    The load method returns None
    '''
    def load(self, rootPath):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionImporter.load
        '''
        return None
    # end def load
# end class SubSystemDefinitionImporterStubNone

class SubSystemDefinitionImporterStub(AbstractSubSystemDefinitionImporter):
    '''
    Stup for AbstractSubSystemDefinitionImporter

    The load method returns not None
    '''
    STATE = 'Loaded'
    def load(self, rootPath):
        '''
        @copydoc pyharness.subsystem.subsystemdefinitionconnector.AbstractSubSystemDefinitionImporter.load
        '''
        return self.STATE
    # end def load
# end class SubSystemDefinitionImporterStub

class SubSystemDefinitionImporterCompositeTestCase(SubSystemCompositeTestCase):
    '''
    Tests a SubSystemDefinitionImporterComposite instance
    '''

    Composite       = SubSystemDefinitionImporterComposite
    SubSystemStub   = SubSystemDefinitionImporterStub

    def testLoad(self):
        '''
        Tests the load method
        '''
        child1 = SubSystemDefinitionImporterStubNone()
        child2 = SubSystemDefinitionImporterStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        obtained = composite.load('')

        self.assertEqual(SubSystemDefinitionImporterStub.STATE,
                         obtained,
                         'Child not saved')

    # end def testLoad

# end class SubSystemDefinitionImporterCompositeTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
