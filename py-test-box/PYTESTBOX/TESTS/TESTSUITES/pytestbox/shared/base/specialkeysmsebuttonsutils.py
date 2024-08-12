#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.specialkeysmsebuttonsutils
:brief:  Helpers for Special keys and mouse buttons feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/11/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from math import ceil
from time import sleep

from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hid.hidmouse import HidMouse
from pyhid.hiddata import HidData
from pyhid.hiddata import OS
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsFactory
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsInterface
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.cidutils import CidInfoConfig
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
HUNDRED_MILLISECONDS = 0.1


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMseButtonsTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on Special keys and mouse buttons feature
    """

    class GetCapabilitiesV6ResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCapabilitiesV6Response``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCapabilitiesV6Response`` API

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS
            return {
                "flags": (cls.check_reset_all_cid_report_settings, config.F_SupportResetAllCidReportSettings),
            }
        # end def get_default_check_map

        @staticmethod
        def check_reset_all_cid_report_settings(test_case, response, expected):
            """
            Check host_index field in response

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: GetCapabilitiesV6Response to check
            :type response: ``GetCapabilitiesV6Response``
            :param expected: Expected value
            :type expected: ``bool``

            :raise ``AssertionError``: Assert host_index that raise an exception
            """
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.flags),
                msg="The resetAllCidReportSettings parameter differs "
                    f"(expected:{expected}, obtained:{response.flags})")
        # end def check_reset_all_cid_report_settings
    # end class GetCapabilitiesV6ResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=SpecialKeysMSEButtons.FEATURE_ID,
                           factory=SpecialKeysMSEButtonsFactory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def reset_all_cid_report_settings(cls, test_case, device_index=None, port_index=None):
            """
            Process ``resetAllCidReportSettings``

            :param test_case: Current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ResetAllCidReportSettingsV6Response
            :rtype: ``ResetAllCidReportSettingsV6Response``
            """
            feature_1b04_index, feature_1b04, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1b04.reset_all_cid_report_settings_cls(
                device_index=device_index,
                feature_index=feature_1b04_index
            )
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1b04.reset_all_cid_report_settings_response_cls)
            return response
        # end def reset_all_cid_report_settings
    # end class HIDppHelper

    @staticmethod
    def check_response_expected_field(test_case, message_with_expected_field, response):
        """
        Check if the fields of a response are the expected one.
        It will not test the HippMessage header nor the padding.

        :param test_case: The test case to use for asserts.
        :type test_case: ``BaseTestCase``
        :param message_with_expected_field: The message with the expected fields.
        :type message_with_expected_field: ``HidppMessage``
        :param response: The response to test.
        :type response: ``BitFieldContainerMixin``

        :raise ``AssertionError``: If test_case does not inherit from ``BaseTestCase``
                                   If the final error message is not empty`
        """
        test_case.assertTrue(expr=isinstance(test_case, BaseTestCase),
                             msg='Wrong use of function check_response_expected_field, parameter test_case should be '
                                 'a BaseTestCase (or inherit from it)')
        test_case.assertTrue(expr=isinstance(message_with_expected_field, HidppMessage),
                             msg='Wrong use of function check_response_is_request_echo, ' +
                                 'parameter request should be a HidppMessage (or inherit from it)')
        test_case.assertTrue(expr=isinstance(response, HidppMessage),
                             msg='Wrong use of function check_response_is_request_echo, ' +
                                 'parameter response should be a HidppMessage (or inherit from it)')

        """
        Check all fields except for the header of hippmessage (5 first fields) and padding.
        """
        set_cid_reporting_field_ids = [field.fid for field in message_with_expected_field.FIELDS]
        set_cid_reporting_response_field_ids = [field.fid for field in response.FIELDS]
        hipp_message_header_fid = [v for k, v in HidppMessage.FID.__dict__.items() if not k.startswith("__")]

        error_message = ""
        if set_cid_reporting_field_ids == set_cid_reporting_response_field_ids:
            for fid in set_cid_reporting_field_ids:
                if fid not in hipp_message_header_fid and fid != message_with_expected_field.FID.PADDING and \
                        message_with_expected_field.getValue(fid) != response.getValue(fid):
                    if error_message == "":
                        error_message += "This parameters differ from the one expected " + \
                                         "(header and padding are not checked):\n"
                    # end if
                    error_message += "\t- " + response.getFieldDefinition(fid).name + "\n"
                    # end if
                # end if
            # end for
        else:
            error_message += "Field IDs are not matching"
        # end if

        test_case.assertTrue(expr=error_message == "",
                             msg=error_message + "\n" + str(message_with_expected_field) + "\n" + str(response))
    # end def check_response_expected_field

    @staticmethod
    def get_cid_count(test_case, feature, feature_index):
        """
        Get CID count

        :param test_case: The test case to use.
        :type test_case: ``BaseTestCase``
        :param feature: Feature interface
        :type feature: ``SpecialKeysMSEButtonsInterface``
        :param feature_index: Feature index
        :type feature_index: ``int``

        :return: the number of items in the control ID table
        :rtype: ``int``
        """
        get_count = feature.get_count_cls(device_index=ChannelUtils.get_device_index(test_case=test_case),
                                          feature_index=feature_index)
        get_count_response = ChannelUtils.send(
            test_case=test_case,
            report=get_count,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=feature.get_count_response_cls)

        return get_count_response.count.toLong()
    # end def get_cid_count

    @staticmethod
    def check_diverted_button_event(test_case, feature, expected_cid_list, diverted_buttons_event=None):
        """
        Check a DivertedButtonEvent's fields.

        :param test_case: The test case to use.
        :type test_case: ``BaseTestCase``
        :param feature: Feature interface
        :type feature: ``SpecialKeysMSEButtonsInterface``
        :param expected_cid_list: The list of CIDs to expect in the event. It should be of length 4 or less. If it is
                                  less than 4 it will be padded with HexList(0).
        :type expected_cid_list: ``list``
        :param diverted_buttons_event: The event to check. If None, an event will be waited on the queue - OPTIONAL
        :type diverted_buttons_event: ``DivertedButtonsEvent``

        :raise ``AssertionError``: If test_case does not inherit from ``BaseTestCase``
                                   If one of the 4 ctrl_id_x parameters does not match the expected value
        """
        max_len_cid_list = 4
        test_case.assertTrue(expr=isinstance(test_case, BaseTestCase),
                             msg='Wrong use of function check_diverted_button_event, ' +
                                 'parameter test_case should be a BaseTestCase (or inherit from it)')
        test_case.assertTrue(expr=isinstance(expected_cid_list, list),
                             msg='Wrong use of function check_diverted_button_event, ' +
                                 'parameter expected_cid_list should be a list')
        test_case.assertTrue(expr=len(expected_cid_list) <= max_len_cid_list,
                             msg=f'Wrong use of function check_diverted_button_event, parameter expected_cid_list '
                                 f'should be of length {max_len_cid_list} or less.')

        if len(expected_cid_list) < max_len_cid_list:
            for _ in range(max_len_cid_list - len(expected_cid_list)):
                expected_cid_list.append(HexList(Numeral(feature.diverted_buttons_event_cls.DEFAULT.CTRL_ID1,
                                                         feature.diverted_buttons_event_cls.LEN.CTRL_ID1 // 8)))
            # end for
        # end if

        if diverted_buttons_event is None:
            diverted_buttons_event = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature.diverted_buttons_event_cls)
            test_case.logTrace('DivertedButtonEvent: %s\n' % str(diverted_buttons_event))
        # end if

        test_case.assertEqual(expected=expected_cid_list[0],
                              obtained=diverted_buttons_event.ctrl_id_1,
                              msg='The ctrl_id_1 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_list[1],
                              obtained=diverted_buttons_event.ctrl_id_2,
                              msg='The ctrl_id_2 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_list[2],
                              obtained=diverted_buttons_event.ctrl_id_3,
                              msg='The ctrl_id_3 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_list[3],
                              obtained=diverted_buttons_event.ctrl_id_4,
                              msg='The ctrl_id_4 parameter differs from the one expected')
    # end def check_diverted_button_event

    @staticmethod
    def check_analytics_key_events(test_case, feature, expected_cid_event_list, analytics_key_events=None):
        """
        Check a AnalyticsKeyEvents's fields.

        :param test_case: The test case to use.
        :type test_case: ``BaseTestCase``
        :param feature: Feature interface
        :type feature: ``SpecialKeysMSEButtonsInterface``
        :param expected_cid_event_list: The list of CIDs and events to expect in the event. It should be of length 10
                                        or less. If it is less than 10 it will be padded with HexList(0).
        :type expected_cid_event_list: ``list``
        :param analytics_key_events: The event to check. If None, an event will be waited on the queue - OPTIONAL
        :type analytics_key_events: ``AnalyticsKeyEvents``

        :raise ``AssertionError``: If test_case does not inherit from ``BaseTestCase``
                                   If one of the 5 ctrl_id_x or event_x parameters does not match the expected value
        """
        test_case.assertTrue(expr=isinstance(test_case, BaseTestCase),
                             msg='Wrong use of function check_analytics_key_events, parameter test_case should be a '
                                 'BaseTestCase (or inherit from it)')
        test_case.assertTrue(expr=isinstance(expected_cid_event_list, list),
                             msg='Wrong use of function check_analytics_key_events, ' +
                                 'parameter expected_cid_event_list should be a list')
        test_case.assertTrue(expr=len(expected_cid_event_list) <= 10,
                             msg='Wrong use of function check_analytics_key_events, ' +
                                 'parameter expected_cid_event_list should be of length 10 or less.')

        if len(expected_cid_event_list) < 10:
            for _ in range(4 - len(expected_cid_event_list)):
                expected_cid_event_list.append(HexList(0))
            # end for
        # end if

        if analytics_key_events is None:
            analytics_key_events = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature.analytics_key_event_cls)
            test_case.logTrace('AnalyticsKeyEvents: %s\n' % str(analytics_key_events))
        # end if

        test_case.assertEqual(expected=expected_cid_event_list[0],
                              obtained=analytics_key_events.ctrl_id_1,
                              msg='The ctrl_id_1 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[1],
                              obtained=analytics_key_events.event_1,
                              msg='The event_1 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[2],
                              obtained=analytics_key_events.ctrl_id_2,
                              msg='The ctrl_id_2 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[3],
                              obtained=analytics_key_events.event_2,
                              msg='The event_2 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[4],
                              obtained=analytics_key_events.ctrl_id_3,
                              msg='The ctrl_id_3 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[5],
                              obtained=analytics_key_events.event_3,
                              msg='The event_3 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[6],
                              obtained=analytics_key_events.ctrl_id_4,
                              msg='The ctrl_id_4 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[7],
                              obtained=analytics_key_events.event_4,
                              msg='The event_4 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[8],
                              obtained=analytics_key_events.ctrl_id_5,
                              msg='The ctrl_id_4 parameter differs from the one expected')
        test_case.assertEqual(expected=expected_cid_event_list[9],
                              obtained=analytics_key_events.event_5,
                              msg='The event_5 parameter differs from the one expected')
    # end def check_analytics_key_events

    @staticmethod
    def check_hid_packet(test_case, cid, action, combined_cid=None, ignore_queue_empty_check=False):
        """
        Check a HID responses.

        :param test_case: The test case to use for asserts.
        :type test_case: ``BaseTestCase``
        :param cid: The CID of the button(s) to check in HID packet.
        :type cid: ``int`` or ``HexList``
        :param action: Action to check, can be 'make' or 'break'.
        :type action: ``str``
        :param combined_cid: The second cid which is combined with the cid input to enable the HID consumer report
                             verification. - OPTIONAL
        :type combined_cid: ``int`` or ``HexList`` or ``None``
        :param ignore_queue_empty_check: Ignore the queue empty check - OPTIONAL
        :type ignore_queue_empty_check: ``bool``

        :raise ``AssertionError``: If one of the HID report fields does not match the expected value
        """
        key_id = CID_TO_KEY_ID_MAP[to_int(cid)]
        # Default OS handling
        marketing_name = test_case.config_manager.get_feature(ConfigurationManager.ID.MARKETING_NAME)
        variant = OS.MAC if marketing_name.endswith('for Mac') else OS.WINDOWS
        if variant not in iter(HidData.KEY_ID_TO_HID_MAP[key_id]):
            # If we have no information about the detected OS, we select the first available variant
            variant = next(iter(HidData.KEY_ID_TO_HID_MAP[key_id]))
        # end if
        responses_class = HidData.KEY_ID_TO_HID_MAP[key_id][variant][action]['Responses_class']
        fields_name = HidData.KEY_ID_TO_HID_MAP[key_id][variant][action]['Fields_name']
        fields_value = HidData.KEY_ID_TO_HID_MAP[key_id][variant][action]['Fields_value']

        if combined_cid:
            combined_key_id = CID_TO_KEY_ID_MAP[to_int(combined_cid)]
            fields_name = ['key_1', 'key_2']
            if action == MAKE:
                fields_value = [HidData.KEY_ID_TO_HID_MAP[combined_key_id][variant][MAKE]['Fields_value'][0][0],
                                fields_value[0][0]]
            elif action == BREAK:
                fields_value = [HidData.KEY_ID_TO_HID_MAP[combined_key_id][variant][MAKE]['Fields_value'][0][0],
                                fields_value[0][0]]
            # end if
        # end if

        for i in range(len(responses_class)):
            hid_packet = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.HID,
                class_type=responses_class[i])
            for j in range(len(fields_name[i])):
                for field in hid_packet.FIELDS:
                    fid = field.getFid()
                    if field.name == fields_name[i][j]:
                        if isinstance(hid_packet.getValue(fid), HexList):
                            value_obtain = hid_packet.getValue(fid).toLong()
                        else:
                            value_obtain = hid_packet.getValue(fid)
                        # end if
                        test_case.assertEquals(expected=fields_value[i][j] if fields_value[i][j] >= 0 else 0,
                                               obtained=value_obtain,
                                               msg="The %s parameter differs from the one expected"
                                                   % fields_name[i][j])
                    # end if
                # end for
            # end for
        # end for

        if not ignore_queue_empty_check:
            # We shouldn't receive any other HID packet
            ChannelUtils.check_queue_empty(test_case=test_case,
                                           queue_name=HIDDispatcher.QueueName.HID,
                                           timeout=HUNDRED_MILLISECONDS)
        # end if
    # end def check_hid_packet

    @staticmethod
    def send_key_by_attribute_flags(test_case, cid, action, press_fn):
        """
        Trigger a key press or a key release.

        :param test_case: The test case to use for asserts.
        :type test_case: ``BaseTestCase``
        :param cid: The CID of the button(s) to check in HID packet.
        :type cid: ``int`` or ``HexList``
        :param action: Action to check, can be 'make' or 'break'.
        :type action: ``str``
        :param press_fn: Flag indicating if we will force press the fn key before any other keystrokes
        :type press_fn: ``bool``

        :return: Flag indicating if a Fn key DivertedButtonsEvent is expected or not after clicked the button
        :rtype: ``bool``
        """
        if isinstance(cid, HexList):
            cid = cid.toLong()
        # end if

        is_additional_fn_keystroke_required = False
        actual_key_id = None
        key_id = CID_TO_KEY_ID_MAP[cid]

        if press_fn is True:
            actual_key_id = CID_TO_KEY_ID_MAP[cid]
            is_additional_fn_keystroke_required = True
        # end if

        if key_id in test_case.button_stimuli_emulator.get_fn_keys():
            is_additional_fn_keystroke_required = True
            actual_key_id = test_case.button_stimuli_emulator.get_fn_keys()[key_id]
        # end if

        if action == MAKE:
            if is_additional_fn_keystroke_required:
                test_case.button_stimuli_emulator.multiple_keys_press([KEY_ID.FN_KEY, actual_key_id], delay=.05)
            else:
                test_case.button_stimuli_emulator.key_press(CID_TO_KEY_ID_MAP[cid])
                sleep(.05)
            # end if
        elif action == BREAK:
            if is_additional_fn_keystroke_required:
                test_case.button_stimuli_emulator.multiple_keys_release([actual_key_id, KEY_ID.FN_KEY], delay=.05)
            else:
                test_case.button_stimuli_emulator.key_release(CID_TO_KEY_ID_MAP[cid])
                sleep(.05)
            # end if
        # end if

        is_fn_key_diverted_event_expected = False
        cid_info = CidInfoConfig.from_cid(test_case.f, cid, test_case.config_manager)
        if cid_info.friendly_name.upper() == 'FN KEY':
            # Case 1: the given cid matches the Fn Key
            is_fn_key_diverted_event_expected = True
        else:
            # Case 2: The additional Fn key is required when the Fn key cid is part of the 0x1B04 key list.
            cid_info_table_cid = test_case.config_manager.get_feature(ConfigurationManager.ID.CID_INFO_TABLE_CID)
            if is_additional_fn_keystroke_required and CidTable.FN_KEY in cid_info_table_cid:
                is_fn_key_diverted_event_expected = True
            # end if
        # end if

        return is_fn_key_diverted_event_expected
    # end def send_key_by_attribute_flags

    class StimulusMask:
        """
        Bitmap enabling the possible user actions
        """
        # First byte is stimulus type
        STIMULUS_TYPE_MASK = 0x00FF
        KEY_PRESSED_POS = 0
        KEY_PRESSED_MASK = (1 << KEY_PRESSED_POS)
        KEY_RELEASED_POS = 1
        KEY_RELEASED_MASK = (1 << KEY_RELEASED_POS)
        POSITIVE_XY_MOVEMENT_POS = 2
        POSITIVE_XY_MOVEMENT_MASK = (1 << POSITIVE_XY_MOVEMENT_POS)
        NEGATIVE_XY_MOVEMENT_POS = 3
        NEGATIVE_XY_MOVEMENT_MASK = (1 << NEGATIVE_XY_MOVEMENT_POS)
        POSITIVE_WHEEL_MOVEMENT_POS = 4
        POSITIVE_WHEEL_MOVEMENT_MASK = (1 << POSITIVE_WHEEL_MOVEMENT_POS)
        NEGATIVE_WHEEL_MOVEMENT_POS = 4
        NEGATIVE_WHEEL_MOVEMENT_MASK = (1 << NEGATIVE_WHEEL_MOVEMENT_POS)

        # Second byte is event type expected
        EXPECTED_EVENT_TYPE_MASK = 0xFF00
        HIDPP_BUTTON_EVENT_POS = 8
        HIDPP_BUTTON_EVENT_MASK = (1 << HIDPP_BUTTON_EVENT_POS)
        HIDPP_RAW_XY_EVENT_POS = 9
        HIDPP_RAW_XY_EVENT_MASK = (1 << HIDPP_RAW_XY_EVENT_POS)
        HIDPP_ANALYTIC_KEY_EVENT_POS = 10
        HIDPP_ANALYTIC_KEY_EVENT_MASK = (1 << HIDPP_ANALYTIC_KEY_EVENT_POS)
        HIDPP_RAW_WHEEL_EVENT_POS = 9
        HIDPP_RAW_WHEEL_EVENT_MASK = (1 << HIDPP_RAW_WHEEL_EVENT_POS)
        HIDPP_FN_INVERSION_EVENT_POS = 12
        HIDPP_FN_INVERSION_EVENT_MASK = (1 << HIDPP_FN_INVERSION_EVENT_POS)
        """
        List of some useful of stimuli

        - PRD is button pressed with expected HID++ diverted button response
        - PRA is button pressed with expected HID++ analytics response
        - PRH is button pressed with expected HID packet response
        - PRA is button pressed with expected analytics response
        - RRD is button released with expected HID++ diverted button response
        - RRA is button released with expected HID++ analytics response
        - RRH is button released with expected HID packet response
        - PXYRHPP is positive XY movement with expected response
        - PXYRH is positive XY movement without response
        - NXYRHPP is negative XY movement with expected response
        - NXYRH is negative XY movement without response
        """
        PRD = KEY_PRESSED_MASK | HIDPP_BUTTON_EVENT_MASK
        RRD = KEY_RELEASED_MASK | HIDPP_BUTTON_EVENT_MASK
        PRA = KEY_PRESSED_MASK | HIDPP_ANALYTIC_KEY_EVENT_MASK
        RRA = KEY_RELEASED_MASK | HIDPP_ANALYTIC_KEY_EVENT_MASK
        PRH = KEY_PRESSED_MASK
        RRH = KEY_RELEASED_MASK
        FN_LOCK_MASK = HIDPP_FN_INVERSION_EVENT_MASK
        PXYRHPP = POSITIVE_XY_MOVEMENT_MASK | HIDPP_RAW_XY_EVENT_MASK
        NXYRHPP = NEGATIVE_XY_MOVEMENT_MASK | HIDPP_RAW_XY_EVENT_MASK
        PXYRH = POSITIVE_XY_MOVEMENT_MASK
        NXYRH = NEGATIVE_XY_MOVEMENT_MASK
        PWHLRHPP = POSITIVE_WHEEL_MOVEMENT_MASK | HIDPP_RAW_WHEEL_EVENT_MASK
        NWHLRHPP = NEGATIVE_WHEEL_MOVEMENT_MASK | HIDPP_RAW_WHEEL_EVENT_MASK
        PWHLRH = POSITIVE_WHEEL_MOVEMENT_MASK
        NWHLRH = NEGATIVE_WHEEL_MOVEMENT_MASK
        PRD_RRD = PRD | RRD
        PRA_RRA = PRA | RRA
        PRH_RRH = PRH | RRH
        PRD_PXYRHPP_RRD = PRD | PXYRHPP | RRD
        PRD_PXYRH_RRD = PRD | PXYRH | RRD
        PRH_PXYRH_RRH = PRH | PXYRH | RRH
        PRD_NXYRHPP_RRD = PRD | NXYRHPP | RRD
        PRD_NXYRH_RRD = PRD | NXYRH | RRD
        PNR_NXYRH_RNR = PRH | NXYRH | RRH
    # end class StimulusMask

    @classmethod
    def send_stimulus_and_verify(cls, test_case, feature, ctrl_id, stimuli_masks, remapped_cid=0,
                                 press_expected_list_in_event=None, release_expected_list_in_event=None,
                                 combined_cid=None, press_fn=False):
        """
        Send a stimulus and verify stimulus event.

        The order of the stimuli is set to KEY_PRESSED_MASK, then XY_MOVEMENT_MASK and then KEY_RELEASED_MASK. If the
        order is not the one wanted, the stimuli masks can be sent as a list instead.

        :param test_case: The test case to use for asserts.
        :type test_case: ``EmuTestCase``
        :param feature: Feature interface
        :type feature: ``SpecialKeysMSEButtonsInterface``
        :param ctrl_id: The CtrlD to check.
        :type ctrl_id: ``int`` or ``HexList``
        :param stimuli_masks: Stimuli masks to use (can be a List of masks).
        :type stimuli_masks: ``int`` or ``list``
        :param remapped_cid: The remap target's CtrlD to check. This parameter will only be used if the expected
                             stimulus event is a HID packet. Otherwise, it is ignored. If = 0, it will check ctrl_id
                             instead - OPTIONAL
        :type remapped_cid: ``int`` or ``HexList``
        :param press_expected_list_in_event: The list of values to expect in the event. This parameter is to be used
                                             in check_diverted_button_event and/or check_analytics_key_events. The
                                             format needed should be checked from their documentation. If it is
                                             None, it will be replace by default values depending on the stimulus done
                                             - OPTIONAL
        :type press_expected_list_in_event: ``list``
        :param release_expected_list_in_event: The list of values to expect in the event. This parameter is to be
                                               used in check_diverted_button_event and/or check_analytics_key_events.
                                               The format needed should be checked from their documentation. If it is
                                               None, it will be replace by default values depending on the stimulus
                                               done - OPTIONAL
        :type release_expected_list_in_event: ``list``
        :param combined_cid: The second cid which is combined with the cid input to enable the HID consumer report
                             verification - OPTIONAL
        :type combined_cid: ``int`` or ``HexList`` or ``None``
        :param press_fn: Flag indicating if we will force press the fn key before any other keystrokes - OPTIONAL
        :type press_fn: ``bool``

        :raise ``AssertionError``: If we received an unexpected message type
        """
        if isinstance(stimuli_masks, int):
            stimuli_masks = [stimuli_masks]
        # end if

        if isinstance(ctrl_id, int):
            ctrl_id = HexList(Numeral(ctrl_id, 2))
        # end if

        if isinstance(remapped_cid, int):
            remapped_cid = HexList(Numeral(remapped_cid, 2))
        # end if

        for stimuli_mask in stimuli_masks:
            if stimuli_mask & cls.StimulusMask.KEY_PRESSED_MASK:
                """
                Send stimulus
                """
                if hasattr(test_case, 'post_requisite_releasing_cid_key'):
                    test_case.post_requisite_releasing_cid_key = ctrl_id
                # end if
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f'Send CID = {ctrl_id} key pressed stimulus to DUT')
                # ------------------------------------------------------------------------------------------------------
                is_fn_key_diverted_event_expected = \
                    SpecialKeysMseButtonsTestUtils.send_key_by_attribute_flags(test_case, ctrl_id, MAKE, press_fn)

                has_hidpp_button_event_mask = (stimuli_mask >> cls.StimulusMask.HIDPP_BUTTON_EVENT_POS) & 1
                has_analytics_event_mask = (stimuli_mask >> cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_POS) & 1
                has_fn_inversion_event_mask = (stimuli_mask >> cls.StimulusMask.HIDPP_FN_INVERSION_EVENT_POS) & 1
                if is_fn_key_diverted_event_expected:
                    stimuli_mask |= cls.StimulusMask.HIDPP_BUTTON_EVENT_MASK
                # end if

                if test_case.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled:
                    _, fn_inversion_feature, _, _ = FnInversionForMultiHostDevicesTestUtils.HIDppHelper.get_parameters(
                        test_case=test_case)
                else:
                    fn_inversion_feature = None
                # end if

                """
                Verify stimulus event
                """
                if stimuli_mask & cls.StimulusMask.EXPECTED_EVENT_TYPE_MASK:
                    if has_hidpp_button_event_mask or has_analytics_event_mask or has_fn_inversion_event_mask:
                        number_of_stimuli = (has_hidpp_button_event_mask + has_analytics_event_mask +
                                             has_fn_inversion_event_mask)

                        inter_stimuli_mask = stimuli_mask
                        for _ in range(number_of_stimuli):
                            event = ChannelUtils.get_only(
                                test_case=test_case,
                                check_first_message=False,
                                queue_name=HIDDispatcher.QueueName.EVENT,
                                class_type=(
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_buttons_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_mouse_xy_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.analytics_key_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_wheel_event_cls
                                )
                                + ((fn_inversion_feature.f_lock_change_event_cls,) if fn_inversion_feature else tuple())
                            )

                            if isinstance(event, feature.diverted_buttons_event_cls) and \
                                    (inter_stimuli_mask & cls.StimulusMask.HIDPP_BUTTON_EVENT_MASK):
                                if press_expected_list_in_event is None:
                                    if is_fn_key_diverted_event_expected:
                                        if not has_hidpp_button_event_mask or has_analytics_event_mask:
                                            press_expected_list_in_event = [Numeral(0x34)]
                                        else:
                                            press_expected_list_in_event = [Numeral(0x34), ctrl_id]
                                        # end if
                                    else:
                                        press_expected_list_in_event = [ctrl_id]
                                    # end if
                                # end if

                                if len(press_expected_list_in_event) < 4:
                                    for _ in range(4 - len(press_expected_list_in_event)):
                                        press_expected_list_in_event.append(Numeral(0, 2))
                                    # end for
                                # end if

                                # --------------------------------------------------------------------------------------
                                LogHelper.log_check(
                                    test_case, 'Validate received divertedButtonsEvent = make '
                                               f'{[str(x) for x in press_expected_list_in_event]}')
                                # --------------------------------------------------------------------------------------
                                test_case.logTrace(f'{event.__class__.__name__}: {event}')
                                cls.check_diverted_button_event(test_case,
                                                                test_case.special_keys_and_mouse_buttons_feature,
                                                                press_expected_list_in_event,
                                                                event)
                                # Get the optional DivertedRawMouseXYEventV2toV6 notification providing the delta X & Y
                                # values accumulated since the last reset or reconnection
                                diverted_raw_xy_mouse_event = ChannelUtils.get_only(
                                    test_case=test_case,
                                    check_first_message=False, allow_no_message=True,
                                    queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=feature.diverted_raw_mouse_xy_event_cls
                                )
                                test_case.logTrace('Optional DivertedRawMouseXYEvent with accumulation since the last '
                                                   f'reset or reconnection: {str(diverted_raw_xy_mouse_event)}')
                                # This is done to detect if we receive two event of the same type,which is not
                                # supposed to happen
                                inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.HIDPP_BUTTON_EVENT_MASK
                                # Restore press_expected_list_in_event for Analytics key test
                                if is_fn_key_diverted_event_expected and \
                                        (stimuli_mask >> cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_POS) & 1:
                                    press_expected_list_in_event = None
                                # end if
                            elif isinstance(event, feature.analytics_key_event_cls) and \
                                    (inter_stimuli_mask & cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_MASK):
                                if press_expected_list_in_event is None:
                                    press_expected_list_in_event = [ctrl_id, HexList(1)]
                                # end if

                                if len(press_expected_list_in_event) < 10:
                                    for index in range(len(press_expected_list_in_event), 10):
                                        if index % 2 == 1:
                                            press_expected_list_in_event.append(HexList(0))
                                        else:
                                            press_expected_list_in_event.append(HexList(Numeral(0, 2)))
                                        # end if
                                    # end for
                                # end if

                                # --------------------------------------------------------------------------------------
                                LogHelper.log_check(
                                    test_case, f'Validate received analyticsKeyEvents  = '
                                               f'{[str(x) for x in press_expected_list_in_event]} and its HID packet')
                                # --------------------------------------------------------------------------------------
                                test_case.logTrace(f'{event.__class__.__name__}: {event}')
                                cls.check_analytics_key_events(test_case,
                                                               test_case.special_keys_and_mouse_buttons_feature,
                                                               press_expected_list_in_event,
                                                               event)
                                if not is_fn_key_diverted_event_expected:
                                    cls.check_hid_packet(test_case=test_case, cid=ctrl_id, action=MAKE)
                                # end if
                                # This is done to detect if we receive two event of the same type,which is not
                                # supposed to happen
                                inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_MASK
                            elif fn_inversion_feature is not None and \
                                    isinstance(event, fn_inversion_feature.f_lock_change_event_cls) and \
                                    (inter_stimuli_mask & cls.StimulusMask.HIDPP_FN_INVERSION_EVENT_MASK):
                                inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.HIDPP_FN_INVERSION_EVENT_MASK
                            else:
                                assert False, f'bad message type: expected {feature.diverted_buttons_event_cls} or ' \
                                              f'{feature.analytics_key_event_cls}, obtained {event.__class__()}'
                            # end if
                        # end for
                    # end if
                else:
                    if remapped_cid == HexList('0000'):
                        remapped_cid = ctrl_id
                    # end if

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(test_case, f'Validate received a make HID packet for CID = {remapped_cid}')
                    # --------------------------------------------------------------------------------------------------
                    cls.check_hid_packet(test_case=test_case, cid=remapped_cid, action=MAKE, combined_cid=combined_cid)
                    # Check that no HID++ event are received
                    ChannelUtils.check_queue_empty(
                        test_case=test_case, timeout=HUNDRED_MILLISECONDS, queue_name=HIDDispatcher.QueueName.EVENT,
                        class_type=(test_case.special_keys_and_mouse_buttons_feature.diverted_buttons_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_mouse_xy_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.analytics_key_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_wheel_event_cls))
                # end if

                # A sleep have to be introduce to avoid other button action too soon
                sleep(HUNDRED_MILLISECONDS)
            # end if

            if stimuli_mask & (cls.StimulusMask.POSITIVE_XY_MOVEMENT_MASK | cls.StimulusMask.NEGATIVE_XY_MOVEMENT_MASK):
                number_of_stimuli = ((stimuli_mask >> cls.StimulusMask.POSITIVE_XY_MOVEMENT_POS) & 1) + \
                                    ((stimuli_mask >> cls.StimulusMask.NEGATIVE_XY_MOVEMENT_POS) & 1)
                inter_stimuli_mask = stimuli_mask
                for _ in range(number_of_stimuli):
                    """
                    Send stimulus
                    """
                    if inter_stimuli_mask & cls.StimulusMask.POSITIVE_XY_MOVEMENT_MASK:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(test_case, 'Send positive XY movement by optical sensor Tool')
                        # ----------------------------------------------------------------------------------------------
                        dx = 5
                        dy = 5
                        inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.POSITIVE_XY_MOVEMENT_MASK
                    elif inter_stimuli_mask & cls.StimulusMask.NEGATIVE_XY_MOVEMENT_MASK:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(test_case, 'Send negative XY movement by optical sensor Tool')
                        # ----------------------------------------------------------------------------------------------
                        dx = -5
                        dy = -5
                        inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.NEGATIVE_XY_MOVEMENT_MASK
                    else:
                        assert False, "Mask error while sending XY displacement"
                    # end if

                    test_case.motion_emulator.xy_motion(dx=dx, dy=dy)
                    test_case.motion_emulator.commit_actions()
                    test_case.motion_emulator.prepare_sequence()

                    """
                    Verify stimulus event
                    """
                    if inter_stimuli_mask & cls.StimulusMask.HIDPP_RAW_XY_EVENT_MASK:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            test_case, 'Validate received divertedRawMouseXYEvent and check the XY movement values '
                                       'are the same as input')
                        # ----------------------------------------------------------------------------------------------
                        diverted_raw_xy_mouse_event = ChannelUtils.get_only(
                            test_case=test_case,
                            check_first_message=False,
                            queue_name=HIDDispatcher.QueueName.EVENT,
                            class_type=feature.diverted_raw_mouse_xy_event_cls
                        )
                        test_case.logTrace('DivertedRawMouseXYEvent: %s\n' % str(diverted_raw_xy_mouse_event))
                        if dx < 0:
                            dx = pow(2, feature.diverted_raw_mouse_xy_event_cls.LEN.DX) + dx
                        # end if
                        if dy < 0:
                            dy = pow(2, feature.diverted_raw_mouse_xy_event_cls.LEN.DY) + dy
                        # end if
                        test_case.assertEquals(expected=HexList(
                            Numeral(dx, ceil(feature.diverted_raw_mouse_xy_event_cls.LEN.DX / 8))),
                            obtained=diverted_raw_xy_mouse_event.dx,
                            msg="The dx parameter differs from the one expected")
                        test_case.assertEquals(expected=HexList(
                            Numeral(dy, ceil(feature.diverted_raw_mouse_xy_event_cls.LEN.DY / 8))),
                            obtained=diverted_raw_xy_mouse_event.dy,
                            msg="The dy parameter differs from the one expected")
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            test_case,
                            'Receive HID mouse XY displacement and check the XY movement values are the same as input')
                        # ----------------------------------------------------------------------------------------------
                        hid_packet = ChannelUtils.get_only(
                            test_case=test_case,
                            check_first_message=False,
                            queue_name=HIDDispatcher.QueueName.HID,
                            class_type=HidMouse
                        )
                        test_case.logTrace('HidMouse: %s\n' % str(hid_packet))
                        for field in hid_packet.FIELDS:
                            fid = field.getFid()
                            if field.name == 'x':
                                test_case.assertEquals(expected=dx,
                                                       obtained=hid_packet.get_absolute_value(fid),
                                                       msg="The dx parameter differs from the one expected")
                            elif field.name == 'y':
                                test_case.assertEquals(expected=dy,
                                                       obtained=hid_packet.get_absolute_value(fid),
                                                       msg="The dy parameter differs from the one expected")
                                test_case.check_queue_empty(
                                    queue=test_case.hidDispatcher.event_message_queue, during=HUNDRED_MILLISECONDS)
                            # end if
                        # end for
                    # end if
                # end for

                # A sleep have to be introduced to avoid other button action too soon
                sleep(HUNDRED_MILLISECONDS)
            # end if

            if stimuli_mask & (
                    cls.StimulusMask.POSITIVE_WHEEL_MOVEMENT_MASK | cls.StimulusMask.NEGATIVE_WHEEL_MOVEMENT_MASK):
                number_of_stimuli = ((stimuli_mask >> cls.StimulusMask.POSITIVE_WHEEL_MOVEMENT_POS) & 1) + \
                                    ((stimuli_mask >> cls.StimulusMask.NEGATIVE_WHEEL_MOVEMENT_POS) & 1)
                inter_stimuli_mask = stimuli_mask
                for _ in range(number_of_stimuli):
                    # Send stimulus
                    if inter_stimuli_mask & cls.StimulusMask.POSITIVE_WHEEL_MOVEMENT_MASK:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(test_case, 'Send positive Wheel movement')
                        # ----------------------------------------------------------------------------------------------
                        delta_v = test_case.main_wheel_emulator.MIN_DELTA_V
                        inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.POSITIVE_WHEEL_MOVEMENT_MASK
                    elif inter_stimuli_mask & cls.StimulusMask.NEGATIVE_XY_MOVEMENT_MASK:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(test_case, 'Send negative Wheel movement')
                        # ----------------------------------------------------------------------------------------------
                        delta_v = - test_case.main_wheel_emulator.MIN_DELTA_V
                        inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.NEGATIVE_WHEEL_MOVEMENT_MASK
                    else:
                        assert False, "Mask error while sending Wheel displacement"
                    # end if

                    test_case.main_wheel_emulator.set_delta_v(delta_v)

                    # Verify stimulus event
                    if inter_stimuli_mask & cls.StimulusMask.HIDPP_RAW_WHEEL_EVENT_MASK:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            test_case, 'Validate received divertedRawMouseXYEvent and check the wheel movement '
                                       'values are the same as input')
                        # ----------------------------------------------------------------------------------------------
                        diverted_raw_wheel_event_cls = \
                            test_case.special_keys_and_mouse_buttons_feature.diverted_raw_wheel_event_cls
                        diverted_raw_wheel_event = ChannelUtils.get_only(
                            test_case=test_case,
                            check_first_message=False,
                            queue_name=HIDDispatcher.QueueName.EVENT,
                            class_type=diverted_raw_wheel_event_cls
                        )
                        if delta_v < 0:
                            delta_v = pow(2, diverted_raw_wheel_event_cls.LEN.DELTA_V) + delta_v
                        # end if
                        test_case.assertEquals(
                            expected=HexList(Numeral(delta_v, diverted_raw_wheel_event_cls.LEN.DELTA_V // 8)),
                            obtained=diverted_raw_wheel_event.delta_v,
                            msg="The delta V parameter differs from the one expected")
                    else:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_check(
                            test_case, 'Receive HID mouse Wheel movement and check the wheel movement values are '
                                       'the same as input')
                        # ----------------------------------------------------------------------------------------------
                        hid_packet = ChannelUtils.get_only(
                            test_case=test_case,
                            check_first_message=False,
                            queue_name=HIDDispatcher.QueueName.HID,
                            class_type=HidMouse
                        )
                        for field in hid_packet.FIELDS:
                            fid = field.getFid()
                            if field.name() == 'wheel':
                                test_case.assertEquals(expected=delta_v,
                                                       obtained=hid_packet.get_absolute_value(fid),
                                                       msg="The dx parameter differs from the one expected")
                            # end if
                        # end for
                    # end if
                # end for

                # A sleep have to be introduce to avoid other button action too soon
                sleep(.3)
            # end if

            if stimuli_mask & cls.StimulusMask.KEY_RELEASED_MASK:
                """
                Send stimulus
                """
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, f'Send CID = {ctrl_id} key released stimulus to DUT')
                # ------------------------------------------------------------------------------------------------------
                is_fn_key_diverted_event_expected = \
                    SpecialKeysMseButtonsTestUtils.send_key_by_attribute_flags(test_case, ctrl_id, BREAK, press_fn)
                if hasattr(test_case, 'post_requisite_releasing_cid_key'):
                    test_case.post_requisite_releasing_cid_key = None
                # end if
                """
                Verify stimulus event
                """
                if stimuli_mask & cls.StimulusMask.EXPECTED_EVENT_TYPE_MASK:
                    if stimuli_mask & (
                            cls.StimulusMask.HIDPP_BUTTON_EVENT_MASK | cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_MASK):
                        number_of_stimuli = ((stimuli_mask >> cls.StimulusMask.HIDPP_BUTTON_EVENT_POS) & 1) + \
                                            ((stimuli_mask >> cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_POS) & 1)

                        inter_stimuli_mask = stimuli_mask
                        for _ in range(number_of_stimuli):
                            event = ChannelUtils.get_only(
                                test_case=test_case,
                                check_first_message=False,
                                queue_name=HIDDispatcher.QueueName.EVENT,
                                class_type=(
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_buttons_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_mouse_xy_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.analytics_key_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_wheel_event_cls)
                            )
                            if isinstance(event, feature.diverted_buttons_event_cls) and \
                                    (inter_stimuli_mask & cls.StimulusMask.HIDPP_BUTTON_EVENT_MASK):
                                if release_expected_list_in_event is None:
                                    release_expected_list_in_event = []
                                # end if

                                if len(release_expected_list_in_event) < 4:
                                    for _ in range(4 - len(release_expected_list_in_event)):
                                        release_expected_list_in_event.append(Numeral(0, 2))
                                    # end for
                                # end if

                                # --------------------------------------------------------------------------------------
                                LogHelper.log_check(
                                    test_case, f'Validate received divertedButtonsEvent = break '
                                               f'{[str(x) for x in release_expected_list_in_event]}')
                                # --------------------------------------------------------------------------------------
                                test_case.logTrace('%s: %s\n' % (event.__class__.__name__, str(event)))
                                cls.check_diverted_button_event(test_case,
                                                                test_case.special_keys_and_mouse_buttons_feature,
                                                                release_expected_list_in_event,
                                                                event)
                                # This is done to detect if we receive two event of the same type,which is not
                                # supposed to happen
                                inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.HIDPP_BUTTON_EVENT_MASK
                                # Restore release_expected_list_in_event
                                if is_fn_key_diverted_event_expected:
                                    release_expected_list_in_event = None
                                # end if
                            elif isinstance(event, feature.analytics_key_event_cls) and \
                                    (inter_stimuli_mask & cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_MASK):
                                if release_expected_list_in_event is None:
                                    release_expected_list_in_event = [ctrl_id]
                                # end if

                                if len(release_expected_list_in_event) < 10:
                                    for index in range(len(release_expected_list_in_event), 10):
                                        if index % 2 == 1:
                                            release_expected_list_in_event.append(HexList(0))
                                        else:
                                            release_expected_list_in_event.append(HexList(Numeral(0, 2)))
                                        # end if
                                    # end for
                                # end if

                                # --------------------------------------------------------------------------------------
                                LogHelper.log_check(
                                    test_case, f'Validate received analyticsKeyEvents = '
                                               f'{[str(x) for x in release_expected_list_in_event]} and its HID packet')
                                # --------------------------------------------------------------------------------------
                                test_case.logTrace('%s: %s\n' % (event.__class__.__name__, str(event)))
                                cls.check_analytics_key_events(test_case,
                                                               test_case.special_keys_and_mouse_buttons_feature,
                                                               release_expected_list_in_event,
                                                               event)
                                if not is_fn_key_diverted_event_expected:
                                    cls.check_hid_packet(test_case=test_case, cid=ctrl_id, action=BREAK)
                                # end if
                                # This is done to detect if we receive two event of the same type,which is not
                                # supposed to happen
                                inter_stimuli_mask &= 0xFFFF ^ cls.StimulusMask.HIDPP_ANALYTIC_KEY_EVENT_MASK
                                # Restore release_expected_list_in_event
                                if is_fn_key_diverted_event_expected:
                                    release_expected_list_in_event = None
                                # end if
                            elif isinstance(event, feature.diverted_raw_mouse_xy_event_cls):
                                LogHelper.log_trace(
                                    test_case,f'Unsolicited {feature.diverted_raw_mouse_xy_event_cls} event')
                            else:
                                assert False, f'bad message type: expected {feature.diverted_buttons_event_cls} or ' \
                                              f'{feature.analytics_key_event_cls}, obtained {event.__class__().name}'
                            # end if
                        # end for
                    # end if
                else:
                    if remapped_cid == HexList('0000'):
                        remapped_cid = ctrl_id
                    # end if

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(test_case, f'Validate received a break HID packet for CID = {remapped_cid}')
                    # --------------------------------------------------------------------------------------------------
                    cls.check_hid_packet(test_case=test_case, cid=remapped_cid, action=BREAK, combined_cid=combined_cid)
                    # Check that no HID++ event and no more HID packet are received
                    ChannelUtils.check_queue_empty(
                        test_case=test_case, timeout=HUNDRED_MILLISECONDS, queue_name=HIDDispatcher.QueueName.EVENT,
                        class_type=(test_case.special_keys_and_mouse_buttons_feature.diverted_buttons_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_mouse_xy_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.analytics_key_event_cls,
                                    test_case.special_keys_and_mouse_buttons_feature.diverted_raw_wheel_event_cls))
                    test_case.check_queue_empty(
                        queue=test_case.hidDispatcher.hid_message_queue, during=HUNDRED_MILLISECONDS)
                # end if

                # A sleep have to be introduce to avoid other button action too soon
                sleep(HUNDRED_MILLISECONDS)
            # end if
        # end for
    # end def send_stimulus_and_verify

    @classmethod
    def verify_response_and_stimulus_event(cls, test_case, feature, request, response_class, stimuli_mask,
                                           remapped_cid=0, combined_cid=None, press_fn=False):
        """
        Send SetCidReporting request and check response and stimulus event.

        The order of the stimuli is set to KEY_PRESSED_MASK, then XY_MOVEMENT_MASK and then KEY_RELEASED_MASK. If the
        order is not the one wanted, the stimuli masks can be sent as a list instead.

        :param test_case: The test case to use for asserts.
        :type test_case: ``BaseTestCase``
        :param feature: Feature interface
        :type feature: ``SpecialKeysMSEButtonsInterface``
        :param request: The request to send.
        :type request: ``SetCidReporting``
        :param response_class: The response class to expect.
        :type response_class: ``SetCidReportingResponse``
        :param stimuli_mask: Stimuli masks to use (can be a List of masks).
        :type stimuli_mask: ``int`` or ``list``
        :param remapped_cid: The remap target's CtrlD to check. This parameter will only be used if the expected
                             stimulus event is a HID packet. Otherwise, it is ignored. If = 0, it will check ctrl_id
                             instead - OPTIONAL
        :type remapped_cid: ``int``
        :param combined_cid: The second cid which is combined with the cid input to enable the HID consumer report
                             verification. - OPTIONAL
        :type combined_cid: ``int`` or ``HexList`` or ``None``
        :param press_fn: Flag indicating if we will force press the fn key before any other keystrokes - OPTIONAL
        :type press_fn: ``bool``
        """
        set_cid_reporting_response = ChannelUtils.send(
            test_case=test_case,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(test_case, 'Validate setCidReporting response parameters should be the same as inputs')
        # --------------------------------------------------------------------------------------------------------------

        cls.check_response_expected_field(test_case, request, set_cid_reporting_response)
        cls.send_stimulus_and_verify(test_case=test_case,
                                     feature=feature,
                                     ctrl_id=request.ctrl_id,
                                     stimuli_masks=stimuli_mask,
                                     remapped_cid=remapped_cid,
                                     combined_cid=combined_cid,
                                     press_fn=press_fn)
    # end def verify_response_and_stimulus_event

    @classmethod
    def verify_response_and_stimulus_event_power_reset(cls, test_case, feature, request, response_class,
                                                       stimuli_mask_before, stimuli_mask_after):
        """
        Send SetCidReporting request and check response and stimulus event.

        The order of the stimuli is set to KEY_PRESSED_MASK, then XY_MOVEMENT_MASK and then KEY_RELEASED_MASK. If the
        order is not the one wanted, the stimuli masks can be sent as a list instead.

        :param test_case: The test case to use for asserts.
        :type test_case: ``BaseTestCase``
        :param feature: Feature interface
        :type feature: ``SpecialKeysMSEButtonsInterface``
        :param request: The request to send.
        :type request: ``SetCidReporting``
        :param response_class: The response class to expect.
        :type response_class: ``SetCidReportingResponse``
        :param stimuli_mask_before: Stimuli masks to use before power reset (can be a List of masks).
        :type stimuli_mask_before: ``int`` or ``list``
        :param stimuli_mask_after: Stimuli masks to use after power reset (can be a List of masks).
        :type stimuli_mask_after: ``int`` or ``list``
        """
        cls.verify_response_and_stimulus_event(test_case=test_case, feature=feature, request=request,
                                               response_class=response_class, stimuli_mask=stimuli_mask_before)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Restart DUT')
        # --------------------------------------------------------------------------------------------------------------
        test_case.reset(hardware_reset=True)

        cls.send_stimulus_and_verify(test_case=test_case,
                                     feature=feature,
                                     ctrl_id=request.ctrl_id,
                                     stimuli_masks=stimuli_mask_after)
    # end def verify_response_and_stimulus_event_power_reset
# end class SpecialKeysMseButtonsTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
