#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.forcesensingbuttonutils
:brief: Helpers for ``ForceSensingButton`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2024/08/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.forcesensingbutton import ForceSensingButton
from pyhid.hidpp.features.common.forcesensingbutton import ForceSensingButtonFactory
from pyhid.hidpp.features.common.forcesensingbutton import GetButtonCapabilitiesResponse
from pyhid.hidpp.features.common.forcesensingbutton import GetButtonConfigResponse
from pyhid.hidpp.features.common.forcesensingbutton import GetCapabilitiesResponse
from pyhid.hidpp.features.common.forcesensingbutton import SetButtonConfigResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ForceSensingButtonTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``ForceSensingButton`` feature
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FORCE_SENSING_BUTTON
            return {
                "number_of_buttons": (cls.check_number_of_buttons, config.F_NumberOfButtons)
            }
        # end def get_default_check_map

        @staticmethod
        def check_number_of_buttons(test_case, response, expected):
            """
            Check number_of_buttons field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCapabilitiesResponse to check
            :type response: ``GetCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert number_of_buttons that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The number_of_buttons shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.number_of_buttons),
                msg="The number_of_buttons parameter differs from the one expected")
        # end def check_number_of_buttons
    # end class GetCapabilitiesResponseChecker

    class ButtonCapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ButtonCapabilities``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FORCE_SENSING_BUTTON
            return {
                "customizable_force": (cls.check_customizable_force, config.F_CustomizableForce),
                "reserved": (cls.check_reserved, 0),
                "default_force": (cls.check_default_force, config.F_DefaultForce),
                "max_force": (cls.check_max_force, config.F_MaxForce if config.F_CustomizableForce else 0),
                "min_force": (cls.check_min_force, config.F_MinForce if config.F_CustomizableForce else 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_customizable_force(test_case, bitmap, expected):
            """
            Check customizable_force field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonCapabilities to check
            :type bitmap: ``ForceSensingButton.ButtonCapabilities``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert customizable_force that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The customizable_force shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.customizable_force),
                msg="The customizable_force parameter differs from the one expected")
        # end def check_customizable_force

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonCapabilities to check
            :type bitmap: ``ForceSensingButton.ButtonCapabilities``
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
        def check_default_force(test_case, bitmap, expected):
            """
            Check default_force field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonCapabilities to check
            :type bitmap: ``ForceSensingButton.ButtonCapabilities``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert default_force that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The default_force shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.default_force),
                msg="The default_force parameter differs from the one expected")
        # end def check_default_force

        @staticmethod
        def check_max_force(test_case, bitmap, expected):
            """
            Check max_force field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonCapabilities to check
            :type bitmap: ``ForceSensingButton.ButtonCapabilities``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_force that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The max_force shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.max_force),
                msg="The max_force parameter differs from the one expected")
        # end def check_max_force

        @staticmethod
        def check_min_force(test_case, bitmap, expected):
            """
            Check min_force field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: ButtonCapabilities to check
            :type bitmap: ``ForceSensingButton.ButtonCapabilities``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_force that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The min_force shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(bitmap.min_force),
                msg="The min_force parameter differs from the one expected")
        # end def check_min_force
    # end class ButtonCapabilitiesChecker

    class GetButtonCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetButtonCapabilitiesResponse``
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
                "buttoncapabilities": (
                    cls.check_buttoncapabilities,
                    ForceSensingButtonTestUtils.ButtonCapabilitiesChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_buttoncapabilities(test_case, message, expected):
            """
            Check ``buttoncapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetButtonCapabilitiesResponse to check
            :type message: ``GetButtonCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``dict``
            """
            ForceSensingButtonTestUtils.ButtonCapabilitiesChecker.check_fields(
                test_case, message.buttoncapabilities, ForceSensingButton.ButtonCapabilities, expected)
        # end def check_buttoncapabilities
    # end class GetButtonCapabilitiesResponseChecker

    class GetButtonConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetButtonConfigResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FORCE_SENSING_BUTTON
            return {
                "current_force": (cls.check_current_force, config.F_DefaultForce)
            }
        # end def get_default_check_map

        @staticmethod
        def check_current_force(test_case, response, expected):
            """
            Check current_force field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetButtonConfigResponse to check
            :type response: ``GetButtonConfigResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert current_force that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The current_force shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.current_force),
                msg="The current_force parameter differs from the one expected")
        # end def check_current_force
    # end class GetButtonConfigResponseChecker

    class SetButtonConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SetButtonConfigResponse``
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
            config = test_case.f.PRODUCT.FEATURES.COMMON.FORCE_SENSING_BUTTON
            return {
                "button_id": (cls.check_button_id, 0),
                "current_force": (cls.check_current_force, config.F_DefaultForce)
            }
        # end def get_default_check_map

        @staticmethod
        def check_button_id(test_case, response, expected):
            """
            Check button_id field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetButtonConfigResponse to check
            :type response: ``SetButtonConfigResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert button_id that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The button_id shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.button_id),
                msg="The button_id parameter differs from the one expected")
        # end def check_button_id

        @staticmethod
        def check_current_force(test_case, response, expected):
            """
            Check current_force field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: SetButtonConfigResponse to check
            :type response: ``SetButtonConfigResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert current_force that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The current_force shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.current_force),
                msg="The current_force parameter differs from the one expected")
        # end def check_current_force
    # end class SetButtonConfigResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=ForceSensingButton.FEATURE_ID,
                           factory=ForceSensingButtonFactory,
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
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_19c0_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_19c0.get_capabilities_response_cls)
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
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.get_capabilities_cls(
                device_index=device_index,
                feature_index=feature_19c0_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_capabilities_and_check_error

        @classmethod
        def get_button_capabilities(cls, test_case, button_id, device_index=None, port_index=None, software_id=None,
                                    padding=None):
            """
            Process ``GetButtonCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param button_id: Button ID
            :type button_id: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetButtonCapabilitiesResponse (if not error)
            :rtype: ``GetButtonCapabilitiesResponse``
            """
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.get_button_capabilities_cls(
                device_index=device_index,
                feature_index=feature_19c0_index,
                button_id=HexList(button_id))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_19c0.get_button_capabilities_response_cls)
        # end def get_button_capabilities

        @classmethod
        def get_button_capabilities_and_check_error(
                cls, test_case, error_codes, button_id, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``GetButtonCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param button_id: Button ID
            :type button_id: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.get_button_capabilities_cls(
                device_index=device_index,
                feature_index=feature_19c0_index,
                button_id=HexList(button_id))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_button_capabilities_and_check_error

        @classmethod
        def get_button_config(cls, test_case, button_id, device_index=None, port_index=None, software_id=None,
                              padding=None):
            """
            Process ``GetButtonConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param button_id: Button ID
            :type button_id: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: GetButtonConfigResponse (if not error)
            :rtype: ``GetButtonConfigResponse``
            """
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.get_button_config_cls(
                device_index=device_index,
                feature_index=feature_19c0_index,
                button_id=HexList(button_id))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_19c0.get_button_config_response_cls)
        # end def get_button_config

        @classmethod
        def get_button_config_and_check_error(
                cls, test_case, error_codes, button_id, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``GetButtonConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param button_id: Button ID
            :type button_id: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.get_button_config_cls(
                device_index=device_index,
                feature_index=feature_19c0_index,
                button_id=HexList(button_id))

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_button_config_and_check_error

        @classmethod
        def set_button_config(cls, test_case, button_id, new_force, device_index=None, port_index=None,
                              software_id=None, padding=None):
            """
            Process ``SetButtonConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param button_id: Button ID
            :type button_id: ``int | HexList``
            :param new_force: New force
            :type new_force: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetButtonConfigResponse (if not error)
            :rtype: ``SetButtonConfigResponse``
            """
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.set_button_config_cls(
                device_index=device_index,
                feature_index=feature_19c0_index,
                button_id=HexList(button_id),
                new_force=new_force)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_19c0.set_button_config_response_cls)
        # end def set_button_config

        @classmethod
        def set_button_config_and_check_error(
                cls, test_case, error_codes, button_id, new_force, function_index=None,
                device_index=None, port_index=None):
            """
            Process ``SetButtonConfig``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param button_id: Button ID
            :type button_id: ``int | HexList``
            :param new_force: New force
            :type new_force: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_19c0_index, feature_19c0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_19c0.set_button_config_cls(
                device_index=device_index,
                feature_index=feature_19c0_index,
                button_id=HexList(button_id),
                new_force=new_force)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_button_config_and_check_error
    # end class HIDppHelper
# end class ForceSensingButtonTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
