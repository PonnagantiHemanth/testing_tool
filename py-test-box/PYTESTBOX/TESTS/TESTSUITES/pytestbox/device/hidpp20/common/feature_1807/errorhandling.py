#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.hidpp20.common.feature_1807.errorhandling
:brief: HID++ 2.0 ``ConfigurableProperties`` error handling test suite
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/10/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.configurableproperties import ConfigurableProperties
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurablepropertiesutils import ConfigurablePropertiesTestUtils
from pytestbox.device.hidpp20.common.feature_1807.configurableproperties import ConfigurablePropertiesTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Martin Cryonnet"
_LOOP_END = "End Test Loop"
_LOOP_START_FID = "Test loop over functionIndex invalid range (typical wrong values)"
_GET_FIRST_PROPERTY = "Get first property present"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
# noinspection PyAttributeOutsideInit
class ConfigurablePropertiesErrorHandlingTestCase(ConfigurablePropertiesTestCase):
    """
    Validate ``ConfigurableProperties`` errorhandling test cases
    """

    @features("Feature1807")
    @level("ErrorHandling")
    def test_wrong_function_index(self):
        """
        Validate function index
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_START_FID)
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range(
                value=list(range(self.feature_1807.get_max_function_index() + 1)),
                max_value=0xF):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send GetPropertyInfo request with a wrong function index:{function_index}")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info_and_check_error(
                test_case=self,
                error_codes=[ErrorCodes.INVALID_FUNCTION_ID],
                property_id=ConfigurableProperties.PropertyId.MIN,
                function_index=function_index)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ERR_1807_0001", _AUTHOR)
    # end def test_wrong_function_index

    @features("Feature1807")
    @level("ErrorHandling")
    def test_get_property_info_invalid_argument(self):
        """
        When sending GetPropertyInfo with propertyId = 0, the firmware shall raise an error INVALID_ARGUMENT
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(
            self, f"Send GetPropertyInfo request with property id = {ConfigurableProperties.PropertyId.DESELECT_ALL}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.get_property_info_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
            property_id=ConfigurableProperties.PropertyId.DESELECT_ALL)

        self.testCaseChecked("ERR_1807_0002", _AUTHOR)
    # end def test_get_property_info_invalid_argument

    @features("Feature1807")
    @level("ErrorHandling")
    def test_requests_unsupported_property(self):
        """
        ERR_1807_0003:
            When sending SelectProperty with a propertyId not supported, the firmware shall raise an error
            INVALID_ARGUMENT

        ERR_1807_0006:
            When sending ReadProperty or WriteProperty after a SelectProperty with a propertyId not supported,
            the firmware shall raise an error NOT_ALLOWED (i.e. No property was selected)
        """
        property_id = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_property_not_supported(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SelectProperty request for {property_id}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT],
            property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED],
            data=0xAA)

        self.testCaseChecked("ERR_1807_0003", _AUTHOR)
        self.testCaseChecked("ERR_1807_0006", _AUTHOR)
    # end def test_requests_unsupported_property

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_requests_with_undefined_property(self):
        """
        ERR_1807_0004:
            When sending SelectProperty with an undefined propertyId (i.e. in its error range), the firmware shall
            raise an error INVALID_ARGUMENT

        ERR_1807_0007:
            When sending ReadProperty or WriteProperty after a SelectProperty with an undefined propertyId (i.e. in its
            error range), the firmware shall raise an error NOT_ALLOWED (i.e. No property was selected)
        """
        property_id = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_undefined_property_ids(self)[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SelectProperty request for property_id: {property_id}")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property_and_check_error(
            test_case=self,
            property_id=property_id,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_property_and_check_error(
            test_case=self,
            data=0xAA,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1807_0004", _AUTHOR)
        self.testCaseChecked("ERR_1807_0007", _AUTHOR)
    # end def test_requests_with_undefined_property

    @features("Feature1807")
    @level("ErrorHandling")
    def test_select_property_both_offsets_out_of_range(self):
        """
        When sending SelectProperty with both offset greater or equal than the maximum size supported by the selected
        propertyId, the firmware shall raise an error INVALID_ARGUMENT
        """
        property_id, property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(
            test_case=self)

        for offset in compute_sup_values(property_size, is_equal=True):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectProperty request for property_id: {property_id} and offset: {offset}")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.HIDppHelper.select_property_and_check_error(
                test_case=self,
                property_id=property_id,
                rd_offset=offset,
                wr_offset=offset,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1807_0005#1", _AUTHOR)
    # end def test_select_property_both_offsets_out_of_range

    @features("Feature1807")
    @level("ErrorHandling")
    def test_select_property_offset_out_of_range_read(self):
        """
        When sending SelectProperty with only a read offset greater or equal than the maximum size supported by the
        selected propertyId, the firmware shall NOT raise any error
        """
        property_id, property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(
            test_case=self)

        for offset in compute_sup_values(property_size, is_equal=True):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SelectProperty request for rd_offset:{offset}")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
                test_case=self,
                property_id=property_id,
                rd_offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectPropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1807.select_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1807_0005#2", _AUTHOR)
    # end def test_select_property_offset_out_of_range_read

    @features("Feature1807")
    @level("ErrorHandling")
    def test_select_property_offset_out_of_range_write(self):
        """
        When sending SelectProperty with only write offset greater or equal than the maximum size supported by the
        selected propertyId, the firmware shall NOT raise any error
        """
        property_id, property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_supported_property(
            test_case=self)

        for offset in compute_sup_values(property_size, is_equal=True):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Send SelectProperty request")
            # ----------------------------------------------------------------------------------------------------------
            response = ConfigurablePropertiesTestUtils.HIDppHelper.select_property(
                test_case=self,
                property_id=property_id,
                wr_offset=offset)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check SelectPropertyResponse fields")
            # ----------------------------------------------------------------------------------------------------------
            ConfigurablePropertiesTestUtils.MessageChecker.check_fields(
                self, response, self.feature_1807.select_property_response_cls, {})
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, _LOOP_END)
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ERR_1807_0005#3", _AUTHOR)
    # end def test_select_property_offset_out_of_range_write

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_read_property_after_max_size(self):
        """
        When sending ReadProperty while the maximum size has already been reached, the firmware shall raise an error
        NOT_ALLOWED
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _GET_FIRST_PROPERTY)
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(
            test_case=self, write_data_if_none=0xAA)

        property_size = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_size(self, property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first present property")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Read property until the end")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.read_data(test_case=self, data_size=property_size)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.NOT_ALLOWED])

        self.testCaseChecked("ERR_1807_0008", _AUTHOR)
    # end def test_read_property_after_max_size

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_read_property_not_present(self):
        """
        Goal: Check that if a property doesn't exist in NVS (i.e. Invalidate the existing chunk), the firmware shall
        raise an error HW_ERROR on a ReadProperty request
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get first property not present")
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(self, present=False)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select first not present property")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        self.testCaseChecked("ERR_1807_0009", _AUTHOR)
    # end def test_read_property_not_present

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_read_property_corrupted(self):
        """
        Goal: Check that if a property is corrupted, the firmware shall raise an error HW_ERROR on a ReadProperty or
        WriteProperty request
            - Reload the existing chunk with a corrupted CRC.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _GET_FIRST_PROPERTY)
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(
            test_case=self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Corrupt property chunk CRC")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_id = ConfigurablePropertiesTestUtils.NvsHelper.get_chunk_id(self, property_id)
        chunk = self.memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += 1
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.load_nvs(test_case=self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select corrupted property")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send ReadProperty request")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.read_property_and_check_error(
            test_case=self,
            error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        self.testCaseChecked("ERR_1807_0010#1", _AUTHOR)
    # end def test_read_property_corrupted

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_write_property_corrupted(self):
        """
        Goal: Check that if a property is corrupted, the firmware shall raise an error HW_ERROR on a ReadProperty or
        WriteProperty request
            - Reload the existing chunk with a corrupted CRC.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, _GET_FIRST_PROPERTY)
        # --------------------------------------------------------------------------------------------------------------
        property_id = ConfigurablePropertiesTestUtils.HIDppHelper.get_first_property_present(
            test_case=self, write_data_if_none=0xAA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Corrupt property chunk CRC")
        # --------------------------------------------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        chunk_id = ConfigurablePropertiesTestUtils.NvsHelper.get_chunk_id(self, property_id)
        chunk = self.memory_manager.nvs_parser.get_chunk(chunk_id=chunk_id)
        chunk.chunk_crc += 1
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.load_nvs(test_case=self)

        self._activate_features()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Select corrupted property")
        # --------------------------------------------------------------------------------------------------------------
        ConfigurablePropertiesTestUtils.HIDppHelper.select_property(self, property_id=property_id)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send WriteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.write_property_and_check_error(
            test_case=self,
            data=0xAA,
            error_codes=[Hidpp2ErrorCodes.HW_ERROR])

        self.testCaseChecked("ERR_1807_0010#2", _AUTHOR)
    # end def test_write_property_corrupted

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_delete_property_not_supported(self):
        """
        When sending DeleteProperty with a propertyId not supported, the firmware shall raise an error INVALID_ARGUMENT
        """
        property_id = ConfigurablePropertiesTestUtils.ConfigurationHelper.get_first_property_not_supported(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.delete_property_and_check_error(
            test_case=self,
            property_id=property_id,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1807_0011#1", _AUTHOR)
    # end def test_delete_property_not_supported

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_delete_property_invalid(self):
        """
        When sending DeleteProperty with a propertyId not supported, the firmware shall raise an error INVALID_ARGUMENT
        """
        property_id = ConfigurableProperties.PropertyId.INVALID

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Send DeleteProperty request")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ConfigurablePropertiesTestUtils.HIDppHelper.delete_property_and_check_error(
            test_case=self,
            property_id=property_id,
            error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])

        self.testCaseChecked("ERR_1807_0011#2", _AUTHOR)
    # end def test_delete_property_invalid

    @features("Feature1807")
    @level("ErrorHandling")
    @services('Debugger')
    def test_delete_property_undefined(self):
        """
        When sending DeleteProperty with a propertyId not supported, the firmware shall raise an error INVALID_ARGUMENT
        """
        for property_id in ConfigurablePropertiesTestUtils.ConfigurationHelper.get_undefined_property_ids(self):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send DeleteProperty request with property id: {property_id}")
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reload_nvs = True
            ConfigurablePropertiesTestUtils.HIDppHelper.delete_property_and_check_error(
                test_case=self,
                property_id=property_id,
                error_codes=[Hidpp2ErrorCodes.INVALID_ARGUMENT])
        # end for

        self.testCaseChecked("ERR_1807_0011#3", _AUTHOR)
    # end def test_delete_property_undefined
# end class ConfigurablePropertiesErrorHandlingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
