#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.usb.bootprotocol
:brief: Validate USB Boot protocol test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/03/14
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features, services
from pyhid.hiddata import HidData
from pyhid.hiddata import OS
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytransport.usb.usbconstants import HidClassSpecificRequest


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedBootProtocolTestCases(CommonBaseTestCase):
    """
    USB Boot Protocol Test Cases
    """

    def tearDown(self):
        # noinspection PyBroadException
        try:
            # Force back the Device Protocol
            self.current_channel.hid_class_specific_request(
                b_request=HidClassSpecificRequest.SET_PROTOCOL,
                interface_id=0,  # index is ignored in this context
                w_value=HidData.Protocol.REPORT)

            # Re-configure the HID report types and HID Guidelines version from test settings
            HidData.set_protocol(mode=HidData.Protocol.REPORT)
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try
        super().tearDown()
    # end def tearDown

    @features('USBProtocol')
    @level('Business', 'SmokeTests')
    def test_set_get_protocol(self):
        """
        Test USB SetProtocol & GetProtocol requests API
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send SetProtocol request to the DUT")
        # ---------------------------------------------------------------------------
        self.current_channel.hid_class_specific_request(
            b_request=HidClassSpecificRequest.SET_PROTOCOL,
            interface_id=0,  # index is ignored in this context
            w_value=HidData.Protocol.BOOT)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f"Send GetProtocol request to the DUT")
        # ---------------------------------------------------------------------------
        message = self.current_channel.hid_class_specific_request(
            b_request=HidClassSpecificRequest.GET_PROTOCOL,
            interface_id=0,  # index is ignored in this context
            w_length=1)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check protocol field in response")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=to_int(message.data),
                         expected=HidData.Protocol.BOOT,
                         msg="The keyboard interface descriptor differs from the one expected")

        self.testCaseChecked("BUS_BOOT_0001")
    # end def test_set_get_protocol

    @features('USBProtocol')
    @level('Business')
    @services('KeyMatrix')
    def test_single_keystroke(self):
        """
        Test USB Keyboard report in boot protocol mode when the user does a single keystroke
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetProtocol request to the DUT")
        # ---------------------------------------------------------------------------
        self.current_channel.hid_class_specific_request(
            b_request=HidClassSpecificRequest.SET_PROTOCOL,
            interface_id=0,  # index is ignored in this context
            w_value=HidData.Protocol.BOOT)

        # Re-configure the HID Keyboard and Mouse reports to match the format defined for the boot protocol
        HidData.set_protocol(mode=HidData.Protocol.BOOT)

        self.kosmos.sequencer.offline_mode = True
        keys = KeyMatrixTestUtils.get_key_list(
            self, group_count=None, group_size=1, random=False)

        for (key_id, ) in keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate a keystroke on the supported key {str(key_id)}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.keystroke(key_id=key_id, duration=.2, repeat=1, delay=.2)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for (key_id, ) in keys:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check HID Keyboard reports on key id {str(key_id)}')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                          variant=OS.BOOT)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                          variant=OS.BOOT)
        # end for

        self.testCaseChecked("FUN_BOOT_0001")
    # end def test_single_keystroke

    @features('USBProtocol')
    @level('Functionality')
    @services('KeyMatrix')
    def test_double_keystroke(self):
        """
        Test USB Keyboard report in boot protocol mode when the user does a double keystroke
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send SetProtocol request to the DUT")
        # ---------------------------------------------------------------------------
        self.current_channel.hid_class_specific_request(
            b_request=HidClassSpecificRequest.SET_PROTOCOL,
            interface_id=0,  # index is ignored in this context
            w_value=HidData.Protocol.BOOT)

        # Re-configure the HID Keyboard and Mouse reports to match the format defined for the boot protocol
        HidData.set_protocol(mode=HidData.Protocol.BOOT)

        self.kosmos.sequencer.offline_mode = True
        pair_of_keys_list = KeyMatrixTestUtils.get_key_list(self, group_count=None, group_size=2, random=True)

        for key_pair in pair_of_keys_list:
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate pressing the key pair {str(key_pair[0])} & {str(key_pair[1])}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_press(key_ids=key_pair, delay=.2)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate releasing the key pair {str(key_pair[0])} & {str(key_pair[1])}')
            # ---------------------------------------------------------------------------
            self.button_stimuli_emulator.multiple_keys_release(key_ids=key_pair, delay=.2)
        # end for

        self.kosmos.sequencer.offline_mode = False
        # Upload the complete scenario into the Kosmos
        self.kosmos.sequencer.play_sequence(block=False)

        for key_pair in pair_of_keys_list:
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check HID Keyboard report ')
            # ---------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_pair[0], MAKE),
                                                          variant=OS.BOOT)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_pair[1], MAKE),
                                                          variant=OS.BOOT)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_pair[0], BREAK),
                                                          variant=OS.BOOT)

            KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self,
                                                          key=KeyMatrixTestUtils.Key(key_pair[1], BREAK),
                                                          variant=OS.BOOT)
        # end for

        self.testCaseChecked("FUN_BOOT_0002")
    # end def test_double_keystroke

# end class SharedBootProtocolTestCases

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
