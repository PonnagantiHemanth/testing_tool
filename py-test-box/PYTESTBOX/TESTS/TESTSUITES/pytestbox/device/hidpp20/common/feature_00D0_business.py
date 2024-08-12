#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00D0_business
:brief: Validates Device HID++ 2.0 Common feature 0x00D0
:author: Stanislas Cottard
:date: 2019/09/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from sys import stdout

from pychannel.blechannel import HidppPipe
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.dfu import Dfu
from pylibrary.emulator.ledid import LED_ID
from pytestbox.base.dfuprocessing import DeviceDfuTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.hidpp20.common.feature_00D0_business import GenericDfuOnTagTestCaseBusiness
from pytestbox.shared.hidpp20.common.feature_00D0_business import GenericDfuTestCaseBusiness
from pytestbox.shared.hidpp20.common.feature_00D0_business import SharedDfuOnTagTestCaseBusiness
from pytestbox.shared.hidpp20.common.feature_00D0_business import SharedDfuTestCaseBusiness


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DfuTestCaseBusiness(SharedDfuTestCaseBusiness, DeviceDfuTestCase):
    """
    Validate DFU Business TestCases
    """

    @features("Feature00D0")
    @features("NoGamingDevice")
    @level("Business")
    @services("Debugger")
    @services("LedIndicator")
    @services("RequiredLeds", (LED_ID.DEVICE_STATUS_GREEN_LED, LED_ID.DEVICE_STATUS_RED_LED,
                               LED_ID.CONNECTIVITY_STATUS_LED_1))
    @bugtracker("UnexpectedHostLEDBehaviourAfterDfu")
    def test_check_led_behaviour_on_dfu(self):
        """
        Check the Battery and Connectivity LEDs behaviour during DFU on a PWS product
        """
        self.generic_check_led_behaviour_on_dfu()

        self.testCaseChecked("FNT_00D0_0005#2")
    # end def test_check_led_behaviour_on_dfu
# end class DfuTestCaseBusiness


class DfuOnTagTestCaseBusiness(SharedDfuOnTagTestCaseBusiness, DeviceDfuTestCase):
    """
    Validate DFU Compatibility
    """
# end class DfuOnTagTestCaseBusiness


