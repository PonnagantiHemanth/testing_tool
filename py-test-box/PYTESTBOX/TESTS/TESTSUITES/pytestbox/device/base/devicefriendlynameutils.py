#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.devicefriendlynameutils
:brief: Helpers for DeviceFriendlyName feature
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2020/09/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from warnings import warn

from pyhid.hidpp.features.common.deviceinformation import ascii_converter
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceFriendlyNameTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on DeviceFriendlyName feature
    """
    class GetFriendlyNameLenHelper(object):
        """
        GetFriendlyNameLen helper
        """
        class MessageChecker(DeviceBaseTestUtils.MessageChecker):
            """
            GetFriendlyNameLen MessageChecker
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Get the default check methods and expected values for the GetFriendlyNameLen API

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: Default check map
                :rtype: ``dict``
                """
                dfn = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME
                return {
                        "name_len": (cls.check_name_len, dfn.F_NameMaxLength),
                        "name_max_len": (cls.check_name_max_len, dfn.F_NameMaxLength),
                        "default_name_len": (cls.check_default_name_len, dfn.F_NameMaxLength),
                }
            # end def get_default_check_map

            @staticmethod
            def check_name_len(test_case, response, expected):
                """
                Check name_len field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetFriendlyNameLenResponse to check
                :type response: ``GetFriendlyNameLenResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.name_len))
                max_value = int(Numeral(expected))
                # -------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate nameLen:{value} is in range(1, {max_value})")
                # -------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(1 <= value <= max_value),
                                     msg=f'The name_len:{value} is not in range(1, {max_value})')
            # end def check_name_len

            @staticmethod
            def check_name_max_len(test_case, response, expected):
                """
                Check name_max_len field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetFriendlyNameLenResponse to check
                :type response: ``GetFriendlyNameLenResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                # -------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate name_max_len:{response.name_max_len} is in [18, 16, 14]")
                # -------------------------------------------------------------------------------------------------
                test_case.assertEqual(
                        expected=HexList(expected),
                        obtained=HexList(response.name_max_len),
                        msg=f"The name_max_len parameter differs "
                            f"(expected:{HexList(expected)}, obtained:{HexList(response.name_max_len)})")
            # end def check_name_max_len

            @staticmethod
            def check_default_name_len(test_case, response, expected):
                """
                Check default_name_len field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetFriendlyNameLenResponse to check
                :type response: ``GetFriendlyNameLenResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.default_name_len))
                max_value = int(Numeral(expected))
                # ----------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate default_name_len:{value} is in range(1, {max_value})")
                # ----------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(1 <= value <= max_value),
                                     msg=f'The default_name_len:{value} is not in range(1, {max_value})')
            # end def check_default_name_len
        # end class class MessageChecker

        class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
            """
            GetFriendlyNameLen HIDppHelper
            """
            @classmethod
            def get_friendly_name_len(cls, test_case):
                """
                Process GetFriendlyNameLen

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: GetFriendlyNameLenResponse
                :rtype: ``GetFriendlyNameLenResponse``
                """
                # ---------------------------------------------------------------
                LogHelper.log_step(test_case, 'Send GetFriendlyNameLen request')
                # ---------------------------------------------------------------
                report = test_case.feature_0007.get_friendly_name_len_cls(
                        test_case.deviceIndex, test_case.feature_0007_index)
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_0007.get_friendly_name_len_response_cls)
                DeviceFriendlyNameTestUtils.GetFriendlyNameLenHelper.MessageChecker.check_fields(
                        test_case, response, test_case.feature_0007.get_friendly_name_len_response_cls)
                return response
            # end def get_friendly_name_len
        # end class HIDppHelper
    # end class GetFriendlyNameLenHelper

    class GetFriendlyNameHelper(object):
        """
        GetFriendlyName helper
        """
        class MessageChecker(DeviceBaseTestUtils.MessageChecker):
            """
            GetFriendlyName MessageChecker
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Get the default check methods and expected values for the GetFriendlyName API

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: Default check map
                :rtype: ``dict``
                """
                dfn = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME
                return {
                        "byte_index": (cls.check_byte_index_range, dfn.F_NameMaxLength),
                        "name_chunk": (cls.check_name_chunk_len, dfn.F_NameMaxLength),
                }
            # end def get_default_check_map

            @staticmethod
            def check_byte_index_range(test_case, response, expected):
                """
                Check byte_index field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetFriendlyNameResponse to check
                :type response: ``GetFriendlyNameResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.byte_index))
                max_value = int(Numeral(expected))
                # ----------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate GetFriendlyName.byte_index:{value} in range(0, {max_value}")
                # ----------------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(0 <= value <= max_value),
                                     msg=f'The byte_index:{value} is not in range(0, {max_value})')
            # end def check_byte_index_range

            @staticmethod
            def check_name_chunk_len(test_case, response, expected):
                """
                Check name_chunk field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetFriendlyNameResponse to check
                :type response: ``GetFriendlyNameResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value_to_test = len(response.name_chunk)
                while value_to_test > 0 and response.name_chunk[value_to_test-1] == 0:
                    value_to_test -= 1
                # end while
                # -------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate GetFriendlyNameResponse.name_chunk: {response.name_chunk}")
                # -------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(1 <= value_to_test <= int(Numeral(expected))),
                                     msg=f'The name_chunk:{response.name_chunk} is not in range(1, {expected})')
            # end def check_name_chunk_len

            @staticmethod
            def check_name_length(test_case, name_len, full_name):
                """
                Check name_len

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param name_len: GetFriendlyName.name_len
                :type name_len: ``int``
                :param full_name: full name
                :type full_name: ``str``
                """
                length = int(Numeral(name_len))
                # ----------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, "Validate GetFriendlyName.name_len with name_chunk length value")
                # ----------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(length == len(full_name)),
                                     msg=f'The name_len({length}) is different from '
                                         f'({len(full_name)}) for ({full_name})')
            # end def check_name_length

            @staticmethod
            def check_length(test_case, obtained, expected):
                """
                Check name_len

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param obtained: GetFriendlyName.name_len
                :type obtained: ``int``
                :param expected: SetFriendlyName.name_len
                :type expected: ``int``
                """
                # ---------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, "Validate GetFriendlyName.name_len == SetFriendlyName.name_len")
                # ---------------------------------------------------------------------------------------------
                test_case.assertEqual(obtained=obtained, expected=expected,
                                      msg=f"GetFriendlyName.name_len({obtained}) ~= "
                                          f"SetFriendlyName.name_len({expected})")
            # end def check_length

            @staticmethod
            def check_name_match(test_case, received_name, given_name):
                """
                Check name_chunk

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param received_name: GetFriendlyName.name_chunk
                :type received_name: ``str`` or ``HexList``
                :param given_name: SetFriendlyName.name_chunk
                :type given_name: ``str`` or ``HexList``
                """
                # -------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, "Validate SetFriendlyName.name_chunk == GetFriendlyName.name_chunk")
                # -------------------------------------------------------------------------------------------------
                test_case.assertEqual(obtained=received_name,
                                      expected=given_name,
                                      msg=f"The given_name({given_name}) differs from received_name({received_name})")
            # end def check_name_match

            @staticmethod
            def check_equal_value(test_case, obtained, expected):
                """
                Check length

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param obtained: Obtained value
                :type obtained: ``int`` or ``str`` or ``HexList``
                :param expected: Expected value
                :type expected: ``int`` or ``str`` or ``HexList``
                """
                # ----------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate equal value obtained:{obtained} expected: {expected}")
                # ----------------------------------------------------------------------------------------------
                test_case.assertEqual(
                        expected=expected,
                        obtained=obtained,
                        msg=f"The value parameter differs (expected:{expected}, obtained:{obtained})")
            # end def check_equal_value
        # end class MessageChecker

        class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
            """
            GetFriendlyName HIDppHelper
            """
            @classmethod
            def get_friendly_name(cls, test_case, byte_index=0):
                """
                Process GetFriendlyName

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param byte_index: parameter index
                :type byte_index: ``int`` or ``HexList``

                :return: GetFriendlyName.NameChunk
                :rtype: ``str``
                """
                # ------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f'Send GetFriendlyName request with byte_index: {byte_index}')
                # ------------------------------------------------------------------------------------------
                report = test_case.feature_0007.get_friendly_name_cls(
                        test_case.deviceIndex, test_case.feature_0007_index, HexList(byte_index))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_0007.get_friendly_name_response_cls)
                DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_fields(
                        test_case, response, test_case.feature_0007.get_friendly_name_response_cls)
                return ascii_converter(response.name_chunk)
            # end def get_friendly_name

            @classmethod
            def get_full_name(cls, test_case, length):
                """
                Process and get full name

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param length: name length
                :type length: ``int`` or ``HexList``

                :return: full name string
                :rtype: ``str``
                """
                full_name = ""
                byte_index = 0
                while byte_index < int(Numeral(length)):
                    response = cls.get_friendly_name(test_case, byte_index=byte_index)
                    if response is None or len(response) <= 0:
                        break
                    # end if
                    byte_index = byte_index + len(response)
                    full_name = full_name + response
                # end while
                DeviceFriendlyNameTestUtils.GetFriendlyNameHelper.MessageChecker.check_name_length(
                        test_case, length, full_name)
                return full_name
            # end def get_full_name
        # end class HIDppHelper
    # end class GetFriendlyNameHelper

    class GetDefaultFriendlyNameHelper(object):
        """
        GetDefaultFriendlyName helper
        """
        class MessageChecker(DeviceBaseTestUtils.MessageChecker):
            """
            GetDefaultFriendlyName MessageChecker
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Get the default check methods and expected values for the GetFriendlyName API

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: Default check map
                :rtype: ``dict``
                """
                dfn = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME
                return {
                        "byte_index": (cls.check_byte_index_range, dfn.F_NameMaxLength),
                        "name_chunk": (cls.check_name_chunk_len, dfn.F_NameMaxLength),
                }
            # end def get_default_check_map

            @staticmethod
            def check_byte_index_range(test_case, response, expected):
                """
                Check byte_index field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetDefaultFriendlyNameResponse to check
                :type response: ``GetDefaultFriendlyNameResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.byte_index))
                max_value = int(Numeral(expected))
                # ------------------------------------------------------------------------------------------------
                LogHelper.log_check(
                        test_case,
                        f"Validate GetDefaultFriendlyNameResponse.byte_index:{value} is in range(0, {max_value})")
                # ------------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(0 <= value <= max_value),
                                     msg=f'The byte_index:{value} is not in range(0, {max_value})')
            # end def check_byte_index_range

            @staticmethod
            def check_name_chunk_len(test_case, response, expected):
                """
                Check name_chunk field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: GetDefaultFriendlyNameResponse to check
                :type response: ``GetDefaultFriendlyNameResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value_to_test = len(response.name_chunk)
                while value_to_test > 0 and response.name_chunk[value_to_test-1] == 0:
                    value_to_test -= 1
                # end while
                # ---------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case,
                                    f"Validate GetDefaultFriendlyNameResponse.nameChunk:{response.name_chunk}")
                # ---------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(0 < value_to_test <= int(Numeral(expected))),
                                     msg=f'The name_chunk({response.name_chunk}) is not in range(0, {expected})')
            # end def check_name_chunk_len

            @staticmethod
            def check_default_name_length(test_case, default_name_len, name):
                """
                Check default_name_len

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param default_name_len: GetFriendlyName.default_name_len
                :type default_name_len: ``int`` or ``HexList``
                :param name: default name
                :type name: ``str``
                """
                # ----------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate GetFriendlyName.default_name_len: {default_name_len}")
                # ----------------------------------------------------------------------------------------------
                length = int(Numeral(default_name_len))
                test_case.assertTrue(expr=(length == len(name)),
                                     msg=f'The default_name_len({length}) is different from ({len(name)})')
            # end def check_default_name_length
        # end class MessageChecker

        class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
            """
            GetDefaultFriendlyName HIDppHelper
            """
            @classmethod
            def get_default_friendly_name(cls, test_case, byte_index=0):
                """
                Process GetDefaultFriendlyName

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param byte_index: parameter index
                :type byte_index: ``int`` or ``HexList``

                :return: GetDefaultFriendlyNameResponse
                :rtype: ``GetDefaultFriendlyNameResponse``
                """
                # -------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f'Send GetDefaultFriendlyName request with byte_index: {byte_index}')
                # -------------------------------------------------------------------------------------------------
                report = test_case.feature_0007.get_default_friendly_name_cls(
                        test_case.deviceIndex, test_case.feature_0007_index, HexList(byte_index))
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_0007.get_default_friendly_name_response_cls)
                DeviceFriendlyNameTestUtils.GetDefaultFriendlyNameHelper.MessageChecker.check_fields(
                        test_case, response, test_case.feature_0007.get_default_friendly_name_response_cls)
                return ascii_converter(response.name_chunk)
            # end def get_default_friendly_name

            @classmethod
            def get_full_name(cls, test_case, length):
                """
                Process and get full name

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param length: name length
                :type length: ``int`` or ``HexList``

                :return: full name string
                :rtype: ``str``
                """
                full_name = ""
                byte_index = 0
                while byte_index < int(Numeral(length)):
                    response = cls.get_default_friendly_name(test_case, byte_index=byte_index)
                    if response is None or len(response) <= 0:
                        break
                    # end if
                    byte_index = byte_index + len(response)
                    full_name = full_name + response
                # end while
                DeviceFriendlyNameTestUtils.GetDefaultFriendlyNameHelper.MessageChecker.check_default_name_length(
                        test_case, length, full_name)
                return full_name
            # end def get_full_name
        # end class HIDppHelper
    # end class GetDefaultFriendlyNameHelper

    class SetFriendlyNameHelper(object):
        """
        SetFriendlyName helper
        """
        class MessageChecker(DeviceBaseTestUtils.MessageChecker):
            """
            SetFriendlyName MessageChecker
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Get the default check methods and expected values for the SetFriendlyNameResponse API

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: Default check map
                :rtype: ``dict``
                """
                dfn = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME
                return {
                        "name_len": (cls.check_name_len, dfn.F_NameMaxLength)
                }
            # end def get_default_check_map

            @staticmethod
            def check_name_len(test_case, response, expected):
                """
                Check name_len field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: SetFriendlyNameResponse to check
                :type response: ``SetFriendlyNameResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.name_len))
                max_value = int(Numeral(expected))
                # ---------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate SetFriendlyName.name_len:{value} in range(1, {max_value})")
                # ---------------------------------------------------------------------------------------------------
                test_case.assertTrue(expr=(1 <= value <= max_value),
                                     msg=f'The name_len({response.name_len}) is not in range(1, {expected})')
            # end def check_name_len

            @staticmethod
            def check_equal_value(test_case, obtained, expected):
                """
                Check values are equal

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param obtained: Obtained value
                :type obtained: ``int`` or ``str`` or ``HexList``
                :param expected: Expected value
                :type expected: ``int`` or ``str`` or ``HexList``
                """
                # ------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate equal value (expected:{expected}, obtained:{obtained})")
                # ------------------------------------------------------------------------------------------------
                test_case.assertEqual(
                        expected=expected,
                        obtained=obtained,
                        msg=f"The value parameter differs (expected:{expected}, obtained:{obtained})")
            # end def check_equal_value
        # end class MessageChecker

        class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
            """
            SetFriendlyName HIDppHelper
            """
            @classmethod
            def set_friendly_name(cls, test_case, byte_index, name_chunk):
                """
                Process SetFriendlyName

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param byte_index: parameter index
                :type byte_index: ``int``
                :param name_chunk: friendly name
                :type name_chunk: ``str`` or ``HexList``

                :return: SetFriendlyNameResponse
                :rtype: ``SetFriendlyNameResponse``
                """
                # --------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case,
                                   f'Send SetFriendlyName request with byte_index:{byte_index} & name:{name_chunk}')
                # --------------------------------------------------------------------------------------------------
                report = test_case.feature_0007.set_friendly_name_cls(
                        test_case.deviceIndex, test_case.feature_0007_index, byte_index, name_chunk)
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_0007.set_friendly_name_response_cls)
                DeviceFriendlyNameTestUtils.SetFriendlyNameHelper.MessageChecker.check_fields(
                        test_case, response, test_case.feature_0007.set_friendly_name_response_cls)
                return response
            # end def set_friendly_name
        # end class HIDppHelper
    # end class SetFriendlyNameHelper

    class ResetFriendlyNameHelper(object):
        """
        ResetFriendlyName helper
        """
        class MessageChecker(DeviceBaseTestUtils.MessageChecker):
            """
            ResetFriendlyName MessageChecker
            """
            @classmethod
            def get_default_check_map(cls, test_case):
                """
                Get the default check methods and expected values for the ResetFriendlyNameResponse API

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: Default check map
                :rtype: ``dict``
                """
                dfn = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_FRIENDLY_NAME
                return {
                        "name_len": (cls.check_name_len, dfn.F_NameMaxLength)
                }
            # end def get_default_check_map

            @staticmethod
            def check_name_len(test_case, response, expected):
                """
                Check name_len field in response

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``
                :param response: ResetFriendlyNameResponse to check
                :type response: ``ResetFriendlyNameResponse``
                :param expected: Expected value
                :type expected: ``int`` or ``HexList``
                """
                value = int(Numeral(response.name_len))
                max_value = int(Numeral(expected))
                # ----------------------------------------------------------------------------------
                LogHelper.log_check(test_case, f"Validate nameLen:{value} is range(1, {max_value})")
                # ----------------------------------------------------------------------------------
                test_case.assertTrue(expr=(1 <= value <= max_value),
                                     msg=f'The name_len:{value} is not in range(1, {max_value})')
            # end def check_name_len
        # end class MessageChecker

        class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
            """
            ResetFriendlyName HIDppHelper
            """
            @classmethod
            def reset_friendly_name(cls, test_case):
                """
                Process ResetFriendlyName

                :param test_case: Current test case
                :type test_case: ``BaseTestCase``

                :return: ResetFriendlyNameResponse
                :rtype: ``ResetFriendlyNameResponse``
                """
                # -------------------------------------------------------------
                LogHelper.log_step(test_case, 'Send ResetFriendlyName request')
                # -------------------------------------------------------------
                report = test_case.feature_0007.reset_friendly_name_cls(
                        test_case.deviceIndex, test_case.feature_0007_index)
                response = test_case.send_report_wait_response(
                        report=report,
                        response_queue=test_case.hidDispatcher.common_message_queue,
                        response_class_type=test_case.feature_0007.reset_friendly_name_response_cls)
                DeviceFriendlyNameTestUtils.ResetFriendlyNameHelper.MessageChecker.check_fields(
                        test_case, response, test_case.feature_0007.reset_friendly_name_response_cls)
                return response
            # end def reset_friendly_name
        # end class HIDppHelper
    # end class ResetFriendlyNameHelper

    class NvsHelper(object):
        """
        Non Volatile Storage helper
        """
        @classmethod
        def validate_nvs_chunk(cls, test_case):
            """
            Check NVS device tde chunk content.

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            """
            if test_case.memory_manager is None:
                # No memory manager for this device
                return None
            # end if
            # Dump receiver NVS
            test_case.memory_manager.read_nvs()
            # Extract TDE chunks
            chunks = test_case.memory_manager.get_chunks_by_name("NVS_DEVICE_FRIENDLY_NAME_ID")
            chunk_size = len(chunks)
            if chunk_size == 0:
                warn("No Device Friendly Name chunk found")
                return None
            # end if
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
                        msg=f"The previous chunk ({i}) and current chunk ({i + 1}) are same ({chunks[i]})")
            # end for
            return True
        # end def validate_nvs_chunk
    # end class NvsHelper
# end class DeviceFriendlyNameTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
