#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.tools.kosmos.optemu
:brief: Kosmos Optical Sensor Emulator Validation
:author: Lila Viollette <lviollette@logitech.com>
:date: 2023/07/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from itertools import count

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hid import HidMouse
from pyhid.hid import HidMouseNvidiaExtension
from pyhid.hiddispatcher import HIDDispatcher
from pyraspi.services.kosmos.module.optemu_interfaces import Action
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.hid.base.hidreportutils import HidReportTestUtils
from pytestbox.device.hid.mouse.displacement.xydisplacement import XYDisplacementTestCase
from pytestbox.tools.kosmos.kosmos import KosmosTestCase

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------

ACTION_TO_EVENT_ID_MAP = {Action.DX: HidReportTestUtils.EventId.X_MOTION,
                          Action.DY: HidReportTestUtils.EventId.Y_MOTION}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class KosmosOptEmuTestCase(XYDisplacementTestCase, KosmosTestCase):
    """
    Kosmos Optical Sensor Emulator Unit Test Validation

    Optical Sensor Emulator Specifications:
        https://docs.google.com/document/d/1mmDj4Wp5VD7-k4KqKQk5ufs4mz6sl-f4q5da_OWdcAs


    NOTE: THOSE TESTS ARE NOT DIRECTED BY ANY PRODUCT SPECIFICATIONS.
    """

    def setUp(self):
        """
        Set up the Test class
        """
        super().setUp()

        # Restore Compression Flag to default
        self.motion_emulator.module.ll_ctrl.compress = True
    # end def setUp

    def set_instructions_compression_mode(self, mode):
        """
        Test Case step: Set the Motion Emulator Module' instruction compression mode.
        mode=True enables the compression, mode=False disables it.

        :param mode: Motion Emulator Module' instruction compression mode
        :type mode: ``bool``

        :raise ``AssertionError``: invalid mode type
        """
        assert isinstance(mode, bool), mode
        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, f'Set Emulator Module instruction compression mode to {mode}')
        # ----------------------------------------------------------------------------------------------------------
        self.motion_emulator.module.ll_ctrl.compress = mode
    # end def set_instructions_compression_mode

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_repeat(self):
        """
        Goals: Verify Kosmos Optical Sensor Model Data update:
         - Repeat feature.
        """
        motion_1 = 1
        motion_2 = 2
        repetition = 10
        expected_motion_1 = motion_1 * (1 + repetition)
        expected_motion_2 = motion_2
        expected_update_count = 0
        for instructions_compression_mode in [False, True]:
            self.set_instructions_compression_mode(instructions_compression_mode)

            for delta_reg in [Action.DX, Action.DY]:
                expected_update_count += 1 + repetition
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate motion events with {delta_reg!s} = {motion_1} and '
                                         f'repetition = {repetition}')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.xy_motion(dx=0, dy=0, repetition=repetition)   # Reset both DX and DY
                self.motion_emulator.set_action(action=delta_reg, value=motion_1)   # Set either DX or DY
                self.motion_emulator.commit_actions()
                # Run test sequence
                self.motion_emulator.prepare_sequence(update_count=expected_update_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Mouse reports are received, accumulating "
                                          f"{delta_reg!s} = {expected_motion_1}")
                # ------------------------------------------------------------------------------------------------------
                HidReportTestUtils.check_motion_accumulation(
                    test_case=self, events=[HidReportTestUtils.Event(event_type=ACTION_TO_EVENT_ID_MAP[delta_reg],
                                                                     value=expected_motion_1)])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_title_2(self, 'Validate reinitialisation of Skip/Repeat counters after end of '
                                            'Skip/Repeat operations')
                # ------------------------------------------------------------------------------------------------------
                expected_update_count += 1
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate motion events with {delta_reg!s} = {motion_2}, no repetition and '
                                         f'no skip')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.set_action(action=delta_reg, value=motion_2)   # Set either DX or DY
                self.motion_emulator.commit_actions()
                # Run test sequence
                self.motion_emulator.prepare_sequence(update_count=expected_update_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Mouse reports are received accumulating "
                                          f"{delta_reg!s} = {expected_motion_2}")
                # ------------------------------------------------------------------------------------------------------
                HidReportTestUtils.check_motion_accumulation(
                    test_case=self, events=[HidReportTestUtils.Event(event_type=ACTION_TO_EVENT_ID_MAP[delta_reg],
                                                                     value=expected_motion_2)])
            # end for
        # end for

        self.testCaseChecked("XXX_NO_SPECS_REF")
    # end def test_repeat

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_skip(self):
        """
        Goals: Verify Kosmos Optical Sensor Model Data update:
         - Skip feature.
        """
        motion_1 = 1
        motion_2 = 2
        skip = 4
        expected_motion_1 = motion_1
        expected_motion_2 = motion_2
        expected_update_count = 0
        for instructions_compression_mode in [False, True]:
            self.set_instructions_compression_mode(instructions_compression_mode)

            for delta_reg in [Action.DX, Action.DY]:
                expected_update_count += 1 + skip
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate motion events with {delta_reg!s} = {motion_1} and skip = {skip}')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.xy_motion(dx=0, dy=0, skip=skip)               # Reset both DX and DY
                self.motion_emulator.set_action(action=delta_reg, value=motion_1)   # Set either DX or DY
                self.motion_emulator.commit_actions()
                # Run test sequence
                self.motion_emulator.prepare_sequence(update_count=expected_update_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Mouse reports are received accumulating "
                                          f"{delta_reg!s} = {expected_motion_1}")
                # ------------------------------------------------------------------------------------------------------
                HidReportTestUtils.check_motion_accumulation(
                    test_case=self, events=[HidReportTestUtils.Event(event_type=ACTION_TO_EVENT_ID_MAP[delta_reg],
                                                                     value=expected_motion_1)])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_title_2(self, 'Validate reinitialisation of Skip/Repeat counters after end of '
                                            'Skip/Repeat operations')
                # ------------------------------------------------------------------------------------------------------
                expected_update_count += 1
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate motion events with {delta_reg!s} = {motion_2}, no repetition and '
                                         f'no skip')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.set_action(action=delta_reg, value=motion_2)   # Set either DX or DY
                self.motion_emulator.commit_actions()
                # Run test sequence
                self.motion_emulator.prepare_sequence(update_count=expected_update_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Mouse reports are received accumulating "
                                          f"{delta_reg!s} = {expected_motion_2}")
                # ------------------------------------------------------------------------------------------------------
                HidReportTestUtils.check_motion_accumulation(
                    test_case=self, events=[HidReportTestUtils.Event(event_type=ACTION_TO_EVENT_ID_MAP[delta_reg],
                                                                     value=expected_motion_2)])
            # end for
        # end for

        self.testCaseChecked("XXX_NO_SPECS_REF")
    # end def test_skip

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_skip_repeat(self):
        """
        Goals: Verify Kosmos Optical Sensor Model Data update:
         - Skip & Repeat features together.
        """
        motion = 2
        repetition = 3
        skip = 4
        skip_2 = 5
        expected_motion = motion * (1 + repetition)
        expected_motion_2 = motion
        expected_update_count = 0
        for instructions_compression_mode in [False, True]:
            self.set_instructions_compression_mode(instructions_compression_mode)

            for delta_reg in [Action.DX, Action.DY]:
                expected_update_count += (1 + repetition) * (1 + skip)
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate motion events with {delta_reg!s} = {motion}, '
                                         f'repetition = {repetition} and skip = {skip}')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.xy_motion(dx=0, dy=0, skip=skip, repetition=repetition)    # Reset both DX and DY
                self.motion_emulator.set_action(action=delta_reg, value=motion)                 # Set either DX or DY
                self.motion_emulator.commit_actions()
                # Run test sequence
                self.motion_emulator.prepare_sequence(update_count=expected_update_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Mouse reports are received accumulating "
                                          f"{delta_reg!s} = {expected_motion}")
                # ------------------------------------------------------------------------------------------------------
                HidReportTestUtils.check_motion_accumulation(
                    test_case=self, events=[HidReportTestUtils.Event(event_type=ACTION_TO_EVENT_ID_MAP[delta_reg],
                                                                     value=expected_motion)])

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_title_2(self, 'Validate restoration of Delta X/Y registers values after end of '
                                            'Skip/Repeat operations')
                # ------------------------------------------------------------------------------------------------------
                expected_update_count += skip_2 + 1
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_step(self, f'Emulate motion events with {delta_reg!s} = {motion} (idem, in cache), '
                                         f'no repetition and skip = {skip_2}')
                # ------------------------------------------------------------------------------------------------------
                self.motion_emulator.set_action(action=Action.SKIP, value=skip_2)
                self.motion_emulator.commit_actions()
                # Run test sequence
                self.motion_emulator.prepare_sequence(update_count=expected_update_count)

                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(self, f"Check Mouse reports are received accumulating "
                                          f"{delta_reg!s} = {expected_motion_2}")
                # ------------------------------------------------------------------------------------------------------
                HidReportTestUtils.check_motion_accumulation(
                    test_case=self, events=[HidReportTestUtils.Event(event_type=ACTION_TO_EVENT_ID_MAP[delta_reg],
                                                                     value=expected_motion_2)])
            # end for
        # end for
        self.testCaseChecked("XXX_NO_SPECS_REF")
    # end def test_skip_repeat

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_instructions_raw(self):
        """
        Goals: Verify Kosmos Optical Sensor Model Data Update:
         - multiple Raw instructions per Emulator Model update.
        """
        motion = 0x123
        expected_update_count = 1
        expected_motion = motion

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Emulate motion events with deltaX = deltaY = {motion}')
        # ----------------------------------------------------------------------------------------------------------
        self.motion_emulator.xy_motion(dx=motion, dy=motion)
        self.motion_emulator.commit_actions()
        # Run test sequence
        self.motion_emulator.prepare_sequence(update_count=expected_update_count)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Mouse reports are received accumulating deltaX =  deltaY = {expected_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION,
                                                             value=expected_motion),
                                    HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.Y_MOTION,
                                                             value=expected_motion)])

        self.testCaseChecked("XXX_NO_SPECS_REF")
    # end def test_instructions_raw

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_instructions_raw_cmp(self):
        """
        Goals: Verify Kosmos Optical Sensor Model Data Update:
         - a Raw instruction followed by a Compressed one, constituting one Emulator Model update.
        """
        # Shorthand notations
        module = self.motion_emulator.module
        c = module.ll_ctrl.reg_map.Commands

        motion_raw = 0xFF
        motion_cmp = 2
        expected_update_count = 1
        expected_motion = motion_cmp
        expected_action = Action.DX

        # Handle X/Y frame translation
        raw_action, raw_value = self.motion_emulator._translate_dx_dy_actions(action=expected_action,
                                                                              value=motion_raw)
        if raw_value == -motion_raw:
            # Axis Inversion
            motion_cmp = -motion_cmp
        # end if

        if raw_action == expected_action:
            # No X/Y axis swap
            instr_raw = module.get_raw_instruction(cmd_idx=c.DELTA_X_L, cmd_val=raw_value, send=False)
            instr_cmp = module.get_compressed_instruction(dx=motion_cmp)
        else:
            # X/Y axis swap
            instr_raw = module.get_raw_instruction(cmd_idx=c.DELTA_Y_L, cmd_val=raw_value, send=False)
            instr_cmp = module.get_compressed_instruction(dy=motion_cmp)
        # end if

        # Manually craft Optical Sensor Emulator module buffer
        self.motion_emulator.module.append(instr_raw)
        self.motion_emulator.module.append(instr_cmp)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_step(self, f'Craft an Emulator Model Data Update with two consecutive instructions:\n'
                                 f'{module.instructions_to_str()}')
        # ----------------------------------------------------------------------------------------------------------
        # Run test sequence
        self.motion_emulator.prepare_sequence(update_count=expected_update_count)

        # ----------------------------------------------------------------------------------------------------------
        LogHelper.log_check(self, f"Check Mouse reports are received accumulating deltaX = {expected_motion}")
        # ----------------------------------------------------------------------------------------------------------
        HidReportTestUtils.check_motion_accumulation(
            test_case=self, events=[HidReportTestUtils.Event(event_type=HidReportTestUtils.EventId.X_MOTION,
                                                             value=expected_motion)])

        self.testCaseChecked("XXX_NO_SPECS_REF")
    # end def test_instructions_raw_cmp

    @features('Mice')
    @level('Functionality')
    @services('OpticalSensor')
    def test_instructions_raw_underrun(self):
        """
        Goals: Verify Kosmos Optical Sensor Model Data Update:
         - Early FIFO underrun during an Emulator Model update.

        Rationale:
            Do NOT set the last send flag on purpose: this is expected to trigger an underrun before the Model Data
            update gets committed.
        """
        module = self.motion_emulator.module
        delta_cmds = list(module.ll_ctrl.reg_map.delta_cmds)
        cmd_val = count(start=0x42)

        for i in range(len(delta_cmds)):
            # Manually craft Optical Sensor Emulator module buffer
            # Do NOT set the last send flag on purpose: this is expected to trigger an underrun before the Model Data
            # update gets committed
            instructions = [module.get_raw_instruction(cmd_idx=delta_cmds[j], cmd_val=next(cmd_val), send=False)
                            for j in range(i + 1)]
            module.extend(instructions)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_step(self, f'Run an invalid/uncompleted Emulator Model Data Update with following '
                                     f'instructions:\n{module.instructions_to_str()}')
            # ----------------------------------------------------------------------------------------------------------
            # Run test sequence
            # Expect 0 update count
            self.motion_emulator.prepare_sequence(update_count=0)

            # ----------------------------------------------------------------------------------------------------------
            LogHelper.log_check(self, "Check no Mouse report is received")
            # ----------------------------------------------------------------------------------------------------------
            ChannelUtils.check_queue_empty(test_case=self, queue_name=HIDDispatcher.QueueName.HID, timeout=0.1,
                                           class_type=(HidMouse, HidMouseNvidiaExtension))

            # Empty other queues to prevent raising warnings in test teardown
            ChannelUtils.empty_queues(test_case=self)
        # end for

        self.testCaseChecked("XXX_NO_SPECS_REF")
    # end def test_instructions_raw_underrun
# end class KosmosOptEmuTestCase

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
