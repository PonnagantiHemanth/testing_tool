#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.smartshifttunableutils
:brief:  Helpers for Smart Shift Tunable feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/10
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunable
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunableFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunableTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on smart shift tunable feature
    """
    class GetCapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check getCapabilities response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected value
            :rtype: ``dict``
            """
            feature_config = test_case.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE
            return {
                "capabilities_reserved": (cls.check_capabilities_reserved, 0),
                "tunable_torque": (cls.check_tunable_torque, feature_config.F_TunableTorque),
                "auto_disengage_default": (cls.check_auto_disengage_default, feature_config.F_AutoDisengageDefault),
                "default_tunable_torque": (cls.check_default_tunable_torque, feature_config.F_DefaultTunableTorque),
                "max_force": (cls.check_max_force, feature_config.F_MaxForce),
            }
        # end def get_default_check_map

        @staticmethod
        def check_capabilities_reserved(test_case, get_capabilities_response, expected):
            """
            Check the capabilities field reserved bits

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_capabilities_response: Response object
            :type get_capabilities_response: ``GetCapabilitiesResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=get_capabilities_response.capabilities_reserved,
                                  expected=expected,
                                  msg='All capabilities reserved bits should be 0 (Reserved for future use)')
        # end def check_capabilities_reserved

        @staticmethod
        def check_tunable_torque(test_case, get_capabilities_response, expected):
            """
            Check tunable torque field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_capabilities_response: Response object
            :type get_capabilities_response: ``GetCapabilitiesResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=int(Numeral(get_capabilities_response.tunable_torque)),
                                  expected=int(expected),
                                  msg='The tunable torque capability parameter should be as expected')
        # end def check_tunable_torque

        @staticmethod
        def check_auto_disengage_default(test_case, get_capabilities_response, expected):
            """
            Check auto disengage default field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_capabilities_response: Response object
            :type get_capabilities_response: ``GetCapabilitiesResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=HexList(get_capabilities_response.auto_disengage_default),
                                  expected=HexList(expected),
                                  msg='The auto disengage default parameter should be as expected')
        # end def check_auto_disengage_default

        @staticmethod
        def check_default_tunable_torque(test_case, get_capabilities_response, expected):
            """
            Check default tunable torque field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_capabilities_response: Response object
            :type get_capabilities_response: ``GetCapabilitiesResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=HexList(get_capabilities_response.default_tunable_torque),
                                  expected=HexList(expected),
                                  msg='The default tunable torque parameter should be as expected')
        # end def check_default_tunable_torque

        @staticmethod
        def check_max_force(test_case, get_capabilities_response, expected):
            """
            Check max force field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_capabilities_response: Response object
            :type get_capabilities_response: ``GetCapabilitiesResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=HexList(get_capabilities_response.max_force),
                                  expected=HexList(expected),
                                  msg='The max force parameter should be as expected')
        # end def check_max_force
    # end class GetCapabilitiesChecker

    class RatchetControlModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Help class to check get/set ratchet control mode response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get map to check default parameters values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Mapping between fields and check method with expected values
            :rtype: ``dict``
            """
            feature_config = test_case.f.PRODUCT.FEATURES.MOUSE.SMART_SHIFT_TUNABLE
            return {
                "wheel_mode": (cls.check_wheel_mode, feature_config.F_WheelModeDefault),
                "auto_disengage": (cls.check_auto_disengage, feature_config.F_AutoDisengageDefault),
                "current_tunable_torque": (cls.check_current_tunable_torque, feature_config.F_DefaultTunableTorque),
            }
        # end def get_default_check_map

        @classmethod
        def get_range_check_map(cls):
            """
            Get map to check range values

            :return: Mapping between fields and check method with expected range
            :rtype: ``dict``
            """
            return {
                "wheel_mode": (cls.check_wheel_mode_range, (SmartShiftTunable.WheelModeConst.FREESPIN,
                                                            SmartShiftTunable.WheelModeConst.RATCHET)),
                "auto_disengage": (cls.check_auto_disengage_range, SmartShiftTunable.AutoDisengageConst.RANGE),
                "current_tunable_torque": (cls.check_current_tunable_torque_range,
                                           SmartShiftTunable.TunableTorqueConst.RANGE),
            }
        # end def get_range_check_map

        @classmethod
        def check_wheel_mode(cls, test_case, get_ratchet_control_mode_response, expected):
            """
            Check wheel mode field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_ratchet_control_mode_response: Response object
            :type get_ratchet_control_mode_response: ``GetRatchetControlModeResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            cls.check_wheel_mode_value(test_case, get_ratchet_control_mode_response.wheel_mode, expected)
        # end def check_wheel_mode

        @classmethod
        def check_wheel_mode_value(cls, test_case, value, expected):
            """
            Check wheel mode value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param value: Current value
            :type value: ``int``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=HexList(value), expected=HexList(expected),
                                  msg='The wheel mode parameter should be as expected')
        # end def check_wheel_mode_value

        @classmethod
        def check_auto_disengage(cls, test_case, get_ratchet_control_mode_response, expected):
            """
            Check auto disengage field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_ratchet_control_mode_response: Response object
            :type get_ratchet_control_mode_response: ``GetRatchetControlModeResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            cls.check_auto_disengage_value(test_case, get_ratchet_control_mode_response.auto_disengage, expected)
        # end def check_auto_disengage

        @classmethod
        def check_auto_disengage_value(cls, test_case, value, expected):
            """
            Check auto disengage value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param value: Current value
            :type value: ``int``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=HexList(value), expected=HexList(expected),
                                  msg='The auto disengage parameter should be as expected')

        # end def check_auto_disengage_value

        @classmethod
        def check_current_tunable_torque(cls, test_case, get_ratchet_control_mode_response, expected):
            """
            Check current tunable torque field

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_ratchet_control_mode_response: Response object
            :type get_ratchet_control_mode_response: ``GetRatchetControlModeResponseV0``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            cls.check_current_tunable_torque_value(
                test_case, get_ratchet_control_mode_response.current_tunable_torque, expected)
        # end def check_current_tunable_torque

        @staticmethod
        def check_current_tunable_torque_value(test_case, value, expected):
            """
            Check current tunable torque value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param value: Current value
            :type value: ``int``
            :param expected: Expected value
            :type expected: ``int``

            :raise ``TestException``: If check fails
            """
            test_case.assertEqual(obtained=HexList(value), expected=HexList(expected),
                                  msg='The current tunable torque parameter should be as expected')
        # end def check_current_tunable_torque_value

        @staticmethod
        def check_wheel_mode_range(test_case, get_ratchet_control_mode_response, expected):
            """
            Check wheel mode range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_ratchet_control_mode_response: Response object
            :type get_ratchet_control_mode_response: ``GetRatchetControlModeResponseV0``
            :param expected: Expected range
            :type expected: ``tuple``

            :raise ``TestException``: If check fails
            """
            test_case.assertTrue(
                expr=(expected[0] <= int(Numeral(get_ratchet_control_mode_response.wheel_mode)) <= expected[1]),
                msg='Wheel mode should be in valid range')
        # end def check_wheel_mode_range

        @staticmethod
        def check_auto_disengage_range(test_case, get_ratchet_control_mode_response, expected):
            """
            Check auto disengage range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_ratchet_control_mode_response: Response object
            :type get_ratchet_control_mode_response: ``GetRatchetControlModeResponseV0``
            :param expected: Expected range
            :type expected: ``tuple``

            :raise ``TestException``: If check fails
            """
            test_case.assertTrue(
                expr=(expected[0] <= int(Numeral(get_ratchet_control_mode_response.auto_disengage)) <= expected[1]),
                msg='Auto disengage should be in valid range')
        # end def check_auto_disengage_range

        @staticmethod
        def check_current_tunable_torque_range(test_case, get_ratchet_control_mode_response, expected):
            """
            Check current tunable torque range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param get_ratchet_control_mode_response: Response object
            :type get_ratchet_control_mode_response: ``GetRatchetControlModeResponseV0``
            :param expected: Expected range
            :type expected: ``tuple``

            :raise ``TestException``: If check fails
            """
            current_tunable_torque = int(Numeral(get_ratchet_control_mode_response.current_tunable_torque))
            test_case.assertTrue(expr=expected[0] <= current_tunable_torque <= expected[1],
                                 msg='Current tunable torque should be in valid range')
        # end def check_current_tunable_torque_range
    # end class RatchetControlModeResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def set_control_mode_configuration(cls, test_case, wheel_mode=None, auto_disengage=None,
                                           current_tunable_torque=None, device_index=None, port_index=None):
            """
            Send set ratchet control mode request, check the changed parameters in the response and return the response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param wheel_mode: Wheel mode to set - OPTIONAL
            :type wheel_mode: ``int``
            :param auto_disengage: Auto disengage value to set - OPTIONAL
            :type auto_disengage: ``int``
            :param current_tunable_torque: Current tunable torque value to set - OPTIONAL
            :type current_tunable_torque: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Set ratchet control mode response
            :rtype: ``SetRatchetControlModeResponseV0``
            """
            feature_2111_index, feature_2111, device_index, port_index = cls.get_parameters(
                test_case, SmartShiftTunable.FEATURE_ID, SmartShiftTunableFactory, device_index, port_index)

            wheel_mode = SmartShiftTunable.WheelModeConst.DO_NOT_CHANGE if wheel_mode is None else wheel_mode
            auto_disengage = SmartShiftTunable.AutoDisengageConst.DO_NOT_CHANGE if \
                auto_disengage is None else auto_disengage
            current_tunable_torque = SmartShiftTunable.TunableTorqueConst.DO_NOT_CHANGE if \
                current_tunable_torque is None else current_tunable_torque

            set_ratchet_control_mode = feature_2111.set_ratchet_control_mode_cls(device_index,
                                                                                 feature_2111_index,
                                                                                 wheel_mode,
                                                                                 auto_disengage,
                                                                                 current_tunable_torque)

            set_ratchet_control_mode_response = test_case.send_report_wait_response(
                report=set_ratchet_control_mode,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2111.set_ratchet_control_mode_response_cls)

            if wheel_mode != SmartShiftTunable.WheelModeConst.DO_NOT_CHANGE:
                SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_wheel_mode(
                    test_case, set_ratchet_control_mode_response, wheel_mode)
            # end if

            if auto_disengage != SmartShiftTunable.AutoDisengageConst.DO_NOT_CHANGE:
                SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_auto_disengage(
                    test_case, set_ratchet_control_mode_response, auto_disengage)
            # end if

            if current_tunable_torque != SmartShiftTunable.TunableTorqueConst.DO_NOT_CHANGE:
                SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_current_tunable_torque(
                    test_case, set_ratchet_control_mode_response, current_tunable_torque)
            # end if

            return set_ratchet_control_mode_response
        # end def set_control_mode_configuration

        @classmethod
        def set_wheel_mode(cls, test_case, wheel_mode, device_index=None, port_index=None):
            """
            Set wheel mode

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param wheel_mode: Wheel mode
            :type wheel_mode: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Set ratchet control mode response
            :rtype: ``SetRatchetControlModeResponseV0``
            """
            return cls.set_control_mode_configuration(
                test_case, wheel_mode=wheel_mode, device_index=device_index, port_index=port_index)
        # end def set_wheel_mode

        @classmethod
        def set_wheel_mode_ratchet(cls, test_case, device_index=None, port_index=None):
            """
            Set wheel mode to ratchet mode

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Set ratchet control mode response
            :rtype: ``SetRatchetControlModeResponseV0``
            """
            return cls.set_wheel_mode(test_case, SmartShiftTunable.WheelModeConst.RATCHET, device_index, port_index)
        # end def set_wheel_mode_ratchet

        @classmethod
        def set_wheel_mode_freespin(cls, test_case, device_index=None, port_index=None):
            """
            Set wheel mode to freespin mode

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Set ratchet control mode response
            :rtype: ``SetRatchetControlModeResponseV0``
            """
            return cls.set_wheel_mode(test_case, SmartShiftTunable.WheelModeConst.FREESPIN, device_index, port_index)
        # end def set_wheel_mode_freespin

        @classmethod
        def get_ratchet_control_mode_response(cls, test_case, device_index=None, port_index=None):
            """
            Send get ratchet control mode and get response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Get ratchet control mode response
            :rtype: ``GetRatchetControlModeResponseV0``
            """
            feature_2111_index, feature_2111, device_index, port_index = cls.get_parameters(
                test_case, SmartShiftTunable.FEATURE_ID, SmartShiftTunableFactory, device_index, port_index)

            get_ratchet_control_mode = feature_2111.get_ratchet_control_mode_cls(device_index, feature_2111_index)

            return test_case.send_report_wait_response(
                report=get_ratchet_control_mode,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2111.get_ratchet_control_mode_response_cls)
        # end def get_ratchet_control_mode_response

        @classmethod
        def get_wheel_mode(cls, test_case, device_index=None, port_index=None):
            """
            Get wheel mode

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Current wheel mode
            :rtype: ``int``
            """
            return cls.get_ratchet_control_mode_response(test_case, device_index, port_index).wheel_mode
        # end def get_wheel_mode

        @classmethod
        def get_and_check_wheel_mode(cls, test_case, expected, device_index=None, port_index=None):
            """
            Get and check wheel mode

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param expected: Expected value
            :type expected: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :raise ``TestException``: If check fails
            """
            SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_wheel_mode_value(
                test_case, cls.get_wheel_mode(test_case, device_index, port_index), expected)
        # end def get_and_check_wheel_mode

        @classmethod
        def set_auto_disengage(cls, test_case, value, device_index=None, port_index=None):
            """
            Set auto disengage

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param value: Value to set
            :type value: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Response to set request
            :rtype: ``SetRatchetControlModeResponseV0``
            """
            return cls.set_control_mode_configuration(
                test_case, auto_disengage=value, device_index=device_index, port_index=port_index)
        # end def set_auto_disengage

        @classmethod
        def get_auto_disengage(cls, test_case, device_index=None, port_index=None):
            """
            Get auto disengage

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Auto disengage value
            :rtype: ``int``
            """
            return cls.get_ratchet_control_mode_response(test_case, device_index, port_index).auto_disengage
        # end def get_auto_disengage

        @classmethod
        def get_and_check_auto_disengage(cls, test_case, expected, device_index=None, port_index=None):
            """
            Get and check auto disengage

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param expected: Expected value
            :type expected: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :raise ``TestException``: If check fails
            """
            SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_auto_disengage_value(
                test_case, cls.get_auto_disengage(test_case, device_index, port_index), expected)
        # end def get_and_check_auto_disengage

        @classmethod
        def set_current_tunable_torque(cls, test_case, value, device_index=None, port_index=None):
            """
            Set current tunable torque

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param value: Value to set
            :type value: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Response to the set request
            :rtype: ``SetRatchetControlModeResponseV0``
            """
            return cls.set_control_mode_configuration(
                test_case, current_tunable_torque=value, device_index=device_index, port_index=port_index)
        # end def set_current_tunable_torque

        @classmethod
        def get_current_tunable_torque(cls, test_case, device_index=None, port_index=None):
            """
            Get current tunable torque

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: Current tunable torque
            :rtype: ``int``
            """
            return cls.get_ratchet_control_mode_response(test_case, device_index, port_index).current_tunable_torque
        # end def get_current_tunable_torque

        @classmethod
        def get_and_check_current_tunable_torque(cls, test_case, expected, device_index=None, port_index=None):
            """
            Get current tunable torque and check the value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param expected: Expected value
            :type expected: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :raise ``TestException``: If check fails
            """
            SmartShiftTunableTestUtils.RatchetControlModeResponseChecker.check_current_tunable_torque_value(
                test_case, cls.get_current_tunable_torque(test_case, device_index, port_index), expected)
        # end def get_and_check_current_tunable_torque
    # end class HIDppHelper
# end class SmartShiftTunableTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
