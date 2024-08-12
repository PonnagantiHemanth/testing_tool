#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.emulator.emulatorinterfaces
    :brief: Base definition of the interface classes for emulation.
    :author: Stanislas Cottard
    :date: 2019/06/17
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
import abc
from time import sleep
from typing import Iterable

from pylibrary.emulator.keybaordlayout import CommonKeyMatrix
from pylibrary.emulator.ledid import LED_ID
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pyraspi.services.kosmos.module.devicetree import DeviceTree

# ------------------------------------------------------------------------------
# Constants
# ------------------------------------------------------------------------------
# Action type strings
MAKE = 'make'
BREAK = 'break'
KEYSTROKE = 'keystroke'


class HOST:
    """
    Host indexes
    """
    CH1 = 1
    CH2 = 2
    CH3 = 3
    ALL = [CH1, CH2, CH3, ]
# end class HOST


# Default test sequence max duration before timeout
SEQUENCER_TIMEOUT_S = 30  # seconds


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class EmulatorInterface(metaclass=abc.ABCMeta):
    """
    Interface for emulator manager.
    """
    __instance = None

    @abc.abstractmethod
    def __init__(self, features):
        """
        :param features: Context features
        :type features: ``context.features``

        :raise ``AssertionError``: If an instance already exists
        """
        raise NotImplementedAbstractMethodError()
    # end def __init__

    @staticmethod
    def get_instance(features):
        """
        Return the Emulators Manager instance if it exists.

        :param features: Context features
        :type features: ``context.features``

        :return: Emulators Manager instance if it exists, None otherwise.
        :rtype: ``EmulatorsManager`` or ``None``
        """
        if EmulatorInterface.__instance is not None:
            return EmulatorInterface.__instance
        else:
            return None
        # end if
    # end def get_instance
# end class EmulatorInterface


