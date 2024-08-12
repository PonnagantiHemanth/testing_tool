#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.brightnesscontrol
:brief: HID++ 2.0 ``BrightnessControl`` command interface definition
:author: YY Liu <yliu5@logitech.com>
:date: 2023/08/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrightnessControl(HidppMessage):
    """
    This feature is for devices with a hardware brightness control capability.
    """
    FEATURE_ID = 0x8040
    MAX_FUNCTION_INDEX_V0 = 2
    MAX_FUNCTION_INDEX_V1 = 4

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
# end class BrightnessControl


class CapabilitiesV0(BitFieldContainerMixin):
    """
    Define ``Capabilities`` information for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      6
    Events                        1
    HW Brightness                 1
    ============================  ==========
    """

    class FID(object):
        """
        Field identifiers
        """
        RESERVED = 0xFF
        EVENTS = RESERVED - 1
        HW_BRIGHTNESS = EVENTS - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED = 0x6
        EVENTS = 0x1
        HW_BRIGHTNESS = 0x1
    # end class LEN

    class POS(object):
        """
        CapabilitiesV0 bit field position
        """
        EVENTS = 1
        HW_BRIGHTNESS = 0
    # end class POS

    class DEFAULT:
        """
        Field default values
        """
        RESERVED = 0x0
    # end class DEFAULT

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=DEFAULT.RESERVED),
        BitField(fid=FID.EVENTS, length=LEN.EVENTS,
                 title="Events", name="events",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.EVENTS) - 1),)),
        BitField(fid=FID.HW_BRIGHTNESS, length=LEN.HW_BRIGHTNESS,
                 title="HwBrightness", name="hw_brightness",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.HW_BRIGHTNESS) - 1),)),
    )
# end class CapabilitiesV0


class CapabilitiesV1(CapabilitiesV0):
    """
    Define ``Capabilities`` information for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      3
    Transient                     1
    HW On Off                     1
    Illumination                  1
    Events                        1
    HW Brightness                 1
    ============================  ==========
    """

    class FID(CapabilitiesV0.FID):
        # See ``CapabilitiesV0.FID``
        TRANSIENT = CapabilitiesV0.FID.RESERVED - 1
        HW_ON_OFF = TRANSIENT - 1
        ILLUMINATION = HW_ON_OFF - 1
        EVENTS = ILLUMINATION - 1
        HW_BRIGHTNESS = EVENTS - 1
    # end class FID

    class LEN(CapabilitiesV0.LEN):
        # See ``CapabilitiesV0.LEN``
        RESERVED = 0x3
        TRANSIENT = 0x1
        HW_ON_OFF = 0x1
        ILLUMINATION = 0x1
        EVENTS = 0x1
        HW_BRIGHTNESS = 0x1
    # end class LEN

    class POS(object):
        """
        CapabilitiesV1 bit field position
        """
        TRANSIENT = 4
        HW_ON_OFF = 3
        ILLUMINATION = 2
        EVENTS = 1
        HW_BRIGHTNESS = 0
    # end class POS

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=CapabilitiesV0.DEFAULT.RESERVED),
        BitField(fid=FID.TRANSIENT, length=LEN.TRANSIENT,
                 title="Transient", name="transient",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.TRANSIENT) - 1),)),
        BitField(fid=FID.HW_ON_OFF, length=LEN.HW_ON_OFF,
                 title="HWOnOff", name="hw_on_off",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.HW_ON_OFF) - 1),)),
        BitField(fid=FID.ILLUMINATION, length=LEN.ILLUMINATION,
                 title="Illumination", name="illumination",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ILLUMINATION) - 1),)),
        BitField(fid=FID.EVENTS, length=LEN.EVENTS,
                 title="Events", name="events",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.EVENTS) - 1),)),
        BitField(fid=FID.HW_BRIGHTNESS, length=LEN.HW_BRIGHTNESS,
                 title="HwBrightness ", name="hw_brightness",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.HW_BRIGHTNESS) - 1),)),
    )
# end class CapabilitiesV1


