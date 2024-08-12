#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.uhs_connection_scheme
:brief: Validate UHS connection scheme for UHS test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2022/11/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.powermodeutils import PowerModesTestUtils
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.receiver.base.receiverinfoutils import ReceiverInfoUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class UhsConnectionSchemeBase(DeviceBaseTestCase):
    """
    UHS connection scheme base class
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # noinspection DuplicatedCode
        f = self.getFeatures()
        self.RECEIVER_PID = f.PRODUCT.DEVICE.CONNECTION_SCHEME.LS2_CS.F_PrePairedReceiverPID
        self.assertNotNone(self.RECEIVER_PID,
                           msg="PrePairedReceiverPID parameter shall be defined in DUT test settings")
        self.DEEP_SLEEP_CURRENT_THRESHOLD = f.PRODUCT.DEVICE.CONNECTION_SCHEME.LS2_CS.F_DeepSleepCurrentThreshold
        self.MAX_WAIT_SLEEP = f.PRODUCT.DEVICE.CONNECTION_SCHEME.LS2_CS.F_MaxWaitSleep

        self.receiver_index = ChannelUtils.get_port_index(test_case=self)

        Ls2ConnectionSchemeTestUtils.check_receiver_arrangement(
            self,
            [(PortConfiguration.PRE_PAIRED_RECEIVER_PORT, to_int(HexList(self.RECEIVER_PID))),
             (PortConfiguration.CRUSH_RECEIVER_PORT, PortConfiguration.USB_PID_CRUSH),
             (PortConfiguration.LS2_RECEIVER_PORT, PortConfiguration.USB_PID_MOLDUCK),
             (PortConfiguration.LS2_RECEIVER2_PORT, PortConfiguration.USB_PID_MOLDUCK),
             (PortConfiguration.CRUSH_RECEIVER2_PORT, PortConfiguration.USB_PID_CRUSH)])

        self.read_receivers_equad_information()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'set device in OOB state')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.disable_all_receiver_usb_ports(self)
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        self.connect_to_the_pre_paired_receiver()

        ChannelUtils.close_channel(test_case=self)

        new_channel = DeviceManagerUtils.get_channel(
            test_case=self,
            channel_id=ChannelIdentifier(port_index=PortConfiguration.PRE_PAIRED_RECEIVER_PORT, device_index=1))
        DeviceManagerUtils.set_channel(test_case=self, new_channel=new_channel)
        DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=self)

        # after oob, the device shall be
        # 1. pre-paired slot is ready
        # 2. crush slot is empty
        # 3. ls2 receiver slot is empty

        # power off the device
        self.power_supply_emulator.turn_off()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, 'enable all receiver ports')
            # ----------------------------------------------------------------------------------------------------------
            Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case=self, desired=[True, True, True, True, True])
            Ls2ConnectionSchemeTestUtils.fix_port_not_response_issue(test_case=self)

            # the code below is used to make sure Crush pads are not in open-lock mode.
            self.build_fake_pairing_information()

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_post_requisite(self, "Reload initial NVS")
            # ------------------------------------------------------------------------------------------------------
            DeviceTestUtils.NvsHelper.restore_nvs(self)
        # end with
        super().tearDown()
    # end def tearDown

    def read_receivers_equad_information(self):
        """
        Read EQuad information of receivers
        """
        self.receiver_equad_info = dict()
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loops to get EQuad info for receivers")
        # --------------------------------------------------------------------------------------------------------------
        for port_index in PortConfiguration.PORT_ARRANGEMENT:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, f"Receiver on the port {port_index}")
            # ----------------------------------------------------------------------------------------------------------
            Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, port_index)
            self.receiver_equad_info[port_index] = ReceiverInfoUtils.get_receiver_equad_info(test_case=self)
        # end for
    # end def read_receivers_equad_information

    def build_fake_pairing_information(self):
        """
        Set fake pairing information for receivers except the pre-paired receiver
        """
        # remove the pre-paired port
        del self.receiver_equad_info[PortConfiguration.PRE_PAIRED_RECEIVER_PORT]

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Loop over receivers to build fake pairing information")
        # --------------------------------------------------------------------------------------------------------------
        for port_index, info in self.receiver_equad_info.items():
            Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, port_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Enable Manufacturing Test Mode")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverTestUtils.HIDppHelper.activate_features(test_case=self, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Erase pairing information")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverInfoUtils.erase_receiver_pairing_info(test_case=self)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set pairing information")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverInfoUtils.set_device_pairing_info_to_receiver(
                test_case=self,
                destination_id=info.last_dest_id,
                default_report_interval=8,
                device_quid=0xabcd,
                equad_major_version=0x11,
                equad_minor_version=0x00,
                equad_device_subclass=2,
                equad_attributes=RandHexList(6))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set extended pairing information")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverInfoUtils.set_device_extended_pairing_info_to_receiver(
                test_case=self,
                serial_number=RandHexList(4),
                report_types=RandHexList(4),
                usability_info=0x0f)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set device name")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverInfoUtils.set_device_name_to_receiver(test_case=self,
                                                          segment_length=14,
                                                          name_string=HexList("fake_device123".encode()))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Set LTK")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverInfoUtils.set_ltk_to_receiver(test_case=self,
                                                  aes_encryption_key_byte_1_to_6=RandHexList(6),
                                                  aes_encryption_key_byte_9_to_16=RandHexList(8))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, "Reset Receiver")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverTestUtils.reset_receiver(test_case=self,
                                             skip_link_established_verification=True)
        # end for
    # end def build_fake_pairing_information

    def connect_to_the_pre_paired_receiver(self):
        """
        Connect to the pre-paired receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Make the device connect to the pre-paired receiver.")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, PortConfiguration.PRE_PAIRED_RECEIVER_PORT)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [True, False, False, False, False])
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Restart the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.restart_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Verify the device is connected to the pre-paired receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def connect_to_the_pre_paired_receiver

    def pair_crush_receiver(self):
        """
        Pair Crush receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Unpair the crush receiver")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Restart the DUT")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()
        sleep(3)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [False, True, False, False, False])
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        self.power_supply_emulator.turn_on()

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Verify the device is connected to the crush receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def pair_crush_receiver

    def pair_ls2_receiver(self):
        """
        Pair LS2 receiver
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Unpair the ls2 receiver")
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER_PORT)

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Restart the DUT.")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_off()
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, [False, False, True, False, False])
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(
            self, PortConfiguration.LS2_RECEIVER_PORT, connect_devices=7)
        self.power_supply_emulator.turn_on()

        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self, msg="Verify the device is connected to the ls2 receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def pair_ls2_receiver

    def check_device_connected(self, link_status=DeviceConnection.LinkStatus.LINK_ESTABLISHED):
        """
        Check if the device is connected to the target receiver

        :param link_status: The expected link status (Values can be found in ``DeviceConnection.LinkStatus``) - OPTIONAL
        :type link_status: ``int``
        """
        ChannelUtils.wait_through_receiver_channel_link_status(
            test_case=self, channel=self.current_channel,
            link_status=link_status
        )
    # end def check_device_connected

    def verify_deep_sleep_current_consumption(self):
        """
        Verify the device is in the deep sleep mode by measuring the current
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Send command to get current value from power supply')
        # --------------------------------------------------------------------------------------------------------------
        current = CommonBaseTestUtils.EmulatorHelper.get_current(
            self, delay=PowerModesTestUtils.OPTICAL_SENSOR_SLEEP_TIME, samples=150) * 1000
        LogHelper.log_info(self, f'Current = {current}uA')

        expected_value = self.DEEP_SLEEP_CURRENT_THRESHOLD
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f'Validate if the current is below {expected_value}uA')
        # --------------------------------------------------------------------------------------------------------------
        self.assertLess(current, expected_value,
                        msg=f'The current value {current}uA shall be below {expected_value}uA')
    # end def verify_deep_sleep_current_consumption

    def verify_oob(self, port_settings, target_port, openlock_mode=QuadDeviceConnection.ConnectDevices.NO_CHANGE):
        """
        Verify the result of the out-of-box

        :param port_settings: the power status of the usb ports
        :type port_settings: ``List``
        :param target_port: candidate receiver port for connection
        :type target_port: ``int``
        :param openlock_mode: The expected openlock_mode (Values can be found in ``QuadDeviceConnection.ConnectDevices``) - OPTIONAL
        :type openlock_mode: ``int``
        """
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, target_port)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, port_settings)

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        self.assertIn(member=openlock_mode,
                      container=[QuadDeviceConnection.ConnectDevices.NO_CHANGE,
                                 QuadDeviceConnection.ConnectDevices.OPEN_LOCK,
                                 QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK],
                      msg="Invalid 'Connect Devices values' value")
        if openlock_mode is not QuadDeviceConnection.ConnectDevices.NO_CHANGE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Openlock the receiver")
            # ----------------------------------------------------------------------------------------------------------
            Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(self, target_port, connect_devices=openlock_mode)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power on the device")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_on()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to the target receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def verify_oob

    def verify_oob_no_receiver_available(self):
        """
        Verify the device goes into the deep sleep mode when power on the OOB device with no receiver available
        """
        Ls2ConnectionSchemeTestUtils.disable_all_receiver_usb_ports(self)
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power on the device")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_on()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wait time-out for no connection")
        # --------------------------------------------------------------------------------------------------------------
        sleep(self.MAX_WAIT_SLEEP)

        self.verify_deep_sleep_current_consumption()
    # end def verify_oob_no_receiver_available

    def verify_power_on(self, port_settings, target_port, openlock_mode=QuadDeviceConnection.ConnectDevices.NO_CHANGE):
        """
        Verify the result of the power-on

        :param port_settings: the power status of the usb ports
        :type port_settings: ``List``
        :param target_port: candidate receiver port for connection
        :type target_port: ``int``
        :param openlock_mode:  The expected openlock_mode (Values can be found in ``QuadDeviceConnection.ConnectDevices``) - OPTIONAL
        :type openlock_mode: ``int``
        """
        self.power_supply_emulator.turn_off()
        sleep(1)

        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, target_port)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, port_settings)

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        self.assertIn(member=openlock_mode,
                      container=[QuadDeviceConnection.ConnectDevices.NO_CHANGE,
                                 QuadDeviceConnection.ConnectDevices.OPEN_LOCK,
                                 QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK],
                      msg="Invalid 'Connect Devices values' value")
        if openlock_mode is not QuadDeviceConnection.ConnectDevices.NO_CHANGE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Openlock the receiver")
            # ----------------------------------------------------------------------------------------------------------
            Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(self, target_port, connect_devices=openlock_mode)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Power on the device")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_on()
        sleep(1)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to the target receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def verify_power_on

    def verify_power_on_no_receiver_available(self):
        """
        Verify the device goes into the deep sleep mode when power on the device with no receiver available
        """
        ChannelUtils.close_channel(self)

        self.power_supply_emulator.turn_off()
        sleep(0.5)

        self.verify_oob_no_receiver_available()
    # end def verify_power_on_no_receiver_available

    def verify_reconnection(self, port_settings, target_port):
        """
        Verify the result of the reconnection

        :param port_settings: the power status of the usb ports
        :type port_settings: ``List``
        :param target_port: candidate receiver port for connection
        :type target_port: ``int``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Waiting the device disconnection from the pre-paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.wait_for_deep_sleep_mode(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Switch to port {target_port}')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, target_port)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Set port status {port_settings}')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, port_settings)

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Wake up the device")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.user_action()

        LogHelper.log_check(self, "Check the connection to the target receiver")
        self.check_device_connected()
    # end def verify_reconnection

    def verify_reconnection_no_receiver_available(self):
        """
        Verify the result of the reconnection when no receiver is available
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Waiting the device disconnection from the pre-paired receiver')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.wait_for_deep_sleep_mode(self)

        ChannelUtils.close_channel(self)

        Ls2ConnectionSchemeTestUtils.disable_all_receiver_usb_ports(self)
        self.device.disable_usb_port(PortConfiguration.CABLE_CONNECTED_PORT)

        self.button_stimuli_emulator.user_action()

        sleep(self.MAX_WAIT_SLEEP)

        self.verify_deep_sleep_current_consumption()
    # end def verify_reconnection_no_receiver_available

    def verify_pairing(self, port_settings, target_port, openlock_mode=QuadDeviceConnection.ConnectDevices.NO_CHANGE):
        """
        Verify the result of the pairing (long-press connect button)

        :param port_settings: the power status of the usb ports
        :type port_settings: ``List``
        :param target_port: candidate receiver port for connection
        :type target_port: ``int``
        :param openlock_mode: The expected openlock_mode (Values can be found in ``QuadDeviceConnection.ConnectDevices``) - OPTIONAL
        :type openlock_mode: ``int``
        """
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(self, target_port)
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, port_settings)

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        self.assertIn(member=openlock_mode,
                      container=[QuadDeviceConnection.ConnectDevices.NO_CHANGE,
                                 QuadDeviceConnection.ConnectDevices.OPEN_LOCK,
                                 QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK],
                      msg="Invalid 'Connect Devices values' value")
        if openlock_mode is not QuadDeviceConnection.ConnectDevices.NO_CHANGE:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Openlock the receiver")
            # ----------------------------------------------------------------------------------------------------------
            Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(self, target_port, connect_devices=openlock_mode)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Long-press the connect button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to the target receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()
    # end def verify_pairing

# end class UhsConnectionSchemeBase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