class FpgaInterface(metaclass=abc.ABCMeta):
    """
    Interface for fpga module.
    """

    @staticmethod
    @abc.abstractmethod
    def reset_module():
        """
        Soft-reset the Microblaze CPU running on the FPGA.

        Wait for the CPU to start and initialize.
        Check if the microblaze is online and ready.
        Return the FPGA status after reset.

        :return: FPGA module status
        :rtype: ``fpga_status_t``
        """
        raise NotImplementedAbstractMethodError()
    # end def reset_module

    @staticmethod
    @abc.abstractmethod
    def pulse_global_go_line():
        """
        Send a high pulse on the Global Go signal going from the RaspberryPi to the FPGA.

        The high-pulse duration has been measured to last between 3 and 4 us.
        Beware that the RaspberryPi Linux OS is not real-time, so the actual pulse duration may be longer.
        """
        raise NotImplementedAbstractMethodError()
    # end def pulse_global_go_line

    @staticmethod
    @abc.abstractmethod
    def is_global_error_flag_raised():
        """
        Return the state of the Global Error flag.

        :return: True if the Global Error Flag is raised, False otherwise
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_global_error_flag_raised

    @staticmethod
    @abc.abstractmethod
    def reset_global_error_flag():
        """
        Reset the state of the Global Error flag
        """
        raise NotImplementedAbstractMethodError()
    # end def reset_global_error_flag
# end class FpgaInterface


class EventInterface(metaclass=abc.ABCMeta):
    """
    Interface for programmable event sequencer module.
    """

    @abc.abstractmethod
    def execute(self, action):
        """
        Add a PES:EXEC instruction to the local PES instruction buffer.

        :param action: Action(s) to be executed.
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase]``
        """
        raise NotImplementedAbstractMethodError()
    # end def execute

    @abc.abstractmethod
    def wait(self, action):
        """
        Add a PES:WAIT instruction to the local PES instruction buffer.

        :param action: Trigger(s) to be awaited for.
        :type action: ``PesResumeEventBase or Iterable[PesResumeEventBase]``
        """
        raise NotImplementedAbstractMethodError()
    # end def wait

    @abc.abstractmethod
    def delay(self, delay_s=None, delay_ns=None, delay_ticks=None, action=None):
        """
        Add a list of PES:DELAY, PES:SUBDELAY and/or PES:EXEC instructions to the local PES instruction buffer.

        Note that the delay duration can be expressed in seconds, nanoseconds or clock tick units.
        Only one delay argument can be used at a time.

        :param delay_s: Delay duration expressed in seconds - OPTIONAL
        :type delay_s: ``float or int or None``
        :param delay_ns: Delay duration expressed in nanoseconds - OPTIONAL
        :type delay_ns: ``float or int or None``
        :param delay_ticks: Delay duration expressed in FPGA clock ticks - OPTIONAL
        :type delay_ticks: ``int or None``
        :param action: Action(s) to be executed at the end of the delay - OPTIONAL
        :type action: ``PesActionEventBase or Iterable[PesActionEventBase] or None``
        """
        raise NotImplementedAbstractMethodError()
    # end def delay

    @abc.abstractmethod
    def marker(self, action):
        """
        Add a PES:MARKER instruction to the local PES instruction buffer.

        :param action: Marker(s) to be triggered. Refer to ``pes_isa_marker_operation_e__enumvalues``.
        :type action: ``pes_isa_marker_operation_e or int``
        """
        raise NotImplementedAbstractMethodError()
    # end def marker

    @abc.abstractmethod
    def wait_go_signal(self):
        """
        Halt the sequencer while a resume event is received from the RPi.
        """
        raise NotImplementedAbstractMethodError()
    # end def wait_go_signal
# end class EventInterface


class SequencerInterface(metaclass=abc.ABCMeta):
    """
    Interface for sequencer module.
    """

    @property
    @abc.abstractmethod
    def offline_mode(self):
        """
        Get offline mode parameter.

        :return: Flag to enable/disable the automatic sending of instructions to the FPGA
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def offline_mode

    @offline_mode.setter
    @abc.abstractmethod
    def offline_mode(self, offline_mode):
        """
        Set offline mode parameter.

        :param offline_mode: Flag to enable/disable the automatic sending of instructions to the FPGA
        :type offline_mode: ``bool``

        :raise ``AssertionError``: argument type should be bool
        """
        raise NotImplementedAbstractMethodError()
    # end def offline_mode

    @abc.abstractmethod
    def play_sequence(self, repetition=0, timeout=SEQUENCER_TIMEOUT_S, block=True):
        """
        Play the test sequence.

        For raised exceptions, refer to ``SequencerInterface.wait_end_of_sequence``.

        :param repetition: How many times the scenario is played again - OPTIONAL
        :type repetition: ``int``
        :param timeout: maximum allowed time without any status change, in seconds,
                        defaults to ``SEQUENCER_TIMEOUT_S`` - OPTIONAL
        :type timeout: ``int or float``
        :param block: Wait until the SEQUENCER state changes from RUNNING to IDLE or ERROR. - OPTIONAL
                      Note: `block` parameter must be True if `repetition` parameter is used.
        :type block: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def play_sequence

    @abc.abstractmethod
    def wait_end_of_sequence(self, timeout=SEQUENCER_TIMEOUT_S):
        """
        Poll Sequencer status periodically.
        Check Sequencer status and return when test sequence is done or presents errors.

        :param timeout: maximum allowed time without any status change, in seconds,
                        defaults to ``SEQUENCER_TIMEOUT_S`` - OPTIONAL
        :type timeout: ``int or float``

        :raise ``SequencerError``: if PES state value is ``SEQUENCER_STATE_ERROR`` or is unexpected
        :raise ``SequencerTimeoutError``: when no new status update was received in `timeout` seconds
        :raise ``AssertionError``: if there are still items in FIFOs or buffers after end of sequence
        """
        raise NotImplementedAbstractMethodError()
    # end def wait_end_of_sequence

    @abc.abstractmethod
    def is_sequencer_state_clean(self, status):
        """
        Check if Sequencer state is clean (FIFOs are empty, Sequencer state is IDLE or RESET)

        :param status: SequencerModule status
        :type status: ``sequencer_status_t``

        :return: Empty list if status is valid; List of error strings otherwise
        :rtype: ``list[str]``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_sequencer_state_clean
# end class SequencerInterface


