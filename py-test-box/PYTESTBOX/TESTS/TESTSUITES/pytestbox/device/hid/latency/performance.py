#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.latency.performance
:brief: Hid Latency Performance test suite
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/08/29
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from unittest import skip

from pychannel.channelinterfaceclasses import LogitechProtocol
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pylibrary.tools.hexlist import HexList
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.bleprotocolutils import ReportReferences
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.ble.gatt.hids.hids import GattHIDSApplicationTestCases
from pytestbox.device.hid.latency.latency import LatencyTestCase
from pytestbox.device.ls2connectionscheme.portconfiguration import PortConfiguration


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class LatencyPerformanceLS2TestCase(LatencyTestCase):
    """
    Test case for latency measurement through the LS2 communication protocol on Sleep and Deep Sleep Mode
    """
    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Sleep mode
        """
        self.measure_and_validate_make_latency_in_sleep_mode()
        self.testCaseChecked("PER_LATY_LS2_0005")
    # end def test_measure_make_latency_in_sleep_mode

    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Break) in Sleep mode
        """
        self.measure_and_validate_break_latency_in_sleep_mode()
        self.testCaseChecked("PER_LATY_LS2_0006")
    # end def test_measure_break_latency_in_sleep_mode

    @features('Unifying')
    @features('SwitchLatency')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_deep_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Deep Sleep mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self,
                           msg="Power off all generic usb ports except LS2 receiver port to make sure no "
                               "interferences from other receivers.")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(
            test_case=self, ports_to_turn_on=(PortConfiguration.PRE_PAIRED_RECEIVER_PORT,))
        self.post_requisite_turn_on_all_generic_usb_ports = True

        self.measure_and_validate_make_latency_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_LS2_0007")
    # end def test_measure_make_latency_in_deep_sleep_mode

    @features('GamingDevice')
    @features('Mice')
    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    @services('OpticalSensor')
    def test_measure_make_latency_in_lift_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Lift mode
        """
        self.measure_and_validate_make_latency_in_lift_mode()
        self.testCaseChecked("PER_LATY_LS2_0008")
    # end def test_measure_make_latency_in_lift_mode

    @features('Mice')
    @features('Unifying')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_sleep_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Sleep mode
        """
        self.measure_and_validate_x_motion_in_sleep_mode()
        self.testCaseChecked("PER_LATY_LS2_0011")
    # end def test_x_motion_in_sleep_mode

    @features('Mice')
    @features('Unifying')
    @features('MotionLatency')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_deep_sleep_mode(self):
        """
        [Switch Latency] Check the switch latency time when the mouse moves to the right or left on X axis
        in Deep Sleep mode
        """
        self.measure_and_validate_x_motion_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_LS2_0012")
    # end def test_x_motion_in_deep_sleep_mode
# end class LatencyPerformanceLS2TestCase