@features.class_decorator("BootloaderBLESupport")
class DfuDirectBleTestCaseBusiness(GenericDfuTestCaseBusiness, DeviceDfuTestCase):
    """
    Validate direct BLE DFU Business TestCases
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features('BLEProtocol')
    @features('Feature00D0')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    def test_complete_dfu_business(self):
        """
        Validate the DFU business case targeting the application entity in direct BLE.
        """
        self.generic_complete_dfu_business()

        self.testCaseChecked("BUS_BLE_00D0_0001#1")
    # end def test_complete_dfu_business

    @features('Feature00D0')
    @features('BLEProtocol')
    @features('NoGamingDevice')
    @level('Business')
    @services('BleContext')
    @services('Debugger')
    @services('LedIndicator')
    @services('RequiredLeds', (LED_ID.DEVICE_STATUS_GREEN_LED, LED_ID.DEVICE_STATUS_RED_LED,
                               LED_ID.CONNECTIVITY_STATUS_LED_1))
    @bugtracker("UnexpectedHostLEDBehaviourAfterDfu")
    def test_check_led_behaviour_on_dfu(self):
        """
        Check the Battery and Connectivity LEDs behaviour during DFU in direct BLE on a PWS product.
        """
        self.generic_check_led_behaviour_on_dfu()

        self.testCaseChecked("BUS_BLE_00D0_0001#2")
    # end def test_check_led_behaviour_on_dfu

    @features('BLEProtocol')
    @features('SecureDfuControlAnyReloadActionType')
    @features('SecureDfuControlChangeActionTypeByDFU')
    @features('Feature00D0')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    def test_change_action_type_by_dfu(self):
        """
        Check action type to enter in bootloader can be changed by DFU in direct BLE.

        JIRA: https://jira.logitech.io/browse/NRF52-121
        """
        self.generic_change_action_type_by_dfu()

        self.testCaseChecked("BUS_BLE_00D0_0002")
    # end def test_change_action_type_by_dfu

    @features('BLEProtocol')
    @features('Feature00D0SoftDevice')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    def test_soft_device_dfu_business(self):
        """
        Validate the DFU business case targeting the softdevice entity in direct BLE.
        """
        self.generic_soft_device_dfu_business()

        self.testCaseChecked("BUS_BLE_00D0_0003")
    # end def test_soft_device_dfu_business

    @features('BLEProtocol')
    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CBC)
    @level('ReleaseCandidate')
    @services("BleContext")
    @services('Debugger')
    def test_complete_dfu_business_aes_cbc(self):
        """
        Validate the DFU business case targeting the application entity with program data encrypted with AES algorithm
        in cipher-block chaining (CBC) in direct BLE.
        """
        self.generic_complete_dfu_business(encrypt_algorithm=Dfu.EncryptionMode.AES_CBC)

        self.testCaseChecked("BUS_BLE_00D0_0004")
    # end def test_complete_dfu_business_aes_cbc

    @features('BLEProtocol')
    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_CFB)
    @level('ReleaseCandidate')
    @services("BleContext")
    @services('Debugger')
    def test_complete_dfu_business_aes_cfb(self):
        """
        Validate the DFU business case targeting the application entity with program data encrypted with AES algorithm
        in cipher feedback (CFB) in direct BLE.
        """
        self.generic_complete_dfu_business(encrypt_algorithm=Dfu.EncryptionMode.AES_CFB)

        self.testCaseChecked("BUS_BLE_00D0_0005")
    # end def test_complete_dfu_business_aes_cfb

    @features('BLEProtocol')
    @features('Feature00D0EncryptCapabilities', Dfu.EncryptionMode.AES_OFB)
    @level('ReleaseCandidate')
    @services("BleContext")
    @services('Debugger')
    def test_complete_dfu_business_aes_ofb(self):
        """
        Validate the DFU business case targeting the application entity with program data encrypted with AES algorithm
        in output feedback (OFB) in direct BLE.
        """
        self.generic_complete_dfu_business(encrypt_algorithm=Dfu.EncryptionMode.AES_OFB)

        self.testCaseChecked("BUS_BLE_00D0_0006")
    # end def test_complete_dfu_business_aes_ofb
# end class DfuDirectBleTestCaseBusiness


class DfuOnTagDirectBleTestCaseBusiness(GenericDfuOnTagTestCaseBusiness, DeviceDfuTestCase):
    """
    Validate direct BLE DFU Compatibility
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    @features('BLEProtocol')
    @features('Feature00D0')
    @features('Feature00D0Tags', GenericDfuOnTagTestCaseBusiness.TAG1)
    @features('Bluetooth')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    @bugtracker('DFU_DirectBLEConnection')
    def test_dfu_over_first_tag(self):
        """
        Validate the DFU compatibility with a previous version (i.e. first given TAG) in direct BLE.
        """
        self._dfu_over_tag(self.TAG1)

        self.testCaseChecked("BUS_BLE_00D0_0007")
    # end def test_dfu_over_first_tag

    @features('BLEProtocol')
    @features('Feature00D0')
    @features('Feature00D0Tags', GenericDfuOnTagTestCaseBusiness.TAG2)
    @features('Bluetooth')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    @bugtracker('DFU_DirectBLEConnection')
    def test_dfu_over_second_tag(self):
        """
        Validate the DFU compatibility with a previous version (i.e. second given TAG) in direct BLE.
        """
        self._dfu_over_tag(self.TAG2)

        self.testCaseChecked("BUS_BLE_00D0_0008")
    # end def test_dfu_over_second_tag

    @features('BLEProtocol')
    @features('Feature00D0')
    @features('Feature00D0Tags', GenericDfuOnTagTestCaseBusiness.TAG3)
    @features('Bluetooth')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    @bugtracker('DFU_DirectBLEConnection')
    def test_dfu_over_third_tag(self):
        """
        Validate the DFU compatibility with a previous version (i.e. third given TAG) in direct BLE.
        """
        self._dfu_over_tag(self.TAG3)

        self.testCaseChecked("BUS_BLE_00D0_0009")
    # end def test_dfu_over_third_tag
# end class DfuOnTagDirectBleTestCaseBusiness


@features.class_decorator("BootloaderBLESupport")
class BleppDfuDirectBleTestCaseBusiness(GenericDfuTestCaseBusiness, DeviceDfuTestCase):
    """
    Validate direct BLE DFU Business TestCases but forcing the use of the BLE++ characteristic
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.BLE

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.original_hidpp_pipe = None
        self.post_requisite_set_hidpp_pipe_back_to_original = False

        super().setUp()

        self.original_hidpp_pipe = self.current_channel.get_hidpp_pipe()
        if self.original_hidpp_pipe != HidppPipe.BLEPP_SERVICE:
            # -----------------------------------------------------------------
            LogHelper.log_prerequisite(self, 'Force the use of BLE++ pipe')
            # -----------------------------------------------------------------
            self.current_channel.set_hidpp_pipe(hidpp_pipe=HidppPipe.BLEPP_SERVICE)
        else:
            # -----------------------------------------------------------------
            LogHelper.log_info(self, 'Already using of BLE++ pipe')
            # -----------------------------------------------------------------
            stdout.write(f"BLE++ pipe was improperly left as the default service for HID++ messages\n")
        # end if
        self.post_requisite_set_hidpp_pipe_back_to_original = True
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_set_hidpp_pipe_back_to_original:
                self.current_channel.set_hidpp_pipe(hidpp_pipe=self.original_hidpp_pipe)
                self.post_requisite_set_hidpp_pipe_back_to_original = False
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    @features('BLEProtocol')
    @features('Feature00D0SoftDevice')
    @level('Business')
    @services("BleContext")
    @services('Debugger')
    def test_soft_device_dfu_business(self):
        """
        Validate the DFU business case targeting the softdevice entity in direct BLE but forcing the use of the
        BLE++ characteristic.
        """
        self.generic_soft_device_dfu_business()

        self.testCaseChecked("BUS_BLEPP_00D0_0001")
    # end def test_soft_device_dfu_business
# end class BleppDfuDirectBleTestCaseBusiness

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
