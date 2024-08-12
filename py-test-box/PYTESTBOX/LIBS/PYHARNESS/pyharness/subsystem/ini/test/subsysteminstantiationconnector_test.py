#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.ini.test.subsysteminstantiationconnectortest

@brief  Tests of Importer/exporters for ini-instantiated subsystems

@author christophe.roquebert

@date   2018/10/20
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from os import makedirs
from os import mkdir
from os.path import abspath
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.subsystem.ini.subsysteminstantiationconnector import IniSubSystemInstantiationExporter
from pyharness.subsystem.ini.subsysteminstantiationconnector import IniSubSystemInstantiationImporter
from pyharness.subsystem.subsysteminstantiation import SubSystemInstantiation
from pyharness.subsystem.test.subsysteminstantiationconnector_test import \
    AbstractSubSystemInstantiationConnectorTestCase
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class SubSystemInstantiationImporterTestCase( TestCase ):
    '''
    Test the SubSystemInstantiationImporter class
    '''

    ROOT_VERSION_NAME               = "ROOTVERSION_1_0"
    SECTION_IN_CONFIG_AND_DEFAULT   = "SECTION_IN_CONFIG_AND_DEFAULT"
    SECTION_IN_DEFAULT              = "SECTION_IN_DEFAULT"

    FEATURE_ISACTIVATED             = "Enabled"
    FEATURE_IN_CONFIG_AND_DEFAULT   = "featureInConfigAndDefault"
    FEATURE_IN_DEFAULT              = "featureInDefault"
    FEATURE_OVERRIDDEN              = "featureOverridden"

    ROOT_VALUE                      = "rootValue"
    CHILD_VALUE                     = "childValue"
    DEFAULT_VALUE                   = "defaultValue"

    CHILD_VERSION_NAME              = "CHILDVERSION_1_0"

    INNER_SYSTEM                    = "INNER"
    INNER_FEATURE                   = "innerFeature"


    def setUp( self ):
        '''
        Initialize test.

        This creates a temporary project for testing.
        '''
        TestCase.setUp(self)

        # Create a convenient hierarchy
        self.__tempDirPath = abspath(mkdtemp("", "test_%s" % self.id()))
        self.__srcDir = join(self.__tempDirPath, "TESTSUITES")
        makedirs(self.__srcDir)

        # Insert the TESTSUITES directory to the path
        sys.path.insert(0, self.__srcDir)


        # ini files directory
        self.__inputDir = join(self.__tempDirPath, "SETTINGS")
        makedirs(self.__inputDir)

        # Root version dir
        self._rootVersionDir = join(self.__inputDir, self.ROOT_VERSION_NAME)
        makedirs(self._rootVersionDir)

        # Create the main.settings.ini file
        rootVersionFile = join(self._rootVersionDir, "main.settings.ini")
        with open(rootVersionFile, "w+") as rootConfigFile:
            rootConfigFile.writelines([
                                       "[" + self.SECTION_IN_CONFIG_AND_DEFAULT + "]" + "\n",
                                       self.FEATURE_ISACTIVATED + "=" + "True" + "\n",
                                       self.FEATURE_IN_CONFIG_AND_DEFAULT + "=\"" + self.ROOT_VALUE + "\"\n",
                                       self.FEATURE_OVERRIDDEN + "=\"" + self.ROOT_VALUE + "\"\n",

                                       "[" + self.SECTION_IN_CONFIG_AND_DEFAULT + "/" + self.INNER_SYSTEM + "]" + "\n",
                                       self.INNER_FEATURE + "=" + "True" + "\n",
                                       ])
        # end with

        # Child version dir
        self._childVersionDir = join(self._rootVersionDir,  self.CHILD_VERSION_NAME)
        mkdir(self._childVersionDir)

        # Create the sub variant xxx.settings.ini file
        self._childVersionFile = join(self._childVersionDir, self.CHILD_VERSION_NAME + ".settings.ini")
        with open(self._childVersionFile, "w+") as childConfigFile:
            childConfigFile.writelines([
                                        "[" + self.SECTION_IN_CONFIG_AND_DEFAULT + "]" + "\n",
                                        self.FEATURE_OVERRIDDEN + "=\"" + self.CHILD_VALUE + "\"\n",

                                        "[" + self.SECTION_IN_CONFIG_AND_DEFAULT + "/" + self.INNER_SYSTEM + "]\n",
                                        "Enabled      = False\n",
                                        self.INNER_FEATURE + " = " + "True\n",
                                       ])
        # end with

        # Default subsystem
        productSubSystemInstantiations = sorted((SubSystemInstantiation(self.SECTION_IN_CONFIG_AND_DEFAULT,
                                                                        features = sorted((SubSystemInstantiation.FeatureInstantiation(self.FEATURE_ISACTIVATED, value = "true"),
                                                                                           SubSystemInstantiation.FeatureInstantiation(self.FEATURE_IN_CONFIG_AND_DEFAULT, value = self.ROOT_VALUE),
                                                                                           SubSystemInstantiation.FeatureInstantiation(self.FEATURE_OVERRIDDEN, value = self.ROOT_VALUE),
                                                                                           ),
                                                                                           key = lambda x: x.name)),
                                                 SubSystemInstantiation(self.SECTION_IN_CONFIG_AND_DEFAULT + "/" + self.INNER_SYSTEM,
                                                                        features = (SubSystemInstantiation.FeatureInstantiation(self.INNER_FEATURE, value = "true"),
                                                                                    )),
                                                ),
                                                key = lambda x: x.path)
        self.productSubSystemInstantiations = productSubSystemInstantiations

        variantSubSystemInstantiations = sorted((SubSystemInstantiation(self.SECTION_IN_CONFIG_AND_DEFAULT,
                                                                        features = (SubSystemInstantiation.FeatureInstantiation(self.FEATURE_OVERRIDDEN, value = self.CHILD_VALUE),
                                                                                    )),
                                                 SubSystemInstantiation(self.SECTION_IN_CONFIG_AND_DEFAULT + "/" + self.INNER_SYSTEM,
                                                                        features = sorted((SubSystemInstantiation.FeatureInstantiation("Enabled", value = "false"),
                                                                                           SubSystemInstantiation.FeatureInstantiation(self.INNER_FEATURE, value = "true"),
                                                                                           ),
                                                                                           key = lambda x: x.name)),
                                                ),
                                                key = lambda x: x.path)
        self.variantSubSystemInstantiations = variantSubSystemInstantiations

    # end def setUp

    def testLoadProduct(self):
        '''
        Tests loading the product feature instantiations.
        '''
        importer = IniSubSystemInstantiationImporter()
        expected = self.productSubSystemInstantiations
        obtained = importer.load(self._rootVersionDir)

        self.assertEqual(expected,
                         obtained,
                         'Invalid instantiation loading on PRODUCT')
    # end def testLoadProduct

    def testLoadVariant(self):
        '''
        Tests loading the variant feature instantiations.
        '''
        importer = IniSubSystemInstantiationImporter()
        obtained = importer.load(self._childVersionDir, moveUp = False)

        self.assertEqual(self.variantSubSystemInstantiations,
                         obtained,
                         'Invalid instantiation loading on VARIANT')
    # end def testLoadVariant

    def testLoadFull(self):
        '''
        Tests loading the variant feature instantiations.
        '''
        importer = IniSubSystemInstantiationImporter()
        obtained = importer.load(self._childVersionDir)

        expected = []
        expected.extend(self.productSubSystemInstantiations)
        expected.extend(self.variantSubSystemInstantiations)

        self.assertEqual(expected,
                         obtained,
                         'Invalid instantiation loading on PRODUCT + VARIANT')
    # end def testLoadFull

    def tearDown( self ):
        '''
        Clean up test.
        '''

        sys.path.remove(self.__srcDir)
        # cleanup
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown
# end class SubSystemInstantiationImporterTestCase

class SubSystemInstantiationConnectorTestCase(AbstractSubSystemInstantiationConnectorTestCase):
    '''
    Tests the consistency between:
    - A SubSystemInstantiationExporter
    - A SubSystemInstantiationImporter
    .
    '''

    @staticmethod
    def _createConnectors():
        '''
        @copydoc pyharness.subsystem.test.subsysteminstantiationconnectortest.AbstractSubSystemInstantiationConnectorTestCase._createConnectors
        '''

        return (IniSubSystemInstantiationImporter(),
                IniSubSystemInstantiationExporter())
    # end def _createConnectors


# end class SubSystemInstantiationConnectorTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
