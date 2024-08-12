#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.business
:brief: HID++ 2.0 Special Keys MSE Buttons business test suite
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/05/14
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique

from pyharness.extensions import level
from pyharness.selector import bugtracker
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfoV0Response
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.emulator.emulatorinterfaces import BREAK
from pylibrary.emulator.emulatorinterfaces import KEYSTROKE
from pylibrary.emulator.emulatorinterfaces import MAKE
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.emulator.keyid import ModifierKeys
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.cidutils import CidEmulation
from pytestbox.base.cidutils import CidInfoConfig
from pytestbox.base.cidutils import CidInfoFlags
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.device.hidpp20.common.feature_1b04.specialkeysmsebuttons import SpecialKeysMSEButtonsTestCase
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMSEButtonsBusinessTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the keyboard reprogrammable keys and mouse buttons business test cases.
    """
    @features('Feature1B04')
    @level('Business')
    def test_get_cid_info_business_case(self):
        """
        Validate the GetCidInfo business case : check all CIDs entries versus product specification.

        v0
            ctrlID, taskID, flags, fkeyPos =  [1]GetCtrlIDInfo(ctrlIDIndex)
        v1
            [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask
        v2 ~ v5
            [1] getCidInfo(index) -> cid, tid, flags, pos, group, gmask, additionalflags
        """
        # Get the supported version
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getCidInfo request with index = ' + str(index))
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate getCidInfo response according to product specification')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info_expected_response_hex = HexList(
                '00' * HidppMessage.HEADER_SIZE,
                self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)[index])
            get_cid_info_expected_response_hex.addPadding(size=HidppMessage.LONG_MSG_SIZE,
                                                          fromLeft=False)
            get_cid_info_expected_response = get_cid_info_response_class.fromHexList(get_cid_info_expected_response_hex)

            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, get_cid_info_expected_response, get_cid_info_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B04_0001")
    # end def test_get_cid_info_business_case

    @features('Feature1B04')
    @level('Business', 'SmokeTests')
    def test_get_cid_reporting_business_case(self):
        """
        Validate the GetCidReporting business case : check all of the flags in each CID as expected defines to
        product specification.

        v0
            ctrlID, controlIDReporting = [2]GetCtrlIDReporting(ctrlID)
        v1
            [2] getCidReporting(cid) -> cid, divert, persist, remap
        v2
            [2] getCidReporting(cid) -> cid, divert, persist, rawXY, remap
        v3
            [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap
        v4
            [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt
        v5
            [2] getCidReporting(cid) -> cid, divert, persist, forceRawXY, rawXY, remap, analyticsKeyEvt, rawWheel
        """
        # Get the supported version
        get_cid_info_response_class = self.get_cid_info_response_class()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo request with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id}')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting = self.special_keys_and_mouse_buttons_feature.get_cid_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=get_cid_info_response.ctrl_id)
            get_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate getCidReporting response according to product '
                                      'specification')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting_expected_response_hex = HexList('00' * HidppMessage.HEADER_SIZE,
                                                              get_cid_info_response.ctrl_id)
            get_cid_reporting_expected_response_hex.addPadding(size=HidppMessage.LONG_MSG_SIZE,
                                                               fromLeft=False)
            get_cid_reporting_expected_response = get_cid_reporting_response_class.fromHexList(
                get_cid_reporting_expected_response_hex)

            # The remap field can be equal to 0 or its own CID and be acceptable
            if not self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_0 and \
                    get_cid_reporting_response.remap == get_cid_reporting_response.ctrl_id:
                get_cid_reporting_expected_response.remap = get_cid_reporting_response.ctrl_id
            # end if

            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, get_cid_reporting_expected_response, get_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B04_0002")
    # end def test_get_cid_reporting_business_case
# end class SpecialKeysMSEButtonsBusinessTestCase


class SpecialKeysMSEButtonsBusinessEmuTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the keyboard reprogrammable keys and mouse buttons business test cases.
    """

    @unique
    class ReportType(IntEnum):
        """
        Define the report type of 0x1b04
        """
        DIVERT = auto()
        REMAP = auto()
        HID = auto()
    # end class ReportType

    def _set_cid_reporting_divert_business_case(self):
        """
        Validate the divert keys for each CID by SetCidReporting.

        v0
            ctrlID, controlIDReporting =  [3]SetCtrlIDReporting(ctrlID, controlIDReporting)
            ctrlIDIndexPressedList   =  [0]ControlIDBroadcastEvent()
        v1
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, remap
        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        v1 ~ v5
            [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value and '
                                     f'verify it has divert capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if not isinstance(get_cid_info_response, GetCidInfoV0Response) and get_cid_info_response.virtual:
                # Virtual buttons are ignored for now
                continue
            # end if

            # Ignore Host Switch buttons
            if Numeral(get_cid_info_response.ctrl_id) in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2,
                                                          CidTable.HOST_SWITCH_3]:
                continue
            # end if

            # This test is only for keys with divert capability
            if not get_cid_info_response.divert:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} does not have divert '
                                         f'capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if self.f.PRODUCT.F_IsPlatform and not get_cid_info_response.mouse:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} is not emulated '
                                         f'on the DEV board yet')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 1, dvalid = 1 '
                                     f'and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 3 and 4, and check 1 to 3
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 0, dvalid = 1 and'
                                     f' all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 6 and 7, and check 4 to 6
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_divert_business_case

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('PassiveHoldPress')
    @bugtracker("DivertOnPress")
    @DocUtils.copy_doc(_set_cid_reporting_divert_business_case)
    def test_set_cid_reporting_divert_business_case_limited(self):
        # See ``_set_cid_reporting_divert_business_case``
        self._set_cid_reporting_divert_business_case()
        self.testCaseChecked("BUS_1B04_0003#limited")
    # end def test_set_cid_reporting_divert_business_case_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('PassiveHoldPress')
    @bugtracker("DivertOnPress")
    @DocUtils.copy_doc(_set_cid_reporting_divert_business_case)
    def test_set_cid_reporting_divert_business_case_full(self):
        # See ``_set_cid_reporting_divert_business_case``
        self._set_cid_reporting_divert_business_case()
        self.testCaseChecked("BUS_1B04_0003#full")
    # end def test_set_cid_reporting_divert_business_case_full

    def _set_cid_reporting_persist_business_case(self):
        """
        Validate the persist keys for each CID by SetCidReporting.

        v0
            ctrlID, controlIDReporting =  [3]SetCtrlIDReporting(ctrlID, controlIDReporting)
            ctrlIDIndexPressedList   =  [0]ControlIDBroadcastEvent()
        v1
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, remap
        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        v1 ~ v5
            [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value and '
                                     f'verify it has persist capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if not isinstance(get_cid_info_response, GetCidInfoV0Response) and get_cid_info_response.virtual:
                # Virtual buttons are ignored for now
                continue
            # end if

            if not get_cid_info_response.persist:
                # This test is only for keys with persist capability
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} does not have persist '
                                         f'capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 1, dvalid = 1, '
                                     f'persist = 1, pvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        persist_valid=True,
                                                        persist=True,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 3 to 8 and check 1 to 5
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event_power_reset(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask_before=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD,
                stimuli_mask_after=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 0, dvalid = 1, '
                                     f'persist = 0, pvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        persist_valid=True,
                                                        persist=False,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 10 and 11, and check 6 to 8
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_persist_business_case

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('HardwareReset')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_persist_business_case)
    def test_set_cid_reporting_persist_business_case_limited(self):
        # See ``_set_cid_reporting_persist_business_case``
        self._set_cid_reporting_persist_business_case()
        self.testCaseChecked("BUS_1B04_0004#limited")
    # end def test_set_cid_reporting_persist_business_case_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('HardwareReset')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_persist_business_case)
    def test_set_cid_reporting_persist_business_case_full(self):
        # See ``_set_cid_reporting_persist_business_case``
        self._set_cid_reporting_persist_business_case()
        self.testCaseChecked("BUS_1B04_0004#full")
    # end def test_set_cid_reporting_persist_business_case_full

    def _set_cid_reporting_raw_xy_business_case(self):
        """
        Validate the rawXY for each CID by SetCidReporting.

        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        v1 ~ v5
            [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
        v2 ~ v5
            [event1] divertedRawMouseXYEvent -> dx, dy
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getCidInfo with index = {index} to get CID value and verify it has '
                           f'rawXY capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if get_cid_info_response.virtual:
                # Virtual buttons are ignored for now
                continue
            # end if

            if not get_cid_info_response.raw_xy:
                # This test is only for keys with rawXY capability
                # ------------------------------------------------------------------------------------------------------
                self.logTrace('CID = ' + str(get_cid_info_response.ctrl_id) + ' does not have rawXY capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace(f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(get_cid_info_response.ctrl_id)) == CidTable.LEFT_CLICK:
                # Workaround for the CID = 0x0050 'Left Arrow' defined in the NRF52 platform configuration
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 1, dvalid = 1, rawyXY = 1, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        raw_xy_valid=True,
                                                        raw_xy=True,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 3 to 5, and check 1 to 4
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_PXYRHPP_RRD)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 6: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 0, dvalid = 1, rawyXY = 1, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        raw_xy_valid=True,
                                                        raw_xy=True,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 7 to 9, and check 5 to 8
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_PXYRH_RRH)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 10: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 0, dvalid = 1, rawyXY = 0, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        raw_xy_valid=True,
                                                        raw_xy=False,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 11 to 13, and check 9 to 12
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_PXYRH_RRH)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_raw_xy_business_case

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.RAW_XY_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('OpticalSensor')
    @DocUtils.copy_doc(_set_cid_reporting_raw_xy_business_case)
    def test_set_cid_reporting_raw_xy_business_case_limited(self):
        # See ``_set_cid_reporting_raw_xy_business_case``
        self._set_cid_reporting_raw_xy_business_case()
        self.testCaseChecked("BUS_1B04_0005#limited")
    # end def test_set_cid_reporting_raw_xy_business_case_limited

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.RAW_XY_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('OpticalSensor')
    @DocUtils.copy_doc(_set_cid_reporting_raw_xy_business_case)
    def test_set_cid_reporting_raw_xy_business_case_full(self):
        # See ``_set_cid_reporting_raw_xy_business_case``
        self._set_cid_reporting_raw_xy_business_case()
        self.testCaseChecked("BUS_1B04_0005#full")
    # end def test_set_cid_reporting_raw_xy_business_case_full

    @features('Feature1B04V3+')
    @features('Feature1B04WithFlags', CidInfoFlags.FORCE_RAW_XY_FLAG)
    @level('Business')
    @services('OpticalSensor')
    def test_set_cid_reporting_force_raw_xy_business_case(self):
        """
        Validate the forceRawXY for each CID by SetCidReporting.

        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        v2 ~ v5
            [event1] divertedRawMouseXYEvent -> dx, dy
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Send getCidInfo with index = {index} to get CID value and verify it has '
                           f'forceRawXY capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # This test is only for keys with force_raw_xy capability
            if not get_cid_info_response.force_raw_xy:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace('CID = ' + str(get_cid_info_response.ctrl_id) + ' does not have forceRawXY capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 2: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 1, dvalid = 1, rawXY = 1, rvalid = 1, forceRawXY = 1, fvalid = 1 and all '
                           f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=True,
                                                        raw_xy_valid=True,
                                                        raw_xy=True,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 3, and check 1 and 2
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PXYRHPP)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 4: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 1, dvalid = 1, rawXY = 0, rvalid = 1, forceRawXY = 1, fvalid = 1 and all '
                           f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=True,
                                                        raw_xy_valid=True,
                                                        raw_xy=False,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 5, and check 3 and 4
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PXYRH)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 6: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 0, dvalid = 1, rawXY = 1, rvalid = 1, forceRawXY = 1, fvalid = 1 and all '
                           f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=True,
                                                        raw_xy_valid=True,
                                                        raw_xy=True,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 7, and check 5 and 6
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PXYRH)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 8: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and '
                           f'set divert = 0, dvalid = 1, rawXY = 0, rvalid = 1, forceRawXY = 1, fvalid = 1 and all '
                           f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=True,
                                                        raw_xy_valid=True,
                                                        raw_xy=False,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 9, and check 7 and 8
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PXYRH)

            # ----------------------------------------------------------------------------------------------------------
            self.logTitle2(f'Test Step 10: Send setCidReporting request with CID = {get_cid_info_response.ctrl_id}and '
                           f'set divert = 0, dvalid = 1, rawXY = 0, rvalid = 1, forceRawXY = 0, fvalid = 1 and all '
                           f'other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=False,
                                                        raw_xy_valid=True,
                                                        raw_xy=False,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 11, and check 9 and 10
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PXYRH)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B04_0006")
    # end def test_set_cid_reporting_force_raw_xy_business_case

    def _set_cid_reporting_analytics_key_evt_business_case(self):
        """
        Validate the analyticsKeyEvt for each CID by setCidReporting.

        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        v1 ~ v5
            [event0] divertedButtonsEvent -> cid1, cid2, cid3, cid4
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value and verify'
                                     f' it has analyticsKeyEvt capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if get_cid_info_response.virtual:
                # Virtual buttons are ignored for now
                continue
            # end if

            # Ignore Host Switch buttons
            if Numeral(get_cid_info_response.ctrl_id) in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2,
                                                          CidTable.HOST_SWITCH_3]:
                continue
            # end if

            # This test is only for keys with analyticsKeyEvt capability
            if not get_cid_info_response.analytics_key_events:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace('CID = ' + str(get_cid_info_response.ctrl_id) + ' does not have analyticsKeyEvt '
                                                                              'capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace(f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            additional_fn_lock_mask = 0
            if int(Numeral(get_cid_info_response.ctrl_id)) == CidTable.FN_LOCK and \
                    self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled:
                additional_fn_lock_mask = SpecialKeysMseButtonsTestUtils.StimulusMask.FN_LOCK_MASK
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set analyticsKeyEvt = 1, '
                                     f'avalid = 1 all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=True)
            # This function do test step 3 and 4, and check 1 to 3
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRA_RRA | additional_fn_lock_mask)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and set '
                      f'analyticsKeyEvt = 0, avalid = 1 all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=False)
            # This function do test step 6 and 7, and check 4 to 6
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH | additional_fn_lock_mask)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_analytics_key_evt_business_case

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_key_evt_business_case)
    def test_set_cid_reporting_analytics_key_evt_business_case_limited(self):
        # See ``_set_cid_reporting_analytics_key_evt_business_case``
        self._set_cid_reporting_analytics_key_evt_business_case()
        self.testCaseChecked("BUS_1B04_0007#limited")
    # end def test_set_cid_reporting_analytics_key_evt_business_case_limited

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_key_evt_business_case)
    def test_set_cid_reporting_analytics_key_evt_business_case_full(self):
        # See ``_set_cid_reporting_analytics_key_evt_business_case``
        self._set_cid_reporting_analytics_key_evt_business_case()
        self.testCaseChecked("BUS_1B04_0007#full")
    # end def test_set_cid_reporting_analytics_key_evt_business_case_full

    def _set_cid_reporting_remap_business_case(self):
        """
        Validate the remap for each Cids by setCidReporting.

        v1
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, remap) -> cid, divert, dvalid, persist, pvalid,
                                                                                remap
        v2
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, rawXY, rvalid, remap) -> cid, divert, dvalid,
                                                                                                persist, pvalid, rawXY,
                                                                                                rvalid, remap
        v3
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap)
                                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap
        v4
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap, avalid,
                                analyticsKeyEvt) -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY,
                                                    rvalid, remap, analyticsKeyEvt
        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getCidInfo with index = 0..getCount()-1 to collect cid, group, '
                                 'gmask in a list')
        # --------------------------------------------------------------------------------------------------------------
        cid_count = SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                 self.special_keys_and_mouse_buttons_feature,
                                                                 self.feature_id)
        cid_group_gmask_list = []
        for index in range(cid_count):
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if get_cid_info_response.virtual:
                # Virtual buttons are ignored for now
                continue
            # end if

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace(f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            cid_group_gmask_list.append((get_cid_info_response.ctrl_id,
                                         get_cid_info_response.group,
                                         get_cid_info_response.gmask))
        # end for

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID, group, gmask in the list')
        # --------------------------------------------------------------------------------------------------------------
        for (cid, group, gmask) in cid_group_gmask_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over all possible remapped CIDs of CID = ' + str(cid))
            # ----------------------------------------------------------------------------------------------------------
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask):
                    continue
                # end if

                group_mask = 1 << (other_group.toLong() - 1) if other_group.toLong() != 0 else 0

                if (gmask.toLong() & group_mask) != 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'remap = {other_cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=other_cid)
                    # This function do test step 3 and 4, and check 1 to 3
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
                        remapped_cid=other_cid)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'remap = {cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=cid)
                    # This function do test step 6 and 7, and check 4 to 6
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop end')
            # ----------------------------------------------------------------------------------------------------------
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_remap_business_case

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Business')
    @DocUtils.copy_doc(_set_cid_reporting_remap_business_case)
    def test_set_cid_reporting_remap_business_case_limited(self):
        # See ``_set_cid_reporting_remap_business_case``
        self._set_cid_reporting_remap_business_case()
        self.testCaseChecked("BUS_1B04_0008#limited")
    # end def test_set_cid_reporting_remap_business_case_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @level('Business')
    @DocUtils.copy_doc(_set_cid_reporting_remap_business_case)
    def test_set_cid_reporting_remap_business_case_full(self):
        # See ``_set_cid_reporting_remap_business_case``
        self._set_cid_reporting_remap_business_case()
        self.testCaseChecked("BUS_1B04_0008#full")
    # end def test_set_cid_reporting_remap_business_case_full

    @features('Feature1B04V5+')
    @features('Feature1B04WithFlags', CidInfoFlags.RAW_WHEEL_FLAG)
    @level('Business')
    @services('MainWheel')
    def test_set_cid_reporting_raw_wheel_business_case(self):
        """
        Validate the rawWheel for each CID by SetCidReporting.

        v5
            [3] setCidReporting(cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                                avalid, analyticsKeyEvt, wvalid, rawWheel)
                    -> cid, divert, dvalid, persist, pvalid, forceRawXY, fvalid, rawXY, rvalid, remap,
                    avalid, analyticsKeyEvt, wvalid, rawWheel
        v2 ~ v5
            [event4] divertedRawWheelEvent -> resolution, periods, deltaV
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value and verify '
                                     f'it has forceRawXY capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # This test is only for keys with raw wheel capability
            if not get_cid_info_response.raw_wheel:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} does not have '
                                         f'rawWheel capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 1, dvalid = 1, '
                                     f'rawWheel = 1, wvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        raw_wheel_valid=True,
                                                        raw_wheel=True,
                                                        divert_valid=True,
                                                        divert=True)
            # This function do test step 3, and check 1 and 2
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PWHLRHPP)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and set divert = 0, '
                      f'dvalid = 1, rawWheel = 1, wvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        raw_wheel_valid=True,
                                                        raw_wheel=True,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 5, and check 3 and 4
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PWHLRH)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send setCidReporting request with CID = {get_cid_info_response.ctrl_id} and set divert = 0, '
                      f'dvalid = 1, rawWheel = 0, wvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        raw_wheel_valid=True,
                                                        raw_wheel=False,
                                                        divert_valid=True,
                                                        divert=False)
            # This function do test step 7, and check 5 and 6
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PWHLRH)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_1B04_0009")
    # end def test_set_cid_reporting_raw_wheel_business_case

    def _set_cid_reporting_to_divert_or_remap_and_validate(self, expected_report):
        """
        Validate the diverted or remapped keys for each CID by SetCidReporting. If expected_report is ReportType.HID,
        then it doesn't invoke setCidReporting API, only keystroke and check if we can receive expected report

        :param expected_report: The expected report type of stimulus
        :type expected_report: ``ReportType``
        """
        cid_hid_list = []
        cid_divert_list = []
        cid_group_gmask_list = []
        cid_info_table = self.config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        # Collect target cids into cid_hid_list(HID), cid_divert_list(DIVERT) and cid_group_gmask_list(REMAP)
        for cid_info_idx in range(len(cid_info_table)):
            cid_info = CidInfoConfig.from_index(self.f, cid_info_idx, self.config_manager).cid_info_payload

            if self.f.PRODUCT.F_IsPlatform and not cid_info.flags.mouse:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {cid_info.ctrl_id} is not emulated on the DEV board yet')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(cid_info.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {cid_info.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # Virtual buttons are ignored
            if not self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_0 and \
                    cid_info.flags.virtual:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {cid_info.ctrl_id}(virtual button) is skipped')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # Ignore Host Switch buttons and FN lock
            if Numeral(cid_info.ctrl_id) in [CidTable.HOST_SWITCH_1, CidTable.HOST_SWITCH_2, CidTable.HOST_SWITCH_3,
                                             CidTable.FN_LOCK]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {cid_info.ctrl_id}(host buttons or fn lock) is skipped')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if
            cid_hid_list.append(cid_info)

            # Divert capability check
            if not cid_info.flags.divert:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {cid_info.ctrl_id} does not have divert capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if
            cid_divert_list.append(cid_info)

            # Divert capability check
            if not cid_info.flags.reprog:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {cid_info.ctrl_id} does not have remap capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if
            cid_group_gmask_list.append((cid_info.ctrl_id,
                                         cid_info.group,
                                         cid_info.gmask))
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        # Loop target list and set to divert or remap by SetCidReporting if needed and validate it
        if expected_report == self.ReportType.HID:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over cid_divert_list {[str(cid.ctrl_id) for cid in cid_hid_list]}')
            # ----------------------------------------------------------------------------------------------------------
            for cid in cid_hid_list:
                # Stimulus and verify directly without setting cid to diverted or remapped
                if expected_report == self.ReportType.HID:
                    SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        ctrl_id=cid.ctrl_id,
                        stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)
                # end if
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop end')
            # ----------------------------------------------------------------------------------------------------------
        elif expected_report == self.ReportType.DIVERT:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f'Test Loop over cid_divert_list {[str(cid.ctrl_id) for cid in cid_divert_list]}')
            # ----------------------------------------------------------------------------------------------------------
            for cid in cid_divert_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid.ctrl_id} and '
                                         'set divert = 1, dvalid = 1 and all other parameters = 0')
                # ------------------------------------------------------------------------------------------------------
                set_cid_request = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
                    device_index=ChannelUtils.get_device_index(test_case=self),
                    feature_index=self.feature_id,
                    ctrl_id=cid.ctrl_id,
                    divert_valid=True,
                    divert=True)
                SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                    test_case=self,
                    feature=self.special_keys_and_mouse_buttons_feature,
                    request=set_cid_request,
                    response_class=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls,
                    stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD)
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop end')
            # ----------------------------------------------------------------------------------------------------------
        elif expected_report == self.ReportType.REMAP:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop over cid_group_gmask_list'
                                     f'{[str(cid[0]) for cid in cid_group_gmask_list]}')
            # ----------------------------------------------------------------------------------------------------------
            for (cid, group, gmask) in cid_group_gmask_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Test Loop over all possible remapped CIDs of CID = ' + str(cid))
                # ------------------------------------------------------------------------------------------------------
                for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                    if (cid, group, gmask) == (other_cid, other_group, other_gmask):
                        continue
                    # end if

                    group_mask = 1 << (other_group.toLong() - 1) if other_group.toLong() != 0 else 0

                    if (gmask.toLong() & group_mask) != 0:
                        # ----------------------------------------------------------------------------------------------
                        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                                 f'remap = {other_cid} and all other parameters = 0')
                        # ----------------------------------------------------------------------------------------------
                        set_cid_request = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
                            device_index=ChannelUtils.get_device_index(test_case=self),
                            feature_index=self.feature_id,
                            ctrl_id=cid,
                            remap=other_cid)

                        # This function do test step 3 and 4, and check 1 to 3
                        SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                            test_case=self,
                            feature=self.special_keys_and_mouse_buttons_feature,
                            request=set_cid_request,
                            response_class=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls,
                            stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
                            remapped_cid=other_cid)
                    # end if
                # end for
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, 'Test Loop end')
                # ------------------------------------------------------------------------------------------------------
            # end for
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Test Loop end')
            # ----------------------------------------------------------------------------------------------------------
        # end if
    # end def _set_cid_reporting_to_divert_or_remap_and_validate

    @features('Feature1B04V6+')
    @features('Feature1B04resetAllCidReportSettings')
    @level('Business')
    def test_reset_all_cid_report_settings_business_case(self):
        """
        Check if resetAllCidReportSettings is able to reset all diverted or remapped settings by setCidReporting

        v6
            [5] resetAllCidReportSettings()
        """
        self._set_cid_reporting_to_divert_or_remap_and_validate(expected_report=self.ReportType.DIVERT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send resetAllCidReportSettings request')
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.HIDppHelper.reset_all_cid_report_settings(self)
        self._set_cid_reporting_to_divert_or_remap_and_validate(expected_report=self.ReportType.HID)

        self._set_cid_reporting_to_divert_or_remap_and_validate(expected_report=self.ReportType.REMAP)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send resetAllCidReportSettings request')
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.HIDppHelper.reset_all_cid_report_settings(self)
        self._set_cid_reporting_to_divert_or_remap_and_validate(expected_report=self.ReportType.HID)

        self.testCaseChecked("BUS_1B04_0010")
    # end def test_reset_all_cid_report_settings_business_case

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_dual_keys_diverted_with_fn_key_limited(self):
        """
        Regardless of fnInversionState state and if keys are diverted the device shall report the shortcut key
        (of the secondary function) to the Host OS for each Fn + dual key pressed.
        """
        self._dual_keys_reporting_business_case(set_diverted=True)
        self.testCaseChecked("BUS_1B04_0011#limited_1")
    # end def test_dual_keys_diverted_with_fn_key_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_dual_keys_diverted_with_fn_key_full(self):
        """
        Regardless of fnInversionState state and if keys are diverted the device shall report the shortcut key
        (of the secondary function) to the Host OS for each Fn + dual key pressed.
        """
        self._dual_keys_reporting_business_case(set_diverted=True)
        self.testCaseChecked("BUS_1B04_0011#full_1")
    # end def test_dual_keys_diverted_with_fn_key_full

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_dual_keys_not_diverted_with_fn_key_limited(self):
        """
        Regardless of fnInversionState state and if keys are not diverted the device shall report the shortcut key
        (of the secondary function) to the Host OS for each Fn + dual key pressed.
        """
        self._dual_keys_reporting_business_case(set_diverted=False)
        self.testCaseChecked("BUS_1B04_0011#limited_2")
    # end def test_dual_keys_not_diverted_with_fn_key_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_dual_keys_not_diverted_with_fn_key_full(self):
        """
        Regardless of fnInversionState state and if keys are not diverted the device shall report the shortcut key
        (of the secondary function) to the Host OS for each Fn + dual key pressed.
        """
        self._dual_keys_reporting_business_case(set_diverted=False)
        self.testCaseChecked("BUS_1B04_0011#full_2")
    # end def test_dual_keys_not_diverted_with_fn_key_full

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.F_KEY_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_f_keys_diverted_limited(self):
        """
        If fnInversionState is deactivated and the key are diverted, the device shall report the F key to the Host OS
        for each Fx key pressed
        """
        self._f_row_key_reporting_business_case(press_fn=False)
        self.testCaseChecked("BUS_1B04_0012#limited_1")
    # end def test_f_keys_diverted_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_f_keys_diverted_full(self):
        """
        If fnInversionState is deactivated and the key are diverted, the device shall report the F key to the Host OS
        for each Fx key pressed
        """
        self._f_row_key_reporting_business_case(press_fn=False)
        self.testCaseChecked("BUS_1B04_0012#full_1")
    # end def test_f_keys_diverted_full

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.F_KEY_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_f_keys_diverted_with_fn_key_limited(self):
        """
        If fnInversionState is activated and the key are diverted, the device shall report the F key to the Host OS for
        each Fn + Fx key pressed
        """
        self._f_row_key_reporting_business_case(press_fn=True)
        self.testCaseChecked("BUS_1B04_0012#limited_2")
    # end def test_f_keys_diverted_with_fn_key_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.F_KEY_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_f_keys_diverted_with_fn_key_full(self):
        """
        If fnInversionState is activated and the key are diverted, the device shall report the F key to the Host OS for
        each Fn + Fx key pressed
        """
        self._f_row_key_reporting_business_case(press_fn=True)
        self.testCaseChecked("BUS_1B04_0012#full_2")
    # end def test_f_keys_diverted_with_fn_key_full

    def _dual_keys_reporting_business_case(self, set_diverted=True):
        """
        Regardless of fnInversionState state and if keys are diverted or not, the device shall report the shortcut key
        (of the secondary function) to the Host OS for each Fn + dual key pressed.
        Dual key: Any other key with dual functions printed (on the F-row or the 6 pack...) except for Fx keys

        :param set_diverted: Flag indicating if the key has to be diverted or not
        :type set_diverted: ``bool``
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            primary_key_id = CID_TO_KEY_ID_MAP[int(Numeral(get_cid_info_response.ctrl_id))]
            if not get_cid_info_response.divert:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID 0x{get_cid_info_response.ctrl_id} because the corresponding key '
                                         f'{primary_key_id!s} is not divertable')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if Numeral(get_cid_info_response.fkey_pos) != 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID 0x{get_cid_info_response.ctrl_id} because the corresponding key '
                                         f'{primary_key_id!s} is not F-row key')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
            if primary_key_id not in fn_keys.values():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID 0x{get_cid_info_response.ctrl_id} because the corresponding key '
                                         f'{primary_key_id!s} is not dual printing key')
                # ------------------------------------------------------------------------------------------------------
                continue
            elif primary_key_id in ModifierKeys.ALL:
                # User can not customize modifier keys
                # cf https://drive.google.com/drive/folders/1DtUCSxiV9y-1CjP2toN43JwG_ICBUibp
                # ------------------------------------------------------------------------------------------------------
                self.log_warning(f'CID 0x{get_cid_info_response.ctrl_id} shall not be divertable: '
                                 f'{primary_key_id!s} can not be a dual printing key')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if set_diverted:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Send setCidReporting request with CID = '
                                         f'{get_cid_info_response.ctrl_id} and set divert = 1, dvalid = 1 '
                                         'and all other parameters = 0')
                # ------------------------------------------------------------------------------------------------------
                set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                            feature_index=self.feature_id,
                                                            ctrl_id=get_cid_info_response.ctrl_id,
                                                            divert_valid=True,
                                                            divert=True)
                # Set the key to diverted
                set_cid_reporting_response = ChannelUtils.send(
                    test_case=self,
                    report=set_cid_reporting,
                    response_queue_name=HIDDispatcher.QueueName.COMMON,
                    response_class_type=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
                # ------------------------------------------------------------------------------------------------------
                SpecialKeysMseButtonsTestUtils.check_response_expected_field(self, set_cid_reporting,
                                                                             set_cid_reporting_response)
            # end if

            # To get secondary key id by fn_keys dict
            secondary_key_id = [k for k, v in fn_keys.items() if v == primary_key_id][0]
            self.post_requisite_reset_fn_lock_state = True
            # Ensure that fnInversionState(on/off) doesn't affect anything
            for fn_lock_state in [False, True]:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Set FN lock to {"ON" if fn_lock_state else "OFF"} by FnLockKeyCombination')
                # ------------------------------------------------------------------------------------------------------
                fn_lock_change = KeyMatrixTestUtils.switch_fn_lock_state(self, enable=fn_lock_state)

                if fn_lock_change and self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_HasFnLock:
                    # ------------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Get fLockChange event")
                    # ------------------------------------------------------------------------------------------------------
                    FnInversionForMultiHostDevicesTestUtils.HIDppHelper.f_lock_change_event(self,
                                                                                            check_first_message=False)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Keystroke Fn + {primary_key_id!s}')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.perform_action_list(
                    action_list=[[KEY_ID.FN_KEY, MAKE], [primary_key_id, KEYSTROKE], [KEY_ID.FN_KEY, BREAK]])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check the HID keycode of secondary key {secondary_key_id!s} is received')
                # ------------------------------------------------------------------------------------------------------
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(secondary_key_id, MAKE)
                )
                KeyMatrixTestUtils.check_hid_report_by_key_id(
                    test_case=self, key=KeyMatrixTestUtils.Key(secondary_key_id, BREAK)
                )
            # end for
        # end for
    # end def _dual_keys_reporting_business_case

    def _f_row_key_reporting_business_case(self, press_fn=True):
        """
        While the F-Row keys are diverted, the device shall report the Fx keys (of the secondary function) to the Host
        OS for each Fn + Fx key pressed when fnInversionState is activated and each Fx key pressed when fnInversionState
        is deactivated

        :param press_fn: Flag indicating if pressing Fn key or not
        :type press_fn: ``bool``
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_info_response_class = self.get_cid_info_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(SpecialKeysMseButtonsTestUtils.get_cid_count(self,
                                                                        self.special_keys_and_mouse_buttons_feature,
                                                                        self.feature_id)):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = self.special_keys_and_mouse_buttons_feature.get_cid_info_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if int(Numeral(get_cid_info_response.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {get_cid_info_response.ctrl_id} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            primary_key_id = CID_TO_KEY_ID_MAP[int(Numeral(get_cid_info_response.ctrl_id))]
            if not get_cid_info_response.divert:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID 0x{get_cid_info_response.ctrl_id} because the corresponding key '
                                         f'{primary_key_id!s} is not divertable')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if Numeral(get_cid_info_response.fkey_pos) == 0:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID 0x{get_cid_info_response.ctrl_id} because the corresponding key '
                                         f'{primary_key_id!s} is F-row key')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            fn_keys = KeyMatrixTestUtils.get_fn_key_list(test_case=self)
            if primary_key_id not in fn_keys.values():
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'Skip CID 0x{get_cid_info_response.ctrl_id} because the corresponding key '
                                         f'{primary_key_id!s} is not dual printing key')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 1, dvalid = 1 '
                                     'and all other parameters = 0')
            # ------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
                                                        divert_valid=True,
                                                        divert=True)
            # Set the key to diverted
            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls)

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
            # ------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(self, set_cid_reporting,
                                                                         set_cid_reporting_response)

            # To get secondary key id by fn_keys dict
            secondary_key_id = [k for k, v in fn_keys.items() if v == primary_key_id][0]
            if press_fn:
                fn_lock_state = False
                actions = [[KEY_ID.FN_KEY, MAKE], [primary_key_id, KEYSTROKE], [KEY_ID.FN_KEY, BREAK]]
            else:
                fn_lock_state = True
                actions = [[primary_key_id, KEYSTROKE]]
            # end if

            self.post_requisite_reset_fn_lock_state = True
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set FN lock to {"ON" if fn_lock_state else "OFF"} by FnLockKeyCombination')
            # ----------------------------------------------------------------------------------------------------------
            fn_lock_change = KeyMatrixTestUtils.switch_fn_lock_state(self, enable=fn_lock_state)

            if fn_lock_change and self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_HasFnLock:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, "Get fLockChange event")
                # ------------------------------------------------------------------------------------------------------
                FnInversionForMultiHostDevicesTestUtils.HIDppHelper.f_lock_change_event(self, check_first_message=False)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Emulate {actions}')
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.perform_action_list(action_list=actions)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, f'Check the HID keycode of secondary key {secondary_key_id!s} is received')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(secondary_key_id, MAKE))
            KeyMatrixTestUtils.check_hid_report_by_key_id(
                test_case=self, key=KeyMatrixTestUtils.Key(secondary_key_id, BREAK))
        # end for
    # end def _f_row_key_reporting_business_case

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_fn_lock_all_keys_diverted_limited(self):
        """
        The Fn Lock change event shall always be received when toggling the Fn lock state, even if all divertable keys
        are set to divert (limited key set range)
        """
        self._divert_all_divertable_keys()
        self._check_only_flock_event()
        self.testCaseChecked("BUS_1B04_0013#limited")
    # end def test_fn_lock_all_keys_diverted_limited

    @features('Feature1B04')
    @features('Feature40A3')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
    @level('Business')
    @services('RequiredKeys', (KEY_ID.FN_KEY,))
    def test_fn_lock_all_keys_diverted_full(self):
        """
        The Fn Lock change event shall always be received when toggling the Fn lock state, even if all divertable keys
        are set to divert (full key set range)
        """
        self._divert_all_divertable_keys()
        self._check_only_flock_event()
        self.testCaseChecked("BUS_1B04_0013#full")
    # end def test_fn_lock_all_keys_diverted_full

    def _divert_all_divertable_keys(self):
        """
        Set all divertable keys to diverted
        """
        cid_divert_list = []
        cid_info_table = self.config_manager.get_feature(ConfigurationManager.ID.CID_TABLE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        # Collect target cid_divert_list(DIVERT)
        for cid_info_idx in range(len(cid_info_table)):
            cid_info = CidInfoConfig.from_index(self.f, cid_info_idx, self.config_manager).cid_info_payload

            if self.f.PRODUCT.F_IsPlatform and not cid_info.flags.mouse:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {CidTable(to_int(cid_info.ctrl_id))!r} '
                                         'is not emulated on the DEV board yet')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if int(Numeral(cid_info.ctrl_id)) not in self.emu_cid_list:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {CidTable(to_int(cid_info.ctrl_id))!r} is not emulated')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # Virtual buttons are ignored
            if not self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_0 and \
                    cid_info.flags.virtual:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {CidTable(to_int(cid_info.ctrl_id))!r}(virtual button) is skipped')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # Divert capability check
            if not cid_info.flags.divert:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(self, f'CID = {CidTable(to_int(cid_info.ctrl_id))!r} '
                                         'does not have divert capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if
            cid_divert_list.append(cid_info)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over cid_divert_list '
                                 f'{[CidTable(to_int(cid.ctrl_id)) for cid in cid_divert_list]}')
        # --------------------------------------------------------------------------------------------------------------
        for cid in cid_divert_list:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {CidTable(to_int(cid.ctrl_id))!r} and '
                                     'set divert = 1, dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_request = self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid.ctrl_id,
                divert_valid=True,
                divert=True)

            set_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=set_cid_request,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
            # ----------------------------------------------------------------------------------------------------------
            SpecialKeysMseButtonsTestUtils.check_response_expected_field(self, set_cid_request,
                                                                         set_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _divert_all_divertable_keys

    def _check_only_flock_event(self):
        """
        Toggle Fn lock state and check if the device only sends a fLockChange event without any other events
        """
        for fn_lock_state in [True, False]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Set FN lock to {"ON" if fn_lock_state else "OFF"} by FnLockKeyCombination')
            # ----------------------------------------------------------------------------------------------------------
            KeyMatrixTestUtils.switch_fn_lock_state(self, enable=fn_lock_state)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check only get a 0x40a3.fLockChange event')
            # ----------------------------------------------------------------------------------------------------------
            self.cleanup_battery_event_from_queue()
            FnInversionForMultiHostDevicesTestUtils.HIDppHelper.f_lock_change_event(self)
            ChannelUtils.check_queue_empty(self, queue_name=HIDDispatcher.QueueName.EVENT)
        # end for
    # end def _check_only_flock_event
# end class SpecialKeysMSEButtonsBusinessEmuTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
