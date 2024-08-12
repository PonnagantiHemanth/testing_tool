#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.lockkeystateutils
:brief: Helpers for ``LockKeyState`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2022/03/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyState
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyStateFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LockKeyStateTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``LockKeyState`` feature
    """

    class LockKeyStateMaskBitMapChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``LockKeyStateMaskBitMap``
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
                "reserved": (cls.check_reserved, 0),
                "kana": (cls.check_kana, 0),
                "compose": (cls.check_compose, 0),
                "scroll_lock": (cls.check_scroll_lock, 0),
                "caps_lock": (cls.check_caps_lock, 0),
                "num_lock": (cls.check_num_lock, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: LockKeyStateMaskBitMap to check
            :type bitmap: ``LockKeyStateMaskBitMap``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg=f"The reserved parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.reserved})")
        # end def check_reserved

        @staticmethod
        def check_kana(test_case, bitmap, expected):
            """
            Check kana field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: LockKeyStateMaskBitMap to check
            :type bitmap: ``LockKeyStateMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Kana shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.kana),
                msg=f"The kana parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.kana})")
        # end def check_kana

        @staticmethod
        def check_compose(test_case, bitmap, expected):
            """
            Check compose field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: LockKeyStateMaskBitMap to check
            :type bitmap: ``LockKeyStateMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="Compose shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.compose),
                msg=f"The compose parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.compose})")
        # end def check_compose

        @staticmethod
        def check_scroll_lock(test_case, bitmap, expected):
            """
            Check scroll_lock field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: LockKeyStateMaskBitMap to check
            :type bitmap: ``LockKeyStateMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="ScrollLock shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.scroll_lock),
                msg=f"The scroll_lock parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.scroll_lock})")
        # end def check_scroll_lock

        @staticmethod
        def check_caps_lock(test_case, bitmap, expected):
            """
            Check caps_lock field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: LockKeyStateMaskBitMap to check
            :type bitmap: ``LockKeyStateMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="CapsLock shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.caps_lock),
                msg=f"The caps_lock parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.caps_lock})")
        # end def check_caps_lock

        @staticmethod
        def check_num_lock(test_case, bitmap, expected):
            """
            Check num_lock field in bitmap

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param bitmap: LockKeyStateMaskBitMap to check
            :type bitmap: ``LockKeyStateMaskBitMap``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertNotNone(
                expected, msg="NumLock shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.num_lock),
                msg=f"The num_lock parameter differs "
                    f"(expected:{expected}, obtained:{bitmap.num_lock})")
        # end def check_num_lock
    # end class LockKeyStateMaskBitMapChecker

    class GetLockKeyStateResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetLockKeyStateResponse``
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
                "lock_key_state_mask_bit_map": (
                    cls.check_lock_key_state_mask_bit_map,
                    LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_lock_key_state_mask_bit_map(test_case, message, expected):
            """
            Check ``lock_key_state_mask_bit_map``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param message: GetLockKeyStateResponse to check
            :type message: ``GetLockKeyStateResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            LockKeyStateTestUtils.LockKeyStateMaskBitMapChecker.check_fields(
                test_case, message.lock_key_state_mask_bit_map, LockKeyState.LockKeyStateMaskBitMap, expected)
        # end def check_lock_key_state_mask_bit_map
    # end class GetLockKeyStateResponseChecker

    class LockKeyChangeEventChecker(GetLockKeyStateResponseChecker):
        """
        Define Helper to check ``LockKeyChangeEvent``
        """
        pass
    # end class LockKeyChangeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=LockKeyState.FEATURE_ID, factory=LockKeyStateFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_lock_key_state(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetLockKeyState``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetLockKeyStateResponse
            :rtype: ``GetLockKeyStateResponse``
            """
            feature_4220_index, feature_4220, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4220.get_lock_key_state_cls(
                device_index=device_index,
                feature_index=feature_4220_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4220.get_lock_key_state_response_cls)
            return response
        # end def get_lock_key_state

        @classmethod
        def lock_key_change_event(cls, test_case, timeout=2,
                                  check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``LockKeyChangeEvent``: get notification from event queue

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

            :return: LockKeyChangeEvent
            :rtype: ``LockKeyChangeEvent``
            """
            _, feature_4220, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_4220.lock_key_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def lock_key_change_event
    # end class HIDppHelper
# end class LockKeyStateTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
