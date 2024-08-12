#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.configtest

@brief  Configuration loading test case

@author christophe.roquebert

@date   2018/09/11
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path import join
from shutil import rmtree
from unittest import TestCase

from pylibrary.tools.config import CachingConfigParser
from pylibrary.tools.config import ConfigParser
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.tempfile import mkdtemp


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConfigTestCase(TestCase):
    '''
    Tests the behavior of the ConfigParser class
    '''

    FILE_CONTENTS = '''[SECTION]\n''' + '''OpTiOn = VALUE'''

    def setUp( self ):
        '''
        Initialize test.
        '''
        TestCase.setUp(self)

        self.__tempDirPath = mkdtemp()

        self.__tempFilePath = join(self.__tempDirPath, "temp.ini")
        with open(self.__tempFilePath, "w+") as tempFile:
            tempFile.write(self.FILE_CONTENTS)
        # end with
    # end def setUp

    def tearDown( self ):
        '''
        Clean up test.
        '''

        # cleanup
        rmtree(self.__tempDirPath, True)

        TestCase.tearDown(self)
    # end def tearDown

    @staticmethod
    def _createConfigParser(*args, **kwArgs):
        '''
        Creates the config parser under test

        @param args   [in] (tuple) Arguments
        @param kwArgs [in] (dict) Keyword arguments
        @return An instance of a ConfigParser
        '''
        return ConfigParser(*args, **kwArgs)
    # end def _createConfigParser

    def test_Get(self):
        '''Test the get method'''
        config = self._createConfigParser()
        config.read([self.__tempFilePath])

        self.assertEqual("VALUE", config.get("SECTION", "OpTiOn", "NOVALUE"))
        self.assertEqual("NOVALUE", config.get("SECTION", "OPTION", "NOVALUE"))
    # end def test_Get


    def test_Get2(self):
        '''Test the get method'''
        config = self._createConfigParser()
        config.read([self.__tempFilePath])

        self.assertEqual("VALUE", config.get("SECTION", "OpTiOn", "NOVALUE"))
        self.assertEqual("NOVALUE", config.get("SECTION", "OPTION", "NOVALUE"))
    # end def test_Get2


    def test_Set(self):
        '''Test the set method'''
        config = self._createConfigParser()
        config.read([self.__tempFilePath])

        config.set("INVALID_SECTION", "INVALID_OPTION", "VALID_VALUE")
        self.assertEqual("VALID_VALUE", config.get("INVALID_SECTION", "INVALID_OPTION", "NOVALUE"))
    # end def test_Set

    def test_Set2(self):
        '''Test the set method'''
        config = self._createConfigParser()
        config.read([self.__tempFilePath])

        config.set("INVALID_SECTION", "INVALID_OPTION", "VALID_VALUE")
        self.assertEqual("VALID_VALUE", config.get("INVALID_SECTION", "INVALID_OPTION", "NOVALUE"))
    # end def test_Set2

    def test_ReadWrite(self):
        '''
        Test the parsing of various config files.
        '''

        fileVectors = (
                       # Normal ini file sections
                        ("Empty file", ""),
                        ("Empty section", "[SECTION]"),
                        ("Normal section", "[SECTION]\noption = value"),

                       # Comments
                        ("Comment", "# This is a comment"),
                        ("Header comment", "# This is a header comment\n[SECTION]"),
                        ("Section comment", "[SECTION]\n# This is a section comment"),

                       # Blank lines
                        ("Blank lines", "\n"),
                        ("Blank line in comment", "# Comment 1\n\n# Comment 2\n\n"),

                       # Continuation lines
                        ("Comment continuation", "# This is a comment\n continuated on a new line (comment)"),
                        ("Property continuation", "[SECTION]\noption = value\n continuated on a new line (option)"),

                       # Complicated sections
                        ("Complicated sections", '''# This is a complicated ini file\n''' +
                                                '''[SECTION1]\n''' +
                                                '''option1 = value1\n''' +
                                                '''option2 = value2\n''' +
                                                '''\n''' +
                                                '''[SECTION2]\n''' +
                                                '''option3 = value3\n'''),
                        )

        index = 0
        for description, inputContents in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)
            outputFilePath = join(self.__tempDirPath, "config_%d_out.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(inputContents)
            # end with

            config = self._createConfigParser()
            config.read([inputFilePath])

            config.write(outputFilePath)

            with open(outputFilePath, "r+") as configFile:
                outputContents = configFile.read()
            # end with

            self.assertEqual(inputContents.strip(),
                             outputContents.strip(),
                             "Inconsistent contents for %s:\nInput:\n%s\nOutput:\n%s" \
                                 % (description, inputContents, outputContents))

            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all elements were tested")
    # end def test_ReadWrite

    def test_Parsing(self):
        '''Test parsing files'''
        fileVectors = (
                       # Type parsing
                       ('Read string option', '[SECTION]\noption = value',
                        ( ("SECTION", "option", "value"),), ),
                       ('Read string option', '[SECTION]\noption = value \b',
                        ( ("SECTION", "option", "value"),), ),
                       ('Read string option', '[SECTION]\noption = "123"',
                        ( ("SECTION", "option", "123"),), ),
                       ('Read string option', '[SECTION]\noption = \'123\'',
                        ( ("SECTION", "option", "123"),), ),
                       ('Read int option', '[SECTION]\noption = 123',
                        ( ("SECTION", "option", 123),), ),
                       ('Read Hexadecimal option', '[SECTION]\noption = 0x0123',
                        ( ("SECTION", "option", 0x0123),), ),
                       ('Read HexList option', '[SECTION]\noption = [01 23]',
                        ( ("SECTION", "option", HexList(0x01, 0x23)),), ),
                       ('Read True option', '[SECTION]\noption = True',
                        ( ("SECTION", "option", True),), ),
                       ('Read False option', '[SECTION]\noption = False',
                        ( ("SECTION", "option", False),), ),
                       ('Read List option', '[SECTION]\noption = ([01],[23])',
                        ( ("SECTION", "option", (HexList(0x01), HexList(0x23)),),), ),
                      )

        index = 0
        for description, inputContents, triplets in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(inputContents)
            # end with

            config = self._createConfigParser()
            config.read([inputFilePath])

            for section, option, value in triplets:
                self.assertEqual(value,
                                  config.get(section, option, None),
                                  "Invalid value for (%s, %s) in %s" %
                                      (section, option, description))
            # end for

            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all elements were tested")
    # end def test_Parsing

    def test_ParsingError(self):
        '''Test parsing files with errors'''
        fileVectors = (
                        ('Multiple options', '[SECTION]\noption = "123"\noption="456"',),
                        ('Multiple sections', '[SECTION]\noption = "123"\n[SECTION]\noption2="456"',),
                        ('Invalid line', '[SECTION]\noption = "123"\nThis is an invalid line',),
                        )

        index = 0
        for description, inputContents in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(inputContents)
            # end with

            config = self._createConfigParser()

            try:
                config.read([inputFilePath])
                self.fail("ConfigParser should not have been able to parse %s:\n%s" %\
                          (description, inputContents))
            except ValueError:
                pass
            # end try
            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all elements were tested")
    # end def test_ParsingError


    def test_ReadMultipleFiles(self):
        '''
        Reads several files, the contents of the later ones overriding the first.

        Comments are ignored in later files.
        '''

        fileVectors = ( '[SECTION]\noption = "123"',
                        '[SECTION]\noption = "456"',
                        '[SECTION]\noption2 = "456"',
                        '[SECTION1]\noption1 = "789"',
                        )

        inputFiles = []
        index = 0
        for fileVector in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(fileVector)
            # end with

            inputFiles.append(inputFilePath)

            index += 1
        # end for


        config = self._createConfigParser()
        config.read(inputFiles)

        self.assertEqual(["SECTION", "SECTION1"],
                         config.sections(),
                         "Sections not overridden")

        self.assertEqual("456",
                         config.get("SECTION", "option"),
                         "Options not overridden")
    # end def test_ReadMultipleFiles

    def test_HasSection(self):
        '''
        Test section lookup
        '''
        fileVectors = ( ('[SECTION]\noption = "123"', "SECTION", True),
                        ('[SECTION]\noption = "456"', "SECTION2", False),
                        )

        index = 0
        for fileVector, section, found in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(fileVector)
            # end with

            config = self._createConfigParser()
            config.read(inputFilePath)

            self.assertEqual(found,
                             config.has_section(section),
                             "Invalid section: %s in \n%s" % (section, fileVector))

            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all configurations were tested")
    # end def test_HasSection

    def test_AddSection(self):
        '''
        Test section add
        '''

        fileVectors = ( '[SECTION]\noption = "123"',
                        '[SECTION]\noption = "456"',
                        '[SECT\\ION]\noption = "456"',
                        )

        index = 0
        for fileVector in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(fileVector)
            # end with

            config = self._createConfigParser()
            config.read(inputFilePath)

            section = "SECTION"
            config.add_section(section)
            config.checkConsistency()

            self.assertEqual(True,
                             config.has_section(section),
                             "Invalid section: %s in \n%s" % (section, fileVector))

            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all configurations were tested")
    # end def test_AddSection

    def test_RemoveSection(self):
        '''
        Tests section removal
        '''
        fileVectors = ( '[SECTION]\noption = "123"',
                        '[SECTION]\n',
                        )

        index = 0
        for fileVector in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(fileVector)
            # end with

            config = self._createConfigParser()
            config.read(inputFilePath)

            section = "SECTION"
            config.remove_section(section)
            config.checkConsistency()


            self.assertEqual(False,
                             config.has_section(section),
                             "Invalid section: %s in \n%s" % (section, fileVector))

            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all configurations were tested")
    # end def test_RemoveSection

    def test_SectionWithSlash(self):
        '''
        Tests the usage of a section name with a slash
        '''
        fileVectors = ( '[SEC/TION]\noption = "123"',
                        '[SEC/TION]\n',
                        )

        index = 0
        for fileVector in fileVectors:
            inputFilePath  = join(self.__tempDirPath, "config_%d_in.ini" % index)

            with open(inputFilePath, "w+") as configFile:
                configFile.write(fileVector)
            # end with

            config = self._createConfigParser()
            config.read(inputFilePath)

            section = "SEC/TION"
            self.assertEqual(True,
                             config.has_section(section),
                             "No section with slash found")

            config.add_section("NEW/SECTION")
            config.checkConsistency()

            outputFilePath  = join(self.__tempDirPath, "config_%d_out.ini" % index)
            config.write(outputFilePath)

            index += 1
        # end for

        self.assertEqual(len(fileVectors),
                         index,
                         "Not all configurations were tested")
    # end def test_SectionWithSlash

    def test_AddOption(self):                                                                                           # pylint:disable=R0201
        '''
        Tests the set method
        '''

        # List of 'things' to add: section, option, value
        operations = (("SECTION1", "OPTION1", "value1"),
                      ("SECTION1", "OPTION2", "value2"),
                      ("SECTION2", "OPTION1", "value1"),
                      ("SECTION2", "OPTION2", "value2"),
                      ("SECTION3",      None,     None),
                      ("SECTION3", "OPTION1", "value1"),
                      ("SECTION3", "OPTION2", "value2"),
                      ("SECTION4",      None,     None),
                      ("SECTION5",      None,     None),
                      ("SECTION4", "OPTION1", "value1"),
                      ("SECTION4", "OPTION2", "value2"),

                      )
        config = self._createConfigParser()
        for section, option, value in operations:
            if (option is None):
                config.add_section(section)
            else:
                config.set(section, option, value)
            # end if

            config.checkConsistency()
        # end for
    # end def test_AddOption

    def test_AddComment(self):
        '''
        Tests the addition of a comment at various places
        '''

        fileContents = ( '[SECTION1]\n',
                         'option1 = "123"\n',
                         'option2 = "456"\n',
                         '[SECTION2]\n',
                         'option1 = "123"\n',
                         'option2 = "456"\n',
                        )

        inputFilePath  = join(self.__tempDirPath, "config_in.ini")

        with open(inputFilePath, "w+") as configFile:
            configFile.writelines(fileContents)
        # end with

        config = self._createConfigParser()
        config.read(inputFilePath)

        # List of 'things' to add: message, section, option, mode, exceptionExpected
        operations = ( \
            ("File before",    None,       None, ConfigParser.MODE_BEFORE, False),
            ("File inside",    None,       None, ConfigParser.MODE_INSIDE, True),
            ("File after",     None,       None, ConfigParser.MODE_AFTER,  False),
            ("Section1 before", "SECTION1", None, ConfigParser.MODE_BEFORE, False),
            ("Section1 inside", "SECTION1", None, ConfigParser.MODE_INSIDE, False),
            ("Section1 after",  "SECTION1", None, ConfigParser.MODE_AFTER,  False),
            ("Section2 before", "SECTION2", None, ConfigParser.MODE_BEFORE, False),
            ("Section2 inside", "SECTION2", None, ConfigParser.MODE_INSIDE, False),
            ("Section2 after",  "SECTION2", None, ConfigParser.MODE_AFTER,  False),
            ("Section3 before", "SECTION3", None, ConfigParser.MODE_BEFORE, True),
            ("Section3 inside", "SECTION3", None, ConfigParser.MODE_INSIDE, True),
            ("Section3 after",  "SECTION3", None, ConfigParser.MODE_AFTER,  True),
            ("Option1.1 before",  "SECTION1", "option1", ConfigParser.MODE_BEFORE, False),
            ("Option1.1 inside",  "SECTION1", "option1", ConfigParser.MODE_INSIDE, True),
            ("Option1.1 after",   "SECTION1", "option1", ConfigParser.MODE_AFTER,  False),
            ("Option2.1 before",  "SECTION2", "option1", ConfigParser.MODE_BEFORE, False),
            ("Option2.1 inside",  "SECTION2", "option1", ConfigParser.MODE_INSIDE, True),
            ("Option2.1 after",   "SECTION2", "option1", ConfigParser.MODE_AFTER,  False),
            ("Option2.3 before",  "SECTION2", "option3", ConfigParser.MODE_BEFORE, True),
            ("Option2.3 inside",  "SECTION2", "option3", ConfigParser.MODE_INSIDE, True),
            ("Option2.3 after",   "SECTION2", "option3", ConfigParser.MODE_AFTER,  True),
            )

        for comment, section, option, mode, exceptionExpected in operations:

            try:
                config.add_comment(comment, section, option, mode)
                self.assertEqual(False,
                                 exceptionExpected,
                                 "No exception generated for \"%s\", %s, %s, %s" %\
                                 (comment, section, option, mode))
            except ValueError:
                self.assertEqual(True,
                                 exceptionExpected,
                                 "Exception generated for \"%s\", %s, %s, %s" %\
                                 (comment, section, option, mode))
            # end try

            config.checkConsistency()
        # end for
    # end def test_AddComment

    def test_AddBlank(self):
        '''
        Tests the addition of a blank lines at various places
        '''

        fileContents = ( '[SECTION1]\n',
                         'option1 = "123"\n',
                         'option2 = "456"\n',
                         '[SECTION2]\n',
                         'option1 = "123"\n',
                         'option2 = "456"\n',
                        )

        inputFilePath  = join(self.__tempDirPath, "config_in.ini")

        with open(inputFilePath, "w+") as configFile:
            configFile.writelines(fileContents)
        # end with

        config = self._createConfigParser()
        config.read(inputFilePath)

        # List of 'things' to add: message, section, option, mode, exceptionExpected
        operations = ( \
            ("File before",    None,       None, ConfigParser.MODE_BEFORE, False),
            ("File inside",    None,       None, ConfigParser.MODE_INSIDE, True),
            ("File after",     None,       None, ConfigParser.MODE_AFTER,  False),
            ("Section1 before", "SECTION1", None, ConfigParser.MODE_BEFORE, False),
            ("Section1 inside", "SECTION1", None, ConfigParser.MODE_INSIDE, False),
            ("Section1 after",  "SECTION1", None, ConfigParser.MODE_AFTER,  False),
            ("Section2 before", "SECTION2", None, ConfigParser.MODE_BEFORE, False),
            ("Section2 inside", "SECTION2", None, ConfigParser.MODE_INSIDE, False),
            ("Section2 after",  "SECTION2", None, ConfigParser.MODE_AFTER,  False),
            ("Section3 before", "SECTION3", None, ConfigParser.MODE_BEFORE, True),
            ("Section3 inside", "SECTION3", None, ConfigParser.MODE_INSIDE, True),
            ("Section3 after",  "SECTION3", None, ConfigParser.MODE_AFTER,  True),
            ("Option1.1 before",  "SECTION1", "option1", ConfigParser.MODE_BEFORE, False),
            ("Option1.1 inside",  "SECTION1", "option1", ConfigParser.MODE_INSIDE, True),
            ("Option1.1 after",   "SECTION1", "option1", ConfigParser.MODE_AFTER,  False),
            ("Option2.1 before",  "SECTION2", "option1", ConfigParser.MODE_BEFORE, False),
            ("Option2.1 inside",  "SECTION2", "option1", ConfigParser.MODE_INSIDE, True),
            ("Option2.1 after",   "SECTION2", "option1", ConfigParser.MODE_AFTER,  False),
            ("Option2.3 before",  "SECTION2", "option3", ConfigParser.MODE_BEFORE, True),
            ("Option2.3 inside",  "SECTION2", "option3", ConfigParser.MODE_INSIDE, True),
            ("Option2.3 after",   "SECTION2", "option3", ConfigParser.MODE_AFTER,  True),
            )

        for comment, section, option, mode, exceptionExpected in operations:

            try:
                config.add_blank(section, option, mode)
                self.assertEqual(False,
                                 exceptionExpected,
                                 "No exception generated for \"%s\", %s, %s, %s" %\
                                 (comment, section, option, mode))
            except ValueError:
                self.assertEqual(True,
                                 exceptionExpected,
                                 "Exception generated for \"%s\", %s, %s, %s" %\
                                 (comment, section, option, mode))
            # end try

            config.checkConsistency()
        # end for
    # end def test_AddBlank
# end class ConfigTestCase

class CachingConfigParserTestCase(ConfigTestCase):
    '''
    Test class for the caching config parser
    '''

    @staticmethod
    def _createConfigParser(*args, **kwArgs):
        '''
        @copydoc pylibrary.tools.test.configtest.ConfigTestCase._createConfigParser
        '''
        return CachingConfigParser(ConfigParser(*args, **kwArgs))
    # end def _createConfigParser
# end class CachingConfigParserTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