@services.class_decorator('USBAnalyser')
@features.class_decorator('LSXLatencyTestsWithUsbAnalyser')
class LatencyPerformanceLS2TestCaseMixin(LatencyTestCase):
    """
    Test case for latency measurement through the LS2 communication protocol with Beagle 480 USB analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._1_KHz

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()


        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # ----------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # Use beagle analyser to trig on HID report
        self.use_beagle_analyser = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Set report rate")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.set_report_rate(
            self,
            connection_type=ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
            report_rate=self.REPORT_RATE)

    # end def setUp

    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_default_switch_in_active_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Active mode

        NB: Mice hybrid switches are not tested on this test
        """
        self.measure_and_validate_make_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_LS2_0001#1")
    # end def test_measure_make_latency_default_switch_in_active_mode

    @features('Unifying')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_make_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Press in low latency mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
        self.measure_and_validate_make_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_LS2_0001#2")
    # end def test_measure_make_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode

    @features('Unifying')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_make_latency_with_hybrid_switch_in_power_save_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Press in power save mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
        self.measure_and_validate_make_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_LS2_0001#3")
    # end def test_measure_make_latency_with_hybrid_switch_in_power_save_mode_in_active_mode

    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_default_switch_in_active_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Active mode

        NB: Mice hybrid switches are not tested on this test
        """
        self.measure_and_validate_break_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_LS2_0002#1")
    # end def test_measure_break_latency_default_switch_in_active_mode

    @features('Unifying')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_break_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Release in low latency mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
        self.measure_and_validate_break_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_LS2_0002#2")
    # end def test_measure_break_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode

    @features('Unifying')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_break_latency_with_hybrid_switch_in_power_save_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Release in power save mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
        self.measure_and_validate_break_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_LS2_0002#3")
    # end def test_measure_break_latency_with_hybrid_switch_in_power_save_mode_in_active_mode

    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_run_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Run mode
        """
        self.measure_and_validate_make_latency_in_run_mode()
        self.testCaseChecked("PER_LATY_LS2_0003")
    # end def test_measure_make_latency_in_run_mode

    @features('Unifying')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_run_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Run mode
        """
        self.measure_and_validate_break_latency_in_run_mode()
        self.testCaseChecked("PER_LATY_LS2_0004")
    # end def test_measure_break_latency_in_run_mode

    @features('Mice')
    @features('Unifying')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='X')
        self.testCaseChecked("PER_LATY_LS2_0009")
    # end def test_x_motion_in_run_mode

    @features('Mice')
    @features('Unifying')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_y_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='Y')
        self.testCaseChecked("PER_LATY_LS2_0010")
    # end def test_y_motion_in_run_mode
# end class LatencyPerformanceLS2TestCaseMixin


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
                          ExtendedAdjustableReportRate.RATE._1_KHz, inheritance=LatencyPerformanceLS2TestCaseMixin)
class LatencyPerformance1kHzLS2TestCase(LatencyPerformanceLS2TestCaseMixin):
    """
    Test case for latency measurement through the LS2 communication protocol at 1 kHz with Beagle 480 USB Analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._1_KHz
# end class LatencyPerformance1kHzLS2TestCase


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
                          ExtendedAdjustableReportRate.RATE._2_KHz, inheritance=LatencyPerformanceLS2TestCaseMixin)
class LatencyPerformance2kHzLS2TestCase(LatencyPerformanceLS2TestCaseMixin):
    """
    Test case for latency measurement through the LS2 communication protocol at 2 kHz with Beagle 480 USB Analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._2_KHz
# end class LatencyPerformance2kHzLS2TestCase


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
                          ExtendedAdjustableReportRate.RATE._4_KHz, inheritance=LatencyPerformanceLS2TestCaseMixin)
class LatencyPerformance4kHzLS2TestCase(LatencyPerformanceLS2TestCaseMixin):
    """
    Test case for latency measurement through the LS2 communication protocol at 4 kHz with Beagle 480 USB Analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._4_KHz
# end class LatencyPerformance4kHzLS2TestCase


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.GAMING_WIRELESS,
                          ExtendedAdjustableReportRate.RATE._8_KHz, inheritance=LatencyPerformanceLS2TestCaseMixin)
