#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.robustness
:brief: HID++ 2.0 Special Keys MSE Buttons robustness test suite
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/06/05
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import CidInfoPayload
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueEmpty
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.cidutils import CidEmulation
from pytestbox.base.cidutils import CidInfoFlags
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.hidpp20.common.feature_1b04.specialkeysmsebuttons import SpecialKeysMSEButtonsTestCase
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMSEButtonsRobustnessTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the Keyboard reprogrammable Keys and Mouse buttons Robustness TestCases.
    """
    @features('Feature1B04')
    @level('Robustness')
    def test_padding(self):
        """
        Validate the GetCount padding bytes are ignored
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over GetCount padding range (several interesting values)')
        # --------------------------------------------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(
                self.special_keys_and_mouse_buttons_feature.get_count_cls.DEFAULT.PADDING,
                self.special_keys_and_mouse_buttons_feature.get_count_cls.LEN.PADDING // 8))):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send GetCount with several value for padding (alternate enable '
                                     'byte to 0 and 1)')
            # ----------------------------------------------------------------------------------------------------------
            get_count = self.special_keys_and_mouse_buttons_feature.get_count_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id)
            get_count.padding = padding_byte
            get_count_response = ChannelUtils.send(
                test_case=self,
                report=get_count,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.special_keys_and_mouse_buttons_feature.get_count_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetCount.count Byte value')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_count.deviceIndex,
                             obtained=get_count_response.deviceIndex,
                             msg='The deviceIndex parameter differs from the one expected')
            self.assertEqual(expected=get_count.featureIndex,
                             obtained=get_count_response.featureIndex,
                             msg='The featureIndex parameter differs from the one expected')
            f = self.getFeatures()
            self.assertEqual(expected=HexList(f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidCount),
                             obtained=get_count_response.count,
                             msg='The count parameter differs from the one expected')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_1B04_0018")
    # end def test_padding
# end class SpecialKeysMSEButtonsRobustnessTestCase


