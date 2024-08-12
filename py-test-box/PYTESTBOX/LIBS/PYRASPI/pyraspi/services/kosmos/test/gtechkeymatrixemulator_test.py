#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.test.gtechkeymatrixemulator_test
:brief: Test for Kosmos Gtech Keymatrix Emulator
:author: Lila Viollette <lviollette@logitech.com>
:date: 2024/04/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from abc import abstractmethod
from itertools import cycle
from itertools import islice
from typing import Dict

from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.gtechkeymatrixemulator import GTECH_KEY_PRESS_LEVEL
from pyraspi.services.kosmos.gtechkeymatrixemulator import GTECH_KEY_RELEASE_LEVEL
from pyraspi.services.kosmos.gtechkeymatrixemulator import KosmosGtechKeyMatrixEmulator
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.kbdgtech import KBD_GTECH_EMU_MODE
from pyraspi.services.kosmos.module.kbdgtech import KbdGtechModule
from pyraspi.services.kosmos.module.test.kbdgtech_test import GALVATRON_BOOT_UP_DURATION_S
from pyraspi.services.kosmos.module.test.kbdgtech_test import GALVATRON_KBD_FW_ID
from pyraspi.services.kosmos.module.test.kbdgtech_test import GALVATRON_USB_HUB_PORT_INDEX
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.test.common_test import KosmosCommonTestCase
from pyraspi.services.kosmos.test.usbhubutils import UsbHubTestCaseUtils
from pytransport.usb.usbhub.usbhubconstants import UsbHubAction

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

