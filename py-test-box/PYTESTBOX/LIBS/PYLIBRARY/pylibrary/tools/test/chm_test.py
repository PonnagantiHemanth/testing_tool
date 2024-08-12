#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.test.chm

@brief  chm testing module

@author christophe roquebert

@date   2018/07/13
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.chm import ChmError
from pylibrary.tools.chm import AbstractHtmlHelp
from pylibrary.tools.chm import HtmlHelpXml
from pylibrary.tools.chm import HtmlHelpContents
from pylibrary.tools.chm import HtmlHelpIndex
from pylibrary.tools.chm import HtmlHelpProject

from os                   import remove
from os.path              import isfile
from unittest             import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class AbstractHtmlHelpTestCase(TestCase):
    '''
    Test the behavoir of AbstractHtmlHelp class
    '''

    def setUp(self):
        '''
        setUp
        '''
        super(AbstractHtmlHelpTestCase, self).setUp()

    # end def setUp

    def tearDown(self):
        '''
        tearDown
        '''
        super(AbstractHtmlHelpTestCase, self).tearDown()
    # end def tearDown

    def test_hh(self):
        '''
        Test it
        '''
        hh = AbstractHtmlHelp('/bar/foo/index')

        # toFile error
        self.assertRaises(ChmError, hh.toFile)

        # fromFile error
        self.assertRaises(ChmError, AbstractHtmlHelp.fromFile, '/bar/foo/index')

    # end def test_hh

# end class AbstractHtmlHelpTestCase

class HtmlHelpXmlTestCase(TestCase):
    '''
    Tests the behavior of the HtmlHelpXml class
    '''

    def setUp(self):
        '''
        setUp
        '''
        super(HtmlHelpXmlTestCase, self).setUp()

    # end def setUp

    def tearDown(self):
        '''
        tearDown
        '''
        if isfile('index'):
            remove('index')
        # end if

        super(HtmlHelpXmlTestCase, self).tearDown()
    # end def tearDown


    def test_hhx(self):
        '''
        Test all methods
        '''
        # __init__
        hhxOut = HtmlHelpXml()

        # createPage
        heading = hhxOut.pages.appendChild(hhxOut.createPage('Heading'))
        heading.appendChild(hhxOut.createPage('Page', 'page.html'))

        # toFile, __str__
        hhxOut.toFile()

        # fromFile, _parse
        hhxIn = HtmlHelpXml.fromFile('index')

        self.assertEqual(hhxOut.pages.childNodes[0].localName,
                         hhxIn.pages.childNodes[0].localName)
    # end def test_hhx

# end class HtmlHelpXmlTestCase

class HtmlHelpContentsTestCase(TestCase):
    '''
    Tests the behavior of the HtmlHelpContents class
    '''

    def setUp(self):
        '''
        setUp
        '''
        super(HtmlHelpContentsTestCase, self).setUp()

    # end def setUp

    def tearDown(self):
        '''
        tearDown
        '''
        if isfile('index.hhc'):
            remove('index.hhc')
        # end if

        super(HtmlHelpContentsTestCase, self).tearDown()
    # end def tearDown

    def test_hhc(self):
        '''
        Test it
        '''
        hhc = HtmlHelpContents()
        hhc.toFile()

        self.assertTrue(isfile('index.hhc'))
    # end def test_hhc


# end class HtmlHelpContentsTestCase

class HtmlHelpIndexTestCase(TestCase):
    '''
    Tests the behavior of the HtmlHelpContents class
    '''

    def setUp(self):
        '''
        setUp
        '''
        super(HtmlHelpIndexTestCase, self).setUp()

    # end def setUp

    def tearDown(self):
        '''
        tearDown
        '''
        if isfile('index.hhk'):
            remove('index.hhk')
        # end if

        super(HtmlHelpIndexTestCase, self).tearDown()
    # end def tearDown

    def test_hhk(self):
        '''
        Test it
        '''
        hhk = HtmlHelpIndex()
        hhk.toFile()

        self.assertTrue(isfile('index.hhk'))
    # end def test_hhk


# end class HtmlHelpIndexTestCase

class HtmlHelpProjectTestCase(TestCase):
    '''
    Tests the behavior of the HtmlHelpProject class
    '''

    def setUp(self):
        '''
        setUp
        '''
        super(HtmlHelpProjectTestCase, self).setUp()

    # end def setUp

    def tearDown(self):
        '''
        tearDown
        '''
        if isfile('index.hhp'):
            remove('index.hhp')
        # end if

        if isfile('index.hhc'):
            remove('index.hhc')
        # end if

        if isfile('index.hhk'):
            remove('index.hhk')
        # end if

        super(HtmlHelpProjectTestCase, self).tearDown()
    # end def tearDown

    def test_hhp(self):
        '''
        Test it
        '''
        # __init__
        hhp = HtmlHelpProject()

        # _setOption / _getOption
        hhp.displayNotes    = not hhp.displayNotes
        hhp.displayProgress = not hhp.displayProgress
        hhp.title           = 'Test chm'

        self.assertFalse(hhp.displayNotes)
        self.assertTrue(hhp.displayProgress)
        self.assertEqual(hhp.title, 'Test chm')

        # toFile
        hhp.toFile()

        self.assertTrue(isfile('index.hhp'))
        self.assertFalse(isfile('index.hhc'))
        self.assertFalse(isfile('index.hhk'))


        hhp = HtmlHelpProject(contents = True,
                              index    = True)
        hhp.toFile()

        self.assertTrue(isfile('index.hhp'))
        self.assertTrue(isfile('index.hhc'))
        self.assertTrue(isfile('index.hhk'))

        # fromFile
        hhp.fromFile('index.hhp')

    # end def test_hhp

# end class HtmlHelpProjectTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
