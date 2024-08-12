#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pytestbox.device.base.keyboardinternationallayoutsutils
:brief: Helpers for ``KeyboardInternationalLayouts`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2022/12/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayouts
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayoutsFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KeyboardInternationalLayoutsTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``KeyboardInternationalLayouts`` feature
    """

    class GetKeyboardLayoutResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetKeyboardLayoutResponse``
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
            config = test_case.f.PRODUCT.FEATURES.KEYBOARD.KEYBOARD_INTERNATIONAL_LAYOUTS
            return {
                "keyboard_layout": (
                    cls.check_keyboard_layout,
                    config.F_KeyboardLayout)
            }
        # end def get_default_check_map

        @staticmethod
        def check_keyboard_layout(test_case, response, expected):
            """
            Check keyboard_layout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetKeyboardLayoutResponse to check
            :type response: ``pyhid.hidpp.features.keyboard.keyboardinternationallayouts.GetKeyboardLayoutResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert keyboard_layout that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="keyboardlayout shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.keyboard_layout),
                msg="The keyboard_layout parameter differs "
                    f"(expected:{expected}, obtained:{response.keyboard_layout})")
        # end def check_keyboard_layout
    # end class GetKeyboardLayoutResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=KeyboardInternationalLayouts.FEATURE_ID,
                           factory=KeyboardInternationalLayoutsFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_keyboard_layout(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetKeyboardLayout``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetKeyboardLayoutResponse
            :rtype: ``GetKeyboardLayoutResponse``
            """
            feature_4540_index, feature_4540, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_4540.get_keyboard_layout_cls(
                device_index=device_index,
                feature_index=feature_4540_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.KEYBOARD,
                response_class_type=feature_4540.get_keyboard_layout_response_cls)
            return response
        # end def get_keyboard_layout
    # end class HIDppHelper
# end class KeyboardInternationalLayoutsTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
