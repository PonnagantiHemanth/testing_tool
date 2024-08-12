#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.mouse.mousewheelanalytics
:brief: HID++ 2.0 ``MouseWheelAnalytics`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2023/10/18
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class MouseWheelAnalytics(HidppMessage):
    """
    This feature allows to get analytics data related to (main) wheel and thumbwheel
    """
    FEATURE_ID = 0x2251
    MAX_FUNCTION_INDEX_V0 = 4

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

    @unique
    class AnalyticsMode(IntEnum):
        """
        The analytics modes
        """
        OFF = 0
        ON = 1
    # end class AnalyticsMode

    @unique
    class WheelMode(IntEnum):
        """
        The wheel modes
        """
        FREE_SPIN = 1
        RATCHET = 2
    # end class WheelMode

    @unique
    class Wheel(IntEnum):
        """
        The scroll wheels available in mice
        """
        MAIN_WHEEL = 1
        THUMBWHEEL = 2
    # end class Wheel

    class Capabilities(BitFieldContainerMixin):
        """
        Define the device capabilities information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      4
        C_Thumbwheel                  1
        C_Smartshift                  1
        C_Ratchet_Free                1
        C_Main_Wheel                  1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            C_THUMBWHEEL = RESERVED - 1
            C_SMARTSHIFT = C_THUMBWHEEL - 1
            C_RATCHET_FREE = C_SMARTSHIFT - 1
            C_MAIN_WHEEL = C_RATCHET_FREE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x4
            C_THUMBWHEEL = 0x1
            C_SMARTSHIFT = 0x1
            C_RATCHET_FREE = 0x1
            C_MAIN_WHEEL = 0x1
        # end class LEN

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.C_THUMBWHEEL, length=LEN.C_THUMBWHEEL,
                     title="C_thumbwheel", name="c_thumbwheel",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.C_THUMBWHEEL) - 1),)),
            BitField(fid=FID.C_SMARTSHIFT, length=LEN.C_SMARTSHIFT,
                     title="C_smartshift", name="c_smartshift",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.C_SMARTSHIFT) - 1),)),
            BitField(fid=FID.C_RATCHET_FREE, length=LEN.C_RATCHET_FREE,
                     title="C_ratchet_free", name="c_ratchet_free",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.C_RATCHET_FREE) - 1),)),
            BitField(fid=FID.C_MAIN_WHEEL, length=LEN.C_MAIN_WHEEL,
                     title="C_main_wheel", name="c_main_wheel",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.C_MAIN_WHEEL) - 1),)),
        )
    # end class Capabilities
# end class MouseWheelAnalytics


# noinspection DuplicatedCode
class MouseWheelAnalyticsModel(FeatureModel):
    """
    Define ``MouseWheelAnalytics`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_ANALYTICS_MODE = 1
        SET_ANALYTICS_MODE = 2
        GET_ROTATION_DATA = 3
        GET_WHEEL_MODE_DATA = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``MouseWheelAnalytics`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_ANALYTICS_MODE: {
                    "request": GetAnalyticsMode,
                    "response": GetAnalyticsModeResponse
                },
                cls.INDEX.SET_ANALYTICS_MODE: {
                    "request": SetAnalyticsMode,
                    "response": SetAnalyticsModeResponse
                },
                cls.INDEX.GET_ROTATION_DATA: {
                    "request": GetRotationData,
                    "response": GetRotationDataResponse
                },
                cls.INDEX.GET_WHEEL_MODE_DATA: {
                    "request": GetWheelModeData,
                    "response": GetWheelModeDataResponse
                }
            }
        }

        return {
            "feature_base": MouseWheelAnalytics,
            "versions": {
                MouseWheelAnalyticsV0.VERSION: {
                    "main_cls": MouseWheelAnalyticsV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class MouseWheelAnalyticsModel


class MouseWheelAnalyticsFactory(FeatureFactory):
    """
    Get ``MouseWheelAnalytics`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``MouseWheelAnalytics`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``MouseWheelAnalyticsInterface``
        """
        return MouseWheelAnalyticsModel.get_main_cls(version)()
    # end def create
# end class MouseWheelAnalyticsFactory


class MouseWheelAnalyticsInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``MouseWheelAnalytics``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_analytics_mode_cls = None
        self.set_analytics_mode_cls = None
        self.get_rotation_data_cls = None
        self.get_wheel_mode_data_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_analytics_mode_response_cls = None
        self.set_analytics_mode_response_cls = None
        self.get_rotation_data_response_cls = None
        self.get_wheel_mode_data_response_cls = None
    # end def __init__
# end class MouseWheelAnalyticsInterface


class MouseWheelAnalyticsV0(MouseWheelAnalyticsInterface):
    """
    Define ``MouseWheelAnalyticsV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> capabilities, main_count_per_turn, thumbwheel_count_per_turn

    [1] getAnalyticsMode() -> reporting_mode

    [2] setAnalyticsMode(reporting_mode) -> reporting_mode

    [3] getRotationData() -> accPosWheel, accNegWheel, accPosThumbwheel, accNegThumbwheel

    [4] getWheelModeData() -> ratchetToFreeWheelCount, freeWheelToRatchetCount, smartShiftCount
    """
    VERSION = 0

    def __init__(self):
        # See ``MouseWheelAnalytics.__init__``
        super().__init__()
        index = MouseWheelAnalyticsModel.INDEX

        # Requests
        self.get_capabilities_cls = MouseWheelAnalyticsModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_analytics_mode_cls = MouseWheelAnalyticsModel.get_request_cls(
            self.VERSION, index.GET_ANALYTICS_MODE)
        self.set_analytics_mode_cls = MouseWheelAnalyticsModel.get_request_cls(
            self.VERSION, index.SET_ANALYTICS_MODE)
        self.get_rotation_data_cls = MouseWheelAnalyticsModel.get_request_cls(
            self.VERSION, index.GET_ROTATION_DATA)
        self.get_wheel_mode_data_cls = MouseWheelAnalyticsModel.get_request_cls(
            self.VERSION, index.GET_WHEEL_MODE_DATA)

        # Responses
        self.get_capabilities_response_cls = MouseWheelAnalyticsModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_analytics_mode_response_cls = MouseWheelAnalyticsModel.get_response_cls(
            self.VERSION, index.GET_ANALYTICS_MODE)
        self.set_analytics_mode_response_cls = MouseWheelAnalyticsModel.get_response_cls(
            self.VERSION, index.SET_ANALYTICS_MODE)
        self.get_rotation_data_response_cls = MouseWheelAnalyticsModel.get_response_cls(
            self.VERSION, index.GET_ROTATION_DATA)
        self.get_wheel_mode_data_response_cls = MouseWheelAnalyticsModel.get_response_cls(
            self.VERSION, index.GET_WHEEL_MODE_DATA)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``MouseWheelAnalyticsInterface.get_max_function_index``
        return MouseWheelAnalyticsModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class MouseWheelAnalyticsV0


class ShortEmptyPacketDataFormat(MouseWheelAnalytics):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetAnalyticsMode
        - GetCapabilities
        - GetRotationData
        - GetWheelModeData

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        PADDING = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseWheelAnalytics.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat

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


class GetAnalyticsMode(ShortEmptyPacketDataFormat):
    """
    Define ``GetAnalyticsMode`` implementation class
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
                         function_index=GetAnalyticsModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetAnalyticsMode


class SetAnalyticsMode(MouseWheelAnalytics):
    """
    Define ``SetAnalyticsMode`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reporting_Mode                8
    Padding                       16
    ============================  ==========
    """

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        REPORTING_MODE = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
        PADDING = REPORTING_MODE - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        REPORTING_MODE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.REPORTING_MODE, length=LEN.REPORTING_MODE,
                 title="Reporting_mode", name="reporting_mode",
                 checks=(CheckHexList(LEN.REPORTING_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseWheelAnalytics.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, reporting_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param reporting_mode: Reporting_Mode
        :type reporting_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetAnalyticsModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.reporting_mode = HexList(Numeral(reporting_mode, self.LEN.REPORTING_MODE // 8))
    # end def __init__
# end class SetAnalyticsMode


class GetRotationData(ShortEmptyPacketDataFormat):
    """
    Define ``GetRotationData`` implementation class
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
                         function_index=GetRotationDataResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetRotationData


