#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1816.interface
:brief: HID++ 2.0 BLEPro pre-pairing interface test suite
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyhid.hiddispatcher import HIDDispatcher
from pylibrary.mcu.nrf52.bleproprepairingchunk import BleProPrePairingNvsChunk
from pylibrary.tools.hexlist import HexList
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
class BleProPrePairingInterfaceTestCase(BleProPrePairingTestCase):
    """
    Validate Device BLE Pro Pre-pairing Interface TestCases
    """
    @features('Feature1816')
    @level('Interface')
    def test_prepairing_data_management(self):
        """
        Validate prepairing_data_management API

        [0] prepairing_management(prepairing_slot, prepairing_management_control)
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_step(
            self, "Send prepairing_data_management with prepairing_slot=0 and prepairing_management_control='Start'")
        # ---------------------------------------------------------------------------
        prepairing_data_management = self.feature_1816.prepairing_data_management_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            prepairing_slot=self.feature_1816.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=self.feature_1816.prepairing_data_management_cls.MODE.START)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for prepairing_data_management acknowledgement")
        # ----------------------------------------------------------------------------
        prepairing_data_management_response = ChannelUtils.send(
            test_case=self, report=prepairing_data_management, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.prepairing_data_management_response_cls)

        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, prepairing_data_management_response, self.feature_1816.prepairing_data_management_response_cls)

        self.testCaseChecked("INT_1816_0001")
    # end def test_prepairing_data_management

    @features('Feature1816')
    @level('Interface')
    def test_set_ltk(self):
        """
        Validate set_LTK API

        [1] set_LTK(ltk)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_LTK with a fixed ltk value")
        # ---------------------------------------------------------------------------
        set_ltk = self.feature_1816.set_ltk_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            ltk=HexList("11" * (self.feature_1816.set_ltk_cls.LEN.KEY // 8)))

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_LTK acknowledgement")
        # ----------------------------------------------------------------------------
        set_ltk_response = ChannelUtils.send(
            test_case=self, report=set_ltk, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.set_ltk_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, set_ltk_response, self.feature_1816.set_ltk_response_cls)

        self.testCaseChecked("INT_1816_0002")
    # end def test_set_ltk

    @features('Feature1816')
    @level('Interface')
    def test_set_irk_remote(self):
        """
        Validate set_IRK_remote API

        [2] set_IRK_remote(irk_remote)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_IRK_remote with a fixed irk_remote value")
        # ---------------------------------------------------------------------------
        set_irk_remote = self.feature_1816.set_irk_remote_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            irk_remote=HexList("22" * (self.feature_1816.set_irk_remote_cls.LEN.KEY // 8)))

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_IRK_remote acknowledgement")
        # ----------------------------------------------------------------------------
        set_irk_remote_response = ChannelUtils.send(
            test_case=self, report=set_irk_remote, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.set_irk_remote_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, set_irk_remote_response, self.feature_1816.set_irk_remote_response_cls)

        self.testCaseChecked("INT_1816_0003")
    # end def test_set_irk_remote

    @features('Feature1816')
    @level('Interface')
    def test_set_irk_local(self):
        """
        Validate set_IRK_local API

        [3] set_IRK_local(irk_local)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_IRK_local with a fixed irk_local value")
        # ---------------------------------------------------------------------------
        set_irk_local = self.feature_1816.set_irk_local_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            irk_local=HexList("33" * (self.feature_1816.set_irk_local_cls.LEN.KEY // 8)))

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_IRK_local acknowledgement")
        # ----------------------------------------------------------------------------
        set_irk_local_response = ChannelUtils.send(
            test_case=self, report=set_irk_local, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.set_irk_local_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, set_irk_local_response, self.feature_1816.set_irk_local_response_cls)

        self.testCaseChecked("INT_1816_0004")
    # end def test_set_irk_local

    @features('Feature1816')
    @features('Feature1816KeysSupported', BleProPrePairingNvsChunk.KEYMAP.KEY_REMOTE_CSRK)
    @level('Interface')
    def test_set_csrk_remote(self):
        """
        Validate set_CSRK_remote API

        [4] set_CSRK_remote(csrk_remote)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_CSRK_remote with a fixed csrk_remote value")
        # ---------------------------------------------------------------------------
        set_csrk_remote = self.feature_1816.set_csrk_remote_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            csrk_remote=HexList("44" * (self.feature_1816.set_csrk_remote_cls.LEN.KEY // 8)))

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_CSRK_remote acknowledgement")
        # ----------------------------------------------------------------------------
        set_csrk_remote_response = ChannelUtils.send(
            test_case=self, report=set_csrk_remote, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.set_csrk_remote_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, set_csrk_remote_response, self.feature_1816.set_csrk_remote_response_cls)

        self.testCaseChecked("INT_1816_0005")
    # end def test_set_csrk_remote

    @features('Feature1816')
    @features('Feature1816KeysSupported', BleProPrePairingNvsChunk.KEYMAP.KEY_LOCAL_CSRK)
    @level('Interface')
    def test_set_csrk_local(self):
        """
        Validate set_CSRK_local API

        [4] set_CSRK_local(csrk_local)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_CSRK_local with a fixed csrk_local value")
        # ---------------------------------------------------------------------------
        set_csrk_local = self.feature_1816.set_csrk_local_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            csrk_local=HexList("55" * (self.feature_1816.set_csrk_local_cls.LEN.KEY // 8)))

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_CSRK_local acknowledgement")
        # ----------------------------------------------------------------------------
        set_csrk_local_response = ChannelUtils.send(
            test_case=self, report=set_csrk_local, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.set_csrk_local_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, set_csrk_local_response, self.feature_1816.set_csrk_local_response_cls)

        self.testCaseChecked("INT_1816_0006")
    # end def test_set_csrk_local

    @features('Feature1816')
    @level('Interface')
    def test_set_prepairing_data(self):
        """
        Validate set_prepairing_data API

        [6] set_prepairing_data(data_type, data)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send set_prepairing_data with data_type='Remote' and a fixed remote_address value")
        # ---------------------------------------------------------------------------
        set_prepairing_data = self.feature_1816.set_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self),
            feature_index=self.feature_1816_index,
            data_type=self.feature_1816.set_prepairing_data_cls.TYPE.REMOTE,
            remote_address=HexList("66" * (self.feature_1816.set_prepairing_data_cls.LEN.ADDRESS // 8)))

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for set_prepairing_data acknowledgement")
        # ----------------------------------------------------------------------------
        set_prepairing_data_response = ChannelUtils.send(
            test_case=self, report=set_prepairing_data, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.set_prepairing_data_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, set_prepairing_data_response, self.feature_1816.set_prepairing_data_response_cls)

        self.testCaseChecked("INT_1816_0007")
    # end def test_set_prepairing_data

    @features('Feature1816')
    @level('Interface')
    def test_get_prepairing_data(self):
        """
        Validate get_prepairing_data API

        [6] get_prepairing_data(data_type, data)
        """
        # Start the pre-pairing sequence and retrieve the local device address
        BleProPrePairingTestUtils.pre_pairing_start_sequence(self, self.feature_1816, self.feature_1816_index,
                                                             get_local_address=False)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Send get_prepairing_data with data_type='Local'")
        # ---------------------------------------------------------------------------
        get_prepairing_data = self.feature_1816.get_prepairing_data_cls(
            device_index=ChannelUtils.get_device_index(test_case=self), feature_index=self.feature_1816_index,
            data_type=self.feature_1816.get_prepairing_data_cls.TYPE.LOCAL)

        # ----------------------------------------------------------------------------
        LogHelper.log_check(self, "Wait for get_prepairing_data acknowledgement")
        # ----------------------------------------------------------------------------
        get_prepairing_data_response = ChannelUtils.send(
            test_case=self, report=get_prepairing_data, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=self.feature_1816.get_prepairing_data_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(
            self, get_prepairing_data_response, self.feature_1816.get_prepairing_data_response_cls)

        self.testCaseChecked("INT_1816_0008")
    # end def test_get_prepairing_data
# end class BleProPrePairingInterfaceTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
