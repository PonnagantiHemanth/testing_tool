#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.test.spidirectaccess_test
:brief: HID++ 2.0 ``SPIDirectAccess`` test module
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import TestCase

from pyhid.hidpp.features.common.spidirectaccess import GetNbDevices
from pyhid.hidpp.features.common.spidirectaccess import GetNbDevicesResponse
from pyhid.hidpp.features.common.spidirectaccess import GetSelectedDevice
from pyhid.hidpp.features.common.spidirectaccess import GetSelectedDeviceResponse
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccess
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccessFactory
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccessV0
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccessV1
from pyhid.hidpp.features.common.spidirectaccess import SelectDevice
from pyhid.hidpp.features.common.spidirectaccess import SelectDeviceResponseV0
from pyhid.hidpp.features.common.spidirectaccess import SelectDeviceResponseV1
from pyhid.hidpp.features.common.spidirectaccess import SpiDirectAccess
from pyhid.hidpp.features.common.spidirectaccess import SpiDirectAccessResponse
from pyhid.hidpp.features.test.root_test import RootTestCase


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SPIDirectAccessInstantiationTestCase(TestCase):
    """
    Test ``SPIDirectAccess`` testing classes instantiations
    """

    @staticmethod
    def test_spi_direct_access():
        """
        Test ``SPIDirectAccess`` class instantiation
        """
        my_class = SPIDirectAccess(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = SPIDirectAccess(device_index=0xff, feature_index=0xff)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_spi_direct_access

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
                                             enable_atomic_cs=False,
                                             disable_fw_access=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetSelectedDeviceResponse(device_index=0xff, feature_index=0xff,
                                             device_idx=0xff,
                                             enable_atomic_cs=True,
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
    def test_select_device_response_v0():
        """
        Test ``SelectDeviceResponseV0`` class instantiation
        """
        my_class = SelectDeviceResponseV0(device_index=0, feature_index=0,
                                          device_idx=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SelectDeviceResponseV0(device_index=0xff, feature_index=0xff,
                                          device_idx=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_select_device_response_v0

    @staticmethod
    def test_select_device_response_v1():
        """
        Test ``SelectDeviceResponseV1`` class instantiation
        """
        my_class = SelectDeviceResponseV1(device_index=0, feature_index=0,
                                          device_idx=0,
                                          enable_atomic_cs=False,
                                          disable_fw_access=False)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SelectDeviceResponseV1(device_index=0xff, feature_index=0xff,
                                          device_idx=0xff,
                                          enable_atomic_cs=True,
                                          disable_fw_access=True)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_select_device_response_v1

    @staticmethod
    def test_spi_direct_access_request():
        """
        Test ``SpiDirectAccess`` class instantiation
        """
        my_class = SpiDirectAccess(device_index=0, feature_index=0,
                                   n_bytes=0,
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
                                   data_in_14=0,
                                   data_in_15=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = SpiDirectAccess(device_index=0xff, feature_index=0xff,
                                   n_bytes=0xff,
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
                                   data_in_14=0xff,
                                   data_in_15=0xff)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_spi_direct_access_request

    @staticmethod
    def test_spi_direct_access_response():
        """
        Test ``SpiDirectAccessResponse`` class instantiation
        """
        my_class = SpiDirectAccessResponse(device_index=0, feature_index=0,
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

        my_class = SpiDirectAccessResponse(device_index=0xff, feature_index=0xff,
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
    # end def test_spi_direct_access_response
# end class SPIDirectAccessInstantiationTestCase


class SPIDirectAccessTestCase(TestCase):
    """
    Test ``SPIDirectAccess`` factory feature
    """

    @classmethod
    def setUpClass(cls):
        """
        Handle class prerequisites
        """
        cls.expected = {
            SPIDirectAccessV0.VERSION: {
                "cls": SPIDirectAccessV0,
                "interfaces": {
                    "get_nb_devices_cls": GetNbDevices,
                    "get_nb_devices_response_cls": GetNbDevicesResponse,
                    "get_selected_device_cls": GetSelectedDevice,
                    "get_selected_device_response_cls": GetSelectedDeviceResponse,
                    "select_device_cls": SelectDevice,
                    "select_device_response_cls": SelectDeviceResponseV0,
                    "spi_direct_access_cls": SpiDirectAccess,
                    "spi_direct_access_response_cls": SpiDirectAccessResponse,
                },
                "max_function_index": 3
            },
            SPIDirectAccessV1.VERSION: {
                "cls": SPIDirectAccessV1,
                "interfaces": {
                    "get_nb_devices_cls": GetNbDevices,
                    "get_nb_devices_response_cls": GetNbDevicesResponse,
                    "get_selected_device_cls": GetSelectedDevice,
                    "get_selected_device_response_cls": GetSelectedDeviceResponse,
                    "select_device_cls": SelectDevice,
                    "select_device_response_cls": SelectDeviceResponseV1,
                    "spi_direct_access_cls": SpiDirectAccess,
                    "spi_direct_access_response_cls": SpiDirectAccessResponse,
                },
                "max_function_index": 3
            },
        }
    # end def setUpClass

    def test_factory(self):
        """
        Test ``SPIDirectAccessFactory``

        :raise ``AssertionError``: Assert class type that raise an exception
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(SPIDirectAccessFactory.create(version)), expected["cls"])
        # end for
    # end def test_factory

    def test_factory_version_out_of_range(self):
        """
        Test ``SPIDirectAccessFactory`` using out of range versions

        :raise ``AssertionError``: Assert creation of class that raise an exception
        """
        for version in [2, 3]:
            with self.assertRaises(KeyError):
                SPIDirectAccessFactory.create(version)
            # end with
        # end for
    # end def test_factory_version_out_of_range

    def test_factory_interfaces(self):
        """
        Check ``SPIDirectAccessFactory`` returns expected interfaces

        :raise ``AssertionError``: Assert get attribute that raise an exception
        """
        for version, cls_map in self.expected.items():
            obj = SPIDirectAccessFactory.create(version)
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
            obj = SPIDirectAccessFactory.create(version)
            self.assertEqual(obj.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class SPIDirectAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