class TimersInterface(metaclass=abc.ABCMeta):
    """
    Interface for the Timers module.
    """

    @abc.abstractmethod
    def reset(self, timers):
        """
        Add a PES:MARKER:RESET instruction to the local PES instruction buffer, for the given Timers.
        This instruction is only available for LOCAL & STOPWATCH timers.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``

        :raise ``KeyError``: If the present timer does not support the requested marker action.
        """
        raise NotImplementedAbstractMethodError()
    # end def reset

    @abc.abstractmethod
    def start(self, timers):
        """
        Add a PES:MARKER:START instruction to the local PES instruction buffer, for the given Timers.
        This instruction is only available for STOPWATCH timers.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``

        :raise ``KeyError``: If the present timer does not support the requested marker action.
        """
        raise NotImplementedAbstractMethodError()
    # end def start

    @abc.abstractmethod
    def restart(self, timers):
        """
        Reset and start one or more timers.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``

        :raise ``KeyError``: If the present timer does not support the requested action.
        """
        raise NotImplementedAbstractMethodError()
    # end def restart

    @abc.abstractmethod
    def stop(self, timers):
        """
        Add a PES:MARKER:STOP instruction to the local PES instruction buffer, for the given Timers.
        This instruction is only available for STOPWATCH timers.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``

        :raise ``KeyError``: If the present timer does not support the requested marker action.
        """
        raise NotImplementedAbstractMethodError()
    # end def stop

    @abc.abstractmethod
    def save(self, timers):
        """
        Save one or more timer's counter value in their respective buffers.

        :param timers: select which timer counter value to save
        :type timers: ``TIMER or Iterable[TIMER]``
        """
        raise NotImplementedAbstractMethodError()
    # end def save

    @abc.abstractmethod
    def download(self, count=None):
        """
        Download buffers of each timer.

        :param count: number of entries to be downloaded from remote buffer - OPTIONAL
                      If not provided, the whole buffers will be downloaded.
        :type count: ``int or None``

        :return: The list of downloaded entries
        :rtype: ``dict[TIMER, List[int]]``
        """
        raise NotImplementedAbstractMethodError()
    # end def download
# end class TimersInterface