class LatencyPerformance8kHzLS2TestCase(LatencyPerformanceLS2TestCaseMixin):
    """
    Test case for latency measurement through the LS2 communication protocol at 8 kHz with Beagle 480 USB Analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._8_KHz
# end class LatencyPerformance8kHzLS2TestCase


class LatencyPerformanceBLEProTestCase(LatencyTestCase):
    """
    Test case for latency measurement through the BLE Pro communication protocol
    """

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_active_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Active mode
        """
        self.measure_and_validate_make_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_BPRO_0001")
    # end def test_measure_make_latency_in_active_mode

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_active_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Active mode
        """
        self.measure_and_validate_break_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_BPRO_0002")
    # end def test_measure_break_latency_in_active_mode

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_run_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Run mode
        """
        self.measure_and_validate_make_latency_in_run_mode()
        self.testCaseChecked("PER_LATY_BPRO_0003")
    # end def test_measure_make_latency_in_run_mode

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_run_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Run mode
        """
        self.measure_and_validate_break_latency_in_run_mode()
        self.testCaseChecked("PER_LATY_BPRO_0004")
    # end def test_measure_break_latency_in_run_mode

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Sleep mode
        """
        self.measure_and_validate_make_latency_in_sleep_mode()
        self.testCaseChecked("PER_LATY_BPRO_0005")
    # end def test_measure_make_latency_in_sleep_mode

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Break) in Sleep mode
        """
        self.measure_and_validate_break_latency_in_sleep_mode()
        self.testCaseChecked("PER_LATY_BPRO_0006")
    # end def test_measure_break_latency_in_sleep_mode

    @features("BLEProProtocol")
    @features('SwitchLatency')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_deep_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Deep Sleep mode
        """
        self.measure_and_validate_make_latency_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_BPRO_0007")
    # end def test_measure_make_latency_in_deep_sleep_mode

    @features('Mice')
    @features("BLEProProtocol")
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='X')
        self.testCaseChecked("PER_LATY_BPRO_0008")
    # end def test_x_motion_in_run_mode

    @features('Mice')
    @features("BLEProProtocol")
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_y_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency time when the mouse moves up or down on Y axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='Y')
        self.testCaseChecked("PER_LATY_BPRO_0009")
    # end def test_y_motion_in_run_mode

    @features('Mice')
    @features("BLEProProtocol")
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_sleep_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Sleep mode
        """
        self.measure_and_validate_x_motion_in_sleep_mode()
        self.testCaseChecked("PER_LATY_BPRO_0010")
    # end def test_x_motion_in_sleep_mode

    @features('Mice')
    @features("BLEProProtocol")
    @features('MotionLatency')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_deep_sleep_mode(self):
        """
        [Switch Latency] Check the switch latency time when the mouse moves to the right or left on X axis
        in Deep Sleep mode
        """
        self.measure_and_validate_x_motion_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_BPRO_0011")
    # end def test_x_motion_in_deep_sleep_mode
# end class LatencyPerformanceBLEProTestCase


class LatencyPerformanceBLETestCase(GattHIDSApplicationTestCases, LatencyTestCase):
    """
    Test case for latency measurement through BLE Direct connection
    """

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        if self.f.PRODUCT.F_IsGaming:
            if self.f.PRODUCT.F_IsMice:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.MOUSE_16BITS_INPUT)
            else:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.GAMING_KEYBOARD_INPUT)
            # end if
        else:
            if self.f.PRODUCT.F_IsMice:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.MOUSE_INPUT)
            else:
                self.notification_queue = self.prerequisite_report_input_test(ReportReferences.KEYBOARD_INPUT)
            # end if
        # end if
    # end def setUp

    def prerequisite_report_input_test(self, report_reference):
        """
        Prerequisite for an input report test.
        Get the whole gatt table
        Subscribe to all reports
        get the report notification queue from the report reference

        :param report_reference: The report reference
        :type report_reference: ``HexList``
        :return: the notification queue
        :rtype: ``queue``
        """
        self._prerequisite_gatt_table()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Get the notification queue for report {report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        characteristic = BleProtocolTestUtils.get_hid_report(
            self, self.gatt_table, self.current_ble_device, report_reference)
        self.assertNotNone(characteristic, msg="Report not present")

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f"Get the notification queue for report {report_reference}")
        # --------------------------------------------------------------------------------------------------------------
        notification_queue = BleProtocolTestUtils.direct_subscribe_notification(self, self.current_ble_device,
                                                                                characteristic)
        self.assertNotNone(notification_queue, msg="Report not present")
        return notification_queue
    # end def prerequisite_report_input_test

    @features('BLEProtocol')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_active_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Active mode
        """
        self.measure_and_validate_make_latency_in_active_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0001")
    # end def test_measure_make_latency_in_active_mode

    @features('BLEProtocol')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_active_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Active mode
        """
        self.measure_and_validate_break_latency_in_active_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0002")
    # end def test_measure_break_latency_in_active_mode

    @features('BLEProtocol')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_run_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Run mode
        """
        self.measure_and_validate_make_latency_in_run_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0003")
    # end def test_measure_make_latency_in_run_mode

    @features('BLEProtocol')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_run_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Run mode
        """
        self.measure_and_validate_break_latency_in_run_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0004")
    # end def test_measure_break_latency_in_run_mode

    @features('BLEProtocol')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Sleep mode
        """
        self.measure_and_validate_make_latency_in_sleep_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0005")
    # end def test_measure_make_latency_in_sleep_mode

    @features('BLEProtocol')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Break) in Sleep mode
        """
        self.measure_and_validate_break_latency_in_sleep_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0006")
    # end def test_measure_break_latency_in_sleep_mode

    @features('BLEProtocol')
    @features('SwitchLatency')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_in_deep_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Deep Sleep mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self,
                           msg="Power off all generic usb ports to make sure no interferences from LS2 receiver.")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(test_case=self)
        self.post_requisite_turn_on_all_generic_usb_ports = True

        self.measure_and_validate_make_latency_in_deep_sleep_mode(ble_notification_queue=self.notification_queue)
        self.testCaseChecked("PER_LATY_BLE_0007")
    # end def test_measure_make_latency_in_deep_sleep_mode

    @features('Mice')
    @features('BLEProtocol')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    @skip('Under development')
    def test_x_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='X')
        self.testCaseChecked("PER_LATY_BLE_0008")
    # end def test_x_motion_in_run_mode

    @features('Mice')
    @features('BLEProtocol')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    @skip('Under development')
    def test_y_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency time when the mouse moves up or down on Y axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='Y')
        self.testCaseChecked("PER_LATY_BLE_0009")
    # end def test_y_motion_in_run_mode

    @features('Mice')
    @features('BLEProtocol')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    @skip('Under development')
    def test_x_motion_in_sleep_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Sleep mode
        """
        self.measure_and_validate_x_motion_in_sleep_mode()
        self.testCaseChecked("PER_LATY_BLE_0010")
    # end def test_x_motion_in_sleep_mode

    @features('Mice')
    @features('BLEProtocol')
    @features('MotionLatency')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('OpticalSensor')
    @skip('Under development')
    def test_x_motion_in_deep_sleep_mode(self):
        """
        [Switch Latency] Check the switch latency time when the mouse moves to the right or left on X axis
        in Deep Sleep mode
        """
        self.measure_and_validate_x_motion_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_BLE_0011")
    # end def test_x_motion_in_deep_sleep_mode
