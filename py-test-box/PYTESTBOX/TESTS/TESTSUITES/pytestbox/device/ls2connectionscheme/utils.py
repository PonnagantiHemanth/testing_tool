#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ls2connectionscheme.utils
:brief: utilities for LS2 connection scheme tests
:author: Zane Lu
:date: 2020/11/3
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep
from pychannel.channelinterfaceclasses import LogitechProtocol
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest, \
    GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection, SetQuadDeviceConnectionRequest, \
    SetQuadDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest, SetConnectionStateResponse
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.enablehidden import EnableHidden, SetEnableHiddenFeatures, SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.common.oobstate import SetOobState, SetOobStateResponse
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.basetest import BaseTestCase
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration
from pyusb.libusbdriver import ChannelIdentifier
from pyusb.libusbdriver import LibusbDriver
from warnings import warn


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class Ls2ConnectionSchemeTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers on device LS2 connection scheme feature
    """

    @staticmethod
    def enable_hidden_features(test_case):
        """
        Enable hidden features 0x1E00
        """
        enable_hidden_features_idx = test_case.updateFeatureMapping(feature_id=EnableHidden.FEATURE_ID)
        set_hidden_req = SetEnableHiddenFeatures(device_index=test_case.deviceIndex,
                                                 feature_index=enable_hidden_features_idx,
                                                 enable_byte=EnableHidden.ENABLED)
        test_case.send_report_wait_response(report=set_hidden_req,
                                            response_queue=test_case.hidDispatcher.common_message_queue,
                                            response_class_type=SetEnableHiddenFeaturesResponse)
    # end def enable_hidden_features

    @staticmethod
    def set_oob_state(test_case):
        """
        Set OOB state 0x1805
        """
        set_oob_state_idx = test_case.updateFeatureMapping(feature_id=SetOobState.FEATURE_ID)
        set_oob_req = SetOobState(device_index=test_case.deviceIndex,
                                  feature_index=set_oob_state_idx)
        test_case.send_report_wait_response(report=set_oob_req,
                                            response_queue=test_case.hidDispatcher.common_message_queue,
                                            response_class_type=SetOobStateResponse)
    # end def set_oob_state

    @staticmethod
    def wait_for_deep_sleep_mode(test_case):
        """
        Wait the device going into deep sleep mode
        """
        # waiting for the device going into deep sleep
        # check the device connection until it is disconnected
        test_case.enable_hidpp_reporting()

        link_status = DeviceConnection.LinkStatus.LINK_ESTABLISHED
        # 30 seconds per loop, 20 times loop
        retry = 0
        max_retries = 20
        one_loop_time = 30
        test_case.logTitle2('waiting the device going into deep sleep')
        while link_status == DeviceConnection.LinkStatus.LINK_ESTABLISHED and retry < max_retries:
            if test_case.is_current_hid_dispatcher_queue_empty(
                    queue=test_case.hidDispatcher.receiver_connection_event_queue):
                sleep(one_loop_time)
                retry += 1
                test_case.logTitle2(f'time passed:{retry * one_loop_time} seconds')
            else:
                device_connection = test_case.getMessage(
                    queue=test_case.hidDispatcher.receiver_connection_event_queue,
                    class_type=DeviceConnection)
                device_info_class = BaseTestCase.get_device_info_bit_field_structure_in_device_connection(
                    device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                link_status = int(Numeral(device_info.device_info_link_status))
            # end if
        # end while
        test_case.assertEqual(obtained=link_status,
                              expected=DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                              msg='The device shall disconnect to the receiver')
    # end def wait_for_deep_sleep_mode

    @staticmethod
    def set_deep_sleep_mode(test_case):
        """
        Make the device go into deep sleep mode
        """
        Ls2ConnectionSchemeTestUtils.disable_all_receiver_usb_ports(test_case)

        test_case.power_supply_emulator.turn_off()
        sleep(0.5)  # wait a moment before turning the power supply on

        test_case.power_supply_emulator.turn_on()

        c = test_case.DEEP_SLEEP_CURRENT_THRESHOLD * 2
        for i in range(5):
            c = Ls2ConnectionSchemeTestUtils.get_current_consumption(test_case)
            test_case.logTitle2(f'loop {i}, current consumption: {c}')
            if c <= test_case.DEEP_SLEEP_CURRENT_THRESHOLD:
                break
            # end if
        # end for

        test_case.assertTrue(expr=(c <= test_case.DEEP_SLEEP_CURRENT_THRESHOLD),
                             msg='The device shall go into the deep sleep mode')
    # end def set_power_modes

    @staticmethod
    def set_receiver_usb_ports(test_case, desired, loops=10):
        """
        Set the receiver ports as the desired status
        """
        ports_status = {}
        for i in range(len(desired)):
            ports_status[PortConfiguration.PORT_ARRANGEMENT[i]] = desired[i]
        # end for

        ready_to_go, retries = test_case.device.set_usb_ports_status(ports_status, loops)

        if ready_to_go and retries > 1:
            warn('It is {} time(s) to set USB ports as desired, current status: {}'.format(retries, desired))
        # end if

        test_case.assertTrue(expr=ready_to_go, msg='The receiver usb ports shall be set correctly')
    # end def set_receiver_usb_ports

    @staticmethod
    def disable_all_receiver_usb_ports(test_case):
        """
        Disable all receiver USB ports
        """
        # here is a weird issue:
        # the port cannot be disabled forever
        # for example, step 1: disable port 1, step 2: disable port 2, step 3: disable port 3
        # after the step 3, the port 1 and 2 are enabled again. why???
        # try to workaround the issue by disabling the ports many times
        Ls2ConnectionSchemeTestUtils.set_receiver_usb_ports(test_case, [False, False, False, False, False])

    # end def disable_all_receiver_usb_ports

    @staticmethod
    def enable_all_usb_ports(test_case):
        """
        Enable all usb ports
        """
        ports_status = {}
        for i in range(PortConfiguration.NUM_OF_RECEIVERS):
            ports_status[PortConfiguration.PORT_ARRANGEMENT[i]] = True
        # end for
        ports_status[PortConfiguration.CABLE_CONNECTED_PORT] = True

        ready_to_go, retries = test_case.device.set_usb_ports_status(ports_status)

        if ready_to_go and retries > 1:
            warn('It is {} time(s) to enable all USB ports'.format(retries))
        # end if

        test_case.assertTrue(expr=ready_to_go, msg='The receiver usb ports shall be set correctly')
    # end def enable_all_usb_ports

    @staticmethod
    def fix_port_not_response_issue(test_case):
        """
        Fix the issue that the low-level drivers can't work correctly when there are many receivers in
        the test environment and the usb hub ports are turned on and off in the test cases.

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        """
        for i in range(PortConfiguration.NUM_OF_RECEIVERS):
            channel = DeviceManagerUtils.get_channel(
                test_case=test_case,
                channel_id=ChannelIdentifier(port_index=PortConfiguration.PORT_ARRANGEMENT[i],
                                             protocol=LogitechProtocol.USB))
            channel.open()
            channel.close()
        # end for
    # end def fix_port_not_response_issue

    @staticmethod
    def switch_to_usb_port(test_case, usb_port_index, force=True):
        """
        Switch the target USB port
        """
        if test_case.receiver_index != usb_port_index or force:
            # the previous port (test_case.receiver_index) should be enabled,
            # otherwise, the script will hang at test_case.device.stop()
            ports_status = test_case.device.get_usb_ports_status()
            previous_port_index = test_case.receiver_index
            if not ports_status[previous_port_index]:
                test_case.device.enable_usb_port(previous_port_index)
            # end if

            test_case.device.enable_usb_port(usb_port_index)
            ChannelUtils.close_channel(test_case=test_case)
            sleep(2)
            new_channel = DeviceManagerUtils.get_channel(
                test_case=test_case, channel_id=ChannelIdentifier(port_index=usb_port_index))
            DeviceManagerUtils.set_channel(test_case=test_case, new_channel=new_channel)
            sleep(2)
            test_case.receiver_index = usb_port_index
            test_case.hidDispatcher.dut_port_index = usb_port_index
            if usb_port_index == PortConfiguration.CABLE_CONNECTED_PORT:
                test_case.hidDispatcher.dut_device_index = Hidpp1Data.DeviceIndex.TRANSCEIVER
            else:
                test_case.hidDispatcher.dut_device_index = 1
            # end if
        # end if
    # end def switch_to_usb_port

    @staticmethod
    def check_receiver_arrangement(test_case, receiver_pids):
        """
        Check the receiver arrangement as desired
        """
        for i in range(len(receiver_pids)):
            port = receiver_pids[i][0]
            pid = receiver_pids[i][1]
            test_case.assertEqual(obtained=str(LibusbDriver.powerUp(test_case.device, port)).lower(),
                                  expected=("{:04x}".format(LibusbDriver.LOGI_VENDOR_ID)
                                            + "{:04x}".format(pid)).lower(),
                                  msg=f"Incorrect receiver arrangement for the port {port + 1}")
            # end if
        # end for
    # end def check_receiver_arrangement

    @staticmethod
    def check_device_connection_via_usb_cable(test_case, usb_port_index):
        """
        Check the device is connected via USB cable
        """
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(test_case, usb_port_index)

        DeviceInformationTestUtils.HIDppHelper.get_fw_info(test_case=test_case, entity_index=0)
    # end def check_device_connection_via_usb_cable

    @staticmethod
    def open_lock_equad_receiver(test_case, receiver_usb_port,
                                 connect_devices=QuadDeviceConnection.ConnectDevices.OPEN_LOCK):
        """
        Open-lock an EQUAD receiver
        """
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(test_case, receiver_usb_port)
        device_connection_req = SetQuadDeviceConnectionRequest(
            connect_devices=connect_devices,
            device_number=0x00,
            open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
        )

        test_case.send_report_wait_response(
            report=device_connection_req,
            response_queue=test_case.hidDispatcher.receiver_response_queue,
            response_class_type=SetQuadDeviceConnectionResponse)
    # end def open_lock_equad_receiver

    @staticmethod
    def unpair_equad_receiver(test_case, receiver_usb_port, device_index=0x01):
        """
        Unpair an EQUAD receiver
        """
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(test_case, receiver_usb_port)
        if Ls2ConnectionSchemeTestUtils.get_paired_device_name(test_case, receiver_usb_port, device_index - 1) \
                is not None:
            device_connection_req = SetQuadDeviceConnectionRequest(
                connect_devices=QuadDeviceConnection.ConnectDevices.DISCONNECT_UNPLUG,
                device_number=device_index,
                open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
            )

            test_case.send_report_wait_response(
                report=device_connection_req,
                response_queue=test_case.hidDispatcher.receiver_response_queue,
                response_class_type=SetQuadDeviceConnectionResponse)
    # end def unpair_equad_receiver

    @staticmethod
    def get_paired_device_name(test_case, receiver_usb_port, device_index):
        """
        Get the paired device name on the specific receiver
        """
        Ls2ConnectionSchemeTestUtils.switch_to_usb_port(test_case, receiver_usb_port)
        device_name_req = GetEQuadDeviceNameRequest(NonVolatilePairingInformation.R0.EQUAD_STEP4_DEVICE_NAME_MIN
                                                    + device_index)
        test_case.send_report_to_device(device_name_req)
        sleep(0.5)
        resp = test_case.clean_message_type_in_queue(test_case.hidDispatcher.receiver_response_queue,
                                                     GetEQuadDeviceNameResponse)
        err_resp = test_case.clean_message_type_in_queue(
            test_case.hidDispatcher.receiver_error_message_queue, Hidpp1ErrorCodes)
        if len(err_resp) != 0 or len(resp) == 0:
            return None
        else:
            return resp[0].name_string
    # end def get_device_name

    @staticmethod
    def get_current_consumption(test_case):
        """
        Get the current consumption
        """
        # The debugger will affect the current measurement result, shall close it before doing test!
        if test_case.debugger:
            test_case.debugger.close()
        # end if
        # Shall disconnect to J-Link before doing current measurement
        test_case.jlink_connection_control.disconnect()
        test_case.power_supply_emulator.configure_measurement_mode("current")
        current_sum = 0
        count = 0
        sleep(60)
        for x in range(150):
            count += 1
            current_sum += test_case.power_supply_emulator.get_current() * 1000
            sleep(.2)
        # end for
        test_case.assertGreater(a=count, b=0)
        current_value = current_sum // count
        test_case.power_supply_emulator.configure_measurement_mode("tension")
        test_case.jlink_connection_control.connect()

        return current_value
    # end def get_current_consumption

# end class Ls2ConnectionSchemeTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
