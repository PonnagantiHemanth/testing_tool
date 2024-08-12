#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.keyboard.feature_4521.disablekeys
:brief: Base for HID++ 2.0 DisableKeys test suites
:author: YY Liu <yliu5@logitech.com>
:date: 2021/12/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeys
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeysFactory
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.disablekeysutils import DisableKeysUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisableKeysBaseTestCase(DeviceBaseTestCase):
    """
    Base test case class for 0x4521 - DisableKeys test case implementation
    """
    def setUp(self):
        """
        Handle test pre-requisites
        """
        super().setUp()

        # ----------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x4521)')
        # ----------------------------------------------------------------------------
        self.feature_4521_index, self.feature_4521, _, _ = DisableKeysUtils.HIDppHelper.get_parameters(
            self, feature_id=DisableKeys.FEATURE_ID, factory=DisableKeysFactory)

        # Common Variables
        self.default_disabled_keys = self.f.PRODUCT.FEATURES.KEYBOARD.DISABLE_KEYS.F_DefaultDisabledKeys
        self.all_disableable_keys = DisableKeysUtils.convert_disableable_keys_to_key_id(self)
    # end def setUp

    def check_key_disabled(self, key_id):
        """
        Check host does not receive keystroke reports from the DUT

        :param key_id: The key which the user strokes
        :type key_id: ``KEY_ID``

        :raise: ``TestException``: If the HID message queue is not empty
        """
        self.assertEqual(expected=True,
                         obtained=self.current_channel.hid_dispatcher.hid_message_queue.empty(),
                         msg=f'The host should not received {str(key_id)} key report from the DUT after the key'
                             f' was disabled')
    # end def check_key_disabled

    def check_key_enabled(self, key_id):
        """
        Check host can receive keystroke reports from the DUT

        :param key_id: The key which the user strokes
        :type key_id: ``KEY_ID``

        :raise: ``TestException``: If check fails
        """
        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, MAKE),
                                                      raise_exception=True)

        KeyMatrixTestUtils.check_hid_report_by_key_id(test_case=self, key=KeyMatrixTestUtils.Key(key_id, BREAK),
                                                      raise_exception=True)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Verify no HID report was missing')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=KeyMatrixTestUtils.get_missing_report_counter(self),
                         msg='Some HID reports were missing')
    # end def check_key_enabled
# end class DisableKeysBaseTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
