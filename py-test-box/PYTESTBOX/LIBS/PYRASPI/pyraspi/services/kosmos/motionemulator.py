#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.motionemulator
:brief: Kosmos Motion Emulator Class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2023/03/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum
from enum import auto
from enum import unique
from functools import reduce
from operator import or_
from typing import Type

from pylibrary.emulator.emulatorinterfaces import MotionEmulationInterface
from pylibrary.emulator.emulatorinterfaces import SEQUENCER_TIMEOUT_S
from pyraspi.services.kosmos.config.opticalsensorconfig import DIRECTION
from pyraspi.services.kosmos.config.opticalsensorconfig import MouseLayoutInterface
from pyraspi.services.kosmos.config.opticalsensorconfig import ORIENTATION
from pyraspi.services.kosmos.config.opticalsensorconfig import SENSOR_ORIENTATION_BY_ID
from pyraspi.services.kosmos.kosmos import Kosmos
from pyraspi.services.kosmos.module.devicetree import DeviceFamilyName
from pyraspi.services.kosmos.module.model.optemu.base import OptEmuRegisterMapBase
from pyraspi.services.kosmos.module.optemu import Action
from pyraspi.services.kosmos.module.optemu_interfaces import OptEmuModuleInterface
from pyraspi.services.kosmos.protocol.generated.messages import ADDA_SEL_DAC_1
from pyraspi.services.kosmos.protocol.generated.messages import opt_emu_status_t


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

@unique
class SENSOR_MODE(IntEnum):
    """
    Optical sensor activity mode
    """
    RUN = auto()
    REST1 = auto()
    REST2 = auto()
    REST3 = auto()
# end class SENSOR_MODE


