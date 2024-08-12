#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.manufacturingmode
:brief: HID++ 2.0 ``ManufacturingMode`` command interface definition
:author: Masan Xu <mxu11@logitech.com>
:date: 2023/06/14
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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ManufacturingMode(HidppMessage):
    """
    This feature allows the device enters manufacturing mode
    """
    FEATURE_ID = 0x1801
    MAX_FUNCTION_INDEX_V0 = 1

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
# end class ManufacturingMode


# noinspection DuplicatedCode
class ManufacturingModeModel(FeatureModel):
    """
    Define ``ManufacturingMode`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        SET_MANUFACTURING_MODE = 0
        GET_MANUFACTURING_MODE = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ManufacturingMode`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.SET_MANUFACTURING_MODE: {
                    "request": SetManufacturingMode,
                    "response": SetManufacturingModeResponse
                },
                cls.INDEX.GET_MANUFACTURING_MODE: {
                    "request": GetManufacturingMode,
                    "response": GetManufacturingModeResponse
                }
            }
        }

        return {
            "feature_base": ManufacturingMode,
            "versions": {
                ManufacturingModeV0.VERSION: {
                    "main_cls": ManufacturingModeV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class ManufacturingModeModel


class ManufacturingModeFactory(FeatureFactory):
    """
    Get ``ManufacturingMode`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ManufacturingMode`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``ManufacturingModeInterface``
        """
        return ManufacturingModeModel.get_main_cls(version)()
    # end def create
# end class ManufacturingModeFactory


class ManufacturingModeInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ManufacturingMode``
    """

    def __init__(self):
        # Requests
        self.set_manufacturing_mode_cls = None
        self.get_manufacturing_mode_cls = None

        # Responses
        self.set_manufacturing_mode_response_cls = None
        self.get_manufacturing_mode_response_cls = None
    # end def __init__
# end class ManufacturingModeInterface


class ManufacturingModeV0(ManufacturingModeInterface):
    """
    Define ``ManufacturingModeV0`` feature

    This feature provides model and unit specific information for version 0

    [0] setManufacturingMode(manufacturingMode) -> None

    [1] getManufacturingMode() -> manufacturingMode
    """
    VERSION = 0

    def __init__(self):
        # See ``ManufacturingMode.__init__``
        super().__init__()
        index = ManufacturingModeModel.INDEX

        # Requests
        self.set_manufacturing_mode_cls = ManufacturingModeModel.get_request_cls(
            self.VERSION, index.SET_MANUFACTURING_MODE)
        self.get_manufacturing_mode_cls = ManufacturingModeModel.get_request_cls(
            self.VERSION, index.GET_MANUFACTURING_MODE)

        # Responses
        self.set_manufacturing_mode_response_cls = ManufacturingModeModel.get_response_cls(
            self.VERSION, index.SET_MANUFACTURING_MODE)
        self.get_manufacturing_mode_response_cls = ManufacturingModeModel.get_response_cls(
            self.VERSION, index.GET_MANUFACTURING_MODE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ManufacturingModeInterface.get_max_function_index``
        return ManufacturingModeModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class ManufacturingModeV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(ManufacturingMode):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetManufacturingMode

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ManufacturingMode.FID):
        # See ``ManufacturingMode.FID``
        PADDING = ManufacturingMode.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ManufacturingMode.LEN):
        # See ``ManufacturingMode.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ManufacturingMode.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ManufacturingMode.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(ManufacturingMode):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetManufacturingModeResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ManufacturingMode.FID):
        # See ``ManufacturingMode.FID``
        PADDING = ManufacturingMode.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ManufacturingMode.LEN):
        # See ``ManufacturingMode.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ManufacturingMode.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ManufacturingMode.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class SetManufacturingMode(ManufacturingMode):
    """
    Define ``SetManufacturingMode`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    Manufacturing Mode            1
    Padding                       16
    ============================  ==========
    """

    class FID(ManufacturingMode.FID):
        # See ``ManufacturingMode.FID``
        RESERVED = ManufacturingMode.FID.SOFTWARE_ID - 1
        MANUFACTURING_MODE = RESERVED - 1
        PADDING = MANUFACTURING_MODE - 1
    # end class FID

    class LEN(ManufacturingMode.LEN):
        # See ``ManufacturingMode.LEN``
        RESERVED = 0x7
        MANUFACTURING_MODE = 0x1
        PADDING = 0x10
    # end class LEN

    FIELDS = ManufacturingMode.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ManufacturingMode.DEFAULT.PADDING),
        BitField(fid=FID.MANUFACTURING_MODE, length=LEN.MANUFACTURING_MODE,
                 title="ManufacturingMode", name="manufacturing_mode",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.MANUFACTURING_MODE) - 1),
                         CheckHexList(LEN.MANUFACTURING_MODE // 8))),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ManufacturingMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, manufacturing_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param manufacturing_mode: Manufacturing Mode
        :type manufacturing_mode: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetManufacturingModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.manufacturing_mode = manufacturing_mode
    # end def __init__
# end class SetManufacturingMode


class GetManufacturingMode(ShortEmptyPacketDataFormat):
    """
    Define ``GetManufacturingMode`` implementation class
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
                         function_index=GetManufacturingModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetManufacturingMode


class SetManufacturingModeResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetManufacturingModeResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetManufacturingMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

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
# end class SetManufacturingModeResponse


class GetManufacturingModeResponse(ManufacturingMode):
    """
    Define ``GetManufacturingModeResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    Manufacturing Mode            1
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetManufacturingMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ManufacturingMode.FID):
        # See ``ManufacturingMode.FID``
        RESERVED = ManufacturingMode.FID.SOFTWARE_ID - 1
        MANUFACTURING_MODE = RESERVED - 1
        PADDING = MANUFACTURING_MODE - 1
    # end class FID

    class LEN(ManufacturingMode.LEN):
        # See ``ManufacturingMode.LEN``
        RESERVED = 0x7
        MANUFACTURING_MODE = 0x1
        PADDING = 0x78
    # end class LEN

    FIELDS = ManufacturingMode.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ManufacturingMode.DEFAULT.PADDING),
        BitField(fid=FID.MANUFACTURING_MODE, length=LEN.MANUFACTURING_MODE,
                 title="ManufacturingMode", name="manufacturing_mode",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.MANUFACTURING_MODE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ManufacturingMode.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, manufacturing_mode, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param manufacturing_mode: Manufacturing Mode
        :type manufacturing_mode: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.manufacturing_mode = manufacturing_mode
    # end def __init__
# end class GetManufacturingModeResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
