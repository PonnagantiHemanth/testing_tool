#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.bugtracking.bugtracker
:brief: Bug tracking decorator module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2019/06/27
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pyharness.selector import bugtracker
from pyusb.libusbdriver import LibusbDriver

# ------------------------------------------------------------------------------
# Features implementation
# ------------------------------------------------------------------------------


def set_expected_failure(context, subsystemName, feature):
    """
    Checks if a feature has a specific value

    :param context: context.
    :type context: ``Context``
    :param subsystemName: sub-system Name.
    :type subsystemName: ``str``
    :param feature: feature name.
    :type feature: ``str``

    :return: True if the bug is expected, False otherwise.
    :rtype: ``bool``
    """
    subsystemList = subsystemName.split('/')
    # noinspection PyBroadException
    try:
        subsystem = context.getFeatures()
        for item in subsystemList:
            subsystem = subsystem.getChild(item)
        # end for
        if feature in dir(subsystem):
            result = getattr(subsystem, feature)
        else:
            result = False
        # end if
    except:
        result = False
    # end try
    return result
# end def set_expected_failure


# -----------------
# Bug tracker
# -----------------
# Feature 0x8061: Libusb driver lost reportRateInfoEvent while the protocol is changing from USB to GamingWireless(2khz)
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_ReportRateInfo_EventLost'))
bugtracker.registerFeature('ReportRateInfo_EventLost', function,
                           featureHelp='Help for the layer lost ReportRateInfoEvent')

# Footloose 0x2201 SetDpiForEachSensor v1: dpi returned value is 0
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Footloose_SetDpiForEachSensor_Dpi'))
bugtracker.registerFeature('Footloose_SetDpiForEachSensor_Dpi', function,
                           featureHelp='Help for Footloose SetDpiForEachSensor bug tracker')

# Footloose 0x1830 SetPowerMode: invalid error code returned
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_SetPowerMode_ErrorCode'))
bugtracker.registerFeature('SetPowerMode_ErrorCode', function,
                           featureHelp='Help for SetPowerMode bug tracker')

# Artanis Premium (PWA, PB1, PB2 samples) 0x1830 measured high current in Dead, Cut-off and Deep-sleep modes
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_SetPowerMode_HighCurrent'))
bugtracker.registerFeature('SetPowerMode_HighCurrent', function,
                           featureHelp='Help for SetPowerMode bug tracker')

# Herzog 0x1861 BatteryLevelsCalibration: MeasureBatteryResponse notification returned when forcing a cut-off
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_BatteryLevelsCalibration_Cut_Off'))
bugtracker.registerFeature('BatteryLevelsCalibration_Cut_Off', function,
                           featureHelp='Help for BatteryLevelsCalibration bug tracker')

# Footloose (corded) 0x1DF3 Cannot receive Link Quality Event since it is sent by a receiver and the corded
# version of footloose does not use one
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_1df3_on_corded_devices'))
bugtracker.registerFeature('1df3_on_corded_devices', function,
                           featureHelp='Help for 1D3F on corded devices bug tracker')

# Herzog 0x2121 GetAnalyticsData: feature version 1 not yet implemented in the Test Env
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Herzog_GetAnalyticsData'))
bugtracker.registerFeature('Herzog_GetAnalyticsData', function,
                           featureHelp='Help for Herzog GetAnalyticsData bug tracker')

# Herzog 0x2110 SetRatchetControlMode hasn't implemented Invalid_Argument error
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_SetRatchetControlMode_ErrorCode'))
bugtracker.registerFeature('SetRatchetControlMode_ErrorCode', function,
                           featureHelp='Help for SetRatchetControlMode bug tracker')

# Herzog 0x1830 when measuring current with debugger plugged in, the result is higher than expected
# Todo: remove here after changed to power board v3
function = lambda context: (LibusbDriver.discover_debug_probe() > 0)
bugtracker.registerFeature('Consumption_higher_with_debugger', function,
                           featureHelp='Help for current measurement bug tracker')

# Foster 0x1E02 DisableFeatures Gotthard should be disabled only after reset (https://jira.logitech.io/browse/FBP-204).
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Foster_DisableFeatures_Gotthard'))
bugtracker.registerFeature('Foster_DisableFeatures_Gotthard', function,
                           featureHelp='Help for DisableFeatures bug tracker')