class SpecialKeysMSEButtonsRobustnessEmuTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the Keyboard reprogrammable Keys and Mouse buttons Robustness TestCases.
    """
    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Robustness')
    def set_cid_reporting_remap_robustness(self):
        """
        Validate the  setCidReporting.remap on a Cid which doesn't belong to one of the specified groups (
        getCidInfo.gmask)

        Since the group information is only informative and does not force a valid range, the remap should still work.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        self.assertTrue(expr=set_cid_reporting_class is not None,
                        msg="Could not know which version is supported")

        self.assertTrue(expr=set_cid_reporting_class is not None,
                        msg="Could not know which version is supported")

        # Virtual buttons are ignored for now
        cid_group_gmask_list = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                for cid_info in self.emu_cid_info_list
                                if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over (CID, group, gmask) values in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for (cid, group, gmask) in cid_group_gmask_list:
            if group == self.NO_GROUP:
                # if CID does not belong to a group, remapping is not possible
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over remapped CID which does not belong to one of the '
                                     f'specified groups that CID = {cid} can be remapped to')
            # ----------------------------------------------------------------------------------------------------------
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask) or other_group == self.NO_GROUP:
                    continue
                # end if

                group_mask = (1 << (other_group - 1)) if other_group != 0 else 0

                if (gmask & group_mask) == 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'remap = {other_cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=other_cid)
                    # This function do test step 2 and 3, and check 1 to 3
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
                        remapped_cid=other_cid)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop end')
            # ----------------------------------------------------------------------------------------------------------

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set remap = '
                                     f'{cid} and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid,
                                                        remap=cid)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same '
                                      'as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def set_cid_reporting_remap_robustness

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(set_cid_reporting_remap_robustness)
    def test_set_cid_reporting_remap_robustness_limited(self):
        # See ``set_cid_reporting_remap_robustness``
        self.set_cid_reporting_remap_robustness()
        self.testCaseChecked("ROB_1B04_0009#limited")
    # end def test_set_cid_reporting_remap_robustness_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(set_cid_reporting_remap_robustness)
    def test_set_cid_reporting_remap_robustness_full(self):
        # See ``set_cid_reporting_remap_robustness``
        self.set_cid_reporting_remap_robustness()
        self.testCaseChecked("ROB_1B04_0009#full")
    # end def test_set_cid_reporting_remap_robustness_full

    def _set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down(self):
        """
        Validate the  divertedButtonsEvent.cid list processing: test 1, 2, 3, 4 then 5 CID make, and 5, 4, 3, 2
        then 1 CID break.

        Since divertedButtonsEvent can only have 4 cids, cid 5 should not trigger any divertedButtonsEvent and
        be ignored.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        self._divert_5buttons_make_and_break(break_down=True)
    # end def _set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED, 5)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down)
    def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down_limited(self):
        # See ``_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down``
        self._set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down()
        self.testCaseChecked("ROB_1B04_0010#limited")
    # end def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL, 5)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down)
    def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down_full(self):
        # See ``_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down``
        self._set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down()
        self.testCaseChecked("ROB_1B04_0010#full")
    # end def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_down_full

    def set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up(self):
        """
        Validate the  divertedButtonsEvent.cid list processing: test 1, 2, 3, 4 then 5 CID make, and 1, 2, 3, 4
        then 5 CID break.

        Since divertedButtonsEvent can only have 4 cids, cid 5 should not trigger any divertedButtonsEvent and
        be ignored.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        self._divert_5buttons_make_and_break(break_down=False)
    # end def set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED, 5)
    @level('Robustness')
    @services('PassiveHoldPress')
    @bugtracker('DivertedButtonsEvent_5th_CID_fill_in')
    @DocUtils.copy_doc(set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up)
    def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up_limited(self):
        # See ``set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up``
        self.set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up()
        self.testCaseChecked("ROB_1B04_0011#limited")
    # end def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL, 5)
    @level('Robustness')
    @services('PassiveHoldPress')
    @bugtracker('DivertedButtonsEvent_5th_CID_fill_in')
    @DocUtils.copy_doc(set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up)
    def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up_full(self):
        # See ``set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up``
        self.set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up()
        self.testCaseChecked("ROB_1B04_0011#full")
    # end def test_set_cid_reporting_diverted_button_event_5_buttons_make_up_break_up_full

    def _set_cid_reporting_diverted_integrity_while_button_pressed(self):
        """
        Validate the  divertedButtonsEvent.cid list processing: Configuration changes such as diverting or undiverting
        a pressed button does not affect this list until the diverted button is released

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        self.assertTrue(expr=set_cid_reporting_class is not None,
                        msg="Could not know which version is supported")

        # Virtual and Host Switch buttons are ignored for now
        cid_list_d = []
        for cid_info_raw_data in self.emu_cid_info_list:
            cid_info = CidInfoPayload.fromHexList(HexList(cid_info_raw_data))
            if cid_info.flags.divert and not cid_info.flags.virtual and Numeral(
                    cid_info.cid) not in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2, CidTable.HOST_SWITCH_3]:
                cid_list_d.append(cid_info.cid)
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Choose CID1 = {cid_list_d[0]} and CID2 = {cid_list_d[1]} from the '
                                 f'list of CIDs with divert capability')
        # --------------------------------------------------------------------------------------------------------------
        cid_1 = cid_list_d[0]
        cid_2 = cid_list_d[1]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_1} and set divert = 1, '
                                 f'dvalid = 1 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                    feature_index=self.feature_id,
                                                    ctrl_id=cid_1,
                                                    divert_valid=True,
                                                    divert=True)
        # This function do test step 3, and check 1 and 2
        SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            request=set_cid_reporting,
            response_class=set_cid_reporting_response_class,
            stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_2} and set divert = 1, '
                                 f'dvalid = 1 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                    feature_index=self.feature_id,
                                                    ctrl_id=cid_2,
                                                    divert_valid=True,
                                                    divert=True)
        # This function do test step 5 and 6, and check 3 to 5
        SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            request=set_cid_reporting,
            response_class=set_cid_reporting_response_class,
            stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)
        # This function do test step 7 and 8, and check 6 and 7
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_1,
            stimuli_masks=[SpecialKeysMseButtonsTestUtils.StimulusMask.RRD,
                           SpecialKeysMseButtonsTestUtils.StimulusMask.PRD])
        # This function do test step 9, and check 8
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_2,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD,
            press_expected_list_in_event=[cid_1, cid_2])
        # This function do test step 10, and check 9
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_2,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRD,
            release_expected_list_in_event=[cid_1])
        # This function do test step 11, and check 10
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_1,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRD)

        # This loop do test step 12 and 13, and check 11 and 12
        for cid_d in cid_list_d[:2]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d} and set divert ='
                                     f' 0, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=True,
                                                        divert=False)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Validate setCidReporting response parameters should be the same'
                                      f' as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
    # end def _set_cid_reporting_diverted_integrity_while_button_pressed

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED, 2)
    @level('Robustness')
    @services('PassiveHoldPress')
    @bugtracker("DivertOnPress")
    @DocUtils.copy_doc(_set_cid_reporting_diverted_integrity_while_button_pressed)
    def test_set_cid_reporting_diverted_integrity_while_button_limited(self):
        # See ``_set_cid_reporting_diverted_integrity_while_button_pressed``
        self._set_cid_reporting_diverted_integrity_while_button_pressed()
        self.testCaseChecked("ROB_1B04_0012#limited")
    # end def test_set_cid_reporting_diverted_integrity_while_button_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL, 2)
    @level('Robustness')
    @services('PassiveHoldPress')
    @bugtracker("DivertOnPress")
    @DocUtils.copy_doc(_set_cid_reporting_diverted_integrity_while_button_pressed)
    def test_set_cid_reporting_diverted_integrity_while_button_full(self):
        # See ``_set_cid_reporting_diverted_integrity_while_button_pressed``
        self._set_cid_reporting_diverted_integrity_while_button_pressed()
        self.testCaseChecked("ROB_1B04_0012#full")
    # end def test_set_cid_reporting_diverted_integrity_while_button_full

    def _set_cid_reporting_diverted_button_event_5_buttons(self):
        """
        Validate the  divertedButtonsEvent.cid list boundary value processing: trigger simultaneously 5 or
        more pressed keys.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        set_cid_reporting_class, set_cid_reporting_response_class = self.set_cid_reporting_classes()

        number_of_button = 5
        if len(self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidListWithoutGhostKey) < number_of_button:
            # Virtual buttons are ignored for now
            cid_list_d = [HexList(cid_info[:4]) for cid_info in
                          self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                          if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.DIVERT_FLAG) == CidInfoFlags.DIVERT_FLAG and
                          (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]
        else:
            cid_list_d = [HexList.fromHexList(cid) for cid in
                          self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidListWithoutGhostKey]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over 5 CID values in valid range but with divert capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_d in cid_list_d[:number_of_button]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setCidReporting request with CID = {cid_d} and set divert = '
                                     '1, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=True,
                                                        divert=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same '
                                      'as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send simultaneously CID1 to CID5 key pressed stimuli to DUT')
        # --------------------------------------------------------------------------------------------------------------
        cid_list_d_int = [CID_TO_KEY_ID_MAP[cid_d.toLong()] for cid_d in cid_list_d[:number_of_button]]
        self.button_stimuli_emulator.multiple_keys_press(cid_list_d_int)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate received divertedButtonsEvent make that should have 4 of '
                                  'the 5 CIDs in one or more packets')
        # --------------------------------------------------------------------------------------------------------------
        expected_data_received = False
        while not expected_data_received:
            diverted_buttons_event = ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=self.special_keys_and_mouse_buttons_feature.diverted_buttons_event_cls)
            if diverted_buttons_event.ctrl_id_1 != HexList(Numeral(0, 2)) and \
               diverted_buttons_event.ctrl_id_2 != HexList(Numeral(0, 2)) and \
               diverted_buttons_event.ctrl_id_3 != HexList(Numeral(0, 2)) and \
               diverted_buttons_event.ctrl_id_4 != HexList(Numeral(0, 2)):
                expected_data_received = True
            # end if
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send simultaneously CID1 to CID5 key released stimuli to DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(cid_list_d_int)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate received divertedButtonsEvent break that should have no CID '
                                  'in one or more packets')
        # --------------------------------------------------------------------------------------------------------------
        expected_data_received = False
        while not expected_data_received:
            diverted_buttons_event = ChannelUtils.get_only(
                test_case=self,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=self.special_keys_and_mouse_buttons_feature.diverted_buttons_event_cls)
            if diverted_buttons_event.ctrl_id_1 == HexList(Numeral(0, 2)) and \
               diverted_buttons_event.ctrl_id_2 == HexList(Numeral(0, 2)) and \
               diverted_buttons_event.ctrl_id_3 == HexList(Numeral(0, 2)) and \
               diverted_buttons_event.ctrl_id_4 == HexList(Numeral(0, 2)):
                expected_data_received = True
            # end if
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over 5 CID values in valid range but with divert capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_d in cid_list_d[:number_of_button]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setCidReporting request with CID = {cid_d} and set divert = '
                                     '0, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=True,
                                                        divert=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same '
                                      'as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_diverted_button_event_5_buttons

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED, 5)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_diverted_button_event_5_buttons)
    def test_set_cid_reporting_diverted_button_event_5_buttons_limited(self):
        # See ``_set_cid_reporting_diverted_button_event_5_buttons``
        self._set_cid_reporting_diverted_button_event_5_buttons()
        self.testCaseChecked("ROB_1B04_0013#limited")
    # end def test_set_cid_reporting_diverted_button_event_5_buttons_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL, 5)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_diverted_button_event_5_buttons)
    def test_set_cid_reporting_diverted_button_event_5_buttons_full(self):
        # See ``_set_cid_reporting_diverted_button_event_5_buttons``
        self._set_cid_reporting_diverted_button_event_5_buttons()
        self.testCaseChecked("ROB_1B04_0013#full")
    # end def test_set_cid_reporting_diverted_button_event_5_buttons_full

    def _set_cid_reporting_raw_xy_integrity_while_button_pressed(self):
        """
        Validate the  divertedRawMouseXYEvent.dx and dy processing: Configuration changes such as diverting or
        undiverting a pressed button does not affect the X/Y data until the diverted button is released.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        set_cid_reporting_class = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls
        set_cid_reporting_response_class = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls

        self.assertTrue(expr=set_cid_reporting_class is not None,
                        msg="Could not know which version is supported")

        # Virtual buttons are ignored for now
        cid_list_r = [HexList(cid_info[:4]) for cid_info in
                      self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                      if (int(cid_info[8:10]+cid_info[16:18], 16) &
                          (CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG)) ==
                      (CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG) and
                      (int(cid_info[8:10]+'00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with rawXY capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_r in cid_list_r:
            if int(Numeral(cid_r)) == CidTable.LEFT_CLICK:
                # Workaround for the CID = 0x0050 'Left Arrow' defined in the NRF52 platform configuration
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set divert = '
                                     '1, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 2, and check 1 and 2
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set rawXY = 1, '
                                     'rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        raw_xy_valid=True,
                                                        raw_xy=True)
            # This function do test step 4 to 8, and check 3 to 8
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=[SpecialKeysMseButtonsTestUtils.StimulusMask.POSITIVE_XY_MOVEMENT_MASK,
                              SpecialKeysMseButtonsTestUtils.StimulusMask.RRD,
                              SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_PXYRHPP_RRD])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set divert = '
                                     '0, dvalid = 1, rawXY = 0, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        divert_valid=True,
                                                        divert=False,
                                                        raw_xy_valid=True,
                                                        raw_xy=False)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same '
                                      'as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_raw_xy_integrity_while_button_pressed

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlags', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG)
    @level('Robustness')
    @services('OpticalSensor')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_raw_xy_integrity_while_button_pressed)
    def test_set_cid_reporting_raw_xy_integrity_while_button_pressed_limited(self):
        # See ``_set_cid_reporting_raw_xy_integrity_while_button_pressed``
        self._set_cid_reporting_raw_xy_integrity_while_button_pressed()
        self.testCaseChecked("ROB_1B04_0014#limited")
    # end def test_set_cid_reporting_raw_xy_integrity_while_button_pressed_limited

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlags', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG, CidEmulation.FULL)
    @level('Robustness')
    @services('OpticalSensor')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_raw_xy_integrity_while_button_pressed)
    def test_set_cid_reporting_raw_xy_integrity_while_button_pressed_full(self):
        # See ``_set_cid_reporting_raw_xy_integrity_while_button_pressed``
        self._set_cid_reporting_raw_xy_integrity_while_button_pressed()
        self.testCaseChecked("ROB_1B04_0014#full")
    # end def test_set_cid_reporting_raw_xy_integrity_while_button_pressed_full

    def _set_cid_reporting_analytics_key_event_integrity_while_button_pressed(self):
        """
        Validate the analyticsKeyEvents.cid list processing: Configuration changes such as diverting or undiverting a
        pressed button does not affect this list until the diverted button is released

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Virtual and Host Switch buttons are ignored for now
        cid_list_a = []
        for cid_info_raw_data in self.emu_cid_info_list:
            cid_info = CidInfoPayload.fromHexList(HexList(cid_info_raw_data))
            if cid_info.additional_flags.analytics_key_events and not cid_info.flags.virtual and Numeral(
                    cid_info.cid) not in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2, CidTable.HOST_SWITCH_3]:
                cid_list_a.append(cid_info.cid)
            # end if
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Choose CID1 = {cid_list_a[0]} and CID2 = {cid_list_a[1]}  from the '
                                 f'list of CIDs with analyticsKeyEvt capability')
        # --------------------------------------------------------------------------------------------------------------
        cid_1 = cid_list_a[0]
        cid_2 = cid_list_a[1]

        # This function do test step 2, and check 1
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_1,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_2} and set '
                                 'analyticsKeyEvt = 1, avalid = 1 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_id,
            ctrl_id=cid_2,
            analytics_key_event_valid=True,
            analytics_key_event=True)
        # This function do test step 4 and 5, and check 2 to 4
        SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            request=set_cid_reporting,
            response_class=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls,
            stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
            combined_cid=cid_1 if DeviceBaseTestUtils.ButtonHelper.is_consumer_cid([cid_1, cid_2]) else None)
        # This function do test step 6, and check 5
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_1,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRH)
        # This function do test step 7 and 8, and check 6 and 7
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_2,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRA_RRA)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_2} and set '
                                 f'analyticsKeyEvt = 0, avalid = 1 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_id,
            ctrl_id=cid_2,
            analytics_key_event_valid=True,
            analytics_key_event=False)
        set_cid_reporting_response = ChannelUtils.send(
            test_case=self,
            report=set_cid_reporting,
            response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as '
                                  'inputs')
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.check_response_expected_field(
            self, set_cid_reporting, set_cid_reporting_response)
    # end def _set_cid_reporting_analytics_key_event_integrity_while_button_pressed

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.LIMITED, 2)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_key_event_integrity_while_button_pressed)
    def test_set_cid_reporting_analytics_key_event_integrity_while_button_pressed_limited(self):
        # See ``_set_cid_reporting_analytics_key_event_integrity_while_button_pressed``
        self._set_cid_reporting_analytics_key_event_integrity_while_button_pressed()
        self.testCaseChecked("ROB_1B04_0015#limited")
    # end def test_set_cid_reporting_analytics_key_event_integrity_while_button_pressed_limited

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.FULL, 2)
    @level('Robustness')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_key_event_integrity_while_button_pressed)
    def test_set_cid_reporting_analytics_key_event_integrity_while_button_pressed_full(self):
        # See ``_set_cid_reporting_analytics_key_event_integrity_while_button_pressed``
        self._set_cid_reporting_analytics_key_event_integrity_while_button_pressed()
        self.testCaseChecked("ROB_1B04_0015#full")
    # end def test_set_cid_reporting_analytics_key_event_integrity_while_button_pressed_full

    def _set_cid_reporting_analytics_key_event_6_buttons(self):
        """
        Validate the analyticsKeyEvents.cid list boundary value processing: trigger simultaneously 6 or more pressed
        keys supporting analytics

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        number_of_button = 6
        button_pressed_state = 1
        button_released_state = 0

        cid_list_a = []
        if len(self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidListWithoutGhostKey) < number_of_button:
            # Virtual and Host Switch buttons are ignored for now
            for cid_info_raw_data in self.emu_cid_info_list:
                cid_info = CidInfoPayload.fromHexList(HexList(cid_info_raw_data))
                if cid_info.additional_flags.analytics_key_events and not cid_info.flags.virtual and Numeral(
                        cid_info.cid) not in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2, CidTable.HOST_SWITCH_3]:
                    cid_list_a.append(cid_info.cid)
                # end if
            # end for
        else:
            cid_list_a = [HexList.fromHexList(cid) for cid in
                          self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidListWithoutGhostKey]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over 6 CID values in valid range but with analyticsKeyEvt capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_a in cid_list_a[:number_of_button]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self,
                f'Send setCidReporting request with CID = {cid_a} and set analyticsKeyEvt = 1, avalid = 1 and all '
                f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid_a,
                analytics_key_event_valid=True,
                analytics_key_event=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, 'Validate setCidReporting response parameters should be the same as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send simultaneously CID1 to CID6 key pressed stimuli to DUT')
        # --------------------------------------------------------------------------------------------------------------
        cid_list_a_int = [CID_TO_KEY_ID_MAP[cid_a.toLong()] for cid_a in cid_list_a[:number_of_button]]
        self.button_stimuli_emulator.multiple_keys_press(cid_list_a_int, delay=.01)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Hold the keys pressed for a few ms')
        # --------------------------------------------------------------------------------------------------------------
        sleep(0.5)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send simultaneously CID1 to CID5 key released stimuli to DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.multiple_keys_release(cid_list_a_int, delay=.01)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Validate received analyticsKeyEvents that should have 5 of the 6 make CIDs')
        # --------------------------------------------------------------------------------------------------------------
        analytics_key_events = ChannelUtils.get_only(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=self.special_keys_and_mouse_buttons_feature.analytics_key_event_cls)

        cids_events_received = [
            (analytics_key_events.ctrl_id_1, analytics_key_events.event_1),
            (analytics_key_events.ctrl_id_2, analytics_key_events.event_2),
            (analytics_key_events.ctrl_id_3, analytics_key_events.event_3),
            (analytics_key_events.ctrl_id_4, analytics_key_events.event_4),
            (analytics_key_events.ctrl_id_5, analytics_key_events.event_5),
        ]

        number_of_events_reported = len([cid for cid, _ in cids_events_received if int(Numeral(cid)) != 0])
        self.assertEqual(5, number_of_events_reported, "analyticsKeyEvents should report 5 of the 6 make CIDs")

        for cid, event in cids_events_received:
            self.assertIn(cid, cid_list_a, "CID should correspond to one of the key pressed")
            self.assertEqual(button_pressed_state, int(Numeral(event)), "Event should be a button pressed")
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(
            self, 'Validate received analyticsKeyEvents that should have 5 of the 6 break CIDs in one or more packets')
        # --------------------------------------------------------------------------------------------------------------
        analytics_key_events = ChannelUtils.get_only(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.EVENT,
            class_type=self.special_keys_and_mouse_buttons_feature.analytics_key_event_cls)
        cids_events_received = [
            (analytics_key_events.ctrl_id_1, analytics_key_events.event_1),
            (analytics_key_events.ctrl_id_2, analytics_key_events.event_2),
            (analytics_key_events.ctrl_id_3, analytics_key_events.event_3),
            (analytics_key_events.ctrl_id_4, analytics_key_events.event_4),
            (analytics_key_events.ctrl_id_5, analytics_key_events.event_5),
        ]

        number_of_events_reported = len([cid for cid, _ in cids_events_received if int(Numeral(cid)) != 0])
        self.assertEqual(5, number_of_events_reported, "analyticsKeyEvents should report 5 of the 6 break CIDs")

        for cid, event in cids_events_received:
            self.assertIn(cid, cid_list_a, "CID should correspond to one of the key released")
            self.assertEqual(button_released_state, int(Numeral(event)), "Event should be a button released")
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(
            self, 'Test Loop over 6 CID values in valid range but with analyticsKeyEvt capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_a in cid_list_a[:number_of_button]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self,
                f'Send setCidReporting request with CID = {cid_a} and set analyticsKeyEvt = 0, avalid = 1 and all '
                f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid_a,
                analytics_key_event_valid=True,
                analytics_key_event=False)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(
                self, 'Validate setCidReporting response parameters should be the same as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_analytics_key_event_6_buttons

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.LIMITED, 6)
    @level('Robustness')
    @services('PassiveHoldPress')
    @bugtracker('AnalyticsKeyEvents_CID_Packing')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_key_event_6_buttons)
    def test_set_cid_reporting_analytics_key_event_6_buttons_limited(self):
        # See ``_set_cid_reporting_analytics_key_event_6_buttons``
        self._set_cid_reporting_analytics_key_event_6_buttons()
        self.testCaseChecked("ROB_1B04_0016#limited")
    # end def test_set_cid_reporting_analytics_key_event_6_buttons_limited

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.FULL, 6)
    @level('Robustness')
    @services('PassiveHoldPress')
    @bugtracker('AnalyticsKeyEvents_CID_Packing')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_key_event_6_buttons)
    def test_set_cid_reporting_analytics_key_event_6_buttons_full(self):
        # See ``_set_cid_reporting_analytics_key_event_6_buttons``
        self._set_cid_reporting_analytics_key_event_6_buttons()
        self.testCaseChecked("ROB_1B04_0016#full")
    # end def test_set_cid_reporting_analytics_key_event_6_buttons_full

    def _divert_5buttons_make_and_break(self, break_down):
        """
        This function is to regroup ROT_1B04_0010 and ROT_1B04_0011 because those two tests have a lot of common areas.

        :param break_down: Breaks are sent down (cid5 to cid1) if true. Otherwise Breaks are sent up (cid1 to cid5).
        :type break_down: ``bool``
        """
        # Get the supported version
        set_cid_reporting_class, set_cid_reporting_response_class = self.set_cid_reporting_classes()

        number_of_button = 5
        cid_list_d = []
        if len(self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidListWithoutGhostKey) < number_of_button:
            # Virtual and Host Switch buttons are ignored for now
            for cid_info_raw_data in self.emu_cid_info_list:
                cid_info = CidInfoPayload.fromHexList(HexList(cid_info_raw_data))
                if cid_info.flags.divert and not cid_info.flags.virtual and Numeral(
                        cid_info.cid) not in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2, CidTable.HOST_SWITCH_3]:
                    cid_list_d.append(cid_info.cid)
                # end if
            # end for
        else:
            cid_list_d = [HexList.fromHexList(cid) for cid in
                          self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidListWithoutGhostKey]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over 5 CID values in valid range but with divert capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_d in cid_list_d[:number_of_button]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d} and set divert ='
                                     f' 1, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=True,
                                                        divert=True)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same '
                                      'as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        expected_cid_list = [HexList(Numeral(0, 2))]*number_of_button
        # This loop do test step 2 to 5, and check 2 to 5
        for index in range(number_of_button-1):
            expected_cid_list[index] = cid_list_d[index]
            SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                ctrl_id=cid_list_d[index],
                stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD,
                press_expected_list_in_event=expected_cid_list[:-1])
        # end for

        try:
            # This loop do test step 6, and check 6
            SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                ctrl_id=cid_list_d[number_of_button-1],
                stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD)
        except (AssertionError, QueueEmpty):
            # Expect not to received divert event due to 4 divert keys had been pressed.
            # https://docs.google.com/spreadsheets/d/1-NbLmKcVQyQ5L576pe5u9BT5iVFYzbCOgSWf1NAjUtM/edit#gid=1&range=A39
            pass
        # end try

        if break_down:
            # noinspection PyBroadException
            try:
                # This loop do test step 7, and check 7
                SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                    test_case=self,
                    feature=self.special_keys_and_mouse_buttons_feature,
                    ctrl_id=cid_list_d[number_of_button-1],
                    stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRD)
            except Exception:
                # Expect not to received divert event due to 4 divert keys had been pressed.
                # https://docs.google.com/spreadsheets/d/1-NbLmKcVQyQ5L576pe5u9BT5iVFYzbCOgSWf1NAjUtM/edit#gid=1&range=A39
                pass
            # end try

            # This loop do test step 8 to 11, and check 8 to 11
            for index in range(number_of_button-2, -1, -1):
                expected_cid_list[index] = HexList(Numeral(0, 2))
                SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                    test_case=self,
                    feature=self.special_keys_and_mouse_buttons_feature,
                    ctrl_id=cid_list_d[index],
                    stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRD,
                    release_expected_list_in_event=expected_cid_list[:-1])
            # end for
        else:
            # This loop do test step 7 to 10, and check 7 to 10
            for index in range(number_of_button-1):
                del(expected_cid_list[0])
                if index == 0:
                    # Release any diverted key, then the 5th pressed key should be filled
                    expected_cid_list.insert(number_of_button-2, cid_list_d[number_of_button-1])
                else:
                    expected_cid_list.append(HexList(Numeral(0, 2)))
                # end if
                SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                    test_case=self,
                    feature=self.special_keys_and_mouse_buttons_feature,
                    ctrl_id=cid_list_d[index],
                    stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRD,
                    release_expected_list_in_event=expected_cid_list[:-1])
            # end for

            del(expected_cid_list[0])
            expected_cid_list.append(HexList(Numeral(0, 2)))
            try:
                # This loop do test step 11, and check 11
                SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                    test_case=self,
                    feature=self.special_keys_and_mouse_buttons_feature,
                    ctrl_id=cid_list_d[number_of_button-1],
                    stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.RRD)
            except (AssertionError, QueueEmpty):
                # Expect not to received divert event due to 4 divert keys had been pressed.
                # https://docs.google.com/spreadsheets/d/1-NbLmKcVQyQ5L576pe5u9BT5iVFYzbCOgSWf1NAjUtM/edit#gid=1&range=A40
                pass
            # end try
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over 5 CID values in valid range but with divert capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_d in cid_list_d[:number_of_button]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d} and set divert ='
                                     f' 0, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=True,
                                                        divert=False)
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=set_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same '
                                      'as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, set_cid_reporting, set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _divert_5buttons_make_and_break
# end class SpecialKeysMSEButtonsRobustnessEmuTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
