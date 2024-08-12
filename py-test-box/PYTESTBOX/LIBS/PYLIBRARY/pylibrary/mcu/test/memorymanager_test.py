#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.mcu.test.memorymanager_test
    :brief:  Memory Manager test module
    :author: Christophe Roquebert
    :date: 2020/06/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.mcu.memorymanagerfactory import MemoryManagerFactory
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeConfigurationManager
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeDeviceDebugger
from pylibrary.mcu.nrf52.test.nrf52memorymanager_test import FakeReceiverDebugger
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class MemoryManagerFactoryTestCase(TestCase):
    """
    MemoryManagerFactory create method validation
    """

    def test_create_from_device_debugger(self):
        """
        Tests create method with FakeDeviceDebugger input
        """
        my_class = MemoryManagerFactory.create(FakeDeviceDebugger(), 'Device', FakeConfigurationManager())
    # end def test_create_from_device_debugger

    def test_create_from_receiver_debugger(self):
        """
        Tests create method with FakeReceiverDebugger input
        """
        my_class = MemoryManagerFactory.create(FakeReceiverDebugger(), 'Receiver', FakeConfigurationManager())
    # end def test_create_from_receiver_debugger

# end class MemoryManagerFactoryTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
