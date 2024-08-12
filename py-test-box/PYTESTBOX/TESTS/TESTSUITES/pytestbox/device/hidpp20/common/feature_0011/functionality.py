#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.1'
:package: pytestbox.device.hidpp20.common.feature_0011.functionality
:brief: HID++ 2.0 ``PropertyAccess`` functionality test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2022/06/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.propertyaccess import PropertyAccess
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils
from pytestbox.device.hidpp20.common.feature_0011.propertyaccess import PropertyAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Kevin Dayet"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class PropertyAccessFunctionalityTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` functionality test cases
    """
    @features("Feature0011")
    @level("Functionality")
    def test_supported_properties(self):
        """
        Check supported properties in DUT matches expected supported properties in configuration list
        Sending GetPropertyInfo with a propertyId not supported by the DUT should return a null flags value.
        And supported flag should be set if a property is supported by the DUT.
        """
        for property_id in range(PropertyAccess.PropertyId.MIN, PropertyAccess.PropertyId.MAX + 1):
            repr_prop_id = repr(PropertyAccess.PropertyId(property_id)) if property_id not in \
                            PropertyAccessTestUtils.ConfigurationHelper.get_undefined_property_ids(
                                test_case=self) else property_id
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Get property {repr_prop_id} info")
            # ----------------------------------------------------------------------------------------------------------
            property_info_response = PropertyAccessTestUtils.HIDppHelper.get_property_info(self, property_id)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check GetPropertyInfoResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            check_map = PropertyAccessTestUtils.\
                GetPropertyInfoResponseChecker.get_check_map_by_property(self, property_id=property_id)
            PropertyAccessTestUtils.GetPropertyInfoResponseChecker.check_fields(
                self, property_info_response, self.feature_0011.get_property_info_response_cls, check_map=check_map)
        # end for

        self.testCaseChecked("FUN_0011_0006", _AUTHOR)
        self.testCaseChecked("ROB_0011_0001", _AUTHOR)
    # end def test_supported_properties

    @features("Feature0011")
    @level("Functionality")
    @services('Debugger')
    def test_corrupted_property(self):
        """
        Check GetPropertyInfo with a corrupted property should return a corrupted flag
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Corrupt property chunk CRC")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_id = PropertyAccessTestUtils.NvsHelper.get_chunk_id(self, property_id)
        chunk = self.memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += (1 if chunk.chunk_crc < 0xFFFF else -1)
        self.post_requisite_reload_nvs = True
        PropertyAccessTestUtils.load_nvs(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get property {repr(property_id)} info")
        # --------------------------------------------------------------------------------------------------------------
        get_property_info_response = PropertyAccessTestUtils.HIDppHelper.get_property_info(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)} is supported, present and corrupted")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.FlagsMaskBitMapChecker
        flags = checker.get_default_check_map(self)
        flags.update({
            "present": (checker.check_present, True),
            "supported": (checker.check_supported, True),
            "corrupted": (checker.check_corrupted, True)
        })
        checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
        check_map = checker.get_check_map_by_property(self, property_id)
        check_map["flags"] = (checker.check_flags, flags)
        checker.check_fields(
            self, get_property_info_response, self.feature_0011.get_property_info_response_cls, check_map=check_map)

        self.testCaseChecked("FUN_0011_0007", _AUTHOR)
    # end def test_corrupted_property

    @features("Feature0011")
    @level("Functionality")
    @services('Debugger')
    def test_deselect_property(self):
        """
        Check SelectProperty with propertyId = 0 deselect the current property.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select property {repr(property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Call Select property with property_id = {repr(PropertyAccess.PropertyId.DESELECT_ALL)}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, PropertyAccess.PropertyId.DESELECT_ALL)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f'Check Hid++ 2.0 Error Code {ErrorCodes.NOT_ALLOWED} returned by the device on read request')
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_0011.read_property_cls(self.original_device_index, self.feature_0011_index)
        PropertyAccessTestUtils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("FUN_0011_0008", _AUTHOR)
    # end def test_deselect_property

    @features("Feature0011")
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
        property_id, property_size = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(
            test_case=self, min_size=2)
        test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(property_id)} with nvs parser")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        PropertyAccessTestUtils.NvsHelper.write_property_id(self, property_id, test_data)

        for offset in range(property_size):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Select property {repr(property_id)} with offset={offset}")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id, rd_offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Read property {repr(property_id)}")
            # ----------------------------------------------------------------------------------------------------------
            read_response = PropertyAccessTestUtils.HIDppHelper.read_property(self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f"Check property {repr(property_id)} data")
            # ----------------------------------------------------------------------------------------------------------
            data_field_len = self.feature_0011.read_property_response_cls.LEN.DATA // 8
            property_data = read_response.data[:min(data_field_len, property_size - offset)]
            expected_data = test_data[offset:min(offset + data_field_len, property_size)]
            self.assertEqual(expected=expected_data,
                             obtained=property_data,
                             msg='Read data should match expected data')
        # end for
        self.testCaseChecked("FUN_0011_0009", _AUTHOR)
    # end def test_select_offset

    @features("Feature0011")
    @level("Functionality")
    @services('Debugger')
    def test_no_multiple_select_read(self):
        """
        Goal: Check only 1 property is selected for reading:
         - select a first property
         - select a second property
         - read property
         - check only last selected property is read
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property supported")
        # --------------------------------------------------------------------------------------------------------------
        first_property_id, property_size = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(
            test_case=self)
        first_test_data = HexList("AA" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(first_property_id)} with nvs parser")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        PropertyAccessTestUtils.NvsHelper.write_property_id(self, first_property_id, first_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get second property supported")
        # --------------------------------------------------------------------------------------------------------------
        second_property_id, property_size = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(
            test_case=self, skip_properties=[first_property_id])
        second_test_data = HexList("55" * property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Write property {repr(second_property_id)} with nvs parser")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.NvsHelper.write_property_id(self, second_property_id, second_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select first property {repr(first_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, first_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Select second property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, second_property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(second_property_id)}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.check_property(self, second_property_id, second_test_data)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, f"Check Hid++ 2.0 Error Code {ErrorCodes.NOT_ALLOWED} returned by the device on read request "
                  f"because second property size is reached and there should be nothing more to read")
        # --------------------------------------------------------------------------------------------------------------
        report = self.feature_0011.read_property_cls(self.original_device_index, self.feature_0011_index)
        PropertyAccessTestUtils.HIDppHelper.send_report_wait_error(
            self, report, error_codes=[ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("FUN_0011_0010", _AUTHOR)
    # end def test_no_multiple_select_read
# end class PropertyAccessFunctionalityTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
