#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.combinedpedals
:brief: HID++ 2.0 ``CombinedPedals`` command interface definition
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/25
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
class CombinedPedals(HidppMessage):
    """
    This feature is used to retrieve the status of combined pedals and to enable/disable the combined pedals.
    """
    FEATURE_ID = 0x80D0
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class CombinedPedals


class CombinedPedalsModel(FeatureModel):
    """
    ``CombinedPedals`` feature model
    """
    class INDEX(object):
        """
        Function/Event index
        """
        # Function index
        GET_COMBINED_PEDALS = 0
        SET_COMBINED_PEDALS = 1

        # Event index
        COMBINED_PEDALS_CHANGED = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        ``CombinedPedals`` feature data model
        """
        return {
            "feature_base": CombinedPedals,
            "versions": {
                CombinedPedalsV0.VERSION: {
                    "main_cls": CombinedPedalsV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_COMBINED_PEDALS: {
                                "request": GetCombinedPedals,
                                "response": GetCombinedPedalsResponse
                            },
                            cls.INDEX.SET_COMBINED_PEDALS: {
                                "request": SetCombinedPedals,
                                "response": SetCombinedPedalsResponse
                            }
                        },
                        "events": {
                            cls.INDEX.COMBINED_PEDALS_CHANGED: {
                                "report": CombinedPedalsChangedEvent
                            }
                        }
                    }
                }
            }
        }
    # end def _get_data_model
# end class CombinedPedalsModel


class CombinedPedalsFactory(FeatureFactory):
    """
    Factory which creates a ``CombinedPedals`` object from a given version
    """
    @staticmethod
    def create(version):
        """
        ``CombinedPedals`` object creation from version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``CombinedPedalsInterface``
        """
        return CombinedPedalsModel.get_main_cls(version)()
    # end def create
# end class CombinedPedalsFactory


class CombinedPedalsInterface(FeatureInterface, ABC):
    """
    Defines required interfaces for ``CombinedPedals`` classes
    """
    def __init__(self):
        # Requests
        self.get_combined_pedals_cls = None
        self.set_combined_pedals_cls = None

        # Responses
        self.get_combined_pedals_response_cls = None
        self.set_combined_pedals_response_cls = None

        # Events
        self.combined_pedals_changed_event_cls = None
    # end def __init__
# end class CombinedPedalsInterface


class CombinedPedalsV0(CombinedPedalsInterface):
    """
    ``CombinedPedalsV0``

    This feature provides model and unit specific information for version 0

    [0] getCombinedPedals() -> combinedPedalsEnabled

    [1] setCombinedPedals(enableCombinedPedals) -> combinedPedalsEnabled

    [Event 0] combinedPedalsChangedEvent -> combinedPedalsEnabled
    """
    VERSION = 0

    def __init__(self):
        # See ``CombinedPedals.__init__``
        super().__init__()
        index = CombinedPedalsModel.INDEX

        # Requests
        self.get_combined_pedals_cls = CombinedPedalsModel.get_request_cls(
            self.VERSION, index.GET_COMBINED_PEDALS)
        self.set_combined_pedals_cls = CombinedPedalsModel.get_request_cls(
            self.VERSION, index.SET_COMBINED_PEDALS)

        # Responses
        self.get_combined_pedals_response_cls = CombinedPedalsModel.get_response_cls(
            self.VERSION, index.GET_COMBINED_PEDALS)
        self.set_combined_pedals_response_cls = CombinedPedalsModel.get_response_cls(
            self.VERSION, index.SET_COMBINED_PEDALS)

        # Events
        self.combined_pedals_changed_event_cls = CombinedPedalsModel.get_report_cls(
            self.VERSION, index.COMBINED_PEDALS_CHANGED)
    # end def __init__

    def get_max_function_index(self):
        # See ``CombinedPedalsInterface.get_max_function_index``
        return CombinedPedalsModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class CombinedPedalsV0


class ShortEmptyPacketDataFormat(CombinedPedals):
    """
    This class is to be used as a base class for several messages in this feature
        - GetCombinedPedals

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(CombinedPedals.FID):
        """
        Field Identifiers
        """
        PADDING = CombinedPedals.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(CombinedPedals.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = CombinedPedals.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=CombinedPedals.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class CombinedPedalsPacketDataFormat(CombinedPedals):
    """
    This class is to be used as a base class for several messages in this feature.
        - GetCombinedPedalsResponse
        - SetCombinedPedalsResponse
        - CombinedPedalsChangedEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    CombinedPedalsEnabled         1
    Padding                       120
    ============================  ==========
    """
    class FID(CombinedPedals.FID):
        """
        Field Identifiers
        """
        RESERVED = CombinedPedals.FID.SOFTWARE_ID - 1
        COMBINED_PEDALS_ENABLED = RESERVED - 1
        PADDING = COMBINED_PEDALS_ENABLED - 1
    # end class FID

    class LEN(CombinedPedals.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x7
        COMBINED_PEDALS_ENABLED = 0x1
        PADDING = 0x78
    # end class LEN

    FIELDS = CombinedPedals.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=CombinedPedals.DEFAULT.PADDING),
        BitField(fid=FID.COMBINED_PEDALS_ENABLED, length=LEN.COMBINED_PEDALS_ENABLED,
                 title="CombinedPedalsEnabled", name="combined_pedals_enabled",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.COMBINED_PEDALS_ENABLED) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=CombinedPedals.DEFAULT.PADDING),
    )
