#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hiddispatcher
:brief: HID dispatcher class
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/08/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from queue import Empty
from sys import stdout
from threading import RLock

from pyhid import hidparser
from pyhid.hid.hidcallstatemanagementcontrol import HidCallStateManagementControl
from pyhid.hid.hidconsumer import HidConsumer
from pyhid.hid.hiddigitizer import HidDigitizer
from pyhid.hid.hidkeyboard import HidKeyboard
from pyhid.hid.hidkeyboardbitmap import HidKeyboardBitmap
from pyhid.hid.hidmouse import HidMouse
from pyhid.hid.hidmouse import HidMouseNvidiaExtension
from pyhid.hid.hidsystemcontrol import HidSystemControl
from pyhid.hid.interfacedescriptors import DescriptorDispatcher
from pyhid.hid.interfacedescriptors import ReportDescriptor
from pyhid.hidpp.features.batteryunifiedlevelstatus import BatteryLevelStatusBroadcastEvent as BatteryEvent
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryCapabilityResponse as BatteryCapability
from pyhid.hidpp.features.batteryunifiedlevelstatus import GetBatteryLevelStatusResponse as BatteryLevel
from pyhid.hidpp.features.batteryunifiedlevelstatus import ShowBatteryStatusResponse as BatteryStatus
from pyhid.hidpp.features.common.analogkeys import AnalogKeysModel
from pyhid.hidpp.features.common.backlight import BacklightModel
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationModel
from pyhid.hidpp.features.common.bleproprepairing import BleProPrepairingModel
from pyhid.hidpp.features.common.changehost import ChangeHostModel
from pyhid.hidpp.features.common.configurabledeviceproperties import ConfigurableDevicePropertiesModel
from pyhid.hidpp.features.common.configurableproperties import ConfigurablePropertiesModel
from pyhid.hidpp.features.common.configurabledeviceregisters import ConfigurableDeviceRegistersModel
from pyhid.hidpp.features.common.controllist import ControlListModel
from pyhid.hidpp.features.common.devicefriendlyname import DeviceFriendlyNameModel
from pyhid.hidpp.features.common.deviceinformation import DeviceInformationModel
from pyhid.hidpp.features.common.devicetypeandname import DeviceTypeAndNameModel
from pyhid.hidpp.features.common.dfu import DfuModel
from pyhid.hidpp.features.common.dfucontrol import DfuControlModel
from pyhid.hidpp.features.common.equaddjdebuginfo import ReadEquadDJDebugInfoResponse as ReadEquadDJDebugInfo
from pyhid.hidpp.features.common.equaddjdebuginfo import WriteEquadDJDebugInfoResponse as WriteEquadDJDebugInfo
from pyhid.hidpp.features.common.equadpairingenc import EquadPairingEncModel
from pyhid.hidpp.features.common.forcepairing import ForcePairingModel
from pyhid.hidpp.features.common.forcesensingbutton import ForceSensingButtonModel
from pyhid.hidpp.features.common.fullkeycustomization import FullKeyCustomizationModel
from pyhid.hidpp.features.common.gpioaccess import GpioAccessModel
from pyhid.hidpp.features.common.hostsinfo import HostsInfoModel
from pyhid.hidpp.features.common.i2cdirectaccess import I2CDirectAccessModel
from pyhid.hidpp.features.common.keepalive import KeepAliveModel
from pyhid.hidpp.features.common.ledtest import LEDTestModel
from pyhid.hidpp.features.common.lightspeedprepairing import LightspeedPrepairingModel
from pyhid.hidpp.features.common.managedeactivatablefeatures import ManageDeactivatableFeaturesModel
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthModel
from pyhid.hidpp.features.common.manufacturingmode import ManufacturingModeModel
from pyhid.hidpp.features.common.oobstate import OobStateModel
from pyhid.hidpp.features.common.opticalswitches import OpticalSwitchesModel
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationModel
from pyhid.hidpp.features.common.powermodes import PowerModesModel
from pyhid.hidpp.features.common.propertyaccess import PropertyAccessModel
from pyhid.hidpp.features.common.rftest import RFTestModel
from pyhid.hidpp.features.common.rftestble import RFTestBLEModel
from pyhid.hidpp.features.common.securedfucontrol import SecureDfuControlModel
from pyhid.hidpp.features.common.specialkeysmsebuttons import SpecialKeysMSEButtonsModel
from pyhid.hidpp.features.common.spidirectaccess import SPIDirectAccessModel
from pyhid.hidpp.features.common.staticmonitormode import StaticMonitorModeModel
from pyhid.hidpp.features.common.tdeaccesstonvm import TdeAccessToNvmModel
from pyhid.hidpp.features.common.temperaturemeasurement import TemperatureMeasurementModel
from pyhid.hidpp.features.common.unifiedbattery import UnifiedBatteryModel
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte0To15Response as GetByte0To15
from pyhid.hidpp.features.common.uniqueidentifier32bytes import GetByte16To31Response as GetByte16To31
from pyhid.hidpp.features.common.uniqueidentifier32bytes import RegenIdResponse as RegenId
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pyhid.hidpp.features.configchange import GetConfigurationCookieResponse as ConfigCookie
from pyhid.hidpp.features.configchange import SetConfigurationCompleteResponse as ConfigComplete
from pyhid.hidpp.features.enablehidden import GetEnableHiddenFeaturesResponse as GetHidden
from pyhid.hidpp.features.enablehidden import SetEnableHiddenFeaturesResponse as SetHidden
from pyhid.hidpp.features.error import ErrorCodes
from pyhid.hidpp.features.error import Hidpp1ErrorCodes
from pyhid.hidpp.features.featureset import FeatureSetModel
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurveModel
from pyhid.hidpp.features.gaming.brakeforce import BrakeForceModel
from pyhid.hidpp.features.gaming.brightnesscontrol import BrightnessControlModel
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedalsModel
from pyhid.hidpp.features.gaming.extendedadjustablereportrate import ExtendedAdjustableReportRateModel
from pyhid.hidpp.features.gaming.gaminggkeys import GamingGKeysModel
from pyhid.hidpp.features.gaming.logimodifiers import LogiModifiersModel
from pyhid.hidpp.features.gaming.macrorecordkey import MacroRecordkeyModel
from pyhid.hidpp.features.gaming.modestatus import ModeStatusModel
from pyhid.hidpp.features.gaming.mousebuttonspy import MouseButtonSpyModel
from pyhid.hidpp.features.gaming.onboardprofiles import OnboardProfilesModel
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatusModel
from pyhid.hidpp.features.gaming.perkeylighting import PerKeyLightingModel
from pyhid.hidpp.features.gaming.profilemanagement import ProfileManagementModel
from pyhid.hidpp.features.gaming.reportrate import ReportRateModel
from pyhid.hidpp.features.gaming.rgbeffects import RGBEffectsModel
from pyhid.hidpp.features.hireswheel import HiResWheelModel
from pyhid.hidpp.features.keyboard.disablecontrolsbycidx import DisableControlsByCIDXModel
from pyhid.hidpp.features.keyboard.disablekeys import DisableKeysModel
from pyhid.hidpp.features.keyboard.disablekeysbyusage import DisableKeysByUsageModel
from pyhid.hidpp.features.keyboard.fninversionformultihostdevices import FnInversionForMultiHostDevicesModel
from pyhid.hidpp.features.keyboard.keyboardinternationallayouts import KeyboardInternationalLayoutsModel
from pyhid.hidpp.features.keyboard.lockkeystate import LockKeyStateModel
from pyhid.hidpp.features.keyboard.multiplatform import MultiPlatformModel
from pyhid.hidpp.features.keyboard.multiroller import MultiRollerModel
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiModel
from pyhid.hidpp.features.mouse.analysismode import AnalysisModeModel
from pyhid.hidpp.features.mouse.extendedadjustabledpi import ExtendedAdjustableDpiModel
from pyhid.hidpp.features.mouse.mousewheelanalytics import MouseWheelAnalyticsModel
from pyhid.hidpp.features.mouse.ratchetwheel import RatchetWheelModel
from pyhid.hidpp.features.mouse.smartshift import GetRatchetControlModeResponse as GetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshift import SetRatchetControlModeResponse as SetRatchetControlMode
from pyhid.hidpp.features.mouse.smartshifttunable import SmartShiftTunableModel
from pyhid.hidpp.features.mouse.thumbwheel import ThumbwheelModel
from pyhid.hidpp.features.peripheral.ads1231 import Ads1231Model
from pyhid.hidpp.features.peripheral.mlx90393multisensor import MLX90393MultiSensorModel
from pyhid.hidpp.features.peripheral.mlx903xx import MLX903xxModel
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826Model
from pyhid.hidpp.features.peripheral.testkeysdisplay import TestKeysDisplayModel
from pyhid.hidpp.features.root import RootModel
from pyhid.hidpp.features.touchpad.touchpadrawxy import TouchpadRawXYModel
from pyhid.hidpp.features.verticalscrolling import GetRollerInfoResponse as GetRollerInfo
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1Model
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.vlp.features.common.contextualdisplay import ContextualDisplayModel
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSetModel
from pyhid.vlp.features.important.vlproot import VLPRootModel
from pyhid.vlp.vlpmessage import VlpMessage
from pyhid.vlp.vlpmessage import VlpMessageRawPayload
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pylibrary.tools.threadutils import QueueWithFilter
from pylibrary.tools.threadutils import synchronized
from pylibrary.tools.util import reverse_bits
from pytransport.transportmessage import TransportMessage

# ----------------------------------------------------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------------------------------------------------
VERBOSE = False

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# A global lock to protect from simultaneous access/modification on handler list
SYNCHRONIZATION_LOCK = RLock()


