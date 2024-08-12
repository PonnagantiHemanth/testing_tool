#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.backlightutils
:brief: Helpers for ``Backlight`` feature
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/09/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.backlight import Backlight
from pyhid.hidpp.features.common.backlight import BacklightFactory
from pyhid.hidpp.features.common.backlight import BacklightInfoEventV1
from pyhid.hidpp.features.common.backlight import BacklightInfoEventV2ToV4
from pyhid.hidpp.features.common.backlight import GetBacklightConfigResponseData1
from pyhid.hidpp.features.common.backlight import GetBacklightConfigResponseData4
from pyhid.hidpp.features.common.backlight import GetBacklightInfoResponseData1
from pyhid.hidpp.features.common.backlight import GetBacklightInfoResponseData4
from pyhid.hidpp.features.common.backlight import SetBacklightEffectResponse
from pyhid.hidpp.features.root import Root
from pylibrary.emulator.ledid import LED_ID
from pylibrary.mcu.backlightchunks import BacklightChunk
from pylibrary.mcu.backlightchunks import BacklightChunkV3
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pyraspi.services.keyboardemulator import KeyboardMixin
from pyraspi.services.kosmos.config.ledlayout import GET_LED_LAYOUT_BY_ID
from pyraspi.services.kosmos.i2c.i2cbacklightparser import BacklightEffectType
from pyraspi.services.kosmos.i2c.i2cbacklightparser import LedDataBacklightParser
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BacklightTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``Backlight`` feature
    """

    # Added for Norman keyboard which turned on ALS to measure ambient light after power LED timeout
    POWER_LED_TIMEOUT = 7
    # Brightness keys timeout (ms)
    BRIGHTNESS_KEYS_FIRST_STEP_TIMEOUT = 600
    BRIGHTNESS_KEYS_EVERY_STEP_TIMEOUT = 250
    # Add 5% margin for backlight duration
    BACKLIGHT_DURATION_5_PERCENT_MARGIN = 1.05
    # Add 10% margin for backlight duration
    BACKLIGHT_DURATION_10_PERCENT_MARGIN = 1.1
    # Add 20% margin for backlight duration
    BACKLIGHT_DURATION_20_PERCENT_MARGIN = 1.2
    # Increment duration of currDurationHandsOUT,  currDurationHandsIN, currDurationPowered (in second)
    INCREMENT_DURATION_HANDS_IN_OUT_OR_POWERED = 5

    class GetBacklightConfigResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetBacklightConfig`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetBacklightConfigResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "configuration": (
                    cls.check_configuration,
                    Backlight.Configuration.ENABLE),
                "supported_options": (
                    cls.check_supported_options,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_SupportedOptions),
                "backlight_effect_list": (
                    cls.check_backlight_effect_list,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_BacklightEffectList),
                "current_backlight_level": (
                    cls.check_current_backlight_level_by_range,
                    (Backlight.CurrentLevel.CURRENT_LEVEL_2, Backlight.CurrentLevel.CURRENT_LEVEL_4)),
                "curr_duration_hands_out": (
                    cls.check_curr_duration_hands_out,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationHandsOut),
                "curr_duration_hands_in": (
                    cls.check_curr_duration_hands_in,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationHandsIn),
                "curr_duration_powered": (
                    cls.check_curr_duration_powered,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationPowered),
                "curr_duration_not_powered": (
                    cls.check_curr_duration_not_powered,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationNotPowered),
                "reserved": (
                    cls.check_reserved,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_configuration(test_case, response, expected):
            """
            Check configuration field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1 | BacklightChunk``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertNotNone(
                expected, msg="Configuration shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.configuration),
                msg=f"The configuration parameter differs "
                    f"(expected:{expected}, obtained:{response.configuration})")
        # end def check_configuration

        @staticmethod
        def check_supported_options(test_case, response, expected):
            """
            Check supported_options field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertNotNone(
                expected, msg="SupportedOptions shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.supported_options),
                msg=f"The supported_options parameter differs "
                    f"(expected:{expected}, obtained:{response.supported_options})")
        # end def check_supported_options

        @staticmethod
        def check_backlight_effect_list(test_case, response, expected):
            """
            Check backlight_effect_list field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertNotNone(
                expected, msg="BacklightEffectList shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.backlight_effect_list),
                msg=f"The backlight_effect_list parameter differs "
                    f"(expected:{expected}, obtained:{response.backlight_effect_list})")
        # end def check_backlight_effect_list

        @staticmethod
        def check_current_backlight_level(test_case, response, expected):
            """
            Check current_backlight_level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            if hasattr(response, 'current_backlight_level'):
                test_case.assertEqual(
                    expected=to_int(expected),
                    obtained=to_int(response.current_backlight_level),
                    msg=f"The current_backlight_level parameter differs "
                        f"(expected:{expected}, obtained:{response.current_backlight_level})")
            # end if
        # end def check_current_backlight_level

        @staticmethod
        def check_current_backlight_level_by_range(test_case, response, expected):
            """
            Check current_backlight_level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1``
            :param expected: Expected value range
            :type expected: ``list[int]``
            """
            if hasattr(response, 'current_backlight_level'):
                test_case.assertIn(
                    member=to_int(response.current_backlight_level),
                    container=expected,
                    msg=f"The current_backlight_level parameter differs "
                        f"(expected range:{expected}, obtained:{response.current_backlight_level})")
            # end if
        # end def check_current_backlight_level_by_range

        @staticmethod
        def check_curr_duration_hands_out(test_case, response, expected):
            """
            Check curr_duration_hands_out field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1 | BacklightChunk``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            if hasattr(response, 'curr_duration_hands_out'):
                test_case.assertEqual(
                    expected=to_int(expected),
                    obtained=to_int(response.curr_duration_hands_out[::-1]),
                    msg=f"The curr_duration_hands_out parameter differs "
                        f"(expected:{expected}, obtained:{response.curr_duration_hands_out[::-1]})")
            # end if
        # end def check_curr_duration_hands_out

        @staticmethod
        def check_curr_duration_hands_in(test_case, response, expected):
            """
            Check curr_duration_hands_in field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1 | BacklightChunk``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            if hasattr(response, 'curr_duration_hands_in'):
                test_case.assertEqual(
                    expected=to_int(expected),
                    obtained=to_int(response.curr_duration_hands_in[::-1]),
                    msg=f"The curr_duration_hands_in parameter differs "
                        f"(expected:{expected}, obtained:{response.curr_duration_hands_in[::-1]})")
            # end if
        # end def check_curr_duration_hands_in

        @staticmethod
        def check_curr_duration_powered(test_case, response, expected):
            """
            Check curr_duration_powered field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1 | BacklightChunk``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            if hasattr(response, 'curr_duration_powered'):
                test_case.assertEqual(
                    expected=to_int(expected),
                    obtained=to_int(response.curr_duration_powered[::-1]),
                    msg=f"The curr_duration_powered parameter differs "
                        f"(expected:{expected}, obtained:{response.curr_duration_powered[::-1]})")
            # end if
        # end def check_curr_duration_powered

        @staticmethod
        def check_curr_duration_not_powered(test_case, response, expected):
            """
            Check curr_duration_not_powered field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData4``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.curr_duration_not_powered[::-1]),
                msg=f"The curr_duration_not_powered parameter differs "
                    f"(expected:{expected}, obtained:{response.curr_duration_not_powered[::-1]})")
        # end def check_curr_duration_not_powered

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightConfigResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetBacklightConfigResponseChecker

    class GetBacklightInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetBacklightInfo`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetBacklightInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "number_of_level": (
                    cls.check_number_of_level,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_NumberOfLevel),
                "current_level": (
                    cls.check_current_level_by_range,
                    (Backlight.CurrentLevel.CURRENT_LEVEL_2, Backlight.CurrentLevel.CURRENT_LEVEL_4)),
                "backlight_status": (
                    cls.check_backlight_status,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_BacklightStatus),
                "backlight_effect": (
                    cls.check_backlight_effect,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_BacklightEffect),
                "oob_duration_hands_out": (
                    cls.check_oob_duration_hands_out,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationHandsOut),
                "oob_duration_hands_in": (
                    cls.check_oob_duration_hands_in,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationHandsIn),
                "oob_duration_powered": (
                    cls.check_oob_duration_powered,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationPowered),
                "oob_duration_not_powered": (
                    cls.check_oob_duration_not_powered,
                    test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_OobDurationNotPowered),
                "reserved": (
                    cls.check_reserved,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_number_of_level(test_case, response, expected):
            """
            Check number_of_level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertNotNone(
                expected, msg="NumberOfLevel shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.number_of_level),
                msg=f"The number_of_level parameter differs "
                    f"(expected:{expected}, obtained:{response.number_of_level})")
        # end def check_number_of_level

        @staticmethod
        def check_current_level(test_case, response, expected):
            """
            Check current_level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.current_level),
                msg=f"The current_level parameter differs "
                    f"(expected:{expected}, obtained:{response.current_level})")
        # end def check_current_level

        @staticmethod
        def check_current_level_by_range(test_case, response, expected):
            """
            Check current_level field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value range
            :type expected: ``list[int]``
            """
            test_case.assertIn(
                member=to_int(response.current_level),
                container=expected,
                msg=f"The current_level parameter differs "
                    f"(expected range:{expected}, obtained:{response.current_level})")
        # end def check_current_level_by_range

        @staticmethod
        def check_backlight_status(test_case, response, expected):
            """
            Check backlight_status field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertNotNone(
                expected, msg="BacklightStatus shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.backlight_status),
                msg=f"The backlight_status parameter differs "
                    f"(expected:{expected}, obtained:{response.backlight_status})")
        # end def check_backlight_status

        @staticmethod
        def check_backlight_effect(test_case, response, expected):
            """
            Check backlight_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1 | BacklightChunk``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertNotNone(
                expected, msg="BacklightEffect shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.backlight_effect),
                msg=f"The backlight_effect parameter differs "
                    f"(expected:{expected}, obtained:{response.backlight_effect})")
        # end def check_backlight_effect

        @staticmethod
        def check_oob_duration_hands_out(test_case, response, expected):
            """
            Check oob_duration_hands_out field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.oob_duration_hands_out[::-1]),
                msg=f"The oob_duration_hands_out parameter differs "
                    f"(expected:{expected}, obtained:{response.oob_duration_hands_out[::-1]})")
        # end def check_oob_duration_hands_out

        @staticmethod
        def check_oob_duration_hands_in(test_case, response, expected):
            """
            Check oob_duration_hands_in field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.oob_duration_hands_in[::-1]),
                msg=f"The oob_duration_hands_in parameter differs "
                    f"(expected:{expected}, obtained:{response.oob_duration_hands_in[::-1]})")
        # end def check_oob_duration_hands_in

        @staticmethod
        def check_oob_duration_powered(test_case, response, expected):
            """
            Check oob_duration_powered field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.oob_duration_powered[::-1]),
                msg=f"The oob_duration_powered parameter differs "
                    f"(expected:{expected}, obtained:{response.oob_duration_powered[::-1]})")
        # end def check_oob_duration_powered

        @staticmethod
        def check_oob_duration_not_powered(test_case, response, expected):
            """
            Check oob_duration_not_powered field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightInfoResponse to check
            :type response: ``GetBacklightInfoResponseData4``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.oob_duration_not_powered[::-1]),
                msg=f"The oob_duration_not_powered parameter differs "
                    f"(expected:{expected}, obtained:{response.oob_duration_not_powered[::-1]})")
        # end def check_oob_duration_not_powered

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetBacklightConfigResponse to check
            :type response: ``GetBacklightInfoResponseData1``
            :param expected: Expected value
            :type expected: ``int | HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved
    # end class GetBacklightInfoResponseChecker

    class BacklightInfoEventResponseChecker(GetBacklightInfoResponseChecker):
        """
        Check ``BacklightInfoEvent`` notification
        """
        pass
    # end class BacklightInfoEventResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=Backlight.FEATURE_ID, factory=BacklightFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_backlight_config(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetBacklightConfig``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetBacklightConfigResponse
            :rtype: ``GetBacklightConfigResponseData1``
            """
            feature_1982_index, feature_1982, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1982.get_backlight_config_cls(
                device_index=device_index,
                feature_index=feature_1982_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1982.get_backlight_config_response_cls)
            return response
        # end def get_backlight_config

        @classmethod
        def set_backlight_config(cls, test_case, configuration, options, backlight_effect=0xFF,
                                 current_backlight_level=2, curr_duration_hands_out=1, curr_duration_hands_in=1,
                                 curr_duration_powered=1, curr_duration_not_powered=1, software_id=0xF,
                                 device_index=None, port_index=None):
            """
            Process ``SetBacklightConfig``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param configuration: Configuration
            :type configuration: ``int | HexList``
            :param options: Options
            :type options: ``int | HexList``
            :param backlight_effect: Backlight Effect - OPTIONAL
            :type backlight_effect: ``int | HexList``
            :param current_backlight_level: The current backlight brightness level set by the SW or HW in
                                            "Permanent Manual Mode". - OPTIONAL
            :type current_backlight_level: ``int | HexList``
            :param curr_duration_hands_out: The needed time to start the FADE-OUT effect after the last keystroke and no
                                            proximity detection. - OPTIONAL
            :type curr_duration_hands_out: ``int | HexList``
            :param curr_duration_hands_in: The needed time to start the FADE-OUT effect after the last interaction with
                                           the device while keeping the object/hands in the detection zone. - OPTIONAL
            :type curr_duration_hands_in: ``int | HexList``
            :param curr_duration_powered: The needed time to start the FADE-OUT effect after the last interaction with
                                          a device externally powered. - OPTIONAL
            :type curr_duration_powered: ``int | HexList``
            :param curr_duration_not_powered: The needed time to start the FADE-OUT effect after the last interaction
                                              with a not externally powered device which has no proximity sensor.
                                              - OPTIONAL
            :type curr_duration_not_powered: ``int | HexList``
            :param software_id: Software Id - OPTIONAL
            :type software_id: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetBacklightConfigResponse
            :rtype: ``SetBacklightConfigResponse``
            """
            feature_1982_index, feature_1982, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1982.set_backlight_config_cls(
                device_index=device_index,
                feature_index=feature_1982_index,
                software_id=software_id,
                configuration=configuration,
                options=options,
                backlight_effect=backlight_effect,
                current_backlight_level=current_backlight_level,
                curr_duration_hands_out=Numeral(curr_duration_hands_out, byteCount=2, littleEndian=True),
                curr_duration_hands_in=Numeral(curr_duration_hands_in, byteCount=2, littleEndian=True),
                curr_duration_powered=Numeral(curr_duration_powered, byteCount=2, littleEndian=True),
                curr_duration_not_powered=Numeral(curr_duration_not_powered, byteCount=2, littleEndian=True))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1982.set_backlight_config_response_cls)
            return response
        # end def set_backlight_config

        @classmethod
        def get_backlight_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetBacklightInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetBacklightInfoResponse
            :rtype: ``GetBacklightInfoResponseData1``
            """
            feature_1982_index, feature_1982, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1982.get_backlight_info_cls(
                device_index=device_index,
                feature_index=feature_1982_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1982.get_backlight_info_response_cls)
            return response
        # end def get_backlight_info

        @classmethod
        def set_backlight_effect(cls, test_case, backlight_effect, device_index=None, port_index=None):
            """
            Process ``SetBacklightEffect``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param backlight_effect: Backlight Effect
            :type backlight_effect: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetBacklightEffectResponse
            :rtype: ``SetBacklightEffectResponse``
            """
            feature_1982_index, feature_1982, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1982.set_backlight_effect_cls(
                device_index=device_index,
                feature_index=feature_1982_index,
                backlight_effect=HexList(backlight_effect))

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1982.set_backlight_effect_response_cls)
            return response
        # end def set_backlight_effect

        @classmethod
        def backlight_info_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                 check_first_message=True, allow_no_message=False, skip_error_message=False,
                                 device_index=None, port_index=None):
            """
            Process ``BacklightInfoEvent``: get notification from event queue

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
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: BacklightInfoEvent
            :rtype: ``BacklightInfoEventV1`` or ``BacklightInfoEventV2ToV4``
            """
            _, feature_1982, _, _ = cls.get_parameters(test_case, device_index=device_index, port_index=port_index)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_1982.backlight_info_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def backlight_info_event

        @classmethod
        def disable_backlight_wow_effect(cls, test_case):
            """
            Disable the WOW effect played on Easy switch LEDs after a DUT power on or a successful pairing.

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f'Check if the 0x1982 Backlight feature is supported by the DUT')
            # ----------------------------------------------------------------------------------------------------------
            feature_1982_index, _, _, _ = BacklightTestUtils.HIDppHelper.get_parameters(test_case, skip_not_found=True)

            if feature_1982_index != Root.FEATURE_NOT_FOUND:
                if Numeral(test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_SupportedOptions) & \
                        Backlight.SupportedOptionsMask.WOW == Backlight.SupportedOptionsMask.WOW:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(
                        test_case, 'Disable the WOW effect played on Easy switch LEDs after a DUT power on.')
                    # --------------------------------------------------------------------------------------------------
                    BacklightTestUtils.HIDppHelper.set_backlight_config(
                        test_case, configuration=Backlight.Configuration.ENABLE,
                        options=BacklightTestUtils.get_default_options(test_case) & ~Backlight.Options.WOW)
                # end if
            # end if
        # end def disable_backlight_wow_effect
    # end class HIDppHelper

    class BacklightSpyHelper:
        """
        Backlight Spy module Helper class
        """
        @classmethod
        def start_monitoring(cls, test_case, reset=True):
            """
            Start the LED spy over I2C monitoring or LED backlight spy.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param reset: flag indicating if we reset the module before starting the monitoring - OPTIONAL
            :type reset: ``bool``
            """
            test_case.led_backlight_parser = None
            fw_id = test_case.f.PRODUCT.F_ProductReference
            if test_case.led_spy_over_i2c is not None:
                # enable I2C monitoring
                test_case.led_spy_over_i2c.start(reset=reset)
            elif test_case.led_spy is not None and LED_ID.BACKLIGHT_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                # enable LED monitoring on the backlight LED
                test_case.led_spy.start([LED_ID.BACKLIGHT_LED])
            # end if
        # end def start_monitoring

        @classmethod
        def stop_monitoring(cls, test_case):
            """
            Stop the LED spy over I2C monitoring or LED backlight spy.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            fw_id = test_case.f.PRODUCT.F_ProductReference
            if test_case.led_spy_over_i2c is not None:
                # stop I2C monitoring
                test_case.led_spy_over_i2c.stop()
            elif test_case.led_spy is not None and LED_ID.BACKLIGHT_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS:
                # stop LED monitoring on the backlight LED
                test_case.led_spy.stop([LED_ID.BACKLIGHT_LED])
            # end if
        # end def stop_monitoring

        @classmethod
        def check_backlight_requirements(cls, test_case, effect_type, led_id_to_check, level=None,
                                         stationary_phase_duration=None, fade_in_phase_duration=None,
                                         fade_out_phase_duration=None, previous_effect=BacklightEffectType.NONE_EFFECT,
                                         layout_type=KeyboardMixin.LAYOUT.DEFAULT):
            """
            Verify the backlight requirements for the given effect type, level and duration (on the expected keys where
            it is played)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param effect_type: effect to check
            :type effect_type: ``Backlight.BacklightEffect``
            :param led_id_to_check: List of expected led id where the backlight effect is played
            :type led_id_to_check: ``list[int]``
            :param level: level to check (default is None and backlight level is not check) - OPTIONAL
            :type level: ``int`` or ``None``
            :param stationary_phase_duration: duration of the stationary phase in second (default is None and the
             duration of the stationary is not check) - OPTIONAL
            :type stationary_phase_duration: ``float`` or ``None``
            :param fade_in_phase_duration: duration of the fade in period in second (default is None and the duration
             of the fade in phase is not check) - OPTIONAL
            :type fade_in_phase_duration: ``float`` or ``None``
            :param fade_out_phase_duration: duration of the fade out period in second (default is None and the duration
             of the fade out phase is not check) - OPTIONAL
            :type fade_out_phase_duration: ``float`` or ``None``
            :param previous_effect: Backlight previous effect at the start of the recording - OPTIONAL
            :type previous_effect: ``BacklightEffectType`` or ``None``
            :param layout_type: keyboard international layout type - OPTIONAL
            :type layout_type: ``KeyboardMixin.LAYOUT``

            Note: This method can't be used for the Reaction effect. Use ``check_reaction_effect`` for Reaction effect
            """
            fw_id = test_case.f.PRODUCT.F_ProductReference
            if test_case.led_spy_over_i2c is not None or \
                    (test_case.led_spy is not None and LED_ID.BACKLIGHT_LED in GET_LED_LAYOUT_BY_ID[fw_id].LEDS):
                if test_case.led_backlight_parser is None:
                    # parse I2C or pwm data to led_values and timestamps lists
                    if test_case.led_spy_over_i2c is not None:
                        timestamps, led_values = test_case.led_spy_over_i2c.parse_backlight_i2c()
                    else:
                        timestamps, led_values = test_case.led_spy.parse_backlight_pwm()
                    # end if
                    test_case.led_backlight_parser = LedDataBacklightParser(timestamps=timestamps,
                                                                            led_values=led_values,
                                                                            fw_id=fw_id,
                                                                            led_id_to_check=led_id_to_check,
                                                                            previous_effect=previous_effect,
                                                                            layout_type=layout_type)
                    # end if
                # end if

                # Check backlight requirements
                test_case.assertTrue(
                    expr=test_case.led_backlight_parser.is_backlight_complying_with_requirement(
                        effect_type=effect_type,
                        led_id_to_check=led_id_to_check,
                        brightness_level=level,
                        stationary_phase_duration=stationary_phase_duration,
                        fade_in_phase_duration=fade_in_phase_duration,
                        fade_out_phase_duration=fade_out_phase_duration,
                        previous_effect=previous_effect),
                    msg='The backlight effect is not compliant with the requirement'
                )
            # end if
        # end def check_backlight_requirements

        @classmethod
        def check_reaction_effect(cls, test_case, keys_sequence, layout_type=KeyboardMixin.LAYOUT.DEFAULT):
            """
            Verify the reaction backlight effect follows the expected keys_sequence

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param keys_sequence: List of unique ``KEY_ID`` and its list of action name (make or break) with timestamp
            :type keys_sequence: ``list[KEY_ID, list[tuple(str, float)]]``
            :param layout_type: keyboard international layout type - OPTIONAL
            :type layout_type: ``KeyboardMixin.LAYOUT``
            """
            if test_case.led_spy_over_i2c is not None:
                # Check reaction backlight effect follows the expected keys_sequence
                test_case.assertTrue(
                    expr=test_case.led_spy_over_i2c.is_backlight_reaction_sequence_correct(sequence=keys_sequence,
                                                                                           layout_type=layout_type),
                    msg='The reaction effect is not correct'
                )
            # end if
        # end def check_reaction_effect
    # end class BacklightSpyHelper

    @classmethod
    def get_supported_backlight_effects(cls, test_case):
        """
        Get supported backlight effects

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: Backlight effect list
        :rtype: ``list[int]``

        :raise ``ValueError``: if input unsupported backlight effect mask
        """
        supported_effects = []
        supported_backlight_effect_list = HexList(test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_BacklightEffectList)
        for effect_mask in Backlight.SupportedBacklightEffectMask:
            if supported_backlight_effect_list & Numeral(effect_mask) > Numeral(0, byteCount=2):
                if effect_mask == Backlight.SupportedBacklightEffectMask.STATIC:
                    supported_effects.append(Backlight.BacklightEffect.STATIC_EFFECT)
                elif effect_mask == Backlight.SupportedBacklightEffectMask.NONE:
                    supported_effects.append(Backlight.BacklightEffect.NONE_EFFECT)
                elif effect_mask == Backlight.SupportedBacklightEffectMask.BREATHING_LIGHT:
                    supported_effects.append(Backlight.BacklightEffect.BREATHING_LIGHT_EFFECT)
                elif effect_mask == Backlight.SupportedBacklightEffectMask.CONTRAST:
                    supported_effects.append(Backlight.BacklightEffect.CONTRAST_EFFECT)
                elif effect_mask == Backlight.SupportedBacklightEffectMask.REACTION:
                    supported_effects.append(Backlight.BacklightEffect.REACTION_EFFECT)
                elif effect_mask == Backlight.SupportedBacklightEffectMask.RANDOM:
                    supported_effects.append(Backlight.BacklightEffect.RANDOM_EFFECT)
                elif effect_mask == Backlight.SupportedBacklightEffectMask.WAVES:
                    supported_effects.append(Backlight.BacklightEffect.WAVES_EFFECT)
                else:
                    raise ValueError(
                        f'Unsupported backlight effect list value in DUT test settings: '
                        f'{supported_backlight_effect_list}. The following bitmap is unknown: {effect_mask}')
                # end if
            # end if
        # end for
        return supported_effects
    # end def get_supported_backlight_effects

    @classmethod
    def get_default_options(cls, test_case):
        """
        Get the default options

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The default options
        :rtype: ``int``
        """
        return Numeral(test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_SupportedOptions)[0]
    # end def get_default_options

    @classmethod
    def get_inverted_default_capability(cls, test_case, backlight_mode=Backlight.Options.AUTOMATIC_MODE):
        """
        Get the inverted default options

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param backlight_mode: Backlight mode
        :type backlight_mode: ``Backlight.Options``

        :return: The default options
        :rtype: ``int``
        """
        default_capability = Numeral(test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_SupportedOptions)[0] & 0x07
        supported_capability = Numeral(test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_SupportedOptions)[1] & 0x07
        inverted_capability = supported_capability ^ default_capability
        _, feature_1982, _, _ = cls.HIDppHelper.get_parameters(test_case)
        return inverted_capability if feature_1982.VERSION < 3 else inverted_capability | backlight_mode
    # end def get_inverted_default_capability

    @classmethod
    def get_non_default_backlight_effect(cls, test_case):
        """
        Get the first supported backlight effect which is not the default one.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The first non-default backlight effect
        :rtype: ``int``
        """
        supported_effects = cls.get_supported_backlight_effects(test_case)
        default_effect = Numeral(test_case.f.PRODUCT.FEATURES.COMMON.BACKLIGHT.F_BacklightEffect)
        return next(iter([x for x in supported_effects if x != default_effect]), None)
    # end def get_non_default_backlight_effect

    @classmethod
    def compute_press_count_to_max_or_min_level(cls, test_case, to_max_level):
        """
        Compute the press count of backlight key to reach the max or min backlight level

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param to_max_level: Flag indicating if we target to reach the maximum backlight level
        :type to_max_level: ``bool``

        :return: The keystroke counter to reach the max or min backlight level
        :rtype: ``int``
        """
        current_level = to_int(cls.HIDppHelper.get_backlight_info(test_case).current_level)
        if to_max_level:
            press_count = Backlight.CurrentLevel.CURRENT_LEVEL_7 - current_level \
                if current_level < Backlight.CurrentLevel.CURRENT_LEVEL_7 else 0
        else:
            press_count = current_level - Backlight.CurrentLevel.CURRENT_LEVEL_0 \
                if current_level > Backlight.CurrentLevel.CURRENT_LEVEL_0 else 0
        # end if

        return press_count
    # end def compute_press_count_to_max_or_min_level

    @classmethod
    def compute_duration_to_max_or_min_level(cls, test_case, to_max_level):
        """
        Compute the duration of press and hold backlight key to reach the max or min backlight level

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param to_max_level: Flag indicating if we target to reach the maximum backlight level
        :type to_max_level: ``bool``

        :return: The duration to reach the max or min backlight level
        :rtype: ``float``
        """
        current_level = to_int(cls.HIDppHelper.get_backlight_info(test_case).current_level)
        if to_max_level:
            first_step_count = 1 if current_level < Backlight.CurrentLevel.CURRENT_LEVEL_7 else 0
            every_step_count = Backlight.CurrentLevel.CURRENT_LEVEL_7 - current_level - 1 \
                if current_level < Backlight.CurrentLevel.CURRENT_LEVEL_7 - 1 else 0
        else:
            first_step_count = 1 if current_level > Backlight.CurrentLevel.CURRENT_LEVEL_0 else 0
            every_step_count = current_level - Backlight.CurrentLevel.CURRENT_LEVEL_0 - 1 \
                if current_level > Backlight.CurrentLevel.CURRENT_LEVEL_0 + 1 else 0
        # end if

        return round((cls.BRIGHTNESS_KEYS_FIRST_STEP_TIMEOUT * first_step_count +
                      cls.BRIGHTNESS_KEYS_EVERY_STEP_TIMEOUT * every_step_count) *
                     BacklightTestUtils.BACKLIGHT_DURATION_5_PERCENT_MARGIN / 1000, 3)
    # end def compute_duration_to_max_or_min_level

    @classmethod
    def get_backlight_chunk(cls, test_case):
        """
        Get the backlight chunk data

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The backlight chunk data
        :rtype: ``BacklightChunk | BacklightChunkV3``
        """
        test_case.memory_manager.read_nvs()
        backlight_chunk_v2 = test_case.memory_manager.get_active_chunk_by_name(chunk_name="NVS_LEDBKLT_ID")
        _, feature_1982, _, _ = cls.HIDppHelper.get_parameters(test_case)
        return backlight_chunk_v2 if feature_1982.VERSION < 3 else BacklightChunkV3.fromHexList(
                HexList(backlight_chunk_v2.ref.clear_data[:backlight_chunk_v2.ref.chunk_length]))
    # end def get_backlight_chunk

    @classmethod
    def switch_backlight_mode(cls, test_case, backlight_mode):
        """
        Switch backlight mode with default options (wow, crown and pwr_save with default settings)

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param backlight_mode: Backlight mode
        :type backlight_mode: ``Backlight.Options``

        :return: The backlight chunk data
        :rtype: ``int``
        """
        return (cls.get_default_options(test_case) & 0x07) | backlight_mode
    # end def switch_backlight_mode

    @classmethod
    def delete_backlight_chunk(cls, test_case):
        """
        Delete the backlight chunk data

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        test_case.memory_manager.read_nvs()
        invalidated_chunk_count = test_case.memory_manager.invalidate_chunks(chunk_names=["NVS_LEDBKLT_ID"])
        if invalidated_chunk_count > 0:
            test_case.memory_manager.load_nvs()
        # end if
    # end def delete_backlight_chunk
# end class BacklightTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
