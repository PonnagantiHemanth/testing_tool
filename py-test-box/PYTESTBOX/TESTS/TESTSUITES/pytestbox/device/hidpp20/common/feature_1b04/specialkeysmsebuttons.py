#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1b04.specialkeysmsebuttons
:brief: HID++ 2.0 Special Keys MSE Buttons test case
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/10/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.core import TYPE_FAILURE
from pyhid.hid.controlidtable import CID_TO_KEY_ID_MAP
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.specialkeysmsebuttons import GetCidReporting
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtons
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsFactory
from pyhid.hidpp.features.configchange import ConfigChange
from pyhid.hidpp.features.configchange import SetConfigurationComplete
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.fninversionformultihostdevicesutils import FnInversionForMultiHostDevicesTestUtils
from pytestbox.device.base.keymatrixutils import KeyMatrixTestUtils
from pytestbox.shared.base.specialkeysmsebuttonsutils import SpecialKeysMseButtonsTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SpecialKeysMSEButtonsTestCase(BaseTestCase):
    """
    Keyboard reprogrammable Keys and Mouse buttons BaseTestCases
    """
    # Control ID group 0 = does not belong to a group
    NO_GROUP = 0

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_releasing_cid_key = None
        self.post_requisite_reset_fn_lock_state = None

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(test_case=self, text='Send Root.GetFeature(0x1B04)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_id = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=SpecialKeysMSEButtons.FEATURE_ID)

        self.emu_cid_info_list = []
        for cid_info in self.config_manager.get_feature(ConfigurationManager.ID.CID_TABLE):
            cid = int(Numeral(HexList(cid_info[:4])))
            if cid in CID_TO_KEY_ID_MAP and CID_TO_KEY_ID_MAP[cid] in self.button_stimuli_emulator.connected_key_ids:
                self.emu_cid_info_list.append(cid_info)
            # end if
        # end for
        self.emu_cid_list = [int(Numeral(HexList(cid_info[:4]))) for cid_info in self.emu_cid_info_list]

        # Get the feature under test
        self.special_keys_and_mouse_buttons_feature = SpecialKeysMSEButtonsFactory.create(
            self.config_manager.get_feature_version(
                self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS))
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_releasing_cid_key is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text='Force the release of the key linked to the CID')
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.keystroke(CID_TO_KEY_ID_MAP[to_int(self.post_requisite_releasing_cid_key)])
            # end if
        # end with

        with self.manage_post_requisite():
            if self.status == TYPE_FAILURE:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(test_case=self, text='Empty all channel queues')
                # ------------------------------------------------------------------------------------------------------
                ChannelUtils.empty_queues(test_case=self)
            # end if
        # end with

        with self.manage_post_requisite():
            if self.status == TYPE_FAILURE and self.f.PRODUCT.FEATURES.COMMON.CONFIG_CHANGE.F_Enabled:
                config_change_feature_id = ChannelUtils.update_feature_mapping(
                    test_case=self, feature_id=ConfigChange.FEATURE_ID)

                if config_change_feature_id == 0:
                    self.log_warning("Impossible to do the Post-requisite because the feature 0x0020 is not accessible")
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_post_requisite(
                        test_case=self, text='If test failed, send x0020.SetConfigurationComplete with '
                                             'ConfigurationCookie = 0x0000 to reset the feature 0x1B04 flags')
                    # --------------------------------------------------------------------------------------------------
                    config_change = SetConfigurationComplete(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=config_change_feature_id,
                                                             configurationCookie=0)
                    ChannelUtils.send(
                        test_case=self,
                        report=config_change,
                        response_queue_name=HIDDispatcher.QueueName.COMMON,
                        response_class_type=SetConfigurationCompleteResponse)
                # end if
            # end if
        # end with

        with self.manage_post_requisite():
            if self.post_requisite_reset_fn_lock_state:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reset fn lock state to OFF (PWS keyboard default)")
                # ------------------------------------------------------------------------------------------------------
                fn_lock_change = KeyMatrixTestUtils.switch_fn_lock_state(self, enable=False)

                if fn_lock_change and self.f.PRODUCT.FEATURES.KEYBOARD.FN_INVERSION_FOR_MULTI_HOST_DEVICES.F_HasFnLock:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(self, "Get fLockChange event")
                    # --------------------------------------------------------------------------------------------------
                    FnInversionForMultiHostDevicesTestUtils.HIDppHelper.f_lock_change_event(self,
                                                                                            check_first_message=False)
                # end if
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def get_cid_info_response_class(self):
        """
        Get the CidInfo supported version

        :return: get_cid_info_response_class
        :rtype: ``GetCidInfoV0Response`` or inherited
        """
        return self.special_keys_and_mouse_buttons_feature.get_cid_info_response_cls
    # end def get_cid_info_response_class

    def get_cid_reporting_response_class(self):
        """
        Get the CidReporting supported version

        :return: get_cid_reporting_response_class
        :rtype: ``GetCidReportingV0Response`` or inherited
        """
        return self.special_keys_and_mouse_buttons_feature.get_cid_reporting_response_cls
    # end def get_cid_reporting_response_class

    def set_cid_reporting_classes(self):
        """
        Get the SetCidReporting supported version

        :return: (set_cid_reporting_class, set_cid_reporting_response_class)
        :rtype: ``Tuple[SpecialKeysMSEButtons, SpecialKeysMSEButtons]``
        """
        return self.special_keys_and_mouse_buttons_feature.set_cid_reporting_cls, \
            self.special_keys_and_mouse_buttons_feature.set_cid_reporting_response_cls
    # end def set_cid_reporting_classes

    def set_cid_reporting_and_get_cid_reporting(self, set_cid_reporting_request, set_cid_reporting_response_class,
                                                get_cid_reporting_expected_response, str_for_log_to_check):
        """
        Send a SetCidReporting request and check the DUT processing thru a GetCidReporting request.

        :param set_cid_reporting_request: The SetCidReporting request V0 to V5
        :type set_cid_reporting_request: ``SetCidReportingV0`` or ``SetCidReportingV1`` or ``SetCidReportingV2`` or
        ``SetCidReportingV3`` or ``SetCidReportingV4`` or ``SetCidReportingV5toV6``
        :param set_cid_reporting_response_class: The SetCidReportingResponse V0 to V5
        :type set_cid_reporting_response_class: ``SetCidReportingV0Response`` or ``SetCidReportingV1Response`` or
        ``SetCidReportingV2Response`` or ``SetCidReportingV3Response`` or ``SetCidReportingV4Response`` or
        ``SetCidReportingV5ToV6Response``
        :param get_cid_reporting_expected_response: The GetCidReporting expected response
        :type get_cid_reporting_expected_response: ``GetCidReportingResponse``
        :param str_for_log_to_check: The str for GetCidReporting check log.
        :type str_for_log_to_check: ``str``
        """
        set_cid_reporting_response = ChannelUtils.send(
            test_case=self, report=set_cid_reporting_request, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=set_cid_reporting_response_class)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate setCidReporting response parameters should be the same as inputs')
        # --------------------------------------------------------------------------------------------------------------
        SpecialKeysMseButtonsTestUtils.check_response_expected_field(
            self, set_cid_reporting_request, set_cid_reporting_response)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send getCidReporting by CID = {get_cid_reporting_expected_response.ctrl_id}')
        # --------------------------------------------------------------------------------------------------------------
        get_cid_reporting = GetCidReporting(device_index=ChannelUtils.get_device_index(test_case=self),
                                            feature_index=self.feature_id,
                                            ctrl_id=get_cid_reporting_expected_response.ctrl_id)
        get_cid_reporting_response = ChannelUtils.send(
            test_case=self, report=get_cid_reporting, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=get_cid_reporting_expected_response.__class__)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'{str_for_log_to_check}')
        # --------------------------------------------------------------------------------------------------------------
        # The remap field can be equal to 0 or its own CID and be acceptable
        if not self.f.PRODUCT.FEATURES.COMMON.SPECIAL_KEYS_MSE_BUTTONS.F_Version_0 and \
                get_cid_reporting_response.remap == get_cid_reporting_response.ctrl_id:
            get_cid_reporting_expected_response.remap = get_cid_reporting_response.ctrl_id
        # end if

        SpecialKeysMseButtonsTestUtils.check_response_expected_field(
            self, get_cid_reporting_expected_response, get_cid_reporting_response)
    # end def set_cid_reporting_and_get_cid_reporting
# end class SpecialKeysMSEButtonsTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
