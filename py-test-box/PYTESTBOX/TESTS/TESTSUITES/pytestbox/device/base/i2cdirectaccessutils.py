#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.i2cdirectaccessutils
:brief: Helpers for ``I2CDirectAccess`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2022/12/06
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.i2cdirectaccess import GetNbDevicesResponse
from pyhid.hidpp.features.common.i2cdirectaccess import GetSelectedDeviceResponse
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccess
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccessFactory
from pyhid.hidpp.features.common.i2cdirectaccess import I2CReadDirectAccessResponse
from pyhid.hidpp.features.common.i2cdirectaccess import I2CWriteDirectAccessResponse
from pyhid.hidpp.features.common.i2cdirectaccess import SelectDeviceResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class I2CPeripherals:
    """
    Define name of the I2C peripherals
    """
    YOKO_TP = "YOKO_TP"
# end class I2CPeripherals


I2C_PERIPHERAL_REGISTER_DICT = {
    # PCT3848QC Yoko touch module - https://drive.google.com/file/d/1nvnVfMAdGCDs-TiU3PGBkQ233DFV18ZD/view
    I2CPeripherals.YOKO_TP: {
        'product_id': {
            'bank_id': 0x00,
            'address': 0x00,
            'value': 0x8D,
            'read_only': True,
        },
        'width_lsb': {
            'bank_id': 0x02,
            'address': 0x00,
            'value': 0x80,
            'read_only': False,
        },
        'width_msb': {
            'bank_id': 0x02,
            'address': 0x01,
            'value': 0x08,
            'read_only': False,
        },
        'height_lsb': {
            'bank_id': 0x02,
            'address': 0x02,
            'value': 0xAB,
            'read_only': False,
        },
        'height_msb': {
            'bank_id': 0x02,
            'address': 0x03,
            'value': 0x04,
            'read_only': False,
        },
        'scan_report_rate_lsb': {
            'bank_id': 0x00,
            'address': 0x12,
            'value': 0x91,
            'read_only': False,
        },
        'scan_report_rate_msb': {
            'bank_id': 0x00,
            'address': 0x13,
            'value': 0x00,
            'read_only': False,
        },
    }
}


class I2CDirectAccessTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``I2CDirectAccess`` feature
    """
    I2C_WRITE_DATA_MAX_LEN = 14

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
                    test_case.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS.F_NumberOfDevices)
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
            :type expected: ``int | HexList``

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
            config = test_case.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS

            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "disable_fw_access": (
                    cls.check_disable_fw_access,
                    config.F_DisableFwAccess)
            }
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, access_config):
            """
            Get the check methods and expected values

            :param access_config: Options linked to I2C peripheral access
            :type access_config: ``int|I2CDirectAccess.AccessConfig``

            :return: Default check map
            :rtype: ``dict``
            """
            access_config = to_int(HexList(access_config))

            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "disable_fw_access": (
                    cls.check_disable_fw_access,
                    access_config & I2CDirectAccess.AccessConfig.FwAccess.MASK)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: AccessConfig to check
            :type bitmap: ``I2CDirectAccess.AccessConfig``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_disable_fw_access(test_case, bitmap, expected):
            """
            Check disable_fw_access field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: AccessConfig to check
            :type bitmap: ``I2CDirectAccess.AccessConfig``
            :param expected: Expected value
            :type expected: ``bool | HexList``

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
                    I2CDirectAccessTestUtils.AccessConfigChecker.get_default_check_map(test_case))
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
            :type expected: ``int | HexList``

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
            I2CDirectAccessTestUtils.AccessConfigChecker.check_fields(
                test_case, message.access_config, I2CDirectAccess.AccessConfig, expected)
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
                    I2CDirectAccessTestUtils.AccessConfigChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_device_idx(test_case, response, expected):
            """
            Check device_idx field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: SelectDeviceResponse to check
            :type response: ``SelectDeviceResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :type message: ``SelectDeviceResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            I2CDirectAccessTestUtils.AccessConfigChecker.check_fields(
                test_case, message.access_config, I2CDirectAccess.AccessConfig, expected)
        # end def check_access_config
    # end class SelectDeviceResponseChecker

    class I2CReadDirectAccessResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``I2CReadDirectAccessResponse``
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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert data_out_1 that raise an exception
            """
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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

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
            :param response: I2CReadDirectAccessResponse to check
            :type response: ``I2CReadDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert data_out_15 that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_out_15),
                msg="The data_out_15 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_out_15})")
        # end def check_data_out_15
    # end class I2CReadDirectAccessResponseChecker

    class I2CWriteDirectAccessResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``I2CWriteDirectAccessResponse``
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
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_n_bytes(test_case, response, expected):
            """
            Check n_bytes field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: I2CWriteDirectAccessResponse to check
            :type response: ``I2CWriteDirectAccessResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert n_bytes that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.n_bytes),
                msg="The n_bytes parameter differs "
                    f"(expected:{expected}, obtained:{response.n_bytes})")
        # end def check_n_bytes
    # end class I2CWriteDirectAccessResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=I2CDirectAccess.FEATURE_ID, factory=I2CDirectAccessFactory,
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
            feature_1e30_index, feature_1e30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e30.get_nb_devices_cls(
                device_index=device_index,
                feature_index=feature_1e30_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e30.get_nb_devices_response_cls)
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
            feature_1e30_index, feature_1e30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e30.get_selected_device_cls(
                device_index=device_index,
                feature_index=feature_1e30_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e30.get_selected_device_response_cls)
            return response
        # end def get_selected_device

        @classmethod
        def select_device(cls, test_case, device_idx, access_config, device_index=None, port_index=None):
            """
            Process ``SelectDevice``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_idx: Device Idx
            :type device_idx: ``int | HexList``
            :param access_config: Access Config
            :type access_config: ``int | HexList | I2CDirectAccess.AccessConfig``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SelectDeviceResponse
            :rtype: ``SelectDeviceResponse``
            """
            feature_1e30_index, feature_1e30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e30.select_device_cls(
                device_index=device_index,
                feature_index=feature_1e30_index,
                device_idx=HexList(device_idx),
                access_config=HexList(access_config))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e30.select_device_response_cls)
            return response
        # end def select_device

        @classmethod
        def i2c_read_direct_access(cls, test_case, n_bytes, register_address, device_index=None, port_index=None):
            """
            Process ``I2CReadDirectAccess``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param n_bytes: N Bytes
            :type n_bytes: ``int | HexList``
            :param register_address: Register Address
            :type register_address: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: I2CReadDirectAccessResponse
            :rtype: ``I2CReadDirectAccessResponse``
            """
            feature_1e30_index, feature_1e30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e30.i2c_read_direct_access_cls(
                device_index=device_index,
                feature_index=feature_1e30_index,
                n_bytes=HexList(n_bytes),
                register_address=HexList(register_address))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e30.i2c_read_direct_access_response_cls)
            return response
        # end def i2c_read_direct_access

        @classmethod
        def i2c_write_direct_access(cls, test_case, n_bytes, register_address,
                                    data_in_1=0, data_in_2=0, data_in_3=0,
                                    data_in_4=0, data_in_5=0, data_in_6=0, data_in_7=0,
                                    data_in_8=0, data_in_9=0, data_in_10=0,
                                    data_in_11=0, data_in_12=0, data_in_13=0, data_in_14=0,
                                    device_index=None, port_index=None):
            """
            Process ``I2CWriteDirectAccess``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param n_bytes: N Bytes
            :type n_bytes: ``int | HexList``
            :param register_address: Register Address
            :type register_address: ``int | HexList``
            :param data_in_1: Data In 1 - OPTIONAL
            :type data_in_1: ``int | HexList``
            :param data_in_2: Data In 2 - OPTIONAL
            :type data_in_2: ``int | HexList``
            :param data_in_3: Data In 3 - OPTIONAL
            :type data_in_3: ``int | HexList``
            :param data_in_4: Data In 4 - OPTIONAL
            :type data_in_4: ``int | HexList``
            :param data_in_5: Data In 5 - OPTIONAL
            :type data_in_5: ``int | HexList``
            :param data_in_6: Data In 6 - OPTIONAL
            :type data_in_6: ``int | HexList``
            :param data_in_7: Data In 7 - OPTIONAL
            :type data_in_7: ``int | HexList``
            :param data_in_8: Data In 8 - OPTIONAL
            :type data_in_8: ``int | HexList``
            :param data_in_9: Data In 9 - OPTIONAL
            :type data_in_9: ``int | HexList``
            :param data_in_10: Data In 10 - OPTIONAL
            :type data_in_10: ``int | HexList``
            :param data_in_11: Data In 11 - OPTIONAL
            :type data_in_11: ``int | HexList``
            :param data_in_12: Data In 12 - OPTIONAL
            :type data_in_12: ``int | HexList``
            :param data_in_13: Data In 13 - OPTIONAL
            :type data_in_13: ``int | HexList``
            :param data_in_14: Data In 14 - OPTIONAL
            :type data_in_14: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: I2CWriteDirectAccessResponse
            :rtype: ``I2CWriteDirectAccessResponse``
            """
            feature_1e30_index, feature_1e30, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1e30.i2c_write_direct_access_cls(
                device_index=device_index,
                feature_index=feature_1e30_index,
                n_bytes=HexList(n_bytes),
                register_address=HexList(register_address),
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
                data_in_14=HexList(data_in_14))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1e30.i2c_write_direct_access_response_cls)
            return response
        # end def i2c_write_direct_access
    # end class HIDppHelper

    @staticmethod
    def get_writeable_register_name(test_case, device_index=None):
        """
        Get the name of the first writable register exposed by the selected I2C peripheral

        :param test_case: Currect test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the I2C peripheral - OPTIONAL
        :type device_index: ``int``

        :return: Register name
        :rtype: ``str|None``

        :raise ``ValueError``: if the selected i2c peripheral is unknown
        """
        device_index = 0 if device_index is None else device_index

        i2c_peripheral_name = test_case.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS.F_I2cPeripherals[device_index]
        if i2c_peripheral_name not in I2C_PERIPHERAL_REGISTER_DICT.keys():
            raise ValueError(f'Unknown i2c peripheral name: {i2c_peripheral_name}')
        # end if

        for register_name in I2C_PERIPHERAL_REGISTER_DICT[i2c_peripheral_name].keys():
            if not I2C_PERIPHERAL_REGISTER_DICT[i2c_peripheral_name][register_name]['read_only']:
                return register_name
            # end if
        # end for

        return None
    # end def get_writeable_register_name

    @staticmethod
    def i2c_write_register(test_case, device_index, register_name, data):
        """
        Write value to the specified register of the selected I2C peripheral

        :param test_case: Currect test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the I2C peripheral
        :type device_index: ``int``
        :param register_name: Register name
        :type register_name: ``str``
        :param data: The data to be written in the register
        :type data: ``int|list[int]``

        :return: I2CWriteDirectAccessResponse
        :rtype: ``I2CWriteDirectAccessResponse``
        """
        device_index = 0 if device_index is None else device_index

        if device_index != 0:
            I2CDirectAccessTestUtils.HIDppHelper.select_device(
                test_case=test_case,
                device_idx=device_index,
                access_config=I2CDirectAccess.AccessConfig())
        # end if

        i2c_peripheral_name = test_case.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS.F_I2cPeripherals[device_index]
        if i2c_peripheral_name == I2CPeripherals.YOKO_TP:
            response = I2CDirectAccessTestUtils.PT38348QC.write_data_to_register(
                test_case=test_case,
                bank_id=I2C_PERIPHERAL_REGISTER_DICT[I2CPeripherals.YOKO_TP][register_name]['bank_id'],
                register_address=I2C_PERIPHERAL_REGISTER_DICT[I2CPeripherals.YOKO_TP][register_name]['address'],
                data=data if isinstance(data, list) else [data])
        else:
            raise ValueError(f'Unknown i2c peripheral name: {i2c_peripheral_name}')
        # end if

        return response
    # end def i2c_write_register

    @staticmethod
    def i2c_read_register(test_case, device_index, n_bytes, register_name):
        """
        Read value from the specified register of the selected I2C peripheral

        :param test_case: Currect test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the I2C peripheral
        :type device_index: ``int``
        :param n_bytes: Number of bytes to be read
        :type n_bytes: ``int``
        :param register_name: Register name
        :type register_name: ``str``

        :return: I2CReadDirectAccessResponse
        :rtype: ``I2CReadDirectAccessResponse``
        """
        device_index = 0 if device_index is None else device_index

        if device_index != 0:
            I2CDirectAccessTestUtils.HIDppHelper.select_device(
                test_case=test_case,
                device_idx=device_index,
                access_config=I2CDirectAccess.AccessConfig())
        # end if

        i2c_peripheral_name = test_case.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS.F_I2cPeripherals[device_index]
        if i2c_peripheral_name == I2CPeripherals.YOKO_TP:
            response = I2CDirectAccessTestUtils.PT38348QC.read_data_from_register(
                test_case=test_case,
                n_bytes=n_bytes,
                bank_id=I2C_PERIPHERAL_REGISTER_DICT[I2CPeripherals.YOKO_TP][register_name]['bank_id'],
                register_address=I2C_PERIPHERAL_REGISTER_DICT[I2CPeripherals.YOKO_TP][register_name]['address'])
        else:
            raise ValueError(f'Unknown i2c peripheral name: {i2c_peripheral_name}')
        # end if

        return response
    # end def i2c_read_register

    @staticmethod
    def i2c_read_product_id(test_case, device_index, n_bytes):
        """
        Read product id form the selected I2C peripheral

        :param test_case: Currect test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param device_index: Index of the I2C peripheral
        :type device_index: ``int``
        :param n_bytes: Number of bytes to be read
        :type n_bytes: ``int``

        :return: I2CReadDirectAccessResponse
        :rtype: ``I2CReadDirectAccessResponse``
        """
        device_index = 0 if device_index is None else device_index

        if device_index != 0:
            I2CDirectAccessTestUtils.HIDppHelper.select_device(
                test_case=test_case,
                device_idx=device_index,
                access_config=I2CDirectAccess.AccessConfig())
        # end if

        i2c_peripheral_name = test_case.f.PRODUCT.FEATURES.COMMON.I2C_DIRECT_ACCESS.F_I2cPeripherals[device_index]
        if i2c_peripheral_name == I2CPeripherals.YOKO_TP:
            response = I2CDirectAccessTestUtils.PT38348QC.read_data_from_register(
                test_case=test_case,
                n_bytes=n_bytes,
                bank_id=I2C_PERIPHERAL_REGISTER_DICT[I2CPeripherals.YOKO_TP]['product_id']['bank_id'],
                register_address=I2C_PERIPHERAL_REGISTER_DICT[I2CPeripherals.YOKO_TP]['product_id']['address'])
        else:
            raise ValueError(f'Unknown i2c peripheral name: {i2c_peripheral_name}')
        # end if

        return response
    # end def i2c_read_product_id

    class PT38348QC:
        """
        Interface for Poco Touch PCT3848QC of PixArt
        """
        class ControlRegisters:
            CTRL_BANK = 0x73
            CTRL_ADDRESS = 0x74
            CTRL_DATA = 0x75
        # end class Control Registers

        @classmethod
        def control_bank(cls, test_case, bank_id):
            """
            Control the target bank to write/read data from I2C peripherals

            :param test_case: Currect test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bank_id: The index of bank
            :type bank_id: ``int``

            :return: I2CWriteDirectAccessResponse
            :rtype: ``I2CWriteDirectAccessResponse``
            """
            return I2CDirectAccessTestUtils.HIDppHelper.i2c_write_direct_access(
                test_case=test_case, n_bytes=1, register_address=cls.ControlRegisters.CTRL_BANK, data_in_1=bank_id)
        # end def control_bank

        @classmethod
        def control_address(cls, test_case, register_address):
            """
            Control the address of register to write/read data from I2C peripherals

            :param test_case: Currect test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param register_address: The address of register
            :type register_address: ``int``

            :return: I2CWriteDirectAccessResponse
            :rtype: ``I2CWriteDirectAccessResponse``
            """
            return I2CDirectAccessTestUtils.HIDppHelper.i2c_write_direct_access(
                test_case=test_case,
                n_bytes=1,
                register_address=cls.ControlRegisters.CTRL_ADDRESS,
                data_in_1=register_address)
        # end def control_address

        @classmethod
        def write_data(cls, test_case, data):
            """
            Write data to I2C peripherals

            :param test_case: Currect test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param data: The data to write to a register
            :type data: ``list[int]``

            :return: I2CWriteDirectAccessResponse
            :rtype: ``I2CWriteDirectAccessResponse``
            """
            assert len(data) <= I2CDirectAccessTestUtils.I2C_WRITE_DATA_MAX_LEN,\
                f"The size of the input {data} is over the maximum size."

            data_length = len(data)
            data = data + ([0] * (I2CDirectAccessTestUtils.I2C_WRITE_DATA_MAX_LEN - len(data)))

            return I2CDirectAccessTestUtils.HIDppHelper.i2c_write_direct_access(
                test_case=test_case,
                n_bytes=data_length,
                register_address=cls.ControlRegisters.CTRL_DATA,
                data_in_1=data[0],
                data_in_2=data[1],
                data_in_3=data[2],
                data_in_4=data[3],
                data_in_5=data[4],
                data_in_6=data[5],
                data_in_7=data[6],
                data_in_8=data[7],
                data_in_9=data[8],
                data_in_10=data[9],
                data_in_11=data[10],
                data_in_12=data[11],
                data_in_13=data[12],
                data_in_14=data[13])
        # end write_data

        @classmethod
        def read_data(cls, test_case, n_bytes):
            """
            Read data from I2C peripherals

            :param test_case: Currect test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param n_bytes: Number of bytes to be read
            :type n_bytes: ``int``

            :return: I2CReadDirectAccessResponse
            :rtype: ``I2CReadDirectAccessResponse``
            """
            return I2CDirectAccessTestUtils.HIDppHelper.i2c_read_direct_access(
                test_case=test_case, n_bytes=n_bytes, register_address=cls.ControlRegisters.CTRL_DATA)
        # end def read_data

        @classmethod
        def write_data_to_register(cls, test_case, bank_id, register_address, data):
            """
            Write data to the specified register

            :param test_case: Currect test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bank_id: The index of bank
            :type bank_id: ``int``
            :param register_address: The address of register
            :type register_address: ``int``
            :param data: The data to be written in the register
            :type data: ``list[int]``

            :return: I2CWriteDirectAccessResponse
            :rtype: ``I2CWriteDirectAccessResponse``
            """
            cls.control_bank(test_case=test_case, bank_id=bank_id)
            cls.control_address(test_case=test_case, register_address=register_address)

            return cls.write_data(test_case=test_case, data=data)
        # end def write_data_to_register

        @classmethod
        def read_data_from_register(cls, test_case, n_bytes, bank_id, register_address):
            """
            Read data from the specified register

            :param test_case: Currect test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param n_bytes: Number of bytes to be read
            :type n_bytes: ``int``
            :param bank_id: The index of bank
            :type bank_id: ``int``
            :param register_address: The address of register
            :type register_address: ``int``

            :return: I2CReadDirectAccessResponse
            :rtype: ``I2CReadDirectAccessResponse``
            """
            cls.control_bank(test_case=test_case, bank_id=bank_id)
            cls.control_address(test_case=test_case, register_address=register_address)

            return cls.read_data(test_case=test_case, n_bytes=n_bytes)
        # end def read_data_from_register
    # end class PT38348QC
# end class I2CDirectAccessTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
