#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.functionality
:brief: HID++ 2.0 Special Keys MSE Buttons functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid.controlidtable import CidTable
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import CidInfoPayload
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidInfo
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReporting
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.docutils import DocUtils
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.cidutils import CidEmulation
from pytestbox.base.cidutils import CidInfoFlags
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_1b04.specialkeysmsebuttons import SpecialKeysMSEButtonsTestCase
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMSEButtonsFunctionalityTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validate the Keyboard reprogrammable Keys and Mouse buttons Functionality TestCases.
    """
    @features('Feature1B04')
    @features('Feature1B04WithFlags', CidInfoFlags.DIVERT_FLAG)
    @level('Functionality')
    def test_set_cid_reporting_divert_valid(self):
        """
        Validate the setCidReporting.dvalid = 0 doesn't change the configuration whatever the divert value (test 0
        and 1).

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the CID values in the config file of the product.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        # Virtual buttons are ignored for now
        if self.f.PRODUCT.F_IsPlatform:
            cid_list_d = [HexList(cid_info[:4]) for cid_info in self.config_manager.get_feature(
                self.config_manager.ID.CID_TABLE) if (CidInfoPayload.fromHexList(HexList(cid_info)).flags.divert and
                                                      not CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual
                                                      and CidInfoPayload.fromHexList(HexList(cid_info)).flags.mouse)]
        else:
            cid_list_d = [HexList(cid_info[:4]) for cid_info in self.config_manager.get_feature(
                self.config_manager.ID.CID_TABLE) if (CidInfoPayload.fromHexList(HexList(cid_info)).flags.divert and
                                                      not CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual)]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with divert capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_d in cid_list_d:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d}, set divert = 1, '
                                     f'dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id=cid_d, divert_valid=True,
                divert=True)
            get_cid_reporting_expected_response = get_cid_reporting_response_class(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id=cid_d, divert=True)
            # This function does the test step 2 and the test checks 1 & 2.
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.divert = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d} and set divert = 0'
                                     f', dvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(
                device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_id,
                ctrl_id=cid_d, divert_valid=False,
                divert=False)
            # This function does the test step 4 and the test checks 3 & 4
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.divert = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d} and set divert = 0'
                                     f', dvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=True,
                                                        divert=False)
            get_cid_reporting_expected_response.divert = False
            # This function does the test step 6 and the test checks 5 & 6
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.divert = 0')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_d} and set divert = 1'
                                     f', dvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_d,
                                                        divert_valid=False,
                                                        divert=True)
            # This function does the test step 8 and the test checks 7 & 8
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.divert = 0')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0015")
    # end def test_set_cid_reporting_divert_valid

    @features('Feature1B04')
    @features('Feature1B04WithFlags', CidInfoFlags.PERSIST_FLAG)
    @level('Functionality')
    def test_set_cid_reporting_persist_valid(self):
        """
        Validate the setCidReporting.pvalid = 0 doesn't change the configuration whatever the persist value (test 0
        and 1).

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        # Virtual buttons are ignored for now
        cid_list_p = [HexList(cid_info[:4]) for cid_info
                      in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                      if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.PERSIST_FLAG) == CidInfoFlags.PERSIST_FLAG and
                      (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with persist capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_p in cid_list_p:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_p} and set persist '
                                     f'= 1, pvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_p,
                                                        persist_valid=True,
                                                        persist=True)
            get_cid_reporting_expected_response = get_cid_reporting_response_class(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid_p,
                persist=True)
            # This function does the test step 2 and the test checks 1 & 2
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.persist = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_p} and set persist'
                                     f' = 0, pvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_p,
                                                        persist_valid=False,
                                                        persist=False)
            # This function does the test step 4 and the test checks 3 & 4
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.persist = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_p} and set persist '
                                     f'= 0, pvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_p,
                                                        persist_valid=True,
                                                        persist=False)
            get_cid_reporting_expected_response.persist = False
            # This function does the test step 6 and the test checks 5 & 6
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.persist = 0')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_p} and set persist '
                                     f'= 1, pvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_p,
                                                        persist_valid=False,
                                                        persist=True)
            # This function does the test step 8 and the test checks 7 & 8
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.persist = 0')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0016")
    # end def test_set_cid_reporting_persist_valid

    @features('Feature1B04V3+')
    @features('Feature1B04WithFlags', CidInfoFlags.FORCE_RAW_XY_FLAG)
    @level('Functionality')
    def test_set_cid_reporting_force_raw_xy_valid(self):
        """
        Validate the setCidReporting.fvalid = 0 doesn't change the configuration whatever the forceRawXY value (test
        0 and 1)

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        cid_list_f = [HexList(cid_info[:4]) for cid_info
                      in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                      if (int(cid_info[8:10] + cid_info[16:18], 16) & CidInfoFlags.FORCE_RAW_XY_FLAG) ==
                      CidInfoFlags.FORCE_RAW_XY_FLAG]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with forceRawXY capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_f in cid_list_f:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_f} and set '
                                     f'forceRawXY = 1, fvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_f,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=True)
            get_cid_reporting_expected_response = get_cid_reporting_response_class(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid_f,
                force_raw_xy=True)
            # This function does the test step 2 and the test checks 1 & 2
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.forceRawXY = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_f} and set '
                                     f'forceRawXY = 0, fvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_f,
                                                        force_raw_xy_valid=False,
                                                        force_raw_xy=False)
            # This function does the test step 4 and the test checks 3 & 4
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.forceRawXY = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_f}and set '
                                     f'forceRawXY = 0, fvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_f,
                                                        force_raw_xy_valid=True,
                                                        force_raw_xy=False)
            get_cid_reporting_expected_response.force_raw_xy = False
            # This function does the test step 6 and the test checks 5 & 6
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.forceRawXY = 0')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_f} and set '
                                     f'forceRawXY = 1, fvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_f,
                                                        force_raw_xy_valid=False,
                                                        force_raw_xy=True)
            # This function does the test step 8 and the test checks 7 & 8
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.forceRawXY = 0')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0017")
    # end def test_set_cid_reporting_force_raw_xy_valid

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlags', CidInfoFlags.RAW_XY_FLAG)
    @level('Functionality')
    def test_set_cid_reporting_raw_xy_valid(self):
        """
        Validate the setCidReporting.rvalid = 0 doesn't change the configuration whatever the rawXY value (test 0 and 1)

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        # Virtual buttons are ignored for now
        if self.f.PRODUCT.F_IsPlatform:
            cid_list_r = [HexList(cid_info[:4]) for cid_info in self.config_manager.get_feature(
                self.config_manager.ID.CID_TABLE) if (
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.divert == 1 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.raw_xy == 1 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual == 0 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.mouse == 1)]
        else:
            cid_list_r = [HexList(cid_info[:4]) for cid_info in self.config_manager.get_feature(
                self.config_manager.ID.CID_TABLE) if (
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.divert == 1 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).additional_flags.raw_xy == 1 and
                    CidInfoPayload.fromHexList(HexList(cid_info)).flags.virtual == 0)]
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with rawXY capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_r in cid_list_r:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set rawXY = '
                                     '1, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        raw_xy_valid=True,
                                                        raw_xy=True)
            get_cid_reporting_expected_response = get_cid_reporting_response_class(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid_r,
                raw_xy=True)
            # This function does the test step 2 and the test checks 1 & 2
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.rawXY = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set rawXY = '
                                     '0, rvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        raw_xy_valid=False,
                                                        raw_xy=False)
            # This function does the test step 4 and the test checks 3 & 4
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.rawXY = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set rawXY = '
                                     '0, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        raw_xy_valid=True,
                                                        raw_xy=False)
            get_cid_reporting_expected_response.raw_xy = False
            # This function does the test step 6 and the test checks 5 & 6
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.rawXY = 0')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set rawXY = '
                                     '1, rvalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        raw_xy_valid=False,
                                                        raw_xy=True)
            # This function does the test step 8 and the test checks 7 & 8
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.rawXY = 0')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0018")
    # end def test_set_cid_reporting_raw_xy_valid

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlags', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG)
    @level('Functionality')
    def test_set_cid_reporting_analytics_key_evt_valid(self):
        """
        Validate the setCidReporting.avalid = 0 doesn't change the configuration whatever the analyticsKeyEvt value (
        test 0 and 1)

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_a = [HexList(cid_info[:4]) for cid_info
                      in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                      if (int(cid_info[16:18], 16) & CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG) ==
                      CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG and
                      (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with analyticsKeyEvt '
                                 'capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_a in cid_list_a:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_a} and set '
                                     f'analyticsKeyEvt = 1, avalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_a,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=True)
            get_cid_reporting_expected_response = get_cid_reporting_response_class(
                device_index=ChannelUtils.get_device_index(test_case=self),
                feature_index=self.feature_id,
                ctrl_id=cid_a,
                analytics_key_evt=True)

            # This function does the test step 2 and the test checks 1 & 2
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.analyticsKeyEvt = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_a} and set '
                                     f'analyticsKeyEvt = 0, avalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_a,
                                                        analytics_key_event_valid=False,
                                                        analytics_key_event=False)
            # This function does the test step 4 and the test checks 3 & 4
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.analyticsKeyEvt = 1')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_a} and set '
                                     f'analyticsKeyEvt = 0, avalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_a,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=False)
            get_cid_reporting_expected_response.analytics_key_evt = False
            # This function does the test step 6 and the test checks 5 & 6
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.analyticsKeyEvt = 0')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_a} and set '
                                     f'analyticsKeyEvt = 1, avalid = 0 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_a,
                                                        analytics_key_event_valid=False,
                                                        analytics_key_event=True)
            # This function does the test step 8 and the test checks 7 & 8
            self.set_cid_reporting_and_get_cid_reporting(
                set_cid_reporting_request=set_cid_reporting,
                set_cid_reporting_response_class=set_cid_reporting_response_class,
                get_cid_reporting_expected_response=get_cid_reporting_expected_response,
                str_for_log_to_check='Validate response.analyticsKeyEvt = 0')
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0019")
    # end def test_set_cid_reporting_analytics_key_evt_valid
