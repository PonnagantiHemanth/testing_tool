#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.shared.hid.mouse.smoothingalgo.smoothingalgo
:brief: Shared Hid mouse smoothing algo test case
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2024/07/04
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from pychannel.channelinterfaceclasses import LinkEnablerInfo
from pyharness.core import TYPE_ERROR
from pyharness.core import TestException
from pyhid.hid import HidMouseNvidiaExtension
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRate
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ReportRateInfoEvent
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfiles
from pylibrary.tools.hexlist import HexList
from pyraspi.tool.beagle.beagle480 import Beagle480
from pyraspi.tool.beagle.beagle480 import BeagleChannel
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA0
from pyraspi.tool.beagle.beagle_py import BG_USB_PID_DATA1
from pytestbox.base.basetest import BaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.devicetestutils import DeviceTestUtils
from pytestbox.device.base.extendedadjustablereportrateutils import ExtendedAdjustableReportRateTestUtils
from pytestbox.device.base.onboardprofilesutils import OnboardProfilesTestUtils
from pytestbox.device.hid.base.hidreportutils import to_signed_int

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
SMOOTH_THRESHOLD_ENABLE = 3
SMOOTH_THRESHOLD_DISABLE = 2
MINIMUM = 1
SMOOTH_AVG_BUFF_SIZE = 10
SKIP_COUNTER = 1


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class SmoothingAlgoTestCase(BaseTestCase):
    """
    Validate mouse XY displacement requirements
    """

    MAX_12_BITS_SIGNED = (1 << 11) - 1
    MIN_12_BITS_SIGNED = -MAX_12_BITS_SIGNED

    def setUp(self):
        """
        Handle test prerequisites.
        """
        self.beagle480 = None
        self.pressed_key_ids = None
        super().setUp()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup initial NVS")
        # --------------------------------------------------------------------------------------------------------------
        DeviceTestUtils.NvsHelper.backup_nvs(self)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self,
            "Test strategy: to effectively capture a true 8kHz stream, the HID mouse endpoint shall be polled regularly"
            "That's why, to reduce the likelihood of a context switch, callbacks have to be disabled."
            "In the LogiUSB C library, the python callback on HID mouse / kdb & dgt reports reception are disabled by"
            " adding the LinkEnablerInfo.DISABLE_xxx_CB_MASK when opening the channel")
        # --------------------------------------------------------------------------------------------------------------
        ChannelUtils.close_channel(test_case=self)
        ChannelUtils.open_channel(
            test_case=self, link_enabler=(LinkEnablerInfo.ALL_MASK + LinkEnablerInfo.DISABLE_MOUSE_CB_MASK +
                                          LinkEnablerInfo.DISABLE_KEYBOARD_CB_MASK +
                                          LinkEnablerInfo.DISABLE_DIGITIZER_CB_MASK))

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Clean WirelessDeviceStatusBroadcastEvent messages")
        # ----------------------------------------------------------------------------------------------------------
        ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                    class_type=WirelessDeviceStatusBroadcastEvent)
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_post_requisite(self, "Clean Battery Status messages")
        # ----------------------------------------------------------------------------------------------------------
        self.cleanup_battery_event_from_queue()
    # end def setUp

    def tearDown(self):
        """
        Handle test post-requisites.
        """
        with self.manage_kosmos_post_requisite():
            if self.pressed_key_ids is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Release all pressed buttons")
                # ------------------------------------------------------------------------------------------------------
                self.button_stimuli_emulator.multiple_keys_release(key_ids=self.pressed_key_ids)
                self.pressed_key_ids = None
            # end if
        # end with
        with self.manage_post_requisite():
            if self.beagle480 is not None:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Close beagle device")
                # ------------------------------------------------------------------------------------------------------
                self.beagle480.close()
            # end if
        # end with
        with self.manage_post_requisite():
            if self.post_requisite_reload_nvs:
                # post_requisite_reload_nvs flag need not be set to True,
                # if the set_report_Rate is performed in host_mode and switched back to onboard_mode
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Reload initial NVS")
                # ------------------------------------------------------------------------------------------------------
                DeviceTestUtils.NvsHelper.restore_nvs(self)
                self.post_requisite_reload_nvs = False

                ChannelUtils.get_only(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, check_first_message=False,
                    class_type=WirelessDeviceStatusBroadcastEvent, allow_no_message=True)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, "Clean Battery Status messages")
                # ------------------------------------------------------------------------------------------------------
                self.cleanup_battery_event_from_queue()

                ChannelUtils.clean_messages(
                    test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                    class_type=(WirelessDeviceStatusBroadcastEvent, ReportRateInfoEvent))
            # end if
        # end with

        super().tearDown()
    # end def tearDown

    def clip(self, motion):
        """
        Apply limitation on the resolution of the given X/Y motion value, depending on whether the DUT is Gaming or not.

        Rationale:
         - If the DUT is from the Gaming category, then return the given motion as-is.
           The X/Y motion resolution of Gaming Products is typically 16 bits.
         - If the DUT is NOT from the Gaming category (i.e. PWS), then apply limitation of resolution.
           The X/Y motion resolution of PWS Products is typically 12 bits.

        :param motion: X or Y motion value
        :type motion: ``int``

        :return: motion value, clipped if DUT is not a Gaming Product, raw otherwise.
        :rtype: ``int``
        """
        if self.f.PRODUCT.F_IsGaming:
            return motion
        else:
            return self.MIN_12_BITS_SIGNED if motion < self.MIN_12_BITS_SIGNED \
                else self.MAX_12_BITS_SIGNED if motion > self.MAX_12_BITS_SIGNED \
                else motion
        # end if
    # end def clip

    def force_report_rate(self, report_rate):
        """
        Force the reporting rate to the given value using the 0x8061 HID++ feature API

        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``

        :raise ``TestException``: If the report Rate could not be configured at 8kHz
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Get feature 0x8061 index")
        # --------------------------------------------------------------------------------------------------------------
        _, self.feature_8061, _, _ = ExtendedAdjustableReportRateTestUtils.HIDppHelper.get_parameters(self)

        # Add a loop to ensure that the DUT has successfully transitioned to the new report rate.
        # We noticed that occasionally, our Bazooka2 sample was resetting and reverting to the default value.
        # Loop counter = 4 is an empirical value based on experience
        loop_counter = 4
        for index in range(loop_counter):
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Send SetReportRate request with report rate = {report_rate}")
            # ----------------------------------------------------------------------------------------------------------
            ExtendedAdjustableReportRateTestUtils.HIDppHelper.set_report_rate(test_case=self, report_rate=report_rate)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, "Wait ReportRateInfoEvent response")
            # ----------------------------------------------------------------------------------------------------------
            response = ExtendedAdjustableReportRateTestUtils.HIDppHelper.report_rate_info_event(
                test_case=self, check_first_message=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check ReportRateInfoEvent response inputs fields are as expected")
            # ----------------------------------------------------------------------------------------------------------
            checker = ExtendedAdjustableReportRateTestUtils.ReportRateInfoEventChecker
            check_map = checker.get_default_check_map(test_case=self)
            check_map.update({
                "report_rate": (checker.check_report_rate, report_rate)
            })
            checker.check_fields(self, response, self.feature_8061.report_rate_info_event_cls, check_map)

            # The DUT could reset after receiving the previous SetReportRate request
            message = ChannelUtils.get_only(
                test_case=self, queue_name=HIDDispatcher.QueueName.EVENT, timeout=3,
                class_type=WirelessDeviceStatusBroadcastEvent, check_first_message=False, allow_no_message=True)
            if message is None:
                break
            elif index == (loop_counter - 1):
                raise TestException(TYPE_ERROR, f'Report Rate could not be configured at {report_rate}')
            else:
                # --------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f"Send SetOnboardMode request with onboardMode = host mode")
                # --------------------------------------------------------------------------------------------------
                OnboardProfilesTestUtils.HIDppHelper.set_onboard_mode(
                    test_case=self, onboard_mode=OnboardProfiles.Mode.HOST_MODE)

                ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                            class_type=(WirelessDeviceStatusBroadcastEvent,
                                                        self.feature_8061.report_rate_info_event_cls))
            # end if
        # end for
    # end def force_report_rate

    def force_report_rate_and_start_usb_capture(
            self, report_rate=ExtendedAdjustableReportRate.ReportRateList.POS.RATE_8KHZ):
        """
        Configure the reporting rate to 8kHz, pause the LogiUSB polling tasks and start the USB capture

        :param report_rate: Report Rate - OPTIONAL
        :type report_rate: ``int`` or ``HexList``
        """
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Change the report rate to {report_rate}")
        # --------------------------------------------------------------------------------------------------------------
        self.post_requisite_reload_nvs = True
        ExtendedAdjustableReportRateTestUtils.force_report_rate(test_case=self, report_rate=report_rate)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Pause the polling tasks processing the received reports")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.mute()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f"Start the USB capture using the Beagle 480 USB analyzer")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480 = Beagle480(test_case=self, channel_type=BeagleChannel.WIRELESS)
        self.beagle480.start_capture(immediate=False)
    # end def force_report_rate_and_start_usb_capture

    def _get_usb_packets(self):
        """
        Get the USB packets received from the Beagle USB analyser

        :return: The packets received from the USB capture device.
        :rtype: ``list[TimestampedBitFieldContainerMixin]``

        :raise ``AssertionError``: If the number of USB packets received from the Beagle USB analyser is too low
        """
        # Add a 5s delay to let the Beagle process all the HID reports
        sleep(5)

        self.beagle480.print_buffer_usage()

        self.beagle480.parse()
        self.beagle480.close()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Resume the polling tasks processing the received reports")
        # --------------------------------------------------------------------------------------------------------------
        self.current_channel.unmute()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, "Filter USB packets to keep HID Mouse report only")
        # --------------------------------------------------------------------------------------------------------------
        self.beagle480.filter(pid_filtering_list=[BG_USB_PID_DATA0, BG_USB_PID_DATA1],
                              report_filtering_list=[HidMouseNvidiaExtension])
        packets = self.beagle480.get_filtered_packets()

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check the number of USB packets received from the Beagle USB analyser')
        # --------------------------------------------------------------------------------------------------------------
        self.assertGreater(
            a=len(packets), b=SMOOTH_AVG_BUFF_SIZE * 2,
            msg=f"No enough packet (i.e. {len(packets)}) received from the Beagle USB analyser")
        return packets
    # end def _get_usb_packets

    def _process_packets(self, packets):
        """
        Compute the delta time between two consecutive HID reports, the total displacement accumulation
        and the number of reports that were split by the receiver

        :param packets: The packets received from the USB capture device.
        :type packets: ``list[TimestampedBitFieldContainerMixin]``

        :return: tuple with delta time between report, accumulation value on x, accumulation value on y and split count
        :rtype: ``tuple[float, int, int, int]``
        """
        beagle_deltas = []
        beagle_accumulated_x = 0
        beagle_accumulated_y = 0
        split_counter = 0

        delta = ''
        beagle_previous_timestamp = None
        for index in range(len(packets)):
            packet = packets[index]
            if beagle_previous_timestamp is not None:
                delta = (packet.timestamp - beagle_previous_timestamp) / 10 ** 3
                beagle_deltas.append(delta)
            # end if
            LogHelper.log_info(self, f'{HexList(packet)} Dx={to_signed_int(packet.x, little_endian=True)}, '
                                     f'Dy={to_signed_int(packet.y, little_endian=True)},Dt= {delta}')
            print(f'{HexList(packet)} Dx={to_signed_int(packet.x, little_endian=True)}, '
                  f'Dy={to_signed_int(packet.y, little_endian=True)},Dt= {delta}')
            beagle_previous_timestamp = packet.timestamp
            beagle_accumulated_x += to_signed_int(packet.x, little_endian=True)
            beagle_accumulated_y += to_signed_int(packet.y, little_endian=True)
            if (abs(to_signed_int(packet.x, little_endian=True)) == SMOOTH_THRESHOLD_DISABLE // 2 and
                    abs(to_signed_int(packet.y, little_endian=True)) == SMOOTH_THRESHOLD_DISABLE // 2):
                split_counter += 1
            # end if
        # end for
        return beagle_deltas, beagle_accumulated_x, beagle_accumulated_y, split_counter
    # end def _process_packets
# end class SmoothingAlgoTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
