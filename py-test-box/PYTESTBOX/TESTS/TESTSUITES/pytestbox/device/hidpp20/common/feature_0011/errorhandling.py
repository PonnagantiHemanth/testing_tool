#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_0011.errorhandling
:brief: HID++ 2.0 ``PropertyAccess`` error handling test suite
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
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.base.propertyaccessutils import PropertyAccessTestUtils
from pytestbox.device.hidpp20.common.feature_0011.propertyaccess import PropertyAccessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Kevin Dayet"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class PropertyAccessErrorHandlingTestCase(PropertyAccessTestCase):
    """
    Validate ``PropertyAccess`` errorhandling test cases
    """

    @features("Feature0011")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(value=list(range(self.feature_0011.get_max_function_index() + 1)),
                                                  max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPropertyInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.HIDppHelper.get_property_info_and_check_error(
                test_case=self,
                property_id=PropertyAccess.PropertyId.MIN,
                function_index=function_index,
                error_codes=[Hidpp2ErrorCodes.INVALID_FUNCTION_ID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_0011_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature0011")
    @level("ErrorHandling")
    def test_get_property_info_invalid_argument(self):
        """
        When sending GetPropertyInfo with propertyId = 0, the firmware shall raise an error INVALID_ARGUMENT
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send GetPropertyInfo request with property id = {PropertyAccess.PropertyId.DESELECT_ALL}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.get_property_info_and_check_error(
            test_case=self,
            property_id=PropertyAccess.PropertyId.DESELECT_ALL,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT]
        )

        self.testCaseChecked("ERR_0011_0002", _AUTHOR)
    # end def test_get_property_info_invalid_argument

    @features("Feature0011")
    @level("ErrorHandling")
    def test_requests_unsupported_property(self):
        """
        ERR_0011_0003:
            When sending SelectProperty with a propertyId not supported, the firmware shall raise an error
            INVALID_ARGUMENT

        ERR_0011_0006:
            When sending ReadProperty after a SelectProperty with a propertyId not supported,
            the firmware shall raise an error NOT_ALLOWED (i.e. No property was selected)
        """
        property_id = PropertyAccessTestUtils.ConfigurationHelper.get_first_property_not_supported(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SelectProperty request with a propertyId {property_id} not supported")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property_and_check_error(
            test_case=self,
            property_id=property_id,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_0011_0003", _AUTHOR)
        self.testCaseChecked("ERR_0011_0006", _AUTHOR)
    # end def test_requests_unsupported_property

    @features("Feature0011")
    @level("ErrorHandling")
    def test_requests_with_undefined_property(self):
        """
        ERR_0011_0004:
            When sending SelectProperty with an undefined propertyId (i.e. in its error range), the firmware shall
            raise an error INVALID_ARGUMENT

        ERR_0011_0007:
            When sending ReadProperty after a SelectProperty with an undefined propertyId (i.e. in its
            error range), the firmware shall raise an error NOT_ALLOWED (i.e. No property was selected)
        """
        property_id = PropertyAccessTestUtils.ConfigurationHelper.get_undefined_property_ids(test_case=self)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SelectProperty request with an undefined propertyId {property_id}")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property_and_check_error(
            test_case=self,
            property_id=property_id,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_0011_0004", _AUTHOR)
        self.testCaseChecked("ERR_0011_0007", _AUTHOR)
    # end def test_requests_with_undefined_property

    @features("Feature0011")
    @level("ErrorHandling")
    def test_select_property_offset_out_of_range(self):
        """
        When sending SelectProperty with both offset greater or equal than the maximum size supported by the selected
        propertyId, the firmware shall raise an error INVALID_ARGUMENT
        """
        property_id, property_size = PropertyAccessTestUtils.ConfigurationHelper.get_first_supported_property(self)

        for offset in compute_sup_values(property_size, is_equal=True):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectProperty request with an unsupported read offset")
            # ----------------------------------------------------------------------------------------------------------
            PropertyAccessTestUtils.HIDppHelper.select_property_and_check_error(
                test_case=self,
                property_id=property_id,
                rd_offset=offset,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_0011_0005", _AUTHOR)
    # end def test_select_property_offset_out_of_range

    @features("Feature0011")
    @level("ErrorHandling")
    def test_read_property_after_max_size(self):
        """
        When sending ReadProperty while the maximum size has already been reached, the firmware shall raise an error
        NOT_ALLOWED
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property until the end")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_data(self, property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_0011_0008", _AUTHOR)
    # end def test_read_property_after_max_size

    @features("Feature0011")
    @level("ErrorHandling")
    @services('Debugger')
    def test_read_property_not_present(self):
        """
        Check that if a property doesn't exist in NVS (i.e. Invalidate the existing chunk), the firmware shall
        raise an error HW_ERROR on a ReadProperty request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property not present")
        # --------------------------------------------------------------------------------------------------------------
        property_id, property_size = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(self, present=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Get property {repr(property_id)} info")
        # --------------------------------------------------------------------------------------------------------------
        get_property_info_response = PropertyAccessTestUtils.HIDppHelper.get_property_info(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check property {repr(property_id)} is supported but not present")
        # --------------------------------------------------------------------------------------------------------------
        checker = PropertyAccessTestUtils.FlagsMaskBitMapChecker
        flags = checker.get_default_check_map(self)
        flags.update({
            "present": (checker.check_present, False),
            "supported": (checker.check_supported, True)
        })
        checker = PropertyAccessTestUtils.GetPropertyInfoResponseChecker
        check_map = checker.get_check_map_by_property(self, property_id)
        check_map.update({
            "flags": (checker.check_flags, flags),
            "size": (checker.check_size, property_size)
        })
        checker.check_fields(
            self, get_property_info_response, self.feature_0011.get_property_info_response_cls, check_map=check_map)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first not present property")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        self.testCaseChecked("ERR_0011_0009", _AUTHOR)
    # end def test_read_property_not_present

    @features("Feature0011")
    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_read_property_after_configurable_property_delete(self):
        """
        Check that if a property is deleted with 0x1807 ConfigurableProperties.DeleteProperties, an error HW_ERROR shall
        be raised on ReadProperty request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property present")
        # --------------------------------------------------------------------------------------------------------------
        property_id, _ = PropertyAccessTestUtils.HIDppHelper.get_first_property_present(
            self, write_data_if_none=0xAA)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Delete property with Ox1807 ConfigurableProperties.DeleteProperties")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.delete_property(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first supported property")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        self.testCaseChecked("ERR_0011_0010", _AUTHOR)
    # end def test_read_property_after_configurable_property_delete

    @features("Feature0011")
    @level("ErrorHandling")
    @services('Debugger')
    def test_read_property_corrupted(self):
        """
        Check that if a property is corrupted, the firmware shall raise an error HW_ERROR on a ReadProperty or
        WriteProperty request
            - Reload the existing chunk with a corrupted CRC.
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
        LogHelper.log_step(self, "Select corrupted property")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        PropertyAccessTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        self.testCaseChecked("ERR_0011_0011", _AUTHOR)
    # end def test_read_property_corrupted
# end class PropertyAccessErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
