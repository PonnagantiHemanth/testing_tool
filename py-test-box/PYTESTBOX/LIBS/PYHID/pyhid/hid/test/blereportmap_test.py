#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.test.blereportmap_test
:brief: BLE report descriptor test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/27
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hid.blereportmap import HidReportKeyboardLedTopRowDescriptor
from pyhid.hid.blereportmap import HidReportKeyboardLedDescriptor
from pyhid.hid.blereportmap import HidReportMap
from pyhid.hid.blereportmap import HidReportMouse12Descriptor
from pyhid.hid.blereportmap import HidReportMouse16Descriptor
from pyhid.hid.blereportmap import HidReportConsumerGenericWithChromeOSDescriptor
from pyhid.hid.blereportmap import HidReportConsumerGenericWithoutChromeOSDescriptor
from pyhid.hid.blereportmap import HidReportConsumerMinimumDescriptor
from pyhid.hid.blereportmap import HidReportHidppLongReportDescriptor
from pyhid.hid.interfacedescriptors import DescriptorDispatcher
from pyhid.hid.test.descriptor_test import DescriptorTestCase
from pylibrary.tools.hexlist import HexList


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleReportMapTestCase(DescriptorTestCase):
    """
    BLE report map testing class
    """

    def test_hid_report_keybord_led_top_raw_descriptor_instantiation(self):
        """
        Test ``HidReportKeyboardLedTopRawDescriptor`` class instantiation
        """
        descriptor = HidReportKeyboardLedTopRowDescriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportKeyboardLedTopRowDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_keybord_led_top_raw_descriptor_instantiation

    def test_hid_report_keybord_led_descriptor_instantiation(self):
        """
        Test ``HidReportKeyboardLedDescriptor`` class instantiation
        """
        descriptor = HidReportKeyboardLedDescriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportKeyboardLedDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_keybord_led_descriptor_instantiation

    def test_hid_report_mouse12_descriptor_instantiation(self):
        """
        Test ``HidReportMouse12Descriptor`` class instantiation
        """
        descriptor = HidReportMouse12Descriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportMouse12Descriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_mouse12_descriptor_instantiation

    def test_hid_report_mouse16_descriptor_instantiation(self):
        """
        Test ``HidReportMouse16Descriptor`` class instantiation
        """
        descriptor = HidReportMouse16Descriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportMouse16Descriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_mouse16_descriptor_instantiation

    def test_hid_report_consumer_generic_with_chrome_os_descriptor_instantiation(self):
        """
        Test ``HidReportConsumerGenericWithChromeOSDescriptor`` class instantiation
        """
        descriptor = HidReportConsumerGenericWithChromeOSDescriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportConsumerGenericWithChromeOSDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_consumer_generic_with_chrome_os_descriptor_instantiation

    def test_hid_report_consumer_generic_without_chrome_os_descriptor_instantiation(self):
        """
        Test ``HidReportConsumerGenericWithoutChromeOSDescriptor`` class instantiation
        """
        descriptor = HidReportConsumerGenericWithoutChromeOSDescriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportConsumerGenericWithoutChromeOSDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_consumer_generic_without_chrome_os_descriptor_instantiation

    def test_hid_report_consumer_minimum_descriptor_instantiation(self):
        """
        Test ``HidReportConsumerMinimumDescriptor`` class instantiation
        """
        descriptor = HidReportConsumerMinimumDescriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportConsumerMinimumDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_consumer_minimum_descriptor_instantiation

    def test_hid_report_hidpp_long_descriptor_instantiation(self):
        """
        Test ``HidReportHidppLongReportDescriptor`` class instantiation
        """
        descriptor = HidReportHidppLongReportDescriptor(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportHidppLongReportDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hid_report_hidpp_long_descriptor_instantiation

    def test_hid_report_map_instantiation(self):
        """
        Test ``HidReportMap`` class instantiation
        """
        descriptor = HidReportMap(self.timestamp)
        self.descriptor_class_checker(instance=descriptor, my_class=HidReportMap,
                                      timestamp=self.timestamp)
    # end def test_hid_report_map_instantiation

    def test_hidpp_interface_descriptor_from_hexlist(self):
        """
        Test ``HidReportMap`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = HidReportMap(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=HidReportMap, timestamp=self.timestamp)
    # end def test_hidpp_interface_descriptor_from_hexlist
# end class BleReportMapTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
