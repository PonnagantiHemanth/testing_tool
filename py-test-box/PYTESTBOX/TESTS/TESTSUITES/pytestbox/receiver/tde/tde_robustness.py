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
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import RFRegisterAccess
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.receiver.tde.tde import TDETestCase
from pytestbox.shared.base.tdeutils import TDETestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class TDERobustnessTestCase(TDETestCase):
    """
    TDE Robustness TestCases
    """
    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_read_test_mode_control_device_index_out_of_range(self):
        """
        Read Test Mode Control with device index out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Device Index significant values')
        # ---------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Read Test Mode Control')
            # ---------------------------------------------------------------------------
            test_mode_control_req = GetTestModeControlRequest()
            test_mode_control_req.device_index = device_index

            err_resp = self.send_report_wait_response(
                report=test_mode_control_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0001")
    # end def test_read_test_mode_control_device_index_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_test_mode_control_device_index_out_of_range(self):
        """
        Write Test Mode Control with device index out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Device Index significant values')
        # ---------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Write Test Mode Control')
            # ---------------------------------------------------------------------------
            test_mode_control_req = SetTestModeControlRequest(TestModeControl.TestModeEnable.DISABLE_TEST_MODE)
            test_mode_control_req.device_index = device_index

            err_resp = self.send_report_wait_response(report=test_mode_control_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0002")
    # end def test_write_test_mode_control_device_index_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_test_mode_control_sub_id_out_of_range(self):
        """
        Test Mode Control with sub id out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Sub Id significant values')
        # ---------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Test Mode Control')
            # ---------------------------------------------------------------------------
            test_mode_control_req = GetTestModeControlRequest()
            test_mode_control_req.sub_id = sub_id

            err_resp = self.send_report_wait_response(report=test_mode_control_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                sub_id,
                Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL,
                [Hidpp1ErrorCodes.ERR_INVALID_SUBID, Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0003")
    # end def test_test_mode_control_sub_id_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_test_mode_control_test_mode_reserved_out_of_range(self):
        """
        Write Test Mode Control with Test Mode Reserved out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over significant values')
        # ---------------------------------------------------------------------------
        significant_values = [
            {
                # Enable RF PER Test Mode
                "test_mode_enable": 0,
                "reserved": 1
            },
            {
                # Enable 3G roller Test mode
                "test_mode_enable": 1,
                "reserved": 1
            },
            {
                # suspend sensor polling
                "test_mode_enable": 0,
                "reserved": 8
            },
            {
                # force full speed polling on device
                "test_mode_enable": 0,
                "reserved": 16
            },
            *[
                {
                    "test_mode_enable": 0,
                    "reserved": int(Numeral(reserved))
                } for reserved in compute_sup_values(HexList(Numeral(SetTestModeControlRequest.DEFAULT.RESERVED,
                                                   SetTestModeControlRequest.LEN.TEST_MODE_RESERVED // 8)))]
        ]
        for values in significant_values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Test Mode Control')
            # ---------------------------------------------------------------------------
            test_mode_control_req = SetTestModeControlRequest(values["test_mode_enable"])
            test_mode_control_req.test_mode_reserved = values["reserved"]

            err_resp = self.send_report_wait_response(report=test_mode_control_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.TEST_MODE_CONTROL,
                [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0004")
    # end def test_write_test_mode_control_test_mode_reserved_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_rf_register_access_device_index_out_of_range(self):
        """
        Write RF Register Access with device index out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Device Index significant values')
        # ---------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send Write RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                                RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                                                RFRegisterAccess.TestModeEnableDisable.RF_OFF)
            rf_register_access_req.device_index = device_index

            err_resp = self.send_report_wait_response(
                report=rf_register_access_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0005")
    # end def test_write_rf_register_access_device_index_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_rf_register_access_sub_id_out_of_range(self):
        """
        RF Register Access with sub id out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Sub Id significant values')
        # ---------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                                RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                                                RFRegisterAccess.TestModeEnableDisable.RF_OFF)
            rf_register_access_req.sub_id = sub_id

            err_resp = self.send_report_wait_response(report=rf_register_access_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                sub_id,
                Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_SUBID, Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0006")
    # end def test_rf_register_access_sub_id_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_rf_register_access_page_out_of_range(self):
        """
        Write RF Register Access with page out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over significant values')
        # ---------------------------------------------------------------------------
        for page in compute_sup_values(int(RFRegisterAccess.RFPageRegister.PAGE_0)):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(page,
                                                                RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                                                RFRegisterAccess.TestModeEnableDisable.RF_OFF)

            err_resp = self.send_report_wait_response(report=rf_register_access_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0007")
    # end def test_write_rf_register_access_page_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_rf_register_access_address_register_out_of_range(self):
        """
        Write RF Register Access with address register out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over significant values')
        # ---------------------------------------------------------------------------
        values = compute_sup_values(int(RFRegisterAccess.Page0AddrReg.RF_FREQUENCY_MODULATION))
        values.append(RFRegisterAccess.Page0AddrReg.RF_FREQUENCY_TUNING)
        for address_register in compute_sup_values(int(RFRegisterAccess.Page0AddrReg.RF_FREQUENCY_MODULATION)):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                                address_register,
                                                                RFRegisterAccess.TestModeEnableDisable.RF_OFF)

            err_resp = self.send_report_wait_response(report=rf_register_access_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0008")
    # end def test_write_rf_register_access_address_register_out_of_range

    def _test_rf_register_access_data_out_of_range(self, page, address_register, values):
        """
        Check values out of range raise an error for a page and an address register
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        for data in values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Write RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(page, address_register, data)

            err_resp = self.send_report_wait_response(
                report=rf_register_access_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
    # end def _test_rf_register_access

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_rf_register_access_page_0_address_0_data_out_of_range(self):
        """
        Check values out of range for Page 0 Address 0
        """
        self.post_requisite_disable_rf = True
        self._test_rf_register_access_data_out_of_range(
            RFRegisterAccess.RFPageRegister.PAGE_0,
            RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
            compute_sup_values(int(RFRegisterAccess.TestModeEnableDisable.RETURN_TO_NORMAL_RECEIVER_MODE)))
        self.testCaseChecked("ROT_TDE_0009")
    # end def test_rf_register_access_page_0_address_0_data_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_rf_register_access_page_0_address_3_data_out_of_range(self):
        """
        Check values out of range for Page 0 Address 3
        """
        self._test_rf_register_access_data_out_of_range(
            RFRegisterAccess.RFPageRegister.PAGE_0,
            RFRegisterAccess.Page0AddrReg.RF_CHANNEL_INDEX,
            compute_sup_values(int(RFRegisterAccess.RFChannelIndex.MAX)))
        self.testCaseChecked("ROT_TDE_0011")
    # end def test_rf_register_access_page_0_address_3_data_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_rf_register_access_page_0_address_5_data_out_of_range(self):
        """
        Check values out of range for Page 0 Address 5
        """
        self._test_rf_register_access_data_out_of_range(
            RFRegisterAccess.RFPageRegister.PAGE_0,
            RFRegisterAccess.Page0AddrReg.RF_FREQUENCY_MODULATION,
            compute_sup_values(int(RFRegisterAccess.RFFrequencyModulation.F_160_KHZ)))
        self.testCaseChecked("ROT_TDE_0012")
    # end def test_rf_register_access_page_0_address_5_data_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_rf_register_access_test_mode_disabled(self):
        """
        0xD1 - RF Register Access : The manufacturing test mode must be enabled in register 0xD0 before accessing this
        register : Write RF Register Access with test mode disabled
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Disable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Write RF Register Access')
        # ---------------------------------------------------------------------------
        rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                            RFRegisterAccess.Page0AddrReg.TEST_MODE_ENABLE_DISABLE,
                                                            RFRegisterAccess.TestModeEnableDisable.RF_OFF)

        err_resp = self.send_report_wait_response(
            report=rf_register_access_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check error response')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
            [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])

        self.testCaseChecked("ROT_TDE_0013")
    # end def test_rf_register_access_test_mode_disabled

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_non_volatile_memory_access_sub_id_out_of_range(self):
        """
        Non Volatile Memory Access with sub id out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Sub Id significant values')
        # ---------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            nvm_access_req = GetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)
            nvm_access_req.sub_id = sub_id

            err_resp = self.send_report_wait_response(report=nvm_access_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                sub_id,
                Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_SUBID, Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0014")
    # end def test_non_volatile_memory_access_sub_id_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_read_non_volatile_memory_access_device_index_out_of_range(self):
        """
        Read Non Volatile Memory Access with device index out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Device Index significant values')
        # ---------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Read Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            test_mode_control_req = GetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)
            test_mode_control_req.device_index = device_index

            err_resp = self.send_report_wait_response(
                report=test_mode_control_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0015")
    # end def test_read_non_volatile_memory_access_device_index_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_non_volatile_memory_access_device_index_out_of_range(self):
        """
        Write Non Volatile Memory Access with device index out of range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Device Index significant values')
        # ---------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Write Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            test_mode_control_req = SetNonVolatileMemoryAccessRequest(
                Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00, 0x00)
            test_mode_control_req.device_index = device_index

            err_resp = self.send_report_wait_response(
                report=test_mode_control_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0016")
    # end def test_write_non_volatile_memory_access_device_index_out_of_range

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_non_volatile_memory_access_address_out_of_range(self):
        """
        Write and Read Non-Volatile Memory Access with test mode enabled only on permitted addresses
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        for address in [self.f.RECEIVER.TDE.F_Non_Volatile_Memory_Access_Size + 1, 0xFFFE, 0xFFFF,
                        (0xFFFF - self.f.RECEIVER.TDE.F_Non_Volatile_Memory_Access_Size + 1) // 2]:
            address_lsb = address & 0xFF
            address_msb = (address >> 8) & 0xFF
            data = 0x00
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Write Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            set_non_volatile_memory_access_req = SetNonVolatileMemoryAccessRequest(
                Hidpp1Data.DeviceIndex.TRANSCEIVER, address_lsb, address_msb, data)

            err_resp = self.send_report_wait_response(
                report=set_non_volatile_memory_access_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Read Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            get_non_volatile_memory_access_req = GetNonVolatileMemoryAccessRequest(
                Hidpp1Data.DeviceIndex.TRANSCEIVER, address_lsb, address_msb)

            err_resp = self.send_report_wait_response(
                report=get_non_volatile_memory_access_req,
                response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        self.testCaseChecked("FNT_TDE_0017")
    # end def test_non_volatile_memory_access_address_out_of_range

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_read_non_volatile_memory_access_test_mode_disabled(self):
        """
        0xD4 - Non-Volatile Memory Access: The manufacturing test mode must be enabled in register 0xD0 before
        accessing this register: Read Non-Volatile Memory Access with test mode disabled
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Disable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Read Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        nvm_access_req = GetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)

        err_resp = self.send_report_wait_response(
            report=nvm_access_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check error response')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
            [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])

        self.testCaseChecked("ROT_TDE_0018")
    # end def test_read_non_volatile_memory_access_test_mode_disabled

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_read_non_volatile_memory_access_test_mode_disabled_written_address(self):
        """
        0xD4 - Non-Volatile Memory Access: The manufacturing test mode must be enabled in register 0xD0 before
        accessing this register: Read Non-Volatile Memory Access with test mode disabled at a previously written address
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Write Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        write_nvm_access_req = SetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00, 0x00)

        write_nvm_access_resp = self.send_report_wait_response(
            report=write_nvm_access_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check write response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, write_nvm_access_resp, SetNonVolatileMemoryAccessResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Disable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Read Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        nvm_access_req = GetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)

        err_resp = self.send_report_wait_response(
            report=nvm_access_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check error response')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
            [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])

        self.testCaseChecked("ROT_TDE_0019")
    # end def test_read_non_volatile_memory_access_test_mode_disabled

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_write_non_volatile_memory_access_test_mode_disabled(self):
        """
        0xD4 - Non-Volatile Memory Access: The manufacturing test mode must be enabled in register 0xD0 before
        accessing this register: Write Non-Volatile Memory Access with test mode disabled
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Disable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Write Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        nvm_access_req = SetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00, 0x00)

        err_resp = self.send_report_wait_response(
            report=nvm_access_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check error response')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
            [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Read Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        nvm_access_req = GetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)

        err_resp = self.send_report_wait_response(
            report=nvm_access_req,
            response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check read raises an error because nothing was written previously')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
            [Hidpp1ErrorCodes.ERR_RESOURCE_ERROR])

        self.testCaseChecked("ROT_TDE_0020")
    # end def test_read_non_volatile_memory_access_test_mode_disabled

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_read_non_volatile_memory_access_padding_ignored(self):
        """
        Check Read Non Volatile Memory Access padding is ignored
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Write Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        write_nvm_access_req = SetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00, 0x00)

        write_nvm_access_resp = self.send_report_wait_response(
            report=write_nvm_access_req,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetNonVolatileMemoryAccessResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check write response')
        # ---------------------------------------------------------------------------
        TDETestUtils.MessageChecker.check_fields(self, write_nvm_access_resp, SetNonVolatileMemoryAccessResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over padding significant values')
        # ---------------------------------------------------------------------------
        for padding in compute_sup_values(HexList(Numeral(GetNonVolatileMemoryAccessRequest.DEFAULT.PADDING,
                                                        GetNonVolatileMemoryAccessRequest.LEN.PADDING // 8))):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Read Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            nvm_access_req = GetNonVolatileMemoryAccessRequest(Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)
            nvm_access_req.padding = padding

            nvm_access_resp = self.send_report_wait_response(report=nvm_access_req,
                                                             response_queue=self.hidDispatcher.receiver_response_queue,
                                                             response_class_type=GetNonVolatileMemoryAccessResponse)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 2: Check read Non Volatile Memory Access')
            # ---------------------------------------------------------------------------
            TDETestUtils.GetNonVolatileMemoryAccessResponseChecker.check_fields(self,
                                                                                nvm_access_resp,
                                                                                GetNonVolatileMemoryAccessResponse)
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End For Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0021")
    # end def test_read_non_volatile_memory_access_padding_ignored

    @features('RcvBLEProTDE')
    @level('Robustness')
    def test_read_rf_register_access_not_supported(self):
        """
        Read RF Register Access should not be supported, for any page register
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over RF Register Page significant values')
        # ---------------------------------------------------------------------------
        for rf_page_register in RFRegisterAccess.RFPageRegister:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 2: Send RF Register Access')
            # ---------------------------------------------------------------------------
            rf_register_access_req = SetRFRegisterAccessRequest(RFRegisterAccess.RFPageRegister.PAGE_0,
                                                                rf_page_register,
                                                                0x00)
            rf_register_access_req.sub_id = Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER
            rf_register_access_req.rf_page_register = rf_page_register

            err_resp = self.send_report_wait_response(report=rf_register_access_req,
                                                      response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                      response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check error response')
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                err_resp,
                Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.RF_REGISTER_ACCESS,
                [Hidpp1ErrorCodes.ERR_INVALID_SUBID, Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("ROT_TDE_0022")
    # end def test_rf_register_access_sub_id_out_of_range

    @features('RcvBLEProTDE')
    @level('Functionality')
    def test_read_non_volatile_memory_access_empty_address(self):
        """
        0xD4 - Non-Volatile Memory Access: Read Non-Volatile Memory Access at address not previously written
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Read Non Volatile Memory Access')
        # ---------------------------------------------------------------------------
        get_non_volatile_memory_access_req = GetNonVolatileMemoryAccessRequest(
            Hidpp1Data.DeviceIndex.TRANSCEIVER, 0x00, 0x00)

        err_resp = self.send_report_wait_response(report=get_non_volatile_memory_access_req,
                                                  response_queue=self.hidDispatcher.receiver_error_message_queue,
                                                  response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check error response')
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp,
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.NON_VOLATILE_MEMORY_ACCESS,
            [Hidpp1ErrorCodes.ERR_RESOURCE_ERROR])

        self.testCaseChecked("ROT_TDE_0023")
    # end def test_read_non_volatile_memory_access_empty_address
# end class TDETestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
