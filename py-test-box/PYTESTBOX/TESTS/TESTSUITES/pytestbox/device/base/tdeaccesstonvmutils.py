#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.tdeaccesstonvmutils
:brief: Helpers for ``TdeAccessToNvm`` feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/07/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import sys

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvm
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvmFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TdeAccessToNvmTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``TdeAccessToNvm`` feature
    """

    class GetTdeMemLengthResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetTdeMemLengthResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.TDE_ACCESS_TO_NVM
            return {
                "memory_length": (cls.check_memory_length, config.F_TdeMaxSize)
            }
        # end def get_default_check_map

        @staticmethod
        def check_memory_length(test_case, response, expected):
            """
            Check memory_length field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetTdeMemLengthResponse to check
            :type response: ``GetTdeMemLengthResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="MemoryLength shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.memory_length),
                msg=f"The memory_length parameter differs "
                    f"(expected:{expected}, obtained:{response.memory_length})")
        # end def check_memory_length
    # end class GetTdeMemLengthResponseChecker

    class TdeReadDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``TdeReadDataResponse``
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
                "starting_position": (cls.check_starting_position, 0),
                "number_of_bytes_to_read_or_write": (cls.check_number_of_bytes_to_read_or_write, 0),
                "data_byte_0": (cls.check_data_byte_0, 0),
                "data_byte_1": (cls.check_data_byte_1, 0),
                "data_byte_2": (cls.check_data_byte_2, 0),
                "data_byte_3": (cls.check_data_byte_3, 0),
                "data_byte_4": (cls.check_data_byte_4, 0),
                "data_byte_5": (cls.check_data_byte_5, 0),
                "data_byte_6": (cls.check_data_byte_6, 0),
                "data_byte_7": (cls.check_data_byte_7, 0),
                "data_byte_8": (cls.check_data_byte_8, 0),
                "data_byte_9": (cls.check_data_byte_9, 0),
                "data_byte_10": (cls.check_data_byte_10, 0),
                "data_byte_11": (cls.check_data_byte_11, 0),
                "data_byte_12": (cls.check_data_byte_12, 0),
                "data_byte_13": (cls.check_data_byte_13, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_starting_position(test_case, response, expected):
            """
            Check starting_position field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="StartingPosition shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.starting_position),
                msg=f"The starting_position parameter differs "
                    f"(expected:{expected}, obtained:{response.starting_position})")
        # end def check_starting_position

        @staticmethod
        def check_number_of_bytes_to_read_or_write(test_case, response, expected):
            """
            Check number_of_bytes_to_read_or_write field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected,
                msg="NumberOfBytesToReadOrWrite shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.number_of_bytes_to_read_or_write),
                msg=f"The number_of_bytes_to_read_or_write parameter differs "
                    f"(expected:{expected}, obtained:{response.number_of_bytes_to_read_or_write})")
        # end def check_number_of_bytes_to_read_or_write

        @staticmethod
        def check_data_byte_0(test_case, response, expected):
            """
            Check data_byte_0 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte0 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_0),
                msg=f"The data_byte_0 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_0})")
        # end def check_data_byte_0

        @staticmethod
        def check_data_byte_1(test_case, response, expected):
            """
            Check data_byte_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte1 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_1),
                msg=f"The data_byte_1 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_1})")
        # end def check_data_byte_1

        @staticmethod
        def check_data_byte_2(test_case, response, expected):
            """
            Check data_byte_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte2 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_2),
                msg=f"The data_byte_2 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_2})")
        # end def check_data_byte_2

        @staticmethod
        def check_data_byte_3(test_case, response, expected):
            """
            Check data_byte_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte3 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_3),
                msg=f"The data_byte_3 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_3})")
        # end def check_data_byte_3

        @staticmethod
        def check_data_byte_4(test_case, response, expected):
            """
            Check data_byte_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte4 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_4),
                msg=f"The data_byte_4 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_4})")
        # end def check_data_byte_4

        @staticmethod
        def check_data_byte_5(test_case, response, expected):
            """
            Check data_byte_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte5 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_5),
                msg=f"The data_byte_5 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_5})")
        # end def check_data_byte_5

        @staticmethod
        def check_data_byte_6(test_case, response, expected):
            """
            Check data_byte_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte6 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_6),
                msg=f"The data_byte_6 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_6})")
        # end def check_data_byte_6

        @staticmethod
        def check_data_byte_7(test_case, response, expected):
            """
            Check data_byte_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte7 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_7),
                msg=f"The data_byte_7 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_7})")
        # end def check_data_byte_7

        @staticmethod
        def check_data_byte_8(test_case, response, expected):
            """
            Check data_byte_8 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte8 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_8),
                msg=f"The data_byte_8 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_8})")
        # end def check_data_byte_8

        @staticmethod
        def check_data_byte_9(test_case, response, expected):
            """
            Check data_byte_9 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte9 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_9),
                msg=f"The data_byte_9 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_9})")
        # end def check_data_byte_9

        @staticmethod
        def check_data_byte_10(test_case, response, expected):
            """
            Check data_byte_10 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte10 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_10),
                msg=f"The data_byte_10 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_10})")
        # end def check_data_byte_10

        @staticmethod
        def check_data_byte_11(test_case, response, expected):
            """
            Check data_byte_11 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte11 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_11),
                msg=f"The data_byte_11 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_11})")
        # end def check_data_byte_11

        @staticmethod
        def check_data_byte_12(test_case, response, expected):
            """
            Check data_byte_12 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte12 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_12),
                msg=f"The data_byte_12 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_12})")
        # end def check_data_byte_12

        @staticmethod
        def check_data_byte_13(test_case, response, expected):
            """
            Check data_byte_13 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: TdeReadDataResponse to check
            :type response: ``TdeReadDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="DataByte13 shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.data_byte_13),
                msg=f"The data_byte_13 parameter differs "
                    f"(expected:{expected}, obtained:{response.data_byte_13})")
        # end def check_data_byte_13
    # end class TdeReadDataResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=TdeAccessToNvm.FEATURE_ID, factory=TdeAccessToNvmFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_tde_mem_length(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetTdeMemLength``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetTdeMemLengthResponse
            :rtype: ``GetTdeMemLengthResponse``
            """
            feature_1eb0_index, feature_1eb0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1eb0.get_tde_mem_length_cls(
                device_index=device_index,
                feature_index=feature_1eb0_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1eb0.get_tde_mem_length_response_cls)
            return response
        # end def get_tde_mem_length

        @classmethod
        def tde_write_data(cls, test_case, starting_position, number_of_bytes_to_read_or_write, data_byte_0=0,
                           data_byte_1=0, data_byte_2=0, data_byte_3=0, data_byte_4=0, data_byte_5=0, data_byte_6=0,
                           data_byte_7=0, data_byte_8=0, data_byte_9=0, data_byte_10=0, data_byte_11=0, data_byte_12=0,
                           data_byte_13=0, device_index=None, port_index=None):
            """
            Process ``TdeWriteData``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param starting_position: Starting Position
            :type starting_position: ``int`` or ``HexList``
            :param number_of_bytes_to_read_or_write: Number Of Bytes To Read Or Write
            :type number_of_bytes_to_read_or_write: ``int`` or ``HexList``
            :param data_byte_0: Data Byte 0
            :type data_byte_0: ``int`` or ``HexList``
            :param data_byte_1: Data Byte 1
            :type data_byte_1: ``int`` or ``HexList``
            :param data_byte_2: Data Byte 2
            :type data_byte_2: ``int`` or ``HexList``
            :param data_byte_3: Data Byte 3
            :type data_byte_3: ``int`` or ``HexList``
            :param data_byte_4: Data Byte 4
            :type data_byte_4: ``int`` or ``HexList``
            :param data_byte_5: Data Byte 5
            :type data_byte_5: ``int`` or ``HexList``
            :param data_byte_6: Data Byte 6
            :type data_byte_6: ``int`` or ``HexList``
            :param data_byte_7: Data Byte 7
            :type data_byte_7: ``int`` or ``HexList``
            :param data_byte_8: Data Byte 8
            :type data_byte_8: ``int`` or ``HexList``
            :param data_byte_9: Data Byte 9
            :type data_byte_9: ``int`` or ``HexList``
            :param data_byte_10: Data Byte 10
            :type data_byte_10: ``int`` or ``HexList``
            :param data_byte_11: Data Byte 11
            :type data_byte_11: ``int`` or ``HexList``
            :param data_byte_12: Data Byte 12
            :type data_byte_12: ``int`` or ``HexList``
            :param data_byte_13: Data Byte 13
            :type data_byte_13: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: TdeWriteDataResponse
            :rtype: ``TdeWriteDataResponse``
            """
            feature_1eb0_index, feature_1eb0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1eb0.tde_write_data_cls(
                device_index=device_index,
                feature_index=feature_1eb0_index,
                starting_position=HexList(starting_position),
                number_of_bytes_to_read_or_write=HexList(number_of_bytes_to_read_or_write),
                data_byte_0=HexList(data_byte_0),
                data_byte_1=HexList(data_byte_1),
                data_byte_2=HexList(data_byte_2),
                data_byte_3=HexList(data_byte_3),
                data_byte_4=HexList(data_byte_4),
                data_byte_5=HexList(data_byte_5),
                data_byte_6=HexList(data_byte_6),
                data_byte_7=HexList(data_byte_7),
                data_byte_8=HexList(data_byte_8),
                data_byte_9=HexList(data_byte_9),
                data_byte_10=HexList(data_byte_10),
                data_byte_11=HexList(data_byte_11),
                data_byte_12=HexList(data_byte_12),
                data_byte_13=HexList(data_byte_13))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1eb0.tde_write_data_response_cls)
            return response
        # end def tde_write_data

        @classmethod
        def tde_read_data(cls, test_case, starting_position, number_of_bytes_to_read, device_index=None,
                          port_index=None):
            """
            Process ``TdeReadData``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param starting_position: Starting Position
            :type starting_position: ``int`` or ``HexList``
            :param number_of_bytes_to_read: Number Of Bytes To Read
            :type number_of_bytes_to_read: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: TdeReadDataResponse
            :rtype: ``TdeReadDataResponse``
            """
            feature_1eb0_index, feature_1eb0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1eb0.tde_read_data_cls(
                device_index=device_index,
                feature_index=feature_1eb0_index,
                starting_position=HexList(starting_position),
                number_of_bytes_to_read=HexList(number_of_bytes_to_read))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1eb0.tde_read_data_response_cls)
            return response
        # end def tde_read_data

        @classmethod
        def tde_clear_data(cls, test_case, device_index=None, port_index=None):
            """
            Process ``TdeClearData``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: TdeClearDataResponse
            :rtype: ``TdeClearDataResponse``
            """
            feature_1eb0_index, feature_1eb0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1eb0.tde_clear_data_cls(
                device_index=device_index,
                feature_index=feature_1eb0_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1eb0.tde_clear_data_response_cls)
            return response
        # end def tde_clear_data
    # end class HIDppHelper

    class NvsHelper(object):
        """
        Non Volatile Memory Helper class
        """

        @classmethod
        def validate_tde_chunk(cls, test_case):
            """
            Check NVS device tde chunk content.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            if test_case.memory_manager is None:
                sys.stdout.write("\nNo memory manager for this device\n")
                return None
            # end if
            # Dump receiver NVS
            test_case.memory_manager.read_nvs()
            # Extract TDE chunks
            chunks = test_case.memory_manager.get_chunks_by_name('NVS_TDE_MFG_ACCESS_ID')
            chunk_size = len(chunks)
            if chunk_size == 0:
                test_case.log_warning("No Device TDE MFG chunk found")
                return None
            # end if
            # ---------------------------------------------------------------------
            LogHelper.log_check(test_case, "Validate previous & current nvs chunk")
            # ---------------------------------------------------------------------
            for i in range(chunk_size):
                if i == 0:
                    continue
                # end if
                if i + 1 == chunk_size:
                    break
                # end if
                test_case.assertNotEqual(
                    unexpected=chunks[i],
                    obtained=chunks[i + 1],
                    msg=f"The previous chunk {i}: {chunks[i]} and current chunk {i + 1}: {chunks[i + 1]} are same")
            # end for
            return True
        # end def validate_tde_chunk

        @classmethod
        def write_tde_chunk(cls, test_case, data, no_reset=False):
            """
            Write data to NVS_TDE_MFG_ACCESS_ID chunk

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param data: TDE memory data
            :type data: ``HexList``
            :param no_reset: Flag enabling to reload the NVS without resetting the device, only stop and run - OPTIONAL
            :type no_reset: ``bool``
            """
            if len(data) > test_case.f.PRODUCT.FEATURES.COMMON.TDE_ACCESS_TO_NVM.F_TdeMaxSize:
                raise ValueError(f"The input data length({len(data)}) is too big, the maximum length of data is: "
                                 f"{test_case.f.PRODUCT.FEATURES.COMMON.TDE_ACCESS_TO_NVM.F_TdeMaxSize}.")
            # end if

            test_case.device_memory_manager.read_nvs()
            test_case.device_memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_TDE_MFG_ACCESS_ID',
                                                                     data=data)
            test_case.device_memory_manager.load_nvs(no_reset=no_reset)
        # end def write_tde_chunk
    # end class NvsHelper
# end class TdeAccessToNvmTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
