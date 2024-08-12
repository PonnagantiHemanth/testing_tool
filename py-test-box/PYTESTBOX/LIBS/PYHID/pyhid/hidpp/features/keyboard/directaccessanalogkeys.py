#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.keyboard.directaccessanalogkeys
:brief: HID++ 2.0 ``DirectAccessAnalogKeys`` command interface definition
:author: YY Liu <yliu5@logitech.com>
:date: 2024/03/27
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
class DirectAccessAnalogKeys(HidppMessage):
    """
    Engineering command to have the capability to access directly the low level analog parameters instead of using the
    0x8101 HID++ command.
    """
    FEATURE_ID = 0x3617
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

    class AnalogMode(BitFieldContainerMixin):
        """
        Define ``AnalogMode`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      5
        Multi Action                  1
        Rapid Trigger                 1
        Normal Trigger                1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            MULTI_ACTION = RESERVED - 1
            RAPID_TRIGGER = MULTI_ACTION - 1
            NORMAL_TRIGGER = RAPID_TRIGGER - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x5
            MULTI_ACTION = 0x1
            RAPID_TRIGGER = 0x1
            NORMAL_TRIGGER = 0x1
        # end class LEN

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.MULTI_ACTION, length=LEN.MULTI_ACTION,
                     title="MultiAction", name="multi_action",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.MULTI_ACTION) - 1),)),
            BitField(fid=FID.RAPID_TRIGGER, length=LEN.RAPID_TRIGGER,
                     title="RapidTrigger", name="rapid_trigger",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RAPID_TRIGGER) - 1),)),
            BitField(fid=FID.NORMAL_TRIGGER, length=LEN.NORMAL_TRIGGER,
                     title="NormalTrigger", name="normal_trigger",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.NORMAL_TRIGGER) - 1),)),
        )
    # end class AnalogMode

    class AssignmentEvent(BitFieldContainerMixin):
        """
        Define ``AssignmentEvent`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Assignment Event 1          4
        Assignment Event 0          4
        Assignment Event 3          4
        Assignment Event 2          4
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            ASSIGNMENT_EVENT_1 = 0xFF
            ASSIGNMENT_EVENT_0 = ASSIGNMENT_EVENT_1 - 1
            ASSIGNMENT_EVENT_3 = ASSIGNMENT_EVENT_0 - 1
            ASSIGNMENT_EVENT_2 = ASSIGNMENT_EVENT_3 - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            ASSIGNMENT_EVENT_1 = 0x4
            ASSIGNMENT_EVENT_0 = 0x4
            ASSIGNMENT_EVENT_3 = 0x4
            ASSIGNMENT_EVENT_2 = 0x4
        # end class LEN

        FIELDS = (
            BitField(fid=FID.ASSIGNMENT_EVENT_1, length=LEN.ASSIGNMENT_EVENT_1,
                     title="AssignmentEvent1", name="assignment_event_1",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_EVENT_1) - 1),)),
            BitField(fid=FID.ASSIGNMENT_EVENT_0, length=LEN.ASSIGNMENT_EVENT_0,
                     title="AssignmentEvent0", name="assignment_event_0",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_EVENT_0) - 1),)),
            BitField(fid=FID.ASSIGNMENT_EVENT_3, length=LEN.ASSIGNMENT_EVENT_3,
                     title="AssignmentEvent3", name="assignment_event_3",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_EVENT_3) - 1),)),
            BitField(fid=FID.ASSIGNMENT_EVENT_2, length=LEN.ASSIGNMENT_EVENT_2,
                     title="AssignmentEvent2", name="assignment_event_2",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_EVENT_2) - 1),)),
        )
    # end class AssignmentEvent
# end class DirectAccessAnalogKeys


# noinspection DuplicatedCode
class DirectAccessAnalogKeysModel(FeatureModel):
    """
    Define ``DirectAccessAnalogKeys`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        SET_ANALOG_KEY_MODE = 1
        SET_NORMAL_TRIGGER = 2
        SET_RAPID_TRIGGER = 3
        SET_MULTI_ACTION = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``DirectAccessAnalogKeys`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.SET_ANALOG_KEY_MODE: {
                    "request": SetAnalogKeyMode,
                    "response": SetAnalogKeyModeResponse
                },
                cls.INDEX.SET_NORMAL_TRIGGER: {
                    "request": SetNormalTrigger,
                    "response": SetNormalTriggerResponse
                },
                cls.INDEX.SET_RAPID_TRIGGER: {
                    "request": SetRapidTrigger,
                    "response": SetRapidTriggerResponse
                },
                cls.INDEX.SET_MULTI_ACTION: {
                    "request": SetMultiAction,
                    "response": SetMultiActionResponse
                }
            }
        }

        return {
            "feature_base": DirectAccessAnalogKeys,
            "versions": {
                DirectAccessAnalogKeysV0.VERSION: {
                    "main_cls": DirectAccessAnalogKeysV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class DirectAccessAnalogKeysModel


class DirectAccessAnalogKeysFactory(FeatureFactory):
    """
    Get ``DirectAccessAnalogKeys`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``DirectAccessAnalogKeys`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``DirectAccessAnalogKeysInterface``
        """
        return DirectAccessAnalogKeysModel.get_main_cls(version)()
    # end def create
# end class DirectAccessAnalogKeysFactory


class DirectAccessAnalogKeysInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``DirectAccessAnalogKeys``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.set_analog_key_mode_cls = None
        self.set_normal_trigger_cls = None
        self.set_rapid_trigger_cls = None
        self.set_multi_action_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.set_analog_key_mode_response_cls = None
        self.set_normal_trigger_response_cls = None
        self.set_rapid_trigger_response_cls = None
        self.set_multi_action_response_cls = None
    # end def __init__
# end class DirectAccessAnalogKeysInterface


class DirectAccessAnalogKeysV0(DirectAccessAnalogKeysInterface):
    """
    Define ``DirectAccessAnalogKeysV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> analogMode, analogKeyNumber, analogResolution

    [1] setAnalogKeyMode(triggerCidx, analogMode) -> None

    [2] setNormalTrigger(triggerCidx, actuationPoint, hysteresis) -> None

    [3] setRapidTrigger(triggerCidx, actuationPoint, sensitivity) -> None

    [4] setMultiAction(triggerCidx, actuationPointMsb, actuationPointLsb, assignment0, assignment1, assignment2,
    assignment3, assignment0Events, assignment1Events, assignment2Events, assignment3Events, mode, hysteresis) -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``DirectAccessAnalogKeys.__init__``
        super().__init__()
        index = DirectAccessAnalogKeysModel.INDEX

        # Requests
        self.get_capabilities_cls = DirectAccessAnalogKeysModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.set_analog_key_mode_cls = DirectAccessAnalogKeysModel.get_request_cls(
            self.VERSION, index.SET_ANALOG_KEY_MODE)
        self.set_normal_trigger_cls = DirectAccessAnalogKeysModel.get_request_cls(
            self.VERSION, index.SET_NORMAL_TRIGGER)
        self.set_rapid_trigger_cls = DirectAccessAnalogKeysModel.get_request_cls(
            self.VERSION, index.SET_RAPID_TRIGGER)
        self.set_multi_action_cls = DirectAccessAnalogKeysModel.get_request_cls(
            self.VERSION, index.SET_MULTI_ACTION)

        # Responses
        self.get_capabilities_response_cls = DirectAccessAnalogKeysModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.set_analog_key_mode_response_cls = DirectAccessAnalogKeysModel.get_response_cls(
            self.VERSION, index.SET_ANALOG_KEY_MODE)
        self.set_normal_trigger_response_cls = DirectAccessAnalogKeysModel.get_response_cls(
            self.VERSION, index.SET_NORMAL_TRIGGER)
        self.set_rapid_trigger_response_cls = DirectAccessAnalogKeysModel.get_response_cls(
            self.VERSION, index.SET_RAPID_TRIGGER)
        self.set_multi_action_response_cls = DirectAccessAnalogKeysModel.get_response_cls(
            self.VERSION, index.SET_MULTI_ACTION)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``DirectAccessAnalogKeysInterface.get_max_function_index``
        return DirectAccessAnalogKeysModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class DirectAccessAnalogKeysV0


class ShortEmptyPacketDataFormat(DirectAccessAnalogKeys):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        PADDING = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DirectAccessAnalogKeys.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(DirectAccessAnalogKeys):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetAnalogKeyModeResponse
        - SetMultiActionResponse
        - SetNormalTriggerResponse
        - SetRapidTriggerResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        PADDING = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DirectAccessAnalogKeys.DEFAULT.PADDING),)
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


class SetAnalogKeyMode(DirectAccessAnalogKeys):
    """
    Define ``SetAnalogKeyMode`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Trigger Cidx                  8
    Analog Mode                   8
    Padding                       8
    ============================  ==========
    """

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        TRIGGER_CIDX = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
        ANALOG_MODE = TRIGGER_CIDX - 1
        PADDING = ANALOG_MODE - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        TRIGGER_CIDX = 0x8
        ANALOG_MODE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.TRIGGER_CIDX, length=LEN.TRIGGER_CIDX,
                 title="TriggerCidx", name="trigger_cidx",
                 checks=(CheckHexList(LEN.TRIGGER_CIDX // 8), CheckByte(),)),
        BitField(fid=FID.ANALOG_MODE, length=LEN.ANALOG_MODE,
                 title="AnalogMode", name="analog_mode",
                 checks=(CheckHexList(LEN.ANALOG_MODE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DirectAccessAnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, trigger_cidx, analog_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param trigger_cidx: Trigger Cidx
        :type trigger_cidx: ``int | HexList``
        :param analog_mode: Analog Mode
        :type analog_mode: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetAnalogKeyModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.trigger_cidx = trigger_cidx
        self.analog_mode = analog_mode
    # end def __init__
# end class SetAnalogKeyMode


class SetNormalTrigger(DirectAccessAnalogKeys):
    """
    Define ``SetNormalTrigger`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Trigger Cidx                  8
    Actuation Point               8
    Hysteresis                    8
    ============================  ==========
    """

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        TRIGGER_CIDX = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
        ACTUATION_POINT = TRIGGER_CIDX - 1
        HYSTERESIS = ACTUATION_POINT - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        TRIGGER_CIDX = 0x8
        ACTUATION_POINT = 0x8
        HYSTERESIS = 0x8
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.TRIGGER_CIDX, length=LEN.TRIGGER_CIDX,
                 title="TriggerCidx", name="trigger_cidx",
                 checks=(CheckHexList(LEN.TRIGGER_CIDX // 8), CheckByte(),)),
        BitField(fid=FID.ACTUATION_POINT, length=LEN.ACTUATION_POINT,
                 title="ActuationPoint", name="actuation_point",
                 checks=(CheckHexList(LEN.ACTUATION_POINT // 8), CheckByte(),)),
        BitField(fid=FID.HYSTERESIS, length=LEN.HYSTERESIS,
                 title="Hysteresis", name="hysteresis",
                 checks=(CheckHexList(LEN.HYSTERESIS // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, trigger_cidx, actuation_point, hysteresis, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param trigger_cidx: Trigger Cidx
        :type trigger_cidx: ``int | HexList``
        :param actuation_point: Actuation Point
        :type actuation_point: ``int | HexList``
        :param hysteresis: Hysteresis
        :type hysteresis: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetNormalTriggerResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.trigger_cidx = trigger_cidx
        self.actuation_point = actuation_point
        self.hysteresis = hysteresis
    # end def __init__
# end class SetNormalTrigger


class SetRapidTrigger(DirectAccessAnalogKeys):
    """
    Define ``SetRapidTrigger`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Trigger Cidx                  8
    Actuation Point               8
    Sensitivity                   8
    ============================  ==========
    """

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        TRIGGER_CIDX = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
        ACTUATION_POINT = TRIGGER_CIDX - 1
        SENSITIVITY = ACTUATION_POINT - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        TRIGGER_CIDX = 0x8
        ACTUATION_POINT = 0x8
        SENSITIVITY = 0x8
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.TRIGGER_CIDX, length=LEN.TRIGGER_CIDX,
                 title="TriggerCidx", name="trigger_cidx",
                 checks=(CheckHexList(LEN.TRIGGER_CIDX // 8), CheckByte(),)),
        BitField(fid=FID.ACTUATION_POINT, length=LEN.ACTUATION_POINT,
                 title="ActuationPoint", name="actuation_point",
                 checks=(CheckHexList(LEN.ACTUATION_POINT // 8), CheckByte(),)),
        BitField(fid=FID.SENSITIVITY, length=LEN.SENSITIVITY,
                 title="Sensitivity", name="sensitivity",
                 checks=(CheckHexList(LEN.SENSITIVITY // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, trigger_cidx, actuation_point, sensitivity, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param trigger_cidx: Trigger Cidx
        :type trigger_cidx: ``int | HexList``
        :param actuation_point: Actuation Point
        :type actuation_point: ``int | HexList``
        :param sensitivity: Sensitivity
        :type sensitivity: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRapidTriggerResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.trigger_cidx = trigger_cidx
        self.actuation_point = actuation_point
        self.sensitivity = sensitivity
    # end def __init__
# end class SetRapidTrigger


class SetMultiAction(DirectAccessAnalogKeys):
    """
    Define ``SetMultiAction`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Trigger Cidx                  8
    Actuation Point MSB           8
    Actuation Point LSB           8
    Assignment 0                  8
    Assignment 1                  8
    Assignment 2                  8
    Assignment 3                  8
    Assignment 0 Events           16
    Assignment 1 Events           16
    Assignment 2 Events           16
    Assignment 3 Events           16
    Mode                          4
    Hysteresis                    4
    ============================  ==========
    """

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        TRIGGER_CIDX = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
        ACTUATION_POINT_MSB = TRIGGER_CIDX - 1
        ACTUATION_POINT_LSB = ACTUATION_POINT_MSB - 1
        ASSIGNMENT_0 = ACTUATION_POINT_LSB - 1
        ASSIGNMENT_1 = ASSIGNMENT_0 - 1
        ASSIGNMENT_2 = ASSIGNMENT_1 - 1
        ASSIGNMENT_3 = ASSIGNMENT_2 - 1
        ASSIGNMENT_0_EVENTS = ASSIGNMENT_3 - 1
        ASSIGNMENT_1_EVENTS = ASSIGNMENT_0_EVENTS - 1
        ASSIGNMENT_2_EVENTS = ASSIGNMENT_1_EVENTS - 1
        ASSIGNMENT_3_EVENTS = ASSIGNMENT_2_EVENTS - 1
        MODE = ASSIGNMENT_3_EVENTS - 1
        HYSTERESIS = MODE - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        TRIGGER_CIDX = 0x8
        ACTUATION_POINT_MSB = 0x8
        ACTUATION_POINT_LSB = 0x8
        ASSIGNMENT_0 = 0x8
        ASSIGNMENT_1 = 0x8
        ASSIGNMENT_2 = 0x8
        ASSIGNMENT_3 = 0x8
        ASSIGNMENT_0_EVENTS = 0x10
        ASSIGNMENT_1_EVENTS = 0x10
        ASSIGNMENT_2_EVENTS = 0x10
        ASSIGNMENT_3_EVENTS = 0x10
        MODE = 0x4
        HYSTERESIS = 0x4
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.TRIGGER_CIDX, length=LEN.TRIGGER_CIDX,
                 title="TriggerCidx", name="trigger_cidx",
                 checks=(CheckHexList(LEN.TRIGGER_CIDX // 8), CheckByte(),)),
        BitField(fid=FID.ACTUATION_POINT_MSB, length=LEN.ACTUATION_POINT_MSB,
                 title="ActuationPointMsb", name="actuation_point_msb",
                 checks=(CheckHexList(LEN.ACTUATION_POINT_MSB // 8), CheckByte(),)),
        BitField(fid=FID.ACTUATION_POINT_LSB, length=LEN.ACTUATION_POINT_LSB,
                 title="ActuationPointLsb", name="actuation_point_lsb",
                 checks=(CheckHexList(LEN.ACTUATION_POINT_LSB // 8), CheckByte(),)),
        BitField(fid=FID.ASSIGNMENT_0, length=LEN.ASSIGNMENT_0,
                 title="Assignment0", name="assignment_0",
                 checks=(CheckHexList(LEN.ASSIGNMENT_0 // 8), CheckByte(),)),
        BitField(fid=FID.ASSIGNMENT_1, length=LEN.ASSIGNMENT_1,
                 title="Assignment1", name="assignment_1",
                 checks=(CheckHexList(LEN.ASSIGNMENT_1 // 8), CheckByte(),)),
        BitField(fid=FID.ASSIGNMENT_2, length=LEN.ASSIGNMENT_2,
                 title="Assignment2", name="assignment_2",
                 checks=(CheckHexList(LEN.ASSIGNMENT_2 // 8), CheckByte(),)),
        BitField(fid=FID.ASSIGNMENT_3, length=LEN.ASSIGNMENT_3,
                 title="Assignment3", name="assignment_3",
                 checks=(CheckHexList(LEN.ASSIGNMENT_3 // 8), CheckByte(),)),
        BitField(fid=FID.ASSIGNMENT_0_EVENTS, length=LEN.ASSIGNMENT_0_EVENTS,
                 title="Assignment0Events", name="assignment_0_events",
                 checks=(CheckHexList(LEN.ASSIGNMENT_0_EVENTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_0_EVENTS) - 1),)),
        BitField(fid=FID.ASSIGNMENT_1_EVENTS, length=LEN.ASSIGNMENT_1_EVENTS,
                 title="Assignment1Events", name="assignment_1_events",
                 checks=(CheckHexList(LEN.ASSIGNMENT_1_EVENTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_1_EVENTS) - 1),)),
        BitField(fid=FID.ASSIGNMENT_2_EVENTS, length=LEN.ASSIGNMENT_2_EVENTS,
                 title="Assignment2Events", name="assignment_2_events",
                 checks=(CheckHexList(LEN.ASSIGNMENT_2_EVENTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_2_EVENTS) - 1),)),
        BitField(fid=FID.ASSIGNMENT_3_EVENTS, length=LEN.ASSIGNMENT_3_EVENTS,
                 title="Assignment3Events", name="assignment_3_events",
                 checks=(CheckHexList(LEN.ASSIGNMENT_3_EVENTS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ASSIGNMENT_3_EVENTS) - 1),)),
        BitField(fid=FID.MODE, length=LEN.MODE,
                 title="Mode", name="mode",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.MODE) - 1),)),
        BitField(fid=FID.HYSTERESIS, length=LEN.HYSTERESIS,
                 title="Hysteresis", name="hysteresis",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.HYSTERESIS) - 1),)),
    )

    def __init__(self, device_index, feature_index, trigger_cidx, actuation_point_msb, actuation_point_lsb,
                 assignment_0, assignment_1, assignment_2, assignment_3, assignment_0_event_1, assignment_0_event_0,
                 assignment_0_event_3, assignment_0_event_2, assignment_1_event_1, assignment_1_event_0,
                 assignment_1_event_3, assignment_1_event_2, assignment_2_event_1, assignment_2_event_0,
                 assignment_2_event_3, assignment_2_event_2, assignment_3_event_1, assignment_3_event_0,
                 assignment_3_event_3, assignment_3_event_2, mode, hysteresis, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param trigger_cidx: Trigger Cidx
        :type trigger_cidx: ``int | HexList``
        :param actuation_point_msb: Actuation Point MSB
        :type actuation_point_msb: ``int | HexList``
        :param actuation_point_lsb: Actuation Point LSB
        :type actuation_point_lsb: ``int | HexList``
        :param assignment_0: Assignment 0
        :type assignment_0: ``int | HexList``
        :param assignment_1: Assignment 1
        :type assignment_1: ``int | HexList``
        :param assignment_2: Assignment 2
        :type assignment_2: ``int | HexList``
        :param assignment_3: Assignment 3
        :type assignment_3: ``int | HexList``
        :param assignment_0_event_1: Assignment 0 Event 1
        :type assignment_0_event_1: ``int | HexList``
        :param assignment_0_event_0: Assignment 0 Event 0
        :type assignment_0_event_0: ``int | HexList``
        :param assignment_0_event_3: Assignment 0 Event 3
        :type assignment_0_event_3: ``int | HexList``
        :param assignment_0_event_2: Assignment 0 Event 2
        :type assignment_0_event_2: ``int | HexList``
        :param assignment_1_event_1: Assignment 1 Event 1
        :type assignment_1_event_1: ``int | HexList``
        :param assignment_1_event_0: Assignment 1 Event 0
        :type assignment_1_event_0: ``int | HexList``
        :param assignment_1_event_3: Assignment 1 Event 3
        :type assignment_1_event_3: ``int | HexList``
        :param assignment_1_event_2: Assignment 1 Event 2
        :type assignment_1_event_2: ``int | HexList``
        :param assignment_2_event_1: Assignment 2 Event 1
        :type assignment_2_event_1: ``int | HexList``
        :param assignment_2_event_0: Assignment 2 Event 0
        :type assignment_2_event_0: ``int | HexList``
        :param assignment_2_event_3: Assignment 2 Event 3
        :type assignment_2_event_3: ``int | HexList``
        :param assignment_2_event_2: Assignment 2 Event 2
        :type assignment_2_event_2: ``int | HexList``
        :param assignment_3_event_1: Assignment 3 Event 1
        :type assignment_3_event_1: ``int | HexList``
        :param assignment_3_event_0: Assignment 3 Event 0
        :type assignment_3_event_0: ``int | HexList``
        :param assignment_3_event_3: Assignment 3 Event 3
        :type assignment_3_event_3: ``int | HexList``
        :param assignment_3_event_2: Assignment 3 Event 2
        :type assignment_3_event_2: ``int | HexList``
        :param mode: Mode
        :type mode: ``int``
        :param hysteresis: Hysteresis
        :type hysteresis: ``int``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetMultiActionResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.trigger_cidx = trigger_cidx
        self.actuation_point_msb = actuation_point_msb
        self.actuation_point_lsb = actuation_point_lsb
        self.assignment_0 = assignment_0
        self.assignment_1 = assignment_1
        self.assignment_2 = assignment_2
        self.assignment_3 = assignment_3
        self.assignment_0_events = self.AssignmentEvent(assignment_event_1=assignment_0_event_1,
                                                        assignment_event_0=assignment_0_event_0,
                                                        assignment_event_3=assignment_0_event_3,
                                                        assignment_event_2=assignment_0_event_2)
        self.assignment_1_events = self.AssignmentEvent(assignment_event_1=assignment_1_event_1,
                                                        assignment_event_0=assignment_1_event_0,
                                                        assignment_event_3=assignment_1_event_3,
                                                        assignment_event_2=assignment_1_event_2)
        self.assignment_2_events = self.AssignmentEvent(assignment_event_1=assignment_2_event_1,
                                                        assignment_event_0=assignment_2_event_0,
                                                        assignment_event_3=assignment_2_event_3,
                                                        assignment_event_2=assignment_2_event_2)
        self.assignment_3_events = self.AssignmentEvent(assignment_event_1=assignment_3_event_1,
                                                        assignment_event_0=assignment_3_event_0,
                                                        assignment_event_3=assignment_3_event_3,
                                                        assignment_event_2=assignment_3_event_2)
        self.mode = mode
        self.hysteresis = hysteresis
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
        :rtype: ``SetMultiAction``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.assignment_0_events = cls.AssignmentEvent.fromHexList(
            inner_field_container_mixin.assignment_0_events)
        inner_field_container_mixin.assignment_1_events = cls.AssignmentEvent.fromHexList(
            inner_field_container_mixin.assignment_1_events)
        inner_field_container_mixin.assignment_2_events = cls.AssignmentEvent.fromHexList(
            inner_field_container_mixin.assignment_2_events)
        inner_field_container_mixin.assignment_3_events = cls.AssignmentEvent.fromHexList(
            inner_field_container_mixin.assignment_3_events)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetMultiAction


class GetCapabilitiesResponse(DirectAccessAnalogKeys):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Analog Mode                   8
    Analog Key Number             8
    Analog Resolution             8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(DirectAccessAnalogKeys.FID):
        # See ``DirectAccessAnalogKeys.FID``
        ANALOG_MODE = DirectAccessAnalogKeys.FID.SOFTWARE_ID - 1
        ANALOG_KEY_NUMBER = ANALOG_MODE - 1
        ANALOG_RESOLUTION = ANALOG_KEY_NUMBER - 1
        PADDING = ANALOG_RESOLUTION - 1
    # end class FID

    class LEN(DirectAccessAnalogKeys.LEN):
        # See ``DirectAccessAnalogKeys.LEN``
        ANALOG_MODE = 0x8
        ANALOG_KEY_NUMBER = 0x8
        ANALOG_RESOLUTION = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = DirectAccessAnalogKeys.FIELDS + (
        BitField(fid=FID.ANALOG_MODE, length=LEN.ANALOG_MODE,
                 title="AnalogMode", name="analog_mode",
                 checks=(CheckHexList(LEN.ANALOG_MODE // 8), CheckByte(),)),
        BitField(fid=FID.ANALOG_KEY_NUMBER, length=LEN.ANALOG_KEY_NUMBER,
                 title="AnalogKeyNumber", name="analog_key_number",
                 checks=(CheckHexList(LEN.ANALOG_KEY_NUMBER // 8), CheckByte(),)),
        BitField(fid=FID.ANALOG_RESOLUTION, length=LEN.ANALOG_RESOLUTION,
                 title="AnalogResolution", name="analog_resolution",
                 checks=(CheckHexList(LEN.ANALOG_RESOLUTION // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DirectAccessAnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, multi_action, rapid_trigger, normal_trigger, analog_key_number,
                 analog_resolution, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param multi_action: Multi Action
        :type multi_action: ``int``
        :param rapid_trigger: Rapid Trigger
        :type rapid_trigger: ``int``
        :param normal_trigger: Normal Trigger
        :type normal_trigger: ``int``
        :param analog_key_number: Analog Key Number
        :type analog_key_number: ``int | HexList``
        :param analog_resolution: Analog Resolution
        :type analog_resolution: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.analog_mode = self.AnalogMode(multi_action=multi_action,
                                           rapid_trigger=rapid_trigger,
                                           normal_trigger=normal_trigger)
        self.analog_key_number = analog_key_number
        self.analog_resolution = analog_resolution
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
        inner_field_container_mixin.analog_mode = cls.AnalogMode.fromHexList(
            inner_field_container_mixin.analog_mode)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class SetAnalogKeyModeResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetAnalogKeyModeResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetAnalogKeyMode,)
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
# end class SetAnalogKeyModeResponse


class SetNormalTriggerResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetNormalTriggerResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetNormalTrigger,)
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
# end class SetNormalTriggerResponse


class SetRapidTriggerResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetRapidTriggerResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRapidTrigger,)
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
# end class SetRapidTriggerResponse


class SetMultiActionResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetMultiActionResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetMultiAction,)
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
# end class SetMultiActionResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