class KosmosInterface(metaclass=abc.ABCMeta):
    """
    Interface for Kosmos Test Box discovery, configuration and usage.
    """
    _instance: 'KosmosInterface' = None

    # DeviceTree: dataclass referencing all the instantiated Kosmos Modules, in correlation to the loaded FPGA bitstream
    # Please refer to ``pyraspi.services.kosmos.module.devicetree.DeviceTree``
    dt: DeviceTree

    @staticmethod
    @abc.abstractmethod
    def get_instance():
        """
        Get ``KosmosInterface`` singleton instance.
        Shall not instantiate ``KosmosInterface`` object by any other way.

        :return: KosmosInterface instance
        :rtype: ``KosmosInterface``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_instance

    @staticmethod
    @abc.abstractmethod
    def is_connected():
        """
        Flag to tell if an actual board is connected on the CI node

        :return: true if an emulator board is connected, false otherwise
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_connected

    @staticmethod
    @abc.abstractmethod
    def discover_emulator(emulation_type, emulator_min_count=1):
        """
        Check if Kosmos system is available, then check its capabilities.

        :param emulation_type: Required emulation type
        :type emulation_type: ``DeviceName or DeviceFamilyName``
        :param emulator_min_count: Minimum count of emulator required; defaults to one - OPTIONAL
        :type emulator_min_count: ``int``

        :return: ``True`` if a Kosmos system is found and has the required capability, ``False`` otherwise
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def discover_emulator

    @staticmethod
    @abc.abstractmethod
    def has_capability(emulation_type, emulator_min_count=1):
        """
        Check if a given capability is supported by the emulator board

        :param emulation_type: Type of emulation required
        :type emulation_type: ``DeviceName or DeviceFamilyName``
        :param emulator_min_count: Minimum count of emulator required; defaults to one - OPTIONAL
        :type emulator_min_count: ``int``

        :return: true if an emulator board has the required capability, false otherwise
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def has_capability

    @staticmethod
    @abc.abstractmethod
    def get_capabilities():
        """
        Get the capabilities from the actual kosmos board

        :return: The mapping of capabilities supported by the actual Kosmos setup
        :rtype: ``dict[DeviceName or DeviceFamilyName, int]``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_capabilities

    @staticmethod
    @abc.abstractmethod
    def is_fake():
        """
        To identify the implementation is for actual Kosmos or mock Kosmos.

        :return: true if emulator is fake, false otherwise
        :rtype: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def is_fake

    @abc.abstractmethod
    def get_status(self):
        """
        Return Kosmos system status.

        :return: remote Kosmos system status.
        :rtype: ``Any``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_status

    @abc.abstractmethod
    def clear(self, force=False):
        """
        Clear modules consuming or producing instructions:
         - Clear local buffers of Modules consuming instructions,
         - Reset remote Modules consuming instructions,
         - Reset remote Modules producing data.

         :param force: abort running sequence, if any, and clear modules
         :type force: ``bool``

         :raise ``AssertionError``: If a sequence is running and `force=False`
        """
        raise NotImplementedAbstractMethodError()
    # end def clear
# end class KosmosInterface


class ButtonStimuliInterface(metaclass=abc.ABCMeta):
    """
    Interface for button stimuli emulation.
    """
    DEFAULT_DURATION = 0.2  # 200ms
    DEFAULT_DELAY = 0.2  # 200ms
    #  Easyswitch, connect button, virtual thumb Wheel: long press duration is 2s
    LONG_PRESS_THRESHOLD = 2  # 2000ms
    # OS layout selection: long press duration is 2s
    # cf https://drive.google.com/drive/folders/1alQi3lfHQvEK3D2LkJy2HXctLpTUo8Vg
    OS_LAYOUT_SELECTION_DURATION = 2.0  # 2000ms
    LONG_PRESS_DURATION = 3.1  # 3100ms

    @property
    @abc.abstractmethod
    def passive_hold_press_support(self):
        """
        Property to tell if a key can be held pressed without active action from emulator
        """
        raise NotImplementedAbstractMethodError()
    # end def passive_hold_press_support

    @property
    def keyboard_layout(self):
        """
        Get the selected physical keyboard layout.

        :return: The physical keyboard layout which was configured
        :rtype: ``CommonKeyMatrix``
        """
        return CommonKeyMatrix
    # end def keyboard_layout

    @abc.abstractmethod
    def release_all(self):
        """
        Release all known buttons
        """
        raise NotImplementedAbstractMethodError()
    # end def release_all

    @abc.abstractmethod
    def change_host(self, host_index=None, delay=None):
        """
        Change host user action

        :param host_index: targeted host index - OPTIONAL
        :type host_index: ``int`` or ``None``
        :param delay: timing after the keystroke - OPTIONAL
        :type delay: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def change_host

    @abc.abstractmethod
    def enter_pairing_mode(self, host_index=None, delay=None):
        """
        Force the device to enter into Discoverable mode

        :param host_index: targeted host index - OPTIONAL
        :type host_index: ``int`` or ``None``
        :param delay: timing after the keystroke - OPTIONAL
        :type delay: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def enter_pairing_mode

    @abc.abstractmethod
    def keystroke(self, key_id, duration=None, repeat=None, delay=None):
        """
        Emulate a keystroke.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID`` or ``int``
        :param duration: delay between make and break - OPTIONAL
        :type duration: ``float`` or ``None``
        :param repeat: repetition counter - OPTIONAL
        :type repeat: ``int`` or ``None``
        :param delay: timing between keystroke - OPTIONAL
        :type delay: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def keystroke

    @abc.abstractmethod
    def key_press(self, key_id):
        """
        Emulate a key press.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID`` or ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def key_press

    @abc.abstractmethod
    def key_release(self, key_id):
        """
        Emulate a key release.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID`` or ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def key_release

    def perform_action_list(self, action_list, duration=DEFAULT_DURATION, delay=DEFAULT_DELAY):
        """
        Emulate a suite of keystroke, make and / or break.

        :param action_list: list of key_id and action name
        :type action_list: ``list[tuple[KEY_ID,str]]``
        :param duration: delay between make and break - OPTIONAL
        :type duration: ``float``
        :param delay: time between 2 actions - OPTIONAL
        :type delay: ``float | None``
        """
        for (key_id, action_id) in action_list:
            if action_id == MAKE:
                self.key_press(key_id)
            elif action_id == BREAK:
                self.key_release(key_id)
            elif action_id == KEYSTROKE:
                self.keystroke(key_id, duration)
            else:
                raise ValueError(f'Wrong action id received: {action_id}')
            # end if
            if delay is not None and len(action_list) > 1:
                sleep(delay)
            # end if
        # end for
    # end def perform_action_list

    def perform_action_list_with_multiple_delays(self, action_list):
        """
        Emulate a suite of make and break with different delays

        :param action_list: list of key_id, action name and delay
        :type action_list: ``list[tuple[KEY_ID, str, float]]``
        """
        for key_id, action_id, delay in action_list:
            # TODO : See if the _sleep can be called after the press/release operation as in perform_action_list method
            self._sleep(delay)
            if action_id == MAKE:
                self.key_press(key_id)
            elif action_id == BREAK:
                self.key_release(key_id)
            else:
                raise ValueError(f'Invalid action_id received: {action_id}')
            # end if
        # end for
    # end def perform_action_list_with_multiple_delays

    @abc.abstractmethod
    def multiple_keys_press(self, key_ids, delay=None):
        """
        Emulate multiple key presses.

        :param key_ids: List of unique identifier of the keys to emulate
        :type key_ids: ``list[KEY_ID or int]``
        :param delay: Delay after each key press, in seconds - OPTIONAL
        :type delay: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def multiple_keys_press

    @abc.abstractmethod
    def multiple_keys_release(self, key_ids, delay=None):
        """
        Emulate multiple key releases.

        :param key_ids: List of unique identifier of the keys to emulate
        :type key_ids: ``list[KEY_ID or int]``
        :param delay: Delay after each key release, in seconds - OPTIONAL
        :type delay: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def multiple_keys_release

    @abc.abstractmethod
    def get_key_id_list(self):
        """
        Get a list of all the possible unique identifiers for this emulator.

        :return: list of supported KEY_ID
        :rtype: ``list``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_key_id_list

    @abc.abstractmethod
    def get_hybrid_key_id_list(self):
        """
        Get a list of all the hybrid button unique identifiers for this emulator.

        :return: list of supported hybrid KEY_ID
        :rtype: ``list``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_hybrid_key_id_list

    @abc.abstractmethod
    def get_fn_keys(self):
        """
        Return the mapping of Fn Function keys

        :return: The Fn function keys mapping table
        :rtype: ``dict``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_fn_keys

    @abc.abstractmethod
    def user_action(self):
        """
        Perform a simple user action
        """
        raise NotImplementedAbstractMethodError()
    # end def user_action

    def _sleep(self, delay):
        """
        Implement specific sleep instruction. Can be overloaded by derived classes.
        """
        if delay is not None and delay > 0:
            sleep(delay)
        # end if
    # end def _sleep

    @abc.abstractmethod
    def simultaneous_keystroke(self, key_ids, duration=None):
        """
        Emulate simultaneous keystrokes.

        :param key_ids: List of unique identifier of the keys to emulate
        :type key_ids: ``list[KEY_ID or int]``
        :param duration: delay between make and break - OPTIONAL
        :type duration: ``float``
        """
        raise NotImplementedAbstractMethodError()
    # end def simultaneous_keystroke
# end class ButtonStimuliInterface


class HybridButtonStimuliInterface(metaclass=abc.ABCMeta):
    """
    Interface for specific hybrid button (optical and galvanic) stimuli emulation.
    """
    @abc.abstractmethod
    def hybrid_key_press(self, key_id, galvanic_emulation=True, optical_emulation=True, galvanic_optical_delay=0):
        """
        Emulate a key press.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID`` or ``int``
        :param galvanic_emulation: flag indicating if the galvanic part is emulated - OPTIONAL
        :type galvanic_emulation: ``bool``
        :param optical_emulation: flag indicating if the optical part is emulated - OPTIONAL
        :type optical_emulation: ``bool``
        :param galvanic_optical_delay: timing between the emulation of the keystroke of the galvanic part and the
                                       optical part. Negative value when the optical switch is pressed before the
                                       galvanic one - OPTIONAL
        :type galvanic_optical_delay: ``float``
        """
        raise NotImplementedAbstractMethodError()
    # end def hybrid_key_press

    @abc.abstractmethod
    def hybrid_key_release(self, key_id, galvanic_emulation=True, optical_emulation=True, galvanic_optical_delay=0):
        """
        Emulate a key release.

        :param key_id: Unique identifier of the key to emulate
        :type key_id: ``KEY_ID`` or ``int``
        :param galvanic_emulation: flag indicating if the galvanic part is emulated - OPTIONAL
        :type galvanic_emulation: ``bool``
        :param optical_emulation: flag indicating if the optical part is emulated - OPTIONAL
        :type optical_emulation: ``bool``
        :param galvanic_optical_delay: timing between the emulation of the keystroke of the galvanic part and the
                                       optical part. Negative value when the optical switch is pressed before the
                                       galvanic one - OPTIONAL
        :type galvanic_optical_delay: ``float``
        """
        raise NotImplementedAbstractMethodError()
    # end def hybrid_key_release
# end class HybridButtonStimuliInterface


class Rpi4ButtonStimuliInterface(ButtonStimuliInterface, metaclass=abc.ABCMeta):
    """
    Interface for button stimuli emulation - Direct hardware control using RaspberryPi4 GPIOs.
    """

    @abc.abstractmethod
    def setup_connected_key_ids(self):
        """
        Setup connected pins list.
        This should be called during setup only.
        """
        raise NotImplementedAbstractMethodError()
    # end def setup_connected_key_ids

    @abc.abstractmethod
    def get_key_id_to_gpio_table(self):
        """
        Get mapping from key id to GPIO

        :return: Key Id to GPIO table
        :rtype: ``dict``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_key_id_to_gpio_table
