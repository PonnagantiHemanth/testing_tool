#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_0003
:brief: Validates Device HID++ 2.0 Common feature 0x0003
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/11/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.bootloadertest import DeviceBootloaderTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.configurabledevicepropertiesutils import ConfigurableDevicePropertiesTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytestbox.shared.hidpp20.common.feature_0003 import DeviceInformationTestCaseMixin
from pytestbox.shared.hidpp20.common.feature_0003 import SharedDeviceInformationTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ApplicationDeviceInformationTestCase(SharedDeviceInformationTestCase, DeviceBaseTestCase):
    """
    Validate Device information TestCases in Application mode
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_reload_nvs = False

        # Start with super setUp()
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp

    def tearDown(self):
        """
        Handles post-requisites
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_reload_nvs:
                # ---------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload initial NVS')
                # ---------------------------------------------------------------------------
                CommonBaseTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try
        super().tearDown()
    # end def tearDown

    @features('Feature0003v4+')
    @features('Feature1806')
    @level('Functionality')
    @services('HardwareReset')
    def test_get_device_serial_number_range(self):
        """
        Validate getDeviceSerialNumber range
        """
        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get feature 0x1806 index')
        # ----------------------------------------------------------------------------
        self.feature_1806_index, self.feature_1806, _, _ = \
            ConfigurableDevicePropertiesTestUtils.HIDppHelper.get_parameters(self, update_test_case=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Backup NVS')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)
        self.post_requisite_reload_nvs = True

        for serial_number in [HexList('00' * self.feature_1806.property_size.SERIAL_NUMBER),
                              HexList('323031354c5a3036445a4e38'),
                              HexList('00' * self.feature_1806.property_size.SERIAL_NUMBER)]:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Enable Manufacturing features')
            # ---------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setDeviceProperties (0x1806) request to set all serial number bytes '
                                     f'to {serial_number}')
            # ----------------------------------------------------------------------------
            serial_number_property_data = HexList(serial_number)
            set_serial_number = self.feature_1806.set_device_properties_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1806_index,
                property_id=self.feature_1806.property_id.SERIAL_NUMBER, flag=0, sub_data_index=0,
                property_data=serial_number_property_data)
            ChannelUtils.send(
                test_case=self,
                report=set_serial_number,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1806.set_device_properties_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getDeviceProperties (0x1806) request to get serial number')
            # ----------------------------------------------------------------------------
            get_serial_number = self.feature_1806.get_device_properties_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1806_index,
                property_id=self.feature_1806.property_id.SERIAL_NUMBER, flag=0, sub_data_index=0,)
            get_device_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=get_serial_number,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_1806.get_device_properties_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check serial number is {serial_number}')
            # ----------------------------------------------------------------------------
            self.assertEqual(serial_number_property_data, get_device_serial_number_response.property_data,
                             "The serial_number parameter differs from the one expected")

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Send getDeviceSerialNumber (0x0003) request to get serial number')
            # ----------------------------------------------------------------------------
            get_device_serial_number_report = self.feature_0003.get_device_serial_number_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index)

            get_device_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=get_device_serial_number_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_serial_number_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check serial number is {serial_number}')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetDeviceSerialNumberResponseChecker.check_device_serial_number(
                test_case=self,
                get_device_serial_number_response=get_device_serial_number_response,
                expected=serial_number)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Turn off / on the power to the device using the power supply service')
            # ---------------------------------------------------------------------------
            self.reset(hardware_reset=True)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, 'Send getDeviceSerialNumber (0x0003) request to get serial number')
            # ----------------------------------------------------------------------------
            get_device_serial_number_report = \
                self.feature_0003.get_device_serial_number_cls(
                    device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_0003_index)

            get_device_serial_number_response = ChannelUtils.send(
                test_case=self,
                report=get_device_serial_number_report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.feature_0003.get_device_serial_number_response_cls)

            # ----------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check serial number is {serial_number} after the reset')
            # ----------------------------------------------------------------------------
            DeviceInformationTestUtils.GetDeviceSerialNumberResponseChecker.check_device_serial_number(
                test_case=self,
                get_device_serial_number_response=get_device_serial_number_response,
                expected=serial_number)
        # end for loop
        self.testCaseChecked("FNT_0003_0005")
    # end def test_get_device_serial_number_range
