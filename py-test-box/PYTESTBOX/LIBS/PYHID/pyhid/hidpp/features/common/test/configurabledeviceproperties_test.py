#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.feature.common.test.configurabledeviceproperties_test
:brief: HID++ 2.0 Configurable Device Properties test module
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/01/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDeviceProperties
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesV6
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesV7
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesV8
from pyhid.hidpp.features.common.configurabledeviceproperties import GetDeviceNameMaxCountResponseV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import GetDeviceNameMaxCountV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import GetDevicePropertiesResponseV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import GetDevicePropertiesV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDeviceExtendModelIdResponseV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDeviceExtendModelIdV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDeviceNameCommitResponseV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDeviceNameCommitV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDeviceNameResponseV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDeviceNameV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDevicePropertiesResponseV6ToV8
from pyhid.hidpp.features.common.configurabledeviceproperties import SetDevicePropertiesV6ToV8
from pyhid.hidpp.features.test.root_test import RootTestCase
from pylibrary.tools.hexlist import HexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class ConfigurableDevicePropertiesInstantiationTestCase(TestCase):
    """
    ConfigurableDeviceProperties testing class
    """
    @staticmethod
    def test_configurable_device_properties():
        """
        Tests ConfigurableDeviceProperties class instantiation
        """
        my_class = ConfigurableDeviceProperties(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = ConfigurableDeviceProperties(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_configurable_device_properties

    @staticmethod
    def test_get_device_name_max_count():
        """
        Tests GetDeviceNameMaxCount class instantiation
        """
        my_class = GetDeviceNameMaxCountV6ToV8(device_index=0x00, feature_index=0x00)

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDeviceNameMaxCountV6ToV8(device_index=0xFF, feature_index=0xFF)

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_name_max_count

    @staticmethod
    def test_get_device_name_max_count_response():
        """
        Tests GetDeviceNameMaxCountResponse class instantiation
        """
        my_class = GetDeviceNameMaxCountResponseV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                device_name_max_count=0x00
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = GetDeviceNameMaxCountResponseV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                device_name_max_count=0xFF
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_get_device_name_max_count_response

    @staticmethod
    def test_set_device_name():
        """
        Tests SetDeviceName class instantiation
        """
        my_class = SetDeviceNameV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                char_index=0x00,
                device_name=HexList("00"),
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDeviceNameV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                char_index=0xFF,
                device_name=HexList("FF" * 15),
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_name

    @staticmethod
    def test_set_device_name_response():
        """
        Tests SetDeviceNameResponse class instantiation
        """
        my_class = SetDeviceNameResponseV6ToV8(
                device_index=0x00,
                feature_index=0x00,
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDeviceNameResponseV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_name_response

    @staticmethod
    def test_set_device_name_commit():
        """
        Tests SetDeviceNameCommit class instantiation
        """
        my_class = SetDeviceNameCommitV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                length=0x00
        )

        RootTestCase._short_function_class_checker(my_class)

        my_class = SetDeviceNameCommitV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                length=0xFF
        )

        RootTestCase._short_function_class_checker(my_class)
    # end def test_set_device_name_commit

    @staticmethod
    def test_set_device_name_commit_response():
        """
        Tests SetDeviceNameCommitResponse class instantiation
        """
        my_class = SetDeviceNameCommitResponseV6ToV8(
                device_index=0x00,
                feature_index=0x00,
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDeviceNameCommitResponseV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_name_response

    @staticmethod
    def test_set_device_extended_model_id():
        """
        Tests SetDeviceExtendedModelID class instantiation
        """
        my_class = SetDeviceExtendModelIdV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                extended_model_id=0x00
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDeviceExtendModelIdV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                extended_model_id=0xFF
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_extended_model_id

    @staticmethod
    def test_set_device_extended_model_id_response():
        """
        Tests SetDeviceExtendedModelIDResponse class instantiation
        """
        my_class = SetDeviceExtendModelIdResponseV6ToV8(
                device_index=0x00,
                feature_index=0x00,
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDeviceExtendModelIdResponseV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_extended_model_id_response

    @staticmethod
    def test_set_device_properties():
        """
        Tests SetDeviceProperties class instantiation
        """
        my_class = SetDevicePropertiesV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                property_id=0x00,
                flag=0x00,
                sub_data_index=0x00,
                property_data=HexList("00" * (SetDevicePropertiesV6ToV8.LEN.PROPERTY_DATA // 8))
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDevicePropertiesV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                property_id=0x00,
                flag=False,
                sub_data_index=0x00,
                property_data=HexList("00" * (SetDevicePropertiesV6ToV8.LEN.PROPERTY_DATA // 8))
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDevicePropertiesV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                property_id=0xFF,
                flag=0x01,
                sub_data_index=0x7F,
                property_data=HexList("FF" * (SetDevicePropertiesV6ToV8.LEN.PROPERTY_DATA // 8))
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDevicePropertiesV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                property_id=0xFF,
                flag=True,
                sub_data_index=0x7F,
                property_data=HexList("FF" * (SetDevicePropertiesV6ToV8.LEN.PROPERTY_DATA // 8))
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_properties

    @staticmethod
    def test_set_device_properties_response():
        """
        Tests SetDevicePropertiesResponse class instantiation
        """
        my_class = SetDevicePropertiesResponseV6ToV8(
                device_index=0x00,
                feature_index=0x00,
        )

        RootTestCase._long_function_class_checker(my_class)

        my_class = SetDevicePropertiesResponseV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
        )

        RootTestCase._long_function_class_checker(my_class)
    # end def test_set_device_properties_response

    @staticmethod
    def test_get_device_properties():
        """
        Tests GetDeviceProperties class instantiation
        """
        my_class = GetDevicePropertiesV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                property_id=0x00,
                flag=0x00,
                sub_data_index=0x00
        )

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDevicePropertiesV6ToV8(
                device_index=0x00,
                feature_index=0x00,
                property_id=0x00,
                flag=False,
                sub_data_index=0x00
        )

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDevicePropertiesV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                property_id=0xFF,
                flag=0x01,
                sub_data_index=0x7F
        )

        RootTestCase._short_function_class_checker(my_class)

        my_class = GetDevicePropertiesV6ToV8(
                device_index=0xFF,
                feature_index=0xFF,
                property_id=0xFF,
                flag=True,
                sub_data_index=0x7F
        )

        RootTestCase._short_function_class_checker(my_class)
    # end def test_get_device_properties

    @staticmethod
    def test_get_device_properties_response():
        """
        Tests GetDevicePropertiesResponse class instantiation
        """
        sizes = ConfigurableDeviceProperties.PropertySizeV8.get_all_sizes()
        for pid in range(len(sizes)):
            property_data_len = sizes[pid - 1]
            if property_data_len > 14:
                property_data_len = 14
            # end if
            my_class = GetDevicePropertiesResponseV6ToV8(
                    device_index=0x00,
                    feature_index=0x00,
                    property_id=pid,
                    sub_data_index=0x00,
                    property_data=HexList("00" * property_data_len)
            )

            RootTestCase._long_function_class_checker(my_class)
        # end for

        for pid in range(len(sizes)):
            property_data_len = sizes[pid - 1]
            if property_data_len > 14:
                property_data_len = 14
            # end if
            my_class = GetDevicePropertiesResponseV6ToV8(
                    device_index=0xFF,
                    feature_index=0xFF,
                    property_id=pid,
                    sub_data_index=0xFF,
                    property_data=HexList("FF" * property_data_len)
            )

            RootTestCase._long_function_class_checker(my_class)
        # end for
    # end def test_get_device_properties_response
# end class ConfigurableDevicePropertiesInstantiationTestCase


class ConfigurableDevicePropertiesTestCase(TestCase):
    """
    ConfigurableDeviceProperties factory testing
    """
    @classmethod
    def setUpClass(cls):
        api_v6_to_v8 = {
                "get_device_name_max_count_cls": GetDeviceNameMaxCountV6ToV8,
                "set_device_name_cls": SetDeviceNameV6ToV8,
                "set_device_name_commit_cls": SetDeviceNameCommitV6ToV8,
                "set_device_extended_model_id_cls": SetDeviceExtendModelIdV6ToV8,
                "set_device_properties_cls": SetDevicePropertiesV6ToV8,
                "get_device_properties_cls": GetDevicePropertiesV6ToV8,
                "get_device_name_max_count_response_cls": GetDeviceNameMaxCountResponseV6ToV8,
                "set_device_name_response_cls": SetDeviceNameResponseV6ToV8,
                "set_device_name_commit_response_cls": SetDeviceNameCommitResponseV6ToV8,
                "set_device_extended_model_id_response_cls": SetDeviceExtendModelIdResponseV6ToV8,
                "set_device_properties_response_cls": SetDevicePropertiesResponseV6ToV8,
                "get_device_properties_response_cls": GetDevicePropertiesResponseV6ToV8,
        }
        cls.expected = {
                6: {
                        "cls": ConfigurableDevicePropertiesV6,
                        "interfaces": api_v6_to_v8,
                        "max_function_index": 5
                },
                7: {
                        "cls": ConfigurableDevicePropertiesV7,
                        "interfaces": api_v6_to_v8,
                        "max_function_index": 5
                },
                8: {
                        "cls": ConfigurableDevicePropertiesV8,
                        "interfaces": api_v6_to_v8,
                        "max_function_index": 5
                },
        }
    # end def setUpClass

    def test_configurable_device_properties_factory(self):
        """
        Tests ConfigurableDeviceProperties Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(ConfigurableDevicePropertiesFactory.create(version)), expected["cls"])
        # end for
    # end def test_configurable_device_properties_factory

    def test_configurable_device_properties_factory_version_out_of_range(self):
        """
        Tests ConfigurableDeviceProperties Factory with out of range versions
        """
        for version in [0, 5, 9]:
            with self.assertRaises(KeyError):
                ConfigurableDevicePropertiesFactory.create(version)
            # end with
        # end for
    # end def test_configurable_device_properties_factory_version_out_of_range

    def test_configurable_device_properties_factory_interfaces(self):
        """
        Check ConfigurableDeviceProperties Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            device_information = ConfigurableDevicePropertiesFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(device_information, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(device_information, interface)
                    # end with
                # end if
            # end for
        # end for
    # end def test_configurable_device_properties_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            device_information = ConfigurableDevicePropertiesFactory.create(version)
            self.assertEqual(device_information.get_max_function_index(), expected["max_function_index"])
        # end for
    # end def test_get_max_function_index
# end class ConfigurableDevicePropertiesTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
