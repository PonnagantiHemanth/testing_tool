#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.recoveryutils
:brief:  Helpers for recovery feature
:author: Stanislas Cottard
:date: 2020/05/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
import time
from enum import Enum
from warnings import warn

from pychannel.throughreceiverchannel import ThroughBleProReceiverChannel
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbReceiverChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.basetest import DeviceBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.productdata import POST_RESET_ACTIONS
from pytestbox.base.productdata import PRE_RESET_ACTIONS
from pytestbox.base.productdata import RECOVERY_KEYS_LIST_MAP
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DisconnectMethod(Enum):
    """
    Enumeration of the methods that can be used to get a device disconnection
    """
    DFU_RESTART = 0x00
    PERFORM_DEVICE_PAIRING_AND_UNPAIRING = 0x01
    DEVICE_OFF_ON = 0x02
    DEVICE_DEEP_SLEEP = 0x03
# end class DisconnectMethod


class RecoveryTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on recovery feature
    """
    @staticmethod
    def tear_down_clean_up(test_case):
        """
        Clean up that needs to be done during tear down

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        """
        test_case.button_stimuli_emulator.release_all()
    # end def tear_down_clean_up

    @classmethod
    def perform_user_actions_for_recovery(cls, test_case, current_device_index):
        """
        Perform the user action to enter recovery bootloader

        For mice: right+left press, then restart device and then right+left release

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param current_device_index: Device index of the current device on application
        :type current_device_index: ``int``
        """
        disconnected = False
        for _ in range(2):
            # Create a single scenario to execute the full recovery entry sequence with Kosmos capabilities
            if test_case.power_slider_emulator is not None:
                if test_case.device_debugger is not None:
                    test_case.device_debugger.close()
                # end if
                # Turn DUT power slider OFF
                test_case.kosmos.sequencer.offline_mode = True
                test_case.button_stimuli_emulator.perform_action_list(cls.get_pre_reset_actions(test_case=test_case))
                test_case.power_slider_emulator.power_off()
                test_case.kosmos.pes.delay(delay_s=0.5)
                if test_case.motion_emulator is not None and test_case.motion_emulator.get_module():
                    # Soft-reset motion emulator
                    test_case.kosmos.pes.execute(
                        action=test_case.motion_emulator.get_module().action_event.RESET)
                # end if
                # Turn DUT power slider ON
                test_case.power_slider_emulator.power_on()
                test_case.kosmos.sequencer.offline_mode = False
                # Run test sequence
                test_case.kosmos.sequencer.play_sequence()
                if test_case.device_debugger is not None:
                    test_case.device_debugger.open()
                    # Emulating a hardware reset is required by the Graviton Dev board
                    test_case.device_debugger.reset(soft_reset=False)
                # end if
            else:
                cls.perform_pre_reset_actions(test_case=test_case)
                cls.perform_restart_action_for_recovery(test_case=test_case)
            # end if

            if isinstance(test_case.current_channel, ThroughReceiverChannel) and not test_case.f.PRODUCT.F_IsGaming:
                DeviceManagerUtils.set_channel(
                    test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
            # end if

            # Wait DeviceConnection notification with link not established
            device_index = 0
            while device_index != current_device_index:
                device_connection = ChannelUtils.get_only(
                    test_case=test_case,
                    channel=test_case.current_channel,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                    class_type=DeviceConnection,
                    timeout=UsbReceiverChannel.SUPERVISION_TIMEOUT,
                    check_first_message=False,
                    allow_no_message=True)

                if device_connection is not None:
                    device_index = int(Numeral(device_connection.device_index))
                    if device_index == current_device_index:
                        device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                            device_connection)
                        device_info = device_info_class.fromHexList(HexList(device_connection.information))
                        test_case.assertEquals(
                            expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                            obtained=int(Numeral(device_info.device_info_link_status)),
                            msg=f'The receiver did not disconnect from the device application, {device_info}')
                        disconnected = True
                    # end if
                else:
                    break
                # end if
            if disconnected:
                break
            # end if
        # end for
        cls.perform_post_reset_actions(test_case=test_case)
    # end def perform_user_actions_for_recovery

    @classmethod
    def filter_and_perform_actions(cls, test_case, action_list, force_action_indexes=None, ignore_action_indexes=None):
        """
        Perform the required key pressed action list.

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param action_list: list of key_id and action name
        :type action_list: ``list[tuple[KEY_ID,str]]``
        :param force_action_indexes: indexes to be kept in the list
        :type force_action_indexes: ``list[int]``
        :param ignore_action_indexes: indexes to be removed from the list
        :type ignore_action_indexes: ``list[int]``
        """
        if force_action_indexes is not None and len(force_action_indexes) > 0:
            for index in reversed(range(len(action_list))):
                if index not in force_action_indexes:
                    action_list.pop(index)
                # end if
            # end for
        # end if
        if ignore_action_indexes is not None and len(ignore_action_indexes) > 0:
            ignore_action_indexes.sort(reverse=True)
            for index in ignore_action_indexes:
                if len(action_list) > index:
                    action_list.pop(index)
                # end if
            # end for
        # end if

        test_case.button_stimuli_emulator.perform_action_list(action_list)

        time.sleep(.5)
    # end def filter_and_perform_actions

    @staticmethod
    def get_pre_reset_actions(test_case):
        """
        Retrieve the list of the pre reset actions.

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        """
        return list(
            RECOVERY_KEYS_LIST_MAP[
                test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.DEVICE_RECOVERY.F_RecoveryKeysVariant][PRE_RESET_ACTIONS])
    # end def get_pre_reset_actions

    @classmethod
    def perform_pre_reset_actions(cls, test_case, force_action_indexes=None, ignore_action_indexes=None):
        """
        Perform the post reset keystrokes.

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param force_action_indexes: indexes to be kept in the list
        :type force_action_indexes: ``list[int]``
        :param ignore_action_indexes: indexes to be removed from the list
        :type ignore_action_indexes: ``list[int]``
        """
        action_list = cls.get_pre_reset_actions(test_case=test_case)

        cls.filter_and_perform_actions(
            test_case=test_case,
            action_list=action_list,
            force_action_indexes=force_action_indexes,
            ignore_action_indexes=ignore_action_indexes)
        # end if
    # end def perform_pre_reset_actions

    @staticmethod
    def get_post_reset_actions(test_case):
        """
        Retrieve the list of the post reset actions.

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        """
        return list(
            RECOVERY_KEYS_LIST_MAP[
               test_case.f.PRODUCT.DEVICE.CONNECTION_SCHEME.DEVICE_RECOVERY.F_RecoveryKeysVariant][POST_RESET_ACTIONS])
    # end def get_post_reset_actions

    @classmethod
    def perform_post_reset_actions(cls, test_case, force_action_indexes=None, ignore_action_indexes=None):
        """
        Perform the post reset keystrokes.

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param force_action_indexes: indexes to be kept in the list
        :type force_action_indexes: ``list[int]``
        :param ignore_action_indexes: indexes to be removed from the list
        :type ignore_action_indexes: ``list[int]``
        """
        action_list = cls.get_post_reset_actions(test_case=test_case)

        cls.filter_and_perform_actions(
            test_case=test_case,
            action_list=action_list,
            force_action_indexes=force_action_indexes,
            ignore_action_indexes=ignore_action_indexes)
    # end def perform_post_reset_actions

    @staticmethod
    def perform_restart_action_for_recovery(test_case):
        """
        Perform the restart action to jump on recovery

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        """
        is_hub_present = LibusbDriver.discover_usb_hub()

        assert test_case.power_supply_emulator is not None or is_hub_present or test_case.device_debugger is not None, \
            "Nothing can be used to perform restart"

        if test_case.device_debugger is not None:
            test_case.device_debugger.reset(soft_reset=False)
            time.sleep(1)
        elif test_case.power_supply_emulator is not None:
            test_case.power_supply_emulator.turn_off()
            test_case.device_debugger.close()

            if is_hub_present and isinstance(test_case, DeviceBaseTestCase):
                if test_case.is_device_corded_or_platform():
                    test_case.turn_off_corded_device_or_platform()
                else:
                    test_case.device.turn_off_usb_charging_cable()
                # end if
            # end if

            time.sleep(.5)

            if is_hub_present and isinstance(test_case, DeviceBaseTestCase):
                if test_case.is_device_corded_or_platform():
                    test_case.turn_on_corded_device_or_platform()
                else:
                    test_case.device.turn_on_usb_charging_cable()
                # end if
            # end if

            test_case.power_supply_emulator.turn_on()
            test_case.device_debugger.open()
        elif is_hub_present and isinstance(test_case, DeviceBaseTestCase) and test_case.is_device_corded_or_platform():
            test_case.turn_off_corded_device_or_platform()
            time.sleep(.5)
            test_case.turn_on_corded_device_or_platform()
        # end if
    # end def perform_restart_action_for_recovery

    @classmethod
    def discover_recovery_bootloader(cls, test_case):
        """
        Start discovery and return the address of the first device in recovery with the right unit ID.

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :return: The bluetooth address of the first device in recovery with the right unit ID
        :rtype: ``HexList`` or ``str``
        """
        DiscoveryTestUtils.start_discovery(test_case=test_case)
        return cls.get_discovered_recovery_device(test_case=test_case)
    # end def discover_recovery_bootloader

    @staticmethod
    def get_discovered_recovery_device(test_case, cancel_discovery_when_found=True):
        """
        Get the address of the first device in recovery with the right unit ID. The discovery must have been started
        before the call of this function

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param cancel_discovery_when_found: If True, the discovery will be canceled after finding a device
        :type cancel_discovery_when_found: ``bool``

        :return: The bluetooth address of the first device in recovery with the right unit ID
        :rtype: ``HexList`` or ``str``
        """
        if test_case.config_manager.current_target == ConfigurationManager.TARGET.DEVICE:
            unit_ids = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_UnitId
        elif test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
            unit_ids = test_case.f.SHARED.DEVICES.F_UnitIds_1
        else:
            warn(message="Unknown target in ConfigurationManager")
            unit_ids = None
        # end if

        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            DeviceManagerUtils.set_channel(
                test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
        # end if

        # Allow 2 devices to be in recovery mode at the same time: 10 groups of notifications * 3 messages per group
        max_msg_cnt = 10 * 3 * 2
        while max_msg_cnt > 0:
            recovery_notification = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                class_type=DeviceRecovery,
                timeout=4,
                check_first_message=False)

            if recovery_notification.notification_part == DeviceRecovery.PART.CONFIGURATION:
                unit_id_in_notification = str(recovery_notification.data.unit_id)
                if unit_id_in_notification in unit_ids:
                    bluetooth_address = recovery_notification.data.bluetooth_address
                    notification_counter = recovery_notification.notification_counter
                    for part in [DeviceRecovery.PART.NAME_1, DeviceRecovery.PART.NAME_2, DeviceRecovery.PART.NAME_3]:
                        recovery_notification = ChannelUtils.get_only(
                            test_case=test_case,
                            queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                            class_type=DeviceRecovery,
                            check_first_message=False,
                            allow_no_message=True)

                        # Part 2 & 3 are optional and depend on the Device Name length
                        if (recovery_notification is None or
                                recovery_notification.notification_counter > notification_counter):
                            break
                        # end if

                        test_case.assertEquals(
                            expected=part,
                            obtained=recovery_notification.notification_part,
                            msg="Did not receive the right part")
                    # end for
                    if cancel_discovery_when_found:
                        DiscoveryTestUtils.cancel_discovery(test_case=test_case)
                    # end if
                    ChannelUtils.clean_messages(
                        test_case=test_case,
                        queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT,
                        class_type=(DiscoveryStatus, DeviceDiscovery, DeviceRecovery))
                    return bluetooth_address
                # end if
            # end if

            max_msg_cnt -= 1
        # end while

        return None
    # end def get_discovered_recovery_device

    @staticmethod
    def connect_to_recovery_device(test_case, bluetooth_address):
        """
        Connect to a recovery device

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param bluetooth_address: The bluetooth address of the device to connect to
        :type bluetooth_address: ``HexList`` or ``str``
        """
        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            DeviceManagerUtils.set_channel(
                test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
        # end if

        # Send 'Perform device connection' request with all authentication method to 0
        write_device_connect = SetPerformDeviceConnectionRequest(
            connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
            bluetooth_address=bluetooth_address)
        ChannelUtils.send(
            test_case=test_case,
            report=write_device_connect,
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPerformDeviceConnectionResponse)
    # end def connect_to_recovery_device

    @classmethod
    def discover_and_connect_recovery_bootloader(cls, test_case, pairing=False):
        """
        Discover the first device in recovery mode with the right unit ID and connect to it

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param pairing: If True, a pairing will be performed after connection - NOT POSSIBLE FOR NOW, IT HAS TO BE False
        :type pairing:``bool``
        """
        pairing_slot = None
        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            DeviceManagerUtils.set_channel(
                test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
        # end if

        # Add a loop to enable a retry mechanism if the stop status is not received during the pairing.
        for _ in range(2):
            bluetooth_address = cls.discover_recovery_bootloader(test_case=test_case)
            if bluetooth_address is None:
                raise AttributeError(f'No Device Recovery notification found with the configured UnitIds')
            # end if

            # Empty receiver notification queues
            ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.RECEIVER_EVENT)
            ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
            ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR)

            cls.connect_to_recovery_device(test_case=test_case, bluetooth_address=bluetooth_address)

            if pairing:
                assert False, "Controlling pairing is not possible yet, not possible with receiver"
            # end if

            # Receive
            DevicePairingTestUtils.PairingChecker.check_start_pairing_status(test_case=test_case)

            try:
                pairing_slot = int(Numeral(DevicePairingTestUtils.PairingChecker.check_stop_pairing_status(
                    test_case=test_case)))
            except (AssertionError, QueueEmpty):
                # Queue still empty after 9 seconds. Retry pairing.
                test_case.log_warning('No PairingStatus message received after 9s')
                continue
            # end try
            break
        # end for

        channel = ThroughBleProReceiverChannel(receiver_channel=test_case.current_channel, device_index=pairing_slot)
        channel.get_transport_id()
        test_case.assertTrue(expr=channel.is_device_connected(), msg="Device on recovery not connected")
        DeviceManagerUtils.add_channel_to_cache(test_case=test_case, channel=channel)

        DeviceManagerUtils.set_channel(test_case=test_case, new_channel=channel)

        test_case.config_manager.current_mode = test_case.config_manager.MODE.BOOTLOADER
    # end def discover_and_connect_recovery_bootloader

    @staticmethod
    def verify_recovery_disconnection(
            test_case,
            disconnection_method_used,
            recovery_device_index,
            application_device_index,
            check_application_connection=True):
        """
        Verify that all notifications associated to the recovery bootloader has been received

        :param test_case: The associated test case
        :type test_case: ``CommonBaseTestCase``
        :param disconnection_method_used: The disconnection method that has been used
        :type disconnection_method_used: ``DisconnectMethod``
        :param recovery_device_index: The device index for the device in recovery
        :type recovery_device_index: ``int``
        :param application_device_index: The device index for the device in application
        :type application_device_index: ``int``
        :param check_application_connection: If True, a check about receiving the DeviceConnection notification with
                                             link established for the application
        :type check_application_connection: ``bool``
        """
        if isinstance(test_case.current_channel, ThroughReceiverChannel):
            DeviceManagerUtils.set_channel(
                test_case=test_case, new_channel=test_case.current_channel.receiver_channel)
        # end if
        
        application_connection = False

        if disconnection_method_used != DisconnectMethod.PERFORM_DEVICE_PAIRING_AND_UNPAIRING:
            # Check received link not established notification
            device_index = 0
            while device_index != recovery_device_index:
                device_connection = ChannelUtils.get_only(
                    test_case=test_case,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                    class_type=DeviceConnection)
                device_index = int(Numeral(device_connection.device_index))
                device_info_class = \
                    test_case.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                if device_index == application_device_index and \
                    int(Numeral(device_info.device_info_link_status)) == \
                        DeviceConnection.LinkStatus.LINK_ESTABLISHED:
                    application_connection = True
                elif device_index == recovery_device_index:
                    test_case.assertEquals(
                        int(Numeral(device_info.device_info_link_status)),
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                        msg=f'The receiver did not disconnect from the device recovery bootloader, {device_info}')
                else:
                    warn(f"Unexpected message received: {device_connection}")
                # end if
            # end while
        # end if

        # Check received DeviceDisconnection meaning pairing slot is cleared
        device_index = 0
        while device_index != recovery_device_index:
            device_disconnection_or_connection = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                class_type=(DeviceDisconnection, DeviceConnection))
            device_index = int(Numeral(device_disconnection_or_connection.device_index))
            if isinstance(device_disconnection_or_connection, DeviceConnection):
                device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                        device_disconnection_or_connection)
                device_info = device_info_class.fromHexList(HexList(device_disconnection_or_connection.information))
                if device_index == application_device_index and int(Numeral(device_info.device_info_link_status)) == \
                        DeviceConnection.LinkStatus.LINK_ESTABLISHED:
                    application_connection = True
                elif device_index == recovery_device_index and int(Numeral(device_info.device_info_link_status)) == \
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED:
                    # Optional link not established notification received during unpairing
                    # cf https://goldenpass.logitech.com:8443/c/ccp_fw/mpr01_gravity/+/8956/1
                    device_index = 0
                # end if
            elif device_index == recovery_device_index:
                test_case.assertEquals(
                    expected=DeviceDisconnection.PERMANENT_DISCONNECTION,
                    obtained=int(Numeral(device_disconnection_or_connection.disconnection_type)),
                    msg=f'The receiver did not disconnect from the device application')
                DeviceManagerUtils.remove_channel_from_cache(
                    test_case=test_case,
                    port_index=ChannelUtils.get_port_index(test_case=test_case),
                    device_index=recovery_device_index)
            else:
                warn(f"Unexpected message received: {device_disconnection_or_connection}")
            # end if
        # end while

        if check_application_connection and not application_connection:
            # Check received link established notification
            device_index = 0
            while device_index != application_device_index:
                device_connection = ChannelUtils.get_only(
                    test_case=test_case,
                    queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT,
                    class_type=DeviceConnection,
                    timeout=3)
                device_index = int(Numeral(device_connection.device_index))
                device_info_class = \
                    test_case.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                if device_index == application_device_index:
                    test_case.assertEquals(
                        expected=DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                        obtained=int(Numeral(device_info.device_info_link_status)),
                        msg=f'The receiver did not connect to application, {device_info}')
                else:
                    warn(f"Unexpected message received: {device_connection}")
                # end if
            # end while
    # end def verify_recovery_disconnection
# end class RecoveryTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
