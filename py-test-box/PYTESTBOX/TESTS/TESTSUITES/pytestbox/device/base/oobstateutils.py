#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.oobstateutils
:brief: Helpers for ``OobState`` feature
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.oobstate import OobState
from pyhid.hidpp.features.common.oobstate import OobStateFactory
from pylibrary.emulator.emulatorinterfaces import HOST
from pylibrary.tools.threadutils import QueueEmpty
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.equaddeviceconnectionutils import EQuadDeviceConnectionUtils
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobStateTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``OobState`` feature
    """
    HOST_LED_TIMEOUT = 30000
    DEVICE_CONNECTION_RETRY_MAX_COUNT = 5

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=OobState.FEATURE_ID, factory=OobStateFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def set_oob_state(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None):
            """
            Process ``SetOobState``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SetOobStateResponse
            :rtype: ``SetOobStateResponse``
            """
            feature_1805_index, feature_1805, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1805.set_oob_state_cls(
                device_index=device_index,
                feature_index=feature_1805_index)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1805.set_oob_state_response_cls)
        # end def set_oob_state

        @classmethod
        def set_oob_state_and_power_cycle(cls, test_case):
            """
            Enable hidden features, send OOB State request, check OOB State response and do a powercycle on the device

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            """
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "Enable hidden features")
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.enable_hidden_features(test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Send SetOobStateRequest")
            # ----------------------------------------------------------------------------------------------------------
            response = cls.set_oob_state(test_case)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(test_case, "Check valid response")
            # ----------------------------------------------------------------------------------------------------------
            OobStateTestUtils.MessageChecker.check_fields(
                test_case=test_case, message=response, expected_cls=test_case.feature_1805.set_oob_state_response_cls,
                check_map={})

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(test_case, "Do a device powercycle")
            # ----------------------------------------------------------------------------------------------------------
            test_case.reset(hardware_reset=True,  verify_wireless_device_status_broadcast_event=False,
                            verify_connection_reset=False, delay=EQuadDeviceConnectionUtils.RESET_DELAY)

            if test_case.f.PRODUCT.F_IsGaming:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, "Unplug USB charging cable")
                # ------------------------------------------------------------------------------------------------------
                test_case.device.turn_off_usb_charging_cable(force=True)
            # end if
        # end def set_oob_state_and_power_cycle
    # end class HIDppHelper

    @classmethod
    def pair_device(cls, test_case, host=HOST.CH1 - 1, pre_pairing=True):
        """
        Pair device to a given host index based on connection protocol and restore the old hid dispatcher

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param host: The host index to pair the device to - OPTIONAL
        :type host: ``int``
        :param pre_pairing: Flag to perform the pre-pairing procedure - OPTIONAL
        :type pre_pairing: ``bool``
        """
        old_hid_dispatcher = test_case.current_channel.hid_dispatcher

        fw_config = test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION
        if fw_config.F_TransportEQuad:
            OobStateTestUtils.pair_equad_device(test_case, pre_pairing=pre_pairing)
        elif fw_config.F_TransportBTLE or fw_config.F_TransportBT:
            DevicePairingTestUtils.pair_device_to_host(test_case, host)
        elif (test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb and
              not ProtocolManagerUtils.is_corded_device_only(test_case=test_case)):
            ProtocolManagerUtils.switch_to_usb_channel(test_case)
        elif ProtocolManagerUtils.is_corded_device_only(test_case=test_case):
            cls.usb_unplug_and_replug(test_case)
        else:
            err_msg = f"Unable to pair device with current protocol: {test_case.current_channel.protocol}"
            raise RuntimeError(err_msg)
        # end if

        old_hid_dispatcher.dump_mapping_in_other_dispatcher(other_dispatcher=test_case.current_channel.hid_dispatcher)
    # end def pair_device

    @classmethod
    def pair_equad_device(cls, test_case, pre_pairing=True):
        """
        Pair device to an EQuad receiver and open channel

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        :param pre_pairing: Flag to perform the pre-pairing procedure - OPTIONAL
        :type pre_pairing: ``bool``

        raise ``AssertionError``: If the device channel is None after pairing procedure was done or
            the device index is not as expected
        """
        test_case.receiver_index = ChannelUtils.get_port_index(test_case=test_case)
        test_case.device.turn_off_usb_charging_cable(force=True)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(test_case, 'Perform new device connection')
        # --------------------------------------------------------------------------------------------------------------
        for i in range(cls.DEVICE_CONNECTION_RETRY_MAX_COUNT):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, f"Try paring the EQuad Device (try {i + 1})")
            # ----------------------------------------------------------------------------------------------------------
            try:
                device_channel = EQuadDeviceConnectionUtils.new_device_connection_and_pre_pairing(
                    test_case=test_case, unit_ids=test_case.f.SHARED.DEVICES.F_UnitIds_1, pre_pairing=pre_pairing,
                    disconnect=True)

                assert device_channel is not None, \
                    "Device channel should not be None after the pairing procedure was done"

                device_index = ChannelUtils.get_device_index(test_case, device_channel)

                test_case.assertEqual(
                    expected=0x01, obtained=device_index,
                    msg='Device index is expected to be 0x01 when a node is setup')

                test_case.pairing_slot = device_index
                test_case.current_channel = device_channel
                ChannelUtils.open_channel(test_case=test_case)

                break

            except (AssertionError, QueueEmpty):
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, "Retry paring the EQuad Device")
                # ------------------------------------------------------------------------------------------------------
            # end try
        # end for
    # end def pair_equad_device

    @classmethod
    def usb_unplug_and_replug(cls, test_case):
        """
        Perform device reset by disable/enable USB port simulating unplug/replug

        :param test_case: Current test case
        :type test_case: ``BaseTestCase``
        """
        splash_animation_duration = 5.5
        try:
            LibusbDriver.disable_usb_port(port_index=ChannelUtils.get_port_index(test_case=test_case))
        finally:
            LibusbDriver.enable_usb_port(port_index=ChannelUtils.get_port_index(test_case=test_case))
        # end try
        CommonBaseTestUtils.verify_communication_disconnection_then_reconnection(test_case=test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, "Sleep to allow time for device state transition animation to complete")
        # --------------------------------------------------------------------------------------------------------------
        sleep(splash_animation_duration)
    # end def usb_unplug_and_replug
# end class OobStateTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
