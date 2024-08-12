#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.basetestutils
:brief: pytestbox Base test utils module
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/04/23
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from contextlib import contextmanager
from enum import IntEnum
from math import ceil
from time import sleep
from warnings import warn

from pychannel.blechannel import BleChannel
# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import LinkEnablerInfo
# noinspection PyUnresolvedReferences
from pychannel.channelinterfaceclasses import LogitechProtocol
from pychannel.throughreceiverchannel import ThroughReceiverChannel
from pychannel.usbchannel import UsbChannel
from pyharness.extensions import WarningLevel
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatus
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.error import Hidpp2ErrorCodes
from pyhid.hidpp.features.error import VlpErrorCodes
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pylibrary.mcu.memorymanager import MODE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class CommonBaseTestUtils:
    """
    Base class for test utils.
    """
    MAX_NOTIFICATION_LOOP_COUNT = 5
    MAX_MESSAGE_COUNT = 4
    WAKE_UP_DEVICE_MAX_TRY = 3
    ENTER_BTLDR_MAX_TRY = 3

    class MessageChecker:
        """
        Base class to help message checking
        """
        class Version(IntEnum):
            """
            Version constants
            """
            ZERO = 0
            ONE = 1
            TWO = 2
            THREE = 3
            FOUR = 4
            FIVE = 5
            SIX = 6
            SEVEN = 7
            EIGHT = 8
            NINE = 9
            TEN = 10
            ELEVEN = 11
            TWELVE = 12
            THIRTEEN = 13
            FOURTEEN = 14
            FIFTEEN = 15
        # end class Version

        @classmethod
        def check_padding_is_zero(cls, test_case, message):
            """
            Check ``padding`` is 0 because all padding bytes should always be 0.

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``
            :param message: Message to check
            :type message: ``HidppMessage``
            """
            test_case.assertEqual(expected=0, obtained=int(Numeral(message.padding)), msg="Padding should be 0")
        # end def check_padding_is_zero

        @classmethod
        def check_device_index(cls, test_case, message, expected):
            """
            Check ``deviceIndex``

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``
            :param message: Message to check
            :type message: ``HidppMessage``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(expected=expected,
                                  obtained=message.deviceIndex,
                                  msg="The deviceIndex parameter differs from the one expected")
        # end def check_device_index

        @classmethod
        def check_feature_index(cls, test_case, message, expected):
            """
            Check ``featureIndex``

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``
            :param message: Message to check
            :type message: ``HidppMessage``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(expected=expected,
                                  obtained=message.featureIndex,
                                  msg="The featureIndex parameter differs from the one expected")
        # end def check_feature_index

        @classmethod
        def check_fields(cls, test_case, message, expected_cls, check_map=None):
            """
            Check message fields (generic method).

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``
            :param message: Message to check
            :type message: ``HidppMessage``
            :param expected_cls: Expected class of the message
            :type expected_cls: ``type`` or ``tuple of type``
            :param check_map: Map of the fields to check - OPTIONAL
            :type check_map: ``dict``
            """
            check_map = check_map if check_map is not None else cls.get_default_check_map(test_case)

            test_case.assertTrue(
                    expr=isinstance(message, expected_cls),
                    msg=f"Message wrong type: {message.__class__.__name__}, should be {expected_cls.__name__}")

            assert_errs = []
            for field in message.FIELDS:
                try:
                    if field.name == "padding" and ("padding" not in check_map or check_map["padding"] is None):
                        cls.check_padding_is_zero(test_case, message)
                    else:
                        check_map.update(
                                {field.name: check_map[alias] for alias in field.aliases if alias in check_map.keys()})
                        if field.name not in ["reportId", "deviceIndex", "featureIndex", "functionIndex", "softwareId",
                                              "report_id", "device_index", "feature_index", "function_index",
                                              "software_id", "sub_id", "address", "vlp_begin", "vlp_end", "vlp_ack",
                                              "vlp_sequence_number", "vlp_reserved", "vlp_payload"]:
                            test_case.assertIn(member=field.name,
                                               container=check_map.keys(),
                                               msg=f"A check method should be associated to field {field.name}")
                        # end if

                        if field.name in check_map and check_map[field.name] is not None:
                            check_map[field.name][0](test_case, message, check_map[field.name][1])
                        # end if
                    # end if
                except AssertionError as assert_err:
                    assert_errs.append(assert_err)
                # end try
            # end for
            test_case.assertListEqual(assert_errs, [], "No failures should be raised during fields checking")
        # end def check_fields

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Map field name to check method and expected value.
            Should be implemented for each message type.

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``

            :return: Map of the fields to check
            :rtype: ``dict``
            """
            raise NotImplementedError('Default check map not implemented')
        # end def get_default_check_map
    # end class MessageChecker

    class NvsHelper:
        """
        Non-Volatile Memory Helper class
        """
        @classmethod
        def clean_pairing_data(cls, test_case):
            """
            Parse NVS content from device and receiver memories to clean pairing information.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            for memory_manager in [test_case.receiver_memory_manager, test_case.device_memory_manager]:
                if memory_manager is not None:
                    nvs_reloaded = memory_manager.clean_pairing_data()

                    if test_case.backup_dut_channel is not None and \
                            memory_manager.chunk_type == MODE.RECEIVER and \
                            nvs_reloaded:
                        ChannelUtils.close_channel(test_case=test_case, channel=test_case.backup_dut_channel)
                    # end if
                # end if
            # end for
        # end def clean_pairing_data

        @classmethod
        def backup_nvs(cls, test_case):
            """
            Backup the nvs file

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            """
            test_case.memory_manager.read_nvs(backup=True)
            if test_case.debugger.CONNECT_UNDER_RESET:
                # Reopen Channel to avoid the issue of the device not being able to connect after a reset
                CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test_case)
                # end if
            # end if
        # end def backup_nvs

        @classmethod
        def restore_nvs(cls, test_case, backup=True, no_reset=False, ble_service_changed_required=False):
            """
            Restore the backed up nvs file

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param backup: Flag enabling the reload of the copy of the initial NVS - OPTIONAL
            :type backup: ``bool``
            :param no_reset: Flag enabling to reload the NVS without resetting the device, only stop and run - OPTIONAL
            :type no_reset: ``bool``
            :param ble_service_changed_required: Flag indicating that a second set of 'Device Connection' notifications
                                                 with link not established then link established is required. This only
                                                 applies to the BLE - OPTIONAL
            :type ble_service_changed_required: ``bool``
            """
            # noinspection PyBroadException
            try:
                CommonBaseTestUtils.load_nvs(test_case=test_case, backup=backup, no_reset=no_reset,
                                             ble_service_changed_required=ble_service_changed_required)
            except Exception:
                test_case.log_traceback_as_warning(supplementary_message="Exception in restore_nvs:",
                                                   warning_level=WarningLevel.ROBUSTNESS)
            # end try
        # end def restore_nvs

        @staticmethod
        def force_service_changed(test_case, nvs_backup_reload=False):
            """
            Force a service changed by reloading an empty chunk NVS_BLE_SYS_ATTR_USR_SRVCS_ID_0.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param nvs_backup_reload: Flag enabling reloading the copy of the initial NVS - OPTIONAL
            :type nvs_backup_reload: ``bool``
            """
            if test_case.device_memory_manager is not None:
                if not nvs_backup_reload or test_case.device_memory_manager.backup_nvs_parser is None:
                    test_case.device_memory_manager.read_nvs(backup=nvs_backup_reload)
                # end if

                if nvs_backup_reload:
                    test_case.device_memory_manager.backup_nvs_parser.add_new_chunk(
                            chunk_id='NVS_BLE_SYS_ATTR_USR_SRVCS_ID_0', data=HexList([0, 0, 0, 0]))
                else:
                    test_case.device_memory_manager.nvs_parser.add_new_chunk(
                            chunk_id='NVS_BLE_SYS_ATTR_USR_SRVCS_ID_0', data=HexList([0, 0, 0, 0]))
                # end if

                test_case.device_memory_manager.load_nvs(backup=nvs_backup_reload)
            # end if
        # end def force_service_changed

        @staticmethod
        def check_new_chunks(test_case, nvs_parser_1, nvs_parser_2, expected_chunks_ids, expected_chunks_data):
            """
            Check new chunks, matching expected chunks ids and chunks data in a NVS Parser compared to a
            previous one

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param nvs_parser_1: First NVS Parser
            :type nvs_parser_1: ``NvsParser``
            :param nvs_parser_2: Second NVS Parser
            :type nvs_parser_2: ``NvsParser``
            :param expected_chunks_ids: Expected chunks ids
            :type expected_chunks_ids: ``list[int]``
            :param expected_chunks_data: Expected chunks data
            :type expected_chunks_data: ``list[HexList]``
            """
            changed_chunks = nvs_parser_1.get_changed_chunks(nvs_parser_2)
            old_chunks = list(zip(*changed_chunks))[0]
            new_chunks = list(zip(*changed_chunks))[1]

            expected_chunks_data_length = len(expected_chunks_data) + 1 \
                if nvs_parser_1.chunk_id_map["NVS_CHUNK_METHOD"] else len(expected_chunks_data)

            test_case.assertEqual(expected=expected_chunks_data_length,
                                  obtained=len(new_chunks),
                                  msg=f"{expected_chunks_data_length} chunks should have changed (expected chunks + "
                                      f"padding)"
                                      if nvs_parser_1.chunk_id_map["NVS_CHUNK_METHOD"] else
                                      f"{expected_chunks_data_length} chunks should have changed")

            for chunk_index in range(0, len(expected_chunks_data)):
                test_case.assertEqual(expected=expected_chunks_ids[chunk_index],
                                      obtained=new_chunks[chunk_index].chunk_id,
                                      msg="New chunks do not match expected ones")
            # end for
            if nvs_parser_1.chunk_id_map["NVS_CHUNK_METHOD"]:
                test_case.assertEqual(expected=nvs_parser_2.chunk_id_map["NVS_EMPTY_CHUNK_ID"] & 0xFF,
                                      obtained=new_chunks[-1].chunk_id,
                                      msg="Last new chunk should be padding chunk")

                for chunk_index in range(0, len(expected_chunks_data)):
                    expected = HexList(list(expected_chunks_data[chunk_index]))
                    expected.addPadding(ceil(len(expected) / nvs_parser_2.nvs_word_size) * nvs_parser_2.nvs_word_size,
                                        pattern='00', fromLeft=False)
                    test_case.assertEqual(
                        obtained=HexList(new_chunks[chunk_index].chunk_data),
                        expected=expected,
                        msg="New chunks data should have the expected value, padded with 0x00")
                # end for

                test_case.assertListEqual(new_chunks[-1].chunk_data,
                                          [0xFF] * len(new_chunks[-1].chunk_data),
                                          msg="Padding should be only FF")

                test_case.assertEqual(expected=nvs_parser_1.chunk_id_map["NVS_EMPTY_CHUNK_ID"] & 0xFF,
                                      obtained=old_chunks[0].chunk_id,
                                      msg="New chunk should be written in previously empty chunk")

                test_case.assertNone(old_chunks[1], "No other chunk from previous NVS should be changed")
            else:
                for chunk_index in range(0, len(expected_chunks_data)):
                    test_case.assertEqual(
                        obtained=HexList(new_chunks[chunk_index].chunk_data),
                        expected=expected_chunks_data[chunk_index],
                        msg="New chunks data should have the expected value")
                # end for
            # end if
        # end def check_new_chunks
    # end class NvsHelper

    class HIDppHelper:
        """
        HID++ helper class
        """
        @staticmethod
        def check_hidpp10_error_message(test_case, error_message, sub_id, register_address, error_codes):
            """
            Help to check an HID++ 1.0 error message.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_message: Error message
            :type error_message: ``Hidpp1ErrorCodes``
            :param sub_id: Expected command sub id in the error message
            :type sub_id: ``int``
            :param register_address: Expected register address in the error message
            :type register_address: ``int``
            :param error_codes: List of possible error codes expected
            :type error_codes: ``list``
            """
            test_case.assertTupleEqual(
                    (sub_id, register_address),
                    (int(Numeral(error_message.command_sub_id)), int(Numeral(error_message.address))),
                    f'Sub Id={error_message.command_sub_id} and Address={error_message.address} in error message shall '
                    f'match expected values i.e. ({sub_id}, {register_address})')

            test_case.assertIn(int(error_message.error_code), error_codes,
                               f'Error code={error_message.error_code} in error message shall be one of the expected '
                               f'values i.e. {error_codes}')
        # end def check_hidpp10_error_message

        @staticmethod
        def check_hidpp20_error_message(test_case, error_message, feature_index, function_index, error_codes):
            """
            Help to check an HID++ 2.0 error message.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_message: Error message
            :type error_message: ``Hidpp2ErrorCodes``
            :param feature_index: Expected feature index in the error message
            :type feature_index: ``int`` or ``HexList``
            :param function_index: Expected function index in the error message
            :type function_index: ``int`` or ``HexList``
            :param error_codes: List of possible error codes expected
            :type error_codes: ``list``
            """
            test_case.assertTupleEqual(
                (int(Numeral(feature_index)), int(Numeral(function_index))),
                (int(Numeral(error_message.feature_index)), int(Numeral(error_message.function_index))),
                f'Feature index (i.e. {int(Numeral(error_message.feature_index))}) and function index (i.e. '
                f'{int(Numeral(error_message.function_index))}) in error message shall match expected values (i.e '
                f'{feature_index} and {function_index})')

            test_case.assertIn(int(error_message.error_code), error_codes,
                               f'Error code in error message should be as expected')
        # end def check_hidpp20_error_message

        @classmethod
        def send_report_wait_error(cls, test_case, report, error_type=None, error_codes=None):
            """
            Send report and wait for an error message

            :param test_case: The current test case
            :type test_case: Class inheriting ``CommonBaseTestCase``
            :param report: Report to send
            :type report: ``HidppMessage``
            :param error_type: Expected error type
            :type error_type: ``Hidpp1ErrorCodes`` or ``Hidpp2ErrorCodes`` or ``VlpErrorCodes``
            :param error_codes: Expected error codes
            :type error_codes: ``list[int]``

            :return: Error message received
            :rtype: ``Hidpp1ErrorCodes | Hidpp2ErrorCodes | VlpErrorCodes``
            """
            assert error_type in (Hidpp1ErrorCodes, Hidpp2ErrorCodes, VlpErrorCodes)
            assert error_codes is not None and isinstance(error_codes, list)

            if error_type == Hidpp1ErrorCodes:
                err_resp = test_case.send_report_wait_response(
                    report=report,
                    response_queue=test_case.hidDispatcher.receiver_error_message_queue,
                    response_class_type=error_type)
            else:
                err_resp = test_case.send_report_wait_response(
                    report=report,
                    response_queue=test_case.hidDispatcher.error_message_queue,
                    response_class_type=error_type)
            # end if

            # ----------------------------------------------------------------------------
            CommonBaseTestUtils.LogHelper.log_check(test_case, 'Check error response')
            # ----------------------------------------------------------------------------
            if error_type is Hidpp1ErrorCodes:
                cls.check_hidpp10_error_message(test_case=test_case,
                                                error_message=err_resp,
                                                sub_id=int(Numeral(report.sub_id)),
                                                register_address=int(Numeral(report.address)),
                                                error_codes=error_codes)
            elif error_type in [Hidpp2ErrorCodes, VlpErrorCodes]:
                cls.check_hidpp20_error_message(test_case=test_case,
                                                error_message=err_resp,
                                                feature_index=int(Numeral(report.featureIndex)),
                                                function_index=int(Numeral(report.functionIndex)),
                                                error_codes=error_codes)
            else:
                raise TypeError("Error type not supported")
            # end if
            return err_resp
        # end def send_report_wait_error
    # end class HIDppHelper

    class EmulatorHelper:
        """
        Helper class for emulators
        """
        @classmethod
        @contextmanager
        def debugger_closed(cls, debugger):
            """
            Close debugger while executing.

            :param debugger: Instance of the device debugger
            :type debugger: ``pytestbox.base.jlinkdebugger.JlinkDebugger`` or ``None``
            """
            if not debugger or not debugger.isOpen():
                yield
            else:
                debugger.close()
                try:
                    yield
                finally:
                    debugger.open()
                # end try
            # end if
        # end def debugger_closed

        @classmethod
        def get_current(cls, test_case, delay=0.0, samples=10):
            """
            Trigger a measurement of the current consumed by the DUT and return the measured value.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param delay: Delay before starting the measurement
            :type delay: ``float``
            :param samples: Number of samples to measure
            :type samples: ``int``

            :return: Current measure by the ina226 module. The value is rounded to 3 digits from decimal point.
            :rtype: ``float``

            :raise ``AssertionError``: If the number of samples is zero.
            """
            assert samples >= 1, "At least 1 sample is required"
            # The debugger will affect the current measurement result, so we shall close the connection and disconnect
            # the I/Os before starting the measurement
            with cls.debugger_closed(debugger=test_case.device_debugger):
                # Shall disconnect to J-Link before doing current measurement
                test_case.jlink_connection_control.disconnect()
                test_case.power_supply_emulator.configure_measurement_mode("current")
                sleep(delay)
                current = test_case.power_supply_emulator.get_current()
                for _ in range(1, samples):
                    current = (current + test_case.power_supply_emulator.get_current()) / 2
                    sleep(.2)
                # end for
                test_case.power_supply_emulator.configure_measurement_mode("tension")
                test_case.jlink_connection_control.connect()
            # end with

            return round(current, 3)
        # end def get_current
    # end class EmulatorHelper

    class UsbHubHelper:
        """
        Helper class for USB Hub control
        """

        @staticmethod
        def turn_on_all_generic_usb_ports(test_case, ports_to_turn_off=None):
            """
            Turn on all generic usb ports: 1, 2, 3, 4, 7 (excluding special purpose usb ports 5 and 6)

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``
            :param ports_to_turn_off: Ports to be turned off instead
            :type ports_to_turn_off: ``tuple[int] | None``
            """
            ports_status = {1: True, 2: True, 3: True, 4: True, 7: True}
            if ports_to_turn_off is not None:
                for i in ports_to_turn_off:
                    ports_status[i] = False
                # end for
            # end if

            ready_to_go, retries = test_case.device.set_usb_ports_status(ports_status)

            if ready_to_go and retries > 1:
                warn(f'It took {retries} tries to set USB ports to the required state: {ports_status}')
            # end if

            test_case.assertTrue(expr=ready_to_go, msg='The usb ports state is not correct')
        # end def turn_on_all_generic_usb_ports

        @staticmethod
        def turn_off_all_generic_usb_ports(test_case, ports_to_turn_on=None):
            """
            Turn off all generic usb ports: 1, 2, 3, 4, 7 (excluding special purpose usb ports 5 and 6)

            :param test_case: Current test case
            :type test_case: ``PyHarnessCase``
            :param ports_to_turn_on: Ports to be turned on instead
            :type ports_to_turn_on: ``tuple[int] | None``
            """
            ports_status = {1: False, 2: False, 3: False, 4: False, 7: False}
            if ports_to_turn_on is not None:
                for i in ports_to_turn_on:
                    ports_status[i] = True
                # end for
            # end if

            ready_to_go, retries = test_case.device.set_usb_ports_status(ports_status)

            if ready_to_go and retries > 1:
                warn(f'It took {retries} tries to set USB ports to the required state: {ports_status}')
            # end if

            test_case.assertTrue(expr=ready_to_go, msg='The usb ports state is not correct')
        # end def turn_off_all_generic_usb_ports
    # end class UsbHubHelper

    @classmethod
    def verify_communication_disconnection_then_reconnection(
            cls,
            test_case,
            device_connection_optional=False,
            ble_service_changed_required=False,
            link_enabler=LinkEnablerInfo.ALL_MASK,
            wireless_broadcast_event_required=True,
            open_channel_at_the_end=True):
        """
        Verify that the communication is disconnected then reconnected. It will mean different verification depending
        on the communication protocol used (USB, UNIFYING, BLE, etc...).

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param device_connection_optional: Flag indicating if the reception of DeviceConnection notification is
                                           optional and will be ignored if failed - OPTIONAL
        :type device_connection_optional: ``bool``
        :param ble_service_changed_required: Flag indicating if it is required to check if service changed
                                             notifications are received. This only applies to the BLE Pro
                                             protocol - OPTIONAL
        :type ble_service_changed_required: ``bool``
        :param link_enabler: List of link to enable or not. It should be constructed using the
                             information from ``LinkEnablerInfo`` - OPTIONAL
        :type link_enabler: ``int`` or ``BitStruct``
        :param wireless_broadcast_event_required: Flag indicating if it is required to check if the wireless broadcast
                                                  event is received. This only applies to the protocol through a
                                                  receiver - OPTIONAL
        :type wireless_broadcast_event_required: ``bool``
        :param open_channel_at_the_end: Flag indicating if it is required to open the channel at the end - OPTIONAL
        :type open_channel_at_the_end: ``bool``

        :raise ``AssertionError``: If either connection or service changed message is missing and the parameters
                                   ``device_connection_optional`` or ``ble_service_changed_required`` requires it
        """
        connection_timestamp = None
        with ChannelUtils.channel_open_state(
                test_case=test_case, open_state_required=False, link_enabler=link_enabler,
                open_associated_channel=True, close_associated_channel=False):
            if isinstance(test_case.current_channel, (BleChannel, UsbChannel)):
                if not device_connection_optional:
                    result = ChannelUtils.wait_usb_ble_channel_connection_state(
                        test_case=test_case,
                        channel=test_case.current_channel,
                        connection_state=False,
                        skip_error=True)

                    if not result:
                        test_case.log_warning(
                            message="USB or BLE Device disconnection missed", warning_level=WarningLevel.ROBUSTNESS)
                    # end if
                # end if

                ChannelUtils.wait_usb_ble_channel_connection_state(
                    test_case=test_case, channel=test_case.current_channel, connection_state=True)
            elif isinstance(test_case.current_channel, ThroughReceiverChannel):
                with ChannelUtils.channel_open_state(
                        test_case=test_case, channel=test_case.current_channel.receiver_channel,
                        open_state_required=True, link_enabler=link_enabler):
                    try:
                        if test_case.current_channel.protocol == LogitechProtocol.BLE_PRO and \
                                ble_service_changed_required:
                            # CR: lble, replace 0x55 notifications with 0x41
                            #   http://goldenpass.logitech.com:8080/c/ccp_fw/mpr01_gravity/+/6542
                            disconnection_connection_minimal_count = 2
                        else:
                            disconnection_connection_minimal_count = 1
                        # end if
                        connection_timestamp = cls.verify_link_not_established_then_link_established_notifications(
                            test_case=test_case,
                            disconnection_connection_minimal_count=disconnection_connection_minimal_count)
                    except (AssertionError, QueueEmpty) as exception:
                        if not device_connection_optional:
                            # Trigger an assertion error so that the result is handled as a test failure
                            raise AssertionError(exception)
                        else:
                            # It happens that the receiver does not see the disconnect/reconnect as notify worthy and
                            # just parasitic reconnection (supposition, not sure)
                            pass
                        # end if
                    # end try
                # end with
            # end if
        # end with

        if isinstance(test_case.current_channel, ThroughReceiverChannel) and wireless_broadcast_event_required:
            with ChannelUtils.channel_open_state(
                    test_case=test_case, channel=test_case.current_channel, open_state_required=True,
                    link_enabler=link_enabler):
                try:
                    cls.verify_wireless_device_status_broadcast_event_reconnection(
                        test_case=test_case, connection_timestamp=connection_timestamp)
                except (AssertionError, QueueEmpty) as no_msg_err:
                    if test_case.current_channel.protocol != LogitechProtocol.BLE_PRO or \
                            not device_connection_optional:
                        # Trigger an assertion error so that the result is handled as a test failure
                        raise AssertionError(no_msg_err)
                    else:
                        # WirelessDeviceStatus will not be sent back if the disconnection did not occur or the
                        # notification could be lost by the libusb library
                        pass
                    # end if
                # end try
            # end with
        # end if

        if open_channel_at_the_end and not test_case.current_channel.is_open:
            ChannelUtils.open_channel(test_case=test_case, link_enabler=link_enabler)
        # end if
    # end def verify_communication_disconnection_then_reconnection

    @classmethod
    def verify_link_not_established_then_link_established_notifications(cls, test_case,
                                                                        disconnection_connection_minimal_count=1):
        """
        Verify that at least a ``DeviceConnection`` with link not established and a ``DeviceConnection`` with link
        established are received.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param disconnection_connection_minimal_count: Number of group (``DeviceConnection`` link not established /
                                                       ``DeviceConnection`` link established) - OPTIONAL
        :type disconnection_connection_minimal_count: ``int``

        :return: timestamp of the last device connection notification received by the receiver
        :rtype: ``int | None``

        :raise ``AssertionError``: If a ``DeviceConnection`` message is not received after multiple wake up retries
        """
        last_connected = False
        notification_loop_counter = 0
        device_transport_id = ChannelUtils.get_transport_id(test_case=test_case)
        connection_timestamp = None

        while not last_connected and notification_loop_counter < cls.MAX_NOTIFICATION_LOOP_COUNT:
            # Wait for device disconnection
            wanted_state = False
            message_counter = 0
            while not wanted_state and message_counter < cls.MAX_MESSAGE_COUNT:
                device_connection = test_case.get_first_message_type_in_queue(
                    queue=test_case.hidDispatcher.receiver_connection_event_queue, class_type=DeviceConnection,
                    timeout=3)
                device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                    device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))

                if (device_transport_id & 0xFF) == to_int(device_info.device_comm_id_lsb) and \
                        ((device_transport_id & 0xFF00) >> 8) == to_int(device_info.device_comm_id_msb) and \
                        test_case.deviceIndex == to_int(device_connection.device_index) and \
                        to_int(device_info.device_info_link_status) == DeviceConnection.LinkStatus.LINK_NOT_ESTABLISHED:
                    wanted_state = True
                else:
                    message_counter += 1
                # end if
            # end while

            if message_counter >= cls.MAX_MESSAGE_COUNT:
                continue
            # end if

            # Wait for device connection
            wanted_state = False
            message_counter = 0
            wake_up_count = 0
            while not wanted_state and message_counter < cls.MAX_MESSAGE_COUNT:
                try:
                    device_connection = test_case.get_first_message_type_in_queue(
                        queue=test_case.hidDispatcher.receiver_connection_event_queue,
                        class_type=DeviceConnection,
                        timeout=4)
                except (AssertionError, QueueEmpty) as exception:
                    if wake_up_count > cls.WAKE_UP_DEVICE_MAX_TRY:
                        # Trigger an assertion error so that the result is handled as a test failure
                        raise AssertionError(exception)
                    # end if
                    test_case.button_stimuli_emulator.user_action()
                    wake_up_count += 1
                    continue
                    # end if
                # end try

                device_info_class = test_case.get_device_info_bit_field_structure_in_device_connection(
                        device_connection)
                device_info = device_info_class.fromHexList(HexList(device_connection.information))

                if (device_transport_id & 0xFF) == to_int(device_info.device_comm_id_lsb) and \
                        ((device_transport_id & 0xFF00) >> 8) == to_int(device_info.device_comm_id_msb) and \
                        test_case.deviceIndex == to_int(device_connection.device_index) and \
                        to_int(device_info.device_info_link_status) == DeviceConnection.LinkStatus.LINK_ESTABLISHED:
                    wanted_state = True
                    connection_timestamp = device_connection.timestamp
                else:
                    message_counter += 1
                # end if
            # end while

            if message_counter >= cls.MAX_MESSAGE_COUNT:
                continue
            # end if

            if wake_up_count > 0:
                test_case.log_warning(message=f"It took multiple tries to connect to the device: {wake_up_count}")
            # end if

            sleep(.2)

            notification_loop_counter += 1
            if notification_loop_counter >= disconnection_connection_minimal_count and \
                    test_case.is_current_hid_dispatcher_queue_empty(
                        queue=test_case.hidDispatcher.receiver_connection_event_queue):
                last_connected = True
            # end if
        # end while
        test_case.assertTrue(expr=notification_loop_counter >= disconnection_connection_minimal_count,
                             msg=f'The disconnection/connection counter ({notification_loop_counter}) differs from '
                                 f'the one expected ({disconnection_connection_minimal_count})')
        return connection_timestamp
    # end def verify_link_not_established_then_link_established_notifications

    @classmethod
    def verify_wireless_device_status_broadcast_event_reconnection(
            cls, test_case, timeout=3, device_index=None, connection_timestamp=None):
        """
        Verify (with assert) that the ``WirelessDeviceStatusBroadcastEvent`` (0x1D4B) is received and that its status is
        ``WirelessDeviceStatus.Status.RECONNECTION``.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
        :type timeout: ``int``
        :param device_index: Device index - OPTIONAL
        :type device_index: ``int`` or ``None``
        :param connection_timestamp: timestamp of the last device connection notification received by the receiver
        :type connection_timestamp: ``int | None``
        """
        wireless_device_status_broadcast_event = test_case.get_first_message_type_in_queue(
                queue=test_case.hidDispatcher.event_message_queue,
                class_type=WirelessDeviceStatusBroadcastEvent,
                timeout=timeout)
        if connection_timestamp is not None:
            while wireless_device_status_broadcast_event.timestamp < connection_timestamp:
                wireless_device_status_broadcast_event = test_case.get_first_message_type_in_queue(
                    queue=test_case.hidDispatcher.event_message_queue,
                    class_type=WirelessDeviceStatusBroadcastEvent,
                    timeout=timeout)
            # end while
        # end if
        test_case.assertEqual(expected=WirelessDeviceStatus.Status.RECONNECTION,
                              obtained=int(Numeral(wireless_device_status_broadcast_event.status)),
                              msg='The Status parameter differs from the one expected')
        if device_index is not None:
            test_case.assertEqual(expected=device_index,
                                  obtained=int(Numeral(wireless_device_status_broadcast_event.device_index)),
                                  msg='The device index parameter differs from the one expected')
        # end if
    # end def verify_wireless_device_status_broadcast_event_reconnection

    @classmethod
    def load_nvs(cls, test_case, backup=False, no_reset=False, ble_service_changed_required=False):
        """
        Method to reload the NVS and check reset connection has occurred.

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param backup: Flag enabling the reload of the copy of the initial NVS - OPTIONAL
        :type backup: ``bool``
        :param no_reset: Flag enabling to reload the NVS without resetting the device, only stop and run - OPTIONAL
        :type no_reset: ``bool``
        :param ble_service_changed_required: Flag indicating that a second set of 'Device Connection' notifications
                                             with link not established then link established is required. This only
                                             applies to the BLE - OPTIONAL
        :type ble_service_changed_required: ``bool``
        """
        closing_channel = False
        if test_case.current_channel.protocol == LogitechProtocol.USB and test_case.current_channel.is_open:
            ChannelUtils.close_channel(test_case=test_case)
            closing_channel = True
        # end if

        try:
            test_case.memory_manager.load_nvs(backup=backup, no_reset=no_reset)

            cls.verify_communication_disconnection_then_reconnection(
                test_case=test_case,
                device_connection_optional=no_reset,
                ble_service_changed_required=ble_service_changed_required)
        finally:
            if closing_channel:
                ChannelUtils.open_channel(test_case=test_case)
            # end if
        # end try
    # end def load_nvs