# end class Rpi4ButtonStimuliInterface


class MotionEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for XY motion emulation.
    """

    @abc.abstractmethod
    def xy_motion(self, dx=None, dy=None, repetition=0, skip=0, prepare_sequence=True):
        """
        Emulate an XY motion.

        :param dx: X motion, default is None (X motion unmodified) - OPTIONAL
        :type dx: ``int``
        :param dy: Y motion, default is None (Y motion unmodified) - OPTIONAL
        :type dy: ``int``
        :param repetition: Number of repeated motion - OPTIONAL
        :type repetition: ``int``
        :param skip: Timings in us between two motions - OPTIONAL
        :type skip: ``int``
        :param prepare_sequence: Prepare a test sequence for the XY motion, default is True - OPTIONAL
        :type prepare_sequence: ``bool``

        :raise ``AssertionException``:  - At least one of `dx` or `dy` parameter must be an integer
        """
        raise NotImplementedAbstractMethodError()
    # end def xy_motion
# end class MotionEmulationInterface


class PowerSupplyEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for power supply emulation.
    """

    @property
    def has_sink_current_capability(self):
        """
        Sink current capability.
        """
        raise NotImplementedAbstractMethodError()
    # end def has_sink_current_capability

    @abc.abstractmethod
    def turn_on(self):
        """
        Emulate a turn-on of the device.
        """
        raise NotImplementedAbstractMethodError()
    # end def turn_on

    @abc.abstractmethod
    def turn_off(self):
        """
        Emulate a turn-off of the device.
        """
        raise NotImplementedAbstractMethodError()
    # end def turn_off

    def is_off(self):
        """
        Provide the current state of the power supply.
        """
        return self.get_voltage() == 0
    # end def is_off

    @abc.abstractmethod
    def set_voltage(self, voltage, fast_ramp=True):
        """
        Set the battery to a certain level.

        :param voltage: Targeted voltage value in V.
        :type voltage: ``float``
        :param fast_ramp: Voltage incrementation method: - OPTIONAL
                            - True: enable several increment values to get faster to the
                                    expected value
                            - False: increment the voltage by small step (around 1mV by step)
        :type fast_ramp: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def set_voltage

    @abc.abstractmethod
    def configure_measurement_mode(self, mode="tension"):
        """
        Choose the measurement mode.

        :param mode: Measurement mode: "tension" or "current" - OPTIONAL
        :type mode: ``str``
        """
        raise NotImplementedAbstractMethodError()
    # end def configure_measurement_mode

    @abc.abstractmethod
    def get_voltage(self):
        """
        Get the battery level.
        """
        raise NotImplementedAbstractMethodError()
    # end def get_voltage

    @abc.abstractmethod
    def get_current(self):
        """
        Get the actual current consumption.
        """
        raise NotImplementedAbstractMethodError()
    # end def get_current

    @abc.abstractmethod
    def restart_device(self, starting_voltage=None):
        """
        Restart the device

        Shall be overloaded by specific power supply implementation

        :param starting_voltage: The voltage to use after restart, if None the Nominal value will be used - OPTIONAL
        :type starting_voltage: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def restart_device

    @abc.abstractmethod
    def recharge(self, enable):
        """
        Set recharge enable or disable

        :param enable: enable or disable the function
        :type enable: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def recharge
# end class PowerSupplyEmulationInterface


class SliderEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for Slider Controller Module.
    """
    @abc.abstractmethod
    def open_slider(self, slider_id):
        """
        Connect the poles 1 & 2 of the given slider.
        Result='position_1-2'

        :param slider_id: Slider identifier
        :type slider_id: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def open_slider

    @abc.abstractmethod
    def close_slider(self, slider_id):
        """
        Connect the poles 2 & 3 of the given slider.
        Result='position_2-3'

        :param slider_id: Slider identifier
        :type slider_id: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def close_slider

    @abc.abstractmethod
    def make_before_break(self, slider_id):
        """
        Physically disconnect the 3 poles of the given slider.
        Result='no contact' (used to emulate a "break-before-make" behavior of a changeover switch.

        :param slider_id: Slider identifier
        :type slider_id: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def make_before_break

    @abc.abstractmethod
    def no_contact_2(self, slider_id):
        """
        Second option to physically disconnect the 3 poles of the given slider.
        Result='no contact' ("no contact")

        :param slider_id: Slider identifier
        :type slider_id: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def no_contact_2
