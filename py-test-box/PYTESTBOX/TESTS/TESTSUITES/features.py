#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: features
:brief: RUNTIME SubSystem implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/07/25
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class RootSubSystem( AbstractSubSystem ):
    """
    The features definition of the ROOT and RUNTIME subsystem.
    This subsystem is MANDATORY for the validation to work properly.

    Note: Declare this subsystem under the name RUNTIME
        This will cause the serialization to read/write the features under
        the section [RUNTIME]
    """

    def __init__( self ):
        AbstractSubSystem.__init__(self, None)

        self.RUNTIME = self.RuntimeSubSystem()                                                                          # pylint:disable=C0103

        self.LOGGING = self.LoggingSubSystem()
    # end def __init__

    class RuntimeSubSystem(AbstractSubSystem):                                                                          # pylint:disable=R0902
        """
        Contains the definition of the RUNTIME subsystem.
        This subsystem is MANDATORY for the validation to work properly.
        """
        def __init__( self ):
            AbstractSubSystem.__init__(self, "RUNTIME")

            # Activate the subsystem by default
            # This is a required feature for all subsystems.
            self.F_Enabled = True

            self.F_InputDirPattern = "SETTINGS/%(PRODUCT)s/%(VARIANT)s"
            self.F_OutputDirPattern = "LOCAL/%(PRODUCT)s/%(VARIANT)s"

            # Random seed: 0: fixed seed, test dependant, None: truly random, int: fixed seed
            self.F_RandSeed = 0

            # Device Manager to use
            self.F_DeviceManager = None
            # USB context class
            self.F_UsbContextClass = None

            self.DEBUGGERS = self.DebuggersSubSystem()
        # end def __init__

        class DebuggersSubSystem(AbstractSubSystem):
            """
            Contains the definition of the DEBUGGERS subsystem.

            Note: Declare this subsystem under the name DEBUGGERS
                This will cause the serialization to read/write the features under
                the section [DEBUGGERS]
            """
            def __init__(self):
                AbstractSubSystem.__init__(self, "DEBUGGERS")

                # Activate the subsystem by default
                # This is a required feature for all subsystems.
                self.F_Enabled = True

                # The list of debuggers' targets and types to use
                # Targets can be Device, Receiver, Device Companion, Receiver Companion for example
                self.F_Targets = ()
                # Types should be defined in DEBUGGERS_MAPPING (cf pyharness.debuggers)
                # e.g. Types   = ("ReceiverMesonJlinkDebugger" , "QuarkJlinkDebugger" , "TLSR8208CDebugger", ...)
                self.F_Types = ()
            # end def __init__
        # end class DebuggersSubSystem

        class LatencySubSystem(AbstractSubSystem):
            """
            Enable/Disable the Latency measurements subsystem.
            """
            def __init__(self):
                AbstractSubSystem.__init__(self, "LATENCY")

                # Flag to enable the USB latency tests with USB analyser (motion and click latency test suites)
                self.F_EnableUSBLatencyTestsWithUsbAnalyser = False
                # Flag to enable the LSX latency tests with USB analyser (motion and click latency test suites)
                self.F_EnableLSXLatencyTestsWithUsbAnalyser = False
            # end def __init__
        # end class LatencySubSystem
    # end class RuntimeSubSystem

    class LoggingSubSystem(AbstractSubSystem):
        """
        Contains the definition of the LOGGING subsystem.
        This subsystem is MANDATORY for the validation to work properly.

        Note: Declare this subsystem under the name LOGGING
            This will cause the serialization to read/write the features under
            the section [LOGGING]
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "LOGGING")

            # Activate the subsystem by default
            # This is a required feature for all subsystems.
            self.F_Enabled = True

            # Enable LogHelper verbose
            self.F_LogHelperVerbose = False
            # Enable LogHelper verbose color
            self.F_LogHelperVerboseColor = False

            # Enable Emulator verbose
            self.F_EmulatorVerbose = False

            # Transport trace level
            # It can be None, an int, or a string representing the name of the level. The possible string values are
            # the name of the different level in ``pylibrary.system.tracelogger.TraceLevel``
            # Example:
            #  - None: disable all traces (Default)
            #  - TraceLevel.ERROR and TraceLevel.WARNING are self explanatory
            #  - TraceLevel.INFO: Info level will be used for packets
            #  - TraceLevel.DEBUG: Debug level will be for every context actions
            self.F_TransportTraceLevel = None

            # Enable logging UART information, require a FTDI on the device and setting SerialSource
            # and flashing debug hex on the device!
            self.F_SerialLoggingEnabled = False

            # Which uart source to use (ex, '/dev/ttyUSB4')
            # to find it use:
            #  "dmesg | grep ttyUSB" show a list of FTDI that are connected and create a usb tty.
            #  with the port information shown the correct tty can be determined. (if too many messages
            #  were received a reboot might be necessary)
            self.F_SerialSource = None
        # end def __init__
    # end class LoggingSubSystem
# end class RootSubSystem

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
