#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.extendedadjustablereportrate
:brief: HID++ 2.0 ``ExtendedAdjustableReportRate`` command interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/05/11
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
class ExtendedAdjustableReportRate(HidppMessage):
    """
    This feature is used to set the report rate by connection type.
    """

    FEATURE_ID = 0x8061
    MAX_FUNCTION_INDEX = 3

    class RATE:
        _125_Hz = 0  # 8ms
        _250_Hz = 1  # 4ms
        _500_Hz = 2  # 2ms
        _1_KHz = 3  # 1ms
        _2_KHz = 4  # 500us
        _4_KHz = 5  # 250us
        _8_KHz = 6  # 125us
    # end class RATE

    class ConnectionType:
        """
        Connection type indexes
        """
        WIRED = 0
        GAMING_WIRELESS = 1
    # end class ConnectionType

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

    class ReportRateList(BitFieldContainerMixin):
        """
        Define ``ReportRateList`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved 0                    9
        Rate 8KHz                     1
        Rate 4KHz                     1
        Rate 2KHz                     1
        Rate 1KHz                     1
        Rate 500Hz                    1
        Rate 250Hz                    1
        Rate 125Hz                    1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED_0 = 0xFF
            RATE_8KHZ = RESERVED_0 - 1
            RATE_4KHZ = RATE_8KHZ - 1
            RATE_2KHZ = RATE_4KHZ - 1
            RATE_1KHZ = RATE_2KHZ - 1
            RATE_500HZ = RATE_1KHZ - 1
            RATE_250HZ = RATE_500HZ - 1
            RATE_125HZ = RATE_250HZ - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED_0 = 0x9
            RATE_8KHZ = 0x1
            RATE_4KHZ = 0x1
            RATE_2KHZ = 0x1
            RATE_1KHZ = 0x1
            RATE_500HZ = 0x1
            RATE_250HZ = 0x1
            RATE_125HZ = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED_0 = 0x0
            RATE_8KHZ = 0x0
            RATE_4KHZ = 0x0
            RATE_2KHZ = 0x0
            RATE_1KHZ = 0x0
            RATE_500HZ = 0x0
            RATE_250HZ = 0x0
            RATE_125HZ = 0x0
        # end class DEFAULT

        class POS(object):
            """
            Report Rate bit field position
            """
            RATE_8KHZ = 6
            RATE_4KHZ = 5
            RATE_2KHZ = 4
            RATE_1KHZ = 3
            RATE_500HZ = 2
            RATE_250HZ = 1
            RATE_125HZ = 0
        # end class POS

        FIELDS = (
            BitField(fid=FID.RESERVED_0, length=LEN.RESERVED_0,
                     title="Reserved0", name="reserved_0",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED_0) - 1),),
                     default_value=DEFAULT.RESERVED_0),
            BitField(fid=FID.RATE_8KHZ, length=LEN.RATE_8KHZ,
                     title="Rate8khz", name="rate_8khz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_8KHZ) - 1),),
                     default_value=DEFAULT.RATE_8KHZ),
            BitField(fid=FID.RATE_4KHZ, length=LEN.RATE_4KHZ,
                     title="Rate4khz", name="rate_4khz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_4KHZ) - 1),),
                     default_value=DEFAULT.RATE_4KHZ),
            BitField(fid=FID.RATE_2KHZ, length=LEN.RATE_2KHZ,
                     title="Rate2khz", name="rate_2khz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_2KHZ) - 1),),
                     default_value=DEFAULT.RATE_2KHZ),
            BitField(fid=FID.RATE_1KHZ, length=LEN.RATE_1KHZ,
                     title="Rate1khz", name="rate_1khz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_1KHZ) - 1),),
                     default_value=DEFAULT.RATE_1KHZ),
            BitField(fid=FID.RATE_500HZ, length=LEN.RATE_500HZ,
                     title="Rate500hz", name="rate_500hz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_500HZ) - 1),),
                     default_value=DEFAULT.RATE_500HZ),
            BitField(fid=FID.RATE_250HZ, length=LEN.RATE_250HZ,
                     title="Rate250hz", name="rate_250hz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_250HZ) - 1),),
                     default_value=DEFAULT.RATE_250HZ),
            BitField(fid=FID.RATE_125HZ, length=LEN.RATE_125HZ,
                     title="Rate125hz", name="rate_125hz",
                     checks=(CheckInt(0, pow(2, LEN.RATE_125HZ) - 1),),
                     default_value=DEFAULT.RATE_125HZ),
        )
    # end class ReportRateList
# end class ExtendedAdjustableReportRate


class ExtendedAdjustableReportRateModel(FeatureModel):
    """
    Define ``ExtendedAdjustableReportRate`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_DEVICE_CAPABILITIES = 0
        GET_ACTUAL_REPORT_RATE_LIST = 1
        GET_REPORT_RATE = 2
        SET_REPORT_RATE = 3

        # Event index
        REPORT_RATE_INFO = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ExtendedAdjustableReportRate`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_DEVICE_CAPABILITIES: {
                    "request": GetDeviceCapabilities,
                    "response": GetDeviceCapabilitiesResponse
                },
                cls.INDEX.GET_ACTUAL_REPORT_RATE_LIST: {
                    "request": GetActualReportRateList,
                    "response": GetActualReportRateListResponse
                },
                cls.INDEX.GET_REPORT_RATE: {
                    "request": GetReportRate,
                    "response": GetReportRateResponse
                },
                cls.INDEX.SET_REPORT_RATE: {
                    "request": SetReportRate,
                    "response": SetReportRateResponse
                }
            },
            "events": {
                cls.INDEX.REPORT_RATE_INFO: {"report": ReportRateInfoEvent}
            }
        }

        return {
            "feature_base": ExtendedAdjustableReportRate,
            "versions": {
                ExtendedAdjustableReportRateV0.VERSION: {
                    "main_cls": ExtendedAdjustableReportRateV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class ExtendedAdjustableReportRateModel


class ExtendedAdjustableReportRateFactory(FeatureFactory):
    """
    Get ``ExtendedAdjustableReportRate`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ExtendedAdjustableReportRate`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ExtendedAdjustableReportRateInterface``
        """
        return ExtendedAdjustableReportRateModel.get_main_cls(version)()
    # end def create
# end class ExtendedAdjustableReportRateFactory


class ExtendedAdjustableReportRateInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ExtendedAdjustableReportRate``
    """

    def __init__(self):
        # Requests
        self.get_device_capabilities_cls = None
        self.get_actual_report_rate_list_cls = None
        self.get_report_rate_cls = None
        self.set_report_rate_cls = None

        # Responses
        self.get_device_capabilities_response_cls = None
        self.get_actual_report_rate_list_response_cls = None
        self.get_report_rate_response_cls = None
        self.set_report_rate_response_cls = None

        # Events
        self.report_rate_info_event_cls = None
    # end def __init__
# end class ExtendedAdjustableReportRateInterface


class ExtendedAdjustableReportRateV0(ExtendedAdjustableReportRateInterface):
    """
    Define ``ExtendedAdjustableReportRateV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getDeviceCapabilities(connectionType) -> reportRateList

    [1] getActualReportRateList() -> reportRateList

    [2] getReportRate(connectionType) -> reportRate

    [3] setReportRate(reportRate) -> None

    [Event 0] reportRateInfoEvent -> connectionType, reportRate
    """

    VERSION = 0

    def __init__(self):
        # See ``ExtendedAdjustableReportRate.__init__``
        super().__init__()
        index = ExtendedAdjustableReportRateModel.INDEX

        # Requests
        self.get_device_capabilities_cls = ExtendedAdjustableReportRateModel.get_request_cls(
            self.VERSION, index.GET_DEVICE_CAPABILITIES)
        self.get_actual_report_rate_list_cls = ExtendedAdjustableReportRateModel.get_request_cls(
            self.VERSION, index.GET_ACTUAL_REPORT_RATE_LIST)
        self.get_report_rate_cls = ExtendedAdjustableReportRateModel.get_request_cls(
            self.VERSION, index.GET_REPORT_RATE)
        self.set_report_rate_cls = ExtendedAdjustableReportRateModel.get_request_cls(
            self.VERSION, index.SET_REPORT_RATE)

        # Responses
        self.get_device_capabilities_response_cls = ExtendedAdjustableReportRateModel.get_response_cls(
            self.VERSION, index.GET_DEVICE_CAPABILITIES)
        self.get_actual_report_rate_list_response_cls = ExtendedAdjustableReportRateModel.get_response_cls(
            self.VERSION, index.GET_ACTUAL_REPORT_RATE_LIST)
        self.get_report_rate_response_cls = ExtendedAdjustableReportRateModel.get_response_cls(
            self.VERSION, index.GET_REPORT_RATE)
        self.set_report_rate_response_cls = ExtendedAdjustableReportRateModel.get_response_cls(
            self.VERSION, index.SET_REPORT_RATE)

        # Events
        self.report_rate_info_event_cls = ExtendedAdjustableReportRateModel.get_report_cls(
            self.VERSION, index.REPORT_RATE_INFO)
    # end def __init__

    def get_max_function_index(self):
        # See ``ExtendedAdjustableReportRateInterface.get_max_function_index``
        return ExtendedAdjustableReportRateModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ExtendedAdjustableReportRateV0


class ShortEmptyPacketDataFormat(ExtendedAdjustableReportRate):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetActualReportRateList

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        PADDING = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(ExtendedAdjustableReportRate):
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

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        PADDING = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class ConnectionInfo(ExtendedAdjustableReportRate):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetDeviceCapabilities
        - GetReportRate

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Connection Type               8
    Padding                       16
    ============================  ==========
    """

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        CONNECTION_TYPE = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
        PADDING = CONNECTION_TYPE - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        CONNECTION_TYPE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.CONNECTION_TYPE, length=LEN.CONNECTION_TYPE,
                 title="ConnectionType", name="connection_type",
                 checks=(CheckHexList(LEN.CONNECTION_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),
    )
# end class ConnectionInfo


class ReportRateInfo(ExtendedAdjustableReportRate):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetDeviceCapabilitiesResponse
        - GetActualReportRateListResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Report Rate List              16
    Padding                       112
    ============================  ==========
    """

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        REPORT_RATE_LIST = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
        PADDING = REPORT_RATE_LIST - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        REPORT_RATE_LIST = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.REPORT_RATE_LIST, length=LEN.REPORT_RATE_LIST,
                 title="ReportRateList", name="report_rate_list",
                 checks=(CheckHexList(LEN.REPORT_RATE_LIST // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REPORT_RATE_LIST) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),
    )
# end class ReportRateInfo


class GetDeviceCapabilities(ConnectionInfo):
    """
    Define ``GetDeviceCapabilities`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, connection_type, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param connection_type: Connection Type 
        :type connection_type: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetDeviceCapabilitiesResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.connection_type = connection_type
    # end def __init__
# end class GetDeviceCapabilities


class GetDeviceCapabilitiesResponse(ReportRateInfo):
    """
    Define ``GetDeviceCapabilitiesResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index,
                 rate_8khz, rate_4khz, rate_2khz, rate_1khz, rate_500hz, rate_250hz, rate_125hz,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rate_8khz: Rate 8KHz
        :type rate_8khz: ``bool`` or ``HexList``
        :param rate_4khz: Rate 4KHz
        :type rate_4khz: ``bool`` or ``HexList``
        :param rate_2khz: Rate 2KHz
        :type rate_2khz: ``bool`` or ``HexList``
        :param rate_1khz: Rate 1KHz
        :type rate_1khz: ``bool`` or ``HexList``
        :param rate_500hz: Rate 500Hz
        :type rate_500hz: ``bool`` or ``HexList``
        :param rate_250hz: Rate 250Hz
        :type rate_250hz: ``bool`` or ``HexList``
        :param rate_125hz: Rate 125Hz
        :type rate_125hz: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.report_rate_list = self.ReportRateList(rate_8khz=rate_8khz,
                                                    rate_4khz=rate_4khz,
                                                    rate_2khz=rate_2khz,
                                                    rate_1khz=rate_1khz,
                                                    rate_500hz=rate_500hz,
                                                    rate_250hz=rate_250hz,
                                                    rate_125hz=rate_125hz)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetDeviceCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.report_rate_list = cls.ReportRateList.fromHexList(
            inner_field_container_mixin.report_rate_list)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetDeviceCapabilitiesResponse


class GetActualReportRateList(ShortEmptyPacketDataFormat):
    """
    Define ``GetActualReportRateList`` implementation class for version 0
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
                         functionIndex=GetActualReportRateListResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetActualReportRateList


class GetActualReportRateListResponse(ReportRateInfo):
    """
    Define ``GetActualReportRateListResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetActualReportRateList,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index,
                 rate_8khz, rate_4khz, rate_2khz, rate_1khz, rate_500hz, rate_250hz, rate_125hz,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param rate_8khz: Rate 8KHz
        :type rate_8khz: ``bool`` or ``HexList``
        :param rate_4khz: Rate 4KHz
        :type rate_4khz: ``bool`` or ``HexList``
        :param rate_2khz: Rate 2KHz
        :type rate_2khz: ``bool`` or ``HexList``
        :param rate_1khz: Rate 1KHz
        :type rate_1khz: ``bool`` or ``HexList``
        :param rate_500hz: Rate 500Hz
        :type rate_500hz: ``bool`` or ``HexList``
        :param rate_250hz: Rate 250Hz
        :type rate_250hz: ``bool`` or ``HexList``
        :param rate_125hz: Rate 125Hz
        :type rate_125hz: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.report_rate_list = self.ReportRateList(rate_8khz=rate_8khz,
                                                    rate_4khz=rate_4khz,
                                                    rate_2khz=rate_2khz,
                                                    rate_1khz=rate_1khz,
                                                    rate_500hz=rate_500hz,
                                                    rate_250hz=rate_250hz,
                                                    rate_125hz=rate_125hz)
    # end def __init__

    @classmethod
    def fromHexList(cls, *args, **kwargs):
        """
        Parse from ``HexList`` instance

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetActualReportRateListResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.report_rate_list = cls.ReportRateList.fromHexList(
            inner_field_container_mixin.report_rate_list)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetActualReportRateListResponse


class GetReportRate(ConnectionInfo):
    """
    Define ``GetReportRate`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, connection_type, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param connection_type: Connection Type 
        :type connection_type: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetReportRateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.connection_type = connection_type
    # end def __init__
# end class GetReportRate


class GetReportRateResponse(ExtendedAdjustableReportRate):
    """
    Define ``GetReportRateResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Report Rate                   8
    Padding                       120
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetReportRate,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        REPORT_RATE = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
        PADDING = REPORT_RATE - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        REPORT_RATE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.REPORT_RATE, length=LEN.REPORT_RATE,
                 title="ReportRate", name="report_rate",
                 checks=(CheckHexList(LEN.REPORT_RATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),
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


class SetReportRate(ExtendedAdjustableReportRate):
    """
    Define ``SetReportRate`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Report Rate                   8
    Padding                       16
    ============================  ==========
    """

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        REPORT_RATE = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
        PADDING = REPORT_RATE - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        REPORT_RATE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.REPORT_RATE, length=LEN.REPORT_RATE,
                 title="ReportRate", name="report_rate",
                 checks=(CheckHexList(LEN.REPORT_RATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),
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
# end class SetReportRateResponse


class ReportRateInfoEvent(ExtendedAdjustableReportRate):
    """
    Define ``ReportRateInfoEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Connection Type               8
    Report Rate                   8
    Padding                       112
    ============================  ==========
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ExtendedAdjustableReportRate.FID):
        # See ``ExtendedAdjustableReportRate.FID``
        CONNECTION_TYPE = ExtendedAdjustableReportRate.FID.SOFTWARE_ID - 1
        REPORT_RATE = CONNECTION_TYPE - 1
        PADDING = REPORT_RATE - 1
    # end class FID

    class LEN(ExtendedAdjustableReportRate.LEN):
        # See ``ExtendedAdjustableReportRate.LEN``
        CONNECTION_TYPE = 0x8
        REPORT_RATE = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = ExtendedAdjustableReportRate.FIELDS + (
        BitField(fid=FID.CONNECTION_TYPE, length=LEN.CONNECTION_TYPE,
                 title="ConnectionType", name="connection_type",
                 checks=(CheckHexList(LEN.CONNECTION_TYPE // 8),
                         CheckByte(),)),
        BitField(fid=FID.REPORT_RATE, length=LEN.REPORT_RATE,
                 title="ReportRate", name="report_rate",
                 checks=(CheckHexList(LEN.REPORT_RATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ExtendedAdjustableReportRate.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, connection_type, report_rate, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param connection_type: Connection Type
        :type connection_type: ``int`` or ``HexList``
        :param report_rate: Report Rate
        :type report_rate: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.connection_type = connection_type
        self.report_rate = report_rate
    # end def __init__
# end class ReportRateInfoEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
