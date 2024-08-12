#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.tde.prepairing_robustness
:brief: Validate BLE Pro Prepairing
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/06/11
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.notifications.deviceconnection import BLEProReceiverInformation
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.prepairingdata import GetPrepairingDataRequest
from pyhid.hidpp.hidpp1.registers.prepairingdata import GetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingdata import PrepairingData
from pyhid.hidpp.hidpp1.registers.prepairingdata import SetPrepairingDataRequest
from pyhid.hidpp.hidpp1.registers.prepairingdata import SetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import PrepairingManagement
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementRequest
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementResponse
from pyhid.hidpp.hidpp1.registers.randomdata import GetRandomDataRequest
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralRequest
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralRequest
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralRequest
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralRequest
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyRequest
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_sup_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.tde.prepairing import PrepairingTestCase
from pytestbox.shared.base.bleproreceiverprepairingutils import BleProReceiverPrepairingTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PrepairingRobustnessTestCase(PrepairingTestCase):
    """
    Prepairing TestCases
    """
    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_sub_id_out_of_range(self):
        """
        Prepairing Management with SubId out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Sub Id significant values')
        # --------------------------------------------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send Prepairing Management with sub id {sub_id}')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            prepairing_management_req = SetPrepairingManagementRequest(
                self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
            prepairing_management_req.sub_id = sub_id
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_management_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                sub_id,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
                [Hidpp1ErrorCodes.ERR_INVALID_SUBID, Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0001")
    # end def test_prepairing_management_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_device_index_out_of_range(self):
        """
        Prepairing Management with Device Index out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Device Index significant values')
        # --------------------------------------------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Prepairing Management')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            prepairing_management_req = SetPrepairingManagementRequest(
                self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
            prepairing_management_req.device_index = device_index
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_management_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0002")
    # end def test_write_test_mode_control_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_pairing_slot_out_of_range(self):
        """
        Prepairing Management with Pairing Slot out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Pairing Slot significant values')
        # --------------------------------------------------------------------------------------------------------------
        pairing_slot_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        pairing_slot_values.append(0x00)
        for pairing_slot in pairing_slot_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Prepairing Management')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            prepairing_management_req = SetPrepairingManagementRequest(
                pairing_slot, PrepairingManagement.PrepairingManagementControl.START)
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_management_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0003")
    # end def test_prepairing_management_pairing_slot_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_prepairing_management_control_out_of_range(self):
        """
        Prepairing Management with Prepairing Management Control out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Prepairing Management Control significant values')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_management_control_values = compute_sup_values(
            int(PrepairingManagement.PrepairingManagementControl.DELETE))
        for prepairing_management_control in prepairing_management_control_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Prepairing Management')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_management_req = SetPrepairingManagementRequest(
                self.prepairing_slot, prepairing_management_control)
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_management_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0004")
    # end def test_prepairing_management_prepairing_management_control_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_pairing_slot_at_store_different_from_start(self):
        """
        0xE7 - Prepairing Management : The command will be rejected (ERR_REQUEST_UNAVAILABLE) if the pairing slot at
        Store step is not the same as the one of Start step
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Pre Pairing Slot significant values')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_slot_values = list(range(1, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots))
        prepairing_slot_values.remove(self.prepairing_slot)
        for prepairing_slot in prepairing_slot_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Prepairing Management Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            set_prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, set_prepairing_management_resp, SetPrepairingManagementResponse, {})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set keys')
            # ----------------------------------------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.set_keys(
                self, self.ltk_key, self.irk_local_key, self.irk_remote_key, self.csrk_local_key, self.csrk_remote_key)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Set Prepairing Data')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
                self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, prepairing_data_resp, SetPrepairingDataResponse, {})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send Prepairing Management Store with pairing slot = {prepairing_slot}')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_management_req = SetPrepairingManagementRequest(
                prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_management_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
                [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0005")
    # end def test_prepairing_management_pairing_slot_at_store_different_from_start

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_store_before_start(self):
        """
        0xE7 - Prepairing Management : Prepairing Management Control Store before Start
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Store')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_management_req = SetPrepairingManagementRequest(
            self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)
        error_response = ChannelUtils.send(
            test_case=self,
            report=prepairing_management_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0006")
    # end def test_prepairing_management_store_before_start

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_store_ltk_missing(self):
        """
        0xE7 - Prepairing Management : The command will be rejected (ERR_REQUEST_UNAVAILABLE) if the mandatory fields
        are not present at Store step : LTK key missing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        set_prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_prepairing_management_resp, SetPrepairingManagementResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Prepairing Data')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Store')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_management_req = SetPrepairingManagementRequest(
            self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)
        error_response = ChannelUtils.send(
            test_case=self,
            report=prepairing_management_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0007")
    # end def test_prepairing_management_store_ltk_missing

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_store_device_address_missing(self):
        """
        xE7 - Prepairing Management : The command will be rejected (ERR_REQUEST_UNAVAILABLE) if the mandatory fields
        are not present at Store step : Device Address missing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        set_prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_prepairing_management_resp, SetPrepairingManagementResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set keys')
        # --------------------------------------------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.set_keys(
            self, self.ltk_key, self.irk_local_key, self.irk_remote_key, self.csrk_local_key, self.csrk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Store')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_management_req = SetPrepairingManagementRequest(
            self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)
        error_response = ChannelUtils.send(
            test_case=self,
            report=prepairing_management_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0008")
    # end def test_prepairing_management_store_device_address_missing

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_management_data_discarded_on_error(self):
        """
        0xE7 - Prepairing Management : The storage of prepairing data is done only in the case of a successful
        pairing sequence. So if an error occurs during the pairing sequence, all the data changes linked to this
        pairing sequence are discarded and the pairing sequence is closed.
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        set_prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_prepairing_management_resp, SetPrepairingManagementResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set keys')
        # --------------------------------------------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.set_keys(
            self, self.ltk_key, self.irk_local_key, self.irk_remote_key, self.csrk_local_key, self.csrk_remote_key)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Prepairing Data')
        # --------------------------------------------------------------------------------------------------------------
        error_response = ChannelUtils.send(
            test_case=self,
            report=SetPrepairingDataRequest(PrepairingData.DataType.LOCAL_ADDRESS, self.device_address),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check data linked to this pairing sequence are discarded')
        # --------------------------------------------------------------------------------------------------------------
        # TODO :
        #  check no data in NVS

        self.testCaseChecked("ROT_RCV_PPA_0009")
    # end def test_prepairing_management_data_discarded_on_error

    def _test_set_key_sub_id_out_of_range(self, request):
        """
        Set key (with prepairing management Start) with SubId out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Sub Id significant values')
        # --------------------------------------------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send Set Key with Sub Id = {sub_id}')
            # ----------------------------------------------------------------------------------------------------------
            request.sub_id = sub_id
            error_response = ChannelUtils.send(
                test_case=self,
                report=request,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                int(Numeral(request.sub_id)),
                int(Numeral(request.address)),
                [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS, Hidpp1ErrorCodes.ERR_INVALID_SUBID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_set_key_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_set_ltk_key_sub_id_out_of_range(self):
        """
        0xE8 - Set LTK Key: SubId out of range (with prepairing management Start)
        """
        self._test_set_key_sub_id_out_of_range(SetLTKKeyRequest(self.ltk_key))
        self.testCaseChecked("ROT_RCV_PPA_0010")
    # end def test_set_ltk_key_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Robustness')
    def test_set_irk_key_local_sub_id_out_of_range(self):
        """
        0xE9 - Set IRK Key (Privacy) - Local : SubId out of range (with prepairing management Start)
        """
        self._test_set_key_sub_id_out_of_range(SetIRKKeyCentralRequest(self.irk_local_key))
        self.testCaseChecked("ROT_RCV_PPA_0011")
    # end def test_set_irk_key_local_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Robustness')
    def test_set_irk_key_remote_sub_id_out_of_range(self):
        """
        0xEA - Set IRK Key (Privacy) - Remote : SubId out of range (with prepairing management Start)
        """
        self._test_set_key_sub_id_out_of_range(SetIRKKeyPeripheralRequest(self.irk_remote_key))
        self.testCaseChecked("ROT_RCV_PPA_0012")
    # end def test_set_irk_key_remote_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Robustness')
    def test_set_csrk_key_local_sub_id_out_of_range(self):
        """
        0xEB - Set CSRK Key (Signature) - Local : SubId out of range (with prepairing management Start)
        """
        self._test_set_key_sub_id_out_of_range(SetCSRKKeyCentralRequest(self.csrk_local_key))
        self.testCaseChecked("ROT_RCV_PPA_0013")
    # end def test_set_csrk_key_local_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Robustness')
    def test_set_csrk_key_remote_sub_id_out_of_range(self):
        """
        0xEC - Set CSRK Key (Privacy) - Remote : SubId out of range (with prepairing management Start)
        """
        self._test_set_key_sub_id_out_of_range(SetCSRKKeyPeripheralRequest(self.csrk_remote_key))
        self.testCaseChecked("ROT_RCV_PPA_0014")
    # end def test_set_csrk_key_remote_sub_id_out_of_range

    def _test_set_key_device_index_out_of_range(self, request):
        """
        Set key (with prepairing management Start) with Device Index out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Device Index significant values')
        # --------------------------------------------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send Set Key with Device Index = {device_index}')
            # ----------------------------------------------------------------------------------------------------------
            request.device_index = device_index
            error_response = ChannelUtils.send(
                test_case=self,
                report=request,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                int(Numeral(request.sub_id)),
                int(Numeral(request.address)),
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
    # end def _test_set_key_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_set_ltk_key_device_index_out_of_range(self):
        """
        0xE8 - Set LTK Key: Device Index out of range (with prepairing management Start)
        """
        self._test_set_key_device_index_out_of_range(SetLTKKeyRequest(self.ltk_key))
        self.testCaseChecked("ROT_RCV_PPA_0015")
    # end def test_set_ltk_key_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Robustness')
    def test_set_irk_key_local_device_index_out_of_range(self):
        """
        0xE9 - Set IRK Key (Privacy) - Local : Device Index out of range (with prepairing management Start)
        """
        self._test_set_key_device_index_out_of_range(SetIRKKeyCentralRequest(self.irk_local_key))
        self.testCaseChecked("ROT_RCV_PPA_0016")
    # end def test_set_irk_key_local_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Robustness')
    def test_set_irk_key_remote_device_index_out_of_range(self):
        """
        0xEA - Set IRK Key (Privacy) - Remote : Device Index out of range (with prepairing management Start)
        """
        self._test_set_key_device_index_out_of_range(SetIRKKeyPeripheralRequest(self.irk_remote_key))
        self.testCaseChecked("ROT_RCV_PPA_0017")
    # end def test_set_irk_key_remote_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Robustness')
    def test_set_csrk_key_local_device_index_out_of_range(self):
        """
        0xEB - Set CSRK Key (Signature) - Local : Device Index out of range (with prepairing management Start)
        """
        self._test_set_key_device_index_out_of_range(SetCSRKKeyCentralRequest(self.csrk_local_key))
        self.testCaseChecked("ROT_RCV_PPA_0018")
    # end def test_set_csrk_key_local_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Robustness')
    def test_set_csrk_key_remote_device_index_out_of_range(self):
        """
        0xEC - Set CSRK Key (Privacy) - Remote : Device Index out of range (with prepairing management Start)
        """
        self._test_set_key_device_index_out_of_range(SetCSRKKeyPeripheralRequest(self.csrk_remote_key))
        self.testCaseChecked("ROT_RCV_PPA_0019")
    # end def test_set_csrk_key_remote_device_index_out_of_range

    def _test_set_key_without_prepairing_management_start(self, request):
        """
        Set key without prepairing management Start
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Set Key')
        # --------------------------------------------------------------------------------------------------------------
        error_response = ChannelUtils.send(
            test_case=self,
            report=request,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            int(Numeral(request.sub_id)),
            int(Numeral(request.address)),
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])
    # end def _test_set_key_without_prepairing_management_start

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_set_ltk_key_without_prepairing_management_start(self):
        """
        0xE8 - Set LTK Key: Without Prepairing Management Start
        """
        self._test_set_key_without_prepairing_management_start(SetLTKKeyRequest(self.ltk_key))
        self.testCaseChecked("ROT_RCV_PPA_0020")
    # end def test_set_ltk_key_without_prepairing_management_start

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Robustness')
    def test_set_irk_key_local_without_prepairing_management_start(self):
        """
        0xE9 - Set IRK Key (Privacy) - Local : Without Prepairing Management Start
        """
        self._test_set_key_without_prepairing_management_start(SetIRKKeyCentralRequest(self.irk_local_key))
        self.testCaseChecked("ROT_RCV_PPA_0021")
    # end def test_set_irk_key_local_without_prepairing_management_start

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Robustness')
    def test_set_irk_key_remote_without_prepairing_management_start(self):
        """
        0xEA - Set IRK Key (Privacy) - Remote : Without Prepairing Management Start
        """
        self._test_set_key_without_prepairing_management_start(SetIRKKeyPeripheralRequest(self.irk_remote_key))
        self.testCaseChecked("ROT_RCV_PPA_0022")
    # end def test_set_irk_key_remote_without_prepairing_management_start

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Robustness')
    def test_set_csrk_key_local_without_prepairing_management_start(self):
        """
        0xEB - Set CSRK Key (Signature) - Local : Without Prepairing Management Start
        """
        self._test_set_key_without_prepairing_management_start(SetCSRKKeyCentralRequest(self.csrk_local_key))
        self.testCaseChecked("ROT_RCV_PPA_0023")
    # end def test_set_csrk_key_local_without_prepairing_management_start

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Robustness')
    def test_set_csrk_key_remote_without_prepairing_management_start(self):
        """
        0xEC - Set CSRK Key (Privacy) - Remote : Without Prepairing Management Start
        """
        self._test_set_key_without_prepairing_management_start(SetCSRKKeyPeripheralRequest(self.csrk_remote_key))
        self.testCaseChecked("ROT_RCV_PPA_0024")
    # end def test_set_csrk_key_remote_without_prepairing_management_start

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_prepairing_data_sub_id_out_of_range(self):
        """
        Prepairing Data with SubId out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Sub Id significant values')
        # --------------------------------------------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send Prepairing Data with sub id {sub_id}')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_data_req = SetPrepairingDataRequest(PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)
            prepairing_data_req.sub_id = sub_id
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_data_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                sub_id,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
                [Hidpp1ErrorCodes.ERR_INVALID_SUBID, Hidpp1ErrorCodes.ERR_INVALID_ADDRESS])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0025")
    # end def test_prepairing_data_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_set_prepairing_data_device_index_out_of_range(self):
        """
        Set Prepairing Data with Device Index out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Device Index significant values')
        # --------------------------------------------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Set Prepairing Data')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_data_req = SetPrepairingDataRequest(PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)
            prepairing_data_req.device_index = device_index
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_data_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0026")
    # end def test_set_prepairing_data_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_get_prepairing_data_device_index_out_of_range(self):
        """
        Get Prepairing Data with Device Index out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Device Index significant values')
        # --------------------------------------------------------------------------------------------------------------
        device_index_values = compute_sup_values(self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots)
        device_index_values.remove(Hidpp1Data.DeviceIndex.TRANSCEIVER)
        device_index_values.append(Hidpp1Data.DeviceIndex.TRANSCEIVER - 1)
        for device_index in device_index_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Get Prepairing Data')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_data_req = GetPrepairingDataRequest(PrepairingData.DataType.LOCAL_ADDRESS)
            prepairing_data_req.device_index = device_index
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_data_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
                [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0027")
    # end def test_set_prepairing_data_device_index_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_set_prepairing_data_set_local_address(self):
        """
        Set Prepairing Data function with Data Type field set to Local Address should not be allowed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Set Prepairing Data')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_data_req = SetPrepairingDataRequest(PrepairingData.DataType.LOCAL_ADDRESS, self.device_address)
        error_response = ChannelUtils.send(
            test_case=self,
            report=prepairing_data_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0028")
    # end def test_set_prepairing_data_set_local_address

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_set_prepairing_data_data_type_out_of_range(self):
        """
        Set Prepairing Data with Data Type out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Device Index significant values')
        # --------------------------------------------------------------------------------------------------------------
        data_type_values = compute_sup_values(int(PrepairingData.DataType.REMOTE_ADDRESS))
        for data_type in data_type_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Set Prepairing Data')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_data_req = SetPrepairingDataRequest(data_type, self.device_address)
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_data_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0029")
    # end def test_set_prepairing_data_data_type_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_get_prepairing_data_data_type_out_of_range(self):
        """
        Get Prepairing Data with Data Type out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Device Index significant values')
        # --------------------------------------------------------------------------------------------------------------
        data_type_values = compute_sup_values(int(PrepairingData.DataType.REMOTE_ADDRESS))
        for data_type in data_type_values:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
            # ----------------------------------------------------------------------------------------------------------
            self.post_requisite_reset_receiver = True
            BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send Get Prepairing Data')
            # ----------------------------------------------------------------------------------------------------------
            prepairing_data_req = GetPrepairingDataRequest(data_type)
            error_response = ChannelUtils.send(
                test_case=self,
                report=prepairing_data_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
                Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
                [Hidpp1ErrorCodes.ERR_INVALID_PARAM_VALUE])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0030")
    # end def test_get_prepairing_data_data_type_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_get_prepairing_data_padding_ignored(self):
        """
        Check Read Prepairing Data padding is ignored
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over padding significant values')
        # --------------------------------------------------------------------------------------------------------------
        for r1 in compute_sup_values(HexList(Numeral(GetPrepairingDataRequest.DEFAULT.R1,
                                                     GetPrepairingDataRequest.LEN.R1 // 8))):
            for r2 in compute_sup_values(HexList(Numeral(GetPrepairingDataRequest.DEFAULT.R2,
                                                         GetPrepairingDataRequest.LEN.R2 // 8))):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
                # ------------------------------------------------------------------------------------------------------
                self.post_requisite_reset_receiver = True
                BleProReceiverPrepairingTestUtils.set_prepairing_management(
                    self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, 'Read Prepairing Data')
                # ------------------------------------------------------------------------------------------------------
                prepairing_data_req = GetPrepairingDataRequest(PrepairingData.DataType.LOCAL_ADDRESS)
                prepairing_data_req.r1 = r1
                prepairing_data_req.r2 = r2
                prepairing_data_resp = ChannelUtils.send(
                    test_case=self,
                    report=prepairing_data_req,
                    response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                    response_class_type=GetPrepairingDataResponse)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check Prepairing Data response')
                # ------------------------------------------------------------------------------------------------------
                BleProReceiverPrepairingTestUtils.GetPrepairingDataResponseChecker.check_fields(
                    self, prepairing_data_resp, GetPrepairingDataResponse)
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End For Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0031")
    # end def test_get_prepairing_data_padding_ignored

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_get_prepairing_data_without_prepairing_management_start(self):
        """
        Check Get Prepairing Data while the session is not yet started
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Prepairing Data - Local Address')
        # --------------------------------------------------------------------------------------------------------------
        error_response = ChannelUtils.send(
            test_case=self,
            report=GetPrepairingDataRequest(PrepairingData.DataType.LOCAL_ADDRESS),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0032")
    # end def test_get_prepairing_data_padding_ignored

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_get_prepairing_data_remote_address(self):
        """
        Get Prepairing Data request with the Data Type set to Remote Address should not be allowed
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Get Prepairing Data')
        # --------------------------------------------------------------------------------------------------------------
        error_response = ChannelUtils.send(
            test_case=self,
            report=GetPrepairingDataRequest(PrepairingData.DataType.REMOTE_ADDRESS),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            error_response,
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_DATA,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0033")
    # end def test_get_prepairing_data_remote_address

    @features('RcvBLEProPrepairing')
    @features('NoRcvBLEProIrkOptional')
    @level('Robustness')
    def test_prepairing_management_store_local_irk_missing(self):
        """
        0xE7 - Prepairing Management : The command will be rejected (ERR_REQUEST_UNAVAILABLE) if the mandatory fields
        are not present at Store step : Local IRK key missing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        set_prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_prepairing_management_resp, SetPrepairingManagementResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set keys except irk local key')
        # --------------------------------------------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.set_keys(
            self, ltk_key=self.ltk_key, irk_local_key=None, irk_remote_key=self.irk_remote_key,
            csrk_local_key=self.csrk_local_key, csrk_remote_key=self.csrk_remote_key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Prepairing Data')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Store')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_management_req = SetPrepairingManagementRequest(
            self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)

        ChannelUtils.send_only(test_case=self, report=prepairing_management_req)
        sleep(0.5)
        resp = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            class_type=SetPrepairingManagementResponse)
        err_resp = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR, class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no valid response is received')
        # --------------------------------------------------------------------------------------------------------------
        self.assertListEqual(resp, [], f'Set Prepairing Management request should not be accepted if IRK Keys not send')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp[0],
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0034")
    # end def test_prepairing_management_store_local_irk_missing

    @features('RcvBLEProPrepairing')
    @features('NoRcvBLEProIrkOptional')
    @level('Robustness')
    def test_prepairing_management_store_remote_irk_missing(self):
        """
        0xE7 - Prepairing Management : The command will be rejected (ERR_REQUEST_UNAVAILABLE) if the mandatory fields
        are not present at Store step : remote IRK key missing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Start')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reset_receiver = True
        set_prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_prepairing_management_resp, SetPrepairingManagementResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set keys except irk remote key')
        # --------------------------------------------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.set_keys(
            self, ltk_key=self.ltk_key, irk_local_key=self.irk_local_key, irk_remote_key=None,
            csrk_local_key=self.csrk_local_key, csrk_remote_key=self.csrk_remote_key)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Set Prepairing Data')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Prepairing Management Store')
        # --------------------------------------------------------------------------------------------------------------
        prepairing_management_req = SetPrepairingManagementRequest(
            self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)

        ChannelUtils.send_only(test_case=self, report=prepairing_management_req)
        sleep(0.5)
        resp = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            class_type=SetPrepairingManagementResponse)
        err_resp = ChannelUtils.clean_messages(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR, class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check no valid response is received')
        # --------------------------------------------------------------------------------------------------------------
        self.assertListEqual(resp, [], f'Set Prepairing Management request should not be accepted if IRK Keys not send')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check error response')
        # --------------------------------------------------------------------------------------------------------------
        CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
            self,
            err_resp[0],
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            Hidpp1Data.Hidpp1RegisterAddress.PREPAIRING_MANAGEMENT,
            [Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE])

        self.testCaseChecked("ROT_RCV_PPA_0035")
    # end def test_prepairing_management_store_remote_irk_missing

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_random_data_sub_id_out_of_range(self):
        """
        0xF6 - Random Data : SubId out of range
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Test Loop over Sub Id significant values')
        # --------------------------------------------------------------------------------------------------------------
        for sub_id in [Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.SET_VERY_LONG_REGISTER,
                       Hidpp1Data.Hidpp1RegisterSubId.GET_VERY_LONG_REGISTER]:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Send Random Data with Sub Id = {sub_id}')
            # ----------------------------------------------------------------------------------------------------------
            request = GetRandomDataRequest()
            request.sub_id = sub_id
            error_response = ChannelUtils.send(
                test_case=self,
                report=request,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error response')
            # ----------------------------------------------------------------------------------------------------------
            CommonBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                self,
                error_response,
                int(Numeral(request.sub_id)),
                int(Numeral(request.address)),
                [Hidpp1ErrorCodes.ERR_INVALID_ADDRESS, Hidpp1ErrorCodes.ERR_INVALID_SUBID])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'End Test Loop')
        # --------------------------------------------------------------------------------------------------------------
        self.testCaseChecked("ROT_RCV_PPA_0036")
    # end def test_random_data_sub_id_out_of_range

    @features('RcvBLEProPrepairing')
    @level('Robustness')
    def test_incomplete_prepairing_slot(self):
        """
        Complete the receiver pre-pairing sequence:
         - validate an empty Device Connection notification is returned on a fake device arrival request
         - verify the 0x0A error code returned on 0xB5 0x5n and 0xB5 0x6n requests
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Clean-up receiver pairing slot')
        # --------------------------------------------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Re-enable HID++ reporting')
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.set_hidpp_reporting(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
        # --------------------------------------------------------------------------------------------------------------
        error_response = ChannelUtils.send(
            test_case=self,
            report=GetBLEProDevicePairingInfoRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + self.prepairing_slot - 1),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate an error is returned with error code ERR_UNKNOWN_DEVICE')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)), expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                         msg='Reading an unused Pairing slot should raise an error with code ERR_UNKNOWN_DEVICE.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read BLE Pro device name request')
        # --------------------------------------------------------------------------------------------------------------
        device_pairing_info_req = GetBLEProDeviceDeviceNameRequest(
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + self.prepairing_slot - 1)
        error_response = ChannelUtils.send(
            test_case=self,
            report=device_pairing_info_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Error message is received with error code ERR_UNKNOWN_DEVICE')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)), expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                         msg='Reading an unused Pairing slot should raise an error with code ERR_UNKNOWN_DEVICE.')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Run Pre Pairing sequence on Receiver')
        # --------------------------------------------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(
            self, self.prepairing_slot, self.ltk_key, self.irk_local_key, self.irk_remote_key, self.csrk_local_key,
            self.csrk_remote_key, self.device_address, force_random_data=True)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        ChannelUtils.send(
            test_case=self,
            report=set_register,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetConnectionStateResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Empty Device Connection notification is received')
        # --------------------------------------------------------------------------------------------------------------
        device_connection = ChannelUtils.get_only(
            test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=DeviceConnection, 
            check_first_message=False, allow_no_message=True)
        self.assertIsNotNone(obj=device_connection,
                             msg='DeviceConnection notifications shall have been received')
        while device_connection is not None:
            if self.prepairing_slot == int(Numeral(device_connection.device_index)):
                device_info = BLEProReceiverInformation.fromHexList(HexList(device_connection.information))
                self.assertTrue(to_int(device_connection.protocol_type) == 0, msg='Protocol type shall be null')
                self.assertTrue(to_int(device_info.bluetooth_pid_lsb) == 0, msg='Bluetooth PID LSB shall be null')
                self.assertTrue(to_int(device_info.bluetooth_pid_msb) == 0, msg='Bluetooth PID LSB shall be null')
                self.assertTrue(to_int(device_info.device_info_link_status) ==
                                DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                                msg='Device Info Link Status shall be set to not established')
                self.assertTrue(to_int(device_info.device_info_device_type) == 0,
                                msg='Device Info Device Type shall be null')
            # end if
            device_connection = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=DeviceConnection, check_first_message=False, allow_no_message=True)
        # end while

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
        # --------------------------------------------------------------------------------------------------------------
        error_response = ChannelUtils.send(
            test_case=self,
            report=GetBLEProDevicePairingInfoRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + self.prepairing_slot - 1),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate an error is returned with error code ERR_REQUEST_UNAVAILABLE')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE,
                         msg='''Reading an ?incomplete (Prepaired) / corrupted? Pairing slot should raise an error 
                                 with error code ERR_REQUEST_UNAVAILABLE.''')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send Read BLE Pro device name request')
        # --------------------------------------------------------------------------------------------------------------
        device_pairing_info_req = GetBLEProDeviceDeviceNameRequest(
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + self.prepairing_slot - 1)
        error_response = ChannelUtils.send(
            test_case=self,
            report=device_pairing_info_req,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
            response_class_type=Hidpp1ErrorCodes)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate Error message is received with code ERR_REQUEST_UNAVAILABLE')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE,
                         msg='Reading an unused Pairing slot should raise an error with code ERR_REQUEST_UNAVAILABLE.')

        self.testCaseChecked("ROT_RCV_PPA_0037")
    # end def test_incomplete_prepairing_slot

# end class PrepairingRobustnessTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
