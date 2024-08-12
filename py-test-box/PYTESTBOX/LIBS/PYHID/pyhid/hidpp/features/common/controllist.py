#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.controllist
:brief: HID++ 2.0 ``ControlList`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/17
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
class ControlList(HidppMessage):
    """
    This feature provides the means to retrieve a list of all physical controls on the device, with each control
    represented by its Control ID (CID).
    """
    FEATURE_ID = 0x1B10
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class ControlList


class ControlListModel(FeatureModel):
    """
    Define ``ControlList`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_COUNT = 0
        GET_CONTROL_LIST = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ControlList`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_COUNT: {
                    "request": GetCount,
                    "response": GetCountResponse
                },
                cls.INDEX.GET_CONTROL_LIST: {
                    "request": GetControlList,
                    "response": GetControlListResponse
                }
            }
        }

        return {
            "feature_base": ControlList,
            "versions": {
                ControlListV0.VERSION: {
                    "main_cls": ControlListV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class ControlListModel


class ControlListFactory(FeatureFactory):
    """
    Get ``ControlList`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ControlList`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ControlListInterface``
        """
        return ControlListModel.get_main_cls(version)()
    # end def create
# end class ControlListFactory


class ControlListInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ControlList``
    """

    def __init__(self):
        # Requests
        self.get_count_cls = None
        self.get_control_list_cls = None

        # Responses
        self.get_count_response_cls = None
        self.get_control_list_response_cls = None
    # end def __init__
# end class ControlListInterface


class ControlListV0(ControlListInterface):
    """
    Define ``ControlListV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetCount() -> Count

    [1] GetControlList(Offset) -> Cid0, Cid1, Cid2, Cid3, Cid4, Cid5, Cid6, Cid7
    """
    VERSION = 0

    def __init__(self):
        # See ``ControlList.__init__``
        super().__init__()
        index = ControlListModel.INDEX

        # Requests
        self.get_count_cls = ControlListModel.get_request_cls(
            self.VERSION, index.GET_COUNT)
        self.get_control_list_cls = ControlListModel.get_request_cls(
            self.VERSION, index.GET_CONTROL_LIST)

        # Responses
        self.get_count_response_cls = ControlListModel.get_response_cls(
            self.VERSION, index.GET_COUNT)
        self.get_control_list_response_cls = ControlListModel.get_response_cls(
            self.VERSION, index.GET_CONTROL_LIST)
    # end def __init__

    def get_max_function_index(self):
        # See ``ControlListInterface.get_max_function_index``
        return ControlListModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ControlListV0


class ShortEmptyPacketDataFormat(ControlList):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCount

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ControlList.FID):
        # See ``ControlList.FID``
        PADDING = ControlList.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ControlList.LEN):
        # See ``ControlList.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ControlList.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ControlList.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class GetCount(ShortEmptyPacketDataFormat):
    """
    Define ``GetCount`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetCountResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCount


