#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.changehost
:brief: HID++ 2.0 ``ChangeHost`` command interface definition
:author: Kevin Dayet <kdayet@logitech.com>
:date: 2021/12/15
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
class ChangeHost(HidppMessage):
    """
    ChangeHost implementation class
    """

    FEATURE_ID = 0x1814
    MAX_FUNCTION_INDEX = 3

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
# end class ChangeHost


class ChangeHostModel(FeatureModel):
    """
    Define ``ChangeHost`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """

        # Function index
        GET_HOST_INFO = 0
        SET_CURRENT_HOST = 1
        GET_COOKIES = 2
        SET_COOKIE = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ChangeHost`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_HOST_INFO: {
                    "request": GetHostInfoV0,
                    "response": GetHostInfoV0Response
                },
                cls.INDEX.SET_CURRENT_HOST: {
                    "request": SetCurrentHost,
                    "response": SetCurrentHostResponse
                },
                cls.INDEX.GET_COOKIES: {
                    "request": GetCookies,
                    "response": GetCookiesResponse
                },
                cls.INDEX.SET_COOKIE: {
                    "request": SetCookie,
                    "response": SetCookieResponse
                }
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_HOST_INFO: {
                    "request": GetHostInfoV1,
                    "response": GetHostInfoV1Response
                },
                cls.INDEX.SET_CURRENT_HOST: {
                    "request": SetCurrentHost,
                    "response": SetCurrentHostResponse
                },
                cls.INDEX.GET_COOKIES: {
                    "request": GetCookies,
                    "response": GetCookiesResponse
                },
                cls.INDEX.SET_COOKIE: {
                    "request": SetCookie,
                    "response": SetCookieResponse
                }
            }
        }

        return {
            "feature_base": ChangeHost,
            "versions": {
                ChangeHostV0.VERSION: {
                    "main_cls": ChangeHostV0,
                    "api": function_map_v0
                },
                ChangeHostV1.VERSION: {
                    "main_cls": ChangeHostV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class ChangeHostModel


class ChangeHostFactory(FeatureFactory):
    """
    Get ``ChangeHost`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ChangeHost`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ChangeHostInterface``
        """
        return ChangeHostModel.get_main_cls(version)()
    # end def create
# end class ChangeHostFactory


class ChangeHostInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ChangeHost`` classes
    """

    def __init__(self):
        # Requests
        self.get_host_info_cls = None
        self.set_current_host_cls = None
        self.get_cookies_cls = None
        self.set_cookie_cls = None

        # Responses
        self.get_host_info_response_cls = None
        self.set_current_host_response_cls = None
        self.get_cookies_response_cls = None
        self.set_cookie_response_cls = None
    # end def __init__
# end class ChangeHostInterface


class ChangeHostV0(ChangeHostInterface):
    """
    Define ``ChangeHostV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getHostInfo() -> nbHost, currHost

    [1] setCurrentHost(hostIndex) -> None

    [2] getCookies() -> cookies

    [3] setCookie(hostIndex, cookie) -> None
    """
    VERSION = 0

    def __init__(self):
        super().__init__()
        index = ChangeHostModel.INDEX

        # Requests
        self.get_host_info_cls = ChangeHostModel.get_request_cls(
            self.VERSION, index.GET_HOST_INFO)
        self.set_current_host_cls = ChangeHostModel.get_request_cls(
            self.VERSION, index.SET_CURRENT_HOST)
        self.get_cookies_cls = ChangeHostModel.get_request_cls(
            self.VERSION, index.GET_COOKIES)
        self.set_cookie_cls = ChangeHostModel.get_request_cls(
            self.VERSION, index.SET_COOKIE)

        # Responses
        self.get_host_info_response_cls = ChangeHostModel.get_response_cls(
            self.VERSION, index.GET_HOST_INFO)
        self.set_current_host_response_cls = ChangeHostModel.get_response_cls(
            self.VERSION, index.SET_CURRENT_HOST)
        self.get_cookies_response_cls = ChangeHostModel.get_response_cls(
            self.VERSION, index.GET_COOKIES)
        self.set_cookie_response_cls = ChangeHostModel.get_response_cls(
            self.VERSION, index.SET_COOKIE)
    # end def __init__

    def get_max_function_index(self):
        # See ``ChangeHostInterface.get_max_function_index``
        return ChangeHostModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ChangeHostV0


class ChangeHostV1(ChangeHostV0):
    """
    Define ``ChangeHostV1`` feature

    This feature provides model and unit specific information for version 1

    [0] getHostInfo() -> nbHost, currHost, rsv, flags
    """

    VERSION = 1
# end class ChangeHostV1


class ShortEmptyPacketDataFormat(ChangeHost):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetHostInfo
        - GetCookies

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ChangeHost.FID):
        # See ``ChangeHost.FID``
        PADDING = ChangeHost.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ChangeHost.LEN):
        # See ``ChangeHost.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ChangeHost.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ChangeHost.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(ChangeHost):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetCurrentHostResponse
        - SetCookieResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ChangeHost.FID):
        # See ``ChangeHost.FID``
        PADDING = ChangeHost.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ChangeHost.LEN):
        # See ``ChangeHost.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ChangeHost.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ChangeHost.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class GetHostInfoV0(ShortEmptyPacketDataFormat):
    """
    Define ``GetHostInfo`` implementation class for version 0
    Get info on the host implementation
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
                         functionIndex=GetHostInfoV0Response.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetHostInfoV0


class GetHostInfoV1(ShortEmptyPacketDataFormat):
    """
    Define ``GetHostInfo`` implementation class for version 1
    Get info on the host implementation
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
                         functionIndex=GetHostInfoV1Response.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetHostInfoV1


class GetHostInfoV0Response(ChangeHost):
    """
    Define ``GetHostInfoResponse`` implementation class for version 0
    Get info on the host implementation

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    nbHost                        8
    currHost                      8
    Padding                       112
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetHostInfoV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ChangeHost.FID):
        """
        Define field identifier(s)
        """

        NB_HOST = ChangeHost.FID.SOFTWARE_ID - 1
        CURR_HOST = NB_HOST - 1
        PADDING = CURR_HOST - 1
    # end class FID

    class LEN(ChangeHost.LEN):
        """
        Define field length(s)
        """

        NB_HOST = 0x8
        CURR_HOST = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = ChangeHost.FIELDS + (
        BitField(fid=FID.NB_HOST, length=LEN.NB_HOST,
                 title="NB_HOST", name="nb_host",
                 checks=(CheckHexList(LEN.NB_HOST // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURR_HOST, length=LEN.CURR_HOST,
                 title="Current Host", name="curr_host",
                 checks=(CheckHexList(LEN.CURR_HOST // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ChangeHost.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nb_host, curr_host, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param nb_host: number of hosts
        :type nb_host: ``int`` or ``HexList``
        :param curr_host: current host
        :type curr_host: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.nb_host = nb_host
        self.curr_host = curr_host
    # end def __init__
# end class GetHostInfoV0Response


class GetHostInfoV1Response(GetHostInfoV0Response):
    """
    Define ``GetHostInfoResponse`` implementation class for version 1
    Get info on the host implementation

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    nbHost                        8
    currHost                      8
    rsv                           7
    flags                         1
    Padding                       104
    ============================  ==========
    """

    REQUEST_LIST = (GetHostInfoV1,)
    VERSION = (1,)

    class FID(GetHostInfoV0Response.FID):
        # See ``GetHostInfoV0Response.FID``
        RSV = GetHostInfoV0Response.FID.CURR_HOST - 1
        FLAGS = RSV - 1
        PADDING = FLAGS - 1
    # end class FID

    class LEN(GetHostInfoV0Response.LEN):
        # See ``GetHostInfoV0Response.LEN``
        RSV = 0x7
        FLAGS = 0x1
        PADDING = 0x68
    # end class LEN

    FIELDS = GetHostInfoV0Response.FIELDS[:-1] + (
        BitField(fid=FID.RSV, length=LEN.RSV,
                 title="Reserved", name="rsv",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.RSV) - 1),)),
        BitField(fid=FID.FLAGS, length=LEN.FLAGS,
                 title="Flags", name="flags",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.FLAGS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ChangeHost.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nb_host, curr_host, rsv, flags, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param nb_host: number of hosts
        :type nb_host: ``int`` or ``HexList``
        :param curr_host: current host
        :type curr_host: ``int`` or ``HexList``
        :param rsv: reserved bits
        :type rsv: ``int`` or ``HexList``
        :param flags: flags
        :type flags: ``bool`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         nb_host=nb_host, curr_host=curr_host,
                         **kwargs)

        self.rsv = rsv
        self.flags = flags
    # end def __init__
