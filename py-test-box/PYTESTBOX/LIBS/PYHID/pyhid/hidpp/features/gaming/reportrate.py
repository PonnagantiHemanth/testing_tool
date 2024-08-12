#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.reportrate
:brief: HID++ 2.0 ``ReportRate`` command interface definition
:author: Suresh Thiyagarajan <sthiyagarajan@logitech.com>
:date: 2022/04/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ReportRate(HidppMessage):
    """
    Define feature to change the device report rate
    """

    FEATURE_ID = 0x8060
    MAX_FUNCTION_INDEX = 2

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
# end class ReportRate


class ReportRateModel(FeatureModel):
    """
    Define ``ReportRate`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_REPORT_RATE_LIST = 0
        GET_REPORT_RATE = 1
        SET_REPORT_RATE = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ReportRate`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_REPORT_RATE_LIST: {
                    "request": GetReportRateList,
                    "response": GetReportRateListResponse
                },
                cls.INDEX.GET_REPORT_RATE: {
                    "request": GetReportRate,
                    "response": GetReportRateResponse
                },
                cls.INDEX.SET_REPORT_RATE: {
                    "request": SetReportRate,
                    "response": SetReportRateResponse
                }
            }
        }

        return {
            "feature_base": ReportRate,
            "versions": {
                ReportRateV0.VERSION: {
                    "main_cls": ReportRateV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class ReportRateModel


class ReportRateFactory(FeatureFactory):
    """
    Get ``ReportRate`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ReportRate`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ReportRateInterface``
        """
        return ReportRateModel.get_main_cls(version)()
    # end def create
# end class ReportRateFactory


class ReportRateInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ReportRate``
    """

    def __init__(self):
        # Requests
        self.get_report_rate_list_cls = None
        self.get_report_rate_cls = None
        self.set_report_rate_cls = None

        # Responses
        self.get_report_rate_list_response_cls = None
        self.get_report_rate_response_cls = None
        self.set_report_rate_response_cls = None
    # end def __init__
# end class ReportRateInterface


class ReportRateV0(ReportRateInterface):
    """
    Define ``ReportRateV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getReportRateList() -> reportRateList

    [1] getReportRate() -> reportRate

    [2] setReportRate(reportRate) -> None
    """

    VERSION = 0

    def __init__(self):
        # See ``ReportRate.__init__``
        super().__init__()
        index = ReportRateModel.INDEX

        # Requests
        self.get_report_rate_list_cls = ReportRateModel.get_request_cls(
            self.VERSION, index.GET_REPORT_RATE_LIST)
        self.get_report_rate_cls = ReportRateModel.get_request_cls(
            self.VERSION, index.GET_REPORT_RATE)
        self.set_report_rate_cls = ReportRateModel.get_request_cls(
            self.VERSION, index.SET_REPORT_RATE)

        # Responses
        self.get_report_rate_list_response_cls = ReportRateModel.get_response_cls(
            self.VERSION, index.GET_REPORT_RATE_LIST)
        self.get_report_rate_response_cls = ReportRateModel.get_response_cls(
            self.VERSION, index.GET_REPORT_RATE)
        self.set_report_rate_response_cls = ReportRateModel.get_response_cls(
            self.VERSION, index.SET_REPORT_RATE)
    # end def __init__

    def get_max_function_index(self):
        # See ``ReportRateInterface.get_max_function_index``
        return ReportRateModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ReportRateV0


class ShortEmptyPacketDataFormat(ReportRate):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetReportRateList
        - GetReportRate

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ReportRate.FID):
        # See ``ReportRate.FID``
        PADDING = ReportRate.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ReportRate.LEN):
        # See ``ReportRate.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ReportRate.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ReportRate.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(ReportRate):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetReportRateResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ReportRate.FID):
        # See ``ReportRate.FID``
        PADDING = ReportRate.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ReportRate.LEN):
        # See ``ReportRate.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ReportRate.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ReportRate.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetReportRateList(ShortEmptyPacketDataFormat):
    """
    Define ``GetReportRateList`` implementation class for version 0
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
                         functionIndex=GetReportRateListResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetReportRateList


class GetReportRateListResponse(ReportRate):
    """
    Define ``GetReportRateListResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportRateList                8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetReportRateList,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ReportRate.FID):
        # See ``ReportRate.FID``
        REPORT_RATE_LIST = ReportRate.FID.SOFTWARE_ID - 1
        PADDING = REPORT_RATE_LIST - 1
    # end class FID

    class LEN(ReportRate.LEN):
        # See ``ReportRate.LEN``
        REPORT_RATE_LIST = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = ReportRate.FIELDS + (
        BitField(fid=FID.REPORT_RATE_LIST, length=LEN.REPORT_RATE_LIST,
                 title="ReportRateList", name="report_rate_list",
                 checks=(CheckHexList(LEN.REPORT_RATE_LIST // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ReportRate.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, report_rate_list, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param report_rate_list: Report Rate List
        :type report_rate_list: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.report_rate_list = report_rate_list
    # end def __init__
# end class GetReportRateListResponse


class GetReportRate(ShortEmptyPacketDataFormat):
    """
    Define ``GetReportRate`` implementation class for version 0
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
                         functionIndex=GetReportRateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetReportRate


class GetReportRateResponse(ReportRate):
    """
    Define ``GetReportRateResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportRate                    8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetReportRate,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ReportRate.FID):
        # See ``ReportRate.FID``
        REPORT_RATE = ReportRate.FID.SOFTWARE_ID - 1
        PADDING = REPORT_RATE - 1
    # end class FID

    class LEN(ReportRate.LEN):
        # See ``ReportRate.LEN``
        REPORT_RATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = ReportRate.FIELDS + (
        BitField(fid=FID.REPORT_RATE, length=LEN.REPORT_RATE,
                 title="ReportRate", name="report_rate",
                 checks=(CheckHexList(LEN.REPORT_RATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ReportRate.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, report_rate, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.report_rate = report_rate
    # end def __init__
# end class GetReportRateResponse


class SetReportRate(ReportRate):
    """
    Define ``SetReportRate`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportRate                    8
    Padding                       16
    ============================  ==========
    """

    class FID(ReportRate.FID):
        # See ``ReportRate.FID``
        REPORT_RATE = ReportRate.FID.SOFTWARE_ID - 1
        PADDING = REPORT_RATE - 1
    # end class FID

    class LEN(ReportRate.LEN):
        # See ``ReportRate.LEN``
        REPORT_RATE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ReportRate.FIELDS + (
        BitField(fid=FID.REPORT_RATE, length=LEN.REPORT_RATE,
                 title="ReportRate", name="report_rate",
                 checks=(CheckHexList(LEN.REPORT_RATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ReportRate.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, report_rate, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetReportRateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.report_rate = report_rate
    # end def __init__
# end class SetReportRate


class SetReportRateResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetReportRateResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetReportRate,)
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
# end class SetReportRateResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