class GetCountResponse(ControlList):
    """
    Define ``GetCountResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Count                         8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCount,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ControlList.FID):
        # See ``ControlList.FID``
        COUNT = ControlList.FID.SOFTWARE_ID - 1
        PADDING = COUNT - 1
    # end class FID

    class LEN(ControlList.LEN):
        # See ``ControlList.LEN``
        COUNT = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = ControlList.FIELDS + (
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ControlList.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.count = count
    # end def __init__
# end class GetCountResponse


class GetControlList(ControlList):
    """
    Define ``GetControlList`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Offset                        8
    Padding                       16
    ============================  ==========
    """

    class FID(ControlList.FID):
        # See ``ControlList.FID``
        OFFSET = ControlList.FID.SOFTWARE_ID - 1
        PADDING = OFFSET - 1
    # end class FID

    class LEN(ControlList.LEN):
        # See ``ControlList.LEN``
        OFFSET = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ControlList.FIELDS + (
        BitField(fid=FID.OFFSET, length=LEN.OFFSET,
                 title="Offset", name="offset",
                 checks=(CheckHexList(LEN.OFFSET // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ControlList.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, offset, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param offset: Offset
        :type offset: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetControlListResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.offset = offset
    # end def __init__
# end class GetControlList


class GetControlListResponse(ControlList):
    """
    Define ``GetControlListResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Cid 0                         16
    Cid 1                         16
    Cid 2                         16
    Cid 3                         16
    Cid 4                         16
    Cid 5                         16
    Cid 6                         16
    Cid 7                         16
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetControlList,)
    VERSION = (0,)
    FUNCTION_INDEX = 1
    NUM_OF_CID_PER_PACKET = 8

    class FID(ControlList.FID):
        # See ``ControlList.FID``
        CID_0 = ControlList.FID.SOFTWARE_ID - 1
        CID_1 = CID_0 - 1
        CID_2 = CID_1 - 1
        CID_3 = CID_2 - 1
        CID_4 = CID_3 - 1
        CID_5 = CID_4 - 1
        CID_6 = CID_5 - 1
        CID_7 = CID_6 - 1
    # end class FID

    class LEN(ControlList.LEN):
        # See ``ControlList.LEN``
        CID_0 = 0x10
        CID_1 = 0x10
        CID_2 = 0x10
        CID_3 = 0x10
        CID_4 = 0x10
        CID_5 = 0x10
        CID_6 = 0x10
        CID_7 = 0x10
    # end class LEN

    FIELDS = ControlList.FIELDS + (
        BitField(fid=FID.CID_0, length=LEN.CID_0,
                 title="Cid0", name="cid_0",
                 checks=(CheckHexList(LEN.CID_0 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_0) - 1),)),
        BitField(fid=FID.CID_1, length=LEN.CID_1,
                 title="Cid1", name="cid_1",
                 checks=(CheckHexList(LEN.CID_1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_1) - 1),)),
        BitField(fid=FID.CID_2, length=LEN.CID_2,
                 title="Cid2", name="cid_2",
                 checks=(CheckHexList(LEN.CID_2 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_2) - 1),)),
        BitField(fid=FID.CID_3, length=LEN.CID_3,
                 title="Cid3", name="cid_3",
                 checks=(CheckHexList(LEN.CID_3 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_3) - 1),)),
        BitField(fid=FID.CID_4, length=LEN.CID_4,
                 title="Cid4", name="cid_4",
                 checks=(CheckHexList(LEN.CID_4 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_4) - 1),)),
        BitField(fid=FID.CID_5, length=LEN.CID_5,
                 title="Cid5", name="cid_5",
                 checks=(CheckHexList(LEN.CID_5 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_5) - 1),)),
        BitField(fid=FID.CID_6, length=LEN.CID_6,
                 title="Cid6", name="cid_6",
                 checks=(CheckHexList(LEN.CID_6 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_6) - 1),)),
        BitField(fid=FID.CID_7, length=LEN.CID_7,
                 title="Cid7", name="cid_7",
                 checks=(CheckHexList(LEN.CID_7 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CID_7) - 1),)),
    )

    def __init__(self, device_index, feature_index, cid_0, cid_1, cid_2, cid_3, cid_4, cid_5, cid_6, cid_7, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param cid_0: Cid 0
        :type cid_0: ``int | HexList``
        :param cid_1: Cid 1
        :type cid_1: ``int | HexList``
        :param cid_2: Cid 2
        :type cid_2: ``int | HexList``
        :param cid_3: Cid 3
        :type cid_3: ``int | HexList``
        :param cid_4: Cid 4
        :type cid_4: ``int | HexList``
        :param cid_5: Cid 5
        :type cid_5: ``int | HexList``
        :param cid_6: Cid 6
        :type cid_6: ``int | HexList``
        :param cid_7: Cid 7
        :type cid_7: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.cid_0 = cid_0
        self.cid_1 = cid_1
        self.cid_2 = cid_2
        self.cid_3 = cid_3
        self.cid_4 = cid_4
        self.cid_5 = cid_5
        self.cid_6 = cid_6
        self.cid_7 = cid_7
    # end def __init__
# end class GetControlListResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
