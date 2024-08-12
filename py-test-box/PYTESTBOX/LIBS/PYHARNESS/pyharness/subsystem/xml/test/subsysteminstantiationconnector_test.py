#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.subsystem.xml.test.subsysteminstantiationconnector

@brief  Tests of Importer/exporters for xml-instantiated subsystems

@author christophe Roquebert

@date   2018/06/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import sys
from os import makedirs
from os import mkdir
from os import rename
from os.path import abspath
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pyharness.subsystem.subsysteminstantiation import SubSystemInstantiation
from pyharness.subsystem.xml.subsysteminstantiationconnector import XmlSubSystemInstantiationImporter
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class SubSystemInstantiationImporterTestCase(TestCase):
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

        self.rootVersionFile = join(self._rootVersionDir, self.ROOT_VERSION_NAME + ".main.xml")
        with open(self.rootVersionFile, "w+") as rootConfigFile:

            rootConfigFile.write('\n'.join((
                                            '<?xml version="1.0" encoding="UTF-8"?>',
                                            '<subsystem version="1.0" type="feature">',
                                            '  <section version="1.0" type="feature">',
                                            '    <name>' + self.SECTION_IN_CONFIG_AND_DEFAULT + '</name>',
                                            '    <features>',
                                            '      <feature>',
                                            '        <name>' + self.FEATURE_ISACTIVATED + '</name>',
                                            '        <type>boolean</type>',
                                            '        <value>True</value>',
                                            '      </feature>',
                                            '      <feature>',
                                            '        <name>' + self.FEATURE_IN_CONFIG_AND_DEFAULT + '</name>',
                                            '        <type>string</type>',
                                            '        <value>' + self.ROOT_VALUE + '</value>'
                                            '      </feature>',
                                            '      <feature>',
                                            '        <name>' + self.FEATURE_OVERRIDDEN + '</name>',
                                            '        <type>string</type>',
                                            '        <value>' + self.ROOT_VALUE + '</value>'
                                            '      </feature>',
                                            '    </features>',
                                            '  </section>',
                                            '  <section version="1.0" type="feature">',
                                            '    <name>' + self.SECTION_IN_CONFIG_AND_DEFAULT + "/" + self.INNER_SYSTEM + '</name>',
                                            '    <features>',
                                            '      <feature>',
                                            '        <name>' + self.INNER_FEATURE + '</name>',
                                            '        <type>boolean</type>',
                                            '        <value>True</value>',
                                            '      </feature>',
                                            '    </features>',
                                            '  </section>',
                                            '</subsystem>'
                                            )))
        # end with

        # Child version dir
        self._childVersionDir = join(self._rootVersionDir,  self.CHILD_VERSION_NAME)
        mkdir(self._childVersionDir)

        self._childVersionFile = join(self._childVersionDir, self.CHILD_VERSION_NAME + ".xml")
        with open(self._childVersionFile, "w+") as childConfigFile:
            childConfigFile.write('\n'.join((
                                             '<?xml version="1.0" encoding="UTF-8"?>',
                                             '<subsystem version="1.0" type="feature">',
                                             '  <section version="1.0" type="feature">',
                                             '    <name>' + self.SECTION_IN_CONFIG_AND_DEFAULT + '</name>',
                                             '    <features>',
                                             '      <feature>',
                                             '        <name>' + self.FEATURE_OVERRIDDEN + '</name>',
                                             '        <type>string</type>',
                                             '        <value>' + self.CHILD_VALUE + '</value>',
                                             '      </feature>',
                                            '    </features>',
                                            '  </section>',
                                            '  <section version="1.0" type="feature">',
                                            '    <name>' + self.SECTION_IN_CONFIG_AND_DEFAULT + "/" + self.INNER_SYSTEM + '</name>',
                                            '    <features>',
                                            '      <feature>',
                                            '        <name>' + self.FEATURE_ISACTIVATED + '</name>',
                                            '        <type>boolean</type>',
                                            '        <value>False</value>',
                                            '      </feature>',
                                            '      <feature>',
                                            '        <name>' + self.INNER_FEATURE + '</name>',
                                            '        <type>boolean</type>',
                                            '        <value>True</value>',
                                            '      </feature>',
                                            '    </features>',
                                            '  </section>',
                                            '</subsystem>'
                                             )))
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
        importer = XmlSubSystemInstantiationImporter()
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
        importer = XmlSubSystemInstantiationImporter()
        obtained = importer.load(self._childVersionDir, moveUp = False)

        self.assertEqual(self.variantSubSystemInstantiations,
                         obtained,
                         'Invalid instantiation loading on VARIANT')
    # end def testLoadVariant

    def testLoadVariant_None(self):
        '''
        Tests loading the variant feature instantiations.
        '''
        rename(self.rootVersionFile, self.rootVersionFile[:-3] + 'ini')
        importer = XmlSubSystemInstantiationImporter()
        obtained = importer.load(self._childVersionDir)

        self.assertIsNone(obtained,
                          'Invalid instantiation loading on VARIANT')
    # end def testLoadVariant_None

    def testLoadFull(self):
        '''
        Tests loading the variant feature instantiations.
        '''
        importer = XmlSubSystemInstantiationImporter()
        obtained = importer.load(self._childVersionDir)

        expected = []
        expected.extend(self.productSubSystemInstantiations)
        expected.extend(self.variantSubSystemInstantiations)

        self.assertEqual(expected,
                         obtained,
                         'Invalid instantiation loading on PRODUCT + VARIANT')
    # end def testLoadFull

    def testLoadFull_None(self):
        '''
        Tests loading the variant feature instantiations.
        '''
        rename(self.rootVersionFile, self.rootVersionFile[:-3] + 'ini')
        rename(self._childVersionFile, self._childVersionFile[:-3] + 'ini')
        importer = XmlSubSystemInstantiationImporter()
        obtained = importer.load(self._childVersionDir)

        self.assertIsNone(obtained,
                          'Invalid instantiation loading on PRODUCT + VARIANT')
    # end def testLoadFull_None

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

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
