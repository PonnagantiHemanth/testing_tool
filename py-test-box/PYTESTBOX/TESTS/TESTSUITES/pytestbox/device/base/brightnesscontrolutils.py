#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.brightnesscontrolutils
:brief: Helpers for ``BrightnessControl`` feature
:author: YY Liu <yliu5@logitech.com>
:date: 2023/08/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from warnings import warn
from time import sleep

from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessChangeEvent
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControl
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlFactory
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV0
from pyhid.hidpp.features.gaming.brightnesscontrol import CapabilitiesV1
from pyhid.hidpp.features.gaming.brightnesscontrol import GetBrightnessResponse
from pyhid.hidpp.features.gaming.brightnesscontrol import GetIlluminationResponse
from pyhid.hidpp.features.gaming.brightnesscontrol import GetInfoResponseV0
from pyhid.hidpp.features.gaming.brightnesscontrol import GetInfoResponseV1
from pyhid.hidpp.features.gaming.brightnesscontrol import IlluminationChangeEvent
from pyhid.hidpp.features.gaming.brightnesscontrol import IlluminationState
from pyhid.hidpp.features.gaming.brightnesscontrol import SetBrightnessResponse
from pyhid.hidpp.features.gaming.brightnesscontrol import SetIlluminationResponse
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagement
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffects
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.base.profilemanagementutils import ProfileManagementTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.base.loghelper import LogHelper


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_ONE_SECOND = 1  # unit: in second
_500_MS = 0.5  # unit: in second


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControlTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``BrightnessControl`` feature
    """

    class CapabilitiesChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``Capabilities``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL
            return cls.get_check_map(
                transient=HexList(config.F_Capabilities).testBit(CapabilitiesV1.POS.TRANSIENT),
                hw_on_off=HexList(config.F_Capabilities).testBit(CapabilitiesV1.POS.HW_ON_OFF),
                illumination=HexList(config.F_Capabilities).testBit(CapabilitiesV1.POS.ILLUMINATION),
                events=HexList(config.F_Capabilities).testBit(CapabilitiesV0.POS.EVENTS),
                hw_brightness=HexList(config.F_Capabilities).testBit(CapabilitiesV1.POS.HW_BRIGHTNESS)
            )
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, transient, hw_on_off, illumination, events, hw_brightness):
            """
            Get the check methods and given expected values

            :param transient: Expected transient capability
            :type transient: ``int``
            :param hw_on_off: Expected hw_on_off capability
            :type hw_on_off: ``int``
            :param illumination: Expected illumination capability
            :type illumination: ``int``
            :param events: Expected events capability
            :type events: ``int``
            :param hw_brightness: Expected hw_brightness capability
            :type hw_brightness: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "transient": (cls.check_transient, transient),
                "hw_on_off": (cls.check_hw_on_off, hw_on_off),
                "illumination": (cls.check_illumination, illumination),
                "events": (cls.check_events, events),
                "hw_brightness": (cls.check_hw_brightness, hw_brightness)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_transient(test_case, bitmap, expected):
            """
            Check transient field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert transient that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.transient),
                msg="The transient parameter differs from the one expected")
        # end def check_transient

        @staticmethod
        def check_hw_on_off(test_case, bitmap, expected):
            """
            Check hw_on_off field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hw_on_off that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.hw_on_off),
                msg="The hw_on_off parameter differs from the one expected")
        # end def check_hw_on_off

        @staticmethod
        def check_illumination(test_case, bitmap, expected):
            """
            Check illumination field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert illumination that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.illumination),
                msg="The illumination parameter differs from the one expected")
        # end def check_illumination

        @staticmethod
        def check_events(test_case, bitmap, expected):
            """
            Check events field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert events that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.events),
                msg="The events parameter differs from the one expected")
        # end def check_events

        @staticmethod
        def check_hw_brightness(test_case, bitmap, expected):
            """
            Check hw_brightness field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hw_brightness that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.hw_brightness),
                msg="The hw_brightness parameter differs from the one expected")
        # end def check_hw_brightness

        @staticmethod
        def check_hw(test_case, bitmap, expected):
            """
            Check hw field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert hw that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.hw),
                msg="The hw parameter differs from the one expected")
        # end def check_hw
    # end class CapabilitiesChecker

    class IlluminationStateChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``IlluminationState``
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
            return cls.get_check_map(
                state=test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_DefaultIlluminationState)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, state):
            """
            Get the check methods with given expected values

            :param state: Expected state
            :type state: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "reserved": (cls.check_reserved, 0),
                "state": (cls.check_state, state)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved(test_case, bitmap, expected):
            """
            Check reserved field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``BrightnessControl.Capabilities``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.reserved),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved

        @staticmethod
        def check_state(test_case, bitmap, expected):
            """
            Check state field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: Capabilities to check
            :type bitmap: ``IlluminationState``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert state that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(bitmap.state),
                msg="The state parameter differs from the one expected")
        # end def check_state
    # end class IlluminationStateChecker

    class GetInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetInfoResponse``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL
            return {
                "max_brightness": (cls.check_max_brightness, config.F_MaxBrightness),
                "min_brightness": (cls.check_min_brightness, config.F_MinBrightness),
                "steps": (cls.check_steps, config.F_Steps),
                "steps_lsb": (cls.check_steps_lsb, to_int(config.F_Steps) & 0xFF),
                "steps_msb": (cls.check_steps_msb, to_int(config.F_Steps) >> 8),
                "capabilities": (
                    cls.check_capabilities,
                    BrightnessControlTestUtils.CapabilitiesChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_max_brightness(test_case, response, expected):
            """
            Check max_brightness field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponseV0 | GetInfoResponseV1``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert max_brightness that raise an exception
            """
            test_case.assertEqual(
                expected=expected,
                obtained=to_int(response.max_brightness),
                msg="The max_brightness parameter differs from the one expected")
        # end def check_max_brightness

        @staticmethod
        def check_min_brightness(test_case, response, expected):
            """
            Check min_brightness field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponseV1``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert min_brightness that raise an exception
            """
            test_case.assertEqual(
                expected=expected,
                obtained=to_int(response.min_brightness),
                msg="The min_brightness parameter differs from the one expected")
        # end def check_min_brightness

        @staticmethod
        def check_steps(test_case, response, expected):
            """
            Check steps field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponseV0``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert steps that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.steps),
                msg="The steps parameter differs from the one expected")
        # end def check_steps

        @staticmethod
        def check_steps_lsb(test_case, response, expected):
            """
            Check steps_lsb field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert steps_lsb that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.steps_lsb),
                msg="The steps_lsb parameter differs from the one expected")
        # end def check_steps_lsb

        @staticmethod
        def check_steps_msb(test_case, response, expected):
            """
            Check steps_msb field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert steps_msb that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.steps_msb),
                msg="The steps_msb parameter differs from the one expected")
        # end def check_steps_msb

        @staticmethod
        def check_capabilities(test_case, message, expected):
            """
            Check ``capabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetInfoResponse to check
            :type message: ``GetInfoResponseV0 | GetInfoResponseV1``
            :param expected: Expected value
            :type expected: ``dict``

            :raise ``AssertionError``: If the feature version is not supported
            """
            if test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_Version_0:
                expected_class = CapabilitiesV0
            elif test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_Version_1:
                expected_class = CapabilitiesV1
            else:
                raise AssertionError("The feature version of BrightnessControl is not supported.")
            # end if

            BrightnessControlTestUtils.CapabilitiesChecker.check_fields(
                test_case, message.capabilities, expected_class, expected)
        # end def check_capabilities
    # end class GetInfoResponseChecker

    class GetBrightnessResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetBrightnessResponse``
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
            return cls.get_check_map(
                brightness=test_case.f.PRODUCT.FEATURES.GAMING.BRIGHTNESS_CONTROL.F_DefaultBrightness)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, brightness):
            """
            Get the check methods with given expected brightness

            :param brightness: Expected brightness
            :type brightness: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "brightness": (cls.check_brightness, brightness)
            }
        # end def get_check_map

        @staticmethod
        def check_brightness(test_case, response, expected):
            """
            Check brightness field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetBrightnessResponse to check
            :type response: ``GetBrightnessResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert brightness that raise an exception
            """
            test_case.assertEqual(
                expected=expected,
                obtained=to_int(response.brightness),
                msg="The brightness parameter differs from the one expected")
        # end def check_brightness
    # end class GetBrightnessResponseChecker

    class GetIlluminationResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetIlluminationResponse``
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
                "illumination_state": (
                    cls.check_illumination_state,
                    BrightnessControlTestUtils.IlluminationStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, illumination_state):
            """
            Get the check methods with given expected values

            :param illumination_state: Expected illumination state
            :type illumination_state: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "illumination_state": (
                    cls.check_illumination_state,
                    BrightnessControlTestUtils.IlluminationStateChecker.get_check_map(state=illumination_state))
            }
        # end def get_check_map

        @staticmethod
        def check_illumination_state(test_case, message, expected):
            """
            Check illumination_state field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetIlluminationResponse to check
            :type message: ``GetIlluminationResponse``
            :param expected: Expected value
            :type expected: ``dict``

            :raise ``AssertionError``: Assert illumination_state that raise an exception
            """
            BrightnessControlTestUtils.IlluminationStateChecker.check_fields(
                test_case, message.illumination_state, IlluminationState, expected)
        # end def check_illumination_state
    # end class GetIlluminationResponseChecker

    class BrightnessChangeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``BrightnessChangeEvent``
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
                "brightness": (cls.check_brightness, 0)
            }
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, brightness):
            """
            Get the check methods with given expected brightness

            :param brightness: Expected brightness
            :type brightness: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            return {
                "brightness": (cls.check_brightness, brightness)
            }
        # end def get_check_map

        @staticmethod
        def check_brightness(test_case, event, expected):
            """
            Check brightness field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: BrightnessChangeEvent to check
            :type event: ``BrightnessChangeEvent``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert brightness that raise an exception
            """
            test_case.assertEqual(
                expected=expected,
                obtained=to_int(event.brightness),
                msg="The brightness parameter differs from the one expected")
        # end def check_brightness
    # end class BrightnessChangeEventChecker

    class IlluminationChangeEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``IlluminationChangeEvent``
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
                "illumination_state": (
                    cls.check_illumination_state,
                    BrightnessControlTestUtils.IlluminationStateChecker.get_default_check_map(test_case))
            }
        # end def get_default_check_map

        @staticmethod
        def check_illumination_state(test_case, message, expected):
            """
            Check illumination_state field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: IlluminationChangeEvent to check
            :type message: ``IlluminationChangeEvent``
            :param expected: Expected value
            :type expected: ``dict``

            :raise ``AssertionError``: Assert illumination_state that raise an exception
            """
            BrightnessControlTestUtils.IlluminationStateChecker.check_fields(
                test_case, message.illumination_state, IlluminationState, expected)
        # end def check_illumination_state
    # end class IlluminationChangeEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case,
                           feature_id=BrightnessControl.FEATURE_ID,
                           factory=BrightnessControlFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_info(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetInfo``

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

            :return: GetInfoResponse (if not error)
            :rtype: ``GetInfoResponseV0 | GetInfoResponseV1``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.get_info_cls(
                device_index=device_index,
                feature_index=feature_8040_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8040.get_info_response_cls)
        # end def get_info

        @classmethod
        def get_info_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetInfo``

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
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.get_info_cls(
                device_index=device_index,
                feature_index=feature_8040_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_info_and_check_error

        @classmethod
        def get_brightness(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetBrightness``

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

            :return: GetBrightnessResponse (if not error)
            :rtype: ``GetBrightnessResponse``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.get_brightness_cls(
                device_index=device_index,
                feature_index=feature_8040_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8040.get_brightness_response_cls)
        # end def get_brightness

        @classmethod
        def get_brightness_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetBrightness``

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
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.get_brightness_cls(
                device_index=device_index,
                feature_index=feature_8040_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_brightness_and_check_error

        @classmethod
        def set_brightness(cls, test_case, brightness, device_index=None, port_index=None, software_id=None,
                           padding=None):
            """
            Process ``SetBrightness``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param brightness: Brightness
            :type brightness: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetBrightnessResponse (if not error)
            :rtype: ``SetBrightnessResponse``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.set_brightness_cls(
                device_index=device_index,
                feature_index=feature_8040_index,
                brightness=brightness)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8040.set_brightness_response_cls)
        # end def set_brightness

        @classmethod
        def set_brightness_and_check_error(
                cls, test_case, error_codes, brightness, function_index=None, device_index=None,
                port_index=None):
            """
            Process ``SetBrightness``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param brightness: Brightness
            :type brightness: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.set_brightness_cls(
                device_index=device_index,
                feature_index=feature_8040_index,
                brightness=brightness)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_brightness_and_check_error

        @classmethod
        def get_illumination(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``GetIllumination``

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

            :return: GetIlluminationResponse (if not error)
            :rtype: ``GetIlluminationResponse``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.get_illumination_cls(
                device_index=device_index,
                feature_index=feature_8040_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8040.get_illumination_response_cls)
        # end def get_illumination

        @classmethod
        def get_illumination_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetIllumination``

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
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.get_illumination_cls(
                device_index=device_index,
                feature_index=feature_8040_index)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_illumination_and_check_error

        @classmethod
        def set_illumination(cls, test_case, state, reserved=None, device_index=None, port_index=None,
                             software_id=None, padding=None):
            """
            Process ``SetIllumination``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param state: Illumination state
            :type state: ``int | HexList``
            :param reserved: Reserved bits of state
            :type reserved: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetIlluminationResponse (if not error)
            :rtype: ``SetIlluminationResponse``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.set_illumination_cls(
                device_index=device_index,
                feature_index=feature_8040_index,
                state=state)

            if reserved is not None:
                report.reserved = reserved
            # end if

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8040.set_illumination_response_cls)
        # end def set_illumination

        @classmethod
        def set_illumination_and_check_error(
                cls, test_case, error_codes, state, function_index=None, device_index=None, port_index=None):
            """
            Process ``SetIllumination``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param state: Illumination state
            :type state: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_8040_index, feature_8040, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8040.set_illumination_cls(
                device_index=device_index,
                feature_index=feature_8040_index,
                state=state)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def set_illumination_and_check_error

        @classmethod
        def brightness_change_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``BrightnessChangeEvent``: get notification from event queue

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

            :return: BrightnessChangeEvent
            :rtype: ``BrightnessChangeEvent``
            """
            _, feature_8040, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8040.brightness_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def brightness_change_event

        @classmethod
        def illumination_change_event(
                cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``IlluminationChangeEvent``: get notification from event queue

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

            :return: IlluminationChangeEvent
            :rtype: ``IlluminationChangeEvent``
            """
            _, feature_8040, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_8040.illumination_change_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def illumination_change_event
    # end class HIDppHelper

    @classmethod
    def get_standard_physical_brightness_controls(cls, test_case):
        """
        Get all standard physical brightness controls on the device

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: KEY_IDs of physical brightness controls available on the device
        :rtype: ``list[KEY_ID]``
        """
        brightness_controls = {KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                               KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN,
                               KEY_ID.DIMMING_KEY}
        return list(brightness_controls.intersection(set(test_case.button_stimuli_emulator.get_key_id_list())))
    # end def get_standard_physical_brightness_controls

    @classmethod
    def get_functional_physical_brightness_controls(cls, test_case):
        """
        Get all functional physical brightness controls on the device

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``

        :return: KEY_IDs of physical brightness controls available on the device
        :rtype: ``list[KEY_ID]``
        """
        brightness_controls = {KEY_ID.BACKLIGHT_UP, KEY_ID.BACKLIGHT_DOWN,
                               KEY_ID.BRIGHTNESS_UP, KEY_ID.BRIGHTNESS_DOWN,
                               KEY_ID.DIMMING_KEY}
        return list(brightness_controls.intersection(set(test_case.button_stimuli_emulator.get_fn_keys())))
    # end def get_functional_physical_brightness_controls

    @classmethod
    def control_brightness_manually(cls, test_case, key_id, is_function_key=False):
        """
        Change the brightness via the physical control

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :param key_id: KEY_IDs of a physical brightness control
        :type key_id: ``KEY_ID``
        :param is_function_key: Flag indicating the physical brightness control is a function key
        :type is_function_key: ``bool``
        """
        if is_function_key:
            test_case.button_stimuli_emulator.key_press(key_id=KEY_ID.FN_KEY)
            sleep(_500_MS)
            test_case.button_stimuli_emulator.keystroke(key_id=test_case.button_stimuli_emulator.get_fn_keys()[key_id])
            test_case.button_stimuli_emulator.key_release(key_id=KEY_ID.FN_KEY)
        else:
            test_case.button_stimuli_emulator.keystroke(key_id=key_id)
        # end if
    # end def control_brightness_manually

    @classmethod
    def set_brightness_and_check_result_from_rgb_monitoring(cls, test_case, brightness,
                                                            red=0xFF, green=0xFF, blue=0xFF,
                                                            calibration_data=None):
        """
        Set brightness and check the brightness via the result of RGB LED monitoring

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :parm brightness: Brightness of LEDs
        :type brightness: ``int``
        :param red: Red value of LED - OPTIONAL
        :type red: ``int``
        :param green: Green value of LED - OPTIONAL
        :type green: ``int``
        :param blue:  Blue value of LED - OPTIONAL
        :type blue: ``int``
        :param calibration_data: Reb, Blue and Green calibration data for zone0, zone1 and zone2 - OPTIONAL
        :type calibration_data: ``list[list[int, int, int]]``

        :raise ``AssertionError``: If the RGB effect running on the device is not the Fixed effect
        """
        current_effect_index = RGBEffectsTestUtils.HIDppHelper.get_info_about_rgb_cluster(
            test_case=test_case, rgb_cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY).rgb_cluster_effect_index
        current_effect = RGBEffectsTestUtils.HIDppHelper.get_info_about_effect_general_info(
            test_case=test_case, rgb_cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
            rgb_cluster_effect_index=to_int(current_effect_index))

        assert to_int(current_effect.effect_id) == RGBEffects.RGBEffectID.FIXED, \
            "The current effect is not the Fixed effect, the effect shall be configured to Fixed effect before " \
            "entering this method."

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Start RGB effect monitoring')
        # --------------------------------------------------------------------------------------------------------------
        RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, "Send setBrightness request to change the brightness")
        # --------------------------------------------------------------------------------------------------------------
        BrightnessControlTestUtils.HIDppHelper.set_brightness(
            test_case=test_case, brightness=brightness)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Stop RGB effect monitoring after 1 second')
        # --------------------------------------------------------------------------------------------------------------
        sleep(_ONE_SECOND)
        RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(test_case=test_case)

        if test_case.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, 'Check RGB brightness of the fixed effect on the primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                test_case=test_case, red_value=red, green_value=green, blue_value=blue,
                brightness=brightness, calibration_data=calibration_data, check_last_packet_only=True,
                cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
        # end if
    # end def set_brightness_and_check_result_from_rgb_monitoring

    @classmethod
    def set_fix_effect_and_check_result_from_rgb_monitoring(cls, test_case, brightness, red=0xFF, green=0xFF, blue=0xFF,
                                                            enable_sw_control=True, calibration_data=None):
        """
        Set fix effect on the primary cluster to check the brightness via the result of RGB LED monitoring

        :param test_case: Current test case
        :type test_case: ``CommonBaseTestCase``
        :parm brightness: Brightness of LEDs
        :type brightness: ``int``
        :param red: Red value of LED - OPTIONAL
        :type red: ``int``
        :param green: Green value of LED - OPTIONAL
        :type green: ``int``
        :param blue:  Blue value of LED - OPTIONAL
        :type blue: ``int``
        :param enable_sw_control: Flag indicating that SW control of RGB cluster shall be enable - OPTIONAL
        :type enable_sw_control: ``bool``
        :param calibration_data: Reb, Blue and Green calibration data for zone0, zone1 and zone2
        :type calibration_data: ``list[list[int, int, int]]``
        """
        if test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_Enabled:
            if enable_sw_control:
                # To fully enter SW control mode, the SW_CONTROL_CLUSTER, SW_CONTROL_POWER_MODE and HOST_MODE shall be
                # enabled. Otherwise, it may cause some unexpected/incorrect behaviors.
                # NB: It's a deal between FW and SW team, when GHub enable SW control, it shall enable all modes
                # mentioned above. So we follow their deal to have the same operation here.
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Enable SW Control of RGB Cluster')
                # ------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.HIDppHelper.manage_sw_control(
                    test_case=test_case, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                    sw_control_flags=RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_ALL_RGB_CLUSTERS |
                    RGBEffectsTestUtils.SwControlFlags.ENABLE_SW_CONTROL_OF_POWER_MODES)

                if test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_Enabled:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, "Set the device into host mode by 0x8100.setOnboardMode")
                    # --------------------------------------------------------------------------------------------------
                    OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(test_case, OnboardProfiles.Mode.HOST_MODE)
                elif test_case.f.PRODUCT.FEATURES.GAMING.PROFILE_MANAGEMENT.F_Enabled:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, f"Set the device into host mode by 0x8101.getSetMode")
                    # --------------------------------------------------------------------------------------------------
                    ProfileManagementTestUtils.HIDppHelper.get_set_mode(
                        test_case=test_case,
                        set_onboard_mode=ProfileManagementTestUtils.RequestType.SET,
                        onboard_mode=ProfileManagement.Mode.HOST_MODE)
                else:
                    warn("The SW_CONTROL mode is not fully enabled, because there is no feature to enter HOST_MODE")
                # end if
            # end if

            if calibration_data is None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Enable the hidden features to get access to the calibration factor')
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.HIDppHelper.activate_features(test_case, manufacturing=True)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Get calibration factor')
                # ------------------------------------------------------------------------------------------------------
                calibration_data = RGBEffectsTestUtils.HIDppHelper.get_rgb_calibration_values(test_case)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                test_case, 'Set Disable effect on primary cluster and wait 1s to be sure no more effect is played')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_disabled_effect(test_case, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                    persistence=RGBEffectsTestUtils.Persistence.VOLATILE)
            sleep(_ONE_SECOND)

            if test_case.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Start RGB effect monitoring')
                # ------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper.start_monitoring(test_case)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Set a fixed effect on primary cluster')
            # ----------------------------------------------------------------------------------------------------------
            RGBEffectsTestUtils.HIDppHelper. \
                set_fixed_effect(test_case, cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY,
                                 red=red, green=green, blue=blue,
                                 mode=RGBEffectsTestUtils.FixedRGBEffectMode.DEFAULT,
                                 persistence=RGBEffectsTestUtils.Persistence.VOLATILE)

            if test_case.kosmos.discover_emulator(emulation_type=DeviceFamilyName.GENERIC_LED_SPY):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, 'Stop RGB effect monitoring after 1 second')
                # ------------------------------------------------------------------------------------------------------
                sleep(_ONE_SECOND)
                RGBEffectsTestUtils.RgbSpyHelper.stop_monitoring(test_case)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case, 'Check RGB brightness of the fixed effect on the primary cluster')
                # ------------------------------------------------------------------------------------------------------
                RGBEffectsTestUtils.RgbSpyHelper.check_fixed_effect(
                    test_case=test_case, red_value=red, green_value=green, blue_value=blue,
                    brightness=brightness, calibration_data=calibration_data, check_last_packet_only=True,
                    cluster_index=RGBEffectsTestUtils.RGBClusterId.PRIMARY)
            # end if
        # end if
    # end def set_fix_effect_and_check_result_from_rgb_monitoring
# end class BrightnessControlTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
