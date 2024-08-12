#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.devicetestutils
:brief: Unified interface for helpers requiring multiple features for device
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/05/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyhid.hidpp.features.common.deviceinformation import DeviceInformation
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBattery
from pyhid.hidpp.features.root import Root
from pytestbox.base.basetestutils import CommonTestUtilsInterface
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.base.protocolmanagerutils import ProtocolManagerUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicemanagedeactivatablefeaturesauthutils import \
    DeviceManageDeactivatableFeaturesAuthTestUtils
from pytestbox.device.base.unifiedbatteryutils import UnifiedBatteryTestUtils
from pytestbox.shared.base.deviceinformationutils import DeviceInformationTestUtils
from pytestbox.shared.base.dfucontrolutils import DfuControlTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceTestUtils(DeviceBaseTestUtils, CommonTestUtilsInterface):
    """
    Class to provide a unique interface for methods requiring multiple features utils.

    This is based on the facade design pattern idea.
    """
    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper, CommonTestUtilsInterface.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def activate_features(cls, test_case, manufacturing=False, compliance=False, gotthard=False,
                              device_index=None, port_index=None):
            # See ``CommonTestUtilsInterface.HIDppHelper.activate_features``

            # Send 0x1E00 enable hidden feature request
            cls.enable_hidden_features(test_case, device_index=device_index, port_index=port_index)
            if manufacturing or compliance or gotthard:
                man_deact_feature_index = cls.get_feature_index(
                    test_case=test_case, feature_id=ManageDeactivatableFeaturesAuth.FEATURE_ID,
                    device_index=device_index, port_index=port_index, skip_not_found=True)
                # Send open session, complete authentication and enable features
                if man_deact_feature_index != Root.FEATURE_NOT_FOUND:
                    DeviceManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(
                        test_case,
                        manufacturing=manufacturing,
                        compliance=compliance,
                        gotthard=gotthard,
                        start_session=True,
                        device_index=device_index,
                        port_index=port_index)
                # end if
            # end if
        # end def activate_features
    # end class HIDppHelper

    class ChargingHelper:
        """
        Charging helper class
        """

        @staticmethod
        def enter_charging_mode(test_case, source=UnifiedBattery.ExternalPowerStatus.WIRED):
            """
            Let the DUT enter charging mode

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param source: External power status - OPTIONAL
            :type source: ``UnifiedBattery.ExternalPowerStatus`` or ``int``

            :raise ``ValueError``: if the input source is unsupported
            """
            test_case.post_requisite_rechargeable = True
            if test_case.power_supply_emulator is not None:
                test_case.power_supply_emulator.recharge(enable=True)
            # end if

            if test_case.current_channel.protocol in LogitechProtocol.gaming_protocols() and \
                    test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
                if source == UnifiedBattery.ExternalPowerStatus.WIRED:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(
                        test_case,
                        f"Power on USB Port {test_case.device.CHARGING_PORT_NUMBER} and switch to USB channel")
                    # --------------------------------------------------------------------------------------------------
                    ProtocolManagerUtils.switch_to_usb_channel(test_case=test_case)
                elif source == UnifiedBattery.ExternalPowerStatus.WIRELESS:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case, "Power on the Crush Pad charging emulator")
                    # --------------------------------------------------------------------------------------------------
                    test_case.device.turn_on_crush_pad_charging_emulator()
                else:
                    raise ValueError(f'Unsupported source type: {source}')
                # end if
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Power on USB Port {test_case.device.CHARGING_PORT_NUMBER}")
                # ------------------------------------------------------------------------------------------------------
                test_case.device.turn_on_usb_charging_cable()
            # end if
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "Turn off the power output")
            # ----------------------------------------------------------------------------------------------------------
            if test_case.power_supply_emulator is not None:
                if (source == UnifiedBattery.ExternalPowerStatus.WIRED and
                        not test_case.power_supply_emulator.has_sink_current_capability):
                    test_case.power_supply_emulator.turn_off()
                # end if
            # end if
        # end def enter_charging_mode

        @staticmethod
        def exit_charging_mode(test_case, source=UnifiedBattery.ExternalPowerStatus.WIRED):
            """
            Let the DUT exit charging mode

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param source: External power status - OPTIONAL
            :type source: ``UnifiedBattery.ExternalPowerStatus`` or ``int``

            :raise ``ValueError``: if the input source is unsupported
            """
            if test_case.power_supply_emulator is not None:
                test_case.power_supply_emulator.recharge(enable=False)
            # end if
            test_case.post_requisite_rechargeable = False
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, "Turn on the power output")
            # ----------------------------------------------------------------------------------------------------------
            if test_case.power_supply_emulator is not None:
                if (source == UnifiedBattery.ExternalPowerStatus.WIRED and
                        not test_case.power_supply_emulator.has_sink_current_capability):
                    test_case.power_supply_emulator.turn_on()
                # end if
            # end if

            if test_case.backup_dut_channel.protocol in LogitechProtocol.gaming_protocols() and \
                    test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
                if source == UnifiedBattery.ExternalPowerStatus.WIRED:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(
                        test_case,
                        f"Power off USB Port {test_case.device.CHARGING_PORT_NUMBER} and switch to receiver channel")
                    # --------------------------------------------------------------------------------------------------
                    ProtocolManagerUtils.exit_usb_channel(test_case=test_case)
                elif source == UnifiedBattery.ExternalPowerStatus.WIRELESS:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_info(test_case, "Power off the Crush Pad charging emulator")
                    # --------------------------------------------------------------------------------------------------
                    test_case.device.turn_off_crush_pad_charging_emulator()
                else:
                    raise ValueError(f'Unsupported source type: {source}')
                # end if
            else:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_info(test_case, f"Power off USB Port {test_case.device.CHARGING_PORT_NUMBER}")
                # ------------------------------------------------------------------------------------------------------
                test_case.device.turn_off_usb_charging_cable()
            # end if
        # end def exit_charging_mode

        WIRED_CHARGING = 'wired_charging'
        WIRELESS_CHARGING = 'wireless_charging'
        WIRELESS_POWERED = 'wireless_powered'

        @classmethod
        def enter_specified_charging_power_status(cls, test_case, charging_status):
            """
            Enter the specified charging/powered status

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param charging_status: Device charging/powered status
            :type charging_status: ``str``

            :return: True if the specified charging status has been entered, False otherwise
            :rtype: ``bool``
            """
            enter_specific_changing_mode = False
            if charging_status == cls.WIRED_CHARGING and test_case.f.PRODUCT.DEVICE.BATTERY.F_USBCharging and \
                    UnifiedBatteryTestUtils.is_the_capability_supported(test_case=test_case,
                                                                        capability=UnifiedBattery.Flags.RECHARGEABLE):
                DeviceTestUtils.ChargingHelper.enter_charging_mode(
                    test_case=test_case, source=UnifiedBattery.ExternalPowerStatus.WIRED)
                test_case.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRED
                enter_specific_changing_mode = True
            elif charging_status == cls.WIRELESS_CHARGING and test_case.f.PRODUCT.DEVICE.BATTERY.F_WirelessCharging \
                    and UnifiedBatteryTestUtils.is_the_capability_supported(test_case=test_case,
                                                                            capability=UnifiedBattery.Flags.RECHARGEABLE):
                DeviceTestUtils.ChargingHelper.enter_charging_mode(
                    test_case=test_case, source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
                test_case.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
                enter_specific_changing_mode = True
            elif charging_status == cls.WIRELESS_POWERED and test_case.f.PRODUCT.DEVICE.BATTERY.F_WirelessCharging and \
                    UnifiedBatteryTestUtils.is_the_capability_supported(
                        test_case=test_case, capability=UnifiedBattery.Flags.REMOVABLE_BATTERY):
                DeviceTestUtils.ChargingHelper.enter_charging_mode(
                    test_case=test_case, source=UnifiedBattery.ExternalPowerStatus.WIRELESS)
                test_case.external_power_source = UnifiedBattery.ExternalPowerStatus.WIRELESS
                test_case.post_requisite_discharge_super_cap = True
                enter_specific_changing_mode = True
            # end if

            return enter_specific_changing_mode
        # end def enter_specified_charging_power_status
    # end class ChargingHelper

    @classmethod
    def jump_on_bootloader(cls, test_case, action_type=None):
        """
        Request the device to jump on the bootloader (if it is not already in bootloader mode).

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param action_type: The action type required - OPTIONAL
        :type action_type: ``int`` or ``None``

        :raise ``AssertionError``: If the device did not jump on the bootloader
        :raise ``Exception``: If the device could not jump on the bootloader after multiple tries
        """
        if test_case.current_channel.protocol in LogitechProtocol.gaming_protocols() and \
                test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_INFORMATION.F_TransportUsb:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(
                test_case, "Current protocol does not allow to jump on bootloader, switch to USB channel")
            # ----------------------------------------------------------------------------------------------------------
            ProtocolManagerUtils.switch_to_usb_channel(test_case)
        # end if

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case, 'Send DFU Control.startDfu to switch in bootloader')
        # --------------------------------------------------------------------------------------------------------------
        test_case.post_requisite_restart_in_main_application = True
        wanted_state = False
        entity_type = None
        try_counter = 0
        while not wanted_state and try_counter < cls.ENTER_BTLDR_MAX_TRY:
            # noinspection PyBroadException
            try:
                DfuControlTestUtils.target_enter_into_dfu_mode(test_case, action_type)

                # We check again if the device is on the bootloader
                entity_type = DeviceInformationTestUtils.get_active_entity_type(
                    test_case=test_case, device_index=ChannelUtils.get_device_index(test_case=test_case))
            except Exception:
                test_case.log_traceback_as_warning(
                    supplementary_message=f"Could not enter DFU mode (try number {try_counter})")
                if try_counter >= cls.ENTER_BTLDR_MAX_TRY - 1:
                    raise
                # end if
            # end try

            if entity_type is not None and entity_type == DeviceInformation.EntityTypeV1.BOOTLOADER:
                wanted_state = True
            else:
                try_counter += 1
            # end if
        # end while

        test_case.assertTrue(expr=wanted_state,
                             msg=f"Device did not jump on bootloader, tried {cls.ENTER_BTLDR_MAX_TRY} times")

        if try_counter > 0:
            test_case.log_warning(message=f"It took multiple tries to jump on bootloader: {try_counter}")
        # end if

        # Update configuration manager current expected mode
        test_case.config_manager.current_mode = test_case.config_manager.MODE.BOOTLOADER
    # end def jump_on_bootloader
# end class DeviceTestUtils

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
