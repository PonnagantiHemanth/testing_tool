#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_00c3.robustness
:brief: HID++ 2.0  Device Secure DFU control robustness test suite
:author: Stanislas Cottard <scottard@logitech.com>, Kevin Dayet <kdayet@logitech.com>
:date: 2020/09/04
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pylibrary.mcu.securitychunks import DfuCtrlChunk
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hidpp20.common.feature_00c3.securedfucontrol import DeviceSecureDfuControlTestCase
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils
from pytestbox.shared.base.dfuutils import DfuTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceSecureDfuControlRobustnessTestCase(DeviceSecureDfuControlTestCase):
    """
    Validate Secure DFU Control robustness testcases for the device (feature 0x00C3).
    """

    @features('SecureDfuControlUseNVS')
    @level('Robustness')
    @services('Debugger')
    def test_entering_dfu_param_in_nvs_superior_to_0(self):
        """
        getDfuControl when param value different than 0 in NVS. Check device is in bootloader mode after the reset
        performed with the requested user actions
        """
        self.generic_entering_dfu_param_in_nvs_superior_to_0()

        self.testCaseChecked("ROB_00C3_0001")
    # end def test_entering_dfu_param_in_nvs_superior_to_0

    @features('SecureDfuControlActionTypeNot0')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_reserved_enable_ignored(self):
        """
        setDfuControl processing shall ignore bits which are reserved for future use in the first enableDfu byte
        """
        self.generic_set_dfu_control_reserved_enable_ignored()

        self.testCaseChecked("ROB_00C3_0002#1")
    # end def test_set_dfu_control_reserved_enable_ignored

    @features('SecureDfuControlActionType0')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_reserved_enable_ignored_action_type_0(self):
        """
        setDfuControl processing shall ignore bits which are reserved for future use in the first enableDfu byte
        """
        self.post_requisite_force_reload_nvs = True

        # --------------------------------------------------------------------------------------------------------------
        self.logTitle2('Test loop over some reserved_enable_dfu values other than 0')
        # --------------------------------------------------------------------------------------------------------------
        for reserved_enable_dfu in compute_wrong_range(value=0x00, max_value=0x7F, min_value=0x01):
            if not self.f.PRODUCT.F_IsGaming:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Add a "NVS_DFU_ID" chunk with enable=0')
                # ------------------------------------------------------------------------------------------------------
                chunk = DfuCtrlChunk(enable=0, param=0)
                self.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_DFU_ID', data=HexList(chunk))
                DfuControlTestUtils.load_nvs(test_case=self)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send DFU setDfuControl with enableDfu=1 and '
                                     f'reserved_enable_dfu={reserved_enable_dfu}')
            # ----------------------------------------------------------------------------------------------------------
            DfuControlTestUtils.set_dfu_control(test_case=self, enable_dfu=1, reserved_enable_dfu=reserved_enable_dfu)
            if self.config_manager.current_protocol not in LogitechProtocol.unifying_protocols():
                DfuTestUtils.verify_communication_disconnection_then_reconnection(
                    test_case=self,
                    ble_service_changed_required=self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_Enabled)
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Check active entity is bootloader')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.update_feature_mapping(test_case=self, feature_id=DeviceInformation.FEATURE_ID)
            DeviceInformationTestUtils.check_active_entity_type(
                test_case=self,
                device_index=ChannelUtils.get_device_index(test_case=self),
                entity_type=DeviceInformation.EntityTypeV1.BOOTLOADER)

            if not self.f.PRODUCT.F_IsGaming:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Dump the NVS and verify the chunk has enable=1')
                # ------------------------------------------------------------------------------------------------------
                self.memory_manager.read_nvs()
                new_dfu_chunk_history = self.memory_manager.nvs_parser.get_chunk_history(chunk_id='NVS_DFU_ID')
                self.assertEqual(expected=1,
                                 obtained=to_int(new_dfu_chunk_history[-1].chunk_data[0]),
                                 msg='The enable parameter differs from the expected one')
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Reset to jump out of bootloader')
            # ----------------------------------------------------------------------------------------------------------
            self.reset()
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("ROB_00C3_0002#2")
    # end def test_set_dfu_control_reserved_enable_ignored_action_type_0

    @features('SecureDfuControlActionTypeNot0')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_reserved_ignored(self):
        """
        setDfuControl processing shall ignore bytes which are reserved for future use
        """
        self.generic_set_dfu_control_reserved_ignored()

        self.testCaseChecked("ROB_00C3_0003")
    # end def test_set_dfu_control_reserved_ignored

    @features('SecureDfuControlAllActionTypes')
    @level('Robustness')
    @services('Debugger')
    def test_get_dfu_control_software_id_ignored(self):
        """
        Validate getDfuControl padding bytes are ignored
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over getDfuControl software_id range (except 1, it is for '
                                 'event)')
        # ---------------------------------------------------------------------------
        for software_id in range(0x02, 0x10):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send getDfuControl with software_id={software_id}')
            # ---------------------------------------------------------------------------
            get_dfu_control = self.feature_under_test.get_dfu_control_cls(device_index=self.deviceIndex,
                                                                          feature_index=self.feature_id)
            get_dfu_control.softwareId = software_id
            get_dfu_control_response = self.send_report_wait_response(
                report=get_dfu_control,
                response_queue=self.hidDispatcher.common_message_queue,
                response_class_type=self.feature_under_test.get_dfu_control_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetDfuStatus response')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.reserved_enable_dfu),
                             msg='The reserved_enable_dfu parameter differs from the expected one')
            self.assertEqual(expected=0,
                             obtained=to_int(get_dfu_control_response.enable_dfu),
                             msg='The enable_dfu parameter differs from the expected one')
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlParam),
                             obtained=to_int(get_dfu_control_response.dfu_control_param),
                             msg='The dfu_control_param parameter differs from the expected one')
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlTimeout),
                             obtained=to_int(get_dfu_control_response.dfu_control_timeout),
                             msg='The dfu_control_timeout parameter differs from the expected one')
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionType),
                             obtained=to_int(get_dfu_control_response.dfu_control_action_type),
                             msg='The dfu_control_action_type parameter differs from the expected one')
            self.assertEqual(expected=to_int(self.f.PRODUCT.FEATURES.COMMON.SECURE_DFU_CONTROL.F_DfuControlActionData),
                             obtained=to_int(get_dfu_control_response.dfu_control_action_data),
                             msg='The dfu_control_action_data parameter differs from the expected one')
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROB_00C3_0004")
    # end def test_get_dfu_control_software_id_ignored

    @features('SecureDfuControlActionTypeNot0')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_software_id_ignored(self):
        """
        Validate setDfuControl SoftwareId input is ignored
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send getDfuControl')
        # ---------------------------------------------------------------------------
        get_dfu_control = self.feature_under_test.get_dfu_control_cls(device_index=self.deviceIndex,
                                                                      feature_index=self.feature_id)
        get_dfu_control_response = self.send_report_wait_response(
            report=get_dfu_control,
            response_queue=self.hidDispatcher.common_message_queue,
            response_class_type=self.feature_under_test.get_dfu_control_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check enable_dfu=0')
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=0,
                         obtained=to_int(get_dfu_control_response.enable_dfu),
                         msg='The enable_dfu parameter differs from the expected one')

        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over setDfuControl software_id range (except 1, it is '
                                               'for event)')
        # ---------------------------------------------------------------------------
        for software_id in range(0x02, 0x10):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(
                self, f'Send DFU setDfuControl with software_id = {software_id}, enable_dfu=1 and the correct magicKey')
            # ---------------------------------------------------------------------------
            set_dfu_control = self.feature_under_test.set_dfu_control_cls(device_index=self.deviceIndex,
                                                                          feature_index=self.feature_id,
                                                                          enable_dfu=1)
            set_dfu_control.softwareId = software_id
            self.send_report_wait_response(report=set_dfu_control,
                                           response_queue=self.hidDispatcher.common_message_queue,
                                           response_class_type=self.feature_under_test.set_dfu_control_response_cls)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Perform the device reset with the requested user actions '
                                                   'simultaneously')
            # ---------------------------------------------------------------------------
            DfuControlTestUtils.perform_action_to_enter_dfu_mode(
                test_case=self,
                action_type=get_dfu_control_response.dfu_control_action_type,
                action_data=get_dfu_control_response.dfu_control_action_data)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check the device is in Bootloader mode')
            # ---------------------------------------------------------------------------
            self.assertTrue(expr=DfuTestUtils.verify_device_on_fw_type(
                test_case=self,
                fw_type=DeviceInformation.EntityTypeV1.BOOTLOADER),
                msg="Device not in bootloader")

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send DFU Restart request to return in application mode')
            # ---------------------------------------------------------------------------
            DfuTestUtils.send_dfu_restart_function(test_case=self)
        # end for
        # ---------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("ROB_00C3_0005")
    # end def test_set_dfu_control_software_id_ignored

    @features('SecureDfuControlAllActionTypes')
    @level('Robustness')
    @services('Debugger')
    def test_get_dfu_control_padding_ignored(self):
        """
        Validate getDfuControl padding bytes are ignored
        """
        self.generic_get_dfu_control_padding_ignored()

        self.testCaseChecked("ROB_00C3_0006")
    # end def test_get_dfu_control_padding_ignored

    @features('SecureDfuControlAllActionTypes')
    @level('Robustness')
    @services('Debugger')
    def test_set_dfu_control_padding_ignored(self):
        """
        Validate setDfuControl padding bytes are ignored
        """
        self.generic_set_dfu_control_padding_ignored()

        self.testCaseChecked("ROB_00C3_0007")
    # end def test_set_dfu_control_padding_ignored
# end class DeviceSecureDfuControlRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