class AbstractHIDMessageHandler(object):
    """
    Common interface for HID message handlers
    """

    def is_message_accepted(self, message):
        """
        Return True if message is accepted by this handler.
        By default, all messages are accepted.

        :param message: Message to test
        :type message: ``object``

        :return: Flag indicating if the message is accepted
        :rtype: ``bool``
        """
        return True
    # end def is_message_accepted

    def is_message_type_accepted(self, message_type):
        """
        Return True if message type is accepted by this handler.
        By default, all message types are accepted.

        :param message_type: Message type to test
        :type message_type: ``type``

        :return: Flag indicating if the message type is accepted
        :rtype: ``bool``
        """
        return True
    # end def is_message_type_accepted

    def handle(self, message):
        """
        Handle message

        :param message: Message to handle
        :type message: ``object``
        """
        raise NotImplementedError
    # end def handle
# end class AbstractHIDMessageHandler


class HidMessageQueue(QueueWithFilter, AbstractHIDMessageHandler):
    """
    Define queue that accepts and stores all HID messages
    """
    def __init__(self, accepted_messages=None, name=None, *args, **kwargs):
        """
        :param accepted_messages: Queue will only store messages of specified types, if no messages are specified,
                                  all messages will be stored - OPTIONAL
        :type accepted_messages: ``tuple`` or ``None``
        :param name: Name - OPTIONAL
        :type name: ``str`` or ``None``
        :param args: Arguments - OPTIONAL
        :type args: ``dict`` or ``HexList``
        :param kwargs: Potential Future Arguments - OPTIONAL
        :type kwargs: ``dict`` or ``HexList``
        """
        super().__init__(*args, **kwargs)
        self._accepted_messages = accepted_messages
        self.name = name
    # end def __init__

    def is_message_accepted(self, message):
        # See ``AbstractHIDMessageHandler.is_message_accepted``
        if self._accepted_messages is None:
            return True
        else:
            return isinstance(message, self._accepted_messages)
        # end if
    # end def is_message_accepted

    def is_message_type_accepted(self, message_type):
        # See ``AbstractHIDMessageHandler.is_message_type_accepted``
        if self._accepted_messages is None:
            return True
        else:
            return message_type in self._accepted_messages
        # end if
    # end def is_message_type_accepted

    def update_accepted_messages(self, accepted_messages):
        """
        Update the list of accepted messages

        :param accepted_messages: Accepted messages types
        :type accepted_messages: ``tuple``
        """
        self._accepted_messages = accepted_messages
    # end def update_accepted_messages

    def handle(self, message):
        # See ``AbstractHIDMessageHandler.handle``
        self.put(message, timeout=5)
    # end def handle

    def check_empty(self, timeout=.01):
        """
        Check no more message in the queue

        :param timeout: Time to wait for message before raising exception [seconds] - OPTIONAL
        :type timeout: ``int``

        :return: True if the queue is empty, otherwise it raises an exception
        :rtype: ``bool``

        :raise ``Exception``: If the queue is not empty
        """
        try:
            message = super().get(timeout=timeout)
            raise Exception(f"The device sent an unexpected message: {str(message)}")
        except Empty:
            return True
        # end try
    # end def check_empty

    def clear(self):
        """
        Clear the queue and return all the messages that were in the queue as a list.

        :return: The list of untreated messages
        :rtype: ``list``
        """
        list_of_untreated_message = []

        while not self.event_empty.is_set():
            list_of_untreated_message.append(self.get())
        # end while

        return list_of_untreated_message
    # end def clear
# end class HidMessageQueue


class MessageType(object):
    """
    Define USB Message category
    """
    GET_DESCRIPTOR = 0
    HID_MOUSE = 1
    HID_KEYBOARD = 2
    HID_PP = 3
    HID_CONSUMER_CTRL = 4
    HID_SYS_CTRL = 5
    HID_CALL_STATE_MGT_CRTL = 6
    HID_DIGITIZER = 7
# end class MessageType


