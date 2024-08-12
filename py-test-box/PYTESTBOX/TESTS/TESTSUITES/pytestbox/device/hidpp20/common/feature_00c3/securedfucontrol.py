#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.securedfucontrol
:brief: HID++ 2.0  Device Secure DFU control test case
:author: Stanislas Cottard <scottard@logitech.com>, Kevin Dayet <kdayet@logitech.com>
:date: 2020/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from os.path import join

from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControl
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlFactory
from pylibrary.tools.numeral import to_int
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils
from pytestbox.shared.hidpp.securedfucontrol import CommonSecureDfuControlTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceSecureDfuControlTestCase(CommonSecureDfuControlTestCase, DeviceBaseTestCase):
    """
    Validate Secure DFU Control TestCases for the device (feature 0x00C3)
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x00C3)')
        # ---------------------------------------------------------------------------
        self.feature_id = ChannelUtils.update_feature_mapping(test_case=self, feature_id=SecureDfuControl.FEATURE_ID)

        # Get the feature under test
        self.feature_under_test = SecureDfuControlFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL))
    # end def setUp

    def _ignore_action_index_test(self, action_to_ignore_index):
        """
        Perform a test that ignore a user action which make it fail to enter DFU mode

        :param action_to_ignore_index: The index of the action to ignore
        :type action_to_ignore_index: ``int``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU setDfuControl with enableDfu=1')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send DFU getDfuControl')
        # ---------------------------------------------------------------------------
        get_dfu_control_response = DfuControlTestUtils.get_dfu_control(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for the getDfuControl response and check enableDfu=1')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=1,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        if action_to_ignore_index == 0:
            action_number_str = "first"
        elif action_to_ignore_index == 1:
            action_number_str = "second"
        elif action_to_ignore_index == 2:
            action_number_str = "third"
        else:
            assert False, "Cannot ignore action number {action_to_ignore_index} because there is only 3 " \
                          "action (from 0 to 2)"
        # end if

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, f'Perform the target reset without the {action_number_str} requested user action')
        # ---------------------------------------------------------------------------
        DfuControlTestUtils.perform_action_to_enter_dfu_mode(
            test_case=self,
            action_type=get_dfu_control_response.dfu_control_action_type,
            action_data=get_dfu_control_response.dfu_control_action_data,
            ignore_action_index=action_to_ignore_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the target stays in Main Application mode')
        # ---------------------------------------------------------------------------
        self.assertTrue(expr=DfuTestUtils.verify_target_on_fw_type(
            test_case=self,
            fw_type=DeviceInformation.EntityTypeV1.MAIN_APP),
            msg="Target not in application")
        self.cleanup_battery_event_from_queue()

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Dump the NVS and check enable byte is 0')
        # ---------------------------------------------------------------------------
        self.memory_manager.read_nvs()
        dfu_chunk = self.memory_manager.get_active_chunk_by_name(chunk_name='NVS_DFU_ID')
        self.assertEqual(expected=0,
                         obtained=to_int(dfu_chunk.enable),
                         msg='The enable parameter differs from the expected one')
    # end def _ignore_action_index_test

    def _test_other_action_type(self, action_type):
        """
        Reload a firmware with a specific action type value. For this to work, there should be the hex file in the
        DFU_FILES folder. The name format of this file is the same name as the regular hex file for the tests with
        "_action_type_XX" added before the ".hex", XX being a hexadecimal representation of the wanted action type
        value on 2 digits

        :param action_type: The wanted action type
        :type action_type: ``int``
        """
        hex_file_name = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)[:-4] + \
            f"_action_type_{action_type:02X}.hex"

        self.post_requisite_program_mcu_initial_state = True

        self.device_debugger.reload_file(firmware_hex_file=hex_file_name)

        DfuTestUtils.verify_communication_disconnection_then_reconnection(
            test_case=self,
            ble_service_changed_required=False)

        self._perform_business_case()
    # end def _test_other_action_type
# end class DeviceSecureDfuControlTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
