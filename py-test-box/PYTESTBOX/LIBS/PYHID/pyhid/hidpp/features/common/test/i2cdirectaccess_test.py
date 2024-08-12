#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.test.i2cdirectaccess_test
:brief: HID++ 2.0 ``I2CDirectAccess`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.i2cdirectaccess import GetNbDevices
from pyhid.hidpp.features.common.i2cdirectaccess import GetNbDevicesResponse
from pyhid.hidpp.features.common.i2cdirectaccess import GetSelectedDevice
from pyhid.hidpp.features.common.i2cdirectaccess import GetSelectedDeviceResponse
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccess
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccessFactory
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccessV0
from pyhid.hidpp.features.common.i2cdirectaccess import I2CReadDirectAccess
from pyhid.hidpp.features.common.i2cdirectaccess import I2CReadDirectAccessResponse
from pyhid.hidpp.features.common.i2cdirectaccess import I2CWriteDirectAccess
from pyhid.hidpp.features.common.i2cdirectaccess import I2CWriteDirectAccessResponse
from pyhid.hidpp.features.common.i2cdirectaccess import SelectDevice
from pyhid.hidpp.features.common.i2cdirectaccess import SelectDeviceResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CDirectAccessInstantiationTestCase(TestCase):
    """
    Test ``I2CDirectAccess`` testing classes instantiations
    """

    @staticmethod
    def test_i2c_direct_access():
        """
        Test ``I2CDirectAccess`` class instantiation
        """
        my_class = I2CDirectAccess(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = I2CDirectAccess(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_i2c_direct_access

    @staticmethod
    def test_get_nb_devices():
        """
        Test ``GetNbDevices`` class instantiation
        """
        my_class = GetNbDevices(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetNbDevices(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_nb_devices

    @staticmethod
    def test_get_nb_devices_response():
        """
        Test ``GetNbDevicesResponse`` class instantiation
        """
        my_class = GetNbDevicesResponse(device_index=0, feature_index=0,
                                        number_of_devices=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetNbDevicesResponse(device_index=0xff, feature_index=0xff,
                                        number_of_devices=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_nb_devices_response

    @staticmethod
    def test_get_selected_device():
        """
        Test ``GetSelectedDevice`` class instantiation
        """
        my_class = GetSelectedDevice(device_index=0, feature_index=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetSelectedDevice(device_index=0xff, feature_index=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_selected_device

    @staticmethod
    def test_get_selected_device_response():
        """
        Test ``GetSelectedDeviceResponse`` class instantiation
        """
        my_class = GetSelectedDeviceResponse(device_index=0, feature_index=0,
                                             device_idx=0,
                                             disable_fw_access=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSelectedDeviceResponse(device_index=0xff, feature_index=0xff,
                                             device_idx=0xff,
                                             disable_fw_access=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_selected_device_response

    @staticmethod
    def test_select_device():
        """
        Test ``SelectDevice`` class instantiation
        """
        my_class = SelectDevice(device_index=0, feature_index=0,
                                device_idx=0,
                                access_config=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = SelectDevice(device_index=0xff, feature_index=0xff,
                                device_idx=0xff,
                                access_config=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_select_device

    @staticmethod
    def test_select_device_response():
        """
        Test ``SelectDeviceResponse`` class instantiation
        """
        my_class = SelectDeviceResponse(device_index=0, feature_index=0,
                                        device_idx=0,
                                        disable_fw_access=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SelectDeviceResponse(device_index=0xff, feature_index=0xff,
                                        device_idx=0xff,
                                        disable_fw_access=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_select_device_response

    @staticmethod
    def test_i2c_read_direct_access():
        """
        Test ``I2CReadDirectAccess`` class instantiation
        """
        my_class = I2CReadDirectAccess(device_index=0, feature_index=0,
                                       n_bytes=0,
                                       register_address=0)

        RootTestCase._short_function_class_checker(my_class)

        my_class = I2CReadDirectAccess(device_index=0xff, feature_index=0xff,
                                       n_bytes=0xff,
                                       register_address=0xff)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_i2c_read_direct_access

    @staticmethod
    def test_i2c_read_direct_access_response():
        """
        Test ``I2CReadDirectAccessResponse`` class instantiation
        """
        my_class = I2CReadDirectAccessResponse(device_index=0, feature_index=0,
                                               n_bytes=0,
                                               data_out_1=0,
                                               data_out_2=0,
                                               data_out_3=0,
                                               data_out_4=0,
                                               data_out_5=0,
                                               data_out_6=0,
                                               data_out_7=0,
                                               data_out_8=0,
                                               data_out_9=0,
                                               data_out_10=0,
                                               data_out_11=0,
                                               data_out_12=0,
                                               data_out_13=0,
                                               data_out_14=0,
                                               data_out_15=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = I2CReadDirectAccessResponse(device_index=0xff, feature_index=0xff,
                                               n_bytes=0xff,
                                               data_out_1=0xff,
                                               data_out_2=0xff,
                                               data_out_3=0xff,
                                               data_out_4=0xff,
                                               data_out_5=0xff,
                                               data_out_6=0xff,
                                               data_out_7=0xff,
                                               data_out_8=0xff,
                                               data_out_9=0xff,
                                               data_out_10=0xff,
                                               data_out_11=0xff,
                                               data_out_12=0xff,
                                               data_out_13=0xff,
                                               data_out_14=0xff,
                                               data_out_15=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_i2c_read_direct_access_response

    @staticmethod
    def test_i2c_write_direct_access():
        """
        Test ``I2CWriteDirectAccess`` class instantiation
        """
        my_class = I2CWriteDirectAccess(device_index=0, feature_index=0,
                                        n_bytes=0,
                                        register_address=0,
                                        data_in_1=0,
                                        data_in_2=0,
                                        data_in_3=0,
                                        data_in_4=0,
                                        data_in_5=0,
                                        data_in_6=0,
                                        data_in_7=0,
                                        data_in_8=0,
                                        data_in_9=0,
                                        data_in_10=0,
                                        data_in_11=0,
                                        data_in_12=0,
                                        data_in_13=0,
                                        data_in_14=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = I2CWriteDirectAccess(device_index=0xff, feature_index=0xff,
                                        n_bytes=0xff,
                                        register_address=0xff,
                                        data_in_1=0xff,
                                        data_in_2=0xff,
                                        data_in_3=0xff,
                                        data_in_4=0xff,
                                        data_in_5=0xff,
                                        data_in_6=0xff,
                                        data_in_7=0xff,
                                        data_in_8=0xff,
                                        data_in_9=0xff,
                                        data_in_10=0xff,
                                        data_in_11=0xff,
                                        data_in_12=0xff,
                                        data_in_13=0xff,
                                        data_in_14=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_i2c_write_direct_access

    @staticmethod
    def test_i2c_write_direct_access_response():
        """
        Test ``I2CWriteDirectAccessResponse`` class instantiation
        """
        my_class = I2CWriteDirectAccessResponse(device_index=0, feature_index=0,
                                                n_bytes=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = I2CWriteDirectAccessResponse(device_index=0xff, feature_index=0xff,
                                                n_bytes=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_i2c_write_direct_access_response
# end class I2CDirectAccessInstantiationTestCase


class I2CDirectAccessTestCase(TestCase):
    """
    Test ``I2CDirectAccess`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            I2CDirectAccessV0.VERSION: {
                "cls": I2CDirectAccessV0,
                "interfaces": {
                    "get_nb_devices_cls": GetNbDevices,
                    "get_nb_devices_response_cls": GetNbDevicesResponse,
                    "get_selected_device_cls": GetSelectedDevice,
                    "get_selected_device_response_cls": GetSelectedDeviceResponse,
                    "select_device_cls": SelectDevice,
                    "select_device_response_cls": SelectDeviceResponse,
                    "i2c_read_direct_access_cls": I2CReadDirectAccess,
                    "i2c_read_direct_access_response_cls": I2CReadDirectAccessResponse,
                    "i2c_write_direct_access_cls": I2CWriteDirectAccess,
                    "i2c_write_direct_access_response_cls": I2CWriteDirectAccessResponse,
                },
                "max_function_index": 4
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``I2CDirectAccessFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(I2CDirectAccessFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``I2CDirectAccessFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [1, 2]:
            with self.assertRaises(KeyError):
                I2CDirectAccessFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``I2CDirectAccessFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = I2CDirectAccessFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(obj, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(obj, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check ``get_max_function_index`` returns correct value at each version

        :raise ``AssertionError``: Assert max_function_index that raise an exception
        """
        for version, expected in self.expected.items():
            obj = I2CDirectAccessFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class I2CDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
