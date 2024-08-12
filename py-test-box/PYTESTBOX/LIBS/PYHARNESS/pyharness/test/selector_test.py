#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pyharness.test.feature

@brief  Test script "feature" decorator implementation module

@author christophe Roquebert

@date   2018/06/03
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from unittest                           import TestCase

from pyharness.selector                 import Features
from pyharness.selector                 import features


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
NEED1 = 'feature1'
NEED1_HELP = 'Help for feature1'
features.registerFeature(NEED1, lambda: True, featureHelp = NEED1_HELP)

NEED2 = 'feature2'
NEED2_HELP = 'Help for feature2'
features.registerFeature(NEED2, lambda: True, featureHelp = NEED2_HELP)

class FeaturesTestCase(TestCase):
    '''
    Features testing class
    '''
    RefClass = Features

    @classmethod
    def _createInstance(cls):
        '''
        Create a RefClass instance

        @return (RefClass) RefClass instance
        '''
        return cls.RefClass()
    # end def _createInstance

    def marker_nofeature(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_nofeature

    @features(NEED1)
    def marker_feature1(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_feature1

    @features(NEED2)
    def marker_feature2(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_feature2

    @features(NEED1, 1)
    def marker_feature1_arg(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_feature1_arg

    @features(NEED1, 1, 2, 3)
    def marker_feature1_args(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_feature1_args

    @features(NEED1)
    @features(NEED2)
    def marker_feature1_feature2(self):
        '''
        marker method, for test purposes
        '''
        pass
    # end def marker_feature1_feature2

    def testNew(self):
        '''
        Tests new method
        '''
        feature1 = self._createInstance()
        feature2 = self._createInstance()

        self.assertEqual(id(feature1), id(feature2), 'Features class shall be a singleton')
    # end def testNew

    def testRegisterFeature(self):
        '''
        Tests registerFeature
        '''
        feature = 'feature_RegisterFeature'
        features.registerFeature(feature, lambda :True)
        features.setHelp(feature, 'Feature help')

        feature = 'feature_RegisterFeature2'
        featureHelp = 'Feature2 help'
        features.registerFeature(feature, lambda :True, featureHelp)
        self.assertEqual(featureHelp, features.getHelp(feature))
    # end def testRegisterFeature

    def testRegisterFeature_WrongType(self):
        '''
        Check type of parameters of registerFeature
        '''
        feature = 'feature_RegisterFeature_WrongType'
        features.registerFeature(feature, lambda :True)

        # Check feature type
        self.assertRaises(TypeError, features.registerFeature, 1, lambda :True)
        self.assertRaises(TypeError, features.registerFeature, [1], lambda :True)
        self.assertRaises(TypeError, features.registerFeature, (1, ), lambda :True)

        # Check function type
        self.assertRaises(TypeError, features.registerFeature, feature, 1)
        self.assertRaises(TypeError, features.registerFeature, feature, '1')
        self.assertRaises(TypeError, features.registerFeature, feature, [1])
        self.assertRaises(TypeError, features.registerFeature, feature, (1, ))

        # Check featureHelp type
        self.assertRaises(TypeError, features.registerFeature, feature, lambda :True, 1)
        self.assertRaises(TypeError, features.registerFeature, feature, lambda :True, [1])
        self.assertRaises(TypeError, features.registerFeature, feature, lambda :True, (1, ))
    # end def testRegisterFeature_WrongType

    def testRegisterFeature_Duplicate(self):
        '''
        Tests registerFeature with duplicate feature
        '''
        feature = 'feature_RegisterFeature_Duplicate'
        features.registerFeature(feature, lambda :True)

        self.assertRaises(ValueError, features.registerFeature, feature, lambda :True)
    # end def testRegisterFeature_Duplicate

    def testHelp(self):
        '''
        Tests getHelp and setHelp methods
        '''
        feature = 'featureHelp'
        featureHelp = 'Help of feature'
        features.registerFeature(feature, lambda: True, featureHelp = featureHelp)

        self.assertEqual(featureHelp, features.getHelp(feature))

        featureHelp = 'New help of feature'
        features.setHelp(feature, featureHelp)
        self.assertEqual(featureHelp, features.getHelp(feature))

    # end def testHelp

    def testIsDecorated(self):
        '''
        Tests the isDecorated method
        '''
        self.assertFalse(features.isDecorated(self.marker_nofeature),
                         'non-featured method should not be detected as defining feature')

        self.assertTrue(features.isDecorated(self.marker_feature1),
                        'one-feature method should be detected as defining a feature')
        self.assertTrue(features.isDecorated(self.marker_feature2),
                        'one-feature method should be detected as defining a feature')
        self.assertTrue(features.isDecorated(self.marker_feature1_arg),
                        'two-feature method should be detected as defining a feature')
        self.assertTrue(features.isDecorated(self.marker_feature1_args),
                        'two-feature method should be detected as defining a feature')
        self.assertTrue(features.isDecorated(self.marker_feature1_feature2),
                        'two-feature method should be detected as defining a feature')
    # end def testIsDecorated

    def testHasFeature_NoFeature(self):
        '''
        Tests the hasFeature method
        '''
        # Non-existent feature
        self.assertFalse(features.hasFeatures(self.marker_nofeature, 'nofeature'),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1, 'nofeature'),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature2, 'nofeature'),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1_arg, 'nofeature'),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1_args, 'nofeature'),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1_feature2, 'nofeature'),
                         'Non-existent feature found')
    # end def testHasFeature_NoFeature

    def testHasFeatures_Feature1(self):
        '''
        Tests the hasFeatures method
        '''

        # Non-existent feature
        self.assertFalse(features.hasFeatures(self.marker_nofeature, NEED1),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1, NEED1),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature2, NEED1),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_arg, NEED1),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_args, NEED1),
                        'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_feature2, NEED1),
                         'Non-existent feature found')
    # end def testHasFeatures_Feature1

    def testHasFeatures_Feature2(self):
        '''
        Tests the hasFeatures method
        '''

        # Non-existent feature
        self.assertFalse(features.hasFeatures(self.marker_nofeature, NEED2),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1, NEED2),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1_arg, NEED2),
                         'Non-existent feature found')
        self.assertFalse(features.hasFeatures(self.marker_feature1_args, NEED2),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature2, NEED2),
                        'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_feature2, NEED2),
                        'Non-existent feature found')
    # end def testHasFeatures_Feature2

    def testHasFeatures_Feature1_Feature2(self):
        '''
        Tests the hasFeatures method
        '''

        # Non-existent feature
        self.assertFalse(features.hasFeatures(self.marker_nofeature, (NEED1, NEED2)),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_arg, (NEED1, NEED2)),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_args, (NEED1, NEED2)),
                         'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1, (NEED1, NEED2)),
                        'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature2, (NEED1, NEED2)),
                        'Non-existent feature found')
        self.assertTrue(features.hasFeatures(self.marker_feature1_feature2, (NEED1, NEED2)),
                        'Non-existent feature found')
    # end def testHasFeatures_Feature1_Feature2

    def testGetFeatures(self):
        '''
        Tests the getFeatures method
        '''
        self.assertEqual(set(),
                         features.getFeatures(self.marker_nofeature),
                         'Invalid getFeatures result found (no feature expected)')
        self.assertEqual(set([('feature1', ())]),
                         features.getFeatures(self.marker_feature1),
                         'Invalid getFeatures result found (feature1 expected)')
        self.assertEqual(set([('feature2', ())]),
                         features.getFeatures(self.marker_feature2),
                         'Invalid getFeatures result found (feature2 expected)')
        self.assertEqual(set([('feature1', (1,))]),
                         features.getFeatures(self.marker_feature1_arg),
                         'Invalid getFeatures result found (both feature expected, single declaration)')
        self.assertEqual(set([('feature1', (1, 2, 3))]),
                         features.getFeatures(self.marker_feature1_args),
                         'Invalid getFeatures result found (both feature expected, single declaration)')
        self.assertEqual(set([('feature1', ()), ('feature2', ())]),
                         features.getFeatures(self.marker_feature1_feature2),
                         'Invalid getFeatures result found (both feature expected, multiple declaration)')

        self.assertEqual(['feature1', 'feature2'],
                         features.getFeatures(),
                         'Invalid getFeatures result found (previous declaration)')

    # end def testGetFeatures

# end class FeaturesTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