# end class SpecialKeysMSEButtonsFunctionalityTestCase


class SpecialKeysMSEButtonsFunctionalityEmuTestCase(SpecialKeysMSEButtonsTestCase):
    """
    Validates Keyboard reprogrammable Keys and Mouse buttons Functionality TestCases
    """
    @features('Feature1B04')
    @features('Feature1B04WithFlags', CidInfoFlags.DIVERT_FLAG)
    @level('Functionality')
    @services('HardwareReset')
    def test_cid_reporting_reset_after_restart(self):
        """
        Restart the DUT to check all settings of getCidReporting should return to default.
        """
        f = self.getFeatures()
        # Get the supported version
        get_cid_info_response_class = self.get_cid_info_response_class()
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()
        get_cid_reporting_response_class = self.get_cid_reporting_response_class()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value and verify '
                                     f'it has divert capability (skip other steps if not)')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = GetCidInfo(device_index=ChannelUtils.get_device_index(test_case=self),
                                      feature_index=self.feature_id,
                                      ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            if not isinstance(get_cid_info_response, SpecialKeysMSEButtons) and get_cid_info_response.virtual:
                # Virtual buttons are ignored for now
                continue

            # This test is only for keys with divert capability
            if not get_cid_info_response.divert:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace('CID = ' + str(get_cid_info_response.ctrl_id) + ' does not have divert capability')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            if self.f.PRODUCT.F_IsPlatform and not get_cid_info_response.mouse:
                # ------------------------------------------------------------------------------------------------------
                self.logTrace(f'CID = {get_cid_info_response.ctrl_id} is not emulated on the DEV board yet')
                # ------------------------------------------------------------------------------------------------------
                continue
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = '
                                     f'{get_cid_info_response.ctrl_id} and set divert = 1, dvalid = 1 and'
                                     f' all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=get_cid_info_response.ctrl_id,
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
        LogHelper.log_step(self, 'Restart DUT')
        # --------------------------------------------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        sleep(self.config_manager.get_feature(self.config_manager.ID.STARTUP_TIME_COLD_BOOT) / 1000)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID index in valid range')
        # --------------------------------------------------------------------------------------------------------------
        for index in range(f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_CidCount):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidInfo with index = {index} to get CID value')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_info = GetCidInfo(device_index=ChannelUtils.get_device_index(test_case=self),
                                      feature_index=self.feature_id,
                                      ctrl_id_index=index)
            get_cid_info_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_info,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_info_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send getCidReporting with CID = {get_cid_info_response.ctrl_id}')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting = GetCidReporting(device_index=ChannelUtils.get_device_index(test_case=self),
                                                feature_index=self.feature_id,
                                                ctrl_id=get_cid_info_response.ctrl_id)
            get_cid_reporting_response = ChannelUtils.send(
                test_case=self,
                report=get_cid_reporting,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=get_cid_reporting_response_class)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check each settings in getCidReportingResponse should return '
                                      'to default')
            # ----------------------------------------------------------------------------------------------------------
            get_cid_reporting_expected_response_hex = HexList('00' * HidppMessage.HEADER_SIZE,
                                                              get_cid_info_response.ctrl_id)
            get_cid_reporting_expected_response_hex.addPadding(size=HidppMessage.LONG_MSG_SIZE,
                                                               fromLeft=False)
            get_cid_reporting_expected_response = get_cid_reporting_response_class.fromHexList(
                get_cid_reporting_expected_response_hex)

            SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                self, get_cid_reporting_expected_response, get_cid_reporting_response)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1B04_0013")
    # end def test_cid_reporting_reset_after_restart

    def _set_cid_reporting_persist_without_divert(self):
        """
        Validate the setCidReporting.persist flag processing but with divert = 0.

        'If either of the divert or persist flags is set, the control will be diverted via HID++ notification.'

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_p = [HexList(cid_info[:4]) for cid_info in self.emu_cid_info_list
                      if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.PERSIST_FLAG) ==
                      CidInfoFlags.PERSIST_FLAG and (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with persist capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_p in cid_list_p:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_p} and set divert ='
                                     f' 0, dvalid = 1, persist = 1, pvalid = 1 and all other '
                                     f'parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_p,
                                                        persist_valid=True,
                                                        persist=True,
                                                        divert_valid=True,
                                                        divert=False)
            # This function does the test step 2 to 7 and check 1 to 5
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event_power_reset(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask_before=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD,
                stimuli_mask_after=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_p} and set divert ='
                                     f' 0, dvalid = 1, persist = 0, pvalid = 1 and all other '
                                     f'parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_p,
                                                        persist_valid=True,
                                                        persist=False,
                                                        divert_valid=True,
                                                        divert=False)
            # This function does the test steps 9 and 10 and the test checks 6 to 8
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
    # end def _set_cid_reporting_persist_without_divert

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.LIMITED, 2)
    @level('Functionality')
    @services('HardwareReset')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_persist_without_divert)
    def test_set_cid_reporting_persist_without_divert_limited(self):
        # See ``_set_cid_reporting_persist_without_divert``
        self._set_cid_reporting_persist_without_divert()
        self.testCaseChecked("FUN_1B04_0014#limited")
    # end def test_set_cid_reporting_persist_without_divert_limited

    @features('Feature1B04')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.FULL, 2)
    @level('Functionality')
    @services('HardwareReset')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_persist_without_divert)
    def test_set_cid_reporting_persist_without_divert_full(self):
        # See ``_set_cid_reporting_persist_without_divert``
        self._set_cid_reporting_persist_without_divert()
        self.testCaseChecked("FUN_1B04_0014#full")
    # end def test_set_cid_reporting_persist_without_divert_full

    def _set_cid_reporting_raw_xy_config_reset(self):
        """
        Validate the setCidReporting.rawXY processing: The "temporary" diversion means that it will be reset to its
        default value when a HID++ configuration reset occurs (i.e. software writes a 0x0000 cookie value).

        This will also do the same test for setCidReporting.divert.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x0020)')
        # --------------------------------------------------------------------------------------------------------------
        config_change_feature_id = ChannelUtils.update_feature_mapping(test_case=self,
                                                                       feature_id=ConfigChange.FEATURE_ID)

        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_list_r = [HexList(cid_info[:4]) for cid_info in self.emu_cid_info_list
                      if (int(cid_info[8:10] + cid_info[16:18], 16) &
                          (CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG)) ==
                      (CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG) and
                      (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with rawXY capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_r in cid_list_r:
            if to_int(cid_r) == CidTable.LEFT_CLICK:
                # Workaround for the CID = 0x0050 'Left Arrow' defined in the NRF52 platform configuration
                continue
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set divert ='
                                     ' 1, dvalid = 1, rawXY = 1, rvalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_r,
                                                        raw_xy_valid=True,
                                                        raw_xy=True,
                                                        divert_valid=True,
                                                        divert=True)
            # This function does the test steps 2 to 4 and the test checks 1 to 4
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_PXYRHPP_RRD)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send x0020.SetConfigurationComplete with Cookie = 0x0000')
            LogHelper.log_check(self, 'Validate the received response from SetConfigurationComplete')
            # ----------------------------------------------------------------------------------------------------------
            set_configuration_complete = SetConfigurationComplete(
                deviceIndex=ChannelUtils.get_device_index(test_case=self),
                featureId=config_change_feature_id,
                configurationCookie=0)
            ChannelUtils.send(
                test_case=self,
                report=set_configuration_complete,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=SetConfigurationCompleteResponse)

            # This function does the test steps 6 to 8 and the test checks 6 to 8
            SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                ctrl_id=cid_r,
                stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_PXYRH_RRH)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_raw_xy_config_reset

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG, CidEmulation.LIMITED)
    @features('Feature0020')
    @level('Functionality')
    @services('OpticalSensor')
    @DocUtils.copy_doc(_set_cid_reporting_raw_xy_config_reset)
    def test_set_cid_reporting_raw_xy_config_reset_limited(self):
        # See ``_set_cid_reporting_raw_xy_config_reset``
        self._set_cid_reporting_raw_xy_config_reset()
        self.testCaseChecked("FUN_1B04_0020#limited")
    # end def test_set_cid_reporting_raw_xy_config_reset_limited

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG, CidEmulation.FULL)
    @features('Feature0020')
    @level('Functionality')
    @services('OpticalSensor')
    @DocUtils.copy_doc(_set_cid_reporting_raw_xy_config_reset)
    def test_set_cid_reporting_raw_xy_config_reset_full(self):
        # See ``_set_cid_reporting_raw_xy_config_reset``
        self._set_cid_reporting_raw_xy_config_reset()
        self.testCaseChecked("FUN_1B04_0020#full")
    # end def test_set_cid_reporting_raw_xy_config_reset_full

    def _set_cid_reporting_analytics_config_reset(self):
        """
        Validate the setCidReporting.analyticsKeyEvt processing: The "temporary" diversion means that it will be
        reset to its default value when a HID++ configuration reset occurs (i.e. software writes a 0x0000 cookie value).

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x0020)')
        # --------------------------------------------------------------------------------------------------------------
        config_change_feature_id = ChannelUtils.update_feature_mapping(test_case=self,
                                                                       feature_id=ConfigChange.FEATURE_ID)

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
        LogHelper.log_info(self, 'Test Loop over CID value in valid range but with analyticsKeyEvt '
                                 'capability')
        # --------------------------------------------------------------------------------------------------------------
        for cid_a in cid_list_a:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_a} and set '
                                     f'analyticsKeyEvt = 1, avalid = 1 and all other parameters = 0')
            # ----------------------------------------------------------------------------------------------------------
            additional_fn_lock_mask = 0
            if int(Numeral(cid_a)) == CidTable.FN_LOCK and \
                    self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_Enabled:
                additional_fn_lock_mask = SpecialKeysMseButtonsTestUtils.StimulusMask.FN_LOCK_MASK
            # end if

            set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                        feature_index=self.feature_id,
                                                        ctrl_id=cid_a,
                                                        analytics_key_event_valid=True,
                                                        analytics_key_event=True)
            # This function does the test steps 2 and 3 and the test checks 1 to 3
            SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                request=set_cid_reporting,
                response_class=set_cid_reporting_response_class,
                stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRA_RRA | additional_fn_lock_mask)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send x0020.SetConfigurationComplete with Cookie = 0x0000')
            LogHelper.log_check(self, 'Validate the received response from SetConfigurationComplete')
            # ----------------------------------------------------------------------------------------------------------
            set_config_complete = SetConfigurationComplete(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                           featureId=config_change_feature_id,
                                                           configurationCookie=0)

            ChannelUtils.send(
                test_case=self,
                report=set_config_complete,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=SetConfigurationCompleteResponse)

            # This function does the test steps 5 and 6 and the test checks 5 and 6
            SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                test_case=self,
                feature=self.special_keys_and_mouse_buttons_feature,
                ctrl_id=cid_a,
                stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH | additional_fn_lock_mask)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_analytics_config_reset

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.LIMITED)
    @features('Feature0020')
    @level('Functionality')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_config_reset)
    def test_set_cid_reporting_analytics_config_reset_limited(self):
        # See ``_set_cid_reporting_analytics_config_reset``
        self._set_cid_reporting_analytics_config_reset()
        self.testCaseChecked("FUN_1B04_0021#limited")
    # end def test_set_cid_reporting_analytics_config_reset_limited

    @features('Feature1B04V4+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.ANALYTICS_KEY_EVENTS_FLAG, CidEmulation.FULL)
    @features('Feature0020')
    @level('Functionality')
    @services('PassiveHoldPress')
    @DocUtils.copy_doc(_set_cid_reporting_analytics_config_reset)
    def test_set_cid_reporting_analytics_config_reset_full(self):
        # See ``_set_cid_reporting_analytics_config_reset``
        self._set_cid_reporting_analytics_config_reset()
        self.testCaseChecked("FUN_1B04_0021#full")
    # end def test_set_cid_reporting_analytics_config_reset_full

    def _set_cid_reporting_remap_config_reset(self):
        """
        Validate the setCidReporting.remap processing: The remapping is temporary and is reset by the device to its
        own control ID when a HID++ configuration reset occurs.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x0020)')
        # --------------------------------------------------------------------------------------------------------------
        config_change_feature_id = ChannelUtils.update_feature_mapping(test_case=self,
                                                                       feature_id=ConfigChange.FEATURE_ID)

        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

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
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask) or other_group == self.NO_GROUP:
                    continue
                # end if

                group_mask = (1 << (other_group - 1)) if other_group != 0 else 0
                if (gmask & group_mask) != 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid}, '
                                             f'set remap = {other_cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=other_cid)
                    # This function does the test steps 2 and 3 and the test checks 1 to 3
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
                        remapped_cid=other_cid)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, 'Send x0020.SetConfigurationComplete with Cookie = 0x0000')
                    LogHelper.log_check(self, 'Validate the response from SetConfigurationComplete')
                    # --------------------------------------------------------------------------------------------------
                    config_change = SetConfigurationComplete(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=config_change_feature_id,
                                                             configurationCookie=0)
                    ChannelUtils.send(
                        test_case=self,
                        report=config_change,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=SetConfigurationCompleteResponse)

                    # This function does the test steps 5 and 6 and the test checks 5 and 6
                    SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        ctrl_id=cid,
                        stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)

                    # We just need to do it for one remap for each CID
                    break
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_remap_config_reset

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @features('Feature0020')
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_config_reset)
    def test_set_cid_reporting_remap_config_reset_limited(self):
        # See ``_set_cid_reporting_remap_config_reset``
        self._set_cid_reporting_remap_config_reset()
        self.testCaseChecked("FUN_1B04_0022#limited")
    # end def test_set_cid_reporting_remap_config_reset_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @features('Feature0020')
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_config_reset)
    def test_set_cid_reporting_remap_config_reset_full(self):
        # See ``_set_cid_reporting_remap_config_reset``
        self._set_cid_reporting_remap_config_reset()
        self.testCaseChecked("FUN_1B04_0022#full")
    # end def test_set_cid_reporting_remap_config_reset_full

    def _set_cid_reporting_remap_integrity(self):
        """
        Validate the setCidReporting.remap processing: While a button remains pressed changes to the remap setting on
        the button do not affect the functionality of the button. The new setting takes effect after the button is
        released.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_group_gmask_list = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                for cid_info in self.emu_cid_info_list
                                if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        for (cid, group, gmask) in cid_group_gmask_list:
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask):
                    continue
                # end if

                group_mask = (1 << (other_group - 1)) if other_group != 0 else 0

                if (gmask & group_mask) != 0:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Select Cid1 = {cid} and its remapped Cid2 = {other_cid}')
                    # --------------------------------------------------------------------------------------------------
                    # This function does the test step 2 and the test check 1
                    SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        ctrl_id=cid,
                        stimuli_masks=[SpecialKeysMseButtonsTestUtils.StimulusMask.PRH])

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'remap = {other_cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=other_cid)
                    # This function does the test step 4 and the test checks 2 and 3
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=[SpecialKeysMseButtonsTestUtils.StimulusMask.RRH])
                    # This function does the test steps 5 and 6 and the test checks 4 and 5
                    SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        ctrl_id=cid,
                        stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
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
                    set_cid_reporting_response = ChannelUtils.send(
                        test_case=self,
                        report=set_cid_reporting,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=set_cid_reporting_response_class)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate setCidReporting response parameters should be '
                                              'the same as inputs')
                    # --------------------------------------------------------------------------------------------------
                    SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                        self, set_cid_reporting, set_cid_reporting_response)

                    # We just need to do it for one remap
                    break
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
    # end def _set_cid_reporting_remap_integrity

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_integrity)
    def test_set_cid_reporting_remap_integrity_limited(self):
        # See ``_set_cid_reporting_remap_integrity``
        self._set_cid_reporting_remap_integrity()
        self.testCaseChecked("FUN_1B04_0023#limited")
    # end def test_set_cid_reporting_remap_integrity_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_integrity)
    def test_set_cid_reporting_remap_integrity_full(self):
        # See ``_set_cid_reporting_remap_integrity``
        self._set_cid_reporting_remap_integrity()
        self.testCaseChecked("FUN_1B04_0023#full")
    # end def test_set_cid_reporting_remap_integrity_full

    def _set_cid_reporting_remap_lower_priority_divert(self):
        """
        Validate the setCidReporting.remap processing: If a control is both temporarily diverted and remapped,
        the control is diverted using the original control ID and the remapping has no effect.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_group_gmask_list_d = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                  for cid_info in self.emu_cid_info_list
                                  if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.DIVERT_FLAG) ==
                                  CidInfoFlags.DIVERT_FLAG and
                                  (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        cid_group_gmask_list = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                for cid_info in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                                if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        can_run = False
        for (cid, group, gmask) in cid_group_gmask_list_d:
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask):
                    continue
                # end if

                group_mask = (1 << (other_group - 1)) if other_group != 0 else 0

                if (gmask & group_mask) != 0:
                    can_run = True
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Select Cid1 = {cid} and its remapped Cid2 =  {other_cid}')
                    # --------------------------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'divert = 1, dvalid = 1, remap = {other_cid} and all '
                                             f'other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        divert_valid=True,
                        divert=True,
                        remap=other_cid)
                    # This function does the test steps 3 and 4 and the test checks 1 to 3
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_RRD)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'divert = 0, dvalid = 1, remap = {other_cid} and all '
                                             f'other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        divert_valid=True,
                        divert=False,
                        remap=cid)

                    # This function does the test steps 6 and 7 and the test checks 4 to 6
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)

                    # We just need to do it for one remap
                    break
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
        # Prevent the test from being passed while it is actually not executed
        self.assertTrue(can_run, "Test should be run at least once")
    # end def _set_cid_reporting_remap_lower_priority_divert

    @features('Feature1B04V1+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_lower_priority_divert)
    def test_set_cid_reporting_remap_lower_priority_divert_limited(self):
        # See ``_set_cid_reporting_remap_lower_priority_divert``
        self._set_cid_reporting_remap_lower_priority_divert()
        self.testCaseChecked("FUN_1B04_0024#limited")
    # end def test_set_cid_reporting_remap_lower_priority_divert_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.FULL)
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_lower_priority_divert)
    def test_set_cid_reporting_remap_lower_priority_divert_full(self):
        # See ``_set_cid_reporting_remap_lower_priority_divert``
        self._set_cid_reporting_remap_lower_priority_divert()
        self.testCaseChecked("FUN_1B04_0024#full")
    # end def test_set_cid_reporting_remap_lower_priority_divert_full

    def _set_cid_reporting_remap_higher_priority_persist(self):
        """
        Validate the setCidReporting.remap processing: If a control is both persistently diverted and remapped,
        the native function of the target control ID will be performed and the diversion has no effect.
        Persistent settings are lower priority than temporary settings.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_group_gmask_list_p = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                  for cid_info in self.emu_cid_info_list
                                  if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.PERSIST_FLAG) !=
                                  CidInfoFlags.PERSIST_FLAG and
                                  (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        cid_group_gmask_list = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                for cid_info in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                                if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        can_run = False
        for (cid, group, gmask) in cid_group_gmask_list_p:
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask):
                    continue
                # end if

                group_mask = (1 << (other_group - 1)) if other_group != 0 else 0

                if (gmask & group_mask) != 0:
                    can_run = True
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Select Cid1 = {cid} and its remapped Cid2 = {other_cid}')
                    # --------------------------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'divert = 1, dvalid = 1, persist = 1, pvalid = 1, '
                                             f'remap = {other_cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        persist_valid=True,
                        persist=True,
                        divert_valid=True,
                        divert=True,
                        remap=other_cid)

                    # This function does the test steps 3 and 4 and the test checks 1 to 3
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
                        remapped_cid=other_cid)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'divert = 0, dvalid = 1, persist = 0, pvalid = 1, '
                                             f'remap = {cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        persist_valid=True,
                        persist=False,
                        divert_valid=True,
                        divert=False,
                        remap=cid)
                    # This function does the test steps 6 and 7 and the test checks 4 to 6
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)

                    # We just need to do it for one remap
                    break
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
        # Prevent the test from being passed while it is actually not executed
        self.assertTrue(can_run, "Test should be run at least once")
    # end def _set_cid_reporting_remap_higher_priority_persist

    @features('Feature1B04V1+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.LIMITED)
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_higher_priority_persist)
    def test_set_cid_reporting_remap_higher_priority_persist_limited(self):
        # See ``_set_cid_reporting_remap_higher_priority_persist``
        self._set_cid_reporting_remap_higher_priority_persist()
        self.testCaseChecked("FUN_1B04_0025#limited")
    # end def test_set_cid_reporting_remap_higher_priority_persist_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.FULL)
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_higher_priority_persist)
    def test_set_cid_reporting_remap_higher_priority_persist_full(self):
        # See ``_set_cid_reporting_remap_higher_priority_persist``
        self._set_cid_reporting_remap_higher_priority_persist()
        self.testCaseChecked("FUN_1B04_0025#full")
    # end def test_set_cid_reporting_remap_higher_priority_persist_full

    def _set_cid_reporting_remap_not_recursive(self):
        """
        Validate the setCidReporting.remap processing: If the target Cid of a remapping is diverted, the native
        function of the target Cid will be performed and the diversion has no effect. Remapping is not recursive.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # Virtual buttons are ignored for now
        cid_group_gmask_list_d = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                  for cid_info in self.config_manager.get_feature(self.config_manager.ID.CID_TABLE)
                                  if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.DIVERT_FLAG) ==
                                  CidInfoFlags.DIVERT_FLAG and
                                  (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        cid_group_gmask_list = [(HexList(cid_info[:4]), int(cid_info[12:14], 16), int(cid_info[14:16], 16))
                                for cid_info in self.emu_cid_info_list
                                if (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        can_run = False
        for (cid, group, gmask) in cid_group_gmask_list:
            for (other_cid, other_group, other_gmask) in cid_group_gmask_list_d:
                if (cid, group, gmask) == (other_cid, other_group, other_gmask):
                    continue
                # end if

                group_mask = (1 << (other_group - 1)) if other_group != 0 else 0

                if (gmask & group_mask) != 0:
                    can_run = True
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Select Cid1 = {cid} and its remapped Cid2 = {other_cid}')
                    # --------------------------------------------------------------------------------------------------
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {other_cid} and '
                                             f'set divert = 1, dvalid = 1 and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=other_cid,
                        divert_valid=True,
                        divert=True, )
                    set_cid_reporting_response = ChannelUtils.send(
                        test_case=self,
                        report=set_cid_reporting,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=set_cid_reporting_response_class)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate setCidReporting response parameters should be '
                                              'the same as inputs')
                    # --------------------------------------------------------------------------------------------------
                    SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                        self, set_cid_reporting, set_cid_reporting_response)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'remap = {other_cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=other_cid)
                    # This function does the test steps 4 and 5 and the test checks 2 to 4
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH,
                        remapped_cid=other_cid)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {other_cid} and '
                                             f'set divert = 0, dvalid = 1 and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=other_cid,
                        divert_valid=True,
                        divert=False)
                    set_cid_reporting_response = ChannelUtils.send(
                        test_case=self,
                        report=set_cid_reporting,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=set_cid_reporting_response_class)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_check(self, 'Validate setCidReporting response parameters should be '
                                              'the same as inputs')
                    # --------------------------------------------------------------------------------------------------
                    SpecialKeysMseButtonsTestUtils.check_response_expected_field(
                        self, set_cid_reporting, set_cid_reporting_response)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid} and set '
                                             f'remap = {cid} and all other parameters = 0')
                    # --------------------------------------------------------------------------------------------------
                    set_cid_reporting = set_cid_reporting_class(
                        device_index=ChannelUtils.get_device_index(test_case=self),
                        feature_index=self.feature_id,
                        ctrl_id=cid,
                        remap=cid)
                    # This function does the test steps 8 and 9 and the test checks 6 to 8
                    SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
                        test_case=self,
                        feature=self.special_keys_and_mouse_buttons_feature,
                        request=set_cid_reporting,
                        response_class=set_cid_reporting_response_class,
                        stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_RRH)

                    # We just need to do it for one remap
                    break
                # end if
            # end for
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop end')
        # --------------------------------------------------------------------------------------------------------------
        # Prevent the test from being passed while it is actually not executed
        self.assertTrue(can_run, "Test should be run at least once")
    # end def _set_cid_reporting_remap_not_recursive

    @features('Feature1B04V1+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG, CidEmulation.LIMITED)
    @features('Feature1B04WithRemappingEmulated', CidEmulation.LIMITED)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_not_recursive)
    def test_set_cid_reporting_remap_not_recursive_limited(self):
        # See ``_set_cid_reporting_remap_not_recursive``
        self._set_cid_reporting_remap_not_recursive()
        self.testCaseChecked("FUN_1B04_0026#limited")
    # end def test_set_cid_reporting_remap_not_recursive_limited

    @features('Feature1B04V1+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.PERSIST_FLAG, CidEmulation.FULL)
    @features('Feature1B04WithRemappingEmulated', CidEmulation.FULL)
    @level('Functionality')
    @DocUtils.copy_doc(_set_cid_reporting_remap_not_recursive)
    def test_set_cid_reporting_remap_not_recursive_full(self):
        # See ``_set_cid_reporting_remap_not_recursive``
        self._set_cid_reporting_remap_not_recursive()
        self.testCaseChecked("FUN_1B04_0026#full")
    # end def test_set_cid_reporting_remap_not_recursive_full

    @features('Feature1B04V2+')
    @features('Feature1B04WithFlagsEmulated', CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG, CidEmulation.LIMITED)
    @level('Functionality')
    @services('OpticalSensor')
    def test_set_cid_reporting_raw_xy_positive_negative(self):
        """
        Validate the divertedRawMouseXYEvent.dx and dy processing: test positive and negative displacement on X and Y.

        GetCidInfo and GetCount are tested with SetCidReporting in the Business test cases.
        Therefore we use the values in the config file.
        """
        # Get the supported version
        (set_cid_reporting_class, set_cid_reporting_response_class) = self.set_cid_reporting_classes()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Get first CID value with rawXY capability')
        # --------------------------------------------------------------------------------------------------------------
        # Virtual buttons are ignored for now
        cid_list_r = [HexList(cid_info[:4]) for cid_info in self.emu_cid_info_list
                      if (int(cid_info[8:10] + cid_info[16:18], 16) &
                          (CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG)) ==
                      (CidInfoFlags.DIVERT_FLAG | CidInfoFlags.RAW_XY_FLAG) and
                      (int(cid_info[8:10] + '00', 16) & CidInfoFlags.VIRTUAL_FLAG) == 0]

        cid_r = cid_list_r[0]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set divert = 1, '
                                 'dvalid = 1, rawXY = 1, rvalid = 1 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                    feature_index=self.feature_id,
                                                    ctrl_id=cid_r,
                                                    raw_xy_valid=True,
                                                    raw_xy=True,
                                                    divert_valid=True,
                                                    divert=True)
        # This function does the test steps 3 to 5 and the test checks 1 to 4
        SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            request=set_cid_reporting,
            response_class=set_cid_reporting_response_class,
            stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_PXYRHPP_RRD)

        # This function does the test steps 6 to 8 and the test checks 5 to 7
        SpecialKeysMseButtonsTestUtils.send_stimulus_and_verify(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            ctrl_id=cid_r,
            stimuli_masks=SpecialKeysMseButtonsTestUtils.StimulusMask.PRD_NXYRHPP_RRD, )

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send setCidReporting request with CID = {cid_r} and set divert = 0, '
                                 'dvalid = 1, rawXY = 0, rvalid = 1 and all other parameters = 0')
        # --------------------------------------------------------------------------------------------------------------
        set_cid_reporting = set_cid_reporting_class(device_index=ChannelUtils.get_device_index(test_case=self),
                                                    feature_index=self.feature_id,
                                                    ctrl_id=cid_r,
                                                    raw_xy_valid=True,
                                                    raw_xy=False,
                                                    divert_valid=True,
                                                    divert=False)
        # This function does the test steps 10 to 12 and the test checks 8 to 11
        SpecialKeysMseButtonsTestUtils.verify_response_and_stimulus_event(
            test_case=self,
            feature=self.special_keys_and_mouse_buttons_feature,
            request=set_cid_reporting,
            response_class=set_cid_reporting_response_class,
            stimuli_mask=SpecialKeysMseButtonsTestUtils.StimulusMask.PRH_PXYRH_RRH)

        self.testCaseChecked("FUN_1B04_0027")
    # end def test_set_cid_reporting_raw_xy_positive_negative
# end class SpecialKeysMSEButtonsFunctionalityEmuTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