# end class CommonBaseTestUtils


# TODO : CommonBaseTestUtils LogHelper is kept for backward compatibility. It will be removed. Make sure to use
#  pytestbox.base.loghelper LogHelper in new implementations and update existing imports
CommonBaseTestUtils.LogHelper = LogHelper


class CommonTestUtilsInterface:
    """
    Interface class to define methods which have to be implemented by facade classes (DeviceTestUtils and
    ReceiverTestUtils)
    """
    class HIDppHelper:
        """
        HID++ helper interface for the facade classes
        """
        @classmethod
        def activate_features(cls, test_case, manufacturing=False, compliance=False, gotthard=False,
                              device_index=None, port_index=None):
            """
            Send HID++ sequence to activate the features locked in the field.

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param manufacturing: Enable Manufacturing features - OPTIONAL
            :type manufacturing: ``bool``
            :param compliance: Enable Compliance features - OPTIONAL
            :type compliance: ``bool``
            :param gotthard: Enable Gotthard - OPTIONAL
            :type gotthard: ``bool``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port Index - OPTIONAL
            :type port_index: ``int`` or ``None``
            """
            raise NotImplementedError("Method activate_features should be implemented in inheriting classes")
        # end def activate_features
    # end class HIDppHelper
# end class CommonTestUtilsInterface

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