# end class LatencyPerformanceBLETestCase


class LatencyPerformanceCrushTestCase(LatencyTestCase):
    """
    Test case for latency measurement through Crush receiver
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.LS2_CA_CRC24_FOR_CRUSH

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_make_latency_in_active_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Active mode
        """
        self.measure_and_validate_make_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0001")
    # end def test_measure_make_latency_in_active_mode

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_break_latency_in_active_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Active mode
        """
        self.measure_and_validate_break_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0002")
    # end def test_measure_break_latency_in_active_mode

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_make_latency_in_run_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Run mode
        """
        self.measure_and_validate_make_latency_in_run_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0003")
    # end def test_measure_make_latency_in_run_mode

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_break_latency_in_run_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Run mode
        """
        self.measure_and_validate_break_latency_in_run_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0004")
    # end def test_measure_break_latency_in_run_mode

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_make_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Sleep mode
        """
        self.measure_and_validate_make_latency_in_sleep_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0005")
    # end def test_measure_make_latency_in_sleep_mode

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_break_latency_in_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Break) in Sleep mode
        """
        self.measure_and_validate_break_latency_in_sleep_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0006")
    # end def test_measure_break_latency_in_sleep_mode

    @features('SwitchLatency')
    @features('Feature1817CrushSlotSupported')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('Crush')
    @services('ButtonPressed')
    def test_measure_make_latency_in_deep_sleep_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Deep Sleep mode
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=self,
                           msg="Power off all generic usb ports except crush receiver port to make sure no "
                               "interferences from LS2 receiver.")
        # --------------------------------------------------------------------------------------------------------------
        DeviceBaseTestUtils.UsbHubHelper.turn_off_all_generic_usb_ports(
            test_case=self, ports_to_turn_on=(PortConfiguration.CRUSH_RECEIVER_PORT,))
        self.post_requisite_turn_on_all_generic_usb_ports = True

        self.measure_and_validate_make_latency_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0007")
    # end def test_measure_make_latency_in_deep_sleep_mode

    @features('Mice')
    @features('MotionLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('OpticalSensor')
    @skip('Under development')
    def test_x_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='X')
        self.testCaseChecked("PER_LATY_CRUSH_0008")
    # end def test_x_motion_in_run_mode

    @features('Mice')
    @features('MotionLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('OpticalSensor')
    @skip('Under development')
    def test_y_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency time when the mouse moves up or down on Y axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='Y')
        self.testCaseChecked("PER_LATY_CRUSH_0009")
    # end def test_y_motion_in_run_mode

    @features('Mice')
    @features('MotionLatency')
    @features('Feature1817CrushSlotSupported')
    @level('Performance')
    @services('Crush')
    @services('OpticalSensor')
    @skip('Under development')
    def test_x_motion_in_sleep_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Sleep mode
        """
        self.measure_and_validate_x_motion_in_sleep_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0010")
    # end def test_x_motion_in_sleep_mode

    @features('Mice')
    @features('MotionLatency')
    @features('Feature1817CrushSlotSupported')
    @features('Feature1830powerMode', 3)
    @level('Performance')
    @services('Crush')
    @services('OpticalSensor')
    @skip('Under development')
    def test_x_motion_in_deep_sleep_mode(self):
        """
        [Switch Latency] Check the switch latency time when the mouse moves to the right or left on X axis
        in Deep Sleep mode
        """
        self.measure_and_validate_x_motion_in_deep_sleep_mode()
        self.testCaseChecked("PER_LATY_CRUSH_0011")
    # end def test_x_motion_in_deep_sleep_mode
