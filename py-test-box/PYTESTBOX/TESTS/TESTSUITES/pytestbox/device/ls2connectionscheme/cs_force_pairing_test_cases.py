#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.cs_force_pairing_test_cases
:brief: Validate LS2 connection scheme for Force Pairing test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2021/06/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformationResponse
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.forcepairingutils import ForcePairingTestUtils
from pytestbox.device.ls2connectionscheme.forcepairing import ForcePairingBaseTestCase
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CSForcePairingTestCases(ForcePairingBaseTestCase):
    """
    LS2 connection scheme - CS Force Pairing Test Cases
    """

    @features('CSForcePairing')
    @features('ThreePairingSlots')
    @level('Business')
    @services('PowerSupply')
    @services('MultiHost')
    def test_set_force_pairing_connect_to_ls2_receiver(self):
        """
        [w/o Connect Button] [Force Pairing] [Mouse]  LS Channel selected at PowerOn and ForcePairing is True -
        The Pairing to a LS2-2Devices receiver is the FIRST priority if the pairing type sent by the SW is LS2-Pairing
        and the user does a power off/on of the device.
        NB: all the other receivers shall be available but ignored !
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Crush paired and powered on')
        # --------------------------------------------------------------------------------------------------------------
        self.pair_crush_receiver()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'LS2-Pairing slot never paired but receiver powered on')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        # -------------------------------------------------------------
        LogHelper.log_step(self, 'get the address of the LS2 receiver')
        # -------------------------------------------------------------
        equad_info_request = GetTransceiverEQuadInformation()
        equad_info_response = ChannelUtils.send(
            test_case=self,
            report=equad_info_request,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetTransceiverEQuadInformationResponse)

        self.connect_to_the_pre_paired_receiver()

        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[True, True, True, False, False])
        ChannelUtils.close_channel(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'open lock the LS2 receiver (connect_devices=7)')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.LS2_RECEIVER_PORT)
        ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)
        Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(
            test_case=self,
            receiver_usb_port=PortConfiguration.LS2_RECEIVER_PORT,
            connect_devices=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'send setForcePairing request for the pre-paired receiver '
                                 f'with the LS2 receiver address={equad_info_response.base_address}')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.pre_paired_channel)
        ForcePairingTestUtils.HIDppHelper.set_force_pairing(test_case=self,
                                                            pairing_address=equad_info_response.base_address,
                                                            device_index=self.DUT_DEVICE_INDEX)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Wait for device to be connected')
        # --------------------------------------------------------------------------------------------------------------
        DeviceManagerUtils.set_channel(test_case=self, new_channel=self.ls2_channel)
        ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'check HID USB report from the LS2 receiver')
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.ButtonHelper.check_user_action(self)

        self.testCaseChecked("BUS_FORCE_PAIRING_0001")
    # end def test_set_force_pairing_connect_to_ls2_receiver

# end class CSForcePairingTestCases

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
