#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.device.hid.mouse.hybridbutton.functionality
:brief: Hid mouse hybrid button functionality test suite
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2024/02/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.modestatus import ModeStatus
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse.hybridbutton.hybridbutton import HybridButtonTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
Event = HidReportTestUtils.Event
EventId = HidReportTestUtils.EventId
KEY_ID_EVENT_MAP = HidReportTestUtils.KEY_ID_EVENT_MAP
BUTTON_MAIN_LOOP_DURATION = 1 / 1000  # in second
BUTTON_MAIN_LOOP_DURATION_MARGIN = BUTTON_MAIN_LOOP_DURATION * 0.1  # in second


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class HybridButtonFunctionalityTestCase(HybridButtonTestCase):
    """
    Validate Mouse hybrid button functionality TestCases
    """
    @features('Mice')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Functionality')
    @services('HybridSwitchPressed')
    def test_optical_switch_in_low_latency_mode(self):
        """
        Validate that, in low latency mode, Make and Break can be generated only via the emulation of the optical part
        """
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all hybrid buttons")
        # --------------------------------------------------------------------------------------------------------------
        for key_id in self.button_stimuli_emulator.get_hybrid_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press on the {str(key_id)} button with only the optical emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_press(key_id=key_id, galvanic_emulation=False,
                                                          optical_emulation=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check a single HID Mouse report with one bit set sent by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self,
                                                         events=[Event(KEY_ID_EVENT_MAP[key_id], value=1)])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {str(key_id)} button with only the optical emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_release(key_id=key_id, galvanic_emulation=False,
                                                            optical_emulation=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check a single HID Mouse report with the bit reset sent by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(KEY_ID_EVENT_MAP[key_id])])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_HID_MSE_HYB_BUT_0001")
    # end def test_optical_switch_in_low_latency_mode

    @features('Mice')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Functionality')
    @services('HybridSwitchPressed')
    def test_galvanic_switch_in_low_latency_mode(self):
        """
        Validate that, in low latency mode, Make and Break can't be generated only via the emulation of the galvanic
        part.
        """
        self.post_requisite_reload_nvs = True
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all hybrid buttons")
        # --------------------------------------------------------------------------------------------------------------
        for key_id in self.button_stimuli_emulator.get_hybrid_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press on the {str(key_id)} button with only the galvanic emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_press(key_id=key_id, galvanic_emulation=True,
                                                          optical_emulation=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Check no HID report is received')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press on the {str(key_id)} button with galvanic and optical emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_press(key_id=key_id, galvanic_emulation=True,
                                                          optical_emulation=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check a single HID Mouse report with one bit set sent by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self,
                                                         events=[Event(KEY_ID_EVENT_MAP[key_id], value=1)])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {str(key_id)} button only on the galvanic switch")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_release(key_id=key_id, galvanic_emulation=True,
                                                            optical_emulation=False)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Check no HID report is received')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {str(key_id)} button with galvanic and optical emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_release(key_id=key_id, galvanic_emulation=True,
                                                            optical_emulation=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check a single HID Mouse report with the bit reset sent by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(KEY_ID_EVENT_MAP[key_id])])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_HID_MSE_HYB_BUT_0002")
    # end def test_galvanic_switch_in_low_latency_mode

    @features('Mice')
    @features('Feature8090HybridSwitchMode', ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)
    @level('Functionality')
    @services('HybridSwitchPressed')
    def test_release_timing_in_low_latency_mode(self):
        """
        Validate that, in low latency mode, a Break can be generated only if the optical part is release during at
        least 2 main loops
        """
        self.post_requisite_reload_nvs = True
        self.set_mode_status_power_mode(power_mode=ModeStatus.ModeStatus1.PowerMode.LOW_LATENCY_MODE)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "Test Loop over all hybrid buttons")
        # --------------------------------------------------------------------------------------------------------------
        for key_id in self.button_stimuli_emulator.get_hybrid_key_id_list():
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Press on the {str(key_id)} with galvanic and optical emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_press(key_id=key_id, galvanic_emulation=True,
                                                          optical_emulation=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check a single HID Mouse report with one bit set sent by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self,
                                                         events=[Event(KEY_ID_EVENT_MAP[key_id], value=1)])

            release_duration = BUTTON_MAIN_LOOP_DURATION + BUTTON_MAIN_LOOP_DURATION_MARGIN
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {str(key_id)} button during {release_duration}s")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.button_stimuli_emulator.hybrid_key_release(key_id=key_id, galvanic_emulation=True,
                                                            optical_emulation=True)
            self.kosmos.pes.delay(delay_s=BUTTON_MAIN_LOOP_DURATION)
            self.button_stimuli_emulator.hybrid_key_press(key_id=key_id, galvanic_emulation=True,
                                                          optical_emulation=True)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_info(self, 'Check no HID report is received')
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID,
                                           timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT)

            release_duration = 2 * BUTTON_MAIN_LOOP_DURATION + BUTTON_MAIN_LOOP_DURATION_MARGIN
            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {str(key_id)} button during {release_duration}s")
            # ----------------------------------------------------------------------------------------------------------
            self.kosmos.sequencer.offline_mode = True
            self.button_stimuli_emulator.hybrid_key_release(key_id=key_id, galvanic_emulation=True,
                                                            optical_emulation=True)
            self.kosmos.pes.delay(delay_s=release_duration)
            self.button_stimuli_emulator.hybrid_key_press(key_id=key_id, galvanic_emulation=True,
                                                          optical_emulation=True)
            self.kosmos.sequencer.offline_mode = False
            self.kosmos.sequencer.play_sequence()

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check two HID Mouse reports received: bit reset in the first one then bit "
                                      "set in the second")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(KEY_ID_EVENT_MAP[key_id])])
            HidReportTestUtils.check_hid_report_by_event(test_case=self,
                                                         events=[Event(KEY_ID_EVENT_MAP[key_id], value=1)])

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f"Release the {str(key_id)} button with galvanic and optical emulation")
            # ----------------------------------------------------------------------------------------------------------
            self.button_stimuli_emulator.hybrid_key_release(key_id=key_id, galvanic_emulation=True,
                                                            optical_emulation=True)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check a single HID Mouse report with the bit reset sent by the DUT")
            # ----------------------------------------------------------------------------------------------------------
            HidReportTestUtils.check_hid_report_by_event(test_case=self, events=[Event(KEY_ID_EVENT_MAP[key_id])])
        # end for
        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(self, "End Test Loop")
        # --------------------------------------------------------------------------------------------------------------

        self.testCaseChecked("BUS_HID_MSE_HYB_BUT_0003")
    # end def test_release_timing_in_low_latency_mode
# end class HybridButtonFunctionalityTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