# Foster 0x1004 ShowBatteryStatus shall return error NOT_ALLOWED
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Foster_ShowBatteryStatus_NotAllowed'))
bugtracker.registerFeature('Foster_ShowBatteryStatus_NotAllowed', function,
                           featureHelp='Help for ShowBatteryStatus bug tracker')

# Mezzy DFU in place Entity type shall be reset when Soft Device has been wiped out
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Mezzy_DfuInPlace_WrongEntityType'))
bugtracker.registerFeature('Mezzy_DfuInPlace_WrongEntityType', function,
                           featureHelp='Help for DfuInPlace bug tracker')

# https://jira.logitech.io/browse/SAV-58 : Wrong companion FW types
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Companion_WrongEntityType'))
bugtracker.registerFeature('Companion_WrongEntityType', function,
                           featureHelp='Help for companion type bug tracker')

# Device BLE Pro 0x1815 Host name shall not be overwritten at reconnection
# Fixed in Patchset: https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/7899
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Device_HostName_ResetAtReconnection'))
bugtracker.registerFeature('Device_HostName_ResetAtReconnection', function,
                           featureHelp='Help for HostFriendlyName bug tracker')

# The last analytics event shall contain 5 CID but got 6 individual analytics event
# https://jira.logitech.io/browse/RBP-40
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_AnalyticsKeyEvents_CID_Packing'))
bugtracker.registerFeature('AnalyticsKeyEvents_CID_Packing', function,
                           featureHelp='Help for AnalyticsKeyEvents bug tracker')

# Inga BLE Pro 0x1982 Event shall be generated if DUT enters/exits from critical battery level
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER',
                                                 'F_Bug_Backlight_EventGenerationForEnterOrExitCriticalBattery'))
bugtracker.registerFeature('Backlight_EventGenerationForEnterOrExitCriticalBattery', function,
                           featureHelp='Help for Backlight bug tracker')

# Inga BLE Pro 0x1982 On the breathing Backlight effect, the LED pwm value does not reach the expected level
# (https://jira.logitech.io/browse/ICFM-36).
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER',
                                                 'F_Bug_Backlight_BreathingEffectLevelByMonitoring'))
bugtracker.registerFeature('Backlight_BreathingEffectLevelByMonitoring', function,
                           featureHelp='Help for Backlight bug tracker')

# On Level 0, when pressing Backlight Up key, the effect duration is much longer than expected (8s instead of 5s)
# (https://jira.logitech.io/browse/INGA-107).
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER',
                                                 'F_Bug_Backlight_DurationEffectLevelZeroToOneByMonitoring'))
bugtracker.registerFeature('Backlight_DurationEffectLevelZeroToOneByMonitoring', function,
                           featureHelp='Help for Backlight bug tracker')

# Snapper has trouble connecting with the reference firmware for tag 1
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_DFU_DirectBLEConnection'))
bugtracker.registerFeature('DFU_DirectBLEConnection', function,
                           featureHelp='Help for Direct BLE connection in DFU test suite bug tracker')

# DivertedButtonsEvent shall contain the CIDs info of the diverted keys which are pressed as much as possible(Up to 4),
# the 5th CID info must be filled in after any the other diverted key is released(https://jira.logitech.io/browse/ICU-9)
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_DivertedButtonsEvent_5th_CID_fill_in'))
bugtracker.registerFeature('DivertedButtonsEvent_5th_CID_fill_in', function,
                           featureHelp='Help for divertedButtonsEvent in 5 buttons make up and break up')

# [CP&G][HID++][0x1B04] Diverting or undiverting a button should not be affected when the button is already pressed.
# https://jira.logitech.io/browse/LEX-182 / https://jira.logitech.io/browse/NRF52-563
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_DivertOnPress'))
bugtracker.registerFeature('DivertOnPress', function, featureHelp='Help for Bug_DivertOnPress bug tracker')

function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_LockKeyState_ReservedBitsHandling'))
bugtracker.registerFeature('LockKeyState_ReservedBitsHandling', function,
                           featureHelp='Help for LockKeyState_ReservedBitsHandling bug tracker')

