#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.opticalswitchesutils
:brief: Helpers for ``OpticalSwitches`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.opticalswitches import OpticalSwitches
from pyhid.hidpp.features.common.opticalswitches import OpticalSwitchesFactory
from pylibrary.mcu.kbdmasktablechunk import KbdMaskTableChunk
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OpticalSwitchesTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``OpticalSwitches`` feature
    """

    class GetHardwareInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetHardwareInfoResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES
            return {
                "nb_columns": (
                    cls.check_nb_columns,
                    config.F_NbColumns),
                "nb_rows": (
                    cls.check_nb_rows,
                    config.F_NbRows),
                "timeout_us": (
                    cls.check_timeout_us,
                    config.F_TimeoutUs)
            }
        # end def get_default_check_map

        @staticmethod
        def check_nb_columns(test_case, response, expected):
            """
            Check nb_columns field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHardwareInfoResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetHardwareInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert nb_columns that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="NbColumns shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nb_columns),
                msg="The nb_columns parameter differs "
                    f"(expected:{expected}, obtained:{response.nb_columns})")
        # end def check_nb_columns

        @staticmethod
        def check_nb_rows(test_case, response, expected):
            """
            Check nb_rows field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHardwareInfoResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetHardwareInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert nb_rows that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="NbRows shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nb_rows),
                msg="The nb_rows parameter differs "
                    f"(expected:{expected}, obtained:{response.nb_rows})")
        # end def check_nb_rows

        @staticmethod
        def check_timeout_us(test_case, response, expected):
            """
            Check timeout_us field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetHardwareInfoResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetHardwareInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert timeout_us that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="TimeoutUs shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.timeout_us),
                msg="The timeout_us parameter differs "
                    f"(expected:{expected}, obtained:{response.timeout_us})")
        # end def check_timeout_us
    # end class GetHardwareInfoResponseChecker

    class GenerateMaskTableResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GenerateMaskTableResponse``
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
            return cls.get_check_map(test_case=test_case, supported_lang_layout_index=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, supported_lang_layout_index):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param supported_lang_layout_index: The index of supported language key layout
            :type supported_lang_layout_index: ``int``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "nb_available_keys": (
                    cls.check_nb_available_keys,
                    test_case.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES.F_NbAvailableKeys[supported_lang_layout_index])
            }
        # end def get_default_check_map

        @staticmethod
        def check_nb_available_keys(test_case, response, expected):
            """
            Check nb_available_keys field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GenerateMaskTableResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GenerateMaskTableResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert nb_available_keys that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="NbAvailableKeys shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.nb_available_keys),
                msg="The nb_available_keys parameter differs "
                    f"(expected:{expected}, obtained:{response.nb_available_keys})")
        # end def check_nb_available_keys
    # end class GenerateMaskTableResponseChecker

    class GetMaskTableResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetMaskTableResponse``
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
            return cls.get_check_map(test_case=test_case, col_index=0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, col_index, supported_lang_layout_index=0):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param col_index: The index of column
            :type col_index: ``int``
            :param supported_lang_layout_index: The index of supported language key layout - OPTIONAL
            :type supported_lang_layout_index: ``int``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.OPTICAL_SWITCHES
            col_mask = getattr(config, f'F_ColumnMaskTable_{col_index}')
            return {
                "port_0_row_mask": (
                    cls.check_port_0_row_mask,
                    (col_mask[supported_lang_layout_index] & 0xFFFF0000) >> 32),
                "port_1_row_mask": (
                    cls.check_port_1_row_mask,
                    col_mask[supported_lang_layout_index] & 0xFFFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_port_0_row_mask(test_case, response, expected):
            """
            Check port_0_row_mask field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetMaskTableResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetMaskTableResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert port_0_row_mask that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Port0RowMask shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.port_0_row_mask),
                msg="The port_0_row_mask parameter differs "
                    f"(expected:{expected}, obtained:{response.port_0_row_mask})")
        # end def check_port_0_row_mask

        @staticmethod
        def check_port_1_row_mask(test_case, response, expected):
            """
            Check port_1_row_mask field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetMaskTableResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetMaskTableResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert port_1_row_mask that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Port1RowMask shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.port_1_row_mask),
                msg="The port_1_row_mask parameter differs "
                    f"(expected:{expected}, obtained:{response.port_1_row_mask})")
        # end def check_port_1_row_mask
    # end class GetMaskTableResponseChecker

    class GetKeyReleaseTimingsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetKeyReleaseTimingsResponse``
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
                "min_duration": (
                    cls.check_min_duration,
                    None),
                "max_duration": (
                    cls.check_max_duration,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_min_duration(test_case, response, expected):
            """
            Check min_duration field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetKeyReleaseTimingsResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetKeyReleaseTimingsResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_duration that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="MinDuration shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.min_duration),
                msg="The min_duration parameter differs "
                    f"(expected:{expected}, obtained:{response.min_duration})")
        # end def check_min_duration

        @staticmethod
        def check_max_duration(test_case, response, expected):
            """
            Check max_duration field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetKeyReleaseTimingsResponse to check
            :type response: ``pyhid.hidpp.features.common.opticalswitches.GetKeyReleaseTimingsResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_duration that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="MaxDuration shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.max_duration),
                msg="The max_duration parameter differs "
                    f"(expected:{expected}, obtained:{response.max_duration})")
        # end def check_max_duration
    # end class GetKeyReleaseTimingsResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=OpticalSwitches.FEATURE_ID, factory=OpticalSwitchesFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_hardware_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetHardwareInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetHardwareInfoResponse
            :rtype: ``GetHardwareInfoResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.get_hardware_info_cls(
                device_index=device_index,
                feature_index=feature_1876_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.get_hardware_info_response_cls)
            return response
        # end def get_hardware_info

        @classmethod
        def generate_mask_table(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GenerateMaskTable``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GenerateMaskTableResponse
            :rtype: ``GenerateMaskTableResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.generate_mask_table_cls(
                device_index=device_index,
                feature_index=feature_1876_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.generate_mask_table_response_cls)
            return response
        # end def generate_mask_table

        @classmethod
        def get_mask_table(cls, test_case, column_idx, device_index=None, port_index=None):
            """
            Process ``GetMaskTable``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param column_idx: Column Idx
            :type column_idx: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetMaskTableResponse
            :rtype: ``GetMaskTableResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.get_mask_table_cls(
                device_index=device_index,
                feature_index=feature_1876_index,
                column_idx=HexList(column_idx))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.get_mask_table_response_cls)
            return response
        # end def get_mask_table

        @classmethod
        def init_test(cls, test_case, device_index=None, port_index=None):
            """
            Process ``InitTest``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: InitTestResponse
            :rtype: ``InitTestResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.init_test_cls(
                device_index=device_index,
                feature_index=feature_1876_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.init_test_response_cls)
            return response
        # end def init_test

        @classmethod
        def get_key_release_timings(cls, test_case, column_idx, device_index=None, port_index=None):
            """
            Process ``GetKeyReleaseTimings``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param column_idx: Column Idx
            :type column_idx: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetKeyReleaseTimingsResponse
            :rtype: ``GetKeyReleaseTimingsResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.get_key_release_timings_cls(
                device_index=device_index,
                feature_index=feature_1876_index,
                column_idx=HexList(column_idx))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.get_key_release_timings_response_cls)
            return response
        # end def get_key_release_timings

        @classmethod
        def config_emit_time(cls, test_case, emit_time_us, device_index=None, port_index=None):
            """
            Process ``ConfigEmitTime``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param emit_time_us: Emit Time Us
            :type emit_time_us: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ConfigEmitTimeResponse
            :rtype: ``ConfigEmitTimeResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.config_emit_time_cls(
                device_index=device_index,
                feature_index=feature_1876_index,
                emit_time_us=HexList(emit_time_us))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.config_emit_time_response_cls)
            return response
        # end def config_emit_time

        @classmethod
        def end_test(cls, test_case, device_index=None, port_index=None):
            """
            Process ``EndTest``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: EndTestResponse
            :rtype: ``EndTestResponse``
            """
            feature_1876_index, feature_1876, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1876.end_test_cls(
                device_index=device_index,
                feature_index=feature_1876_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1876.end_test_response_cls)
            return response
        # end def end_test
    # end class HIDppHelper

    class NvsHelper(DeviceBaseTestUtils.NvsHelper):
        # See ``CommonBaseTestUtils.NvsHelper``
        @staticmethod
        def add_kbd_mask_table(test_case, kbd_mask_table, no_reset=False):
            """
            Add a NVS_KBD_MASK_TABLE_ID chunk

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param kbd_mask_table: The keyboard mask table
            :type kbd_mask_table: ``HexList``
            :param no_reset: Flag enabling to reload the NVS without resetting the device, only stop and run - OPTIONAL
            :type no_reset: ``bool``
            """
            test_case.device_memory_manager.read_nvs()
            test_case.device_memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_KBD_MASK_TABLE_ID',
                                                                     data=kbd_mask_table)
            test_case.device_memory_manager.load_nvs(no_reset=no_reset)
        # end def add_kbd_mask_table

        @staticmethod
        def get_kbd_mask_table(test_case):
            """
            Get keyboard mask table from NVS

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The ``KbdMaskTableChunk`` object
            :rtype: ``KbdMaskTableChunk``
            """
            test_case.memory_manager.read_nvs()
            return test_case.memory_manager.get_chunks_by_name(chunk_name='NVS_KBD_MASK_TABLE_ID')
        # end def write_kbd_mask_table
    # end class NvsHelper
# end class OpticalSwitchesTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
