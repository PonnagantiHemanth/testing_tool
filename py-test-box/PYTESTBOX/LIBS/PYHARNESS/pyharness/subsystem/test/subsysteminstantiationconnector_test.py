#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.test.subsysteminstantiationconnectortest

@brief  Abstract tests of SubSystemInstantiationConnector classes

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

from pyharness.subsystem.subsysteminstantiation import SubSystemInstantiation
from pyharness.subsystem.subsysteminstantiationconnector import AbstractSubSystemInstantiationExporter
from pyharness.subsystem.subsysteminstantiationconnector import AbstractSubSystemInstantiationImporter
from pyharness.subsystem.subsysteminstantiationconnector import SubSystemInstantiationExporterComposite
from pyharness.subsystem.subsysteminstantiationconnector import SubSystemInstantiationImporterComposite
from pyharness.subsystem.test.subsystemcomposite_test import SubSystemCompositeTestCase
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractSubSystemInstantiationConnectorTestCase(TestCase):
    '''
    Tests the consistency between:
    - A SubSystemInstantiationExporter
    - A SubSystemInstantiationImporter
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
        self.__srcDir = join(self._tempDirPath, "SETTINGS")
        makedirs(self.__srcDir)

        # Insert the SETTINGS directory to the path
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

    def testConsistency(self):
        '''
        Tests the consistency between two SubSystemInstantiation:
        - The first one is the reference
        - The second one is the first, exported then imported.
        '''
        importer, exporter = self._createConnectors()

        if (    (importer is not None)
            and (exporter is not None)):


            subSystemInstantiations = {'PRODUCT': (SubSystemInstantiation(path     = 'SYSTEM/SUBSYSTEM',
                                                                          features = (SubSystemInstantiation.FeatureInstantiation(name = 'Feature1',
                                                                                                                                  value = 'SampleValue'),
                                                                                      )),
                                                   ),
                                       'PRODUCT/VARIANT': (SubSystemInstantiation(path     = 'SYSTEM/SUBSYSTEM',
                                                                                  features = (SubSystemInstantiation.FeatureInstantiation(name = 'Feature1',
                                                                                                                                  value = 'SampleValue2'),
                                                                                              SubSystemInstantiation.FeatureInstantiation(name = 'Feature2',
                                                                                                                                  value = 'SampleValue1'),
                                                                                              )),
                                                           ),
                                        }

            expected = []
            expected.extend(subSystemInstantiations['PRODUCT'])
            expected.extend(subSystemInstantiations['PRODUCT/VARIANT'])

            # Do the actual operation.
            exporter.save(self.__srcDir, subSystemInstantiations)
            obtained = importer.load(join(self.__srcDir, 'PRODUCT', 'VARIANT'))

            self.assertEqual(expected,
                             obtained,
                             'Inconsistent instantiations, from importer to exporter')
        # end if
    # end def testConsistency
# end class AbstractSubSystemInstantiationConnectorTestCase

class SubSystemInstantiationImporterStubNone(AbstractSubSystemInstantiationImporter):
    '''
    Stup for AbstractSubSystemInstantiationImporter

    The load method returns None
    '''
    def load(self, leafPath, moveUp = True):
        '''
        @copydoc pyharness.subsystem.subsysteminstantiationconnector.AbstractSubSystemInstantiationImporter.load
        '''
        return None
    # end def load
# end class SubSystemInstantiationImporterStubNone

class SubSystemInstantiationImporterStub(AbstractSubSystemInstantiationImporter):
    '''
    Stup for AbstractSubSystemInstantiationImporter

    The load method returns not None
    '''
    STATE = 'Loaded'
    def load(self, leafPath, moveUp = True):
        '''
        @copydoc pyharness.subsystem.subsysteminstantiationconnector.AbstractSubSystemInstantiationImporter.load
        '''
        return self.STATE
    # end def load
# end class SubSystemInstantiationImporterStub

class SubSystemInstantiationImporterCompositeTestCase(SubSystemCompositeTestCase):
    '''
    Tests a SubSystemInstantiationImporterComposite instance
    '''

    Composite       = SubSystemInstantiationImporterComposite
    SubSystemStub   = SubSystemInstantiationImporterStub

    def testLoad(self):
        '''
        Tests the load method
        '''
        child1 = SubSystemInstantiationImporterStubNone()
        child2 = SubSystemInstantiationImporterStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        obtained = composite.load('')

        self.assertEqual(SubSystemInstantiationImporterStub.STATE,
                         obtained,
                         'Child not saved')

    # end def testLoad

# end class SubSystemInstantiationImporterCompositeTestCase

class SubSystemInstantiationExporterStub(AbstractSubSystemInstantiationExporter):
    '''
    Stup for AbstractSubSystemInstantiationExporter
    '''
    NOT_SAVED   = 'Not saved'
    SAVED       = 'Saved'

    def __init__(self):
        '''
        Constructor
        '''
        super(SubSystemInstantiationExporterStub, self).__init__()

        self.state = self.NOT_SAVED

    # end def __init__

    def save(self, rootPath, subSystemInstantiations):
        '''
        @copydoc pyharness.subsystem.subsysteminstantiationconnector.AbstractSubSystemInstantiationExporter.save
        '''
        self.state = self.SAVED
    # end def save

# end class SubSystemInstantiationExporterStub

class SubSystemDefinitionExporterCompositeTestCase(SubSystemCompositeTestCase):
    '''
    Tests a SubSystemDefinitionExporterComposite instance
    '''

    Composite       = SubSystemInstantiationExporterComposite
    SubSystemStub   = SubSystemInstantiationExporterStub

    def testSave(self):
        '''
        Tests the save method
        '''
        child1 = SubSystemInstantiationExporterStub()
        child2 = SubSystemInstantiationExporterStub()
        composite = self._createComposite()

        composite.add(child1)
        composite.add(child2)

        composite.save('', None)

        self.assertEqual(SubSystemInstantiationExporterStub.SAVED,
                         child1.state,
                         'Child not saved')

        self.assertEqual(SubSystemInstantiationExporterStub.SAVED,
                         child2.state,
                         'Child not saved')

    # end def testSave

# end class SubSystemDefinitionExporterCompositeTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
