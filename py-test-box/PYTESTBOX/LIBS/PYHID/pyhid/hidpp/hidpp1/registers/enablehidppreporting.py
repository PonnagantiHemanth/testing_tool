#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.enablehidppreporting
    :brief: HID++ 1.0 Enable HID++ reporting registers definition
    :author: Christophe Roquebert
    :date: 2020/02/19
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegister
from pyhid.hidpp.hidpp1.setgetregister import GetRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.bitfield import BitField
from pyhid.field import CheckInt
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class EnableHidReportingModel(BaseRegisterModel):
    """
    Register Enable HID++ Reporting model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get register model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetEnableHidppReportingRequest,
                "response": SetEnableHidppReportingResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetEnableHidppReportingRequest,
                "response": GetEnableHidppReportingResponse
            }
        }
    # end def _get_data_model
# end class EnableHidReportingModel


class HidppReportingFlagsStructure(BitFieldContainerMixin):
    """
    Bitfield structure of HID++ reporting register.

    Format:
    || @b Name                                              || @b Bit count ||
    || DeviceReportingFlagNumpadNumericKeys                 || 1            ||
    || DeviceReportingFlagFLockStatus                       || 1            ||
    || DeviceReportingFlagRollerH                           || 1            ||
    || DeviceReportingFlagBatteryStatus                     || 1            ||
    || DeviceReportingFlagMouseExtraButtons                 || 1            ||
    || DeviceReportingFlagRollerV                           || 1            ||
    || DeviceReportingFlagPowerKeys                         || 1            ||
    || DeviceReportingFlagConsumerVendorSpecificControl     || 1            ||
    || ReceiverReportingFlagReserved                        || 1            ||
    || ReceiverReportingFlagChannelChangeNotifications      || 1            ||
    || ReceiverReportingFlagAttackDetectionNotifications    || 1            ||
    || ReceiverReportingFlagTouchpadMultiTouchNotifications || 1            ||
    || ReceiverReportingFlagSoftwarePresent                 || 1            ||
    || ReceiverReportingFlagQuadLinkQualityInfo             || 1            ||
    || ReceiverReportingFlagUINotifications                 || 1            ||
    || ReceiverReportingFlagWirelessNotifications           || 1            ||
    || DeviceContReportingFlagReserved                      || 5            ||
    || DeviceContReportingFlagConfigurationComplete         || 1            ||
    || DeviceContReportingFlagVoIPTelephony                 || 1            ||
    || DeviceContReportingFlag3DGesture                     || 1            ||
    """
    class FID(object):
        """
        Field Identifiers
        """
        DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS = 0xFB
        DEVICE_REPORTING_FLAG_F_LOCK_STATUS = DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS - 1
        DEVICE_REPORTING_FLAG_ROLLER_H = DEVICE_REPORTING_FLAG_F_LOCK_STATUS - 1
        DEVICE_REPORTING_FLAG_BATTERY_STATUS = DEVICE_REPORTING_FLAG_ROLLER_H - 1
        DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS = DEVICE_REPORTING_FLAG_BATTERY_STATUS - 1
        DEVICE_REPORTING_FLAG_ROLLER_V = DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS - 1
        DEVICE_REPORTING_FLAG_POWER_KEYS = DEVICE_REPORTING_FLAG_ROLLER_V - 1
        DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL = DEVICE_REPORTING_FLAG_POWER_KEYS - 1

        RECEIVER_REPORTING_FLAG_RESERVED = DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL - 1
        RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS = RECEIVER_REPORTING_FLAG_RESERVED - 1
        RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS = \
            RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS - 1
        RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS = \
            RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS - 1
        RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT = RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS - 1
        RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO = RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT - 1
        RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS = RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO - 1
        RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS = RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS - 1

        DEVICE_CONT_REPORTING_RESERVED = RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS - 1
        DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE = DEVICE_CONT_REPORTING_RESERVED - 1
        DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY = DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE - 1
        DEVICE_CONT_REPORTING_FLAG_3D_GESTURE = DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY - 1
    # end class FID

    class LEN(object):
        """
        Field Lengths in bits
        """
        DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS = 0x01
        DEVICE_REPORTING_FLAG_F_LOCK_STATUS = 0x01
        DEVICE_REPORTING_FLAG_ROLLER_H = 0x01
        DEVICE_REPORTING_FLAG_BATTERY_STATUS = 0x01
        DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS = 0x01
        DEVICE_REPORTING_FLAG_ROLLER_V = 0x01
        DEVICE_REPORTING_FLAG_POWER_KEYS = 0x01
        DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL = 0x01

        RECEIVER_REPORTING_FLAG_RESERVED = 0x01
        RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS = 0x01
        RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS = 0x01
        RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS = 0x01
        RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT = 0x01
        RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO = 0x01
        RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS = 0x01
        RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS = 0x01

        DEVICE_CONT_REPORTING_RESERVED = 0x05
        DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE = 0x01
        DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY = 0x01
        DEVICE_CONT_REPORTING_FLAG_3D_GESTURE = 0x01
    # end class LEN

    FIELDS = (
        # DEVICE_REPORTING_FLAG
        BitField(FID.DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS,
                 LEN.DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS,
                 title='DeviceReportingFlagNumpadNumericKeys',
                 name='device_reporting_flag_numpad_numeric_keys',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_NUMPAD_NUMERIC_KEYS) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_F_LOCK_STATUS,
                 LEN.DEVICE_REPORTING_FLAG_F_LOCK_STATUS,
                 title='DeviceReportingFlagFLockStatus',
                 name='device_reporting_flag_f_lock_status',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_F_LOCK_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_F_LOCK_STATUS) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_ROLLER_H,
                 LEN.DEVICE_REPORTING_FLAG_ROLLER_H,
                 title='DeviceReportingFlagRollerH',
                 name='device_reporting_flag_roller_h',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_ROLLER_H // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_ROLLER_H) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_BATTERY_STATUS,
                 LEN.DEVICE_REPORTING_FLAG_BATTERY_STATUS,
                 title='DeviceReportingFlagBatteryStatus',
                 name='device_reporting_flag_battery_status',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_BATTERY_STATUS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_BATTERY_STATUS) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS,
                 LEN.DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS,
                 title='DeviceReportingFlagMouseExtraButtons',
                 name='device_reporting_flag_mouse_extra_buttons',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_MOUSE_EXTRA_BUTTONS) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_ROLLER_V,
                 LEN.DEVICE_REPORTING_FLAG_ROLLER_V,
                 title='DeviceReportingFlagRollerV',
                 name='device_reporting_flag_roller_v',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_ROLLER_V // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_ROLLER_V) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_POWER_KEYS,
                 LEN.DEVICE_REPORTING_FLAG_POWER_KEYS,
                 title='DeviceReportingFlagPowerKeys',
                 name='device_reporting_flag_power_keys',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_POWER_KEYS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_POWER_KEYS) - 1),)),
        BitField(FID.DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL,
                 LEN.DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL,
                 title='DeviceReportingFlagConsumerVendorSpecificControl',
                 name='device_reporting_flag_consumer_vendor_specific_control',
                 checks=(CheckHexList(LEN.DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.DEVICE_REPORTING_FLAG_CONSUMER_VENDOR_SPECIFIC_CONTROL) - 1),)),

        # RECEIVER_REPORTING_FLAG
        BitField(FID.RECEIVER_REPORTING_FLAG_RESERVED,
                 LEN.RECEIVER_REPORTING_FLAG_RESERVED,
                 title='ReceiverReportingFlagReserved',
                 name='receiver_reporting_flag_reserved',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS,
                 LEN.RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS,
                 title='ReceiverReportingFlagChannelChangeNotifications',
                 name='receiver_reporting_flag_channel_change_notifications',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_CHANNEL_CHANGE_NOTIFICATIONS) - 1),)),
        BitField(FID.RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS,
                 LEN.RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS,
                 title='ReceiverReportingFlagAttackDetectionNotifications',
                 name='receiver_reporting_flag_attack_detection_notifications',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_ATTACK_DETECTION_NOTIFICATIONS) - 1),)),
        BitField(FID.RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS,
                 LEN.RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS,
                 title='ReceiverReportingFlagTouchpadMultiTouchNotifications',
                 name='receiver_reporting_flag_touchpad_multi_touch_notifications',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2,
                                                LEN.RECEIVER_REPORTING_FLAG_TOUCHPAD_MULTI_TOUCH_NOTIFICATIONS) - 1),)),
        BitField(FID.RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT,
                 LEN.RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT,
                 title='ReceiverReportingFlagSoftwarePresent',
                 name='receiver_reporting_flag_software_present',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_SOFTWARE_PRESENT) - 1),)),
        BitField(FID.RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO,
                 LEN.RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO,
                 title='ReceiverReportingFlagQuadLinkQualityInfo',
                 name='receiver_reporting_flag_quad_link_quality_info',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_QUAD_LINK_QUALITY_INFO) - 1),)),
        BitField(FID.RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS,
                 LEN.RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS,
                 title='ReceiverReportingFlagUINotifications',
                 name='receiver_reporting_flag_ui_notifications',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_UI_NOTIFICATIONS) - 1),)),
        BitField(FID.RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS,
                 LEN.RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS,
                 title='ReceiverReportingFlagWirelessNotifications',
                 name='receiver_reporting_flag_wireless_notifications',
                 checks=(CheckHexList(LEN.RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.RECEIVER_REPORTING_FLAG_WIRELESS_NOTIFICATIONS) - 1),)),

        # DEVICE_CONT_REPORTING_FLAG
        BitField(FID.DEVICE_CONT_REPORTING_RESERVED,
                 LEN.DEVICE_CONT_REPORTING_RESERVED,
                 title='DeviceContReportingFlagReserved',
                 name='device_cont_reporting_reserved',
                 checks=(CheckHexList(LEN.DEVICE_CONT_REPORTING_RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_CONT_REPORTING_RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE,
                 LEN.DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE,
                 title='DeviceContReportingFlagConfigurationComplete',
                 name='device_cont_reporting_flag_configuration_complete',
                 checks=(CheckHexList(LEN.DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.DEVICE_CONT_REPORTING_FLAG_CONFIGURATION_COMPLETE) - 1),)),
        BitField(FID.DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY,
                 LEN.DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY,
                 title='DeviceContReportingFlagVoIPTelephony',
                 name='device_cont_reporting_flag_vo_ip_telephony',
                 checks=(CheckHexList(LEN.DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY // 8),
                         CheckInt(min_value=0,
                                  max_value=pow(2, LEN.DEVICE_CONT_REPORTING_FLAG_VO_IP_TELEPHONY) - 1),)),
        BitField(FID.DEVICE_CONT_REPORTING_FLAG_3D_GESTURE,
                 LEN.DEVICE_CONT_REPORTING_FLAG_3D_GESTURE,
                 title='DeviceContReportingFlag3DGesture',
                 name='device_cont_reporting_flag_3d_gesture',
                 checks=(CheckHexList(LEN.DEVICE_CONT_REPORTING_FLAG_3D_GESTURE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_CONT_REPORTING_FLAG_3D_GESTURE) - 1),)),
    )

    def device_reporting_flags(self):
        return (self.device_reporting_flag_numpad_numeric_keys << 7) + \
               (self.device_reporting_flag_f_lock_status << 6) + \
               (self.device_reporting_flag_roller_h << 5) + \
               (self.device_reporting_flag_battery_status << 4) + \
               (self.device_reporting_flag_mouse_extra_buttons << 3) + \
               (self.device_reporting_flag_roller_v << 2) + \
               (self.device_reporting_flag_power_keys << 1) + \
               (self.device_reporting_flag_consumer_vendor_specific_control)
    # end def device_reporting_flags

    def receiver_reporting_flags(self):
        return (self.receiver_reporting_flag_reserved << 6) + \
               (self.receiver_reporting_flag_attack_detection_notifications << 5) + \
               (self.receiver_reporting_flag_touchpad_multi_touch_notifications << 4) + \
               (self.receiver_reporting_flag_software_present << 3) + \
               (self.receiver_reporting_flag_quad_link_quality_info << 2) + \
               (self.receiver_reporting_flag_ui_notifications << 1) + \
               (self.receiver_reporting_flag_wireless_notifications)
    # end def device_reporting_flags

# end class HidppReportingFlagsStructure


class SetEnableHidppReportingRequest(SetRegister):
    """
    Enable HID++ reporting write short register command
    """

    FIELDS = SetRegister.FIELDS + HidppReportingFlagsStructure.FIELDS

    def __init__(self,
                 device_reporting_flag_numpad_numeric_keys=0, device_reporting_flag_f_lock_status=0,
                 device_reporting_flag_roller_h=0, device_reporting_flag_battery_status=0,
                 device_reporting_flag_mouse_extra_buttons=0, device_reporting_flag_roller_v=0,
                 device_reporting_flag_power_keys=0, device_reporting_flag_consumer_vendor_specific_control=0,
                 receiver_reporting_flag_channel_change_notifications=0,
                 receiver_reporting_flag_attack_detection_notifications=0,
                 receiver_reporting_flag_touchpad_multi_touch_notifications=0,
                 receiver_reporting_flag_software_present=0, receiver_reporting_flag_quad_link_quality_info=0,
                 receiver_reporting_flag_ui_notifications=0, receiver_reporting_flag_wireless_notifications=0,
                 device_cont_reporting_flag_configuration_complete=0,
                 device_cont_reporting_flag_vo_ip_telephony=0, device_cont_reporting_flag_3d_gesture=0,):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENABLE_HIDPP_REPORTING)

        self.device_reporting_flag_numpad_numeric_keys = device_reporting_flag_numpad_numeric_keys
        self.device_reporting_flag_f_lock_status = device_reporting_flag_f_lock_status
        self.device_reporting_flag_roller_h = device_reporting_flag_roller_h
        self.device_reporting_flag_battery_status = device_reporting_flag_battery_status
        self.device_reporting_flag_mouse_extra_buttons = device_reporting_flag_mouse_extra_buttons
        self.device_reporting_flag_roller_v = device_reporting_flag_roller_v
        self.device_reporting_flag_power_keys = device_reporting_flag_power_keys
        self.device_reporting_flag_consumer_vendor_specific_control = \
            device_reporting_flag_consumer_vendor_specific_control
        self.receiver_reporting_flag_channel_change_notifications = receiver_reporting_flag_channel_change_notifications
        self.receiver_reporting_flag_attack_detection_notifications = \
            receiver_reporting_flag_attack_detection_notifications
        self.receiver_reporting_flag_touchpad_multi_touch_notifications = \
            receiver_reporting_flag_touchpad_multi_touch_notifications
        self.receiver_reporting_flag_software_present = receiver_reporting_flag_software_present
        self.receiver_reporting_flag_quad_link_quality_info = \
            receiver_reporting_flag_quad_link_quality_info
        self.receiver_reporting_flag_ui_notifications = receiver_reporting_flag_ui_notifications
        self.receiver_reporting_flag_wireless_notifications = receiver_reporting_flag_wireless_notifications
        self.device_cont_reporting_flag_configuration_complete = device_cont_reporting_flag_configuration_complete
        self.device_cont_reporting_flag_vo_ip_telephony = device_cont_reporting_flag_vo_ip_telephony
        self.device_cont_reporting_flag_3d_gesture = device_cont_reporting_flag_3d_gesture
    # end def __init__
# end class SetEnableHidppReportingRequest


class SetEnableHidppReportingResponse(SetRegisterResponse):
    """
    Enable HID++ reporting write short register command
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENABLE_HIDPP_REPORTING)
    # end def __init__