class IlluminationState(BitFieldContainerMixin):
    """
    Define ``IlluminationState`` information

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    State                         1
    ============================  ==========
    """
    OFF = 0
    ON = 1

    class FID(object):
        """
        Field identifiers
        """
        RESERVED = 0xFF
        STATE = RESERVED - 1
    # end class FID

    class LEN(object):
        """
        Field lengths in bits
        """
        RESERVED = 0x7
        STATE = 0x1
    # end class LEN

    FIELDS = (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
        BitField(fid=FID.STATE, length=LEN.STATE,
                 title="State", name="state",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.STATE) - 1),)),
    )
# end class IlluminationState


class BrightnessControlModel(FeatureModel):
    """
    Define ``BrightnessControl`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_INFO = 0
        GET_BRIGHTNESS = 1
        SET_BRIGHTNESS = 2
        GET_ILLUMINATION = 3
        SET_ILLUMINATION = 4

        # Event index
        BRIGHTNESS_CHANGE = 0
        ILLUMINATION_CHANGE = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``BrightnessControl`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_INFO: {
                    "request": GetInfo,
                    "response": GetInfoResponseV0
                },
                cls.INDEX.GET_BRIGHTNESS: {
                    "request": GetBrightness,
                    "response": GetBrightnessResponse
                },
                cls.INDEX.SET_BRIGHTNESS: {
                    "request": SetBrightness,
                    "response": SetBrightnessResponse
                }
            },
            "events": {
                cls.INDEX.BRIGHTNESS_CHANGE: {"report": BrightnessChangeEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_INFO: {
                    "request": GetInfo,
                    "response": GetInfoResponseV1
                },
                cls.INDEX.GET_BRIGHTNESS: {
                    "request": GetBrightness,
                    "response": GetBrightnessResponse
                },
                cls.INDEX.SET_BRIGHTNESS: {
                    "request": SetBrightness,
                    "response": SetBrightnessResponse
                },
                cls.INDEX.GET_ILLUMINATION: {
                    "request": GetIllumination,
                    "response": GetIlluminationResponse
                },
                cls.INDEX.SET_ILLUMINATION: {
                    "request": SetIllumination,
                    "response": SetIlluminationResponse
                }
            },
            "events": {
                cls.INDEX.BRIGHTNESS_CHANGE: {"report": BrightnessChangeEvent},
                cls.INDEX.ILLUMINATION_CHANGE: {"report": IlluminationChangeEvent}
            }
        }

        return {
            "feature_base": BrightnessControl,
            "versions": {
                BrightnessControlV0.VERSION: {
                    "main_cls": BrightnessControlV0,
                    "api": function_map_v0
                },
                BrightnessControlV1.VERSION: {
                    "main_cls": BrightnessControlV1,
                    "api": function_map_v1
                },
            }
        }
    # end def _get_data_model
# end class BrightnessControlModel


# noinspection DuplicatedCode
class BrightnessControlFactory(FeatureFactory):
    """
    Get ``BrightnessControl`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``BrightnessControl`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``BrightnessControlInterface``
        """
        return BrightnessControlModel.get_main_cls(version)()
    # end def create
# end class BrightnessControlFactory


class BrightnessControlInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``BrightnessControl``
    """

    def __init__(self):
        # Requests
        self.get_info_cls = None
        self.get_brightness_cls = None
        self.set_brightness_cls = None
        self.get_illumination_cls = None
        self.set_illumination_cls = None

        # Responses
        self.get_info_response_cls = None
        self.get_brightness_response_cls = None
        self.set_brightness_response_cls = None
        self.get_illumination_response_cls = None
        self.set_illumination_response_cls = None

        # Events
        self.brightness_change_event_cls = None
        self.illumination_change_event_cls = None
    # end def __init__
# end class BrightnessControlInterface


