#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.hid.common.feature_0003
:brief: Validates HID++ common feature 0x0003
:author: Stanislas Cottard
:date: 2019/11/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import copy
from abc import ABC
from sys import stdout

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesFactory
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceInformationTestCaseMixin(CommonBaseTestCase, ABC):
    """
    Validates Device information TestCases
    """
    def setUpClass(self):
        """
        Define variables
        """
        super().setUpClass()

        self.feature_0003 = None
        self.feature_0003_index = None
    # end def setUpClass

    def generic_get_device_info_get_fw_info_business(self):
        """
        Validate getDeviceInfo GetFwInfo business case
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceInfo request')
        # ----------------------------------------------------------------------------
        get_device_info_response = DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for GetDeviceInfo response and check product-specific constants')
        # ----------------------------------------------------------------------------
        DeviceInformationTestUtils.GetDeviceInfoResponseChecker.check_fields(
            self, get_device_info_response, self.feature_0003.get_device_info_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the entity index in [0..'
                                 f'{int(Numeral(get_device_info_response.entity_count)) - 1}]')
        # ----------------------------------------------------------------------------
        for i in range(int(Numeral(get_device_info_response.entity_count))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetFwInfo request with entityIdx = {i}')
            # ----------------------------------------------------------------------------
            get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(test_case=self, entity_index=i)
            # Print FW info in the console to help to identify firmware under test
            stdout.write(f"Entity {i} : {ascii_converter(get_fw_info_response.fw_prefix)} "
                         f"{get_fw_info_response.fw_build} (Type {to_int(get_fw_info_response.fw_type)})\n")

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetFwInfo response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls,
                DeviceInformationTestUtils.GetFwInfoResponseChecker.get_check_map_for_entity(self, i))
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
    # end def generic_get_device_info_get_fw_info_business

    def generic_get_device_serial_number_api(self):
        """
        Validate getDeviceSerialNumber interface, introduced in version 4
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceSerialNumber request')
        # ----------------------------------------------------------------------------
        get_device_serial_number_report = self.feature_0003.get_device_serial_number_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index)

        get_device_serial_number_response = ChannelUtils.send(
            test_case=self,
            report=get_device_serial_number_report,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_0003.get_device_serial_number_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for GetDeviceSerialNumber response and check product-specific serial number')
        # ----------------------------------------------------------------------------
        DeviceInformationTestUtils.GetDeviceSerialNumberResponseChecker.check_fields(
            self, get_device_serial_number_response, self.feature_0003.get_device_serial_number_response_cls)
    # end def generic_get_device_serial_number_api

# end class DeviceInformationTestCaseMixin


class SharedDeviceInformationTestCase(DeviceInformationTestCaseMixin, ABC):
    """
    Validates Device information TestCases
    """

    @features('Feature0003')
    @level('Interface')
    def test_get_device_info_api(self):
        """
        Validate getDeviceInfo interface
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetDeviceInfo request')
        # ----------------------------------------------------------------------------
        get_device_info_response = DeviceInformationTestUtils.HIDppHelper.get_device_info(test_case=self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for GetDeviceInfo response and check product-specific constants')
        # ----------------------------------------------------------------------------
        DeviceInformationTestUtils.GetDeviceInfoResponseChecker.check_fields(
            self, get_device_info_response, self.feature_0003.get_device_info_response_cls)

        self.testCaseChecked("FNT_0003_0001")
    # end def test_get_device_info_api

    @features('Feature0003')
    @level('Interface')
    def test_get_fw_info_api(self):
        """
        Validate getFwInfo interface
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetFwInfo request with entityIdx = 0')
        # ----------------------------------------------------------------------------
        get_fw_info_response = DeviceInformationTestUtils.HIDppHelper.get_fw_info(test_case=self, entity_index=0)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for GetFwInfo response and check product-specific constants')
        # ----------------------------------------------------------------------------
        DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
            self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls)

        self.testCaseChecked("FNT_0003_0002")
    # end def test_get_fw_info_api

    @features('Feature0003')
    @level('Business', 'SmokeTests')
    def test_get_device_info_get_fw_info_business(self):
        """
        Validate getDeviceInfo GetFwInfo business case
        """
        self.generic_get_device_info_get_fw_info_business()

        self.testCaseChecked("FNT_0003_0003")
    # end def test_get_device_info_get_fw_info_business

    @features('Feature0003v4+')
    @level('Interface')
    def test_get_device_serial_number_api(self):
        """
        Validate getDeviceSerialNumber interface, introduced in version 4
        """
        self.generic_get_device_serial_number_api()

        self.testCaseChecked("FNT_0003_0004")
    # end def test_get_device_serial_number_api

    @features('Feature0003v4+')
    @features('Feature1806')
    @level('Functionality')
    def test_get_device_serial_number_default_value(self):
        """
        Validate getDeviceSerialNumber default value
        """
        initial_nvs_parser = self.get_dut_nvs_parser()

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Load NVS memory without any Serial Number chunk Id')
        # ----------------------------------------------------------------------------
        nvs_parser_copy = copy.deepcopy(initial_nvs_parser)
        nvs_parser_copy.delete_chunk(chunk_id="NVS_SERIAL_NUMBER_ID")
        self.debugger.reload_file(nvs_hex_file=nvs_parser_copy.to_hex_file())
        self.reset()

        try:
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getDeviceSerialNumber request to get serial number')
            # ----------------------------------------------------------------------------
            get_device_serial_number_report = self.feature_0003.get_device_serial_number_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index)

            get_device_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=get_device_serial_number_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_serial_number_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check all bytes of serial number are 0x00')
            # ----------------------------------------------------------------------------
            # Get the 0x1806 feature
            feature_1806 = ConfigurableDevicePropertiesFactory.create(
                self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.CONFIGURABLE_DEVICE_PROPERTIES))

            DeviceInformationTestUtils.GetDeviceSerialNumberResponseChecker.check_device_serial_number(
                test_case=self,
                get_device_serial_number_response=get_device_serial_number_response,
                expected='00' * feature_1806.property_size.SERIAL_NUMBER)
        finally:
            # ----------------------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Load NVS memory with initial Serial Number')
            # ----------------------------------------------------------------------------
            self.debugger.reload_file(nvs_hex_file=initial_nvs_parser.to_hex_file())
        # end try

        self.testCaseChecked("FNT_0003_0006")
    # end def test_get_device_serial_number_default_value

    @features('Feature0003')
    @level('ErrorHandling')
    def test_get_fw_info_wrong_entity_index(self):
        """
        Validate getFwInfo with entity index greater than the entity count raise an error
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the entity index in ['
                                 f'{self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount}..0xFF] (only interesting '
                                 'values)')
        # ----------------------------------------------------------------------------
        for entity_index in compute_wrong_range(value=list(range(
                self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_EntityCount)), max_value=0xFF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetFwInfo request with entityIdx = {entity_index}')
            # ----------------------------------------------------------------------------
            get_fw_info_report = self.feature_0003.get_fw_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index,
                entity_index=entity_index)

            error_response = ChannelUtils.send(
                test_case=self,
                report=get_fw_info_report,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check InvalidArgument (0x02) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=ErrorCodes.INVALID_ARGUMENT,
                             msg="The error_code parameter differs from the one expected")
        # end for
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_0003_0001")
    # end def test_get_fw_info_wrong_entity_index

    @features('Feature0003')
    @level('ErrorHandling')
    def test_wrong_function_index(self):
        """
        Validate sending a wrong function index raises an error
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the function index in '
                                 f'[{self.feature_0003.get_max_function_index() + 1}..0xF] (only interesting values)')
        # ----------------------------------------------------------------------------
        for function_index in \
                compute_wrong_range(value=list(range(
                    self.feature_0003.get_max_function_index() + 1)), max_value=0xF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetFwInfo request with entityIdx = 0 and functionIndex = {function_index}')
            # ----------------------------------------------------------------------------
            get_fw_info_report = self.feature_0003.get_fw_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index,
                entity_index=0)
            get_fw_info_report.functionIndex = function_index

            error_response = ChannelUtils.send(
                test_case=self,
                report=get_fw_info_report,
                response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check InvalidFunctionId (0x07) Error Code returned by the device')
            # ----------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=ErrorCodes.INVALID_FUNCTION_ID,
                             msg="The error_code parameter differs from the one expected")
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_0003_0002")
    # end def test_wrong_function_index

    @features('Feature0003')
    @level('Robustness')
    def test_get_device_info_software_id_robustness(self):
        """
        Validate getDeviceInfo robustness to software ID
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the software ID other than the default '
                                 f'{DeviceInformation.DEFAULT.SOFTWARE_ID} (only interesting values)')
        # ----------------------------------------------------------------------------
        for software_id in compute_wrong_range(value=DeviceInformation.DEFAULT.SOFTWARE_ID, max_value=0xF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetDeviceInfo request with softwareId = {software_id}')
            # ----------------------------------------------------------------------------
            get_device_info_report = self.feature_0003.get_device_info_cls(
                ChannelUtils.get_device_index(test_case=self), self.feature_0003_index)

            get_device_info_report.softwareId = software_id

            get_device_info_response = ChannelUtils.send(
                test_case=self,
                report=get_device_info_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_info_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetDeviceInfo response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetDeviceInfoResponseChecker.check_fields(
                self, get_device_info_response, self.feature_0003.get_device_info_response_cls)
        # end for loop
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_0003_0003")
    # end def test_get_device_info_software_id_robustness

    @features('Feature0003')
    @level('Robustness')
    def test_get_fw_info_software_id_robustness(self):
        """
        Validate getFwInfo robustness to software ID
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the software ID other than the default '
                                 f'{DeviceInformation.DEFAULT.SOFTWARE_ID} (only interesting values)')
        # ----------------------------------------------------------------------------
        for software_id in compute_wrong_range(value=DeviceInformation.DEFAULT.SOFTWARE_ID, max_value=0xF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetFwInfo request with entityIdx = 0 and softwareId = {software_id}')
            # ----------------------------------------------------------------------------
            get_fw_info_report = self.feature_0003.get_fw_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index,
                entity_index=0)
            get_fw_info_report.softwareId = software_id

            get_fw_info_response = ChannelUtils.send(
                test_case=self,
                report=get_fw_info_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_fw_info_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetFwInfo response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls)
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------

        self.testCaseChecked("ROT_0003_0004")
    # end def test_get_fw_info_software_id_robustness

    @features('Feature0003')
    @level('Robustness')
    def test_get_device_info_padding_robustness(self):
        """
        Validate getDeviceInfo robustness to padding
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the padding other than the default '
                                 f'{DeviceInformation.DEFAULT.PADDING} (only interesting values)')
        # ----------------------------------------------------------------------------
        for padding in compute_sup_values(
                HexList(Numeral(DeviceInformation.DEFAULT.PADDING,
                                self.feature_0003.get_device_info_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetDeviceInfo request with padding = {padding}')
            # ----------------------------------------------------------------------------
            get_device_info_report = self.feature_0003.get_device_info_cls(
                ChannelUtils.get_device_index(test_case=self), self.feature_0003_index)

            get_device_info_report.padding = padding

            get_device_info_response = ChannelUtils.send(
                test_case=self,
                report=get_device_info_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_info_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetDeviceInfo response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetDeviceInfoResponseChecker.check_fields(
                self, get_device_info_response, self.feature_0003.get_device_info_response_cls)
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.testCaseChecked("ROT_0003_0005")
    # end def test_get_device_info_padding_robustness

    @features('Feature0003')
    @level('Robustness')
    def test_get_fw_info_padding_robustness(self):
        """
        Validate getFwInfo robustness to padding
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the software ID other than the default '
                                 f'{DeviceInformation.DEFAULT.PADDING} (only interesting values)')
        # ----------------------------------------------------------------------------
        for padding in \
                compute_sup_values(
                    HexList(Numeral(DeviceInformation.DEFAULT.PADDING,
                                    self.feature_0003.get_fw_info_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetFwInfo request with entityIdx = 0 and padding = {padding}')
            # ----------------------------------------------------------------------------
            get_fw_info_report = self.feature_0003.get_fw_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index,
                entity_index=0)
            get_fw_info_report.padding = padding

            get_fw_info_response = ChannelUtils.send(
                test_case=self,
                report=get_fw_info_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_fw_info_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetFwInfo response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetFwInfoResponseChecker.check_fields(
                self, get_fw_info_response, self.feature_0003.get_fw_info_response_cls)
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.testCaseChecked("ROT_0003_0006")
    # end def test_get_fw_info_padding_robustness

    @features('Feature0003v4+')
    @level('Robustness')
    def test_get_device_serial_number_robustness(self):
        """
        Validate getDeviceSerialNumber robustness to padding
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the padding other than the default '
                                 f'{DeviceInformation.DEFAULT.PADDING} (only interesting values)')
        # ----------------------------------------------------------------------------
        for padding in compute_sup_values(HexList(Numeral(
                DeviceInformation.DEFAULT.PADDING,
                self.feature_0003.get_device_serial_number_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetDeviceSerialNumber request with padding = {padding}')
            # ----------------------------------------------------------------------------
            get_device_serial_number_report = \
                self.feature_0003.get_device_serial_number_cls(
                    device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index)

            get_device_serial_number_report.padding = padding

            get_device_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=get_device_serial_number_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_serial_number_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetDeviceSerialNumber response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetDeviceSerialNumberResponseChecker.check_fields(
                self, get_device_serial_number_response, self.feature_0003.get_device_serial_number_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.testCaseChecked("ROT_0003_0008")
    # end def test_get_device_serial_number_robustness

    @features('Feature0003v4+')
    @level('Robustness')
    def test_get_device_serial_number_software_id_robustness(self):
        """
        Validate getDeviceSerialNumber robustness to software ID
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over the software ID other than the default '
                                 f'{DeviceInformation.DEFAULT.SOFTWARE_ID} (only interesting values)')
        # ----------------------------------------------------------------------------
        for software_id in compute_wrong_range(
                value=DeviceInformation.DEFAULT.SOFTWARE_ID, max_value=0xF):
            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send GetDeviceSerialNumber request with softwareId = {software_id}')
            # ----------------------------------------------------------------------------
            get_device_serial_number_report = \
                self.feature_0003.get_device_serial_number_cls(
                    device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index)

            get_device_serial_number_report.softwareId = software_id

            get_device_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=get_device_serial_number_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_serial_number_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Wait for GetDeviceSerialNumber response and check product-specific constants')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetDeviceSerialNumberResponseChecker.check_fields(
                self, get_device_serial_number_response, self.feature_0003.get_device_serial_number_response_cls)

        # ----------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ----------------------------------------------------------------------------
        self.testCaseChecked("ROT_0003_0009")
    # end def test_get_device_serial_number_software_id_robustness
# end class DeviceInformationTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
