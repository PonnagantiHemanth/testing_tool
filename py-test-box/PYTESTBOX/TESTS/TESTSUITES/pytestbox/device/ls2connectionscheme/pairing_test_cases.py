#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.pairing_test_cases
:brief: Validate LS2 connection scheme for LS2 pairing test cases
:author: Zane Lu <zlu@logitech.com>
:date: 2024/1/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pytestbox.device.ls2connectionscheme.uhs_connection_scheme import UhsConnectionSchemeBase
from pytestbox.device.ls2connectionscheme.utils import Ls2ConnectionSchemeTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingTestCases(UhsConnectionSchemeBase):
    """
    LS2 connection scheme - Pairing Test Cases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'power on the device')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.turn_on()
    # end def setUp

    @features('Ls2ConnectionScheme')
    @features('LS2Pairing')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_business_case(self):
        """
        Pairing business Case
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Unpair the receiver at the PortConfiguration.LS2_RECEIVER2_PORT')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to another LS2 receiver")
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_pairing(port_settings=[False, False, False, True, False],
                            target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                            openlock_mode=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        self.testCaseChecked("BUS_LS2_PAIRING_0001")
    # end def test_pairing_business_case

    @features('Ls2ConnectionScheme')
    @features('LS2Pairing')
    @level('Functionality')
    @services('PowerSupply')
    def test_no_pairing_when_receiver_is_off(self):
        """
        LS2 Pairing - The device shall fail the pairing sequence if the open lock request is not received immediately
        (the keyboard receiver unplugged when the user does the long press).
        The device shall then enter into deep sleep mode
        """
        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[False, False, False, False, False])

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Long-press the connect button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        sleep(self.MAX_WAIT_SLEEP) # wait for pairing failed

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device goes into the deep sleep mode")
        # --------------------------------------------------------------------------------------------------------------
        self.verify_deep_sleep_current_consumption()

        self.testCaseChecked("FNT_LS2_PAIRING_0002")
    # end def test_no_pairing_when_receiver_is_off

    @features('Ls2ConnectionScheme')
    @features('LS2Pairing')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_prepaired_receiver_replacement(self):
        """
        LS2 Pairing - The pre-paired receiver is replaced if pairing type is NOT LS2-Pairing
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, 'Unpair the receiver at the PortConfiguration.LS2_RECEIVER2_PORT')
        # --------------------------------------------------------------------------------------------------------------
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to another LS2 receiver")
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_pairing(port_settings=[False, False, False, True, False],
                            target_port=PortConfiguration.LS2_RECEIVER2_PORT,
                            openlock_mode=QuadDeviceConnection.ConnectDevices.OPEN_LOCK)

        self.testCaseChecked("BUS_LS2_PAIRING_0003")
    # end def test_pairing_prepaired_receiver_replacement

    @features('Ls2ConnectionScheme')
    @features('ThreePairingSlots')
    @features('LS2Pairing')
    @level('Business')
    @services('PowerSupply')
    def test_pairing_to_crush(self):
        """
        LS2 Pairing - The Pairing to Crush is completed if no LS2 recevier detected or the pairing failed
        """
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.CRUSH_RECEIVER_PORT)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to Crush receiver")
        # --------------------------------------------------------------------------------------------------------------
        # port_settings=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        self.verify_pairing(port_settings=[False, True, False, False, False],
                            target_port=PortConfiguration.CRUSH_RECEIVER_PORT)

        self.testCaseChecked("BUS_LS2_PAIRING_0004")
    # end def test_pairing_to_crush

    @features('Ls2ConnectionScheme')
    @features('LS2Pairing')
    @level('Functionality')
    @services('PowerSupply')
    def test_device_shall_ignore_any_long_press_action_when_in_pairing_mode(self):
        """
        LS2 Pairing - When in pairing mode , the device shall ignore any long press action on the Connect or
        Lightspeed button. The device shall then enter into deep sleep mode when reaching the 3 minutes timeout while
        the user has long press on the connect or lightspeed button multiple times.
        """
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)

        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[False, False, False, True, False])

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        Ls2ConnectionSchemeTestUtils.open_lock_equad_receiver(self,
                                                              PortConfiguration.LS2_RECEIVER2_PORT,
                                                              connect_devices=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Long-press the connect button 3 times")
        # --------------------------------------------------------------------------------------------------------------
        # time consuming operations, do this 3 times only
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION,
                                               repeat=3)
        sleep(DiscoveryTestUtils.DEVICE_DISCOVERY_TIMEOUT) # wait 3 minutes

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the device goes into the deep sleep mode")
        # --------------------------------------------------------------------------------------------------------------
        self.verify_deep_sleep_current_consumption()

        self.testCaseChecked("FNT_LS2_PAIRING_0005")
    # end def test_device_shall_ignore_any_long_press_action_when_in_pairing_mode

    @features('Ls2ConnectionScheme')
    @features('LS2Pairing')
    @level('Functionality')
    @services('PowerSupply')
    def test_return_in_reconnection_if_short_press_on_the_button_in_the_middle_of_the_pairing_sequence(self):
        """
        LS2 Pairing - The device will return in Reconnection mode if the user does a short press on the Lightspeed
        button in the middle of the pairing sequence.
        """
        Ls2ConnectionSchemeTestUtils.unpair_equad_receiver(self, PortConfiguration.LS2_RECEIVER2_PORT)
        self.pair_ls2_receiver()

        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[False, False, True, True, False])

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Long-press the connect button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION,
                                               delay=ButtonStimuliInterface.DEFAULT_DELAY)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "short-press the connect button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON)
        if self.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportBTLE:
            # support LS and BLE, click again to switch back to LS channel
            sleep(0.5)
            self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to the target receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()

        self.testCaseChecked("FNT_LS2_PAIRING_0006")
    # end def test_return_in_reconnection_if_short_press_on_the_button_in_the_middle_of_the_pairing_sequence

    @features('Ls2ConnectionScheme')
    @features('LS2Pairing')
    @level('Functionality')
    @services('PowerSupply')
    def test_exit_pairing_mode_if_device_is_reset(self):
        """
        LS2 Pairing - The device will exit the pairing mode if the user does a device power off / on.
        """
        self.pair_ls2_receiver()

        # desired=["pre-paired", "Crush", "LS2-Pairing", "another LS2 receiver", "another Crush"]
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(self, desired=[False, False, True, False, False])

        ChannelUtils.set_hidpp_reporting(self)
        ChannelUtils.clean_messages(
            test_case=self,
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
            class_type=(DeviceConnection, DeviceDisconnection))

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Long-press the connect button")
        # --------------------------------------------------------------------------------------------------------------
        self.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                               duration=ButtonStimuliInterface.LONG_PRESS_DURATION)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Reset the device")
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.restart_device()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, "Check the connection to the target receiver")
        # --------------------------------------------------------------------------------------------------------------
        self.check_device_connected()

        self.testCaseChecked("FNT_LS2_PAIRING_0007")
    # end def test_exit_pairing_mode_if_device_is_reset

# end class PairingTestCases

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
