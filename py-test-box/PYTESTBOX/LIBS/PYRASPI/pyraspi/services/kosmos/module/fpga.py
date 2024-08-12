#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pyraspi.services.kosmos.module.fpga
:brief: Kosmos FPGA Module Class
:author: Lila Viollette <lviollette@logitech.com>
:date: 2022/01/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABCMeta
from time import sleep

from pylibrary.emulator.emulatorinterfaces import FpgaInterface
from pyraspi.raspi import Raspi
from pyraspi.services.daemon import Daemon
from pyraspi.services.globalreset import GlobalReset
from pyraspi.services.kosmos.module.module import StatusResetModuleBaseClass
from pyraspi.services.kosmos.module.module import StatusResetModuleSettings
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_RESET
from pyraspi.services.kosmos.protocol.generated.messages import MSG_ID_FPGA_CMD_STATUS
from pyraspi.services.kosmos.protocol.generated.messages import fpga_status_t

if Raspi.is_host_raspberry_pi():
    from RPi import GPIO
# end if

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------

CPU_BOOT_TIME_S: float = 0.5  # Wait min 500 ms for the CPU to start and initialize


# ------------------------------------------------------------------------------
# global variables
# ------------------------------------------------------------------------------

# Set by GPIO interrupt when Global Error signal is received
_global_error_flag_raised: bool = False


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
def _gpio_interrupt_event(gpio):
    """
    Method called by the ``GPIO.add_event_detect()`` function, triggered by the Global Error signal.
    Note that this method will be called from a different thread, dedicated to RPi.GPIO functionality.

    :param gpio: GPIO pin number
    :type gpio: ``int``

    :raise ``ValueError``: Unknown GPIO channel
    """
    global _global_error_flag_raised
    if gpio == Raspi.PIN.GLOBAL_ERROR:
        _global_error_flag_raised = True
    else:
        raise ValueError(f'Unknown GPIO channel {gpio}.')
    # end if
# end def _gpio_interrupt_event