# The returned value of device_idx mismatches with the input of selectDevice requests
# https://jira.logitech.io/browse/NRF52-394
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_SelectDevice_MismatchDeviceIndex'))
bugtracker.registerFeature('SelectDevice_MismatchDeviceIndex', function,
                           featureHelp='Help for SelectDevice_MismatchDeviceIndex bug tracker')

# FW returns an unexpected error INVALID_ARGUMENT(0x02), when the first padding byte is not 0x00
# https://jira.logitech.io/browse/NRF52-395
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_GetSelectedDevice_PaddingBytesHandling'))
bugtracker.registerFeature('GetSelectedDevice_PaddingBytesHandling', function,
                           featureHelp='Help for GetSelectedDevice_PaddingBytesHandling bug tracker')
# No platform event sent after changing platform index
# https://jira.logitech.io/browse/NMM-23
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_PlatformChange_EventNotSent'))
bugtracker.registerFeature('PlatformChange_EventNotSent', function,
                           featureHelp='Help for PlatformChange_EventNotSent bug tracker')

# The INVALID_ARGUMENT is not sent when the nBytes is greater than the upper limit.
# https://jira.logitech.io/browse/YOKTOUCH-212
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_I2cWriteDirectAccess_InvalidNBytes'))
bugtracker.registerFeature('I2cWriteDirectAccess_InvalidNBytes', function,
                           featureHelp='Help for I2cWriteDirectAccess_InvalidNBytes bug tracker')

# Incorrect appearance in ble gap service for some devices in bootloader.
# https://jira.logitech.io/browse/BT-459
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_BLE_GAP_Appearance_Bootloader'))
bugtracker.registerFeature('BLE_GAP_Appearance_Bootloader', function,
                           featureHelp='Help for Bug_Ble_Gap_Appearance_Bootloader bug tracker')

# Feature 9001: Unexpected response in frame capture api
# https://github.com/Logitech/cpg-samarkand-hidpp-docs/issues/365
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_FrameCapture_UnexpectedResponse'))
bugtracker.registerFeature('Unexpected_FrameCapture_Response', function,
                           featureHelp='Help for FrameCapture_UnexpectedResponse bug tracker')

# Feature 9205: Unexpected response in read touch status api
# https://github.com/Logitech/cpg-samarkand-hidpp-docs/issues/382
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_ReadTouchStatus_UnexpectedResponse'))
bugtracker.registerFeature('Unexpected_ReadTouchStatus_Response', function,
                           featureHelp='Help for ReadTouchStatus_UnexpectedResponse bug tracker')

# Feature 9205: Error not thrown while trying to write to melexis area register
# https://github.com/Logitech/cpg-samarkand-hidpp-docs/issues/382
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER',
                                                 'F_Bug_WriteSensorRegister_ErrorCodeNotReturned'))
bugtracker.registerFeature('WriteSensorRegisterErrorCode_NotReturned', function,
                           featureHelp='Help for WriteSensorRegister_ErrorCodeNotReturned bug tracker')

# BLE GATT HIDS: Protocol Mode characteristic present in bootloader.
# https://jira.logitech.io/browse/BT-481
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_BLE_HID_Bootloader_Protocol_Mode_Present'))
bugtracker.registerFeature('BLE_HID_Bootloader_Protocol_Mode_Present', function,
                           featureHelp='Help for BLE_HID_Bootloader_Protocol_Mode_Present bug tracker')

# BLE Enumeration: out-of-bank memory access firmware issue
# Patchset fixing the issue is : https://goldenpass.logitech.com:8443/c/ccp_fw/lfa/+/10042
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_BLE_Enumeration_Memory_Access_Issue'))
bugtracker.registerFeature('BLE_Enumeration_Memory_Access_Issue', function,
                           featureHelp='Help for BLE_Enumeration_Memory_Access_Issue bug tracker')

# BLE GATT HIDS: NPI report map is out of date with the current specification
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_BLE_Unsupported_Report_Map'))
bugtracker.registerFeature('BLE_Unsupported_Report_Map', function,
                           featureHelp='Help for BLE_Unsupported_Report_Map bug tracker')

