#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.base.features
:brief: pytestbox SubSystem implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/11/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ProductSubSystem(AbstractSubSystem):
    """
    PRODUCT SubSystem
    """

    def __init__(self):
        AbstractSubSystem.__init__(self, "PRODUCT")

        # ------------
        # Main feature
        # ------------
        self.F_Enabled = False

        self.F_DeviceID = ''

        self.F_ProductID = ''

        # GetFwInfo TransportID
        self.F_TransportID = ('C088',)

        # Bluetooth PID
        self.F_BluetoothPID = None

        # EQuad PID
        self.F_EQuadPID = None

        # HID++ device index parameter:
        # - 0xFF for direct USB connection
        # - 0x01 if first device on USB receiver
        # - 0x0n if n th device on USB receiver
        self.F_DeviceIndex = 0xFF

        self.F_ProductReference = None

        self.F_NvsStartAddress = 0
        self.F_NvsSize = 0
        self.F_NvsBankSize = 0
        # Specify if a full bank has to be erased to delete a chunk. This means that banks will be switched on a
        # chunk delete action. This is the case for example on STM32H7 like Lexend.
        self.F_FullBankErase = False

        # This is to specify if the DUT is a platform
        self.F_IsPlatform = False
        # This is to specify if the DUT's power is on the FTDI port
        self.F_PowerOnFTDI = False

        self.F_IsGaming = False

        self.F_IsMice = False
        self.F_IsKeyPad = False
        self.F_IsLightingDevice = False

        # Specify if the DUT has a companion MCU
        self.F_CompanionMCU = False

        # Business Features Enabler/Disabler SubSystem
        self.FEATURES = self.FeaturesSubSystem()

        # Device settings
        self.DEVICE = self.DeviceSubSystem()

        # Debounce settings
        self.DEBOUNCE = self.DebounceSubSystem()

        # Latency SubSystem
        self.LATENCY = self.LatencySubSystem()

        # NVS Chunk Ids settings
        self.NVS_CHUNK_IDS = self.NvsChunkIdsSubSystem()

        # NVS and UICR
        self.NVS_UICR = self.NvsUicrSubSystem()

        # Code CheckList
        self.CODE_CHECKLIST = self.CodeCheckListSubSystem()

        # HID Reports definition
        self.HID_REPORT = self.HidReportSubSystem()

        # Timings
        self.TIMINGS = self.TimingsSubSystem()

        # USB Communication
        self.USB_COMMUNICATION = self.UsbCommunicationSubSystem()

        # Protocols
        self.PROTOCOLS = self.ProtocolsSubSystem()

        # Dual bank
        self.DUAL_BANK = self.DualBankSubSystem()
    # end def __init__

    class FeaturesSubSystem(AbstractSubSystem):
        """
        Business Features Enabler/Disabler SubSystem
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "FEATURES")

            # # Main feature
            self.F_Enabled = True

            # # HID++ feature
            # Important Features
            self.IMPORTANT = self.ImportantFeatureSubSystem()

            # Common Features
            self.COMMON = self.CommonFeatureSubSystem()

            # Mouse Features
            self.MOUSE = self.MouseSubSystem()

            # Keyboard Features
            self.KEYBOARD = self.KeyboardSubSystem()

            # Touchpad Features
            self.TOUCHPAD = self.TouchpadFeatureSubSystem()

            # Gaming Features
            self.GAMING = self.GamingSubSystem()

            # Peripheral Test Features
            self.PERIPHERAL = self.PeripheralTestFeatureSubSystem()

            # # VLP feature
            self.VLP = self.VariableLengthProtocolSubSystem()
        # end def __init__

        class ImportantFeatureSubSystem(AbstractSubSystem):
            """
            Important Features Enabler/Disabler Subsystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "IMPORTANT")

                self.F_Enabled = False

                # 0x0000 Root
                self.ROOT = self.RootSubSystem()

                # 0x0001 Feature Set
                self.FEATURE_SET = self.FeatureSetSubSystem()
            # end def __init__

            class RootSubSystem(AbstractSubSystem):
                """
                Feature 0x0000

                Enable/Disable Root SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ROOT")

                    # FeatureSet feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False

                    # The protocol number is a field that hints the host software if it should support the device.
                    # - 0x02 for our gaming devices
                    # - 0x05 for our core products
                    self.F_ProtocolNum = HexList('04')

                    # This field further hints at which software should support the device
                    # - 0x02 for our gaming devices
                    # - 0x05 for our core products
                    # in Application mode
                    self.F_TargetSW = HexList('05')
                    # in BootLoader mode
                    self.F_BootLoaderTargetSW = None
                # end def __init__
            # end class RootSubSystem

            class FeatureSetSubSystem(AbstractSubSystem):
                """
                Feature 0x0001

                Enable/Disable FeatureSet SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "FEATURE_SET")

                    # FeatureSet feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False

                    # The number of features in the set, not including the root feature
                    # NB: Response check could be disabled during early development phase by keeping the None settings
                    # in Application when communicating over:
                    # - USB (corded devices)
                    self.F_FeatureCountInUSB = None
                    # - Unifying (proprietary RF receiver)
                    self.F_FeatureCountInUFY = None
                    # - BLE (BLE Pro receiver)
                    self.F_FeatureCountInBLE = None
                    # in Bootloader when communicating over:
                    # - USB (corded devices)
                    self.F_BootloaderFeatureCountInUSB = None
                    # - Unifying (proprietary RF receiver)
                    self.F_BootloaderFeatureCountInUFY = None
                    # - BLE (BLE Pro receiver)
                    self.F_BootloaderFeatureCountInBLE = None
                # end def __init__
            # end class FeatureSetSubSystem
        # end class ImportantFeatureSubSystem

        class CommonFeatureSubSystem(AbstractSubSystem):
            """
            Common Features Enabler/Disabler Subsystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "COMMON")

                # Common features
                self.F_Enabled = False

                # 0x0003 Device Info
                self.DEVICE_INFORMATION = self.DeviceInformationSubSystem()

                # 0x0005 Device Type And Name
                self.DEVICE_TYPE_AND_NAME = self.DeviceTypeAndNameSubSystem()

                # 0x0007 Device Friendly Name
                self.DEVICE_FRIENDLY_NAME = self.DeviceFriendlyNameSubSystem()

                # 0x0008 Keep Alive
                self.KEEP_ALIVE = self.KeepAliveSubSystem()

                # 0x0011 Property Access
                self.PROPERTY_ACCESS = self.PropertyAccessSubSystem()

                # 0x0020 Config Change
                self.CONFIG_CHANGE = self.ConfigChangeSubSystem()

                # 0x0021 32 Bytes Unique Identifier
                self.UNIQUE_IDENTIFIER_32_BYTES = self.UniqueIdentifier32BytesSubSystem()

                # feature 0x00C2 and register 0xF0 DFU Control
                self.DFU_CONTROL = self.DfuControlSubSystem()

                # feature 0x00C3 and register 0xF5 Secure DFU Control
                self.SECURE_DFU_CONTROL = self.SecureDfuControlSubSystem()

                # 0x00D0 DFU
                self.DFU = self.DfuSubSystem()

                # 0x1000 Battery Unified Level Status
                self.BATTERY_UNIFIED_LEVEL_STATUS = self.BatteryUnifiedLevelStatusSubSystem()

                # 0x1004 Unified Battery
                self.UNIFIED_BATTERY = self.UnifiedBatterySubSystem()

                # 0x1500 Force Pairing
                self.FORCE_PAIRING = self.ForcePairingSubSystem()

                # 0x1602 Password Authentication
                self.PASSWORD_AUTHENTICATION = self.PasswordAuthenticationSubSystem()

                # 0x1801 Manufacturing Mode
                self.MANUFACTURING_MODE = self.ManufacturingModeSubSystem()

                # 0x1802 Device Reset
                self.DEVICE_RESET = self.DeviceResetSubSystem()

                # 0x1803 GPIO access
                self.GPIO_ACCESS = self.GpioAccessSubSystem()

                # 0x1805 OOB State
                self.OOB_STATE = self.OobStateSubSystem()

                # 0x1806 Configurable Device Properties
                self.CONFIGURABLE_DEVICE_PROPERTIES = self.ConfDevPropSubSystem()

                # 0x1807 Configurable Properties
                self.CONFIGURE_PROPERTIES = self.ConfigurePropertiesSubSystem()

                # 0x180B Configurable Device Registers
                self.CONFIGURABLE_DEVICE_REGISTERS = self.ConfigurableDeviceRegistersSubSystem()

                # 0x1814 Change Host
                self.CHANGE_HOST = self.ChangeHostSubSystem()

                # 0x1815 Hosts Info
                self.HOSTS_INFO = self.HostsInfo()

                # 0x1816 Device BLE Pro pre-pairing
                self.BLE_PRO_PREPAIRING = self.BleProPrepairing()

                # 0x1817 Lightspeed Prepairing
                self.LIGHTSPEED_PREPAIRING = self.LightspeedPrepairingSubSystem()

                # 0x1830 Power Modes
                self.POWER_MODES = self.PowerModesSubSystem()

                # 0x1861 Battery Levels Calibration
                self.BATTERY_LEVELS_CALIBRATION = self.BatteryLevelsCalibrationSubSystem()

                # 0x1876 Optical Switches
                self.OPTICAL_SWITCHES = self.OpticalSwitchesSubSystem()

                # 0x1890 RF Test
                self.RF_TEST = self.RFTestSubSystem()

                # 0x18A1 LED Test
                self.LED_TEST = self.LEDTestSubSystem()

                # 0x18B0 Monitor Mode
                self.STATIC_MONITOR_MODE = self.StaticMonitorModeSubSystem()

                # 0x1982 Backlight
                self.BACKLIGHT = self.BacklightSubSystem()

                # 0x19C0 Force Sensing Button
                self.FORCE_SENSING_BUTTON = self.ForceSensingButtonSubSystem()

                # 0x1B04 Special Keys MSE Buttons
                self.SPECIAL_KEYS_MSE_BUTTONS = self.SpecialKeysMSEButtonsSubSystem()

                # 0x1B05 Full Key Customization
                self.FULL_KEY_CUSTOMIZATION = self.FullKeyCustomizationSubSystem()

                # 0x1B08 Analog Keys
                self.ANALOG_KEYS = self.AnalogKeysSubSystem()

                # 0x1B10 Control List
                self.CONTROL_LIST = self.ControlListSubSystem()

                # 0x1D4B Wireless Device Status
                self.WIRELESS_DEVICE_STATUS = self.WirelessDeviceStatusSubSystem()

                # 0x1DF3 eQuad DJ Debug Info
                self.EQUAD_DJ_DEBUG_INFO = self.EquadDJDebugInfoSubSystem()

                # 0x1E00 Enable Hidden Features
                self.ENABLE_HIDDEN = self.EnableHiddenSubSystem()

                # 0x1E01 Manage Deactivatable Features
                self.MANAGE_DEACTIVATABLE_FEATURES = self.ManageDeactivatableFeaturesSubSystem()

                # 0x1E02 Manage Deactivatable Features
                self.MANAGE_DEACTIVATABLE_FEATURES_AUTH = self.ManageDeactivatableFeaturesAuthSubSystem()

                # 0x1E22 SPI Direct Access
                self.SPI_DIRECT_ACCESS = self.SPIDirectAccessSubSystem()

                # 0x1E30 I2C Direct Access
                self.I2C_DIRECT_ACCESS = self.I2CDirectAccessSubSystem()

                # 0x1EB0 TDE Access to NVM Features
                self.TDE_ACCESS_TO_NVM = self.TdeAccessToNvmSubSystem()

                # 0x1F30 Temperature Measurement Features
                self.TEMPERATURE_MEASUREMENT = self.TemperatureMeasurementSubSystem()

            # end def __init__

            class DeviceInformationSubSystem(AbstractSubSystem):
                """
                Feature 0x0003

                Enable/Disable Firmware Info Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DEVICE_INFORMATION")

                    # Firmware Info feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False
                    self.F_Version_5 = False
                    self.F_Version_6 = False
                    self.F_Version_7 = False

                    # GetDeviceInfo response fields
                    ###############################
                    # The number of firmware and hardware entities
                    # in Application mode
                    self.F_EntityCount = 0x03
                    # in BootLoader mode
                    self.F_BootLoaderEntityCount = None
                    # List of four bytes random array that serves as per unit identifier
                    # It is a list so that there can be more than just one device under test
                    self.F_UnitId = ('00000000',)
                    # Support transport USB
                    # in Application mode
                    self.F_TransportUsb = False
                    # in BootLoader mode
                    self.F_BootLoaderTransportUsb = None
                    # Support transport eQuad
                    # in Application mode
                    self.F_TransportEQuad = False
                    # in BootLoader mode
                    self.F_BootLoaderTransportEQuad = None
                    # Support transport Bluetooth low energy
                    # in Application
                    self.F_TransportBTLE = False
                    # in Bootloader
                    self.F_BootLoaderTransportBTLE = None
                    # Support transport Bluetooth
                    # in Application
                    self.F_TransportBT = False
                    # in Bootloader
                    self.F_BootLoaderTransportBT = None
                    # Six bytes array model ID
                    # in Application mode
                    self.F_ModelId = '000000000000'
                    # in BootLoader mode
                    self.F_BootLoaderModelId = None
                    # One byte extended model ID
                    # in Application mode
                    self.F_ExtendedModelId = 0
                    # in BootLoader mode
                    self.F_BootLoaderExtendedModelId = None
                    # Serial number support flag
                    self.F_CapabilitiesSerialNumber = False

                    # GetFwInfo response constant fields
                    # All of them are lists for entity index
                    ###############################
                    # 1 byte entity type
                    # in Application mode
                    self.F_FwType = ('00',)
                    # in BootLoader mode
                    self.F_BootLoaderFwType = None
                    # 3 bytes string prefix, if empty ('') its byte value will be considered as 0x000000
                    # in Application mode
                    self.F_FwPrefix = ('XXX',)
                    # in BootLoader mode
                    self.F_BootLoaderFwPrefix = None
                    # 1 byte fw number in BCD format
                    # in Application mode
                    self.F_FwNumber = ('00',)
                    # in BootLoader mode
                    self.F_BootLoaderFwNumber = None
                    # 1 byte fw revision in BCD format
                    # in Application mode
                    self.F_Revision = ('00',)
                    # in BootLoader mode
                    self.F_BootLoaderRevision = None
                    # 2 bytes fw build in BCD format
                    # NB: Response check could be disabled during early development phase with 'None' keyword
                    # example: ('None', 'None', '0125')
                    # in Application mode
                    self.F_Build = ('0000',)
                    # in BootLoader mode
                    self.F_BootLoaderBuild = None
                    # 7 bits reserved (rest of the byte which includes 'active' as bit 0)
                    self.F_FwReserved = None
                    # 2 bytes transport ID. It is associated with the currently used transport
                    # in Application mode
                    self.F_TransportId = ('0000',)
                    self.F_TransportIdInUSB = None
                    # in BootLoader mode
                    self.F_BootLoaderTransportId = None
                    self.F_BootLoaderTransportIdInUSB = None
                    # 5 bytes Optional extra versioning information
                    # ExtraVersionInformation[0..3] provide the first four bytes of the commit SHA that was the HEAD of
                    # the git repo when the build was made. ExtraVersionInformation[4] indicates the build status.
                    # 0x00 means clean build and the other values mean that either there were modified files, or the
                    # build process was somehow altered, for instance by passing additional arguments to the tool-chain
                    # Bit 2 indicates that the firmware was built with the main debug flag set (since v3)
                    # Bit 1 indicates that the firmware was built with "CI_BUILD" flag (since v3)
                    # Bit 0 indicates that the build was dirty in any other way (since v3)
                    # Note: the F_ExtraVersionInformation can be generated from firmware build process.
                    # Then the settings here can keep default value None. Search "Create extraVer.json" in
                    # QUARK\NORMAN\HEAD\Jenkinsfile to copy jq command in your product Jenkinsfile
                    self.F_ExtraVersionInformation = None

                    # GetSerialNumber response constant fields
                    # List of 12 bytes array serial number in Base34 Alphanumeric scheme
                    # It is a list so that there can be more than just one device under test
                    self.F_SerialNumber = ('000000000000000000000000',)
                # end def __init__
            # end class DeviceInformationSubSystem

            class DeviceTypeAndNameSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x0005 (Device Type And Name) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DEVICE_TYPE_AND_NAME")

                    # DeviceTypeAndName feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False
                    self.F_Version_5 = False

                    # Device Marketing Name
                    # in Application mode - NB: shall be a str as it's called with endswith()
                    self.F_MarketingName = ''
                    # in BootLoader mode
                    self.F_BootLoaderMarketingName = None

                    # Device type (MOUSE, KEYBOARD, ...)
                    #     KEYBOARD        = 0
                    #     MOUSE           = 3
                    #     PRESENTER       = 6
                    self.F_DeviceType = 3
                # end def __init__
            # end class DeviceTypeAndNameSubSystem

            class DeviceFriendlyNameSubSystem(AbstractSubSystem):
                """
                Feature 0x0007

                Enable/Disable DeviceFriendlyName Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DEVICE_FRIENDLY_NAME")

                    # DeviceFriendlyName feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    self.F_NameMaxLength = 0x00
                # end def __init__
            # end class DeviceFriendlyNameSubSystem

            class KeepAliveSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x0008 (Keep Alive) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "KEEP_ALIVE")

                    # KeepAlive
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_TimeoutMax = None
                    self.F_TimeoutMin = None
                    self.F_ToleranceMs = None
                # end def __init__

            # end class KeepAliveSubSystem

            class PropertyAccessSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x0011 (Property Access) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "PROPERTY_ACCESS")

                    # PropertyAccess feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # List of supported properties
                    # A string name matching PropertyAccess.PropertyId or an int can be used
                    # Example: ('EXTENDED_MODEL_ID', '2')
                    self.F_SwAccessibleProperties = ()
                    # List of property sizes specific to the DUT
                    # It is a list of strings following the pattern :
                    # '<name as in PropertyAccess.PropertyId>:<size as an int>'
                    # Example: SpecificPropertiesSizes = ('EXTENDED_MODEL_ID:1',)
                    self.F_SwAccessiblePropertiesSizes = ()
                # end def __init__
            # end class PropertyAccessSubSystem

            class ConfigChangeSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x0020 (Config Change) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CONFIG_CHANGE")

                    # ConfigChange feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class ConfigChangeSubSystem

            class UniqueIdentifier32BytesSubSystem(AbstractSubSystem):
                """
                Feature 0x0021

                Enable/Disable UniqueIdentifier32Bytes SubSystem

                Random 32 Bytes Unique Identifier on the device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "UNIQUE_IDENTIFIER_32_BYTES")

                    # UNIQUE_IDENTIFIER_32_BYTES feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                # end def __init__
            # end class UniqueIdentifier32BytesSubSystem

            class DfuControlSubSystem(AbstractSubSystem):
                """
                Feature 0x00C2

                Enable/Disable DFU Control SubSystem

                Control DFU on a device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DFU_CONTROL")

                    # DFU Control feature
                    self.F_Enabled = False
                    self.F_NotAvailable = 1

                    # Version and parameters for 0x00C2
                    self.F_Version_0 = False
                    self.F_DfuControlParam = 0

                    # Read capabilities for 0xF0
                    self.F_F0ReadCapabilities = False
                # end def __init__
            # end class DfuControlSubSystem

            class SecureDfuControlSubSystem(AbstractSubSystem):
                """
                Feature 0x00C3 for device
                Register 0xF5 for receiver

                Secure DFU Control SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "SECURE_DFU_CONTROL")

                    # Secure DFU Control feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    self.F_DfuControlParam = 0
                    self.F_DfuControlTimeout = 0
                    self.F_DfuControlActionType = 0
                    self.F_DfuControlActionData = 0

                    # Action type in firmware to reload to test different values than the default one
                    # It is a tuple of str that represent int in base 10
                    # For example ('0', '1', '2', '3') with
                    # ACTION_TYPE_NONE -> 0
                    # ACTION_TYPE_OFF_ON -> 1
                    # ACTION_TYPE_OFF_ON_KEYBOARD -> 2
                    # ACTION_TYPE_OFF_ON_BUTTON -> 3
                    # ACTION_CONFIRMATION_ON_SCREEN -> 4
                    self.F_ReloadActionTypes = ()

                    # Flags to enable tests using reload action types:
                    #  * Enable OtherActionType to activate tests where a new firmware with an other action type than
                    #  the default one is reloaded in the device to check action types functionality. This should
                    #  typically be enabled on platforms, not on devices.
                    #  * Enable ChangeActionTypeByDFU to activate tests where the action type is changed by DFU to check
                    #  it can be changed by DFU. This should typically be enabled on platforms and on devices where the
                    #  default action type is none.
                    self.F_OtherActionType = False
                    self.F_ChangeActionTypeByDFU = False

                    # Cancel action supported by DUT
                    self.F_CancelDfuSupported = False
                # end def __init__
            # end class SecureDfuControlSubSystem

            class DfuSubSystem(AbstractSubSystem):
                """
                Feature 0x00D0

                Enable/Disable DFU SubSystem

                DFU on a device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DFU")

                    # DFU feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False

                    # The magic string used in the command 0x00D0 DfuStart
                    self.F_MagicString = ""
                    self.F_ImagesMagicString = ""

                    # List of the upgradable entities by entity type (gotten from command 0x0003 GetFwInfo)
                    self.F_UpgradableEntityTypes = None

                    # The error level can be 1, 2 or 3
                    self.F_ErrorLevel = 1

                    # Hex file name to program using jlink (the full name, should have the .hex extension)
                    self.F_HexFileName = ""
                    # DFU file name for the Application (the full name, should have the .dfu extension)
                    self.F_ApplicationDfuFileName = ""
                    # FW file name for the Bootloader (the full name, should have the .hex extension)
                    self.F_BootHexFileName = ""
                    # DFU file name for the Bootloader (the full name, should have the .dfu extension)
                    self.F_BootloaderDfuFileName = ""
                    # DFU file name for the SoftDevice (the full name, should have .dfu the extension)
                    self.F_SoftDeviceDfuFileName = ""
                    # DFU file name for the Lightning (the full name, should have the .dfu extension)
                    # There can be more than one lightning, for now there can be 2
                    self.F_LightningDfuFilesName = ("", "",)
                    # FW file name for the Embedded images (the full name, should have the .hex extension)
                    self.F_ImagesHexFileName = ""
                    # DFU file name for the Embedded images (the full name, should have the .dfu extension)
                    self.F_ImagesDfuFileName = ""

                    # The quantum program is the minimum number of bytes of program data to be writen in one go.
                    # This means that the program data length should be a multiple of this number.
                    # For example, on herzog the program data goes to the flash of the nrf52 and this flash is align on
                    # 4 bytes so it can write data by 4 bytes. Then QuantumProgram = 4.
                    self.F_QuantumProgram = 0
                    # The quantum check is the minimum number of bytes of check data to be writen in one go.
                    # This means that the check data length should be a multiple of this number.
                    # For example, on herzog the check data goes to the ram of the nrf52 and this ram is align on
                    # 1 byte so it can write data by 1 byte. Then QuantumCheck = 1.
                    self.F_QuantumCheck = 0

                    # Notify that the current DFU process in the bootloader perform a Flash Write Verify after each
                    # write.
                    # A Flash Write Verify is the action of reading the flash after a write to verify that it went well.
                    self.F_FlashWriteVerify = False
                    # Notify that the current DFU process in the bootloader perform a verification that the command 1
                    # and 2 have been done before trying the command 3.
                    self.F_VerifyCmd3DoneAfterCmd1And2 = False
                    # Notify that the current DFU process in the bootloader perform a verification of the flag in the
                    # command 0x00D0 DfuStart.
                    self.F_VerifyFlag = False
                    # Value of the current software flags to avoid using the wrong one in command 0x00D0 DfuStart.
                    self.F_DfuStartFlags = 0
                    # Value of the current software security level to avoid using the wrong one in command 0x00D0
                    # DfuStart.
                    self.F_DfuStartSecurLvl = 0

                    # Address in the NVS of the flag of the current firmware to verify, only if F_VerifyFlag is on
                    self.F_AddressForFlagInNvs = 0
                    # Value of an all set flag in the device NVS, for example in flash all bits to 0
                    self.F_FlagBitSetValueInNvs = 0
                    # Value of an all cleared flag in the device NVS, for example in flash all bits to 1
                    self.F_FlagBitClearedValueInNvs = 0

                    # The low bound of the address range for the application in the device memory.
                    self.F_LowestApplicationAddress = 0
                    # The high bound of the address range for the application in the device memory.
                    self.F_HighestApplicationAddress = 0
                    # Size of the buffer at the end of the application range used as a validity flag
                    # - 4 Bytes on the majority of our NRF52 projects
                    # - 0 Byte on projects supporting the 'DFU in place' feature
                    self.F_ApplicationValidityFlagSize = 4
                    # The 2 following parameters are initialized with Nordic NRF52 SoftDevice family values but could be
                    # overridden in test config to ensure forward compatibility
                    # The low bound of the upgradable soft device address range matching the end of the MBR sector.
                    self.F_LowestSoftDeviceAddress = 0x00001000
                    # The address in the soft device memory range where to extract the soft device size.
                    self.F_SoftDeviceSizeAddress = 0x00003008
                    # Notify that the current DFU process in the bootloader perform an additional authentication on
                    # the program data.
                    self.F_AdditionalAuthentication = False

                    # The device capabilities for the field encrypt in DfuStart command
                    # You can find the values in Dfu.EncryptionMode from pyhid.hidpp.features.common.dfu
                    self.F_EncryptCapabilities = ('1',)

                    # The target support the 'DFU in place' feature
                    self.F_DfuInPlace = False

                    # DFU signature algorithm
                    self.F_SignatureAlgorithm = 'RSA'

                    # List the firmware code tags with which the dfu shall be compatible with (up to 3 tags)
                    # For example ('RBM15_00_B0006') or ('RBM15_00_B0006', 'RBM15_00_B0008', 'RBM15_00_B0009')
                    self.F_CompatibleTags = ()
                    # List the action types associated to the above compatible tags, if some action types to enter in
                    # bootloader have change since a tag. Naming from GetDfuControlResponseV0.ACTION is used with a
                    # "action_" prefix, e.g "action_off_on" for off/on.
                    self.F_CompatibleTagsDfuControlActionType = ()

                    # Hex file name for the companion MCU
                    self.F_CompanionHexFileName = ""
                    # DFU file name for the companion MCU
                    self.F_CompanionDfuFileName = ""
                    # DFU with higher security level file name for the companion MCU
                    self.F_CompanionDfuFileNameNextSecurityLevel = ""
                    # The low bound of the address range for the companion MCU in the device memory.
                    self.F_CompanionLowestApplicationAddress = 0
                    # The high bound of the address range for the companion MCU in the device memory.
                    self.F_CompanionHighestApplicationAddress = 0

                    # When a signature is not valid, the signature verification algorithm must fail at the
                    # initialization, before the computation by the algorithm. To check this, we can check that the
                    # time to receive the DFU status is shorter in case of an invalid signature. This attribute
                    # defines the maximum time allowed to receive the DFU status in this case. It should be shorter
                    # than the normal time.
                    self.F_CheckValidateStatusFailAtInitTimeLimit = 0
                # end def __init__
            # end class DfuSubSystem

            class BatteryUnifiedLevelStatusSubSystem(AbstractSubSystem):
                """
                Feature 0x1000

                Enable/Disable Battery Unified Level Status SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BATTERY_UNIFIED_LEVEL_STATUS")

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # BATTERY feature
                    self.F_Enabled = False
                    self.F_AllBatteryDischargeLevels = None
                    self.F_NumberOfLevels = 0
                    self.F_Flags = 0
                    self.F_NominalBatteryLife = None
                    self.F_BatteryCriticalLevel = 0

                    # BATTERY level transition values
                    self.F_BatteryRangeByLevel = None
                # end def __init__
            # end class BatteryUnifiedLevelStatusSubSystem

            class UnifiedBatterySubSystem(AbstractSubSystem):
                """
                Feature 0x1004

                Enable/Disable Unified Battery SubSystem

                The unified battery status on a device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "UNIFIED_BATTERY")

                    # UNIFIED_BATTERY feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False
                    self.F_Version_5 = False

                    # Supported Levels: list of percentage (0 or 1).
                    # example:
                    # v0 -> (full, good, low, critical) so ('100', '-1', '-1', '10') means that full and critical are
                    # supported and not good and low.
                    self.F_SupportedLevels = ()
                    # Capabilities Flags:list of bool (0 or 1).
                    # example:
                    # v0 & v1 -> (rchgc, socc) so (1, 0) means that rchgc is supported and not socc.
                    # v2 -> (rchgc, socc, show) so (1, 0, 1) means that rchgc & show are supported and not socc.
                    # v3 -> (rchgc, socc, show, battSrcIdx) so (1, 0, 0, 1) means that rchgc & battSrcIdx are supported
                    #  and not socc nor show.
                    self.F_CapabilitiesFlags = ()
                    # The Battery source index identifies the battery used in case of battery multi-sourcing support.
                    # Return 0x00 if the battery source index is unknown.
                    self.F_BatterySourceIndex = 0
                    # Levels: list of mV values, should have the same size as (100 / StateOfChargeStep) + 1
                    # example for 10% step -> 11 values should be defined matching
                    # 100%, 90%, 80%, 70%, .... 10%, 0%
                    #  - Levels in mV when discharging
                    #
                    # Voltage selection from EE battery test report. Here are the guidelines to select the voltage:
                    #  - PWS: Select voltage for SoC = 95%, the available voltages could be from SoC = 99% to 95% in the
                    #         battery test report.
                    #  - Gaming: Select voltage for SoC = 90%, the available voltages could be from SoC = 95% to 85% in
                    #            the battery test report.
                    self.F_DischargeSOCmV = ()
                    #  - Levels in mV when charging
                    self.F_RechargeSOCmV = ()
                    # The value of the state of charge step in %
                    # Core device has 5% resolution
                    # Gaming device has 1% resolution but uses 10% instead. Because of 5mV variation.
                    self.F_StateOfChargeStep = 0
                    # Button CID to use to wakeup from deep sleep
                    self.F_DeepSleepWakeUpButtonCid = 0x00
                    # Enable or disable charging test
                    # Disable charging test for gaming keyboard because it is not supported.
                    self.F_EnableChargingTests = False
                # end def __init__
            # end class UnifiedBatterySubSystem

            class PasswordAuthenticationSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1602 (Password Authentication) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "PASSWORD_AUTHENTICATION")

                    # PasswordAuthentication feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    # Flags definition
                    # - bit 0 = Constant credentials
                    # - bit 1 = Full authentication
                    # - bit 2 = Long password
                    self.F_ConstantCredentials = False
                    self.F_FullAuthentication = False
                    self.F_SupportLongPassword = False
                # end def __init__
            # end class PasswordAuthenticationSubSystem

            class ManufacturingModeSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1801 (Manufacturing Mode) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MANUFACTURING_MODE")

                    # ManufacturingMode feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class ManufacturingModeSubSystem

            class DeviceResetSubSystem(AbstractSubSystem):
                """
                Feature 0x1802

                Enable/Disable Device Reset Enabler/Disabler SubSystem

                Forces a reset on the device which receives the command.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DEVICE_RESET")

                    # DeviceReset feature
                    self.F_Enabled = False

                    # Power mode timings (in second)
                    # [ Run, Walk, Sleep, DeepSleep]
                    self.F_PowerModeDelay = ('0', '1', '5', '900')
                # end def __init__
            # end class DeviceResetSubSystem

            class GpioAccessSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1803 (Gpio Access) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "GPIO_ACCESS")

                    # GpioAccess feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Number of Ports
                    self.F_NumberOfPorts = None

                    # GPIO Mask Input
                    self.F_GpioInputMask = ()

                    # GPIO Mask Output
                    self.F_GpioOutputMask = ()

                    # GPIO Unused Pin Mask
                    self.F_GpioUnusedMask = ()

                    # GPIO Forbidden Pin Mask
                    self.F_GpioForbiddenMask = ()

                    # GPIO Input Value
                    self.F_GpioInputValue = ()

                    # GPIO Output Value
                    self.F_GpioOutputValue = ()

                    # If the GPIO output register has read and write access
                    self.F_SupportReadGroupOut = True
                # end def __init__
            # end class GpioAccessSubSystem

            class OobStateSubSystem(AbstractSubSystem):
                """
                Define Feature 0x1805

                Enable/Disable Device OOB State SubSystem

                Forces a reset to OOB state on the device which receives the command.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "OOB_STATE")

                    # OOB State feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class OobStateSubSystem

            class ConfDevPropSubSystem(AbstractSubSystem):
                """
                Feature 0x1806

                Enable/Disable Configurable device properties SubSystem

                This feature sets in the device non volatile memory configurable attributes for a
                given model. This feature is only available when manufacturing mode is enabled.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CONFIGURABLE_DEVICE_PROPERTIES")

                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_6 = False
                    self.F_Version_7 = False
                    self.F_Version_8 = False

                    # Total size in bytes of the device name that can be stored in the device (Max 50 chars)
                    self.F_DeviceNameMaxCount = 0x32

                    self.F_SupportedPropertyIds = ()
                # end def __init__
            # end class ConfDevPropSubSystem

            class ConfigurePropertiesSubSystem(AbstractSubSystem):
                """
                Feature 0x1807

                Configurable Properties SubSystem
                This feature configures some properties of the device during production.
                It is meant to replace HID++ Feature 0x1806.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CONFIGURABLE_PROPERTIES")

                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False

                    # List of supported properties
                    # A string name matching ConfigurableProperties.PropertyId or an int can be used
                    # Example: ('EXTENDED_MODEL_ID', '2')
                    self.F_SupportedProperties = ()
                    # List of property sizes specific to the DUT
                    # It is a list of strings following the pattern :
                    # '<name as in ConfigurableProperties.PropertyId>:<size as an int>'
                    # Example: SpecificPropertiesSizes = ('EXTENDED_MODEL_ID:1',)
                    self.F_SpecificPropertiesSizes = ()

                    # Filter unstable test that caused by firmware. The flag is used for Cinderella_TKL test
                    # framework CI node only and will be removed after fixed the issue.
                    # https://jira.logitech.io/browse/CINDERELLA-214
                    # TODO : This is a workaround. Remove this filter as soon as the problem is understood and fixed
                    self.F_FilterUnstableTest = False
                # end def __init__
            # end class ConfigurePropertiesSubSystem

            class ConfigurableDeviceRegistersSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x180B (Configurable Device Registers) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CONFIGURABLE_DEVICE_REGISTERS")

                    # ConfigurableDeviceRegisters feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_Capabilities = None
                    self.F_VariableRegisterSize = ()
                    self.F_SupportedRegisters = ()
                    self.F_ConfigurableRegisters = ()
                # end def __init__
            # end class ConfigurableDeviceRegistersSubSystem

            class ChangeHostSubSystem(AbstractSubSystem):
                """
                Feature 0x1814

                Enable/Disable (Change Host) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CHANGE_HOST")

                    # ChangeHost feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    self.F_Flags = 0
                    self.F_TypeC = False
                # end def __init__
            # end class ChangeHostSubSystem

            class HostsInfo(AbstractSubSystem):
                """
                Feature 0x1815

                Enable/Disable Hosts Info SubSystem

                The Hosts Info feature allows managing host information on devices with multihost capabilities
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "HOSTS_INFO")

                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_1 = False
                    self.F_Version_2 = False

                    # Capability Mask
                    self.F_SupportSetOSVersion = False
                    self.F_SupportSetName = False
                    self.F_SupportGetName = False
                    self.F_SupportBLEDescriptor = False
                    self.F_SupportBTDescriptor = False
                    self.F_SupportUSBDescriptor = False

                    # Feature Info parameters
                    self.F_HostNameMaxLength = 0

                    # Host Info
                    # 4 - BLE.
                    # 5 - BLE Pro (Bolt)
                    self.F_HostBusType = 5
                # end def __init__
            # end class HostsInfo

            class BleProPrepairing(AbstractSubSystem):
                """
                Feature 0x1816

                Enable/Disable Ble Pro Pre-pairing SubSystem

                The BLE Pro prepairing feature exposes a set of command in order to set prepairing data useful for
                BLE Pro.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BLE_PRO_PREPAIRING")

                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Mandatory Key Set
                    # IrkOptional = False if setting IRK Keys is mandatory in device prepairing sequence (Default)
                    # IrkOptional = True if setting IRK Keys is not mandatory in device prepairing sequence
                    self.F_IrkOptional = False
                    # Supported Key Set
                    # Keys Bitmap
                    #   KEY_LTK = 0x01
                    #   KEY_LOCAL_ADDR = 0x02
                    #   KEY_LOCAL_IRK = 0x04
                    #   KEY_LOCAL_CSRK = 0x08
                    #   KEY_REMOTE_ADDR = 0x20
                    #   KEY_REMOTE_IRK = 0x40
                    #   KEY_REMOTE_CSRK = 0x80
                    self.F_KeysSupported = 0x67
                # end def __init__
            # end class BleProPrepairing

            class LightspeedPrepairingSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1817 (Lightspeed Prepairing) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "LIGHTSPEED_PREPAIRING")

                    # LightspeedPrepairing feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # equad attribute usage: 0 if hardcoded, 1 if configurable during prepairing procedure
                    self.F_UseAttr = 0
                    # Pre pairing slots availability
                    self.F_Ls2Slot = False
                    self.F_CrushSlot = False
                    self.F_LsSlot = False
                # end def __init__
            # end class LightspeedPrepairingSubSystem

            class PowerModesSubSystem(AbstractSubSystem):
                """
                Feature 0x1830

                Enable/Disable Power Modes Enabler/Disabler SubSystem

                Get and set the power mode of a device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "POWER_MODES")

                    # PowerModes feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Should be TOTAL_NUMBER_OF_POWER_MODES
                    self.F_TotalNumber = 0
                    # List of power modes number
                    self.F_NumberList = ''
                    # Current consumption threshold for DEEP_SLEEP (in uA)
                    self.F_CurrentThresholdDeepSleep = 0
                    # Current consumption threshold for DEAD_MODE (in uA)
                    self.F_CurrentThresholdDeadMode = 100
                # end def __init__
            # end class PowerModesSubSystem

            class BatteryLevelsCalibrationSubSystem(AbstractSubSystem):
                """
                Feature 0x1861

                Enable/Disable Battery Levels Calibration SubSystem

                Get and set the battery calibration of a device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BATTERY_LEVELS_CALIBRATION")

                    # PowerModes feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # The number of required calibration points
                    self.F_RequiredCalibrationPointNb = 0
                    # List of the required calibration points
                    self.F_RequiredCalibrationPoints = ()
                    # Coefficient of the ADC used to measure the battery, mV to ADC samples
                    self.F_AdcCoefficient = 0.0

                    # Comparator (if a comparator is used instead of an ADC to measure battery level)
                    self.F_Comparator = False
                    # Comparator reference voltage(e.g., Internal references 1.2, 1.8, 2.4V)
                    self.F_CompVRef = 0.0
                    # Comparator min threshold
                    self.F_CompMinThreshold = 0
                    # Comparator max threshold
                    self.F_CompMaxThreshold = 63
                # end def __init__
            # end class BatteryLevelsCalibrationSubSystem

            class OpticalSwitchesSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1876 (Optical Switches) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "OPTICAL_SWITCHES")

                    # OpticalSwitches feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    self.F_NbColumns = None
                    self.F_NbRows = None
                    self.F_TimeoutUs = None
                    # Optical switch array keyboard requires the available key mask table to understand which key is
                    # available or unavailable that can be ignored in firmware key operation. We shall configure the
                    # available key mask table for each supported key layouts, otherwise key layout related tests
                    # will get fail.
                    self.F_DefaultKeyLayout = 0
                    # Use the language name defined in pyraspi.services.keyboardmulator.KeyboardMixin.Layout
                    # EX: SupportedKeyLayout = ('ISO_104_KEY', 'JIS_109_KEY')
                    #     NbAvailableKeys = ('68', '6D')
                    #     ColumnMaskTable_0 = ('F18780000000003F', 'D18700000000003F')
                    self.F_SupportedKeyLayout = ()
                    self.F_NbAvailableKeys = ()
                    self.F_ColumnMaskTable_0 = ()
                    self.F_ColumnMaskTable_1 = ()
                    self.F_ColumnMaskTable_2 = ()
                    self.F_ColumnMaskTable_3 = ()
                    self.F_ColumnMaskTable_4 = ()
                    self.F_ColumnMaskTable_5 = ()
                    self.F_ColumnMaskTable_6 = ()
                    self.F_ColumnMaskTable_7 = ()
                    self.F_ColumnMaskTable_8 = ()
                    self.F_ColumnMaskTable_9 = ()
                    self.F_ColumnMaskTable_10 = ()
                    self.F_ColumnMaskTable_11 = ()
                    self.F_ColumnMaskTable_12 = ()
                    self.F_ColumnMaskTable_13 = ()
                    self.F_ColumnMaskTable_14 = ()
                    self.F_ColumnMaskTable_15 = ()
                # end def __init__
            # end class OpticalSwitchesSubSystem

            class RFTestSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1890 (RF Test) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "RF_TEST")

                    # RFTest feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False
                    self.F_Version_5 = False
                    self.F_Version_6 = False
                    self.F_Version_7 = False
                    self.F_Version_8 = False
                    self.F_Version_9 = False
                # end def __init__
            # end class RFTestSubSystem

            class LEDTestSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x18A1 (LED Test) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "LED_TEST")

                    # LEDTest feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_BacklightLED = 0
                    self.F_BatteryGreenLED = 0
                    self.F_BatteryRedLED = 0
                    self.F_CapsLockLED = 0
                    self.F_ProductSpecificLED0 = 0
                    self.F_ProductSpecificLED1 = 0
                    self.F_ProductSpecificLED2 = 0
                    self.F_ProductSpecificLED3 = 0
                    self.F_ProductSpecificLED4 = 0
                    self.F_ProductSpecificLED5 = 0
                    self.F_ProductSpecificLED6 = 0
                    self.F_ProductSpecificLED7 = 0
                    self.F_ProductSpecificLED8 = 0
                    self.F_ProductSpecificLED9 = 0
                    self.F_ProductSpecificLED10 = 0
                    self.F_ProductSpecificLED11 = 0
                    self.F_ProductSpecificLED12 = 0
                    self.F_ProductSpecificLED13 = 0
                    self.F_ProductSpecificLED14 = 0
                    self.F_ProductSpecificLED15 = 0
                    self.F_ProductSpecificLED16 = 0
                    self.F_ProductSpecificLED17 = 0
                    self.F_ProductSpecificLED18 = 0
                    self.F_ProductSpecificLED19 = 0
                    self.F_ProductSpecificLED20 = 0
                    self.F_ProductSpecificLED21 = 0
                    self.F_ProductSpecificLED22 = 0
                    self.F_ProductSpecificLED23 = 0
                    self.F_RGB = 0
                    self.F_RollerLED = 0
                # end def __init__
            # end class LEDTestSubSystem

            class StaticMonitorModeSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x18B0 (Monitor Mode) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "STATIC_MONITOR_MODE")

                    # StaticMonitorMode feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # StaticMonitorMode modes
                    self.F_KeyboardMode = False
                    self.F_Mice = False
                    self.F_EnhancedKeyboardMode = False
                    self.F_KeyboardWithLargerMatrixMode = False
                    self.F_EnhancedKeyboardWithLargerMatrixMode = False
                # end def __init__
            # end class StaticMonitorModeSubSystem

            class BacklightSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1982 (Backlight) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BACKLIGHT")

                    # Backlight feature
                    self.F_Enabled = False

                    # Supported Version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False

                    # Supported settings
                    self.F_BacklightEffect = None
                    self.F_BacklightEffectList = None
                    self.F_BacklightStatus = None
                    self.F_NumberOfLevel = None
                    self.F_SupportedOptions = '0000'
                    # The default backlight duration while proximity sensor didn't detect user hands
                    # The unit is 5sec per number. Duration = 5 x F_OobDurationHandsOut (sec)
                    self.F_OobDurationHandsOut = 1
                    # The default backlight duration while proximity sensor detected user hands
                    self.F_OobDurationHandsIn = 1
                    # The default backlight duration while plugged USB charging cable
                    self.F_OobDurationPowered = 1
                    # The default backlight duration while the device is not powered externally by an USB cable
                    self.F_OobDurationNotPowered = 0
                # end def __init__
            # end class BacklightSubSystem

            class ForceSensingButtonSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x19C0 (Force Sensing Button) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "FORCE_SENSING_BUTTON")

                    # ForceSensingButton feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    # customizable force (0: Not supported, 1: supported).
                    self.F_CustomizableForce = None
                    # Default force value to trigger the button.
                    self.F_DefaultForce = None
                    # Maximum force value to trigger the button.
                    self.F_MaxForce = None
                    # Minimum force value to trigger the button.
                    self.F_MinForce = None
                    # Number of buttons supported by the device.
                    self.F_NumberOfButtons = None
                # end def __init__
            # end class ForceSensingButtonSubSystem

            class SpecialKeysMSEButtonsSubSystem(AbstractSubSystem):
                """
                Feature 0x1B04

                Enable/Disable SpecialKeysMSEButtons Enabler/Disabler SubSystem

                Mechanism to access Keyboard reprogrammable Keys and Mouse buttons on a device
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "SPECIAL_KEYS_MSE_BUTTONS")

                    # SpecialKeysMSEButtons feature
                    self.F_Enabled = False

                    # CID count expected from GetCount function
                    self.F_CidCount = 0

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False
                    self.F_Version_5 = False
                    self.F_Version_6 = False

                    # For tests that need 3 or more Cid keys pressed simultaneously and no worry about Ghost key.
                    # Select at least 6 Cids and the selected Cid should support divert and analytics event.
                    self.F_CidListWithoutGhostKey = ()

                    # Expected CIDs information table
                    self.F_CidInfoTable = None

                    # resetAllCidReportSettings function. True: Supported, False: Not supported
                    self.F_SupportResetAllCidReportSettings = None

                    # CID Info Table
                    self.CID_INFO_TABLE = self.CidInfoTable()
                # end def __init__

                class CidInfoTable(AbstractSubSystem):
                    """
                    SpecialKeysMSEButtons CID Info Table SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "CID_INFO_TABLE")

                        self.F_Enabled = False

                        self.F_FriendlyName = ()
                        self.F_Cid = ()
                        self.F_Task = ()
                        self.F_FlagVirtual = ()
                        self.F_FlagPersist = ()
                        self.F_FlagDivert = ()
                        self.F_FlagReprog = ()
                        self.F_FlagFnTog = ()
                        self.F_FlagHotKey = ()
                        self.F_FlagFKey = ()
                        self.F_FlagMouse = ()
                        self.F_Pos = ()
                        self.F_Group = ()
                        self.F_GMask = ()
                        self.F_AdditionalFlagsRawWheel = ()
                        self.F_AdditionalFlagsAnalyticsKeyEvents = ()
                        self.F_AdditionalFlagsForceRawXY = ()
                        self.F_AdditionalFlagsRawXY = ()
                    # end def __init__
                # end class CidInfoTable
            # end class SpecialKeysMSEButtonsSubSystem

            class FullKeyCustomizationSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1B05 (Full Key Customization) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "FULL_KEY_CUSTOMIZATION")

                    # FullKeyCustomization feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_FkcConfigFileMaxsize = None
                    self.F_FkcConfigFileVer = None
                    self.F_FkcConfigMaxTriggers = None
                    self.F_SwConfigCapabilities = None
                    self.F_FkcEnabled = None
                    self.F_MacroDefFileMaxsize = None
                    self.F_MacroDefFileVer = None
                    self.F_PowerOnFkcEnable = None
                    self.F_ToggleKey0Cidx = ()
                    self.F_ToggleKey1Cidx = ()
                    self.F_ToggleKey2Cidx = ()
                    self.F_ToggleKey3Cidx = ()
                    self.F_ToggleKey4Cidx = ()
                    self.F_ToggleKey5Cidx = ()
                    self.F_ToggleKey6Cidx = ()
                    self.F_ToggleKey7Cidx = ()
                    self.F_ToggleKey0Enabled = True
                    self.F_ToggleKey1Enabled = False
                    self.F_ToggleKey2Enabled = False
                    self.F_ToggleKey3Enabled = False
                    self.F_ToggleKey4Enabled = False
                    self.F_ToggleKey5Enabled = False
                    self.F_ToggleKey6Enabled = False
                    self.F_ToggleKey7Enabled = False
                # end def __init__
            # end class FullKeyCustomizationSubSystem

            class AnalogKeysSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1B08 (Analog Keys) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ANALOG_KEYS")

                    # AnalogKeys feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    # Product capabilities read from 0x1b08.getCapabilities request
                    # https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x1b08_analog_keys_v0.adoc#getCapabilities
                    self.F_AnalogKeyConfigFileMaxsize = None
                    self.F_AnalogKeyConfigFileVer = None
                    self.F_AnalogKeyLevelResolution = None
                    # The OOB state of Rapid Trigger, it's read by 0x1b08.getRapidTriggerState
                    # https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x1b08_analog_keys_v0.adoc#getRapidTriggerState
                    self.F_RapidTriggerState = False

                    # The configurations of Base Profile, they shall be provided in either PRD, Firmware Spec or
                    # Product IXD requirement doc. e.g. :
                    # https://docs.google.com/presentation/d/1Kb_YNnCbtEPULrytotzNVt9CcR5R7Mqm36vb38OnUqU/view#slide=id.g2c897e71444_0_0
                    self.F_ActuationScalingRange = ()
                    self.F_SensitivityScalingRange = ()
                    self.F_DefaultActuationPoint = 0
                    self.F_DefaultSensitivity = 0
                # end def __init__
            # end class AnalogKeysSubSystem

            class ControlListSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1B10 (Control List) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CONTROL_LIST")

                    # ControlList feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_Count = None

                    # TODO - Remove these parameters once the roller layout settings are defined
                    # Flags indicating the device has the corresponding roller
                    # (NB: the CID is defined in the control ID list)
                    self.F_HasRoller_0 = False
                    self.F_HasRoller_1 = False
                # end def __init__
            # end class ControlListSubSystem

            class WirelessDeviceStatusSubSystem(AbstractSubSystem):
                """
                Feature 0x1D4B

                Enable/Disable WirelessDeviceStatus SubSystem

                Wireless status of the device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "WIRELESS_DEVICE_STATUS")

                    # WIRELESS_DEVICE_STATUS feature
                    self.F_Enabled = False
                # end def __init__
            # end class WirelessDeviceStatusSubSystem

            class EquadDJDebugInfoSubSystem(AbstractSubSystem):
                """
                Feature 0x1DF3

                Enable/Disable eQuad DJ Debug Info SubSystem

                Enable/disable debug on a device.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "EQUAD_DJ_DEBUG_INFO")

                    # EQUAD_DJ_DEBUG_INFO feature
                    self.F_Enabled = False
                # end def __init__
            # end class EquadDJDebugInfoSubSystem

            class EnableHiddenSubSystem(AbstractSubSystem):
                """
                Feature 0x1E00

                Enable/Disable EnableHidden SubSystem

                Enable the hidden features on the device which receives the command.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ENABLE_HIDDEN")

                    # EnableHidden feature
                    self.F_Enabled = False
                # end def __init__
            # end class EnableHiddenSubSystem

            class ManageDeactivatableFeaturesSubSystem(AbstractSubSystem):
                """
                Feature 0x1E01

                Enable/Disable Manage Deactivatable Features SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MANAGE_DEACTIVATABLE_FEATURES")

                    # ManageDeactivatableFeatures feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported counters
                    self.F_SupportManufacturingCounter = False
                    self.F_SupportComplianceCounter = False
                    self.F_SupportGothardCounter = False

                    # Maximum counters values
                    self.F_MaxManufacturingCounter = 0xFF
                    self.F_MaxComplianceCounter = 0xFF
                    self.F_MaxGothardCounter = 0xFF

                    # Authentication feature
                    self.F_AuthFeature = 0x0000
                # end def __init__
            # end class ManageDeactivatableFeaturesSubSystem

            class ManageDeactivatableFeaturesAuthSubSystem(AbstractSubSystem):
                """
                Feature 0x1E02

                Enable/Disable Manage Deactivatable Features based on authentication SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MANAGE_DEACTIVATABLE_FEATURES_AUTH")

                    # ManageDeactivatableFeatures feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Support info
                    self.F_SupportManufacturing = False
                    self.F_SupportCompliance = False
                    self.F_SupportGotthard = False

                    # Persistent activation info
                    self.F_PersistentActivationManufacturing = False
                    self.F_PersistentActivationCompliance = False
                    self.F_PersistentActivationGotthard = False

                    # Authentication feature
                    self.F_AuthFeature = 0x0000
                # end def __init__
            # end class ManageDeactivatableFeaturesAuthSubSystem

            class SPIDirectAccessSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1E22 (SPI Direct Access) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "SPI_DIRECT_ACCESS")

                    # SPIDirectAccess feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_NumberOfDevices = 0
                    self.F_DisableFwAccess = False
                    self.F_EnableAtomicCs = False

                    # Device supported SPI peripherals
                    # Accepted SPI peripherals can be referred in
                    # pytestbox.device.base.spidirectaccessutils.SPI_PERIPHERAL_REGISTER_DICT
                    # e.g. settings for SNAPPER: ('PLUTO', 'RAMBO_X')
                    self.F_SpiPeripherals = None
                # end def __init__
            # end class SPIDirectAccessSubSystem

            class I2CDirectAccessSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1E30 (I2C Direct Access) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "I2C_DIRECT_ACCESS")

                    # I2CDirectAccess feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_NumberOfDevices = None
                    self.F_DisableFwAccess = False

                    # Device supported I2C peripherals
                    # e.g. settings for YOKO TP: ('YOKO_TP',)
                    self.F_I2cPeripherals = None
                # end def __init__
            # end class I2CDirectAccessSubSystem

            class TdeAccessToNvmSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1EB0 (Tde Access To Nvm) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "TDE_ACCESS_TO_NVM")

                    # TdeAccessToNvm feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    # TDE Maximum Size
                    # Refer: X1EB0_TDE_DATA_LENGTH in c source file and set the value in product config.
                    self.F_TdeMaxSize = None
                    self.F_TdeStartingPosition = 0x00
                    self.F_TdeBufferSize = 0x0E
                # end def __init__
            # end class TdeAccessToNvmSubSystem

            class TemperatureMeasurementSubSystem(AbstractSubSystem):
                """
                Feature 0x1F30

                Enable/Disable Temperature Measurement Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "TEMPERATURE_MEASUREMENT")

                    # TemperatureMeasurement feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Number Of Sensors
                    self.F_SensorCount = 0
                # end def __init__
            # end class TemperatureMeasurementSubSystem

            class ForcePairingSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x1500 (Force Pairing) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "FORCE_PAIRING")

                    # ForcePairing feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Time before the led goes off in seconds
                    self.F_MaxWaitForLedOff = 10

                    # has immersive lighting
                    self.F_HasImmersiveLighting = False

                # end def __init__
            # end class ForcePairingSubSystem

        # end class CommonFeatureSubSystem

        class MouseSubSystem(AbstractSubSystem):
            """
            Mouse Enabler/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "MOUSE")

                # MOUSE feature
                self.F_Enabled = False

                # Mouse settings
                # Currently supported optical sensor: HERO, HERO2, ROBIN, TCOB, PAW3333, TOG6, PLUTO
                self.F_OpticalSensorName = None
                # The DPI min and max boundary defined by product
                self.F_DpiMinMax = ()
                # Flag indicating the mice support the lightspeed connection button
                # NB: The connected GPIO of RPi with connection button on mice shall be corresponding to BUTTON_16
                self.F_LsConnectionButton = False

                # 0x2100 Vertical Scrolling SubSystem
                self.VERTICAL_SCROLLING = self.VerticalScrollingSubSystem()

                # 0x2110 Smart Shift 3G/EPM wheel enhancement
                self.SMART_SHIFT = self.SmartShiftSubSystem()

                # 0x2111 Smart Shift 3G/EPM wheel with tunable torque
                self.SMART_SHIFT_TUNABLE = self.SmartShiftTunableSubSystem()

                # 0x2121 HiRes Wheel
                self.HI_RES_WHEEL = self.HiResWheelSubSystem()

                # 0x2130 Ratchet Wheel
                self.RATCHET_WHEEL = self.RatchetWheelSubSystem()

                # 0x2150 Thumbwheel
                self.THUMBWHEEL = self.ThumbwheelSubSystem()

                # 0x2201 Adjustable DPI SubSystem
                self.ADJUSTABLE_DPI = self.AdjDPISubSystem()

                # 0x2202 Extended Adjustable DPI SubSystem
                self.EXTENDED_ADJUSTABLE_DPI = self.ExtendedAdjustableDpiSubSystem()

                # 0x2250 AnalysisMode SubSystem
                self.ANALYSIS_MODE = self.AnalysisModeSubSystem()

                # 0x2251 Mouse Wheel Analytics
                self.MOUSE_WHEEL_ANALYTICS = self.MouseWheelAnalyticsSubSystem()
            # end def __init__

            class VerticalScrollingSubSystem(AbstractSubSystem):
                """
                Feature 0x2100

                VerticalScrolling Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "VERTICAL_SCROLLING")

                    # Vertical Scrolling feature
                    self.F_Enabled = False

                    # Roller Type
                    self.F_RollerType = None
                    # Num of ratchet by turn
                    # Typical values are:
                    # - 18 for mini rollers (mainly 3G mini wheel)
                    # - 24 for all 20mm wheels "big wheel"
                    # - 36 for uRatchet wheel on Gyro (18mm)
                    self.F_NumOfRatchetByTurn = 0x18
                    # Scroll lines: this is the desired default value for SW
                    # 0x00 means 'do not change system setting'
                    self.F_ScrollLines = 0
                # end def __init__
            # end class VerticalScrollingSubSystem

            class SmartShiftSubSystem(AbstractSubSystem):
                """
                Feature 0x2110

                SmartShift Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "SMART_SHIFT")

                    # SmartShift feature
                    self.F_Enabled = False

                    # Parameters
                    self.F_WheelMode = 2
                    self.F_AutoDisengage = 16
                    self.F_AutoDisengageDefault = 16
                # end def __init__
            # end class SmartShiftSubSystem

            class SmartShiftTunableSubSystem(AbstractSubSystem):
                """
                Feature 0x2111

                Smart Shift Tunable Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "SMART_SHIFT_TUNABLE")

                    # Smart Shift Tunable feature
                    self.F_Enabled = False

                    # Supported versions
                    self.F_Version_0 = False

                    # Parameters
                    self.F_TunableTorque = False
                    self.F_WheelModeDefault = 0x00
                    self.F_AutoDisengageDefault = 0x00
                    self.F_DefaultTunableTorque = 0x00
                    self.F_MaxForce = 0x00
                # end def __init__
            # end class SmartShiftTunableSubSystem

            class HiResWheelSubSystem(AbstractSubSystem):
                """
                Feature 0x2121
                HiRes Wheel Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "HI_RES_WHEEL")

                    # HiRes Wheel feature
                    self.F_Enabled = False
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Capability
                    self.F_Multiplier = 0
                    self.F_HasAnalyticsData = 0
                    self.F_HasSwitch = 0
                    self.F_HasInvert = 0
                    self.F_RatchetsPerRotation = 0
                    self.F_WheelDiameter = 0

                    # Herzog analytics Data
                    self.F_EpmChargingTime = 0
                # end def __init__
            # end class HiResWheelSubSystem

            class RatchetWheelSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x2130 (Ratchet Wheel) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "RATCHET_WHEEL")

                    # RatchetWheel feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class RatchetWheelSubSystem

            class ThumbwheelSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x2150 (Thumbwheel) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "THUMBWHEEL")

                    # Thumbwheel feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Thumbwheel Info
                    self.F_NativeRes = None
                    self.F_DivertedRes = None
                    self.F_SingleTapCapability = None
                    self.F_ProxyCapability = None
                    self.F_TouchCapability = None
                    self.F_TimeStampCapability = None
                    self.F_TimeUnit = None
                # end def __init__
            # end class ThumbwheelSubSystem

            class AdjDPISubSystem(AbstractSubSystem):
                """
                Feature 0x2201

                Adjustable DPI Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ADJUSTABLE_DPI")

                    # Adjustable DPI feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False

                    # The number of sensor entities
                    self.F_SensorCount = 0

                    # DPI Settings - List
                    self.F_DpiListReportList = False
                    self.F_DPI_1 = 0
                    self.F_DPI_2 = 0
                    self.F_DPI_3 = 0
                    self.F_DPI_4 = 0
                    self.F_DPI_5 = 0
                    self.F_DPI_6 = 0

                    # DPI Settings - Range
                    self.F_DpiListReportRange = False
                    self.F_DpiMin = 0
                    self.F_DpiMax = 0
                    self.F_DpiStep = 0

                    self.F_DpiDefault = 0

                    # Gaming mice provides the setting for user to select predefined DPI at each level.
                    # The number of DPI levels are up to the F_MaxSupportedDpiLevels.
                    # For example: F_PredefinedDpiValueList = ('800', '1200', '1600', '2400', '3200')
                    #              F_PredefinedDpiValueList = ('400', '800', '1600', '3200')
                    self.F_PredefinedDpiValueList = ()
                    self.F_MaxSupportedDpiLevels = 0
                # end def __init__
            # end class AdjDPISubSystem

            class ExtendedAdjustableDpiSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x2202 (Extended Adjustable Dpi) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "EXTENDED_ADJUSTABLE_DPI")

                    # ExtendedAdjustableDpi feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    self.F_NumSensor = 0
                    # ref:
                    # https://docs.google.com/spreadsheets/d/1fHES9fbcy3xw5zI63b_kUY7rx_kKyM8A-BhIR8U6qxQ/edit#gid=1361978000
                    self.F_NumDpiLevels = 0
                    self.F_ProfileSupported = False
                    self.F_CalibrationSupported = False
                    self.F_LodSupported = False
                    self.F_DpiYSupported = False
                    self.F_DpiRangesX = ()
                    self.F_DpiRangesY = ()
                    self.F_DpiListX = ()
                    self.F_DpiListY = ()
                    self.F_DpiLodList = ()
                    self.F_DefaultDpiX = 0
                    self.F_DefaultDpiY = 0
                    self.F_DefaultLod = 0
                    self.F_MouseWidth = 0  # mm
                    self.F_MouseLength = 0  # mm
                    self.F_CalibDpiX = 0
                    self.F_CalibDpiY = 0
                # end def __init__
            # end class ExtendedAdjustableDpiSubSystem

            class AnalysisModeSubSystem(AbstractSubSystem):
                """
                Feature 0x2250

                AnalysisMode Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ANALYSIS_MODE")

                    # AnalysisMode feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_OverflowCapability = False
                # end def __init__
            # end class AnalysisModeSubSystem

            class MouseWheelAnalyticsSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x2251 (Mouse Wheel Analytics) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MOUSE_WHEEL_ANALYTICS")

                    # MouseWheelAnalytics feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Capabilities
                    self.F_MainWheelCapability = False
                    self.F_MainWheelCountPerTurn = 0
                    self.F_RatchetFreeCapability = False
                    self.F_SmartShiftCapability = False
                    self.F_ThumbwheelCapability = False
                    self.F_ThumbwheelCountPerTurn = 0
                # end def __init__
            # end class MouseWheelAnalyticsSubSystem
        # end class MouseSubSystem

        class KeyboardSubSystem(AbstractSubSystem):
            """
            Keyboard Enabler/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "KEYBOARD")

                # Ghost Key detection capability
                self.F_GhostKeyDetection = False

                # Support Keyboard Ghost Keys, Key Code, Layout, Sholo related tests
                self.F_GhostKeys = True
                self.F_KeyCode = True
                self.F_Layout = True
                self.F_Sholo = True

                # Double press PP/NT support
                # ref:
                # https://docs.google.com/document/d/1Yebz9EikFP38I6lRIUav_JWwU4SgoWPzxfCzQGAj1SQ/edit#bookmark=id.c7ioidyhqlbh
                self.F_PlayPauseDoublePress = False

                # KEYBOARD feature
                self.F_Enabled = False

                # 0x3617 Direct Access Analog Keys
                self.DIRECT_ACCESS_ANALOG_KEYS = self.DirectAccessAnalogKeysSubSystem()

                # 0x40A3 Fn Inversion for Multi-Host Devices SubSystem
                self.FN_INVERSION_FOR_MULTI_HOST_DEVICES = self.FnInversionForMultiHostDevicesSubSystem()

                # 0x4220 Lock Key State
                self.LOCK_KEY_STATE = self.LockKeyStateSubSystem()

                # 0x4521 Disable Keys SubSystem
                self.DISABLE_KEYS = self.DisableKeysSubSystem()

                # 0x4522 Disable Keys By Usage SubSystem
                self.DISABLE_KEYS_BY_USAGE = self.DisableKeysByUsageSubSystem()

                # 0x4523 Disable Controls By CIDX
                self.DISABLE_CONTROLS_BY_CIDX = self.DisableControlsByCIDXSubSystem()

                # 0x4531 Multi Platform
                self.MULTI_PLATFORM = self.MultiPlatformSubSystem()

                # 0x4540 Keyboard International Layouts SubSystem
                self.KEYBOARD_INTERNATIONAL_LAYOUTS = self.KeyboardInternationalLayoutsSubSystem()

                # 0x4610 Multi Roller
                self.MULTI_ROLLER = self.MultiRollerSubSystem()
            # end def __init__

            class DirectAccessAnalogKeysSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x3617 (Direct Access Analog Keys) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DIRECT_ACCESS_ANALOG_KEYS")

                    # DirectAccessAnalogKeys feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_AnalogKeyNumber = None
                    self.F_AnalogResolution = None

                    # Analog modes
                    # Flag indicating two actuation points, assignments and events could be configured
                    self.F_MultiAction = False
                    # Flag indicating actuation point and hysteresis could be configured
                    self.F_NormalTrigger = False
                    # Flag indicating actuation point, sensitivity continuous mode could be configured
                    self.F_RapidTrigger = False
                # end def __init__
            # end class DirectAccessAnalogKeysSubSystem

            class FnInversionForMultiHostDevicesSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x40A3 (Fn Inversion for multi-host devices) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "FN_INVERSION_FOR_MULTI_HOST_DEVICES")
                    # FnInversionForMultiHostDevices feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # 0 = Fn Inversion Off, 1 = Fn Inversion On
                    self.F_FnInversionDefaultState = 0
                    # True = device has fn lock manual option capability
                    self.F_HasFnLock = False
                # end def __init__
            # end class FnInversionForMultiHostDevicesSubSystem

            class LockKeyStateSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x4220 (Lock Key State) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "LOCK_KEY_STATE")

                    # LockKeyState feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class LockKeyStateSubSystem

            class DisableKeysSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x4521 (DisableKeys) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DISABLE_KEYS")
                    # DisableKeys feature
                    self.F_Enabled = False
                    self.F_Version_0 = False

                    # Set True if the key have disableable capability, otherwise set False.
                    self.F_CapsLock = False
                    self.F_NumLock = False
                    self.F_ScrollLock = False
                    self.F_Insert = False
                    self.F_Windows = False

                    # Default disabled keys bitmap of the device
                    # i.e: CapsLock and ScrollLock are default disabled keys
                    # F_DefaultDisabledKeys = 5 (1*2^0 + 0*2^1 + 1*2^2 + 0*2^3 + 0*2^4)
                    self.F_DefaultDisabledKeys = 0
                # end def __init__
            # end class DisableKeysSubSystem

            class DisableKeysByUsageSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x4522 (DisableKeysByUsage) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DISABLE_KEYS_BY_USAGE")
                    # DisableKeysByUsage feature
                    self.F_Enabled = False
                    self.F_Version_0 = False
                    self.F_MaxDisabledUsages = 0x23
                    self.F_DefaultDisableKeys = ('KEYBOARD_MENU', 'KEYBOARD_LEFT_WIN_OR_OPTION')
                # end def __init__
            # end class DisableKeysByUsageSubSystem

            class DisableControlsByCIDXSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x4523 (Disable Controls By CIDX) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DISABLE_CONTROLS_BY_CIDX")

                    # DisableControlsByCIDX feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    # The following 6 parameters are boolean values
                    self.F_GameModeSupported = None
                    self.F_GameModeLockSupported = None
                    self.F_GameModeEnabled = None
                    self.F_GameModeLocked = None
                    self.F_PowerOnGameMode = None
                    self.F_PowerOnGameModeLock = None
                    self.F_PowerOnGameModeSupported = None
                    self.F_PowerOnGameModeLockSupported = None
                # end def __init__
            # end class DisableControlsByCIDXSubSystem

            class MultiPlatformSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x4531 (Multi Platform) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MULTI_PLATFORM")

                    # MultiPlatform feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_OsMask = ()
                    self.F_OsDetection = None
                    self.F_SetHostPlatform = None
                    # The size of following 5 settings are relied on the host number of the device supports
                    # i.e. if the device supports 2 hosts, the self.F_Status = ('1', '0')
                    self.F_Status = ('1', '0', '0')
                    self.F_PlatformIndex = ('0', '0', '0')
                    self.F_PlatformSource = ('0', '0', '0')
                    self.F_AutoPlatform = ('255', '255', '255')
                    self.F_AutoDescriptor = ('255', '255', '255')
                    # These fields are unused and ignored
                    self.F_FromRevision = ()
                    self.F_FromVersion = ()
                    self.F_ToRevision = ()
                    self.F_ToVersion = ()
                # end def __init__
            # end class MultiPlatformSubSystem

            class KeyboardInternationalLayoutsSubSystem(AbstractSubSystem):
                """
                Feature 0x4540

                KeyboardInternationalLayouts Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "KEYBOARD_INTERNATIONAL_LAYOUTS")

                    # KeyboardInternationalLayouts feature
                    self.F_Enabled = False
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Keyboard Layouts
                    #     US                            = 1
                    #     US International(105 Keys)    = 2
                    #     UK                            = 3
                    #     ...
                    self.F_KeyboardLayout = None
                # end def __init__
            # end class KeyboardInternationalLayoutsSubSystem

            class MultiRollerSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x4610 (Multi Roller) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MULTI_ROLLER")

                    # MultiRoller feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_NumRollers = None
                    # Fill the following information according to the capabilities of rollers
                    # e.g. F_IncrementsPerRatchet = ('120', '180')
                    # e.g. F_TimestampReport = ('1', '0') -> The first roller supports TimestampReport, the second not.
                    self.F_IncrementsPerRatchet = ()
                    self.F_IncrementsPerRotation = ()
                    self.F_LightbarId = ()
                    self.F_TimestampReport = ()
                # end def __init__
            # end class MultiRollerSubSystem
        # end class KeyboardSubSystem

        class TouchpadFeatureSubSystem(AbstractSubSystem):
            """
            Touchpad Features Enabler/Disabler Subsystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "TOUCHPAD")

                # Touchpad features
                self.F_Enabled = False

                # 0x6100 Touchpad Raw XY
                self.TOUCHPAD_RAW_XY = self.TouchpadRawXYSubSystem()
            # end def __init__

            class TouchpadRawXYSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x6100 (Touchpad Raw XY) SubSystem

                The Touchpad raw data feature describes the parameters and possible raw report formats of a touchpad.
                If the raw reporting is turned on, then any keyboard/mouse reporting is automatically turned off.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "TOUCHPAD_RAW_XY")
                    # TouchpadRawXY feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_XSize = None
                    self.F_YSize = None
                    self.F_ZDataRange = None
                    self.F_AreaDataRange = None
                    self.F_TimestampUnits = None
                    self.F_MaxFingerCount = None
                    self.F_Origin = None
                    self.F_PenSupport = None
                    self.F_RawReportMappingVersion = None
                    self.F_DPI = None
                    self.F_ReportBitmap = None
                    self.F_OneFingerClick = None
                    self.F_OneFingerTap = None
                    self.F_OneFingerMove = None
                    self.F_OneFingerClickHoldAndOtherFingersMoves = None
                    self.F_OneFingerClickHoldAndMove = None
                    self.F_OneFingerDoubleClick = None
                    self.F_OneFingerDoubleTap = None
                    self.F_TwoFingersTap = None
                    self.F_OneFingerDoubleTapNotReleaseThe2ndTap = None
                    self.F_OneFingerOnTheLeftCorner = None
                    self.F_OneFingerOnTheRightCorner = None
                    self.F_ThreeFingersTapAndDrag = None
                    self.F_TwoFingersSlideLeftRight = None
                    self.F_TwoFingersScrollUpDown = None
                    self.F_TwoFingersClick = None
                    self.F_ThreeFingersSwipe = None
                # end def __init__
            # end class TouchpadRawXYSubSystem
        # end class TouchpadFeatureSubSystem

        class GamingSubSystem(AbstractSubSystem):
            """
            Gaming Enabler/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "GAMING")

                # Gaming feature
                self.F_Enabled = False

                # 0x8030 MacroRecord key
                self.MACRORECORD_KEY = self.MacroRecordkeySubSystem()

                # 0x8040 Brightness Control
                self.BRIGHTNESS_CONTROL = self.BrightnessControlSubSystem()

                # 0x8051 Logi Modifiers
                self.LOGI_MODIFIERS = self.LogiModifiersSubSystem()

                # 0x8060 Report Rate
                self.REPORT_RATE = self.ReportRateSubSystem()

                # 0x8061 Extended Adjustable Report Rate
                self.EXTENDED_ADJUSTABLE_REPORT_RATE = self.ExtendedAdjustableReportRateSubSystem()

                # 0x8071 RGBEffects SubSystem
                self.RGB_EFFECTS = self.RGBEffectsSubSystem()

                # 0x8081 Per Key Lighting
                self.PER_KEY_LIGHTING = self.PerKeyLightingSubSystem()

                # 0x8090 Mode Status
                self.MODE_STATUS = self.ModeStatusSubSystem()

                # 0x80A4 Axis Response Curve
                self.AXIS_RESPONSE_CURVE = self.AxisResponseCurveSubSystem()

                # 0x80D0 Combined Pedals
                self.COMBINED_PEDALS = self.CombinedPedalsSubSystem()

                # 0x8100 Onboard Profiles
                self.ONBOARD_PROFILES = self.OnboardProfilesSubSystem()

                # 0x8101 Profile Management
                self.PROFILE_MANAGEMENT = self.ProfileManagementSubSystem()

                # 0x8110 MouseButtonSpy SubSystem
                self.MOUSE_BUTTON_SPY = self.MouseButtonSpySubSystem()

                # 0x8134 Brake Force
                self.BRAKE_FORCE = self.BrakeForceSubSystem()

                # 0x8135 Pedal Status
                self.PEDAL_STATUS = self.PedalStatusSubSystem()
            # end def __init__

            class MacroRecordkeySubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8030 (MacroRecord key) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MACRORECORD_KEY")

                    # MacroRecordkey feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class MacroRecordkeySubSystem

            class BrightnessControlSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8040 (Brightness Control) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BRIGHTNESS_CONTROL")

                    # BrightnessControl feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_MaxBrightness = 0
                    self.F_MinBrightness = 0
                    self.F_Steps = 0
                    self.F_PreDefineBrightnessLevels = ()
                    self.F_DefaultBrightness = 0
                    self.F_DefaultIlluminationState = 0
                    # Bit 0 -> 7
                    # v0 - [hw, events]
                    # v1 - [hw_brightness, events, illumination, hw_on_off, transient]
                    self.F_Capabilities = 0
                    # Setting for the device type is "Contextual Key" only
                    # unit - in seconds
                    self.F_DimmingOffTimeout = 0
                # end def __init__
            # end class BrightnessControlSubSystem

            class LogiModifiersSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8051 (Logi Modifiers) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "LOGI_MODIFIERS")

                    # LogiModifiers feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    # gettable modifiers
                    self.F_GM_LeftCtrl = False
                    self.F_GM_LeftShift = False
                    self.F_GM_LeftAlt = False
                    self.F_GM_LeftGui = False
                    self.F_GM_RightCtrl = False
                    self.F_GM_RightShift = False
                    self.F_GM_RightAlt = False
                    self.F_GM_RightGui = False
                    self.F_GM_Fn = False
                    self.F_GM_GShift = False
                    # force pressable modifiers
                    self.F_FM_Fn = False
                    self.F_FM_GShift = False
                # end def __init__

            # end class LogiModifiersSubSystem

            class ReportRateSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8060 (Report Rate) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "REPORT_RATE")

                    # ReportRate feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_ReportRateList = None
                # end def __init__
            # end class ReportRateSubSystem

            class ExtendedAdjustableReportRateSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8061 (Extended Adjustable Report Rate) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "EXTENDED_ADJUSTABLE_REPORT_RATE")

                    # ExtendedAdjustableReportRate feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported Report Rate List
                    # For example: F_SupportedReportRateList = ('0008', '0018', )
                    # 0x0008 means device supports 1KHz in Wired mode
                    # 0x0018 means device supports 2KHz and 1KHz in Gaming Wireless protocol mode
                    self.F_SupportedReportRateList = None
                    # Default Report Rate when connected via a wired protocol
                    self.F_DefaultReportRateWired = None
                    # Default Report Rate when connected via a wireless protocol
                    self.F_DefaultReportRateWireless = None
                # end def __init__
            # end class ExtendedAdjustableReportRateSubSystem

            class RGBEffectsSubSystem(AbstractSubSystem):
                """
                Feature 0x8071

                RGBEffects SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "RGB_EFFECTS")

                    self.F_Enabled = False
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False
                    self.F_Version_4 = False

                    # Info about device
                    self.F_RgbClusterCount = None
                    self.F_NvCapabilities = None
                    self.F_ExtCapabilities = None
                    self.F_NumberOfMultiClusterEffects = None  # since V2
                    self.F_HasEdgeLedDriver = None
                    self.F_TdeEdgeLedDriverAddress = None

                    self.ClusterInfoTable = self.ClusterInfoTableSubSystem()
                    self.EffectInfoTable = self.EffectInfoTableSubSystem()
                    self.NvCapabilityInfoTable = self.NvCapabilityInfoTableSubSystem()
                    self.RGBLedBinInfoTable = self.RGBLedBinInfoTableSubSystem()
                    self.CustomOnboardStoredEffectInfoTable = self.CustomOnboardStoredEffectInfoTableSubSystem()

                    # The number of custom effect slot count is from the sum of fw entity with type=8
                    self.F_CustomEffectSlotCount = None  # since V1

                    self.F_RgbNoActTimeoutToPSave = None
                    self.F_RgbNoActTimeoutToOff = None
                # end def __init__

                class ClusterInfoTableSubSystem(AbstractSubSystem):
                    """
                    ClusterInfoTable SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "CLUSTER_INFO_TABLE")

                        self.F_Enabled = False
                        self.F_ClusterIndex = ()
                        self.F_LocationEffect = ()
                        self.F_EffectsNumber = ()
                        self.F_DisplayPersistencyCapabilities = ()
                        self.F_EffectPersistencyCapabilities = ()
                        self.F_MultiLedPatternCapabilities = ()
                    # end def __init__
                # end class ClusterInfoTableSubSystem

                class EffectInfoTableSubSystem(AbstractSubSystem):
                    """
                    EffectInfoTable SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "EFFECT_INFO_TABLE")

                        self.F_Enabled = False
                        self.F_ClusterIndex = ()
                        self.F_EffectIndex = ()
                        self.F_EffectId = ()
                        self.F_EffectCapabilities = ()
                        self.F_EffectPeriod = ()
                    # end def __init__
                # end class EffectInfoTableSubSystem

                class NvCapabilityInfoTableSubSystem(AbstractSubSystem):
                    """
                    NvCapabilityInfoTable SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "NV_CAPABILITY_INFO_TABLE")

                        self.F_Enabled = False
                        self.F_NvCapabilities = ()
                        self.F_CapabilityState = ()
                        self.F_Param1 = ()
                        self.F_Param2 = ()
                        self.F_Param3 = ()
                        self.F_Param4 = ()
                        self.F_Param5 = ()
                        self.F_Param6 = ()
                    # end def __init__
                # end class NvCapabilityInfoTableSubSystem

                class RGBLedBinInfoTableSubSystem(AbstractSubSystem):
                    """
                    RGBLedBinInfoTable SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "RGB_LED_BIN_INFO_TABLE")

                        self.F_Enabled = False
                        # RGB LED Bin Info (Given by TDE)
                        self.F_BinValueBrightness = ()
                        self.F_BinValueColor = ()
                        self.F_CalibrationFactor = ()
                        self.F_Brightness = ()
                        self.F_ColorMetric_X = ()
                        self.F_ColorMetric_Y = ()
                    # end def __init__
                # end class RGBLedBinInfoTableSubSystem

                class CustomOnboardStoredEffectInfoTableSubSystem(AbstractSubSystem):
                    """
                    CustomOnboardStoredEffectInfoTable SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "CUSTOM_ON_BOARD_STORED_EFFECT_INFO_TABLE")

                        self.F_Enabled = False
                        # Test data: store a set of settings for a slot
                        self.F_SlotState = ()
                        self.F_Defaults = ()
                        self.F_UUID_0_10 = ()
                        self.F_UUID_11_16 = ()
                        self.F_EffectName_0_10 = ()
                        self.F_EffectName_11_21 = ()
                        self.F_EffectName_22_31 = ()
                    # end def __init__
                # end class CustomOnboardStoredEffectInfoTableSubSystem
            # end class RGBEffectsSubSystem

            class PerKeyLightingSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8081 (PerKey Lighting) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "PER_KEY_LIGHTING")

                    # PerKeyLighting feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False

                    self.ZONE_INFO_TABLE = self.ZoneInfoTable()
                # end def __init__

                class ZoneInfoTable(AbstractSubSystem):
                    """
                    Define the Supported Lighting Zones Info Table
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "ZONE_INFO_TABLE")

                        self.F_SupportedZoneParam = ()
                        self.F_ZonePresenceGroup0 = ()
                        self.F_ZonePresenceGroup1 = ()
                        self.F_ZonePresenceGroup2 = ()
                        self.F_ZonePresenceGroup3 = ()
                        self.F_ZonePresenceGroup4 = ()
                        self.F_ZonePresenceGroup5 = ()
                        self.F_ZonePresenceGroup6 = ()
                        self.F_ZonePresenceGroup7 = ()
                        self.F_ZonePresenceGroup8 = ()
                        self.F_ZonePresenceGroup9 = ()
                        self.F_ZonePresenceGroup10 = ()
                        self.F_ZonePresenceGroup11 = ()
                        self.F_ZonePresenceGroup12 = ()
                        self.F_ZonePresenceGroup13 = ()
                    # end def __init__
                # end class ZoneInfoTable
            # end class PerKeyLightingSubSystem

            class ModeStatusSubSystem(AbstractSubSystem):
                """
                Feature 0x8090

                ModeStatus Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MODE_STATUS")

                    # ModeStatus feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False
                    self.F_Version_2 = False
                    self.F_Version_3 = False

                    # Supported settings
                    self.F_ModeStatus0 = 0
                    self.F_ModeStatus1 = 0
                    self.F_ModeStatus0ChangedByHw = False
                    self.F_ModeStatus0ChangedBySw = False
                    self.F_PowerSaveModeSupported = False
                    self.F_NonGamingSurfaceModeSupported = False
                # end def __init__
            # end class ModeStatusSubSystem

            class OnboardProfilesSubSystem(AbstractSubSystem):
                """
                Feature 0x8100

                Onboard Profiles Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ONBOARD_PROFILES")

                    # OnboardProfiles feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_MemoryModelID = 1
                    self.F_ProfileFormatID = 0
                    self.F_MacroFormatID = 1
                    self.F_ProfileCount = 0
                    self.F_ProfileCountOOB = 1
                    self.F_ButtonCount = None
                    self.F_SectorCount = None
                    self.F_SectorSize = None
                    self.F_MechanicalLayout = None
                    self.F_VariousInfo = None
                    self.F_SectorCountRule = None
                    self.F_SupportedHostLayer = None
                    self.F_FieldsList = None
                    # Additional information be used for Profile Format v5
                    # If disabled multi-cluster,
                    #     main RGB zone = cluster_1_active_effect
                    #     2nd RGB zone = cluster_0_active_effect
                    # else
                    #     multi-cluster =  cluster_0_active_effect
                    self.F_Has2ndRgbZone = False
                    # Goal: override the default report rate for CI testing
                    # Set the following values in an onboard profile during test node setup
                    # (done by SetupTestCase._configure_report_rate method)
                    # NOTE: Normally, no need to set these values.
                    # If set, some tests may fail due to the expected default rate is changed.
                    self.F_ConfigureReportRateWireless = None
                    self.F_ConfigureReportRateWired = None

                    # OOB Profile Directory
                    self.OOB_PROFILE_DIRECTORY = self.OOBProfileDirectorySubSystem()
                    # OOB Profile
                    self.OOB_PROFILE = self.OOBProfileSubSystem()
                # end def __init__

                class OOBProfileDirectorySubSystem(AbstractSubSystem):
                    """
                    OOBProfileDirectory SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "OOB_PROFILE_DIRECTORY")

                        self.F_Enabled = False

                        # Support multiple profiles by tuple,
                        # - Index 0: Profile 1
                        #   ...
                        # - Index N: Profile N
                        #
                        # F_Status: Set 1 to enable profile
                        self.F_SectorId = ('0xFFFF',)
                        self.F_Status = ('0x00',)
                    # end def __init__
                # end class OOBProfileDirectorySubSystem

                class OOBProfileSubSystem(AbstractSubSystem):
                    """
                    OOBProfile SubSystem (Including fields in format V1 ~ V5)
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "OOB_PROFILES")

                        self.F_Enabled = False

                        # Support multiple profiles by tuple,
                        # - Index 0: Profile 1
                        #   ...
                        # - Index N: Profile N
                        self.F_ReportRate = ('0', '0', '0',)
                        self.F_ReportRateWireless = ('0', '0', '0',)
                        self.F_ReportRateWired = ('0', '0', '0',)
                        self.F_DefaultDpiIndex = ('0xFF', '0xFF', '0xFF',)
                        self.F_ShiftDpiIndex = ('0xFF', '0xFF', '0xFF',)
                        self.F_DPI_0 = ('0', '0', '0',)
                        self.F_DPI_1 = ('0', '0', '0',)
                        self.F_DPI_2 = ('0', '0', '0',)
                        self.F_DPI_3 = ('0', '0', '0',)
                        self.F_DPI_4 = ('0', '0', '0',)
                        self.F_DPI_X_0 = ('0', '0', '0',)
                        self.F_DPI_Y_0 = ('0', '0', '0',)
                        self.F_DPI_LOD_0 = ('0', '0', '0',)
                        self.F_DPI_X_1 = ('0', '0', '0',)
                        self.F_DPI_Y_1 = ('0', '0', '0',)
                        self.F_DPI_LOD_1 = ('0', '0', '0',)
                        self.F_DPI_X_2 = ('0', '0', '0',)
                        self.F_DPI_Y_2 = ('0', '0', '0',)
                        self.F_DPI_LOD_2 = ('0', '0', '0',)
                        self.F_DPI_X_3 = ('0', '0', '0',)
                        self.F_DPI_Y_3 = ('0', '0', '0',)
                        self.F_DPI_LOD_3 = ('0', '0', '0',)
                        self.F_DPI_X_4 = ('0', '0', '0',)
                        self.F_DPI_Y_4 = ('0', '0', '0',)
                        self.F_DPI_LOD_4 = ('0', '0', '0',)
                        self.F_DpiDeltaX = ('0', '0', '0',)
                        self.F_DpiDeltaY = ('0', '0', '0',)
                        self.F_LedColorRed = ('0xFF', '0xFF', '0xFF',)
                        self.F_LedColorGreen = ('0xFF', '0xFF', '0xFF',)
                        self.F_LedColorBlue = ('0xFF', '0xFF', '0xFF',)
                        self.F_PowerMode = ('0xFF', '0xFF', '0xFF',)
                        self.F_AngleSnapping = ('0', '0', '0',)
                        self.F_WriteCounter = ('0xFFFF', '0xFFFF', '0xFFFF',)
                        self.F_PowerSaveTimeout_S = ('0', '0', '0',)
                        self.F_PowerOffTimeout_S = ('0', '0', '0',)
                        self.F_Button_0 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_1 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_2 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_3 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_4 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_5 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_6 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_7 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_8 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_9 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_10 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_11 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_12 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_13 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_14 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_Button_15 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_0 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_1 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_2 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_3 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_4 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_5 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_6 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_7 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_8 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_9 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_10 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_11 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_12 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_13 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_14 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_GShiftButton_15 = ('0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF', '0xFF 0xFF 0xFF 0xFF',)
                        self.F_ProfileName = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF '
                                              '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_LogoEffect = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_SideEffect = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_LogoActiveEffect = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                   '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                   '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_SideActiveEffect = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                   '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                   '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_LogoPassiveEffect = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                    '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                    '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_SidePassiveEffect = ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                    '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                                                    '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF')
                        self.F_Cluster_0_ActiveEffect = \
                            ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF')
                        self.F_Cluster_1_ActiveEffect = \
                            ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF')
                        self.F_Cluster_0_PassiveEffect = \
                            ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF')
                        self.F_Cluster_1_PassiveEffect = \
                            ('0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',
                             '0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF 0xFF',)
                        self.F_LightningFlag = ('0xFF', '0xFF', '0xFF',)
                        self.F_CRC = ('0xFFFF', '0xFFFF', '0xFFFF',)
                    # end def __init__
                # end class OOBProfileSubSystem
            # end class OnboardProfilesSubSystem

            class ProfileManagementSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x8101 (Profile Management) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "PROFILE_MANAGEMENT")

                    # ProfileManagement feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_FileSystemVersion = None
                    self.F_ProfileTagVersion = None
                    self.F_MaxSectorSize = None
                    self.F_RamBufferSize = None
                    self.F_MaxSectorId = None
                    self.F_MaxFileId = None
                    self.F_MaxDirectorySectorId = None
                    self.F_TotalFlashSizeKb = None
                    self.F_FlashEraseCounter = None
                    self.F_FlashLifeExpect = None
                    self.F_NumOnboardProfiles = 0
                    self.F_EditBufferCapabilities = None
                    self.F_TagList = ()

                    # OOB Profile Directory
                    self.OOB_PROFILE_DIRECTORY = self.OOBProfileDirectorySubSystem()
                    # OOB Profile
                    self.OOB_PROFILE = self.OOBProfileSubSystem()
                # end def __init__

                class OOBProfileDirectorySubSystem(AbstractSubSystem):
                    """
                    OOBProfileDirectory SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "OOB_PROFILE_DIRECTORY")

                        self.F_Enabled = False

                        # Supported settings
                        self.F_FileId = ()
                        self.F_FeatureId = ()
                        self.F_FileTypeId = ()
                        self.F_Length = ()
                        self.F_Crc32 = ()
                        self.F_SectorId_Lsb = ()
                    # end def __init__
                # end class OOBProfileDirectorySubSystem

                class OOBProfileSubSystem(AbstractSubSystem):
                    """
                    OOBProfile SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "OOB_PROFILES")

                        self.F_Enabled = False

                        # Supported settings
                        # Find the expected settings from product PRD document.
                        self.F_ProfileIdentifier = ()
                        self.F_ProfileVersion = ()
                        self.F_ProfileName = ()
                        self.F_LightningFlag = ()
                        self.F_ActiveCluster0Effect = ()
                        self.F_ActiveCluster1Effect = ()
                        self.F_PassiveCluster0Effect = ()
                        self.F_PassiveCluster1Effect = ()
                        self.F_PSTimeout = ()
                        self.F_POTimeout = ()
                        self.F_X4523CidxBitmap = ()
                        # Detail for analog generic setting
                        # https://docs.google.com/spreadsheets/d/1A5ulSaInsIXFLJy8QHn8mbt_ovU9mIrnIxE8Gja8OHQ/view?gid=1479623692#gid=1479623692
                        self.F_AnalogGenericSetting = ()
                    # end def __init__
                # end class OOBProfileSubSystem
            # end class ProfileManagementSubSystem

            class AxisResponseCurveSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x80A4 (Axis Response Curve) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "AXIS_RESPONSE_CURVE")

                    # AxisResponseCurve feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported settings
                    self.F_AxisCount = None
                    self.F_AxisResolution = None
                    self.F_CalculatedValue = None
                    self.F_HidUsage = ()
                    self.F_HidUsagePage = None
                    self.F_MaxGetPointCount = None
                    self.F_MaxPointCount = None
                    self.F_MaxSetPointCount = None
                    self.F_Capabilities = None
                    self.F_PointCount = ()
                    self.F_PointIndex = None
                    self.F_Properties = None
                    self.F_ActivePointCount = None
                    self.F_Status = None
                # end def __init__
            # end class AxisResponseCurveSubSystem

            class CombinedPedalsSubSystem(AbstractSubSystem):
                """
                Feature 0x80D0

                CombinedPedals Enabler/Disabler SubSystem
                """
                def __init__(self):
                    AbstractSubSystem.__init__(self, "COMBINED_PEDALS")

                    # CombinedPedals feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                # end def __init__
            # end class CombinedPedalsSubSystem

            class MouseButtonSpySubSystem(AbstractSubSystem):
                """
                Feature 0x8110

                Enable/Disable MouseButtonSpy SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MOUSE_BUTTON_SPY")

                    self.F_Enabled = False
                    self.F_Version_0 = False
                    self.F_NbButtons = 0
                # end def __init__
            # end class MouseButtonSpySubSystem

            class BrakeForceSubSystem(AbstractSubSystem):
                """
                Feature 0x8134

                Enable/Disable BrakeForce Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BRAKE_FORCE")

                    # BrakeForce feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_MaximumKgLoad = None
                # end def __init__
            # end class BrakeForceSubSystem

            class PedalStatusSubSystem(AbstractSubSystem):
                """
                Feature 0x8135

                Enable/Disable Pedal Status Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "PEDAL_STATUS")

                    # PedalStatus feature
                    self.F_Enabled = False
                    # Supported version
                    self.F_Version_0 = False

                    # Total Pedals Count
                    # Refer: NB_OF_PEDALS in c source file and set the value in product config.
                    self.F_TotalPedalsCount = 0
                    self.F_PortType = ()
                    self.F_PortStatus = ()
                # end def __init__
            # end class PedalStatusSubSystem
        # end class GamingSubSystem

        class PeripheralTestFeatureSubSystem(AbstractSubSystem):
            """
            Peripheral Test Features Enabler/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "PERIPHERAL")

                # Peripheral Test features
                self.F_Enabled = False

                # 0x9001 PMW3816 and PMW3826
                self.PMW3816_AND_PMW3826 = self.PMW3816andPMW3826SubSystem()

                # 0x9205 MLX903xx
                self.MLX903XX = self.MLX903xxSubSystem()

                # 0x9209: MLX 90393 MultiSensor
                self.MLX_90393_MULTI_SENSOR = self.MLX90393MultiSensorSubSystem()

                # 0x9215 ADS 1231
                self.ADS_1231 = self.Ads1231SubSystem()

                # 0x92E2 Test Keys Display
                self.TEST_KEYS_DISPLAY = self.TestKeysDisplaySubSystem()
            # end def __init__

            class PMW3816andPMW3826SubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x9001 (PMW3816 and PMW3826) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "PMW3816_AND_PMW3826")

                    # PMW3816andPMW3826 feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Version_1 = False

                    # Supported register addresses
                    self.F_ReadOnlyRegisters = ()
                    self.F_ReadAndWriteRegisters = ()
                    self.F_WriteOnlyRegisters = ()

                    # Max register addresses
                    self.F_MaxRegisterAddress = None

                    # Strap data
                    self.F_StrapData = 0
                # end def __init__
            # end class PMW3816andPMW3826SubSystem

            class MLX903xxSubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x9205 (MLX903xx) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MLX903XX")

                    # MLX903xx feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported register addresses
                    self.F_CustomerAreaUsedRegisters = ()
                    self.F_CustomerAreaFreeRegisters = ()
                    self.F_MelexisAreaRegisters = ()
                    self.F_EpmIqs624Registers = ()
                # end def __init__
            # end class MLX903xxSubSystem

            class MLX90393MultiSensorSubSystem(AbstractSubSystem):
                """
                Feature 0x9209

                MLX 90393 Multi Sensor SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "MLX_90393_MULTI_SENSOR")

                    self.F_Enabled = False
                    # Supported version
                    self.F_Version_0 = False
                    self.F_SensorCount = 0
                    self.F_RegisterCount = 0
                    self.F_DefaultRegisterValue = ()
                    self.F_CalibrationData = ()
                    self.F_Parameters = ()
                    self.F_MonitorTestCount = None
                    self.F_MonitorTestThreshold = None
                # end def __init__
            # end class MLX90393MultiSensorSubSystem

            class Ads1231SubSystem(AbstractSubSystem):
                """
                Feature 0x9215

                Ads 1231 Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ADS_1231")

                    # Ads1231 feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Supported settings
                    self.F_SupportManageDynamicCalibrationParameters = False
                # end def __init__
            # end class Ads1231SubSystem

            class TestKeysDisplaySubSystem(AbstractSubSystem):
                """
                Enable/Disable Feature 0x92E2 (Test Keys Display) SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "TEST_KEYS_DISPLAY")

                    # TestKeysDisplay feature
                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False
                    self.F_Capabilities = 0
                    self.F_RowCount = None
                    self.F_ColumnCount = None
                    self.F_IconCount = None
                # end def __init__
            # end class TestKeysDisplaySubSystem
        # end class PeripheralTestFeatureSubSystem

        class VariableLengthProtocolSubSystem(AbstractSubSystem):
            """
            VLP Features Enabler/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "VLP")

                # # VLP feature
                # enabler
                self.F_Enabled = False
                # VLP Extended support
                self.F_Extended = False
                # Multi-Packet support
                self.F_MultiPacket = False
                # Transfer Buffer size for VLP protocol
                self.F_TransferBufferSize = 0
                # User Action returns HID/HID++ packet - Default is HID
                self.F_UserActionHIDPP = False

                # Switching of report type within the same multi-packet transfer support
                self.F_MultiPacketMultiReportTypes = False

                # VLP Important Features
                self.IMPORTANT = self.ImportantFeatureSubSystem()

                # VLP Common Features
                self.COMMON = self.CommonFeatureSubSystem()
            # end def __init__

            class ImportantFeatureSubSystem(AbstractSubSystem):
                """
                Important Features Enabler/Disabler Subsystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "IMPORTANT")

                    # enabler
                    self.F_Enabled = False

                    # 0x0102 VLP Root
                    self.ROOT = self.RootSubSystem()

                    # 0x0103 VLP Feature Set
                    self.FEATURE_SET = self.FeatureSetSubSystem()
                # end def __init__

                class RootSubSystem(AbstractSubSystem):
                    """
                    Feature 0x0102

                    Enable/Disable VLP Root Enabler/Disabler SubSystem
                    """
                    def __init__(self):
                        AbstractSubSystem.__init__(self, "ROOT")

                        # enabler
                        self.F_Enabled = False

                        # Supported version
                        self.F_Version_0 = False

                        # The protocol number is a field that hints the host software if it should support the device.
                        self.F_ProtocolNumMajor = HexList('00')
                        self.F_ProtocolNumMinor = HexList('00')

                        # Total Available memory for the device
                        self.F_FeatureMaxMemory = None

                        # Total Available memory for the device
                        self.F_TotalMemory = None
                    # end def __init__
                # end class RootSubSystem

                class FeatureSetSubSystem(AbstractSubSystem):
                    """
                    Enable/Disable Feature 0x0103 (VLP Feature Set) SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "FEATURE_SET")

                        # VLPFeatureSet feature
                        self.F_Enabled = False

                        # Supported version
                        self.F_Version_0 = False

                        self.F_FeatureCount = 0
                        self.F_FeatureRecordSize = 0
                        self.F_FeatureMaxMemory = 0
                    # end def __init__
                # end class FeatureSetSubSystem
            # end class ImportantFeatureSubSystem

            class CommonFeatureSubSystem(AbstractSubSystem):
                """
                Common Features Enabler/Disabler Subsystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "COMMON")

                    # enabler
                    self.F_Enabled = False

                    # 0x19A1 Contextual Display
                    self.CONTEXTUAL_DISPLAY = self.ContextualDisplaySubSystem()
                # end def __init__

                class ContextualDisplaySubSystem(AbstractSubSystem):
                    """
                    Enable/Disable Feature 0x19A1 (Contextual Display) SubSystem
                    """

                    def __init__(self):
                        AbstractSubSystem.__init__(self, "CONTEXTUAL_DISPLAY")

                        # ContextualDisplay feature
                        self.F_Enabled = False

                        # Supported version
                        self.F_Version_0 = False
                        self.F_Version_1 = False

                        # Total number of screens supported
                        self.F_DeviceScreenCount = 0
                        self.F_MaxImageSize = 0
                        self.F_MaxImageFPS = 0
                        self.F_ButtonCount = 0

                        # Capabilities Flag - order: deferrableDisplayUpdates, RGB565, RGB888, JPEG, calibrated, origin
                        self.F_CapabilitiesFlags = ('0', '0', '0', '0', '0', '0')

                        self.F_SupportedDeviceStates = ()
                        self.F_SetDeviceStates = ()
                        self.F_DefaultDeviceState = None
                        self.F_FeatureMaxMemory = None

                        # Display Info Table
                        self.DISPLAY_INFO_TABLE = self.DisplayInfoTable()
                        # Display Info Table
                        self.BUTTON_TABLE = self.ButtonTable()
                        # Display Info Table
                        self.VISIBLE_AREA_TABLE = self.VisibleAreaTable()
                    # end def __init__

                    class DisplayInfoTable(AbstractSubSystem):
                        """
                        Contextual Display Info Table SubSystem
                        """

                        def __init__(self):
                            AbstractSubSystem.__init__(self, "DISPLAY_INFO_TABLE")

                            self.F_Enabled = False

                            self.F_DisplayIndex = ()
                            self.F_DisplayShape = ()
                            self.F_DisplayDimension = ()
                            self.F_HorizontalRes = ()
                            self.F_VerticalRes = ()
                            self.F_ButtonCount = ()
                            self.F_VisibleAreaCount = ()
                        # end def __init__
                    # end class DisplayInfoTable

                    class ButtonTable(AbstractSubSystem):
                        """
                        Contextual Display Info Table SubSystem
                        """

                        def __init__(self):
                            AbstractSubSystem.__init__(self, "BUTTON_TABLE")

                            self.F_Enabled = False

                            self.F_ButtonIndex = ()
                            self.F_ButtonShape = ()
                            self.F_ButtonLocationX = ()
                            self.F_ButtonLocationY = ()
                            self.F_ButtonLocationWidth = ()
                            self.F_ButtonLocationHeight = ()
                        # end def __init__
                    # end class ButtonTable

                    class VisibleAreaTable(AbstractSubSystem):
                        """
                        Contextual Display Info Table SubSystem
                        """

                        def __init__(self):
                            AbstractSubSystem.__init__(self, "VISIBLE_AREA_TABLE")

                            self.F_Enabled = False

                            self.F_VisibleAreaIndex = ()
                            self.F_VisibleAreaShape = ()
                            self.F_VisibleAreaLocationX = ()
                            self.F_VisibleAreaLocationY = ()
                            self.F_VisibleAreaLocationWidth = ()
                            self.F_VisibleAreaLocationHeight = ()
                        # end def __init__
                    # end class VisibleAreaTable
                # end class ContextualDisplaySubSystem
            # end class CommonFeatureSubSystem
        # end class VariableLengthProtocolSubSystem
    # end class FeaturesSubSystem

    class DeviceSubSystem(AbstractSubSystem):
        """
        Device attributes SubSystem
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "DEVICE")

            self.F_Enabled = False

            self.F_MaxWaitSleep = 0
            self.F_MaxWaitDeepSleep = 0

            # The possible values are 'None', 'membrane', 'mechanical' and 'optical_switch_array'.
            self.F_KeyboardType = None
            self.F_Is60PercentKeyboard = False
            # The possible values are 'None', 'mechanical' and 'hybrid'.
            self.F_MouseSwitchType = None

            # The possible values are 'game_mode_slider' or 'game_mode_button'
            self.F_GameModeButtonType = None

            self.F_NbHosts = 0

            # DUT Reset Strategy (refer to values in DeviceBaseTestUtils.ResetHelper.ResetStrategy)
            # The possible values are: None, 'power_slider', 'power_supply', 'usb_hub', 'debugger'
            self.F_ResetStrategy = None

            # Minimum MCU operating voltage (VDD)
            self.F_MCUMinOperatingVoltage = None

            # Battery settings
            self.BATTERY = self.BatterySubSystem()

            # Device Connection scheme
            self.CONNECTION_SCHEME = self.ConnectionScheme()

            # Fn Lock
            self.FN_LOCK = self.FnLockSubSystem()

            # EVT Tests
            self.EVT_AUTOMATION = self.EVTAutomationSubSystem()
        # end def __init__

        class BatterySubSystem(AbstractSubSystem):
            """
            Battery Enabler/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "BATTERY")

                # Maximum battery value (spec dependant)
                self.F_MaximumVoltage = 1.6
                # Nominal battery value (spec dependant)
                self.F_NominalVoltage = 1.3
                # Cutoff battery value (spec dependant)
                self.F_CutOffVoltage = 0.9
                # Charge by USB charging cable
                self.F_USBCharging = False
                # Charge by Wireless charging module/emulator
                self.F_WirelessCharging = False
                # The Artanis (Gaming mouse) charging IC requires to turn off the power output while USB charging
                self.F_TurnOffPowerOutputWhileUSBCharging = False

                # Timing during which the battery measurement are suspended after a change notification
                # - Unified battery implementation: 16 seconds
                # - Battery Unified Level Status implementation: 30 seconds
                self.F_BatteryMeasureBlindWindow = 16
            # end def __init__
        # end class BatterySubSystem

        class ConnectionScheme(AbstractSubSystem):
            """
            Connection Scheme SubSystem
            """
            def __init__(self):
                AbstractSubSystem.__init__(self, "CONNECTION_SCHEME")

                self.F_Enabled = True

                # Multiple Connection Channels
                # - False: Mono Channel (CH1)
                # - True: Multiple Channels (CH1, CH2 & CH3)
                self.F_MultipleChannels = False
                # Multiple EasySwitch Buttons
                # - False: Connect Button
                # - True: EasySwitch CH1, EasySwitch CH2 & EasySwitch CH3
                self.F_MultipleEasySwitchButtons = False

                # Device BLE Pro connection scheme
                self.BLE_PRO_CONNECTION_SCHEME = self.BleProConnectionScheme()

                # Device LS2 connection scheme
                self.LS2_CONNECTION_SCHEME = self.Ls2ConnectionScheme()

                # Device Recovery
                self.DEVICE_RECOVERY = self.DeviceRecoverySubSystem()
            # end def __init__

            class BleProConnectionScheme(AbstractSubSystem):
                """
                Ble Pro Connection Scheme SubSystem

                The BLE Pro Connection Scheme feature groups the BLE Pro connectivity and the Safe pre-paired receiver
                specifications.
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "BLE_PRO_CS")

                    self.F_Enabled = False

                    # Supported version
                    self.F_Version_0 = False

                    # Safe pre-paired receiver
                    self.F_SafePrePairedReceiver = False

                    # BLE Service Change Support
                    # https://app.lucidchart.com/documents/edit/4ec2b55b-188c-4473-b6ec-2cb9ed9513ee/eyl1Z~CmRrKD
                    # #?folder_id=home&browser=list
                    self.F_BLEServiceChangeSupport = False

                    # Enable connectivity LEDs functional behavior verification
                    # on BLE Pro/BLE device (Single-Host or Multi-Host)
                    self.F_ConnectivityLEDsCheck = True
                # end def __init__
            # end class BleProConnectionScheme

            class Ls2ConnectionScheme(AbstractSubSystem):
                """
                LS2 Connection Scheme SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "LS2_CS")

                    self.F_Enabled = False
                    self.F_LS2_Support = False
                    self.F_UHS_Support = False
                    self.F_USB_Cable_Support = False
                    self.F_PrePairedReceiverPID = None
                    self.F_DeepSleepCurrentThreshold = 0
                    self.F_MaxWaitSleep = 0
                    self.F_ThreePairingSlots = True
                    self.F_ConnectButton = False
                    self.F_ProtocolSwitch = False
                    self.F_WakeUpByConnectButton = False
                    self.F_BleSupport = False
                # end def __init__
            # end class Ls2ConnectionScheme

            class DeviceRecoverySubSystem(AbstractSubSystem):
                """
                Device Recovery Enabler/Disabler SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "DEVICE_RECOVERY")

                    self.F_Enabled = False

                    # recovery keys list variant
                    # 0 - Platform Mouse
                    # 1 - Standard Mouse Product
                    self.F_RecoveryKeysVariant = None
                # end def __init__
            # end class DeviceRecoverySubSystem
        # end class ConnectionScheme

        class FnLockSubSystem(AbstractSubSystem):
            """
            Fn Lock Sub System
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "FN_LOCK")
                self.F_Enabled = False

                # PWS Fn lock UX version control
                # https://drive.google.com/drive/folders/1E9WrxhLDCfGva29-LtERU2VoQi_D-w8w
                self.F_PWS_UX_V1_0 = False
                self.F_PWS_UX_V1_1 = False
                self.F_PWS_UX_V1_2 = False
                self.F_PWS_UX_V1_3 = False

                # Gaming Fn lock UX version control
                # https://drive.google.com/drive/folders/1pVAlquKxrpbePOgjVZqCW35LM5Wx0sc1
                self.F_GAMING_UX_V1_0 = False
            # end def __init__
        # end class FnLockSubSystem

        class EVTAutomationSubSystem(AbstractSubSystem):
            """
            EVT Automation Enabled/Disabler SubSystem
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "EVT_AUTOMATION")
                self.F_Enabled = False

                # Typing Test SubSystem
                self.TYPING_TEST = self.TypingTestSubSystem()
                self.BATTERY_NOTIFICATION_TEST = self.BatteryNotificationTestSubSystem()
            # end def __init__

            class TypingTestSubSystem(AbstractSubSystem):
                """
                Enable/Disable Typing Test SubSystem
                """
                def __init__(self):
                    AbstractSubSystem.__init__(self, "TYPING_TEST")
                    self.F_Enabled = True
                    # Optional flag to generate google sheet during test run
                    self.F_CreateGoogleSheet = False
                    # If not enabled, typing test with lesser number of test loops is executed
                    self.F_RunTypingTestCompleteEVT = False
                    # Spreadsheet ID of the EVT Report Document for a particular NPI
                    self.F_EVTReportSpreadsheetID = None
                # end def __init__
            # end class TypingTestSubSystem

            class BatteryNotificationTestSubSystem(AbstractSubSystem):
                """
                Enable/Disable Battery Notification Test SubSystem
                """
                def __init__(self):
                    AbstractSubSystem.__init__(self, "BATTERY_NOTIFICATION_TEST")
                    self.F_Enabled = False
                # end def __init__
            # end class BatteryNotificationTestSubSystem
        # end class EVTAutomationSubSystem
    # end class DeviceSubSystem

    class DebounceSubSystem(AbstractSubSystem):
        """
        Debounce Enabler/Disabler SubSystem
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "DEBOUNCE")

            # Debounce feature
            self.F_Enabled = False

            # Supported version (i.e. which algorithm)
            self.F_Version_1 = False
            self.F_Version_2 = False

            # Debounce settings (timings)
            self.F_0PercentMakeDebounceUs = 0
            self.F_100PercentMakeDebounceUs = 0
            self.F_MakeBlindWindowUs = 0
            self.F_0PercentBreakDebounceUs = 0
            self.F_100PercentBreakDebounceUs = 0
            self.F_BreakBlindWindowUs = 0
            self.F_100PercentMakeDeepSleepUs = 0
        # end def __init__
    # end class DebounceSubSystem

    class LatencySubSystem(AbstractSubSystem):
        """
        Feature Latency Timings
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "LATENCY")

            # Flag to enable the USB latency tests using a Beagle 480 USB analyser (motion and click latency test suites)
            self.F_EnableUSBLatencyTestsWithUsbAnalyser = False
            # Flag to enable the LSX latency tests using a Beagle 480 USB analyser (motion and click latency test suites)
            self.F_EnableLSXLatencyTestsWithUsbAnalyser = False

            # Switch Latency SubSystem
            self.SWITCH_LATENCY = self.SwitchLatencySubSystem()

            # Motion Latency SubSystem
            self.MOTION_LATENCY = self.MotionLatencySubSystem()
        # end def __init__

        class SwitchLatencySubSystem(AbstractSubSystem):
            """
            Feature Switch Latency Timings
            """
            def __init__(self):
                AbstractSubSystem.__init__(self, "SWITCH_LATENCY")
                # Switch Latency feature
                self.F_Enabled = False

                # Switch latency time on BLE or BLE Pro or LS2 in deep sleep mode in us
                self.F_MinSwitchLatencyDeepSleepMode = 0
                self.F_AvgSwitchLatencyDeepSleepMode = 0
                self.F_Percentile95SwitchLatencyDeepSleepMode = 0

                # Switch latency time on BLE or BLE Pro or LS2 in sleep mode in us
                self.F_MinSwitchLatencySleepMode = 0
                self.F_AvgSwitchLatencySleepMode = 0
                self.F_Percentile95SwitchLatencySleepMode = 0

                # Switch latency time on BLE or BLE Pro or LS2 or USB in lift mode in us
                self.F_MinSwitchLatencyLiftMode = 0
                self.F_AvgSwitchLatencyLiftMode = 0
                self.F_Percentile95SwitchLatencyLiftMode = 0

                # Switch latency on BLE or BLE pro in run mode in us
                self.F_MinSwitchLatencyRunMode = 0
                self.F_AvgPressLatencyRunMode = 0
                self.F_Percentile95PressLatencyRunMode = 0
                self.F_AvgReleaseLatencyRunMode = 0
                self.F_Percentile95ReleaseLatencyRunMode = 0

                # Switch latency time on LS2 in us
                # Concerning minimum switch latency, for now we decided to have a common value to make and release
                # actions whatever the report rate.
                # The hypothesis for make latency is that the minimum value is not impacted by the report rate because
                # it is just the processing time of the process and the duration to send the information to the host.
                # It is the mean value that is changing and the max value (and so the dispersion).
                # For break latency it's different because the behaviour can be different between a galvanic switch and
                # a hybrid switch. For example on wakanda the hybrid break latency is the same as hybrid make latency
                # but the galvanic break latency is different from hybrid break latency and depends on the report rate
                # In order to not complicate too much these parameter only 1 minimum latency is checked whatever the
                # report rate or the make/break.
                # If there is a need, it will be possible to add a minimum latency for each report rate depending on
                # the switch type (hybrid/galvanic)
                self.F_MinSwitchLatencyLs2RunMode = 0
                self.F_AvgSwitchLatencyReleaseLs2RunMode = 0
                self.F_Percentile95SwitchLatencyReleaseLs2RunMode = 0
                # At 1 kHz
                self.F_AvgSwitchLatencyPressLs2RunMode1kHz = 0
                self.F_Percentile95SwitchLatencyPressLs2RunMode1kHz = 0
                # At 2 kHz
                self.F_AvgSwitchLatencyPressLs2RunMode2kHz = 0
                self.F_Percentile95SwitchLatencyPressLs2RunMode2kHz = 0
                # At 4 kHz
                self.F_AvgSwitchLatencyPressLs2RunMode4kHz = 0
                self.F_Percentile95SwitchLatencyPressLs2RunMode4kHz = 0
                # At 8 kHz
                self.F_AvgSwitchLatencyPressLs2RunMode8kHz = 0
                self.F_Percentile95SwitchLatencyPressLs2RunMode8kHz = 0

                # Switch latency time on USB in us
                self.F_MinSwitchLatencyUsb = 0
                self.F_AvgSwitchLatencyReleaseUsb = 0
                self.F_Percentile99SwitchLatencyReleaseUsb = 0
                # At 1 kHz
                self.F_AvgSwitchLatencyPressUsb1kHz = 0
                self.F_Percentile99SwitchLatencyPressUsb1kHz = 0
                # At 2 kHz
                self.F_AvgSwitchLatencyPressUsb2kHz = 0
                self.F_Percentile99SwitchLatencyPressUsb2kHz = 0
                # At 4 kHz
                self.F_AvgSwitchLatencyPressUsb4kHz = 0
                self.F_Percentile99SwitchLatencyPressUsb4kHz = 0
                # At 8 kHz
                self.F_AvgSwitchLatencyPressUsb8kHz = 0
                self.F_Percentile99SwitchLatencyPressUsb8kHz = 0
            # end def __init__
        # end class SwitchLatencySubSystem

        class MotionLatencySubSystem(AbstractSubSystem):
            """
            Feature Motion Latency Timings
            """
            def __init__(self):
                AbstractSubSystem.__init__(self, "MOTION_LATENCY")
                # Motion Latency feature
                self.F_Enabled = False

                # Motion latency time on BLE or BLE Pro in run mode in us
                self.F_MinMotionLatencyRunMode = 0
                self.F_AvgMotionLatencyRunMode = 0
                self.F_Percentile95MotionLatencyRunMode = 0
                # Motion latency time on BLE or BLE Pro or LS2 in sleep mode in us
                self.F_MinMotionLatencySleepMode = 0
                self.F_AvgMotionLatencySleepMode = 0
                self.F_Percentile95MotionLatencySleepMode = 0
                # Motion latency time on BLE or BLE Pro or LS2 in deep sleep mode in us
                self.F_MinMotionLatencyDeepSleepMode = 0
                self.F_AvgMotionLatencyDeepSleepMode = 0
                self.F_Percentile95MotionLatencyDeepSleepMode = 0
                # Motion latency time on LS2 in run mode in us
                # Concerning minimum motion latency, we decided to check only 1 value whatever the report rate.
                # The hypothesis for motion latency is that the minimum value is not impacted by the report rate because
                # it is just the processing time of the process and the duration to send the information to the host.
                self.F_MinMotionLatencyLs2RunMode = 0
                # At 1 kHz
                self.F_AvgMotionLatencyLs2RunMode1kHz = 0
                self.F_Percentile95MotionLatencyLs2RunMode1kHz = 0
                # At 2 kHz
                self.F_AvgMotionLatencyLs2RunMode2kHz = 0
                self.F_Percentile95MotionLatencyLs2RunMode2kHz = 0
                # At 4 kHz
                self.F_AvgMotionLatencyLs2RunMode4kHz = 0
                self.F_Percentile95MotionLatencyLs2RunMode4kHz = 0
                # At 8 kHz
                self.F_AvgMotionLatencyLs2RunMode8kHz = 0
                self.F_Percentile95MotionLatencyLs2RunMode8kHz = 0
                # Motion latency time on USB in us
                self.F_MinMotionLatencyUsb = 0
                # At 1 kHz
                self.F_AvgMotionLatencyUsb1kHz = 0
                self.F_Percentile99MotionLatencyUsb1kHz = 0
                # At 2 kHz
                self.F_AvgMotionLatencyUsb2kHz = 0
                self.F_Percentile99MotionLatencyUsb2kHz = 0
                # At 4 kHz
                self.F_AvgMotionLatencyUsb4kHz = 0
                self.F_Percentile99MotionLatencyUsb4kHz = 0
                # At 8 kHz
                self.F_AvgMotionLatencyUsb8kHz = 0
                self.F_Percentile99MotionLatencyUsb8kHz = 0
            # end def __init__
        # end class MotionLatencySubSystem
    # end class LatencySubSystem

    class NvsChunkIdsSubSystem(AbstractSubSystem):
        """
        Nvs Chunk Ids SubSystem
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "NVS_CHUNK_IDS")

            self.F_Enabled = False

            # Chunk Id map variant
            self.F_IsGamingVariant = False

            # List of chunk ids to be customized
            self.F_ChunkIdNames = ()
            self.F_ChunkIdValues = ()
        # end def __init__
    # end class NvsChunkIdsSubSystem

    class CodeCheckListSubSystem(AbstractSubSystem):
        """
        Code CheckList SubSystem
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "CODE_CHECKLIST")

            self.F_Enabled = False

            # Stack depth verification
            self.F_StackVerification = False

            # Ram initialization
            self.F_RamInitialization = False
            # ELF bootloader file name
            self.F_BootLoaderElfFileName = None
        # end def __init__
    # end class CodeCheckListSubSystem

    class NvsUicrSubSystem(AbstractSubSystem):
        """
        NVS and UICR SubSystem
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "NVS_UICR")

            self.F_Enabled = False

            # NVS Encryption
            self.F_NVSEncryption = False

            # Bootloader Address
            self.F_BootloaderAddress = None

            # UICR Registers supported
            self.F_PSELRESET = 0xFFFFFFFF
            self.F_NFCPINS = None
            self.F_DEBUGCTRL = None
            self.F_REGOUT0 = None

            # use Customer 31 register to store a magic number used to ensure UICR programming
            # cf https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/9153
            self.F_MagicNumber = False
        # end def __init__
    # end class NvsUicrSubSystem

    class HidReportSubSystem(AbstractSubSystem):
        """
        Hid Report SubSystem
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "HID_REPORT")

            self.F_Enabled = False

            # HID report mapping
            # cf https://docs.google.com/spreadsheets/d/1f066R9V1WS2B9Ebh9_8tvdEAXs39QA2BnQbnTBNNvgU/edit#gid=856308430
            self.F_HidGuidelinesVersion = None

            # HID reports format
            self.F_HidMouseType = None
            self.F_HidKeyboardType = None

            # HID report customization linked to a system feature
            # The list of functions that lead to a change is as follows:
            # ('horizontal_scrolling',) if the DUT supports the C&P Virtual Thumbwheel feature [CP_VTHUMB]
            # ('emoji_menu_button',) if the DUT supports the reconfigurable island button for emoji menu
            self.F_HidOptions = ()

            # List of consumer usage in the product specific consumer report (or minimal report in code)
            # valid names used are field of pyhid.hid.usbhidusagetable.ConsumerHidUsage
            # current source is product specific code for the order
            # TODO: Add a better source of information
            self.F_ProductSpecificUsages = ()

            # Usages in the top row feature descriptor
            # ref:
            # https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id.8ahvvyb76ay
            self.F_TopRowUsagesCount = None

        # end def __init__
    # end class HidReportSubSystem

    class TimingsSubSystem(AbstractSubSystem):
        """
        Firmware internal timings (main loop duration, frequency, ...)
        """
        def __init__(self):
            AbstractSubSystem.__init__(self, "TIMINGS")

            self.F_Enabled = False

            # Device startup time in ms
            self.F_StartupTime = 0
            self.F_StartupTimeColdBoot = None

            # 2kHz core timings (Fast tick, RX & TX instant, ...)
            self.F_2kHzSupport = False
        # end def __init__
    # end class TimingsSubSystem

    class UsbCommunicationSubSystem(AbstractSubSystem):
        """
        USB communication SubSystem
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "USB_COMMUNICATION")

            # FeatureSet feature
            self.F_Enabled = False

            # SET_IDLE supported
            self.F_SetIdleSupported = False
        # end def __init__
    # end class UsbCommunicationSubSystem

    class ProtocolsSubSystem(AbstractSubSystem):
        """
        Protocols Sub System
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "PROTOCOLS")

            # Choose the default protocol to use for tests. If specified, the values can be found in
            # ``pychannel.channelinterfaceclasses.LogitechProtocol``, the int value or the str name of the constants
            # can be used, for example: DefaultProtocol = 'BLE' will be the same as DefaultProtocol = -2
            self.F_DefaultProtocol = None

            # USB protocol SubSystem
            self.USB = self.USBSubSystem()

            # BLE protocol SubSystem
            self.BLE = self.BLESubSystem()

            # BLE Pro protocol SubSystem
            self.BLE_PRO = self.BLEProSubSystem()
        # end def __init__

        class USBSubSystem(AbstractSubSystem):
            """
            USB Protocol
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "USB")

                # USB protocol feature
                self.F_Enabled = False

                # Interface descriptors format
                # The possible descriptors are:
                # - KeyboardBitmapInterfaceDescriptor, KeyboardBitmapReceiverDescriptor, KeyboardBitmapKeyDescriptor,
                #   KeyboardInterfaceDescriptor or KeyboardReceiverDescriptor for the keyboard interface
                # - MouseInterfaceDescriptor, MouseKeyDescriptor or MouseNvidiaExtensionKeyDescriptor for the mouse
                #   interface
                # - HIDppInterfaceDescriptor for the Hid++ interface
                # - WindowsDigitizer5FingersDescriptor for the receiver Digitizer interface (only on Mezzy 2.0) or
                #   WindowsDigitizer3FingersDescriptor for the device Digitizer interface (TouchPad products)
                self.F_KeyboardInterfaceDescriptor = None
                self.F_MouseInterfaceDescriptor = None
                self.F_HidppInterfaceDescriptor = None
                self.F_DigitizerInterfaceDescriptor = None

                # Other device specific fields
                # - Top Row Feature Usage Maximum LSB i.e. CNT3 constant in specification
                # cf
                # https://docs.google.com/document/d/14XE95sAj5tIiLu3_wCByI2ETt9VEh92PjC1aIIBWnsQ/edit#bookmark=id
                # .8ahvvyb76ay
                self.F_TopRawUsageMaximum = None
            # end def __init__
        # end class USBSubSystem

        class BLESubSystem(AbstractSubSystem):
            """
            BLE Protocol
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "BLE")

                # BLE protocol feature
                self.F_Enabled = False

                # Hid report map format
                self.F_HidReportMap = None

                # Support of BLE++ service CCCD toggled mechanism defined in this following flowchart as
                # "Future implementation proposal"
                # https://lucid.app/lucidchart/4ec2b55b-188c-4473-b6ec-2cb9ed9513ee/edit?shared=true&page=TuoIO9Dc9RQc#
                # And implemented on the quark platform through the following patchset:
                # https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/9044
                self.F_BLEppCccdToggled = False

                self.F_ChromeSupport = False

                self.F_OsDetection = False

                # DUT follows the specification for ble described on spaces.logitech.com (July 2023)
                self.F_Spaces_Specifications = False

                self.F_Software_Revision = None

                # Version of Battery service (BAS)
                # Possible values:
                # - None : Backward Compatibility mode for devices with Battery service 1.0 dating before February 2024
                # - "1.0" : Device has battery service aligned with the 1.0 version of BAS BLE SIG specification
                # - "1.1" : Device has battery service aligned with the 1.1 version of BAS BLE SIG specification
                self.F_BAS_Version = None

                # BLE context class ID to use in pytestbox.receiver.setup.setup test cases to change the type of BLE
                # context tu use by uploading the right firmware to the DK used as the BLE context hardware.
                # The values can be found in ``pyusb.libusbdriver.BleContextClassId``, the int value or the str name
                # of the constants can be used, for example: BleContextClassId = 'NRF_BLE_LIB' will be the same as
                # BleContextClassId = 1
                # This will be used only if there is a possibility to switch off the jlink lines of the device to
                # the DK debugger to then be able to flash the DK's firmware
                self.F_BleContextClassId = None

                self.ADVERTISING = self.AdvertisingSubSystem()
                self.CONNECTION_PARAMETERS = self.ConnectionParametersSubSystem()
            # end def __init__

            class AdvertisingSubSystem(AbstractSubSystem):
                """
                ADVERTISING SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "ADVERTISING")

                    # Pairing mode advertising packet information
                    self.F_FirstAdvertisingIntervalMs = 0
                    self.F_FirstAdvertisingWindowS = 0.0
                    self.F_SecondAdvertisingIntervalMs = 0
                    self.F_SecondAdvertisingWindowS = 0.0
                    self.F_SwiftPairCapability = False
                    self.F_FastPairCapability = False
                    self.F_FastPairModelId = "000000"

                    # Pairing mode scan response information
                    self.F_TxPower = 0
                    self.F_AuthenticationType = 0
                    self.F_DeviceType = 0

                    # Prepairing
                    # When prepairing information are present and unused, the device will alternate between two
                    # advertising sub windows:
                    # - The sub window in seconds for regular pairing mode undirected advertising
                    self.F_UnusedPrepairingInfoRegularAdvertisingSubWindowS = 0.0
                    # - The sub window in seconds for prepairing directed advertising
                    self.F_UnusedPrepairingInfoPrepairingAdvertisingSubWindowS = 0.0

                    # Application reconnection mode advertising packet information
                    self.F_ApplicationReconnectionAdvertisingWindowS = 0.0

                    # Bootloader reconnection mode advertising packet information
                    self.F_BootloaderReconnectionAdvertisingCompleteWindowS = 0.0
                    self.F_BootloaderReconnectionAdvertisingFirstHdcSubWindowS = 0.0
                    self.F_BootloaderReconnectionAdvertisingHdcSubWindowS = 0.0
                    self.F_BootloaderReconnectionAdvertisingLcdSubWindowS = 0.0
                    self.F_BootloaderReconnectionAdvertisingLcdIntervalMs = 0

                    # Bootloader recovery mode advertising packet information
                    self.F_BootloaderRecoveryAdvertisingCompleteWindowS = 0.0
                # end def __init__
            # end class AdvertisingSubSystem

            class ConnectionParametersSubSystem(AbstractSubSystem):
                """
                CONNECTION_PARAMETERS SubSystem
                """

                def __init__(self):
                    AbstractSubSystem.__init__(self, "CONNECTION_PARAMETERS")
                    # Flag indicating default os connection parameters are overriden in the settings
                    self.F_OverrideDefaultOS = False

                    # Default OS connection parameter override value
                    self.F_DefaultOSMinConnectionInterval = 0.0
                    self.F_DefaultOSMaxConnectionInterval = 0.0
                    self.F_DefaultOSSlaveLatency = 0.0
                    self.F_DefaultOSSupervisionTimeout = 0.0
                # end def __init__
            # end class ConnectionParametersSubSystem

        # end class BLESubSystem

        class BLEProSubSystem(AbstractSubSystem):
            """
            BLE Pro Protocol
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "BLE_PRO")

                # BLE Pro protocol feature
                self.F_Enabled = False

                # Supported Version
                self.F_Version_0 = False
                self.F_Version_1 = False
                self.F_Version_2 = False
            # end def __init__
        # end class BLEProSubSystem
    # end class ProtocolsSubSystem

    class DualBankSubSystem(AbstractSubSystem):
        """
        Dual Bank Sub System
        """

        def __init__(self):
            AbstractSubSystem.__init__(self, "DUAL_BANK", enabled=False)

            # Private key used to sign applications (leave empty if root of trust is enabled)
            self.F_Key = ''
            # Sign Type
            self.F_SignType = ''
            # RSA Key Length
            self.F_RSAKeyLength = None
            # RSA Key Exponent
            self.F_RSAKeyExp = None

            # Slots
            self.SLOTS = self.SlotsSubSystem()
            # Bootloader Image Communication
            self.BOOTLOADER_IMAGE_COMMUNICATION = self.BootImgCommSubSystem()
            # Root Of Trust Table
            self.ROOT_OF_TRUST_TABLE = self.RootOfTrustTableSubSystem()
            # Key Hierarchy (Here, consider that the key hierarchy is the same for both slots)
            self.KEY_HIERARCHY = self.KeyHierarchySubSystem()
        # end def __init__

        class SlotsSubSystem(AbstractSubSystem):
            """
            Slots Sub System
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "SLOTS", enabled=False)

                # Slot Base
                self.F_Base = ()

                # Slot Device Name
                self.F_DeviceName = ()

                # Slot Header
                # Slot versions
                self.F_VersionMajor = ()
                self.F_VersionMinor = ()
                self.F_VersionRevision = ()
                self.F_VersionBuildNumber = ()

                # Flash/ROM address the image has been built for
                self.F_LoadAddr = ()
                # Size of the image header (bytes)
                self.F_HeaderSize = ()
                # Size of protected TLV area
                self.F_ProtectTLVSize = ()
                # Image size (does not include header)
                self.F_ImageSize = ()
                # Image header flags
                self.F_Flags = ()
            # end def __init__
        # end class SlotsSubSystem

        class BootImgCommSubSystem(AbstractSubSystem):
            """
            Bootloader Image Communication Sub System
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "BOOTLOADER_IMAGE_COMMUNICATION", enabled=False)

                # Structure's version
                self.F_Version = 0x00
                # Firmware Prefix. See : https://spaces.logitech.com/display/CPGFWLOG/Bootloaders
                self.F_FwPrefix = ""
                # Firmware number
                self.F_FwNumber = 0x00
                # Firmware version
                self.F_FwVersion = 0x00
                # Firmware build number
                self.F_FwBuildNumber = 0x0000
                # Git hash MSBs
                self.F_GitHash = None
                # Build flags
                self.F_DirtyBuildFlag = 0
                self.F_DebugBuildFlag = 0
                self.F_DevelopmentCredentialsFlag = 0
                # Root of trust
                self.F_RootOfTrustCount = 0
                self.F_RootOfTrustAddr = 0x00000000
            # end def __init__
        # end class BootImgCommSubSystem

        class RootOfTrustTableSubSystem(AbstractSubSystem):
            """
            Root Of Trust Table Sub System
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "ROOT_OF_TRUST_TABLE", enabled=False)

                # Root of trust type in encoded flags
                self.F_Types = ()
                # Root of trust keys
                self.F_Keys = ()
            # end def __init__
        # end class RootOfTrustTableSubSystem

        class KeyHierarchySubSystem(AbstractSubSystem):
            """
           Key Hierarchy Sub System
            """

            def __init__(self):
                AbstractSubSystem.__init__(self, "KEY_HIERARCHY", enabled=False)

                # Root of trust type in encoded flags
                self.F_UseX509Certificate = False
                # Key Count
                self.F_KeyCount = 0
                # Keys
                self.F_Keys = ()
            # end def __init__
        # end class KeyHierarchySubSystem
    # end class DualBankSubSystem
# end class ProductSubSystem

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
