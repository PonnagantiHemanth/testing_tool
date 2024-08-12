#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.peripheral.testkeysdisplay
:brief: HID++ 2.0 ``TestKeysDisplay`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/02
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# noinspection DuplicatedCode
class TestKeysDisplay(HidppMessage):
    """
    Test and calibration of key display device like Lexend contextual keys display.
    """
    FEATURE_ID = 0x92E2
    MAX_FUNCTION_INDEX_V0 = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class TestKeysDisplay


# noinspection DuplicatedCode
class TestKeysDisplayModel(FeatureModel):
    """
    Define ``TestKeysDisplay`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        SET_BACKLIGHT_PWM_DUTY_CYCLE = 1
        SET_DISPLAY_RGB_VALUE = 2
        SET_DISPLAY_POWER_STATE = 3
        SET_KEY_ICON = 4
        SET_KEY_CALIBRATION_OFFSET = 5
        SET_KEY_CALIBRATION_OFFSET_IN_FLASH = 6
        SET_DISPLAY_AGEING_MODE_STATE = 7

        # Event index
        KEY_PRESS = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``TestKeysDisplay`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.SET_BACKLIGHT_PWM_DUTY_CYCLE: {
                    "request": SetBacklightPWMDutyCycle,
                    "response": SetBacklightPWMDutyCycleResponse
                },
                cls.INDEX.SET_DISPLAY_RGB_VALUE: {
                    "request": SetDisplayRGBValue,
                    "response": SetDisplayRGBValueResponse
                },
                cls.INDEX.SET_DISPLAY_POWER_STATE: {
                    "request": SetDisplayPowerState,
                    "response": SetDisplayPowerStateResponse
                },
                cls.INDEX.SET_KEY_ICON: {
                    "request": SetKeyIcon,
                    "response": SetKeyIconResponse
                },
                cls.INDEX.SET_KEY_CALIBRATION_OFFSET: {
                    "request": SetKeyCalibrationOffset,
                    "response": SetKeyCalibrationOffsetResponse
                },
                cls.INDEX.SET_KEY_CALIBRATION_OFFSET_IN_FLASH: {
                    "request": SetKeyCalibrationOffsetInFlash,
                    "response": SetKeyCalibrationOffsetInFlashResponse
                },
                cls.INDEX.SET_DISPLAY_AGEING_MODE_STATE: {
                    "request": SetDisplayAgeingModeState,
                    "response": SetDisplayAgeingModeStateResponse
                }
            },
            "events": {
                cls.INDEX.KEY_PRESS: {"report": KeyPressEvent}
            }
        }

        return {
            "feature_base": TestKeysDisplay,
            "versions": {
                TestKeysDisplayV0.VERSION: {
                    "main_cls": TestKeysDisplayV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class TestKeysDisplayModel


class TestKeysDisplayFactory(FeatureFactory):
    """
    Get ``TestKeysDisplay`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``TestKeysDisplay`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``TestKeysDisplayInterface``
        """
        return TestKeysDisplayModel.get_main_cls(version)()
    # end def create
# end class TestKeysDisplayFactory


class TestKeysDisplayInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``TestKeysDisplay``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.set_backlight_pwm_duty_cycle_cls = None
        self.set_display_rgb_value_cls = None
        self.set_display_power_state_cls = None
        self.set_key_icon_cls = None
        self.set_key_calibration_offset_cls = None
        self.set_key_calibration_offset_in_flash_cls = None
        self.set_display_ageing_mode_state_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.set_backlight_pwm_duty_cycle_response_cls = None
        self.set_display_rgb_value_response_cls = None
        self.set_display_power_state_response_cls = None
        self.set_key_icon_response_cls = None
        self.set_key_calibration_offset_response_cls = None
        self.set_key_calibration_offset_in_flash_response_cls = None
        self.set_display_ageing_mode_state_response_cls = None

        # Events
        self.key_press_event_cls = None
    # end def __init__
# end class TestKeysDisplayInterface


class TestKeysDisplayV0(TestKeysDisplayInterface):
    """
    Define ``TestKeysDisplayV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> capabilities

    [1] setBacklightPWMDutyCycle(dutyPwm) -> None

    [2] setDisplayRGBValue(red, blue, green) -> None

    [3] setDisplayPowerState(powerState) -> None

    [4] setKeyIcon(keyColumn, keyRow, iconIndex) -> None

    [5] setKeyCalibrationOffset(keyColumn, keyRow, xOffset, yOffset) -> None

    [6] setKeyCalibrationOffsetInFlash() -> None

    [7] setDisplayAgeingModeState() -> None

    [Event 0] KeyPressEvent -> btn0, btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12,
    btn13, btn14, btn15
    """
    VERSION = 0

    def __init__(self):
        # See ``TestKeysDisplay.__init__``
        super().__init__()
        index = TestKeysDisplayModel.INDEX

        # Requests
        self.get_capabilities_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.set_backlight_pwm_duty_cycle_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_BACKLIGHT_PWM_DUTY_CYCLE)
        self.set_display_rgb_value_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_DISPLAY_RGB_VALUE)
        self.set_display_power_state_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_DISPLAY_POWER_STATE)
        self.set_key_icon_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_KEY_ICON)
        self.set_key_calibration_offset_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_KEY_CALIBRATION_OFFSET)
        self.set_key_calibration_offset_in_flash_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_KEY_CALIBRATION_OFFSET_IN_FLASH)
        self.set_display_ageing_mode_state_cls = TestKeysDisplayModel.get_request_cls(
            self.VERSION, index.SET_DISPLAY_AGEING_MODE_STATE)

        # Responses
        self.get_capabilities_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.set_backlight_pwm_duty_cycle_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_BACKLIGHT_PWM_DUTY_CYCLE)
        self.set_display_rgb_value_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_DISPLAY_RGB_VALUE)
        self.set_display_power_state_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_DISPLAY_POWER_STATE)
        self.set_key_icon_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_KEY_ICON)
        self.set_key_calibration_offset_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_KEY_CALIBRATION_OFFSET)
        self.set_key_calibration_offset_in_flash_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_KEY_CALIBRATION_OFFSET_IN_FLASH)
        self.set_display_ageing_mode_state_response_cls = TestKeysDisplayModel.get_response_cls(
            self.VERSION, index.SET_DISPLAY_AGEING_MODE_STATE)

        # Events
        self.key_press_event_cls = TestKeysDisplayModel.get_report_cls(
            self.VERSION, index.KEY_PRESS)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``TestKeysDisplayInterface.get_max_function_index``
        return TestKeysDisplayModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class TestKeysDisplayV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(TestKeysDisplay):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities
        - SetDisplayAgeingModeState
        - SetKeyCalibrationOffsetInFlash

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        PADDING = TestKeysDisplay.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(TestKeysDisplay):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBacklightPWMDutyCycleResponse
        - SetDisplayAgeingModeStateResponse
        - SetDisplayPowerStateResponse
        - SetDisplayRGBValueResponse
        - SetKeyCalibrationOffsetInFlashResponse
        - SetKeyCalibrationOffsetResponse
        - SetKeyIconResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        PADDING = TestKeysDisplay.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetCapabilities(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


# noinspection DuplicatedCode
class SetBacklightPWMDutyCycle(TestKeysDisplay):
    """
    Define ``SetBacklightPWMDutyCycle`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Duty PWM                      16
    Padding                       8
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        DUTY_PWM = TestKeysDisplay.FID.SOFTWARE_ID - 1
        PADDING = DUTY_PWM - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        DUTY_PWM = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.DUTY_PWM, length=LEN.DUTY_PWM,
                 title="DutyPwm", name="duty_pwm",
                 checks=(CheckHexList(LEN.DUTY_PWM // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DUTY_PWM) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index, duty_pwm, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param duty_pwm: Duty PWM
        :type duty_pwm: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetBacklightPWMDutyCycleResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.duty_pwm = HexList(Numeral(duty_pwm, self.LEN.DUTY_PWM // 8))
    # end def __init__
# end class SetBacklightPWMDutyCycle


# noinspection DuplicatedCode
class SetDisplayRGBValue(TestKeysDisplay):
    """
    Define ``SetDisplayRGBValue`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RGB Value                     24
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        RGB_VALUE = TestKeysDisplay.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        RGB_VALUE = 0x18
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.RGB_VALUE, length=LEN.RGB_VALUE,
                 title="RgbValue", name="rgb_value",
                 checks=(CheckHexList(LEN.RGB_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RGB_VALUE) - 1),)),)

    def __init__(self, device_index, feature_index, rgb_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param rgb_value: RGB Value
        :type rgb_value: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetDisplayRGBValueResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.rgb_value = HexList(Numeral(rgb_value, self.LEN.RGB_VALUE // 8))
    # end def __init__
# end class SetDisplayRGBValue


# noinspection DuplicatedCode
class SetDisplayPowerState(TestKeysDisplay):
    """
    Define ``SetDisplayPowerState`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Power State                   8
    Padding                       16
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        POWER_STATE = TestKeysDisplay.FID.SOFTWARE_ID - 1
        PADDING = POWER_STATE - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        POWER_STATE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.POWER_STATE, length=LEN.POWER_STATE,
                 title="PowerState", name="power_state",
                 checks=(CheckHexList(LEN.POWER_STATE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),)

    def __init__(self, device_index, feature_index, power_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param power_state: Power State
        :type power_state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetDisplayPowerStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.power_state = HexList(Numeral(power_state, self.LEN.POWER_STATE // 8))
    # end def __init__
# end class SetDisplayPowerState


class SetKeyIcon(TestKeysDisplay):
    """
    Define ``SetKeyIcon`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Column                    8
    Key Row                       8
    Icon Index                    8
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        KEY_COLUMN = TestKeysDisplay.FID.SOFTWARE_ID - 1
        KEY_ROW = KEY_COLUMN - 1
        ICON_INDEX = KEY_ROW - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        KEY_COLUMN = 0x8
        KEY_ROW = 0x8
        ICON_INDEX = 0x8
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.KEY_COLUMN, length=LEN.KEY_COLUMN,
                 title="KeyColumn", name="key_column",
                 checks=(CheckHexList(LEN.KEY_COLUMN // 8), CheckByte(),)),
        BitField(fid=FID.KEY_ROW, length=LEN.KEY_ROW,
                 title="KeyRow", name="key_row",
                 checks=(CheckHexList(LEN.KEY_ROW // 8), CheckByte(),)),
        BitField(fid=FID.ICON_INDEX, length=LEN.ICON_INDEX,
                 title="IconIndex", name="icon_index",
                 checks=(CheckHexList(LEN.ICON_INDEX // 8), CheckByte(),)),)

    def __init__(self, device_index, feature_index, key_column, key_row, icon_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_column: Key Column
        :type key_column: ``int | HexList``
        :param key_row: Key Row
        :type key_row: ``int | HexList``
        :param icon_index: Icon Index
        :type icon_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetKeyIconResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.key_column = HexList(Numeral(key_column, self.LEN.KEY_COLUMN // 8))
        self.key_row = HexList(Numeral(key_row, self.LEN.KEY_ROW // 8))
        self.icon_index = HexList(Numeral(icon_index, self.LEN.ICON_INDEX // 8))
    # end def __init__
# end class SetKeyIcon


# noinspection DuplicatedCode
class SetKeyCalibrationOffset(TestKeysDisplay):
    """
    Define ``SetKeyCalibrationOffset`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Column                    8
    Key Row                       8
    X Offset                      8
    Y Offset                      8
    Padding                       96
    ============================  ==========
    """

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        KEY_COLUMN = TestKeysDisplay.FID.SOFTWARE_ID - 1
        KEY_ROW = KEY_COLUMN - 1
        X_OFFSET = KEY_ROW - 1
        Y_OFFSET = X_OFFSET - 1
        PADDING = Y_OFFSET - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        KEY_COLUMN = 0x8
        KEY_ROW = 0x8
        X_OFFSET = 0x8
        Y_OFFSET = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.KEY_COLUMN, length=LEN.KEY_COLUMN,
                 title="KeyColumn", name="key_column",
                 checks=(CheckHexList(LEN.KEY_COLUMN // 8), CheckByte(),)),
        BitField(fid=FID.KEY_ROW, length=LEN.KEY_ROW,
                 title="KeyRow", name="key_row",
                 checks=(CheckHexList(LEN.KEY_ROW // 8), CheckByte(),)),
        BitField(fid=FID.X_OFFSET, length=LEN.X_OFFSET,
                 title="XOffset", name="x_offset",
                 checks=(CheckHexList(LEN.X_OFFSET // 8), CheckByte(),)),
        BitField(fid=FID.Y_OFFSET, length=LEN.Y_OFFSET,
                 title="YOffset", name="y_offset",
                 checks=(CheckHexList(LEN.Y_OFFSET // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, key_column, key_row, x_offset, y_offset, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_column: Key Column
        :type key_column: ``int | HexList``
        :param key_row: Key Row
        :type key_row: ``int | HexList``
        :param x_offset: X Offset
        :type x_offset: ``int | HexList``
        :param y_offset: Y Offset
        :type y_offset: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetKeyCalibrationOffsetResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_column = HexList(Numeral(key_column, self.LEN.KEY_COLUMN // 8))
        self.key_row = HexList(Numeral(key_row, self.LEN.KEY_ROW // 8))
        self.x_offset = HexList(Numeral(x_offset, self.LEN.X_OFFSET // 8))
        self.y_offset = HexList(Numeral(y_offset, self.LEN.Y_OFFSET // 8))
    # end def __init__
# end class SetKeyCalibrationOffset


# noinspection DuplicatedCode
class SetKeyCalibrationOffsetInFlash(ShortEmptyPacketDataFormat):
    """
    Define ``SetKeyCalibrationOffsetInFlash`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetKeyCalibrationOffsetInFlashResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class SetKeyCalibrationOffsetInFlash


class SetDisplayAgeingModeState(ShortEmptyPacketDataFormat):
    """
    Define ``SetDisplayAgeingModeState`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetDisplayAgeingModeStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class SetDisplayAgeingModeState


class GetCapabilitiesResponse(TestKeysDisplay):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Capabilities                  8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        CAPABILITIES = TestKeysDisplay.FID.SOFTWARE_ID - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        CAPABILITIES = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, capabilities, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param capabilities: Capabilities
        :type capabilities: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        capabilities_copy = HexList(capabilities.copy())
        capabilities_copy.addPadding(self.LEN.CAPABILITIES // 8)
        self.capabilities = capabilities_copy
    # end def __init__
# end class GetCapabilitiesResponse


class SetBacklightPWMDutyCycleResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetBacklightPWMDutyCycleResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetBacklightPWMDutyCycle,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetBacklightPWMDutyCycleResponse


class SetDisplayRGBValueResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetDisplayRGBValueResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDisplayRGBValue,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDisplayRGBValueResponse


class SetDisplayPowerStateResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetDisplayPowerStateResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDisplayPowerState,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDisplayPowerStateResponse


class SetKeyIconResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetKeyIconResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetKeyIcon,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetKeyIconResponse


class SetKeyCalibrationOffsetResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetKeyCalibrationOffsetResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetKeyCalibrationOffset,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetKeyCalibrationOffsetResponse


class SetKeyCalibrationOffsetInFlashResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetKeyCalibrationOffsetInFlashResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetKeyCalibrationOffsetInFlash,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetKeyCalibrationOffsetInFlashResponse


class SetDisplayAgeingModeStateResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetDisplayAgeingModeStateResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetDisplayAgeingModeState,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetDisplayAgeingModeStateResponse


class KeyPressEvent(TestKeysDisplay):
    """
    Define ``KeyPressEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    btn7                          1
    btn6                          1
    btn5                          1
    btn4                          1
    btn3                          1
    btn2                          1
    btn1                          1
    btn0                          1
    btn15                         1
    btn14                         1
    btn13                         1
    btn12                         1
    btn11                         1
    btn10                         1
    btn9                          1
    btn8                          1
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(TestKeysDisplay.FID):
        # See ``TestKeysDisplay.FID``
        BTN7 = TestKeysDisplay.FID.SOFTWARE_ID - 1
        BTN6 = BTN7 - 1
        BTN5 = BTN6 - 1
        BTN4 = BTN5 - 1
        BTN3 = BTN4 - 1
        BTN2 = BTN3 - 1
        BTN1 = BTN2 - 1
        BTN0 = BTN1 - 1
        BTN15 = BTN0 - 1
        BTN14 = BTN15 - 1
        BTN13 = BTN14 - 1
        BTN12 = BTN13 - 1
        BTN11 = BTN12 - 1
        BTN10 = BTN11 - 1
        BTN9 = BTN10 - 1
        BTN8 = BTN9 - 1
        PADDING = BTN8 - 1
    # end class FID

    class LEN(TestKeysDisplay.LEN):
        # See ``TestKeysDisplay.LEN``
        BTN7 = 0x1
        BTN6 = 0x1
        BTN5 = 0x1
        BTN4 = 0x1
        BTN3 = 0x1
        BTN2 = 0x1
        BTN1 = 0x1
        BTN0 = 0x1
        BTN15 = 0x1
        BTN14 = 0x1
        BTN13 = 0x1
        BTN12 = 0x1
        BTN11 = 0x1
        BTN10 = 0x1
        BTN9 = 0x1
        BTN8 = 0x1
        PADDING = 0x70
    # end class LEN

    FIELDS = TestKeysDisplay.FIELDS + (
        BitField(fid=FID.BTN7, length=LEN.BTN7,
                 title="Btn7", name="btn7",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN7) - 1),)),
        BitField(fid=FID.BTN6, length=LEN.BTN6,
                 title="Btn6", name="btn6",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN6) - 1),)),
        BitField(fid=FID.BTN5, length=LEN.BTN5,
                 title="Btn5", name="btn5",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN5) - 1),)),
        BitField(fid=FID.BTN4, length=LEN.BTN4,
                 title="Btn4", name="btn4",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN4) - 1),)),
        BitField(fid=FID.BTN3, length=LEN.BTN3,
                 title="Btn3", name="btn3",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN3) - 1),)),
        BitField(fid=FID.BTN2, length=LEN.BTN2,
                 title="Btn2", name="btn2",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN2) - 1),)),
        BitField(fid=FID.BTN1, length=LEN.BTN1,
                 title="Btn1", name="btn1",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN1) - 1),)),
        BitField(fid=FID.BTN0, length=LEN.BTN0,
                 title="Btn0", name="btn0",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN0) - 1),)),
        BitField(fid=FID.BTN15, length=LEN.BTN15,
                 title="Btn15", name="btn15",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN15) - 1),)),
        BitField(fid=FID.BTN14, length=LEN.BTN14,
                 title="Btn14", name="btn14",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN14) - 1),)),
        BitField(fid=FID.BTN13, length=LEN.BTN13,
                 title="Btn13", name="btn13",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN13) - 1),)),
        BitField(fid=FID.BTN12, length=LEN.BTN12,
                 title="Btn12", name="btn12",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN12) - 1),)),
        BitField(fid=FID.BTN11, length=LEN.BTN11,
                 title="Btn11", name="btn11",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN11) - 1),)),
        BitField(fid=FID.BTN10, length=LEN.BTN10,
                 title="Btn10", name="btn10",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN10) - 1),)),
        BitField(fid=FID.BTN9, length=LEN.BTN9,
                 title="Btn9", name="btn9",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN9) - 1),)),
        BitField(fid=FID.BTN8, length=LEN.BTN8,
                 title="Btn8", name="btn8",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.BTN8) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TestKeysDisplay.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, btn7, btn6, btn5, btn4, btn3, btn2, btn1, btn0, btn15, btn14,
                 btn13, btn12, btn11, btn10, btn9, btn8, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param btn7: btn7
        :type btn7: ``bool | HexList``
        :param btn6: btn6
        :type btn6: ``bool | HexList``
        :param btn5: btn5
        :type btn5: ``bool | HexList``
        :param btn4: btn4
        :type btn4: ``bool | HexList``
        :param btn3: btn3
        :type btn3: ``bool | HexList``
        :param btn2: btn2
        :type btn2: ``bool | HexList``
        :param btn1: btn1
        :type btn1: ``bool | HexList``
        :param btn0: btn0
        :type btn0: ``bool | HexList``
        :param btn15: btn15
        :type btn15: ``bool | HexList``
        :param btn14: btn14
        :type btn14: ``bool | HexList``
        :param btn13: btn13
        :type btn13: ``bool | HexList``
        :param btn12: btn12
        :type btn12: ``bool | HexList``
        :param btn11: btn11
        :type btn11: ``bool | HexList``
        :param btn10: btn10
        :type btn10: ``bool | HexList``
        :param btn9: btn9
        :type btn9: ``bool | HexList``
        :param btn8: btn8
        :type btn8: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.btn7 = btn7
        self.btn6 = btn6
        self.btn5 = btn5
        self.btn4 = btn4
        self.btn3 = btn3
        self.btn2 = btn2
        self.btn1 = btn1
        self.btn0 = btn0
        self.btn15 = btn15
        self.btn14 = btn14
        self.btn13 = btn13
        self.btn12 = btn12
        self.btn11 = btn11
        self.btn10 = btn10
        self.btn9 = btn9
        self.btn8 = btn8
    # end def __init__
# end class KeyPressEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
