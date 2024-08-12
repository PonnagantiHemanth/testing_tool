# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@package    pytestbox.hid.mouse.feature_2110_interface
@brief      Validates HID mouse feature 0x2110 interface test cases
@author     Fred Chen
@date       2019/10/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pytestbox.base.basetest import BaseTestCase
from pyharness.selector import features
from pyharness.extensions import level
from pyhid.hidpp.features.mouse.smartshift import SmartShift
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlModeResponse
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlModeResponse
from pyhid.hidpp.features.hireswheel import RatchetSwitchEvent
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV1Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV2Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV3Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV4Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV5toV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV1
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV2
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV3
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV4
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV5toV6
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV1Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV2Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV3Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV4Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import SetCidReportingV5ToV6Response
from pyhid.hidpp.features.common.specialkeysmsebuttons import DivertedButtonsEvent
from pyhid.hid.hidmouse import HidMouse
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytransport.transportcontext import TransportContextException


# ------------------------------------------------------------------------------
# constant
# ------------------------------------------------------------------------------
DONOTCHANGE = SmartShift.WheelMode.DoNotChange  # can be used for auto_disengage and auto_disengage_default
FREESPIN = SmartShift.WheelMode.FreeSpin
RATCHET = SmartShift.WheelMode.Ratchet


CID_TO_GPIO_TABLE = {0x0050: 0,
                     0x0051: 1,
                     0x0052: 2,
                     0x0053: 3,
                     0x0056: 4,
                     0x00C3: 5,
                     0x00C4: 6, }


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class SmartShiftBaseClassTestCase(BaseTestCase):
    """
    SmartShift Base Class
    """

    def setUp(self):
        """
        Handles test prerequisites.
        """
        # flags for teardown
        self.teardown_restore_ratchet = False
        self.teardown_restore_remap = False
        self.teardown_restore_remap_cid = None
        self.teardown_restore_remap_remapped_cid = None
        self.teardown_restore_divert = False
        self.cur_settings = None
        super(SmartShiftBaseClassTestCase, self).setUp()

        # ---------------------------------------------------------------------------
        self.logTitle2('Pre-requisite#1: Send Root.GetFeature(0x2110)')
        # ---------------------------------------------------------------------------
        self.feature_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=SmartShift.FEATURE_ID)
    # end def setUp

    def tearDown(self):
        """
        Handles test prerequisites.
        """
        # noinspection PyBroadException
        try:
            if self.teardown_restore_ratchet or self.teardown_restore_remap or self.teardown_restore_divert:
                # ---------------------------------------------------------------------------
                self.logTitle2('Post-requisite#1: Reload and verify the value stored during pre-requisite')
                # ---------------------------------------------------------------------------
                restore_settings(test_case=self)
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try

        super(SmartShiftBaseClassTestCase, self).tearDown()
    # end def tearDown

# end class SmartShiftBaseClassTestCase


