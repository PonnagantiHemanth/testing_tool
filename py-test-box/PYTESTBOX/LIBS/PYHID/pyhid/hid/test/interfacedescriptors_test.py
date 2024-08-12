#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.hid.test.interfacedescriptors_test
:brief: USB interface descriptors test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/01/21
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid.hid.interfacedescriptors import ConsumerGenericChromeOSKeyDescriptor
from pyhid.hid.interfacedescriptors import ConsumerGenericKeyDescriptor
from pyhid.hid.interfacedescriptors import DescriptorDispatcher
from pyhid.hid.interfacedescriptors import FingerCollection
from pyhid.hid.interfacedescriptors import GenericDesktopCallStateControlKeyDescriptor
from pyhid.hid.interfacedescriptors import GenericDesktopSystemControlKeyDescriptor
from pyhid.hid.interfacedescriptors import GenericDesktopSystemControlKeyboardV14Descriptor
from pyhid.hid.interfacedescriptors import HIDppInterfaceDescriptor
from pyhid.hid.interfacedescriptors import HIDppLongMessageDescriptor
from pyhid.hid.interfacedescriptors import HIDppMessageDescriptor
from pyhid.hid.interfacedescriptors import HIDppReceiverInterfaceDescriptor
from pyhid.hid.interfacedescriptors import HIDppShortMessageDescriptor
from pyhid.hid.interfacedescriptors import KeyboardBitmapInterfaceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardBitmapKeyDescriptor
from pyhid.hid.interfacedescriptors import KeyboardDeviceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardInterfaceDescriptor
from pyhid.hid.interfacedescriptors import KeyboardReceiverDescriptor
from pyhid.hid.interfacedescriptors import MouseCommonDescriptor
from pyhid.hid.interfacedescriptors import MouseInterfaceDescriptor
from pyhid.hid.interfacedescriptors import MouseKeyDescriptor
from pyhid.hid.interfacedescriptors import MouseNvidiaExtensionKeyDescriptor
from pyhid.hid.interfacedescriptors import MouseReceiverInterfaceDescriptor
from pyhid.hid.interfacedescriptors import TopRawKeyDescriptor
from pyhid.hid.interfacedescriptors import WindowsDeviceCapabilitiesFeature
from pyhid.hid.interfacedescriptors import WindowsDeviceCertificationStatusFeature
from pyhid.hid.interfacedescriptors import WindowsDigitizer3FingersDescriptor
from pyhid.hid.interfacedescriptors import WindowsDigitizer5FingersDescriptor
from pyhid.hid.test.descriptor_test import DescriptorTestCase
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class InterfaceDescriptorsTestCase(DescriptorTestCase):
    """
    InterfaceDescriptors testing class
    """

    def test_interface_dispatcher_instantiation(self):
        """
        Test ``DescriptorDispatcher`` class instantiation
        """
        dispatcher = DescriptorDispatcher(timestamp=self.timestamp)
        self.descriptor_class_checker(dispatcher, my_class=DescriptorDispatcher, timestamp=self.timestamp)
    # end def test_interface_dispatcher_instantiation

    def test_consumer_generic_key_descriptor_instantiation(self):
        """
        Test ``ConsumerGenericKeyDescriptor`` class instantiation
        """
        descriptor = ConsumerGenericKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=ConsumerGenericKeyDescriptor, timestamp=self.timestamp)
    # end def test_consumer_generic_key_descriptor_instantiation

    def test_consumer_generic_key_descriptor_raw_data(self):
        """
        Test ``ConsumerGenericChromeOSKeyDescriptor`` class raw data
        """
        descriptor = ConsumerGenericKeyDescriptor()
        self.assertEqual(HexList(descriptor), HexList('050C0901A101850395027510150126FF0219012AFF028100C0'))
    # end def test_consumer_generic_key_descriptor_raw_data

    def test_consumer_generic_chrome_key_descriptor_instantiation(self):
        """
        Test ``ConsumerGenericChromeOSKeyDescriptor`` class instantiation
        """
        descriptor = ConsumerGenericChromeOSKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=ConsumerGenericChromeOSKeyDescriptor,
                                      timestamp=self.timestamp)
    # end def test_consumer_generic_chrome_key_descriptor_instantiation

    def test_consumer_generic_chrome_key_descriptor_raw_data(self):
        """
        Test ``ConsumerGenericChromeOSKeyDescriptor`` class raw data
        """
        descriptor = ConsumerGenericChromeOSKeyDescriptor()
        self.assertEqual(HexList(descriptor), HexList('060CFF0901A101850395027510150126FF0219012AFF028100C0'))
    # end def test_consumer_generic_chrome_key_descriptor_raw_data

    def test_generic_desktop_system_control_key_descriptor_instantiation(self):
        """
        Test ``GenericDesktopSystemControlKeyDescriptor`` class instantiation
        """
        descriptor = GenericDesktopSystemControlKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=GenericDesktopSystemControlKeyDescriptor,
                                      timestamp=self.timestamp)
    # end def test_generic_desktop_system_control_key_descriptor_instantiation

    def test_generic_desktop_system_control_key_descriptor_raw_data(self):
        """
        Test ``GenericDesktopSystemControlKeyDescriptor`` class raw data
        """
        descriptor = GenericDesktopSystemControlKeyDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010980A101850495017502150125030982098109838100750115002501099B810675058103C0'))
    # end def test_generic_desktop_system_control_key_descriptor_raw_data

    def test_generic_desktop_system_control_keyboard_v1_4_descriptor_instantiation(self):
        """
        Test ``GenericDesktopSystemControlKeyboardV14Descriptor`` class instantiation
        """
        descriptor = GenericDesktopSystemControlKeyboardV14Descriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=GenericDesktopSystemControlKeyboardV14Descriptor,
                                      timestamp=self.timestamp)
    # end def test_generic_desktop_system_control_keyboard_v1_4_descriptor_instantiation

    def test_generic_desktop_system_control_keyboard_v1_4_descriptor_raw_data(self):
        """
        Test ``GenericDesktopSystemControlKeyboardV14Descriptor`` class raw data
        """
        descriptor = GenericDesktopSystemControlKeyboardV14Descriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010980A1018504950175021501250309820981098381009502750115002501099B09A9810695017504'
                                 '8103C0'))
    # end def test_generic_desktop_system_control_keyboard_v1_4_descriptor_raw_data

    def test_generic_desktop_call_state_control_key_descriptor_instantiation(self):
        """
        Test ``GenericDesktopCallStateControlKeyDescriptor`` class instantiation
        """
        descriptor = GenericDesktopCallStateControlKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=GenericDesktopCallStateControlKeyDescriptor,
                                      timestamp=self.timestamp)
    # end def test_generic_desktop_call_state_control_key_descriptor_instantiation

    def test_generic_desktop_call_state_control_key_descriptor_raw_data(self):
        """
        Test ``GenericDesktopCallStateControlKeyDescriptor`` class raw data
        """
        descriptor = GenericDesktopCallStateControlKeyDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010913A101850B950175011500250109E18106750F8103C0'))
    # end def test_generic_desktop_call_state_control_key_descriptor_raw_data

    def test_keyboard_device_descriptor_instantiation(self):
        """
        Test ``KeyboardDeviceDescriptor`` class instantiation
        """
        descriptor = KeyboardDeviceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=KeyboardDeviceDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_device_descriptor_instantiation

    def test_keyboard_device_descriptor_raw_data(self):
        """
        Test ``KeyboardDeviceDescriptor`` class raw data
        """
        descriptor = KeyboardDeviceDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010906A1019508750115002501050719E029E781028103950575011500250105081901290591029503'
                                 '91039506750826FF000507190029FF8100C0'))
    # end def test_keyboard_device_descriptor_raw_data

    def test_keyboard_device_descriptor_from_hexlist(self):
        """
        Test ``KeyboardDeviceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = KeyboardDeviceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=descriptor.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=KeyboardDeviceDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_device_descriptor_from_hexlist

    def test_keyboard_key_descriptor_instantiation(self):
        """
        Test ``KeyboardReceiverDescriptor`` class instantiation
        """
        descriptor = KeyboardReceiverDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=KeyboardReceiverDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_key_descriptor_instantiation

    def test_keyboard_key_descriptor_raw_data(self):
        """
        Test ``KeyboardReceiverDescriptor`` class raw data
        """
        descriptor = KeyboardReceiverDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010906A1019508750115002501050719E029E781028103950505081901290591029501750391039506'
                                 '7508150026FF00050719002AFF008100C0'))
    # end def test_keyboard_key_descriptor_raw_data

    def test_keyboard_key_descriptor_from_hexlist(self):
        """
        Test ``KeyboardReceiverDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = KeyboardReceiverDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=descriptor.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=KeyboardReceiverDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_key_descriptor_from_hexlist

    def test_top_raw_key_descriptor_instantiation(self):
        """
        Test ``TopRawKeyDescriptor`` class instantiation
        """
        descriptor = TopRawKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=TopRawKeyDescriptor, timestamp=self.timestamp)
    # end def test_top_raw_key_descriptor_instantiation

    def test_top_raw_key_descriptor_configuration(self):
        """
        Test ``TopRawKeyDescriptor`` class customization
        """
        for cnt3 in [1, 2, 4, 8, 16, 32, 64, 128]:
            descriptor = TopRawKeyDescriptor(cnt3=cnt3, timestamp=self.timestamp)
            self.descriptor_class_checker(descriptor, my_class=TopRawKeyDescriptor, timestamp=self.timestamp)
            self.assertEqual(to_int(descriptor.top_raw_report_count & 0xFF), cnt3)
            self.assertEqual(to_int(descriptor.top_raw_usage_maximum & 0xFF), cnt3)
        # end for
    # end def test_top_raw_key_descriptor_configuration

    def test_top_raw_key_descriptor_raw_data(self):
        """
        Test ``TopRawKeyDescriptor`` class raw data
        """
        descriptor = TopRawKeyDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('0901A102850995007520170000008027FFFFFF7F050A19012900B103C0'))
    # end def test_top_raw_key_descriptor_raw_data

    def test_keyboard_interface_descriptor_instantiation(self):
        """
        Test ``KeyboardInterfaceDescriptor`` class instantiation
        """
        descriptor = KeyboardInterfaceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=KeyboardInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_interface_descriptor_instantiation

    def test_keyboard_interface_descriptor_from_hexlist(self):
        """
        Test ``KeyboardInterfaceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = KeyboardInterfaceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=KeyboardInterfaceDescriptor,
                                      timestamp=self.timestamp)
    # end def test_keyboard_interface_descriptor_from_hexlist

    def test_keyboard_bitmap_key_descriptor_instantiation(self):
        """
        Test ``KeyboardBitmapKeyDescriptor`` class instantiation
        """
        descriptor = KeyboardBitmapKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=KeyboardBitmapKeyDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_bitmap_key_descriptor_instantiation

    def test_keyboard_bitmap_key_descriptor_from_hexlist(self):
        """
        Test ``KeyboardBitmapKeyDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = KeyboardBitmapKeyDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=KeyboardBitmapKeyDescriptor,
                                      timestamp=self.timestamp)
    # end def test_keyboard_bitmap_key_descriptor_from_hexlist

    def test_keyboard_bitmap_interface_descriptor_instantiation(self):
        """
        Test ``KeyboardBitmapInterfaceDescriptor`` class instantiation
        """
        descriptor = KeyboardBitmapInterfaceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=KeyboardBitmapInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_keyboard_bitmap_interface_descriptor_instantiation

    def test_keyboard_bitmap_interface_descriptor_from_hexlist(self):
        """
        Test ``KeyboardBitmapInterfaceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = KeyboardBitmapInterfaceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=KeyboardBitmapInterfaceDescriptor,
                                      timestamp=self.timestamp)
    # end def test_keyboard_bitmap_interface_descriptor_from_hexlist

    def test_mouse_common_descriptor_instantiation(self):
        """
        Test ``MouseCommonDescriptor`` class instantiation
        """
        descriptor = MouseCommonDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=MouseCommonDescriptor, timestamp=self.timestamp)
    # end def test_mouse_common_descriptor_instantiation

    def test_mouse_key_descriptor_instantiation(self):
        """
        Test ``MouseKeyDescriptor`` class instantiation
        """
        descriptor = MouseKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=MouseKeyDescriptor, timestamp=self.timestamp)
    # end def test_mouse_key_descriptor_instantiation

    def test_mouse_key_descriptor_from_hexlist(self):
        """
        Test ``MouseKeyDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = MouseKeyDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=MouseKeyDescriptor, timestamp=self.timestamp)
    # end def test_mouse_key_descriptor_from_hexlist

    def test_mouse_nvidia_extension_key_descriptor_instantiation(self):
        """
        Test ``MouseNvidiaExtensionKeyDescriptor`` class instantiation
        """
        descriptor = MouseNvidiaExtensionKeyDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=MouseNvidiaExtensionKeyDescriptor, timestamp=self.timestamp)
    # end def test_mouse_nvidia_extension_key_descriptor_instantiation

    def test_mouse_nvidia_extension_key_descriptor_from_hexlist(self):
        """
        Test ``MouseNvidiaExtensionKeyDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = MouseNvidiaExtensionKeyDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=MouseNvidiaExtensionKeyDescriptor,
                                      timestamp=self.timestamp)
    # end def test_mouse_nvidia_extension_key_descriptor_from_hexlist

    def test_mouse_interface_descriptor_instantiation(self):
        """
        Test ``MouseInterfaceDescriptor`` class instantiation
        """
        descriptor = MouseInterfaceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=MouseInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_mouse_interface_descriptor_instantiation

    def test_mouse_interface_descriptor_from_hexlist(self):
        """
        Test ``MouseInterfaceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = MouseInterfaceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=MouseInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_mouse_interface_descriptor_from_hexlist

    def test_mouse_interface_descriptor_raw_data(self):
        """
        Test ``MouseInterfaceDescriptor`` class raw data
        """
        descriptor = MouseInterfaceDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010902A10185020901A100951075011500250105091901291081029502751016008026FF7F05010930'
                                 '09318106950175081580257F09388106050C0A38028106C0C0050C0901A101850395027510150126FF02'
                                 '19012AFF028100C005010980A1018504950175021501250309820981098381009502750115002501099B'
                                 '09A98106950175048103C0'))
    # end def test_mouse_interface_descriptor_raw_data

    def test_mouse_receiver_interface_descriptor_instantiation(self):
        """
        Test ``MouseReceiverInterfaceDescriptor`` class instantiation
        """
        descriptor = MouseReceiverInterfaceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=MouseReceiverInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_mouse_receiver_interface_descriptor_instantiation

    def test_mouse_receiver_interface_descriptor_from_hexlist(self):
        """
        Test ``MouseReceiverInterfaceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = MouseReceiverInterfaceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=MouseReceiverInterfaceDescriptor,
                                      timestamp=self.timestamp)
    # end def test_mouse_receiver_interface_descriptor_from_hexlist

    def test_mouse_receiver_interface_descriptor_raw_data(self):
        """
        Test ``MouseReceiverInterfaceDescriptor`` class raw data
        """
        descriptor = MouseReceiverInterfaceDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('05010902A10185020901A100951075011500250105091901291081029502751016018026FF7F05010930'
                                 '09318106950175081581257F093881069501050C0A38028106C0C0050C0901A101850395027510150126'
                                 'FF0219012AFF028100C005010980A101850495017502150125030982098109838100750115002501099B'
                                 '810675058103C005010913A101850B950175011500250109E18106750F8103C0'))
    # end def test_mouse_receiver_interface_descriptor_raw_data

    def test_hidpp_message_descriptor_instantiation(self):
        """
        Test ``HIDppMessageDescriptor`` class instantiation
        """
        descriptor = HIDppMessageDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=HIDppMessageDescriptor, timestamp=self.timestamp)
    # end def test_hidpp_message_descriptor_instantiation

    def test_hidpp_short_message_descriptor_instantiation(self):
        """
        Test ``HIDppShortMessageDescriptor`` class instantiation
        """
        descriptor = HIDppShortMessageDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=HIDppShortMessageDescriptor, timestamp=self.timestamp)
    # end def test_hidpp_short_message_descriptor_instantiation

    def test_hidpp_short_key_descriptor_raw_data(self):
        """
        Test ``HIDppShortMessageDescriptor`` class raw data
        """
        descriptor = HIDppShortMessageDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('0643FF0A0103A101851095067508150026FF000901810009019100C0'))
    # end def test_hidpp_short_key_descriptor_raw_data

    def test_hidpp_long_message_descriptor_instantiation(self):
        """
        Test ``HIDppLongMessageDescriptor`` class instantiation
        """
        descriptor = HIDppLongMessageDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=HIDppLongMessageDescriptor, timestamp=self.timestamp)
    # end def test_hidpp_long_message_descriptor_instantiation

    def test_hidpp_long_key_descriptor_raw_data(self):
        """
        Test ``HIDppLongMessageDescriptor`` class raw data
        """
        descriptor = HIDppLongMessageDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('0643FF0A0203A101851195137508150026FF000902810009029100C0'))
    # end def test_hidpp_long_key_descriptor_raw_data

    def test_hidpp_interface_descriptor_instantiation(self):
        """
        Test ``HIDppInterfaceDescriptor`` class instantiation
        """
        descriptor = HIDppInterfaceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=HIDppInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_hidpp_interface_descriptor_instantiation

    def test_hidpp_interface_descriptor_from_hexlist(self):
        """
        Test ``HIDppInterfaceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = HIDppInterfaceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=HIDppInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_hidpp_interface_descriptor_from_hexlist

    def test_hidpp_interface_descriptor_raw_data(self):
        """
        Test ``HIDppInterfaceDescriptor`` class raw data
        """
        descriptor = HIDppInterfaceDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('0643FF0A0103A101851095067508150026FF000901810009019100C00643FF0A0203A101851195137508'
                                 '150026FF000902810009029100C0'))
    # end def test_hidpp_interface_descriptor_raw_data

    def test_hidpp_receiver_interface_instantiation(self):
        """
        Test ``HIDppInterfaceDescriptor`` class instantiation
        """
        descriptor = HIDppReceiverInterfaceDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=HIDppReceiverInterfaceDescriptor, timestamp=self.timestamp)
    # end def test_hidpp_receiver_interface_instantiation

    def test_hidpp_receiver_interface_from_hexlist(self):
        """
        Test ``HIDppReceiverInterfaceDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = HIDppReceiverInterfaceDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=HIDppReceiverInterfaceDescriptor,
                                      timestamp=self.timestamp)
    # end def test_hidpp_receiver_interface_from_hexlist

    def test_hidpp_receiver_interface_descriptor_raw_data(self):
        """
        Test ``HIDppReceiverInterfaceDescriptor`` class raw data
        """
        descriptor = HIDppReceiverInterfaceDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('0600FF0901A101851095067508150026FF000901810009019100C00600FF0902A1018511951375081500'
                                 '26FF000902810009029100C0'))
    # end def test_hidpp_receiver_interface_descriptor_raw_data

    def test_finger_collection_instantiation(self):
        """
        Test ``FingerCollection`` class instantiation
        """
        descriptor = FingerCollection(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=FingerCollection, timestamp=self.timestamp)
    # end def test_finger_collection_instantiation

    def test_finger_collection_raw_data(self):
        """
        Test ``FingerCollection`` class raw data
        """
        descriptor = FingerCollection()
        self.assertEqual(HexList(descriptor),
                         HexList('0922A102950275011500250109470942810295017506250409518102750826FF0009308102A4750C26D7'
                                 '0A3500469204550E651105010930810226FA0646F30209318102B4C0'))
    # end def test_finger_collection_raw_data

    def test_win_dev_cap_descriptor_instantiation(self):
        """
        Test ``WindowsDeviceCapabilitiesFeature`` class instantiation
        """
        descriptor = WindowsDeviceCapabilitiesFeature(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=WindowsDeviceCapabilitiesFeature, timestamp=self.timestamp)
    # end def test_win_dev_cap_descriptor_instantiation

    def test_win_dev_cap_descriptor_raw_data(self):
        """
        Test ``WindowsDeviceCapabilitiesFeature`` class raw data
        """
        descriptor = WindowsDeviceCapabilitiesFeature()
        self.assertEqual(HexList(descriptor),
                         HexList('85297508250F0955B102'))
    # end def test_win_dev_cap_descriptor_raw_data

    def test_win_dev_cer_descriptor_instantiation(self):
        """
        Test ``WindowsDeviceCertificationStatusFeature`` class instantiation
        """
        descriptor = WindowsDeviceCertificationStatusFeature(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=WindowsDeviceCertificationStatusFeature,
                                      timestamp=self.timestamp)
    # end def test_win_dev_cer_descriptor_instantiation

    def test_win_dev_cer_descriptor_raw_data(self):
        """
        Test ``WindowsDeviceCertificationStatusFeature`` class raw data
        """
        descriptor = WindowsDeviceCertificationStatusFeature()
        self.assertEqual(HexList(descriptor),
                         HexList('852A96000126FF000600FF09C5B102'))
    # end def test_win_dev_cer_descriptor_raw_data

    def test_windows_digitizer_5fingers_descriptor_instantiation(self):
        """
        Test ``WindowsDigitizer5FingersDescriptor`` class instantiation
        """
        descriptor = WindowsDigitizer5FingersDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=WindowsDigitizer5FingersDescriptor, timestamp=self.timestamp)
    # end def test_windows_digitizer_5fingers_descriptor_instantiation

    def test_windows_digitizer_5fingers_descriptor_from_hexlist(self):
        """
        Test ``WindowsDigitizer5FingersDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = WindowsDigitizer5FingersDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=WindowsDigitizer5FingersDescriptor,
                                      timestamp=self.timestamp)
    # end def test_windows_digitizer_5fingers_descriptor_from_hexlist

    def test_windows_digitizer_5fingers_descriptor_raw_data(self):
        """
        Test ``WindowsDigitizer5FingersDescriptor`` class raw data
        """
        descriptor = WindowsDigitizer5FingersDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('050D0905A10185280922A102950275011500250109470942810295017506250409518102750826FF0009'
                                 '308102A4750C26D70A3500469204550E651105010930810226FA0646F30209318102B4C00922A1029502'
                                 '75011500250109470942810295017506250409518102750826FF0009308102A4750C26D70A3500469204'
                                 '550E651105010930810226FA0646F30209318102B4C00922A10295027501150025010947094281029501'
                                 '7506250409518102750826FF0009308102A4750C26D70A3500469204550E651105010930810226FA0646'
                                 'F30209318102B4C00922A102950275011500250109470942810295017506250409518102750826FF0009'
                                 '308102A4750C26D70A3500469204550E651105010930810226FA0646F30209318102B4C00922A1029502'
                                 '75011500250109470942810295017506250409518102750826FF0009308102A4750C26D70A3500469204'
                                 '550E651105010930810226FA0646F30209318102B4C07507250509548102750125010509090181027510'
                                 '27FFFF000047FFFF0000550C660110050D095681026500550085297508250F0955B102852A96000126FF'
                                 '000600FF09C5B102C0'))
    # end def test_windows_digitizer_5fingers_descriptor_raw_data

    def test_windows_digitizer_3fingers_descriptor_instantiation(self):
        """
        Test ``WindowsDigitizer3FingersDescriptor`` class instantiation
        """
        descriptor = WindowsDigitizer3FingersDescriptor(timestamp=self.timestamp)
        self.descriptor_class_checker(descriptor, my_class=WindowsDigitizer3FingersDescriptor, timestamp=self.timestamp)
    # end def test_windows_digitizer_3fingers_descriptor_instantiation

    def test_windows_digitizer_3fingers_descriptor_from_hexlist(self):
        """
        Test ``WindowsDigitizer3FingersDescriptor`` can be instantiated from ``DescriptorDispatcher.fromHexList`` method
        """
        descriptor = WindowsDigitizer3FingersDescriptor(timestamp=self.timestamp)
        interface = DescriptorDispatcher.fromHexList(HexList(descriptor), timestamp=self.timestamp)
        self.descriptor_class_checker(instance=interface, my_class=WindowsDigitizer3FingersDescriptor,
                                      timestamp=self.timestamp)
    # end def test_windows_digitizer_3fingers_descriptor_from_hexlist

    def test_windows_digitizer_3fingers_descriptor_raw_data(self):
        """
        Test ``WindowsDigitizer3FingersDescriptor`` class raw data
        """
        descriptor = WindowsDigitizer3FingersDescriptor()
        self.assertEqual(HexList(descriptor),
                         HexList('050D0905A10185280922A102950275011500250109470942810295017506250409518102750826FF0009'
                                 '308102A4750C26D70A3500469204550E651105010930810226FA0646F30209318102B4C00922A1029502'
                                 '75011500250109470942810295017506250409518102750826FF0009308102A4750C26D70A3500469204'
                                 '550E651105010930810226FA0646F30209318102B4C00922A10295027501150025010947094281029501'
                                 '7506250409518102750826FF0009308102A4750C26D70A3500469204550E651105010930810226FA0646'
                                 'F30209318102B4C0750725050954810275012501050909018102751027FFFF000047FFFF0000550C6601'
                                 '10050D095681026500550085297508250F0955B102852A96000126FF000600FF09C5B102C0'))
    # end def test_windows_digitizer_3fingers_descriptor_raw_data

# end class InterfaceDescriptorsTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
