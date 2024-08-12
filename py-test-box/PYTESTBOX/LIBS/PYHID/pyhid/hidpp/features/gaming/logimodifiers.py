#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.gaming.logimodifiers
:brief: HID++ 2.0 ``LogiModifiers`` command interface definition
:author: Zane Lu <zlu@logitech.com>
:date: 2023/05/18
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
class LogiModifiers(HidppMessage):
    """
    This feature provides the means to get the pressed state as well as forcefully press certain modifier keys.
    """
    FEATURE_ID = 0x8051
    MAX_FUNCTION_INDEX_V0 = 5

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

    class GettableModifiers(BitFieldContainerMixin):
        """
        Define ``GettableModifiers`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        G Shift                       1
        Fn                            1
        Right Gui                     1
        Right Alt                     1
        Right Shift                   1
        Right Ctrl                    1
        Left Gui                      1
        Left Alt                      1
        Left Shift                    1
        Left Ctrl                     1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            G_SHIFT = RESERVED - 1
            FN = G_SHIFT - 1
            RIGHT_GUI = FN - 1
            RIGHT_ALT = RIGHT_GUI - 1
            RIGHT_SHIFT = RIGHT_ALT - 1
            RIGHT_CTRL = RIGHT_SHIFT - 1
            LEFT_GUI = RIGHT_CTRL - 1
            LEFT_ALT = LEFT_GUI - 1
            LEFT_SHIFT = LEFT_ALT - 1
            LEFT_CTRL = LEFT_SHIFT - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            G_SHIFT = 0x1
            FN = 0x1
            RIGHT_GUI = 0x1
            RIGHT_ALT = 0x1
            RIGHT_SHIFT = 0x1
            RIGHT_CTRL = 0x1
            LEFT_GUI = 0x1
            LEFT_ALT = 0x1
            LEFT_SHIFT = 0x1
            LEFT_CTRL = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            GSHIFT = 0x00
            FN = 0x00
            RIGHT_GUI = 0x00
            RIGHT_ALT = 0x00
            RIGHT_SHIFT = 0x00
            RIGHT_CTRL = 0x00
            LEFT_GUI = 0x00
            LEFT_ALT = 0x00
            LEFT_SHIFT = 0x00
            LEFT_CTRL = 0x00
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.G_SHIFT, length=LEN.G_SHIFT,
                     title="GShift", name="g_shift",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.G_SHIFT) - 1),),
                     default_value=DEFAULT.GSHIFT),
            BitField(fid=FID.FN, length=LEN.FN,
                     title="Fn", name="fn",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FN) - 1),),
                     default_value=DEFAULT.FN),
            BitField(fid=FID.RIGHT_GUI, length=LEN.RIGHT_GUI,
                     title="RightGui", name="right_gui",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RIGHT_GUI) - 1),),
                     default_value=DEFAULT.RIGHT_GUI),
            BitField(fid=FID.RIGHT_ALT, length=LEN.RIGHT_ALT,
                     title="RightAlt", name="right_alt",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RIGHT_ALT) - 1),),
                     default_value=DEFAULT.RIGHT_ALT),
            BitField(fid=FID.RIGHT_SHIFT, length=LEN.RIGHT_SHIFT,
                     title="RightShift", name="right_shift",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RIGHT_SHIFT) - 1),),
                     default_value=DEFAULT.RIGHT_SHIFT),
            BitField(fid=FID.RIGHT_CTRL, length=LEN.RIGHT_CTRL,
                     title="RightCtrl", name="right_ctrl",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RIGHT_CTRL) - 1),),
                     default_value=DEFAULT.RIGHT_CTRL),
            BitField(fid=FID.LEFT_GUI, length=LEN.LEFT_GUI,
                     title="LeftGui", name="left_gui",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LEFT_GUI) - 1),),
                     default_value=DEFAULT.LEFT_GUI),
            BitField(fid=FID.LEFT_ALT, length=LEN.LEFT_ALT,
                     title="LeftAlt", name="left_alt",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LEFT_ALT) - 1),),
                     default_value=DEFAULT.LEFT_ALT),
            BitField(fid=FID.LEFT_SHIFT, length=LEN.LEFT_SHIFT,
                     title="LeftShift", name="left_shift",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LEFT_SHIFT) - 1),),
                     default_value=DEFAULT.LEFT_SHIFT),
            BitField(fid=FID.LEFT_CTRL, length=LEN.LEFT_CTRL,
                     title="LeftCtrl", name="left_ctrl",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.LEFT_CTRL) - 1),),
                     default_value=DEFAULT.LEFT_CTRL),
        )
    # end class GettableModifiers

    class ForceableModifiers(BitFieldContainerMixin):
        """
        Define ``ForceableModifiers`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved1                     6
        G Shift                       1
        FFn                           1
        Reserved2                     8
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED1 = 0xFF
            G_SHIFT = RESERVED1 - 1
            FN = G_SHIFT - 1
            RESERVED2 = FN - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED1 = 0x6
            G_SHIFT = 0x1
            FN = 0x1
            RESERVED2 = 0x8
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED1 = 0x0
            GSHIFT = 0x00
            FN = 0x00
            RESERVED2 = 0x00
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED1, length=LEN.RESERVED1,
                     title="Reserved1", name="reserved1",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED1) - 1),),
                     default_value=DEFAULT.RESERVED1),
            BitField(fid=FID.G_SHIFT, length=LEN.G_SHIFT,
                     title="GShift", name="g_shift",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.G_SHIFT) - 1),),
                     default_value=DEFAULT.GSHIFT),
            BitField(fid=FID.FN, length=LEN.FN,
                     title="Fn", name="fn",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.FN) - 1),),
                     default_value=DEFAULT.FN),
            BitField(fid=FID.RESERVED2, length=LEN.RESERVED2,
                     title="Reserved2", name="reserved2",
                     checks=(CheckHexList(LEN.RESERVED2 // 8), CheckByte(),),
                     default_value=DEFAULT.RESERVED2),
        )
    # end class ForceableModifiers

    class LocallyPressedState(GettableModifiers):
        """
        See ``GettableModifiers`` information
        """
        pass
    # end class LocallyPressedState

    class ForcedPressedState(ForceableModifiers):
        """
        See ``ForceableModifiers`` information
        """
        pass
    # end class ForcedPressedState

    class ReportedModifiers(GettableModifiers):
        """
        See ``GettableModifiers`` information
        """
        pass
    # end class ReportedModifiers

# end class LogiModifiers


class LogiModifiersModel(FeatureModel):
    """
    Define ``LogiModifiers`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_LOCALLY_PRESSED_STATE = 1
        SET_FORCED_PRESSED_STATE = 2
        SET_PRESS_EVENTS = 3
        GET_FORCED_PRESSED_STATE = 4
        GET_PRESS_EVENTS = 5

        # Event index
        PRESS = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``LogiModifiers`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_LOCALLY_PRESSED_STATE: {
                    "request": GetLocallyPressedState,
                    "response": GetLocallyPressedStateResponse
                },
                cls.INDEX.SET_FORCED_PRESSED_STATE: {
                    "request": SetForcedPressedState,
                    "response": SetForcedPressedStateResponse
                },
                cls.INDEX.SET_PRESS_EVENTS: {
                    "request": SetPressEvents,
                    "response": SetPressEventsResponse
                },
                cls.INDEX.GET_FORCED_PRESSED_STATE: {
                    "request": GetForcedPressedState,
                    "response": GetForcedPressedStateResponse
                },
                cls.INDEX.GET_PRESS_EVENTS: {
                    "request": GetPressEvents,
                    "response": GetPressEventsResponse
                }
            },
            "events": {
                cls.INDEX.PRESS: {"report": PressEvent}
            }
        }

        return {
            "feature_base": LogiModifiers,
            "versions": {
                LogiModifiersV0.VERSION: {
                    "main_cls": LogiModifiersV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class LogiModifiersModel


class LogiModifiersFactory(FeatureFactory):
    """
    Get ``LogiModifiers`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``LogiModifiers`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``LogiModifiersInterface``
        """
        return LogiModifiersModel.get_main_cls(version)()
    # end def create
# end class LogiModifiersFactory


class LogiModifiersInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``LogiModifiers``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_locally_pressed_state_cls = None
        self.set_forced_pressed_state_cls = None
        self.set_press_events_cls = None
        self.get_forced_pressed_state_cls = None
        self.get_press_events_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_locally_pressed_state_response_cls = None
        self.set_forced_pressed_state_response_cls = None
        self.set_press_events_response_cls = None
        self.get_forced_pressed_state_response_cls = None
        self.get_press_events_response_cls = None

        # Events
        self.press_event_cls = None
    # end def __init__
# end class LogiModifiersInterface


class LogiModifiersV0(LogiModifiersInterface):
    """
    Define ``LogiModifiersV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> gettableModifiers, forceableModifiers

    [1] getLocallyPressedState() -> locallyPressedState

    [2] setForcedPressedState(forcedPressedState) -> None

    [3] setPressEvents(reportedModifiers) -> None

    [4] getForcedPressedState() -> forcedPressedState

    [5] getPressEvents() -> reportedModifiers

    [Event 0] PressEvent -> locallyPressedState
    """
    VERSION = 0

    def __init__(self):
        # See ``LogiModifiers.__init__``
        super().__init__()
        index = LogiModifiersModel.INDEX

        # Requests
        self.get_capabilities_cls = LogiModifiersModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_locally_pressed_state_cls = LogiModifiersModel.get_request_cls(
            self.VERSION, index.GET_LOCALLY_PRESSED_STATE)
        self.set_forced_pressed_state_cls = LogiModifiersModel.get_request_cls(
            self.VERSION, index.SET_FORCED_PRESSED_STATE)
        self.set_press_events_cls = LogiModifiersModel.get_request_cls(
            self.VERSION, index.SET_PRESS_EVENTS)
        self.get_forced_pressed_state_cls = LogiModifiersModel.get_request_cls(
            self.VERSION, index.GET_FORCED_PRESSED_STATE)
        self.get_press_events_cls = LogiModifiersModel.get_request_cls(
            self.VERSION, index.GET_PRESS_EVENTS)

        # Responses
        self.get_capabilities_response_cls = LogiModifiersModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_locally_pressed_state_response_cls = LogiModifiersModel.get_response_cls(
            self.VERSION, index.GET_LOCALLY_PRESSED_STATE)
        self.set_forced_pressed_state_response_cls = LogiModifiersModel.get_response_cls(
            self.VERSION, index.SET_FORCED_PRESSED_STATE)
        self.set_press_events_response_cls = LogiModifiersModel.get_response_cls(
            self.VERSION, index.SET_PRESS_EVENTS)
        self.get_forced_pressed_state_response_cls = LogiModifiersModel.get_response_cls(
            self.VERSION, index.GET_FORCED_PRESSED_STATE)
        self.get_press_events_response_cls = LogiModifiersModel.get_response_cls(
            self.VERSION, index.GET_PRESS_EVENTS)

        # Events
        self.press_event_cls = LogiModifiersModel.get_report_cls(
            self.VERSION, index.PRESS)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``LogiModifiersInterface.get_max_function_index``
        return LogiModifiersModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class LogiModifiersV0


class ShortEmptyPacketDataFormat(LogiModifiers):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities
        - GetLocallyPressedState
        - GetForcedPressedState
        - GetPressEvents

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        PADDING = LogiModifiers.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(LogiModifiers):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetForcedPressedStateResponse
        - SetPressEventsResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        PADDING = LogiModifiers.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class MixedContainer1(LogiModifiers):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetLocallyPressedStateResponse
        - GetPressEventsResponse
        - PressEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Locally Pressed State         16
    Padding                       112
    ============================  ==========
    """

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        LOCALLY_PRESSED_STATE = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = LOCALLY_PRESSED_STATE - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        LOCALLY_PRESSED_STATE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.LOCALLY_PRESSED_STATE, length=LEN.LOCALLY_PRESSED_STATE,
                 title="LocallyPressedState", name="locally_pressed_state",
                 checks=(CheckHexList(LEN.LOCALLY_PRESSED_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LOCALLY_PRESSED_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )
# end class MixedContainer1


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


class GetLocallyPressedState(ShortEmptyPacketDataFormat):
    """
    Define ``GetLocallyPressedState`` implementation class
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
                         function_index=GetLocallyPressedStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetLocallyPressedState


class SetForcedPressedState(LogiModifiers):
    """
    Define ``SetForcedPressedState`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Forced Pressed State          16
    Padding                       8
    ============================  ==========
    """

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        FORCED_PRESSED_STATE = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = FORCED_PRESSED_STATE - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        FORCED_PRESSED_STATE = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.FORCED_PRESSED_STATE, length=LEN.FORCED_PRESSED_STATE,
                 title="ForcedPressedState", name="forced_pressed_state",
                 checks=(CheckHexList(LEN.FORCED_PRESSED_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FORCED_PRESSED_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, g_shift, fn, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param g_shift: G Shift
        :type g_shift: ``int | HexList``
        :param fn: Fn
        :type fn: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetForcedPressedStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.forced_pressed_state = self.ForcedPressedState(reserved1=0,
                                                            g_shift=g_shift,
                                                            fn=fn,
                                                            reserved2=0)
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
        :rtype: ``SetForcedPressedState``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.forced_pressed_state = cls.ForcedPressedState.fromHexList(
            inner_field_container_mixin.forced_pressed_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetForcedPressedState


class SetPressEvents(LogiModifiers):
    """
    Define ``SetPressEvents`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reported Modifiers            16
    Padding                       8
    ============================  ==========
    """

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        REPORTED_MODIFIERS = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = REPORTED_MODIFIERS - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        REPORTED_MODIFIERS = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.REPORTED_MODIFIERS, length=LEN.REPORTED_MODIFIERS,
                 title="ReportedModifiers", name="reported_modifiers",
                 checks=(CheckHexList(LEN.REPORTED_MODIFIERS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REPORTED_MODIFIERS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, g_shift, fn, right_gui, right_alt, right_shift, right_ctrl,
                 left_gui, left_alt, left_shift, left_ctrl, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param g_shift: G Shift
        :type g_shift: ``int | HexList``
        :param fn: Fn
        :type fn: ``int | HexList``
        :param right_gui: Right Gui
        :type right_gui: ``int | HexList``
        :param right_alt: Right Alt
        :type right_alt: ``int | HexList``
        :param right_shift: Right Shift
        :type right_shift: ``int | HexList``
        :param right_ctrl: Right Ctrl
        :type right_ctrl: ``int | HexList``
        :param left_gui: Left Gui
        :type left_gui: ``int | HexList``
        :param left_alt: Left Alt
        :type left_alt: ``int | HexList``
        :param left_shift: Left Shift
        :type left_shift: ``int | HexList``
        :param left_ctrl: Left Ctrl
        :type left_ctrl: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetPressEventsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.reported_modifiers = self.ReportedModifiers(g_shift=g_shift,
                                                         fn=fn,
                                                         right_gui=right_gui,
                                                         right_alt=right_alt,
                                                         right_shift=right_shift,
                                                         right_ctrl=right_ctrl,
                                                         left_gui=left_gui,
                                                         left_alt=left_alt,
                                                         left_shift=left_shift,
                                                         left_ctrl=left_ctrl)
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
        :rtype: ``SetPressEvents``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.reported_modifiers = cls.ReportedModifiers.fromHexList(
            inner_field_container_mixin.reported_modifiers)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetPressEvents


class GetForcedPressedState(ShortEmptyPacketDataFormat):
    """
    Define ``GetForcedPressedState`` implementation class
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
                         function_index=GetForcedPressedStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetForcedPressedState


class GetPressEvents(ShortEmptyPacketDataFormat):
    """
    Define ``GetPressEvents`` implementation class
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
                         function_index=GetPressEventsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetPressEvents


class GetCapabilitiesResponse(LogiModifiers):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Gettable Modifiers            16
    Forceable Modifiers           16
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        GETTABLE_MODIFIERS = LogiModifiers.FID.SOFTWARE_ID - 1
        FORCEABLE_MODIFIERS = GETTABLE_MODIFIERS - 1
        PADDING = FORCEABLE_MODIFIERS - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        GETTABLE_MODIFIERS = 0x10
        FORCEABLE_MODIFIERS = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.GETTABLE_MODIFIERS, length=LEN.GETTABLE_MODIFIERS,
                 title="GettableModifiers", name="gettable_modifiers",
                 checks=(CheckHexList(LEN.GETTABLE_MODIFIERS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.GETTABLE_MODIFIERS) - 1),)),
        BitField(fid=FID.FORCEABLE_MODIFIERS, length=LEN.FORCEABLE_MODIFIERS,
                 title="ForceableModifiers", name="forceable_modifiers",
                 checks=(CheckHexList(LEN.FORCEABLE_MODIFIERS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FORCEABLE_MODIFIERS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, gm_g_shift, gm_fn, gm_right_gui, gm_right_alt, gm_right_shift,
                 gm_right_ctrl, gm_left_gui, gm_left_alt, gm_left_shift, gm_left_ctrl, fm_g_shift, fm_fn, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param gm_g_shift: GM G Shift
        :type gm_g_shift: ``int | HexList``
        :param gm_fn: GM Fn
        :type gm_fn: ``int | HexList``
        :param gm_right_gui: GM Right Gui
        :type gm_right_gui: ``int | HexList``
        :param gm_right_alt: GM Right Alt
        :type gm_right_alt: ``int | HexList``
        :param gm_right_shift: GM Right Shift
        :type gm_right_shift: ``int | HexList``
        :param gm_right_ctrl: GM Right Ctrl
        :type gm_right_ctrl: ``int | HexList``
        :param gm_left_gui: GM Left Gui
        :type gm_left_gui: ``int | HexList``
        :param gm_left_alt: GM Left Alt
        :type gm_left_alt: ``int | HexList``
        :param gm_left_shift: GM Left Shift
        :type gm_left_shift: ``int | HexList``
        :param gm_left_ctrl: GM Left Ctrl
        :type gm_left_ctrl: ``int | HexList``
        :param fm_g_shift: FM G Shift
        :type fm_g_shift: ``int | HexList``
        :param fm_fn: FM Fn
        :type fm_fn: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.gettable_modifiers = self.GettableModifiers(gm_g_shift=gm_g_shift,
                                                         gm_fn=gm_fn,
                                                         gm_right_gui=gm_right_gui,
                                                         gm_right_alt=gm_right_alt,
                                                         gm_right_shift=gm_right_shift,
                                                         gm_right_ctrl=gm_right_ctrl,
                                                         gm_left_gui=gm_left_gui,
                                                         gm_left_alt=gm_left_alt,
                                                         gm_left_shift=gm_left_shift,
                                                         gm_left_ctrl=gm_left_ctrl)
        self.forceable_modifiers = self.ForceableModifiers(fm_g_shift=fm_g_shift,
                                                           fm_fn=fm_fn)
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
        inner_field_container_mixin.gettable_modifiers = cls.GettableModifiers.fromHexList(
            inner_field_container_mixin.gettable_modifiers)
        inner_field_container_mixin.forceable_modifiers = cls.ForceableModifiers.fromHexList(
            inner_field_container_mixin.forceable_modifiers)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class GetLocallyPressedStateResponse(LogiModifiers):
    """
    Define ``GetLocallyPressedStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Locally Pressed State         16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetLocallyPressedState,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        LOCALLY_PRESSED_STATE = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = LOCALLY_PRESSED_STATE - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        LOCALLY_PRESSED_STATE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.LOCALLY_PRESSED_STATE, length=LEN.LOCALLY_PRESSED_STATE,
                 title="LocallyPressedState", name="locally_pressed_state",
                 checks=(CheckHexList(LEN.LOCALLY_PRESSED_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LOCALLY_PRESSED_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, g_shift, fn, right_gui, right_alt, right_shift, right_ctrl,
                 left_gui, left_alt, left_shift, left_ctrl, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param g_shift: G Shift
        :type g_shift: ``int | HexList``
        :param fn: Fn
        :type fn: ``int | HexList``
        :param right_gui: Right Gui
        :type right_gui: ``int | HexList``
        :param right_alt: Right Alt
        :type right_alt: ``int | HexList``
        :param right_shift: Right Shift
        :type right_shift: ``int | HexList``
        :param right_ctrl: Right Ctrl
        :type right_ctrl: ``int | HexList``
        :param left_gui: Left Gui
        :type left_gui: ``int | HexList``
        :param left_alt: Left Alt
        :type left_alt: ``int | HexList``
        :param left_shift: Left Shift
        :type left_shift: ``int | HexList``
        :param left_ctrl: Left Ctrl
        :type left_ctrl: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.locally_pressed_state = self.LocallyPressedState(g_shift=g_shift,
                                                              fn=fn,
                                                              right_gui=right_gui,
                                                              right_alt=right_alt,
                                                              right_shift=right_shift,
                                                              right_ctrl=right_ctrl,
                                                              left_gui=left_gui,
                                                              left_alt=left_alt,
                                                              left_shift=left_shift,
                                                              left_ctrl=left_ctrl)
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
        :rtype: ``GetLocallyPressedStateResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.locally_pressed_state = cls.LocallyPressedState.fromHexList(
            inner_field_container_mixin.locally_pressed_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetLocallyPressedStateResponse


class SetForcedPressedStateResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetForcedPressedStateResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetForcedPressedState,)
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
# end class SetForcedPressedStateResponse


class SetPressEventsResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetPressEventsResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetPressEvents,)
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
# end class SetPressEventsResponse


class GetForcedPressedStateResponse(LogiModifiers):
    """
    Define ``GetForcedPressedStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Forced Pressed State          16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetForcedPressedState,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        FORCED_PRESSED_STATE = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = FORCED_PRESSED_STATE - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        FORCED_PRESSED_STATE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.FORCED_PRESSED_STATE, length=LEN.FORCED_PRESSED_STATE,
                 title="ForcedPressedState", name="forced_pressed_state",
                 checks=(CheckHexList(LEN.FORCED_PRESSED_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FORCED_PRESSED_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, g_shift, fn, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param g_shift: G Shift
        :type g_shift: ``int | HexList``
        :param fn: Fn
        :type fn: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.forced_pressed_state = self.ForcedPressedState(reserved1=0,
                                                            g_shift=g_shift,
                                                            fn=fn,
                                                            reserved2=0)
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
        :rtype: ``GetForcedPressedStateResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.forced_pressed_state = cls.ForcedPressedState.fromHexList(
            inner_field_container_mixin.forced_pressed_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetForcedPressedStateResponse


class GetPressEventsResponse(LogiModifiers):
    """
    Define ``GetPressEventsResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reported Modifiers            16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPressEvents,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        REPORTED_MODIFIERS = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = REPORTED_MODIFIERS - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        REPORTED_MODIFIERS = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.REPORTED_MODIFIERS, length=LEN.REPORTED_MODIFIERS,
                 title="ReportedModifiers", name="reported_modifiers",
                 checks=(CheckHexList(LEN.REPORTED_MODIFIERS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REPORTED_MODIFIERS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, g_shift, fn, right_gui, right_alt, right_shift, right_ctrl,
                 left_gui, left_alt, left_shift, left_ctrl, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param g_shift: G Shift
        :type g_shift: ``int | HexList``
        :param fn: Fn
        :type fn: ``int | HexList``
        :param right_gui: Right Gui
        :type right_gui: ``int | HexList``
        :param right_alt: Right Alt
        :type right_alt: ``int | HexList``
        :param right_shift: Right Shift
        :type right_shift: ``int | HexList``
        :param right_ctrl: Right Ctrl
        :type right_ctrl: ``int | HexList``
        :param left_gui: Left Gui
        :type left_gui: ``int | HexList``
        :param left_alt: Left Alt
        :type left_alt: ``int | HexList``
        :param left_shift: Left Shift
        :type left_shift: ``int | HexList``
        :param left_ctrl: Left Ctrl
        :type left_ctrl: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.reported_modifiers = self.ReportedModifiers(g_shift=g_shift,
                                                         fn=fn,
                                                         right_gui=right_gui,
                                                         right_alt=right_alt,
                                                         right_shift=right_shift,
                                                         right_ctrl=right_ctrl,
                                                         left_gui=left_gui,
                                                         left_alt=left_alt,
                                                         left_shift=left_shift,
                                                         left_ctrl=left_ctrl)
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
        :rtype: ``GetPressEventsResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.reported_modifiers = cls.ReportedModifiers.fromHexList(
            inner_field_container_mixin.reported_modifiers)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetPressEventsResponse


class PressEvent(LogiModifiers):
    """
    Define ``PressEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Locally Pressed State         16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(LogiModifiers.FID):
        # See ``LogiModifiers.FID``
        LOCALLY_PRESSED_STATE = LogiModifiers.FID.SOFTWARE_ID - 1
        PADDING = LOCALLY_PRESSED_STATE - 1
    # end class FID

    class LEN(LogiModifiers.LEN):
        # See ``LogiModifiers.LEN``
        LOCALLY_PRESSED_STATE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = LogiModifiers.FIELDS + (
        BitField(fid=FID.LOCALLY_PRESSED_STATE, length=LEN.LOCALLY_PRESSED_STATE,
                 title="LocallyPressedState", name="locally_pressed_state",
                 checks=(CheckHexList(LEN.LOCALLY_PRESSED_STATE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LOCALLY_PRESSED_STATE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LogiModifiers.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, g_shift, fn, right_gui, right_alt, right_shift, right_ctrl,
                 left_gui, left_alt, left_shift, left_ctrl, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param g_shift: G Shift
        :type g_shift: ``int | HexList``
        :param fn: Fn
        :type fn: ``int | HexList``
        :param right_gui: Right Gui
        :type right_gui: ``int | HexList``
        :param right_alt: Right Alt
        :type right_alt: ``int | HexList``
        :param right_shift: Right Shift
        :type right_shift: ``int | HexList``
        :param right_ctrl: Right Ctrl
        :type right_ctrl: ``int | HexList``
        :param left_gui: Left Gui
        :type left_gui: ``int | HexList``
        :param left_alt: Left Alt
        :type left_alt: ``int | HexList``
        :param left_shift: Left Shift
        :type left_shift: ``int | HexList``
        :param left_ctrl: Left Ctrl
        :type left_ctrl: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.locally_pressed_state = self.LocallyPressedState(g_shift=g_shift,
                                                              fn=fn,
                                                              right_gui=right_gui,
                                                              right_alt=right_alt,
                                                              right_shift=right_shift,
                                                              right_ctrl=right_ctrl,
                                                              left_gui=left_gui,
                                                              left_alt=left_alt,
                                                              left_shift=left_shift,
                                                              left_ctrl=left_ctrl)
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
        :rtype: ``PressEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.locally_pressed_state = cls.LocallyPressedState.fromHexList(
            inner_field_container_mixin.locally_pressed_state)
        return inner_field_container_mixin
    # end def fromHexList
# end class PressEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
