#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.tde.tde
:brief: Validates TDE sequence
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import GetNonVolatileMemoryAccessRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import GetNonVolatileMemoryAccessResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import SetNonVolatileMemoryAccessRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import SetNonVolatileMemoryAccessResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionResponse
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoRequest
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoResponse
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import ReceiverFwInfo
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import RFRegisterAccess
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessRequest
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.receiver.tde.tde import TDETestCase
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class TDEFunctionalityTestCase(TDETestCase):
    """
    TDE Functionality Test Case
    """
    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_receiver_tde_sequence_business_case(self):
        """
        BLE Pro - TDE Sequence for the receiver

        Sequence Diagram:
            TDE -> Receiver: Test Mode Control - Enable Manufacturing Test Mode
            TDE -> Receiver: Get FW Version
            TDE -> Receiver: Get Bootloader Version
            TDE -> Receiver: Read UID & Pass Flag
            TDE -> Receiver: Set RF Channel
            TDE -> Receiver: Enable RX
            TDE -> Receiver: Disable RF
            TDE -> Receiver: Read receiver Pairing Information
            TDE -> Receiver: Set RF Power
            TDE -> Receiver: Set Channel
            TDE -> Receiver: Enable TX
            TDE -> Receiver: Disable TX
            TDE -> Receiver: Write UID & Pass Flag
            TDE -> Receiver: Test Mode Control - Disable Test Mode
        """
        # Define values for tests
        tde_uid_nvmem_addr = 0x0001
        tde_pass_flag_nvmem_addr = 0x0002
        tde_uid_data = 0xA5
        tde_pass_flag_data = 0x11

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable Manufacturing Test Mode')
        # ---------------------------------------------------------------------------
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check enabled Manufacturing Test Mode')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Get FW Version')
        # ---------------------------------------------------------------------------
        # Get entity index for FW
        fw_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(str(HexList(
            ReceiverFwInfo.EntityType.MAIN_APP)))

        receiver_fw_info_resp = self.send_report_wait_response(
            report=GetReceiverFwInfoRequest(fw_entity_idx),
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetReceiverFwInfoResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check receiver fw information')
        # ---------------------------------------------------------------------------
        EnumerationTestUtils.ReceiverFwInfoResponseChecker.check_fields(
            self, receiver_fw_info_resp, GetReceiverFwInfoResponse,
            EnumerationTestUtils.ReceiverFwInfoResponseChecker.get_check_map_for_entity(self, fw_entity_idx))

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Get Bootloader Version')
        # ---------------------------------------------------------------------------
        # Get entity index for bootloader
        btld_entity_idx = self.config_manager.get_feature(ConfigurationManager.ID.FW_TYPE).index(
            str(HexList(ReceiverFwInfo.EntityType.BOOTLOADER)))

        receiver_fw_info_resp = self.send_report_wait_response(
            report=GetReceiverFwInfoRequest(btld_entity_idx),
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetReceiverFwInfoResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check receiver bootloader information')
        # ---------------------------------------------------------------------------
        EnumerationTestUtils.ReceiverFwInfoResponseChecker.check_fields(
            self, receiver_fw_info_resp, GetReceiverFwInfoResponse,
            EnumerationTestUtils.ReceiverFwInfoResponseChecker.get_check_map_for_entity(self, btld_entity_idx))

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Read UID')
        # ---------------------------------------------------------------------------
        read_uid_req = GetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                         nvm_address_lsb=tde_uid_nvmem_addr & 0xFF,
                                                         nvm_address_msb=(tde_uid_nvmem_addr >> 8) & 0xFF)

        err_rsp = self.send_report_wait_response(
            report=read_uid_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check read UID raises an error')
        # ---------------------------------------------------------------------------
        self.assertTupleEqual(
            (Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER, Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS),
            (int(Numeral(err_rsp.command_sub_id)), int(Numeral(err_rsp.address))),
            f'Reading an empty address should raise an error')

        self.assertEqual(Hidpp1ErrorCodes.ERR_RESOURCE_ERROR, int(err_rsp.error_code),
                         f'Reading an empty address should raise an ERR_RESOURCE_ERROR error')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Read Pass Flag')
        # ---------------------------------------------------------------------------
        read_pass_flag_req = GetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                               nvm_address_lsb=tde_pass_flag_nvmem_addr & 0xFF,
                                                               nvm_address_msb=(tde_pass_flag_nvmem_addr >> 8) & 0xFF)

        err_rsp = self.send_report_wait_response(
            report=read_pass_flag_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check read Pass Flag raises an error')
        # ---------------------------------------------------------------------------
        self.assertTupleEqual(
            (Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER, Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS),
            (int(Numeral(err_rsp.command_sub_id)), int(Numeral(err_rsp.address))),
            f'Reading an empty address should raise an error')

        self.assertEqual(Hidpp1ErrorCodes.ERR_RESOURCE_ERROR, int(err_rsp.error_code),
                         f'Reading an empty address should raise an ERR_RESOURCE_ERROR error')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Set RF Channel')
        # ---------------------------------------------------------------------------
        set_rf_channel_req = SetRFRegisterAccessRequest(rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
                                                        address_register=RFRegisterAccess.Page0AddrReg.RF_CHANNEL,
                                                        data=RFRegisterAccess.RFChannel.F_2400_MHZ)

        set_rf_channel_resp = self.send_report_wait_response(
            report=set_rf_channel_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check set RF Channel response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, set_rf_channel_resp, SetRFRegisterAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable RX')
        # ---------------------------------------------------------------------------
        self.post_requisite_disable_rf = True
        enable_rx_req = SetRFRegisterAccessRequest(
            rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
            address_register=RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
            data=RFRegisterAccess.TestModeEnableDisable.CONTINUOUS_RX_MODE_ENABLED)

        enable_rx_resp = self.send_report_wait_response(
            report=enable_rx_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check enable RX response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, enable_rx_resp, SetRFRegisterAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Disable RF')
        # ---------------------------------------------------------------------------
        disable_rf_req = SetRFRegisterAccessRequest(
            rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
            address_register=RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
            data=RFRegisterAccess.TestModeEnableDisable.RF_OFF)

        disable_rf_resp = self.send_report_wait_response(
            report=disable_rf_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check disable RF response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, disable_rf_resp, SetRFRegisterAccessResponse, {})
        self.post_requisite_disable_rf = False

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Read receiver Pairing information')
        # ---------------------------------------------------------------------------
        fw_info = EnumerationTestUtils.get_fw_version(self)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check FW version response')
        # ---------------------------------------------------------------------------
        EnumerationTestUtils.FwVersionResponseChecker.check_fields(self, fw_info, GetFwVersionResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Set RF Power')
        # ---------------------------------------------------------------------------
        set_rf_power_req = SetRFRegisterAccessRequest(rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
                                                      address_register=RFRegisterAccess.Page0AddrReg.RF_TX_POWER,
                                                      data=RFRegisterAccess.RFTXPower.NRF52xxxFamily.PLUS_0_DBM)

        set_rf_power_resp = self.send_report_wait_response(
            report=set_rf_power_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check set RF Power response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, set_rf_power_resp, SetRFRegisterAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Set RF Channel')
        # ---------------------------------------------------------------------------
        set_rf_channel_req = SetRFRegisterAccessRequest(rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
                                                        address_register=RFRegisterAccess.Page0AddrReg.RF_CHANNEL,
                                                        data=RFRegisterAccess.RFChannel.F_2400_MHZ)

        set_rf_channel_resp = self.send_report_wait_response(
            report=set_rf_channel_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check set RF Channel response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, set_rf_channel_resp, SetRFRegisterAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable TX')
        # ---------------------------------------------------------------------------
        self.post_requisite_disable_rf = True
        enable_tx_req = SetRFRegisterAccessRequest(
            rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
            address_register=RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
            data=RFRegisterAccess.TestModeEnableDisable.CONTINUOUS_WAVE_MODE_ENABLED)

        enable_tx_resp = self.send_report_wait_response(
            report=enable_tx_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check enable TX response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, enable_tx_resp, SetRFRegisterAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Disable TX')
        # ---------------------------------------------------------------------------
        disable_rf_req = SetRFRegisterAccessRequest(
            rf_page_register=RFRegisterAccess.RFPageRegister.PAGE_0,
            address_register=RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
            data=RFRegisterAccess.TestModeEnableDisable.RF_OFF)

        disable_rf_resp = self.send_report_wait_response(
            report=disable_rf_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check disable TX response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, disable_rf_resp, SetRFRegisterAccessResponse, {})
        self.post_requisite_disable_rf = False

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Write UID')
        # ---------------------------------------------------------------------------
        write_uid_req = SetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                          nvm_address_lsb=tde_uid_nvmem_addr & 0xFF,
                                                          nvm_address_msb=(tde_uid_nvmem_addr >> 8) & 0xFF,
                                                          data=tde_uid_data)

        write_uid_resp = self.send_report_wait_response(
            report=write_uid_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check write UID response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, write_uid_resp, SetNonVolatileMemoryAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Read UID')
        # ---------------------------------------------------------------------------
        read_uid_req = GetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                         nvm_address_lsb=tde_uid_nvmem_addr & 0xFF,
                                                         nvm_address_msb=(tde_uid_nvmem_addr >> 8) & 0xFF)

        read_uid_resp = self.send_report_wait_response(
            report=read_uid_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check read UID response')
        # ---------------------------------------------------------------------------
        TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.check_fields(
            self,
            read_uid_resp,
            GetNonVolatileMemoryAccessResponse,
            TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.get_check_map(tde_uid_nvmem_addr & 0xFF,
                                                                                 (tde_uid_nvmem_addr >> 8) & 0xFF,
                                                                                 tde_uid_data)
        )

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Write Pass Flag')
        # ---------------------------------------------------------------------------
        write_pass_flag_req = SetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                                nvm_address_lsb=tde_pass_flag_nvmem_addr & 0xFF,
                                                                nvm_address_msb=(tde_pass_flag_nvmem_addr >> 8) & 0xFF,
                                                                data=tde_pass_flag_data)

        write_pass_flag_resp = self.send_report_wait_response(
            report=write_pass_flag_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check write Pass Flag response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, write_pass_flag_resp, SetNonVolatileMemoryAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Read Pass Flag')
        # ---------------------------------------------------------------------------
        read_pass_flag_req = GetNonVolatileMemoryAccessRequest(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                                                               nvm_address_lsb=tde_pass_flag_nvmem_addr & 0xFF,
                                                               nvm_address_msb=(tde_pass_flag_nvmem_addr >> 8) & 0xFF)

        read_pass_flag_resp = self.send_report_wait_response(
            report=read_pass_flag_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check read Pass Flag response')
        # ---------------------------------------------------------------------------
        TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.check_fields(
            self,
            read_pass_flag_resp,
            GetNonVolatileMemoryAccessResponse,
            TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.get_check_map(tde_pass_flag_nvmem_addr & 0xFF,
                                                                                 (tde_pass_flag_nvmem_addr >> 8) & 0xFF,
                                                                                 tde_pass_flag_data)
        )

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Test Mode Control - Disable Manufacturing Test Mode')
        # ---------------------------------------------------------------------------
        disable_test_mode_control_req = SetTestModeControlRequest(
            test_mode_enable=TestModeControl.TestModeEnable.DISABLE_TEST_MODE
        )
        disable_test_mode_control_resp = self.send_report_wait_response(
            report=disable_test_mode_control_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetTestModeControlResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check Test Mode Control response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, disable_test_mode_control_resp, SetTestModeControlResponse, {})

        self.testCaseChecked("FNT_TDE_0001")
    # end def test_receiver_tde_sequence_business_case

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_read_test_mode_control(self):
        """
        Check Test Mode Control read command
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Read Test Mode Control')
        # ---------------------------------------------------------------------------
        test_mode_control_req = GetTestModeControlRequest()

        test_mode_control_resp = self.send_report_wait_response(
            report=test_mode_control_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetTestModeControlResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check Read Test Mode Control response')
        # ---------------------------------------------------------------------------
        TDETestUtils.GetTestModeControlResponseChecker.check_fields(
            self, test_mode_control_resp, GetTestModeControlResponse)

        self.testCaseChecked("FNT_TDE_0002")
    # end def test_read_test_mode_control
    
    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_write_test_mode_enable(self):
        """
        Check Write Test Mode Control enable
        """
        log_step, log_check = 1, 1
        for test_mode_enable in TestModeControl.TestModeEnable:
            # Enable Test Mode Control
            TDETestUtils.set_check_test_mode(self, test_mode_enable=test_mode_enable,
                                             log_step=log_step, log_check=log_check)
            log_step, log_check = log_step + 1, log_check + 1

            # Read Test Mode Control
            TDETestUtils.get_check_test_mode(self, test_mode_enable=test_mode_enable,
                                             log_step=log_step, log_check=log_check)
            log_step, log_check = log_step + 1, log_check + 1

        self.testCaseChecked("FNT_TDE_0003")
    # end def test_write_test_mode_enable

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_rf_register_access_test_mode_enabled(self):
        """
        0xD1 - RF Register Access : The manufacturing test mode must be enabled in register 0xD0 before accessing this
        register : Write RF Register Access with test mode enabled
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Write RF Register Access')
        # ---------------------------------------------------------------------------
        rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                            RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                                            RFRegisterAccess.TestModeEnableDisable.RF_OFF)

        rf_register_access_resp = self.send_report_wait_response(
            report=rf_register_access_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetRFRegisterAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check write RF Register Access response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, rf_register_access_resp, SetRFRegisterAccessResponse, {})

        self.testCaseChecked("FNT_TDE_0004")
    # end def test_rf_register_access_test_mode_enabled

    def _test_rf_register_access(self, page, address_register, values):
        """
        Check all available values for a page and an address register
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        for data in values:
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Write RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(page, address_register, data)

            rf_register_access_resp = self.send_report_wait_response(
                report=rf_register_access_req,
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetRFRegisterAccessResponse)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check write RF Register Access response')
            # ---------------------------------------------------------------------------
            TDETestUtils.MessageChecker.check_fields(self, rf_register_access_resp, SetRFRegisterAccessResponse, {})
        # end for
    # end def _test_rf_register_access

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_rf_register_access_page_0_address_0(self):
        """
        Check all available values for Page 0 Address 0 can be written
        """
        self.post_requisite_disable_rf = True
        supported_values = list(RFRegisterAccess.TestModeEnableDisable)
        supported_values.remove(RFRegisterAccess.TestModeEnableDisable.RETURN_TO_NORMAL_RECEIVER_MODE)
        self._test_rf_register_access(RFRegisterAccess.RFPageRegister.PAGE_0,
                                      RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                      supported_values)
        self.testCaseChecked("FNT_TDE_0005")
    # end def test_rf_register_access_page_0_address_0

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_rf_register_access_page_0_address_1(self):
        """
        Check all available values for Page 0 Address 1 can be written
        """
        self._test_rf_register_access(RFRegisterAccess.RFPageRegister.PAGE_0,
                                      RFRegisterAccess.Page0AddrReg.RF_CHANNEL,
                                      RFRegisterAccess.RFChannel)
        self.testCaseChecked("FNT_TDE_0006")
    # end def test_rf_register_access_page_0_address_1

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_rf_register_access_page_0_address_2(self):
        """
        Check all available values for Page 0 Address 2 can be written
        """
        self._test_rf_register_access(RFRegisterAccess.RFPageRegister.PAGE_0,
                                      RFRegisterAccess.Page0AddrReg.RF_TX_POWER,
                                      range(0x00, 0xFF))
        self.testCaseChecked("FNT_TDE_0007")
    # end def test_rf_register_access_page_0_address_2

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_rf_register_access_page_0_address_5(self):
        """
        Check all available values for Page 0 Address 5 can be written
        """
        self._test_rf_register_access(RFRegisterAccess.RFPageRegister.PAGE_0,
                                      RFRegisterAccess.Page0AddrReg.RF_FREQUENCY_MODULATION,
                                      RFRegisterAccess.RFFrequencyModulation)
        self.testCaseChecked("FNT_TDE_0009")
    # end def test_rf_register_access_page_0_address_5
    
    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_non_volatile_memory_access_test_mode_enabled(self):
        """
        0xD4 - Non-Volatile Memory Access: The manufacturing test mode must be enabled in register 0xD0 before
        accessing this register: Write and Read Non-Volatile Memory Access with test mode enabled
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Write Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        set_non_volatile_memory_access_req = SetNonVolatileMemoryAccessRequest(
            Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00, 0x00)

        set_non_volatile_memory_access_resp = self.send_report_wait_response(
            report=set_non_volatile_memory_access_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check write Non Volatile Memory Access response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(
            self, set_non_volatile_memory_access_resp, SetNonVolatileMemoryAccessResponse, {})

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Read Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        get_non_volatile_memory_access_req = GetNonVolatileMemoryAccessRequest(
            Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)

        get_non_volatile_memory_access_resp = self.send_report_wait_response(
            report=get_non_volatile_memory_access_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check read Non Volatile Memory Access response')
        # ---------------------------------------------------------------------------
        TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.check_fields(
            self, get_non_volatile_memory_access_resp, GetNonVolatileMemoryAccessResponse)

        self.testCaseChecked("FNT_TDE_0010")
    # end def test_non_volatile_memory_access_test_mode_enabled

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_non_volatile_memory_access_address_range(self):
        """
        0xD4 - Non-Volatile Memory Access: Write and Read Non-Volatile Memory Access address range
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        for address in [0,
                        self.f.RECEIVER.TDE.F_Non_Volatile_Memory_Access_Size // 2,
                        self.f.RECEIVER.TDE.F_Non_Volatile_Memory_Access_Size - 1]:
            address_lsb = address & 0xFF
            address_msb = (address >> 8) & 0xFF
            data = 0x00
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Write Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            set_non_volatile_memory_access_req = SetNonVolatileMemoryAccessRequest(
                Hidpp1Data.DeviceIndex.TRANSCEIVER, address_lsb, address_msb, data)

            set_non_volatile_memory_access_resp = self.send_report_wait_response(
                report=set_non_volatile_memory_access_req,
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetNonVolatileMemoryAccessResponse)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check write Non Volatile Memory Access response')
            # ---------------------------------------------------------------------------
            TDETestUtils.MessageChecker.check_fields(
                self, set_non_volatile_memory_access_resp, SetNonVolatileMemoryAccessResponse, {})

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Read Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            get_non_volatile_memory_access_req = GetNonVolatileMemoryAccessRequest(
                Hidpp1Data.DeviceIndex.TRANSCEIVER, address_lsb, address_msb)

            get_non_volatile_memory_access_resp = self.send_report_wait_response(
                report=get_non_volatile_memory_access_req,
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=GetNonVolatileMemoryAccessResponse)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check read Non Volatile Memory Access response')
            # ---------------------------------------------------------------------------
            TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.check_fields(
                self, get_non_volatile_memory_access_resp, GetNonVolatileMemoryAccessResponse,
                TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.get_check_map(address_lsb, address_msb, data)
            )
        # end for

        self.testCaseChecked("FNT_TDE_0011")
    # end def test_non_volatile_memory_access_address_range
# end class TDETestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
