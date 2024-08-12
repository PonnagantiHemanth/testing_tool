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
from unittest import TestCase

from pyhid import hidparser
from pyhid.hidparser.Device import Collection
from pyhid.hidparser.enums import ReportType
from pylibrary.tools.numeral import RandNumeral
from pylibrary.tools.util import reverse_bits


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class MouseTestCase(TestCase):                                               #pylint:disable=R0904
    """
    Tests of the BitField class
    """

    def test_footlose_interface0(self):
        """
        Tests footloose interface 0 (MOUSE) parsing and deserializing
        """
        # Report ID
        MOUSE_REPORT_ID = 0
        # Report in Collection
        BUTTONS = 0
        XY = 1
        WHEEL = 2
        AC_PAN = 3

        footlose_interface0 = bytes([
            0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
            0x09, 0x02,  # USAGE (Mouse)
            0xa1, 0x01,  # COLLECTION (Application)
            0x09, 0x01,  # USAGE (Pointer)
            0xa1, 0x00,  # COLLECTION (Physical)
            0x95, 0x10,  # REPORT COUNT(16)
            0x75, 0x01,  # REPORT SIZE (1)
            0x15, 0x00,  # LOGICAL_MINIMUM (0)
            0x25, 0x01,  # LOGICAL_MAXIMUM (1)
            0x05, 0x09,  # USAGE_PAGE (Button)
            0x19, 0x01,  # USAGE_MINIMUM (Button 1)
            0x29, 0x10,  # USAGE_MAXIMUM (Button 16)
            0x81, 0x02,  # INPUT (Data,Var,Abs)
            0x95, 0x02,  # REPORT_COUNT (2)
            0x75, 0x10,  # REPORT_SIZE (16)
            0x16, 0x01, 0x80,  # LOGICAL MINIMUM (-32 767)
            0x26, 0xFF, 0x7F,  # LOGICAL MINIMUM (+32 767)
            0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
            0x09, 0x30,  # USAGE (X)
            0x09, 0x31,  # USAGE (Y)
            0x81, 0x06,  # INPUT (Data,Var,Rel)
            0x95, 0x01,  # REPORT_COUNT (1)
            0x75, 0x08,  # REPORT_SIZE (8)
            0x15, 0x81,  # LOGICAL_MINIMUM (-127)
            0x25, 0x7f,  # LOGICAL_MAXIMUM (127)
            0x09, 0x38,  # USAGE_(Wheel)
            0x81, 0x06,  # INPUT (Data,Value,Relative,Bit Field)
            0x95, 0x01,  # REPORT_COUNT (1)
            0x05, 0x0C,  # USAGE_PAGE (Consumer)
            0x0A, 0x38, 0x02,  # USAGE (AC Pan)
            0x81, 0x06,  # INPUT (Data,Value,Relative,Bit Field)
            0xc0,  # END_COLLECTION
            0xc0  # END_COLLECTION
        ])

        # This returns a Device
        mouse_from_desc = hidparser.parse(bytes(footlose_interface0.hex(), 'utf-8'))

        pointer = mouse_from_desc.reports[MOUSE_REPORT_ID].inputs.mouse.pointer
        self.assertIsInstance(pointer,
                              Collection,
                              "mouse.pointer shall be of type Collection !")
        # ------------------------------
        # Check Button attributes
        # ------------------------------
        self.assertEqual(pointer[BUTTONS].size,
                         1,
                         "Buttons size shall be equal to 1 !")
        self.assertEqual(pointer[BUTTONS].count,
                         16,
                         "Buttons count shall be equal to 16 !")
        self.assertEqual(pointer[BUTTONS].report_type,
                         ReportType.INPUT,
                         "Buttons report type shall be equal to INPUT !")
        # ------------------------------
        # Check XY attribute
        # ------------------------------
        self.assertEqual(pointer[XY].size,
                         16,
                         "X size shall be equal to 16 !")
        self.assertEqual(pointer[XY].count,
                         2,
                         "X count shall be equal to 2 !")
        self.assertEqual(pointer[XY].report_type,
                         ReportType.INPUT,
                         "X report type shall be equal to INPUT !")
        # ------------------------------
        # Check WHEEL attribute
        # ------------------------------
        self.assertEqual(pointer[WHEEL].size,
                         8,
                         "WHEEL size shall be equal to 8 !")
        self.assertEqual(pointer[WHEEL].count,
                         1,
                         "WHEEL count shall be equal to 1 !")
        self.assertEqual(pointer[WHEEL].report_type,
                         ReportType.INPUT,
                         "WHEEL report type shall be equal to INPUT !")
        # ------------------------------
        # Check AC_PAN attribute
        # ------------------------------
        self.assertEqual(pointer[AC_PAN].size,
                         8,
                         "AC_PAN size shall be equal to 8 !")
        self.assertEqual(pointer[AC_PAN].count,
                         1,
                         "AC_PAN count shall be equal to 1 !")
        self.assertEqual(pointer[AC_PAN].report_type,
                         ReportType.INPUT,
                         "AC_PAN report type shall be equal to INPUT !")

        # ------------------------------
        # Tests X and Y positives values
        # ------------------------------
        x_position = int(RandNumeral(2, maxVal=0x7FFF))
        y_position = int(RandNumeral(2, maxVal=0x7FFF))
        x = reverse_bits(x_position, 16)
        y = reverse_bits(y_position, 16)

        # Read from the physical device
        data = bytes([0x00, 0x00,
                      (x >> 8), (x & 0xFF),
                      (y >> 8), (y & 0xFF),
                      0x00, 0x00])
        # Deserialize the data and populate the object members
        mouse_from_desc.deserialize(data)

        # Read x,y from mouse
        pointer = mouse_from_desc.reports[MOUSE_REPORT_ID].inputs.mouse.pointer
        self.assertEqual(x_position,
                         pointer.x,
                         "X Field values should be equal !")
        self.assertEqual(y_position,
                         pointer.y,
                         "Y Field values should be equal !")

        # ------------------------------
        # Tests X and Y negatives values
        # ------------------------------
        x_position = int(RandNumeral(2, minVal=0x8000))
        y_position = int(RandNumeral(2, minVal=0x8000))
        x = reverse_bits(x_position, 16)
        y = reverse_bits(y_position, 16)

        # Read from the physical device
        data = bytes([0x00, 0x00,
                      (x >> 8), (x & 0xFF),
                      (y >> 8), (y & 0xFF),
                      0x00, 0x00])
        # Deserialize the data and populate the object members
        mouse_from_desc.deserialize(data)

        # Read x,y from mouse
        pointer = mouse_from_desc.reports[MOUSE_REPORT_ID].inputs.mouse.pointer
        self.assertEqual(x_position-0x10000,
                         pointer.x,
                         "X Field values should be equal !")
        self.assertEqual(y_position-0x10000,
                         pointer.y,
                         "Y Field values should be equal !")
    # end def test_footlose_interface0

    def test_graviton_interface0(self):
        """
        Tests graviton interface 0 (MOUSE) parsing and deserializing
        """
        # Report ID
        MOUSE_REPORT_ID = 2
        # Report in Collection
        BUTTONS = 0
        XY = 1
        WHEEL = 2
        AC_PAN = 3

        graviton_interface0 = bytes([

            0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
            0x09, 0x02,  # USAGE (Mouse)
            0xA1, 0x01,  # COLLECTION (Application)
            0x85, 0x02,  # REPORT ID (2)
            0x09, 0x01,  # USAGE (Pointer)
            0xA1, 0x00,  # COLLECTION (Physical)
            0x95, 0x10,  # REPORT_COUNT (16)
            0x75, 0x01,  # REPORT SIZE (1)
            0x15, 0x00,
            0x25, 0x01,
            0x05, 0x09,  # USAGE_PAGE ()
            0x19, 0x01,
            0x29, 0x10,
            0x81, 0x02,
            0x95, 0x02,  # REPORT_COUNT (2)
            0x75, 0x10,  # REPORT SIZE (16)
            0x16, 0x01, 0x80,
            0x26, 0xFF, 0x7F,
            0x05, 0x01,  # USAGE_PAGE ()
            0x09, 0x30,  # USAGE (X)
            0x09, 0x31,  # USAGE (Y)
            0x81, 0x06,
            0x95, 0x01,  # REPORT_COUNT (1)
            0x75, 0x08,  # REPORT SIZE (8)
            0x15, 0x81,  # LOGICAL_MINIMUM (-127)
            0x25, 0x7F,
            0x09, 0x38,  # USAGE (Wheel)
            0x81, 0x06,  # INPUT (Data,Value,Relative,Bit Field)
            0x95, 0x01,  # REPORT_COUNT (1)
            0x05, 0x0C,  # USAGE_PAGE (Consumer)
            0x0A, 0x38, 0x02,  # USAGE (AC Pan)
            0x81, 0x06,  # INPUT (Data,Value,Relative,Bit Field)
            0xC0,  # END_COLLECTION
            0xC0,  # END_COLLECTION
            0x05, 0x0C,  # USAGE_PAGE (Consumer)
            0x09, 0x01,  # USAGE (Pointer)
            0xA1, 0x01,  # COLLECTION (Application)
            0x85, 0x03,  # REPORT ID (3)
            0x95, 0x02,  # REPORT_COUNT (2)
            0x75, 0x10,  # REPORT SIZE (16)
            0x15, 0x01,  # LOGICAL_MINIMUM (-1)
            0x26, 0xFF, 0x02,  # LOGICAL_MAXIMUM (767)
            0x19, 0x01,  # USAGE_MINIMUM (Button 1)
            0x2A, 0xFF, 0x02,
            0x81, 0x00,
            0xC0,  # END_COLLECTION
            0x05, 0x01,  # USAGE_PAGE (Generic Desktop)
            0x09, 0x80,  # USAGE (System Control)
            0xA1, 0x01,  # COLLECTION (Application)
            0x85, 0x04,  # REPORT ID (4)
            0x95, 0x01,  # REPORT_COUNT (1)
            0x75, 0x02,  # REPORT SIZE (2)
            0x15, 0x01,
            0x25, 0x03,
            0x09, 0x82,  # USAGE (System Sleep)
            0x09, 0x81,  # USAGE (System Power Down)
            0x09, 0x83,  # USAGE (System Wake Up)
            0x81, 0x00,
            0x75, 0x06,  # REPORT SIZE (6)
            0x81, 0x03,
            0xC0  # END_COLLECTION
        ])

        # This returns a Device
        mouse_from_desc = hidparser.parse(bytes(graviton_interface0.hex(), 'utf-8'))

        pointer = mouse_from_desc.reports[MOUSE_REPORT_ID].inputs.mouse.pointer
        self.assertIsInstance(pointer,
                              Collection,
                              "mouse.pointer shall be of type Collection !")
        # ------------------------------
        # Check Button attributes
        # ------------------------------
        self.assertEqual(pointer[BUTTONS].size,
                         1,
                         "Buttons size shall be equal to 1 !")
        self.assertEqual(pointer[BUTTONS].count,
                         16,
                         "Buttons count shall be equal to 16 !")
        self.assertEqual(pointer[BUTTONS].report_type,
                         ReportType.INPUT,
                         "Buttons report type shall be equal to INPUT !")
        # ------------------------------
        # Check XY attribute
        # ------------------------------
        self.assertEqual(pointer[XY].size,
                         16,
                         "X size shall be equal to 16 !")
        self.assertEqual(pointer[XY].count,
                         2,
                         "X count shall be equal to 2 !")
        self.assertEqual(pointer[XY].report_type,
                         ReportType.INPUT,
                         "X report type shall be equal to INPUT !")
        # ------------------------------
        # Check WHEEL attribute
        # ------------------------------
        self.assertEqual(pointer[WHEEL].size,
                         8,
                         "WHEEL size shall be equal to 8 !")
        self.assertEqual(pointer[WHEEL].count,
                         1,
                         "WHEEL count shall be equal to 1 !")
        self.assertEqual(pointer[WHEEL].report_type,
                         ReportType.INPUT,
                         "WHEEL report type shall be equal to INPUT !")
        # ------------------------------
        # Check AC_PAN attribute
        # ------------------------------
        self.assertEqual(pointer[AC_PAN].size,
                         8,
                         "AC_PAN size shall be equal to 8 !")
        self.assertEqual(pointer[AC_PAN].count,
                         1,
                         "AC_PAN count shall be equal to 1 !")
        self.assertEqual(pointer[AC_PAN].report_type,
                         ReportType.INPUT,
                         "AC_PAN report type shall be equal to INPUT !")

        # ------------------------------
        # Tests X and Y positives values
        # ------------------------------
        x_position = int(RandNumeral(2, maxVal=0x7FFF))
        y_position = int(RandNumeral(2, maxVal=0x7FFF))
        x = reverse_bits(x_position, 16)
        y = reverse_bits(y_position, 16)

        # Read from the physical device
        data = bytes([0x02, 0x00, 0x00,
                      (x >> 8), (x & 0xFF),
                      (y >> 8), (y & 0xFF),
                      0x00, 0x00])
        # Deserialize the data and populate the object members
        mouse_from_desc.deserialize(data)

        # Read x,y from mouse
        pointer = mouse_from_desc.reports[MOUSE_REPORT_ID].inputs.mouse.pointer
        self.assertEqual(x_position,
                         pointer.x,
                         "X Field values should be equal !")
        self.assertEqual(y_position,
                         pointer.y,
                         "Y Field values should be equal !")

        # ------------------------------
        # Tests X and Y negatives values
        # ------------------------------
        x_position = int(RandNumeral(2, minVal=0x8000))
        y_position = int(RandNumeral(2, minVal=0x8000))
        x = reverse_bits(x_position, 16)
        y = reverse_bits(y_position, 16)

        # Read from the physical device
        data = bytes([0x02, 0x00, 0x00,
                      (x >> 8), (x & 0xFF),
                      (y >> 8), (y & 0xFF),
                      0x00, 0x00])
        # Deserialize the data and populate the object members
        mouse_from_desc.deserialize(data)

        # Read x,y from mouse
        pointer = mouse_from_desc.reports[MOUSE_REPORT_ID].inputs.mouse.pointer
        self.assertEqual(x_position-0x10000,
                         pointer.x,
                         "X Field values should be equal !")
        self.assertEqual(y_position-0x10000,
                         pointer.y,
                         "Y Field values should be equal !")
    # end def test_footlose_interface0

# end class MouseTestCase

if __name__ == '__main__':
    from unittest import main
    main()
# end if
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
