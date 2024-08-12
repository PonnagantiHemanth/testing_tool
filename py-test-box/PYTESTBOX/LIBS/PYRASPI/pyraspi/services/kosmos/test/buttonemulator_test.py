#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.buttonemulator_test
:brief: Tests for Kosmos Button & Slider Controller
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/09/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.emulator.emulatorinterfaces import HOST
from pyraspi.services.kosmos.buttonemulator import KosmosButtonEmulator
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@require_kosmos_device(DeviceName.BAS)
class KosmosButtonEmulatorTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Button Emulator class.
    """
    DELAY = .5

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos and instantiate the Button emulator class
        """
        super().setUpClass()

        cls.button_emulator = KosmosButtonEmulator(kosmos=cls.kosmos, fw_id='RBM21')
    # end def setUpClass

    def test_passive_hold_press_support(self):
        """
        Validate passive_hold_press_support() method
        """
        self.assertTrue(self.button_emulator.passive_hold_press_support)
    # end def test_passive_hold_press_support

    def test_release_all(self):
        """
        Validate release_all() method
        """
        self.button_emulator.release_all()
    # end def test_release_all

    def test_change_host(self):
        """
        Validate change_host() method
        """
        self.button_emulator.change_host(host_index=HOST.CH1)
    # end def test_change_host

    def test_enter_pairing_mode(self):
        """
        Validate enter_pairing_mode() method
        """
        self.button_emulator.enter_pairing_mode(host_index=HOST.CH2)
        self.button_emulator.change_host(host_index=HOST.CH1)
    # end def test_enter_pairing_mode

    def test_keystroke(self):
        """
        Validate keystroke() method.
        """
        key_id = self.button_emulator.keyword_key_ids["user_action"]
        # Check all parameters except 'key_id' are optional
        self.button_emulator.keystroke(key_id)
        # Check all parameters could be updated
        self.button_emulator.keystroke(key_id, duration=KosmosButtonEmulatorTestCase.DELAY, repeat=2,
                                       delay=KosmosButtonEmulatorTestCase.DELAY)
    # end def test_keystroke

    def test_key_press(self):
        """
        Validate key_press() method.
        """
        for key_id in self.button_emulator._button_layout.KEYS.keys():
            self.button_emulator.key_press(key_id)
        # end for
    # end def test_key_press

    def test_key_release(self):
        """
        Validate key_release() method.
        """
        for key_id in self.button_emulator._button_layout.KEYS.keys():
            self.button_emulator.key_release(key_id)
        # end for
    # end def test_key_release

    def test_multiple_keys_press(self):
        """
        Validate multiple_keys_press() method.
        """
        key_ids = list(self.button_emulator._button_layout.KEYS.keys())[:3]
        # Check all parameters except 'key_ids' are optional
        self.button_emulator.multiple_keys_press(key_ids)
        # Check all parameters could be updated
        self.button_emulator.multiple_keys_press(key_ids, delay=KosmosButtonEmulatorTestCase.DELAY)
    # end def test_multiple_keys_press

    def test_multiple_keys_release(self):
        """
        Validate multiple_keys_release() method.
        """
        key_ids = list(self.button_emulator._button_layout.KEYS.keys())[:3]
        # Check all parameters except 'key_ids' are optional
        self.button_emulator.multiple_keys_release(key_ids)
        # Check all parameters could be updated
        self.button_emulator.multiple_keys_release(key_ids, delay=KosmosButtonEmulatorTestCase.DELAY)
    # end def test_multiple_keys_release

    def test_get_key_id_list(self):
        """
        Validate get_key_id_list() method
        """
        self.assertEqual(self.button_emulator._button_layout.KEYS.keys(), self.button_emulator.get_key_id_list())
    # end def test_get_key_id_list

    def test_user_action(self):
        """
        Validate user_action() method.
        """
        self.button_emulator.user_action()
    # end def test_user_action

    def test_simultaneous_keystroke(self):
        """
        Validate simultaneous_keystroke() method.
        """
        key_ids = list(self.button_emulator._button_layout.KEYS.keys())[:3]
        # Check all parameters except 'key_ids' are optional
        self.button_emulator.simultaneous_keystroke(key_ids)
        # Check all parameters could be updated
        self.button_emulator.simultaneous_keystroke(key_ids, duration=KosmosButtonEmulatorTestCase.DELAY)
    # end def test_simultaneous_keystroke
# end class KosmosButtonEmulatorTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