class GetWheelModeData(ShortEmptyPacketDataFormat):
    """
    Define ``GetWheelModeData`` implementation class
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
                         function_index=GetWheelModeDataResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetWheelModeData


class GetCapabilitiesResponse(MouseWheelAnalytics):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Capabilities                  8
    Main_Count_Per_Turn           16
    Thumbwheel_Count_Per_Turn     16
    Padding                       88
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        CAPABILITIES = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
        MAIN_COUNT_PER_TURN = CAPABILITIES - 1
        THUMBWHEEL_COUNT_PER_TURN = MAIN_COUNT_PER_TURN - 1
        PADDING = THUMBWHEEL_COUNT_PER_TURN - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        CAPABILITIES = 0x8
        MAIN_COUNT_PER_TURN = 0x10
        THUMBWHEEL_COUNT_PER_TURN = 0x10
        PADDING = 0x58
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckHexList(LEN.CAPABILITIES // 8), CheckByte(),)),
        BitField(fid=FID.MAIN_COUNT_PER_TURN, length=LEN.MAIN_COUNT_PER_TURN,
                 title="Main_count_per_turn", name="main_count_per_turn",
                 checks=(CheckHexList(LEN.MAIN_COUNT_PER_TURN // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAIN_COUNT_PER_TURN) - 1),)),
        BitField(fid=FID.THUMBWHEEL_COUNT_PER_TURN, length=LEN.THUMBWHEEL_COUNT_PER_TURN,
                 title="Thumbwheel_count_per_turn", name="thumbwheel_count_per_turn",
                 checks=(CheckHexList(LEN.THUMBWHEEL_COUNT_PER_TURN // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.THUMBWHEEL_COUNT_PER_TURN) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseWheelAnalytics.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, c_thumbwheel, c_smartshift, c_ratchet_free, c_main_wheel,
                 main_count_per_turn, thumbwheel_count_per_turn, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param c_thumbwheel: C_Thumbwheel
        :type c_thumbwheel: ``bool | HexList``
        :param c_smartshift: C_Smartshift
        :type c_smartshift: ``bool | HexList``
        :param c_ratchet_free: C_Ratchet_Free
        :type c_ratchet_free: ``bool | HexList``
        :param c_main_wheel: C_Main_Wheel
        :type c_main_wheel: ``bool | HexList``
        :param main_count_per_turn: Main_Count_Per_Turn
        :type main_count_per_turn: ``HexList``
        :param thumbwheel_count_per_turn: Thumbwheel_Count_Per_Turn
        :type thumbwheel_count_per_turn: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.capabilities = MouseWheelAnalytics.Capabilities(c_thumbwheel=c_thumbwheel, c_smartshift=c_smartshift,
                                                             c_ratchet_free=c_ratchet_free, c_main_wheel=c_main_wheel)
        self.main_count_per_turn = HexList(Numeral(main_count_per_turn, self.LEN.MAIN_COUNT_PER_TURN // 8))
        self.thumbwheel_count_per_turn = HexList(Numeral(thumbwheel_count_per_turn,
                                                         self.LEN.THUMBWHEEL_COUNT_PER_TURN // 8))
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
        :rtype: ``GetCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.capabilities = MouseWheelAnalytics.Capabilities.fromHexList(
            inner_field_container_mixin.capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class GetAnalyticsModeResponse(MouseWheelAnalytics):
    """
    Define ``GetAnalyticsModeResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reporting_Mode                8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetAnalyticsMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        REPORTING_MODE = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
        PADDING = REPORTING_MODE - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        REPORTING_MODE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.REPORTING_MODE, length=LEN.REPORTING_MODE,
                 title="Reporting_mode", name="reporting_mode",
                 checks=(CheckHexList(LEN.REPORTING_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseWheelAnalytics.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, reporting_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param reporting_mode: Reporting_Mode
        :type reporting_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.reporting_mode = HexList(Numeral(reporting_mode, self.LEN.REPORTING_MODE // 8))
    # end def __init__
# end class GetAnalyticsModeResponse


class SetAnalyticsModeResponse(MouseWheelAnalytics):
    """
    Define ``SetAnalyticsModeResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reporting_Mode                8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetAnalyticsMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        REPORTING_MODE = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
        PADDING = REPORTING_MODE - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        REPORTING_MODE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.REPORTING_MODE, length=LEN.REPORTING_MODE,
                 title="Reporting_mode", name="reporting_mode",
                 checks=(CheckHexList(LEN.REPORTING_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseWheelAnalytics.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, reporting_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param reporting_mode: Reporting_Mode
        :type reporting_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.reporting_mode = HexList(Numeral(reporting_mode, self.LEN.REPORTING_MODE // 8))
    # end def __init__
# end class SetAnalyticsModeResponse


class GetRotationDataResponse(MouseWheelAnalytics):
    """
    Define ``GetRotationDataResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Acc Pos Wheel                 32
    Acc Neg Wheel                 32
    Acc Pos Thumbwheel            32
    Acc Neg Thumbwheel            32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRotationData,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        ACC_POS_WHEEL = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
        ACC_NEG_WHEEL = ACC_POS_WHEEL - 1
        ACC_POS_THUMBWHEEL = ACC_NEG_WHEEL - 1
        ACC_NEG_THUMBWHEEL = ACC_POS_THUMBWHEEL - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        ACC_POS_WHEEL = 0x20
        ACC_NEG_WHEEL = 0x20
        ACC_POS_THUMBWHEEL = 0x20
        ACC_NEG_THUMBWHEEL = 0x20
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.ACC_POS_WHEEL, length=LEN.ACC_POS_WHEEL,
                 title="AccPosWheel", name="acc_pos_wheel",
                 checks=(CheckHexList(LEN.ACC_POS_WHEEL // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACC_POS_WHEEL) - 1),)),
        BitField(fid=FID.ACC_NEG_WHEEL, length=LEN.ACC_NEG_WHEEL,
                 title="AccNegWheel", name="acc_neg_wheel",
                 checks=(CheckHexList(LEN.ACC_NEG_WHEEL // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACC_NEG_WHEEL) - 1),)),
        BitField(fid=FID.ACC_POS_THUMBWHEEL, length=LEN.ACC_POS_THUMBWHEEL,
                 title="AccPosThumbwheel", name="acc_pos_thumbwheel",
                 checks=(CheckHexList(LEN.ACC_POS_THUMBWHEEL // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACC_POS_THUMBWHEEL) - 1),)),
        BitField(fid=FID.ACC_NEG_THUMBWHEEL, length=LEN.ACC_NEG_THUMBWHEEL,
                 title="AccNegThumbwheel", name="acc_neg_thumbwheel",
                 checks=(CheckHexList(LEN.ACC_NEG_THUMBWHEEL // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ACC_NEG_THUMBWHEEL) - 1),)),
    )

    def __init__(self, device_index, feature_index, acc_pos_wheel, acc_neg_wheel, acc_pos_thumbwheel,
                 acc_neg_thumbwheel, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param acc_pos_wheel: Acc Pos Wheel
        :type acc_pos_wheel: ``HexList``
        :param acc_neg_wheel: Acc Neg Wheel
        :type acc_neg_wheel: ``HexList``
        :param acc_pos_thumbwheel: Acc Pos Thumbwheel
        :type acc_pos_thumbwheel: ``HexList``
        :param acc_neg_thumbwheel: Acc Neg Thumbwheel
        :type acc_neg_thumbwheel: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.acc_pos_wheel = HexList(Numeral(acc_pos_wheel, self.LEN.ACC_POS_WHEEL // 8))
        self.acc_neg_wheel = HexList(Numeral(acc_neg_wheel, self.LEN.ACC_NEG_WHEEL // 8))
        self.acc_pos_thumbwheel = HexList(Numeral(acc_pos_thumbwheel, self.LEN.ACC_POS_THUMBWHEEL // 8))
        self.acc_neg_thumbwheel = HexList(Numeral(acc_neg_thumbwheel, self.LEN.ACC_NEG_THUMBWHEEL // 8))
    # end def __init__
# end class GetRotationDataResponse


class GetWheelModeDataResponse(MouseWheelAnalytics):
    """
    Define ``GetWheelModeDataResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Ratchet To Free Wheel Count   32
    Free Wheel To Ratchet Count   32
    Smart Shift Count             32
    Padding                       32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetWheelModeData,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(MouseWheelAnalytics.FID):
        # See ``MouseWheelAnalytics.FID``
        RATCHET_TO_FREE_WHEEL_COUNT = MouseWheelAnalytics.FID.SOFTWARE_ID - 1
        FREE_WHEEL_TO_RATCHET_COUNT = RATCHET_TO_FREE_WHEEL_COUNT - 1
        SMART_SHIFT_COUNT = FREE_WHEEL_TO_RATCHET_COUNT - 1
        PADDING = SMART_SHIFT_COUNT - 1
    # end class FID

    class LEN(MouseWheelAnalytics.LEN):
        # See ``MouseWheelAnalytics.LEN``
        RATCHET_TO_FREE_WHEEL_COUNT = 0x20
        FREE_WHEEL_TO_RATCHET_COUNT = 0x20
        SMART_SHIFT_COUNT = 0x20
        PADDING = 0x20
    # end class LEN

    FIELDS = MouseWheelAnalytics.FIELDS + (
        BitField(fid=FID.RATCHET_TO_FREE_WHEEL_COUNT, length=LEN.RATCHET_TO_FREE_WHEEL_COUNT,
                 title="RatchetToFreeWheelCount", name="ratchet_to_free_wheel_count",
                 checks=(CheckHexList(LEN.RATCHET_TO_FREE_WHEEL_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RATCHET_TO_FREE_WHEEL_COUNT) - 1),)),
        BitField(fid=FID.FREE_WHEEL_TO_RATCHET_COUNT, length=LEN.FREE_WHEEL_TO_RATCHET_COUNT,
                 title="FreeWheelToRatchetCount", name="free_wheel_to_ratchet_count",
                 checks=(CheckHexList(LEN.FREE_WHEEL_TO_RATCHET_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FREE_WHEEL_TO_RATCHET_COUNT) - 1),)),
        BitField(fid=FID.SMART_SHIFT_COUNT, length=LEN.SMART_SHIFT_COUNT,
                 title="SmartShiftCount", name="smart_shift_count",
                 checks=(CheckHexList(LEN.SMART_SHIFT_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SMART_SHIFT_COUNT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=MouseWheelAnalytics.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ratchet_to_free_wheel_count, free_wheel_to_ratchet_count,
                 smart_shift_count, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param ratchet_to_free_wheel_count: Ratchet To Free Wheel Count
        :type ratchet_to_free_wheel_count: ``HexList``
        :param free_wheel_to_ratchet_count: Free Wheel To Ratchet Count
        :type free_wheel_to_ratchet_count: ``HexList``
        :param smart_shift_count: Smart Shift Count
        :type smart_shift_count: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.ratchet_to_free_wheel_count = HexList(Numeral(ratchet_to_free_wheel_count,
                                                           self.LEN.RATCHET_TO_FREE_WHEEL_COUNT // 8))
        self.free_wheel_to_ratchet_count = HexList(Numeral(free_wheel_to_ratchet_count,
                                                           self.LEN.FREE_WHEEL_TO_RATCHET_COUNT // 8))
        self.smart_shift_count = HexList(Numeral(smart_shift_count, self.LEN.SMART_SHIFT_COUNT // 8))
    # end def __init__
# end class GetWheelModeDataResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