# end class GetHostInfoV1Response


class SetCurrentHost(ChangeHost):
    """
    Define ``SetCurrentHost`` implementation class for versions 0 & 1
    Set the current host; no return, since, if successful, the device will most probably reset

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    hostIndex                     8
    Padding                       16
    ============================  ==========
    """

    class FID(ChangeHost.FID):
        """
        Define field identifier(s)
        """
        HOST_INDEX = ChangeHost.FID.SOFTWARE_ID - 1
        PADDING = HOST_INDEX - 1
    # end class FID

    class LEN(ChangeHost.LEN):
        """
        Define field length(s)
        """
        HOST_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ChangeHost.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="Host Index", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ChangeHost.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: index of host
        :type host_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetCurrentHostResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.host_index = host_index
    # end def __init__
# end class SetCurrentHost


class SetCurrentHostResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetCurrentHostResponse`` implementation class for versions 0 & 1
    Set the current host; no return, since, if successful, the device will most probably reset
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCurrentHost,)
    VERSION = (0,1,)
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
# end class SetCurrentHostResponse


class GetCookies(ShortEmptyPacketDataFormat):
    """
    Define ``GetCookies`` implementation class for versions 0 & 1
    Get the data byte for each host
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
                         functionIndex=GetCookiesResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCookies


class GetCookiesResponse(ChangeHost):
    """
    Define ``GetCookiesResponse`` implementation class for versions 0 & 1
    Get the data byte for each host

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    cookies                       128
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCookies,)
    VERSION = (0,1,)
    FUNCTION_INDEX = 2

    class FID(ChangeHost.FID):
        """
        Define field identifier(s)
        """

        COOKIES = ChangeHost.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ChangeHost.LEN):
        """
        Define field length(s)
        """

        COOKIES = 0x80
    # end class LEN

    FIELDS = ChangeHost.FIELDS + (
        BitField(fid=FID.COOKIES, length=LEN.COOKIES,
                 title="Cookies", name="cookies",
                 checks=(CheckHexList(LEN.COOKIES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COOKIES) - 1),)),
    )

    def __init__(self, device_index, feature_index, cookies, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param cookies: cookie values for each host
        :type cookies: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.cookies = cookies
    # end def __init__
# end class GetCookiesResponse


class SetCookie(ChangeHost):
    """
    Define ``SetCookie`` implementation class for versions 0 & 1
    Write the specified cookie

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    hostIndex                     8
    cookie                        8
    Padding                       8
    ============================  ==========
    """

    class FID(ChangeHost.FID):
        """
        Define field identifier(s)
        """

        HOST_INDEX = ChangeHost.FID.SOFTWARE_ID - 1
        COOKIE = HOST_INDEX - 1
        PADDING = COOKIE - 1
    # end class FID

    class LEN(ChangeHost.LEN):
        """
        Define field length(s)
        """

        HOST_INDEX = 0x8
        COOKIE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = ChangeHost.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="Host Index", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),)),
        BitField(fid=FID.COOKIE, length=LEN.COOKIE,
                 title="Cookie", name="cookie",
                 checks=(CheckHexList(LEN.COOKIE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ChangeHost.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, cookie, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param host_index: index of host
        :type host_index: ``int`` or ``HexList``
        :param cookie: cookie value for host
        :type cookie: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetCookieResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.host_index = host_index
        self.cookie = cookie
    # end def __init__
# end class SetCookie


class SetCookieResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetCookieResponse`` implementation class for versions 0 & 1
    Write the specified cookie
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetCookie,)
    VERSION = (0,1,)
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
# end class SetCookieResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
