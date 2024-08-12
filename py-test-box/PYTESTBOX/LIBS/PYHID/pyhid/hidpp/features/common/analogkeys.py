#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.analogkeys
:brief: HID++ 2.0 ``AnalogKeys`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2024/03/13
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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class AnalogKeys(HidppMessage):
    """
    This feature allows the host software to control & monitor Analog Keys.
    """
    FEATURE_ID = 0x1B08
    MAX_FUNCTION_INDEX_V0 = 3

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

    class RapidTriggerSettings(BitFieldContainerMixin):
        """
        Define ``RapidTriggerSettings`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Rapid Trigger State           1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            RAPID_TRIGGER_STATE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            RAPID_TRIGGER_STATE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            RAPID_TRIGGER_STATE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.RAPID_TRIGGER_STATE, length=LEN.RAPID_TRIGGER_STATE,
                     title="RapidTriggerState", name="rapid_trigger_state",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RAPID_TRIGGER_STATE) - 1),),
                     default_value=DEFAULT.RAPID_TRIGGER_STATE),
        )
    # end class RapidTriggerTSettings

    class KeyTravelSettings(BitFieldContainerMixin):
        """
        Define ``KeyTravelSettings`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Key Travel Event State        1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            KEY_TRAVEL_EVENT_STATE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            KEY_TRAVEL_EVENT_STATE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            KEY_TRAVEL_EVENT_STATE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.KEY_TRAVEL_EVENT_STATE, length=LEN.KEY_TRAVEL_EVENT_STATE,
                     title="KeyTravelEventState", name="key_travel_event_state",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.KEY_TRAVEL_EVENT_STATE) - 1),),
                     default_value=DEFAULT.KEY_TRAVEL_EVENT_STATE),
        )
    # end class KeyTravelSettings
# end class AnalogKeys


class AnalogKeysModel(FeatureModel):
    """
    Define ``AnalogKeys`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_RAPID_TRIGGER_STATE = 1
        SET_RAPID_TRIGGER_STATE = 2
        SET_KEY_TRAVEL_EVENT_STATE = 3

        # Event index
        KEY_TRAVEL_CHANGE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``AnalogKeys`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_RAPID_TRIGGER_STATE: {
                    "request": GetRapidTriggerState,
                    "response": GetRapidTriggerStateResponse
                },
                cls.INDEX.SET_RAPID_TRIGGER_STATE: {
                    "request": SetRapidTriggerState,
                    "response": SetRapidTriggerStateResponse
                },
                cls.INDEX.SET_KEY_TRAVEL_EVENT_STATE: {
                    "request": SetKeyTravelEventState,
                    "response": SetKeyTravelEventStateResponse
                }
            },
            "events": {
                cls.INDEX.KEY_TRAVEL_CHANGE: {"report": KeyTravelChangeEvent}
            }
        }

        return {
            "feature_base": AnalogKeys,
            "versions": {
                AnalogKeysV0.VERSION: {
                    "main_cls": AnalogKeysV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class AnalogKeysModel


class AnalogKeysFactory(FeatureFactory):
    """
    Get ``AnalogKeys`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``AnalogKeys`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``AnalogKeysInterface``
        """
        return AnalogKeysModel.get_main_cls(version)()
    # end def create
# end class AnalogKeysFactory


class AnalogKeysInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``AnalogKeys``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_rapid_trigger_state_cls = None
        self.set_rapid_trigger_state_cls = None
        self.set_key_travel_event_state_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_rapid_trigger_state_response_cls = None
        self.set_rapid_trigger_state_response_cls = None
        self.set_key_travel_event_state_response_cls = None

        # Events
        self.key_travel_change_event_cls = None
    # end def __init__
# end class AnalogKeysInterface


class AnalogKeysV0(AnalogKeysInterface):
    """
    Define ``AnalogKeysV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> analogKeyConfigFileVer, analogKeyConfigFileMaxsize, analogKeyLevelResolution

    [1] getRapidTriggerState() -> rtSettings

    [2] setRapidTriggerState(rtSettings) -> rtSettings

    [3] setKeyTravelEventState(ktSettings) -> ktSettings

    [Event 0] KeyTravelChangeEvent -> keyCidx, keyTravel
    """
    VERSION = 0

    def __init__(self):
        # See ``AnalogKeys.__init__``
        super().__init__()
        index = AnalogKeysModel.INDEX

        # Requests
        self.get_capabilities_cls = AnalogKeysModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_rapid_trigger_state_cls = AnalogKeysModel.get_request_cls(
            self.VERSION, index.GET_RAPID_TRIGGER_STATE)
        self.set_rapid_trigger_state_cls = AnalogKeysModel.get_request_cls(
            self.VERSION, index.SET_RAPID_TRIGGER_STATE)
        self.set_key_travel_event_state_cls = AnalogKeysModel.get_request_cls(
            self.VERSION, index.SET_KEY_TRAVEL_EVENT_STATE)

        # Responses
        self.get_capabilities_response_cls = AnalogKeysModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_rapid_trigger_state_response_cls = AnalogKeysModel.get_response_cls(
            self.VERSION, index.GET_RAPID_TRIGGER_STATE)
        self.set_rapid_trigger_state_response_cls = AnalogKeysModel.get_response_cls(
            self.VERSION, index.SET_RAPID_TRIGGER_STATE)
        self.set_key_travel_event_state_response_cls = AnalogKeysModel.get_response_cls(
            self.VERSION, index.SET_KEY_TRAVEL_EVENT_STATE)

        # Events
        self.key_travel_change_event_cls = AnalogKeysModel.get_report_cls(
            self.VERSION, index.KEY_TRAVEL_CHANGE)
    # end def __init__

    def get_max_function_index(self):
        # See ``AnalogKeysInterface.get_max_function_index``
        return AnalogKeysModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class AnalogKeysV0


class ShortEmptyPacketDataFormat(AnalogKeys):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities
        - GetRapidTriggerState

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        PADDING = AnalogKeys.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AnalogKeys.DEFAULT.PADDING),)
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


class GetRapidTriggerState(ShortEmptyPacketDataFormat):
    """
    Define ``GetRapidTriggerState`` implementation class
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
                         function_index=GetRapidTriggerStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetRapidTriggerState


class SetRapidTriggerState(AnalogKeys):
    """
    Define ``SetRapidTriggerState`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Rapid Trigger Settings        8
    Reserved                      16
    ============================  ==========
    """

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        RAPID_TRIGGER_SETTINGS = AnalogKeys.FID.SOFTWARE_ID - 1
        RESERVED = RAPID_TRIGGER_SETTINGS - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        RAPID_TRIGGER_SETTINGS = 0x8
        RESERVED = 0x10
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.RAPID_TRIGGER_SETTINGS, length=LEN.RAPID_TRIGGER_SETTINGS,
                 title="RapidTriggerSettings", name="rapid_trigger_settings",
                 checks=(CheckHexList(LEN.RAPID_TRIGGER_SETTINGS // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rapid_trigger_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param rapid_trigger_state: Rapid Trigger State
        :type rapid_trigger_state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRapidTriggerStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.rapid_trigger_settings = self.RapidTriggerSettings(rapid_trigger_state=rapid_trigger_state)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``SetRapidTriggerState``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.rapid_trigger_settings = cls.RapidTriggerSettings.fromHexList(
            inner_field_container_mixin.rapid_trigger_settings)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetRapidTriggerState


class SetKeyTravelEventState(AnalogKeys):
    """
    Define ``SetKeyTravelEventState`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Travel Settings           8
    Reserved                      16
    ============================  ==========
    """

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        KEY_TRAVEL_SETTINGS = AnalogKeys.FID.SOFTWARE_ID - 1
        RESERVED = KEY_TRAVEL_SETTINGS - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        KEY_TRAVEL_SETTINGS = 0x8
        RESERVED = 0x10
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.KEY_TRAVEL_SETTINGS, length=LEN.KEY_TRAVEL_SETTINGS,
                 title="KeyTravelSettings", name="key_travel_settings",
                 checks=(CheckHexList(LEN.KEY_TRAVEL_SETTINGS // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, key_travel_event_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_travel_event_state: Key Travel Event State
        :type key_travel_event_state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetKeyTravelEventStateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.key_travel_settings = self.KeyTravelSettings(key_travel_event_state=key_travel_event_state)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``object``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``

        :return: Class instance
        :rtype: ``SetKeyTravelEventState``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.key_travel_settings = cls.KeyTravelSettings.fromHexList(
            inner_field_container_mixin.key_travel_settings)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetKeyTravelEventState


class GetCapabilitiesResponse(AnalogKeys):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ==============================  ==========
    Name                            Bit count
    ==============================  ==========
    Analog Key Config File Ver      8
    Analog Key Config File Maxsize  16
    Analog Key Level Resolution     8
    Reserved                        96
    ==============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        ANALOG_KEY_CONFIG_FILE_VER = AnalogKeys.FID.SOFTWARE_ID - 1
        ANALOG_KEY_CONFIG_FILE_MAXSIZE = ANALOG_KEY_CONFIG_FILE_VER - 1
        ANALOG_KEY_LEVEL_RESOLUTION = ANALOG_KEY_CONFIG_FILE_MAXSIZE - 1
        RESERVED = ANALOG_KEY_LEVEL_RESOLUTION - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        ANALOG_KEY_CONFIG_FILE_VER = 0x8
        ANALOG_KEY_CONFIG_FILE_MAXSIZE = 0x10
        ANALOG_KEY_LEVEL_RESOLUTION = 0x8
        RESERVED = 0x60
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.ANALOG_KEY_CONFIG_FILE_VER, length=LEN.ANALOG_KEY_CONFIG_FILE_VER,
                 title="AnalogKeyConfigFileVer", name="analog_key_config_file_ver",
                 checks=(CheckHexList(LEN.ANALOG_KEY_CONFIG_FILE_VER // 8), CheckByte(),)),
        BitField(fid=FID.ANALOG_KEY_CONFIG_FILE_MAXSIZE, length=LEN.ANALOG_KEY_CONFIG_FILE_MAXSIZE,
                 title="AnalogKeyConfigFileMaxsize", name="analog_key_config_file_maxsize",
                 checks=(CheckHexList(LEN.ANALOG_KEY_CONFIG_FILE_MAXSIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ANALOG_KEY_CONFIG_FILE_MAXSIZE) - 1),)),
        BitField(fid=FID.ANALOG_KEY_LEVEL_RESOLUTION, length=LEN.ANALOG_KEY_LEVEL_RESOLUTION,
                 title="AnalogKeyLevelResolution", name="analog_key_level_resolution",
                 checks=(CheckHexList(LEN.ANALOG_KEY_LEVEL_RESOLUTION // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, analog_key_config_file_ver, analog_key_config_file_maxsize,
                 analog_key_level_resolution, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param analog_key_config_file_ver: Analog Key Config File Ver
        :type analog_key_config_file_ver: ``int | HexList``
        :param analog_key_config_file_maxsize: Analog Key Config File Maxsize
        :type analog_key_config_file_maxsize: ``int | HexList``
        :param analog_key_level_resolution: Analog Key Level Resolution
        :type analog_key_level_resolution: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.analog_key_config_file_ver = HexList(
            Numeral(analog_key_config_file_ver, self.LEN.ANALOG_KEY_CONFIG_FILE_VER // 8))
        self.analog_key_config_file_maxsize = HexList(
            Numeral(analog_key_config_file_maxsize, self.LEN.ANALOG_KEY_CONFIG_FILE_MAXSIZE // 8))
        self.analog_key_level_resolution = HexList(
            Numeral(analog_key_level_resolution, self.LEN.ANALOG_KEY_LEVEL_RESOLUTION // 8))
    # end def __init__
# end class GetCapabilitiesResponse


class GetRapidTriggerStateResponse(AnalogKeys):
    """
    Define ``GetRapidTriggerStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Rapid Trigger Settings        8
    Reserved                      120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRapidTriggerState,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        RAPID_TRIGGER_SETTINGS = AnalogKeys.FID.SOFTWARE_ID - 1
        RESERVED = RAPID_TRIGGER_SETTINGS - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        RAPID_TRIGGER_SETTINGS = 0x8
        RESERVED = 0x78
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.RAPID_TRIGGER_SETTINGS, length=LEN.RAPID_TRIGGER_SETTINGS,
                 title="RapidTriggerSettings", name="rapid_trigger_settings",
                 checks=(CheckHexList(LEN.RAPID_TRIGGER_SETTINGS // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rapid_trigger_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param rapid_trigger_state: Rapid Trigger State
        :type rapid_trigger_state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rapid_trigger_settings = self.RapidTriggerSettings(rapid_trigger_state=rapid_trigger_state)
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
        :rtype: ``GetRapidTriggerStateResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.rapid_trigger_settings = cls.RapidTriggerSettings.fromHexList(
            inner_field_container_mixin.rapid_trigger_settings)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetRapidTriggerStateResponse


class SetRapidTriggerStateResponse(AnalogKeys):
    """
    Define ``SetRapidTriggerStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Rapid Trigger Settings        8
    Reserved                      120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRapidTriggerState,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        RAPID_TRIGGER_SETTINGS = AnalogKeys.FID.SOFTWARE_ID - 1
        RESERVED = RAPID_TRIGGER_SETTINGS - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        RAPID_TRIGGER_SETTINGS = 0x8
        RESERVED = 0x78
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.RAPID_TRIGGER_SETTINGS, length=LEN.RAPID_TRIGGER_SETTINGS,
                 title="RapidTriggerSettings", name="rapid_trigger_settings",
                 checks=(CheckHexList(LEN.RAPID_TRIGGER_SETTINGS // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, rapid_trigger_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param rapid_trigger_state: Rapid Trigger State
        :type rapid_trigger_state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.rapid_trigger_settings = self.RapidTriggerSettings(rapid_trigger_state=rapid_trigger_state)
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
        :rtype: ``SetRapidTriggerStateResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.rapid_trigger_settings = cls.RapidTriggerSettings.fromHexList(
            inner_field_container_mixin.rapid_trigger_settings)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetRapidTriggerStateResponse


class SetKeyTravelEventStateResponse(AnalogKeys):
    """
    Define ``SetKeyTravelEventStateResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Travel Settings           8
    Reserved                      120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetKeyTravelEventState,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        KEY_TRAVEL_SETTINGS = AnalogKeys.FID.SOFTWARE_ID - 1
        RESERVED = KEY_TRAVEL_SETTINGS - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        KEY_TRAVEL_SETTINGS = 0x8
        RESERVED = 0x78
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.KEY_TRAVEL_SETTINGS, length=LEN.KEY_TRAVEL_SETTINGS,
                 title="KeyTravelSettings", name="key_travel_settings",
                 checks=(CheckHexList(LEN.KEY_TRAVEL_SETTINGS // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, key_travel_event_state, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_travel_event_state: Key Travel Event State
        :type key_travel_event_state: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_travel_settings = self.KeyTravelSettings(key_travel_event_state=key_travel_event_state)
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
        :rtype: ``SetKeyTravelEventStateResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.key_travel_settings = cls.KeyTravelSettings.fromHexList(
            inner_field_container_mixin.key_travel_settings)
        return inner_field_container_mixin
    # end def fromHexList
# end class SetKeyTravelEventStateResponse


class KeyTravelChangeEvent(AnalogKeys):
    """
    Define ``KeyTravelChangeEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Key Cidx                      8
    Key Travel                    8
    Reserved                      112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(AnalogKeys.FID):
        # See ``AnalogKeys.FID``
        KEY_CIDX = AnalogKeys.FID.SOFTWARE_ID - 1
        KEY_TRAVEL = KEY_CIDX - 1
        RESERVED = KEY_TRAVEL - 1
    # end class FID

    class LEN(AnalogKeys.LEN):
        # See ``AnalogKeys.LEN``
        KEY_CIDX = 0x8
        KEY_TRAVEL = 0x8
        RESERVED = 0x70
    # end class LEN

    FIELDS = AnalogKeys.FIELDS + (
        BitField(fid=FID.KEY_CIDX, length=LEN.KEY_CIDX,
                 title="KeyCidx", name="key_cidx",
                 checks=(CheckHexList(LEN.KEY_CIDX // 8), CheckByte(),)),
        BitField(fid=FID.KEY_TRAVEL, length=LEN.KEY_TRAVEL,
                 title="KeyTravel", name="key_travel",
                 checks=(CheckHexList(LEN.KEY_TRAVEL // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=AnalogKeys.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, key_cidx, key_travel, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param key_cidx: Key Cidx
        :type key_cidx: ``int | HexList``
        :param key_travel: Key Travel
        :type key_travel: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.key_cidx = HexList(Numeral(key_cidx, self.LEN.KEY_CIDX // 8))
        self.key_travel = HexList(Numeral(key_travel, self.LEN.KEY_TRAVEL // 8))
    # end def __init__
# end class KeyTravelChangeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
