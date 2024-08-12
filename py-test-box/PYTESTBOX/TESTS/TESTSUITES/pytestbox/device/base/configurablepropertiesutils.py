#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.configurablepropertiesutils
:brief: Helpers for ``ConfigurableProperties`` feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/10/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesFactory
from pyhid.hidpp.features.common.configurableproperties import GetPropertyInfoResponse as CPGetPropertyInfoResponse
from pyhid.hidpp.features.common.configurableproperties import ReadPropertyResponse as CPReadPropertyResponse
from pyhid.hidpp.features.common.propertyaccess import GetPropertyInfoResponse as PAGetPropertyInfoResponse
from pyhid.hidpp.features.common.propertyaccess import ReadPropertyResponse as PAReadPropertyResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.nvsparser import AddressBasedNvsParser
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurablePropertiesTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ConfigurableProperties`` feature
    """

    class ConfigurationHelper(object):
        """
        Configurable Properties configuration management helper
        """
        # These properties will be overridden in 0x0011 PropertyAccessUtils
        SUPPORTED_PROPERTIES = ConfigurationManager.ID.SUPPORTED_PROPERTIES
        SUPPORTED_PROPERTIES_SIZES = ConfigurationManager.ID.SPECIFIC_PROPERTIES_SIZES
        LIBRARY = ConfigurableProperties

        @classmethod
        def get_undefined_property_ids(cls, test_case):
            """
            Get Undefined property ids list

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Undefined property ids list
            :rtype:  ``list[int]``

            :raise ``NotImplementedError``: If the version is not yet implemented
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_PROPERTIES
            version = test_case.config_manager.get_feature_version(config)
            if version == ConfigurablePropertiesTestUtils.MessageChecker.Version.ZERO:
                property_id = ConfigurableProperties.PropertyIdV0
            elif version == ConfigurablePropertiesTestUtils.MessageChecker.Version.ONE:
                property_id = ConfigurableProperties.PropertyIdV1
            elif version == ConfigurablePropertiesTestUtils.MessageChecker.Version.TWO:
                property_id = ConfigurableProperties.PropertyIdV2
            elif version == ConfigurablePropertiesTestUtils.MessageChecker.Version.THREE:
                property_id = ConfigurableProperties.PropertyIdV3
            elif version == ConfigurablePropertiesTestUtils.MessageChecker.Version.FOUR:
                property_id = ConfigurableProperties.PropertyIdV4
            else:
                raise NotImplementedError(f"Version {version} is not implemented")
            # end if

            return [
                property_id.RESERVED_1,
                property_id.RESERVED_2,
                *range(property_id.RESERVED_RANGE_1_START, property_id.RESERVED_RANGE_1_END + 1),
                *range(property_id.RESERVED_RANGE_2_START, property_id.RESERVED_RANGE_2_END + 1)
            ]
        # end def get_undefined_property_ids

        @classmethod
        def is_supported(cls, test_case, property_id):
            """
            Check if a property is supported

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``

            :return: Flag indicating that a property is supported
            :rtype: ``bool``
            """
            return property_id in test_case.config_manager.get_feature(cls.SUPPORTED_PROPERTIES)
        # end def is_supported

        @classmethod
        def get_sizes(cls, test_case):
            """
            Get all the sizes of all supported properties from the device test settings if available else from the
            default value list

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Property sizes
            :rtype: ``dict[ConfigurableProperties.PropertyId, int]``
            """
            properties = test_case.config_manager.get_feature(cls.SUPPORTED_PROPERTIES)
            prop_sizes = test_case.config_manager.get_feature(cls.SUPPORTED_PROPERTIES_SIZES)
            return {prop: (prop_sizes[prop] if prop in prop_sizes else
                           int(getattr(cls.LIBRARY.PropertyDefaultSize,
                                       cls.LIBRARY.PropertyId(prop).name,
                                       0))
                           ) for prop in properties}
        # end def get_sizes

        @classmethod
        def get_size(cls, test_case, property_id):
            """
            Get the property size from the device test settings if available else from the default value list

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``

            :return: Property size
            :rtype: ``int``
            """
            prop_sizes = cls.get_sizes(test_case)
            return prop_sizes[property_id] if property_id in prop_sizes else 0
        # end def get_size

        @classmethod
        def get_first_supported_property(cls, test_case, min_size=0, skip_properties=None):
            """
            Get first supported property matching the size requirement

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param min_size: Minimum property size required - OPTIONAL
            :type min_size: ``int``
            :param skip_properties: Properties not wanted for selection - OPTIONAL
            :type skip_properties: ``list[int] | None``

            :return: Property id and size
            :rtype: ``tuple[ConfigurableProperties.PropertyId, int]``

            :raise ``ValueError``: Assert the size requirement which raises error
            """
            skip_properties = [] if skip_properties is None else skip_properties
            properties = [prop for prop in
                          test_case.config_manager.get_feature(cls.SUPPORTED_PROPERTIES)
                          if prop not in skip_properties]
            assert len(properties) > 0, f'No property left after skipping the provided list {skip_properties})'
            for property_id in properties:
                property_size = cls.get_size(test_case, property_id)
                if property_size >= min_size:
                    return property_id, property_size
                # end if
            # end for
            raise ValueError(f'No property matches the size requirement ({min_size})')
        # end def get_first_supported_property

        @classmethod
        def get_first_property_not_supported(cls, test_case):
            """
            Get first not supported property

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Property id not supported
            :rtype: ``ConfigurableProperties.PropertyId``

            :raise ``ValueError``: Assert the property requirement which raises error
            """
            for prop_id in range(cls.LIBRARY.PropertyId.MIN, cls.LIBRARY.PropertyId.MAX + 1):
                if prop_id not in test_case.config_manager.get_feature(cls.SUPPORTED_PROPERTIES) \
                        and prop_id not in cls.get_undefined_property_ids(test_case=test_case):
                    return prop_id
                # end if
            # end for
            raise ValueError(f'All known properties are supported')
        # end def get_first_property_not_supported
    # end class ConfigurationHelper

    class FlagsMaskBitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FlagsMaskBitMap``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "corrupted": (cls.check_corrupted, 0),
                "present": (cls.check_present, 0),
                "supported": (cls.check_supported, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: FlagsMaskBitMap to check
            :type bitmap: ``ConfigurableProperties.FlagsMaskBitMap``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_corrupted(test_case, bitmap, expected):
            """
            Check corrupted field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: FlagsMaskBitMap to check
            :type bitmap: ``ConfigurableProperties.FlagsMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert corrupted that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The corrupted shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.corrupted),
                msg="The corrupted parameter differs from the one expected")
        # end def check_corrupted

        @staticmethod
        def check_present(test_case, bitmap, expected):
            """
            Check present field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: FlagsMaskBitMap to check
            :type bitmap: ``ConfigurableProperties.FlagsMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert present that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The present shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.present),
                msg="The present parameter differs from the one expected")
        # end def check_present

        @staticmethod
        def check_supported(test_case, bitmap, expected):
            """
            Check supported field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: FlagsMaskBitMap to check
            :type bitmap: ``ConfigurableProperties.FlagsMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert supported that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The supported shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.supported),
                msg="The supported parameter differs from the one expected")
        # end def check_supported
    # end class FlagsMaskBitMapChecker

    class GetPropertyInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetPropertyInfoResponse``
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "flags": (cls.check_flags,
                          ConfigurablePropertiesTestUtils.FlagsMaskBitMapChecker.get_default_check_map(test_case)),
                "size": (cls.check_size, None)
            }
        # end def get_default_check_map

        @classmethod
        def get_check_map_by_property(cls, test_case, property_id):
            """
            Get the default check methods and expected values for the ``GetPropertyInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``

            :return: Check map for given property identifier
            :rtype: ``dict``
            """
            if ConfigurablePropertiesTestUtils.ConfigurationHelper.is_supported(test_case, property_id):
                size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(test_case, property_id)
                supported = True
                prop = ConfigurableProperties.PropertyId
                if ProtocolManagerUtils.is_corded_device_only(test_case=test_case):
                     # There is no 0x1807 settings in the NVS due to corded devices didn't do test_node_setup().
                    present = False
                else:
                    present = property_id in (prop.RGB_LED_BIN_INFORMATION_ZONE0,
                                              prop.RGB_LED_BIN_INFORMATION_ZONE1,
                                              prop.RGB_LED_BIN_INFORMATION_ZONE2,
                                              prop.RGB_LED_BIN_INFORMATION_ZONE3,
                                              prop.RGB_LED_BIN_INFORMATION_ZONE4)
                # end if
            else:
                size = 0
                supported = False
                present = False
            # end if

            checker = ConfigurablePropertiesTestUtils.FlagsMaskBitMapChecker
            flags = checker.get_default_check_map(test_case)
            flags.update({
                "present": (checker.check_present, present),
                "supported": (checker.check_supported, supported)
            })
            check_map = cls.get_default_check_map(test_case)
            check_map.update({
                "flags": (cls.check_flags, flags),
                "size": (cls.check_size, size)
            })
            return check_map
        # end def get_check_map_by_property

        @staticmethod
        def check_flags(test_case, message, expected):
            """
            Check ``flags``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetPropertyInfoResponse to check
            :type message: ``pyhid.hidpp.features.common.configurableproperties.GetPropertyInfoResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ConfigurablePropertiesTestUtils.FlagsMaskBitMapChecker.check_fields(
                test_case, message.flags, ConfigurableProperties.FlagsMaskBitMap, expected)
        # end def check_flags

        @staticmethod
        def check_size(test_case, response, expected):
            """
            Check size field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetPropertyInfoResponse to check
            :type response: ``pyhid.hidpp.features.common.configurableproperties.GetPropertyInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert size that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The size shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.size),
                msg="The size parameter differs from the one expected")
        # end def check_size
    # end class GetPropertyInfoResponseChecker

    class ReadPropertyResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadPropertyResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "data": (cls.check_data, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ReadPropertyResponse to check
            :type response: ``pyhid.hidpp.features.common.configurableproperties.ReadPropertyResponse``
            :param expected: Expected value
            :type expected: ``HexList | int``

            :raise ``AssertionError``: Assert data that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The data shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(Numeral(expected)),
                obtained=HexList(response.data),
                msg="The data parameter differs from the one expected")
        # end def check_data
    # end class ReadPropertyResponseChecker

    class CommonNvsHelper(DeviceBaseTestUtils.NvsHelper):
        # See ``DeviceBaseTestUtils.NvsHelper``
        # TODO : To be completed
        prop = ConfigurableProperties.PropertyId
        property_chunk_name_map = {
            prop.EXTENDED_MODEL_ID: 'NVS_EXTENDED_MODEL_ID',
            prop.KEYBOARD_LAYOUT: 'NVS_KEYBOARD_INTERNATIONAL_LAYOUT_ID',
            prop.RGB_LED_BIN_INFORMATION_ZONE0: 'NVS_RGB_LEDBIN_BACKUP_ZONE0_ID',
            prop.RGB_LED_BIN_INFORMATION_ZONE1: 'NVS_RGB_LEDBIN_BACKUP_ZONE1_ID',
            prop.EQUAD_DEVICE_NAME: 'NVS_EQUAD_SHORT_NAME_ID',
            prop.BLE_GAP_ADV_SERVICE_DATA: None,
            prop.BLE_GAP_ADV_OUTPUT_POWER: 'NVS_BLE_AD_OUTPUT_POWER_ID',
            prop.RGB_LED_BIN_INFORMATION_ZONE2: 'NVS_RGB_LEDBIN_BACKUP_ZONE2_ID',
            prop.SERIAL_NUMBER: 'NVS_SERIAL_NUMBER_ID',
            prop.CAR_SIMULATOR_PEDALS_TYPES: 'NVS_EXT_PEDAL_SIGNATURE_ID',
            prop.RGB_LED_ZONE_INTENSITY: None,
            prop.RGB_LED_DRIVER_ID: None,
            prop.HIDPP_DEVICE_NAME: 'NVS_DEVICE_NAME_ID',
            prop.EQUAD_ID: "NVS_EQUAD_ID_ID",
            prop.USB_VID: "NVS_USB_VID_ID",
            prop.USB_BL_PID: "NVS_USB_BTLDR_PID_ID",
            prop.USB_APP_PID: "NVS_USB_APP_PID_ID",
            prop.USB_MANUFACTURER_STRING: "NVS_USB_MANUF_STRG_ID",
            prop.USB_BL_PRODUCT_STRING: "NVS_USB_BTLDR_PROD_STRG_ID",
            prop.USB_APP_PRODUCT_STRING: "NVS_USB_APP_PROD_STRG_ID",
            prop.BLE_GAP_BL_NAME: None,
            prop.BLE_GAP_APP_NAME: "NVS_BLE_GAP_APP_NAME_ID",
            prop.BLE_GAP_BL_ADV_NAME_SIZE: "NVS_BLE_GAP_BL_ADV_NAME_SIZE_ID",
            prop.BLE_GAP_APP_ADV_NAME_SIZE: "NVS_BLE_GAP_APP_ADV_NAME_SIZE_ID",
            prop.BLE_GAP_BL_SR_NAME_SIZE: "NVS_BLE_GAP_BL_SR_NAME_SIZE_ID",
            prop.BLE_GAP_APP_SR_NAME_SIZE: "NVS_BLE_GAP_APP_SR_NAME_SIZE_ID",
            prop.BLE_DIS_VID: "NVS_BLE_DIS_VID_ID",
            prop.BLE_DIS_BL_PID: "NVS_BLE_DIS_BTLDR_PID_ID",
            prop.BLE_DIS_APP_PID: "NVS_BLE_DIS_APP_PID_ID",
            prop.BLE_DIS_MANUFACTURER_NAME: "NVS_BLE_DIS_MANUF_NAME_ID",
            prop.BLE_DIS_BL_MODEL_NUMBER: "NVS_BLE_DIS_BTLDR_MODEL_NB_ID",
            prop.BLE_DIS_APP_MODEL_NUMBER: "NVS_BLE_DIS_APP_MODEL_NB_ID",
            prop.HW_VERSION: "NVS_HW_VERSION_ID",
            prop.SOFTWARE_EXTRA_INFORMATION: "NVS_SW_EXTRA_INFO_ID",
            prop.PART_NUMBER: "NVS_PART_NUMBER_ID",
            prop.REGULATORY_MODEL_NUMBER: "NVS_REGULATORY_MODEL_NUMBER_ID",
            prop.RGB_LED_BIN_INFORMATION_ZONE3: "NVS_RGB_LEDBIN_BACKUP_ZONE3_ID",
            prop.RGB_LED_BIN_INFORMATION_ZONE4: "NVS_RGB_LEDBIN_BACKUP_ZONE4_ID",
            prop.DISABLE_EASY_PAIRING: "NVS_DISABLE_EASY_PAIRING_ID"
        }

        @classmethod
        def read_property_id(cls, test_case, property_id):
            """
            Get the last chunk in NVS matching the given property id

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``

            :return: Last chunk matching property id
            :rtype: ``pylibrary.tools.nvsparser.NvsChunk``
            """
            test_case.memory_manager.read_nvs()
            chunk_name = cls.property_chunk_name_map[property_id]
            chunks = test_case.memory_manager.nvs_parser.get_chunk_history(chunk_name)
            return chunks[-1].clear_data if len(chunks) > 0 else None
        # end def read_property_id

        @classmethod
        def get_chunk_id(cls, test_case, property_id):
            """
            Get chunk id corresponding to a property id

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``

            :return: Chunk id matching the given property id
            :rtype: ``int``
            """
            chunk_id = test_case.memory_manager.nvs_parser.chunk_id_map[cls.property_chunk_name_map[property_id]]
            return chunk_id[0] if isinstance(chunk_id, list) else chunk_id
        # end def get_chunk_id

        @classmethod
        def write_property_id(cls, test_case, property_id, data):
            """
            Write a new chunk in NVS matching the given property id

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param data: Property data
            :type data: ``HexList``

            :raise ``AssertionError``: Assert size that raises an error
            """
            size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(test_case, property_id)
            data = HexList(data)
            assert len(data) == size, f'Provided data ({data}) does not match the expected size ({size})'
            if test_case.memory_manager is not None:
                test_case.memory_manager.read_nvs()
                chunk_name = cls.property_chunk_name_map[property_id]
                test_case.memory_manager.nvs_parser.add_new_chunk(chunk_id=chunk_name, data=data)
                ConfigurablePropertiesTestUtils.load_nvs(test_case=test_case)
            # end if
        # end def write_property_id

        @classmethod
        def invalidate_chunk(cls, test_case, property_id):
            """
            Invalidate the chunk in NVS matching the given property id

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            """
            chunk_name = cls.property_chunk_name_map[property_id]
            test_case.memory_manager.read_nvs()
            invalidated_chunk_count = test_case.memory_manager.invalidate_chunks(chunk_names=[chunk_name])
            if invalidated_chunk_count > 0:
                test_case.memory_manager.load_nvs()
            # end if
        # end def invalidate_chunk
    # end class CommonNvsHelper

    class NvsHelper(CommonNvsHelper):
        # See ``CommonNvsHelper``
        @classmethod
        def check_new_chunks_after_write_data(cls, test_case, initial_parser, final_parser, property_id, expected_data):
            """
            Check new chunks after writing a property with multiple write property requests. A chunk should have been
            written after each write request.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param initial_parser: First NVS Parser
            :type initial_parser: ``pylibrary.tools.nvsparser.NvsParser``
            :param final_parser: Second NVS Parser
            :type final_parser: ``pylibrary.tools.nvsparser.NvsParser``
            :param property_id: Property id
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param expected_data: Expected chunk data
            :type expected_data: ``HexList``
            """
            _, feature_1807, _, _ = ConfigurablePropertiesTestUtils.HIDppHelper.get_parameters(test_case)
            expected_chunks_data = []
            CHUNK_ADDRESS_MASK = 0xFFF if isinstance(initial_parser, AddressBasedNvsParser) else 0xFF
            if isinstance(final_parser, AddressBasedNvsParser):
                # Address Based NVS would have a single chunk with all the data
                expected_chunks_data = [expected_data]
            else:
                data_field_len = feature_1807.write_property_cls.LEN.DATA // 8
                d, m = divmod(len(expected_data), data_field_len)
                for index in range(d):
                    pos = index * data_field_len
                    expected_chunks_data.append(expected_data[pos:pos + data_field_len])
                # end for
                if m > 0:
                    pos = d * data_field_len
                    expected_chunks_data.append(expected_data[pos:])
                # end if

                for index in range(1, len(expected_chunks_data)):
                    expected_chunks_data[index] = expected_chunks_data[index - 1] + expected_chunks_data[index]
                # end for

                for data in expected_chunks_data:
                    data.addPadding(ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(test_case, property_id),
                                    fromLeft=False)
                # end for
            # end if

            expected_chunks_ids = ([cls.get_chunk_id(test_case, property_id) & CHUNK_ADDRESS_MASK]
                                   * len(expected_chunks_data))

            ConfigurablePropertiesTestUtils.NvsHelper.check_new_chunks(
                test_case, initial_parser, final_parser,
                expected_chunks_ids, expected_chunks_data)
        # end def check_new_chunks_after_write_data
    # end class NvsHelper

    class CommonHIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=None,
                           factory=None,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_property_info(cls, test_case, property_id, device_index=None, port_index=None, software_id=None,
                              padding=None):
            """
            Process ``GetPropertyInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetPropertyInfoResponse
            :rtype: ``CPGetPropertyInfoResponse | PAGetPropertyInfoResponse``
            """
            feature_index, feature, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature.get_property_info_cls(
                device_index=device_index,
                feature_index=feature_index,
                property_id=HexList(property_id))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature.get_property_info_response_cls)
        # end def get_property_info

        @classmethod
        def get_property_info_and_check_error(
                cls, test_case, error_codes, property_id, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetPropertyInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_index, feature, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature.get_property_info_cls(
                device_index=device_index,
                feature_index=feature_index,
                property_id=HexList(property_id))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_property_info_and_check_error

        @classmethod
        def read_property(cls, test_case, device_index=None, port_index=None,  software_id=None, padding=None):
            """
            Process ``ReadProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReadPropertyResponse
            :rtype: ``CPReadPropertyResponse | PAReadPropertyResponse``
            """
            feature_index, feature, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature.read_property_cls(
                device_index=device_index,
                feature_index=feature_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature.read_property_response_cls)
        # end def read_property

        @classmethod
        def read_property_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``ReadProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_index, feature, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature.read_property_cls(
                device_index=device_index,
                feature_index=feature_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def read_property_and_check_error

        @classmethod
        def read_data(cls, test_case, data_size):
            """
            Read property data longer than a single read request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param data_size: Data size to read
            :type data_size: ``int``

            :return: Property data
            :rtype: ``HexList``
            """
            data = HexList()
            _, feature_id, _, _ = cls.get_parameters(test_case)
            data_field_len = feature_id.read_property_response_cls.LEN.DATA // 8
            d, m = divmod(data_size, data_field_len)
            for _ in range(d):
                data += cls.read_property(test_case).data
            # end for
            if m > 0:
                new_data = cls.read_property(test_case).data
                new_data.addPadding(data_field_len, fromLeft=False)
                data += new_data
            # end if
            data = data[:data_size]
            return data
        # end def read_data
    # end class CommonHIDppHelper

    class HIDppHelper(CommonHIDppHelper):
        # See ``CommonHIDppHelper``
        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=ConfigurableProperties.FEATURE_ID,
                           factory=ConfigurablePropertiesFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def select_property(cls, test_case, property_id, rd_offset=0, wr_offset=0, device_index=None, port_index=None,
                            software_id=None, padding=None):
            """
            Process ``SelectProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier [1 to 255] or 0 to deselect all properties.
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param rd_offset: Property read offset in bytes - OPTIONAL
            :type rd_offset: ``int | HexList``
            :param wr_offset: Property write offset in bytes - OPTIONAL
            :type wr_offset: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SelectPropertyResponse
            :rtype: ``pyhid.hidpp.features.common.configurableproperties.SelectPropertyResponse``
            """
            feature_1807_index, feature_1807, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1807.select_property_cls(
                device_index=device_index,
                feature_index=feature_1807_index,
                property_id=HexList(property_id),
                rd_offset=rd_offset,
                wr_offset=wr_offset)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1807.select_property_response_cls)
        # end def select_property

        @classmethod
        def select_property_and_check_error(
                cls, test_case, error_codes, property_id, rd_offset=0, wr_offset=0, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SelectProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param property_id: Property identifier [1 to 255] or 0 to deselect all properties.
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param rd_offset: Property read offset in bytes - OPTIONAL
            :type rd_offset: ``int | HexList``
            :param wr_offset: Property write offset in bytes - OPTIONAL
            :type wr_offset: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: SelectPropertyResponse
            :rtype: ``pyhid.hidpp.features.common.configurableproperties.SelectPropertyResponse``
            """
            feature_1807_index, feature_1807, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1807.select_property_cls(
                device_index=device_index,
                feature_index=feature_1807_index,
                property_id=HexList(property_id),
                rd_offset=rd_offset,
                wr_offset=wr_offset)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def select_property_and_check_error

        @classmethod
        def write_property(cls, test_case, data, device_index=None, port_index=None, software_id=None):
            """
            Process ``WriteProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param data: Property data
            :type data: ``HexList | int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: WritePropertyResponse
            :rtype: ``pyhid.hidpp.features.common.configurableproperties.WritePropertyResponse``
            """
            feature_1807_index, feature_1807, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1807.write_property_cls(
                device_index=device_index,
                feature_index=feature_1807_index,
                data=HexList(data))

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1807.write_property_response_cls)
        # end def write_property

        @classmethod
        def write_property_and_check_error(
                cls, test_case, error_codes, data, device_index=None, port_index=None, function_index=None):
            """
            Process ``WriteProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param data: Property data
            :type data: ``HexList | int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``

            :return: WritePropertyResponse
            :rtype: ``pyhid.hidpp.features.common.configurableproperties.WritePropertyResponse``
            """
            feature_1807_index, feature_1807, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1807.write_property_cls(
                device_index=device_index,
                feature_index=feature_1807_index,
                data=HexList(data))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def write_property_and_check_error

        @classmethod
        def delete_property(cls, test_case, property_id, device_index=None, port_index=None, software_id=None,
                            padding=None):
            """
            Process ``DeleteProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: DeletePropertyResponse
            :rtype: ``pyhid.hidpp.features.common.configurableproperties.DeletePropertyResponse``
            """
            feature_1807_index, feature_1807, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1807.delete_property_cls(
                device_index=device_index,
                feature_index=feature_1807_index,
                property_id=HexList(property_id))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1807.delete_property_response_cls)
        # end def delete_property

        @classmethod
        def delete_property_and_check_error(
                cls, test_case, error_codes, property_id, device_index=None, port_index=None, function_index=None):
            """
            Process ``DeleteProperty``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``

            :return: DeletePropertyResponse
            :rtype: ``pyhid.hidpp.features.common.configurableproperties.DeletePropertyResponse``
            """
            feature_1807_index, feature_1807, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1807.delete_property_cls(
                device_index=device_index,
                feature_index=feature_1807_index,
                property_id=HexList(property_id))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def delete_property_and_check_error

        @classmethod
        def write_data(cls, test_case, data):
            """
            Write property data longer than a single write request

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param data: Property data
            :type data: ``HexList | int``

            :return: List of responses
            :rtype: ``list[pyhid.hidpp.features.common.configurableproperties.WritePropertyResponse]``
            """
            _, feature_1807, _, _ = cls.get_parameters(test_case)
            data = HexList(data)
            data_field_len = feature_1807.write_property_cls.LEN.DATA // 8
            d, m = divmod(len(data), data_field_len)
            responses = []
            for index in range(d):
                pos = index * data_field_len
                responses.append(cls.write_property(test_case, data[pos:pos + data_field_len]))
            # end for
            if m > 0:
                pos = d * data_field_len
                data = data[pos:]
                data.addPadding(size=data_field_len, fromLeft=False)
                responses.append(cls.write_property(test_case, data))
            # end if
            return responses
        # end def write_data

        @classmethod
        def is_present(cls, test_case, property_id, device_index=None, port_index=None):
            """
            Check if a property is present

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param property_id: Property identifier
            :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: True if property is present
            :rtype: ``bool``
            """
            property_info = cls.get_property_info(test_case, property_id, device_index, port_index)
            return ConfigurableProperties.FlagsMaskBitMap(property_info.flags).present
        # end def is_present

        @classmethod
        def search_present(cls, test_case, present=True, min_size=0, skip_properties=None, device_index=None,
                           port_index=None):
            """
            Search the first property matching the presence and size requirements

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param present: Flag to indicate whether property should be present - OPTIONAL
            :type present: ``bool``
            :param min_size: Minimum property size required - OPTIONAL
            :type min_size: ``int``
            :param skip_properties: Properties not wanted for selection - OPTIONAL
            :type skip_properties: ``list | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: Property id or None if no match
            :rtype: ``ConfigurableProperties.PropertyId | None``
            """
            skip_properties = [] if skip_properties is None else skip_properties
            properties = [prop for prop in
                          test_case.config_manager.get_feature(ConfigurationManager.ID.SUPPORTED_PROPERTIES)
                          if prop not in skip_properties]

            for property_id in properties:
                # Check property size first because it's faster, no need to send requests if size doesn't match
                property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(test_case, property_id)
                if property_size >= min_size:
                    is_present = cls.is_present(test_case, property_id, device_index, port_index)
                    if (is_present and present) or (not is_present and not present):
                        return property_id
                    # end if
                # end if
            # end for
        # end def search_present

        @classmethod
        def get_first_property_present(cls, test_case, present=True, min_size=0, skip_properties=None,
                                       write_data_if_none=None, device_index=None, port_index=None):
            """
            Get the first property matching the presence and size requirements. If no property is found at first
            search, write the first supported one.

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param present: Flag to indicate whether property should be present - OPTIONAL
            :type present: ``bool``
            :param min_size: Minimum property size required - OPTIONAL
            :type min_size: ``int``
            :param skip_properties: Properties not wanted for selection - OPTIONAL
            :type skip_properties: ``list | None``
            :param write_data_if_none: Data to write if a property has to be written - OPTIONAL
            :type write_data_if_none: ``int | None`` - OPTIONAL
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``

            :return: Property id
            :rtype: ``ConfigurableProperties.PropertyId``
            """
            property_id = cls.search_present(test_case, present, min_size, skip_properties, device_index, port_index)
            if property_id is not None:
                return property_id
            # end if
            property_id, property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.\
                get_first_supported_property(test_case, min_size, skip_properties)
            test_case.post_requisite_reload_nvs = True
            if present:
                cls.select_property(test_case, property_id)
                if write_data_if_none is None:
                    write_data_if_none = HexList("00")
                else:
                    write_data_if_none = HexList(write_data_if_none)
                # end if
                cls.write_data(test_case, write_data_if_none)
            else:
                cls.delete_property(test_case, property_id)
            # end if
            return property_id
        # end def get_first_property_present
    # end class HIDppHelper

    @classmethod
    def check_property(cls, test_case, property_id, data, hidpp_check=True, nvs_check=True):
        """
        Check Property in HID++ read response and in NVS

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param property_id: Property identifier
        :type property_id: ``ConfigurableProperties.PropertyId | int | HexList``
        :param data: Expected data
        :type data: ``HexList``
        :param hidpp_check: Enable check by HID++ read request - OPTIONAL
        :type hidpp_check: ``bool``
        :param nvs_check: Enable NVS check - OPTIONAL
        :type nvs_check: ``bool``

        :raise ``AssertionError``: Assert the parameter presence that raises an error
        """
        assert (hidpp_check is True or nvs_check is True), \
            f'At least, one of these 2 options shall be True (hidpp_check is {hidpp_check} ' \
            f'and nvs_check is {nvs_check})'

        if hidpp_check:
            cls.HIDppHelper.select_property(test_case, property_id)
            property_data = cls.HIDppHelper.read_data(test_case, len(data))
            test_case.assertEqual(expected=data, obtained=property_data, msg='Read data should match expected data')
        # end if

        if nvs_check:
            data_size = cls.ConfigurationHelper.get_size(test_case, ConfigurableProperties.PropertyId(property_id))
            property_data = HexList(cls.NvsHelper.read_property_id(test_case, property_id))[:data_size]
            test_case.assertEqual(expected=data, obtained=property_data, msg='Data in NVS should match expected data')
        # end if
    # end def check_property
# end class ConfigurablePropertiesTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
