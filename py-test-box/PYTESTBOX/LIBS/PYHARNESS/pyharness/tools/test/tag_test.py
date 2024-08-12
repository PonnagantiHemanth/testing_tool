#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.tools.test.tag

@brief  Tests of the tag module

@author christophe.roquebert

@date   2018/12/08
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.tools.tag                 import Tag
from unittest                           import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class TestTag(Tag):
    '''
    A test-specific test tag class
    '''
    TAG_IDENTIFIER = 'testtag'

    def __init__(self):
        '''
        Constructor
        '''
        super(TestTag, self).__init__(self.TAG_IDENTIFIER)
    # end def __init__
# end class TestTag

TESTTAG = TestTag()

TESTTAG.setHelp('tag1', 'This is tag1\'s help')

class TagTestCase(TestCase):
    '''
    Tests of the Tag class, and its derived classes
    '''

    def marker_notags(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_notags

    @TESTTAG('tag1')
    def marker_tag1(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_tag1

    @TESTTAG('tag2')
    def marker_tag2(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_tag2

    @TESTTAG('tag1', 'tag2')
    def marker_tag1_tag2_onedecl(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_tag1_tag2_onedecl

    @TESTTAG('tag1')
    @TESTTAG('tag2')
    def marker_tag1_tag2_twodecls(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_tag1_tag2_twodecls

    def testGetTagRepositories(self):
        '''
        Tests the getTagRepositories method
        '''
        self.assertTrue(TestTag.TAG_IDENTIFIER in TestTag.getTagRepositories(),
                        'Tag class not registered')
    # end def testGetTagRepositories

    def testMultipleRegistration(self):
        '''
        Tests multiple registrations of the Tag class
        '''

        self.assertRaises(AssertionError,
                          TestTag)
    # end def testMultipleRegistration

    def testDefinesTag(self):
        '''
        Tests the definesTag method
        '''
        self.assertFalse(TESTTAG.definesTag(self.marker_notags()),
                         'non-tagged method should not be detected as defining tag')

        self.assertTrue(TESTTAG.definesTag(self.marker_tag1),
                        'one-tag method should be detected as defining a tag')
        self.assertTrue(TESTTAG.definesTag(self.marker_tag2),
                        'one-tag method should be detected as defining a tag')
        self.assertTrue(TESTTAG.definesTag(self.marker_tag1_tag2_onedecl),
                        'two-tag method should be detected as defining a tag')
        self.assertTrue(TESTTAG.definesTag(self.marker_tag1_tag2_twodecls),
                        'two-tag method should be detected as defining a tag')
    # end def testDefinesTag

    def testHasTag_NoTag(self):
        '''
        Tests the hasTag method
        '''

        # Non-existent tag
        self.assertFalse(TESTTAG.hasTag(self.marker_notags, 'notag'),
                         'Non-existent tag found')
        self.assertFalse(TESTTAG.hasTag(self.marker_tag1, 'notag'),
                         'Non-existent tag found')
        self.assertFalse(TESTTAG.hasTag(self.marker_tag2, 'notag'),
                         'Non-existent tag found')
        self.assertFalse(TESTTAG.hasTag(self.marker_tag1_tag2_onedecl, 'notag'),
                         'Non-existent tag found')
        self.assertFalse(TESTTAG.hasTag(self.marker_tag1_tag2_twodecls, 'notag'),
                         'Non-existent tag found')
    # end def testHasTag_NoTag

    def testHasTag_Tag1(self):
        '''
        Tests the hasTag method
        '''

        # Non-existent tag
        self.assertFalse(TESTTAG.hasTag(self.marker_notags, 'tag1'),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1, 'tag1'),
                         'Non-existent tag found')
        self.assertFalse(TESTTAG.hasTag(self.marker_tag2, 'tag1'),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1_tag2_onedecl, 'tag1'),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1_tag2_twodecls, 'tag1'),
                         'Non-existent tag found')
    # end def testHasTag_Tag1

    def testHasTag_Tag2(self):
        '''
        Tests the hasTag method
        '''

        # Non-existent tag
        self.assertFalse(TESTTAG.hasTag(self.marker_notags, 'tag2'),
                         'Non-existent tag found')
        self.assertFalse(TESTTAG.hasTag(self.marker_tag1, 'tag2'),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag2, 'tag2'),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1_tag2_onedecl, 'tag2'),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1_tag2_twodecls, 'tag2'),
                         'Non-existent tag found')
    # end def testHasTag_Tag2

    def testHasTag_Tag1_Tag2(self):
        '''
        Tests the hasTag method
        '''

        # Non-existent tag
        self.assertFalse(TESTTAG.hasTag(self.marker_notags, ('tag1', 'tag2')),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1, ('tag1', 'tag2')),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag2, ('tag1', 'tag2')),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1_tag2_onedecl, ('tag1', 'tag2')),
                         'Non-existent tag found')
        self.assertTrue(TESTTAG.hasTag(self.marker_tag1_tag2_twodecls, ('tag1', 'tag2')),
                         'Non-existent tag found')
    # end def testHasTag_Tag1_Tag2

    def testGetTags(self):
        '''
        Tests the getTags method
        '''
        self.assertEqual(set(),
                         TESTTAG.getTags(self.marker_notags),
                         'Invalid getTags result found (no tags expected)')
        self.assertEqual(set(['tag1']),
                         TESTTAG.getTags(self.marker_tag1),
                         'Invalid getTags result found (tag1 expected)')
        self.assertEqual(set(['tag2']),
                         TESTTAG.getTags(self.marker_tag2),
                         'Invalid getTags result found (tag2 expected)')
        self.assertEqual(set(['tag1', 'tag2']),
                         TESTTAG.getTags(self.marker_tag1_tag2_onedecl),
                         'Invalid getTags result found (both tags expected, single declaration)')
        self.assertEqual(set(['tag1', 'tag2']),
                         TESTTAG.getTags(self.marker_tag1_tag2_twodecls),
                         'Invalid getTags result found (both tags expected, multiple declaration)')

        self.assertEqual(['tag1', 'tag2'],
                         TESTTAG.getTags(),
                         'Invalid getTags result found (previous declaration)')

    # end def testGetTags

    def testRestrictTags(self):
        '''
        Tests the restricttags method
        '''
        # Restrict the tags to 'tag1'
        TESTTAG.restrictTags(['tag1'])
        self.assertEqual(TESTTAG._tagSet,                                                                               #pylint:disable=W0212
                         set(['tag1']),
                         'Wrong set of tags restriction')

        self.assertRaises(ValueError,
                          TESTTAG,
                          'tag2')

    # end def testRestrictTags

    def testTagHelp(self):
        '''
        Tests the setHelp/getHelp methods
        '''
        self.assertEqual(TESTTAG.getHelp('tag1'),
                         'This is tag1\'s help',
                         'Invalid help')
        self.assertTrue(TESTTAG.getHelp('tag2') is None,
                        'Invalid help')
        self.assertEqual(TESTTAG.getHelp(),
                         {'tag1': 'This is tag1\'s help'},
                         'Invalid help')

    # end def testTagHelp
# end class TagTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
