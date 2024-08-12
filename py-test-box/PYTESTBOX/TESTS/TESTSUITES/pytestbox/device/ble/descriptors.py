#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.descriptors
:brief: Validate BLE descriptors test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
# noinspection PyUnresolvedReferences
from pyhid.hid.blereportmap import HidGamingMouseReportMap
# Next lines add classes in the global symbol table which is used to retrieve the expected format from settings
# noinspection PyUnresolvedReferences
from pyhid.hid.blereportmap import HidGamingReportMap
# noinspection PyUnresolvedReferences
from pyhid.hid.blereportmap import HidMouseReportMap
# noinspection PyUnresolvedReferences
from pyhid.hid.blereportmap import HidReportMap
from pylibrary.tools.hexlist import HexList
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DescriptorsTestCases(DeviceBaseTestCase):
    """
    BLE descriptors Test Cases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features('BLEProtocol')
    @features('HidReportMap')
    @level('Functionality')
    @services('BleContext')
    @bugtracker('BLE_Unsupported_Report_Map')
    def test_report_map(self):
        """
        Test report map descriptor on a BLE device
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Get BLE Keyboard interface descriptor")
        # ---------------------------------------------------------------------------
        ble_descriptor = self.current_channel.get_interface_descriptor(interface=0)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check BLE descriptor fields {str(HexList(ble_descriptor))}")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=HexList(ble_descriptor),
                         expected=HexList(globals()[self.f.PRODUCT.PROTOCOLS.BLE.F_HidReportMap]()),
                         msg="The keyboard interface descriptor differs from the one expected")

        self.testCaseChecked("INT_BLE_DESC_0001")
    # end def test_report_map
# end class DescriptorsTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
