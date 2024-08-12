#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pytestbox.shared.base.bleproreceiverprepairingutils
    :brief:  Helpers for BLE Pro Receiver Pre Pairing feature
    :author: Martin Cryonnet
    :date: 2020/06/11
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.throughreceiverchannel import ThroughReceiverChannel, ThroughBleProReceiverChannel
from pychannel.usbchannel import UsbChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.hidpp1.registers.prepairingdata import PrepairingData, GetPrepairingDataRequest, \
    GetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingdata import SetPrepairingDataRequest, SetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import PrepairingManagement
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementRequest
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementResponse
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralRequest, SetCSRKKeyCentralResponse
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralRequest, SetCSRKKeyPeripheralResponse
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralRequest, SetIRKKeyCentralResponse
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralRequest, SetIRKKeyPeripheralResponse
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyRequest, SetLTKKeyResponse
from pyhid.hidpp.hidpp1.registers.randomdata import GetRandomDataRequest
from pyhid.hidpp.hidpp1.registers.randomdata import GetRandomDataResponse
from pylibrary.tools.numeral import Numeral
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.devicemanagerutils import DeviceManagerUtils
from pytestbox.device.base.bleproprepairingutils import BleProPrePairingTestUtils
from pyusb.libusbdriver import ChannelIdentifier


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleProReceiverPrepairingTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for common checks on Receiver Prepairing features
    """
    @staticmethod
    def set_prepairing_management(test_case, pairing_slot, prepairing_management_control):
        """
        Send Prepairing Management Write request
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=SetPrepairingManagementRequest(pairing_slot, prepairing_management_control),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPrepairingManagementResponse
        )
    # end def set_prepairing_management

    @staticmethod
    def set_prepairing_data(test_case, data_type, address):
        """
        Send Prepairing Management Write request
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=SetPrepairingDataRequest(data_type, address),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=SetPrepairingDataResponse
        )
    # end def set_prepairing_data

    @staticmethod
    def get_prepairing_data(test_case, data_type):
        """
        Send Prepairing Management Write request
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetPrepairingDataRequest(data_type),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetPrepairingDataResponse
        )
    # end def get_prepairing_data

    @staticmethod
    def get_random_data(test_case):
        """
        Send Get Random Data request
        """
        return ChannelUtils.send(
            test_case=test_case,
            report=GetRandomDataRequest(),
            channel=ChannelUtils.get_receiver_channel(test_case=test_case),
            response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
            response_class_type=GetRandomDataResponse)
    # end def get_random_data

    @classmethod
    def get_randomized_key(cls, test_case):
        """
        Retrieve a random number using the receiver 0xF6 regrister
        """
        response = cls.get_random_data(test_case)
        test_case.assertTrue(expr=isinstance(response, GetRandomDataResponse))
        return response.random_data
    # end def get_randomized_key

    @classmethod
    def set_keys(cls, test_case, ltk_key=None, irk_local_key=None, irk_remote_key=None, csrk_local_key=None,
                 csrk_remote_key=None, force_random_data=False):
        """
        Set keys as in the standard sequence

        :param test_case: Current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ltk_key: Long term key
        :type ltk_key: ``HexList``
        :param irk_local_key: IRK Local Key
        :type irk_local_key: ``HexList``
        :param irk_remote_key: IRK Remote Key
        :type irk_remote_key: ``HexList``
        :param csrk_local_key: CSRK Local Key
        :type csrk_local_key: ``HexList``
        :param csrk_remote_key: CSRK Remote Key
        :type csrk_remote_key: ``HexList``
        :param force_random_data: Flag to enable the generation of the key by calling the 0xF6 Random data request
        :type force_random_data: ``bool``

        :return: LTK, IRK Local, IRK remote, CSRK Local and CSRK remote keys
        :rtype: ``tuple``
        """
        if ltk_key is not None:
            if force_random_data:
                ltk_key = cls.get_randomized_key(test_case)
            # end if
            set_ltk_key_resp = ChannelUtils.send(
                test_case=test_case,
                report=SetLTKKeyRequest(ltk_key),
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetLTKKeyResponse
            )
            cls.MessageChecker.check_fields(test_case, set_ltk_key_resp, SetLTKKeyResponse, {})
        # end if

        if test_case.f.RECEIVER.TDE.F_IRK and irk_local_key is not None:
            if force_random_data:
                irk_local_key = cls.get_randomized_key(test_case)
            # end if
            set_irk_local_key_resp = ChannelUtils.send(
                test_case=test_case,
                report=SetIRKKeyCentralRequest(irk_local_key),
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetIRKKeyCentralResponse
            )
            cls.MessageChecker.check_fields(test_case, set_irk_local_key_resp, SetIRKKeyCentralResponse, {})
        # end if

        if test_case.f.RECEIVER.TDE.F_IRK and irk_remote_key is not None:
            if force_random_data:
                irk_remote_key = cls.get_randomized_key(test_case)
            # end if
            set_irk_remote_key_resp = ChannelUtils.send(
                test_case=test_case,
                report=SetIRKKeyPeripheralRequest(irk_remote_key),
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetIRKKeyPeripheralResponse
            )
            cls.MessageChecker.check_fields(test_case, set_irk_remote_key_resp, SetIRKKeyPeripheralResponse, {})
        # end if

        if test_case.f.RECEIVER.TDE.F_CSRK and csrk_local_key is not None:
            if force_random_data:
                csrk_local_key = cls.get_randomized_key(test_case)
            # end if
            set_csrk_local_key_resp = ChannelUtils.send(
                test_case=test_case,
                report=SetCSRKKeyCentralRequest(csrk_local_key),
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetCSRKKeyCentralResponse
            )
            cls.MessageChecker.check_fields(test_case, set_csrk_local_key_resp, SetCSRKKeyCentralResponse, {})
        # end if

        if test_case.f.RECEIVER.TDE.F_CSRK and csrk_remote_key is not None:
            if force_random_data:
                csrk_remote_key = cls.get_randomized_key(test_case)
            # end if
            set_csrk_remote_key_resp = ChannelUtils.send(
                test_case=test_case,
                report=SetCSRKKeyPeripheralRequest(csrk_remote_key),
                channel=ChannelUtils.get_receiver_channel(test_case=test_case),
                response_queue_name=HIDDispatcher.QueueName.RECEIVER_RESPONSE,
                response_class_type=SetCSRKKeyPeripheralResponse
            )
            cls.MessageChecker.check_fields(test_case, set_csrk_remote_key_resp, SetCSRKKeyPeripheralResponse, {})
        # end if

        return ltk_key, irk_local_key, irk_remote_key, csrk_local_key, csrk_remote_key
    # end def set_keys

    @classmethod
    def receiver_prepairing_sequence(cls, test_case, prepairing_slot, ltk_key, irk_local_key=None, irk_remote_key=None,
                                     csrk_local_key=None, csrk_remote_key=None, device_address=None,
                                     pre_pairing_main_class=None, pre_pairing_index=None, force_random_data=False):
        """
        Perform full standard sequence
        """
        prepairing_management_resp = cls.set_prepairing_management(
            test_case, prepairing_slot, PrepairingManagement.PrepairingManagementControl.START)
        cls.MessageChecker.check_fields(test_case, prepairing_management_resp, SetPrepairingManagementResponse, {})

        ltk_key, irk_local_key, irk_remote_key, csrk_local_key, csrk_remote_key = cls.set_keys(
            test_case, ltk_key, irk_local_key, irk_remote_key, csrk_local_key, csrk_remote_key, force_random_data)

        if device_address is None:
            device_address = BleProPrePairingTestUtils.pre_pairing_start_sequence(
                test_case, pre_pairing_main_class, pre_pairing_index)

        prepairing_data_resp = cls.set_prepairing_data(
            test_case, PrepairingData.DataType.REMOTE_ADDRESS, device_address)
        cls.MessageChecker.check_fields(test_case, prepairing_data_resp, SetPrepairingDataResponse, {})

        receiver_address = cls.get_prepairing_data(test_case, PrepairingData.DataType.LOCAL_ADDRESS).local_address

        prepairing_management_resp = cls.set_prepairing_management(
            test_case, prepairing_slot, PrepairingManagement.PrepairingManagementControl.STORE)
        cls.MessageChecker.check_fields(test_case, prepairing_management_resp, SetPrepairingManagementResponse, {})

        # Since the receiver finished adding
        if DeviceManagerUtils.get_channel(
                test_case=test_case,
                channel_id=ChannelIdentifier(
                    port_index=ChannelUtils.get_port_index(test_case=test_case),
                    device_index=prepairing_slot)) is None:
            if isinstance(test_case.current_channel, UsbChannel):
                current_receiver_channel = test_case.current_channel
            elif isinstance(test_case.current_channel, ThroughReceiverChannel):
                current_receiver_channel = test_case.current_channel.receiver_channel
            else:
                assert False, \
                    "Cannot use this method on a channel other than UsbReceiverChannel or ThroughReceiverChannel"
            # end if

            new_channel = ThroughBleProReceiverChannel(
                receiver_channel=current_receiver_channel, device_index=prepairing_slot)
            DeviceManagerUtils.add_channel_to_cache(test_case=test_case, channel=new_channel)

            test_case.backup_dut_channel.hid_dispatcher.dump_mapping_in_other_dispatcher(
                other_dispatcher=new_channel.hid_dispatcher)
        # end if

        return receiver_address, device_address, ltk_key, irk_local_key, irk_remote_key, csrk_local_key, csrk_remote_key
    # end def

    class GetPrepairingDataResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Prepairing Data response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Default checks
            """
            return {
                "data_type": (cls.check_data_type, PrepairingData.DataType.LOCAL_ADDRESS),
                "local_address": None,  # TODO : (cls.check_ble_address, get local address from NVS)
            }
        # end def get_default_check_map

        @staticmethod
        def check_data_type(test_case, message, expected):
            """
            Check Data Type field
            """
            test_case.assertEqual(obtained=int(Numeral(message.data_type)), expected=expected,
                                  msg="Data Type is not as expected")
        # end def check_data_type

        @staticmethod
        def check_ble_address(test_case, message, expected):
            """
            Check BLE Address (Local or Remote) field
            """
            test_case.assertEqual(obtained=int(Numeral(message.ble_address)), expected=expected,
                                  msg="BLE Address is not as expected")
        # end def check_ble_address
    # end class GetPrepairingDataResponseChecker

    class GetRandomDataResponseChecker(CommonBaseTestUtils.MessageChecker):
        """
        This class provides helpers for common checks on Random Data response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Default checks
            """
            return {
                "random_data": None,
            }
        # end def get_default_check_map
    # end class GetRandomDataResponseChecker
# end class ReceiverPrepairingTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
