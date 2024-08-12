#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.test.mouse_test

@brief  PyHid Mouse Descriptor parser testing module

@author christophe Roquebert

@date   2019/01/28
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyhid import hidparser
from unittest import TestCase
from pyhid.hidparser.Device import Collection
from pyhid.hidparser.enums import ReportType
from pylibrary.tools.numeral import RandNumeral

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class KeyboardTestCase(TestCase):                                               #pylint:disable=R0904
    """
    Tests of the BitField class
    """

    def test_footlose_interface1(self):
        """
        Tests footloose interface 1 (KEYBOARD) parsing and deserializing
        """
        # Report ID
        KEYBOARD_REPORT_ID = 1
        # Report in Collection
        KEYPAD = 1
        CONSTANT = 1
        OTHERS = 2

        footlose_interface1 = bytes([
            0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
            0x09, 0x06,  # Usage (Keyboard)
            0xA1, 0x01,  # Collection (Application)
            0x85, 0x01,  # Report ID (1)
            0x95, 0x08,  # Report Count (8)
            0x75, 0x01,  # Report Size (1)
            0x15, 0x00,  # Logical Minimum (0)
            0x25, 0x01,  # Logical Maximum (1)
            0x05, 0x07,  # Usage Page (Kbrd/Keypad)
            0x19, 0xE0,  # Usage Minimum (0xE0)
            0x29, 0xE7,  # Usage Maximum (0xE7)
            0x81, 0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
            0x81, 0x03,  # Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
            0x95, 0x05,  # Report Count (5)
            0x05, 0x08,  # Usage Page (LEDs)
            0x19, 0x01,  # Usage Minimum (Num Lock)
            0x29, 0x05,  # Usage Maximum (Kana)
            0x91, 0x02,  # Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
            0x95, 0x01,  # Report Count (1)
            0x75, 0x03,  # Report Size (3)
            0x91, 0x03,  # Output (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
            0x95, 0x06,  # Report Count (6)
            0x75, 0x08,  # Report Size (8)
            0x15, 0x00,  # Logical Minimum (0)
            0x26, 0xFF, 0x00,  # Logical Maximum (255)
            0x05, 0x07,  # Usage Page (Kbrd/Keypad)
            0x19, 0x00,  # Usage Minimum (0x00)
            0x2A, 0xFF, 0x00,  # Usage Maximum (0xFF)
            0x81, 0x00,  # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
            0xC0,  # End Collection
            0x05, 0x0C,  # Usage Page (Consumer)
            0x09, 0x01,  # Usage (Consumer Control)
            0xA1, 0x01,  # Collection (Application)
            0x85, 0x03,  # Report ID (3)
            0x95, 0x02,  # Report Count (2)
            0x75, 0x10,  # Report Size (16)
            0x15, 0x01,  # Logical Minimum (1)
            0x26, 0x3C, 0x02,  # Logical Maximum (767)
            0x19, 0x01,  # Usage Minimum (Consumer Control)
            0x2A, 0xFF, 0x02,  # Usage Maximum (0x02FF)
            0x81, 0x00,  # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
            0xC0,  # End Collection
            0x05, 0x01,  # Usage Page (Generic Desktop Ctrls)
            0x09, 0x80,  # Usage (Sys Control)
            0xA1, 0x01,  # Collection (Application)
            0x85, 0x04,  # Report ID (4)
            0x95, 0x01,  # Report Count (1)
            0x75, 0x02,  # Report Size (2)
            0x15, 0x01,  # Logical Minimum (1)
            0x25, 0x03,  # Logical Maximum (3)
            0x09, 0x82,  # Usage (Sys Sleep)
            0x09, 0x81,  # Usage (Sys Power Down)
            0x09, 0x83,  # Usage (Sys Wake Up)
            0x81, 0x00,  # Input (Data,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
            0x75, 0x06,  # Report Size (6)
            0x81, 0x03,  # Input (Const,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
            0xC0,  # End Collection
        ])

        # This returns a Device
        keyboard_from_desc = hidparser.parse(bytes(footlose_interface1.hex(), 'utf-8'))

        keyboard = keyboard_from_desc.reports[KEYBOARD_REPORT_ID].inputs.keyboard
        self.assertIsInstance(keyboard,
                              Collection,
                              "keyboard shall be of type Collection !")
        # ------------------------------
        # Check Button attributes
        # ------------------------------
        self.assertEqual(keyboard[KEYPAD].size,
                         1,
                         "KEYPAD size shall be equal to 1 !")
        self.assertEqual(keyboard[KEYPAD].count,
                         8,
                         "KEYPAD count shall be equal to 8 !")
        self.assertEqual(keyboard[KEYPAD].report_type,
                         ReportType.INPUT,
                         "KEYPAD report type shall be equal to INPUT !")
        # ------------------------------
        # Check CONSTANT attribute
        # ------------------------------
        self.assertEqual(keyboard[CONSTANT].size,
                         1,
                         "X size shall be equal to 1 !")
        self.assertEqual(keyboard[CONSTANT].count,
                         8,
                         "X count shall be equal to 8 !")
        self.assertEqual(keyboard[CONSTANT].report_type,
                         ReportType.INPUT,
                         "X report type shall be equal to INPUT !")
        # ------------------------------
        # Check OTHERS attribute
        # ------------------------------
        self.assertEqual(keyboard[OTHERS].size,
                         8,
                         "OTHERS size shall be equal to 8 !")
        self.assertEqual(keyboard[OTHERS].count,
                         6,
                         "OTHERS count shall be equal to 6 !")
        self.assertEqual(keyboard[OTHERS].report_type,
                         ReportType.INPUT,
                         "OTHERS report type shall be equal to INPUT !")

        # ------------------------------
        # Tests X and Y positives values
        # ------------------------------
        # x_position = int(RandNumeral(2, maxVal=0x7FFF))
        # y_position = int(RandNumeral(2, maxVal=0x7FFF))
        #
        # Read from the physical device
        data = bytes([KEYBOARD_REPORT_ID, 0x12, 0x34,
                      0x56, 0x78,
                      0x9A, 0xBC,
                      0xDE, 0xF0])
        # Deserialize the data and populate the object members
        keyboard_from_desc.deserialize(data)

        # Read x,y from mouse
        pointer = keyboard_from_desc.reports[KEYBOARD_REPORT_ID].inputs.keyboard
        self.assertEqual(1,
                         pointer[0].value[3],
                         "bit4 of KeyPad Field values should be equal !")
        self.assertEqual(1,
                         pointer[0].value[6],
                         "bit1 of KeyPad Field values should be equal !")
    # end def test_footlose_interface1

    def test_raylan_interface1(self):
        """
        Tests footloose interface 1 (KEYBOARD) parsing and deserializing
        """

        raylan_interface1 = bytes([
            0x05, 0x01,      # Usage Page (Generic Desktop Ctrls)
            0x09, 0x06,      # Usage 0x0006
            0xa1, 0x01,      # (BeginCollection (01) (level 0)
            0x05, 0x07,           # Usage Page 0x0007
            0x19, 0x00,           # Usage Min 0x0000
            0x29, 0xe7,           # Usage Max 0x00e7
            0x15, 0x00,           # Logical Min 0
            0x26, 0xe7, 0x00,        # Logical Max 231
            0x75, 0x08,           # Report Size 8
            0x95, 0x14,           # Report Count 20
            0x85, 0x01,           # Report ID 1
            0x81, 0x00,           # Input
            0xc0,            # EndCollection (level 0)
            0x05, 0x0c,      # Usage Page 0x000c
            0x09, 0x01,      # Usage 0x0001
            0xa1, 0x01,      # (BeginCollection (01) (level 0)
            0x85, 0x02,           # Report ID 2
            0x15, 0x00,           # Logical Min 0
            0x25, 0x01,           # Logical Max 1
            0x75, 0x01,           # Report Size 1
            0x95, 0x07,           # Report Count 7
            0x09, 0xb5,           # Usage 0x00b5
            0x09, 0xb6,           # Usage 0x00b6
            0x09, 0xb7,           # Usage 0x00b7
            0x09, 0xcd,           # Usage 0x00cd
            0x09, 0xe9,           # Usage 0x00e9
            0x09, 0xea,           # Usage 0x00ea
            0x09, 0xe2,           # Usage 0x00e2
            0x81, 0x02,           # Input
            0x95, 0x01,           # Report Count 1
            0x81, 0x01,           # Input
            0xc0,              # EndCollection (level 0)
            0x06, 0x43, 0xff,  # Usage Page 0xff43
            0x0a, 0x02, 0x06,  # Usage 0x0602
            0xa1, 0x01,        # (BeginCollection (01) (level 0)
            0x85, 0x11,           # Report ID 17
            0x75, 0x08,           # Report Size 8
            0x95, 0x13,           # Report Count 19
            0x15, 0x00,           # Logical Min 0
            0x26, 0xff, 0x00,     # Logical Max 255
            0x09, 0x02,           # Usage 0x0002
            0x81, 0x00,           # Input
            0x09, 0x02,           # Usage 0x0002
            0x91, 0x00,           # Output
            0xc0,              # EndCollection (level 0)
            0x06, 0x43, 0xff,  # Usage Page 0xff43
            0x0a, 0x04, 0x06,  # Usage 0x0604
            0xa1, 0x01,        # (BeginCollection (01) (level 0)
            0x85, 0x12,           # Report ID 18
            0x75, 0x08,           # Report Size 8
            0x95, 0x3f,           # Report Count 63
            0x15, 0x00,           # Logical Min 0
            0x26, 0xff, 0x00,     # Logical Max 255
            0x09, 0x04,           # Usage 0x0004
            0x81, 0x00,           # Input
            0x09, 0x04,           # Usage 0x0004
            0x91, 0x00,           # Output
            0xc0,              # EndCollection (level 0)
        ])

        # This returns a Device
        keyboard_from_desc = hidparser.parse(bytes(raylan_interface1.hex(), 'utf-8'))

    # end def test_raylan_interface1

# end class KeyboardTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