# end class LatencyPerformanceCrushTestCase


@services.class_decorator('USBAnalyser')
@features.class_decorator('USBLatencyTestsWithUsbAnalyser')
class LatencyPerformanceUSBTestCaseMixin(LatencyTestCase):
    """
    Test case for latency measurement through USB with Beagle 480 USB Analyser
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._1_KHz

    def setUp(self):
        """
        Handle test prerequisites.
        """
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # Use beagle analyser to trig on HID report
        self.use_beagle_analyser = True

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Set report rate")
        # --------------------------------------------------------------------------------------------------------------
        ExtendedAdjustableReportRateTestUtils.set_report_rate(
            self,
            connection_type=ExtendedAdjustableReportRate.ConnectionType.WIRED,
            report_rate=self.REPORT_RATE)
    # end def setUp

    @features('USB')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_make_latency_default_switch_in_active_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Active mode

        NB: Mice hybrid switches are not tested on this test
        """
        self.measure_and_validate_make_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_USB_0001#1")
    # end def test_measure_make_latency_default_switch_in_active_mode

    @features('USB')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_make_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Press in low latency mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
        self.measure_and_validate_make_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_USB_0001#2")
    # end def test_measure_make_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode

    @features('USB')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_make_latency_with_hybrid_switch_in_power_save_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Press in power save mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
        self.measure_and_validate_make_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_USB_0001#3")
    # end def test_measure_make_latency_with_hybrid_switch_in_power_save_mode_in_active_mode

    @features('USB')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    def test_measure_break_latency_in_active_mode(self):
        """
        Check the switch latency time on Release (100% Break) in Active mode

        NB: Mice hybrid switches are not tested on this test
        """
        self.measure_and_validate_break_latency_in_active_mode()
        self.testCaseChecked("PER_LATY_USB_0002#1")
    # end def test_measure_break_latency_in_active_mode

    @features('USB')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_break_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Release in low latency mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
        self.measure_and_validate_break_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_USB_0002#2")
    # end def test_measure_break_latency_with_hybrid_switch_in_low_latency_mode_in_active_mode

    @features('USB')
    @features('SwitchLatency')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
    @level('Performance')
    @services('HybridSwitchPressed')
    def test_measure_break_latency_with_hybrid_switch_in_power_save_mode_in_active_mode(self):
        """
        Check the hybrid switch latency time on Release in power save mode in Active mode
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.POWER_SAVE_MODE)
        self.measure_and_validate_break_latency_in_active_mode(check_hybrid_switch=True)
        self.testCaseChecked("PER_LATY_USB_0002#3")
    # end def test_measure_break_latency_with_hybrid_switch_in_power_save_mode_in_active_mode

    @features('GamingDevice')
    @features('Mice')
    @features('USB')
    @features('SwitchLatency')
    @level('Performance')
    @services('ButtonPressed')
    @services('OpticalSensor')
    def test_measure_make_latency_in_lift_mode(self):
        """
        Check the switch latency time on Press (100% Make) in Lift mode
        """
        self.measure_and_validate_make_latency_in_lift_mode()
        self.testCaseChecked("PER_LATY_USB_0003")
    # end def test_measure_make_latency_in_lift_mode

    @features('Mice')
    @features('USB')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_x_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='X')
        self.testCaseChecked("PER_LATY_USB_0004")
    # end def test_x_motion_in_run_mode

    @features('Mice')
    @features('USB')
    @features('MotionLatency')
    @level('Performance')
    @services('OpticalSensor')
    def test_y_motion_in_run_mode(self):
        """
        [Switch Latency] Check the motion latency when the mouse moves to the right or left on X axis in Run mode
        """
        self.measure_and_validate_xy_motion_in_run_mode(direction='Y')
        self.testCaseChecked("PER_LATY_USB_0005")
    # end def test_y_motion_in_run_mode
# end class LatencyPerformanceUSBTestCaseMixin


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.WIRED,
                          ExtendedAdjustableReportRate.RATE._1_KHz, inheritance=LatencyPerformanceUSBTestCaseMixin)
class LatencyPerformance1kHzUSBTestCase(LatencyPerformanceUSBTestCaseMixin):
    """
    Test case for latency measurement through USB at 1 kHz with Beagle 480 USB Analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._1_KHz
