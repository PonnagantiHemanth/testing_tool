#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.receiver.tde.prepairing_functionality
:brief: Validates BLE Pro Receiver Prepairing Functionality
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/06/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hidpp.hidpp1.registers.prepairingdata import GetPrepairingDataRequest
from pyhid.hidpp.hidpp1.registers.prepairingdata import GetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingdata import PrepairingData
from pyhid.hidpp.hidpp1.registers.prepairingdata import SetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import PrepairingManagement
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementResponse
from pyhid.hidpp.hidpp1.registers.randomdata import GetRandomDataResponse
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralRequest
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralResponse
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralRequest
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralResponse
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralRequest
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralResponse
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralRequest
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralResponse
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyRequest
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.hexlist import HexList
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.receiver.tde.prepairing import PrepairingTestCase
from pytestbox.shared.base.bleproreceiverprepairingutils import BleProReceiverPrepairingTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PrepairingFunctionalityTestCase(PrepairingTestCase):
    """
    Prepairing TestCases
    """
    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_receiver_prepairing_sequence_business_case(self):
        """
        BLE Pro - Pairing/Prepairing: Receiver Prepairing sequence

        Sequence Diagram:
            TDE -> Receiver : Test Mode Control - Enable Manufacturing Test Mode
            TDE -> Receiver : Prepairing Data Management - Slot 1 - Start
            TDE -> Receiver : Get Random Data
            TDE -> Receiver : Set LTK Key
            TDE -> Receiver : Get Random Data
            TDE -> Receiver : Set IRK Key - Local
            TDE -> Receiver : Get Random Data
            TDE -> Receiver : Set IRK Key - Remote
            TDE -> Receiver : Get Random Data
            TDE -> Receiver : Set CSRK Key - Local
            TDE -> Receiver : Get Random Data
            TDE -> Receiver : Set CSRK Key - Remote
            TDE -> Receiver : Prepairing Data - Remote - Device Address (Use Test Address)
            TDE -> Receiver : Prepairing Data Management - Slot 1 - Store
            TDE -> Receiver : Test Mode Control - Disable Test Mode
        """
        ReceiverTestUtils.HIDppHelper.activate_features(self, manufacturing=True)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Set LTK Key with a randomized key retrieved by the 0xF6 register')
        # ---------------------------------------------------------------------------
        randomized_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
        set_ltk_key_resp = self.send_report_wait_response(
            report=SetLTKKeyRequest(randomized_key),
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetLTKKeyResponse
        )

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check Set LTK Key response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(self, set_ltk_key_resp, SetLTKKeyResponse, {})

        if self.f.RECEIVER.TDE.F_IRK:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 3: Set IRK Local Key with a randomized key retrieved by the 0xF6 register')
            # ---------------------------------------------------------------------------
            randomized_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
            set_irk_local_key_resp = self.send_report_wait_response(
                report=SetIRKKeyCentralRequest(randomized_key),
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetIRKKeyCentralResponse
            )

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 3: Check Set IRK Key - Local response')
            # ---------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, set_irk_local_key_resp, SetIRKKeyCentralResponse, {})

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 4: Set IRK Remote Key with a randomized key retrieved by the 0xF6 register')
            # ---------------------------------------------------------------------------
            randomized_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
            set_irk_remote_key_resp = self.send_report_wait_response(
                report=SetIRKKeyPeripheralRequest(randomized_key),
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetIRKKeyPeripheralResponse
            )

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 4: Check Set IRK Key - Remote response')
            # ---------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, set_irk_remote_key_resp, SetIRKKeyPeripheralResponse, {})

        if self.f.RECEIVER.TDE.F_CSRK:
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 5: Set CSRK Local Key with a randomized key retrieved by the 0xF6 register')
            # ---------------------------------------------------------------------------
            randomized_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
            set_csrk_local_key_resp = self.send_report_wait_response(
                report=SetCSRKKeyCentralRequest(randomized_key),
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetCSRKKeyCentralResponse
            )

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 5: Check Set CSRK Key - Local response')
            # ---------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, set_csrk_local_key_resp, SetCSRKKeyCentralResponse, {})

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 6: Set CSRK Remote Key with a randomized key retrieved by the 0xF6 register')
            # ---------------------------------------------------------------------------
            randomized_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
            set_csrk_remote_key_resp = self.send_report_wait_response(
                report=SetCSRKKeyPeripheralRequest(randomized_key),
                response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetCSRKKeyPeripheralResponse
            )

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 6: Check Set CSRK Key - Remote response')
            # ---------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, set_csrk_remote_key_resp, SetCSRKKeyPeripheralResponse, {})
        # end if

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 7: Prepairing Data - Remote - Device Address')
        # ---------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 7: Check Prepairing Data response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 8: Prepairing Data Management - Slot {self.prepairing_slot} - Store')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 8: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        TDETestUtils.set_test_mode_control(self, TestModeControl.TestModeEnable.DISABLE_TEST_MODE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 9: Check Prepairing Data in NVS')
        # ---------------------------------------------------------------------------
        # TODO : check data in NVS

        self.testCaseChecked("FNT_RCV_PPA_0001")
    # end def test_receiver_prepairing_sequence_business_case

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_prepairing_management_api(self):
        """
        0xE7 - Prepairing Management : API validation
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 1: Prepairing Data Management - Slot 1 - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        self.testCaseChecked("FNT_RCV_PPA_0002")
    # end def test_prepairing_management_api

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_prepairing_management_pairing_slots(self):
        """
        0xE7 - Prepairing Management for each pairing slot in valid range
        """
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over Pairing Slot values')
        # ---------------------------------------------------------------------------
        for pairing_slot in range(1, self.f.RECEIVER.ENUMERATION.F_Number_Of_Pairing_Slots):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {pairing_slot} - Start')
            # ---------------------------------------------------------------------------
            prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
                self, pairing_slot, PrepairingManagement.PrepairingManagementControl.START)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check Prepairing Data Management response')
            # ---------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
                self, prepairing_management_resp, SetPrepairingManagementResponse, {})
        # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------
        self.testCaseChecked("FNT_RCV_PPA_0003")
    # end def test_prepairing_management_pairing_slots

    def _test_set_key(self, request, expected_resp_cls):
        """
        Set key API validation (with prepairing management Start)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Set Key')
        # ---------------------------------------------------------------------------
        set_key_resp = self.send_report_wait_response(
            report=request,
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=expected_resp_cls
        )

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Set Key response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(self, set_key_resp, expected_resp_cls, {})
    # end def _test_set_key

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_set_ltk_key_api(self):
        """
        0xE8 - Set LTK Key: API Validation (with prepairing management Start)
        """
        self._test_set_key(SetLTKKeyRequest(self.ltk_key), SetLTKKeyResponse)
        self.testCaseChecked("FNT_RCV_PPA_0004")
    # end def test_set_ltk_key_api

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Functionality')
    def test_set_irk_key_local_api(self):
        """
        0xE9 - Set IRK Key (Privacy) - Local : API Validation (with prepairing management Start)
        """
        self._test_set_key(SetIRKKeyCentralRequest(self.irk_local_key), SetIRKKeyCentralResponse)
        self.testCaseChecked("FNT_RCV_PPA_0005")
    # end def test_set_irk_key_local_api

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIRK')
    @level('Functionality')
    def test_set_irk_key_remote_api(self):
        """
        0xEA - Set IRK Key (Privacy) - Remote : API Validation (with prepairing management Start)
        """
        self._test_set_key(SetIRKKeyPeripheralRequest(self.irk_remote_key), SetIRKKeyPeripheralResponse)
        self.testCaseChecked("FNT_RCV_PPA_0006")
    # end def test_set_irk_key_remote_api

    # TODO : test @features('NoRcvBLEProIRK')

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Functionality')
    def test_set_csrk_key_local_api(self):
        """
        0xEB - Set CSRK Key (Signature) - Local : API Validation (with prepairing management Start)
        """
        self._test_set_key(SetCSRKKeyCentralRequest(self.csrk_local_key), SetCSRKKeyCentralResponse)
        self.testCaseChecked("FNT_RCV_PPA_0007")
    # end def test_set_csrk_key_local_api

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProCSRK')
    @level('Functionality')
    def test_set_csrk_key_remote_api(self):
        """
        0xEC - Set CSRK Key (Privacy) - Remote : API Validation (with prepairing management Start)
        """
        self._test_set_key(SetCSRKKeyPeripheralRequest(self.csrk_remote_key), SetCSRKKeyPeripheralResponse)
        self.testCaseChecked("FNT_RCV_PPA_0008")
    # end def test_set_csrk_key_remote_api

    # TODO : test @features('NoRcvBLEProCSRK')

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_prepairing_management_delete(self):
        """
        Check Prepairing Management Control field Prepairing Management command can be set to Delete
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Delete')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.DELETE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check Prepairing data are deleted in NVS')
        # ---------------------------------------------------------------------------
        # TODO : check data deleted in NVS

        self.testCaseChecked("FNT_RCV_PPA_0009")
    # end def test_prepairing_management_delete

    @features('RcvBLEProPrepairing')
    @features('NoRcvBLEProIrkOptional')
    @level('Functionality')
    def test_receiver_prepairing_sequence_mandatory_fields_only(self):
        """
        BLE Pro - Pairing/Prepairing: Receiver Prepairing sequence (mandatory fields only)

        Sequence Diagram:
            TDE -> Receiver : Prepairing Data Management - Slot 1 - Start
            TDE -> Receiver : Set LTK Key
            TDE -> Receiver : Prepairing Data - Remote - Device Address (Use Test Address)
            TDE -> Receiver : Set IRK Key - Local
            TDE -> Receiver : Set IRK Key - Remote
            TDE -> Receiver : Prepairing Data Management - Slot 1 - Store
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Set LTK Key')
        # ---------------------------------------------------------------------------
        set_ltk_key_resp = self.send_report_wait_response( report=SetLTKKeyRequest(self.ltk_key),
            response_queue=self.hidDispatcher.receiver_response_queue, response_class_type=SetLTKKeyResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check Set LTK Key response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(self, set_ltk_key_resp, SetLTKKeyResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Set IRK Key - Local')
        # ---------------------------------------------------------------------------
        set_irk_local_key_resp = self.send_report_wait_response(report=SetIRKKeyCentralRequest(self.irk_local_key),
            response_queue=self.hidDispatcher.receiver_response_queue, response_class_type=SetIRKKeyCentralResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check Set IRK Key - Local response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_irk_local_key_resp, SetIRKKeyCentralResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 4: Set IRK Key - Remote')
        # ---------------------------------------------------------------------------
        set_irk_remote_key_resp = self.send_report_wait_response(report=SetIRKKeyPeripheralRequest(self.irk_remote_key),
            response_queue=self.hidDispatcher.receiver_response_queue, response_class_type=SetIRKKeyPeripheralResponse)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Check Set IRK Key - Remote response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, set_irk_remote_key_resp, SetIRKKeyPeripheralResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 5: Prepairing Data - Remote - Device Address')
        # ---------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 5: Check Prepairing Data response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 6: Prepairing Data Management - Slot {self.prepairing_slot} - Store')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 6: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 7: Check Data in NVS')
        # ---------------------------------------------------------------------------
        # TODO : check data in NVS

        self.testCaseChecked("FNT_RCV_PPA_0010")
    # end def test_receiver_prepairing_sequence_mandatory_fields_only

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIrkOptional')
    @level('Functionality')
    def test_receiver_prepairing_sequence_mandatory_fields_only_no_irk(self):
        """
        BLE Pro - Pairing/Prepairing: Receiver Prepairing sequence (mandatory fields only)

        Sequence Diagram:
            TDE -> Receiver : Prepairing Data Management - Slot 1 - Start
            TDE -> Receiver : Set LTK Key
            TDE -> Receiver : Prepairing Data - Remote - Device Address (Use Test Address)
            TDE -> Receiver : Prepairing Data Management - Slot 1 - Store
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Set LTK Key')
        # ---------------------------------------------------------------------------
        set_ltk_key_resp = self.send_report_wait_response(
            report=SetLTKKeyRequest(self.ltk_key),
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=SetLTKKeyResponse
        )

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check Set LTK Key response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(self, set_ltk_key_resp, SetLTKKeyResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 3: Prepairing Data - Remote - Device Address')
        # ---------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 3: Check Prepairing Data response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 4: Prepairing Data Management - Slot {self.prepairing_slot} - Store')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 4: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 5: Check Data in NVS')
        # ---------------------------------------------------------------------------
        # TODO : check data in NVS

        self.testCaseChecked("FNT_RCV_PPA_0010")
    # end def test_receiver_prepairing_sequence_mandatory_fields_only_no_irk

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_pairing_data_virtually_erased_at_start(self):
        """
        0xE7 - Prepairing Management : No partial update supported : At the reception of the "Start", the pairing
        data for the given slot are virtually erased
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Run Receiver Prepairing Sequence')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       self.ltk_key,
                                                                       self.irk_local_key,
                                                                       self.irk_remote_key,
                                                                       self.csrk_local_key,
                                                                       self.csrk_remote_key,
                                                                       self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check data erased')
        # ---------------------------------------------------------------------------
        # TODO : check : no data in NVS

        self.testCaseChecked("FNT_RCV_PPA_0011")
    # end def test_pairing_data_virtually_erased_at_start

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_pairing_data_replaced(self):
        """
        0xE7 - Prepairing Management : No partial update supported : In case of successful sequence, the pairing data
        are replaced
        """
        new_device_address = HexList('A5A5A5A5A5A5')
        new_ltk_key = HexList('5F5E5D5C5B5A59585756555453525150')
        new_irk_local_key = HexList('6F6E6D6C6B6A69686766656463626160')
        new_irk_remote_key = HexList('7F7E7D7C7B7A79787776757473727170')
        new_csrk_local_key = HexList('8F8E8D8C8B8A89888786858483828180')
        new_csrk_remote_key = HexList('9F9E9D9C9B9A99989796959493929190')

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Run Receiver Prepairing Sequence')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       self.ltk_key,
                                                                       self.irk_local_key,
                                                                       self.irk_remote_key,
                                                                       self.csrk_local_key,
                                                                       self.csrk_remote_key,
                                                                       self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Run new Receiver Prepairing Sequence with new values')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       new_ltk_key,
                                                                       new_irk_local_key,
                                                                       new_irk_remote_key,
                                                                       new_csrk_local_key,
                                                                       new_csrk_remote_key,
                                                                       new_device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Check data are replaced')
        # ---------------------------------------------------------------------------
        #  TODO : check : data in NVS are replaced

        self.testCaseChecked("FNT_RCV_PPA_0012")
    # end def test_pairing_data_replaced

    @features('RcvBLEProPrepairing')
    @features('NoRcvBLEProIrkOptional')
    @level('Functionality')
    def test_pairing_data_replaced_mandatory_fields_only(self):
        """
        0xE7 - Prepairing Management : No partial update supported : In case of successful sequence with mandatory
        fields only, the pairing data are replaced
        """
        new_device_address = HexList('A5A5A5A5A5A5')
        new_ltk_key = HexList('5F5E5D5C5B5A59585756555453525150')
        new_irk_local_key = HexList('6F6E6D6C6B6A69686766656463626160')
        new_irk_remote_key = HexList('7F7E7D7C7B7A79787776757473727170')

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Run Receiver Prepairing Sequence')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       self.ltk_key,
                                                                       self.irk_local_key,
                                                                       self.irk_remote_key,
                                                                       self.csrk_local_key,
                                                                       self.csrk_remote_key,
                                                                       self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Run new Receiver Prepairing Sequence (mandatory fields only) with new values')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       new_ltk_key,
                                                                       new_irk_local_key,
                                                                       new_irk_remote_key,
                                                                       device_address=new_device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Check data are replaced and optional fields are deleted')
        # ---------------------------------------------------------------------------
        #  TODO : check : data in NVS are replaced (optional fields are deleted [TBC])

        self.testCaseChecked("FNT_RCV_PPA_0013")
    # end def test_pairing_data_replaced_mandatory_fields_only

    @features('RcvBLEProPrepairing')
    @features('RcvBLEProIrkOptional')
    @level('Functionality')
    def test_pairing_data_replaced_mandatory_fields_only_no_irk(self):
        """
        0xE7 - Prepairing Management : No partial update supported : In case of successful sequence with mandatory
        fields only, the pairing data are replaced
        """
        new_device_address = HexList('A5A5A5A5A5A5')
        new_ltk_key = HexList('5F5E5D5C5B5A59585756555453525150')

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Run Receiver Prepairing Sequence')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       self.ltk_key,
                                                                       self.irk_local_key,
                                                                       self.irk_remote_key,
                                                                       self.csrk_local_key,
                                                                       self.csrk_remote_key,
                                                                       self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Run new Receiver Prepairing Sequence (mandatory fields only) with new values')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(self,
                                                                       self.prepairing_slot,
                                                                       new_ltk_key,
                                                                       device_address=new_device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 1: Check data are replaced and optional fields are deleted')
        # ---------------------------------------------------------------------------
        #  TODO : check : data in NVS are replaced (optional fields are deleted [TBC])

        self.testCaseChecked("FNT_RCV_PPA_0013")
    # end def test_pairing_data_replaced_mandatory_fields_only_no_irk

    @features('RcvBLEProPrepairing')
    @level('Functionality')
    def test_new_local_address_at_start(self):
        """
        0xE7 - Prepairing Management : At the reception of the Start, a new local bluetooth address is generated
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Get initial Local Address')
        # ---------------------------------------------------------------------------
        # TODO : get initial local ble address in NVS

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 2: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 2: Check new local BLE address is set')
        # ---------------------------------------------------------------------------
        # TODO : check : new local ble address in NVS

        self.testCaseChecked("FNT_RCV_PPA_0014")
    # end def test_new_local_address_at_start

    @features('RcvBLEProPrepairing')
    @level('Interface')
    def test_write_prepairing_data_api(self):
        """
        0xED - Prepairing Data : API validation (Write)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Prepairing Data - Remote - Device Address')
        # ---------------------------------------------------------------------------
        prepairing_data_resp = BleProReceiverPrepairingTestUtils.set_prepairing_data(
            self, PrepairingData.DataType.REMOTE_ADDRESS, self.device_address)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check Prepairing Data response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_data_resp, SetPrepairingDataResponse, {})

        self.testCaseChecked("FNT_RCV_PPA_0015")
    # end def test_write_prepairing_data_api

    @features('RcvBLEProPrepairing')
    @level('Interface')
    def test_read_prepairing_data_api(self):
        """
        0xED - Prepairing Data : API validation (Read)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Prepairing Data Management - Slot {self.prepairing_slot} - Start')
        # ---------------------------------------------------------------------------
        prepairing_management_resp = BleProReceiverPrepairingTestUtils.set_prepairing_management(
            self, self.prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Prepairing Data Management response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.MessageChecker.check_fields(
            self, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Prepairing Data - Local Address')
        # ---------------------------------------------------------------------------
        prepairing_data_resp = self.send_report_wait_response(
            report=GetPrepairingDataRequest(PrepairingData.DataType.LOCAL_ADDRESS),
            response_queue=self.hidDispatcher.receiver_response_queue,
            response_class_type=GetPrepairingDataResponse
        )

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 2: Check Prepairing Data response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.GetPrepairingDataResponseChecker.check_fields(
            self, prepairing_data_resp, GetPrepairingDataResponse)

        self.testCaseChecked("FNT_RCV_PPA_0016")
    # end def test_read_prepairing_data_api

    @features('RcvBLEProPrepairing')
    @level('Interface')
    def test_get_random_data_api(self):
        """
        0xF6 - Random Data : API validation (Read)
        """
        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Step 1: Send Random Data request')
        # ---------------------------------------------------------------------------
        random_data_resp = BleProReceiverPrepairingTestUtils.get_random_data(self)

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Check 1: Check Random Data response')
        # ---------------------------------------------------------------------------
        BleProReceiverPrepairingTestUtils.GetRandomDataResponseChecker.check_fields(
            self, random_data_resp, GetRandomDataResponse)

        self.testCaseChecked("FNT_RCV_PPA_0017")
    # end def test_get_random_data_api

    @features('RcvBLEProPrepairing')
    @level('Security')
    def test_get_random_data_entropy(self):
        """
        Random Data High-quality entropy verification
        """
        COUNT = 16
        unique_keys = [[]] * COUNT

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Loop {COUNT} times')
        # ---------------------------------------------------------------------------
        for i in range(len(unique_keys)):
            # ---------------------------------------------------------------------------
            self.logTitle2('Test Step 1: Send Random Data request')
            # ---------------------------------------------------------------------------
            randomized_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Compare the new key with the previous ones (at least 1 out of the 16 '
                           'bytes shall be different)')
            # ---------------------------------------------------------------------------
            if i > 0:
                self.assertTrue(expr=(randomized_key not in unique_keys),
                                msg="The random key is already in the list")
            # end if
            unique_keys[i] = randomized_key
            # end for
        # ---------------------------------------------------------------------------
        self.logTitle2('End Test Loop')
        # ---------------------------------------------------------------------------

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 2: Compare the {COUNT} received numbers and validate each byte value had changed '
                       'at least once.')
        # ---------------------------------------------------------------------------
        results = [False] * 16
        for z in range(len(results)):
            for i in range(len(unique_keys)):
                for j in range(i + 1, len(unique_keys)):
                    if unique_keys[i][z] != unique_keys[j][z]:
                        results[z] = True
                        break
                    # end if
                # end for
                if results[z]:
                    break
                # end if
            # end for
        # end for

        self.assertEqual(obtained=results,
                         expected=[True] * 16,
                         msg="Some bytes never changes")

        # ---------------------------------------------------------------------------
        self.logTitle2(f'Test Check 3: Compare the {COUNT} received numbers and validate each bit had changed '
                       'at least once.')
        # ---------------------------------------------------------------------------
        results = [False] * 128
        for z in range(len(results)):
            for i in range(len(unique_keys)):
                for j in range(i + 1, len(unique_keys)):
                    if unique_keys[i].testBit(z) != unique_keys[j].testBit(z):
                        results[z] = True
                        break
                    # end if
                # end for
                if results[z]:
                    break
                # end if
            # end for
        # end for

        self.assertEqual(obtained=results,
                         expected=[True] * 128,
                         msg="Some bits never changes")

        self.testCaseChecked("FNT_RCV_PPA_0018")
    # end def test_get_random_data_entropy
# end class PrepairingFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
