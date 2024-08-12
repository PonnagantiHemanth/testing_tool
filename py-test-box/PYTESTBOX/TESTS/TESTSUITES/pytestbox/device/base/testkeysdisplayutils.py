#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.testkeysdisplayutils
:brief: Helpers for ``TestKeysDisplay`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.peripheral.testkeysdisplay import GetCapabilitiesResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import KeyPressEvent
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetBacklightPWMDutyCycleResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayAgeingModeStateResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayPowerStateResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetDisplayRGBValueResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyCalibrationOffsetInFlashResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyCalibrationOffsetResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import SetKeyIconResponse
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplay
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplayFactory
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class TestKeysDisplayTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``TestKeysDisplay`` feature
    """

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
            config = test_case.f.PRODUCT.FEATURES.PERIPHERAL.TEST_KEYS_DISPLAY
            return {"capabilities": (cls.check_capabilities, config.F_Capabilities)}
        # end def get_default_check_map

        @staticmethod
        def check_capabilities(test_case, response, expected):
            """
            Check capabilities field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert capabilities that raise an exception
            """
            test_case.assertNotNone(expected, msg="The capabilities shall be defined in the DUT settings")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(response.capabilities),
                                  msg="The capabilities parameter differs from the one expected")
        # end def check_capabilities

    # end class GetCapabilitiesResponseChecker

    class KeyPressEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``KeyPressEvent``
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
                "btn0": (cls.check_btn0, False),
                "btn1": (cls.check_btn1, False),
                "btn2": (cls.check_btn2, False),
                "btn3": (cls.check_btn3, False),
                "btn4": (cls.check_btn4, False),
                "btn5": (cls.check_btn5, False),
                "btn6": (cls.check_btn6, False),
                "btn7": (cls.check_btn7, False),
                "btn8": (cls.check_btn8, False),
                "btn9": (cls.check_btn9, False),
                "btn10": (cls.check_btn10, False),
                "btn11": (cls.check_btn11, False),
                "btn12": (cls.check_btn12, False),
                "btn13": (cls.check_btn13, False),
                "btn14": (cls.check_btn14, False),
                "btn15": (cls.check_btn15, False)
            }
        # end def get_default_check_map

        @staticmethod
        def check_btn0(test_case, event, expected):
            """
            Check btn0 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn0 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn0 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn0),
                                  msg="The btn0 parameter differs from the one expected")
        # end def check_btn0

        @staticmethod
        def check_btn1(test_case, event, expected):
            """
            Check btn1 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn1 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn1 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn1),
                                  msg="The btn1 parameter differs from the one expected")
        # end def check_btn1

        @staticmethod
        def check_btn2(test_case, event, expected):
            """
            Check btn2 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn2 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn2 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn2),
                                  msg="The btn2 parameter differs from the one expected")
        # end def check_btn2

        @staticmethod
        def check_btn3(test_case, event, expected):
            """
            Check btn3 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn3 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn3 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn3),
                                  msg="The btn3 parameter differs from the one expected")
        # end def check_btn3

        @staticmethod
        def check_btn4(test_case, event, expected):
            """
            Check btn4 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn4 that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The btn4 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn4),
                                  msg="The btn4 parameter differs from the one expected")
        # end def check_btn4

        @staticmethod
        def check_btn5(test_case, event, expected):
            """
            Check btn5 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn5 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn5 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn5),
                                  msg="The btn5 parameter differs from the one expected")
        # end def check_btn5

        @staticmethod
        def check_btn6(test_case, event, expected):
            """
            Check btn6 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn6 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn6 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn6),
                                  msg="The btn6 parameter differs from the one expected")
        # end def check_btn6

        @staticmethod
        def check_btn7(test_case, event, expected):
            """
            Check btn7 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn7 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn7 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn7),
                                  msg="The btn7 parameter differs from the one expected")
        # end def check_btn7

        @staticmethod
        def check_btn8(test_case, event, expected):
            """
            Check btn8 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn8 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn8 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn8),
                                  msg="The btn8 parameter differs from the one expected")
        # end def check_btn8

        @staticmethod
        def check_btn9(test_case, event, expected):
            """
            Check btn9 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn9 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn9 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn9),
                                  msg="The btn9 parameter differs from the one expected")
        # end def check_btn9

        @staticmethod
        def check_btn10(test_case, event, expected):
            """
            Check btn10 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn10 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn10 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn10),
                                  msg="The btn10 parameter differs from the one expected")
        # end def check_btn10

        @staticmethod
        def check_btn11(test_case, event, expected):
            """
            Check btn11 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn11 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn11 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn11),
                                  msg="The btn11 parameter differs from the one expected")
        # end def check_btn11

        @staticmethod
        def check_btn12(test_case, event, expected):
            """
            Check btn12 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn12 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn12 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn12),
                                  msg="The btn12 parameter differs from the one expected")
        # end def check_btn12

        @staticmethod
        def check_btn13(test_case, event, expected):
            """
            Check btn13 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn13 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn13 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn13),
                                  msg="The btn13 parameter differs from the one expected")
        # end def check_btn13

        @staticmethod
        def check_btn14(test_case, event, expected):
            """
            Check btn14 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn14 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn14 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn14),
                                  msg="The btn14 parameter differs from the one expected")
        # end def check_btn14

        @staticmethod
        def check_btn15(test_case, event, expected):
            """
            Check btn15 field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: KeyPressEvent to check
            :type event: ``KeyPressEvent``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert btn15 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The btn15 shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(event.btn15),
                                  msg="The btn15 parameter differs from the one expected")
        # end def check_btn15
    # end class KeyPressEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=TestKeysDisplay.FEATURE_ID, factory=TestKeysDisplayFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(test_case, feature_id, factory, device_index, port_index, update_test_case,
                                          skip_not_found)
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

            :return: GetCapabilitiesResponse
            :rtype: ``GetCapabilitiesResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_92e2_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.get_capabilities_response_cls)
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
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_92e2_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def set_backlight_pwm_duty_cycle(cls, test_case, duty_pwm, device_index=None, port_index=None,
                                         software_id=None, padding=None):
            """
            Process ``SetBacklightPWMDutyCycle``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param duty_pwm: Duty PWM
            :type duty_pwm: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetBacklightPWMDutyCycleResponse
            :rtype: ``SetBacklightPWMDutyCycleResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_backlight_pwm_duty_cycle_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                duty_pwm=HexList(duty_pwm))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_backlight_pwm_duty_cycle_response_cls)
        # end def set_backlight_pwm_duty_cycle

        @classmethod
        def set_backlight_pwm_duty_cycle_and_check_error(cls, test_case, error_codes, duty_pwm, function_index=None, 
                                                         device_index=None, port_index=None):
            """
            Process ``SetBacklightPWMDutyCycle``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param duty_pwm: Duty PWM
            :type duty_pwm: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_backlight_pwm_duty_cycle_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                duty_pwm=HexList(duty_pwm))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_backlight_pwm_duty_cycle_and_check_error

        @classmethod
        def set_display_rgb_value(cls, test_case, rgb_value, device_index=None, port_index=None, software_id=None):
            """
            Process ``SetDisplayRGBValue``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param rgb_value: RGB Value
            :type rgb_value: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: SetDisplayRGBValueResponse
            :rtype: ``SetDisplayRGBValueResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_display_rgb_value_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                rgb_value=HexList(rgb_value))

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_display_rgb_value_response_cls)
        # end def set_display_rgb_value

        @classmethod
        def set_display_rgb_value_and_check_error(
                cls, test_case, error_codes, rgb_value, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SetDisplayRGBValue``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param rgb_value: RGB Value
            :type rgb_value: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_display_rgb_value_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                rgb_value=HexList(rgb_value))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_display_rgb_value_and_check_error

        @classmethod
        def set_display_power_state(cls, test_case, power_state, device_index=None, port_index=None, software_id=None,
                                    padding=None):
            """
            Process ``SetDisplayPowerState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param power_state: Power State
            :type power_state: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetDisplayPowerStateResponse
            :rtype: ``SetDisplayPowerStateResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_display_power_state_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                power_state=HexList(power_state))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_display_power_state_response_cls)
        # end def set_display_power_state

        @classmethod
        def set_display_power_state_and_check_error(
                cls, test_case, error_codes, power_state, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SetDisplayPowerState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param power_state: Power State
            :type power_state: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_display_power_state_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                power_state=HexList(power_state))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_display_power_state_and_check_error

        @classmethod
        def set_key_icon(cls, test_case, key_column, key_row, icon_index, device_index=None, port_index=None,
                         software_id=None):
            """
            Process ``SetKeyIcon``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param key_column: Key Column
            :type key_column: ``int | HexList``
            :param key_row: Key Row
            :type key_row: ``int | HexList``
            :param icon_index: Icon Index
            :type icon_index: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: SetKeyIconResponse
            :rtype: ``SetKeyIconResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_key_icon_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                key_column=HexList(key_column),
                key_row=HexList(key_row),
                icon_index=HexList(icon_index))

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_key_icon_response_cls)
        # end def set_key_icon

        @classmethod
        def set_key_icon_and_check_error(
                cls, test_case, error_codes, key_column, key_row, icon_index, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetKeyIcon``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param key_column: Key Column
            :type key_column: ``int | HexList``
            :param key_row: Key Row
            :type key_row: ``int | HexList``
            :param icon_index: Icon Index
            :type icon_index: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_key_icon_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                key_column=HexList(key_column),
                key_row=HexList(key_row),
                icon_index=HexList(icon_index))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_key_icon_and_check_error

        @classmethod
        def set_key_calibration_offset(cls, test_case, key_column, key_row, x_offset, y_offset, device_index=None,
                                       port_index=None, software_id=None, padding=None):
            """
            Process ``SetKeyCalibrationOffset``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param key_column: Key Column
            :type key_column: ``int | HexList``
            :param key_row: Key Row
            :type key_row: ``int | HexList``
            :param x_offset: X Offset
            :type x_offset: ``int | HexList``
            :param y_offset: Y Offset
            :type y_offset: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetKeyCalibrationOffsetResponse
            :rtype: ``SetKeyCalibrationOffsetResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_key_calibration_offset_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                key_column=HexList(key_column),
                key_row=HexList(key_row),
                x_offset=HexList(x_offset),
                y_offset=HexList(y_offset))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_key_calibration_offset_response_cls)
        # end def set_key_calibration_offset

        @classmethod
        def set_key_calibration_offset_and_check_error(cls, test_case, error_codes, key_column, key_row,
                                                       x_offset, y_offset, function_index=None, device_index=None,
                                                       port_index=None):
            """
            Process ``SetKeyCalibrationOffset``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param key_column: Key Column
            :type key_column: ``int | HexList``
            :param key_row: Key Row
            :type key_row: ``int | HexList``
            :param x_offset: X Offset
            :type x_offset: ``int | HexList``
            :param y_offset: Y Offset
            :type y_offset: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_key_calibration_offset_cls(
                device_index=device_index,
                feature_index=feature_92e2_index,
                key_column=HexList(key_column),
                key_row=HexList(key_row),
                x_offset=HexList(x_offset),
                y_offset=HexList(y_offset))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_key_calibration_offset_and_check_error

        @classmethod
        def set_key_calibration_offset_in_flash(cls, test_case, device_index=None, port_index=None, software_id=None,
                                                padding=None):
            """
            Process ``SetKeyCalibrationOffsetInFlash``

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

            :return: SetKeyCalibrationOffsetInFlashResponse
            :rtype: ``SetKeyCalibrationOffsetInFlashResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_key_calibration_offset_in_flash_cls(
                device_index=device_index,
                feature_index=feature_92e2_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_key_calibration_offset_in_flash_response_cls)
        # end def set_key_calibration_offset_in_flash

        @classmethod
        def set_key_calibration_offset_in_flash_and_check_error(cls, test_case, error_codes, function_index=None,
                                                                device_index=None, port_index=None):
            """
            Process ``SetKeyCalibrationOffsetInFlash``

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
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_key_calibration_offset_in_flash_cls(
                device_index=device_index,
                feature_index=feature_92e2_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_key_calibration_offset_in_flash_and_check_error

        @classmethod
        def set_display_ageing_mode_state(cls, test_case, device_index=None, port_index=None, software_id=None,
                                          padding=None):
            """
            Process ``SetDisplayAgeingModeState``

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

            :return: SetDisplayAgeingModeStateResponse
            :rtype: ``SetDisplayAgeingModeStateResponse``
            """
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_display_ageing_mode_state_cls(
                device_index=device_index,
                feature_index=feature_92e2_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_92e2.set_display_ageing_mode_state_response_cls)
        # end def set_display_ageing_mode_state

        @classmethod
        def set_display_ageing_mode_state_and_check_error(cls, test_case, error_codes, function_index=None,
                                                          device_index=None, port_index=None):
            """
            Process ``SetDisplayAgeingModeState``

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
            feature_92e2_index, feature_92e2, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_92e2.set_display_ageing_mode_state_cls(
                device_index=device_index,
                feature_index=feature_92e2_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_display_ageing_mode_state_and_check_error

        @classmethod
        def key_press_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                            check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``KeyPressEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: KeyPressEvent
            :rtype: ``KeyPressEvent``
            """
            _, feature_92e2, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_92e2.key_press_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def key_press_event
    # end class HIDppHelper

    @classmethod
    def create_key_matrix(cls, test_case):
        """
        Create a key matrix based on the row and column count from the product config

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: The product specific key matrix
        :rtype: ``list[list[KEY_ID]]``
        """
        config = test_case.f.PRODUCT.FEATURES.PERIPHERAL.TEST_KEYS_DISPLAY
        key_matrix = []
        row_count = config.F_RowCount
        col_count = config.F_ColumnCount
        keys = iter([KEY_ID.BUTTON_1, KEY_ID.BUTTON_2, KEY_ID.BUTTON_3, KEY_ID.BUTTON_4, KEY_ID.BUTTON_5,
                     KEY_ID.BUTTON_6, KEY_ID.BUTTON_7, KEY_ID.BUTTON_8, KEY_ID.BUTTON_9, KEY_ID.BUTTON_10,
                     KEY_ID.BUTTON_11, KEY_ID.BUTTON_12, KEY_ID.BUTTON_13, KEY_ID.BUTTON_14, KEY_ID.BUTTON_15,
                     KEY_ID.BUTTON_16])
        for row in range(row_count):
            key_matrix.append([])
            for _ in range(col_count):
                key_matrix[row].append(next(keys))
            # end for
        # end for

        return key_matrix
    # end def create_key_matrix
# end class TestKeysDisplayTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