# Feature 9205: read and write callibration method byte 0 as index.
# https://jira.logitech.io/browse/BARDI-5
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Read_Write_Callibration_Format'))
bugtracker.registerFeature('Read_Write_Callibration_Format', function,
                           featureHelp='Help for Read_Write_Callibration_Format bug tracker')

# Feature 40A3: wrong default Fn Inversion state for PWS products
# https://jira.logitech.io/browse/NRF52-477
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Default_Fn_Inversion_State'))
bugtracker.registerFeature('Default_Fn_Inversion_State', function,
                           featureHelp='Help for Default_Fn_Inversion_State bug tracker')

# Feature 40A3: Pollux Fn inversion state is reversed in test settings to enable keyboard tests
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Pollux_Fn_Lock_Reversed'))
bugtracker.registerFeature('Pollux_Fn_Lock_Reversed', function,
                           featureHelp='Help for Pollux_Fn_Lock_Reversed bug tracker')

# Wrong feature version returns, 0x8081 version is incorrect on Harpy
# https://jira.logitech.io/browse/NRF52-386
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Wrong_8081_Feature_Version'))
bugtracker.registerFeature('Wrong_8081_Feature_Version', function,
                           featureHelp='Help for Wrong_8081_Feature_Version bug tracker')

# Wrong key code translation for Backlight decrease & increase in Chrome OS mode
# https://jira.logitech.io/browse/NRF52-468
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_ChromeOS_Backlight_KeyCode'))
bugtracker.registerFeature('ChromeOS_Backlight_KeyCode', function,
                           featureHelp='Help for ChromeOS_Backlight_KeyCode bug tracker')

# Dictation key: missing abort handling when any other key is pressed
# https://jira.logitech.io/browse/NRF52-469
# Fixed in https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/10493
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Dictation_Abort_Handling'))
bugtracker.registerFeature('Dictation_Abort_Handling', function,
                           featureHelp='Help for Dictation_Abort_Handling bug tracker')

# While the device is in pairing mode, a long press on the Connect or the same EasySwitch button does
# reset the pairing timeout while it is expected to not do it
# https://jira.logitech.io/browse/NRF52-186
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER',
                                                 'F_Bug_Pairing_Mode_Long_Press_Timeout_Reset'))
bugtracker.registerFeature('Pairing_Mode_Long_Press_Timeout_Reset', function,
                           featureHelp='Help for Pairing_Mode_Long_Press_Timeout_Reset bug tracker')

# Feature 0x4531 : Wrong platformSource on Norman
# https://jira.logitech.io/browse/NORMAN-197, https://jira.logitech.io/browse/NRF52-411
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER',
                                                 'F_Bug_Platform_Source'))
bugtracker.registerFeature('Platform_Source', function,
                           featureHelp='Help for wrong platform source bug tracker')

# BLE Pro Pairing: At OOB, user activity will trigger broadcasting performs twice
# https://jira.logitech.io/browse/NRF52-104
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_User_Activity_Advertising_Twice'))
bugtracker.registerFeature('User_Activity_Advertising_Twice', function,
                           featureHelp='Help for User_Activity_Advertising_Twice bug tracker')

# Feature 18B0: On pressing some keys after enabling monitor mode, they are being reported as pressed in the
# subsequent monitor mode events even if that key was previously released
# https://jira.logitech.io/browse/NORMAN-216
function = lambda context: set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Sticky_Keys_In_Monitor_Mode_Event')
bugtracker.registerFeature('StickyKeysInMonitorModeEvent', function,
                           featureHelp='Help for sticky keys in monitor mode event bug tracker')

# Feature 18B0: Firmware reports Keyboard Row and Col incorrectly
# https://jira.logitech.io/browse/NRF52-490
function = lambda context: set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_MonitorMode_BadRowColValues')
bugtracker.registerFeature('MonitorMode_BadRowColValues', function,
                           featureHelp='Help for bad row and column values in monitor mode event bug tracker')

