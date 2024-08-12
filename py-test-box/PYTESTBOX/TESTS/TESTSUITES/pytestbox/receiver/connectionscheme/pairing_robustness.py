#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.receiver.connectionscheme.pairing_robustness
    :brief: Validates 'device pairing' feature
    :author: Christophe Roquebert
    :date: 2020/04/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.hidpp1.notifications.deviceconnection import BLEProReceiverInformation
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import NonVolatilePairingInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import compute_inf_values
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.enumerationutils import EnumerationTestUtils
from pytestbox.shared.connectionscheme.pairing_robustness import SharedPairingRobustnessTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PairingRobustnessTestCase(SharedPairingRobustnessTestCase, ReceiverBaseTestCase):
    """
    Receiver Pairing Robustness TestCases
    """
    def setUp(self):
        """
        Handles test prerequisites.
        """
        self.post_requisite_turn_on = False

        super().setUp()
    # end def setUp

    def tearDown(self):
        """
        Handles test post-requisites.
        """
        # noinspection PyBroadException
        try:
            if self.post_requisite_turn_on and self.device_debugger is not None:
                self.device_debugger.run()
                self.post_requisite_turn_on = False
            # end if
        except Exception:
            self.log_traceback_as_warning(supplementary_message="Exception in tearDown:")
        # end try
        super().tearDown()
    # end def tearDown

    @features('BLEDevicePairing')
    @level('Robustness')
    def test_bad_device_index(self):
        """
        Invalid Device Index shall raise an error message with SUB ID=0x8F
        """
        auth_method = DevicePairingTestUtils.get_authentication_method(self)
        # ---------------------------------------------------------------------------
        self.logTitle2('Test Loop over device_index invalid range (typical wrong values)')
        # ---------------------------------------------------------------------------
        for wrong_device_index in compute_inf_values(SetPerformDeviceConnectionRequest.DEFAULT.DEVICE_INDEX):
            # ---------------------------------------------------------------------------
            self.logTitle2(f'''Test Step 1: Send 'Perform device connection' request with Connect Devices = 3 and index=
            {wrong_device_index}''')
            # ---------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(device_index=wrong_device_index,
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.PAIRING,
                bluetooth_address=self.device_bluetooth_address, emu_2buttons_auth_method=(auth_method ==
                    SetPerformDeviceConnectionRequest.MASK.EMU_2BUTTONS_AUTH_METHOD),
                passkey_auth_method=(auth_method == SetPerformDeviceConnectionRequest.MASK.PASSKEY_AUTH_METHOD))
            write_device_connect_response = ChannelUtils.send(
                test_case=self,
                report=write_device_connect,
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            self.logTitle2('Test Check 1: Check HID++ 1.0 ERR_UNKNOWN_DEVICE (8) Error Code returned by the device')
            # ---------------------------------------------------------------------------
            self.assertEqual(expected=Hidpp1ErrorCodes.ERR_UNKNOWN_DEVICE,
                             obtained=int(Numeral(write_device_connect_response.errorCode)),
                             msg='The errorCode parameter differs from the one expected')
        # end for

        # ---------------------------------------------------------------------------
        self.logTitle2('Test Step 2: Send Perform Device Discovery to Cancel discovery')
        # ---------------------------------------------------------------------------
        DiscoveryTestUtils.cancel_discovery(self)
        self.clean_message_type_in_queue(self.hidDispatcher.receiver_event_queue,
                                         (DeviceDiscovery, DiscoveryStatus))

        self.testCaseChecked("ROT_DEV_PAIR_0001")
    # end def test_bad_device_index

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_incomplete_pairing_slot_no_enumeration(self):
        """
        Create a inconsistent pairing block by deleting the 0x28 chunk in receiver nvs
         - validate a empty Device Connection notification is returned on a fake device arrival request
         - verify the 0x0A error code returned on 0xB5 0x5n and 0xB5 0x6n requests
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Clean-up receiver pairing slot')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(self)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Roll out the Pairing sequence and retrieve the pairing slot')
        # ---------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Invalidate BLE_BOND_INFO chunk')
        # ---------------------------------------------------------------------------
        self._invalidate_bond_info_chunk(pairing_slots=[pairing_slot])

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Turn off DUT to prevent re-enumeration')
        # ---------------------------------------------------------------------------
        if self.device_debugger is not None:
            self.post_requisite_turn_on = True
            self.device_debugger.stop()
        # end if

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Power off/on the receiver')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Re-enable HID++ reporting
        self.enable_hidpp_reporting()

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        self.send_report_wait_response(report=set_register,
                                       response_queue=self.hidDispatcher.receiver_response_queue,
                                       response_class_type=SetConnectionStateResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate Empty Device Connection notification is received')
        # ---------------------------------------------------------------------------
        device_connection = self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.receiver_connection_event_queue,
            class_type=DeviceConnection,
            allow_no_message=True)
        self.assertIsNotNone(obj=device_connection,
                             msg='DeviceConnection notifications shall have been received')
        while device_connection is not None:
            if pairing_slot == int(Numeral(device_connection.device_index)):
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
            device_connection = self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.receiver_connection_event_queue,
                class_type=DeviceConnection,
                allow_no_message=True)
        # end while

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
        # ---------------------------------------------------------------------------
        error_response = self.send_report_wait_response(
            report=GetBLEProDevicePairingInfoRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot - 1),
            response_queue=self.hidDispatcher.receiver_error_message_queue, response_class_type=Hidpp1ErrorCodes)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate an error is returned with error code '
                                                      'ERR_REQUEST_UNAVAILABLE')
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE,
                         msg='''Reading an ?incomplete (Prepaired) / corrupted? Pairing slot should raise an error 
                                 with error code ERR_REQUEST_UNAVAILABLE.''')

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Read BLE Pro device name request')
        # ---------------------------------------------------------------------------
        device_pairing_info_req = GetBLEProDeviceDeviceNameRequest(
            NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + pairing_slot - 1)
        error_response = self.send_report_wait_response(
            report=device_pairing_info_req, response_queue=self.hidDispatcher.receiver_error_message_queue,
            response_class_type=Hidpp1ErrorCodes)
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate Error message is received with code '
                                                      'ERR_REQUEST_UNAVAILABLE')
        # ---------------------------------------------------------------------------
        self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                         expected=Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE,
                         msg='Reading an unused Pairing slot should raise an error with code ERR_REQUEST_UNAVAILABLE.')

        self.testCaseChecked("ROT_DEV_PAIR_0010")
    # end def test_incomplete_pairing_slot_no_enumeration

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_incomplete_pairing_slot_enumeration(self):
        """
        Create a inconsistent pairing block by deleting the 0x28 chunk in receiver nvs
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Clean-up receiver pairing slot')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(self)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Roll out the Pairing sequence and retrieve the pairing '
                                                             'slot')
        # ---------------------------------------------------------------------------
        pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Invalidate BLE_BOND_INFO chunk')
        # ---------------------------------------------------------------------------
        self._invalidate_bond_info_chunk(pairing_slots=[pairing_slot])

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Power off/on the receiver')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Re-enable HID++ reporting
        self.enable_hidpp_reporting()

        # create user activity to force the device to reconnect
        self.button_stimuli_emulator.user_action()

        # Wait for the device to reconnect and the receiver to finish the re-enumeration
        self.getMessage(queue=self.hidDispatcher.receiver_connection_event_queue, class_type=DeviceConnection)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        self.send_report_wait_response(report=set_register,
                                       response_queue=self.hidDispatcher.receiver_response_queue,
                                       response_class_type=SetConnectionStateResponse)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Check a valid Device Connection notification is received')
        # ---------------------------------------------------------------------------
        device_connection = self.get_first_message_type_in_queue(
            queue=self.hidDispatcher.receiver_connection_event_queue,
            class_type=DeviceConnection,
            allow_no_message=True)
        self.assertIsNotNone(obj=device_connection,
                             msg='DeviceConnection notifications shall have been received')
        while device_connection is not None:
            if pairing_slot == int(Numeral(device_connection.device_index)):
                device_info = BLEProReceiverInformation.fromHexList(HexList(device_connection.information))
                self.assertTrue(to_int(device_connection.protocol_type) == DeviceConnection.ProtocolTypes.BLE_PRO,
                                msg='Protocol type shall be BLE PRO')
                self.assertTrue(to_int(device_info.device_info_link_status) ==
                                DeviceConnection.LinkStatus.LINK_ESTABLISHED,
                                msg='Device Info Link Status shall be set to established')
                break
            # end if
            device_connection = self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.receiver_connection_event_queue,
                class_type=DeviceConnection,
                allow_no_message=True)
        # end while

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
        # ---------------------------------------------------------------------------
        f = self.getFeatures()
        device_name_resp = EnumerationTestUtils.get_device_pairing_information(self, pairing_slot=pairing_slot)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_check(self, 'Validate BLE PRo device pairing information response is '
                                                      'received')
        # ---------------------------------------------------------------------------
        self.assertTrue(str(HexList(device_name_resp.device_unit_id)) in f.SHARED.DEVICES.F_UnitIds_1,
                        msg=f'Wrong device_unit_id parameter ({HexList(device_name_resp.device_unit_id)}) '
                            f'received in Get BLE Pro Device PairingInfo Response')

        self.testCaseChecked("ROT_DEV_PAIR_0011")
    # end def test_incomplete_pairing_slot_enumeration

    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_unpair_incomplete_pairing_slot(self):
        """
        Create a inconsistent pairing block by deleting the 0x28 chunk in receiver nvs
         - validate we can unpair the ghost pairing slot
        """
        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Clean-up receiver pairing slot')
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.unpair_all(self)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Roll out 5 Pairing sequences')
        # ---------------------------------------------------------------------------
        self.pairing_slot_list = []
        current_pairing_slot = None
        for i in range(DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT-1):
            # Retrieve current device BT address
            self.device_bluetooth_address = DiscoveryTestUtils.discover_device(self)

            if current_pairing_slot is not None:
                # Previous connection is lost when starting the new sequence
                device_connection = self.getMessage(
                    queue=self.hidDispatcher.receiver_connection_event_queue, class_type=DeviceConnection)

                device_info_class = self.get_device_info_bit_field_structure_in_device_connection(device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))
                assert (int(Numeral(device_info.device_info_link_status)) ==
                        DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED)
            # end if
            # Pair the discovered device
            current_pairing_slot = DevicePairingTestUtils.pair_device(self, self.device_bluetooth_address)
            self.pairing_slot_list.append(current_pairing_slot)
            if current_pairing_slot == DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT:
                break
            # end if
        # end for

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Invalidate BLE_BOND_INFO chunk')
        # ---------------------------------------------------------------------------
        slots = list(range(2, DevicePairingTestUtils.NvsManager.RECEIVER_PAIRING_SLOT_COUNT))
        self._invalidate_bond_info_chunk(pairing_slots=slots)

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_prerequisite(self, 'Power off/on the receiver')
        # ---------------------------------------------------------------------------
        self.reset(hardware_reset=True)
        # Re-enable HID++ reporting
        self.enable_hidpp_reporting()

        # ---------------------------------------------------------------------------
        CommonBaseTestUtils.LogHelper.log_step(self, 'Send a fake device arrival request')
        # --------------------------------------------------------------------------
        set_register = SetConnectionStateRequest(write_action_on_connection_fake_device_arrival=1)
        self.send_report_wait_response(report=set_register,
                                       response_queue=self.hidDispatcher.receiver_response_queue,
                                       response_class_type=SetConnectionStateResponse)

        for pairing_slot in slots:
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate Empty Device Connection notification is received')
            # ---------------------------------------------------------------------------
            device_connection = self.get_first_message_type_in_queue(
                queue=self.hidDispatcher.receiver_connection_event_queue,
                class_type=DeviceConnection,
                allow_no_message=True)
            self.assertIsNotNone(obj=device_connection,
                                 msg='DeviceConnection notifications shall have been received')
            while device_connection is not None:
                if pairing_slot == int(Numeral(device_connection.device_index)):
                    device_info = BLEProReceiverInformation.fromHexList(HexList(device_connection.information))
                    self.assertTrue(to_int(device_connection.protocol_type) == 0, msg='Protocol type shall be null')
                    self.assertTrue(to_int(device_info.bluetooth_pid_lsb) == 0, msg='Bluetooth PID LSB shall be null')
                    self.assertTrue(to_int(device_info.bluetooth_pid_msb) == 0, msg='Bluetooth PID LSB shall be null')
                    self.assertTrue(to_int(device_info.device_info_link_status) ==
                                    DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED,
                                    msg='Device Info Link Status shall be set to not established')
                    self.assertTrue(to_int(device_info.device_info_device_type) == 0,
                                    msg='Device Info Device Type shall be null')
                    break
                # end if
                device_connection = self.get_first_message_type_in_queue(
                    queue=self.hidDispatcher.receiver_connection_event_queue,
                    class_type=DeviceConnection,
                    allow_no_message=True)
            # end while
        # end for

        # Empty connection event message queue
        self.empty_queue(queue=self.hidDispatcher.receiver_connection_event_queue)

        for pairing_slot in slots:
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send Read BLE Pro device pairing information request')
            # ---------------------------------------------------------------------------
            error_response = self.send_report_wait_response(
                report=GetBLEProDevicePairingInfoRequest(
                    NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_PAIRING_INFO_MIN + pairing_slot - 1),
                response_queue=self.hidDispatcher.receiver_error_message_queue, response_class_type=Hidpp1ErrorCodes)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Validate an error is returned with error code '
                                                    'ERR_REQUEST_UNAVAILABLE')
            # ---------------------------------------------------------------------------
            self.assertEqual(obtained=int(Numeral(error_response.errorCode)),
                             expected=Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE,
                             msg='''Reading an ?incomplete (Prepaired) / corrupted? Pairing slot should raise an error 
                                     with error code ERR_REQUEST_UNAVAILABLE.''')

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Send Read BLE Pro device name request')
            # ---------------------------------------------------------------------------
            device_pairing_info_req = GetBLEProDeviceDeviceNameRequest(
                NonVolatilePairingInformation.R0.BLE_PRO_DEVICE_DEVICE_NAME_MIN + pairing_slot - 1)
            error_response = self.send_report_wait_response(
                report=device_pairing_info_req, response_queue=self.hidDispatcher.receiver_error_message_queue,
                response_class_type=Hidpp1ErrorCodes)
            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check Error message is received with code '
                                                          'ERR_REQUEST_UNAVAILABLE')
            # ---------------------------------------------------------------------------
            self.assertEqual(
                obtained=int(Numeral(error_response.errorCode)), expected=Hidpp1ErrorCodes.ERR_REQUEST_UNAVAILABLE,
                msg='Reading an unused Pairing slot should raise an error with code ERR_REQUEST_UNAVAILABLE.')

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_step(self, 'Perform device connection request with Connect Devices=3 '
                                                         '(Unpair)')
            # ---------------------------------------------------------------------------
            write_device_connect = SetPerformDeviceConnectionRequest(
                connect_devices=SetPerformDeviceConnectionRequest.ConnectState.UNPAIRING,
                bluetooth_address=self.device_bluetooth_address,
                pairing_slot_to_be_unpaired=pairing_slot)
            write_device_connect_response = self.send_report_wait_response(
                report=write_device_connect, response_queue=self.hidDispatcher.receiver_response_queue,
                response_class_type=SetPerformDeviceConnectionResponse)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check the response to the Write command is success')
            # ---------------------------------------------------------------------------
            DevicePairingTestUtils.PerformDeviceConnectionResponseChecker.check_fields(
                self, write_device_connect_response, SetPerformDeviceConnectionResponse)

            # ---------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(self, 'Check Device disconnection notification received')
            # ---------------------------------------------------------------------------
            device_disconnection = self.getMessage(queue=self.hidDispatcher.receiver_connection_event_queue,
                                                   class_type=DeviceDisconnection)
            self.assertTrue(int(Numeral(device_disconnection.disconnection_type)) ==
                            DeviceDisconnection.PERMANENT_DISCONNECTION,
                            msg='Wrong disconnection_type parameter received in device disconnection notification')
            self.assertTrue(int(Numeral(device_disconnection.pairing_slot)) == pairing_slot,
                            msg='Wrong pairing_slot parameter received in device disconnection notification')
        # end for

        self.testCaseChecked("ROT_DEV_PAIR_0012")
    # end def test_unpair_incomplete_pairing_slot

    def _invalidate_bond_info_chunk(self, pairing_slots):
        """
        Invalidate the receiver NVS_BLE_BOND_INFO_ID_V0_x chunk (id in [0x0128.. 0x012F]) and
        NVS_BLE_BOND_INFO_ID_x chunk (id in [0x0138.. 0x013F])

        :param pairing_slots: slots to invalidate
        :type pairing_slots: ``list of int``
        """
        chunk_name_list = []
        self.memory_manager.read_nvs()
        for slot in pairing_slots:
            chunk_name_list.append(f'NVS_BLE_BOND_INFO_ID_V0_{slot-1}')
            chunk_name_list.append(f'NVS_BLE_BOND_INFO_ID_{slot-1}')
        # end for
        invalidated_chunk_count = self.memory_manager.invalidate_chunks(chunk_name_list)
        assert(invalidated_chunk_count > 0)
        CommonBaseTestUtils.load_nvs(self)
    # end def _invalidate_bond_info_chunk

# end class PairingRobustnessTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
