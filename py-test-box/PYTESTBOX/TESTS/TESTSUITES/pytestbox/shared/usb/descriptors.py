#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.usb.descriptors
:brief: Validate USB descriptors test cases
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC

from pychannel.channelinterfaceclasses import LogitechReportType
from pyharness.extensions import level
from pyharness.selector import features
# noinspection PyUnresolvedReferences
from pyhid.hid.descriptor import ReportDescriptor
from pyhid.hid.interfacedescriptors import DrifterHIDppInterfaceDescriptor
from pyhid.hid.interfacedescriptors import HIDppInterfaceDescriptor
from pyhid.hid.interfacedescriptors import HIDppReceiverInterfaceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardBitmapInterfaceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardBitmapKeyDescriptor
from pyhid.hid.interfacedescriptors import KeyboardBitmapReceiverDescriptor
from pyhid.hid.interfacedescriptors import KeyboardDeviceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardInterfaceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardReceiverDescriptor
from pyhid.hid.interfacedescriptors import MouseInterfaceDescriptor
from pyhid.hid.interfacedescriptors import MouseKeyDescriptor
from pyhid.hid.interfacedescriptors import MouseNvidiaExtensionKeyDescriptor
from pyhid.hid.interfacedescriptors import MouseReceiverInterfaceDescriptor
from pyhid.hid.interfacedescriptors import MouseReceiverNvidiaExtensionKeyDescriptor
from pyhid.hid.interfacedescriptors import VlpInterfaceDescriptor
from pyhid.hid.interfacedescriptors import WindowsDigitizer3FingersDescriptor
from pyhid.hid.interfacedescriptors import WindowsDigitizer5FingersDescriptor
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.loghelper import LogHelper

