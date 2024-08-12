#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.bleproprepairingutils
:brief:  Helpers for BLE Pro Pre-pairing feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2020/06/08
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from functools import reduce

from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairing
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingFactory
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingInterface
from pylibrary.mcu.nrf52.bleproprepairingchunk import BleProPrePairingNvsChunk
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.util import UtilNonNumericEnum
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytransport.ble.bleconstants import BleGenericIntConstant


# ----------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------
MAX_RETRY = 3


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleProPrePairingTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers on device BLE Pro pre-pairing feature
    """

    @classmethod
    def pre_pairing_start_sequence(cls, test_case, pre_pairing_main_class, pre_pairing_index, get_local_address=True):
        """
        Start a pre-pairing sequence with the 'Start' request and retrieve the randomly generated device bluetooth
        address.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pre_pairing_main_class: Device BLE Pro pre-pairing feature main class
        :type pre_pairing_main_class: ``BleProPrepairingVx``
        :param pre_pairing_index: 0x1816 HID++ feature index in device mapping table
        :type pre_pairing_index: ``int``

        :return: the device address randomly generated for the prepairing slot 0
        :rtype: ``HexList``
        """
        # Send prepairing_data_management with prepairing_slot=0 and prepairing_management_control='Start'
        prepairing_data_management = pre_pairing_main_class.prepairing_data_management_cls(
            device_index=test_case.original_device_index, feature_index=pre_pairing_index,
            prepairing_slot=pre_pairing_main_class.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=pre_pairing_main_class.prepairing_data_management_cls.MODE.START)
        # Wait for prepairing_data_management acknowledgement
        prepairing_data_management_response = test_case.send_report_wait_response(report=prepairing_data_management,
            response_queue=test_case.hidDispatcher.common_message_queue,
            response_class_type=pre_pairing_main_class.prepairing_data_management_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, prepairing_data_management_response,
            pre_pairing_main_class.prepairing_data_management_response_cls)

        # Send get_prepairing_data with data_type='Local'
        if get_local_address:
            get_prepairing_data = pre_pairing_main_class.get_prepairing_data_cls(
                device_index=test_case.original_device_index, feature_index=pre_pairing_index,
                data_type=pre_pairing_main_class.get_prepairing_data_cls.TYPE.LOCAL)
            # Wait for get_prepairing_data acknowledgement
            get_prepairing_data_response = test_case.send_report_wait_response(report=get_prepairing_data,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.get_prepairing_data_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, get_prepairing_data_response,
                pre_pairing_main_class.get_prepairing_data_response_cls)
            local_address = get_prepairing_data_response.local_address
        else:
            local_address = None
        # end if

        return local_address
    # end def pre_pairing_start_sequence

    @classmethod
    def pre_pairing_sequence(cls, test_case, pre_pairing_main_class, pre_pairing_index,
                             long_term_key=UtilNonNumericEnum.AUTO_FILL,
                             remote_identity_resolving_key=UtilNonNumericEnum.AUTO_FILL,
                             local_identity_resolving_key=UtilNonNumericEnum.AUTO_FILL,
                             remote_connection_signature_resolving_key=UtilNonNumericEnum.AUTO_FILL,
                             local_connection_signature_resolving_key=UtilNonNumericEnum.AUTO_FILL,
                             receiver_address=UtilNonNumericEnum.AUTO_FILL,
                             start=True, store=True):
        """
        Set the mandatory pairing key data (set_LTK)
        Set the optional pairing keys data (set_IRK, set_CSRK)

        The keys and the receiver address can be:
            * A wanted ``HexList`` value
            * ``UtilNonNumericEnum.AUTO_FILL``: it will be randomly generated
            * ``None``: the action associated to it will not be done

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pre_pairing_main_class: Device BLE Pro pre-pairing feature main class
        :type pre_pairing_main_class: ``BleProPrepairingVx``
        :param pre_pairing_index: 0x1816 HID++ feature index in device mapping table
        :type pre_pairing_index: ``int``
        :param long_term_key: 16 bytes Long term key (named key11 in flowchart) - OPTIONAL
        :type long_term_key: ``HexList`` or ``UtilNonNumericEnum`` or ``None``
        :param remote_identity_resolving_key: 16 bytes remote Identity Resolving Key (named key21 in
                                              flowchart) - OPTIONAL
        :type remote_identity_resolving_key: ``HexList`` or ``UtilNonNumericEnum`` or ``None``
        :param local_identity_resolving_key: 16 bytes local Identity Resolving Key (named key22 in flowchart) - OPTIONAL
        :type local_identity_resolving_key: ``HexList`` or ``UtilNonNumericEnum`` or ``None``
        :param remote_connection_signature_resolving_key: 16 bytes remote Connection Signature Resolving Key (named
                                                          key31 in flowchart) - OPTIONAL
        :type remote_connection_signature_resolving_key: ``HexList`` or ``UtilNonNumericEnum`` or ``None``
        :param local_connection_signature_resolving_key: 16 bytes local Connection Signature Resolving Key (named
                                                         key32 in flowchart) - OPTIONAL
        :type local_connection_signature_resolving_key: ``HexList`` or ``UtilNonNumericEnum`` or ``None``
        :param receiver_address: 6 bytes remote receiver address - OPTIONAL
        :type receiver_address: ``HexList`` or ``UtilNonNumericEnum`` or ``None``
        :param start: Flag to send the Start request - OPTIONAL
        :type start: ``bool``
        :param store: Flag to send the Store request - OPTIONAL
        :type store: ``bool``

        :return: The device address randomly generated for the prepairing slot 0
        :rtype: ``HexList``
        """
        # ------------------- Check for autofill -------------------
        if long_term_key == UtilNonNumericEnum.AUTO_FILL:
            long_term_key = RandHexList(pre_pairing_main_class.set_ltk_cls.LEN.KEY//8)
        # end if
        if remote_identity_resolving_key == UtilNonNumericEnum.AUTO_FILL:
            remote_identity_resolving_key = RandHexList(pre_pairing_main_class.set_irk_remote_cls.LEN.KEY//8)
        # end if
        if local_identity_resolving_key == UtilNonNumericEnum.AUTO_FILL:
            local_identity_resolving_key = RandHexList(pre_pairing_main_class.set_irk_local_cls.LEN.KEY//8)
        # end if
        if remote_connection_signature_resolving_key == UtilNonNumericEnum.AUTO_FILL:
            remote_connection_signature_resolving_key = RandHexList(
                pre_pairing_main_class.set_csrk_remote_cls.LEN.KEY//8)
        # end if
        if local_connection_signature_resolving_key == UtilNonNumericEnum.AUTO_FILL:
            local_connection_signature_resolving_key = RandHexList(
                pre_pairing_main_class.set_csrk_local_cls.LEN.KEY//8)
        # end if
        if receiver_address == UtilNonNumericEnum.AUTO_FILL:
            receiver_address = BleProPrePairingTestUtils.generate_random_static_address(test_case=test_case)
        # end if

        # ------------------- Sanity check -------------------
        if long_term_key is not None:
            assert len(long_term_key) == pre_pairing_main_class.set_ltk_cls.LEN.KEY//8
        # end if
        if remote_identity_resolving_key is not None:
            assert len(remote_identity_resolving_key) == pre_pairing_main_class.set_irk_remote_cls.LEN.KEY//8
        # end if
        if local_identity_resolving_key is not None:
            assert len(local_identity_resolving_key) == pre_pairing_main_class.set_irk_local_cls.LEN.KEY//8
        # end if
        if remote_connection_signature_resolving_key is not None:
            assert (len(remote_connection_signature_resolving_key) ==
                    pre_pairing_main_class.set_csrk_remote_cls.LEN.KEY//8)
        # end if
        if local_connection_signature_resolving_key is not None:
            assert (len(local_connection_signature_resolving_key) ==
                    pre_pairing_main_class.set_csrk_local_cls.LEN.KEY//8)
        # end if

        # ------------------- Wanted actions -------------------
        if start:
            # Start the pre-pairing sequence and retrieve the local device address
            device_address = cls.pre_pairing_start_sequence(test_case, pre_pairing_main_class, pre_pairing_index)
        else:
            device_address = None
        # end if

        if long_term_key is not None:
            # Send set_LTK with the provided long term key value
            set_ltk = pre_pairing_main_class.set_ltk_cls(device_index=test_case.original_device_index,
                feature_index=pre_pairing_index, ltk=long_term_key)
            # Wait for set_LTK acknowledgement
            set_ltk_response = test_case.send_report_wait_response(report=set_ltk,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.set_ltk_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, set_ltk_response,
                pre_pairing_main_class.set_ltk_response_cls)
            cls.set_key(test_case, 'long_term_key', long_term_key)
        # end if

        if remote_identity_resolving_key is not None:
            # Send set_IRK_remote with the provided remote Identity Resolving Key value
            set_irk_remote = pre_pairing_main_class.set_irk_remote_cls(device_index=test_case.original_device_index,
                feature_index=pre_pairing_index, irk_remote=remote_identity_resolving_key)
            # Wait for set_IRK_remote acknowledgement
            set_irk_remote_response = test_case.send_report_wait_response(report=set_irk_remote,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.set_irk_remote_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, set_irk_remote_response,
                pre_pairing_main_class.set_irk_remote_response_cls)
            cls.set_key(test_case, 'remote_identity_resolving_key', remote_identity_resolving_key)
        # end if

        if local_identity_resolving_key is not None:
            # Send set_IRK_local with the provided local Identity Resolving Key value
            set_irk_local = pre_pairing_main_class.set_irk_local_cls(device_index=test_case.original_device_index,
                feature_index=pre_pairing_index, irk_local=local_identity_resolving_key)
            # Wait for set_IRK_local acknowledgement
            set_irk_local_response = test_case.send_report_wait_response(report=set_irk_local,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.set_irk_local_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, set_irk_local_response,
                pre_pairing_main_class.set_irk_local_response_cls)
            cls.set_key(test_case, 'local_identity_resolving_key', local_identity_resolving_key)
        # end if

        if remote_connection_signature_resolving_key is not None and (test_case.config_manager.get_feature(
                ConfigurationManager.ID.BLE_PRO_PREPAIRING_CFG) & BleProPrePairingNvsChunk.KEYMAP.KEY_REMOTE_CSRK ==
                                                                      BleProPrePairingNvsChunk.KEYMAP.KEY_REMOTE_CSRK):
            # Send set_CSRK_remote with the provided remote Connection Signature Resolving Key value
            set_csrk_remote = pre_pairing_main_class.set_csrk_remote_cls(device_index=test_case.original_device_index,
                feature_index=pre_pairing_index, csrk_remote=remote_connection_signature_resolving_key)
            # Wait for set_CSRK_remote acknowledgement
            set_csrk_remote_response = test_case.send_report_wait_response(report=set_csrk_remote,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.set_csrk_remote_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, set_csrk_remote_response,
                pre_pairing_main_class.set_csrk_remote_response_cls)
            cls.set_key(test_case, 'remote_connection_signature_resolving_key',
                        remote_connection_signature_resolving_key)
        # end if

        if local_connection_signature_resolving_key and (test_case.config_manager.get_feature(
                ConfigurationManager.ID.BLE_PRO_PREPAIRING_CFG) & BleProPrePairingNvsChunk.KEYMAP.KEY_LOCAL_CSRK ==
                                                                      BleProPrePairingNvsChunk.KEYMAP.KEY_LOCAL_CSRK):
            # Send set_CSRK_local with the provided local Connection Signature Resolving Key value
            set_csrk_local = pre_pairing_main_class.set_csrk_local_cls(device_index=test_case.original_device_index,
                feature_index=pre_pairing_index, csrk_local=local_connection_signature_resolving_key)
            # Wait for set_CSRK_local acknowledgement
            set_csrk_local_response = test_case.send_report_wait_response(report=set_csrk_local,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.set_csrk_local_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, set_csrk_local_response,
                pre_pairing_main_class.set_csrk_local_response_cls)
            cls.set_key(test_case, 'local_connection_signature_resolving_key',
                        local_connection_signature_resolving_key)
        # end if

        # Set the remote receiver address and end the pre-pairing sequence
        cls.pre_pairing_end_sequence(test_case, pre_pairing_main_class, pre_pairing_index, receiver_address, store)

        return device_address
    #end def pre_pairing_sequence

    @classmethod
    def pre_pairing_end_sequence(cls, test_case, pre_pairing_main_class, pre_pairing_index, receiver_address=None,
                                 store=True):
        """
        Store the receiver bluetooth address in device memory and complete the pre-pairing sequence with the 'Store'
        request

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pre_pairing_main_class: Device BLE Pro pre-pairing feature main class
        :type pre_pairing_main_class: ``BleProPrepairingVx``
        :param pre_pairing_index: 0x1816 HID++ feature index in device mapping table
        :type pre_pairing_index: ``int``
        :param receiver_address: 6 bytes remote receiver address
        :type receiver_address: ``HexList``
        :param store: Flag to send the Store request
        :type store: ``bool``
        """
        if receiver_address is not None:
            # Send set_prepairing_data with data_type='remote'
            set_prepairing_data = pre_pairing_main_class.set_prepairing_data_cls(
                device_index=test_case.original_device_index, feature_index=pre_pairing_index,
                data_type=pre_pairing_main_class.set_prepairing_data_cls.TYPE.REMOTE,
                remote_address=receiver_address)
            # Wait for set_prepairing_data acknowledgement
            set_prepairing_data_response = test_case.send_report_wait_response(report=set_prepairing_data,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.set_prepairing_data_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, set_prepairing_data_response,
                pre_pairing_main_class.set_prepairing_data_response_cls)
            cls.set_key(test_case, 'receiver_address', receiver_address)
        # end if

        if store:
            # Send prepairing_data_management with prepairing_slot=0 and prepairing_management_control='Store'
            prepairing_data_management = pre_pairing_main_class.prepairing_data_management_cls(
                device_index=test_case.original_device_index, feature_index=pre_pairing_index,
                prepairing_slot=pre_pairing_main_class.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
                mode=pre_pairing_main_class.prepairing_data_management_cls.MODE.STORE)
            # Wait for prepairing_data_management acknowledgement
            prepairing_data_management_response = test_case.send_report_wait_response(report=prepairing_data_management,
                response_queue=test_case.hidDispatcher.common_message_queue,
                response_class_type=pre_pairing_main_class.prepairing_data_management_response_cls)
            # Check the response to the command is success
            BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, prepairing_data_management_response,
                pre_pairing_main_class.prepairing_data_management_response_cls)
        # end if
    #end def pre_pairing_end_sequence

    @classmethod
    def delete_pre_pairing_slot(cls, test_case, pre_pairing_main_class, pre_pairing_index):
        """
        Send the pre-pairing 'Delete' request

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pre_pairing_main_class: Device BLE Pro pre-pairing feature main class
        :type pre_pairing_main_class: ``BleProPrepairingVx``
        :param pre_pairing_index: 0x1816 HID++ feature index in device mapping table
        :type pre_pairing_index: ``int``
        """
        # Send prepairing_management with prepairing_slot=0 and prepairing_management_control='Delete'
        prepairing_data_management = pre_pairing_main_class.prepairing_data_management_cls(
            device_index=test_case.original_device_index, feature_index=pre_pairing_index,
            prepairing_slot=pre_pairing_main_class.prepairing_data_management_cls.DEFAULT.PREPAIRING_SLOT,
            mode=pre_pairing_main_class.prepairing_data_management_cls.MODE.DELETE)
        # Wait for prepairing_data_management acknowledgement
        prepairing_data_management_response = test_case.send_report_wait_response(report=prepairing_data_management,
            response_queue=test_case.hidDispatcher.common_message_queue,
            response_class_type=pre_pairing_main_class.prepairing_data_management_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(test_case, prepairing_data_management_response,
            pre_pairing_main_class.prepairing_data_management_response_cls)
    #end def delete_pre_pairing_slot

    @classmethod
    def get_remote_address_value(cls, testcase, pre_pairing_main_class, pre_pairing_index):
        """
        Retrieve the receiver bluetooth address in device memory

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param pre_pairing_main_class: Device BLE Pro pre-pairing feature main class
        :type pre_pairing_main_class: ``BleProPrepairingVx``
        :param pre_pairing_index: 0x1816 HID++ feature index in device mapping table
        :type pre_pairing_index: ``int``

        :return: the 6 bytes remote receiver address
        :rtype: ``HexList``
        """
        get_prepairing_data = pre_pairing_main_class.get_prepairing_data_cls(device_index=testcase.deviceIndex,
            feature_index=pre_pairing_index,
            data_type=pre_pairing_main_class.get_prepairing_data_cls.TYPE.REMOTE)
        get_prepairing_data_response = testcase.send_report_wait_response(report=get_prepairing_data,
            response_queue=testcase.hidDispatcher.common_message_queue,
            response_class_type=pre_pairing_main_class.get_prepairing_data_response_cls)
        # Check the response to the command is success
        BleProPrePairingTestUtils.PrePairingResponseChecker.check_fields(testcase, get_prepairing_data_response,
            pre_pairing_main_class.get_prepairing_data_response_cls)

        return get_prepairing_data_response.remote_address
    # end def get_remote_address_value

    @classmethod
    def set_key(cls, test_case, key_name, key_value):
        """
        Set the provided key value

        :param test_case: Current test case
        :type test_case: ``DevicePairingTestCase or BaseTestCase``
        :param key_name: Key Unique identifier
        :type key_name: ``str``
        :param key_value: Key payload
        :type key_value: ``HexList``
        """
        if not hasattr(test_case, 'pre_pairing_keys'):
            test_case.pre_pairing_keys = {}
        # end if
        test_case.pre_pairing_keys[f'{key_name}'] = HexList(key_value)
    # end def set_key

    @classmethod
    def get_key(cls, test_case, key_name):
        """
        Retrieve the requested key value

        :param test_case: Current test case
        :type test_case: ``DevicePairingTestCase or BaseTestCase``
        :param key_name: Key Unique identifier
        :type key_name: ``str``

        :return: long term key
        :rtype: ``int``
        """
        if not hasattr(test_case, 'pre_pairing_keys'):
            return None
        # end if
        if key_name in test_case.pre_pairing_keys:
            return test_case.pre_pairing_keys[f'{key_name}']
        else:
            return None
        # end if
    # end def get_key

    class PrePairingResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Pre Pairing responses checker class
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the Pre Pairing responses API

            :param test_case: Current test case
            :type test_case: ``BleProPrePairingTestCase or BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "data_type": None,
                "local_address": None,
            }
        # end def get_default_check_map
    # end class PrePairingResponseChecker

    class NvsHelper():
        """
        Non Volatile Memory Helper class
        """

        @classmethod
        def get_latest_pre_pairing_chunk(cls, test_case, backup=False):
            """
            Check NVS device pre pairing chunk content.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param backup: Flag enabling to save a copy of the initial NVS
            :type backup: ``bool``
            """
            # Dump receiver NVS
            test_case.memory_manager.read_nvs(backup)
            # Extract BLE pre-pairing chunks
            chunks = test_case.memory_manager.get_chunks_by_name('NVS_BLE_PRO_PRE_PAIRING_ID_0')
            if len(chunks) == 0:
                test_case.log_warning(f"No Device BLE pre-pairing chunk found")
                return None
            else:
                return chunks[-1]
            # end if
        # end def get_latest_pre_pairing_chunk

        @classmethod
        def check_device_pre_pairing_data(cls, test_case):
            """
            Check NVS device pre pairing chunk content.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            pre_pairing_chunk = cls.get_latest_pre_pairing_chunk(test_case)
            # Check the long term key is matching
            test_case.assertEqual(obtained=pre_pairing_chunk.long_term_key,
                  expected=BleProPrePairingTestUtils.get_key(test_case, 'long_term_key'),
                  msg="set_ltk and NVS BLE pre-pairing chunk LTK Keys don't match")
            # Check the remote_identity_resolving_key is matching
            test_case.assertEqual(obtained=pre_pairing_chunk.keys.remote_identity_resolving_key,
                  expected=BleProPrePairingTestUtils.get_key(test_case, 'remote_identity_resolving_key'),
                  msg="set_irk_remote and NVS BLE pre-pairing chunk IRK Keys don't match")
            # Check the local_identity_resolving_key is matching
            test_case.assertEqual(obtained=pre_pairing_chunk.keys.local_identity_resolving_key,
                  expected=BleProPrePairingTestUtils.get_key(test_case, 'local_identity_resolving_key'),
                  msg="set_irk_local and NVS BLE pre-pairing chunk IRK Keys don't match")
            if BleProPrePairingTestUtils.get_key(test_case, 'remote_connection_signature_resolving_key') is not None:
                # Check the remote_connection_signature_resolving_key is matching
                test_case.assertEqual(obtained=pre_pairing_chunk.keys.remote_connection_signature_resolving_key,
                      expected=BleProPrePairingTestUtils.get_key(test_case, 'remote_connection_signature_resolving_key'),
                      msg="set_csrk_remote and NVS BLE pre-pairing chunk CSRK Keys don't match")
            # end if
            if BleProPrePairingTestUtils.get_key(test_case, 'local_connection_signature_resolving_key') is not None:
                # Check the local_connection_signature_resolving_key is matching
                test_case.assertEqual(obtained=pre_pairing_chunk.keys.local_connection_signature_resolving_key,
                      expected=BleProPrePairingTestUtils.get_key(test_case, 'local_connection_signature_resolving_key'),
                      msg="set_csrk_local and NVS BLE pre-pairing chunk CSRK Keys don't match")
            #end if
            # Check the receiver_address is matching
            test_case.assertEqual(obtained=pre_pairing_chunk.keys.remote_address,
                  expected=BleProPrePairingTestUtils.get_key(test_case, 'receiver_address'),
                  msg="set_prepairing_data and NVS BLE pre-pairing chunk receiver address don't match")
        #end def check_device_pre_pairing_data

    @classmethod
    def get_1816_and_generate_keys_prepairing(cls, test_case):
        """
        Generate the 0x1816 classes and index, as well as the necessary keys (random) for prepairing.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: A tuple with all generated element
        :rtype: ``tuple[int, BleProPrepairingInterface, HexList, HexList, HexList, HexList, HexList]``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(test_case, 'Get feature 1816 index')
        # ---------------------------------------------------------------------------
        feature_1816_index = ChannelUtils.update_feature_mapping(
            test_case=test_case, feature_id=BleProPrepairing.FEATURE_ID)
        feature_1816 = BleProPrepairingFactory.create(
            ChannelUtils.get_feature_version(test_case=test_case, feature_index=feature_1816_index))

        ltk_key, irk_remote_key, irk_local_key, csrk_remote_key, csrk_local_key = cls.generate_keys_prepairing(
            test_case=test_case, feature_1816=feature_1816)

        return feature_1816_index, feature_1816, ltk_key, irk_remote_key, irk_local_key, csrk_remote_key, csrk_local_key
    # end def get_1816_and_generate_keys_prepairing

    @staticmethod
    def generate_keys_prepairing(test_case, feature_1816):
        """
        Generate (random) the necessary keys for prepairing.

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param feature_1816: Interface class of feature 0x1816
        :type feature_1816: ``BleProPrepairingInterface``

        :return: A tuple with all generated element
        :rtype: ``tuple[HexList, HexList, HexList, HexList, HexList]``
        """
        # ---------------------------------------------------------------------------
        LogHelper.log_info(test_case, 'Generate keys')
        # ---------------------------------------------------------------------------
        ltk_key = RandHexList(feature_1816.set_ltk_cls.LEN.KEY//8)
        irk_remote_key = RandHexList(feature_1816.set_irk_remote_cls.LEN.KEY//8)
        irk_local_key = RandHexList(feature_1816.set_irk_local_cls.LEN.KEY//8)
        csrk_remote_key = RandHexList(feature_1816.set_csrk_remote_cls.LEN.KEY//8)
        csrk_local_key = RandHexList(feature_1816.set_csrk_local_cls.LEN.KEY//8)

        return ltk_key, irk_remote_key, irk_local_key, csrk_remote_key, csrk_local_key
    # end def generate_keys_prepairing

    @staticmethod
    def generate_random_static_address(test_case):
        """
        Generate (random) a random static address following the BLE standard (see Bluetooth Core Spec v5.3 Vol 6,
        Part B, Section 1.3.2.1).

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The generated address in little endian
        :rtype: ``HexList``
        """
        # This whole loop is to make sure that the address follow the standard (see docstring)
        for _ in range(MAX_RETRY):
            address = RandHexList(BleGenericIntConstant.BLE_ADDRESS_LENGTH)
            # The random part of the address has to be tested, the 2 MSB has then to not be part of it according to
            # standard (see docstring)
            is_valid = not reduce(lambda x, y: x & y, list(address.testBit(0) == address.testBit(z)
                                                           for z in range(1, len(address[:-1])*8)))
            if is_valid:
                break
            # end if
        else:
            raise RuntimeError(f"Could not get acceptable address after {MAX_RETRY} retry(ies)")
        # end for

        # Force the two most significant bits to 1 to be a random static address (see spec in docstring)
        address[-1] = address[-1] | 0xC0
        # ---------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"Random static address generated: {address}")
        # ---------------------------------------------------------------------------

        return address
    # end def generate_random_static_address

    @staticmethod
    def get_range_random_static_address(test_case):
        """
        Get the possible range of random static address following the BLE standard (see Bluetooth Core Spec v5.3 Vol 6,
        Part B, Section 1.3.2.1), the values are in little endian:

            * min = 01:00:00:00:00:C0
            * max = FE:FF:FF:FF:FF:FF

        :param test_case: Test case object
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :return: The address range in little endian
        :rtype: ``tuple[HexList, HexList]``
        """
        min_address = HexList("0100000000C0")
        max_address = HexList("FEFFFFFFFFFF")
        # ---------------------------------------------------------------------------
        LogHelper.log_info(test_case, f"Random static address range: min = {min_address} max = {max_address}")
        # ---------------------------------------------------------------------------

        return min_address, max_address
    # end def get_range_random_static_address
# end class BleProPrePairingTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