# end class CombinedPedalsPacketDataFormat


class GetCombinedPedals(ShortEmptyPacketDataFormat):
    """
    ``GetCombinedPedals`` implementation class for version 0
    """
    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetCombinedPedalsResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCombinedPedals


class GetCombinedPedalsResponse(CombinedPedalsPacketDataFormat):
    """
    ``GetCombinedPedalsResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCombinedPedals,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, combined_pedals_enabled, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param combined_pedals_enabled: Pedals are combined or not
        :type combined_pedals_enabled: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.combined_pedals_enabled = combined_pedals_enabled
    # end def __init__
# end class GetCombinedPedalsResponse


class SetCombinedPedals(CombinedPedals):
    """
    ``SetCombinedPedals`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    EnableCombinedPedals          1
    Padding                       16
    ============================  ==========
    """
    class FID(CombinedPedals.FID):
        """
        Field Identifiers
        """
        RESERVED = CombinedPedals.FID.SOFTWARE_ID - 1
        ENABLE_COMBINED_PEDALS = RESERVED - 1
        PADDING = ENABLE_COMBINED_PEDALS - 1
    # end class FID

    class LEN(CombinedPedals.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x7
        ENABLE_COMBINED_PEDALS = 0x1
        PADDING = 0x10
    # end class LEN

    FIELDS = CombinedPedals.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=CombinedPedals.DEFAULT.PADDING),
        BitField(fid=FID.ENABLE_COMBINED_PEDALS, length=LEN.ENABLE_COMBINED_PEDALS,
                 title="EnableCombinedPedals", name="enable_combined_pedals",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.ENABLE_COMBINED_PEDALS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=CombinedPedals.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enable_combined_pedals, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param enable_combined_pedals: If set, then the device starts reporting combined pedals.
                                       If reset, then the device starts reporting separate pedals
        :type enable_combined_pedals: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetCombinedPedalsResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.enable_combined_pedals = enable_combined_pedals
    # end def __init__
# end class SetCombinedPedals


class SetCombinedPedalsResponse(CombinedPedalsPacketDataFormat):
    """
    ``SetCombinedPedalsResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCombinedPedals,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, combined_pedals_enabled, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param combined_pedals_enabled: Pedals are combined or not
        :type combined_pedals_enabled: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.combined_pedals_enabled = combined_pedals_enabled
    # end def __init__
# end class SetCombinedPedalsResponse


class CombinedPedalsChangedEvent(CombinedPedalsPacketDataFormat):
    """
    ``CombinedPedalsChangedEvent`` implementation class for version 0
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, combined_pedals_enabled, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param combined_pedals_enabled: Pedals are combined or not
        :type combined_pedals_enabled: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.combined_pedals_enabled = combined_pedals_enabled
    # end def __init__
# end class CombinedPedalsChangedEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