class SmartShiftInterfaceTestCase(SmartShiftBaseClassTestCase):
    """
    Validates SmartShift Interface TestCases
    """

    @features('Feature2110')
    @level('Interface')
    def test_GetRatchetControlModeAPI(self):
        """
        @tc_synopsis Validates getRatchetControlMode API (Feature 0x2110)

        [0] getRatchetControlMode() -> wheelMode, autoDisengage, autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send getRatchetControlMode')
        # ---------------------------------------------------------------------------
        response = get_ratchet_control_mode(test_case=self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate returned values are in valid range')
        # ---------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response, check_valid_range=True)

        self.testCaseChecked("FNT_2110_0001")
    # end def test_GetRatchetControlModeAPI

    @features('Feature2110')
    @level('Interface')
    def test_SetRatchetControlModeAPI(self):
        """
        @tc_synopsis Validates setRatchetControlMode API (Feature 0x2110)

        [1] setRatchetControlMode(wheelMode, autoDisengage, autoDisengageDefault) -> wheelMode, autoDisengage,
            autoDisengageDefault
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Send setRatchetControlMode with the values to 0')
        # ---------------------------------------------------------------------------
        response = set_ratchet_control_mode(test_case=self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Validate returned values are the echo of the request')
        # ---------------------------------------------------------------------------
        verify_ratchet_control_mode(test_case=self, response=response)

        self.testCaseChecked("FNT_2110_0002")
    # end def test_SetRatchetControlModeAPI

# end class SmartShiftInterfaceTestCase


def restore_settings(test_case):
    """
    Restore settings after finished a test

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    """
    if test_case.teardown_restore_ratchet:
        response = set_ratchet_control_mode(test_case=test_case,
                                            wheel_mode=test_case.cur_settings.wheel_mode,
                                            auto_disengage=test_case.cur_settings.auto_disengage,
                                            auto_disengage_default=test_case.cur_settings.auto_disengage_default)
        verify_ratchet_control_mode(test_case=test_case, response=response,
                                    wheel_mode=test_case.cur_settings.wheel_mode,
                                    auto_disengage=test_case.cur_settings.auto_disengage,
                                    auto_disengage_default=test_case.cur_settings.auto_disengage_default)
    # end if

    if test_case.teardown_restore_remap:
        set_cid_reporting_response = remap_button(test_case=test_case,
                                                  cid=test_case.teardown_restore_remap_cid,
                                                  remap_id=test_case.teardown_restore_remap_remapped_cid)
        verify_remap_button(test_case=test_case,
                            response=set_cid_reporting_response,
                            expected_cid=test_case.teardown_restore_remap_cid,
                            expected_remap_cid=test_case.teardown_restore_remap_remapped_cid)
    # end if

    if test_case.teardown_restore_divert:
        set_cid_reporting_response = divert_button(test=test_case,
                                                   cid=0xC4,
                                                   divert_valid=1,
                                                   divert=0)
        verify_divert_button(test=test_case, response=set_cid_reporting_response,
                             expected_cid=0xC4, divert_valid=1, divert=0)
    # end if
# end def restore_settings


def get_ratchet_control_mode(test_case):
    """
    Get the ratchet control settings

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :return: response data from DUT
    :rtype: ``GetRatchetControlModeResponse``
    """
    get_ratchet_ctrl_mode = GetRatchetControlMode(device_index=ChannelUtils.get_device_index(test_case=test_case),
                                                  feature_index=test_case.feature_index)
    return ChannelUtils.send(
        test_case=test_case, report=get_ratchet_ctrl_mode, response_queue_name=HIDDispatcher.QueueName.MOUSE,
        response_class_type=GetRatchetControlModeResponse)
# end def get_ratchet_control_mode


def set_ratchet_control_mode(test_case, wheel_mode=DONOTCHANGE, auto_disengage=DONOTCHANGE,
                             auto_disengage_default=DONOTCHANGE):
    """
    Set the ratchet control settings

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :param wheel_mode: possible wheel mode
    :type wheel_mode: ``int``
    :param auto_disengage: auto disengage value
    :type auto_disengage: ``int``
    :param auto_disengage_default: default value of auto disengage
    :type auto_disengage_default: ``int``
    :return: response data from DUT
    :rtype: ``SetRatchetControlModeResponse``
    """
    set_ratchet_ctrl_mode = SetRatchetControlMode(
        device_index=ChannelUtils.get_device_index(test_case=test_case), feature_index=test_case.feature_index,
        wheel_mode=int(Numeral(wheel_mode)), auto_disengage=int(Numeral(auto_disengage)),
        auto_disengage_default=int(Numeral(auto_disengage_default)))
    return ChannelUtils.send(
        test_case=test_case, report=set_ratchet_ctrl_mode, response_queue_name=HIDDispatcher.QueueName.MOUSE,
        response_class_type=SetRatchetControlModeResponse)
# end def set_ratchet_control_mode


def verify_ratchet_control_mode(test_case, response, wheel_mode=DONOTCHANGE, auto_disengage=DONOTCHANGE,
                                auto_disengage_default=DONOTCHANGE, check_valid_range=False):
    """
    Verify API response

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :param  response: response data from DUT
    :type response: ``SetRatchetControlModeResponse`` or ``GetRatchetControlModeResponse``
    :param wheel_mode: possible wheel mode
    :type wheel_mode: ``int``
    :param auto_disengage: auto disengage value
    :type auto_disengage: ``int``
    :param auto_disengage_default: default value of auto disengage
    :type auto_disengage_default: ``int``
    :param check_valid_range: check settings is in valid range
    :type check_valid_range: ``int``
    """
    if check_valid_range:
        test_case.assertNotEqual(unexpected=DONOTCHANGE, obtained=int(Numeral(response.wheel_mode)),
                                 msg=f'The wheel_mode={int(Numeral(response.wheel_mode))} is invalid')
        test_case.assertLessEqual(a=int(Numeral(response.wheel_mode)), b=RATCHET,
                                  msg=f'The wheel_mode={int(Numeral(response.wheel_mode))} is invalid')
    else:
        test_case.assertEqual(expected=int(Numeral(wheel_mode)), obtained=int(Numeral(response.wheel_mode)),
                              msg=f'The wheel_mode={int(Numeral(response.wheel_mode))} differs from the one expected')
        test_case.assertEqual(expected=int(Numeral(auto_disengage)), obtained=int(Numeral(response.auto_disengage)),
                              msg=f'The auto_disengage={int(Numeral(response.auto_disengage))} differs from the one '
                                  f'expected')
        test_case.assertEqual(expected=int(Numeral(auto_disengage_default)),
                              obtained=int(Numeral(response.auto_disengage_default)),
                              msg=f'The auto_disengage_default={int(Numeral(response.auto_disengage_default))} '
                                  f'differs from the one expected')
    # end if
# end def verify_ratchet_control_mode


def check_ratchet_switch_event(test_case, wheel_mode):
    """
    Check 0x2121 Ratchet Switch Event

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :param wheel_mode: possible wheel mode
    :type wheel_mode: ``int``
    """
    ratchet_switch_event = ChannelUtils.get_only(
        test_case=test_case, queue_name=HIDDispatcher.QueueName.EVENT, class_type=RatchetSwitchEvent,
        check_first_message=False, timeout=3)
    test_case.assertEqual(expected=int(Numeral(wheel_mode))-1, obtained=int(Numeral(ratchet_switch_event.state)),
                          msg='The wheel_mode parameter differs from the one expected')
# end def check_ratchet_switch_event


def verify_keystroke(test_case, cid):
    """
    Verify keystroke from HID packets

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``t
    :param cid: button control ID
    :type cid: ``int``
    """
    hid_packet_make = ChannelUtils.get_only(
        test_case=test_case, queue_name=HIDDispatcher.QueueName.HID, class_type=HidMouse)
    hid_packet_break = ChannelUtils.get_only(
        test_case=test_case, queue_name=HIDDispatcher.QueueName.HID, class_type=HidMouse)
    target_button = f'button{CID_TO_GPIO_TABLE[int(Numeral(cid))] + 1}'
    for f in hid_packet_make.FIELDS:
        if f.name == target_button:
            test_case.assertEqual(expected=1, obtained=int(Numeral(hid_packet_make.getValue(f.fid))),
                                  msg=f'The {f.name} parameter differs from the one expected')
        else:
            test_case.assertEqual(expected=0, obtained=int(Numeral(hid_packet_make.getValue(f.fid))),
                                  msg=f'The {f.name} parameter differs from the one expected')
        # end if
    # end for
    for f in hid_packet_break.FIELDS:
        if f.name == target_button:
            test_case.assertEqual(expected=0, obtained=int(Numeral(hid_packet_break.getValue(f.fid))),
                                  msg=f'The {f.name} parameter differs from the one expected')
        # end if
    # end for
# end def verify_keystroke


def get_1b04_classes(test):
    """
    Get the supported classes by 0x1B04 version

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    @return:        [out] (list)        supported classes list
    """
    get_cid_info_response_class = None
    set_cid_reporting_class = None
    set_cid_reporting_response_class = None
    f = test.getFeatures()
    if f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_1:
        get_cid_info_response_class = GetCidInfoV1Response
        set_cid_reporting_class = SetCidReportingV1
        set_cid_reporting_response_class = SetCidReportingV1Response
    elif f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_2:
        get_cid_info_response_class = GetCidInfoV2Response
        set_cid_reporting_class = SetCidReportingV2
        set_cid_reporting_response_class = SetCidReportingV2Response
    elif f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_3:
        get_cid_info_response_class = GetCidInfoV3Response
        set_cid_reporting_class = SetCidReportingV3
        set_cid_reporting_response_class = SetCidReportingV3Response
    elif f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_4:
        get_cid_info_response_class = GetCidInfoV4Response
        set_cid_reporting_class = SetCidReportingV4
        set_cid_reporting_response_class = SetCidReportingV4Response
    elif f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_5:
        get_cid_info_response_class = GetCidInfoV5toV6Response
        set_cid_reporting_class = SetCidReportingV5toV6
        set_cid_reporting_response_class = SetCidReportingV5ToV6Response
    # end if

    test.assertTrue(expr=get_cid_info_response_class is not None,
                    msg="Could not know which version is supported")

    return get_cid_info_response_class, set_cid_reporting_class, set_cid_reporting_response_class
# end def get_1b04_classes


def remap_button(test_case, cid, remap_id):
    """
    Remap cid to remap_cid

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :param cid: button control ID
    :type cid: ``int``
    :param remap_id: button control ID to remap
    :type remap_id: ``int``
    :return: set cid reporting response class
    :rtype: ``SetCidReportingV1Response`` to ``SetCidReportingV5ToV6Response``
    """
    set_cid_reporting = test_case.set_cid_reporting_class(
        device_index=ChannelUtils.get_device_index(test_case=test_case),
        feature_index=test_case.specialkeysmousebuttons_feature_index,
        ctrl_id=int(Numeral(cid)), remap=int(Numeral(remap_id)))
    set_cid_reporting_response = ChannelUtils.send(
        test_case=test_case, report=set_cid_reporting, response_queue_name=HIDDispatcher.QueueName.COMMON,
        response_class_type=test_case.set_cid_reporting_response_class)

    return set_cid_reporting_response
# end def remap_button


def get_cids_can_remap_to_c4(test_case):
    """
    Get cid list that can be remapped to 0xC4 (SmartShift)

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :return: cid list
    :rtype: ``list``
    """
    group_id_00c4 = [int(cid_info[12:14])
                     for cid_info in test_case.config_manager.get_feature(test_case.config_manager.ID.CID_TABLE)
                     if HexList(cid_info[:4]) == HexList('00C4')]
    cids_can_remap_to_00c4 = [
        HexList(cid_info[:4])
        for cid_info in test_case.config_manager.get_feature(test_case.config_manager.ID.CID_TABLE)
        if cid_info[:4] != '00C4' and
        (int(cid_info[14:16]) & 2 ** (group_id_00c4[0] - 1)) == 2 ** (group_id_00c4[0] - 1)]
    return cids_can_remap_to_00c4
# end def get_cids_can_remap_to_c4


def get_cids_for_c4_can_remap_to(test):
    """
    Get th cid list that 0xC4 (SmartShift) can be remapped to

    @param test:    [in] (test case)    an instance of test case object
    @return:        [out] (list)        cid list
    """
    gmask_00c4 = [int(cid_info[14:16])
                  for cid_info in test.config_manager.get_feature(test.config_manager.ID.CID_TABLE)
                  if HexList(cid_info[:4]) == HexList('00C4')]
    cids_for_c4_can_remap_to = [HexList(cid_info[:4])
                                for cid_info in test.config_manager.get_feature(test.config_manager.ID.CID_TABLE)
                                if cid_info[:4] != '00C4' and
                                (2 ** (int(cid_info[12:14]) - 1) & gmask_00c4[0]) == 2 ** (int(cid_info[12:14]) - 1)]
    return cids_for_c4_can_remap_to
# end def get_cids_for_c4_can_remap_to


def verify_remap_button(test_case, response, expected_cid, expected_remap_cid):
    """
    Verify remap button result

    :param test_case: The current test case
    :type test_case: ``CommonBaseTestCase``
    :param response: response data from DUT
    :type response: `SetCidReportingV1Response`` to ``SetCidReportingV5ToV6Response``
    :param expected_cid: button control ID
    :type expected_cid: ``int``
    :param expected_remap_cid:  [in] (int)      expected remap cid value
    :type expected_remap_cid: ``int``
    """
    test_case.assertEqual(expected=int(Numeral(expected_cid)), obtained=int(Numeral(response.ctrl_id)),
                          msg='The ctrl_id parameter differs from the one expected')
    test_case.assertEqual(expected=int(Numeral(expected_remap_cid)), obtained=int(Numeral(response.remap)),
                          msg='The remap parameter differs from the one expected')
# end def verify_remap_button


def divert_button(test, cid, divert_valid, divert):
    """
    Divert cid button

    @param test:                        [in] (test case)    an instance of test case object
    @param cid:                         [in] (int)          button control ID
    @param divert_valid:                [in] (int)          divert_valid flag
    @param divert:                      [in] (int)          divert flag
    @return:                            [out] (class)       response data from DUT
    """
    set_cid_reporting = test.set_cid_reporting_class(
        device_index=ChannelUtils.get_device_index(test_case=test),
        feature_index=test.specialkeysmousebuttons_feature_index,
        ctrl_id=int(Numeral(cid)), divert_valid=int(Numeral(divert_valid)), divert=int(Numeral(divert)))
    set_cid_reporting_response = ChannelUtils.send(
        test_case=test, report=set_cid_reporting, response_queue_name=HIDDispatcher.QueueName.COMMON,
        response_class_type=test.set_cid_reporting_response_class)

    return set_cid_reporting_response
# end def divert_button


def verify_divert_button(test, response, expected_cid, divert_valid, divert):
    """
    Verify divert button result

    @param test:            [in] (test case)    an instance of test case object
    @param response:        [in] (class)        response data from DUT
    @param expected_cid:    [in] (int)          expected button control ID
    @param divert_valid:    [in] (int)          expected divert_valid flag
    @param divert:          [in] (int)          expected divert flag
    """
    test.assertEqual(expected=int(Numeral(expected_cid)),
                     obtained=int(Numeral(response.ctrl_id)),
                     msg='The divert parameter differs from the one expected')
    test.assertEqual(expected=int(Numeral(divert)),
                     obtained=int(Numeral(response.divert)),
                     msg='The divert parameter differs from the one expected')
    test.assertEqual(expected=int(Numeral(divert_valid)),
                     obtained=int(Numeral(response.divert_valid)),
                     msg='The divert_valid parameter differs from the one expected')
# end def verify_divert_button


def verify_divert_event(test, expected_make, expected_break):
    """
    Verify divert event

    @param test:            [in] (test case)    an instance of test case object
    @param expected_make:   [in] (list)         expected make state for 4 cids
    @param expected_break:  [in] (list)         expected break state for 4 cids
    """
    divert_make = ChannelUtils.get_only(
        test_case=test, queue_name=HIDDispatcher.QueueName.EVENT, class_type=DivertedButtonsEvent)
    divert_break = ChannelUtils.get_only(
        test_case=test, queue_name=HIDDispatcher.QueueName.EVENT, class_type=DivertedButtonsEvent)
    test.assertEqual(expected=expected_make[0],
                     obtained=int(Numeral(divert_make.ctrl_id_1)),
                     msg='The ctrl_id_1 parameter differs from the one expected')
    test.assertEqual(expected=expected_make[1],
                     obtained=int(Numeral(divert_make.ctrl_id_2)),
                     msg='The ctrl_id_2 parameter differs from the one expected')
    test.assertEqual(expected=expected_make[2],
                     obtained=int(Numeral(divert_make.ctrl_id_3)),
                     msg='The ctrl_id_3 parameter differs from the one expected')
    test.assertEqual(expected=expected_make[3],
                     obtained=int(Numeral(divert_make.ctrl_id_4)),
                     msg='The ctrl_id_4 parameter differs from the one expected')
    test.assertEqual(expected=expected_break[0],
                     obtained=int(Numeral(divert_break.ctrl_id_1)),
                     msg='The ctrl_id_1 parameter differs from the one expected')
    test.assertEqual(expected=expected_break[1],
                     obtained=int(Numeral(divert_break.ctrl_id_2)),
                     msg='The ctrl_id_2 parameter differs from the one expected')
    test.assertEqual(expected=expected_break[2],
                     obtained=int(Numeral(divert_break.ctrl_id_3)),
                     msg='The ctrl_id_3 parameter differs from the one expected')
    test.assertEqual(expected=expected_break[3],
                     obtained=int(Numeral(divert_break.ctrl_id_4)),
                     msg='The ctrl_id_4 parameter differs from the one expected')
# end def verify_divert_event


def reset_device_by_x1802(test):
    """
    Software reset DUT

    @param test:    [in] (test case)    an instance of test case object
    """
    force_device_reset = ForceDeviceReset(deviceIndex=ChannelUtils.get_device_index(test_case=test),
                                          featureId=test.devicereset_feature_index)
    try:
        ChannelUtils.send_only(test_case=test, report=force_device_reset, timeout=.6)
    except TransportContextException as e:
        if e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                             TransportContextException.Cause.CONTEXT_ERROR_IO,
                             TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
            pass
        else:
            raise
        # end if
    # end try
    # Wait for the receiver to send back the DeviceConnection notification
    # It seems that in Unifying it is not happening.
    # TODO However it seems to be sent by Unifying gaming receiver (tested with footloose), it would be
    #  interesting to investigate a better solution
    if not isinstance(test.current_channel, ThroughEQuadReceiverChannel):
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test)
    # end if
# end def reset_device_by_x1802

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
