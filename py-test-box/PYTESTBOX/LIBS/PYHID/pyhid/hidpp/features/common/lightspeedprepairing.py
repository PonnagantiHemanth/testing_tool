#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.lightspeedprepairing
:brief: HID++ 2.0 ``LightspeedPrepairing`` command interface definition
:author: Zane Lu <zlu@logitech.com>
:date: 2022/06/07
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
class LightspeedPrepairing(HidppMessage):
    """
    eQuad Pairing with Encryption with slot management
    """

    FEATURE_ID = 0x1817
    MAX_FUNCTION_INDEX = 4

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

    class DataDetailsPairingAddress(BitFieldContainerMixin):
        """
        Provide parsing of data field for the pairing address
        """
        class FID:
            """
            Field Identifiers
            """
            PAIRING_ADDRESS_BASE = 0xFF
            ADDRESS_DEST = PAIRING_ADDRESS_BASE - 1
            UNUSED = ADDRESS_DEST - 1
        # end class FID

        class LEN:
            """
            Field length in bits
            """
            PAIRING_ADDRESS_BASE = 0x20
            ADDRESS_DEST = 0x08
            UNUSED = 0x08
        # end class LEN

        class DEFAULT:
            ADDRESS_DEST = 0x01
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.PAIRING_ADDRESS_BASE,
                     length=LEN.PAIRING_ADDRESS_BASE,
                     title="PairingAddressBase",
                     name="pairing_address_base",
                     checks=(CheckHexList(LEN.PAIRING_ADDRESS_BASE // 8), CheckByte(),)),
            BitField(fid=FID.ADDRESS_DEST,
                     length=LEN.ADDRESS_DEST,
                     title="AddressDest",
                     name="address_dest",
                     checks=(CheckHexList(LEN.ADDRESS_DEST // 8), CheckByte(),)),
            BitField(fid=FID.UNUSED,
                     length=LEN.UNUSED,
                     title="Unused",
                     name="unused",
                     checks=(CheckHexList(LEN.UNUSED // 8), CheckByte(),)),
        )
    # end class DataDetailsPairingAddress

    class DataDetailsEquadAttributes(BitFieldContainerMixin):
        """
        Provide parsing of data field for the EQUAD attributes
        """
        class FID:
            """
            Field Identifiers
            """
            EQUAD_ATTRIBUTES = 0xFF
        # end class FID

        class LEN:
            """
            Field length in bits
            """
            EQUAD_ATTRIBUTES = 0x30
        # end class LEN

        FIELDS = (
            BitField(fid=FID.EQUAD_ATTRIBUTES,
                     length=LEN.EQUAD_ATTRIBUTES,
                     title="EquadAttributes",
                     name="equad_attributes",
                     checks=(CheckHexList(LEN.EQUAD_ATTRIBUTES // 8), CheckByte(),)),
        )
    # end class DataDetailsEquadAttributes
# end class LightspeedPrepairing


class LightspeedPrepairingModel(FeatureModel):
    """
    Define ``LightspeedPrepairing`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        PREPAIRING_MANAGEMENT = 1
        SET_LTK = 2
        SET_PREPAIRING_DATA = 3
        GET_PREPAIRING_DATA = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``LightspeedPrepairing`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.PREPAIRING_MANAGEMENT: {
                    "request": PrepairingManagement,
                    "response": PrepairingManagementResponse
                },
                cls.INDEX.SET_LTK: {
                    "request": SetLTK,
                    "response": SetLTKResponse
                },
                cls.INDEX.SET_PREPAIRING_DATA: {
                    "request": SetPrepairingData,
                    "response": SetPrepairingDataResponse
                },
                cls.INDEX.GET_PREPAIRING_DATA: {
                    "request": GetPrepairingData,
                    "response": GetPrepairingDataResponse
                }
            }
        }

        return {
            "feature_base": LightspeedPrepairing,
            "versions": {
                LightspeedPrepairingV0.VERSION: {
                    "main_cls": LightspeedPrepairingV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class LightspeedPrepairingModel


class LightspeedPrepairingFactory(FeatureFactory):
    """
    Get ``LightspeedPrepairing`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``LightspeedPrepairing`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``LightspeedPrepairingInterface``
        """
        return LightspeedPrepairingModel.get_main_cls(version)()
    # end def create
# end class LightspeedPrepairingFactory


class LightspeedPrepairingInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``LightspeedPrepairing``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.prepairing_management_cls = None
        self.set_ltk_cls = None
        self.set_prepairing_data_cls = None
        self.get_prepairing_data_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.prepairing_management_response_cls = None
        self.set_ltk_response_cls = None
        self.set_prepairing_data_response_cls = None
        self.get_prepairing_data_response_cls = None
    # end def __init__
# end class LightspeedPrepairingInterface


class LightspeedPrepairingV0(LightspeedPrepairingInterface):
    """
    Define ``LightspeedPrepairingV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> useAttr, lS2, crush, lS

    [1] prepairingManagement(lS2, crush, lS, prepairing_management_control) -> None

    [2] setLTK(ltk) -> None

    [3] setPrepairingData(dataType, data) -> None

    [4] getPrepairingData(information_type, data_type, reserved) -> information_type, data_type, data
    """

    VERSION = 0

    def __init__(self):
        # See ``LightspeedPrepairing.__init__``
        super().__init__()
        index = LightspeedPrepairingModel.INDEX

        # Requests
        self.get_capabilities_cls = LightspeedPrepairingModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.prepairing_management_cls = LightspeedPrepairingModel.get_request_cls(
            self.VERSION, index.PREPAIRING_MANAGEMENT)
        self.set_ltk_cls = LightspeedPrepairingModel.get_request_cls(
            self.VERSION, index.SET_LTK)
        self.set_prepairing_data_cls = LightspeedPrepairingModel.get_request_cls(
            self.VERSION, index.SET_PREPAIRING_DATA)
        self.get_prepairing_data_cls = LightspeedPrepairingModel.get_request_cls(
            self.VERSION, index.GET_PREPAIRING_DATA)

        # Responses
        self.get_capabilities_response_cls = LightspeedPrepairingModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.prepairing_management_response_cls = LightspeedPrepairingModel.get_response_cls(
            self.VERSION, index.PREPAIRING_MANAGEMENT)
        self.set_ltk_response_cls = LightspeedPrepairingModel.get_response_cls(
            self.VERSION, index.SET_LTK)
        self.set_prepairing_data_response_cls = LightspeedPrepairingModel.get_response_cls(
            self.VERSION, index.SET_PREPAIRING_DATA)
        self.get_prepairing_data_response_cls = LightspeedPrepairingModel.get_response_cls(
            self.VERSION, index.GET_PREPAIRING_DATA)
    # end def __init__

    def get_max_function_index(self):
        # See ``LightspeedPrepairingInterface.get_max_function_index``
        return LightspeedPrepairingModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class LightspeedPrepairingV0


class ShortEmptyPacketDataFormat(LightspeedPrepairing):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetCapabilities

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        PADDING = LightspeedPrepairing.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(LightspeedPrepairing):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - PrepairingManagementResponse
        - SetLTKResponse
        - SetPrepairingDataResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        PADDING = LightspeedPrepairing.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See LightspeedPrepairing.LEN
        PADDING = 0x80
    # end class LEN

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetCapabilities(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class for version 0
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
                         functionIndex=GetCapabilitiesResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetCapabilitiesResponse(LightspeedPrepairing):
    """
    Define ``GetCapabilitiesResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved_Flags                7
    UseAttr                       1
    Reserved_Slots                5
    LS2                           1
    Crush                         1
    LS                            1
    Padding                       112
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        RESERVED_FLAGS = LightspeedPrepairing.FID.SOFTWARE_ID - 1
        USE_ATTR = RESERVED_FLAGS - 1
        RESERVED_SLOTS = USE_ATTR - 1
        LS2 = RESERVED_SLOTS - 1
        CRUSH = LS2 - 1
        LS = CRUSH - 1
        PADDING = LS - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        RESERVED_FLAGS = 0x7
        USE_ATTR = 0x1
        RESERVED_SLOTS = 0x5
        LS2 = 0x1
        CRUSH = 0x1
        LS = 0x1
        PADDING = 0x70
    # end class LEN

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.RESERVED_FLAGS, length=LEN.RESERVED_FLAGS,
                 title="ReservedFlags", name="reserved_flags",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_FLAGS) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
        BitField(fid=FID.USE_ATTR, length=LEN.USE_ATTR,
                 title="UseAttr", name="use_attr",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.USE_ATTR) - 1),)),
        BitField(fid=FID.RESERVED_SLOTS, length=LEN.RESERVED_SLOTS,
                 title="ReservedSlots", name="reserved_slots",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_SLOTS) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
        BitField(fid=FID.LS2, length=LEN.LS2,
                 title="LS2", name="ls2",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.LS2) - 1),)),
        BitField(fid=FID.CRUSH, length=LEN.CRUSH,
                 title="Crush", name="crush",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CRUSH) - 1),)),
        BitField(fid=FID.LS, length=LEN.LS,
                 title="LS", name="ls",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.LS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, use_attr, ls2, crush, ls, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param use_attr: Use Attr
        :type use_attr: ``int`` or ``HexList``
        :param ls2: LS2 Pairing (2:1 pairing)
        :type ls2: ``bool`` or ``HexList``
        :param crush: Crush Pairing
        :type crush: ``bool`` or ``HexList``
        :param ls: LS Pairing
        :type ls: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.use_attr = use_attr
        self.ls2 = ls2
        self.crush = crush
        self.ls = ls
    # end def __init__
# end class GetCapabilitiesResponse


class PrepairingManagement(LightspeedPrepairing):
    """
    Define ``PrepairingManagement`` implementation class for version 0

    Format:
    =============================  ==========
    Name                           Bit count
    =============================  ==========
    Reserved_Slot                  5
    LS2                            1
    Crush                          1
    LS                             1
    Prepairing Management Control  8
    Padding                        112
    =============================  ==========
    """

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        RESERVED_SLOT = LightspeedPrepairing.FID.SOFTWARE_ID - 1
        LS2 = RESERVED_SLOT - 1
        CRUSH = LS2 - 1
        LS = CRUSH - 1
        PREPAIRING_MANAGEMENT_CONTROL = LS - 1
        PADDING = PREPAIRING_MANAGEMENT_CONTROL - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        RESERVED_SLOT = 0x5
        LS2 = 0x1
        CRUSH = 0x1
        LS = 0x1
        PREPAIRING_MANAGEMENT_CONTROL = 0x8
        PADDING = 0x70
    # end class LEN

    class PairingSlot:
        """
        Pairing Slot Definition
        """
        LS = 0x01
        CRUSH = 0x02
        LS2 = 0x04
    # end class PairingSlot

    class Control:
        """
        Prepairing Manaement Control Definition
        """
        START = 0x00
        STORE = 0x01
        DELETE = 0x02
    # end class Control

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.RESERVED_SLOT, length=LEN.RESERVED_SLOT,
                 title="ReservedSlot", name="reserved_slot",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RESERVED_SLOT) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
        BitField(fid=FID.LS2, length=LEN.LS2,
                 title="LS2", name="ls2",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.LS2) - 1),)),
        BitField(fid=FID.CRUSH, length=LEN.CRUSH,
                 title="Crush", name="crush",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CRUSH) - 1),)),
        BitField(fid=FID.LS, length=LEN.LS,
                 title="LS", name="ls",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.LS) - 1),)),
        BitField(fid=FID.PREPAIRING_MANAGEMENT_CONTROL, length=LEN.PREPAIRING_MANAGEMENT_CONTROL,
                 title="PrepairingManagementControl", name="prepairing_management_control",
                 checks=(CheckHexList(LEN.PREPAIRING_MANAGEMENT_CONTROL // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, ls2, crush, ls, prepairing_management_control, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ls2: LS2
        :type ls2: ``bool`` or ``HexList``
        :param crush: Crush
        :type crush: ``bool`` or ``HexList``
        :param ls: LS
        :type ls: ``bool`` or ``HexList``
        :param prepairing_management_control: prepairing_management_control
        :type prepairing_management_control: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=PrepairingManagementResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.ls2 = ls2
        self.crush = crush
        self.ls = ls
        self.prepairing_management_control = prepairing_management_control
    # end def __init__
# end class PrepairingManagement


class PrepairingManagementResponse(LongEmptyPacketDataFormat):
    """
    Define ``PrepairingManagementResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (PrepairingManagement,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class PrepairingManagementResponse


class SetLTK(LightspeedPrepairing):
    """
    Define ``SetLTK`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ltk                           128
    ============================  ==========
    """

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        LTK = LightspeedPrepairing.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        LTK = 0x80
    # end class LEN

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.LTK, length=LEN.LTK,
                 title="ltk", name="ltk",
                 checks=(CheckHexList(LEN.LTK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.LTK) - 1),)),
    )

    def __init__(self, device_index, feature_index, ltk, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param ltk: ltk
        :type ltk: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetLTKResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.ltk = ltk
    # end def __init__
# end class SetLTK


class SetLTKResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetLTKResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetLTK,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetLTKResponse


class SetPrepairingData(LightspeedPrepairing):
    """
    Define ``SetPrepairingData`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    dataType                      8
    data                          48
    Reserved                      72
    ============================  ==========
    """

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        DATATYPE = LightspeedPrepairing.FID.SOFTWARE_ID - 1
        DATA = DATATYPE - 1
        RESERVED = DATA - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        DATATYPE = 0x8
        DATA = 0x30
        RESERVED = 0x48
    # end class LEN

    class DataType:
        PAIRING_ADDRESS = 0x00
        EQUAD_ATTRIBUTES = 0x01
    # end class DataType

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.DATATYPE, length=LEN.DATATYPE,
                 title="DataType", name="data_type",
                 checks=(CheckHexList(LEN.DATATYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, data_type,
                 pairing_address_base=None, address_dest=None,
                 equad_attributes=None, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data_type: Data Type
        :type data_type: ``int`` or ``HexList``
        :param pairing_address_base: pairing address base - OPTIONAL
        :type pairing_address_base: ``HexList``
        :param address_dest: address dest - OPTIONAL
        :type address_dest: `int`` or ``HexList``
        :param equad_attributes: equad attributes - OPTIONAL
        :type equad_attributes: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetPrepairingDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data_type = HexList(data_type)
        if self.data_type == HexList(GetPrepairingData.DataType.PAIRING_ADDRESS):
            self.data = self.DataDetailsPairingAddress(
                pairing_address_base=pairing_address_base,
                address_dest=address_dest,
                unused=0x00
            )
        else:
            self.data = self.DataDetailsEquadAttributes(
                equad_attributes=equad_attributes
            )
        # end if
    # end def __init__
# end class SetPrepairingData


class SetPrepairingDataResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetPrepairingDataResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetPrepairingData,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

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
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SetPrepairingDataResponse


class GetPrepairingData(LightspeedPrepairing):
    """
    Define ``GetPrepairingData`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    information_type              8
    data_type                     8
    Reserved                      112
    ============================  ==========
    """

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        INFORMATION_TYPE = LightspeedPrepairing.FID.SOFTWARE_ID - 1
        DATA_TYPE = INFORMATION_TYPE - 1
        RESERVED = DATA_TYPE - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        INFORMATION_TYPE = 0x8
        DATA_TYPE = 0x8
        RESERVED = 0x70
    # end class LEN

    class InfoType:
        PAIRING = 0x00
        PRE_PAIRING = 0xFF
    # end class InfoType

    class DataType:
        PAIRING_ADDRESS = 0x00
        EQUAD_ATTRIBUTES = 0x01
    # end class DataType

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.INFORMATION_TYPE, length=LEN.INFORMATION_TYPE,
                 title="information_type", name="information_type",
                 checks=(CheckHexList(LEN.INFORMATION_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_TYPE, length=LEN.DATA_TYPE,
                 title="data_type", name="data_type",
                 checks=(CheckHexList(LEN.DATA_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),)),
    )

    def __init__(self, device_index, feature_index, information_type, data_type, reserved, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param information_type: information_type
        :type information_type: ``int`` or ``HexList``
        :param data_type: data_type
        :type data_type: ``int`` or ``HexList``
        :param reserved: Reserved
        :type reserved: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetPrepairingDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.information_type = information_type
        self.data_type = data_type
        self.reserved = reserved
    # end def __init__
# end class GetPrepairingData


class GetPrepairingDataResponse(LightspeedPrepairing):
    """
    Define ``GetPrepairingDataResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    information_type              8
    data_type                     8
    data                          48
    Padding                       64
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPrepairingData,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(LightspeedPrepairing.FID):
        # See ``LightspeedPrepairing.FID``
        INFORMATION_TYPE = LightspeedPrepairing.FID.SOFTWARE_ID - 1
        DATA_TYPE = INFORMATION_TYPE - 1
        DATA = DATA_TYPE - 1
        PADDING = DATA - 1
    # end class FID

    class LEN(LightspeedPrepairing.LEN):
        # See ``LightspeedPrepairing.LEN``
        INFORMATION_TYPE = 0x8
        DATA_TYPE = 0x8
        DATA = 0x30
        PADDING = 0x40
    # end class LEN

    FIELDS = LightspeedPrepairing.FIELDS + (
        BitField(fid=FID.INFORMATION_TYPE, length=LEN.INFORMATION_TYPE,
                 title="information_type", name="information_type",
                 checks=(CheckHexList(LEN.INFORMATION_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_TYPE, length=LEN.DATA_TYPE,
                 title="data_type", name="data_type",
                 checks=(CheckHexList(LEN.DATA_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),),
                 default_value=LightspeedPrepairing.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, information_type, data_type, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param information_type: information_type
        :type information_type: ``int`` or ``HexList``
        :param data_type: data_type
        :type data_type: ``int`` or ``HexList``
        :param data: data
        :type data: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.information_type = information_type
        self.data_type = data_type
        self.data = data
        # end if
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parsing from HexList instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetPrepairingDataResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        if inner_field_container_mixin.data_type == HexList(GetPrepairingData.DataType.PAIRING_ADDRESS):
            inner_field_container_mixin.data = cls.DataDetailsPairingAddress.fromHexList(
                inner_field_container_mixin.data)
        else:
            inner_field_container_mixin.data = cls.DataDetailsEquadAttributes.fromHexList(
                inner_field_container_mixin.data)
        # end if
        return inner_field_container_mixin
    # end def fromHexList
# end class GetPrepairingDataResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