class KosmosMotionEmulator(MotionEmulationInterface):
    """
    XY Motion emulator leveraging Kosmos setup
    """

    module: OptEmuModuleInterface
    VERBOSE: bool = False

    _kosmos: Kosmos
    _sensor_layout: Type[MouseLayoutInterface]

    def __init__(self, kosmos, fw_id):
        """
        :param kosmos: an instance of a Kosmos class
        :type kosmos: ``Kosmos``
        :param fw_id: The FW name
        :type fw_id: ``str``

        :raise ``AssertionError``: Invalid firmware ID or sensor orientation map
        """
        self._kosmos = kosmos
        self.module = self.get_module()

        assert fw_id in SENSOR_ORIENTATION_BY_ID, f'Don\'t support the fw_id : {fw_id}'
        self._sensor_layout = SENSOR_ORIENTATION_BY_ID[fw_id]

        _direction_to_orientation_map = self._sensor_layout.MOTION
        assert (reduce(or_, _direction_to_orientation_map) & ~ORIENTATION.INVERSE) & (ORIENTATION.X | ORIENTATION.Y), \
            f'Invalid direction to orientation map: {_direction_to_orientation_map}\n' \
            f'{str(_direction_to_orientation_map)}'
        assert all(ORIENTATION.X in orientation or ORIENTATION.Y in orientation
                   for orientation in _direction_to_orientation_map.values()), \
            f'Invalid direction to orientation map: {_direction_to_orientation_map}\n' \
            f'{str(_direction_to_orientation_map)}'

        self._action_to_orientation_map = {Action.DX: _direction_to_orientation_map[DIRECTION.X],
                                           Action.DY: _direction_to_orientation_map[DIRECTION.Y]}
        self._orientation_to_action_map = {ORIENTATION.X: Action.DX,
                                           ORIENTATION.Y: Action.DY}

        self._check_pods_configuration()
    # end def __init__

    def get_module(self):
        """
        Return the module instance which provides the motion emulation.

        Note: The current implementation will return the first Optical Sensor Emulator module present in the Kosmos
              DeviceTree.

        Note: ``StopIteration`` will be raised if no Optical Sensor Emulator is present in the Kosmos DeviceTree

        :return: The module instance to be tested.
        :rtype: ``OptEmuModuleInterface``
        """
        return next(devices[0] for device_name, devices in self._kosmos.dt.items()
                    if devices and device_name in DeviceFamilyName.OPTICAL_SENSOR)
    # end def get_module

    def status(self, sanity_checks=True):
        """
        Return the Motion Emulator module status.

        :param sanity_checks: If True, run sanity checks on the status reply and raise an error if something is wrong.
                              If False, skip sanity checks. Defaults to True - OPTIONAL
        :type sanity_checks: ``bool``

        :return: Motion Emulator module status.
        :rtype: ``opt_emu_status_t``
        """
        return self.module.status(sanity_checks=sanity_checks)
    # end def status

    def reset(self):
        """
        Reset the Motion Emulator module: both hardware (FPGA, MCU) and software (Python).
        Return the module status after reset.

        :return: Motion Emulator module status after reset of the module.
        :rtype: ``opt_emu_status_t``
        """
        return self.module.reset_module()
    # end def reset

    def xy_motion(self, dx=None, dy=None, lift=None, repetition=0, skip=0):
        # See ``MotionEmulationInterface.xy_motion``
        assert isinstance(dx, int) or isinstance(dy, int), 'At least one of dx or dy parameter must be an integer.'

        if dx is not None:
            self.set_action(action=Action.DX, value=dx)
        # end if
        if dy is not None:
            self.set_action(action=Action.DY, value=dy)
        # end if
        if lift is not None:
            self.set_action(action=Action.LIFT, value=lift)
        # end if
        if repetition:
            self.set_action(action=Action.REPETITION, value=repetition)
        # end if
        if skip:
            self.set_action(action=Action.SKIP, value=skip)
        # end if
    # end def xy_motion

    def set_sensor_mode(self, mode=SENSOR_MODE.RUN):
        """
        Force the sensor activity mode exposed to the MCU

        :param mode: targeted sensor activity mode, defaults to `SENSOR_MODE.RUN` - OPTIONAL
        :type mode: ``SENSOR_MODE``

        :raise ``ValueError``: If `mode` value is not in `SENSOR_MODE` enum
        """

        if mode == SENSOR_MODE.RUN or mode == SENSOR_MODE.REST1:
            self.set_action(action=Action.POWER_MODE_REST2, value=None)
            self.set_action(action=Action.POWER_MODE_SLEEP, value=None)
        elif mode == SENSOR_MODE.REST2:
            self.set_action(action=Action.POWER_MODE_REST2, value=True)
        elif mode == SENSOR_MODE.REST3:
            self.set_action(action=Action.POWER_MODE_SLEEP, value=True)
        else:
            raise ValueError(mode)
        # end if
    # end def set_sensor_mode

    def set_action(self, action, value):
        """
        Update the Optical Sensor Emulator current state, with the given action and value.

        Notes:
         - Call ``update(action, value)`` method as many times as required.
         - Duplicate actions or value rollbacks have no impact. Only the State difference matters.
         - ``Action.DX`` and ``Action.DY`` actions are processed taking care of sensor orientation translation

        :param action: High-level action for updating the Optical Sensor Emulator State
        :type action: ``Action``
        :param value: High-level action value
        :type value: ``int or bool or None``
        """
        if action in self._action_to_orientation_map.keys():
            action, value = self._translate_dx_dy_actions(action, value)
        # end if

        self.module.hl_ctrl.update(action=action, value=value)
    # end def set_action

    def _translate_dx_dy_actions(self, action, value):
        """
        Translate XY Action, from Mouse to Sensor XY reference frames.

        :param action: High-level action for updating the Optical Sensor Emulator State
        :type action: ``Action``
        :param value: High-level action value
        :type value: ``int or bool or None``

        :return: The translated action and value
        :rtype: ``(Action, int or bool or None)``
        """
        orientation = self._action_to_orientation_map[action]
        translated_action = self._orientation_to_action_map[orientation & ~ORIENTATION.INVERSE]
        translated_value = -value if ORIENTATION.INVERSE in orientation else value
        return translated_action, translated_value
    # end def _translate_dx_dy_actions

    def commit_actions(self):
        """
        Commit the Optical Sensor Emulator current State to the Emulator module's local instructions buffer.
        Initialize next State.
        """
        self.module.hl_ctrl.commit()
    # end def commit_actions

    def prepare_sequence(self, forced_update=False, timeout=SEQUENCER_TIMEOUT_S, update_count=None):
        """
        Prepare the test sequence, and run it if Sequencer is not in `offline_mode`.

        :param forced_update: The first Emulator update will happen without waiting the DUT to poll the sensor,
                              useful to trigger the DUT out of sleep mode, defaults to ``False`` - OPTIONAL
        :type forced_update: ``bool``
        :param timeout: Test sequence timeout, in seconds, defaults to ``SEQUENCER_TIMEOUT_S`` - OPTIONAL
        :type timeout: ``int or float``
        :param update_count: Expected Emulator Model Data update count, unchecked if None or Kosmos Sequencer is in
                             offline mode; defaults to None - OPTIONAL
        :type update_count: ``int or None``

        :return: Emulator Module status if not in offline mode, None otherwise
        :rtype: ``opt_emu_status_t or None``

        :raise ``AssertionError``: unexpected Emulator status at the end of Test Sequence
        """
        self.VERBOSE and print(f'Emulator Module instructions buffer:\n{self.module.instructions_to_str()}\n')

        # Start Sensor Emulator model update
        self._kosmos.dt.pes.execute(action=self.module.action_event.START)

        if forced_update:
            self._kosmos.dt.pes.execute(action=self.module.action_event.UPDATE)
        # end if

        # Wait until Sensor Emulator finishes its sequence
        self._kosmos.dt.pes.wait(action=self.module.resume_event.FIFO_UNDERRUN)

        if not self._kosmos.dt.sequencer.offline_mode:
            # Run test sequence
            self._kosmos.dt.sequencer.play_sequence(timeout=timeout)

            # Validation of Emulator status
            status = self.status()
            expected_update_count = status.update_count if update_count is None else update_count
            expect = opt_emu_status_t(setup_done=True, fifo_underrun=True, update_count=expected_update_count)
            assert expect == status, f'Unexpected Emulator Status at the end of Test Sequence:\n' \
                                     f'EXPECT: {str(expect)}\n' \
                                     f'ACTUAL: {str(status)}'
            return status
        # end if

        return None
    # end def prepare_sequence

    @property
    def limits(self):
        """
        Return the Optical Sensor Emulator's Limits constants.

        :return: Optical Sensor Emulator's Limits constants
        :rtype: ``OptEmuRegisterMapBase.Limits``
        """
        return self.module.ll_ctrl.reg_map.Limits
    # end def property getter limits

    def _check_pods_configuration(self):
        """
        Check that at least one of the DAC1 channels is associated with an optical sensor.

        :raise ``AssertionError``: If no DAC1 channel is associated with an optical sensor.
        """
        # Extract DAC1 channels associated devices
        optical_sensor_channels_ids = []
        for channel_id, channel in self._kosmos.pods_configuration.dacs[ADDA_SEL_DAC_1].channels.items():
            if (channel.associated_device is DeviceFamilyName.OPTICAL_SENSOR or
                    channel.associated_device in DeviceFamilyName.OPTICAL_SENSOR):
                optical_sensor_channels_ids.append(channel_id)
                break
            # end if
        # end for
        assert len(optical_sensor_channels_ids), "No DAC1 channel associated with an optical sensor"
    # end def _check_pods_configuration
# end class KosmosMotionEmulator

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
