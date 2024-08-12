#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyharness.debuggers.nrfprobedebugger_test
:brief: ``NrfProbeDebugger`` unit tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/01/22
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from os.path import abspath
from os.path import join
from sys import stdout
from sys import path
from unittest import TestCase
from unittest import skipIf

# We shall keep the pysetup import before Nrf54H20ProbeDebugger to resolve TESTS_PATH from local LIBS
FILE_PATH = abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("LIBS")]
PYSETUP_DIR = join(WS_DIR, "LIBS", "PYSETUP", "PYTHON")
if PYSETUP_DIR not in path:
    path.insert(0, PYSETUP_DIR)
# end if
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH

from pyharness.debuggers.nrfprobedebugger import Nrf54H20ProbeDebugger
from pyharness.debuggers.nrfprobedebugger import NrfProbeDebugger
from pylibrary.tools.hexlist import HexList
from pytransport.usb.logiusbcontext.logiusbcontext import LogiusbUsbContext
from pytransport.usb.usbconstants import ProductId
from pytransport.usb.usbconstants import VendorId

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
VERBOSE = False

# Error message to be printed when no Nordic probe connected to the raspberry PI.
UNSUPPORTED_SETUP_ERR_MSG = f'NRF probe lib debug probe not detected on this setup'
# - the uicr approtect register (the prod binary is read-back protected)
UICR_APPROTECT_REGISTER_OFFSET = 0x208


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@skipIf(len(LogiusbUsbContext.get_plugged_devices(
    vid=VendorId.SEGGER_MICROCONTROLLER_SYSTEM_GMBH,
    pid=[ProductId.SEGGER_J_LINK, ProductId.SEGGER_J_LINK_PLUS,
         ProductId.NRF52_DK_V1, ProductId.NRF52_DK_V2, ProductId.NRF52_DK_V3])) == 0, UNSUPPORTED_SETUP_ERR_MSG)
class NrfProbeDebuggerTestCase(TestCase):
    """
    Unitary Test for ``NrfProbeDebugger`` class.
    """
    def test_get_instance(self):
        """
        Validate debugger instanciation.
        """
        self.debugger = NrfProbeDebugger()
        self.assertTrue(isinstance(self.debugger, NrfProbeDebugger))
    # end def test_get_instance

    def test_lib_api_with_nrf54h20(self):
        """
        Validate nrf_probe_lib methods on a ``Nrf54H20ProbeDebugger`` instance.
        """
        self.debugger = Nrf54H20ProbeDebugger()
        if VERBOSE:
            stdout.write(f"library version: {self.debugger.getVersion()}\n")
            stdout.write(f"MCU name: {self.debugger.get_device()}\n")
        # end if

        # Open the connection
        self.debugger.open()
        mcu_type = self.debugger.get_mcu_type()
        if mcu_type is None or not str(mcu_type).startswith(self.debugger.MCU_NAME.split('_')[0]):
            # Check of MCU type failed
            stdout.write(f'Wrong MCU type detected: {mcu_type}')
            return
        # end if
        stdout.write(f"Device information: {self.debugger.log_device_info()}\n")

        # Read APPROTECT register
        data = self.debugger.readMemory(
            addressOrLabel=self.debugger.UICR_START_ADDRESS + UICR_APPROTECT_REGISTER_OFFSET, length=1)
        if VERBOSE:
            stdout.write(f'APPROTECT register = {data}\n')
        # end if
        # Read first 128 bytes
        data = self.debugger.readMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, length=128)
        if VERBOSE:
            stdout.write(f'NVS data = {data}\n')
        # end if

        self.debugger.reset(soft_reset=False)
        # Read first 128 bytes
        data_after_hard_reset = self.debugger.readMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, length=128)
        if VERBOSE:
            stdout.write(f'NVS data after hard reset = {data_after_hard_reset}\n')
        # end if
        assert data == data_after_hard_reset

        # Uncomment when soft reset behavior is fixed by Nordic
        # self.debugger.reset(soft_reset=True)
        # # Read first 128 bytes
        # data_after_soft_reset = self.debugger.readMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, length=128)
        # if VERBOSE:
        #     stdout.write(f'NVS data after soft reset = {data_after_soft_reset}\n')
        # # end if
        # assert data == data_after_soft_reset

        # Pause the program
        self.debugger.stop()
        written_data = data[:8] + HexList('AA' * 8) + data[16:]
        if VERBOSE:
            stdout.write(f'Written data = {written_data}\n')
        # end if
        # Rewrite the first 128 bytes with the same data
        self.debugger.writeMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, data=written_data)
        # Continue running the program
        self.debugger.run()
        # Re-read first 128 bytes
        data_after_write = self.debugger.readMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, length=128)
        if VERBOSE:
            stdout.write(f'NVS data after write = {data_after_write}\n')
        # end if
        assert written_data == data_after_write

        # Rewrite the first 128 bytes with the same data
        self.debugger.writeMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, data=data)
        # Re-read first 128 bytes
        data_after_rewrite = self.debugger.readMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, length=128)
        if VERBOSE:
            stdout.write(f'NVS data after rewrite = {data_after_rewrite}\n')
        # end if
        assert data == data_after_rewrite

        # Erase firmware
        self.debugger.erase_firmware()

        # Flash firmware
        fw_hex = join(TESTS_PATH, "DFU_FILES", 'tiger_app_uicr_merged.hex')
        self.debugger.reload_file(firmware_hex_file=fw_hex)

        # Re-read first 128 bytes
        data_after_flash = self.debugger.readMemory(addressOrLabel=self.debugger.NVS_START_ADDRESS, length=128)
        if VERBOSE:
            stdout.write(f'NVS data after flash = {data_after_flash}\n')
        # end if
    # end def test_lib_api_with_nrf54h20
# end class NrfProbeDebuggerTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
