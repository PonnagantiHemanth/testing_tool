#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.hidpp20.common.feature_1807.functionality
:brief: HID++ 2.0 ``ConfigurableProperties`` functionality test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from random import choices
from random import randint
from string import ascii_uppercase
from string import digits

from math import ceil

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils as Utils
from pytestbox.device.hidpp20.common.feature_1807.configurableproperties import ConfigurablePropertiesTestCase
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class ConfigurablePropertiesFunctionalityTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` functionality test cases
    """

    @features("Feature1807")
    @level("Functionality")
    def test_supported_properties(self):
        """
        Check supported properties in DUT matches expected supported properties in configuration list
        Sending GetPropertyInfo with a propertyId not supported by the DUT should return a null flags value.
        And supported flag should be set if a property is supported by the DUT.
        """
        for property_id in range(ConfigurableProperties.PropertyId.MIN, ConfigurableProperties.PropertyId.MAX + 1):
            repr_prop_id = repr(ConfigurableProperties.PropertyId(property_id)) if property_id not in \
                    Utils.ConfigurationHelper.get_undefined_property_ids(self) else property_id
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Get property {repr_prop_id} info")
            # ----------------------------------------------------------------------------------------------------------
            property_info_response = Utils.HIDppHelper.get_property_info(self, property_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            checker = Utils.GetPropertyInfoResponseChecker
            check_map = checker.get_check_map_by_property(self, property_id=property_id)
            checker.check_fields(
                self, property_info_response, self.feature_1807.get_property_info_response_cls, check_map=check_map)
        # end for

        self.testCaseChecked("FUN_1807_0004", _AUTHOR)
        self.testCaseChecked("ROB_1807_0004", _AUTHOR)
    # end def test_supported_properties

    @features("Feature1807")
    @features('Feature1802')
    @level("Functionality")
    @services('Debugger')
    def test_property_persistent_to_hidpp_reset(self):
        """
        Goal: Check the new property value is immediately committed to non-volatile storage when calling the
        WriteProperty function and is persistent to a reset done with the following reset methods:
         - using the HID++ ForceReset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device with HID++")
        # --------------------------------------------------------------------------------------------------------------
        Utils.ResetHelper.hidpp_reset(self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, property_id, test_data)

        self.testCaseChecked("FUN_1807_0005#1", _AUTHOR)
    # end def test_property_persistent_to_hidpp_reset

    @features("Feature1807")
    @level("Functionality")
    @services('PowerSwitch')
    @services('Debugger')
    def test_property_persistent_to_hw_reset(self):
        """
        Goal: Check the new property value is immediately committed to non-volatile storage when calling the
        WriteProperty function and is persistent to a reset done with the following reset methods:
         - using Power Slider
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device with Power Slider")
        # --------------------------------------------------------------------------------------------------------------
        Utils.ResetHelper.power_switch_reset(self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, property_id, test_data)

        self.testCaseChecked("FUN_1807_0005#2", _AUTHOR)
    # end def test_property_persistent_to_hw_reset

    @features("Feature1807")
    @level("Functionality")
    @services('PowerSupply')
    @services('Debugger')
    def test_property_persistent_to_pwr_reset(self):
        """
        Goal: Check the new property value is immediately committed to non-volatile storage when calling the
        WriteProperty function and is persistent to a reset done with the following reset methods:
         - using Power Supply
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset device with Power Supply")
        # --------------------------------------------------------------------------------------------------------------
        Utils.ResetHelper.power_supply_reset(self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, property_id, test_data)

        self.testCaseChecked("FUN_1807_0005#3", _AUTHOR)
    # end def test_property_persistent_to_pwr_reset

    @features("Feature1807")
    @features("BLEProProtocol")
    @level("Functionality")
    @services('Debugger')
    def test_property_persistent_to_disconnection(self):
        """
        Goal: Check the new property value is immediately committed to non-volatile storage when calling the
        WriteProperty function and is persistent to a disconnection.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset receiver to disconnect and reconnect")
        # --------------------------------------------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)
        ReceiverTestUtils.reset_receiver(self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, property_id, test_data)

        self.testCaseChecked("FUN_1807_0006", _AUTHOR)
    # end def test_property_persistent_to_disconnection

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_ignore_after_max_size(self):
        """
        Goal: Check that if the maximum size is reached, the remaining bytes are ignored.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = Utils.ConfigurationHelper.get_first_supported_property(self)
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))
        longer_test_data = HexList(test_data + HexList("55"))

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, longer_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check new chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        final_parser = self.memory_manager.nvs_parser
        Utils.NvsHelper.check_new_chunks_after_write_data(self, initial_parser, final_parser, property_id, test_data)

        self.testCaseChecked("FUN_1807_0007", _AUTHOR)
    # end def test_ignore_after_max_size

    @features("Feature1807")
    @features("NoFeature1807FilterUnstableTest")
    @level("Functionality")
    @services('Debugger')
    def test_keep_unmodified_out_of_write_request_before_offset(self):
        """
        Goal: Check that all bytes except the ones included in the WriteProperty request are kept unmodified.
        Loop over all offset value from 0 to GetPropertyInfo.size - 1:
        - Initialize all bytes to 0x00 then send writeProperty with data full of 0xFF
        - Initialize all bytes to 0xFF then send writeProperty with data full of 0x00
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported with a minimum size of 2 bytes")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(
            self, min_size=2, skip_properties=[ConfigurableProperties.PropertyId.SERIAL_NUMBER,
                                               ConfigurableProperties.PropertyId.HIDPP_DEVICE_NAME,
                                               # RGB LED Information may be configured (in test node setup),
                                               # so it is better not to use them for this test
                                               ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0,
                                               ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1,
                                               ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2,
                                               ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3,
                                               ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4
                                               ])

        self.post_requisite_reload_nvs = True
        # Limit the number of values to test to reduce test duration
        offset_test_values = list(range(property_size - 1, -1, -1))
        while len(offset_test_values) > 5:
            offset_test_values.pop(randint(1, len(offset_test_values) - 2))
        # end while
        for init_pattern in [HexList("00"), HexList("FF")]:
            for offset in offset_test_values:
                init_data = HexList(init_pattern) * property_size

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Select property {repr(property_id)} (offset = 0)")
                # ------------------------------------------------------------------------------------------------------
                Utils.HIDppHelper.select_property(self, property_id)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write property {repr(property_id)} with data = {init_data}")
                # ------------------------------------------------------------------------------------------------------
                Utils.HIDppHelper.write_data(self, init_data)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                Utils.check_property(self, property_id, HexList(init_data))

                test_data = (init_pattern ^ HexList("FF")) * (property_size - offset)

                initial_parser = self._get_initial_parser(log=False)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Select property {repr(property_id)} (offset = {offset})")
                # ------------------------------------------------------------------------------------------------------
                Utils.HIDppHelper.select_property(self, property_id, wr_offset=offset)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Write property {repr(property_id)} with data = {test_data}")
                # ------------------------------------------------------------------------------------------------------
                write_responses = Utils.HIDppHelper.write_data(self, test_data)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check property {repr(property_id)}")
                # ------------------------------------------------------------------------------------------------------
                expected_data = init_data[:offset] + test_data
                Utils.check_property(self, property_id, expected_data)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check new chunk in NVS")
                # ------------------------------------------------------------------------------------------------------
                final_parser = self.memory_manager.nvs_parser
                data_field_len = self.feature_1807.write_property_cls.LEN.DATA // 8
                expected_chunks_data = []
                n = 0
                while n < len(write_responses):
                    expected_chunks_data.append(expected_data[:offset + (n + 1) * data_field_len]
                                                + init_data[offset + (n + 1) * data_field_len:])
                    n += 1
                # end while
                Utils.NvsHelper.check_new_chunks(
                    test_case=self,
                    nvs_parser_1=initial_parser,
                    nvs_parser_2=final_parser,
                    expected_chunks_ids=[Utils.NvsHelper.get_chunk_id(self, property_id) & 0xFF] * len(write_responses),
                    expected_chunks_data=expected_chunks_data)
            # end for
        # end for
        self.testCaseChecked("FUN_1807_0008#1", _AUTHOR)
    # end def test_keep_unmodified_out_of_write_request_before_offset

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_init_out_of_write_request_before_offset(self):
        """
        Goal: Check that if a property does not exist, it is created and all other bytes are initialized to 0:
            Write only the last byte of the property then check all bytes except the last one are 0
        """
        test_data = HexList("FF")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present with a minimum size of 2 bytes")
        # --------------------------------------------------------------------------------------------------------------
        property_id = Utils.HIDppHelper.get_first_property_present(
            self,
            present=False,
            min_size=2,
            skip_properties=[
                # Serial Number format has to be respected, so it is better not to use it for this test
                ConfigurableProperties.PropertyId.SERIAL_NUMBER,
                # RGB LED Information may be configured (in test node setup), so it is better not to use them
                ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE0,
                ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE1,
                ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE2,
                ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE3,
                ConfigurableProperties.PropertyId.RGB_LED_BIN_INFORMATION_ZONE4
            ]
        )
        property_size = Utils.ConfigurationHelper.get_size(self, property_id)

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id, wr_offset=property_size - 1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        expected_data = HexList("00" * (property_size - 1)) + test_data
        Utils.check_property(self, property_id, HexList(expected_data))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check new chunk in NVS")
        # --------------------------------------------------------------------------------------------------------------
        final_parser = self.memory_manager.nvs_parser
        Utils.NvsHelper.check_new_chunks(self,
                                         initial_parser,
                                         final_parser,
                                         [Utils.NvsHelper.get_chunk_id(self, property_id) & 0xFF],
                                         [expected_data])

        self.testCaseChecked("FUN_1807_0009#1", _AUTHOR)
    # end def test_init_out_of_write_request_before_offset

    @features("Feature1807")
    @level("Functionality")
    def test_deselect_property(self):
        """
        Goal: Check SelectProperty with propertyId = 0 deselect the current property.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = Utils.ConfigurationHelper.get_first_supported_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Call Select property with property_id = {repr(ConfigurableProperties.PropertyId.DESELECT_ALL)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, ConfigurableProperties.PropertyId.DESELECT_ALL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Check Hid++ 2.0 Error Code {Hidpp2ErrorCodes.NOT_ALLOWED} returned by the device on read request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1807.read_property_cls(self.original_device_index, self.feature_1807_index)
        Utils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("FUN_1807_0010", _AUTHOR)
    # end def test_deselect_property

    @features("Feature1807")
    @features("NoFullBankErase")
    @level("Functionality")
    @services('Debugger')
    def test_delete_property(self):
        """
        Goal: Check we can delete an existing property
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id = Utils.HIDppHelper.get_first_property_present(test_case=self, write_data_if_none=0xAA)

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        response = Utils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Check Hid++ 2.0 Error Code {Hidpp2ErrorCodes.HW_ERROR} returned by the device on read request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1807.read_property_cls(self.original_device_index, self.feature_1807_index)
        Utils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check chunk has been deleted in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        final_parser = self.memory_manager.nvs_parser
        changed_chunks = initial_parser.get_changed_chunks(final_parser, delete=True)

        self.assertEqual(expected=1,
                         obtained=len(changed_chunks),
                         msg="Only 1 chunk should have changed: the deleted property chunk")

        self.assertEqual(expected=Utils.NvsHelper.get_chunk_id(self, property_id) & 0xFF,
                         obtained=changed_chunks[0][0].chunk_id,
                         msg="Chunk previous id should be property chunk id")

        self.assertEqual(expected=final_parser.chunk_id_map["NVS_INVALID_CHUNK_ID"] & 0xFF,
                         obtained=changed_chunks[0][1].chunk_id,
                         msg="Chunk id should now be invalid chunk id")

        self.testCaseChecked("FUN_1807_0011", _AUTHOR)
    # end def test_delete_property

    @features("Feature1807")
    @features("FullBankErase")
    @level("Functionality")
    @services('Debugger')
    def test_delete_property(self):
        """
        Goal: Check we can delete an existing property
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id = Utils.HIDppHelper.get_first_property_present(test_case=self, write_data_if_none=0xAA)

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        response = Utils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Check Hid++ 2.0 Error Code {Hidpp2ErrorCodes.HW_ERROR} returned by the device on read request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1807.read_property_cls(self.original_device_index, self.feature_1807_index)
        Utils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check chunk has been deleted in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        final_parser = self.memory_manager.nvs_parser
        changed_chunks = initial_parser.get_changed_chunks(final_parser, delete=True)

        self.assertEqual(expected=2,
                         obtained=len(changed_chunks),
                         msg="2 chunks should have changed: the deleted property chunk and padding")
        property_chunks = final_parser.get_chunk_history(
            chunk_id=Utils.NvsHelper.get_chunk_id(self, property_id), active_bank_only=True)
        self.assertEqual(expected=0, obtained=len(property_chunks), msg="Property chunk should be deleted")
        initial_padding_chunk = initial_parser.get_chunk_history(
            chunk_id=initial_parser.chunk_id_map["NVS_EMPTY_CHUNK_ID"], active_bank_only=True)
        final_padding_chunk = final_parser.get_chunk_history(
            chunk_id=final_parser.chunk_id_map["NVS_EMPTY_CHUNK_ID"], active_bank_only=True)
        property_chunk = initial_parser.get_chunk_history(
            chunk_id=Utils.NvsHelper.get_chunk_id(self, property_id))[-1]
        # 1 word for header (id, length and crc) and then data
        property_chunk_size = (initial_parser.nvs_word_size +
                               initial_parser.nvs_word_size *
                               ceil(property_chunk.chunk_length / initial_parser.nvs_word_size))
        self.assertGreaterEqual(len(final_padding_chunk[-1].chunk_data),
                                len(initial_padding_chunk[-1].chunk_data) + property_chunk_size,
                                msg="Padding size should be increased by at least deleted chunk size")

        self.testCaseChecked("FUN_1807_0011", _AUTHOR)
    # end def test_delete_property

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_delete_property_not_present(self):
        """
        Goal: Check there is no error when trying to delete a property which does not exist (i.e. invalidate the
        targeted chunk in NVS).
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property not present")
        # --------------------------------------------------------------------------------------------------------------
        property_id = Utils.HIDppHelper.get_first_property_present(self, present=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        response = Utils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        self.testCaseChecked("FUN_1807_0012", _AUTHOR)
    # end def test_delete_property_not_present

    @features("Feature1807")
    @features("NoFullBankErase")
    @level("Functionality")
    @services('Debugger')
    def test_delete_corrupted_property(self):
        """
        Goal: Check there is no error when trying to delete a property which is corrupted (i.e. corrupt the CRC in NVS).
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id = Utils.HIDppHelper.get_first_property_present(test_case=self, write_data_if_none=0xAA)

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Corrupt property chunk CRC")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_id = Utils.NvsHelper.get_chunk_id(self, property_id)
        chunk = self.memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += 1
        self.post_requisite_reload_nvs = True
        Utils.load_nvs(test_case=self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check chunk has been deleted in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        final_parser = self.memory_manager.nvs_parser
        changed_chunks = initial_parser.get_changed_chunks(final_parser, delete=True)

        self.assertEqual(expected=1,
                         obtained=len(changed_chunks),
                         msg="Only 1 chunk should have changed: the deleted property chunk")

        self.assertEqual(expected=Utils.NvsHelper.get_chunk_id(self, property_id) & 0xFF,
                         obtained=changed_chunks[0][0].chunk_id,
                         msg="Chunk previous id should be property chunk id")

        self.assertEqual(expected=final_parser.chunk_id_map["NVS_INVALID_CHUNK_ID"] & 0xFF,
                         obtained=changed_chunks[0][1].chunk_id,
                         msg="Chunk id should now be invalid chunk id")

        self.testCaseChecked("FUN_1807_0013", _AUTHOR)
    # end def test_delete_corrupted_property

    @features("Feature1807")
    @features("FullBankErase")
    @level("Functionality")
    @services('Debugger')
    def test_delete_corrupted_property(self):
        """
        Goal: Check there is no error when trying to delete a property which is corrupted (i.e. corrupt the CRC in NVS).
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id = Utils.HIDppHelper.get_first_property_present(test_case=self, write_data_if_none=0xAA)

        initial_parser = self._get_initial_parser()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Corrupt property chunk CRC")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_id = Utils.NvsHelper.get_chunk_id(self, property_id)
        chunk = self.memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += 1
        self.post_requisite_reload_nvs = True
        Utils.load_nvs(test_case=self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check chunk has been deleted in NVS')
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        final_parser = self.memory_manager.nvs_parser
        changed_chunks = initial_parser.get_changed_chunks(final_parser, delete=True)

        self.assertEqual(expected=2,
                         obtained=len(changed_chunks),
                         msg="2 chunks should have changed: the deleted property chunk and padding")
        property_chunks = final_parser.get_chunk_history(
            chunk_id=Utils.NvsHelper.get_chunk_id(self, property_id), active_bank_only=True)
        self.assertEqual(expected=0, obtained=len(property_chunks), msg="Property chunk should be deleted")
        initial_padding_chunk = initial_parser.get_chunk_history(
            chunk_id=initial_parser.chunk_id_map["NVS_EMPTY_CHUNK_ID"], active_bank_only=True)
        final_padding_chunk = final_parser.get_chunk_history(
            chunk_id=final_parser.chunk_id_map["NVS_EMPTY_CHUNK_ID"], active_bank_only=True)
        property_chunk = initial_parser.get_chunk_history(
            chunk_id=Utils.NvsHelper.get_chunk_id(self, property_id))[-1]
        # 1 word for header (id, length and crc) and then data
        property_chunk_size = (initial_parser.nvs_word_size +
                               initial_parser.nvs_word_size *
                               ceil(property_chunk.chunk_length / initial_parser.nvs_word_size))
        self.assertGreaterEqual(len(final_padding_chunk[-1].chunk_data),
                                len(initial_padding_chunk[-1].chunk_data) + property_chunk_size,
                                msg="Padding size should be increased by at least deleted chunk size")

        self.testCaseChecked("FUN_1807_0013", _AUTHOR)
    # end def test_delete_corrupted_property

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_select_offset(self):
        """
        Goal: Check any offset can be used to select property:
            - Write property fully
            - For read offset in [0..property size], read it back
            - Check only bytes after offset are return
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self, min_size=2)
        test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, test_data)

        for offset in range(property_size):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Select property {repr(property_id)} with offset={offset}")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.select_property(self, property_id, rd_offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Read property {repr(property_id)}")
            # ----------------------------------------------------------------------------------------------------------
            read_response = Utils.HIDppHelper.read_property(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check property {repr(property_id)} data")
            # ----------------------------------------------------------------------------------------------------------
            data_field_len = self.feature_1807.read_property_response_cls.LEN.DATA // 8
            property_data = read_response.data[:min(data_field_len, property_size - offset)]
            expected_data = test_data[offset:min(offset + data_field_len, property_size)]
            self.assertEqual(expected=expected_data,
                             obtained=property_data,
                             msg='Read data should match expected data')
        # end for
        self.testCaseChecked("FUN_1807_0014", _AUTHOR)
    # end def test_select_offset

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_no_multiple_select_read(self):
        """
        Goal: Check only 1 property is selected for reading:
         - select a first property
         - select a second property
         - read property
         - check only last selected property is read
        This also checks that deselect is not needed to select a new property
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        first_property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        first_test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Select property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, first_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get second property supported")
        # --------------------------------------------------------------------------------------------------------------
        second_property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(
            test_case=self, skip_properties=[first_property_id])
        second_test_data = HexList("55" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Select property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_data(self, second_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select first property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select second property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, second_property_id, second_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check Hid++ 2.0 Error Code {Hidpp2ErrorCodes.NOT_ALLOWED} returned by the device on read request "
                  f"because second property size is reached and there should be nothing more to read")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1807.read_property_cls(self.original_device_index, self.feature_1807_index)
        Utils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("FUN_1807_0015", _AUTHOR)
    # end def test_no_multiple_select_read

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_no_multiple_select_write(self):
        """
        Goal: Check only 1 property is selected:
         - select a first property
         - select a second property
         - write property
         - check only last selected property is written:
           - read first property, check it is not modified
           - read second property, check it has new data
           - check NVS
        This also checks that deselect is not needed to select a new property
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        first_property_id, first_property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        first_test_data = HexList("AA" * first_property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Select property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, first_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get second property supported")
        # --------------------------------------------------------------------------------------------------------------
        second_property_id, second_property_size = Utils.ConfigurationHelper.get_first_supported_property(
            test_case=self, skip_properties=[first_property_id])
        second_test_data = HexList("55" * second_property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Select property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.write_data(self, second_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select first property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select second property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Write property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        test_data = HexList("DE" * (first_property_size + second_property_size))
        Utils.HIDppHelper.write_data(self, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check second property {repr(second_property_id)} was written")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, second_property_id, test_data[:second_property_size])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check first property {repr(first_property_id)} did not change")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, first_property_id, first_test_data)

        self.testCaseChecked("FUN_1807_0016", _AUTHOR)
    # end def test_no_multiple_select_write

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_delete_after_select(self):
        """
        Check deleting a property after selecting another one doesn't delete the selected one
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        first_property_id, property_size = Utils.ConfigurationHelper.get_first_supported_property(self)
        first_test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Select property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        Utils.HIDppHelper.write_data(self, first_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get second property present")
        # --------------------------------------------------------------------------------------------------------------
        second_property_id = Utils.HIDppHelper.get_first_property_present(
            test_case=self, skip_properties=[first_property_id], write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select first property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Delete second property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.delete_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check DeletePropertyResponse fields")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Check Hid++ 2.0 Error Code {Hidpp2ErrorCodes.HW_ERROR} returned by the device on read request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_1807.read_property_cls(self.original_device_index, self.feature_1807_index)
        Utils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check first property {repr(first_property_id)} did not change")
        # --------------------------------------------------------------------------------------------------------------
        Utils.check_property(self, first_property_id, first_test_data)

        self.testCaseChecked("FUN_1807_0017", _AUTHOR)
    # end def test_delete_after_select

    @features("Feature1807")
    @features("Feature0003")
    @features("Feature1807SupportedPropertyId", ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID)
    @level("Functionality")
    @services('Debugger')
    def test_extended_model_id_default_restored(self):
        """
        Check the Extended model id default value is restored when deleting an existing property:
         - check the property id is supported and present, select the property, delete it
         - check 0x0003.getDeviceInfo matches
        """
        property_id = ConfigurableProperties.PropertyId.EXTENDED_MODEL_ID
        test_data = HexList("AA" * Utils.ConfigurationHelper.get_size(self, property_id))

        self.post_requisite_reload_nvs = True
        self._write_check_supported_property(property_id, test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Extended Model Id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        extended_model_id = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check extended model id matches written data")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(test_data,
                         extended_model_id,
                         "Extended Model Id obtained from feature 0x0003 should match written data")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Delete property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        response = Utils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check valid response")
        # --------------------------------------------------------------------------------------------------------------
        Utils.MessageChecker.check_fields(self, response, self.feature_1807.delete_property_response_cls, check_map={})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read Extended Model Id with feature 0x0003")
        # --------------------------------------------------------------------------------------------------------------
        extended_model_id = DeviceInformationTestUtils.HIDppHelper.get_extended_model_id(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check extended model id matches default value")
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(int(Numeral(self.config_manager.get_feature(ConfigurationManager.ID.EXTENDED_MODEL_ID))),
                         int(Numeral(extended_model_id)),
                         "Extended Model Id obtained from feature 0x0003 should be default value")

        self.testCaseChecked("FUN_1807_0018", _AUTHOR)
    # end def test_extended_model_id_default_restored

    @features("Feature1807")
    @level("Functionality")
    @services('Debugger')
    def test_parallel_read_write(self):
        """
        Goal: Check read and write operations could be done in parallel (i.e. read and write offsets are independent):
         - select a property (with a sufficient size) with read and write offsets = 0
         - without additional select property, loop until end of property size (let offsets increment automatically):
          - write property
          - read property
          - check data written is read back, i.e. read offset is not incremented with write offset
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get biggest property supported")
        # --------------------------------------------------------------------------------------------------------------
        sizes = Utils.ConfigurationHelper.get_sizes(self)
        property_id = max(sizes, key=sizes.get)
        property_size = Utils.ConfigurationHelper.get_size(self, property_id)
        test_data = HexList.fromString(''.join(choices(ascii_uppercase + digits, k=property_size)))
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test data = {test_data}")
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        Utils.HIDppHelper.select_property(self, property_id)

        self.post_requisite_reload_nvs = True
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self,
                           "Without additional select property, loop until end of property size (let offsets "
                           "increment automatically)")
        # --------------------------------------------------------------------------------------------------------------
        pos = 0
        data_field_len = self.feature_1807.write_property_cls.LEN.DATA // 8
        while pos + data_field_len <= len(test_data):
            test_data_chunk = test_data[pos:pos + data_field_len]
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write property {repr(property_id)} at offset {pos}")
            # ----------------------------------------------------------------------------------------------------------
            Utils.HIDppHelper.write_property(self, test_data_chunk)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Read property {repr(property_id)} at offset {pos}")
            # ----------------------------------------------------------------------------------------------------------
            read_response = Utils.HIDppHelper.read_property(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check property {repr(property_id)} data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=test_data_chunk,
                             obtained=read_response.data,
                             msg='Read data should match expected data')

            pos += data_field_len
            if pos == len(test_data):
                break
            # end if
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Write the last block of the property {repr(property_id)} at offset {pos}")
            # ----------------------------------------------------------------------------------------------------------
            test_data_chunk = test_data[pos:]
            test_data_chunk.addPadding(size=data_field_len, fromLeft=False)
            Utils.HIDppHelper.write_property(self, test_data_chunk)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Read the last block of the property {repr(property_id)} at offset {pos}")
            # ----------------------------------------------------------------------------------------------------------
            read_response = Utils.HIDppHelper.read_property(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check property {repr(property_id)} data")
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=test_data_chunk,
                             obtained=read_response.data,
                             msg='Read data should match expected data')
        # end while
        self.testCaseChecked("FUN_1807_0019", _AUTHOR)
    # end def test_parallel_read_write
# end class ConfigurablePropertiesFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
