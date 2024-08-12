#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.test.reset_test
:brief: Tests for Kosmos Reset Class
:author: Alexandre Lafaye <alafaye@logitech.com>
:date: 2023/07/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from logging import DEBUG
from logging import WARNING
from logging import basicConfig
from logging import info

from pylibrary.emulator.keyid import KEY_ID
from pyraspi.bus.spi import SpiTransactionTimeoutError
from pyraspi.services.kosmos.keymatrixemulator import KosmosKeyMatrixEmulator
from pyraspi.services.kosmos.module.devicetree import DeviceName
from pyraspi.services.kosmos.module.test.module_test import require_kosmos_device
from pyraspi.services.kosmos.powerslideremulator import KosmosPowerSliderEmulator
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_HW_REV_READ
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST_CMD_BREAKPOINT
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST_CMD_MB_ASSERT
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_TEST_CMD_TIMEOUT
from pyraspi.services.kosmos.test.keymatrixemulator_test import KBD_FW_ID
from pyraspi.services.kosmos.test.kosmos_test import KosmosCommonTestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class KosmosResetTestCase(KosmosCommonTestCase):
    """
    Unitary Test for Kosmos Test class
    """

    @classmethod
    def setUpClass(cls):
        """
        Open Kosmos
        """
        super().setUpClass()
        basicConfig(level=DEBUG if cls.VERBOSE else WARNING)
    # end def setUpClass

    def tearDown(self):
        """
        Clean unit test, especially any global error flag that would not have been caught
        """
        # Assess if Global Error Flag was raised during test
        if self.kosmos.dt.fpga.is_global_error_flag_raised():
            self.kosmos.dt.fpga.reset_global_error_flag()
        # end if

        super().tearDown()
    # end def tearDown

    def check_sequencer_status(self):
        """
        Check if the sequencer was left in a clean state

        :raise ``AssertionError``: Sequencer status has errors
        """
        status = self.kosmos.dt.sequencer.status()
        error_list = self.kosmos.dt.sequencer.is_sequencer_state_clean(status)
        info(f"Current Sequencer status: {status}")
        info(f"Current Sequencer error list: {error_list}")
        self.assertFalse(error_list, msg=f'{status}\n{error_list}')
    # end def check_sequencer_status

    def test_breakpoint_loop(self):
        """
        Check for robustness by triggering a selected amount of breakpoints
        """
        loop_number = 100
        for loop in range(loop_number):
            info(f"Test no {loop}")
            self.test_breakpoint()
        # end for
    # end def test_breakpoint_loop

    def test_breakpoint(self):
        """
        Check if the microblaze is properly recovering after triggering a breakpoint
        """
        info(self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ))
        with self.assertRaises(SpiTransactionTimeoutError):
            self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_TEST, MSG_ID_TEST_CMD_BREAKPOINT)
        # end with
        info(f"Expected breakpoint timeout")
        reset_status = self.kosmos.dt.fpga.soft_reset_microblaze()
        info(f"Reset return {reset_status}")
        self.check_sequencer_status()
    # end def test_breakpoint

    def test_timeout(self):
        """
        Check if the microblaze is properly recovering after triggering a timeout
        """
        info(self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ))

        with self.assertRaises(SpiTransactionTimeoutError):
            self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_TEST, MSG_ID_TEST_CMD_TIMEOUT)
        # end with
        info(f"Expected delay timeout")
        info(f"Reset return {self.kosmos.dt.fpga.soft_reset_microblaze()}")
        self.check_sequencer_status()
    # end def test_timeout

    def test_assert(self):
        """
        Check if the microblaze is properly recovering after triggering an assert
        """
        info(self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ))
        with self.assertRaises(SpiTransactionTimeoutError):
            self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_TEST, MSG_ID_TEST_CMD_MB_ASSERT)
        # end with
        info(f"Expected assert timeout")
        info(f"Reset return {self.kosmos.dt.fpga.soft_reset_microblaze()}")
        self.check_sequencer_status()
    # end def test_assert

    @require_kosmos_device(DeviceName.KBD_MATRIX)
    def test_breakpoint_kdb(self):
        """
        Check if the KBD_MATRIX module is working properly working after a microblaze reset
        """
        self._kbd_emu = KosmosKeyMatrixEmulator(kosmos=self.kosmos, fw_id=KBD_FW_ID, verbose=self.VERBOSE)

        info(self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ))
        with self.assertRaises(SpiTransactionTimeoutError):
            self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_TEST, MSG_ID_TEST_CMD_BREAKPOINT)
        # end with
        info(f"Expected breakpoint timeout")
        info(f"Reset return {self.kosmos.dt.fpga.soft_reset_microblaze()}")
        self.kosmos.dt.fpga.reset_global_error_flag()  # Reset Global Error flag manually before tearDown() catches it
        for key_id in range(KEY_ID.KEYBOARD_A, KEY_ID.KEYBOARD_Z + 1):
            self._kbd_emu.keystroke(key_id=KEY_ID(key_id), delay=.1)
        # end for
        self.check_sequencer_status()
    # end def test_breakpoint_kdb

    @require_kosmos_device(DeviceName.BAS)
    def test_breakpoint_slider(self):
        """
        Check if the slider module is properly working after a microblaze reset
        """
        self._slider_emulator = KosmosPowerSliderEmulator(kosmos=self.kosmos, fw_id=KBD_FW_ID)

        info(self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_FPGA, MSG_ID_FPGA_CMD_HW_REV_READ))
        with self.assertRaises(SpiTransactionTimeoutError):
            self.kosmos.dt.fpga_transport.send_control_message(MSG_ID_TEST, MSG_ID_TEST_CMD_BREAKPOINT)
        # end with
        info(f"Expected breakpoint timeout")
        info(f"Reset return {self.kosmos.dt.fpga.soft_reset_microblaze()}")
        self.kosmos.dt.fpga.reset_global_error_flag()  # Reset Global Error flag manually before tearDown() catches it
        self._slider_emulator.reset()
        self.check_sequencer_status()
    # end def test_breakpoint_slider
# end class KosmosResetTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
