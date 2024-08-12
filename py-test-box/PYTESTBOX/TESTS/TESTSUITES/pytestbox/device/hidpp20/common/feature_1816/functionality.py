#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.functionality
:brief: HID++ 2.0 BLEPro pre-pairing functionality test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/22
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.oobstate import OobStateFactory
from pyhid.hidpp.features.error import ErrorCodes
from pylibrary.mcu.nrf52.bleproprepairingchunk import BleProPrePairingNvsChunk
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.util import UtilNonNumericEnum
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pytestbox.device.hidpp20.common.feature_1816.bleproprepaing import BleProPrePairingTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
_AUTHOR = "Christophe Roquebert"


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BleProPrePairingFunctionalityTestCase(BleProPrePairingTestCase):
    """
    Validate Device BLE Pro pre-pairing functionality TestCases
    """

    @features('Feature1816')
    @level('Functionality')
    def test_prepairing_delete(self):
        """
        Delete the device prepairing data on slot 0
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send prepairing_data_management with prepairing_slot=0 and prepairing_management_control='Delete'")
        # ---------------------------------------------------------------------------
        prepairing_data_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.DELETE)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for prepairing_data_management acknowledgement")
        # ----------------------------------------------------------------------------
        prepairing_data_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_data_management, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.prepairing_data_management_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, prepairing_data_management_response, self.feature_1816.prepairing_data_management_response_cls)

        self.testCaseChecked("FUN_1816_0001")
    # end def test_prepairing_delete

    @features('Feature1816')
    @features('Feature1805')
    @level('Functionality')
    @services('Debugger')
    def test_prepairing_persistence_oob(self):
        """
        Check the pre-pairing data have been preserved after a OOB reset
        """
        self.post_requisite_program_nvs = True
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Roll out the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        initial_local_address = BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Send Root.GetFeature(0x1805)")
        # ---------------------------------------------------------------------------
        feature_1805_index = ChannelUtils.update_feature_mapping(test_case=self, feature_id=OobState.FEATURE_ID)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Retrieve the Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self, backup=True)
        initial_remote_address = pre_pairing_chunk.keys.remote_address

        # Get the 0x1805 feature
        feature_1805 = OobStateFactory.create(
            self.config_manager.get_feature_version(self.f.PRODUCT.FEATURES.COMMON.OOB_STATE))
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Force device in OOB state")
        # ---------------------------------------------------------------------------
        set_oob_state = feature_1805.set_oob_state_cls(device_index=ChannelUtils.get_device_index(test_case=self),
                                                       feature_index=feature_1805_index)
        ChannelUtils.send(test_case=self, report=set_oob_state, response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=feature_1805.set_oob_state_response_cls)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Retrieve the Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertNotNone(pre_pairing_chunk, msg="OobState request shall not erase the BLE Pro pre-pairing chunk")
        current_remote_address = pre_pairing_chunk.keys.remote_address

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current Remote addresses match")
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=initial_remote_address,
                         obtained=current_remote_address,
                         msg='The current Remote address differs from the initial one')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current Local addresses match")
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=initial_local_address,
                         obtained=pre_pairing_chunk.keys.local_address,
                         msg='The current Local address differs from the initial one')

        self.testCaseChecked("FUN_1816_0002")
    # end def test_prepairing_persistence_oob

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_prepairing_replacement(self):
        """
        Replace the PrePairing slot0 data: Relaunch the pre-pairing sequence on an already paired slot0
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, "Roll out the Device Pre-pairing sequence to retrieve the initial Local address")
        # ---------------------------------------------------------------------------
        initial_local_address = BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence a second time")
        # ---------------------------------------------------------------------------
        current_local_address = BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Retrieve the current Local address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the new Local address has been stored")
        # ----------------------------------------------------------------------------
        self.assertEqual(expected=current_local_address,
                         obtained=pre_pairing_chunk.keys.local_address,
                         msg='The current Local address differs from the initial one')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and current Local addresses differ")
        # ----------------------------------------------------------------------------
        self.assertNotEqual(unexpected=initial_local_address,
                            obtained=current_local_address,
                            msg='The current Local address shall differ from the initial one')

        self.testCaseChecked("FUN_1816_0003")
    # end def test_prepairing_replacement

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_prepairing_storing(self):
        """
        Replace the PrePairing slot0 data: Relaunch the pre-pairing sequence on an already paired slot0
        """
        ltk_key, irk_remote_key, irk_local_key, csrk_remote_key, csrk_local_key = \
            BleProPrePairingTestUtils.generate_keys_prepairing(test_case=self, feature_1816=self.feature_1816)
        receiver_address = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, "Roll out the Device Pre-pairing sequence to retrieve the initial Local address")
        # ---------------------------------------------------------------------------
        initial_local_address = BleProPrePairingTestUtils.pre_pairing_sequence(
            self, self.feature_1816, self.feature_1816_index, long_term_key=ltk_key,
            remote_identity_resolving_key=irk_remote_key, local_identity_resolving_key=irk_local_key,
            remote_connection_signature_resolving_key=csrk_remote_key,
            local_connection_signature_resolving_key=csrk_local_key,
            receiver_address=receiver_address)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Roll out the Device Pre-pairing sequence a second time except the last 'Store' request")
        # ---------------------------------------------------------------------------
        returned_local_address = BleProPrePairingTestUtils.pre_pairing_sequence(
            self, self.feature_1816, self.feature_1816_index, long_term_key=ltk_key,
            remote_identity_resolving_key=irk_remote_key, local_identity_resolving_key=irk_local_key,
            remote_connection_signature_resolving_key=csrk_remote_key,
            local_connection_signature_resolving_key=csrk_local_key,
            receiver_address=receiver_address, store=False)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify initial and returned Local addresses differ")
        # ----------------------------------------------------------------------------
        self.assertNotEqual(unexpected=initial_local_address,
                            obtained=returned_local_address,
                            msg='The returned Local address shall differ from the initial one')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Verify the new Local address has NOT been stored")
        # ----------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertNotEqual(unexpected=returned_local_address,
                            obtained=pre_pairing_chunk.keys.local_address,
                            msg='The current Local address shall differ from the returned one')

        self.testCaseChecked("FUN_1816_0004")
    # end def test_prepairing_storing

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def _test_remote_address_consistency(self):
        """
        ! Deprecated ! Check the remote addresses from the set and get functions are matching.
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data with data_type='Remote' and a fixed remote_address value")
        # ---------------------------------------------------------------------------
        remote_address = HexList("66" * (self.feature_1816.set_prepairing_data_cls.LEN.ADDRESS // 8))
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_prepairing_data acknowledgement")
        # ----------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_end_sequence(self, self.feature_1816, self.feature_1816_index,
                                                           receiver_address=remote_address, store=False)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=remote_address,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0005")
    # end def test_remote_address_consistency

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_key_boundary_values(self):
        """
        Check all key values are allowed testing boundaries (0x00 * 16 bytes ; 0xFF * 16 bytes) and a randomly
        chosen one.
        """
        min_address_value, max_address_value = BleProPrePairingTestUtils.get_range_random_static_address(test_case=self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence with all keys = 0x00 * 16 bytes")
        # ---------------------------------------------------------------------------
        min_key_value = HexList("00" * (self.feature_1816.set_ltk_cls.LEN.KEY // 8))
        BleProPrePairingTestUtils.pre_pairing_sequence(
            self, self.feature_1816, self.feature_1816_index, long_term_key=min_key_value,
            remote_identity_resolving_key=min_key_value, local_identity_resolving_key=min_key_value,
            remote_connection_signature_resolving_key=min_key_value,
            local_connection_signature_resolving_key=min_key_value, receiver_address=min_address_value)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check lowest possible values in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------
        BleProPrePairingTestUtils.NvsHelper.check_device_pre_pairing_data(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence with all keys = 0xFF * 16 bytes")
        # ---------------------------------------------------------------------------
        max_key_value = HexList("FF" * (self.feature_1816.set_ltk_cls.LEN.KEY // 8))
        BleProPrePairingTestUtils.pre_pairing_sequence(
            self, self.feature_1816, self.feature_1816_index, long_term_key=max_key_value,
            remote_identity_resolving_key=max_key_value, local_identity_resolving_key=max_key_value,
            remote_connection_signature_resolving_key=max_key_value,
            local_connection_signature_resolving_key=max_key_value, receiver_address=max_address_value)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check highest possible values in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------
        BleProPrePairingTestUtils.NvsHelper.check_device_pre_pairing_data(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence with all keys to a randomly chosen value")
        # ---------------------------------------------------------------------------
        random_key_value = RandHexList(self.feature_1816.set_ltk_cls.LEN.KEY // 8)
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            self, self.feature_1816, self.feature_1816_index, long_term_key=random_key_value,
            remote_identity_resolving_key=random_key_value, local_identity_resolving_key=random_key_value,
            remote_connection_signature_resolving_key=random_key_value,
            local_connection_signature_resolving_key=random_key_value, receiver_address=random_address_value)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check random values in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------
        BleProPrePairingTestUtils.NvsHelper.check_device_pre_pairing_data(self)

        self.testCaseChecked("FUN_1816_0006")
    # end def test_key_boundary_values

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_remote_irk_before_ltk(self):
        """
        Check a success status is returned if the remote Identity Resolving Key (IRK) is being set while the
        Long-Term Key (LTK) has not being set.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Start a pre-pairing sequence with the 'Start' request then send the remote IRK key "
                                 "as the first request of the sequence")
        # ---------------------------------------------------------------------------
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response to the set key command is a success")
        # ----------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=None, remote_identity_resolving_key=UtilNonNumericEnum.AUTO_FILL,
            local_identity_resolving_key=None, remote_connection_signature_resolving_key=None,
            local_connection_signature_resolving_key=None, receiver_address=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the rest of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=False, remote_identity_resolving_key=None, receiver_address=random_address_value)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0007")
    # end def test_remote_irk_before_ltk

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_local_irk_before_remote_irk(self):
        """
        Check a success status is returned if the local Identity Resolving Key (IRK) is being set while the
        remote Identity Resolving Key (IRK) has not being set.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Start a pre-pairing sequence with the 'Start' request then send the local IRK key "
                                 "as the first request of the sequence")
        # ---------------------------------------------------------------------------
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response to the set key command is a success")
        # ----------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=None, remote_identity_resolving_key=None,
            local_identity_resolving_key=UtilNonNumericEnum.AUTO_FILL, remote_connection_signature_resolving_key=None,
            local_connection_signature_resolving_key=None, receiver_address=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the rest of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=False, local_identity_resolving_key=None, receiver_address=random_address_value)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0008")
    # end def test_local_irk_before_remote_irk

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_remote_csrk_before_local_irk(self):
        """
        Check a success status is returned if the local Identity Resolving Key (IRK) is being set while the
        remote Identity Resolving Key (IRK) has not being set.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Start a pre-pairing sequence with the 'Start' request then send the remote CSRK "
                                 "key as the first request of the sequence")
        # ---------------------------------------------------------------------------
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response to the set key command is a success")
        # ----------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=None, remote_identity_resolving_key=None,
            local_identity_resolving_key=None, remote_connection_signature_resolving_key=UtilNonNumericEnum.AUTO_FILL,
            local_connection_signature_resolving_key=None, receiver_address=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the rest of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=False, remote_connection_signature_resolving_key=None, receiver_address=random_address_value)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0009")
    # end def test_remote_csrk_before_local_irk

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_local_csrk_before_remote_irk(self):
        """
        Check a success status is returned if the local Connection Signature Resolving Key (CSRK) is being set while
        the remote Connection Signature Resolving Key (CSRK) has not being set.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Start a pre-pairing sequence with the 'Start' request then send the local CSRK "
                                 "key as the first request of the sequence")
        # ---------------------------------------------------------------------------
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response to the set key command is a success")
        # ----------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=None, remote_identity_resolving_key=None,
            local_identity_resolving_key=None, remote_connection_signature_resolving_key=None,
            local_connection_signature_resolving_key=UtilNonNumericEnum.AUTO_FILL, receiver_address=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the rest of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=False, local_connection_signature_resolving_key=None, receiver_address=random_address_value)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0010")
    # end def test_local_csrk_before_remote_irk

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_remote_address_before_local_csrk(self):
        """
        Check a success status is returned if the remote address is being set while the
        local Connection Signature Resolving Key (CSRK) has not being set.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Start a pre-pairing sequence with the 'Start' request then send the remote "
                                 "address as the first request of the sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the response to the set pairing data command is a success")
        # ----------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            long_term_key=None, remote_identity_resolving_key=None,
            local_identity_resolving_key=None, remote_connection_signature_resolving_key=None,
            local_connection_signature_resolving_key=None, receiver_address=random_address_value, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the rest of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=False, receiver_address=None)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0011")
    # end def test_remote_address_before_local_csrk

    @features('Feature1816')
    @features('NoFeature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_mandatory_part(self):
        """
        Check a success status is returned on the Store request while the optional parameters have not being set.
         (mandatory parameters are ltk & remote address)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the mandatory part of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
            receiver_address=random_address_value, store=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0012")
    # end def test_sequence_mandatory_part

    @features('Feature1816')
    @features('Feature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_mandatory_part_irk_optional(self):
        """
        Check a success status is returned on the Store request while the optional parameters have not being set.
         (mandatory parameters are ltk & remote address)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the mandatory part of the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            remote_identity_resolving_key=None, local_identity_resolving_key=None,
            remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
            receiver_address=random_address_value, store=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0012")
    # end def test_sequence_mandatory_part_irk_optional

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_restart(self):
        """
        Check a success status is returned if the Start request is called twice.
        Check the second sequence could be completed
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the mandatory part of the Device Pre-pairing sequence except the last "
                                 "'Store' request")
        # ---------------------------------------------------------------------------
        first_random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
            receiver_address=first_random_address_value, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out a second time the mandatory part of the Device Pre-pairing sequence "
                                 "including the last 'Store' request")
        # ---------------------------------------------------------------------------
        second_random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, remote_connection_signature_resolving_key=None, local_connection_signature_resolving_key=None,
            receiver_address=second_random_address_value, store=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=second_random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        self.testCaseChecked("FUN_1816_0013")
    # end def test_sequence_restart

    @features('Feature1816')
    @features('Feature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_restart_no_optional_keys(self):
        """
        Complete a first sequence with optional keys set except the last 'Store' exchange then call 'Start' and
        finish the second sequence without the optional keys.
        Check optional fields are empty in NVS.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the whole the Device Pre-pairing sequence except the last 'Store' request")
        # ---------------------------------------------------------------------------
        first_random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, receiver_address=first_random_address_value, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out a second time the mandatory part of the Device Pre-pairing sequence "
                                 "including the last 'Store' request")
        # ---------------------------------------------------------------------------
        second_random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, receiver_address=second_random_address_value, store=True)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=second_random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check optional fields are empty in NVS")
        # ----------------------------------------------------------------------------
        # TODO: add NVS parser call

        self.testCaseChecked("FUN_1816_0014")
    # end def test_sequence_restart_no_optional_keys

    @features('Feature1816')
    @features('NoFeature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_without_remote_irk(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the remote Identity Resolving Key (IRK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the whole Device Pre-pairing sequence except the remote irk set key request")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, remote_identity_resolving_key=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Store'")
        # ---------------------------------------------------------------------------
        prepairing_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
        prepairing_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=prepairing_management_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("FUN_1816_0015")
    # end def test_sequence_without_remote_irk

    @features('Feature1816')
    @features('Feature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_without_remote_irk_optional(self):
        """
        Check the pairing data are updated while the remote Identity Resolving Key (IRK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the whole Device Pre-pairing sequence except the remote irk set key request")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, remote_identity_resolving_key=None, receiver_address=random_address_value, store=False)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check remote IRK Key is not set in NVS")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList("00" * (self.feature_1816.set_irk_remote_cls.LEN.KEY // 8)),
                         obtained=pre_pairing_chunk.keys.remote_identity_resolving_key,
                         msg='The remote IRK Key slot shall be filled with 0x00')

        self.testCaseChecked("FUN_1816_0015")
    # end def test_sequence_without_remote_irk_optional

    @features('Feature1816')
    @features('NoFeature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_without_local_irk(self):
        """
        Check an HID++ error code NOT_ALLOWED (5) is raised if the local Identity Resolving Key (IRK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the whole Device Pre-pairing sequence except the local irk set key request")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, local_identity_resolving_key=None, store=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send prepairing_data_management with prepairing_slot=0 and "
                                 "prepairing_management_control='Store'")
        # ---------------------------------------------------------------------------
        prepairing_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.STORE)
        prepairing_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_management, response_queue_name=HIDDispatcher.QueueName.ERROR,
            response_class_type=ErrorCodes)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check HID++ 2.0 NOT_ALLOWED (5) Error Code returned by the device")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=ErrorCodes.NOT_ALLOWED,
                         obtained=prepairing_management_response.errorCode,
                         msg='The errorCode parameter differs from the one expected')

        self.testCaseChecked("FUN_1816_0016")
    # end def test_sequence_without_local_irk

    @features('Feature1816')
    @features('Feature1816IrkOptional')
    @level('Functionality')
    @services('Debugger')
    def test_sequence_without_local_irk_optional(self):
        """
        Check the pairing data are updated while the local Identity Resolving Key (IRK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the whole Device Pre-pairing sequence except the local irk set key request")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, local_identity_resolving_key=None, receiver_address=random_address_value, store=False)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check local IRK Key is not set in NVS")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList("00" * (self.feature_1816.set_irk_local_cls.LEN.KEY // 8)),
                         obtained=pre_pairing_chunk.keys.local_identity_resolving_key,
                         msg='The local IRK Key slot shall be filled with 0x00')

        self.testCaseChecked("FUN_1816_0016")
    # end def test_sequence_without_local_irk_optional

    @features('Feature1816')
    @features('Feature1816KeysSupported', BleProPrePairingNvsChunk.KEYMAP.KEY_REMOTE_CSRK)
    @level('Functionality')
    @services('Debugger')
    def test_sequence_without_remote_csrk(self):
        """
        Check the pairing data are updated while the remote Connection Signature Resolving Key (CSRK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Roll out the whole Device Pre-pairing sequence except the remote csrk set key request")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, remote_connection_signature_resolving_key=None, receiver_address=random_address_value,
            store=False)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check Remote CSRK Key is not set in NVS")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList("00" * (self.feature_1816.set_csrk_remote_cls.LEN.KEY // 8)),
                         obtained=pre_pairing_chunk.keys.remote_connection_signature_resolving_key,
                         msg='The Remote CSRK Key slot shall be filled with 0x00')

        self.testCaseChecked("FUN_1816_0017")
    # end def test_sequence_without_remote_csrk

    @features('Feature1816')
    @features('Feature1816KeysSupported', BleProPrePairingNvsChunk.KEYMAP.KEY_LOCAL_CSRK)
    @level('Functionality')
    @services('Debugger')
    def test_sequence_without_local_csrk(self):
        """
        Check the pairing data are updated while the local Connection Signature Resolving Key (CSRK) has not being set
        when the Store action is requested.
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the whole Device Pre-pairing sequence except the local csrk set key request")
        # ---------------------------------------------------------------------------
        random_address_value = BleProPrePairingTestUtils.generate_random_static_address(test_case=self)
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index,
            start=True, local_connection_signature_resolving_key=None, receiver_address=random_address_value,
            store=False)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Retrieve the current Remote address using the JLink debugger")
        # ---------------------------------------------------------------------------
        pre_pairing_chunk = BleProPrePairingTestUtils.NvsHelper.get_latest_pre_pairing_chunk(self)
        self.assertEqual(expected=random_address_value,
                         obtained=pre_pairing_chunk.keys.remote_address,
                         msg='The Remote addresses shall match its randomly chosen value')

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Check local CSRK Key is not set in NVS")
        # ---------------------------------------------------------------------------
        self.assertEqual(expected=HexList("00" * (self.feature_1816.set_csrk_local_cls.LEN.KEY // 8)),
                         obtained=pre_pairing_chunk.keys.local_connection_signature_resolving_key,
                         msg='The local CSRK Key slot shall be filled with 0x00')

        self.testCaseChecked("FUN_1816_0018")
    # end def test_sequence_without_local_csrk

    @features('Feature1816')
    @level('Functionality')
    @services('Debugger')
    def test_nvs_chunk_validation(self):
        """
        Device Pre-pairing sequence Business Case

        To set the prepairing data, the requested sequence is :
        - prepairing_management (Start)
        - set the mandatory pairing data (set_LTK, set_prepairing_data (remoteAddress))
        - set the optional pairing data (set_IRK, set_CSRK, set_prepairing_data, ??)
        - prepairing_management (Store)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Roll out the Device Pre-pairing sequence")
        # ---------------------------------------------------------------------------
        BleProPrePairingTestUtils.pre_pairing_sequence(
            test_case=self, pre_pairing_main_class=self.feature_1816, pre_pairing_index=self.feature_1816_index)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check data in BLE Bond Id NVS chunk")
        # --------------------------------------------------------------------------
        BleProPrePairingTestUtils.NvsHelper.check_device_pre_pairing_data(self)

        self.testCaseChecked("FUN_1816_0019")
    # end def test_nvs_chunk_validation
# end class BleProPrePairingFunctionalityTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
