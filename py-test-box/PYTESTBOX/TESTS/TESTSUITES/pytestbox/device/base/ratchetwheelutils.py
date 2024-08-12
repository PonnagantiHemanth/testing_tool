#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.ratchetwheelutils
:brief: Helpers for ``RatchetWheel`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/11/30
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheel
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheelFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RatchetWheelTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``RatchetWheel`` feature
    """

    class FlagChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``Flag``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case=test_case)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, divert=0):
            """
            Get check map for different values of divert parameter

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param divert: Divert bit's value - OPTIONAL
            :type divert: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reserved": (
                    cls.check_reserved,
                    0),
                "divert": (
                    cls.check_divert,
                    divert)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Flag to check
            :type bitmap: ``RatchetWheel.Flag``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_divert(test_case, bitmap, expected):
            """
            Check divert field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: Flag to check
            :type bitmap: ``RatchetWheel.Flag``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert divert that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Divert shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.divert),
                msg="The divert parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.divert})")
        # end def check_divert
    # end class FlagChecker

    class GetWheelModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetWheelModeResponse``
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
            return cls.get_check_map(test_case=test_case)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, divert=0):
            """
            Get check map for different values of diver parameter

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param divert: Divert bit's value - OPTIONAL
            :type divert: ``int``
            """
            return {
                "flag": (
                    cls.check_flag,
                    RatchetWheelTestUtils.FlagChecker.get_check_map(test_case, divert=divert))
            }
        # end def get_check_map

        @staticmethod
        def check_flag(test_case, message, expected):
            """
            Check ``flag``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetWheelModeResponse to check
            :type message: ``pyhid.hidpp.features.mouse.ratchetwheel.GetWheelModeResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            RatchetWheelTestUtils.FlagChecker.check_fields(
                test_case, message.flag, RatchetWheel.Flag, expected)
        # end def check_flag
    # end class GetWheelModeResponseChecker

    class SetModeStatusResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetModeStatusResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case=test_case)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, divert=0):
            """
            Get check map for different values of divert

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param divert: Divert bit's value - OPTIONAL
            :type divert: ``int``

            :return: Check map
            :rtype: ``dict``
            """

            return {
                "flag": (
                    cls.check_flag,
                    RatchetWheelTestUtils.FlagChecker.get_check_map(test_case, divert=divert))
            }
        # end def get_check_map

        @staticmethod
        def check_flag(test_case, message, expected):
            """
            Check ``flag``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: SetModeStatusResponse to check
            :type message: ``pyhid.hidpp.features.mouse.ratchetwheel.SetModeStatusResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            RatchetWheelTestUtils.FlagChecker.check_fields(
                test_case, message.flag, RatchetWheel.Flag, expected)
        # end def check_flag
    # end class SetModeStatusResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=RatchetWheel.FEATURE_ID, factory=RatchetWheelFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_wheel_mode(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetWheelMode``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetWheelModeResponse
            :rtype: ``GetWheelModeResponse``
            """
            feature_2130_index, feature_2130, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2130.get_wheel_mode_cls(
                device_index=device_index,
                feature_index=feature_2130_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2130.get_wheel_mode_response_cls)
            return response
        # end def get_wheel_mode

        @classmethod
        def set_mode_status(cls, test_case, divert, device_index=None, port_index=None):
            """
            Process ``SetModeStatus``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param divert: Divert bit's value
            :type divert: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetModeStatusResponse
            :rtype: ``SetModeStatusResponse``
            """
            feature_2130_index, feature_2130, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_2130.set_mode_status_cls(
                device_index=device_index,
                feature_index=feature_2130_index,
                divert=divert)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.MOUSE,
                response_class_type=feature_2130.set_mode_status_response_cls)
            return response
        # end def set_mode_status

        @classmethod
        def wheel_movement_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                 check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``WheelMovementEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: WheelMovementEvent
            :rtype: ``WheelMovementEvent``
            """
            _, feature_2130, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_2130.wheel_movement_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def wheel_movement_event
    # end class HIDppHelper
# end class RatchetWheelTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
