#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.test.enablehidden_test

@brief  HID++ 2.0 EnableHidden test module

@author Stanislas Cottard

@date   2019/04/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class EnableHiddenTestCase(TestCase):
    """
    EnableHidden testing class
    """

    @staticmethod
    def test_enable_hidden():
        """
        Tests EnableHidden class instantiation
        """
        my_class = EnableHidden(device_index=0,
                                feature_index=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_enable_hidden

    @staticmethod
    def test_get_enable_hidden_features():
        """
        Tests GetEnableHiddenFeatures class instantiation
        """
        my_class = GetEnableHiddenFeatures(device_index=0,
                                           feature_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_enable_hidden_features

    @staticmethod
    def test_set_enable_hidden_features():
        """
        Tests SetEnableHiddenFeatures class instantiation
        """
        my_class = SetEnableHiddenFeatures(device_index=0,
                                           feature_index=0,
                                           enable_byte=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_enable_hidden_features

    @staticmethod
    def test_get_enable_hidden_features_response():
        """
        Tests GetEnableHiddenFeaturesResponse class instantiation
        """
        my_class = GetEnableHiddenFeaturesResponse(device_index=0,
                                                   feature_index=0,
                                                   enable_byte=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_enable_hidden_features_response

    @staticmethod
    def test_set_enable_hidden_features_response():
        """
        Tests SetEnableHiddenFeaturesResponse class instantiation
        """
        my_class = SetEnableHiddenFeaturesResponse(device_index=0,
                                                   feature_index=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_enable_hidden_features_response
# end class EnableHiddenTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