# end class SliderEmulationInterface


class PowerSliderEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for Power Slider Controller Module.
    """
    @abc.abstractmethod
    def power_off(self):
        """
        Power off the DUT using the power switch
        """
        raise NotImplementedAbstractMethodError()
    # end def power_off

    @abc.abstractmethod
    def power_on(self):
        """
        Power on the DUT using the power switch
        """
        raise NotImplementedAbstractMethodError()
    # end def power_on

    @abc.abstractmethod
    def reset(self, duration=.5):
        """
        Reset the DUT using the power switch

        :param duration: time during which the DUT is off - OPTIONAL
        :type duration: ``float``
        """
        raise NotImplementedAbstractMethodError()
    # end def reset
# end class PowerSliderEmulationInterface


class AmbientLightSensorEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for ambient light sensor emulation
    """
    @abc.abstractmethod
    def set_ambient_light_intensity(self, illuminance=None):
        """
        Set the ambient light intensity to a certain level.

        :param illuminance: Targeted illuminance value in lux. Set to ``None`` to force the default value - OPTIONAL
        :type illuminance: ``float`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def set_ambient_light_intensity

    @abc.abstractmethod
    def get_luminance_threshold_backlight_off(self):
        """
        Get the luminance threshold to turn off the backlight.

        :return: the default luminance value
        :rtype: ``float``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_luminance_threshold_backlight_off
