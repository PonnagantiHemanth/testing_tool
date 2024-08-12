#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hidpp20.common.feature_1000
:brief: Validate HID common feature 0x1000
:author: Fred Chen <fchen7@logitech.com>
:date: 2019/02/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from queue import Empty
from time import sleep

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryLevelStatusBroadcastEvent
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryUnifiedLevelStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryCapability
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryCapabilityResponse
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryLevelStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryLevelStatusResponse
from pyhid.hidpp.features.batteryunifiedlevelstatus import ShowBatteryStatus
from pyhid.hidpp.features.batteryunifiedlevelstatus import ShowBatteryStatusResponse
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.util import compute_sup_values
from pylibrary.tools.util import compute_wrong_range
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pyusb.libusbdriver import LibusbDriver


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ApplicationBatteryUnifiedLevelStatusTestCase(BaseTestCase):
    """
    Validate Battery Unified Level Status TestCases
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.post_requisite_cleanup_message = False
        self.post_requisite_rechargeable = False
        self.post_requisite_turn_off_charging_cable = False

        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Send Root.GetFeature(0x1000)')
        # --------------------------------------------------------------------------------------------------------------
        self.feature_1000_index = ChannelUtils.update_feature_mapping(
            test_case=self, feature_id=BatteryUnifiedLevelStatus.FEATURE_ID)
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_post_requisite():
            if self.post_requisite_cleanup_message:
                ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)
                ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
            # end if
        # end with
        with self.manage_kosmos_post_requisite():
            if self.post_requisite_rechargeable:
                self.power_supply_emulator.recharge(enable=False)
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_turn_off_charging_cable:
                LibusbDriver.turn_off_usb_charging_cable()
            # end if
        # end with
        super().tearDown()
    # end def tearDown

    @features('Feature1000')
    @level('Interface')
    @services('PowerSupply')
    def test_get_battery_level_status(self):
        """
        Validate GetBatteryLevelStatus normal processing (Feature 0x1000)

        Battery Unified Level Status
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [0]GetBatteryLevelStatus
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Restart the device with input voltage to its maximum value')
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        self.reset(hardware_reset=True, starting_voltage=f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send BatteryUnifiedLevelStatus.GetBatteryLevelStatus')
        # --------------------------------------------------------------------------------------------------------------
        get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                         featureId=self.feature_1000_index)
        get_battery_level_status_response = ChannelUtils.send(
            test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetBatteryLevelStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryDischargeLevel value')
        # --------------------------------------------------------------------------------------------------------------
        level_tuple = battery_level_analyze(
            self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_AllBatteryDischargeLevels)
        self.assertEqual(expected=True,
                         obtained=int(get_battery_level_status_response.batteryDischargeLevel) in level_tuple,
                         msg="The batteryDischargeLevel parameter (%d) differs from the one expected"
                             % get_battery_level_status_response.batteryDischargeLevel)
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryDischargeNextLevel value')
        # --------------------------------------------------------------------------------------------------------------
        level_index = level_tuple.index(int(get_battery_level_status_response.batteryDischargeLevel))
        self.assertEqual(expected=level_tuple[level_index+1],
                         obtained=int(get_battery_level_status_response.batteryDischargeNextLevel),
                         msg='The batteryDischargeNextLevel parameter differs from the one expected')
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryStatus value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=BatteryStatus.DISCHARGING,
                         obtained=int(get_battery_level_status_response.batteryStatus),
                         msg='The batteryStatus parameter differs from the one expected')

        self.testCaseChecked("INT_1000_0001")
    # end def test_get_battery_level_status

    @features('Feature1000')
    @level('Time-consuming')
    @services('PowerSupply')
    def test_get_battery_level_with_whole_range(self):
        """
        Validate GetBatteryLevelStatus with level from highest to lowest (Feature 0x1000)

        Battery Unified Level Status
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [0]GetBatteryLevelStatus
        """
        self.post_requisite_cleanup_message = True

        # reset DUT with max voltage
        f = self.getFeatures()
        self.reset(hardware_reset=True, starting_voltage=f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        # Loop over voltage values from max to cut-off by small step
        voltage_steps = generate_v_test_steps(test_case=self)
        for mV_voltage in voltage_steps:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Use the power supply control tool to change the battery level '
                                     'from highest to lowest')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(mV_voltage/1000, fast_ramp=False)

            (expected_level_values, expected_next_level_values, exception_expected,
             exception_required, might_have_batt_event) = self.get_expected_levels(mV_voltage)

            measured_voltage = self.power_supply_emulator.get_voltage() * 1000

            # If the voltage is close to a battery level transition, wait awhile to see if the DUT send the notification
            # The timeout might be enlarge again for various products in the future to have a stable test result.
            if might_have_batt_event:
                try:
                    ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT, timeout=8.5,
                                          class_type=BatteryLevelStatusBroadcastEvent, check_first_message=False)
                except (AssertionError, Empty):
                    pass
                # end try
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send BatteryUnifiedLevelStatus.GetBatteryLevelStatus')
            # ----------------------------------------------------------------------------------------------------------
            get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=self.feature_1000_index)
            ChannelUtils.send_only(test_case=self, report=get_battery_level_status)
            response = None
            if exception_required:
                try:
                    # With wireless devices, the receiver will send a disconnection message
                    response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.RECEIVER_ERROR,
                                                     class_type=Hidpp1ErrorCodes)
                except (AssertionError, Empty):
                    # Corded devices are not expected to return anything when reaching cuf-on voltage
                    pass
                # end try
                # Free HIDMouse and HIDKeyboard queue
                ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)

            elif not exception_expected:
                response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON,
                                                 class_type=GetBatteryLevelStatusResponse)
            else:
                try:
                    response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON,
                                                     class_type=GetBatteryLevelStatusResponse)
                except (AssertionError, Empty):
                    try:
                        # With wireless devices, the receiver will send a disconnection message
                        response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.ERROR,
                                                         class_type=ErrorCodes)
                    except (AssertionError, Empty):
                        # Corded devices are not expected to return anything when reaching cuf-on voltage
                        pass
                    # end try
                # end try

                # Free HIDMouse and HIDKeyboard queue
                ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)
            # end if
            if isinstance(response, GetBatteryLevelStatusResponse):
                self.logTrace('GetBatteryLevelStatus Response at %d\n' % measured_voltage)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryDischargeLevel value')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=True,
                                 obtained=int(response.batteryDischargeLevel) in expected_level_values,
                                 msg='The batteryDischargeLevel parameter (%d) differs from the one expected at %dmV '
                                     '(%s), actual voltage: %dmV' % (int(response.batteryDischargeLevel), mV_voltage,
                                                                     str(expected_level_values),
                                                                     self.power_supply_emulator.get_voltage() * 1000))
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryDischargeNextLevel value')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=True,
                                 obtained=int(response.batteryDischargeNextLevel) in expected_next_level_values,
                                 msg='The batteryDischargeNextLevel parameter differs from the one expected(%s)'
                                     % (str(expected_next_level_values)))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryStatus value')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=True,
                                 obtained=int(response.batteryStatus) in [0, 3],
                                 msg='The batteryStatus parameter differs from the one expected')
            elif isinstance(response, Hidpp1ErrorCodes):
                self.logTrace('ErrorCodes Response at %d\n' % measured_voltage)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Check Error Codes ERR_RESOURCE_ERROR (9) returned by the receiver')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=HexList(Hidpp1ErrorCodes.ERROR_TAG),
                                 obtained=response.errorTag,
                                 msg='The received error code do not match the expected one !')

                self.assertEqual(expected=Hidpp1ErrorCodes.ERR_RESOURCE_ERROR,
                                 obtained=response.errorCode,
                                 msg='The received error code do not match the expected one !')
            # end if

            while not ChannelUtils.warn_queue_not_empty(
                    test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT):
                pass
            # end while
        # end for

        self.testCaseChecked("FUN_1000_0002")
    # end def test_get_battery_level_with_whole_range

    @features('Feature1000')
    @level('Functionality')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_get_battery_status(self):
        """
        Validate GetBatteryLevelStatus with level from highest to lowest (Feature 0x1000)

        Battery Unified Level Status
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [0]GetBatteryLevelStatus
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send BatteryUnifiedLevelStatus.GetBatteryLevelStatus')
        # --------------------------------------------------------------------------------------------------------------
        get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                         featureId=self.feature_1000_index)
        get_battery_level_status_response = ChannelUtils.send(
            test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetBatteryLevelStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate that status is equal to 0')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=BatteryStatus.DISCHARGING,
                         obtained=int(get_battery_level_status_response.batteryStatus),
                         msg='The batteryStatus parameter don t match discharging value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable connection to the USB port')
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_rechargeable = True
        self.power_supply_emulator.recharge(enable=True)
        self.post_requisite_turn_off_charging_cable = True
        LibusbDriver.turn_on_usb_charging_cable()
        # Sleep awhile for visual inspection on battery LED
        sleep(3)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate that the status is equal to 1')
        # --------------------------------------------------------------------------------------------------------------
        get_battery_level_status_response = ChannelUtils.send(
            test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetBatteryLevelStatusResponse)

        self.assertEqual(expected=BatteryStatus.RECHARGING,
                         obtained=int(get_battery_level_status_response.batteryStatus),
                         msg='The batteryStatus parameter don t match discharging value')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Use power supply control tool change the battery level to highest level')
        # --------------------------------------------------------------------------------------------------------------
        self.power_supply_emulator.recharge(enable=False)
        self.post_requisite_rechargeable = False

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate that status is equal to 3')
        # --------------------------------------------------------------------------------------------------------------
        get_battery_level_status_response = ChannelUtils.send(
            test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetBatteryLevelStatusResponse)

        self.assertEqual(expected=BatteryStatus.CHARGE_COMPLETE,
                         obtained=int(get_battery_level_status_response.batteryStatus),
                         msg='The batteryStatus parameter don t match discharging value')

        LibusbDriver.turn_off_usb_charging_cable()
        self.post_requisite_turn_off_charging_cable = False

        self.testCaseChecked("FUN_1000_0003")
    # end def test_get_battery_status

    @features('Feature1000')
    @level('Interface')
    @services('PowerSupply')
    def test_battery_level_status_broadcast_event(self):
        """
        Validate BatteryLevelStatusBroadcastEvent normal processing (Feature 0x1000)

        Battery Unified Level Status
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [event0]BatteryLevelStatusBroadcastEvent()
        """
        # Variable enabling to force a DUT power-off after any voltage decreasing test
        self.post_requisite_cleanup_message = True

        # reset DUT with max voltage
        f = self.getFeatures()
        self.reset(hardware_reset=True, starting_voltage=f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        for level_index in range(f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_NumberOfLevels-1):
            level_ranges = f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_BatteryRangeByLevel
            mv_voltage = int(level_ranges[(level_index*2) + 1])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Use the power supply control tool to change the battery level from '
                                     'numberOfLevels-1 to numberOdLevels-2')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(mv_voltage / 1000, fast_ramp=False)

            (expected_level_values, expected_next_level_values, exception_expected,
             exception_required, might_have_batt_event) = self.get_expected_levels(mv_voltage)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Get the message send from product')
            # ----------------------------------------------------------------------------------------------------------
            # Set timeout to 10 seconds due to FW has a low priority to update and send battery level status event
            response = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT, timeout=10,
                class_type=BatteryLevelStatusBroadcastEvent, check_first_message=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate BatteryLevelStatusBroadcastEvent.batteryDischargeLevel value')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=True,
                             obtained=int(response.batteryDischargeLevel) in expected_level_values,
                             msg='The batteryDischargeLevel parameter differs from the one expected at %dmV (%s)'
                                 % (mv_voltage, str(expected_level_values)))
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate BatteryLevelStatusBroadcastEvent.batteryDischargeNextLevel value')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=True,
                             obtained=int(response.batteryDischargeNextLevel) in expected_next_level_values,
                             msg='The batteryDischargeNextLevel parameter differs from the one expected(%s)'
                                 % (str(expected_next_level_values)))

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate BatteryLevelStatusBroadcastEvent.batteryStatus value')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=True,
                             obtained=int(response.batteryStatus) in [0, 3],
                             msg='The batteryStatus parameter differs from the one expected')
        # end for

        self.testCaseChecked("INT_1000_0004")
    # end def test_battery_level_status_broadcast_event

    @features('Feature1000')
    @level('Business')
    @services('PowerSupply')
    # @services('LedIndicator')
    def test_get_battery_level_for_discharging(self):
        """
        Validate GetBatteryLevelStatus discharging Business case sequence (Feature 0x1000)

        Battery Unified Level Status
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [0]GetBatteryLevelStatus()
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [event0]BatteryLevelStatusBroadcastEvent()
        """
        # Variable enabling to force a DUT power-off after any voltage decreasing test
        self.post_requisite_cleanup_message = True

        # reset DUT with max voltage
        f = self.getFeatures()
        self.reset(hardware_reset=True, starting_voltage=f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage)

        # Loop over voltage values from max to cut-off by small step
        voltage_steps = generate_v_test_steps(test_case=self)
        for mV_voltage in voltage_steps:
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Use the power supply control tool to change the battery level '
                                     'in the range[numberOfLevels-1..0]')
            # ----------------------------------------------------------------------------------------------------------
            self.power_supply_emulator.set_voltage(mV_voltage / 1000, fast_ramp=False)

            (expected_level_values, expected_next_level_values, exception_expected,
             exception_required, might_have_batt_event) = self.get_expected_levels(mV_voltage)

            measured_voltage = self.power_supply_emulator.get_voltage() * 1000

            # If set v in the range of battery level transition, wait awhile for DUT to complete status update
            # The timeout might be enlarge again for various products in the future to have a stable test result.
            if might_have_batt_event:
                try:
                    ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.BATTERY_EVENT, timeout=8.5,
                                          class_type=BatteryLevelStatusBroadcastEvent, check_first_message=False)
                except (AssertionError, Empty):
                    pass
                # end try
            # end if

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, 'Send BatteryUnifiedLevelStatus.GetBatteryLevelStatus')
            # ----------------------------------------------------------------------------------------------------------
            get_battery_level_status = GetBatteryLevelStatus(
                deviceIndex=ChannelUtils.get_device_index(test_case=self), featureId=self.feature_1000_index)
            ChannelUtils.send_only(test_case=self, report=get_battery_level_status)
            if not exception_expected:
                response = ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON,
                                                 class_type=GetBatteryLevelStatusResponse)
            else:
                try:
                    ChannelUtils.get_only(test_case=self, queue_name=HIDDispatcher.QueueName.COMMON,
                                          class_type=GetBatteryLevelStatusResponse)
                except (AssertionError, Empty):
                    # Free HIDMouse and HIDKeyboard queue
                    ChannelUtils.empty_queue(self, queue_name=HIDDispatcher.QueueName.HID)
                finally:
                    # Cut-off upper limit value reached - end of test loop
                    break
                # end try
            # end if
            if isinstance(response, GetBatteryLevelStatusResponse):
                self.logTrace('GetBatteryLevelStatus Response at %d\n' % measured_voltage)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the GetBatteryLevelStatus.batteryDischargeLevel value '
                                          'and BatteryLevelStatusBroadcastEvent.batteryDischargeLevel')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=True,
                                 obtained=int(response.batteryDischargeLevel) in expected_level_values,
                                 msg='The batteryDischargeLevel parameter (%d) differs from the one expected at %dmV '
                                     '(%s)' % (int(response.batteryDischargeLevel), mV_voltage,
                                               str(expected_level_values)))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate the GetBatteryLevelStatus.batteryDischargeNextLevel value '
                                          'and BatteryLevelStatusBroadcastEvent.batteryDischargeNextLevel')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=True,
                                 obtained=int(response.batteryDischargeNextLevel) in expected_next_level_values,
                                 msg='The batteryDischargeNextLevel parameter differs from the one expected(%s)'
                                     % (str(expected_next_level_values)))

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryStatus value')
                # ------------------------------------------------------------------------------------------------------
                self.assertEqual(expected=True,
                                 obtained=int(response.batteryStatus) in [0, 3],
                                 msg='The batteryStatus parameter differs from the one expected')
            # end if

            while not ChannelUtils.warn_queue_not_empty(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT):
                pass
            # end while
        # end for

        self.testCaseChecked("BUS_1000_0005")
    # end def test_get_battery_level_for_discharging

    @features('Feature1000')
    @level('Time-consuming')
    @services('PowerSupply')
    @services('Rechargeable')
    def test_get_battery_level_for_recharging(self):
        """
        Validate GetBatteryLevelStatus recharging Business case sequence (Feature 0x1000)

        Battery Unified Level Status
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [0]GetBatteryLevelStatus()
         batteryDischargeLevel, batteryDischargeNextLevel, batteryStatus [event0]BatteryLevelStatusBroadcastEvent()
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Use the power supply control tool to change the battery level '
                                 'in the range[0..numberOfLevels-1]')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetBatteryLevelStatus and get the message send from product')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the GetBatteryLevelStatus.batteryDischargeLevel value and '
                                  'BatteryLevelStatusBroadcastEvent.batteryDischargeLevel')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the GetBatteryLevelStatus.batteryDischargeNextLevel value '
                                  'and BatteryLevelStatusBroadcastEvent.batteryDischargeNextLevel')
        # --------------------------------------------------------------------------------------------------------------

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryLevelStatus.batteryStatus value')
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("FUN_1000_0006")
    # end def test_get_battery_level_for_recharging

    @features('Feature1000')
    @level('Interface')
    def test_get_battery_capability(self):
        """
        Validate GetBatteryCapability normal processing (Feature 0x1000)

        Battery Unified Level Status
         numberOfLevels, flags, nominalBatteryLife, batteryCriticalLevel [1]GetBatteryCapability
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send BatteryUnifiedLevelStatus.GetBatteryCapability')
        # --------------------------------------------------------------------------------------------------------------
        get_battery_capability = GetBatteryCapability(
            deviceIndex=ChannelUtils.get_device_index(test_case=self), featureId=self.feature_1000_index)
        get_battery_capability_response = ChannelUtils.send(
            test_case=self, report=get_battery_capability, response_queue_name=HIDDispatcher.QueueName.COMMON,
            response_class_type=GetBatteryCapabilityResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryCapability.numberOfLevels value')
        # --------------------------------------------------------------------------------------------------------------
        f = self.getFeatures()
        self.assertEqual(expected=f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_NumberOfLevels,
                         obtained=int(get_battery_capability_response.numberOfLevels),
                         msg='The numberOfLevels parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryCapability.flags value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_Flags,
                         obtained=int(get_battery_capability_response.flags),
                         msg='The flags parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryCapability.nominalBatteryLife value')
        # --------------------------------------------------------------------------------------------------------------
        forced_value = None
        first_char = str(get_battery_capability_response.nominalBatteryLife)[0]
        first_char_dict = {'E': 'years', 'C': 'days', 'A': 'hours', '8': 'minutes', '6': 'seconds', '4': 'milliseconds',
                           '2': 'microseconds', '0': 'nanoseconds'}
        if first_char_dict[first_char]:
            forced_value = str(int(get_battery_capability_response.nominalBatteryLife) - (int(first_char, 16) << 12)) \
                           + ' ' + str(first_char_dict[first_char])
        # end if
        self.assertEqual(expected=f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_NominalBatteryLife,
                         obtained=forced_value,
                         msg='The nominalBatteryLife parameter differs from the one expected')

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate GetBatteryCapability.batteryCriticalLevel value')
        # --------------------------------------------------------------------------------------------------------------
        self.assertEqual(expected=f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_BatteryCriticalLevel,
                         obtained=int(get_battery_capability_response.batteryCriticalLevel),
                         msg='The batteryCriticalLevel parameter differs from the one expected')

        self.testCaseChecked("INT_1000_0007")
    # end def test_get_battery_capability

    @features('Feature1000v1')
    @level('Interface')
    # @services('LedIndicator')
    def test_show_battery_status(self):
        """
        Validate ShowBatteryStatus normal processing (Feature 0x1000)

        Battery Unified Level Status
         [2]ShowBatteryStatus
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send BatteryUnifiedLevelStatus.ShowBatteryStatus')
        # --------------------------------------------------------------------------------------------------------------
        # --------------------------------------------------------------------------------------------------------------
        # TODO Change test spec because it does send a response
        LogHelper.log_check(self, 'Validate that the device will not return any response or error')
        # --------------------------------------------------------------------------------------------------------------
        show_battery_status = ShowBatteryStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                featureId=self.feature_1000_index)
        ChannelUtils.send(test_case=self, report=show_battery_status,
                          response_queue_name=HIDDispatcher.QueueName.COMMON,
                          response_class_type=ShowBatteryStatusResponse)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Validate the status of led lightening')
        # --------------------------------------------------------------------------------------------------------------
        # TODO

        self.testCaseChecked("INT_1000_0008")
    # end def test_show_battery_status

    @features('Feature1000v0')
    @level('ErrorHandling')
    def test_wrong_function_index_v0(self):
        """
        Validate BatteryUnifiedLevelStatus robustness processing for v0

        Function indexes valid range [0..1],
            Tests wrong indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetBatteryLevelStatus with wrong index value')
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(BatteryUnifiedLevelStatus.MAX_FUNCTION_INDEX_V0+1)],
                                                  max_value=0xF):
            get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=self.feature_1000_index)
            get_battery_level_status.functionIndex = int(function_index)
            get_battery_level_status_response = ChannelUtils.send(
                test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId (7)  returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_battery_level_status.featureIndex,
                             obtained=get_battery_level_status_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_battery_level_status_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for

        self.testCaseChecked("ERR_1000_0001")
    # end def test_wrong_function_index_v0

    @features('Feature1000v1')
    @level('ErrorHandling')
    def test_wrong_function_index_v1(self):
        """
        Validate BatteryUnifiedLevelStatus robustness processing for v1

        Function indexes valid range [0..2],
            Tests wrong indexes
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetBatteryLevelStatus with wrong index value')
        # --------------------------------------------------------------------------------------------------------------
        for function_index in compute_wrong_range([x for x in range(BatteryUnifiedLevelStatus.MAX_FUNCTION_INDEX_V1+1)],
                                                  max_value=0xF):
            get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=self.feature_1000_index)
            get_battery_level_status.functionIndex = int(function_index)
            get_battery_level_status_response = ChannelUtils.send(
                test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.ERROR,
                response_class_type=ErrorCodes)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check Error Codes InvalidFunctionId (7)  returned by the device')
            # ----------------------------------------------------------------------------------------------------------
            self.assertEqual(expected=get_battery_level_status.featureIndex,
                             obtained=get_battery_level_status_response.featureIndex,
                             msg='The request and response feature indexes differ !')
            self.assertEqual(expected=ErrorCodes.INVALID_FUNCTION_ID,
                             obtained=get_battery_level_status_response.errorCode,
                             msg='The received error code do not match the expected one !')
        # end for

        self.testCaseChecked("ERR_1000_0002")
    # end def test_wrong_function_index_v1

    @features('Feature1000')
    @level('Robustness')
    def test_other_software_id(self):
        """
        Validate BatteryUnifiedLevelStatus softwareId are ignored

        getBatteryLevelStatus = [0]GetBatteryLevelStatus()
        Request: 0x10.DeviceIndex.FeatureIndex.0x00.0x00.0x00.0x00
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetBatteryLevelStatus with several value for softwareId')
        # --------------------------------------------------------------------------------------------------------------
        for software_id in range(1, 0x10):
            get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=self.feature_1000_index)
            get_battery_level_status.softwareId = software_id
            get_battery_level_status_response = ChannelUtils.send(
                test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=GetBatteryLevelStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetBatteryLevelStatus response received')
            # ----------------------------------------------------------------------------------------------------------
            level_tuple = battery_level_analyze(
                self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_AllBatteryDischargeLevels)
            self.assertEqual(expected=True,
                             obtained=int(get_battery_level_status_response.batteryDischargeLevel) in level_tuple,
                             msg="The batteryDischargeLevel parameter (%d) differs from the one expected"
                                 % get_battery_level_status_response.batteryDischargeLevel)
        # end for

        self.testCaseChecked("ROB_1000_0003")
    # end def test_other_software_id

    @features('Feature1000')
    @level('Robustness')
    def test_other_padding_bytes(self):
        """
        Validate BatteryUnifiedLevelStatus padding bytes are ignored

        getBatteryLevelStatus = [0]GetBatteryLevelStatus()
        Request: 0x10.DeviceIndex.FeatureIndex.0x0F.0xAA.0xBB.0xCC
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, 'Send GetBatteryLevelStatus with several value for padding')
        # --------------------------------------------------------------------------------------------------------------
        for padding_byte in compute_sup_values(HexList(Numeral(GetBatteryLevelStatus.DEFAULT.PADDING,
                                                               GetBatteryLevelStatus.LEN.PADDING//8))):
            get_battery_level_status = GetBatteryLevelStatus(deviceIndex=ChannelUtils.get_device_index(test_case=self),
                                                             featureId=self.feature_1000_index)
            get_battery_level_status.padding = padding_byte
            get_battery_level_status_response = ChannelUtils.send(
                test_case=self, report=get_battery_level_status, response_queue_name=HIDDispatcher.QueueName.COMMON,
                response_class_type=GetBatteryLevelStatusResponse)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, 'Validate GetBatteryLevelStatus response received')
            # ----------------------------------------------------------------------------------------------------------
            level_tuple = battery_level_analyze(
                self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_AllBatteryDischargeLevels)
            self.assertEqual(expected=True,
                             obtained=int(get_battery_level_status_response.batteryDischargeLevel) in level_tuple,
                             msg="The batteryDischargeLevel parameter (%d) differs from the one expected"
                                 % get_battery_level_status_response.batteryDischargeLevel)
        # end for

        self.testCaseChecked("ROB_1000_0004")
    # end def test_other_padding_bytes

    def get_expected_levels(self, voltage):
        """
        Provide expected results per voltage value

        :param voltage: The targeted voltage
        :type voltage: ``int``

        :return: A tuple with the expected level, the next level, a flag indicating a possible cut-off,
                 a flag indicating a mandatory cut-off and a flag indicating an expected battery event
        :rtype: ``tuple[int, int, bool, bool, bool]``
        """
        expected_level_values = None
        expected_next_level_values = None
        exception_expected = False
        exception_required = False
        might_have_batt_event = False

        level_tuple = battery_level_analyze(
            self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_AllBatteryDischargeLevels)
        level_ranges = self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_BatteryRangeByLevel
        level_count = self.f.PRODUCT.FEATURES.COMMON.BATTERY_UNIFIED_LEVEL_STATUS.F_NumberOfLevels
        for level_index in range(level_count):
            if voltage >= int(level_ranges[level_index*2]):
                expected_level_values = level_tuple[level_index:level_index+1]
                expected_next_level_values = level_tuple[level_index+1:level_index+2]
                if level_index == (level_count - 1):
                    exception_expected = True
                # end if
                break
            elif voltage >= int(level_ranges[(level_index*2)+1]):
                expected_level_values = level_tuple[level_index:level_index+2]
                expected_next_level_values = level_tuple[level_index+1:level_index+3]
                if level_index == (level_count - 1):
                    # At this stage, the cuf-off could occur
                    exception_expected = True
                # end if
                might_have_batt_event = True
                break
            elif level_index == (level_count - 1):
                exception_required = True
            # end if
        # end for
        return (expected_level_values, expected_next_level_values, exception_expected, exception_required,
                might_have_batt_event)
    # end def get_expected_levels
# end class ApplicationBatteryUnifiedLevelStatusTestCase


# To analyze each battery discharge level
def battery_level_analyze(levels):
    """
    Format the battery level parameter

    :param levels: The list of states of charge triggering a level transition
                   (e.g. F_AllBatteryDischargeLevels = "90 50 20 5 0")
    :type levels: ``str``

    :return: formatted battery level
    :rtype: ``tuple[int]``
    """
    return tuple(int(x) for x in levels.split(" "))
# end def battery_level_analyze


def generate_v_test_steps(test_case):
    """
    Generate voltage list for test

    :param test_case: The current test case
    :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``

    :return: The voltage list
    :rtype: ``list[int]``
    """
    f = test_case.getFeatures()
    voltage_steps = list(range(int(float(f.PRODUCT.DEVICE.BATTERY.F_MaximumVoltage) * 1000),
                               int(float(f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage) * 1000 + 50),
                               -50))
    voltage_steps.extend(list(range(int(float(f.PRODUCT.DEVICE.BATTERY.F_NominalVoltage) * 1000 + 50),
                                    int(float(f.PRODUCT.DEVICE.BATTERY.F_CutOffVoltage) * 1000 - 110),
                                    -10)))
    return voltage_steps
# end def generate_v_test_steps

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
