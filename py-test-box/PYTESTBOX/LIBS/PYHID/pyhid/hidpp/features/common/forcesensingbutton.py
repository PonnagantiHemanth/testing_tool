#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.forcesensingbutton
:brief: HID++ 2.0 ``ForceSensingButton`` command interface definition
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2024/08/05
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
class ForceSensingButton(HidppMessage):
    """
    Force Sensing Button implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """
    FEATURE_ID = 0x19C0
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

    # noinspection DuplicatedCode
    class ButtonCapabilities(BitFieldContainerMixin):
        """
        Define ``ButtonCapabilities`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      15
        Customizable Force            1
        Default force                 8
        Max force                     8
        Min force                     8
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            CUSTOMIZABLE_FORCE = RESERVED - 1
            DEFAULT_FORCE = CUSTOMIZABLE_FORCE - 1
            MAX_FORCE = DEFAULT_FORCE - 1
            MIN_FORCE = MAX_FORCE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0xF
            CUSTOMIZABLE_FORCE = 0x1
            DEFAULT_FORCE = 0x8
            MAX_FORCE = 0x8
            MIN_FORCE = 0x8
        # end class LEN

        class DEFAULT(object):
            """
            Fields Default values
            """
            RESERVED = 0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     default_value=DEFAULT.RESERVED,
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
            BitField(fid=FID.CUSTOMIZABLE_FORCE, length=LEN.CUSTOMIZABLE_FORCE,
                     title="CustomizableForce", name="customizable_force",
                     checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CUSTOMIZABLE_FORCE) - 1),)),
            BitField(fid=FID.DEFAULT_FORCE, length=LEN.DEFAULT_FORCE,
                     title="DefaultForce", name="default_force",
                     checks=(CheckHexList(LEN.DEFAULT_FORCE // 8), CheckByte(),)),
            BitField(fid=FID.MAX_FORCE, length=LEN.MAX_FORCE,
                     title="MaxForce", name="max_force",
                     checks=(CheckHexList(LEN.MAX_FORCE // 8), CheckByte(),)),
            BitField(fid=FID.MIN_FORCE, length=LEN.MIN_FORCE,
                     title="MinForce", name="min_force",
                     checks=(CheckHexList(LEN.MIN_FORCE // 8), CheckByte(),)),
        )
    # end class ButtonCapabilities
# end class ForceSensingButton


# noinspection DuplicatedCode
class ForceSensingButtonModel(FeatureModel):
    """
    Define ``ForceSensingButton`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_BUTTON_CAPABILITIES = 1
        GET_BUTTON_CONFIG = 2
        SET_BUTTON_CONFIG = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ForceSensingButton`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_BUTTON_CAPABILITIES: {
                    "request": GetButtonCapabilities,
                    "response": GetButtonCapabilitiesResponse
                },
                cls.INDEX.GET_BUTTON_CONFIG: {
                    "request": GetButtonConfig,
                    "response": GetButtonConfigResponse
                },
                cls.INDEX.SET_BUTTON_CONFIG: {
                    "request": SetButtonConfig,
                    "response": SetButtonConfigResponse
                }
            }
        }

        return {
            "feature_base": ForceSensingButton,
            "versions": {
                ForceSensingButtonV0.VERSION: {
                    "main_cls": ForceSensingButtonV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class ForceSensingButtonModel


class ForceSensingButtonFactory(FeatureFactory):
    """
    Get ``ForceSensingButton`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ForceSensingButton`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``ForceSensingButtonInterface``
        """
        return ForceSensingButtonModel.get_main_cls(version)()
    # end def create
# end class ForceSensingButtonFactory


class ForceSensingButtonInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ForceSensingButton``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_button_capabilities_cls = None
        self.get_button_config_cls = None
        self.set_button_config_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_button_capabilities_response_cls = None
        self.get_button_config_response_cls = None
        self.set_button_config_response_cls = None
    # end def __init__
# end class ForceSensingButtonInterface


class ForceSensingButtonV0(ForceSensingButtonInterface):
    """
    Define ``ForceSensingButtonV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> numberOfButtons

    [1] getButtonCapabilities(buttonId) -> button_capabilities(customizableForce, defaultForce, maxForce, minForce)

    [2] getButtonConfig(buttonId) -> currentForce

    [3] setButtonConfig(buttonId, newForce) -> buttonId, currentForce
    """
    VERSION = 0

    def __init__(self):
        # See ``ForceSensingButton.__init__``
        super().__init__()
        index = ForceSensingButtonModel.INDEX

        # Requests
        self.get_capabilities_cls = ForceSensingButtonModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_button_capabilities_cls = ForceSensingButtonModel.get_request_cls(
            self.VERSION, index.GET_BUTTON_CAPABILITIES)
        self.get_button_config_cls = ForceSensingButtonModel.get_request_cls(
            self.VERSION, index.GET_BUTTON_CONFIG)
        self.set_button_config_cls = ForceSensingButtonModel.get_request_cls(
            self.VERSION, index.SET_BUTTON_CONFIG)

        # Responses
        self.get_capabilities_response_cls = ForceSensingButtonModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_button_capabilities_response_cls = ForceSensingButtonModel.get_response_cls(
            self.VERSION, index.GET_BUTTON_CAPABILITIES)
        self.get_button_config_response_cls = ForceSensingButtonModel.get_response_cls(
            self.VERSION, index.GET_BUTTON_CONFIG)
        self.set_button_config_response_cls = ForceSensingButtonModel.get_response_cls(
            self.VERSION, index.SET_BUTTON_CONFIG)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ForceSensingButtonInterface.get_max_function_index``
        return ForceSensingButtonModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class ForceSensingButtonV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(ForceSensingButton):
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

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        PADDING = ForceSensingButton.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class ButtonIDRequest(ForceSensingButton):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetButtonCapabilities
        - GetButtonConfig

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Button ID                     8
    Reserved                      16
    ============================  ==========
    """

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        BUTTON_ID = ForceSensingButton.FID.SOFTWARE_ID - 1
        RESERVED = BUTTON_ID - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        BUTTON_ID = 0x8
        RESERVED = 0x10
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.BUTTON_ID, length=LEN.BUTTON_ID,
                 title="ButtonId", name="button_id",
                 checks=(CheckHexList(LEN.BUTTON_ID // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),
    )
# end class ButtonIDRequest


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


class GetButtonCapabilities(ButtonIDRequest):
    """
    Define ``GetButtonCapabilities`` implementation class
    """

    def __init__(self, device_index, feature_index, button_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param button_id: Button ID
        :type button_id: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetButtonCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.button_id = HexList(Numeral(button_id, self.LEN.BUTTON_ID // 8))
    # end def __init__
# end class GetButtonCapabilities


class GetButtonConfig(ButtonIDRequest):
    """
    Define ``GetButtonConfig`` implementation class
    """

    def __init__(self, device_index, feature_index, button_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param button_id: Button ID
        :type button_id: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetButtonConfigResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.button_id = HexList(Numeral(button_id, self.LEN.BUTTON_ID // 8))
    # end def __init__
# end class GetButtonConfig


class SetButtonConfig(ForceSensingButton):
    """
    Define ``SetButtonConfig`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Button ID                     8
    New force                     8
    Reserved                      8
    ============================  ==========
    """

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        BUTTON_ID = ForceSensingButton.FID.SOFTWARE_ID - 1
        NEW_FORCE = BUTTON_ID - 1
        RESERVED = NEW_FORCE - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        BUTTON_ID = 0x8
        NEW_FORCE = 0x8
        RESERVED = 0x8
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.BUTTON_ID, length=LEN.BUTTON_ID,
                 title="ButtonId", name="button_id",
                 checks=(CheckHexList(LEN.BUTTON_ID // 8), CheckByte(),)),
        BitField(fid=FID.NEW_FORCE, length=LEN.NEW_FORCE,
                 title="NewForce", name="new_force",
                 checks=(CheckHexList(LEN.NEW_FORCE // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, button_id, new_force, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param button_id: Button ID
        :type button_id: ``int | HexList``
        :param new_force: New force
        :type new_force: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetButtonConfigResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        self.button_id = HexList(Numeral(button_id, self.LEN.BUTTON_ID // 8))
        self.new_force = new_force
    # end def __init__
# end class SetButtonConfig


class GetCapabilitiesResponse(ForceSensingButton):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Number of Buttons             8
    Reserved                      120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        NUMBER_OF_BUTTONS = ForceSensingButton.FID.SOFTWARE_ID - 1
        RESERVED = NUMBER_OF_BUTTONS - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        NUMBER_OF_BUTTONS = 0x8
        RESERVED = 0x78
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.NUMBER_OF_BUTTONS, length=LEN.NUMBER_OF_BUTTONS,
                 title="NumberOfButtons", name="number_of_buttons",
                 checks=(CheckHexList(LEN.NUMBER_OF_BUTTONS // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, number_of_buttons, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param number_of_buttons: Number of Buttons
        :type number_of_buttons: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.number_of_buttons = number_of_buttons
    # end def __init__
# end class GetCapabilitiesResponse


class GetButtonCapabilitiesResponse(ForceSensingButton):
    """
    Define ``GetButtonCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ButtonCapabilities            40
    Reserved                      88
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetButtonCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        BUTTON_CAPABILITIES = ForceSensingButton.FID.SOFTWARE_ID - 1
        RESERVED = BUTTON_CAPABILITIES - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        BUTTON_CAPABILITIES = 0x28
        RESERVED = 0x58
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.BUTTON_CAPABILITIES, length=LEN.BUTTON_CAPABILITIES,
                 title="ButtonCapabilities", name="button_capabilities",
                 checks=(CheckHexList(LEN.BUTTON_CAPABILITIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.BUTTON_CAPABILITIES) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, customizable_force, default_force, max_force, min_force, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param customizable_force: Customizable Force
        :type customizable_force: ``bool | HexList``
        :param default_force: Default force
        :type default_force: ``HexList``
        :param max_force: Max force
        :type max_force: ``HexList``
        :param min_force: Min force
        :type min_force: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.button_capabilities = self.ButtonCapabilities(customizable_force=customizable_force,
                                                           default_force=default_force,
                                                           max_force=max_force,
                                                           min_force=min_force)
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
        :rtype: ``GetButtonCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.button_capabilities = cls.ButtonCapabilities.fromHexList(
            inner_field_container_mixin.button_capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetButtonCapabilitiesResponse


class GetButtonConfigResponse(ForceSensingButton):
    """
    Define ``GetButtonConfigResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Current Force                 8
    Reserved                      120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetButtonConfig,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        CURRENT_FORCE = ForceSensingButton.FID.SOFTWARE_ID - 1
        RESERVED = CURRENT_FORCE - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        CURRENT_FORCE = 0x8
        RESERVED = 0x78
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.CURRENT_FORCE, length=LEN.CURRENT_FORCE,
                 title="CurrentForce", name="current_force",
                 checks=(CheckHexList(LEN.CURRENT_FORCE // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, current_force, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param current_force: Current Force
        :type current_force: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.current_force = current_force
    # end def __init__
# end class GetButtonConfigResponse


class SetButtonConfigResponse(ForceSensingButton):
    """
    Define ``SetButtonConfigResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Button ID                     8
    Current Force                 8
    Reserved                      112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetButtonConfig,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(ForceSensingButton.FID):
        # See ``ForceSensingButton.FID``
        BUTTON_ID = ForceSensingButton.FID.SOFTWARE_ID - 1
        CURRENT_FORCE = BUTTON_ID - 1
        RESERVED = CURRENT_FORCE - 1
    # end class FID

    class LEN(ForceSensingButton.LEN):
        # See ``ForceSensingButton.LEN``
        BUTTON_ID = 0x8
        CURRENT_FORCE = 0x8
        RESERVED = 0x70
    # end class LEN

    FIELDS = ForceSensingButton.FIELDS + (
        BitField(fid=FID.BUTTON_ID, length=LEN.BUTTON_ID,
                 title="ButtonId", name="button_id",
                 checks=(CheckHexList(LEN.BUTTON_ID // 8), CheckByte(),)),
        BitField(fid=FID.CURRENT_FORCE, length=LEN.CURRENT_FORCE,
                 title="CurrentForce", name="current_force",
                 checks=(CheckHexList(LEN.CURRENT_FORCE // 8), CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckByte(),),
                 default_value=ForceSensingButton.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, button_id, current_force, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param button_id: Button ID
        :type button_id: ``int | HexList``
        :param current_force: Current Force
        :type current_force: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        self.button_id = HexList(Numeral(button_id, self.LEN.BUTTON_ID // 8))
        self.current_force = current_force
    # end def __init__
# end class SetButtonConfigResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