# end class AmbientLightSensorEmulationInterface


class ProximitySensorEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for Proximity Sensor emulation
    """
    @abc.abstractmethod
    def set_proximity_presence(self, enable=True):
        """
        Emulate the proximity presence detect by the sensor

        :param enable: Flag indicating if an object was detected by the sensor - OPTIONAL
        :type enable: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def set_proximity_presence
# end class ProximitySensorEmulationInterface


class LedSpyInterface(metaclass=abc.ABCMeta):
    """
    Interface for LEDs monitoring module.
    """

    @abc.abstractmethod
    def start(self, led_identifiers):
        """
        Start the monitoring of some given IOs

        :param led_identifiers: List of LED to start monitoring
        :type led_identifiers: ``list[LED_ID]``
        """
        raise NotImplementedAbstractMethodError()
    # end def start

    @abc.abstractmethod
    def stop(self, led_identifiers):
        """
        Stop the monitoring of some given IOs

        :param led_identifiers: List of LED to start monitoring
        :type led_identifiers: ``list[LED_ID]``
        """
        raise NotImplementedAbstractMethodError()
    # end def stop

    def reset(self):
        """
        Initialize transition iterator to None to restart parsing the transition from the start
        """
        raise NotImplementedAbstractMethodError()
    # end def reset

    def flush_led_data(self):
        """
        Flush LED fifo into SW buffer
        """
        raise NotImplementedAbstractMethodError()
    # end def flush_led_data

    def get_timeline(self):
        """
        Post process the data received on the PWM Led spy stream

        For each PWM signal, we compute the average period (or pulse width), the duty cycle, the period standard
        deviation, the duty cycle standard deviation and a spiking counter (pulse width less than X polls)

        :return: A structure with all events that occurred during the LED monitoring period
        :rtype: ``pyraspi.services.kosmos.leds.leddataparser.TimeLine`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_timeline

    @abc.abstractmethod
    def get_led_identifiers(self):
        """
        Retrieve the list of led identifiers for which the monitoring is enabled.

        :return: list of active led identifiers
        :rtype: ``list[LED_ID]``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_led_identifiers