class BrightnessControlV0(BrightnessControlInterface):
    """
    Define ``BrightnessControlV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getInfo() -> maxBrightness, steps, capabilities

    [1] getBrightness() -> brightness

    [2] setBrightness(brightness) -> None

    [Event 0] BrightnessChangeEvent -> brightness
    """
    VERSION = 0

    def __init__(self):
        # See ``BrightnessControl.__init__``
        super().__init__()
        index = BrightnessControlModel.INDEX

        # Requests
        self.get_info_cls = BrightnessControlModel.get_request_cls(
            self.VERSION, index.GET_INFO)
        self.get_brightness_cls = BrightnessControlModel.get_request_cls(
            self.VERSION, index.GET_BRIGHTNESS)
        self.set_brightness_cls = BrightnessControlModel.get_request_cls(
            self.VERSION, index.SET_BRIGHTNESS)

        # Responses
        self.get_info_response_cls = BrightnessControlModel.get_response_cls(
            self.VERSION, index.GET_INFO)
        self.get_brightness_response_cls = BrightnessControlModel.get_response_cls(
            self.VERSION, index.GET_BRIGHTNESS)
        self.set_brightness_response_cls = BrightnessControlModel.get_response_cls(
            self.VERSION, index.SET_BRIGHTNESS)

        # Events
        self.brightness_change_event_cls = BrightnessControlModel.get_report_cls(
            self.VERSION, index.BRIGHTNESS_CHANGE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``BrightnessControlInterface.get_max_function_index``
        return BrightnessControlModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class BrightnessControlV0


class BrightnessControlV1(BrightnessControlV0):
    """
    Define ``BrightnessControlV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getInfo() -> maxBrightness, steps, capabilities

    [1] getBrightness() -> brightness

    [2] setBrightness(brightness) -> None

    [3] getIllumination() -> state

    [4] setIllumination() -> None

    [Event 0] BrightnessChangeEvent -> brightness

    [Event 1] IlluminationChangeEvent -> state
    """
    VERSION = 1

    def __init__(self):
        # See ``BrightnessControl.__init__``
        super().__init__()
        index = BrightnessControlModel.INDEX

        # Requests
        self.get_illumination_cls = BrightnessControlModel.get_request_cls(
            self.VERSION, index.GET_ILLUMINATION)
        self.set_illumination_cls = BrightnessControlModel.get_request_cls(
            self.VERSION, index.SET_ILLUMINATION)

        # Responses
        self.get_illumination_response_cls = BrightnessControlModel.get_response_cls(
            self.VERSION, index.GET_ILLUMINATION)
        self.set_illumination_response_cls = BrightnessControlModel.get_response_cls(
            self.VERSION, index.SET_ILLUMINATION)

        # Events
        self.illumination_change_event_cls = BrightnessControlModel.get_report_cls(
            self.VERSION, index.ILLUMINATION_CHANGE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``BrightnessControlInterface.get_max_function_index``
        return BrightnessControlModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class BrightnessControlV1


class ShortEmptyPacketDataFormat(BrightnessControl):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetBrightness
        - GetInfo

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        PADDING = BrightnessControl.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(BrightnessControl):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetBrightnessResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        PADDING = BrightnessControl.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class BrightnessData(BrightnessControl):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - BrightnessChangeEvent
        - GetBrightnessResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Brightness                    16
    Padding                       112
    ============================  ==========
    """

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        BRIGHTNESS = BrightnessControl.FID.SOFTWARE_ID - 1
        PADDING = BRIGHTNESS - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        BRIGHTNESS = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.BRIGHTNESS, length=LEN.BRIGHTNESS,
                 title="Brightness", name="brightness",
                 checks=(CheckHexList(LEN.BRIGHTNESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BRIGHTNESS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),
    )
# end class BrightnessData


class IlluminationStateContainer(BrightnessControl):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetIlluminationResponse
        - IlluminationChangeEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Illumination State            8
    Padding                       120
    ============================  ==========
    """
    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        ILLUMINATION_STATE = BrightnessControl.FID.SOFTWARE_ID - 1
        PADDING = ILLUMINATION_STATE - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        ILLUMINATION_STATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.ILLUMINATION_STATE, length=LEN.ILLUMINATION_STATE,
                 title="IlluminationState", name="illumination_state",
                 checks=(CheckHexList(LEN.ILLUMINATION_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ILLUMINATION_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),
    )
# end class IlluminationStateContainer


class GetInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetInfo`` implementation class
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
                         function_index=GetInfoResponseV0.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetInfo


class GetBrightness(ShortEmptyPacketDataFormat):
    """
    Define ``GetBrightness`` implementation class
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
                         function_index=GetBrightnessResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetBrightness


class SetBrightness(BrightnessControl):
    """
    Define ``SetBrightness`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Brightness                    16
    Padding                       8
    ============================  ==========
    """

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        BRIGHTNESS = BrightnessControl.FID.SOFTWARE_ID - 1
        PADDING = BRIGHTNESS - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        BRIGHTNESS = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.BRIGHTNESS, length=LEN.BRIGHTNESS,
                 title="Brightness", name="brightness",
                 checks=(CheckHexList(LEN.BRIGHTNESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BRIGHTNESS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, brightness, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param brightness: Brightness
        :type brightness: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetBrightnessResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        self.brightness = brightness
    # end def __init__
# end class SetBrightness


class GetIllumination(ShortEmptyPacketDataFormat):
    """
    Define ``GetIllumination`` implementation class
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
                         function_index=GetIlluminationResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetIllumination


class SetIllumination(BrightnessControl):
    """
    Define ``SetIllumination`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Illumination State            8
    Padding                       16
    ============================  ==========
    """

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        ILLUMINATION_STATE = BrightnessControl.FID.SOFTWARE_ID - 1
        PADDING = ILLUMINATION_STATE - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        ILLUMINATION_STATE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.ILLUMINATION_STATE, length=LEN.ILLUMINATION_STATE,
                 title="IlluminationState", name="illumination_state",
                 checks=(CheckHexList(LEN.ILLUMINATION_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ILLUMINATION_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param state: Illumination State
        :type state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetIlluminationResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        self.illumination_state = IlluminationState(state=state)
    # end def __init__
# end class SetIllumination


class GetInfoResponseV0(BrightnessControl):
    """
    Define ``GetInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Max Brightness                16
    Steps                         8
    Capabilities                  8
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        MAX_BRIGHTNESS = BrightnessControl.FID.SOFTWARE_ID - 1
        STEPS = MAX_BRIGHTNESS - 1
        CAPABILITIES = STEPS - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        MAX_BRIGHTNESS = 0x10
        STEPS = 0x8
        CAPABILITIES = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.MAX_BRIGHTNESS, length=LEN.MAX_BRIGHTNESS,
                 title="MaxBrightness", name="max_brightness",
                 checks=(CheckHexList(LEN.MAX_BRIGHTNESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_BRIGHTNESS) - 1),)),
        BitField(fid=FID.STEPS, length=LEN.STEPS,
                 title="Steps", name="steps",
                 checks=(CheckHexList(LEN.STEPS // 8), CheckByte(),)),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, max_brightness, steps, events, hw_brightness, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param max_brightness: Max Brightness
        :type max_brightness: ``int | HexList``
        :param steps: Steps
        :type steps: ``int | HexList``
        :param events: Events
        :type events: ``int | HexList``
        :param hw_brightness: HW brightness
        :type hw_brightness: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.max_brightness = max_brightness
        self.steps = steps
        self.capabilities = CapabilitiesV0(events=events, hw_brightness=hw_brightness)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capabilities = CapabilitiesV0.fromHexList(
            inner_field_container_mixin.capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetInfoResponseV0


class GetInfoResponseV1(BrightnessControl):
    """
    Define ``GetInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Max Brightness                16
    Steps LSB                     8
    Capabilities                  8
    Min Brightness                16
    Steps MSB                     8
    Padding                       72
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfo,)
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(BrightnessControl.FID):
        # See ``BrightnessControl.FID``
        MAX_BRIGHTNESS = BrightnessControl.FID.SOFTWARE_ID - 1
        STEPS_LSB = MAX_BRIGHTNESS - 1
        CAPABILITIES = STEPS_LSB - 1
        MIN_BRIGHTNESS = CAPABILITIES - 1
        STEPS_MSB = MIN_BRIGHTNESS - 1
        PADDING = STEPS_MSB - 1
    # end class FID

    class LEN(BrightnessControl.LEN):
        # See ``BrightnessControl.LEN``
        MAX_BRIGHTNESS = 0x10
        STEPS_LSB = 0x8
        CAPABILITIES = 0x8
        MIN_BRIGHTNESS = 0x10
        STEPS_MSB = 0x8
        PADDING = 0x48
    # end class LEN

    FIELDS = BrightnessControl.FIELDS + (
        BitField(fid=FID.MAX_BRIGHTNESS, length=LEN.MAX_BRIGHTNESS,
                 title="MaxBrightness", name="max_brightness",
                 checks=(CheckHexList(LEN.MAX_BRIGHTNESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_BRIGHTNESS) - 1),)),
        BitField(fid=FID.STEPS_LSB, length=LEN.STEPS_LSB,
                 title="StepsLsb", name="steps_lsb",
                 checks=(CheckHexList(LEN.STEPS_LSB // 8), CheckByte(),)),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8), CheckByte(),)),
        BitField(fid=FID.MIN_BRIGHTNESS, length=LEN.MIN_BRIGHTNESS,
                 title="MinBrightness", name="min_brightness",
                 checks=(CheckHexList(LEN.MIN_BRIGHTNESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MIN_BRIGHTNESS) - 1),)),
        BitField(fid=FID.STEPS_MSB, length=LEN.STEPS_MSB,
                 title="StepsMsb", name="steps_msb",
                 checks=(CheckHexList(LEN.STEPS_MSB // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=BrightnessControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, max_brightness, steps_lsb, transient, hw_on_off, illumination,
                 events, hw_brightness, min_brightness, steps_msb, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param max_brightness: Max Brightness
        :type max_brightness: ``int | HexList``
        :param steps_lsb: Steps LSB
        :type steps_lsb: ``int | HexList``
        :param transient: Transient
        :type transient: ``int``
        :param hw_on_off: HW On/Off
        :type hw_on_off: ``int``
        :param illumination: Illumination
        :type illumination: ``int``
        :param events: Events
        :type events: ``int``
        :param hw_brightness: HW Brightness
        :type hw_brightness: ``int``
        :param min_brightness: Min Brightness
        :type min_brightness: ``int | HexList``
        :param step_msb: Steps MSB
        :type steps_lsb: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.max_brightness = max_brightness
        self.steps_lsb = steps_lsb
        self.steps_msb = steps_msb
        self.capabilities = CapabilitiesV1(transient=transient,
                                           hw_on_off=hw_on_off,
                                           illumination=illumination,
                                           events=events,
                                           hw_brightness=hw_brightness)
        self.min_brightness = min_brightness
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capabilities = CapabilitiesV1.fromHexList(
            inner_field_container_mixin.capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetInfoResponseV1


class GetBrightnessResponse(BrightnessData):
    """
    Define ``GetBrightnessResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Brightness                    16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetBrightness,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, brightness, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param brightness: Brightness
        :type brightness: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.brightness = brightness
    # end def __init__
# end class GetBrightnessResponse


class SetBrightnessResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetBrightnessResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetBrightness,)
    VERSION = (0, 1,)
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
# end class SetBrightnessResponse


class GetIlluminationResponse(IlluminationStateContainer):
    """
    Define ``GetIlluminationResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Illumination State            8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetIllumination,)
    VERSION = (1,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param state: Illumination State
        :type state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.illumination_state = IlluminationState(state=state)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.illumination_state = IlluminationState.fromHexList(
            inner_field_container_mixin.illumination_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetIlluminationResponse


class SetIlluminationResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetIlluminationResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetIllumination,)
    VERSION = (1,)
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
# end class SetIlluminationResponse


class BrightnessChangeEvent(BrightnessData):
    """
    Define ``BrightnessChangeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Brightness                    16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, brightness, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param brightness: Brightness
        :type brightness: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.brightness = brightness
    # end def __init__
# end class BrightnessChangeEvent


class IlluminationChangeEvent(IlluminationStateContainer):
    """
    Define ``IlluminationChangeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Illumination State            8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param state: Illumination state
        :type state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.illumination_state = IlluminationState(state=state)
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``GetInfoResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.illumination_state = IlluminationState.fromHexList(
            inner_field_container_mixin.illumination_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class IlluminationChangeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
