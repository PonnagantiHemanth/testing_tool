#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.analysismodeutils
:brief: Helpers for ``AnalysisMode`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/07/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hid import HidMouse
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.analysismode import AccumulationPacket
from pyhid.hidpp.features.mouse.analysismode import AnalysisMode
from pyhid.hidpp.features.mouse.analysismode import AnalysisModeFactory
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisDataV0Response
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisDataV1Response
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisModeV0Response
from pyhid.hidpp.features.mouse.analysismode import GetAnalysisModeV1Response
from pyhid.hidpp.features.mouse.analysismode import SetAnalysisModeV0Response
from pyhid.hidpp.features.mouse.analysismode import SetAnalysisModeV1Response
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.hid.base.hidreportutils import to_signed_int


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalysisModeTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``AnalysisMode`` feature
    """

    class GetAnalysisModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetAnalysisModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.MOUSE.ANALYSIS_MODE
            check_map = {
                "mode": (cls.check_mode, AnalysisMode.MODE.OFF)
            }
            if test_case.config_manager.get_feature_version(config) > 0:
                check_map.update(
                    {
                        "capabilities": (cls.check_capabilities, config.F_OverflowCapability)
                    }
                )
            # end if
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_mode(test_case, response, expected):
            """
            Check mode field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetAnalysisModeResponse to check
            :type response: ``GetAnalysisModeV0Response`` or ``GetAnalysisModeV1Response``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert mode that raise an exception
            """
            test_case.assertNotNone(expected, msg="The mode shall be passed as an argument")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(response.mode),
                                  msg="The mode parameter differs from the one expected")
        # end def check_mode

        @staticmethod
        def check_capabilities(test_case, response, expected):
            """
            Check capabilities field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetAnalysisModeResponse to check
            :type response: ``GetAnalysisModeV1Response``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert mode that raise an exception
            """
            test_case.assertNotNone(expected, msg="The capabilities shall be passed as an argument")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(response.capabilities.overflow),
                                  msg="The capabilities parameter differs from the one expected")
        # end def check_capabilities
    # end class GetAnalysisModeResponseChecker

    class SetAnalysisModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetAnalysisModeResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "mode": (cls.check_mode, AnalysisMode.MODE.OFF)
            }
        # end def get_default_check_map

        @staticmethod
        def check_mode(test_case, response, expected):
            """
            Check mode field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetAnalysisModeResponse to check
            :type response: ``SetAnalysisModeV0Response`` or ``SetAnalysisModeV1Response``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``

            :raise ``AssertionError``: Assert mode that raise an exception
            """
            test_case.assertNotNone(expected, msg="The mode shall be passed as an argument")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(response.mode),
                                  msg="The mode parameter differs from the one expected")
        # end def check_mode
    # end class SetAnalysisModeResponseChecker

    class GetAnalysisDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetAnalysisDataResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "data": (cls.check_data, HexList(Numeral(source=GetAnalysisDataV0Response.DefaultValue.DATA,
                                                         byteCount=GetAnalysisDataV0Response.LEN.DATA // 8)))
            }
        # end def get_default_check_map

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetAnalysisDataResponse to check
            :type response: ``GetAnalysisDataV0Response`` or ``GetAnalysisDataV1Response``
            :param expected: Expected value
            :type expected: ``HexList`` or ``int``

            :raise ``AssertionError``: Assert data that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The data shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(response.data),
                                  msg="The data parameter differs from the one expected")
        # end def check_data
    # end class GetAnalysisDataResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=AnalysisMode.FEATURE_ID,
                           factory=AnalysisModeFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_analysis_mode(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetAnalysisMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int`` or ``None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int`` or ``None``

            :return: GetAnalysisModeResponse
            :rtype: ``GetAnalysisModeV0Response`` or  ``GetAnalysisModeV1Response``
            """
            feature_2250_index, feature_2250, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2250.get_analysis_mode_cls(
                device_index=device_index,
                feature_index=feature_2250_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(test_case=test_case, report=report,
                                     response_queue_name=HIDDispatcher.QueueName.MOUSE,
                                     response_class_type=feature_2250.get_analysis_mode_response_cls)
        # end def get_analysis_mode

        @classmethod
        def get_analysis_mode_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetAnalysisMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int`` or ``None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            """
            feature_2250_index, feature_2250, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2250.get_analysis_mode_cls(device_index=device_index, feature_index=feature_2250_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_analysis_mode_and_check_error

        @classmethod
        def set_analysis_mode(cls, test_case, mode, device_index=None, port_index=None, software_id=None,
                              padding=None):
            """
            Process ``SetAnalysisMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param mode: The mode is used to start or stop the analysis mode
            :type mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int`` or ``None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int`` or ``None``

            :return: SetAnalysisModeResponse
            :rtype: ``SetAnalysisModeV0Response`` or ``SetAnalysisModeV1Response``
            """
            feature_2250_index, feature_2250, device_index, _ = cls.get_parameters(test_case,
                                                                                   device_index=device_index,
                                                                                   port_index=port_index)

            report = feature_2250.set_analysis_mode_cls(device_index=device_index, feature_index=feature_2250_index,
                                                        mode=HexList(mode))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(test_case=test_case, report=report,
                                     response_queue_name=HIDDispatcher.QueueName.MOUSE,
                                     response_class_type=feature_2250.set_analysis_mode_response_cls)
        # end def set_analysis_mode

        @classmethod
        def set_analysis_mode_and_check_error(
                cls, test_case, error_codes, mode, function_index=None, device_index=None, port_index=None):
            """
            Process ``SetAnalysisMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param mode: The mode is used to start or stop the analysis mode
            :type mode: ``int`` or ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int`` or ``None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            """
            feature_2250_index, feature_2250, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2250.set_analysis_mode_cls(device_index=device_index, feature_index=feature_2250_index,
                                                        mode=HexList(mode))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_analysis_mode_and_check_error

        @classmethod
        def get_analysis_data(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetAnalysisData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int`` or ``None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int`` or ``None``

            :return: GetAnalysisDataResponse
            :rtype: ``GetAnalysisDataV0Response`` or ``GetAnalysisDataV1Response``
            """
            feature_2250_index, feature_2250, device_index, _ = cls.get_parameters(test_case,
                                                                                   device_index=device_index,
                                                                                   port_index=port_index)

            report = feature_2250.get_analysis_data_cls(device_index=device_index, feature_index=feature_2250_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(test_case=test_case, report=report,
                                     response_queue_name=HIDDispatcher.QueueName.MOUSE,
                                     response_class_type=feature_2250.get_analysis_data_response_cls)
        # end def get_analysis_data

        @classmethod
        def get_analysis_data_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetAnalysisData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int`` or ``None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            """
            feature_2250_index, feature_2250, device_index, _ = cls.get_parameters(test_case, device_index=device_index,
                                                                                   port_index=port_index)

            report = feature_2250.get_analysis_data_cls(device_index=device_index, feature_index=feature_2250_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_analysis_data_and_check_error
    # end class HIDppHelper

    @classmethod
    def compute_cumulative_displacement(cls, test_case):
        """
        Retrieve all HID Mouse messages sent on the HID interface.
        Split positive and negative values into 2 groups.
        Compute cumulative counter for X and Y parameters.

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :return: Concatenated structure of 4 counters of 4 bytes each
        :rtype: ``AccumulationPacket``
        """
        cumulative_counters = AccumulationPacket()
        response = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                         class_type=HidMouse, timeout=0.1, allow_no_message=True)
        while response is not None:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_trace(test_case, f'HID Mouse Response: {response}')
            # ----------------------------------------------------------------------------------------------------------
            if response.get_absolute_value(HidMouse.FID.X_POS) > 0:
                next_accu = int(Numeral(cumulative_counters.accuPositiveX)) + \
                            response.get_absolute_value(HidMouse.FID.X_POS)

                if next_accu >= test_case.positive_clamped_value:
                    test_case.accu_positive_x_overflow = True
                    if test_case.config.F_OverflowCapability:
                        cumulative_counters.accuPositiveX = test_case.positive_clamped_value
                    else:
                        cumulative_counters.accuPositiveX = next_accu - test_case.positive_clamped_value - 1
                    # end if
                else:
                    cumulative_counters.accuPositiveX = next_accu
                # end if

            elif response.get_absolute_value(HidMouse.FID.X_POS) < 0:
                next_accu = to_signed_int(Numeral(cumulative_counters.accuNegativeX)) + \
                            response.get_absolute_value(HidMouse.FID.X_POS)

                if next_accu < to_signed_int(Numeral(test_case.negative_clamped_value)):
                    test_case.accu_negative_x_overflow = True
                    if test_case.config.F_OverflowCapability:
                        cumulative_counters.accuNegativeX = test_case.negative_clamped_value
                    else:
                        cumulative_counters.accuNegativeX = cls.twos_complement(
                            test_case.negative_clamped_value + next_accu + 1)
                    # end if
                else:
                    cumulative_counters.accuNegativeX = cls.twos_complement(next_accu)
                # end if
            # end if

            if response.get_absolute_value(HidMouse.FID.Y_POS) > 0:
                next_accu = int(Numeral(cumulative_counters.accuPositiveY)) + \
                            response.get_absolute_value(HidMouse.FID.Y_POS)

                if next_accu >= test_case.positive_clamped_value:
                    test_case.accu_positive_y_overflow = True
                    if test_case.config.F_OverflowCapability:
                        cumulative_counters.accuPositiveY = test_case.positive_clamped_value
                    else:
                        cumulative_counters.accuPositiveY = next_accu - test_case.positive_clamped_value - 1
                    # end if
                else:
                    cumulative_counters.accuPositiveY = next_accu
                # end if

            elif response.get_absolute_value(HidMouse.FID.Y_POS) < 0:
                next_accu = to_signed_int(Numeral(cumulative_counters.accuNegativeY)) + response.get_absolute_value(
                    HidMouse.FID.Y_POS)

                if next_accu < to_signed_int(Numeral(test_case.negative_clamped_value)):
                    cls.accu_negative_y_overflow = True
                    if test_case.config.F_OverflowCapability:
                        cumulative_counters.accuNegativeY = test_case.negative_clamped_value
                    else:
                        cumulative_counters.accuNegativeY = cls.twos_complement(
                            test_case.negative_clamped_value + next_accu + 1)
                    # end if
                else:
                    cumulative_counters.accuNegativeY = cls.twos_complement(next_accu)
                # end if
            # end if

            response = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                             class_type=HidMouse, timeout=0.1, allow_no_message=True)
        # end while

        return cumulative_counters
    # end def compute_cumulative_displacement

    @staticmethod
    def twos_complement(n):
        """
        Get the two's complement of a number in a 4 byte long hexlist format

        :param n: The number
        :type n: ``int`` or  ``HexList``

        :return: The two's compliment of the number
        :rtype: ``HexList``
        """
        if n >= 0:
            return HexList(Numeral(n, byteCount=4, fixedLength=True))
        elif n < 0:
            return HexList(~Numeral(-n, byteCount=4, fixedLength=True) + 1)
        # end if
    # end def twos_complement

    @classmethod
    def emulate_continuous_motion(cls, test_case, x=0, y=0):
        """
        Emulate motion that can even be greater than max x and max y optical sensor register capability

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param x: The x displacement value - OPTIONAL
        :type x: ``int``
        :param y: The y displacement value - OPTIONAL
        :type y: ``int``
        """
        max_dx_displacement = test_case.delta_signed_max if x >= 0 else test_case.delta_signed_min + 1
        max_dy_displacement = test_case.delta_signed_max if y >= 0 else test_case.delta_signed_min + 1
        x_repetition = int(x / max_dx_displacement) - 1
        y_repetition = int(y / max_dy_displacement) - 1

        if x:
            dx = x % max_dx_displacement if max_dx_displacement > 0 else -(abs(x) % abs(max_dy_displacement))
            if dx:
                test_case.motion_emulator.xy_motion(dx=dx, dy=0)
                test_case.motion_emulator.commit_actions()
                test_case.motion_emulator.prepare_sequence()
            # end if

            if x_repetition >= 0:
                if x_repetition > OptEmuRegisterMapBase.Limits.REPEAT_MAX:
                    for _ in range((x_repetition - 1) // OptEmuRegisterMapBase.Limits.REPEAT_MAX):
                        test_case.motion_emulator.xy_motion(
                            dx=max_dx_displacement, dy=0, repetition=OptEmuRegisterMapBase.Limits.REPEAT_MAX - 1)
                        test_case.motion_emulator.commit_actions()
                        test_case.motion_emulator.prepare_sequence()
                    # end for
                    x_repetition %= OptEmuRegisterMapBase.Limits.REPEAT_MAX
                # end if
                test_case.motion_emulator.xy_motion(dx=max_dx_displacement, dy=0, repetition=x_repetition)
                test_case.motion_emulator.commit_actions()
                test_case.motion_emulator.prepare_sequence()
            # end if
        # end if

        if y:
            dy = y % max_dy_displacement if max_dy_displacement > 0 else -(abs(y) % abs(max_dy_displacement))
            if dy:
                test_case.motion_emulator.xy_motion(dx=0, dy=dy)
                test_case.motion_emulator.commit_actions()
                test_case.motion_emulator.prepare_sequence()
            # end if
            if y_repetition >= 0:
                if y_repetition > OptEmuRegisterMapBase.Limits.REPEAT_MAX:
                    for _ in range((y_repetition - 1) // OptEmuRegisterMapBase.Limits.REPEAT_MAX):
                        test_case.motion_emulator.xy_motion(
                            dx=0, dy=max_dy_displacement, repetition=OptEmuRegisterMapBase.Limits.REPEAT_MAX - 1)
                        test_case.motion_emulator.commit_actions()
                        test_case.motion_emulator.prepare_sequence()
                    # end for
                    y_repetition %= OptEmuRegisterMapBase.Limits.REPEAT_MAX
                # end if
                test_case.motion_emulator.xy_motion(dx=0, dy=max_dy_displacement, repetition=y_repetition)
                test_case.motion_emulator.commit_actions()
                test_case.motion_emulator.prepare_sequence()
            # end if
        # end if
    # end def emulate_continuous_motion
# end class AnalysisModeTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