VERBOSE = False  # Toggle verbose mode for this Unit Test file


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class GtechKeymatrixEmulatorAbstractTestCase:
    """
    This class is used to wrap Abstract TestCase classes, so that they cannot be automatically discovered
    and executed by test executors (unittest, pytest...).

    Refer to ``pyraspi.services.kosmos.module.test.module_test.AbstractTestClass``
    """


    class PowerBaseTestCase(UsbHubTestCaseUtils, metaclass=ABCMeta):
        """
        Kosmos KBD Gtech Module Power Base Test Class (handles power on/off).

        This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (rightmost port).
        """

        @classmethod
        def setUpClass(cls):
            """
            Setup KosmosGtechKeyMatrixEmulator class
            """
            super().setUpClass()
            cls.power_off()
        # end def setUpClass


        def setUp(self):
            """
            Setup test
            """
            super().setUp()
            self.power_on()
        # end def setUp

        def tearDown(self):
            """
            TearDown test
            """
            self.power_off()
            super().tearDown()
        # end def tearDown

        @classmethod
        def power_on(cls):
            """
            Power ON the keyboard.
            """
            cls.set_usb_port(port_index=GALVATRON_USB_HUB_PORT_INDEX, status=UsbHubAction.ON,
                             delay=GALVATRON_BOOT_UP_DURATION_S)
        # end def power_on

        @classmethod
        def power_off(cls):
            """
            Power OFF the keyboard.
            """
            cls.set_usb_port(port_index=GALVATRON_USB_HUB_PORT_INDEX, status=UsbHubAction.OFF)
        # end def power_off
    # end class PowerBaseTestCase

    @require_kosmos_device(DeviceName.KBD_GTECH)
    class BaseTestCase(KosmosCommonTestCase, PowerBaseTestCase, metaclass=ABCMeta):
        """
        Kosmos KBD Gtech Module Base Test Class.
        """
        # Update type hints
        module: KbdGtechModule
        kbd_emu: KosmosGtechKeyMatrixEmulator

        @classmethod
        def setUpClass(cls):
            """
            Setup KosmosGtechKeyMatrixEmulator class
            """
            super().setUpClass()

            cls._setup_emulator_under_test()
            cls.VERBOSE = VERBOSE  # Set KosmosCommonTestCase.VERBOSE mode
        # end def setUpClass

        def setUp(self):
            """
            Setup test
            """
            self.kbd_emu.setup_defaults()
            super().setUp()
        # end def setUp

        @classmethod
        def _setup_emulator_under_test(cls):
            """
            Setup the Emulator under test
            """
            cls.kbd_emu = KosmosGtechKeyMatrixEmulator(kosmos=cls.kosmos, fw_id=GALVATRON_KBD_FW_ID, verbose=VERBOSE)
        # end def _setup_emulator_under_test
    # end class BaseTestCase

    class MixinBaseTestCase(BaseTestCase, metaclass=ABCMeta):
        """
        Kosmos KBD Gtech Module Mixin Base Test Class (add abstract and concrete test methods).
        """

        @property
        @abstractmethod
        def key_ids_under_test(self):
            """
            Return a mapping of KEY_ID to be tested.

            :return: collection of KEY_ID to be tested
            :rtype: ``Dict[KEY_ID, int] or Dict[KEY_ID, Tuple[int, int]]``
            """
            raise NotImplementedAbstractMethodError()
        # end def property getter key_ids_under_test

        @abstractmethod
        def test_get_bank_lane_addr(self):
            """
            Test of `KbdGtechModule.get_bank_lane_addr` method.
            """
            raise NotImplementedAbstractMethodError()
        # end def test_get_bank_lane_addr

        @abstractmethod
        def test_release_all(self):
            """
           Validate `KbdGtechModule.release_all` method is not blocking, independently of `emu_mode`.
            """
            raise NotImplementedAbstractMethodError()
        # end def test_release_all

        @abstractmethod
        def test_release_all_complete(self):
            """
           Validate `KbdGtechModule.release_all` method is not blocking, independently of `emu_mode`.
            """
            raise NotImplementedAbstractMethodError()
        # end def test_release_all_complete

        def test_keystroke(self):
            """
            Validate `KbdGtechModule.keystroke` method is actuating each key sequentially.
            """
            keypress_duration_s = .005
            keyrelease_duration_s = .010
            test_duration = ((keypress_duration_s + keyrelease_duration_s) *
                             len(self.key_ids_under_test) + 1)

            # Prepare PES sequence
            self.kosmos.sequencer.offline_mode = True

            # Press then Release each key
            for key_id in self.key_ids_under_test:
                self.kbd_emu.keystroke(key_id=key_id, duration=keypress_duration_s, delay=keyrelease_duration_s)
            # end for

            # Execute PES sequence
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(timeout=test_duration)
        # end def test_keystroke

        def test_key_press_key_release(self):
            """
            Validate `KbdGtechModule.key_press` and `KbdGtechModule.key_release` methods are actuating each key
            sequentially.
            """
            # Prepare PES sequence
            self.kosmos.sequencer.offline_mode = True

            # Press each key
            for key_id in self.key_ids_under_test:
                self.kbd_emu.key_press(key_id=key_id)
            # end for

            # Release each key
            for key_id in self.key_ids_under_test:
                self.kbd_emu.key_release(key_id=key_id)
            # end for

            # Execute PES sequence
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()
        # end def test_key_press_key_release
    # end class MixinBaseTestCase

    class LegacyKbdGtechBaseTestCase(MixinBaseTestCase, metaclass=ABCMeta):
        """
        Kosmos KBD Gtech Module Test Class related to KBD functional mode: Legacy
        (Key Press & Key Release ony).

        This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
        """

        @property
        def key_ids_under_test(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.key_ids_under_test``
            return self.kbd_emu.keyboard_layout.KEYID_2_CHAINID
        # end def property getter key_ids_under_test

        def test_get_bank_lane_addr(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_get_bank_lane_addr``

            # Print all transformations KEYID to FPGA memory layout
            if self.VERBOSE:
                for key_id, chain_id in self.key_ids_under_test.items():
                    bank, lane, addr = self.kbd_emu.get_bank_lane_addr(key_id=key_id)
                    context = f'addr: {addr:2}, bank: {bank}, lane: {lane:2} <=> chain_id: {chain_id:2}, key_id: {key_id!r}'
                    print(context)
                # end for
            # end if

            # Validate all transformations KEYID to FPGA memory layout
            bank_prev, lane_prev, addr_prev = None, None, None
            for i, (key_id, chain_id) in enumerate(self.key_ids_under_test.items()):
                bank, lane, addr = self.kbd_emu.get_bank_lane_addr(key_id=key_id)
                context = f'addr: {addr:2}, bank: {bank}, lane: {lane:2} <=> chain_id: {chain_id:2}, key_id: {key_id!r}'
                if bank_prev is not None:
                    self.assertEqual((i // 6) % 2, bank, msg=context)
                    self.assertEqual(i // 12, addr, msg=context)
                    if lane == 0:
                        self.assertEqual(lane_prev, 5, msg=context)
                        if addr:
                            if bank:
                                self.assertEqual(addr_prev, addr, msg=context)
                            else:
                                self.assertEqual(addr_prev, addr - 1, msg=context)
                            # end if
                        # end if
                    else:
                        self.assertEqual(lane_prev, lane - 1, msg=context)
                        self.assertEqual(addr_prev, addr, msg=context)
                    # end if
                # end if
                bank_prev, lane_prev, addr_prev = bank, lane, addr
            # end for

            addr_count = self.kbd_emu.kbd.settings.kbd_addr_count
            test_memory = [
                [0x00 for _ in range(addr_count)],  # bank 0
                [0x00 for _ in range(addr_count)]  # bank 1
            ]

            for key_id, chain_id in self.key_ids_under_test.items():
                bank, lane, addr = self.kbd_emu.get_bank_lane_addr(key_id=key_id)
                context = f'addr: {addr:2}, bank: {bank}, lane: {lane:2} <=> chain_id: {chain_id:2}, key_id: {key_id!r}'
                mem_lut = test_memory[bank][addr]
                self.assertEqual(0, mem_lut & (1 << lane), msg=context)
                test_memory[bank][addr] = mem_lut | (1 << lane)
            # end for

            # Print all transformations KEYID to FPGA Bank memory content
            if self.VERBOSE:
                print('-' * 80)
                for bank, test_bank in enumerate(test_memory):
                    print(f'Bank[{bank}] = ' + ', '.join(f'{mem_lut:#02x}' for mem_lut in test_bank))
                # end for
            # end if

            # Validate all transformations KEYID to FPGA Bank memory content
            for bank, test_bank in enumerate(test_memory):  # values: 0, 1
                for addr, test_lane in enumerate(test_bank):  # values: 0 to 63
                    msg = f'test_memory[{bank}]={test_bank}, test_memory[{bank}][{addr}]={test_lane}'
                    if addr < 7:
                        self.assertEqual(0x3F, test_lane, msg=msg)
                    elif addr == 7:
                        pass  # content may vary depending on keyboard layout
                    else:
                        self.assertEqual(0x00, test_lane, msg=msg)
                    # end if
                # end for
            # end for
        # end def test_get_bank_lane_addr

        def test_release_all(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_release_all``
            # Reset all keys, while KBD Emulator mode is EMULATED
            self.kbd_emu.release_all()

            # Disable Kosmos Gtech Keyboard Emulator
            self.kbd_emu.kbd.emu_mode_msg(KBD_GTECH_EMU_MODE.REAL)
            # Reset all keys, while KBD Emulator mode is REAL
            self.kbd_emu.release_all()
        # end def test_release_all

        def test_release_all_complete(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_release_all_complete``

            # Press each key
            for key_id in self.key_ids_under_test.keys():
                self.kbd_emu.key_press(key_id=key_id)
            # end for

            self.kbd_emu.release_all()
        # end def test_release_all_complete
    # end class LegacyKbdGtechBaseTestCase

    class AnalogKbdGtechBaseTestCase(MixinBaseTestCase, metaclass=ABCMeta):
        """
        Kosmos KBD Gtech Module Test Class related to KBD functional mode: Analog
        (Key Release: displacement level 0 / Key Press displacement level 40)

        This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
        """

        def setUp(self):
            """
            Setup test
            """
            super().setUp()

            # Change KBD Functional Mode from Legacy to Analog
            self.kbd_emu.kbd.func_mode_analog()
        # end def setUp

        @property
        def key_ids_under_test(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.key_ids_under_test``
            return self.kbd_emu.keyboard_layout.KEYID_2_CHAINID
        # end def property getter key_ids_under_test

        def test_get_bank_lane_addr(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_get_bank_lane_addr``

            # Validate all transformations KEYID to FPGA memory layout
            for i, (key_id, chain_id) in enumerate(self.key_ids_under_test.items()):
                bank, lane, addr = self.kbd_emu.get_bank_lane_addr(key_id=key_id)
                context = f'addr: {addr:2}, bank: {bank}, lane: {lane:2} <=> chain_id: {chain_id:2}, key_id: {key_id!r}'
                self.printd(context)
                self.assertEqual(i & 1, bank, msg=context)
                self.assertEqual(0x00, lane, msg=context)
                self.assertEqual(i >> 1, addr, msg=context)
            # end for
        # end def test_get_bank_lane_addr

        def test_release_all(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_release_all``

            # Press a key
            self.kbd_emu.key_displacement(key_id=KEY_ID.KEYBOARD_L, displacement=33)

            # Reset all keys
            self.kbd_emu.release_all()
        # end def test_release_all

        def test_release_all_complete(self):
            # See ``GtechKeymatrixEmulatorAbstractTestCase.BaseTestCase.test_release_all_complete``

            # Set displacement for each keys
            for key_id, displacement in zip(self.key_ids_under_test,
                                            cycle(range(GTECH_KEY_RELEASE_LEVEL + 1, GTECH_KEY_PRESS_LEVEL + 1))):
                self.kbd_emu.key_displacement(key_id=key_id, displacement=displacement)
            # end for

            # Reset all keys
            self.kbd_emu.release_all()
        # end def test_release_all_complete

        def test_key_displacement(self):
            """
            Validate `KbdGtechModule.key_displacement` method.
            Validate KBD instructions: KBD_COMMAND_UPDATE_SEND, KBD_COMMAND_RESET.

            Loop though the first 10 keys. Set one key at a time to a specific displacement level.
            Increase displacement after each key loop.

            """
            test_duration = 0
            test_key_count = 10

            # Prepare PES sequence
            self.kosmos.sequencer.offline_mode = True

            # Key Press then Key Release
            for key_id in islice(self.key_ids_under_test.keys(), test_key_count):
                for displacement in range(GTECH_KEY_RELEASE_LEVEL, GTECH_KEY_PRESS_LEVEL + 1):
                    self.kbd_emu.key_displacement(key_id=key_id, displacement=displacement)
                    test_duration += 0.001
                # end for
            # end for

            # Execute PES sequence
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence(timeout=test_duration + 2)

            # Reset all keys
            self.kbd_emu.release_all()
        # end def test_key_displacement

        def test_key_displacement_all_range_all_keys(self):
            """
            Validate `KbdGtechModule.key_displacement` method.
            Validate KBD instructions: KBD_COMMAND_UPDATE, KBD_COMMAND_UPDATE_SEND, KBD_COMMAND_RESET.

            Set all keys at the same time, to each displacement levels 0-40
            """

            key_ids = list(self.key_ids_under_test.keys())

            test_fifo_fill_delay = 1e-4  # time required to re-fill the FPGA FIFOs (conservative value)
            test_duration = len(key_ids) * test_fifo_fill_delay

            # Run a test sequence for each displacement value
            for displacement in range(GTECH_KEY_RELEASE_LEVEL, GTECH_KEY_PRESS_LEVEL + 1):
                # Prepare PES sequence
                self.kosmos.sequencer.offline_mode = True

                # Update each key's displacement value
                for key_id in key_ids:
                    update_only = (key_id != key_ids[-1])  # Update if not last key; update+send all when last key
                    self.kbd_emu.key_displacement(key_id=key_id, displacement=displacement, update_only=update_only)
                    self.kosmos.pes.delay(delay_s=test_fifo_fill_delay)
                # end for

                # Execute PES sequence
                self.kosmos.sequencer.offline_mode = False
                self.kosmos.sequencer.play_sequence(timeout=test_duration + 2)
            # end for

            # Reset all keys
            self.kbd_emu.release_all()
        # end def test_key_displacement_all_range_all_keys
    # end class AnalogKbdGtechBaseTestCase
# end class GtechKeymatrixEmulatorAbstractTestCase


class LegacyKbdGtechModuleTestCase(GtechKeymatrixEmulatorAbstractTestCase.LegacyKbdGtechBaseTestCase):
    """
    Kosmos KBD Gtech Module Test Class related to KBD functional mode: Legacy
    (Key Press & Key Release ony).

    This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
    """
    pass  # Refer to test  implementation in ``GtechKeymatrixEmulatorAbstractTestCase.LegacyKbdGtechBaseTestCase``
# end class LegacyKbdGtechModuleTestCase


class AnalogKbdGtechModuleTestCase(GtechKeymatrixEmulatorAbstractTestCase.AnalogKbdGtechBaseTestCase):
    """
    Kosmos KBD Gtech Module Test Class related to KBD functional mode: Analog
    (Key Release: displacement level 0 / Key Press displacement level 40)

    This test class requires the Galvatron Keyboard to be plugged into the Phidget USH hub port 1 (the rightmost port).
    """
    pass  # Refer to test  implementation in ``GtechKeymatrixEmulatorAbstractTestCase.AnalogKbdGtechBaseTestCase``
# end class AnalogKbdGtechModuleTestCase


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
