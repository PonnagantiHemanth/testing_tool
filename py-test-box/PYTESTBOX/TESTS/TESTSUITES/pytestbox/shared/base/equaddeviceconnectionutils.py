#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.base.equaddeviceconnectionutils
:brief:  Helpers for EQuad Device Connection
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2022/06/13
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import ChannelException
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pyharness.core import TestException
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.lightspeedprepairing import PrepairingManagement, GetPrepairingData
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.root import Root
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import QuadDeviceConnection
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionResponse
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.lightspeedprepairingutils import LightspeedPrepairingTestUtils
from pytestbox.receiver.base.receiverbasetestutils import ReceiverBaseTestUtils
from pytestbox.receiver.base.receivertestutils import ReceiverTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class EQuadDeviceConnectionUtils(CommonBaseTestUtils):
    """
    Provide helpers for EQuad Device Connection
    """
    MAX_CONNECTION_RETRY = 5
    MAX_DEVICE_INDEX = 7

    # Delay to let the device reset completely (margin included for robustness)
    RESET_DELAY = 5.0

    class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
        # See ``CommonBaseTestUtils.HIDppHelper``
        @staticmethod
        def device_connection(test_case):
            """
            Connect EQuad device

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            """
            quad_device_connect_req = SetQuadDeviceConnectionRequest(
                connect_devices=QuadDeviceConnection.ConnectDevices.OPEN_LOCK,
                device_number=QuadDeviceConnection.DeviceNumber.NOT_APPLICABLE,
                open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
            )
            ChannelUtils.send(
                test_case=test_case,
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                report=quad_device_connect_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetQuadDeviceConnectionResponse
            )
        # end def device_connection

        @staticmethod
        def device_disconnection(test_case, device_index=0x00):
            """
            Disconnect EQuad device

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            """
            quad_device_connect_req = SetQuadDeviceConnectionRequest(
                connect_devices=QuadDeviceConnection.ConnectDevices.DISCONNECT_UNPLUG,
                device_number=device_index,
                open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
            )
            ChannelUtils.send(
                test_case=test_case,
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                report=quad_device_connect_req,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetQuadDeviceConnectionResponse
            )
        # end def device_disconnection
    # end class HIDppHelper

    @classmethod
    def new_device_connection(cls, test_case, unit_ids, disconnect=False, retry=MAX_CONNECTION_RETRY):
        """
        Perform new device connection

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param unit_ids: Possible Unit Ids of the device to connect
        :type unit_ids: ``list[int|HexList|str]``
        :param disconnect: Flag to disconnect the device before starting the new connection - OPTIONAL
        :type disconnect: ``bool``
        :param retry: Maximum retries, in case of failure - OPTIONAL
        :type retry: ``int``

        :raise ``TestException``: If Unit Id of the new connected device does not match the expected one
        """
        if disconnect:
            device_index = 1
            err_resp = None
            while err_resp is None and device_index <= cls.MAX_DEVICE_INDEX:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case=test_case, msg=f'Disconnect device {device_index}')
                # ------------------------------------------------------------------------------------------------------
                quad_device_connect_req = SetQuadDeviceConnectionRequest(
                    connect_devices=QuadDeviceConnection.ConnectDevices.DISCONNECT_UNPLUG,
                    device_number=device_index,
                    open_lock_timeout=QuadDeviceConnection.OpenLockTimeout.USE_DEFAULT
                )
                try:
                    ChannelUtils.send(
                        test_case=test_case,
                        channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                        report=quad_device_connect_req,
                        response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                        response_class_type=SetQuadDeviceConnectionResponse
                    )
                    device_index += 1
                except (AssertionError, QueueEmpty):
                    err_resp = ChannelUtils.get_only(test_case=test_case,
                                                     channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                                                     queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                                     class_type=Hidpp1ErrorCodes)
                    ReceiverBaseTestUtils.HIDppHelper.check_hidpp10_error_message(
                        test_case,
                        err_resp,
                        to_int(quad_device_connect_req.sub_id),
                        to_int(quad_device_connect_req.address),
                        [Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE])
                # end try
            # end while
        # end if

        ChannelUtils.clean_messages(
            test_case=test_case, channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=Hidpp1Message)
        ChannelUtils.clean_messages(
            test_case=test_case, channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR, class_type=Hidpp1ErrorCodes)

        # Remove potential dead channel (for example if an unpair was performed)
        test_case.device.refresh_through_receiver_channel_cache()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg='Perform new device connection')
        # --------------------------------------------------------------------------------------------------------------
        EQuadDeviceConnectionUtils.HIDppHelper.device_connection(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg='Perform an user action to keep the device in run mode')
        # --------------------------------------------------------------------------------------------------------------
        test_case.button_stimuli_emulator.user_action()

        if test_case.f.PRODUCT.FEATURES.MOUSE.F_LsConnectionButton and \
                KEY_ID.BUTTON_16 in test_case.button_stimuli_emulator.connected_key_ids:
            # For original CI node to do the pairing procedure on a mouse
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f'Long press Connection Button for 3 seconds')
            # ----------------------------------------------------------------------------------------------------------
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.BUTTON_16,
                                                        duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
        elif (not test_case.config_manager.get_feature(ConfigurationManager.ID.IS_PLATFORM) and
              KEY_ID.CONNECT_BUTTON in test_case.button_stimuli_emulator.connected_key_ids):
            # For Kosmos to do the pairing procedure on a mouse
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f'Long press {KEY_ID.CONNECT_BUTTON!s} for 3 seconds')
            # ----------------------------------------------------------------------------------------------------------
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON,
                                                        duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
        elif KEY_ID.LS2_BLE_CONNECTION_TOGGLE in test_case.button_stimuli_emulator.connected_key_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case,
                               msg=f'Long press {KEY_ID.LS2_BLE_CONNECTION_TOGGLE!s} for 3 seconds')
            # ----------------------------------------------------------------------------------------------------------
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_BLE_CONNECTION_TOGGLE,
                                                        duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
        elif KEY_ID.LS2_CONNECTION in test_case.button_stimuli_emulator.connected_key_ids:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg=f'Long press {KEY_ID.LS2_CONNECTION!s} for 3 seconds')
            # ----------------------------------------------------------------------------------------------------------
            test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_CONNECTION,
                                                        duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg='Reset device')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=test_case, delay=cls.RESET_DELAY)
        # end if

        ChannelUtils.clean_messages(
            test_case=test_case, channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT, class_type=Hidpp1Message)
        ChannelUtils.clean_messages(
            test_case=test_case, channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR, class_type=Hidpp1ErrorCodes)

        try:
            device_channel = DeviceManagerUtils.get_channel(
                test_case=test_case,
                channel_id=ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=test_case),
                                             transport_id=test_case.f.PRODUCT.F_EQuadPID)
            )

            if device_channel is None:
                channel_receiver = ChannelUtils.get_receiver_channel(test_case=test_case)
                new_channel = ThroughEQuadReceiverChannel(receiver_channel=channel_receiver, device_index=1)
                new_channel.get_transport_id()
                new_channel.is_device_connected()
                DeviceManagerUtils.add_channel_to_cache(test_case=test_case, channel=new_channel)
                device_channel = new_channel

                assert device_channel is not None, "No new channel was found after the pairing procedure was done"
            # end if

            if not device_channel.is_device_connected(force_refresh_cache=True):
                ChannelUtils.wait_for_channel_device_to_be_connected(
                    test_case=test_case, channel=device_channel, open_channel=True)
            else:
                ChannelUtils.open_channel(test_case=test_case, channel=device_channel)
            # end if

            root_version = test_case.config_manager.get_feature_version(test_case.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
            device_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case,
                               msg='Check Unit Id is expected to be sure to be paired with the expected device')
            # ----------------------------------------------------------------------------------------------------------
            test_case.current_channel = device_channel
            new_unit_id = DeviceInformationTestUtils.HIDppHelper.get_device_info(
                test_case=test_case, device_index=ChannelUtils.get_device_index(test_case, device_channel)).unit_id
            test_case.assertIn(
                member=str(new_unit_id),
                container=[str(unit_id) for unit_id in unit_ids],
                msg="Unit Id should match one of the expected one, i.e. expected device should be connected")
        except (TestException, AssertionError, ChannelException):
            test_case.current_channel = test_case.backup_dut_channel
            retry -= 1
            if retry:
                cls.new_device_connection(test_case=test_case, unit_ids=unit_ids, disconnect=disconnect, retry=retry)
            else:
                raise
            # end if
        # end try
    # end def new_device_connection

    @classmethod
    def new_device_connection_and_pre_pairing(cls, test_case, unit_ids, disconnect=False, pre_pairing=True,
                                              retry=MAX_CONNECTION_RETRY):
        """
        Perform new device connection and pre-pairing

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param unit_ids: Possible Unit Ids of the device to connect
        :type unit_ids: ``list[int|HexList|str]``
        :param disconnect: Flag to disconnect the device before starting the new connection - OPTIONAL
        :type disconnect: ``bool``
        :param pre_pairing: Flag to perform the pre-pairing procedure - OPTIONAL
        :type pre_pairing: ``bool``
        :param retry: Maximum retries, in case of failure - OPTIONAL
        :type retry: ``int``

        :return: A list of channels from the device manager
        :rtype: ``BaseCommunicationChannel`` or ``None``

        :raise ``TestException``: If Unit Id of the new connected device does not match the expected one
        """
        cls.new_device_connection(test_case=test_case, unit_ids=unit_ids, disconnect=disconnect, retry=retry)

        device_channel = DeviceManagerUtils.get_channel(
            test_case=test_case,
            channel_id=ChannelIdentifier(port_index=ChannelUtils.get_port_index(test_case=test_case),
                                         transport_id=test_case.f.PRODUCT.F_EQuadPID)
        )
        assert device_channel is not None, "Device channel should not be None after the pairing procedure was done"

        device_index = ChannelUtils.get_device_index(test_case, device_channel)
        test_case.assertEqual(
            expected=0x01, obtained=device_index, msg='Device index is expected to be 0x01 when a node is setup')
        test_case.pairing_slot = device_index
        test_case.current_channel = device_channel
        ChannelUtils.open_channel(test_case=test_case)
        root_version = test_case.config_manager.get_feature_version(test_case.f.PRODUCT.FEATURES.IMPORTANT.ROOT)
        test_case.current_channel.hid_dispatcher.add_feature_entry(Root.FEATURE_INDEX, Root.FEATURE_ID, root_version)

        if pre_pairing:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Enable Manufacturing Features')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(
                test_case=test_case, manufacturing=True, device_index=test_case.pairing_slot)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Get EQuad attributes of paired device")
            # ----------------------------------------------------------------------------------------------------------
            LightspeedPrepairingTestUtils.HIDppHelper.prepairing_management(
                test_case=test_case,
                ls2=False,
                crush=False,
                ls=True,
                prepairing_management_control=PrepairingManagement.Control.START)
            paired_device_equad_attributes = LightspeedPrepairingTestUtils.HIDppHelper.get_prepairing_data(
                test_case=test_case,
                information_type=GetPrepairingData.InfoType.PAIRING,
                data_type=GetPrepairingData.DataType.EQUAD_ATTRIBUTES).data.equad_attributes

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Get receiver pairing information")
            # ----------------------------------------------------------------------------------------------------------
            equad_info, pairing_info, extended_pairing_info, equad_name, fw_information = \
                ReceiverTestUtils.get_receiver_nv_pairing_info(test_case=test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Start device pre-pairing sequence")
            # ----------------------------------------------------------------------------------------------------------
            long_term_key = LightspeedPrepairingTestUtils.pre_pairing_sequence(
                test_case=test_case,
                slot_index=PrepairingManagement.PairingSlot.LS,
                base_address=equad_info.base_address,
                last_dest_id=equad_info.last_dest_id,
                equad_attributes=paired_device_equad_attributes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Send 0x1805.SetOobState request")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.HIDppHelper.set_oob_state(test_case=test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Perform a device reset")
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ResetHelper.hidpp_reset(test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Start receiver pre-pairing sequence")
            # ----------------------------------------------------------------------------------------------------------
            ReceiverTestUtils.perform_receiver_pre_pairing_sequence(test_case=test_case,
                                                                    equad_info=equad_info,
                                                                    pairing_info=pairing_info,
                                                                    extended_pairing_info=extended_pairing_info,
                                                                    equad_name=equad_name,
                                                                    long_term_key=long_term_key,
                                                                    skip_link_established_verification=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, 'Perform a device hardware reset')
            # ----------------------------------------------------------------------------------------------------------
            DeviceBaseTestUtils.ResetHelper.hardware_reset(test_case=test_case,
                                                           delay=EQuadDeviceConnectionUtils.RESET_DELAY)
        # end if

        return device_channel
    # end def new_device_connection_and_pre_pairing
# end class EQuadDeviceConnectionUtils
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