# YOKO TP supports DFU for touch module but test framework doesn't support it yet.
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_DFU_OnTouchModule'))
bugtracker.registerFeature('Bug_DFU_OnTouchModule', function,
                           featureHelp='Help for Upgradable FW entity in DFU test suite bug tracker')

# For VLP1, no forward nor backward compatibility is supported
# https://jira.logitech.io/browse/LEX-93
# https://jira.logitech.io/browse/LEX-120
# https://jira.logitech.io/browse/LEX-126
function = lambda context: (set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_VLPNoForwardBackwardCompatibility'))
bugtracker.registerFeature('VLPNoForwardBackwardCompatibility', function,
                           featureHelp='Help for VLP forward and backward compatibility not supported bug tracker')

# Feature 0x19A1: Unsupported image format Error not received when image_payload and image_format param doesn't match
# https://jira.logitech.io/browse/LEX-159
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_UnsupportedImageFormat'))
bugtracker.registerFeature('VLPUnsupportedImageFormat', function,
                           featureHelp='Help for Bug_Unsupported_Image_Format bug tracker')

# Keypass Pairing: Inability to erase leading zeros
# https://jira.logitech.io/browse/BT-597
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Erasing_Leading_Zero'))
bugtracker.registerFeature('Erasing_Leading_Zero', function,
                           featureHelp='Help for Bug_Erasing_Leading_Zero bug tracker')

# Unexpected behaviour of Host LED after Dfu is completed in a pws device
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Unexpected_Host_LED_Behaviour_After_Dfu'))
bugtracker.registerFeature('UnexpectedHostLEDBehaviourAfterDfu', function,
                           featureHelp='Help for Unexpected Host LED Behaviour After Dfu bug tracker')

# Overflow in soft device from properties writes
# https://jira.logitech.io/browse/BT-555
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_SoftDeviceOverflowOnPropertyChange'))
bugtracker.registerFeature('SoftDeviceOverflowOnPropertyChange', function,
                           featureHelp='Help for SoftDeviceOverflowOnPropertyChange bug tracker')

# BLE.Advertising: SHORT_LOCAL_NAME is not present or with wrong length
# https://jira.logitech.io/browse/CINDERELLA-206
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_AdvertisingShortLocalName'))
bugtracker.registerFeature('AdvertisingShortLocalName', function,
                           featureHelp='Help for AdvertisingShortLocalName bug tracker')

# Feature 0x8040: Set brightness is not persistence after power reset
# https://jira.logitech.io/browse/CINDERELLA-203
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_BrightnessNotPersistence'))
bugtracker.registerFeature('BrightnessNotPersistence', function,
                           featureHelp='Help for BrightnessNotPersistence bug tracker')

# Feature 0x8040: Received unexpected brightnessChangeEvent
# https://jira.logitech.io/browse/CINDERELLA-204
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_UnexpectedBrightnessChangeEvent'))
bugtracker.registerFeature('UnexpectedBrightnessChangeEvent', function,
                           featureHelp='Help for UnexpectedBrightnessChangeEvent bug tracker')

# Feature 0x8071: The rgbClusterEffectIndex didn't be updated after changed effect
# https://jira.logitech.io/browse/CINDERELLA-202
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_RgbClusterEffectIndexNotUpdated'))
bugtracker.registerFeature('RgbClusterEffectIndexNotUpdated', function,
                           featureHelp='Help for RgbClusterEffectIndexNotUpdated bug tracker')

# Feature 0x8101: The macro is not sent in onboard mode when the keyboard is in deep sleep
# https://jira.logitech.io/browse/CINDERELLA-41
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_MacroNotSentDeepSleep'))
bugtracker.registerFeature('MacroNotSentDeepSleep', function,
                           featureHelp='Help for MacroNotSentDeepSleep bug tracker')

# Feature 0x1807: Wrong version of the feature returned
# https://jira.logitech.io/browse/CINDERELLA-210
function = lambda context: (
    set_expected_failure(context, 'BUG_TRACKER', 'F_Bug_Wrong1807VersionReturned'))
bugtracker.registerFeature('Wrong1807VersionReturned', function,
                           featureHelp='Help for Wrong1807VersionReturned bug tracker')

# ------------------------------------------------------------------------------
# End of file
# ------------------------------------------------------------------------------
