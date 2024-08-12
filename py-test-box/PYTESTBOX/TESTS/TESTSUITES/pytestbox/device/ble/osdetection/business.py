#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.osdetection.buisness
:brief: Validate BLE OS detection Business test cases
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2022/07/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pylibrary.mcu.nrf52.blenvschunks import BleNvsChunks
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import BleProPid
from pytestbox.device.base.bleprotocolutils import IosModelName
from pytestbox.device.base.bleprotocolutils import OsXModelName
from pytestbox.device.ble.osdetection.osdetection import OsDetectionTestCases


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
_AUTHOR = "Sylvana Ieri"


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class OsDetectionBusinessTestCases(OsDetectionTestCases):
    """
    BLE OS Detection Business Test Cases
    """

    @features('OsDetection')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_chrome_detection(self):
        """
        Verify the OS detected in NVS is Chrome when the Host DIS matches Google Chromebook characteristics
        """
        os_wanted = BleNvsChunks.OsDetectedType.CHROME
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to Chrome")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text='Check that the os detected in the device is Chrome although it is not declared as supported in the multi OS feature')
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(os_wanted=os_wanted)
        self.testCaseChecked("BUS_OS_DETEC_0002", _AUTHOR)
    # end def test_chrome_detection

    @features('OsDetection')
    @level('Business', 'SmokeTests')
    @services('BleContext')
    @services('Debugger')
    def test_osx_detection(self):
        """
        Verify the OS detected in NVS is OSX when the Host DIS matches Apple Mac characteristics

        """
        os_wanted = BleNvsChunks.OsDetectedType.OSX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over valid OSX names")
        # --------------------------------------------------------------------------------------------------------------
        for name in OsXModelName:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text=f"Change host OS emulation to OSX with name {name.value}")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted, name=name)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text='Check that the os detected in the device is OSX')
            # ----------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(os_wanted)
            self._reset_os_detection_test()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("BUS_OS_DETEC_0003", _AUTHOR)
    # end def test_osx_detection

    @features('OsDetection')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_ios_detection(self):
        """
        Verify the OS detected in NVS is IOS when the Host DIS matches Apple iPhone characteristics
        """
        os_wanted = BleNvsChunks.OsDetectedType.IOS
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over valid IOS names")
        # --------------------------------------------------------------------------------------------------------------
        for name in IosModelName:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text=f"Change host OS emulation to IOS with name {name.value}")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted, name=name)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text='Check that the os detected in the device is IOS')
            # ----------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(os_wanted)
            self._reset_os_detection_test()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("BUS_OS_DETEC_0004", _AUTHOR)
    # end def test_ios_detection

    @features('OsDetection')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_ble_pro_detection(self):
        """
        Verify the OS detected in NVS is BLE pro when the Host DIS matches Logitech device characteristics
        """
        os_wanted = BleNvsChunks.OsDetectedType.LOGITECH_BLE_PRO
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, f"Test Loop over PID from 0x{BleProPid.RANGE_START:x} to  0x{BleProPid.RANGE_END:x}")
        # --------------------------------------------------------------------------------------------------------------
        for pid in range(BleProPid.RANGE_START, BleProPid.RANGE_END+1):  # inclusively iterate through the range
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case=self, text=f"Change host OS emulation to BLE Pro with PID:0x{pid:04X}")
            # ----------------------------------------------------------------------------------------------------------
            BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted, ble_pro_pid=pid)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case=self, text='Check that the os detected in the device is BLE pro')
            # ----------------------------------------------------------------------------------------------------------
            self._scan_connect_encrypt_and_read_detected_os(os_wanted)
            self._reset_os_detection_test()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("BUS_OS_DETEC_0005", _AUTHOR)
    # end def test_ble_pro_detection

    @features('OsDetection')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_windows_detection(self):
        """
        Verify the OS detected in NVS is undetermined when the Host DIS matches Microsoft Windows characteristics
        """
        os_wanted = BleNvsChunks.OsDetectedType.UNDETERMINED  # used for windows
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to Windows")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text='Check that the os detected in the device is UNDETERMINED')
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(os_wanted)
        self.testCaseChecked("BUS_OS_DETEC_0007", _AUTHOR)
    # end def test_windows_detection

    @features('OsDetection')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    def test_linux_detection(self):
        """
        Verify the OS detected in NVS is undetermined is Linux when the Host DIS matches Linux characteristics.
        """
        os_wanted = BleNvsChunks.OsDetectedType.LINUX
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case=self, text="Change host OS emulation to Linux")
        # --------------------------------------------------------------------------------------------------------------
        BleProtocolTestUtils.change_host_os_emulation(test_case=self, os_emulation_type=os_wanted)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case=self, text='Check that the os detected in the device is UNDETERMINED')
        # --------------------------------------------------------------------------------------------------------------
        self._scan_connect_encrypt_and_read_detected_os(BleNvsChunks.OsDetectedType.UNDETERMINED)
        self.testCaseChecked("BUS_OS_DETEC_0008", _AUTHOR)
    # end def test_linux_detection
# end class OsDetectionBusinessTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
