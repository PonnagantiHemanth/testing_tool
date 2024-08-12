#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.spidirectaccessutils
:brief:  Helpers for SPI Direct Access feature
:author: Fred Chen <fchen7@logitech.com>
:date:   2020/11/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from warnings import warn

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.spidirectaccess import GetNbDevicesResponse
from pyhid.hidpp.features.common.spidirectaccess import GetSelectedDeviceResponse
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccess
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccessFactory
from pyhid.hidpp.features.common.spidirectaccess import SelectDeviceResponseV0
from pyhid.hidpp.features.common.spidirectaccess import SelectDeviceResponseV1
from pyhid.hidpp.features.common.spidirectaccess import SpiDirectAccessResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# Constant
# ----------------------------------------------------------------------------------------------------------------------
NEXT_CMD = 0x80  # The recommended value to use as the next command in a transaction
HERO_SENSOR_HIGH_SPEED_THRESHOLD = 12800  # The DPI step changed from 50 to 100
SPI_DATA_MAX_LEN = 15
PAW3333_DPI_TABLE = {
    0: 50,
    1: 100,
    2: 150,
    4: 200,
    5: 250,
    6: 300,
    7: 350,
    8: 400,
    9: 450,
    10: 500,
    11: 500,
    13: 600,
    14: 650,
    15: 700,
    16: 750,
    17: 800,
    18: 850,
    19: 900,
    20: 950,
    22: 1000,
    23: 1050,
    24: 1100,
    25: 1150,
    26: 1200,
    27: 1250,
    28: 1300,
    29: 1350,
    31: 1400,
    32: 1450,
    33: 1500,
    34: 1550,
    35: 1600,
    36: 1650,
    37: 1700,
    38: 1750,
    40: 1800,
    41: 1850,
    42: 1900,
    43: 1950,
    44: 2000,
    45: 2050,
    46: 2100,
    47: 2150,
    49: 2200,
    50: 2250,
    51: 2300,
    52: 2350,
    53: 2400,
    54: 2450,
    55: 2500,
    56: 2550,
    58: 2600,
    59: 2650,
    63: 2700,
    64: 2750,
    65: 2800,
    66: 2850,
    68: 2900,
    69: 2950,
    70: 3000,
    71: 3050,
    72: 3100,
    73: 3150,
    75: 3200,
    76: 3250,
    77: 3300,
    78: 3350,
    79: 3400,
    80: 3450,
    82: 3500,
    83: 3550,
    84: 3600,
    85: 3650,
    86: 3700,
    88: 3750,
    89: 3800,
    90: 3850,
    91: 3900,
    92: 3950,
    94: 4000,
    95: 4050,
    96: 4100,
    97: 4150,
    98: 4200,
    99: 4250,
    101: 4300,
    102: 4350,
    103: 4400,
    104: 4450,
    105: 4500,
    106: 4550,
    108: 4600,
    109: 4650,
    110: 4700,
    111: 4750,
    112: 4800,
    114: 4850,
    115: 4900,
    116: 4950,
    117: 5000,
    118: 5050,
    119: 5100,
    121: 5150,
    122: 5200,
    123: 5250,
    124: 5300,
    125: 5350,
    127: 5400,
    128: 5450,
    129: 5500,
    130: 5550,
    131: 5600,
    133: 5650,
    134: 5700,
    135: 5750,
    136: 5800,
    137: 5850,
    138: 5900,
    140: 5950,
    141: 5600,
    142: 6050,
    143: 6100,
    144: 6150,
    145: 6200,
    147: 6250,
    148: 6300,
    149: 6350,
    150: 6400,
    151: 6450,
    152: 6500,
    154: 6550,
    155: 6600,
    156: 6650,
    157: 6700,
    159: 6750,
    160: 6800,
    161: 6850,
    162: 6900,
    163: 6950,
    164: 7000,
    166: 7050,
    167: 7100,
    168: 7150,
    169: 7200,
    170: 7250,
    171: 7300,
    173: 7350,
    174: 7400,
    175: 7450,
    176: 7500,
    177: 7550,
    179: 7600,
    180: 7650,
    181: 7700,
    182: 7750,
    183: 7800,
    184: 7850,
    186: 7900,
    187: 7950,
    188: 8000
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OpticalSensorName:
    HERO = 'HERO'
    HERO2 = 'HERO2'
    ROBIN = 'ROBIN'
    TCOB_TRACKBALL = 'TCOB'
    TCOB_NO_TRACKBALL = 'TCOB_NO_TRACKBALL'
    PAW3333 = 'PAW3333'
    TOG6 = 'TOG6'
    TOGX = 'TOGX'
    PLUTO = 'PLUTO'
# end class OpticalSensorName


SPI_PERIPHERAL_REGISTER_DICT = {
    # E7788 Hero sensor - https://drive.google.com/drive/search?q=e7788
    OpticalSensorName.HERO: {
        'product_id': {
            'address': 0x80 | 0x00,
            'value': 0x88,
        },
        'dpi_x': {
            'address': 0x80 | 0x0C,
            'value': 0x1F,
        },
        'dpi_y': {
            'address': 0x80 | 0x0D,
            'value': 0x1F,
        },
    },
    # E7790 Hero2 sensor - https://drive.google.com/drive/search?q=e7790
    OpticalSensorName.HERO2: {
        'product_id': {
            'address': 0x80 | 0x00,
            'value': 0x90,
        },
        'dpi_x': {
            'address': 0x80 | 0x0C,
            'value': 0x1F,
        },
        'dpi_y': {
            'address': 0x80 | 0x0D,
            'value': 0x1F,
        },
        'dpi_step': {
            'address': 0x80 | 0x0E,
            'value': 0x31,
        },
        'res_cor_h': {
            'address': 0x80 | 0x1C,
            'value': 0x00,
        },
        'res_cor_l': {
            'address': 0x80 | 0x1D,
            'value': 0x00,
        }
    },
    # E7792 Robin sensor - https://drive.google.com/drive/search?q=E7792
    OpticalSensorName.ROBIN: {
        'product_id': {
            'address': 0x80 | 0x00,
            'value': 0x92,
        },
        'dpi_x': {
            'address': 0x80 | 0x20,
            'value': 0x1F,
        },
        'dpi_y': {
            'address': 0x80 | 0x24,
            'value': 0x1F,
        },
    },
    # PWA3266DW TCOB Trackball sensor - https://drive.google.com/drive/folders/15tK2Yp8c42B-OhyzAQ7nRBewDkg84Om8
    OpticalSensorName.TCOB_TRACKBALL: {
        'product_id': {
            'address': 0x00,
            'value': 0x4B,
        },
        'dpi_x_lo': {
            'address': 0x48,
            'value': 0x00,
        },
        'dpi_y_lo': {
            'address': 0x49,
            'value': 0x00,
        },
        'dpi_x_y_hi': {
            'address': 0x4A,
            'value': 0x22,
        }
    },
    # PWA3266DW TCOB NO Trackball sensor - https://drive.google.com/drive/folders/15tK2Yp8c42B-OhyzAQ7nRBewDkg84Om8
    OpticalSensorName.TCOB_NO_TRACKBALL: {
        'product_id': {
            'address': 0x00,
            'value': 0x4B,
        },
        'dpi_x_lo': {
            'address': 0x48,
            'value': 0x00,
        },
        'dpi_y_lo': {
            'address': 0x49,
            'value': 0x00,
        },
        'dpi_x_y_hi': {
            'address': 0x4A,
            'value': 0x22,
        }
    },
    # PAW3333 sensor - https://drive.google.com/drive/search?q=paw%203333
    OpticalSensorName.PAW3333: {
        'product_id': {
            'address': 0x00,
            'value': 0x4C,
        },
        'dpi': {
            'address': 0x1B,
            'value': 0x21,
        }
    },
    # TOG6 sensor - https://drive.google.com/drive/folders/1zfZQUaBs9OwSOJgT8VaDb09oeSaQ1fDT
    OpticalSensorName.TOG6: {
        'product_id': {
            'address': 0x00,
            'value': 0x49,
            'reset': 0x49
        },
        'revision_id': {
            'address': 0x01,
            'value': 0x00,
            'reset': 0x00
        },
        'motion': {
            'address': 0x02,
            'value': (),
            'reset': 0x00
        },
        'delta_x_l': {
            'address': 0x03,
            'value': (),
            'reset': 0x00
        },
        'delta_x_h': {
            'address': 0x04,
            'value': (),
            'reset': 0x00
        },
        'delta_y_l': {
            'address': 0x05,
            'value': (),
            'reset': 0x00
        },
        'delta_y_h': {
            'address': 0x06,
            'value': (),
            'reset': 0x00
        },
        'squal': {
            'address': 0x07,
            'value': (),
            'reset': 0x00
        },
        'pixel_sum': {
            'address': 0x08,
            'value': (),
            'reset': 0x00
        },
        'maximum_pixel': {
            'address': 0x09,
            'value': (),
            'reset': 0x00
        },
        'minimum_pixel': {
            'address': 0x0A,
            'value': (),
            'reset': 0x00
        },
        'shutter_lower': {
            'address': 0x0B,
            'value': (),
            'reset': 0x00
        },
        'shutter_upper': {
            'address': 0x0C,
            'value': (),
            'reset': 0x00
        },
        'chip_observation': {
            'address': 0x15,
            'value': (),
            'reset': 0x00
        },
        'burst_motion_read': {
            'address': 0x16,
            'value': (),
            'reset': 0x00
        },
        'powerup_reset': {
            'address': 0x3A,
            'value': (),
            'reset': ()
        },
        'shutdown': {
            'address': 0x3B,
            'value': (),
            'reset': ()
        },
        'performance': {
            'address': 0x40,
            'value': (),
            'reset': 0x00
        },
        'dpi': {
            'address': 0x4E,
            'value': (),
            'reset': 0x14
        },
        'pixel_grab': {
            'address': 0x58,
            'value': (),
            'reset': 0x0
        },
        'pixel_grab_status': {
            'address': 0x59,
            'value': (),
            'reset': 0x00
        },
        'axis_control': {
            'address': 0x59,
            'value': (),
            'reset': 0xE0
        },
        'inv_product_id': {
            'address': 0x5F,
            'value': 0xB6,
            'reset': 0xB6
        },
        'rest1_period_glass': {
            'address': 0x70,
            'value': (),
            'reset': 0x09
        },
        'rest1_downshift_glass': {
            'address': 0x71,
            'value': (),
            'reset': 0x10
        },
        'run_downshift': {
            'address': 0x77,
            'value': (),
            'reset': 0x03
        },
        'rest1_period_nonglass': {
            'address': 0x78,
            'value': (),
            'reset': 0x09
        },
        'rest1_downshift_nonglass': {
            'address': 0x79,
            'value': (),
            'reset': 0x10
        },
        'rest2_period': {
            'address': 0x7A,
            'value': (),
            'reset': 0x19
        },
        'rest2_downshift': {
            'address': 0x7B,
            'value': (),
            'reset': 0x5E
        },
        'rest3_period': {
            'address': 0x7C,
            'value': (),
            'reset': 0x3F
        },
    },
    # TOGX sensor - https://drive.google.com/drive/folders/1OE2ecgEvqSsFuawL4NoMZpUrBv-hgkgv
    OpticalSensorName.TOGX: {
        'product_id': {
            'address': 0x00,
            'value': 0x49,
            'reset': 0x49
        },
        'revision_id': {
            'address': 0x01,
            'value': 0x00,
            'reset': 0x00
        },
        'motion': {
            'address': 0x02,
            'value': (),
            'reset': 0x00
        },
        'delta_x_l': {
            'address': 0x03,
            'value': (),
            'reset': 0x00
        },
        'delta_x_h': {
            'address': 0x04,
            'value': (),
            'reset': 0x00
        },
        'delta_y_l': {
            'address': 0x05,
            'value': (),
            'reset': 0x00
        },
        'delta_y_h': {
            'address': 0x06,
            'value': (),
            'reset': 0x00
        },
        'squal': {
            'address': 0x07,
            'value': (),
            'reset': 0x00
        },
        'pixel_sum': {
            'address': 0x08,
            'value': (),
            'reset': 0x00
        },
        'maximum_pixel': {
            'address': 0x09,
            'value': (),
            'reset': 0x00
        },
        'minimum_pixel': {
            'address': 0x0A,
            'value': (),
            'reset': 0x00
        },
        'shutter_lower': {
            'address': 0x0B,
            'value': (),
            'reset': 0x00
        },
        'shutter_upper': {
            'address': 0x0C,
            'value': (),
            'reset': 0x00
        },
        'chip_observation': {
            'address': 0x15,
            'value': (),
            'reset': 0x00
        },
        'burst_motion_read': {
            'address': 0x16,
            'value': (),
            'reset': 0x00
        },
        'powerup_reset': {
            'address': 0x3A,
            'value': (),
            'reset': ()
        },
        'shutdown': {
            'address': 0x3B,
            'value': (),
            'reset': ()
        },
        'performance': {
            'address': 0x40,
            'value': (),
            'reset': 0x00
        },
        'dpi': {
            'address': 0x4E,
            'value': (),
            'reset': 0x14
        },
        'pixel_grab': {
            'address': 0x58,
            'value': (),
            'reset': 0x0
        },
        'pixel_grab_status': {
            'address': 0x59,
            'value': (),
            'reset': 0x00
        },
        'axis_control': {
            'address': 0x59,
            'value': (),
            'reset': 0xE0
        },
        'inv_product_id': {
            'address': 0x5F,
            'value': 0xB6,
            'reset': 0xB6
        },
        'rest1_period_glass': {
            'address': 0x70,
            'value': (),
            'reset': 0x09
        },
        'rest1_downshift_glass': {
            'address': 0x71,
            'value': (),
            'reset': 0x10
        },
        'run_downshift': {
            'address': 0x77,
            'value': (),
            'reset': 0x03
        },
        'rest1_period_nonglass': {
            'address': 0x78,
            'value': (),
            'reset': 0x09
        },
        'rest1_downshift_nonglass': {
            'address': 0x79,
            'value': (),
            'reset': 0x10
        },
        'rest2_period': {
            'address': 0x7A,
            'value': (),
            'reset': 0x19
        },
        'rest2_downshift': {
            'address': 0x7B,
            'value': (),
            'reset': 0x5E
        },
        'rest3_period': {
            'address': 0x7C,
            'value': (),
            'reset': 0x3F
        },
    },
    # E7792 PLUTO sensor - https://drive.google.com/drive/search?q=E7792
    OpticalSensorName.PLUTO: {
        'product_id': {
            'address': 0x80 | 0x00,
            'value': 0x92,
        },
        'dpi_x': {
            'address': 0x80 | 0x0C,
            'value': 0x1F,
        },
        'dpi_y': {
            'address': 0x80 | 0x0D,
            'value': 0x1F,
        },
    },
    # E7770 Rambo X Magnetic Mouse Wheel Sensor - https://drive.google.com/drive/folders/1jBTVsJFQWjzJgC8kLMN5wNOQCoQUxgec
    'RAMBO_X': {
        'chip_version': {
            'address': 0xFC,
            'value': 0x12,
        }
    }
}


class SPIDirectAccessTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``SPIDirectAccess`` feature
    """
    class GetNbDevicesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetNbDevicesResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "number_of_devices": (
                    cls.check_number_of_devices,
                    test_case.f.PRODUCT.FEATURES.COMMON.SPI_DIRECT_ACCESS.F_NumberOfDevices)
            }
        # end def get_default_check_map

        @staticmethod
        def check_number_of_devices(test_case, response, expected):
            """
            Check number_of_devices field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetNbDevicesResponse to check
            :type response: ``GetNbDevicesResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert number_of_devices that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="NumberOfDevices shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.number_of_devices),
                msg="The number_of_devices parameter differs "
                    f"(expected:{expected}, obtained:{response.number_of_devices})")
        # end def check_number_of_devices
    # end class GetNbDevicesResponseChecker

    class AccessConfigChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``AccessConfig``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.SPI_DIRECT_ACCESS
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "enable_atomic_cs": (
                    cls.check_enable_atomic_cs,
                    config.F_EnableAtomicCs),
                "disable_fw_access": (
                    cls.check_disable_fw_access,
                    config.F_DisableFwAccess)
            }
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, access_config):
            """
            Get the check methods and expected values

            :param access_config: The access configuration
            :type access_config: ``int|SPIDirectAccess.AccessConfig``

            :return: Default check map
            :rtype: ``dict``
            """
            access_config = to_int(HexList(access_config))

            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "enable_atomic_cs": (
                    cls.check_enable_atomic_cs,
                    (access_config & 2) >> 1),
                "disable_fw_access": (
                    cls.check_disable_fw_access,
                    access_config & 1)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: AccessConfig to check
            :type bitmap: ``SPIDirectAccess.AccessConfig``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_enable_atomic_cs(test_case, bitmap, expected):
            """
            Check enable_atomic_cs field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: AccessConfig to check
            :type bitmap: ``SPIDirectAccess.AccessConfig``
            :param expected: Expected value
            :type expected: ``bool|HexList``

            :raise ``AssertionError``: Assert enable_atomic_cs that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.enable_atomic_cs),
                msg="The enable_atomic_cs parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.enable_atomic_cs})")
        # end def check_enable_atomic_cs

        @staticmethod
        def check_disable_fw_access(test_case, bitmap, expected):
            """
            Check disable_fw_access field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: AccessConfig to check
            :type bitmap: ``SPIDirectAccess.AccessConfig``
            :param expected: Expected value
            :type expected: ``bool|HexList``

            :raise ``AssertionError``: Assert disable_fw_access that raise an exception
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.disable_fw_access),
                msg="The disable_fw_access parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.disable_fw_access})")
        # end def check_disable_fw_access
    # end class AccessConfigChecker

    class GetSelectedDeviceResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetSelectedDeviceResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "device_idx": (
                    cls.check_device_idx,
                    0),
                "access_config": (
                    cls.check_access_config,
                    SPIDirectAccessTestUtils.AccessConfigChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_device_idx(test_case, response, expected):
            """
            Check device_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetSelectedDeviceResponse to check
            :type response: ``GetSelectedDeviceResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert device_idx that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.device_idx),
                msg="The device_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.device_idx})")
        # end def check_device_idx

        @staticmethod
        def check_access_config(test_case, message, expected):
            """
            Check ``access_config``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetSelectedDeviceResponse to check
            :type message: ``GetSelectedDeviceResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            SPIDirectAccessTestUtils.AccessConfigChecker.check_fields(
                test_case, message.access_config, SPIDirectAccess.AccessConfig, expected)
        # end def check_access_config
    # end class GetSelectedDeviceResponseChecker

    class SelectDeviceResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SelectDeviceResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "device_idx": (
                    cls.check_device_idx,
                    0),
                "access_config": (
                    cls.check_access_config,
                    SPIDirectAccessTestUtils.AccessConfigChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_device_idx(test_case, response, expected):
            """
            Check device_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SelectDeviceResponse to check
            :type response: ``SelectDeviceResponseV0|SelectDeviceResponseV1``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert device_idx that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.device_idx),
                msg="The device_idx parameter differs "
                    f"(expected:{expected}, obtained:{response.device_idx})")
        # end def check_device_idx

        @staticmethod
        def check_access_config(test_case, message, expected):
            """
            Check ``access_config``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: SelectDeviceResponse to check
            :type message: ``SelectDeviceResponseV0|SelectDeviceResponseV1``
            :param expected: Expected value
            :type expected: ``dict``
            """
            SPIDirectAccessTestUtils.AccessConfigChecker.check_fields(
                test_case, message.access_config, SPIDirectAccess.AccessConfig, expected)
        # end def check_access_config
    # end class SelectDeviceResponseChecker

    class SpiDirectAccessResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SpiDirectAccessResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "n_bytes": (
                    cls.check_n_bytes,
                    0),
                "data_out_1": (
                    cls.check_data_out_1,
                    0),
                "data_out_2": (
                    cls.check_data_out_2,
                    0),
                "data_out_3": (
                    cls.check_data_out_3,
                    0),
                "data_out_4": (
                    cls.check_data_out_4,
                    0),
                "data_out_5": (
                    cls.check_data_out_5,
                    0),
                "data_out_6": (
                    cls.check_data_out_6,
                    0),
                "data_out_7": (
                    cls.check_data_out_7,
                    0),
                "data_out_8": (
                    cls.check_data_out_8,
                    0),
                "data_out_9": (
                    cls.check_data_out_9,
                    0),
                "data_out_10": (
                    cls.check_data_out_10,
                    0),
                "data_out_11": (
                    cls.check_data_out_11,
                    0),
                "data_out_12": (
                    cls.check_data_out_12,
                    0),
                "data_out_13": (
                    cls.check_data_out_13,
                    0),
                "data_out_14": (
                    cls.check_data_out_14,
                    0),
                "data_out_15": (
                    cls.check_data_out_15,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_n_bytes(test_case, response, expected):
            """
            Check n_bytes field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert n_bytes that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.n_bytes),
                msg="The n_bytes parameter differs "
                    f"(expected:{expected}, obtained:{response.n_bytes})")
        # end def check_n_bytes

        @staticmethod
        def check_data_out_1(test_case, response, expected):
            """
            Check data_out_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_1 that raise an exception
            """
            if test_case.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName in [OpticalSensorName.HERO,
                                                                          OpticalSensorName.HERO2,
                                                                          OpticalSensorName.ROBIN,
                                                                          OpticalSensorName.PLUTO]:
                # The first byte is sensor status, the expected register data start from the second byte,
                # so ignore the check.
                return
            # end if

            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_1),
                msg="The data_out_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_1})")
        # end def check_data_out_1

        @staticmethod
        def check_data_out_2(test_case, response, expected):
            """
            Check data_out_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_2 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_2),
                msg="The data_out_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_2})")
        # end def check_data_out_2

        @staticmethod
        def check_data_out_3(test_case, response, expected):
            """
            Check data_out_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_3 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_3),
                msg="The data_out_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_3})")
        # end def check_data_out_3

        @staticmethod
        def check_data_out_4(test_case, response, expected):
            """
            Check data_out_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_4 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_4),
                msg="The data_out_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_4})")
        # end def check_data_out_4

        @staticmethod
        def check_data_out_5(test_case, response, expected):
            """
            Check data_out_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_5 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_5),
                msg="The data_out_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_5})")
        # end def check_data_out_5

        @staticmethod
        def check_data_out_6(test_case, response, expected):
            """
            Check data_out_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_6 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_6),
                msg="The data_out_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_6})")
        # end def check_data_out_6

        @staticmethod
        def check_data_out_7(test_case, response, expected):
            """
            Check data_out_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_7 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_7),
                msg="The data_out_7 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_7})")
        # end def check_data_out_7

        @staticmethod
        def check_data_out_8(test_case, response, expected):
            """
            Check data_out_8 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_8 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_8),
                msg="The data_out_8 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_8})")
        # end def check_data_out_8

        @staticmethod
        def check_data_out_9(test_case, response, expected):
            """
            Check data_out_9 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_9 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_9),
                msg="The data_out_9 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_9})")
        # end def check_data_out_9

        @staticmethod
        def check_data_out_10(test_case, response, expected):
            """
            Check data_out_10 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_10 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_10),
                msg="The data_out_10 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_10})")
        # end def check_data_out_10

        @staticmethod
        def check_data_out_11(test_case, response, expected):
            """
            Check data_out_11 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_11 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_11),
                msg="The data_out_11 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_11})")
        # end def check_data_out_11

        @staticmethod
        def check_data_out_12(test_case, response, expected):
            """
            Check data_out_12 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_12 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_12),
                msg="The data_out_12 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_12})")
        # end def check_data_out_12

        @staticmethod
        def check_data_out_13(test_case, response, expected):
            """
            Check data_out_13 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_13 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_13),
                msg="The data_out_13 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_13})")
        # end def check_data_out_13

        @staticmethod
        def check_data_out_14(test_case, response, expected):
            """
            Check data_out_14 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_14 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_14),
                msg="The data_out_14 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_14})")
        # end def check_data_out_14

        @staticmethod
        def check_data_out_15(test_case, response, expected):
            """
            Check data_out_15 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SpiDirectAccessResponse to check
            :type response: ``SpiDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int|HexList``

            :raise ``AssertionError``: Assert data_out_15 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_15),
                msg="The data_out_15 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_15})")
        # end def check_data_out_15
    # end class SpiDirectAccessResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=SPIDirectAccess.FEATURE_ID, factory=SPIDirectAccessFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)

        # end def get_parameters

        @classmethod
        def get_nb_devices(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetNbDevices``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetNbDevicesResponse
            :rtype: ``GetNbDevicesResponse``
            """
            feature_1e22_index, feature_1e22, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e22.get_nb_devices_cls(
                device_index=device_index,
                feature_index=feature_1e22_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e22.get_nb_devices_response_cls)
            return response

        # end def get_nb_devices

        @classmethod
        def get_selected_device(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetSelectedDevice``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetSelectedDeviceResponse
            :rtype: ``GetSelectedDeviceResponse``
            """
            feature_1e22_index, feature_1e22, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e22.get_selected_device_cls(
                device_index=device_index,
                feature_index=feature_1e22_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e22.get_selected_device_response_cls)
            return response

        # end def get_selected_device

        @classmethod
        def select_device(cls, test_case, device_idx, access_config, device_index=None, port_index=None):
            """
            Process ``SelectDevice``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_idx: Device Idx
            :type device_idx: ``int|HexList``
            :param access_config: Access Config
            :type access_config: ``int|HexList|SPIDirectAccess.AccessConfig``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SelectDeviceResponse
            :rtype: ``SelectDeviceResponseV0|SelectDeviceResponseV1``
            """
            feature_1e22_index, feature_1e22, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e22.select_device_cls(
                device_index=device_index,
                feature_index=feature_1e22_index,
                device_idx=HexList(device_idx),
                access_config=HexList(access_config))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e22.select_device_response_cls)
            return response
        # end def select_device

        @classmethod
        def spi_direct_access(cls, test_case, n_bytes, data_in_1=0, data_in_2=0, data_in_3=0, data_in_4=0, data_in_5=0,
                              data_in_6=0, data_in_7=0, data_in_8=0, data_in_9=0, data_in_10=0, data_in_11=0,
                              data_in_12=0, data_in_13=0, data_in_14=0, data_in_15=0,
                              device_index=None, port_index=None):
            """
            Process ``SpiDirectAccess``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param n_bytes: N Bytes
            :type n_bytes: ``int|HexList``
            :param data_in_1: Data In 1 - OPTIONAL
            :type data_in_1: ``int|HexList``
            :param data_in_2: Data In 2 - OPTIONAL
            :type data_in_2: ``int|HexList``
            :param data_in_3: Data In 3 - OPTIONAL
            :type data_in_3: ``int|HexList``
            :param data_in_4: Data In 4 - OPTIONAL
            :type data_in_4: ``int|HexList``
            :param data_in_5: Data In 5 - OPTIONAL
            :type data_in_5: ``int|HexList``
            :param data_in_6: Data In 6 - OPTIONAL
            :type data_in_6: ``int|HexList``
            :param data_in_7: Data In 7 - OPTIONAL
            :type data_in_7: ``int|HexList``
            :param data_in_8: Data In 8 - OPTIONAL
            :type data_in_8: ``int|HexList``
            :param data_in_9: Data In 9 - OPTIONAL
            :type data_in_9: ``int|HexList``
            :param data_in_10: Data In 10 - OPTIONAL
            :type data_in_10: ``int|HexList``
            :param data_in_11: Data In 11 - OPTIONAL
            :type data_in_11: ``int|HexList``
            :param data_in_12: Data In 12 - OPTIONAL
            :type data_in_12: ``int|HexList``
            :param data_in_13: Data In 13 - OPTIONAL
            :type data_in_13: ``int|HexList``
            :param data_in_14: Data In 14 - OPTIONAL
            :type data_in_14: ``int|HexList``
            :param data_in_15: Data In 15 - OPTIONAL
            :type data_in_15: ``int|HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SpiDirectAccessResponse
            :rtype: ``SpiDirectAccessResponse``
            """
            feature_1e22_index, feature_1e22, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e22.spi_direct_access_cls(
                device_index=device_index,
                feature_index=feature_1e22_index,
                n_bytes=HexList(n_bytes),
                data_in_1=HexList(data_in_1),
                data_in_2=HexList(data_in_2),
                data_in_3=HexList(data_in_3),
                data_in_4=HexList(data_in_4),
                data_in_5=HexList(data_in_5),
                data_in_6=HexList(data_in_6),
                data_in_7=HexList(data_in_7),
                data_in_8=HexList(data_in_8),
                data_in_9=HexList(data_in_9),
                data_in_10=HexList(data_in_10),
                data_in_11=HexList(data_in_11),
                data_in_12=HexList(data_in_12),
                data_in_13=HexList(data_in_13),
                data_in_14=HexList(data_in_14),
                data_in_15=HexList(data_in_15))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e22.spi_direct_access_response_cls)
            return response
        # end def spi_direct_access
    # end class HIDppHelper

    @classmethod
    def send_spi_command(cls, test_case, command, n_bytes=None):
        """
        Send SPI command

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited
        :param command: Raw data to be transferred to the currently selected SPI peripheral
        :type command: ``list[int]``
        :param n_bytes: Number of bytes to be transferred - OPTIONAL
        :type n_bytes: ``int|HexList``

        :return: SpiDirectAccessResponse
        :rtype: ``SpiDirectAccessResponse``

        :raise ``AssertionError``: If the size of the input command is over the maximum size
        """
        assert len(command) <= SPI_DATA_MAX_LEN, "The size of the input command is over the maximum size."
        n_bytes = len(command) if n_bytes is None else n_bytes
        command = command + ([0] * (SPI_DATA_MAX_LEN - len(command)))

        return cls.HIDppHelper.spi_direct_access(test_case=test_case,
                                                 n_bytes=n_bytes,
                                                 data_in_1=command[0],
                                                 data_in_2=command[1],
                                                 data_in_3=command[2],
                                                 data_in_4=command[3],
                                                 data_in_5=command[4],
                                                 data_in_6=command[5],
                                                 data_in_7=command[6],
                                                 data_in_8=command[7],
                                                 data_in_9=command[8],
                                                 data_in_10=command[9],
                                                 data_in_11=command[10],
                                                 data_in_12=command[11],
                                                 data_in_13=command[12],
                                                 data_in_14=command[13],
                                                 data_in_15=command[14])
    # end def send_spi_command

    @classmethod
    def get_dpi(cls, test_case, expected_dpi):
        """
        Get DPI from optical sensor

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited
        :param expected_dpi: The expected DPI value for high speed threshold checking in the case of HERO sensor
        :type expected_dpi: ``int``

        :return: The DPI from sensor
        :rtype: ``dict``
        """
        DeviceTestUtils.HIDppHelper.activate_features(
            test_case, manufacturing=True, device_index=ChannelUtils.get_device_index(test_case=test_case))

        dpi_from_sensor = None
        optical_sensor_name = test_case.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName
        if optical_sensor_name is not None:
            optical_sensor_name = optical_sensor_name.upper()
        # end if

        if optical_sensor_name == OpticalSensorName.HERO:
            dpi_from_sensor = cls._get_dpi_from_hero_sensor(test_case, expected_dpi)
        elif optical_sensor_name == OpticalSensorName.HERO2:
            dpi_from_sensor = cls._get_dpi_from_hero_2_sensor(test_case)
        elif optical_sensor_name == OpticalSensorName.ROBIN:
            dpi_from_sensor = cls._get_dpi_from_robin_sensor(test_case)
        elif optical_sensor_name in [OpticalSensorName.TOG6, OpticalSensorName.TOGX]:
            dpi_from_sensor = cls._get_dpi_from_tog6_sensor(test_case)
        elif optical_sensor_name == OpticalSensorName.TCOB_TRACKBALL:
            dpi_from_sensor = cls._get_dpi_from_tcob_sensor(test_case)
        elif optical_sensor_name == OpticalSensorName.TCOB_NO_TRACKBALL:
            dpi_from_sensor = cls._get_dpi_from_tcob_non_track_ball_sensor(test_case)
        elif optical_sensor_name == OpticalSensorName.PAW3333:
            dpi_from_sensor = cls._get_dpi_from_paw3333_sensor(test_case)
        elif optical_sensor_name == OpticalSensorName.PLUTO:
            dpi_from_sensor = cls._get_dpi_from_pluto_sensor(test_case)
        else:
            warn(f'Unknown optical sensor name: {optical_sensor_name}')
        # end if

        return dpi_from_sensor
    # end def get_dpi

    @classmethod
    def get_product_id(cls, test_case):
        """
        Get Product ID from the optical sensor

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The Product ID from the optical sensor
        :rtype: ``int``
        """
        optical_sensor_name = test_case.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName

        response_product_id = None
        data_in_1 = SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['product_id']['address']

        if optical_sensor_name in [OpticalSensorName.HERO, OpticalSensorName.HERO2,
                                   OpticalSensorName.ROBIN, OpticalSensorName.PLUTO]:
            data_in_2 = NEXT_CMD
            response_product_id = cls.HIDppHelper.spi_direct_access(
                test_case=test_case, n_bytes=2, data_in_1=data_in_1, data_in_2=data_in_2).data_out_2
        elif optical_sensor_name in [OpticalSensorName.TCOB_TRACKBALL, OpticalSensorName.TCOB_NO_TRACKBALL,
                                     OpticalSensorName.TOG6, OpticalSensorName.TOGX]:
            response_product_id = cls.HIDppHelper.spi_direct_access(
                test_case=test_case, n_bytes=1, data_in_1=data_in_1).data_out_1
        elif optical_sensor_name == OpticalSensorName.PAW3333:
            response_product_id = cls.HIDppHelper.spi_direct_access(
                test_case=test_case, n_bytes=2, data_in_1=data_in_1).data_out_2
        else:
            warn(f'Unknown optical sensor name: {optical_sensor_name}')
        # end if

        return to_int(response_product_id)
    # end def get_product_id

    @classmethod
    def _get_dpi_from_hero_sensor(cls, test_case, expected_dpi):
        """
        Get DPI value from HERO sensor

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited
        :param expected_dpi: The expected DPI value
        :type expected_dpi: ``int``

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        # Get DPI on X axis
        response_x = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO]['dpi_x']['address'],
            data_in_2=NEXT_CMD)

        # Get DPI on Y axis
        response_y = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO]['dpi_y']['address'],
            data_in_2=NEXT_CMD)

        # Calculate DPI
        step = 50
        if expected_dpi > HERO_SENSOR_HIGH_SPEED_THRESHOLD:
            step = 100
        # end if
        step_count_x = to_int(response_x.data_out_2) + 1
        step_count_y = to_int(response_y.data_out_2) + 1
        return {'x': step_count_x * step, 'y': step_count_y * step}
    # end def _get_dpi_from_hero_sensor

    @classmethod
    def _get_dpi_from_hero_2_sensor(cls, test_case):
        """
        Get DPI value from HERO 2 sensor

        ref: https://docs.google.com/a/logitech.com/viewer?a=v&pid=sites&srcid=bG9naXRlY2guY29tfDJkLW9wdGljYWwtdGVhbS1tYW5hZ2VtZW50fGd4OjNkMjEzMmVlNjI4NmQzMjc

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        # Get DPI on X axis
        response_x = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO2]['dpi_x']['address'],
            data_in_2=NEXT_CMD)

        # Get DPI on Y axis
        response_y = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO2]['dpi_y']['address'],
            data_in_2=NEXT_CMD)

        # Get step
        response_step = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO2]['dpi_step']['address'],
            data_in_2=NEXT_CMD)

        dpi_x = (to_int(response_step.data_out_2) + 1) * (to_int(response_x.data_out_2) + 1)
        dpi_y = (to_int(response_step.data_out_2) + 1) * (to_int(response_y.data_out_2) + 1)
        # Reverse the dpi x and y because FW would like to keep X in horizontal
        return {'x': dpi_y, 'y': dpi_x}
    # end def _get_dpi_from_hero_2_sensor

    @classmethod
    def _get_dpi_from_robin_sensor(cls, test_case):
        """
        Get DPI value from ROBIN sensor

        ref: https://sites.google.com/a/logitech.com/2d-optical-team-management/sensor-specifications-guidelines/ic/em/e7792-pluto

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        # Get DPI on X axis
        response_x = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.ROBIN]['dpi_x']['address'],
            data_in_2=NEXT_CMD)

        # Get DPI on Y axis
        response_y = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.ROBIN]['dpi_y']['address'],
            data_in_2=NEXT_CMD)

        # Calculate DPI
        step_count_x = to_int(response_x.data_out_2) + 1
        step_count_y = to_int(response_y.data_out_2) + 1
        return {'x': step_count_x * 50, 'y': step_count_y * 50}
    # end def _get_dpi_from_robin_sensor

    @classmethod
    def _get_dpi_from_tcob_non_track_ball_sensor(cls, test_case):
        """
        Get DPI Value from TCOB Sensor without Trackball.

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        return cls._get_dpi_from_tcob_sensor(test_case=test_case, track_ball=False)
    # end def _get_dpi_from_tcob_non_track_ball_sensor

    @classmethod
    def _get_dpi_from_tcob_sensor(cls, test_case, track_ball=True):
        """
        Get DPI value from TCOB sensor

        ref: PAW3266+One lens FW Guideline Rev0.2
             https://docs.google.com/document/d/1iMEnCUKopFCDcJGsCgPQpLbHh5RerMQknx03bAOC11E/edit?usp=sharing

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited
        :param track_ball: Flag indicating if the sensor is a Trackball or Trackball-less model - OPTIONAL
        :type track_ball: ``bool``

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        optical_sensor_name = OpticalSensorName.TCOB_TRACKBALL if track_ball else OpticalSensorName.TCOB_NO_TRACKBALL
        # Get DPI on X axis
        response_x = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=1,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['dpi_x_lo']['address'])

        # Get DPI on Y axis
        response_y = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=1,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['dpi_y_lo']['address'])

        # Get high byte
        response_high_byte = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=1,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[optical_sensor_name]['dpi_x_y_hi']['address'])
        x_high_byte = to_int(response_high_byte.data_out_1) & 0xF
        y_high_byte = (to_int(response_high_byte.data_out_1) & 0xF0) >> 4

        ball_surface_ratio = 1.026 if track_ball else 1
        ball_xy_ratio = 1.078 if track_ball else 1.067
        dpi_factor = 2.48

        # Calculate DPI
        x_dpi_from_sensor = to_int(response_x.data_out_1) + (x_high_byte << 8)
        y_dpi_from_sensor = to_int(response_y.data_out_1) + (y_high_byte << 8)
        x_dpi = round(x_dpi_from_sensor * dpi_factor / ball_surface_ratio)
        y_dpi = round(y_dpi_from_sensor * dpi_factor / ball_xy_ratio / ball_surface_ratio)
        return {'x': x_dpi, 'y': y_dpi}
    # end def _get_dpi_from_tcob_sensor

    @classmethod
    def _get_dpi_from_tog6_sensor(cls, test_case):
        """
        Get DPI value from TOG6 / TOGX sensor

        ref: https://drive.google.com/file/d/1h5XE6GDz5tPRlmoJtqKbBzUYftsouIyo/view?usp=sharing

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        # Get DPI on X and Y axis
        response = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=1,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.TOG6]['dpi']['address'])

        step_count = to_int(response.data_out_1) + 1
        dpi_from_sensor = step_count * 50
        return {'x': dpi_from_sensor, 'y': dpi_from_sensor}
    # end def _get_dpi_from_tog6_sensor

    @classmethod
    def _get_dpi_from_pluto_sensor(cls, test_case):
        """
        Get DPI value from Pluto One sensor

        ref:
        https://docs.google.com/a/logitech.com/viewer?a=v&pid=sites&srcid=bG9naXRlY2guY29tfDJkLW9wdGljYWwtdGVhbS1tYW5hZ2VtZW50fGd4Ojc5MThkYzMwZjQxODZmMTY
        from
        https://sites.google.com/a/logitech.com/2d-optical-team-management/sensor-specifications-guidelines/ic/em/e7792-pluto

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict[str, int]``
        """
        # Get DPI on X axis
        response_x = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.PLUTO]['dpi_x']['address'],
            data_in_2=NEXT_CMD)

        # Get DPI on Y axis
        response_y = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.PLUTO]['dpi_y']['address'],
            data_in_2=NEXT_CMD)

        # Calculate DPI
        x_dpi_from_sensor = to_int(response_x.data_out_2)
        y_dpi_from_sensor = to_int(response_y.data_out_2)
        x_dpi = 400 + x_dpi_from_sensor * 100
        y_dpi = 400 + y_dpi_from_sensor * 100
        return {'x': x_dpi, 'y': y_dpi}
    # end def _get_dpi_from_pluto_sensor

    @classmethod
    def _get_dpi_from_paw3333_sensor(cls, test_case):
        """
        Get DPI value from PAW3333 sensor

        ref: https://docs.google.com/document/d/1LGNveZ8kc9_AL2PjOgZZoK100SF6n5d5MkVdYjCdbeM/edit?usp=sharing
             https://docs.google.com/spreadsheets/d/1oNXo5g2QeVR-BoyPe_ovETSdRiu4G4-3/edit?usp=sharing&ouid=103895408122325971643&rtpof=true&sd=true

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        # Get DPI
        response = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=1,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.PAW3333]['dpi']['address'])

        # Calculate DPI
        dpi = PAW3333_DPI_TABLE[to_int(response.data_out_2)]
        return {'x': dpi, 'y': dpi}
    # end def _get_dpi_from_paw3333_sensor

    @classmethod
    def _get_dpi_calibration_correction(cls, test_case):
        """
        Get DPI calibration correction from HERO 2 sensor

        ref: https://docs.google.com/a/logitech.com/viewer?a=v&pid=sites&srcid=bG9naXRlY2guY29tfDJkLW9wdGljYWwtdGVhbS1tYW5hZ2VtZW50fGd4OjNkMjEzMmVlNjI4NmQzMjc

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.DeviceBaseTestCase`` or inherited

        :return: The DPI values at x and y axis
        :rtype: ``dict``
        """
        # FIXME: Shall request DPI first, otherwise cannot get response from DUT
        cls.get_dpi(test_case=test_case, expected_dpi=1000)

        # Get ResCor_h
        res_cor_h = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO2]['res_cor_h']['address'],
            data_in_2=NEXT_CMD)

        # Get DPI on Y axis
        res_cor_l = cls.HIDppHelper.spi_direct_access(
            test_case=test_case, n_bytes=2,
            data_in_1=SPI_PERIPHERAL_REGISTER_DICT[OpticalSensorName.HERO2]['res_cor_l']['address'],
            data_in_2=NEXT_CMD)

        # Combine high and low byte with sign bit
        res_cor = int.from_bytes([to_int(res_cor_h.data_out_2), to_int(res_cor_l.data_out_2)],
                                 'big', signed=True)
        return res_cor
    # end def _get_dpi_calibration_correction
# end class SPIDirectAccessTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
