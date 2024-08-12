#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.devicebasetestutils
:brief:  Helpers for device specific feature
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/05/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import warnings
from enum import StrEnum
from enum import auto
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.logiconstants import LogitechBleConstants
from pychannel.throughreceiverchannel import ThroughEQuadReceiverChannel
from pyhid.hid import HID_REPORTS
from pyhid.hid.controlidtable import CONSUMER_CID_LIST
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeatures
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.oobstate import OobStateFactory
from pyhid.hidpp.features.devicereset import DeviceReset
from pyhid.hidpp.features.devicereset import ForceDeviceReset
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeatures
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.root import Root
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplay
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplayFactory
from pyhid.vlp.features.important.vlproot import VLPRoot
from pylibrary.emulator.emulatorinterfaces import ButtonStimuliInterface
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.mcu.connectchunks import ConnectIdChunkData
from pylibrary.mcu.nrf52.blenvschunks import LastBluetoothAddress
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.hexlist import RandHexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.configurationmanager import ConfigurationManager
from pytestbox.base.loghelper import LogHelper
from pytransport.transportcontext import TransportContextException


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class DeviceBaseTestUtils(CommonBaseTestUtils):
    """
    This class provides helpers for device specific features
    """
    class NvsHelper(CommonBaseTestUtils.NvsHelper):
        # See ``CommonBaseTestUtils.NvsHelper``
        @staticmethod
        def check_connect_id(test_case, memory_manager, expected_host_index, expected_pairing_source=None):
            """
            Check connect id chunk in device's NVS.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param memory_manager: Device memory manager (can be test case ``memory_manager`` or
                                   ``device_manager`` or ``receiver_manager``)
            :type memory_manager: ``MemoryManager``
            :param expected_host_index: Expected host index in NVS
            :type expected_host_index: ``int``
            :param expected_pairing_source: Expected pairing source in NVS - OPTIONAL
            :type expected_pairing_source: ``ConnectIdChunkData.PairingSrc`` or ``None``
            """
            connect_id_chunk = memory_manager.get_active_chunk_by_name(chunk_name='NVS_CONNECT_ID')

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, f'Check Channel {expected_host_index + 1} is used, i.e Host Index = {expected_host_index}')
            # ----------------------------------------------------------------------------------------------------------
            test_case.assertEqual(expected=expected_host_index,
                                  obtained=int(Numeral(connect_id_chunk.data.host_index)),
                                  msg=f'Channel {expected_host_index + 1} should be used, i.e. Host Index should be '
                                      f'{expected_host_index}')

            if expected_pairing_source is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f'Check Pairing Source on Host Index {expected_host_index}')
                # ------------------------------------------------------------------------------------------------------
                test_case.assertEqual(
                    expected=expected_pairing_source,
                    obtained=int(Numeral(getattr(connect_id_chunk.data,
                                                 f'pairing_src_{expected_host_index}'))),
                    msg=f'Pairing source on Channel {expected_host_index + 1} should be {expected_pairing_source}')
            # end if
        # end def check_connect_id

        @classmethod
        def change_host(cls, test_case, memory_manager, host_index, expected_pairing_source=None):
            """
            Change host on device using NVS.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param memory_manager: Device memory manager (can be test case ``memory_manager`` or
                                   ``device_manager`` or ``receiver_manager``)
            :type memory_manager: ``MemoryManager``
            :param host_index: Host's index to activate
            :type host_index: ``int``
            :param expected_pairing_source: Expected pairing source in NVS - OPTIONAL
            :type expected_pairing_source: ``ConnectIdChunkData.PairingSrc`` or ``None``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Change host on Device')
            # ----------------------------------------------------------------------------------------------------------
            memory_manager.read_nvs()
            # TODO Add switch_to_host_id to NvsManagerInterface to use it as type in this method in the docstring
            memory_manager.switch_to_host_id(host_id=host_index, is_test_setup=False)
            memory_manager.load_nvs()
            sleep(2.0)

            memory_manager.read_nvs()
            cls.check_connect_id(test_case=test_case, memory_manager=memory_manager, expected_host_index=host_index,
                                 expected_pairing_source=expected_pairing_source)
        # end def change_host

        @classmethod
        def change_protocol_gaming_devices(cls, test_case, protocol):
            """
            Change protocol on gaming device using NVS

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param protocol: Protocol to change to
            :type protocol: ``LogitechProtocol``
            """
            test_case.assertTrue(expr=test_case.f.PRODUCT.NVS_CHUNK_IDS.F_IsGamingVariant)
            test_case.memory_manager.read_nvs()
            connect_id_chunk = test_case.memory_manager.get_active_chunk_by_name(chunk_name='NVS_CONNECT_ID')
            curr_host_idx = to_int(connect_id_chunk.data.host_index)
            if protocol == LogitechProtocol.BLE:
                # If true, the alternate mode is selected
                setattr(connect_id_chunk.data, f'alt_mode_{curr_host_idx}', True)

                # Reset CONN_BLE and CONN_BLE_LS2 to 0 in conn_flags to let device enter advertising state
                # connFlags bit definition
                # #define CONN_USB       BIT_00
                # #define CONN_UFY       BIT_01
                # #define CONN_CRUSH     BIT_02
                # #define CONN_BT        BIT_03
                # #define CONN_BLE       BIT_04
                # #define CONN_BLE_LS2   BIT_05
                # #define CONN_LS2       BIT_06
                #
                # https://spaces.logitech.com/display/ES/02+LS2+Connection+scheme
                conn_flags = getattr(connect_id_chunk.data, f'conn_flags_{curr_host_idx}')
                setattr(connect_id_chunk.data, f'conn_flags_{curr_host_idx}', conn_flags & 0b11001111)
            else:
                setattr(connect_id_chunk.data, f'alt_mode_{curr_host_idx}', False)
            # end if
            test_case.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_CONNECT_ID', data=HexList(connect_id_chunk))
            # Force device reset so that changes have immediate effect
            test_case.memory_manager.load_nvs()
            sleep(0.5)
        # end def change_protocol_gaming_devices

        @staticmethod
        def check_dfu_out_of_recovery(test_case, memory_manager):
            """
            Check there is a unique instance of the "dfu out of recovery" chunk in device's NVS

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param memory_manager: Device memory manager (can be the test case ``memory_manager`` or
                                   ``device_manager`` or ``receiver_manager``)
            :type memory_manager: ``MemoryManager``
            """
            dfu_out_of_recovery_id_chunk_list = memory_manager.get_chunks_by_name(
                chunk_name='NVS_DFU_OUT_OF_RECOVERY_ID')

            test_case.assertTrue(expr=len(dfu_out_of_recovery_id_chunk_list) == 1,
                                 msg=f'NVS_DFU_OUT_OF_RECOVERY_ID not found or not unique (found '
                                     f'{len(dfu_out_of_recovery_id_chunk_list)})')
        # end def check_dfu_out_of_recovery

        @staticmethod
        def get_last_gap_address(test_case, memory_manager):
            """
            Retrieve the last Bluetooth address saved in NVS.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param memory_manager: Memory manager (can be the test case ``memory_manager`` or ``device_manager`` or
                                   ``receiver_manager``)
            :type memory_manager: ``MemoryManager``

            :return: Last Bluetooth address saved in NVS
            :rtype: ``HexList``
            """
            last_gap_address_chunk_list = memory_manager.get_chunks_by_name(chunk_name='NVS_BLE_LAST_GAP_ADDR_USED')

            test_case.assertTrue(expr=len(last_gap_address_chunk_list) >= 1,
                                 msg='NVS_BLE_LAST_GAP_ADDR_USED not found')
            return last_gap_address_chunk_list[-1].device_bluetooth_address
        # end def get_last_gap_address

        @staticmethod
        def force_last_gap_address(test_case):
            """
            Force the last Bluetooth address in NVS.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            address_size = (LastBluetoothAddress.LEN.DEVICE_BLUETOOTH_ADDRESS // 8) - 1
            address_current_device = RandHexList(size=address_size) + HexList("D0")
            last_gap_address_chunk = LastBluetoothAddress(device_address_type=LogitechBleConstants.ADDRESS_TYPE,
                                                          device_resolvable_private_address_flag=False,
                                                          device_bluetooth_address=address_current_device)

            test_case.memory_manager.read_nvs()
            test_case.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_BLE_LAST_GAP_ADDR_USED',
                                                              data=HexList(last_gap_address_chunk))
            test_case.memory_manager.load_nvs()
        # end def force_last_gap_address

        @staticmethod
        def force_tde_counters(test_case):
            """
            Re-enable TDE commands by reloading a chunk NVS_X1E01_CONN_CNTR_ID.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :raise ``DeprecationWarning``: This method shall not be called anymore as the 0x1E01 feature is deprecated.
            """
            warnings.warn(
                "This method shall not be called anymore as the 0x1E01 feature is deprecated.", DeprecationWarning)
            if DeviceBaseTestUtils.HIDppHelper.get_feature_index(
                    test_case=test_case, feature_id=ManageDeactivatableFeatures.FEATURE_ID,
                    skip_not_found=True) == Root.FEATURE_NOT_FOUND:
                return
            # end if
            if test_case.memory_manager is not None:
                test_case.memory_manager.read_nvs()
                conn_cntr_chunks = test_case.memory_manager.get_chunks_by_name(chunk_name='NVS_X1E01_CONN_CNTR_ID')
                if conn_cntr_chunks is not None and len(conn_cntr_chunks):
                    new_data = HexList([
                        test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxManufacturingCounter,
                        test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxComplianceCounter,
                        test_case.f.PRODUCT.FEATURES.COMMON.MANAGE_DEACTIVATABLE_FEATURES.F_MaxGothardCounter])
                    test_case.memory_manager.nvs_parser.add_new_chunk(chunk_id='NVS_X1E01_CONN_CNTR_ID', data=new_data)
                # end if
                test_case.memory_manager.load_nvs()
            # end if
        # end def force_tde_counters

        @staticmethod
        def restore_pairing(test_case, no_reset=False):
            """
            Restore pairing data from backed up NVS

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param no_reset: Flag enabling to reload the NVS without resetting the device, only stop and run - OPTIONAL
            :type no_reset: ``bool``
            """
            test_case.memory_manager.read_nvs()
            test_case.memory_manager.nvs_parser.copy_pairing(
                other_nvs_parser=test_case.memory_manager.backup_nvs_parser)
            test_case.memory_manager.load_nvs(no_reset=no_reset)
        # end def restore_pairing
    # end class NvsHelper

    class ButtonHelper:
        """
        Button helper class
        """
        @staticmethod
        def check_user_action(test_case):
            """
            Check HID messages are received on user action.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :raise ``AssertionError``: If all retries failed to receive a message.
            """
            if test_case.f.PRODUCT.FEATURES.VLP.F_UserActionHIDPP:
                _, feature_19a1, _, _ = DeviceBaseTestUtils.HIDppHelper().get_vlp_parameters(
                    test_case=test_case,
                    feature_id=ContextualDisplay.FEATURE_ID,
                    factory=ContextualDisplayFactory)
            # end if
            if test_case.config_manager.current_target == ConfigurationManager.TARGET.RECEIVER:
                # Fetch Device USB Descriptors which have not yet been retrieved as the DUT is the receiver
                ChannelUtils.get_descriptors(test_case=test_case)
            # end if
            retry = 2

            while retry > 0:
                try:
                    ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                class_type=HID_REPORTS)
                    ChannelUtils.empty_queue(test_case=test_case, queue_name=HIDDispatcher.QueueName.VLP_EVENT)

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case, 'Perform User Action')
                    # --------------------------------------------------------------------------------------------------
                    test_case.button_stimuli_emulator.user_action()

                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case, 'Check command is received')
                    # --------------------------------------------------------------------------------------------------
                    if test_case.f.PRODUCT.FEATURES.VLP.F_UserActionHIDPP:
                        vlp_msg = ChannelUtils.get_only(test_case=test_case,
                                                        queue_name=HIDDispatcher.QueueName.VLP_EVENT,
                                                        class_type=feature_19a1.button_event_cls)
                        test_case.assertNotNone(obtained=vlp_msg, msg='VLP button event message should be received')
                        retry = 0
                    else:
                        hid_msg = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                        class_type=HID_REPORTS)
                        test_case.assertNotNone(obtained=hid_msg, msg='HID mouse/keyboard message should be received')

                        hid_msg = ChannelUtils.get_only(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                                        class_type=HID_REPORTS)
                        test_case.assertNotNone(obtained=hid_msg, msg='HID mouse/keyboard message should be received')
                        retry = 0
                    # end if
                except (AssertionError, QueueEmpty) as no_msg_err:
                    retry -= 1
                    if retry <= 0:
                        raise AssertionError(no_msg_err)
                    # end if
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case, 'Retry user action')
                    # --------------------------------------------------------------------------------------------------
                # end try
            # end while
        # end def check_user_action

        @staticmethod
        def check_no_hid_report(test_case):
            """
            Check no HID reports are received following a user action.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            """
            hid_message_classes = HID_REPORTS
            ChannelUtils.clean_messages(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID,
                                        class_type=hid_message_classes)
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Perform User Action')
            # ----------------------------------------------------------------------------------------------------------
            test_case.button_stimuli_emulator.user_action()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Check no HID report is received')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=test_case, queue_name=HIDDispatcher.QueueName.HID, timeout=.5)
        # end def check_no_hid_report

        @staticmethod
        def is_consumer_cid(cid_list):
            """
            Check whether both cids are of consumer type.

            :param cid_list: Cid list
            :type cid_list: ``list[int|HexList]``

            :return: True if both cids are of consumer type otherwise False
            :rtype: ``bool``
            """
            for cid in cid_list:
                if to_int(cid) not in CONSUMER_CID_LIST:
                    return False
                # end if
            # end for
            return True
        # end def is_consumer_cid
    # end class ButtonHelper

    class HIDppHelper(CommonBaseTestUtils.HIDppHelper):
        # See ``CommonBaseTestUtils.HIDppHelper``
        @classmethod
        def send_report_wait_error(cls, test_case, report, error_type=Hidpp2ErrorCodes, error_codes=None):
            # See ``CommonBaseTestUtils.HIDppHelper.send_report_wait_error``
            return super().send_report_wait_error(test_case, report, error_type, error_codes)
        # end def send_report_wait_error

        @classmethod
        def get_parameters(cls, test_case, feature_id, factory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            """
            Get commonly used parameters, i.e:
                * feature index
                * feature interface
                * device index
                * port index

            If enabled, add feature object and index as attributes of the given test_case:
                * test_case.feature_<feature_id>
                * test_case.feature_<feature_id>_index

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param feature_id: Feature index on 2 bytes (ex. 0x1815)
            :type feature_id: ``int``
            :param factory: Feature factory class, it should be a subclass of ``FeatureFactory``
            :type factory: ``type``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param update_test_case: Enable update of test_case attributes - OPTIONAL
            :type update_test_case: ``bool``
            :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                                   not found if ``False`` and return 0 if ``True`` - OPTIONAL
            :type skip_not_found: ``bool``

            :return: Feature index, feature interface, device index, port index
            :rtype: ``tuple[int, FeatureInterface, int, int]``

            :raise ``AssertionError``: If the parameter ``factory`` is not a subclass of ``FeatureFactory``
            """
            assert issubclass(factory, FeatureFactory), \
                f"The parameter factory should be a subclass of FeatureFactory, {factory} is not"
            feature_interface = None
            device_index = device_index if device_index is not None else ChannelUtils.get_device_index(
                test_case=test_case)
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(test_case=test_case)

            if update_test_case is None:
                update_test_case = (port_index == ChannelUtils.get_port_index(test_case=test_case))
            # end if
            feature_index = cls.get_feature_index(test_case=test_case, feature_id=feature_id,
                                                  device_index=device_index, port_index=port_index,
                                                  skip_not_found=skip_not_found)
            if feature_index != Root.FEATURE_NOT_FOUND:

                feature_interface = factory.create(ChannelUtils.get_feature_version(
                        test_case=test_case, feature_index=feature_index))

                if update_test_case:
                    setattr(test_case, f'feature_{to_int(feature_id):04X}_index'.lower(), feature_index)
                    setattr(test_case, f'feature_{to_int(feature_id):04X}'.lower(), feature_interface)
                # end if

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(
                    test_case, f'Feature {HexList(Numeral(feature_id))} index : {hex(feature_index)}')
                # ------------------------------------------------------------------------------------------------------
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(
                    test_case, f'Feature {HexList(Numeral(feature_id))} not found !')
                # ------------------------------------------------------------------------------------------------------
            # end if

            return feature_index, feature_interface, device_index, port_index
        # end def get_parameters

        @classmethod
        def get_vlp_parameters(cls, test_case, feature_id, factory, device_index=None, port_index=None,
                           update_test_case=None, skip_not_found=False):
            """
            Get commonly used parameters for VLP features, i.e:
                * feature index
                * feature interface
                * device index
                * port index

            If enabled, add feature object and index as attributes of the given test_case:
                * test_case.feature_<feature_id>
                * test_case.feature_<feature_id>_index

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param feature_id: Feature index on 2 bytes (ex. 0x1815)
            :type feature_id: ``int``
            :param factory: Feature factory class, it should be a subclass of ``FeatureFactory``
            :type factory: ``type``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param update_test_case: Enable update of test_case attributes - OPTIONAL
            :type update_test_case: ``bool``
            :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                                   not found if ``False`` and return 0 if ``True`` - OPTIONAL
            :type skip_not_found: ``bool``

            :return: Feature index, feature interface, device index, port index
            :rtype: ``tuple[int, FeatureInterface, int, int]``

            :raise ``AssertionError``: If the parameter ``factory`` is not a subclass of ``FeatureFactory``
            """
            assert issubclass(factory, FeatureFactory), \
                f"The parameter factory should be a subclass of FeatureFactory, {factory} is not"

            device_index = device_index if device_index is not None else ChannelUtils.get_device_index(
                test_case=test_case)
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(test_case=test_case)

            if update_test_case is None:
                update_test_case = (port_index == ChannelUtils.get_port_index(test_case=test_case))
            # end if

            feature_index = cls.get_vlp_feature_index(test_case=test_case, feature_id=feature_id,
                                                      device_index=device_index, port_index=port_index,
                                                      skip_not_found=skip_not_found)
            feature_interface = factory.create(
                ChannelUtils.get_vlp_feature_version(test_case=test_case, feature_index=feature_index))

            if update_test_case:
                setattr(test_case, f'feature_{to_int(feature_id):04X}_index'.lower(), feature_index)
                setattr(test_case, f'feature_{to_int(feature_id):04X}'.lower(), feature_interface)
            # end if

            # ------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, f'Feature {HexList(Numeral(feature_id))} index : {hex(feature_index)}')
            # ------------------------------------------------------------------------------------------------------

            return feature_index, feature_interface, device_index, port_index

        # end def get_vlp_parameters

        @classmethod
        def get_feature_index(cls, test_case, feature_id, device_index=None, port_index=None, skip_not_found=False):
            """
            Get feature index from feature id.

            First, get the feature index from the HID dispatcher if the feature is already available. If not,
            send the Root getFeature request to get the feature index from the device.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param feature_id: Feature ID
            :type feature_id: ``int`` or ``HexList``
            :param device_index: Device Index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port Index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                                   not found if ``False`` and return 0 if ``True`` - OPTIONAL
            :type skip_not_found: ``bool``

            :return: Feature index
            :rtype: ``int``
            """
            feature_index = test_case.current_channel.hid_dispatcher.get_feature_index(feature_id=feature_id)
            if feature_index is None:
                root_feature_idx = test_case.current_channel.hid_dispatcher.get_feature_index(
                    feature_id=Root.FEATURE_ID)
                if root_feature_idx is None:
                    test_case.current_channel.hid_dispatcher.add_feature_entry(
                        feature_index=Root.FEATURE_INDEX, feature_id=Root.FEATURE_ID,
                        feature_version=int(test_case.f.SHARED.DEVICES.F_RootFeatureVersion[0]))
                # end if
                test_case._set_current_channel_to_expected_one(device_index=device_index, port_index=port_index)  # noqa
                feature_index = ChannelUtils.update_feature_mapping(test_case=test_case, feature_id=feature_id,
                                                                    skip_not_found=skip_not_found)
            # end if
            return feature_index
        # end def get_feature_index

        @classmethod
        def get_vlp_feature_index(cls, test_case, feature_id, device_index=None, port_index=None, skip_not_found=False):
            """
            Get feature index from feature id.

            First, get the feature index from the HID dispatcher if the feature is already available. If not,
            send the Root getFeature request to get the feature index from the device.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param feature_id: Feature ID
            :type feature_id: ``int`` or ``HexList``
            :param device_index: Device Index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port Index - OPTIONAL
            :type port_index: ``int`` or ``None``
            :param skip_not_found: Flag indicating that the method shall raise an error when the feature ID is
                                   not found if ``False`` and return 0 if ``True`` - OPTIONAL
            :type skip_not_found: ``bool``

            :return: Feature index
            :rtype: ``int``
            """
            feature_index = test_case.current_channel.hid_dispatcher.get_vlp_feature_index(feature_id=feature_id)
            if feature_index is None:
                vlp_root_feature_idx = test_case.current_channel.hid_dispatcher.get_vlp_feature_index(
                    feature_id=VLPRoot.FEATURE_ID)
                if vlp_root_feature_idx is None:
                    test_case.current_channel.hid_dispatcher.add_vlp_feature_entry(
                        feature_index=Root.FEATURE_INDEX, feature_id=VLPRoot.FEATURE_ID,
                        feature_version=int(test_case.f.SHARED.DEVICES.F_VLPRootFeatureVersion[0]))
                # end if
                test_case._set_current_channel_to_expected_one(device_index=device_index, port_index=port_index)  # noqa
                feature_index = ChannelUtils.update_vlp_feature_mapping(test_case=test_case, feature_id=feature_id,
                                                                    skip_not_found=skip_not_found)
            # end if
            return feature_index
        # end def get_vlp_feature_index

        @classmethod
        def enable_hidden_features(cls, test_case, device_index=None, port_index=None):
            """
            Send HID++ request to set enable hidden features.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port Index - OPTIONAL
            :type port_index: ``int`` or ``None``
            """
            device_index = device_index if device_index is not None else ChannelUtils.get_device_index(
                test_case=test_case)
            port_index = port_index if port_index is not None else ChannelUtils.get_port_index(test_case=test_case)

            enable_hidden_features_idx = cls.get_feature_index(
                test_case=test_case, feature_id=EnableHidden.FEATURE_ID, device_index=device_index,
                port_index=port_index)
            set_hidden = SetEnableHiddenFeatures(device_index=device_index, feature_index=enable_hidden_features_idx,
                                                 enable_byte=EnableHidden.ENABLED)
            ChannelUtils.send(test_case=test_case,
                              report=set_hidden,
                              response_queue_name=HIDDispatcher.QueueName.COMMON,
                              response_class_type=SetEnableHiddenFeaturesResponse)
        # end def enable_hidden_features

        @classmethod
        def set_oob_state(cls, test_case, enable_hidden_features=True, device_index=None, port_index=None):
            """
            Send HID++ request to set OOB State.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param enable_hidden_features: Send request to enable hidden feature - OPTIONAL
            :type enable_hidden_features: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port Index - OPTIONAL
            :type port_index: ``int`` or ``None``
            """
            feature_1805_index, feature_1805, device_index, port_index = cls.get_parameters(
                test_case=test_case, feature_id=OobState.FEATURE_ID, factory=OobStateFactory,
                device_index=device_index, port_index=port_index)

            if enable_hidden_features:
                # OOB State is tagged as engineering but not deactivatable (it is an exception), so no need to activate
                # any deactivatable features
                cls.enable_hidden_features(test_case=test_case, device_index=device_index, port_index=port_index)
            # end if

            set_oob_state = feature_1805.set_oob_state_cls(device_index=device_index, feature_index=feature_1805_index)
            ChannelUtils.send(test_case=test_case,
                              report=set_oob_state,
                              response_queue_name=HIDDispatcher.QueueName.COMMON,
                              response_class_type=feature_1805.set_oob_state_response_cls)
        # end def set_oob_state
    # end class HIDppHelper

    class ResetHelper:
        """
        Reset helper class
        """

        class ResetStrategy(StrEnum):
            """
            List of available DUT Reset Strategies.

            Related setting: ``pytestbox.base.features.ProductSubSystem.DeviceSubSystem.F_ResetStrategy``.
            """
            POWER_SLIDER = auto()
            POWER_SUPPLY = auto()
            USB_HUB = auto()
            DEBUGGER = auto()
        # end class ResetStrategy

        @classmethod
        def get_reset_strategy(cls, test_case):
            """
            Get the DUT Reset Strategy from the settings and return the matching Enum value if a strategy is set.

            Related setting: ``pytestbox.base.features.ProductSubSystem.DeviceSubSystem.F_ResetStrategy``

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :return: ResetStrategy enum value if a strategy was set, or else None
            :rtype: ``ResetStrategy or None``

            :raise: ``AssertionError``: if F_ResetStrategy setting string is not all lowercase
            :raise: ``ValueError``: if F_ResetStrategy setting string is not a valid value from ResetStrategy enum
            """
            reset_strategy = test_case.getFeatures().PRODUCT.DEVICE.F_ResetStrategy
            if reset_strategy is None:
                return None
            # end if

            assert reset_strategy.islower(), ('F_ResetStrategy setting must be written in lower case, '
                                              f'got "{reset_strategy}".')
            return cls.ResetStrategy(reset_strategy)
        # end def get_reset_strategy

        @classmethod
        def hardware_reset(cls, test_case, starting_voltage=None, delay=0.0):
            """
            Perform a hardware reset.
            This will NOT handle anything else (channel, connection events, ...) than the reset.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param starting_voltage: Value of the hardware reset voltage - OPTIONAL
            :type starting_voltage: ``float`` or ``None``
            :param delay: Delay to wait for the device to reset in seconds - OPTIONAL
            :type delay: ``int`` or ``float``

            :raise ``AssertionError``: No DUT Reset Strategy could be inferred from the available resources.
            :raise ``ValueError``: Invalid reset_strategy value.
            """
            # Get the DUT Reset Strategy from Device Settings
            reset_strategy = cls.get_reset_strategy(test_case=test_case)

            # If unset, define the DUT reset strategy based on the available resources
            if reset_strategy is None:
                device_not_powered_via_usb = (test_case.device.get_usb_ports_status()
                                              [test_case.device.CHARGING_PORT_NUMBER] is False)

                if test_case.power_slider_emulator is not None:
                    reset_strategy = cls.ResetStrategy.POWER_SLIDER
                elif test_case.power_supply_emulator is not None and device_not_powered_via_usb:
                    reset_strategy = cls.ResetStrategy.POWER_SUPPLY
                elif test_case.device_debugger is not None:
                    reset_strategy = cls.ResetStrategy.DEBUGGER
                # end if
                assert reset_strategy, 'No DUT Reset Strategy could be inferred from the available resources.'
            # end if

            match reset_strategy:
                case cls.ResetStrategy.POWER_SLIDER:
                    with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=test_case.device_debugger):
                        # Turn DUT power slider OFF
                        test_case.kosmos.sequencer.offline_mode = True
                        test_case.power_slider_emulator.power_off()
                        test_case.kosmos.pes.delay(delay_s=0.5)
                        if test_case.motion_emulator is not None and test_case.motion_emulator.get_module():
                            # Soft-reset motion emulator
                            test_case.motion_emulator.get_module().action_event.RESET()
                        # end if
                        # Turn DUT power slider ON
                        test_case.power_slider_emulator.power_on()
                        test_case.kosmos.sequencer.offline_mode = False
                        # Run test sequence
                        test_case.kosmos.sequencer.play_sequence()
                    # end with

                case cls.ResetStrategy.POWER_SUPPLY:
                    # Reset the DUT by power-cycling the power supply output
                    with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=test_case.device_debugger):
                        test_case.power_supply_emulator.restart_device(starting_voltage=starting_voltage)
                    # end with

                case cls.ResetStrategy.USB_HUB:
                    # Reset the DUT by power-cycling the USB port
                    with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=test_case.device_debugger):
                        usb_port_index = 1  # Rightmost USB port
                        test_case.device.set_usb_ports_status(ports_on_off_config={usb_port_index: False})   # Power OFF
                        test_case.device.set_usb_ports_status(ports_on_off_config={usb_port_index: True})    # Power ON
                    # end with

                case cls.ResetStrategy.DEBUGGER:
                    test_case.device_debugger.reset(soft_reset=False)

                case _:
                    raise ValueError(f'Invalid reset_strategy={reset_strategy}')
            # end match

            sleep(delay)
        # end def hardware_reset

        @staticmethod
        def hidpp_reset(test_case, device_index=None):
            """
            DUT reset using an HID++ Force Device Reset request (0x1802 feature)

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            """
            device_index = device_index if device_index is not None else ChannelUtils.get_device_index(
                test_case=test_case)

            feature_1802_index = ChannelUtils.update_feature_mapping(
                test_case=test_case, feature_id=DeviceReset.FEATURE_ID)
            DeviceBaseTestUtils.HIDppHelper.enable_hidden_features(test_case=test_case)
            force_device_reset = ForceDeviceReset(deviceIndex=device_index, featureId=feature_1802_index)
            try:
                ChannelUtils.send_only(test_case=test_case, report=force_device_reset)
            except TransportContextException as e:
                # This exception is only acceptable if the channel is on a USB device and for certain causes. This is
                # because the device sometimes resets before the acknowledgment of the USB communication. They have
                # been identified with libusbdriver, if the USB solution changes the list of caused might have to change
                # too.
                if test_case.current_channel.protocol == LogitechProtocol.USB and \
                        e.get_cause() in (TransportContextException.Cause.CONTEXT_ERROR_PIPE,
                                          TransportContextException.Cause.CONTEXT_ERROR_IO,
                                          TransportContextException.Cause.CONTEXT_ERROR_NO_DEVICE):
                    pass
                elif test_case.current_channel.protocol == LogitechProtocol.BLE and \
                        e.get_cause() == TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION:
                    # Hadron target occasionally disconnects from BLE before sending the response
                    pass
                else:
                    raise
                # end if
            # end try
            # Wait DUT to complete reset procedure
            # It seems that in Unifying it is not happening.
            if not isinstance(test_case.current_channel, ThroughEQuadReceiverChannel):
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test_case)
            # end if
        # end def hidpp_reset

        @staticmethod
        def power_switch_reset(test_case):
            """
            DUT reset using the Power Slider emulator

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :raise ``RuntimeError``: If Power Slider emulator is not available
            """
            if test_case.power_slider_emulator is not None:
                with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=test_case.device_debugger):
                    test_case.power_slider_emulator.reset()
                # end with
            else:
                raise RuntimeError("Power Slider emulator not available to reset")
            # end if
        # end def power_switch_reset

        @staticmethod
        def power_supply_reset(test_case):
            """
            DUT reset using the Power Supply emulator

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

            :raise ``RuntimeError``: If Power Supply emulator is not available
            """
            if test_case.power_supply_emulator is not None:
                with CommonBaseTestUtils.EmulatorHelper.debugger_closed(debugger=test_case.device_debugger):
                    test_case.power_supply_emulator.restart_device()
                # end with
            else:
                raise RuntimeError("Power Supply emulator not available to reset")
            # end if
        # end def power_supply_reset
    # end class ResetHelper

    @classmethod
    def enter_pairing_mode_ble(cls, test_case):
        """
        Enter pairing mode with BLE protocol enabled

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :raise ``AssertionError``: If there is no available mechanism to enter BLE pairing mode
        """
        if test_case.f.PRODUCT.F_IsGaming:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg="Gaming device: Enter BLE pairing mode")
            # ----------------------------------------------------------------------------------------------------------
            if not test_case.f.PRODUCT.F_IsPlatform and test_case.button_stimuli_emulator is not None and \
                len(set(test_case.button_stimuli_emulator.connected_key_ids).intersection(
                    {KEY_ID.CONNECT_BUTTON, KEY_ID.LS2_BLE_CONNECTION_TOGGLE, KEY_ID.BLE_CONNECTION})) > 0:
                if test_case.f.PRODUCT.F_IsMice:
                    # Wait connection LED timeout
                    sleep(5)
                    # Double click connection button to switch to BLE channel
                    test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.CONNECT_BUTTON, delay=0.05, repeat=2)
                else:
                    if KEY_ID.LS2_BLE_CONNECTION_TOGGLE in test_case.button_stimuli_emulator.connected_key_ids:
                        # Wait connection LED timeout
                        sleep(5)
                        # According to Gaming Functional lighten UE
                        # https://docs.google.com/document/d/1HYH3pSkqrYSelMjBzNNW0_GgX7i8M203YJ7JAshUfW0/edit#heading=h.5g93bvekip21
                        # When press connection toggle button the connection LED will be ON to display the connectivity
                        # status, then press the connection toggle button again before the connection LED is timeout,
                        # the connection will switch to another protocol and enter pairing mode if the pair information
                        # is not available.
                        test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.LS2_BLE_CONNECTION_TOGGLE,
                                                                    delay=0.05,
                                                                    repeat=2)
                    else:
                        test_case.button_stimuli_emulator.keystroke(key_id=KEY_ID.BLE_CONNECTION,
                                                                    duration=ButtonStimuliInterface.LONG_PRESS_DURATION)
                    # end if
                # end if
            elif test_case.device_debugger:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case=test_case, msg="Enter BLE pairing mode by change protocol in NVS")
                # ------------------------------------------------------------------------------------------------------
                test_case.post_requisite_reload_nvs = True
                DeviceBaseTestUtils.NvsHelper.change_protocol_gaming_devices(test_case=test_case,
                                                                             protocol=LogitechProtocol.BLE)
                DeviceBaseTestUtils.NvsHelper.force_last_gap_address(test_case=test_case)
            else:
                raise AssertionError("No available mechanism to enter BLE pairing mode.")
            # end if
        else:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case=test_case, msg="PWS device: Enter BLE pairing mode")
            # ----------------------------------------------------------------------------------------------------------
            # Todo use current host instead of forcing to 1
            # force host to 1 to have the same behaviour on keyboards and on mice
            test_case.button_stimuli_emulator.enter_pairing_mode(host_index=HOST.CH1, delay=0.5)
        # end if
        test_case.memory_manager.read_nvs(backup=False)
    # end def enter_pairing_mode_ble

    @staticmethod
    def power_on_device(test_case):
        """
        Power on device

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :raise ``Exception``: If no power supply or power slider emulator
        """
        if test_case.power_slider_emulator is not None:
            test_case.power_slider_emulator.power_on()
        elif test_case.power_supply_emulator is not None:
            test_case.power_supply_emulator.turn_on()
        else:
            raise Exception('No power supply or power slider emulator!')
        # end if
    # end def power_on_device

    @staticmethod
    def power_off_device(test_case):
        """
        Power off device

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

        :raise ``Exception``: If no power supply or power slider emulator
        """
        if test_case.power_slider_emulator is not None:
            test_case.power_slider_emulator.power_off()
        elif test_case.power_supply_emulator is not None:
            test_case.power_supply_emulator.turn_off()
        else:
            raise Exception('No power supply or power slider emulator!')
        # end if
    # end def power_off_device
# end class DeviceBaseTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# End of file
# ----------------------------------------------------------------------------------------------------------------------