# end class ApplicationDeviceInformationTestCase


@features.class_decorator("BootloaderAvailable", inheritance=SharedDeviceInformationTestCase)
class BootloaderDeviceInformationTestCase(SharedDeviceInformationTestCase, DeviceBootloaderTestCase):
    """
    Validate Device information TestCases in Bootloader
    """
    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()
        
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp
# end class BootloaderDeviceInformationTestCase


class ApplicationDeviceInformationUsbTestCase(DeviceInformationTestCaseMixin, DeviceBaseTestCase):
    """
    Validate Device information TestCases in Application mode while the DUT is connected through USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_reload_nvs = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp

    @features('Feature0003')
    @features('USB')
    @features('Wireless')
    @level('Business')
    def test_get_device_info_get_fw_info_business(self):
        """
        Validate getDeviceInfo GetFwInfo business case while the DUT is connected through USB protocol
        """
        self.generic_get_device_info_get_fw_info_business()

        self.testCaseChecked("FNT_0003_0003")
    # end def test_get_device_info_get_fw_info_business

    @features('Feature0003v4+')
    @features('USB')
    @features('Wireless')
    @level('Interface')
    def test_get_device_serial_number_api(self):
        """
        Validate getDeviceSerialNumber interface, introduced in version 4 while the DUT is connected through USB
        protocol
        """
        self.generic_get_device_serial_number_api()

        self.testCaseChecked("FNT_0003_0004")
    # end def test_get_device_serial_number_api
# end class ApplicationDeviceInformationUsbTestCase


@features.class_decorator("BootloaderAvailable")
class BootloaderDeviceInformationUsbTestCase(DeviceInformationTestCaseMixin, DeviceBootloaderTestCase):
    """
    Validate Device information TestCases in Application mode while the DUT is in bootloader mode and
    connected through USB protocol
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB

    def setUp(self):
        """
        Handle test prerequisites.
        """
        # Bypass direct parent setUp and call DeviceBootloaderTestCase setUp
        DeviceBaseTestCase.setUp(self)

        if self.debugger is not None:
            # -----------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Backup initial NVS')
            # -----------------------------------------------------------------
            self.memory_manager.read_nvs(backup=True)
        # end if

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Force the DUT in bootloader mode')
        # ----------------------------------------------------------------------------
        self.dut_jump_on_bootloader()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x0003 index")
        # --------------------------------------------------------------------------------------------------------------
        self.feature_0003_index, self.feature_0003, _, _ = DeviceInformationTestUtils.HIDppHelper.get_parameters(
            self, update_test_case=True)
    # end def setUp

    def tearDown(self):
        """
        Handle post-requisites
        """
        # noinspection PyBroadException
        with self.manage_post_requisite():
            # ---------------------------------------------------------------------------
            LogHelper.log_post_requisite(test_case=self, text="Restart in Main Application mode")
            # ---------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self)

            # ---------------------------------------------------------------------------
            LogHelper.log_post_requisite(test_case=self, text="Verify the DUT is in Application mode")
            # ---------------------------------------------------------------------------
            DfuTestUtils.verify_device_on_fw_type(test_case=self,
                                                  fw_type=DeviceInformation.EntityTypeV1.MAIN_APP)
        # end with
        super().tearDown()
    # end def tearDown

    @features('Feature0003')
    @features('USB')
    @features('Wireless')
    @level('Business')
    def test_get_device_info_get_fw_info_business(self):
        """
        Validate getDeviceInfo GetFwInfo business case while the DUT is in bootloader mode and connected through USB
        protocol
        """
        self.generic_get_device_info_get_fw_info_business()

        self.testCaseChecked("FNT_0003_0003")
    # end def test_get_device_info_get_fw_info_business

    @features('Feature0003v4+')
    @features('USB')
    @features('Wireless')
    @level('Interface')
    def test_get_device_serial_number_api(self):
        """
        Validate getDeviceSerialNumber interface, introduced in version 4 while the DUT is in bootloader mode and
        connected through USB protocol
        """
        self.generic_get_device_serial_number_api()

        self.testCaseChecked("FNT_0003_0004")
    # end def test_get_device_serial_number_api
# end class BootloaderDeviceInformationUsbTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
