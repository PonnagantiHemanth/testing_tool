#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.dfucontrol_test

@brief  HID++ 2.0 PowerModes test module

@author Stanislas Cottard

@date   2019/04/04
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.dfucontrol import DfuControlModel
from pyhid.hidpp.features.common.dfucontrol import DfuControlFactory
from pyhid.hidpp.features.common.dfucontrol import DfuControlInterface
from pyhid.hidpp.features.common.dfucontrol import DfuControlV0
from pyhid.hidpp.features.common.dfucontrol import DfuControl
from pyhid.hidpp.features.common.dfucontrol import GetDfuStatus
from pyhid.hidpp.features.common.dfucontrol import GetDfuStatusResponse
from pyhid.hidpp.features.common.dfucontrol import StartDfu
from pyhid.hidpp.features.common.dfucontrol import StartDfuResponse
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DfuControlInstantiationTestCase(TestCase):
    """
    DfuControl testing class
    """

    @staticmethod
    def test_dfu_control():
        """
        Tests DfuControl class instantiation
        """
        my_class = DfuControl(device_index=0,
                              feature_index=0)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_dfu_control

    @staticmethod
    def test_get_dfu_status():
        """
        Tests GetDfuStatus class instantiation
        """
        my_class = GetDfuStatus(device_index=0,
                                feature_index=0)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_dfu_status

    @staticmethod
    def test_start_dfu():
        """
        Tests StartDfu class instantiation
        """
        my_class = StartDfu(device_index=0,
                            feature_index=0,
                            enter_dfu=0,
                            dfu_control_param=0,
                            dfu_magic_key=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_start_dfu

    @staticmethod
    def test_get_dfu_status_response():
        """
        Tests GetDfuStatusResponse class instantiation
        """
        my_class = GetDfuStatusResponse(device_index=0,
                                        feature_index=0,
                                        enter_dfu=False,
                                        dfu_control_param=0,
                                        not_avail=False)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_dfu_status_response

    @staticmethod
    def test_start_dfu_response():
        """
        Tests StartDfu class instantiation
        """
        my_class = StartDfuResponse(device_index=0,
                                    feature_index=0)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_dfu_status_response
# end class DfuControlInstantiationTestCase


class DfuControlTestCase(TestCase):
    """
    Dfu Control factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": DfuControlV0,
                "interfaces": {
                    "get_dfu_status_cls": GetDfuStatus,
                    "start_dfu_cls": StartDfu,
                },
                "max_function_index": 1
            },
        }
    # end def setUpClass

    def test_dfu_control_factory(self):
        """
        Tests DFU control Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DfuControlFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_dfu_control_factory

    def test_dfu_control_factory_version_out_of_range(self):
        """
        Tests DFU control Factory with out of range versions
        """
        for version in [1, 2, 3]:
            with self.assertRaises(KeyError):
                DfuControlFactory.create(version)
            # end with
        # end for
    # end def test_dfu_control_factory_version_out_of_range

    def test_dfu_control_factory_interfaces(self):
        """
        Check DFU control Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            dfu_control = DfuControlFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(dfu_control, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(dfu_control, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_dfu_control_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            dfu_control = DfuControlFactory.create(version)
            self.assertEqual(dfu_control.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class DfuControlTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