class HIDDispatcher(object):
    """
    Define dispatcher for HID messages coming from the device.
    """

    class QueueName(object):
        """
        Define name of the ``HidMessageQueue`` in the dispatcher.
        """
        IMPORTANT = "Important Queue"
        COMMON = "Common Queue"
        MOUSE = "Mouse Queue"
        KEYBOARD = "Keyboard Queue"
        TOUCHPAD = "Touchpad Queue"
        GAMING = "Gaming Queue"
        PERIPHERAL = "Peripheral Queue"
        INTERFACE_DESCRIPTOR = "Interface Descriptor Queue"
        EVENT = "Event Queue"
        BATTERY_EVENT = "Battery Event Queue"
        ERROR = "Errors Queue"
        HID = "HID Queue"
        RECEIVER_ERROR = "Receiver Errors Queue"
        RECEIVER_RESPONSE = "Receiver Response Queue"
        RECEIVER_EVENT = "Receiver Event Queue"
        RECEIVER_CONNECTION_EVENT = "Receiver Connection Event Queue"
        VLP_IMPORTANT = "VLP Important Queue"
        VLP_COMMON = "VLP Common Queue"
        VLP_EVENT = "VLP Event Queue"
    # end class QueueName

    def __init__(self):
        self._feature_table = {
            # --- Important --------------------------------------------------------------------------------------------
            # 0x0000 IRoot
            **RootModel.get_available_responses_map(),
            # 0x0001 IFeatureSet
            **FeatureSetModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Common -----------------------------------------------------------------------------------------------
            # 0x0003 Device Information
            **DeviceInformationModel.get_available_responses_map(),
            # 0x0005 Device Name and Type
            **DeviceTypeAndNameModel.get_available_responses_map(),
            # 0x0007 Device Friendly Name
            **DeviceFriendlyNameModel.get_available_responses_map(),
            # 0x0008 Keep Alive
            **KeepAliveModel.get_available_responses_map(),
            # 0x0011 Property Access
            **PropertyAccessModel.get_available_responses_map(),
            # 0x0020 Config Change
            (ConfigCookie.FEATURE_ID, ConfigCookie.VERSION, ConfigCookie.FUNCTION_INDEX): ConfigCookie,
            (ConfigComplete.FEATURE_ID, ConfigComplete.VERSION, ConfigComplete.FUNCTION_INDEX): ConfigComplete,
            # 0x0021 32 Byte Unique (Random) Identifier
            (GetByte0To15.FEATURE_ID, GetByte0To15.VERSION, GetByte0To15.FUNCTION_INDEX): GetByte0To15,
            (GetByte16To31.FEATURE_ID, GetByte16To31.VERSION, GetByte16To31.FUNCTION_INDEX): GetByte16To31,
            (RegenId.FEATURE_ID, RegenId.VERSION, RegenId.FUNCTION_INDEX): RegenId,
            # 0x00C2 DFU Control
            **DfuControlModel.get_available_responses_map(),
            # 0x00C3 Secure DFU Control
            **SecureDfuControlModel.get_available_responses_map(),
            # 0x00D0 DFU
            **DfuModel.get_available_responses_map(),
            # 0x1000 Battery Unified Level Status
            (BatteryLevel.FEATURE_ID, BatteryLevel.VERSION, BatteryLevel.FUNCTION_INDEX): BatteryLevel,
            (BatteryCapability.FEATURE_ID, BatteryCapability.VERSION,
             BatteryCapability.FUNCTION_INDEX): BatteryCapability,
            (BatteryStatus.FEATURE_ID, BatteryStatus.VERSION, BatteryStatus.FUNCTION_INDEX): BatteryStatus,
            # 0x1004 Unified Battery
            **UnifiedBatteryModel.get_available_responses_map(),
            # 0x1500 Force Pairing
            **ForcePairingModel.get_available_responses_map(),
            # 0x1602 Password Authentication
            **PasswordAuthenticationModel.get_available_responses_map(),
            # 0x1801 Manufacturing Mode
            **ManufacturingModeModel.get_available_responses_map(),
            # 0x1803 GPIO Access
            **GpioAccessModel.get_available_responses_map(),
            # 0x1805 OOB State
            **OobStateModel.get_available_responses_map(),
            # 0x1806 Configurable Device Properties
            **ConfigurableDevicePropertiesModel.get_available_responses_map(),
            # 0x1807 Configurable Properties
            **ConfigurablePropertiesModel.get_available_responses_map(),
            # 0x180B Configurable Device Registers
            **ConfigurableDeviceRegistersModel.get_available_responses_map(),
            # 0x1811 Equad Pairing Encryption
            **EquadPairingEncModel.get_available_responses_map(),
            # 0x1814 Change Host
            **ChangeHostModel.get_available_responses_map(),
            # 0x1815 Hosts Info
            **HostsInfoModel.get_available_responses_map(),
            # 0x1816 Ble Pro Pairing
            **BleProPrepairingModel.get_available_responses_map(),
            # 0x1817 Lightspeed Prepairing
            **LightspeedPrepairingModel.get_available_responses_map(),
            # 0x1830 Power Modes
            **PowerModesModel.get_available_responses_map(),
            # 0x1861 Battery Levels Calibration
            **BatteryLevelsCalibrationModel.get_available_responses_map(),
            # 0x1876 Optical Switches
            **OpticalSwitchesModel.get_available_responses_map(),
            # 0x1890 RF Test
            **RFTestModel.get_available_responses_map(),
            # 0x1891 RF Test BLE
            **RFTestBLEModel.get_available_responses_map(),
            # 0x18B0 Monitor Mode
            **StaticMonitorModeModel.get_available_responses_map(),
            # 0x18A1 LED Test
            **LEDTestModel.get_available_responses_map(),
            # 0x1982 Backlight
            **BacklightModel.get_available_responses_map(),
            # 0x19C0 Force Sensing Button
            **ForceSensingButtonModel.get_available_responses_map(),
            # 0x1B04 Keyboard Reprogrammable Keys and Mouse Buttons
            **SpecialKeysMSEButtonsModel.get_available_responses_map(),
            # 0x1B05 Full Key Customization
            **FullKeyCustomizationModel.get_available_responses_map(),
            # 0x1B08 Analog Keys
            **AnalogKeysModel.get_available_responses_map(),
            # 0x1B10 Control List
            **ControlListModel.get_available_responses_map(),
            # 0x1DF3 - EquadDJ Debug Info
            (ReadEquadDJDebugInfo.FEATURE_ID, ReadEquadDJDebugInfo.VERSION, ReadEquadDJDebugInfo.FUNCTION_INDEX):
                ReadEquadDJDebugInfo,
            (WriteEquadDJDebugInfo.FEATURE_ID, WriteEquadDJDebugInfo.VERSION, WriteEquadDJDebugInfo.FUNCTION_INDEX):
                WriteEquadDJDebugInfo,
            # 0x1E00 Enable Hidden Features
            (GetHidden.FEATURE_ID, GetHidden.VERSION, GetHidden.FUNCTION_INDEX): GetHidden,
            (SetHidden.FEATURE_ID, SetHidden.VERSION, SetHidden.FUNCTION_INDEX): SetHidden,
            # 0x1E01 Manage Deactivatable Features
            **ManageDeactivatableFeaturesModel.get_available_responses_map(),
            # 0x1E02 Manage Deactivatable Features
            **ManageDeactivatableFeaturesAuthModel.get_available_responses_map(),
            # 0x1E22 SPI Direct Access
            **SPIDirectAccessModel.get_available_responses_map(),
            # 0x1E30 I2C Direct Access
            **I2CDirectAccessModel.get_available_responses_map(),
            # 0x1EB0 TDE Access To Non-Volatile Memory
            **TdeAccessToNvmModel.get_available_responses_map(),
            # 0x1F30 Temperature Measurement
            **TemperatureMeasurementModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Mouse ------------------------------------------------------------------------------------------------
            # 0x2100 Vertical Scrolling
            (GetRollerInfo.FEATURE_ID, GetRollerInfo.VERSION, GetRollerInfo.FUNCTION_INDEX): GetRollerInfo,
            # 0x2110 Smart Shift
            (GetRatchetControlMode.FEATURE_ID, GetRatchetControlMode.VERSION, GetRatchetControlMode.FUNCTION_INDEX):
                GetRatchetControlMode,
            (SetRatchetControlMode.FEATURE_ID, SetRatchetControlMode.VERSION, SetRatchetControlMode.FUNCTION_INDEX):
                SetRatchetControlMode,
            # 0x2111 SmartShift 3G/EPM wheel with tunable torque
            **SmartShiftTunableModel.get_available_responses_map(),
            # 0x2121 HiRes Wheel
            **HiResWheelModel.get_available_responses_map(),
            # 0x2130 Ratchet Wheel
            **RatchetWheelModel.get_available_responses_map(),
            # 0x2150 Thumbwheel
            **ThumbwheelModel.get_available_responses_map(),
            # 0x2201 Adjustable DPI
            **AdjustableDpiModel.get_available_responses_map(),
            # 0x2202 Extended Adjustable DPI
            **ExtendedAdjustableDpiModel.get_available_responses_map(),
            # 0x2250 Analysis Mode
            **AnalysisModeModel.get_available_responses_map(),
            # 0x2251 Mouse Wheel Analytics
            **MouseWheelAnalyticsModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Keyboard ---------------------------------------------------------------------------------------------
            # 0x40A3 Fn Inversion for Multi-Host Devices
            **FnInversionForMultiHostDevicesModel.get_available_responses_map(),
            # 0x4220 Lock Key State
            **LockKeyStateModel.get_available_responses_map(),
            # 0x4521 Disable Keys
            **DisableKeysModel.get_available_responses_map(),
            # 0x4522 Disable Keys By Usage
            **DisableKeysByUsageModel.get_available_responses_map(),
            # 0x4523 Disable Controls By CIDX
            **DisableControlsByCIDXModel.get_available_responses_map(),
            # 0x4531 Multi Platform
            **MultiPlatformModel.get_available_responses_map(),
            # 0x4540 Keyboard International Layouts
            **KeyboardInternationalLayoutsModel.get_available_responses_map(),
            # 0x4610 Multi Roller
            **MultiRollerModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Touchpad ---------------------------------------------------------------------------------------------
            # 0x6100 Touchpad Raw XY
            **TouchpadRawXYModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Gaming -----------------------------------------------------------------------------------------------
            # 0x8010 Gaming G Keys
            **GamingGKeysModel.get_available_responses_map(),
            # 0x8030 MacroRecord key
            **MacroRecordkeyModel.get_available_responses_map(),
            # 0x8040 Brightness Control
            **BrightnessControlModel.get_available_responses_map(),
            # 0x8051 Logi Modifiers
            **LogiModifiersModel.get_available_responses_map(),
            # 0x8060 Report Rate
            **ReportRateModel.get_available_responses_map(),
            # 0x8061 Extended Adjustable Report Rate
            **ExtendedAdjustableReportRateModel.get_available_responses_map(),
            # 0x8071 RGB Effects
            **RGBEffectsModel.get_available_responses_map(),
            # 0x8081 PerKey Lighting
            **PerKeyLightingModel.get_available_responses_map(),
            # 0x8090 Mode Status
            **ModeStatusModel.get_available_responses_map(),
            # 0x80A4 Axis Response Curve
            **AxisResponseCurveModel.get_available_responses_map(),
            # 0x80D0 Combined Pedals
            **CombinedPedalsModel.get_available_responses_map(),
            # 0x8100 Onboard Profiles
            **OnboardProfilesModel.get_available_responses_map(),
            # 0x8101 Profile Management
            **ProfileManagementModel.get_available_responses_map(),
            # 0x8110 Mouse Button Spy
            **MouseButtonSpyModel.get_available_responses_map(),
            # 0x8134 Brake Force
            **BrakeForceModel.get_available_responses_map(),
            # 0x8135 Pedal Status
            **PedalStatusModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Peripheral -------------------------------------------------------------------------------------------
            # 0x9001 PMW3816 and PMW3826
            **PMW3816andPMW3826Model.get_available_responses_map(),
            # 0x9205 MLX903xx
            **MLX903xxModel.get_available_responses_map(),
            # 0x9209 MLX 90393 Multi Sensor
            **MLX90393MultiSensorModel.get_available_responses_map(),
            # 0x9215 Ads 1231
            **Ads1231Model.get_available_responses_map(),
            # 0x92E2 Test Keys Display
            **TestKeysDisplayModel.get_available_responses_map(),
            # ----------------------------------------------------------------------------------------------------------

            # Error commands
            (Hidpp1ErrorCodes.FEATURE_ID, Hidpp1ErrorCodes.VERSION, Hidpp1ErrorCodes.FUNCTION_INDEX): Hidpp1ErrorCodes,
            (ErrorCodes.FEATURE_ID, ErrorCodes.VERSION, ErrorCodes.FUNCTION_INDEX): ErrorCodes,
        }

        self._event_table = {
            # --- Common -----------------------------------------------------------------------------------------------
            # 0x0008 Keep Alive Feature
            **KeepAliveModel.get_available_events_map(),
            # 0x00C3 Secure DFU Control
            **SecureDfuControlModel.get_available_events_map(),
            # 0x00D0 DFU
            **DfuModel.get_available_events_map(),
            # 0x1000 Battery Unified Level Status
            (BatteryEvent.FEATURE_ID, BatteryEvent.VERSION, BatteryEvent.FUNCTION_INDEX): BatteryEvent,
            # 0x1004 Unified Battery
            **UnifiedBatteryModel.get_available_events_map(),
            # 0x1500 Force Pairing
            **ForcePairingModel.get_available_events_map(),
            # 0x18B0 Monitor Mode
            **StaticMonitorModeModel.get_available_events_map(),
            # 0x1982 Backlight
            **BacklightModel.get_available_events_map(),
            # 0x1B04 Keyboard Reprogrammable Keys and Mouse Buttons
            **SpecialKeysMSEButtonsModel.get_available_events_map(),
            # 0x1B05 Full Key Customization
            **FullKeyCustomizationModel.get_available_events_map(),
            # 0x1B08 Analog Keys
            **AnalogKeysModel.get_available_events_map(),
            # 0x1D4B Wireless Device Status
            (WirelessDeviceStatusBroadcastEvent.FEATURE_ID, WirelessDeviceStatusBroadcastEvent.VERSION,
             WirelessDeviceStatusBroadcastEvent.FUNCTION_INDEX): WirelessDeviceStatusBroadcastEvent,
            # ----------------------------------------------------------------------------------------------------------

            # --- Mouse ------------------------------------------------------------------------------------------------
            # 0x2121 HiRes Wheel
            **HiResWheelModel.get_available_events_map(),
            # 0x2130 Ratchet Wheel
            **RatchetWheelModel.get_available_events_map(),
            # 0x2150 Thumbwheel
            **ThumbwheelModel.get_available_events_map(),
            # 0x2202 Extended Adjustable DPI
            **ExtendedAdjustableDpiModel.get_available_events_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Keyboard ---------------------------------------------------------------------------------------------
            # 0x40A3 Fn Inversion for Multi-Host Devices
            **FnInversionForMultiHostDevicesModel.get_available_events_map(),
            # 0x4220 Lock Key State
            **LockKeyStateModel.get_available_events_map(),
            # 0x4523 Disable Controls By CIDX
            **DisableControlsByCIDXModel.get_available_events_map(),
            # 0x4531 Multi Platform
            **MultiPlatformModel.get_available_events_map(),
            # 0x4610 Multi Roller
            **MultiRollerModel.get_available_events_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Touchpad ---------------------------------------------------------------------------------------------
            # 0x6100 Touchpad Raw XY
            **TouchpadRawXYModel.get_available_events_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Gaming -----------------------------------------------------------------------------------------------
            # 0x8030 MacroRecord key
            **MacroRecordkeyModel.get_available_events_map(),
            # 0x8040 Brightness Control
            **BrightnessControlModel.get_available_events_map(),
            # 0x8051 Logi Modifiers
            **LogiModifiersModel.get_available_events_map(),
            # 0x8061 Extended Adjustable Report Rate
            **ExtendedAdjustableReportRateModel.get_available_events_map(),
            # 0x8071 RGB Effects
            **RGBEffectsModel.get_available_events_map(),
            # 0x8090 Mode Status
            **ModeStatusModel.get_available_events_map(),
            # 0x80A4 Axis Respone Curve
            **AxisResponseCurveModel.get_available_events_map(),
            # 0x80D0 Combined Pedals
            **CombinedPedalsModel.get_available_events_map(),
            # 0x8100 Onboard Profiles
            **OnboardProfilesModel.get_available_events_map(),
            # 0x8101 Profile Management
            **ProfileManagementModel.get_available_events_map(),
            # 0x8134 Brake Force
            **BrakeForceModel.get_available_events_map(),
            # ----------------------------------------------------------------------------------------------------------

            # --- Peripheral -------------------------------------------------------------------------------------------
            # 0x9001 PMW3816 and PMW3826
            **PMW3816andPMW3826Model.get_available_events_map(),
            # 0x9205 MLX903xx
            **MLX903xxModel.get_available_events_map(),
            # 0x9209 MLX 90393 Multi Sensor
            **MLX90393MultiSensorModel.get_available_events_map(),
            # 0x9215 Ads 1231
            **Ads1231Model.get_available_events_map(),
            # 0x92E2 Test Keys Display
            **TestKeysDisplayModel.get_available_events_map(),
            # ----------------------------------------------------------------------------------------------------------
        }

        self._receiver_response_table = Hidpp1Model.get_available_responses_map()

        self._receiver_event_table = Hidpp1Model.get_available_events_map()

        # Feature index to feature id mapping
        self._feature_index_to_id = {
            Hidpp1ErrorCodes.ERROR_TAG: (Hidpp1ErrorCodes.FEATURE_ID, Hidpp1ErrorCodes.VERSION[0]),
            ErrorCodes.ERROR_TAG: (ErrorCodes.FEATURE_ID, ErrorCodes.VERSION[0])
        }

        # --------------------------------------------------------------------------------------------------------------
        # VLP Section
        # --------------------------------------------------------------------------------------------------------------
        self._vlp_features_table = {
            # 0x0102 VLP Root
            **VLPRootModel.get_available_responses_map(),

            # 0x0103 VLP Feature Set
            **VLPFeatureSetModel.get_available_responses_map(),

            # 0x19A1 Contextual Display
            **ContextualDisplayModel.get_available_responses_map(),

            # Error commands
            (ErrorCodes.FEATURE_ID, ErrorCodes.VERSION, ErrorCodes.FUNCTION_INDEX): ErrorCodes,
        }

        self._vlp_event_table = {
            # 0x19A1 Contextual Display
            **ContextualDisplayModel.get_available_events_map(),
        }

        self._vlp_feature_index_to_id = {
            ErrorCodes.ERROR_TAG: (ErrorCodes.FEATURE_ID, ErrorCodes.VERSION[0]),
        }
        # --------------------------------------------------------------------------------------------------------------
        # End of VLP Section
        # --------------------------------------------------------------------------------------------------------------

        # List of all active handlers
        self._handlers = []
        # Pre-register queue for features
        self.queue_list = []

        # First declaration of queues before being initialized in ``init_feature_message_queues``
        self.important_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.IMPORTANT)
        self.common_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.COMMON)
        self.mouse_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.MOUSE)
        self.keyboard_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.KEYBOARD)
        self.touchpad_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.TOUCHPAD)
        self.gaming_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.GAMING)
        self.peripheral_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.PERIPHERAL)
        self.interface_descriptor_queue = HidMessageQueue(name=HIDDispatcher.QueueName.INTERFACE_DESCRIPTOR)
        self.event_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.EVENT)
        self.battery_event_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.BATTERY_EVENT)
        self.error_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.ERROR)
        self.hid_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.HID)
        self.receiver_error_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.RECEIVER_ERROR)
        self.receiver_response_queue = HidMessageQueue(name=HIDDispatcher.QueueName.RECEIVER_RESPONSE)
        self.receiver_event_queue = HidMessageQueue(name=HIDDispatcher.QueueName.RECEIVER_EVENT)
        self.receiver_connection_event_queue = HidMessageQueue(name=HIDDispatcher.QueueName.RECEIVER_CONNECTION_EVENT)
        self.vlp_important_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.VLP_IMPORTANT)
        self.vlp_common_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.VLP_COMMON)
        self.vlp_event_message_queue = HidMessageQueue(name=HIDDispatcher.QueueName.VLP_EVENT)

        # Initialize features queues
        self.init_feature_message_queues()

        # Default queue to store all uncaught messages
        self.default_message_queue = HidMessageQueue(name="Default Queue")

        # Initialize sequence number
        self.msg_sequence_number = 0

        # Initialize device collections
        self.mouse_collections = None
        self.keyboard_collections = None
        self.digitizer_collections = None

        # Initialize report_id_list per interface
        self.mouse_report_id_list = []
        self.keyboard_report_id_list = []
        self.digitizer_report_id_list = []
        self.is_ready = False
    # end def __init__

    def init_feature_message_queues(self):
        """
        Update queues to store messages by feature.
        """
        # HID++ Important messages
        accepted_messages = (
            # 0x0000 IRoot
            RootModel.get_available_responses_classes() +
            # 0x0001 IFeatureSet
            FeatureSetModel.get_available_responses_classes()
        )
        self.important_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.important_message_queue)

        # HID++ Common messages
        accepted_messages = (
            # 0x0003 Device Information
            DeviceInformationModel.get_available_responses_classes() +
            # 0x0005 Device Name and Type
            DeviceTypeAndNameModel.get_available_responses_classes() +
            # 0x0007 Device Friendly Name
            DeviceFriendlyNameModel.get_available_responses_classes() +
            # 0x0008 Keep Alive
            KeepAliveModel.get_available_responses_classes() +
            # 0x0011 Property Access
            PropertyAccessModel.get_available_responses_classes() +
            # 0x0020 Config Change
            (ConfigCookie, ConfigComplete,) +
            # 0x0021 32 Byte Unique (Random) Identifier
            (GetByte0To15, GetByte16To31, RegenId,) +
            # 0x00C2 DFU Control
            DfuControlModel.get_available_responses_classes() +
            # 0x00C3 Secure DFU Control
            SecureDfuControlModel.get_available_responses_classes() +
            # 0x00D0 DFU
            DfuModel.get_available_responses_classes() +
            # 0x1000 Battery Unified Level Status
            (BatteryLevel, BatteryCapability, BatteryStatus,) +
            # 0x1004 Unified Battery
            UnifiedBatteryModel.get_available_responses_classes() +
            # 0x1500 Force Pairing
            ForcePairingModel.get_available_responses_classes() +
            # 0x1602 Password Authentication
            PasswordAuthenticationModel.get_available_responses_classes() +
            # 0x1801 Manufacturing Mode
            ManufacturingModeModel.get_available_responses_classes() +
            # 0x1803 GPIO Access
            GpioAccessModel.get_available_responses_classes() +
            # 0x1805 OOB State
            OobStateModel.get_available_responses_classes() +
            # 0x1806 Configurable Device Properties
            ConfigurableDevicePropertiesModel.get_available_responses_classes() +
            # 0x1807 Configurable Properties
            ConfigurablePropertiesModel.get_available_responses_classes() +
            # 0x180B Configurable Device Registers
            ConfigurableDeviceRegistersModel.get_available_responses_classes() +
            # 0x1811 Equad Pairing Encryption
            EquadPairingEncModel.get_available_responses_classes() +
            # 0x1814 Change Host
            ChangeHostModel.get_available_responses_classes() +
            # 0x1815 Hosts Info
            HostsInfoModel.get_available_responses_classes() +
            # 0x1816 Ble Pro Pairing
            BleProPrepairingModel.get_available_responses_classes() +
            # 0x1817 Lightspeed Prepairing
            LightspeedPrepairingModel.get_available_responses_classes() +
            # 0x1830 Power Modes
            PowerModesModel.get_available_responses_classes() +
            # 0x1861 Battery Levels Calibration
            BatteryLevelsCalibrationModel.get_available_responses_classes() +
            # 0x1876 Optical Switches
            OpticalSwitchesModel.get_available_responses_classes() +
            # 0x1890 RF Test
            RFTestModel.get_available_responses_classes() +
            # 0x1891 RF Test BLE
            RFTestBLEModel.get_available_responses_classes() +
            # 0x18B0 Monitor Mode
            StaticMonitorModeModel.get_available_responses_classes() +
            # 0x18A1 LED Test
            LEDTestModel.get_available_responses_classes() +
            # 0x1982 Backlight
            BacklightModel.get_available_responses_classes() +
            # 0x19C0 Force Sensing Button
            ForceSensingButtonModel.get_available_responses_classes() +
            # 0x1B04 Keyboard Reprogrammable Keys and Mouse Buttons
            SpecialKeysMSEButtonsModel.get_available_responses_classes() +
            # 0x1B05 Full Key Customization
            FullKeyCustomizationModel.get_available_responses_classes() +
            # 0x1B08 Analog Keys
            AnalogKeysModel.get_available_responses_classes() +
            # 0x1B10 Control List
            ControlListModel.get_available_responses_classes() +
            # 0x1DF3 - EquadDJ Debug Info
            (ReadEquadDJDebugInfo, WriteEquadDJDebugInfo,) +
            # 0x1E00 Enable Hidden Features
            (GetHidden, SetHidden,) +
            # 0x1E01 Manage Deactivatable Features
            ManageDeactivatableFeaturesModel.get_available_responses_classes() +
            # 0x1E02 Manage Deactivatable Features
            ManageDeactivatableFeaturesAuthModel.get_available_responses_classes() +
            # 0x1E22 SPI Direct Access
            SPIDirectAccessModel.get_available_responses_classes() +
            # 0x1E30 I2C Direct Access
            I2CDirectAccessModel.get_available_responses_classes() +
            # 0x1EB0 TDE Access To Non-Volatile Memory
            TdeAccessToNvmModel.get_available_responses_classes() +
            # 0x1F30 Temperature Measurement
            TemperatureMeasurementModel.get_available_responses_classes()
        )
        self.common_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.common_message_queue)

        # HID++ Mouse messages
        accepted_messages = (
            # 0x2100 Vertical Scrolling
            (GetRollerInfo,) +
            # 0x2110 Smart Shift
            (GetRatchetControlMode, SetRatchetControlMode,) +
            # 0x2111 SmartShift 3G/EPM wheel with tunable torque
            SmartShiftTunableModel.get_available_responses_classes() +
            # 0x2121 HiRes Wheel
            HiResWheelModel.get_available_responses_classes() +
            # 0x2130 Ratchet Wheel
            RatchetWheelModel.get_available_responses_classes() +
            # 0x2150 Thumbwheel
            ThumbwheelModel.get_available_responses_classes() +
            # 0x2201 Adjustable DPI
            AdjustableDpiModel.get_available_responses_classes() +
            # 0x2202 Extended Adjustable DPI
            ExtendedAdjustableDpiModel.get_available_responses_classes() +
            # 0x2250 Analysis Mode
            AnalysisModeModel.get_available_responses_classes() +
            # 0x2251 Mouse Wheel Analytics
            MouseWheelAnalyticsModel.get_available_responses_classes()
        )
        self.mouse_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.mouse_message_queue)

        # HID++ Keyboard messages
        accepted_messages = (
            # 0x40A3 Fn Inversion for Multi-Host Devices
            FnInversionForMultiHostDevicesModel.get_available_responses_classes() +
            # 0x4220 Lock Key State
            LockKeyStateModel.get_available_responses_classes() +
            # 0x4521 Disable Keys
            DisableKeysModel.get_available_responses_classes() +
            # 0x4522 Disable Keys By Usage
            DisableKeysByUsageModel.get_available_responses_classes() +
            # 0x4523 Disable Controls By CIDX
            DisableControlsByCIDXModel.get_available_responses_classes() +
            # 0x4531 Multi Platform
            MultiPlatformModel.get_available_responses_classes() +
            # 0x4540 Keyboard International Layouts
            KeyboardInternationalLayoutsModel.get_available_responses_classes() +
            # 0x4610 Multi Roller
            MultiRollerModel.get_available_responses_classes()
        )
        self.keyboard_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.keyboard_message_queue)

        # HID++ Touchpad messages
        accepted_messages = (
            # 0x6100 Touchpad Raw XY
            TouchpadRawXYModel.get_available_responses_classes()
        )
        self.touchpad_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.touchpad_message_queue)

        # HID++ Gaming messages
        accepted_messages = (
            # 0x8010 Gaming G Keys
            GamingGKeysModel.get_available_responses_classes() +
            # 0x8030 MacroRecord key
            MacroRecordkeyModel.get_available_responses_classes() +
            # 0x8040 Brightness Control
            BrightnessControlModel.get_available_responses_classes() +
            # 0x8051 Logi Modifiers
            LogiModifiersModel.get_available_responses_classes() +
            # 0x8060 Report Rate
            ReportRateModel.get_available_responses_classes() +
            # 0x8061 Extended Adjustable Report Rate
            ExtendedAdjustableReportRateModel.get_available_responses_classes() +
            # 0x8071 RGB Effects
            RGBEffectsModel.get_available_responses_classes() +
            # 0x8081 PerKey Lighting
            PerKeyLightingModel.get_available_responses_classes() +
            # 0x8090 Mode Status
            ModeStatusModel.get_available_responses_classes() +
            # 0x80A4 Axis Response Curve
            AxisResponseCurveModel.get_available_responses_classes() +
            # 0x80D0 Combined Pedals
            CombinedPedalsModel.get_available_responses_classes() +
            # 0x8100 Onboard Profiles
            OnboardProfilesModel.get_available_responses_classes() +
            # 0x8101 Profile Management
            ProfileManagementModel.get_available_responses_classes() +
            # 0x8110 Mouse Button Spy
            MouseButtonSpyModel.get_available_responses_classes() +
            # 0x8134 Brake Force
            BrakeForceModel.get_available_responses_classes() +
            # 0x8135 Pedal Status
            PedalStatusModel.get_available_responses_classes()
        )
        self.gaming_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.gaming_message_queue)

        # HID++ Peripheral messages
        accepted_messages = (
            # 0x9001 PMW3816 and PMW3826
            PMW3816andPMW3826Model.get_available_responses_classes() +
            # 0x9205 MLX903xx
            MLX903xxModel.get_available_responses_classes() +
            # 0x9209 MLX 90393 Multi Sensor
            MLX90393MultiSensorModel.get_available_responses_classes() +
            # 0x9215 Ads 1231
            Ads1231Model.get_available_responses_classes() +
            # 0x92E2 Test Keys Display
            TestKeysDisplayModel.get_available_responses_classes()
        )
        self.peripheral_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.peripheral_message_queue)

        # Interface configuration descriptor messages
        self.interface_descriptor_queue.update_accepted_messages(accepted_messages=(ReportDescriptor,))
        self.queue_list.append(self.interface_descriptor_queue)

        # HID++ Event messages
        accepted_messages = (
            # --- Common -----------------------------------------------------------------------------------------------
            # 0x0008 Keep Alive
            KeepAliveModel.get_available_events_classes() +
            # 0x00C2 DFU Control
            DfuModel.get_available_events_classes() +
            # 0x00C3 Secure DFU Control
            SecureDfuControlModel.get_available_events_classes() +
            # 0x1500 Force Pairing
            ForcePairingModel.get_available_events_classes() +
            # 0x18B0 Monitor Mode
            StaticMonitorModeModel.get_available_events_classes() +
            # 0x1982 Backlight
            BacklightModel.get_available_events_classes() +
            # 0x1B04 Keyboard Reprogrammable Keys and Mouse Buttons
            SpecialKeysMSEButtonsModel.get_available_events_classes() +
            # 0x1B05 Full Key Customization
            FullKeyCustomizationModel.get_available_events_classes() +
            # 0x1B08 Analog Keys
            AnalogKeysModel.get_available_events_classes() +
            # 0x1D4B Wireless Device Status
            (WirelessDeviceStatusBroadcastEvent,) +
            # ----------------------------------------------------------------------------------------------------------

            # --- Mouse ------------------------------------------------------------------------------------------------
            # 0x2121 HiRes Wheel
            HiResWheelModel.get_available_events_classes() +
            # 0x2130 Ratchet Wheel
            RatchetWheelModel.get_available_events_classes() +
            # 0x2150 Thumbwheel
            ThumbwheelModel.get_available_events_classes() +
            # 0x2202 Extended Adjustable DPI
            ExtendedAdjustableDpiModel.get_available_events_classes() +
            # ----------------------------------------------------------------------------------------------------------

            # --- Keyboard ---------------------------------------------------------------------------------------------
            # 0x40A3 Fn Inversion for Multi-Host Devices
            FnInversionForMultiHostDevicesModel.get_available_events_classes() +
            # 0x4220 Lock Key State
            LockKeyStateModel.get_available_events_classes() +
            # 0x4523 Disable Controls By CIDX
            DisableControlsByCIDXModel.get_available_events_classes() +
            # 0x4531 Multi Platform
            MultiPlatformModel.get_available_events_classes() +
            # 0x4610 Multi Roller
            MultiRollerModel.get_available_events_classes() +
            # ----------------------------------------------------------------------------------------------------------

            # --- Touchpad ---------------------------------------------------------------------------------------------
            # 0x6100 Touchpad Raw XY
            TouchpadRawXYModel.get_available_events_classes() +
            # ----------------------------------------------------------------------------------------------------------

            # --- Gaming -----------------------------------------------------------------------------------------------
            # 0x8030 MacroRecord key
            MacroRecordkeyModel.get_available_events_classes() +
            # 0x8040 Brightness Control
            BrightnessControlModel.get_available_events_classes() +
            # 0x8051 Logi Modifiers
            LogiModifiersModel.get_available_events_classes() +
            # 0x8061 Extended Adjustable Report Rate
            ExtendedAdjustableReportRateModel.get_available_events_classes() +
            # 0x8071 RGB Effects
            RGBEffectsModel.get_available_events_classes() +
            # 0x8090 Mode Status
            ModeStatusModel.get_available_events_classes() +
            # 0x80D0 Combined Pedals
            CombinedPedalsModel.get_available_events_classes() +
            # 0x80A4 Axis Response Curve
            AxisResponseCurveModel.get_available_events_classes() +
            # 0x8100 Onboard Profiles
            OnboardProfilesModel.get_available_events_classes() +
            # 0x8101 Profile Management
            ProfileManagementModel.get_available_events_classes() +
            # 0x8134 Brake Force
            BrakeForceModel.get_available_events_classes() +
            # ----------------------------------------------------------------------------------------------------------

            # --- Peripheral -------------------------------------------------------------------------------------------
            # 0x9001 PMW3816 and PMW3826
            PMW3816andPMW3826Model.get_available_events_classes() +
            # 0x9205 MLX903xx
            MLX903xxModel.get_available_events_classes() +
            # 0x9215 Ads 1231
            Ads1231Model.get_available_events_classes() +
            # 0x92E2 Test Keys Display
            TestKeysDisplayModel.get_available_events_classes()
            # ----------------------------------------------------------------------------------------------------------
        )
        self.event_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.event_message_queue)

        # HID++ Battery Event messages
        accepted_messages = (
            # 0x1000 Battery Unified Level Status
            (BatteryEvent,) +
            # 0x1004 Unified Battery
            UnifiedBatteryModel.get_available_events_classes()
        )
        self.battery_event_message_queue.update_accepted_messages(accepted_messages=accepted_messages)
        self.queue_list.append(self.battery_event_message_queue)

        # HID++ Error messages
        self.error_message_queue.update_accepted_messages(accepted_messages=(ErrorCodes,))
        self.queue_list.append(self.error_message_queue)

        # HID++ Error messages
        self.receiver_error_message_queue.update_accepted_messages(accepted_messages=(Hidpp1ErrorCodes,))
        self.queue_list.append(self.receiver_error_message_queue)

        # HID messages
        self.hid_message_queue.update_accepted_messages(accepted_messages=(
            HidCallStateManagementControl, HidConsumer, HidDigitizer, HidKeyboard, HidKeyboardBitmap, HidMouse,
            HidSystemControl))
        self.queue_list.append(self.hid_message_queue)

        # Receiver responses
        self.receiver_response_queue.update_accepted_messages(
            accepted_messages=Hidpp1Model.get_available_responses_classes())
        self.queue_list.append(self.receiver_response_queue)

        # Receiver events
        self.receiver_event_queue.update_accepted_messages(
            accepted_messages=Hidpp1Model.get_available_events_classes())
        self.queue_list.append(self.receiver_event_queue)

        # Special queue for Receiver connection events
        self.receiver_connection_event_queue.update_accepted_messages(
            accepted_messages=Hidpp1Model.get_connection_events_classes())
        self.queue_list.append(self.receiver_connection_event_queue)

        # --------------------------------------------------------------------------------------------------------------
        # VLP Queues Section
        # --------------------------------------------------------------------------------------------------------------
        accepted_messages = (
            # 0x0102 VLP Root
            VLPRootModel.get_available_responses_classes(),
            # 0x0103 VLP Feature Set
            VLPFeatureSetModel.get_available_responses_classes(),
        )
        self.vlp_important_message_queue.update_accepted_messages(accepted_messages)

        accepted_messages = (
            # 0x19A1 Contextual Display
            ContextualDisplayModel.get_available_responses_classes()
        )
        self.vlp_common_message_queue.update_accepted_messages(accepted_messages)

        accepted_messages = (
            # 0x19A1 Contextual Display
            ContextualDisplayModel.get_available_events_classes()
        )
        self.vlp_event_message_queue.update_accepted_messages(accepted_messages)

        self.queue_list.append(self.vlp_important_message_queue)
        self.queue_list.append(self.vlp_common_message_queue)
        self.queue_list.append(self.vlp_event_message_queue)

        for my_queue in self.queue_list:
            self.add_handler(my_queue)
        # end for
    # end def init_feature_message_queues

    def clear_feature_entries(self, table=None):
        """
        Clear all entries into the mapping

        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``
        """
        table = self._feature_index_to_id if table is None else table
        table.clear()
        # Feature index to feature id mapping
        table.update({
            Hidpp1ErrorCodes.ERROR_TAG: (Hidpp1ErrorCodes.FEATURE_ID, Hidpp1ErrorCodes.VERSION[0]),
            ErrorCodes.ERROR_TAG: (ErrorCodes.FEATURE_ID, ErrorCodes.VERSION[0])
        })
    # end def clear_feature_entries

    def add_feature_entry(self, feature_index, feature_id, feature_version, table=None):
        """
        Add an entry into the mapping

        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param feature_id: Feature Identifier
        :type feature_id: ``int``
        :param feature_version: Version of the feature
        :type feature_version: ``int``
        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``
        """
        table = self._feature_index_to_id if table is None else table
        value = (int(Numeral(feature_id)), int(Numeral(feature_version)))
        # Delete entry in table if value already in dict to keep uniqueness
        # If a value is already in the dict then 2 feature index can be associated to a feature id.
        # This can happen if the firmware of a device changes (e.g. after a DFU) and the features changes.
        # So it is safer to delete before adding.
        if value in table.values():
            del table[list(table.keys())[list(table.values()).index(value)]]
        # end if
        table[int(feature_index)] = value
    # end def add_feature_entry

    def add_vlp_feature_entry(self, feature_index, feature_id, feature_version, table=None):
        """
        Add an entry into the VLP feature mapping

        :param feature_index: Feature Index
        :type feature_index: ``int``
        :param feature_id: Feature Identifier
        :type feature_id: ``int``
        :param feature_version: Version of the feature
        :type feature_version: ``int``
        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``
        """
        table = self._vlp_feature_index_to_id if table is None else table
        value = (int(Numeral(feature_id)), int(Numeral(feature_version)))
        # Delete entry in table if value already in dict to keep uniqueness
        # If a value is already in the dict then 2 feature index can be associated to a feature id.
        # This can happen if the firmware of a device changes (e.g. after a DFU) and the features changes.
        # So it is safer to delete before adding.
        if value in table.values():
            del table[list(table.keys())[list(table.values()).index(value)]]
        # end if
        table[int(feature_index)] = value
    # end def add_vlp_feature_entry

    def get_feature_entry_by_index(self, feature_index, table=None):
        """
        Get an entry from the mapping by its index

        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``

        :return: Feature entry in the table
        :rtype: ``tuple``

        :raise ``KeyError``: If feature_index is unknown
        """
        table = self._feature_index_to_id if table is None else table
        feature_index = int(Numeral(feature_index))
        if feature_index not in table:
            raise KeyError(f"The feature index {feature_index} is not in feature index to id table")
        # end if
        return table[feature_index]
    # end def get_feature_entry_by_index

    def get_vlp_feature_entry_by_index(self, feature_index, table=None):
        """
        Get an entry from the mapping by its index

        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``

        :return: Feature entry in the table
        :rtype: ``tuple``

        :raise ``KeyError``: If feature_index is unknown
        """
        table = self._vlp_feature_index_to_id if table is None else table
        feature_index = int(Numeral(feature_index))
        if feature_index not in table:
            raise KeyError(f"The feature index {feature_index} is not in VLP feature index to id table")
        # end if
        return table[feature_index]
    # end def get_vlp_feature_entry_by_index

    def get_feature_index(self, feature_id, table=None):
        """
        Get feature index from feature id in feature index to id table

        :param feature_id: Feature ID
        :type feature_id: ``int`` or ``HexList``
        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``

        :return: Feature index
        :rtype: ``int``
        """
        table = self._feature_index_to_id if table is None else table
        feature_id = int(Numeral(feature_id))
        id_to_idx = {value[0]: index for index, value in table.items()}
        return id_to_idx[feature_id] if feature_id in id_to_idx else None
    # end def get_feature_index

    def get_vlp_feature_index(self, feature_id, table=None):
        """
        Get VLP feature index from feature id in feature index to id table

        :param feature_id: Feature ID
        :type feature_id: ``int`` or ``HexList``
        :param table: Feature index to id table - OPTIONAL
        :type table: ``dict`` or ``None``

        :return: Feature index
        :rtype: ``int``
        """
        table = self._vlp_feature_index_to_id if table is None else table
        feature_id = int(Numeral(feature_id))
        id_to_idx = {value[0]: index for index, value in table.items()}
        return id_to_idx[feature_id] if feature_id in id_to_idx else None
    # end def get_vlp_feature_index

    @synchronized(SYNCHRONIZATION_LOCK)
    def add_handler(self, handler):
        """
        Add a handler to the list

        :param handler: Handler to add
        :type handler: ``AbstractHIDMessageHandler``
        """
        self._handlers.append(handler)
    # end def add_handler

    @synchronized(SYNCHRONIZATION_LOCK)
    def remove_handler(self, handler):
        """
        Remove a handler from the list (if in the list)

        :param handler: Handler to remove
        :type handler: ``AbstractHIDMessageHandler``
        """
        if handler in self._handlers:
            self._handlers.remove(handler)
        # end if
    # end def remove_handler

    @synchronized(SYNCHRONIZATION_LOCK)
    def remove_all_handlers(self):
        """
        Remove all handlers from the list
        """
        self._handlers.clear()
    # end def remove_all_handlers

    def get_queue_by_name(self, name):
        """
        Get the queue by given name

        :param name: Name of the queue
        :type name: ``str``

        :return: Queue
        :rtype: ``HidMessageQueue``
        """
        for queue in self.queue_list:
            if queue.name == name:
                return queue
            # end if
        # end for
    # end def get_queue_by_name

    @synchronized(SYNCHRONIZATION_LOCK)
    def process_interrupt_hidpp(self, transport_message):
        """
        Process on reception of an interrupt for HID++ interface:
          - message is read from interrupt
          - message is sent to handlers that accept it

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The queue where the message has been put in or None if the given message could not be treated
        :rtype: ``HidMessageQueue`` or ``None``
        """
        if len(transport_message.data) == 0:
            return None
        # end if

        # Get potential reportId from usb message
        report_id = transport_message.data[0]
        report_len = len(transport_message.data)

        # Check message type
        if report_id in HidppMessage.HIDPP_REPORT_ID_LIST and report_len in HidppMessage.HIDPP_REPORT_LEN_LIST:
            hid_message = self.get_response_message(transport_message=transport_message)
            return self._post_message_process(message=hid_message)
        elif report_id in VlpMessage.REPORT_ID_LIST:
            vlp_message = self.get_vlp_message(transport_message=transport_message)
            return self._post_message_process(message=vlp_message)
            # TODO - remove the 3 following conditions after executing a full regression run
        elif report_id in self.mouse_report_id_list:
            return self.process_interrupt_hid_mouse(transport_message=transport_message)
        elif report_id in self.keyboard_report_id_list:
            return self.process_interrupt_hid_keyboard(transport_message=transport_message)
        elif report_id in self.digitizer_report_id_list:
            return self.process_interrupt_hid_digitizer(transport_message=transport_message)
        # end if
    # end def process_interrupt_hidpp

    def get_hidpp1_message(self, transport_message):
        """
        Check if message is a receiver notification but without device_index = 0xFF.
        According to https://sites.google.com/a/logitech.com/samarkand/appendix/hid-2-0-protocol-definition,
        some feature_index can be sent by the receiver in HID++ 1 with the index matching the device and not
        the receiver one (0xFF): 64 (0x40), 65 (0x41), 73 (0x49), 75 (0x4B), 143 (0x8F)

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The Hid++ message
        :rtype: ``HidMessage`` or ``None``
        """
        message = None

        data = transport_message.data
        if len(data) > Hidpp1Data.Offset.SUB_ID:
            sub_id = data[Hidpp1Data.Offset.SUB_ID]
            message_class = None
            r0 = None

            if sub_id in Hidpp1Model.get_register_sub_ids():
                address = data[Hidpp1Data.Offset.REGISTER_ADDRESS]
                if Hidpp1Model.has_r0(address):
                    r0 = data[Hidpp1Data.Offset.REGISTER_R0]
                # end if
                message_class = Hidpp1Model.get_message_cls(sub_id, "response", address, r0)
            elif sub_id in self._receiver_event_table.keys():
                message_class = self._receiver_event_table[sub_id]
            # end if

            if message_class is not None:
                message = message_class.fromHexList(data, timestamp=transport_message.timestamp)
                transport_message.message_class = message_class
            # end if
        # end if

        return message
    # end def get_hidpp1_message

    @staticmethod
    def parse_hidpp2_header(data):
        """
        Get feature index, function index and software id from message data

        :param data: Transport message data
        :type data: ``HexList``

        :return: Feature index, function index and software id
        :rtype: ``tuple``
        """
        # Retrieve feature Index in current message
        feature_index = data[HidppMessage.OFFSET.FEATURE_INDEX]
        if feature_index not in [ErrorCodes.ERROR_TAG, Hidpp1ErrorCodes.ERROR_TAG]:
            # Retrieve function index in current message
            function_index = data[HidppMessage.OFFSET.FUNCTION_ID] >> 4
            # Retrieve software id in current message
            software_id = data[HidppMessage.OFFSET.SOFTWARE_ID] & 0xF
        else:
            # Force function id to 0
            function_index = ErrorCodes.FUNCTION_INDEX
            software_id = 0xF
        # end if
        return feature_index, function_index, software_id
    # end def parse_hidpp2_header

    def get_hidpp2_message_from_event(self, transport_message, index):
        """
        Get HID++ message instantiated from transport message data in case of an event received

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``
        :param index: Index in the feature index to id table
        :type index: ``tuple``

        :return: The Hid++ message
        :rtype: ``HidMessage`` or ``None``
        """
        message = None
        for (table_id, table_versions, table_index) in self._event_table.keys():
            # Try every possible version supported by the framework
            for ver in table_versions:
                # If one version is a perfect match, keep that one
                if (table_id, ver, table_index) == index:
                    message = self._event_table[(table_id, table_versions, table_index)].fromHexList(
                        transport_message.data, timestamp=transport_message.timestamp)
                    transport_message.message_class = self._event_table[
                        (table_id, table_versions, table_index)]
                    break
                # end if
            # end for
            if message is not None:
                # Entry found in the table, exit the loop
                break
            # end if
        # end for
        return message
    # end def get_hidpp2_message_from_event

    def get_hidpp2_message(self, transport_message):
        """
        Get HID++ message instantiated from transport message data

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The Hid++ message
        :rtype: ``HidMessage`` or ``None``
        """
        message = None
        message_class = None
        data = transport_message.data

        if len(data) > HidppMessage.OFFSET.SOFTWARE_ID:
            feature_index, function_index, software_id = self.parse_hidpp2_header(data)

            if feature_index in self._feature_index_to_id:
                feature_id, feature_version = self._feature_index_to_id[feature_index]
                if software_id == 0:
                    message_class = self.get_message_class(
                        self._event_table, feature_id, feature_version, function_index)
                # end if

                if message_class is None:
                    message_class = self.get_message_class(
                        self._feature_table, feature_id, feature_version, function_index)
                # end if

                if message_class is not None:
                    message = message_class.fromHexList(data, timestamp=transport_message.timestamp)
                    transport_message.message_class = message_class
                # end if
            # end if
        # end if
        return message
    # end def get_hidpp2_message

    def get_response_message(self, transport_message):
        """
        Instantiate and return an ``HidMessage`` based on the feature id, feature version and function id
        characteristics extracted from the transport message

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The Hid++ message
        :rtype: ``HidMessage`` or ``None``
        """
        message = self.get_hidpp1_message(transport_message)

        if message is None:
            message = self.get_hidpp2_message(transport_message)
        # end if

        return message
    # end def get_response_message

    @staticmethod
    def get_message_class(table, feature_id, feature_version, function_index):
        """
        Get message class matching feature id, feature version and function index in given table

        :param table: Features table
        :type table: ``dict``
        :param feature_id: Feature id
        :type feature_id: ``int``
        :param feature_version: Feature version
        :type feature_version: ``int``
        :param function_index: Function index
        :type function_index: ``int``

        :return: Matching message class
        :rtype: ``HidppMessage`` or ``VlpMessage`` or ``None``

        :raise ``KeyError``: If multiple entries match the feature characteristics
        """
        message_class = None
        features_table = table
        if (feature_id, feature_version, function_index) in features_table:
            message_class = features_table[(feature_id, feature_version, function_index)]
        else:
            match_keys = [key for key in features_table.keys()
                          if feature_id == key[0] and feature_version in key[1]
                          and function_index in ((key[2],) if isinstance(key[2], int) else key[2])]
            if len(match_keys) == 1:
                message_class = features_table[match_keys[0]]
            elif len(match_keys) > 1:
                raise KeyError(f"Too many matching entries in features table :\n"
                               f"Feature ID = {feature_id}, feature version = {feature_version}, function index = "
                               f"{function_index} is referenced {len(match_keys)} times")
            # end if
        # end if
        return message_class
    # end def get_message_class

    def get_vlp_message(self, transport_message):
        """
        Get VLP message instantiated from transport message data

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: VLP message if feature can be identified, else ``None``
        :rtype: ``VlpMessage`` or ``None``
        """
        vlp_message = None
        vlp_message_class = None
        data = transport_message.data

        if len(data) > VlpMessage.HEADER_SIZE // 8:
            vlp_message = VlpMessageRawPayload.fromHexList(data, timestamp=transport_message.timestamp)
            feature_index = to_int(vlp_message.feature_index)
            function_index = vlp_message.function_index
            software_id = vlp_message.software_id

            if feature_index in self._vlp_feature_index_to_id:
                feature_id, feature_version = self._vlp_feature_index_to_id[feature_index]
                if feature_index == ErrorCodes.ERROR_TAG or software_id != 0:
                    vlp_message_class = self.get_message_class(
                        self._vlp_features_table, feature_id, feature_version, function_index)
                else:
                    vlp_message_class = self.get_message_class(
                        self._vlp_event_table, feature_id, feature_version, function_index)
                # end if
            # end if
            if vlp_message_class is not None:
                transport_message.message_class = vlp_message_class
                vlp_message = vlp_message_class.fromHexList(data, timestamp=transport_message.timestamp)
            # end if
        # end if
        return vlp_message
    # end def get_vlp_message

    @synchronized(SYNCHRONIZATION_LOCK)
    def process_interrupt_hid_mouse(self, transport_message):
        """
        Process on reception of an interrupt for HID mouse interface:
          - message is read from interrupt
          - message is sent to handlers that accept it

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The queue where the message has been put in or None if the given message could not be treated
        :rtype: ``HidMessageQueue`` or ``None``
        """
        message = None

        if len(transport_message.data) == 0:
            return None
        # end if

        data, message_type = self.analyse_hid_message(usbmessage=transport_message, message_type=MessageType.HID_MOUSE)
        if message_type == MessageType.HID_MOUSE and data is not None:
            if len(data) == HidMouseNvidiaExtension.BITFIELD_LENGTH:
                message = HidMouseNvidiaExtension.fromHexList(data, timestamp=transport_message.timestamp)
                transport_message.message_class = HidMouseNvidiaExtension
            else:
                message = HidMouse.fromHexList(data, timestamp=transport_message.timestamp)
                transport_message.message_class = HidMouse
            # end if
        elif message_type == MessageType.HID_CONSUMER_CTRL and data is not None:
            message = HidConsumer.fromHexList(data, timestamp=transport_message.timestamp)
            transport_message.message_class = HidConsumer
        elif message_type == MessageType.HID_SYS_CTRL and data is not None:
            message = HidSystemControl.fromHexList(data, timestamp=transport_message.timestamp)
            transport_message.message_class = HidSystemControl
        elif message_type == MessageType.HID_CALL_STATE_MGT_CRTL and data is not None:
            message = HidCallStateManagementControl.fromHexList(data, timestamp=transport_message.timestamp)
            transport_message.message_class = HidCallStateManagementControl
        # end if

        if VERBOSE:
            stdout.write(f"{message}\n")
        # end if

        return self._post_message_process(message=message)
    # end def process_interrupt_hid_mouse

    @synchronized(SYNCHRONIZATION_LOCK)
    def process_interrupt_hid_keyboard(self, transport_message):
        """
        Process on reception of an interrupt for HID keyboard interface:
          - message is read from interrupt
          - message is sent to handlers that accept it

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The queue where the message has been put in or None if the given message could not be treated
        :rtype: ``HidMessageQueue`` or ``None``
        """
        message = None

        if len(transport_message.data) == 0:
            return None
        # end if

        # Check message type
        data, message_type = self.analyse_hid_message(transport_message, message_type=MessageType.HID_KEYBOARD)
        if message_type == MessageType.HID_KEYBOARD and data is not None:
            if len(data) == HidKeyboard.BITFIELD_LENGTH:
                message = HidKeyboard.fromHexList(data, timestamp=transport_message.timestamp)
                transport_message.message_class = HidKeyboard
            elif len(data) == HidKeyboardBitmap.BITFIELD_LENGTH:
                message = HidKeyboardBitmap.fromHexList(data, timestamp=transport_message.timestamp)
                transport_message.message_class = HidKeyboardBitmap
            # end if
        elif message_type == MessageType.HID_CONSUMER_CTRL and data is not None:
            message = HidConsumer.fromHexList(data)
            transport_message.message_class = HidConsumer
        # end if

        if VERBOSE:
            stdout.write(f"{message}\n")
        # end if

        return self._post_message_process(message=message)
    # end def process_interrupt_hid_keyboard

    @synchronized(SYNCHRONIZATION_LOCK)
    def process_interrupt_hid_digitizer(self, transport_message):
        """
        Process on reception of an interrupt for HID digitizer interface:
          - message is read from interrupt
          - message is sent to handlers that accept it

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The queue where the message has been put in or None if the given message could not be treated
        :rtype: ``HidMessageQueue`` or ``None``
        """
        message = None

        if len(transport_message.data) == 0:
            return None
        # end if

        # Check message type
        data, message_type = self.analyse_hid_message(transport_message, message_type=MessageType.HID_DIGITIZER)
        if message_type == MessageType.HID_DIGITIZER and data is not None:
            message = HidDigitizer.fromHexList(data)
            transport_message.message_class = HidDigitizer
        # end if

        return self._post_message_process(message=message)
    # end def process_interrupt_hid_digitizer

    @synchronized(SYNCHRONIZATION_LOCK)
    def process_control_read_get_descriptor(self, transport_message):
        """
        Process on reception of an interrupt :
          - message is read from interrupt
          - message is sent to handlers that accept it

        :param transport_message: Transport message to analyse
        :type transport_message: ``TransportMessage``

        :return: The queue where the message has been put in or None if the given message could not be treated
        :rtype: ``HidMessageQueue`` or ``None``
        """
        message = None

        if len(transport_message.data) == 0:
            return None
        # end if

        device = hidparser.parse(bytes(str(transport_message.data), 'utf-8'), timestamp=transport_message.timestamp)
        for i in range(len(device.all.items)):
            usage_name = device.all.items[i].usage.name
            if usage_name not in ['MOUSE', 'KEYBOARD', 'HIDPP_MODE_SHORT', 'HIDPP2_MODE_0301',
                                  'HIDPP2_MODE_0302', 'TOUCH_PAD', 'VLP_MODE_1A02',
                                  'VLP_MODE_1A08', 'VLP_MODE_1A10']:
                continue
            elif usage_name == 'MOUSE':
                self.mouse_collections = device
                if len(device.reports) > 1:
                    # if more than one application collection
                    self.mouse_report_id_list = device.reports.keys()
                    field_index = 0
                    for item_index in range(len(device.all.mouse.pointer.items)):
                        for _ in range(device.all.mouse.pointer.items[item_index].count):
                            HidMouse.FIELDS[field_index].length = device.all.mouse.pointer.items[item_index].size
                            field_index += 1
                        # end for
                    # end for
                else:
                    self.mouse_report_id_list = []
                # end if
            elif usage_name == 'KEYBOARD':
                self.keyboard_collections = device
                if len(device.reports) > 1:
                    # if more than one application collection
                    self.keyboard_report_id_list = device.reports.keys()
                else:
                    self.keyboard_report_id_list = []
                # end if
            elif usage_name == 'TOUCH_PAD':
                self.digitizer_collections = device
                if len(device.reports) > 1:
                    # if more than one application collection
                    self.digitizer_report_id_list = device.reports.keys()
                else:
                    self.digitizer_report_id_list = []
                # end if
            # end if
            message = DescriptorDispatcher.fromHexList(transport_message.data, timestamp=transport_message.timestamp)
        # end for

        if VERBOSE:
            stdout.write(f'{str(device)}\n')
        # end if

        return self._post_message_process(message=message)
    # end def process_control_read_get_descriptor

    def _post_message_process(self, message):
        """
        Give the message to the correct handler.

        :param message: The message processed
        :type message: ``object``

        :return: The queue where the message has been put in or None if no message was given
        :rtype: ``HidMessageQueue`` or ``None``
        """
        if message is None:
            # Case 1: message not yet implemented
            # Case 2: notifications not handled (example: Color LED Effects in gaming products)
            #
            # Having no message to notify is an error case : raise an exception
            # raise QueueEmpty("Invalid message received:\n%s" % data)
            return None
        # end if

        queue_receiving = None
        # increment message sequence number for next one
        self.msg_sequence_number += 1

        # Send message to all eligible callback entries
        for handler in self._handlers:
            if handler.__class__.__name__ == 'HidMessageQueue':
                if handler.is_message_accepted(message):
                    queue_receiving = handler
                    # Send message to only one queue
                    break
                # end if
            # end if
        # end for

        if queue_receiving is None:
            queue_receiving = self.default_message_queue
        # end if

        queue_receiving.handle(message)

        return queue_receiving
    # end def _post_message_process

    def analyse_hid_message(self, usbmessage, message_type):
        """
        Analyse HID message (MOUSE or KEYBOARD)

        :param usbmessage: Usb message to analyse
        :type usbmessage: ``TransportMessage``
        :param message_type: Message type, values can be found in ``MessageType``
        :type message_type: ``int``

        :return: Deserialized data, and message type, both None if the message couldn't be treated
        :rtype: ``tuple``
        """
        data_collections = None
        report_id_list = []
        if message_type == MessageType.HID_MOUSE and self.mouse_collections is not None:
            data_collections = self.mouse_collections
            report_id_list = self.mouse_report_id_list
        elif message_type == MessageType.HID_KEYBOARD and self.keyboard_collections is not None:
            data_collections = self.keyboard_collections
            report_id_list = self.keyboard_report_id_list
        elif message_type == MessageType.HID_DIGITIZER and self.digitizer_collections is not None:
            data_collections = self.digitizer_collections
            report_id_list = self.digitizer_report_id_list
        # end if

        if data_collections is not None:
            payload = usbmessage.data
            if len(report_id_list) > 0:
                report_id = payload[0]
                payload = payload[1:]
            else:
                report_id = 0
            # end if

            if report_id not in data_collections.reports.keys():
                return None, None  # TODO: Warn when this situation happens
            elif hasattr(data_collections.reports[report_id].inputs, 'mouse'):
                message_type = MessageType.HID_MOUSE
            elif hasattr(data_collections.reports[report_id].inputs, 'keyboard'):
                message_type = MessageType.HID_KEYBOARD
            elif hasattr(data_collections.reports[report_id].inputs, 'consumer_control'):
                message_type = MessageType.HID_CONSUMER_CTRL
            elif hasattr(data_collections.reports[report_id].inputs, 'system_control'):
                message_type = MessageType.HID_SYS_CTRL
            elif hasattr(data_collections.reports[report_id].inputs, 'call_state_management_control'):
                message_type = MessageType.HID_CALL_STATE_MGT_CRTL
            elif hasattr(data_collections.reports[report_id].inputs, 'touch_pad'):
                message_type = MessageType.HID_DIGITIZER
            # end if

            # Reverse the bits inside each byte of the payload
            for payload_index in range(len(payload)):
                payload[payload_index] = reverse_bits(payload[payload_index])
            # end for
            if len(report_id_list) > 0:
                payload = HexList(report_id) + payload
            # end if

            # Deserialize the data and populate the object members
            big_endian_payload = data_collections.deserialize(bytes(payload))

            return HexList(big_endian_payload.hex), message_type
        elif message_type == MessageType.HID_KEYBOARD and len(usbmessage.data) == 8:
            # Boot protocol Keyboard format
            return HexList(reverse_bits(usbmessage.data[0])) + HexList(usbmessage.data[1:]), message_type
        # end if

        return None, None
    # end def analyse_hid_message

    def get_first_request_class_from_feature_id_and_version(self, feature_id=0, version=0):
        """
        Get the first request class of a feature in the feature table from the feature ID and the version

        :param feature_id: ID of the feature wanted - OPTIONAL
        :type feature_id: ``HexList`` or ``int``
        :param version: Version of the feature wanted - OPTIONAL
        :type version: ``HexList`` or ``int``

        :return: The class of the first function request of the feature wanted, None if the feature is not known by
                 this dispatcher
        :rtype: ``type`` or ``None``
        """

        request_class = None

        if isinstance(feature_id, HexList):
            feature_id = feature_id.toLong()
        # end if

        if isinstance(version, HexList):
            version = version.toLong()
        # end if

        try:
            response_class = self._feature_table[(feature_id, version, 0)]

            request_class = response_class.REQUEST_LIST[0]
        except KeyError:
            pass
        # end try

        return request_class
    # end def get_first_request_class_from_feature_id_and_version

    def clear_all_queues(self):
        """
        Clear all queues and return all untreated messages as a list (separation by queue is then lost).

        :return: List of untreated messages
        :rtype: ``list``
        """
        list_of_untreated_message = []

        for queue in self.queue_list:
            list_of_untreated_message.extend(queue.clear())
        # end for

        return list_of_untreated_message
    # end def clear_all_queues

    def dump_mapping_in_other_dispatcher(self, other_dispatcher):
        """
        Dump the mapping in other dispatcher.

        :param other_dispatcher: Other dispatcher to dump the mapping in
        :type other_dispatcher: ``HIDDispatcher``
        """
        for feature_index in self._feature_index_to_id.copy():
            feature_id, feature_version = self._feature_index_to_id[feature_index]
            other_dispatcher.add_feature_entry(
                feature_index=feature_index, feature_id=feature_id, feature_version=feature_version)
        # end for
    # end def dump_mapping_in_other_dispatcher
# end class HIDDispatcher

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