# ----------------------------------------------------------------------------
# constant
# ----------------------------------------------------------------------------
VALID_DESCRIPTORS = [HIDppInterfaceDescriptor,
                     HIDppReceiverInterfaceDescriptor,
                     DrifterHIDppInterfaceDescriptor,
                     KeyboardBitmapInterfaceDescriptor,
                     KeyboardBitmapReceiverDescriptor,
                     KeyboardBitmapKeyDescriptor,
                     KeyboardDeviceDescriptor,
                     KeyboardInterfaceDescriptor,
                     KeyboardReceiverDescriptor,
                     MouseInterfaceDescriptor,
                     MouseReceiverInterfaceDescriptor,
                     MouseKeyDescriptor,
                     MouseNvidiaExtensionKeyDescriptor,
                     MouseReceiverNvidiaExtensionKeyDescriptor,
                     VlpInterfaceDescriptor,
                     WindowsDigitizer5FingersDescriptor,
                     WindowsDigitizer3FingersDescriptor]


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedDescriptorsTestCases(CommonBaseTestCase, ABC):
    """
    USB descriptors Test Cases
    """

    @features('USBProtocol')
    @features('Keyboard')
    @level('Functionality')
    def test_keyboard_interface_descriptor(self):
        """
        Test USB Keyboard interface descriptor
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Get USB Keyboard interface descriptor")
        # ---------------------------------------------------------------------------
        usb_descriptor = self.current_channel.get_interface_descriptor(
            interface=self.current_channel.report_type_to_interface[LogitechReportType.KEYBOARD])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB descriptor fields")
        # ---------------------------------------------------------------------------
        kwargs = {}
        if self.f.PRODUCT.PROTOCOLS.USB.F_TopRawUsageMaximum is not None:
            kwargs['cnt3'] = self.f.PRODUCT.PROTOCOLS.USB.F_TopRawUsageMaximum
        # end if
        expected_descriptor = self._get_descriptor_class(
            self.f.PRODUCT.PROTOCOLS.USB.F_KeyboardInterfaceDescriptor)(**kwargs)
        self.assertEqual(obtained=usb_descriptor,
                         expected=expected_descriptor,
                         msg="The keyboard interface descriptor differs from the one expected")

        self.testCaseChecked("FUN_USB_DESC_0001")
    # end def test_keyboard_interface_descriptor

    @features('USBProtocol')
    @features('Mice')
    @level('Functionality')
    def test_mouse_interface_descriptor(self):
        """
        Test USB Mouse interface descriptor
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Get USB Mouse interface descriptor")
        # ---------------------------------------------------------------------------
        usb_descriptor = self.current_channel.get_interface_descriptor(
            interface=self.current_channel.report_type_to_interface[LogitechReportType.MOUSE])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB descriptor fields")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor,
                         expected=self._get_descriptor_class(self.f.PRODUCT.PROTOCOLS.USB.F_MouseInterfaceDescriptor)(),
                         msg="The mouse interface descriptor differs from the one expected")

        self.testCaseChecked("FUN_USB_DESC_0002")
    # end def test_mouse_interface_descriptor

    @features('USBProtocol')
    @level('Functionality')
    def test_hidpp_interface_descriptor(self):
        """
        Test USB HID++ interface descriptor
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Get USB HID++ interface descriptor")
        # ---------------------------------------------------------------------------
        usb_descriptor = self.current_channel.get_interface_descriptor(
            interface=self.current_channel.report_type_to_interface[LogitechReportType.HIDPP])

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB descriptor fields")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor,
                         expected=self._get_descriptor_class(self.f.PRODUCT.PROTOCOLS.USB.F_HidppInterfaceDescriptor)(),
                         msg="The HID++ interface descriptor differs from the one expected")

        self.testCaseChecked("FUN_USB_DESC_0003")
    # end def test_hidpp_interface_descriptor

    @features('USBProtocol')
    @features('DigitizerInterface')
    @level('Functionality')
    def test_digitizer_interface_descriptor(self):
        """
        Test USB digitizer interface descriptor
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Get USB digitizer interface descriptor")
        # ---------------------------------------------------------------------------
        usb_descriptor = self.current_channel.get_interface_descriptor(
            interface=self.current_channel.report_type_to_interface[LogitechReportType.DIGITIZER])

        expected_descriptor = self._get_descriptor_class(self.f.PRODUCT.PROTOCOLS.USB.F_DigitizerInterfaceDescriptor)()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the finger collection number 1")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor.win_dig_finger_1,
                         expected=expected_descriptor.win_dig_finger_1,
                         msg="The first finger collection differs from the one expected")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the finger collection number 2")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor.win_dig_finger_2,
                         expected=expected_descriptor.win_dig_finger_2,
                         msg="The second finger collection differs from the one expected")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the finger collection number 3")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor.win_dig_finger_3,
                         expected=expected_descriptor.win_dig_finger_3,
                         msg="The third finger collection differs from the one expected")

        if hasattr(expected_descriptor, 'win_dig_finger_4'):
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the finger collection number 4")
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=usb_descriptor.win_dig_finger_4,
                             expected=expected_descriptor.win_dig_finger_4,
                             msg="The forth finger collection differs from the one expected")
        # end if

        if hasattr(expected_descriptor, 'win_dig_finger_5'):
            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, "Check the finger collection number 5")
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=usb_descriptor.win_dig_finger_5,
                             expected=expected_descriptor.win_dig_finger_5,
                             msg="The fifth finger collection differs from the one expected")
        # end if

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the  windows device capabilities feature")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor.win_dig_capabilities_feature,
                         expected=expected_descriptor.win_dig_capabilities_feature,
                         msg="The windows device capabilities feature differs from the one expected")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the  windows device certification feature")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor.win_dig_certification_feature,
                         expected=expected_descriptor.win_dig_certification_feature,
                         msg="The windows device certification feature differs from the one expected")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check USB descriptor fields")
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=usb_descriptor,
                         expected=expected_descriptor,
                         msg="The digitizer interface descriptor differs from the one expected")

        self.testCaseChecked("FUN_USB_DESC_0004")
    # end def test_digitizer_interface_descriptor

    @staticmethod
    def _get_descriptor_class(key):
        """
        Retrieve the theoretical descriptor class

        :param key: Descriptor class name
        :type key: ``str``

        :return: Descriptor class object
        :rtype: ``ReportDescriptor`` object
        """
        if globals()[key] in VALID_DESCRIPTORS:
            return globals()[key]
        else:
            return None
        # end if
    # end def _get_descriptor_class
# end class SharedDescriptorsTestCases

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
