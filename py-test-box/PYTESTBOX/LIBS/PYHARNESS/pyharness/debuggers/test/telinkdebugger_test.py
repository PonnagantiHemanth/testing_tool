#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyharness.debuggers.test.telinkdebugger_test
:brief: ``TLSR8208CDebugger`` unit tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/10/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from sys import stdout
from unittest import TestCase
from unittest import skipIf

from pyharness.debuggers.telinkdebugger import TLSR8208CDebugger
from pytransport.usb.logiusbcontext.logiusbcontext import LogiusbUsbContext
from pytransport.usb.usbconstants import ProductId
from pytransport.usb.usbconstants import VendorId

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
VERBOSE = True

# Error message to be printed when no Telink probe connected to the raspberry PI.
UNSUPPORTED_SETUP_ERR_MSG = f'Telink Maaxter debug probe not detected on this setup'


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
@skipIf(len(LogiusbUsbContext.get_plugged_devices(vid=VendorId.MAAXTER, pid=ProductId.TELINK_MAXXTER)) == 0,
        UNSUPPORTED_SETUP_ERR_MSG)
class TLSR8208CDebuggerTestCase(TestCase):
    """
    Unitary Test for ``TLSR8208CDebugger`` class.
    """
    def test_get_instance(self):
        """
        Validate debugger instanciation.
        """
        self.debugger = TLSR8208CDebugger()
        self.assertTrue(isinstance(self.debugger, TLSR8208CDebugger))
    # end def test_get_instance

    def test_read_write_memory(self):
        """
        Validate readMemory and writeMemory methods.
        """
        self.debugger = TLSR8208CDebugger()

        if VERBOSE:
            stdout.write(f"library version: {self.debugger.getVersion()}\n")
            stdout.write(f"MCU name: {self.debugger.get_device()}\n")
        # end if
        # Open the connection
        self.debugger.open()
        # Reset the MCU
        self.debugger.reset()
        # Read first 128 bytes
        data = self.debugger.readMemory(addressOrLabel=0, length=128)
        # Rewrite the first 128 bytes with the same data
        self.debugger.writeMemory(addressOrLabel=0, data=data)
        # Pause the program
        self.debugger.stop()
        # Continue running the program
        self.debugger.run()

    # end def test_read_write_memory
# end class TLSR8208CDebuggerTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
