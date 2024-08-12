#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pytestbox.device.base.onboardprofilesutils
:brief: Helpers for ``OnboardProfiles`` feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from queue import Empty
from random import choice
from random import randint
from time import sleep

from pyhid.hid import HidConsumer
from pyhid.hid import HidKeyboard
from pyhid.hid import HidKeyboardBitmap
from pyhid.hid import HidMouse
from pyhid.hid import HidMouseNvidiaExtension
from pyhid.hid.usbhidusagetable import STANDARD_KEYS
from pyhid.hiddata import OS, HidData
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.onboardprofiles import ActiveProfileResolutionChangedEvent
from pyhid.hidpp.features.gaming.onboardprofiles import EndWriteResponse
from pyhid.hidpp.features.gaming.onboardprofiles import ExecuteMacroResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetActiveProfileResolutionResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetActiveProfileResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetCrcResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardModeResponse
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardProfilesInfoResponseV0
from pyhid.hidpp.features.gaming.onboardprofiles import GetOnboardProfilesInfoResponseV1
from pyhid.hidpp.features.gaming.onboardprofiles import GetProfileFieldsListResponse
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfilesFactory
from pyhid.hidpp.features.gaming.onboardprofiles import ReadDataResponse
from pyhid.hidpp.features.gaming.onboardprofiles import SetActiveProfileResolutionResponse
from pyhid.hidpp.features.gaming.onboardprofiles import SetActiveProfileResponse
from pyhid.hidpp.features.gaming.onboardprofiles import SetOnboardModeResponse
from pyhid.hidpp.features.gaming.onboardprofiles import WriteDataResponse
from pyhid.hidpp.features.mouse.extendedadjustabledpi import SensorDpiParametersEvent
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.profileformat import DpiResolutions
from pylibrary.mcu.profileformat import ProfileButton
from pylibrary.mcu.profileformat import ProfileDirectory
from pylibrary.mcu.profileformat import ProfileFieldName
from pylibrary.mcu.profileformat import ProfileFormatV1
from pylibrary.mcu.profileformat import ProfileFormatV2
from pylibrary.mcu.profileformat import ProfileFormatV3
from pylibrary.mcu.profileformat import ProfileFormatV4
from pylibrary.mcu.profileformat import ProfileFormatV5
from pylibrary.mcu.profileformat import ProfileFormatV6
from pylibrary.mcu.profileformat import ProfileMacro
from pylibrary.tools.crc import Crc16ccitt
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.reportrateutils import ReportRateTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OnboardProfilesTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``OnboardProfiles`` feature
    """
    PROFILE_NAME_BYTE_LENGTH = 48

    class GetOnboardProfilesInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetOnboardProfilesInfo`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetOnboardProfilesInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES
            fields_to_check = {
                "memory_model_id": (cls.check_memory_model_id, config.F_MemoryModelID),
                "profile_format_id": (cls.check_profile_format_id, config.F_ProfileFormatID),
                "macro_format_id": (cls.check_macro_format_id, config.F_MacroFormatID),
                "profile_count": (cls.check_profile_count, config.F_ProfileCount),
                "profile_count_oob": (cls.check_profile_count_oob, config.F_ProfileCountOOB),
                "button_count": (cls.check_button_count, config.F_ButtonCount),
                "sector_count": (cls.check_sector_count, config.F_SectorCount),
                "sector_size": (cls.check_sector_size, config.F_SectorSize),
                "mechanical_layout": (cls.check_mechanical_layout, config.F_MechanicalLayout),
                "various_info": (cls.check_various_info, config.F_VariousInfo),
                "sector_count_rule": (cls.check_sector_count_rule, config.F_SectorCountRule)
            }

            feature_8100_index, feature_8100, device_index, _ = \
                OnboardProfilesTestUtils.HIDppHelper.get_parameters(test_case)
            if feature_8100.VERSION > 0:
                fields_to_check['supported_host_layer'] = \
                    (cls.check_supported_host_layer, HexList(Numeral(config.F_SupportedHostLayer)))
            # end if
            return fields_to_check
        # end def get_default_check_map

        @staticmethod
        def check_memory_model_id(test_case, response, expected):
            """
            Check memory_model_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.memory_model_id),
                msg=f"The memory_model_id parameter differs "
                    f"(expected:{expected}, obtained:{response.memory_model_id})")
        # end def check_memory_model_id

        @staticmethod
        def check_profile_format_id(test_case, response, expected):
            """
            Check profile_format_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.profile_format_id),
                msg=f"The profile_format_id parameter differs "
                    f"(expected:{expected}, obtained:{response.profile_format_id})")
        # end def check_profile_format_id

        @staticmethod
        def check_macro_format_id(test_case, response, expected):
            """
            Check macro_format_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.macro_format_id),
                msg=f"The macro_format_id parameter differs "
                    f"(expected:{expected}, obtained:{response.macro_format_id})")
        # end def check_macro_format_id

        @staticmethod
        def check_profile_count(test_case, response, expected):
            """
            Check profile_count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.profile_count),
                msg=f"The profile_count parameter differs "
                    f"(expected:{expected}, obtained:{response.profile_count})")
        # end def check_profile_count

        @staticmethod
        def check_profile_count_oob(test_case, response, expected):
            """
            Check profile_count_oob field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.profile_count_oob),
                msg=f"The profile_count_oob parameter differs "
                    f"(expected:{expected}, obtained:{response.profile_count_oob})")
        # end def check_profile_count_oob

        @staticmethod
        def check_button_count(test_case, response, expected):
            """
            Check button_count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.button_count),
                msg=f"The button_count parameter differs "
                    f"(expected:{expected}, obtained:{response.button_count})")
        # end def check_button_count

        @staticmethod
        def check_sector_count(test_case, response, expected):
            """
            Check sector_count field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sector_count),
                msg=f"The sector_count parameter differs "
                    f"(expected:{expected}, obtained:{response.sector_count})")
        # end def check_sector_count

        @staticmethod
        def check_sector_size(test_case, response, expected):
            """
            Check sector_size field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sector_size),
                msg=f"The sector_size parameter differs "
                    f"(expected:{expected}, obtained:{response.sector_size})")
        # end def check_sector_size

        @staticmethod
        def check_mechanical_layout(test_case, response, expected):
            """
            Check mechanical_layout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.mechanical_layout),
                msg=f"The mechanical_layout parameter differs "
                    f"(expected:{expected}, obtained:{response.mechanical_layout})")
        # end def check_mechanical_layout

        @staticmethod
        def check_various_info(test_case, response, expected):
            """
            Check various_info field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.various_info),
                msg=f"The various_info parameter differs "
                    f"(expected:{expected}, obtained:{response.various_info})")
        # end def check_various_info

        @staticmethod
        def check_sector_count_rule(test_case, response, expected):
            """
            Check sector_count_rule field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sector_count_rule),
                msg=f"The sector_count_rule parameter differs "
                    f"(expected:{expected}, obtained:{response.sector_count_rule})")
        # end def check_sector_count_rule

        @staticmethod
        def check_supported_host_layer(test_case, response, expected):
            """
            Check supported_host_layer field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardProfilesInfoResponse to check
            :type response: ``GetOnboardProfilesInfoResponseV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.supported_host_layer),
                msg=f"The supported_host_layer parameter differs "
                    f"(expected:{expected}, obtained:{response.supported_host_layer})")
        # end def check_supported_host_layer
    # end class GetOnboardProfilesInfoResponseChecker

    class GetOnboardModeResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetOnboardMode`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetOnboardModeResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "onboard_mode": (cls.check_onboard_mode, OnboardProfiles.Mode.ONBOARD_MODE)
            }
        # end def get_default_check_map

        @staticmethod
        def check_onboard_mode(test_case, response, expected):
            """
            Check onboard_mode field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetOnboardModeResponse to check
            :type response: ``GetOnboardModeResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.onboard_mode),
                msg=f"The onboard_mode parameter differs "
                    f"(expected:{expected}, obtained:{response.onboard_mode})")
        # end def check_onboard_mode
    # end class GetOnboardModeResponseChecker

    class GetActiveProfileResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetActiveProfile`` and ``ProfileActivatedEvent`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetActiveProfileResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            oob_onboard_profile = 0x0101
            return {
                "profile_id": (cls.check_profile_id, oob_onboard_profile)
            }
        # end def get_default_check_map

        @staticmethod
        def check_profile_id(test_case, response, expected):
            """
            Check profile_id field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetActiveProfileResponse to check
            :type response: ``GetActiveProfileResponse`` or ``ProfileActivatedEvent``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.profile_id),
                msg=f"The profile_id parameter differs "
                    f"(expected:{expected}, obtained:{response.profile_id})")
        # end def check_profile_id
    # end class GetActiveProfileResponseChecker

    class ReadDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``ReadData`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``ReadDataResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            default_value_of_unused_fields = HexList([0xFF] * 16)
            return {
                "data": (cls.check_data, default_value_of_unused_fields)
            }
        # end def get_default_check_map

        @staticmethod
        def check_data(test_case, response, expected):
            """
            Check data field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ReadDataResponse to check
            :type response: ``ReadDataResponse``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=expected,
                obtained=response.data,
                msg=f"The data parameter differs "
                    f"(expected:{expected}, obtained:{response.data})")
        # end def check_data
    # end class ReadDataResponseChecker

    class WriteDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``WriteData`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``WriteDataResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "frame_nb": (cls.check_frame_nb, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_frame_nb(test_case, response, expected):
            """
            Check frame_nb field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: WriteDataResponse to check
            :type response: ``WriteDataResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.frame_nb),
                msg=f"The frame_nb parameter differs "
                    f"(expected:{expected}, obtained:{response.frame_nb})")
        # end def check_frame_nb
    # end class WriteDataResponseChecker

    class GetCrcResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetCrc`` response
        """

        CRC_IN_UNUSED_SECTOR = 0xB92A

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCrcResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(count=test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_SectorCount)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, count):
            """
            Get the check methods and expected values for the ``GetCrcResponse`` API

            :param count: The number of sector
            :type count: ``int``

            :return: Check map
            :rtype: ``dict``
            """
            max_crc_count = 8
            # FW computes CRC by 0xFF (253 bytes) if cannot find the profile in NVS. So the CRC result is 0xB92A.
            crc_answer = {}
            for crc_idx in range(1, max_crc_count + 1):
                method = getattr(OnboardProfilesTestUtils.GetCrcResponseChecker, f'check_crc_{crc_idx}')
                crc_answer[f'crc_{crc_idx}'] = (method, cls.CRC_IN_UNUSED_SECTOR) if crc_idx <= count else (method, 0)
            # end for
            return crc_answer
        # end def get_check_map

        @staticmethod
        def check_crc_1(test_case, response, expected):
            """
            Check crc_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_1),
                msg=f"The crc_1 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_1})")
        # end def check_crc_1

        @staticmethod
        def check_crc_2(test_case, response, expected):
            """
            Check crc_2 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_2),
                msg=f"The crc_2 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_2})")
        # end def check_crc_2

        @staticmethod
        def check_crc_3(test_case, response, expected):
            """
            Check crc_3 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_3),
                msg=f"The crc_3 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_3})")
        # end def check_crc_3

        @staticmethod
        def check_crc_4(test_case, response, expected):
            """
            Check crc_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_4),
                msg=f"The crc_4 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_4})")
        # end def check_crc_4

        @staticmethod
        def check_crc_5(test_case, response, expected):
            """
            Check crc_5 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_5),
                msg=f"The crc_5 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_5})")
        # end def check_crc_5

        @staticmethod
        def check_crc_6(test_case, response, expected):
            """
            Check crc_6 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_6),
                msg=f"The crc_6 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_6})")
        # end def check_crc_6

        @staticmethod
        def check_crc_7(test_case, response, expected):
            """
            Check crc_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_7),
                msg=f"The crc_7 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_7})")
        # end def check_crc_7

        @staticmethod
        def check_crc_8(test_case, response, expected):
            """
            Check crc_8 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCrcResponse to check
            :type response: ``GetCrcResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc_8),
                msg=f"The crc_8 parameter differs "
                    f"(expected:{hex(to_int(expected))}, obtained:{response.crc_8})")
        # end def check_crc_8
    # end class GetCrcResponseChecker

    class GetActiveProfileResolutionResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetActiveProfileResolution`` and ``ActiveProfileResolutionChangedEvent`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetActiveProfileResolutionResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            res_index = test_case.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[0]
            return {
                "resolution_index": (cls.check_resolution_index, res_index)
            }
        # end def get_default_check_map

        @staticmethod
        def check_resolution_index(test_case, response, expected):
            """
            Check resolution_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetActiveProfileResolutionResponse to check
            :type response: ``GetActiveProfileResolutionResponse`` or ``ActiveProfileResolutionChangedEvent``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.resolution_index),
                msg=f"The resolution_index parameter differs "
                    f"(expected:{expected}, obtained:{response.resolution_index})")
        # end def check_resolution_index
    # end class GetActiveProfileResolutionResponseChecker

    class GetProfileFieldsListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetProfileFieldsList`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetProfileFieldsListResponse`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            fields_list = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_FieldsList
            return {
                "fields_list": (cls.check_fields_list, HexList(Numeral(fields_list)))
            }
        # end def get_default_check_map

        @staticmethod
        def check_fields_list(test_case, response, expected):
            """
            Check fields_list field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetProfileFieldsListResponse to check
            :type response: ``GetProfileFieldsListResponse``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=expected,
                obtained=response.fields_list,
                msg=f"The fields_list parameter differs "
                    f"(expected:{expected}, obtained:{response.fields_list})")
        # end def check_fields_list
    # end class GetProfileFieldsListResponseChecker

    class ProfileActivatedEventChecker(GetActiveProfileResponseChecker):
        """
        Check ``ProfileActivatedEvent`` response
        """
    # end class ProfileActivatedEventChecker

    class ActiveProfileResolutionChangedEventChecker(GetActiveProfileResolutionResponseChecker):
        """
        Check ``ActiveProfileResolutionChangedEvent`` response
        """
    # end class ActiveProfileResolutionChangedEventChecker

    class ProfileChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``Profile`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``Profile``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return cls.get_check_map(test_case, 0)
        # end def get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, index):
            """
            Get the check methods and expected values for the ``Profile``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param index: The index of specific profile
            :type index: ``int``

            :return: Check map
            :rtype: ``dict``

            :raise ``ValueError``: If input an unsupported profile format id
            """
            get_feature = test_case.config_manager.get_feature
            _id = ConfigurationManager.ID
            profile_format_id = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileFormatID
            if profile_format_id < ProfileFormatV6.ID:
                expected_btn_fields = get_feature(_id.OOB_PROFILES_BTN_16)[index]
                expected_g_shift_btn_fields = get_feature(_id.OOB_PROFILES_G_SHIFT_BTN_16)[index]
            elif profile_format_id == ProfileFormatV6.ID:
                expected_btn_fields = get_feature(_id.OOB_PROFILES_BTN_12)[index]
                expected_g_shift_btn_fields = get_feature(_id.OOB_PROFILES_G_SHIFT_BTN_12)[index]
            else:
                raise ValueError(f'Unsupported profile format id: {profile_format_id}')
            # end if

            return {
                "report_rate": (cls.check_report_rate, get_feature(_id.OOB_PROFILES_REPORT_RATE)[index]),
                "default_dpi_index": (cls.check_default_dpi_index,
                                      get_feature(_id.OOB_PROFILES_DEFAULT_DPI_INDEX)[index]),
                "shift_dpi_index": (cls.check_shift_dpi_index,
                                    get_feature(_id.OOB_PROFILES_SHIFT_DPI_INDEX)[index]),
                "dpi_0_to_4": (cls.check_dpi_0_to_4,
                               DpiResolutions.from_dpi_list(get_feature(_id.OOB_PROFILES_DPI_LIST)[index])),
                "led_color_red": (cls.check_led_color_red, get_feature(_id.OOB_PROFILES_LED_COLOR_RED)[index]),
                "led_color_blue": (cls.check_led_color_green, get_feature(_id.OOB_PROFILES_LED_COLOR_GREEN)[index]),
                "led_color_green": (cls.check_led_color_blue, get_feature(_id.OOB_PROFILES_LED_COLOR_BLUE)[index]),
                "power_mode": (cls.check_power_mode, get_feature(_id.OOB_PROFILES_POWER_MODE)[index]),
                "angle_snapping": (cls.check_angle_snapping, get_feature(_id.OOB_PROFILES_ANGLE_SNAPPING)[index]),
                "reserved_14": (cls.check_reserved_14, None),
                "btn_0_to_15": (cls.check_btn_0_to_15, get_feature(_id.OOB_PROFILES_BTN_16)[index]),
                "g_shift_btn_0_to_15": (cls.check_g_shift_btn_0_to_15,
                                        get_feature(_id.OOB_PROFILES_G_SHIFT_BTN_16)[index]),
                "profile_name_0_to_23": (cls.check_profile_name_0_to_23, get_feature(_id.OOB_PROFILES_NAME)[index]),
                "reserved_45": (cls.check_reserved_45, None),
                "crc": (cls.check_crc, get_feature(_id.OOB_PROFILES_CRC)[index]),
                # V2 & V3
                "logo_effect": (cls.check_logo_effect, get_feature(_id.OOB_PROFILES_LOGO_EFFECT)[index]),
                "side_effect": (cls.check_side_effect, get_feature(_id.OOB_PROFILES_SIDE_EFFECT)[index]),
                "reserved_23": (cls.check_reserved_23, None),
                # V4 & V5
                "write_counter": (cls.check_write_counter, get_feature(_id.OOB_PROFILES_WRITE_COUNTER)[index]),
                "reserved_8": (cls.check_reserved_8, None),
                "pwr_save_timeout": (cls.check_power_save_timeout,
                                     get_feature(_id.OOB_PROFILES_POWER_SAVE_TIMEOUT)[index]),
                "pwr_off_timeout": (cls.check_power_off_timeout,
                                    get_feature(_id.OOB_PROFILES_POWER_OFF_TIMEOUT)[index]),
                # V4
                "logo_active_effect": (cls.check_logo_active_effect,
                                       get_feature(_id.OOB_PROFILES_LOGO_ACTIVE_EFFECT)[index]),
                "side_active_effect": (cls.check_side_active_effect,
                                       get_feature(_id.OOB_PROFILES_SIDE_ACTIVE_EFFECT)[index]),
                "logo_passive_effect": (cls.check_logo_passive_effect,
                                        get_feature(_id.OOB_PROFILES_LOGO_PASSIVE_EFFECT)[index]),
                "side_passive_effect": (cls.check_side_passive_effect,
                                        get_feature(_id.OOB_PROFILES_SIDE_PASSIVE_EFFECT)[index]),
                "reserved_1": (cls.check_reserved_1, None),
                # V5
                "cluster_0_active_effect": (cls.check_cluster_0_active_effect,
                                            get_feature(_id.OOB_PROFILES_CLUSTER_0_ACTIVE_EFFECT)[index]),
                "cluster_1_active_effect": (cls.check_cluster_1_active_effect,
                                            get_feature(_id.OOB_PROFILES_CLUSTER_1_ACTIVE_EFFECT)[index]),
                "cluster_0_passive_effect": (cls.check_cluster_0_passive_effect,
                                             get_feature(_id.OOB_PROFILES_CLUSTER_0_PASSIVE_EFFECT)[index]),
                "cluster_1_passive_effect": (cls.check_cluster_1_passive_effect,
                                             get_feature(_id.OOB_PROFILES_CLUSTER_1_PASSIVE_EFFECT)[index]),
                "lightning_flag": (cls.check_lightning_flag,
                                   get_feature(_id.OOB_PROFILES_LIGHTNING_FLAG)[index]),
                # V6
                "report_rate_wireless": (cls.check_report_rate_wireless,
                                         get_feature(_id.OOB_PROFILES_REPORT_RATE_WIRELESS)[index]),
                "report_rate_wired": (cls.check_report_rate_wired,
                                      get_feature(_id.OOB_PROFILES_REPORT_RATE_WIRED)[index]),
                "dpi_xy_0_to_4": (cls.check_dpi_xy_0_to_4,
                                  DpiResolutions.from_dpi_list(get_feature(_id.OOB_PROFILES_DPI_XY_LIST)[index])),
                "dpi_delta_x": (cls.check_dpi_delta_x, get_feature(_id.OOB_PROFILES_DPI_DELTA_X)[index]),
                "dpi_delta_y": (cls.check_dpi_delta_y, get_feature(_id.OOB_PROFILES_DPI_DELTA_Y)[index]),
                "reserved_7": (cls.check_reserved_7, None),
                "btn_0_to_11": (cls.check_btn_0_to_11, get_feature(_id.OOB_PROFILES_BTN_12)[index]),
                "reserved_16": (cls.check_reserved_16, None),
                "g_shift_btn_0_to_11": (cls.check_g_shift_btn_0_to_11,
                                        get_feature(_id.OOB_PROFILES_G_SHIFT_BTN_12)[index]),
                # Common fields
                ProfileFieldName.BUTTON: (cls.check_button_fields, expected_btn_fields),
                ProfileFieldName.G_SHIFT_BUTTON: (cls.check_g_shift_button_fields, expected_g_shift_btn_fields),
            }
        # end def get_check_map

        @staticmethod
        def check_report_rate(test_case, response, expected):
            """
            Check report_rate field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.report_rate),
                msg=f"The report_rate parameter differs "
                    f"(expected:{expected}, obtained:{response.report_rate})")
        # end def check_report_rate

        @staticmethod
        def check_report_rate_wireless(test_case, response, expected):
            """
            Check report_rate_wireless field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.report_rate_wireless),
                msg=f"The report_rate_wireless parameter differs "
                    f"(expected:{expected}, obtained:{response.report_rate_wireless})")
        # end def check_report_rate_wireless

        @staticmethod
        def check_report_rate_wired(test_case, response, expected):
            """
            Check report_rate_wired field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.report_rate_wired),
                msg=f"The report_rate_wired parameter differs "
                    f"(expected:{expected}, obtained:{response.report_rate_wired})")
        # end def check_report_rate_wired

        @staticmethod
        def check_default_dpi_index(test_case, response, expected):
            """
            Check default_dpi_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.default_dpi_index),
                msg=f"The default_dpi_index parameter differs "
                    f"(expected:{expected}, obtained:{response.default_dpi_index})")
        # end def check_default_dpi_index

        @staticmethod
        def check_shift_dpi_index(test_case, response, expected):
            """
            Check shift_dpi_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.shift_dpi_index),
                msg=f"The shift_dpi_index parameter differs "
                    f"(expected:{expected}, obtained:{response.shift_dpi_index})")
        # end def check_shift_dpi_index

        @staticmethod
        def check_dpi_0_to_4(test_case, response, expected):
            """
            Check dpi_0_to_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.dpi_0_to_4,
                msg=f"The dpi_0_to_4 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.dpi_0_to_4})")
        # end def check_dpi_0_to_4

        @staticmethod
        def check_dpi_xy_0_to_4(test_case, response, expected):
            """
            Check dpi_xy_0_to_4 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.dpi_xy_0_to_4,
                msg=f"The dpi_xy_0_to_4 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.dpi_xy_0_to_4})")
        # end def check_dpi_xy_0_to_4

        @staticmethod
        def check_dpi_delta_x(test_case, response, expected):
            """
            Check dpi_delta_x field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_delta_x),
                msg=f"The dpi_delta_x parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_delta_x})")
        # end def check_dpi_delta_x

        @staticmethod
        def check_dpi_delta_y(test_case, response, expected):
            """
            Check dpi_delta_y field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.dpi_delta_y),
                msg=f"The dpi_delta_y parameter differs "
                    f"(expected:{expected}, obtained:{response.dpi_delta_y})")
        # end def check_dpi_delta_y

        @staticmethod
        def check_led_color_red(test_case, response, expected):
            """
            Check led_color_red field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.led_color_red),
                msg=f"The led_color_red parameter differs "
                    f"(expected:{expected}, obtained:{response.led_color_red})")
        # end def check_led_color_red

        @staticmethod
        def check_led_color_green(test_case, response, expected):
            """
            Check led_color_green field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.led_color_green),
                msg=f"The led_color_green parameter differs "
                    f"(expected:{expected}, obtained:{response.led_color_green})")
        # end def check_led_color_green

        @staticmethod
        def check_led_color_blue(test_case, response, expected):
            """
            Check led_color_blue field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.led_color_blue),
                msg=f"The led_color_blue parameter differs "
                    f"(expected:{expected}, obtained:{response.led_color_blue})")
        # end def check_led_color_blue

        @staticmethod
        def check_power_mode(test_case, response, expected):
            """
            Check power_mode field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.power_mode),
                msg=f"The power_mode parameter differs "
                    f"(expected:{expected}, obtained:{response.power_mode})")
        # end def check_power_mode

        @staticmethod
        def check_angle_snapping(test_case, response, expected):
            """
            Check angle_snapping field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.angle_snapping),
                msg=f"The angle_snapping parameter differs "
                    f"(expected:{expected}, obtained:{response.angle_snapping})")
        # end def check_angle_snapping

        @staticmethod
        def check_write_counter(test_case, response, expected):
            """
            Check write_counter field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4`` or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.write_counter),
                msg=f"The write_counter parameter differs "
                    f"(expected:{expected}, obtained:{response.write_counter})")
        # end def check_write_counter

        @staticmethod
        def check_reserved_1(test_case, response, expected):
            """
            Check reserved_1 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_1 != HexList(0) and response.reserved_1 != HexList(0xFF):
                warnings.warn(f'The reserved_1 contains none empty data: {response.reserved_1}')
            # end if
        # end def check_reserved_1

        @staticmethod
        def check_reserved_7(test_case, response, expected):
            """
            Check reserved_7 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_7 != HexList([0] * 7) and response.reserved_7 != HexList([0xFF] * 7):
                warnings.warn(f'The reserved_7 contains none empty data: {response.reserved_7}')
            # end if
        # end def check_reserved_7

        @staticmethod
        def check_reserved_8(test_case, response, expected):
            """
            Check reserved_8 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4`` or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_8 != HexList([0] * 8) and response.reserved_8 != HexList([0xFF] * 8):
                warnings.warn(f'The reserved_8 contains none empty data: {response.reserved_8}')
            # end if
        # end def check_reserved_8

        @staticmethod
        def check_reserved_14(test_case, response, expected):
            """
            Check reserved_14 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_14 != HexList([0] * 14) and response.reserved_14 != HexList([0xFF] * 14):
                warnings.warn(f'The reserved_14 contains none empty data: {response.reserved_14}')
            # end if
        # end def check_reserved_14

        @staticmethod
        def check_reserved_16(test_case, response, expected):
            """
            Check reserved_16 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_16 != HexList([0] * 16) and response.reserved_16 != HexList([0xFF] * 16):
                warnings.warn(f'The reserved_16 contains none empty data: {response.reserved_16}')
            # end if
        # end def check_reserved_16

        @staticmethod
        def check_reserved_23(test_case, response, expected):
            """
            Check reserved_23 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV2`` or ``ProfileFormatV3``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_23 != HexList([0] * 23) and response.reserved_23 != HexList([0xFF] * 23):
                warnings.warn(f'The reserved_23 contains none empty data: {response.reserved_23}')
            # end if
        # end def check_reserved_23

        @staticmethod
        def check_reserved_45(test_case, response, expected):
            """
            Check reserved_45 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            if response.reserved_45 != HexList([0] * 45) and response.reserved_45 != HexList([0xFF] * 45):
                warnings.warn(f'The reserved_45 contains none empty data: {response.reserved_45}')
            # end if
        # end def check_reserved_45

        @staticmethod
        def check_power_save_timeout(test_case, response, expected):
            """
            Check power_save_timeout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4`` or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.power_save_timeout),
                msg=f"The power_save_timeout parameter differs "
                    f"(expected:{expected}, obtained:{to_int(response.power_save_timeout)})")
        # end def check_power_save_timeout

        @staticmethod
        def check_power_off_timeout(test_case, response, expected):
            """
            Check power_off_timeout field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4`` or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=expected,
                obtained=to_int(response.power_off_timeout),
                msg=f"The power_off_timeout parameter differs "
                    f"(expected:{expected}, obtained:{to_int(response.power_off_timeout)})")
        # end def check_power_off_timeout

        @staticmethod
        def check_btn_0_to_15(test_case, response, expected):
            """
            Check btn_0_to_15 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.btn_0_to_15,
                msg=f"The btn_0_to_15 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.btn_0_to_15})")
        # end def check_btn_0_to_15

        @staticmethod
        def check_btn_0_to_11(test_case, response, expected):
            """
            Check btn_0_to_11 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.btn_0_to_11,
                msg=f"The btn_0_to_11 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.btn_0_to_11})")
        # end def check_btn_0_to_11

        @staticmethod
        def check_button_fields(test_case, response, expected):
            """
            Check button_fields in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.button_fields,
                msg=f"The button_fields parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.button_fields})")
        # end def check_button_fields

        @staticmethod
        def check_g_shift_btn_0_to_15(test_case, response, expected):
            """
            Check g_shift_btn_0_to_15 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.g_shift_btn_0_to_15,
                msg=f"The g_shift_btn_0_to_15 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.g_shift_btn_0_to_15})")
        # end def check_g_shift_btn_0_to_15

        @staticmethod
        def check_g_shift_btn_0_to_11(test_case, response, expected):
            """
            Check g_shift_btn_0_to_11 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.g_shift_btn_0_to_11,
                msg=f"The g_shift_btn_0_to_11 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.g_shift_btn_0_to_11})")
        # end def check_g_shift_btn_0_to_11

        @staticmethod
        def check_g_shift_button_fields(test_case, response, expected):
            """
            Check g_shift_button_fields in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.g_shift_button_fields,
                msg=f"The g_shift_button_fields parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.g_shift_button_fields})")
        # end def check_g_shift_button_fields

        @staticmethod
        def check_profile_name_0_to_23(test_case, response, expected):
            """
            Check profile_name_0_to_23 field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.profile_name_0_to_23,
                msg=f"The profile_name_0_to_23 parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.profile_name_0_to_23})")
        # end def check_profile_name_0_to_23

        @staticmethod
        def check_logo_effect(test_case, response, expected):
            """
            Check logo_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV2`` or ``ProfileFormatV3``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.logo_effect,
                msg=f"The logo_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.logo_effect})")
        # end def check_logo_effect

        @staticmethod
        def check_side_effect(test_case, response, expected):
            """
            Check side_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV2`` or ``ProfileFormatV3``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.side_effect,
                msg=f"The side_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.side_effect})")
        # end def check_side_effect

        @staticmethod
        def check_logo_active_effect(test_case, response, expected):
            """
            Check logo_active_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.logo_active_effect,
                msg=f"The logo_active_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.logo_active_effect})")
        # end def check_logo_active_effect

        @staticmethod
        def check_side_active_effect(test_case, response, expected):
            """
            Check side_active_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.side_active_effect,
                msg=f"The side_active_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.side_active_effect})")
        # end def check_side_active_effect

        @staticmethod
        def check_logo_passive_effect(test_case, response, expected):
            """
            Check logo_passive_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.logo_passive_effect,
                msg=f"The logo_passive_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.logo_passive_effect})")
        # end def check_logo_passive_effect

        @staticmethod
        def check_side_passive_effect(test_case, response, expected):
            """
            Check side_passive_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV4``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.side_passive_effect,
                msg=f"The side_passive_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.side_passive_effect})")
        # end def check_side_passive_effect

        @staticmethod
        def check_cluster_0_active_effect(test_case, response, expected):
            """
            Check cluster_0_active_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.cluster_0_active_effect,
                msg=f"The cluster_0_active_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.cluster_0_active_effect})")
        # end def check_cluster_0_active_effect

        @staticmethod
        def check_cluster_1_active_effect(test_case, response, expected):
            """
            Check cluster_1_active_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.cluster_1_active_effect,
                msg=f"The cluster_1_active_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.cluster_1_active_effect})")
        # end def check_cluster_1_active_effect

        @staticmethod
        def check_cluster_0_passive_effect(test_case, response, expected):
            """
            Check cluster_0_passive_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.cluster_0_passive_effect,
                msg=f"The cluster_0_passive_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.cluster_0_passive_effect})")
        # end def check_cluster_0_passive_effect

        @staticmethod
        def check_cluster_1_passive_effect(test_case, response, expected):
            """
            Check cluster_1_passive_effect field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``list`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=response.cluster_1_passive_effect,
                msg=f"The cluster_1_passive_effect parameter differs "
                    f"(expected:{HexList(expected)}, obtained:{response.cluster_1_passive_effect})")
        # end def check_cluster_1_passive_effect

        @staticmethod
        def check_lightning_flag(test_case, response, expected):
            """
            Check lightning_flag field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.lightning_flag),
                msg=f"The lightning_flag parameter differs "
                    f"(expected:{expected}, obtained:{response.lightning_flag})")
        # end def check_lightning_flag

        @staticmethod
        def check_crc(test_case, response, expected):
            """
            Check crc field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: ProfileFormat to check
            :type response: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                            or ``ProfileFormatV5`` or ``ProfileFormatV6``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.crc),
                msg=f"The crc parameter differs "
                    f"(expected:{expected}, obtained:{response.crc})")
        # end def check_crc
    # end class ProfileChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=OnboardProfiles.FEATURE_ID, factory=OnboardProfilesFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_onboard_profiles_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetOnboardProfilesInfo``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetOnboardProfilesInfoResponse
            :rtype: ``GetOnboardProfilesInfoResponseV0`` or ``GetOnboardProfilesInfoResponseV1``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.get_onboard_profiles_info_cls(
                device_index, feature_8100_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.get_onboard_profiles_info_response_cls)
            return response
        # end def get_onboard_profiles_info

        @classmethod
        def set_onboard_mode(cls, test_case, onboard_mode, device_index=None, port_index=None):
            """
            Process ``SetOnboardMode``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param onboard_mode: Indicates the device onboard mode.
            :type onboard_mode: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetOnboardModeResponse
            :rtype: ``SetOnboardModeResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.set_onboard_mode_cls(
                device_index, feature_8100_index,
                onboard_mode=onboard_mode)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.set_onboard_mode_response_cls)
            return response
        # end def set_onboard_mode

        @classmethod
        def get_onboard_mode(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetOnboardMode``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetOnboardModeResponse
            :rtype: ``GetOnboardModeResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.get_onboard_mode_cls(
                device_index, feature_8100_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.get_onboard_mode_response_cls)
            return response
        # end def get_onboard_mode

        @classmethod
        def set_active_profile(cls, test_case, profile_id, device_index=None, port_index=None):
            """
            Process ``SetActiveProfile``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_id: Indicates the onboard profile to activate.
            :type profile_id: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetActiveProfileResponse
            :rtype: ``SetActiveProfileResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.set_active_profile_cls(
                device_index, feature_8100_index,
                profile_id=profile_id)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.set_active_profile_response_cls)
            return response
        # end def set_active_profile

        @classmethod
        def get_active_profile(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetActiveProfile``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetActiveProfileResponse
            :rtype: ``GetActiveProfileResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.get_active_profile_cls(
                device_index, feature_8100_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.get_active_profile_response_cls)
            return response
        # end def get_active_profile

        @classmethod
        def read_data(cls, test_case, sector_id, sub_address, read_count=0, device_index=None, port_index=None):
            """
            Process ``ReadData``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sector_id: Sector to read from
            :type sector_id: ``int`` or ``HexList``
            :param sub_address: Sub address to read from
            :type sub_address: ``int`` or ``HexList``
            :param read_count: Number of bytes to read - OPTIONAL
            :type read_count: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ReadDataResponse
            :rtype: ``ReadDataResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.read_data_cls(
                device_index, feature_8100_index,
                sector_id=sector_id,
                sub_address=sub_address,
                read_count=read_count)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.read_data_response_cls)
            return response
        # end def read_data

        @classmethod
        def start_write(cls, test_case, sector_id, sub_address, write_count, device_index=None, port_index=None):
            """
            Process ``StartWrite``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sector_id: Sector to write to (final destination)
            :type sector_id: ``int`` or ``HexList``
            :param sub_address: Sub address to write to (final destination)
            :type sub_address: ``int`` or ``HexList``
            :param write_count: Number of bytes to write
            :type write_count: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: StartWriteResponse
            :rtype: ``StartWriteResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.start_write_cls(
                device_index, feature_8100_index,
                sector_id=sector_id,
                sub_address=sub_address,
                write_count=write_count)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.start_write_response_cls)
            return response
        # end def start_write

        @classmethod
        def write_data(cls, test_case, data, device_index=None, port_index=None):
            """
            Process ``WriteData``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param data: Data to write
            :type data: ``list`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: WriteDataResponse
            :rtype: ``WriteDataResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.write_data_cls(device_index, feature_8100_index, data=data)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.write_data_response_cls)
            return response
        # end def write_data

        @classmethod
        def end_write(cls, test_case, device_index=None, port_index=None):
            """
            Process ``EndWrite``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: EndWriteResponse
            :rtype: ``EndWriteResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.end_write_cls(device_index, feature_8100_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.end_write_response_cls)
            return response
        # end def end_write

        @classmethod
        def execute_macro(cls, test_case, sector_id, sub_address, device_index=None, port_index=None):
            """
            Process ``ExecuteMacro``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sector_id: Sector to execute
            :type sector_id: ``int`` or ``HexList``
            :param sub_address: Sub address to execute
            :type sub_address: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ExecuteMacroResponse
            :rtype: ``ExecuteMacroResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.execute_macro_cls(
                device_index, feature_8100_index,
                sector_id=sector_id,
                sub_address=sub_address)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.execute_macro_response_cls)
            return response
        # end def execute_macro

        @classmethod
        def get_crc(cls, test_case, sector_id, device_index=None, port_index=None):
            """
            Process ``GetCrc``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sector_id: Sector to start
            :type sector_id: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetCrcResponse
            :rtype: ``GetCrcResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.get_crc_cls(device_index, feature_8100_index, sector_id=sector_id)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.get_crc_response_cls)
            return response
        # end def get_crc

        @classmethod
        def get_active_profile_resolution(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetActiveProfileResolution``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetActiveProfileResolutionResponse
            :rtype: ``GetActiveProfileResolutionResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.get_active_profile_resolution_cls(device_index, feature_8100_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.get_active_profile_resolution_response_cls)
            return response
        # end def get_active_profile_resolution

        @classmethod
        def set_active_profile_resolution(cls, test_case, resolution_index, device_index=None, port_index=None):
            """
            Process ``SetActiveProfileResolution``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param resolution_index: The Resolution index in range [0..4]
            :type resolution_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetActiveProfileResolutionResponse
            :rtype: ``SetActiveProfileResolutionResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.set_active_profile_resolution_cls(
                device_index, feature_8100_index, resolution_index=resolution_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.set_active_profile_resolution_response_cls)
            return response
        # end def set_active_profile_resolution

        @classmethod
        def get_profile_fields_list(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetProfileFieldsList``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetProfileFieldsListResponse
            :rtype: ``GetProfileFieldsListResponse``
            """
            feature_8100_index, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8100.get_profile_fields_list_cls(device_index, feature_8100_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_8100.get_profile_fields_list_response_cls)
            return response
        # end def get_profile_fields_list

        @classmethod
        def profile_activated_event(cls, test_case, device_index=None, port_index=None):
            """
            Process ``ProfileActivatedEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ProfileActivatedEvent
            :rtype: ``ProfileActivatedEvent``
            """
            _, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            return ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT,
                                         class_type=feature_8100.profile_activated_event_cls)
        # end def profile_activated_event

        @classmethod
        def active_profile_resolution_changed_event(cls, test_case, device_index=None, port_index=None):
            """
            Process ``ActiveProfileResolutionChangedEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ActiveProfileResolutionChangedEvent
            :rtype: ``ActiveProfileResolutionChangedEvent``
            """
            _, feature_8100, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)
            return ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT,
                                         class_type=feature_8100.active_profile_resolution_changed_event_cls,
                                         check_first_message=False)
        # end def active_profile_resolution_changed_event
    # end class HIDppHelper

    class DirectorySettings(ProfileDirectory):
        """
        Profile Directory Settings class implementation
        """

        def __init__(self, directory_items):
            """
            :param directory_items: Available profiles in the profile directory
            :type directory_items: ``dict[int, ProfileDirectory.Item]``
            """
            self.directory_items = directory_items
        # end def __init__

        @classmethod
        def create_default_profile_directory(cls, test_case):
            """
            Create a default profile directory

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: The ``DirectorySettings`` object
            :rtype: ``OnboardProfilesTestUtils.DirectorySettings``
            """
            directory_items = {}
            profile_1 = OnboardProfiles.SectorId.PROFILE_START
            profile_count_oob = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCountOOB
            for idx in range(profile_count_oob):
                directory_items[profile_1 + idx] = ProfileDirectory.Item(sector_id=profile_1 + idx,
                                                                         enabled=OnboardProfiles.Status.ENABLED)
            # end for
            directory_settings = OnboardProfilesTestUtils.DirectorySettings(directory_items)
            cls.write_profile_directory(test_case, OnboardProfiles.SectorId.PROFILE_DIRECTORY, directory_settings)

            return directory_settings
        # end def create_default_profile_directory

        @classmethod
        def create_profile_directory(cls, test_case, directory_items):
            """
            Create a profile directory from the given profile directory items

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param directory_items: Available profiles in the profile directory
            :type directory_items: ``dict[int, ProfileDirectory.Item]``

            :return: The ``DirectorySettings`` object
            :rtype: ``OnboardProfilesTestUtils.DirectorySettings``
            """
            directory_settings = OnboardProfilesTestUtils.DirectorySettings(directory_items)
            cls.write_profile_directory(test_case, OnboardProfiles.SectorId.PROFILE_DIRECTORY, directory_settings)
            return directory_settings
        # end def create_profile_directory

        @staticmethod
        def write_profile_directory(test_case, profile_directory_id, directory_settings):
            """
            Write profile directory in flash memory

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_directory_id: Profile directory id
            :type profile_directory_id: ``int`` or ``HexList``
            :param directory_settings: Profile directory settings
            :type directory_settings: ``OnboardProfilesTestUtils.DirectorySettings``
            """
            assert profile_directory_id in [OnboardProfiles.SectorId.OOB_PROFILE_DIRECTORY,
                                            OnboardProfiles.SectorId.PROFILE_DIRECTORY]
            sector_raw_data = OnboardProfilesTestUtils.convert_to_full_sector_data(test_case,
                                                                                   HexList(directory_settings))
            OnboardProfilesTestUtils.write_sector(test_case, profile_directory_id, sector_raw_data)
        # end def write_profile_directory

        @classmethod
        def read_profile_directory(cls, test_case, profile_directory_id):
            """
            Read profile directory

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_directory_id: Profile directory id
            :type profile_directory_id: ``int`` or ``HexList``

            :return: The ``DirectorySettings`` object
            :rtype: ``OnboardProfilesTestUtils.DirectorySettings``
            """
            test_case.assertEqual(profile_directory_id & 0xFF, 0)
            sector_raw_data = OnboardProfilesTestUtils.read_sector(test_case, profile_directory_id)
            directory_settings = cls.from_hex_list(sector_raw_data)
            return directory_settings
        # end def read_profile_directory

        def convert_to_test_config_format(self):
            """
            Convert directory settings to the form of test configuration

            :return: The directory settings
            :rtype: ``dict[int, int]``
            """
            test_config = {}
            for item in self.directory_items.values():
                test_config[to_int(item.sector_id)] = to_int(item.enabled)
            # end for
            return test_config
        # end def convert_to_test_config_format

        @classmethod
        def from_hex_list(cls, profile_directory_raw_data):
            """
            Instantiate ``DirectorySettings`` by profile directory raw data

            :param profile_directory_raw_data: Profile directory raw data
            :type profile_directory_raw_data: ``HexList``

            :return: DirectorySettings object
            :rtype: ``OnboardProfilesTestUtils.DirectorySettings``
            """
            available_length = len(profile_directory_raw_data) - 4
            read_pos = 0
            directory_items = {}
            while read_pos <= available_length:
                profile_id = int(Numeral(profile_directory_raw_data[read_pos: read_pos + 2]))
                status = int(Numeral(profile_directory_raw_data[read_pos + 2]))
                if profile_id == cls.END_OF_PROFILE:
                    break
                else:
                    directory_items[profile_id] = cls.Item(sector_id=profile_id, enabled=status)
                # end if
                read_pos += 4
            # end while
            return OnboardProfilesTestUtils.DirectorySettings(directory_items)
        # end def from_hex_list

        def __hexlist__(self):
            """
            Convert ``DirectorySettings`` to its ``HexList`` representation

            :return: DirectorySettingsy data in ``HexList``
            :rtype: ``HexList``
            """
            directory_hex_list = HexList()
            for item in self.directory_items.values():
                directory_hex_list += HexList(item)
            # end for
            return directory_hex_list
        # end def __hexlist__
    # end class DirectorySettings

    class Profile:
        """
        Profile utils implementation
        """

        @classmethod
        def read_profile(cls, test_case, profile_id):
            """
            Read all data in the profile

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_id: Profile id
            :type profile_id: ``int`` or ``HexList``

            :return: Profile Format
            :rtype: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                    or ``ProfileFormatV5`` or ``ProfileFormatV6``

            :raise ``ValueError``: If input an unsupported profile format id
            """
            is_oob_profile = True if (profile_id & 0xFF00) > 0 else False
            profile_number = profile_id & 0x00FF
            test_case.assertGreater(profile_number, 0)
            profile_count = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCount
            profile_count_oob = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCountOOB
            profile_format_id = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileFormatID
            if is_oob_profile:
                test_case.assertLessEqual(profile_number, profile_count_oob)
            else:
                test_case.assertLessEqual(profile_number, profile_count)
            # end if

            if profile_format_id == ProfileFormatV1.ID:
                profile = ProfileFormatV1.fromHexList(OnboardProfilesTestUtils.read_sector(test_case, profile_id))
            elif profile_format_id == ProfileFormatV2.ID:
                profile = ProfileFormatV2.fromHexList(OnboardProfilesTestUtils.read_sector(test_case, profile_id))
            elif profile_format_id == ProfileFormatV3.ID:
                profile = ProfileFormatV3.fromHexList(OnboardProfilesTestUtils.read_sector(test_case, profile_id))
            elif profile_format_id == ProfileFormatV4.ID:
                profile = ProfileFormatV4.fromHexList(OnboardProfilesTestUtils.read_sector(test_case, profile_id))
            elif profile_format_id == ProfileFormatV5.ID:
                profile = ProfileFormatV5.fromHexList(OnboardProfilesTestUtils.read_sector(test_case, profile_id))
            elif profile_format_id == ProfileFormatV6.ID:
                profile = ProfileFormatV6.fromHexList(OnboardProfilesTestUtils.read_sector(test_case, profile_id))
            else:
                raise ValueError(f'Unsupported profile format id: {profile_format_id}')
            # end if

            return profile
        # end def read_profile

        @classmethod
        def write_profile(cls, test_case, profile_id, profile):
            """
            Overwrite profile by input data

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_id: Profile id
            :type profile_id: ``int`` or ``HexList``
            :param profile: Profile data to sector
            :type profile: ``ProfileFormatV1`` or ``ProfileFormatV2`` or ``ProfileFormatV3`` or ``ProfileFormatV4``
                           or ``ProfileFormatV5`` or ``ProfileFormatV6``

            :return: The crc value of profile
            :rtype: ``int``
            """
            profile_count = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCount
            test_case.assertGreater(profile_id, 0)
            test_case.assertLessEqual(profile_id, profile_count)
            profile.crc = OnboardProfilesTestUtils.calculate_crc(HexList(profile)[:-2])
            OnboardProfilesTestUtils.write_sector(test_case, profile_id, HexList(profile))
            return profile.crc
        # end def write_profile

        @classmethod
        def create_default_profiles(cls, test_case, modifier=None):
            """
            Create default profiles and profile directory by OOB profiles

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param modifier: The set of (attribute, value) pair - OPTIONAL
            :type modifier: ``dict``
            """
            profile_count_oob = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCountOOB
            for n in range(profile_count_oob):
                profile = cls.read_profile(test_case, OnboardProfiles.SectorId.OOB_PROFILE_START + n)
                if modifier is not None:
                    for key in modifier.keys():
                        if hasattr(profile, key):
                            setattr(profile, key, modifier[key])
                        # end if
                    # end for
                # end if
                cls.write_profile(test_case, OnboardProfiles.SectorId.PROFILE_START + n, profile)
            # end for
        # end def create_default_profiles

        @classmethod
        def create_profile_by_oob_profile(cls, test_case, oob_profile_id, dest_profile_id, modifier=None):
            """
            Create a default profile by a specific OOB profile

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param oob_profile_id: OOB profile ID
            :type oob_profile_id: ``int``
            :param dest_profile_id: Destination profile ID
            :type dest_profile_id: ``int``
            :param modifier: The set of (attribute, value) pair - OPTIONAL
            :type modifier: ``dict``

            :return: The crc value of profile
            :rtype: ``int``
            """
            profile_count_oob = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCountOOB
            profile_count = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCount
            assert (oob_profile_id & 0x00FF) <= profile_count_oob
            assert dest_profile_id <= profile_count
            profile = cls.read_profile(test_case, oob_profile_id)
            if modifier is not None:
                for key in modifier.keys():
                    if hasattr(profile, key):
                        setattr(profile, key, modifier[key])
                    # end if
                # end for
            # end if
            return cls.write_profile(test_case, dest_profile_id, profile)
        # end def create_profile_by_oob_profile

        @classmethod
        def create_software_profile_with_attributes(cls, test_case, profile_id=None, modifiers=None,
                                                    set_active_profile=True):
            """
            Create a software profile from the default OOB profile and modify the value of specify attribute

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_id: The profile ID - OPTIONAL
            :type profile_id: ``int``
            :param modifiers: The set of (attribute, value) pair - OPTIONAL
            :type modifiers: ``dict``
            :param set_active_profile: Flag indicating if the software profile is active - OPTIONAL
            :type set_active_profile: ``bool``
            """
            cls.create_default_profiles(test_case, modifiers)
            OnboardProfilesTestUtils.DirectorySettings.create_default_profile_directory(test_case)
            if set_active_profile:
                profile_id = profile_id if profile_id is not None else OnboardProfiles.SectorId.PROFILE_START
                OnboardProfilesTestUtils.HIDppHelper.set_active_profile(test_case, profile_id=profile_id)
            # end if
        # end def create_software_profile_with_attributes

        @classmethod
        def create_profile_and_set_function_buttons(
                cls, test_case, profile_id, function_buttons, p1=None, clean_message=True):
            """
            Create a user profile and reassign button setting to function execution buttons

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_id: The profile ID
            :type profile_id: ``int``
            :param function_buttons: The set of key-value(KEY_ID.BUTTON_X, function_id)  pair
            :type function_buttons: ``dict``
            :param p1: The parameter be used for Enabled Profile specific number - OPTIONAL
            :type p1: ``int``
            :param clean_message: Flag indicating if we clean up all message queues - OPTIONAL
            :type clean_message: ``bool``

            :raise ``AssertionError``: Invalid function ID
            :raise ``ValueError``: Invalid profile format ID
            """
            button_modifier = {}
            for button in function_buttons:
                function_id = function_buttons[button]
                assert function_id in ProfileButton.FunctionExecution
                button_modifier[button - KEY_ID.BUTTON_1] = ProfileButton.create_function_button(function_id, p1)
            # end for
            raw_btn_settings = HexList(OnboardProfilesTestUtils.get_default_button_settings(test_case,
                                                                                            modifier=button_modifier))
            cls.create_profile_by_oob_profile(
                test_case, oob_profile_id=OnboardProfiles.SectorId.OOB_PROFILE_START,
                dest_profile_id=profile_id, modifier={ProfileFieldName.BUTTON: raw_btn_settings})
            OnboardProfilesTestUtils.DirectorySettings.create_profile_directory(
                test_case,
                {profile_id: ProfileDirectory.Item(sector_id=profile_id, enabled=OnboardProfiles.Status.ENABLED)})

            # Empty message queues
            if clean_message:
                sleep(1)
                OnboardProfilesTestUtils.clean_up_messages(test_case)
            # end if
        # end def create_profile_and_set_function_buttons

        @classmethod
        def modify_user_profile(cls, test_case, profile_id, modifier, clean_message=True):
            """
            Modify some fields of en existing user profile

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_id: Profile ID
            :type profile_id: ``int``
            :param modifier: The set of (attribute, value) pair
            :type modifier: ``dict[str, int]``
            :param clean_message: Clean up all of message queues
            :type clean_message: ``bool``
            """
            user_profile = cls.read_profile(test_case=test_case, profile_id=profile_id)
            for key in (x for x in modifier if hasattr(user_profile, x)):
                user_profile.setValue(user_profile.getFidFromName(key), modifier[key])
            # end for

            cls.write_profile(test_case, profile_id, user_profile)

            if clean_message:
                sleep(1)
                OnboardProfilesTestUtils.clean_up_messages(test_case)
            # end if
        # end def modify_user_profile
    # end class Profile

    class ButtonRemapping(ProfileButton):
        """
        Remapping utils for profile button and GShift button
        """

        MAX_BUTTON_COUNT_V1_V5 = 16
        MAX_BUTTON_COUNT_V6 = 12

        def __init__(self, profile_format_id, remapped_buttons=None):
            """
            :param remapped_buttons: The settings of profile buttons - OPTIONAL
            :type remapped_buttons: ``list[Button]``
            """
            self.buttons = remapped_buttons if remapped_buttons else []
            self.remapped_button_to_action_map = {}
            self.profile_format_id = profile_format_id
        # end def __init__

        def reset(self):
            """
            Reset all settings of button remapping
            """
            self.buttons = []
            self.remapped_button_to_action_map = {}
        # end def reset

        @property
        def count(self):
            """
            The number of profile buttons

            :return: Profile button count
            :rtype: ``int``
            """
            return len(self.buttons)
        # end getter def count

        @classmethod
        def from_hex_list(cls, button_raw_data):
            """
            Instantiate ``ButtonRemapping`` by profile raw data

            :param button_raw_data: Profile button raw data list
            :type button_raw_data: ``HexList``

            :return: ButtonRemapping object
            :rtype: ``OnboardProfilesTestUtils.ButtonRemapping``

            :raise ``AssertionError``: If the length of button raw data is not evenly divisible by the DATA_SIZE
            """
            assert len(button_raw_data) % ProfileButton.DATA_SIZE == 0
            buttons = []
            number_of_button = int(len(button_raw_data) / ProfileButton.DATA_SIZE)
            for n in range(number_of_button):
                button_setting = button_raw_data[ProfileButton.DATA_SIZE * n: ProfileButton.DATA_SIZE * (n + 1)]
                buttons.append(ProfileButton.Button(param_1=button_setting[0], param_2=button_setting[1],
                                                    param_3=button_setting[2], param_4=button_setting[3]))
            # end for
            profile_format_id = ProfileFormatV5.ID \
                if (len(button_raw_data) / ProfileButton.DATA_SIZE) == cls.MAX_BUTTON_COUNT_V1_V5 else \
                ProfileFormatV6.ID
            return OnboardProfilesTestUtils.ButtonRemapping(profile_format_id=profile_format_id,
                                                            remapped_buttons=buttons)
        # end def from_hex_list

        def __hexlist__(self):
            """
            Convert ``ButtonRemapping`` to its ``HexList`` representation

            :return: ButtonRemapping data in ``HexList``
            :rtype: ``HexList``
            """
            button_settings = HexList()
            for button in self.buttons:
                button_settings += HexList(button)
            # end for

            button_count = self.MAX_BUTTON_COUNT_V6 if self.profile_format_id == ProfileFormatV6.ID else \
                self.MAX_BUTTON_COUNT_V1_V5

            # Padding 0xFF for unused/unsupported button setting fields
            button_settings += HexList('FF') * (button_count - self.count) * ProfileButton.DATA_SIZE

            return button_settings
        # end def __hexlist__

        @classmethod
        def from_default_button_settings(cls, test_case, profile_index=0, button_type=0, modifier=None):
            """
            Get the default button settings
            Set modifier to change default settings for specific button

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param profile_index: The index of profile - OPTIONAL
            :type profile_index: ``int``
            :param button_type: The button type - OPTIONAL
            :type button_type: ``ProfileButton.ButtonType | int``
            :param modifier: The button settings - OPTIONAL
            :type modifier: ``dict[int, ProfileButton.Button]``

            :return: The ButtonRemapping object
            :rtype: ``OnboardProfilesTestUtils.ButtonRemapping``
            """
            return OnboardProfilesTestUtils.get_default_button_settings(
                test_case=test_case, profile_index=profile_index, button_type=button_type, modifier=modifier)
        # end def get_default_button_settings

        def create_mouse_remapping(self, count):
            """
            Create the number of mouse button remapping

            :param count: The number of remapping
            :type count: ``int``
            """
            for _ in range(count):
                self.buttons.append(ProfileButton.create_mouse_button(
                    button_mask=choice(list(ProfileButton.ButtonMask))))
            # end for
        # end def create_mouse_remapping

        def create_standard_key_remapping(self, count, with_modifier=False):
            """
            Create the number of standard key remapping

            :param count: The number of remapping
            :type count: ``int``
            :param with_modifier: Indicate the standard key has modifier key or not
            :type with_modifier: ``bool``
            """
            for n in range(count):
                modifier = ProfileButton.Modifier.NO_ACTION if not with_modifier \
                    else choice(list(ProfileButton.Modifier))
                key_id = choice(list(STANDARD_KEYS.keys()))
                self.buttons.append(ProfileButton.create_standard_key(modifier=modifier, key_id=key_id))
                self.remapped_button_to_action_map[n] = [key_id, ] if modifier is ProfileButton.Modifier.NO_ACTION \
                    else [ProfileButton.convert_modifier_to_key_id(modifier), key_id]
            # end for
        # end def create_standard_key_remapping
    # end class ButtonRemapping

    class MacroSettings(ProfileMacro):
        """
        Macro Settings class implementation
        """

        def __init__(self, test_case, os_variant=None):
            """
            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param os_variant: OS detected by the firmware - OPTIONAL
            :type os_variant: ``str`` or ``None``
            """
            self.macro_list = []
            self.key_action_list = []
            self.supported_buttons = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ButtonCount
            self.sector_size = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_SectorSize
            self.os_variant = OS.WINDOWS if os_variant is None else os_variant
        # end def __init__

        def reset(self):
            """
            Reset macro settings to empty
            """
            self.macro_list = []
            self.key_action_list = []
        # end def reset

        def get_random_button(self):
            """
            Get the random profile button or GShift button

            :return: Button bit field
            :rtype: ``Numeral``
            """
            assert self.supported_buttons > 0
            button = randint(0, self.supported_buttons - 1)
            return Numeral(2 ** button, byteCount=2)
        # end def get_random_button

        @staticmethod
        def get_random_key_id():
            """
            Get a standard key id randomly

            :return: A key_id of standard key
            :rtype: ``KEY_ID``
            """
            return choice(list(STANDARD_KEYS.keys()))
        # end def get_random_key_id

        @classmethod
        def get_random_consumer_key_id(cls):
            """
            Get a consumer key id randomly

            :return: A key_id of consumer key
            :rtype: ``KEY_ID``
            """
            return choice(list(HidData.CONSUMER_KEYS.keys()))
        # end def get_random_consumer_key_id

        def create_n_random_key_strokes(self, count, add_macro_end=True):
            """
            Create number of ket strokes by random key selection

            :param count: The number of key settings
            :type count: ``int``
            :param add_macro_end: Indicate whether appends macro end settings - OPTIONAL
            :type add_macro_end: ``bool``
            """
            for _ in range(count):
                key_id = self.get_random_key_id()
                self.macro_list.append(ProfileMacro.create_std_key_stroke(modifier=0, key_id=key_id))
                self.key_action_list.append(key_id)
            # end for

            if add_macro_end:
                self.macro_list.append(ProfileMacro.create_macro_end())
            # end if
        # end def create_n_random_key_strokes

        def create_key_stroke_list(self, key_id_list, add_macro_end=True):
            """
            Create number of ket strokes by key_id_list

            :param key_id_list: The key id list
            :type key_id_list: ``list[KEY_ID]``
            :param add_macro_end: Indicate whether appends macro end settings - OPTIONAL
            :type add_macro_end: ``bool``
            """
            for key_id in key_id_list:
                self.macro_list.append(ProfileMacro.create_std_key_stroke(modifier=0, key_id=key_id))
                self.key_action_list.append(key_id)
            # end for

            if add_macro_end:
                self.macro_list.append(ProfileMacro.create_macro_end())
            # end if
        # end def create_key_stroke_list

        def __hexlist__(self):
            """
            Convert ``Macro`` to its ``HexList`` representation

            :return: Macro data in ``HexList``
            :rtype: ``HexList``
            """
            return HexList(self.macro_list)
        # end def __hexlist__

        def write_to_sector(self, test_case, sector_id):
            """
            Write macro to sector
            TODO: Shall support the case of macro raw data length > Sector Size

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param sector_id: The sector id
            :type sector_id: ``int | HexList``
            """
            sector_raw_data = OnboardProfilesTestUtils.convert_to_full_sector_data(test_case, HexList(self.macro_list))
            OnboardProfilesTestUtils.write_sector(test_case, sector_id, sector_raw_data)
        # end def write_to_sector
    # end class MacroSettings

    @classmethod
    def calculate_crc(cls, sector_raw_data):
        """
        Calculate crc value for profile.
        Note: Shall not include crc data in the input profile raw data

        :param sector_raw_data: Sector raw data
        :type sector_raw_data: ``HexList``

        :return: CRC value
        :rtype: ``int``
        """
        crc_check = Crc16ccitt()
        crc_check.start_crc(sector_raw_data)
        return crc_check.crc
    # end def calculate_crc

    @classmethod
    def read_sector(cls, test_case, sector_id):
        """
        Read all data in the sector

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param sector_id: Sector id
        :type sector_id: ``int`` or ``HexList``

        :return: The raw data list of sector
        :rtype: ``HexList``
        """
        raw_data = None
        sub_address = 0
        read_count = number_of_rows = 16
        sector_size = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_SectorSize
        for row in range(number_of_rows):
            if sector_size == 255:
                # The max sub_address is (SectorSize-16) for not crossing the border.
                if row == number_of_rows - 2:
                    read_count = 15
                else:
                    read_count = 16
                # end if
            # end if
            response = cls.HIDppHelper.read_data(test_case, sector_id, sub_address, read_count)
            if raw_data is None:
                raw_data = response.data
            else:
                if read_count == 16:
                    raw_data += response.data
                else:
                    raw_data += response.data[:-1]
                # end if
            # end if

            # The max sub_address is (SectorSize-16) for not crossing the border.
            sub_address += read_count
        # end for
        return raw_data
    # end def read_sector

    @classmethod
    def write_sector(cls, test_case, sector_id, data):
        """
        Overwrite sector by input data

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param sector_id: Sector id
        :type sector_id: ``int`` or ``HexList``
        :param data: Data to sector
        :type data: ``list[int]`` or ``HexList``

        :raise ``ChannelException`` or ``AssertionError`` or ``Hidpp2ErrorCodes``: If no message with the wanted
                                                             ``class_type`` is received or caused by invalid profile.
        """
        data_list = HexList(data)
        assert len(data_list) in [255, 256]
        if len(data_list) == 255:
            # Force sector data length to 256 bytes
            data_list.append(0xFF)
        # end if
        sector_size = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_SectorSize
        cls.HIDppHelper.start_write(test_case, sector_id, 0, sector_size)
        bytes_per_row = number_of_rows = 16
        for row in range(number_of_rows):
            # Write 16 bytes to the device per time
            cls.HIDppHelper.write_data(test_case, data_list[row * bytes_per_row: (row + 1) * bytes_per_row])
        # end for

        try:
            cls.HIDppHelper.end_write(test_case)
        except (AssertionError, Empty):
            error = ChannelUtils.get_only(
                test_case=test_case, queue_name=HIDDispatcher.QueueName.ERROR, timeout=.5, allow_no_message=True)
            if error is not None:
                raise AssertionError(error)
            else:
                raise
            # end if
        # end try
    # end def write_sector

    @classmethod
    def convert_to_full_sector_data(cls, test_case, data):
        """
        Convert settings data to full sector data, including crc calculation

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param data: Settings data in hex list
        :type data: ``HexList``

        :return: Full sector data
        :rtype: ``HexList``
        """
        sector_size = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_SectorSize
        full_sector_data = data + (HexList('FF') * (sector_size - len(data) - 2))
        crc = OnboardProfilesTestUtils.calculate_crc(full_sector_data)
        full_sector_data += HexList(Numeral(crc, byteCount=2))
        return full_sector_data
    # end def convert_to_sector_raw_data

    @classmethod
    def str_to_profile_name(cls, name):
        """
        Convert the string name to utf-16 profile name

        :param name: The profile name
        :type name: ``str``

        :return: The profile name
        :rtype: ``utf-16``
        """
        name_byte_list = list(name.encode("utf-16"))
        if len(name_byte_list) <= cls.PROFILE_NAME_BYTE_LENGTH:
            new_profile_name = name_byte_list + ([0] * (cls.PROFILE_NAME_BYTE_LENGTH - len(name_byte_list)))
        else:
            new_profile_name = name_byte_list[:cls.PROFILE_NAME_BYTE_LENGTH]
        # end if
        return HexList(new_profile_name)
    # end def str_to_profile_name

    @classmethod
    def profile_name_to_str(cls, profile_name_0_to_23):
        """
        Convert utf-16 profile name to string

        :param profile_name_0_to_23: Profile name
        :type profile_name_0_to_23: ``utf-16``

        :return: The profile name
        :rtype: ``str``
        """
        return bytearray(HexList(profile_name_0_to_23)).decode('utf-16').strip('\0')
    # end def profile_name_to_str

    @classmethod
    def get_default_button_settings(cls, test_case, profile_index=0, button_type=0, modifier=None):
        """
        Get the default button settings
        Set modifier to change default settings for specific button

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param profile_index: The index of profile - OPTIONAL
        :type profile_index: ``int``
        :param button_type: The button type - OPTIONAL
        :type button_type: ``ProfileButton.ButtonType | int``
        :param modifier: The button settings - OPTIONAL
        :type modifier: ``dict[int, ProfileButton.Button]``

        :return: The ButtonRemapping object
        :rtype: ``OnboardProfileTestUtils.ButtonRemapping``

        :raise ``ValueError``: If input an unsupported profile format id
        """
        assert button_type in [ProfileButton.ButtonType.BUTTON, ProfileButton.ButtonType.G_SHIFT]
        profile_format_id = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileFormatID
        if profile_format_id < ProfileFormatV6.ID:
            btn_config_id = ConfigurationManager.ID.OOB_PROFILES_BTN_16
            g_shift_btn_config_id = ConfigurationManager.ID.OOB_PROFILES_G_SHIFT_BTN_16
        elif profile_format_id == ProfileFormatV6.ID:
            btn_config_id = ConfigurationManager.ID.OOB_PROFILES_BTN_12
            g_shift_btn_config_id = ConfigurationManager.ID.OOB_PROFILES_G_SHIFT_BTN_12
        else:
            raise ValueError(f'Unsupported profile format id: {profile_format_id}')
        # end if
        if button_type == ProfileButton.ButtonType.BUTTON:
            btn_settings = test_case.config_manager.get_feature(btn_config_id)[profile_index]
            profile_buttons = cls.ButtonRemapping.from_hex_list(HexList(btn_settings))
        else:
            g_shift_btn_settings = test_case.config_manager.get_feature(g_shift_btn_config_id)[profile_index]
            profile_buttons = cls.ButtonRemapping.from_hex_list(HexList(g_shift_btn_settings))
        # end if
        if modifier is not None:
            for key_idx in modifier:
                profile_buttons.buttons[key_idx] = modifier[key_idx]
            # end for
        # end if
        return profile_buttons
    # end def get_default_button_settings

    @classmethod
    def get_rgb_effect_stored_field_name(cls, power_mode, lightning_flag):
        """
        Get the RGB effect stored field name

        Note: The function require Profile Format v5

        :param power_mode: The possible values are 'active' and 'passive'
        :type power_mode: ``str``
        :param lightning_flag: The lightning flag
        :type lightning_flag: ``int``

        :return: The RGB effect stored field name
        :rtype: ``str`` or ``None``
        """
        effect_store_field_name = None
        if power_mode == 'active':
            if lightning_flag & 0x01:
                effect_store_field_name = 'cluster_0_active_effect'
            else:
                effect_store_field_name = 'cluster_1_active_effect'
            # end if
        elif power_mode == 'passive':
            if lightning_flag & 0x02:
                effect_store_field_name = 'cluster_0_passive_effect'
            else:
                effect_store_field_name = 'cluster_1_passive_effect'
            # end if
        # end if
        return effect_store_field_name
    # end def get_rgb_effect_stored_field_name

    @classmethod
    def adjust_lightning_flag_by_rgb_effect_id(cls, test_case, power_mode, rgb_effect_id, oob_profile_index=0):
        """
        Adjust the lightning flag by the required RGB effect ID

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param power_mode: The possible values are 'active' and 'passive'
        :type power_mode: ``str``
        :param rgb_effect_id: The RGB Effect ID
        :type rgb_effect_id: ``RGBEffectID``
        :param oob_profile_index: The index of OOB profile - OPTIONAL
        :type oob_profile_index: ``int``

        :return: The modified lightning flag
        :rtype: ``int``
        """
        assert power_mode in ['active', 'passive']
        cluster, _ = RGBEffectsTestUtils.get_effect_info(test_case, rgb_effect_id)
        lightning_flag = test_case.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_LIGHTNING_FLAG)[oob_profile_index]
        if power_mode == 'active':
            power_mode_bit = 0x01
        else:
            power_mode_bit = 0x02
        # end if
        if lightning_flag & power_mode_bit:
            # Enabled multi-cluster
            if cluster == 0xFF:
                # The fixed effect be supported in the same cluster
                modified_lightning_flag = lightning_flag
            else:
                # The fixed effect be supported in the different cluster. Disable the multi-cluster
                modified_lightning_flag = lightning_flag & (0xFF - power_mode_bit)
            # end if
        else:
            # Disabled multi-cluster
            if cluster == 0xFF:
                # The fixed effect be supported in the different cluster. Enable the multi-cluster
                modified_lightning_flag = lightning_flag | power_mode_bit
            else:
                # The fixed effect be supported in the same cluster.
                modified_lightning_flag = lightning_flag
            # end if
        # end if
        return modified_lightning_flag
    # end def adjust_lightning_flag_by_rgb_effect_id

    @classmethod
    def get_rgb_effect_stored_field_checker(cls, rgb_effect_stored_field_name):
        """
        Get the RGB effect stored field checker

        Note: The function require Profile Format v5

        :param rgb_effect_stored_field_name: The stored field name of RGB effect in profile format v5
        :type rgb_effect_stored_field_name: ``str``

        :return: The checker of RGB effect stored field
        :rtype: ``ProfileChecker`` or ``None``
        """
        if rgb_effect_stored_field_name == 'logo_effect':
            return cls.ProfileChecker.check_logo_effect
        elif rgb_effect_stored_field_name == 'side_effect':
            return cls.ProfileChecker.check_side_effect
        elif rgb_effect_stored_field_name == 'logo_active_effect':
            return cls.ProfileChecker.check_logo_active_effect
        elif rgb_effect_stored_field_name == 'side_active_effect':
            return cls.ProfileChecker.check_side_active_effect
        elif rgb_effect_stored_field_name == 'logo_passive_effect':
            return cls.ProfileChecker.check_logo_passive_effect
        elif rgb_effect_stored_field_name == 'side_passive_effect':
            return cls.ProfileChecker.check_side_passive_effect
        elif rgb_effect_stored_field_name == 'cluster_0_active_effect':
            return cls.ProfileChecker.check_cluster_0_active_effect
        elif rgb_effect_stored_field_name == 'cluster_1_active_effect':
            return cls.ProfileChecker.check_cluster_1_active_effect
        elif rgb_effect_stored_field_name == 'cluster_0_passive_effect':
            return cls.ProfileChecker.check_cluster_0_passive_effect
        elif rgb_effect_stored_field_name == 'cluster_1_passive_effect':
            return cls.ProfileChecker.check_cluster_1_passive_effect
        else:
            return None
        # end if
    # end def get_rgb_effect_stored_field_checker

    @classmethod
    def to_2_bytes_form(cls, data):
        """
        Convert int to 2 bytes form

        :param data: data
        :type data: ``int``

        :return: The 2 byte value of int data
        :rtype: ``HexList``
        """
        return HexList(data.to_bytes(2, 'big'))
    # end def to_2_bytes_form

    @classmethod
    def to_raw_dpi_0_to_4(cls, dpi_list):
        """
        Convert DPI list to dpi_0_to_4 or dpi_xy_0_to_4 raw data

        Note: Support profile format v6

        :param dpi_list: The DPI list
        :type dpi_list: ``list[int]``

        :return: The raw data of dpi_0_to_4 or dpi_xy_0_to_4
        :rtype: ``HexList``
        """
        return HexList(DpiResolutions.from_dpi_list(dpi_list))
    # end def to_raw_dpi_0_to_4

    @classmethod
    def get_none_default_dpi_index(cls, test_case, oob_profile_index=0):
        """
        Return the none default DPI index and DPI

        Note: Support profile format v6

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param oob_profile_index: The index of OOB profile - OPTIONAL
        :type oob_profile_index: ``int``

        :return: The none default DPI index
        :rtype: ``int``
        """
        default_dpi_index = test_case.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[oob_profile_index]
        none_default_dpi_index = 1 if default_dpi_index == 0 else 0
        return none_default_dpi_index
    # end def get_none_default_dpi_index

    @classmethod
    def get_default_dpi(cls, test_case, oob_profile_index=0):
        """
        Return the default DPI index and DPI

        Note: Support profile format v6

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param oob_profile_index: The index of OOB profile - OPTIONAL
        :type oob_profile_index: ``int``

        :return: The default resolution index and DPI
        :rtype: ``int, int`` or ``int, list[int, int, int]``
        """
        default_dpi_index = test_case.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[oob_profile_index]
        dpi_list = test_case.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DPI_LIST)[oob_profile_index]
        return default_dpi_index, dpi_list[default_dpi_index]
    # end def get_default_dpi

    @classmethod
    def get_none_default_dpi(cls, test_case, oob_profile_index=0):
        """
        Return the none default DPI index and DPI

        Note: Support profile format v6

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param oob_profile_index: The index of OOB profile - OPTIONAL
        :type oob_profile_index: ``int``

        :return: The none default DPI index and DPI
        :rtype: ``int, int`` or ``int, list[int, int, int]``
        """
        default_dpi_index = test_case.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DEFAULT_DPI_INDEX)[oob_profile_index]
        none_default_dpi_index = 1 if default_dpi_index == 0 else 0
        dpi_list = test_case.config_manager.get_feature(
            ConfigurationManager.ID.OOB_PROFILES_DPI_LIST)[oob_profile_index]
        return none_default_dpi_index, dpi_list[none_default_dpi_index]
    # end def get_none_default_dpi

    @classmethod
    def keystroke(cls, test_case, key_id):
        """
        Emulator key stroke by key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: The key id
        :type key_id: ``KEY_ID``
        """
        if test_case.f.PRODUCT.F_IsMice:
            test_case.button_stimuli_emulator.keystroke(key_id=key_id)
        else:
            x40a3_enabled = test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled
            if x40a3_enabled:
                FnInversionForMultiHostDevicesTestUtils.enable_fn_inversion(test_case)
            # end if

            test_case.button_stimuli_emulator.keystroke(key_id=test_case.button_stimuli_emulator.get_fn_keys()[key_id])

            if x40a3_enabled:
                FnInversionForMultiHostDevicesTestUtils.restore_fn_inversion(test_case)
            # end if
        # end if
    # end def keystroke

    @classmethod
    def key_press(cls, test_case, key_id):
        """
        Emulator key press by key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: The key id
        :type key_id: ``KEY_ID``
        """
        if test_case.f.PRODUCT.F_IsMice:
            test_case.button_stimuli_emulator.key_press(key_id=key_id)
        else:
            x40a3_enabled = test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled
            if x40a3_enabled:
                FnInversionForMultiHostDevicesTestUtils.enable_fn_inversion(test_case)
            # end if

            test_case.button_stimuli_emulator.key_press(key_id=test_case.button_stimuli_emulator.get_fn_keys()[key_id])
        # end if
    # end def key_press

    @classmethod
    def key_release(cls, test_case, key_id):
        """
        Emulator key release by key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param key_id: The key id
        :type key_id: ``KEY_ID``
        """
        if test_case.f.PRODUCT.F_IsMice:
            test_case.button_stimuli_emulator.key_release(key_id=key_id)
        else:
            test_case.button_stimuli_emulator.key_release(
                key_id=test_case.button_stimuli_emulator.get_fn_keys()[key_id])

            x40a3_enabled = test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled
            if x40a3_enabled:
                FnInversionForMultiHostDevicesTestUtils.restore_fn_inversion(test_case)
            # end if
        # end if
    # end def key_release

    @classmethod
    def perform_action_list(cls, test_case, action_list):
        """
        Emulator key stroke by key id

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param action_list: The action list
        :type action_list: ``list[list]``
        """
        if test_case.f.PRODUCT.F_IsMice:
            test_case.button_stimuli_emulator.perform_action_list(action_list)
        else:
            x40a3_enabled = test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled
            if x40a3_enabled:
                FnInversionForMultiHostDevicesTestUtils.enable_fn_inversion(test_case)
            # end if

            fn_action_list = []
            for action in action_list:
                fn_action_list.append([test_case.button_stimuli_emulator.get_fn_keys()[action[0]], action[1]])
            # end for

            test_case.button_stimuli_emulator.perform_action_list(fn_action_list)
            if x40a3_enabled:
                FnInversionForMultiHostDevicesTestUtils.restore_fn_inversion(test_case)
            # end if
        # end if
    # end def perform_action_list

    @classmethod
    def get_none_default_report_rate(cls, test_case, profile_index=0):
        """
        Return the none default report rate

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param profile_index: The profile index - OPTIONAL
        :type profile_index: ``int``

        :return: The none default report rate
        :rtype: ``int``
        """
        profile_count_oob = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES.F_ProfileCountOOB
        assert profile_index < profile_count_oob
        supported_report_rate_list = ReportRateTestUtils.get_default_report_rate_list(test_case)
        default_report_rate = \
            test_case.config_manager.get_feature(ConfigurationManager.ID.OOB_PROFILES_REPORT_RATE)[profile_index]
        for report_rate in reversed(supported_report_rate_list):
            if report_rate != default_report_rate:
                return report_rate
            # end if
        # end for
    # end def get_none_default_report_rate

    @classmethod
    def clean_up_messages(cls, test_case, delay=None):
        """
        Clean up messages generated by user profile creation

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param delay: Given the delay(s) to get the reports before clean messages - OPTIONAL
        :type delay: ``int|float``
        """
        if delay:
            sleep(delay)
        # end if

        ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.MOUSE,
                                    class_type=SensorDpiParametersEvent)
        ChannelUtils.clean_messages(
            test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
            class_type=(HidMouse, HidMouseNvidiaExtension, HidKeyboard, HidKeyboardBitmap, HidConsumer))
    # end def clean_up_messages

    @classmethod
    def get_btn_field_name(cls, test_case):
        """
        Get the name of button fields from the corresponding ProfileFormatID

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The name of button fields
        :rtype: ``str``

        :raise ``ValueError``: If input an unsupported profile format id
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES
        if config.F_ProfileFormatID < 6:
            btn_field_name = 'btn_0_to_15'
        elif config.F_ProfileFormatID == 6:
            btn_field_name = 'btn_0_to_11'
        else:
            raise ValueError(f'Unsupported profile format id: {config.F_ProfileFormatID}')
        # end if

        return btn_field_name
    # end def get_btn_field_name

    @classmethod
    def get_g_shift_btn_field_name(cls, test_case):
        """
        Get the name of g shift button fields from the corresponding ProfileFormatID

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The name of g shift button fields
        :rtype: ``str``

        :raise ``ValueError``: If input an unsupported profile format id
        """
        config = test_case.f.PRODUCT.FEATURES.GAMING.ONBOARD_PROFILES
        if config.F_ProfileFormatID < 6:
            g_shift_btn_field_name = 'g_shift_btn_0_to_15'
        elif config.F_ProfileFormatID == 6:
            g_shift_btn_field_name = 'g_shift_btn_0_to_11'
        else:
            raise ValueError(f'Unsupported profile format id: {config.F_ProfileFormatID}')
        # end if

        return g_shift_btn_field_name
    # end def get_g_shift_btn_field_name
# end class OnboardProfilesTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
