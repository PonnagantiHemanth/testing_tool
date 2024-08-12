#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.bugtracking.features
:brief:  pytestbox Bug tracker SubSystem implementation
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/06/27
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.systems import AbstractSubSystem


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BugTrackerSubSystem(AbstractSubSystem):
    """
    BUG_TRACKER SubSystem
    """

    def __init__(self):
        AbstractSubSystem.__init__(self, "BUG_TRACKER")

        # ------------
        # Bug Tracker feature
        # ------------
        # Feature 0x8061: Can't receive reportRateInfoEvent while the protocol is changing from USB to LS2
        self.F_Bug_ReportRateInfo_EventLost = False

        # Footloose 0x2201 SetDpiForEachSensor v1: dpi returned value is 0
        self.F_Bug_Footloose_SetDpiForEachSensor_Dpi = False

        # Footloose 0x1830 SetPowerMode: invalid error code returned
        self.F_Bug_SetPowerMode_ErrorCode = False

        # Artanis Premium (PWA, PB1, PB2 samples) 0x1830 measured high current in Dead, Cut-off and Deep-sleep modes
        # While debugger connected to Artanis Premium, the debugger cannot be closed successfully then caused high
        # current in power mode tests.
        self.F_Bug_SetPowerMode_HighCurrent = False

        # Herzog UFY: MeasureBatteryResponse notification returned when forcing a cut-off
        self.F_Bug_BatteryLevelsCalibration_Cut_Off = False

        # Footloose (corded) 0x1DF3 Cannot receive Link Quality Event since it is sent by a receiver and the corded
        # version of footloose does not use one
        self.F_Bug_1df3_on_corded_devices = False

        # Herzog 0x2121 GetAnalyticsData: feature version 1 not yet implemented in the Test Env
        self.F_Bug_Herzog_GetAnalyticsData = False

        # Herzog 0x2110 SetRatchetControlMode hasn't implemented Invalid_Argument error
        self.F_Bug_SetRatchetControlMode_ErrorCode = False

        # Foster 0x1E02 DisableFeatures Gotthard should be disabled only after reset
        # (https://jira.logitech.io/browse/FBP-204).
        self.F_Bug_Foster_DisableFeatures_Gotthard = False

        # Foster 0x1004 ShowBatteryStatus shall return error NOT_ALLOWED
        self.F_Bug_Foster_ShowBatteryStatus_NotAllowed = False

        # Mezzy DFU in place Entity type shall be reset when Soft Device has been wiped out
        self.F_Bug_Mezzy_DfuInPlace_WrongEntityType = False

        # https://jira.logitech.io/browse/SAV-58 : Wrong companion FW types
        self.F_Bug_Companion_WrongEntityType = False

        # Device BLE Pro 0x1815 Host name shall not be overwritten at reconnection
        # Fixed in Patchset: https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/7899
        self.F_Bug_Device_HostName_ResetAtReconnection = False

        # The last analytics event shall contain 5 CID but got 6 individual analytics event
        self.F_Bug_AnalyticsKeyEvents_CID_Packing = False

        # Inga BLE Pro 0x1982 Event to be generated if DUT enter/exit from critical battery level
        self.F_Bug_Backlight_EventGenerationForEnterOrExitCriticalBattery = False

        # Inga BLE Pro 0x1982 On the breathing Backlight effect, the LED pwm value does not reach the expected level
        # (https://jira.logitech.io/browse/ICFM-36).
        self.F_Bug_Backlight_BreathingEffectLevelByMonitoring = False

        # On Level 0, when pressing Backlight Up key, the effect duration is much longer than expected
        # (https://jira.logitech.io/browse/INGA-107).
        self.F_Bug_Backlight_DurationEffectLevelZeroToOneByMonitoring = False

        # Snapper has trouble connecting with the reference firmware for tag 1
        self.F_Bug_DFU_DirectBLEConnection = False

        # DivertedButtonsEvent shall contain the CIDs info of the diverted keys which are pressed as much as possible
        # (Up to 4), the 5th CID info must be filled in after any the other diverted key is released
        # https://jira.logitech.io/browse/ICU-9
        self.F_Bug_DivertedButtonsEvent_5th_CID_fill_in = False

        # [CP&G][HID++][0x1B04] Diverting or undiverting a button should not be affected when the button is already pressed.
        # https://jira.logitech.io/browse/LEX-182 / https://jira.logitech.io/browse/NRF52-563
        self.F_Bug_DivertOnPress = False

        # Device echos the input data in reserved bits is an unexpected behavior.
        # Enable this bugtracker only on NPI that haven't cherry picked the following patchset:
        # https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/7550
        self.F_Bug_LockKeyState_ReservedBitsHandling = False

        # The returned value of device_idx mismatches with the input of selectDevice requests
        # https://jira.logitech.io/browse/NRF52-394
        self.F_Bug_SelectDevice_MismatchDeviceIndex = False

        # FW returns an unexpected error INVALID_ARGUMENT(0x02), when the first padding byte is not 0x00
        # https://jira.logitech.io/browse/NRF52-395
        self.F_Bug_GetSelectedDevice_PaddingBytesHandling = False

        # No platform event sent after changing platform index
        # https://jira.logitech.io/browse/NMM-23
        self.F_Bug_PlatformChange_EventNotSent = False

        # The INVALID_ARGUMENT is not sent when the nBytes is greater than the upper limit.
        # https://jira.logitech.io/browse/YOKTOUCH-212
        self.F_Bug_I2cWriteDirectAccess_InvalidNBytes = False

        # Incorrect appearance in ble gap service for some devices in bootloader.
        # https://jira.logitech.io/browse/BT-459
        self.F_Bug_BLE_GAP_Appearance_Bootloader = False

        # Feature 9001: Unexpected response in frame capture api
        # https://github.com/Logitech/cpg-samarkand-hidpp-docs/issues/365
        self.F_Bug_FrameCapture_UnexpectedResponse = False

        # Feature 9205: Unexpected response in read touch status api
        # https://github.com/Logitech/cpg-samarkand-hidpp-docs/issues/382
        self.F_Bug_ReadTouchStatus_UnexpectedResponse = False

        # Feature 9205: Error not thrown while trying to write to melexis area register
        # https://github.com/Logitech/cpg-samarkand-hidpp-docs/issues/382
        self.F_Bug_WriteSensorRegister_ErrorCodeNotReturned = False

        # BLE GATT HIDS: Protocol Mode characteristic present in bootloader.
        # https://jira.logitech.io/browse/BT-481
        self.F_Bug_BLE_HID_Bootloader_Protocol_Mode_Present = False

        # BLE Enumeration: out-of-bank memory access firmware issue
        # https://goldenpass.logitech.com:8443/c/ccp_fw/lfa/+/10042
        self.F_Bug_BLE_Enumeration_Memory_Access_Issue = False

        # BLE GATT HIDS: NPI report map is out of date with the current specification
        self.F_Bug_BLE_Unsupported_Report_Map = False

        # Feature 9205: read and write callibration method byte 0 as chunk index.
        # https://jira.logitech.io/browse/BARDI-5
        self.F_Bug_Read_Write_Callibration_Format = False

        # Feature 40A3: wrong default Fn Inversion state for PWS products
        # https://jira.logitech.io/browse/NRF52-477
        self.F_Bug_Default_Fn_Inversion_State = False
        # Feature 40A3: Pollux Fn inversion state is reversed in test settings to enable keyboard tests
        self.F_Bug_Pollux_Fn_Lock_Reversed = False

        # Wrong feature version returns, 0x8081 version is incorrect on Harpy
        # https://jira.logitech.io/browse/NRF52-386
        self.F_Bug_Wrong_8081_Feature_Version = False

        # Wrong key code translation for Backlight decrease & increase in Chrome OS mode
        # https://jira.logitech.io/browse/NRF52-468
        self.F_Bug_ChromeOS_Backlight_KeyCode = False

        # Dictation key: missing abort handling when any other key is pressed
        # https://jira.logitech.io/browse/NRF52-469
        self.F_Bug_Dictation_Abort_Handling = False

        # While the device is in pairing mode, a long press on the Connect or the same EasySwitch button does
        # reset the pairing timeout while it is expected to not do it
        # https://jira.logitech.io/browse/NRF52-186
        self.F_Bug_Pairing_Mode_Long_Press_Timeout_Reset = False

        # Feature 0x4531 : Wrong platformSource on Norman
        # (https://jira.logitech.io/browse/NORMAN-197, https://jira.logitech.io/browse/NRF52-411).
        self.F_Bug_Platform_Source = False

        # BLE Pro Pairing: At OOB, user activity will trigger broadcasting performs twice
        # https://jira.logitech.io/browse/NRF52-104
        self.F_Bug_User_Activity_Advertising_Twice = False

        # Feature 18B0: On pressing some keys after enabling monitor mode, they are being reported as pressed in the
        # subsequent monitor mode events even if that key was previously released
        # https://jira.logitech.io/browse/NORMAN-216
        self.F_Bug_Sticky_Keys_In_Monitor_Mode_Event = False

        # Feature 18B0: Firmware reports Keyboard Row and Col incorrectly
        # https://jira.logitech.io/browse/NRF52-490
        self.F_Bug_MonitorMode_BadRowColValues = False

        # YOKO TP supports DFU for touch module but test framework doesn't support it yet.
        self.F_Bug_DFU_OnTouchModule = False

        # For VLP1, no forward nor backward compatibility is supported
        # https://jira.logitech.io/browse/LEX-93
        # https://jira.logitech.io/browse/LEX-120
        # https://jira.logitech.io/browse/LEX-126
        self.F_Bug_VLPNoForwardBackwardCompatibility = False

        # Feature 0x19A1: Unsupported image format Error not received when image_payload and image_format param doesn't match
        # https://jira.logitech.io/browse/LEX-159
        self.F_Bug_UnsupportedImageFormat = False

        # Keypass Pairing: Inability to erase leading zeros
        # https://jira.logitech.io/browse/BT-597
        self.F_Bug_Erasing_Leading_Zero = False

        # Unexpected behaviour of Host LED after Dfu is completed in a pws device
        # https://jira.logitech.io/browse/CAR-97
        self.F_Bug_Unexpected_Host_LED_Behaviour_After_Dfu = False

        # Overflow in soft device from properties writes
        # https://jira.logitech.io/browse/BT-555
        self.F_Bug_SoftDeviceOverflowOnPropertyChange = False

        # BLE.Advertising: SHORT_LOCAL_NAME is not present or with wrong length
        # https://jira.logitech.io/browse/CINDERELLA-206
        self.F_Bug_AdvertisingShortLocalName = False

        # Feature 0x8040: Set brightness is not persistence after power reset
        # https://jira.logitech.io/browse/CINDERELLA-203
        self.F_Bug_BrightnessNotPersistence = False

        # Feature 0x8040: Received unexpected brightnessChangeEvent
        # https://jira.logitech.io/browse/CINDERELLA-204
        self.F_Bug_UnexpectedBrightnessChangeEvent = False

        # Feature 0x8071: The rgbClusterEffectIndex didn't be updated after changed effect
        # https://jira.logitech.io/browse/CINDERELLA-202
        self.F_Bug_RgbClusterEffectIndexNotUpdated = False

        # Feature 0x8101: The macro is not sent in onboard mode when the keyboard is in deep sleep
        # https://jira.logitech.io/browse/CINDERELLA-41
        self.F_Bug_MacroNotSentDeepSleep = False

        # Feature 0x1807: Wrong version of the feature returned
        # https://jira.logitech.io/browse/CINDERELLA-210
        self.F_Bug_Wrong1807VersionReturned = False

    # end def __init__
# end class BugTrackerSubSystem

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
