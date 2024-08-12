#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.test.illunination_test

@brief  PyHid Illumination Descriptor parser testing module

@author christophe Roquebert

@date   2019/07/15
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest import TestCase

from pyhid import hidparser
from pyhid.hidparser.Device import Collection
from pyhid.hidparser.enums import ReportType
from pylibrary.tools.util import reverse_bits


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class IllunminationTestCase(TestCase):                                               #pylint:disable=R0904
    """
    Tests of the BitField class
    """

    EXAMPLE_DESCRIPTOR = bytes([
        0x05, 0x59,    # USAGE_PAGE(LightingAndIllumination)
        0x09, 0x01,    # USAGE(LampArray)
        0xa1, 0x01,    # COLLECTION(Application)
        0x85, 0x01,    # REPORT_ID(1)
        0x09, 0x02,    # USAGE(LampArrayAttributesReport)
        0xa1, 0x02,    # COLLECTION(Logical)
        0x09, 0x03,    # USAGE(LampCount)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0x00, 0x00,    # LOGICAL_MAXIMUM(65535)
        0x75, 0x10,    # REPORT_SIZE(16)
        0x95, 0x01,    # REPORT_COUNT(1)
        0xb1, 0x03,    # FEATURE(Cnst, Var, Abs)
        0x09, 0x04,    # USAGE(BoundingBoxWidthInMicrometers)
        0x09, 0x05,    # USAGE(BoundingBoxHeightInMicrometers)
        0x09, 0x06,    # USAGE(BoundingBoxDepthInMicrometers)
        0x09, 0x07,    # USAGE(LampArrayKind)
        0x09, 0x08,    # USAGE(MinUpdateIntervalInMicroseconds)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0xff, 0x7f,    # LOGICAL_MAXIMUM(2147483647)
        0x75, 0x20,    # REPORT_SIZE(32)
        0x95, 0x05,    # REPORT_COUNT(5)
        0xb1, 0x03,    # FEATURE(Cnst, Var, Abs)
        0xc0,    # END_COLLECTION
        0x85, 0x02,    # REPORT_ID(2)
        0x09, 0x20,    # USAGE(LampAttributesRequestReport)
        0xa1, 0x02,    # COLLECTION(Logical)
        0x09, 0x21,    # USAGE(LampId)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0x00, 0x00,    # LOGICAL_MAXIMUM(65535)
        0x75, 0x10,    # REPORT_SIZE(16)
        0x95, 0x01,    # REPORT_COUNT(1)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0xc0,    # END_COLLECTION
        0x85, 0x03,    # REPORT_ID(3)
        0x09, 0x22,    # USAGE(LampAttributesReponseReport)
        0xa1, 0x02,    # COLLECTION(Logical)
        0x09, 0x21,    # USAGE(LampId)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0x00, 0x00,    # LOGICAL_MAXIMUM(65535)
        0x75, 0x10,    # REPORT_SIZE(16)
        0x95, 0x01,    # REPORT_COUNT(1)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0x09, 0x23,    # USAGE(PositionXInMicrometers)
        0x09, 0x24,    # USAGE(PositionYInMicrometers)
        0x09, 0x25,    # USAGE(PositionZInMicrometers)
        0x09, 0x27,    # USAGE(UpdateLatencyInMicroseconds)
        0x09, 0x26,    # USAGE(LampPurposes)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0xff, 0x7f,    # LOGICAL_MAXIMUM(2147483647)
        0x75, 0x20,    # REPORT_SIZE(32)
        0x95, 0x05,    # REPORT_COUNT(5)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0x09, 0x28,    # USAGE(RedLevelCount)
        0x09, 0x29,    # USAGE(GreenLevelCount)
        0x09, 0x2a,    # USAGE(BlueLevelCount)
        0x09, 0x2b,    # USAGE(IntensityLevelCount)
        0x09, 0x2c,    # USAGE(IsProgrammable)
        0x09, 0x2d,    # USAGE(InputBinding)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x26, 0xff, 0x00,    # LOGICAL_MAXIMUM(255)
        0x75, 0x08,    # REPORT_SIZE(8)
        0x95, 0x06,    # REPORT_COUNT(6)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0xc0,    # END_COLLECTION
        0x85, 0x04,    # REPORT_ID(4)
        0x09, 0x50,    # USAGE(LampMultiUpdateReport)
        0xa1, 0x02,    # COLLECTION(Logical)
        0x09, 0x03,    # USAGE(LampCount)
        0x09, 0x55,    # USAGE(LampUpdateFlags)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x25, 0x08,    # LOGICAL_MAXIMUM(8)
        0x75, 0x08,    # REPORT_SIZE(8)
        0x95, 0x02,    # REPORT_COUNT(2)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0x09, 0x21,    # USAGE(LampId)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0x00, 0x00,    # LOGICAL_MAXIMUM(65535)
        0x75, 0x10,    # REPORT_SIZE(16)
        0x95, 0x08,    # REPORT_COUNT(8)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel )
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel )
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x26, 0xff, 0x00,    # LOGICAL_MAXIMUM(255)
        0x75, 0x08,    # REPORT_SIZE(8)
        0x95, 0x20,    # REPORT_COUNT(32)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0xc0,    # END_COLLECTION
        0x85, 0x05,    # REPORT_ID(5)
        0x09, 0x60,    # USAGE(LampRangeUpdateReport)
        0xa1, 0x02,    # COLLECTION(Logical)
        0x09, 0x55,    # USAGE(LampUpdateFlags)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x25, 0x08,    # LOGICAL_MAXIMUM(8)
        0x75, 0x08,    # REPORT_SIZE(8)
        0x95, 0x01,    # REPORT_COUNT(1)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0x09, 0x61,    # USAGE(LampIdStart)
        0x09, 0x62,    # USAGE(LampIdEnd)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x27, 0xff, 0xff, 0x00, 0x00,    # LOGICAL_MAXIMUM(65535)
        0x75, 0x10,    # REPORT_SIZE(16)
        0x95, 0x02,    # REPORT_COUNT(2)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0x09, 0x51,    # USAGE(RedUpdateChannel)
        0x09, 0x52,    # USAGE(GreenUpdateChannel)
        0x09, 0x53,    # USAGE(BlueUpdateChannel)
        0x09, 0x54,    # USAGE(IntensityUpdateChannel)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x26, 0xff, 0x00,    # LOGICAL_MAXIMUM(255)
        0x75, 0x08,    # REPORT_SIZE(8)
        0x95, 0x04,    # REPORT_COUNT(4)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0xc0,    # END_COLLECTION
        0x85, 0x06,    # REPORT_ID(6)
        0x09, 0x70,    # USAGE(LampArrayControlReport)
        0xa1, 0x02,    # COLLECTION(Logical)
        0x09, 0x71,    # USAGE(AutonomousMode)
        0x15, 0x00,    # LOGICAL_MINIMUM(0)
        0x25, 0x01,    # LOGICAL_MAXIMUM(1)
        0x75, 0x08,    # REPORT_SIZE(8)
        0x95, 0x01,    # REPORT_COUNT(1)
        0xb1, 0x02,    # FEATURE(Data, Var, Abs)
        0xc0,    # END_COLLECTION
        0xc0    # END_COLLECTION
    ])

    def test_example_descriptor(self):
        """
        Tests example descriptor coming from:
        file:hutrr84_-_lighting_and_illumination_page.pdf
        """
        # Report ID
        LAMP_ARRAY_ATTRIBUTES_REPORT_ID = 1
        LAMP_ATTRIBUTES_REQUEST_REPORT_ID = 2

        # This returns a Device
        device_from_desc = hidparser.parse(bytes(self.EXAMPLE_DESCRIPTOR.hex(), 'utf-8'))

        lamp_array = device_from_desc.reports[LAMP_ARRAY_ATTRIBUTES_REPORT_ID].features.lamp_array
        self.assertIsInstance(lamp_array,
                              Collection,
                              "lamp array shall be of type Collection !")
        lamp_array_attributes_report = device_from_desc.reports[LAMP_ARRAY_ATTRIBUTES_REPORT_ID].features.lamp_array.lamp_array_attributes_report
        self.assertIsInstance(lamp_array_attributes_report,
                              Collection,
                              "lamp array attributes reports hall be of type Collection !")
        # ------------------------------
        # Check LampCount attributes
        # ------------------------------
        self.assertEqual(lamp_array_attributes_report[0].size,
                         16,
                         "lamp_array_attributes_report[0] size shall be equal to 16 !")
        self.assertEqual(lamp_array_attributes_report[0].count,
                         1,
                         "lamp_array_attributes_report[0] count shall be equal to 1 !")
        self.assertEqual(lamp_array_attributes_report[0].report_type,
                         ReportType.FEATURE,
                         "lamp_array_attributes_report[0] type shall be equal to FEATURE !")
        # ------------------------------
        # Check BOUNDING_BOX_WIDTH_IN_MICROMETERS attribute
        # ------------------------------
        self.assertEqual(lamp_array_attributes_report[1].size,
                         32,
                         "lamp_array_attributes_report[1] size shall be equal to 16 !")
        self.assertEqual(lamp_array_attributes_report[1].count,
                         5,
                         "lamp_array_attributes_report[1] count shall be equal to 1 !")
        self.assertEqual(lamp_array_attributes_report[1].report_type,
                         ReportType.FEATURE,
                         "lamp_array_attributes_report[1] type shall be equal to FEATURE !")

        # ------------------------------
        # Tests values
        # ------------------------------
        raw_lamp_count = 0x30   # 48 lamps
        lamp_count = reverse_bits(raw_lamp_count, 16)
        raw_width = 0x06B6C0   # Width = 440 000 um
        width = reverse_bits(raw_width, 32)
        raw_height = 0x020F58   # Height = 135 000 um
        height = reverse_bits(raw_height, 32)
        raw_depth = 0x7530  # Depth = 30 000 um
        depth = reverse_bits(raw_depth, 32)
        raw_kind = 0x01   # LampArrayKind = LampArray is part of a keyboard/keypad device
        kind = reverse_bits(raw_kind, 32)
        raw_interval = 0x64   # MinUpdateIntervalInMicroseconds = 100 ms
        interval = reverse_bits(raw_interval, 32)
        #
        # Read from the physical device
        data = bytes([LAMP_ARRAY_ATTRIBUTES_REPORT_ID,
                      (lamp_count >> 8), (lamp_count & 0xFF),
                      (width >> 24) & 0xFF, (width >> 16) & 0xFF, (width >> 8) & 0xFF, (width & 0xFF),
                      (height >> 24) & 0xFF, (height >> 16) & 0xFF, (height >> 8) & 0xFF, (height & 0xFF),
                      (depth >> 24) & 0xFF, (depth >> 16) & 0xFF, (depth >> 8) & 0xFF, (depth & 0xFF),
                      (kind >> 24) & 0xFF, (kind >> 16) & 0xFF, (kind >> 8) & 0xFF, (kind & 0xFF),
                      (interval >> 24) & 0xFF, (interval >> 16) & 0xFF, (interval >> 8) & 0xFF, (interval & 0xFF),
                      ])
        # Deserialize the data and populate the object members
        device_from_desc.deserialize(data, ReportType.FEATURE)

        # Read data
        lamp_array_attributes_report = device_from_desc.reports[
            LAMP_ARRAY_ATTRIBUTES_REPORT_ID].features.lamp_array.lamp_array_attributes_report
        self.assertEqual(48,
                         lamp_array_attributes_report.lamp_count,
                         "lamp_count differs from expected value !")
        self.assertEqual(440000,
                         lamp_array_attributes_report.bounding_box_width_in_micrometers,
                         "bounding_box_width_in_micrometers differs from expected value !")
        self.assertEqual(1,
                         lamp_array_attributes_report.lamp_array_kind,
                         "lamp_array_kind differs from expected value !")
    # end def test_example_descriptor

    def test_lamp_multi_update_report(self):
        """
        Tests LampMultiUpdateReport coming from:
        file:hutrr84_-_lighting_and_illumination_page.pdf

        LampCount 0x05
        LampId #1 0x19
        LampId #2 0x23
        LampId #3 0x72
        LampId #4 0x56
        LampId #5 0x64
        LampId #6 (ignored)
        LampId #7 (ignored)
        LampId #8 (ignored)
        RGBI tuple #1 0xFF 0x00 0xFF 0x80
        RGBI tuple #2 0x80 0x80 0xFF 0xFF
        RGBI tuple #3 0x00 0x00 0x80 0xFF
        RGBI tuple #4 0xFF 0x80 0x00 0x80
        RGBI tuple #5 0xFF 0xFF 0x00 0xFF
        RGBI tuple #6 (ignored)
        RGBI tuple #7 (ignored)
        RGBI tuple #8 (ignored)
        """
        LAMP_MULTI_UPDATE_REPORT_ID = 4

        # This returns a Device
        device_from_desc = hidparser.parse(bytes(self.EXAMPLE_DESCRIPTOR.hex(), 'utf-8'))

        lamp_multi_update = device_from_desc.reports[LAMP_MULTI_UPDATE_REPORT_ID].features.lamp_array

        raw_lamp_count = 0x05  # 5 lamps
        lamp_count = reverse_bits(raw_lamp_count, 8)
        raw_lamp_flags = 0x01
        lamp_flags = reverse_bits(raw_lamp_flags, 8)
        raw_lamp_id_1 = 0x19
        lamp_id_1 = reverse_bits(raw_lamp_id_1, 16)
        raw_lamp_id_2 = 0x23
        lamp_id_2 = reverse_bits(raw_lamp_id_2, 16)
        raw_lamp_id_3 = 0x72
        lamp_id_3 = reverse_bits(raw_lamp_id_3, 16)
        raw_lamp_id_4 = 0x56
        lamp_id_4 = reverse_bits(raw_lamp_id_4, 16)
        raw_lamp_id_5 = 0x64
        lamp_id_5 = reverse_bits(raw_lamp_id_5, 16)
        raw_rgb_1 = 0xFF00FF80
        rgb_1 = reverse_bits(raw_rgb_1, 32)
        raw_rgb_2 = 0x8080FFFF
        rgb_2 = reverse_bits(raw_rgb_2, 32)
        raw_rgb_3 = 0x000080FF
        rgb_3 = reverse_bits(raw_rgb_3, 32)
        raw_rgb_4 = 0xFF800080
        rgb_4 = reverse_bits(raw_rgb_4, 32)
        raw_rgb_5 = 0xFFFF00FF
        rgb_5 = reverse_bits(raw_rgb_5, 32)

        # Read from the physical device
        data = bytes([LAMP_MULTI_UPDATE_REPORT_ID,
                      lamp_count, lamp_flags,
                      (lamp_id_1 >> 8), (lamp_id_1 & 0xFF),
                      (lamp_id_2 >> 8), (lamp_id_2 & 0xFF),
                      (lamp_id_3 >> 8), (lamp_id_3 & 0xFF),
                      (lamp_id_4 >> 8), (lamp_id_4 & 0xFF),
                      (lamp_id_5 >> 8), (lamp_id_5 & 0xFF),
                      0x00, 0x00,
                      0x00, 0x00,
                      0x00, 0x00,
                      (rgb_1 >> 24) & 0xFF, (rgb_1 >> 16) & 0xFF, (rgb_1 >> 8) & 0xFF, (rgb_1 & 0xFF),
                      (rgb_2 >> 24) & 0xFF, (rgb_2 >> 16) & 0xFF, (rgb_2 >> 8) & 0xFF, (rgb_2 & 0xFF),
                      (rgb_3 >> 24) & 0xFF, (rgb_3 >> 16) & 0xFF, (rgb_3 >> 8) & 0xFF, (rgb_3 & 0xFF),
                      (rgb_4 >> 24) & 0xFF, (rgb_4 >> 16) & 0xFF, (rgb_4 >> 8) & 0xFF, (rgb_4 & 0xFF),
                      (rgb_5 >> 24) & 0xFF, (rgb_5 >> 16) & 0xFF, (rgb_5 >> 8) & 0xFF, (rgb_5 & 0xFF),
                      0xAA, 0xAA, 0xAA, 0xAA,
                      0xBB, 0xBB, 0xBB, 0xBB,
                      0xCC, 0xCC, 0xCC, 0xCC,
                      ])
        # Deserialize the data and populate the object members
        device_from_desc.deserialize(data, ReportType.FEATURE)

        pass

    # end def  test_lamp_multi_update_report

# end class IlluminationTestCase



if __name__ == '__main__':
    from unittest import main
    main()
# end if
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
