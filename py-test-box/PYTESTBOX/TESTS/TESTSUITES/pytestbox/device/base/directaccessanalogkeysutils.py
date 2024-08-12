#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.directaccessanalogkeysutils
:brief: Helpers for ``DirectAccessAnalogKeys`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import DirectAccessAnalogKeys
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import DirectAccessAnalogKeysFactory
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import GetCapabilitiesResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetAnalogKeyModeResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetMultiActionResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetNormalTriggerResponse
from pyhid.hidpp.features.keyboard.directaccessanalogkeys import SetRapidTriggerResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DirectAccessAnalogKeysTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``DirectAccessAnalogKeys`` feature
    """

    class AnalogModeChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``AnalogMode``
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
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DIRECT_ACCESS_ANALOG_KEYS
            return {
                "reserved": (cls.check_reserved, 0),
                "multi_action": (cls.check_multi_action, config.F_MultiAction),
                "rapid_trigger": (cls.check_rapid_trigger, config.F_RapidTrigger),
                "normal_trigger": (cls.check_normal_trigger, config.F_NormalTrigger)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: AnalogMode to check
            :type bitmap: ``DirectAccessAnalogKeys.AnalogMode``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_multi_action(test_case, bitmap, expected):
            """
            Check multi_action field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: AnalogMode to check
            :type bitmap: ``DirectAccessAnalogKeys.AnalogMode``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert multi_action that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The multi_action shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.multi_action),
                msg="The multi_action parameter differs from the one expected")
        # end def check_multi_action

        @staticmethod
        def check_rapid_trigger(test_case, bitmap, expected):
            """
            Check rapid_trigger field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: AnalogMode to check
            :type bitmap: ``DirectAccessAnalogKeys.AnalogMode``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert rapid_trigger that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The rapid_trigger shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.rapid_trigger),
                msg="The rapid_trigger parameter differs from the one expected")
        # end def check_rapid_trigger

        @staticmethod
        def check_normal_trigger(test_case, bitmap, expected):
            """
            Check normal_trigger field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: AnalogMode to check
            :type bitmap: ``DirectAccessAnalogKeys.AnalogMode``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert normal_trigger that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The normal_trigger shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.normal_trigger),
                msg="The normal_trigger parameter differs from the one expected")
        # end def check_normal_trigger
    # end class AnalogModeChecker

    class GetCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesResponse``
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
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.DIRECT_ACCESS_ANALOG_KEYS
            return {
                "analog_mode": (
                    cls.check_analog_mode,
                    DirectAccessAnalogKeysTestUtils.AnalogModeChecker.get_default_check_map(test_case)),
                "analog_key_number": (cls.check_analog_key_number, config.F_AnalogKeyNumber),
                "analog_resolution": (cls.check_analog_resolution, config.F_AnalogResolution)
            }
        # end def get_default_check_map

        @staticmethod
        def check_analog_mode(test_case, message, expected):
            """
            Check ``analog_mode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetCapabilitiesResponse to check
            :type message: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            DirectAccessAnalogKeysTestUtils.AnalogModeChecker.check_fields(
                test_case, message.analog_mode, DirectAccessAnalogKeys.AnalogMode, expected)
        # end def check_analog_mode

        @staticmethod
        def check_analog_key_number(test_case, response, expected):
            """
            Check analog_key_number field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert analog_key_number that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The analog_key_number shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.analog_key_number),
                msg="The analog_key_number parameter differs from the one expected")
        # end def check_analog_key_number

        @staticmethod
        def check_analog_resolution(test_case, response, expected):
            """
            Check analog_resolution field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert analog_resolution that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The analog_resolution shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.analog_resolution),
                msg="The analog_resolution parameter differs from the one expected")
        # end def check_analog_resolution
    # end class GetCapabilitiesResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=DirectAccessAnalogKeys.FEATURE_ID,
                           factory=DirectAccessAnalogKeysFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetCapabilitiesResponse (if not error)
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_3617_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_3617.get_capabilities_response_cls)
        # end def get_capabilities

        @classmethod
        def get_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_3617_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def set_analog_key_mode(cls, test_case, trigger_cidx, analog_mode, device_index=None, port_index=None,
                                software_id=None, padding=None):
            """
            Process ``SetAnalogKeyMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param analog_mode: Analog Mode
            :type analog_mode: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetAnalogKeyModeResponse (if not error)
            :rtype: ``SetAnalogKeyModeResponse``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_analog_key_mode_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                analog_mode=HexList(analog_mode))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_3617.set_analog_key_mode_response_cls)
        # end def set_analog_key_mode

        @classmethod
        def set_analog_key_mode_and_check_error(
                cls, test_case, error_codes, trigger_cidx, analog_mode, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetAnalogKeyMode``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param analog_mode: Analog Mode
            :type analog_mode: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_analog_key_mode_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                analog_mode=HexList(analog_mode))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_analog_key_mode_and_check_error

        @classmethod
        def set_normal_trigger(cls, test_case, trigger_cidx, actuation_point, hysteresis, device_index=None,
                               port_index=None, software_id=None):
            """
            Process ``SetNormalTrigger``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param actuation_point: Actuation Point
            :type actuation_point: ``int | HexList``
            :param hysteresis: Hysteresis
            :type hysteresis: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: SetNormalTriggerResponse (if not error)
            :rtype: ``SetNormalTriggerResponse``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_normal_trigger_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                actuation_point=HexList(actuation_point),
                hysteresis=HexList(hysteresis))

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_3617.set_normal_trigger_response_cls)
        # end def set_normal_trigger

        @classmethod
        def set_normal_trigger_and_check_error(
                cls, test_case, error_codes, trigger_cidx, actuation_point, hysteresis,
                function_index=None, device_index=None, port_index=None):
            """
            Process ``SetNormalTrigger``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param actuation_point: Actuation Point
            :type actuation_point: ``int | HexList``
            :param hysteresis: Hysteresis
            :type hysteresis: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_normal_trigger_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                actuation_point=HexList(actuation_point),
                hysteresis=HexList(hysteresis))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_normal_trigger_and_check_error

        @classmethod
        def set_rapid_trigger(cls, test_case, trigger_cidx, actuation_point, sensitivity, device_index=None,
                              port_index=None, software_id=None):
            """
            Process ``SetRapidTrigger``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param actuation_point: Actuation Point
            :type actuation_point: ``int | HexList``
            :param sensitivity: Sensitivity
            :type sensitivity: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: SetRapidTriggerResponse (if not error)
            :rtype: ``SetRapidTriggerResponse``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_rapid_trigger_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                actuation_point=HexList(actuation_point),
                sensitivity=HexList(sensitivity))

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_3617.set_rapid_trigger_response_cls)
        # end def set_rapid_trigger

        @classmethod
        def set_rapid_trigger_and_check_error(
                cls, test_case, error_codes, trigger_cidx, actuation_point, sensitivity,
                function_index=None, device_index=None, port_index=None):
            """
            Process ``SetRapidTrigger``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param actuation_point: Actuation Point
            :type actuation_point: ``int | HexList``
            :param sensitivity: Sensitivity
            :type sensitivity: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_rapid_trigger_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                actuation_point=HexList(actuation_point),
                sensitivity=HexList(sensitivity))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_rapid_trigger_and_check_error

        @classmethod
        def set_multi_action(cls, test_case, trigger_cidx, actuation_point_msb, actuation_point_lsb, assignment_0,
                             assignment_1, assignment_2, assignment_3, assignment_0_event_1, assignment_0_event_0,
                             assignment_0_event_3, assignment_0_event_2, assignment_1_event_1, assignment_1_event_0,
                             assignment_1_event_3, assignment_1_event_2, assignment_2_event_1, assignment_2_event_0,
                             assignment_2_event_3, assignment_2_event_2, assignment_3_event_1, assignment_3_event_0,
                             assignment_3_event_3, assignment_3_event_2, mode, hysteresis, device_index=None,
                             port_index=None, software_id=None):
            """
            Process ``SetMultiAction``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param actuation_point_msb: Actuation Point MSB
            :type actuation_point_msb: ``int | HexList``
            :param actuation_point_lsb: Actuation Point LSB
            :type actuation_point_lsb: ``int | HexList``
            :param assignment_0: Assignment 0
            :type assignment_0: ``int | HexList``
            :param assignment_1: Assignment 1
            :type assignment_1: ``int | HexList``
            :param assignment_2: Assignment 2
            :type assignment_2: ``int | HexList``
            :param assignment_3: Assignment 3
            :type assignment_3: ``int | HexList``
            :param assignment_0_event_1: Assignment 0 Event 1
            :type assignment_0_event_1: ``int | HexList``
            :param assignment_0_event_0: Assignment 0 Event 0
            :type assignment_0_event_0: ``int | HexList``
            :param assignment_0_event_3: Assignment 0 Event 3
            :type assignment_0_event_3: ``int | HexList``
            :param assignment_0_event_2: Assignment 0 Event 2
            :type assignment_0_event_2: ``int | HexList``
            :param assignment_1_event_1: Assignment 1 Event 1
            :type assignment_1_event_1: ``int | HexList``
            :param assignment_1_event_0: Assignment 1 Event 0
            :type assignment_1_event_0: ``int | HexList``
            :param assignment_1_event_3: Assignment 1 Event 3
            :type assignment_1_event_3: ``int | HexList``
            :param assignment_1_event_2: Assignment 1 Event 2
            :type assignment_1_event_2: ``int | HexList``
            :param assignment_2_event_1: Assignment 2 Event 1
            :type assignment_2_event_1: ``int | HexList``
            :param assignment_2_event_0: Assignment 2 Event 0
            :type assignment_2_event_0: ``int | HexList``
            :param assignment_2_event_3: Assignment 2 Event 3
            :type assignment_2_event_3: ``int | HexList``
            :param assignment_2_event_2: Assignment 2 Event 2
            :type assignment_2_event_2: ``int | HexList``
            :param assignment_3_event_1: Assignment 3 Event 1
            :type assignment_3_event_1: ``int | HexList``
            :param assignment_3_event_0: Assignment 3 Event 0
            :type assignment_3_event_0: ``int | HexList``
            :param assignment_3_event_3: Assignment 3 Event 3
            :type assignment_3_event_3: ``int | HexList``
            :param assignment_3_event_2: Assignment 3 Event 2
            :type assignment_3_event_2: ``int | HexList``
            :param mode: Mode
            :type mode: ``int``
            :param hysteresis: Hysteresis
            :type hysteresis: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: SetMultiActionResponse (if not error)
            :rtype: ``SetMultiActionResponse``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_multi_action_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                actuation_point_msb=HexList(actuation_point_msb),
                actuation_point_lsb=HexList(actuation_point_lsb),
                assignment_0=HexList(assignment_0),
                assignment_1=HexList(assignment_1),
                assignment_2=HexList(assignment_2),
                assignment_3=HexList(assignment_3),
                assignment_0_event_1=assignment_0_event_1,
                assignment_0_event_0=assignment_0_event_0,
                assignment_0_event_3=assignment_0_event_3,
                assignment_0_event_2=assignment_0_event_2,
                assignment_1_event_1=assignment_1_event_1,
                assignment_1_event_0=assignment_1_event_0,
                assignment_1_event_3=assignment_1_event_3,
                assignment_1_event_2=assignment_1_event_2,
                assignment_2_event_1=assignment_2_event_1,
                assignment_2_event_0=assignment_2_event_0,
                assignment_2_event_3=assignment_2_event_3,
                assignment_2_event_2=assignment_2_event_2,
                assignment_3_event_1=assignment_3_event_1,
                assignment_3_event_0=assignment_3_event_0,
                assignment_3_event_3=assignment_3_event_3,
                assignment_3_event_2=assignment_3_event_2,
                mode=mode,
                hysteresis=hysteresis)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_3617.set_multi_action_response_cls)
        # end def set_multi_action

        @classmethod
        def set_multi_action_and_check_error(
                cls, test_case, error_codes, trigger_cidx, actuation_point_msb, actuation_point_lsb,
                assignment_0, assignment_1, assignment_2, assignment_3, assignment_0_event_1, assignment_0_event_0,
                assignment_0_event_3, assignment_0_event_2, assignment_1_event_1, assignment_1_event_0,
                assignment_1_event_3, assignment_1_event_2, assignment_2_event_1, assignment_2_event_0,
                assignment_2_event_3, assignment_2_event_2, assignment_3_event_1, assignment_3_event_0,
                assignment_3_event_3, assignment_3_event_2, mode, hysteresis, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SetMultiAction``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param trigger_cidx: Trigger Cidx
            :type trigger_cidx: ``int | HexList``
            :param actuation_point_msb: Actuation Point MSB
            :type actuation_point_msb: ``int | HexList``
            :param actuation_point_lsb: Actuation Point LSB
            :type actuation_point_lsb: ``int | HexList``
            :param assignment_0: Assignment 0
            :type assignment_0: ``int | HexList``
            :param assignment_1: Assignment 1
            :type assignment_1: ``int | HexList``
            :param assignment_2: Assignment 2
            :type assignment_2: ``int | HexList``
            :param assignment_3: Assignment 3
            :type assignment_3: ``int | HexList``
            :param assignment_0_event_1: Assignment 0 Event 1
            :type assignment_0_event_1: ``int | HexList``
            :param assignment_0_event_0: Assignment 0 Event 0
            :type assignment_0_event_0: ``int | HexList``
            :param assignment_0_event_3: Assignment 0 Event 3
            :type assignment_0_event_3: ``int | HexList``
            :param assignment_0_event_2: Assignment 0 Event 2
            :type assignment_0_event_2: ``int | HexList``
            :param assignment_1_event_1: Assignment 1 Event 1
            :type assignment_1_event_1: ``int | HexList``
            :param assignment_1_event_0: Assignment 1 Event 0
            :type assignment_1_event_0: ``int | HexList``
            :param assignment_1_event_3: Assignment 1 Event 3
            :type assignment_1_event_3: ``int | HexList``
            :param assignment_1_event_2: Assignment 1 Event 2
            :type assignment_1_event_2: ``int | HexList``
            :param assignment_2_event_1: Assignment 2 Event 1
            :type assignment_2_event_1: ``int | HexList``
            :param assignment_2_event_0: Assignment 2 Event 0
            :type assignment_2_event_0: ``int | HexList``
            :param assignment_2_event_3: Assignment 2 Event 3
            :type assignment_2_event_3: ``int | HexList``
            :param assignment_2_event_2: Assignment 2 Event 2
            :type assignment_2_event_2: ``int | HexList``
            :param assignment_3_event_1: Assignment 3 Event 1
            :type assignment_3_event_1: ``int | HexList``
            :param assignment_3_event_0: Assignment 3 Event 0
            :type assignment_3_event_0: ``int | HexList``
            :param assignment_3_event_3: Assignment 3 Event 3
            :type assignment_3_event_3: ``int | HexList``
            :param assignment_3_event_2: Assignment 3 Event 2
            :type assignment_3_event_2: ``int | HexList``
            :param mode: Mode
            :type mode: ``int``
            :param hysteresis: Hysteresis
            :type hysteresis: ``int``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_3617_index, feature_3617, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_3617.set_multi_action_cls(
                device_index=device_index,
                feature_index=feature_3617_index,
                trigger_cidx=HexList(trigger_cidx),
                actuation_point_msb=HexList(actuation_point_msb),
                actuation_point_lsb=HexList(actuation_point_lsb),
                assignment_0=HexList(assignment_0),
                assignment_1=HexList(assignment_1),
                assignment_2=HexList(assignment_2),
                assignment_3=HexList(assignment_3),
                assignment_0_event_1=assignment_0_event_1,
                assignment_0_event_0=assignment_0_event_0,
                assignment_0_event_3=assignment_0_event_3,
                assignment_0_event_2=assignment_0_event_2,
                assignment_1_event_1=assignment_1_event_1,
                assignment_1_event_0=assignment_1_event_0,
                assignment_1_event_3=assignment_1_event_3,
                assignment_1_event_2=assignment_1_event_2,
                assignment_2_event_1=assignment_2_event_1,
                assignment_2_event_0=assignment_2_event_0,
                assignment_2_event_3=assignment_2_event_3,
                assignment_2_event_2=assignment_2_event_2,
                assignment_3_event_1=assignment_3_event_1,
                assignment_3_event_0=assignment_3_event_0,
                assignment_3_event_3=assignment_3_event_3,
                assignment_3_event_2=assignment_3_event_2,
                mode=mode,
                hysteresis=hysteresis)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_multi_action_and_check_error
    # end class HIDppHelper
# end class DirectAccessAnalogKeysTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