# end class LatencyPerformance1kHzUSBTestCase


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.WIRED,
                          ExtendedAdjustableReportRate.RATE._2_KHz, inheritance=LatencyPerformanceUSBTestCaseMixin)
class LatencyPerformance2kHzUSBTestCase(LatencyPerformanceUSBTestCaseMixin):
    """
    Test case for latency measurement through USB at 2 kHz with Beagle 480 USB Analyser
    """
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._2_KHz
# end class LatencyPerformance2kHzUSBTestCase


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.WIRED,
                          ExtendedAdjustableReportRate.RATE._4_KHz, inheritance=LatencyPerformanceUSBTestCaseMixin)
class LatencyPerformance4kHzUSBTestCase(LatencyPerformanceUSBTestCaseMixin):
    """
    Test case for latency measurement through USB at 4 kHz with Beagle 480 USB Analyser
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._4_KHz
# end class LatencyPerformance4kHzUSBTestCase


@features.class_decorator('Feature8061SupportedReportRate', ExtendedAdjustableReportRate.ConnectionType.WIRED,
                          ExtendedAdjustableReportRate.RATE._8_KHz, inheritance=LatencyPerformanceUSBTestCaseMixin)
class LatencyPerformance8kHzUSBTestCase(LatencyPerformanceUSBTestCaseMixin):
    """
    Test case for latency measurement through USB at 8 kHz with Beagle 480 USB Analyser
    """
    PROTOCOL_TO_CHANGE_TO = LogitechProtocol.USB
    REPORT_RATE = ExtendedAdjustableReportRate.RATE._8_KHz
# end class LatencyPerformance8kHzUSBTestCase
# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
