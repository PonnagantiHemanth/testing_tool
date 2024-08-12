#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.powermodeutils
:brief:  Helpers for Power Mode feature
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from time import sleep

from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.powermodes import GetPowerModesTotalNumberResponse
from pyhid.hidpp.features.common.powermodes import PowerModes
from pyhid.hidpp.features.common.powermodes import PowerModesFactory
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.rgbeffectsutils import RGBEffectsTestUtils
from pytransport.transportcontext import TransportContextException


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PowerModesTestUtils(DeviceBaseTestUtils):
    """
    Test utils for Power Mode feature
    """

    CURRENT_MEASUREMENT_DELAY_TIME = 6
    OPTICAL_SENSOR_SLEEP_TIME = 96  # Robin sensor needs 96 seconds to enter sleep mode

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=PowerModes.FEATURE_ID, factory=PowerModesFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_power_mode_total_number(cls, test_case, device_index=None, port_index=None):
            """
            Force the device into deep sleep mode thru the 0x1830 SetPowerMode request.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: get power modes response
            :rtype: ``GetPowerModesTotalNumberResponse``
            """
            feature_1830_index, feature_1830, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_1830.get_power_modes_total_number_cls(
                device_index=device_index, feature_index=feature_1830_index)

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=feature_1830.get_power_modes_total_number_response_cls)
            return response
        # end def get_power_mode_total_number

        @classmethod
        def enter_deep_sleep(cls, test_case, device_index=None, port_index=None):
            """
            Force the device into deep sleep mode thru the 0x1830 SetPowerMode request.

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :raise ``AssertionError``: If the set power mode response parameter differs from the one expected
            :raise ``TransportContextException``:
                If the cause is not DEVICE_NOT_CONNECTED or DEVICE_DISCONNECTION_DURING_OPERATION
            """
            feature_1830_index, feature_1830, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Enable the hidden features to get access to the PowerModes feature')
            # ----------------------------------------------------------------------------------------------------------
            DeviceTestUtils.HIDppHelper.activate_features(test_case, manufacturing=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(test_case, 'Send SetPowerMode with powerModeNumber = 3')
            # ----------------------------------------------------------------------------------------------------------
            set_power_mode = feature_1830.set_power_mode_cls(device_index=device_index,
                                                             feature_index=feature_1830_index,
                                                             power_mode_number=PowerModes.DEEP_SLEEP)
            try:
                ChannelUtils.send_only(test_case=test_case, report=set_power_mode)
                get_possible = True
            except TypeError:
                # Since the deep sleep can be happening at every moment, it can be done before the device softdevice
                # even have the chance to return a response to the write request on the HID++ characteristic
                # During ble connections. This then triggers a host softdevice error that appears here, but the device
                # is correctly in sleep mode
                get_possible = False
                LogHelper.log_trace(test_case=test_case, msg="Device entered deep sleep before ble response received")
            except TransportContextException as e:
                # Since the deep sleep can be happening at every moment, it can be done before the device softdevice
                # even have the chance to return a response to the write request on the HID++ characteristic
                # During ble connections. This then triggers a host ble stack error that appears here, but the device
                # is correctly in sleep mode
                if e.get_cause() in [TransportContextException.Cause.DEVICE_NOT_CONNECTED,
                                     TransportContextException.Cause.DEVICE_DISCONNECTION_DURING_OPERATION]:
                    get_possible = False
                else:
                    raise
                # end if
            # end try

            if get_possible:
                set_power_mode_response = ChannelUtils.get_only(
                        test_case=test_case,
                        queue_name=HIDDispatcher.QueueName.COMMON,
                        class_type=feature_1830.set_power_mode_response_cls,
                        allow_no_message=True)  # The command response is optional and depends on the requested mode

                if set_power_mode_response:
                    LogHelper.log_info(test_case, f'SetPowerMode Response: {str(set_power_mode_response)}\n')

                    test_case.assertEqual(expected=set_power_mode.power_mode_number,
                                          obtained=set_power_mode_response.power_mode_number,
                                          msg='The set_power_mode_response parameter differs from the one expected')
                # end if
            # end if
            # The firmware will take time before entering deep sleep mode after receiving the 0x1830 request.
            sleep(5)
        # end def enter_deep_sleep
    # end class HIDppHelper

    class PowerModeHelper:
        """
        Power mode helper class
        """
        RUN = 'run_mode'
        WALK = 'walk_mode'
        SLEEP = 'sleep_mode'
        DEEP_SLEEP = 'deep_sleep_mode'

        @classmethod
        def enter_specified_power_mode(cls, test_case, power_mode):
            """
            Enter the specified power mode

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param power_mode: Device power mode
            :type power_mode: ``str``

            :return: Flag indicating that the DUT has entered the specified power mode
            :rtype: ``bool``
            """
            entered_power_mode = False
            if power_mode == cls.RUN:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(test_case, "Perform an user action to make the device in run mode")
                # ------------------------------------------------------------------------------------------------------
                test_case.button_stimuli_emulator.user_action()
                entered_power_mode = True
            elif power_mode == cls.WALK:
                # INDEX 1 is the time to enter walk mode
                time_to_enter_walk_mode = int(test_case.f.PRODUCT.FEATURES.COMMON.DEVICE_RESET.F_PowerModeDelay[1])
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    test_case, "Perform an user action and wait "
                               f"{time_to_enter_walk_mode} seconds to make the device in walk mode")
                # ------------------------------------------------------------------------------------------------------
                test_case.button_stimuli_emulator.user_action()
                sleep(time_to_enter_walk_mode)
                entered_power_mode = True
            elif power_mode == cls.SLEEP and test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_Enabled:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(
                    test_case, "Perform an user action and wait for a few seconds"
                               f"({test_case.f.PRODUCT.DEVICE.F_MaxWaitSleep}) to make the device in sleep mode")
                # ------------------------------------------------------------------------------------------------------
                if test_case.f.PRODUCT.FEATURES.GAMING.RGB_EFFECTS.F_Enabled:
                    RGBEffectsTestUtils.HIDppHelper.manage_rgb_power_mode(
                        test_case, get_or_set=RGBEffectsTestUtils.GetOrSet.SET,
                        rgb_power_mode=RGBEffectsTestUtils.PowerMode.POWER_SAVE_MODE)
                else:
                    test_case.button_stimuli_emulator.user_action()
                    sleep(test_case.f.PRODUCT.DEVICE.F_MaxWaitSleep)
                # end if
                entered_power_mode = True
            elif power_mode == cls.DEEP_SLEEP and test_case.f.PRODUCT.FEATURES.COMMON.UNIFIED_BATTERY.F_Enabled:
                if test_case.f.PRODUCT.FEATURES.COMMON.POWER_MODES.F_Enabled:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(test_case, "Send 0x1830.SetPowerMode with PowerModeNum=3(deep-sleep)")
                    # --------------------------------------------------------------------------------------------------
                    PowerModesTestUtils.HIDppHelper.enter_deep_sleep(test_case)
                else:
                    # --------------------------------------------------------------------------------------------------
                    LogHelper.log_step(
                        test_case,
                        f"Wait for {test_case.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep} seconds to enter deep-sleep mode")
                    # --------------------------------------------------------------------------------------------------
                    sleep(test_case.f.PRODUCT.DEVICE.F_MaxWaitDeepSleep)
                # end if
                entered_power_mode = True
            # end if

            return entered_power_mode
        # end def enter_specified_power_mode
    # end class PowerModeHelper
# end class PowerModesTestUtils

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