# end class SetEnableHidppReportingResponse


class GetEnableHidppReportingRequest(GetRegisterRequest):
    """
    Enable HID++ reporting read short register command
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENABLE_HIDPP_REPORTING)
    # end def __init__
# end class GetEnableHidppReportingRequest


class GetEnableHidppReportingResponse(GetRegister):
    """
    Enable HID++ reporting write short register command
    """
    FIELDS = GetRegister.FIELDS + HidppReportingFlagsStructure.FIELDS

    def __init__(self,
                 device_reporting_flag_numpad_numeric_keys=0, device_reporting_flag_f_lock_status=0,
                 device_reporting_flag_roller_h=0, device_reporting_flag_battery_status=0, \
                 device_reporting_flag_mouse_extra_buttons=0, device_reporting_flag_roller_v=0,
                 device_reporting_flag_power_keys=0, device_reporting_flag_consumer_vendor_specific_control=0,
                 receiver_reporting_flag_channel_change_notifications=0,
                 receiver_reporting_flag_attack_detection_notifications=0,
                 receiver_reporting_flag_touchpad_multi_touch_notifications=0,
                 receiver_reporting_flag_software_present=0, receiver_reporting_flag_quad_link_quality_info=0,
                 receiver_reporting_flag_ui_notifications=0, receiver_reporting_flag_wireless_notifications=0,
                 device_cont_reporting_flag_configuration_complete=0,
                 device_cont_reporting_flag_vo_ip_telephony=0, device_cont_reporting_flag_3d_gesture=0,):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.ENABLE_HIDPP_REPORTING)

        self.device_reporting_flag_numpad_numeric_keys = device_reporting_flag_numpad_numeric_keys
        self.device_reporting_flag_f_lock_status = device_reporting_flag_f_lock_status
        self.device_reporting_flag_roller_h = device_reporting_flag_roller_h
        self.device_reporting_flag_battery_status = device_reporting_flag_battery_status
        self.device_reporting_flag_mouse_extra_buttons = device_reporting_flag_mouse_extra_buttons
        self.device_reporting_flag_roller_v = device_reporting_flag_roller_v
        self.device_reporting_flag_power_keys = device_reporting_flag_power_keys
        self.device_reporting_flag_consumer_vendor_specific_control = \
            device_reporting_flag_consumer_vendor_specific_control
        self.receiver_reporting_flag_channel_change_notifications = receiver_reporting_flag_channel_change_notifications
        self.receiver_reporting_flag_attack_detection_notifications = \
            receiver_reporting_flag_attack_detection_notifications
        self.receiver_reporting_flag_touchpad_multi_touch_notifications = \
            receiver_reporting_flag_touchpad_multi_touch_notifications
        self.receiver_reporting_flag_software_present = receiver_reporting_flag_software_present
        self.receiver_reporting_flag_quad_link_quality_info = \
            receiver_reporting_flag_quad_link_quality_info
        self.receiver_reporting_flag_ui_notifications = receiver_reporting_flag_ui_notifications
        self.receiver_reporting_flag_wireless_notifications = receiver_reporting_flag_wireless_notifications
        self.device_cont_reporting_flag_configuration_complete = device_cont_reporting_flag_configuration_complete
        self.device_cont_reporting_flag_vo_ip_telephony = device_cont_reporting_flag_vo_ip_telephony
        self.device_cont_reporting_flag_3d_gesture = device_cont_reporting_flag_3d_gesture
    # end def __init__
# end class GetEnableHidppReportingResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