# end class LedSpyInterface


class LedSpyOverI2cInterface(metaclass=abc.ABCMeta):
    """
    Interface for I2C monitoring module.
    """

    @abc.abstractmethod
    def start(self, reset=True, led_identifiers=None):
        """
        Start the monitoring of some given IOs

        :param reset: Reset the module before starting the monitoring - OPTIONAL
        :type reset: ``bool``
        :param led_identifiers: List of LED to start monitoring - OPTIONAL
        :type led_identifiers: ``list[LED_ID]``
        """
        raise NotImplementedAbstractMethodError()
    # end def start

    @abc.abstractmethod
    def stop(self, parse_i2c_frame=True):
        """
        Stop the monitoring of some given IOs

        :param parse_i2c_frame: Flag indicating if we parse the I2C frames to extract leds intensity values
                                timeline - OPTIONAL
        :type parse_i2c_frame: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def stop

    @abc.abstractmethod
    def download(self):
        """
        Download I2C capture data buffer
        """
        raise NotImplementedAbstractMethodError()
    # end def download

    def get_timeline(self):
        """
        Post process the data received on the backlight I2C stream.

        :return: A structure with all events that occurred during the LED monitoring period
        :rtype: ``pyraspi.services.kosmos.leds.leddataparser.TimeLine``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_timeline
# end class LedSpyOverI2cInterface


class WheelEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for wheel emulation
    """
    @abc.abstractmethod
    def get_speed(self):
        """
        Get the wheel speed

        :return: Wheel speed
        :rtype: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_speed

    @abc.abstractmethod
    def set_speed(self, speed):
        """
        Set the wheel speed

        :param speed: Wheel speed to set
        :type speed: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def set_speed
# end class WheelEmulationInterface


class RatchetEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for ratchet emulation
    """
    class STATE:
        """
        Ratchet states
        """
        DISENGAGED = 0
        ENGAGED = 1
    # end class STATE

    @abc.abstractmethod
    def get_state(self):
        """
        Get ratchet state

        :return: Ratchet state
        :rtype: ``STATE``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_state

    @abc.abstractmethod
    def set_state(self, state):
        """
        Set ratchet state

        :param state: Ratchet state to set
        :type state: ``STATE``
        """
        raise NotImplementedAbstractMethodError()
    # end def set_state
# end class RatchetEmulationInterface

class GameModeEmulationInterface(metaclass=abc.ABCMeta):
    """
    Interface for GameMode Slider Controller Module.
    """
    class MODE:
        """
        Mode states
        """
        DISABLED = 0
        ENABLED = 1
    # end class MODE

    @abc.abstractmethod
    def get_state(self):
        """
        Get game mode state

        :return: Mode state
        :rtype: ``MODE``
        """
        raise NotImplementedAbstractMethodError()
    # end def get_state

    @abc.abstractmethod
    def set_mode(self, activate_game_mode=False):
        """
        Set the DUT in the normal mode

        :param activate_game_mode: Flag indicating if the mode is force to gaming - OPTIONAL
        :type activate_game_mode: ``bool``
        """
        raise NotImplementedAbstractMethodError()
    # end def set_mode
# end class GameModeEmulationInterface

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