class FpgaModule(StatusResetModuleBaseClass, FpgaInterface):
    """
    Kosmos FPGA Module class
    """

    def __init__(self):
        module_settings = StatusResetModuleSettings(
            name=r'FPGA',
            instance_id=None,  # Module is a singleton
            optional=False,
            msg_id=MSG_ID_FPGA,
            status_type=fpga_status_t,
            msg_cmd_status=MSG_ID_FPGA_CMD_STATUS,
            msg_cmd_reset=MSG_ID_FPGA_CMD_RESET
        )
        super().__init__(module_settings=module_settings)

        # Initialize RPi pins to interface the FPGA
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        # Output pins
        GPIO.setup(Raspi.PIN.STATUS_LED_1, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(Raspi.PIN.GLOBAL_GO, GPIO.OUT, initial=GPIO.LOW)
        # Input pins
        GPIO.setup(Raspi.PIN.AUX_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Raspi.PIN.AUX_3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Raspi.PIN.AUX_4, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Raspi.PIN.AUX_5, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Raspi.PIN.AUX_6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(Raspi.PIN.AUX_7, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # Input/output pins
        self.reset_global_error_flag()

        if Daemon.is_host_kosmos():
            GPIO.setup(Raspi.PIN.AUX_8, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(Raspi.PIN.CMOD_0, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(Raspi.PIN.CMOD_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            GPIO.setup(Raspi.PIN.CMOD_2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        # end if
    # end def __init__

    def __del__(self):
        """
        Clear the FPGA resources.
        """
        try:
            # De-initialize RPi pins
            GPIO.setmode(GPIO.BOARD)
            GPIO.setwarnings(False)
            GPIO.remove_event_detect(Raspi.PIN.GLOBAL_ERROR)

            # Output pin (set as input with pull-down to avoid interferences)
            GPIO.setup(Raspi.PIN.STATUS_LED_1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

            # Output pin (keep as output LOW, because pull-down is not strong enough to avoid interferences)
            GPIO.setup(Raspi.PIN.GLOBAL_GO, GPIO.OUT, initial=GPIO.LOW)

            # Input/output pin (set as input with pull-up to avoid interferences)
            GPIO.setup(Raspi.PIN.GLOBAL_ERROR, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            # Input pins (set as inputs without pull-up, pull-down nor interrupt)
            GPIO.cleanup(Raspi.PIN.AUX_2)
            GPIO.cleanup(Raspi.PIN.AUX_3)
            GPIO.cleanup(Raspi.PIN.AUX_4)
            GPIO.cleanup(Raspi.PIN.AUX_5)
            GPIO.cleanup(Raspi.PIN.AUX_6)
            GPIO.cleanup(Raspi.PIN.AUX_7)

            if Daemon.is_host_kosmos():
                GPIO.cleanup(Raspi.PIN.AUX_8)
                GPIO.cleanup(Raspi.PIN.CMOD_0)
                GPIO.cleanup(Raspi.PIN.CMOD_1)
                GPIO.cleanup(Raspi.PIN.CMOD_2)
            # end if
        except RuntimeError:
            pass
        # end try
    # end def __del__

    def is_status_reply_valid(self, status):
        """
        Validate Status structure.

        :param status: Status structure
        :type status: ``fpga_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
        :rtype: ``List[str]``
        """
        return super().is_status_reply_valid(status)
    # end def is_status_reply_valid

    def is_reset_reply_valid(self, status):
        """
        Validate Reset command's Status reply structure.

        :param status: Status structure
        :type status: ``fpga_status_t``

        :return: Empty list if status is valid; List of error strings if any of the following conditions is met:
                  - base class method returned a list of error
        :rtype: ``List[str]``
        """
        return super().is_reset_reply_valid(status)
    # end def is_reset_reply_valid

    @staticmethod
    def pulse_global_go_line():
        # See ``FpgaInterface.pulse_global_go_line``
        GPIO.output(Raspi.PIN.GLOBAL_GO, GPIO.HIGH)
        GPIO.output(Raspi.PIN.GLOBAL_GO, GPIO.LOW)
    # end def pulse_global_go_line

    @staticmethod
    def is_global_error_flag_raised():
        """
        Return the state of the Global Error flag.

        :return: True if the Global Error Flag is raised, False otherwise
        :rtype: ``bool``
        """
        global _global_error_flag_raised
        return _global_error_flag_raised
    # end def is_global_error_flag_raised

    @staticmethod
    def reset_global_error_flag():
        """
        Reset the state of the Global Error flag
        """
        global _global_error_flag_raised
        _global_error_flag_raised = False
    # end def reset_global_error_flag

    def reset_module(self):
        # See ``FpgaInterface.reset_module``
        return self.soft_reset_microblaze()
    # end def reset_module

    def soft_reset_microblaze(self):
        """
        Soft-reset the Microblaze CPU running on the FPGA, using the Global Error signal.

        Wait for the CPU to start and initialize.
        Check if the microblaze is online and ready.
        Return the FPGA status after reset.

        :return: FPGA module status
        :rtype: ``fpga_status_t``
        """
        # Raise the Error Flag, which in turn will make the microblaze soft-reset itself
        GlobalReset.raise_global_error_flag(callback=_gpio_interrupt_event)

        # Call post-reset callbacks: actions to be done after reset of the module or the system
        self._process_reset_callbacks()

        # Wait for the CPU to start and initialize
        sleep(CPU_BOOT_TIME_S)

        # Get new status after reboot
        return self.status()
    # end def soft_reset_microblaze

    def _process_reset_callbacks(self):
        # See ``StatusResetModuleBaseClass._process_reset_callbacks``
        # Process FPGA module reset callbacks
        super()._process_reset_callbacks()

        # Process all other modules reset callbacks
        for module in self.dt.flatmap.values():
            if isinstance(module, StatusResetModuleBaseClass) and module is not self:
                module._process_reset_callbacks()
            # end if
        # end for
    # end def _process_reset_callbacks
# end class FpgaModule

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
