#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.passwordauthentication
:brief: HID++ 2.0 ``PasswordAuthentication`` command interface definition
:author: Anil Gadad <agadad@logitech.com>
:date: 2021/10/27
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
class PasswordAuthentication(HidppMessage):
    """
    Authentication feature based on a simple password.
    """
    FEATURE_ID = 0x1602
    MAX_FUNCTION_INDEX_V0 = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        # noinspection PyTypeChecker
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class PasswordAuthentication


# noinspection DuplicatedCode
class PasswordAuthenticationModel(FeatureModel):
    """
    Define ``PasswordAuthentication`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        START_SESSION = 0
        END_SESSION = 1
        PASSWD0 = 2
        PASSWD1 = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``PasswordAuthentication`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.START_SESSION: {
                    "request": StartSession,
                    "response": StartSessionResponse
                },
                cls.INDEX.END_SESSION: {
                    "request": EndSession,
                    "response": EndSessionResponse
                },
                cls.INDEX.PASSWD0: {
                    "request": Passwd0,
                    "response": Passwd0Response
                },
                cls.INDEX.PASSWD1: {
                    "request": Passwd1,
                    "response": Passwd1Response
                }
            }
        }

        return {
            "feature_base": PasswordAuthentication,
            "versions": {
                PasswordAuthenticationV0.VERSION: {
                    "main_cls": PasswordAuthenticationV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class PasswordAuthenticationModel


class PasswordAuthenticationFactory(FeatureFactory):
    """
    Get ``PasswordAuthentication`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``PasswordAuthentication`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``PasswordAuthenticationInterface``
        """
        return PasswordAuthenticationModel.get_main_cls(version)()
    # end def create
# end class PasswordAuthenticationFactory


class PasswordAuthenticationInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``PasswordAuthentication``
    """

    def __init__(self):
        # Requests
        self.start_session_cls = None
        self.end_session_cls = None
        self.passwd0_cls = None
        self.passwd1_cls = None

        # Responses
        self.start_session_response_cls = None
        self.end_session_response_cls = None
        self.passwd0_response_cls = None
        self.passwd1_response_cls = None
    # end def __init__
# end class PasswordAuthenticationInterface


class PasswordAuthenticationV0(PasswordAuthenticationInterface):
    """
    Define ``PasswordAuthenticationV0`` feature

    This feature provides model and unit specific information for version 0

    [0] startSession(accountName) -> longPassword, fullAuthentication, constantCredentials

    [1] endSession(accountName) -> None

    [2] passwd0(passwd) -> status

    [3] passwd1(passwd) -> status
    """
    VERSION = 0

    def __init__(self):
        # See ``PasswordAuthentication.__init__``
        super().__init__()
        index = PasswordAuthenticationModel.INDEX

        # Requests
        self.start_session_cls = PasswordAuthenticationModel.get_request_cls(
            self.VERSION, index.START_SESSION)
        self.end_session_cls = PasswordAuthenticationModel.get_request_cls(
            self.VERSION, index.END_SESSION)
        self.passwd0_cls = PasswordAuthenticationModel.get_request_cls(
            self.VERSION, index.PASSWD0)
        self.passwd1_cls = PasswordAuthenticationModel.get_request_cls(
            self.VERSION, index.PASSWD1)

        # Responses
        self.start_session_response_cls = PasswordAuthenticationModel.get_response_cls(
            self.VERSION, index.START_SESSION)
        self.end_session_response_cls = PasswordAuthenticationModel.get_response_cls(
            self.VERSION, index.END_SESSION)
        self.passwd0_response_cls = PasswordAuthenticationModel.get_response_cls(
            self.VERSION, index.PASSWD0)
        self.passwd1_response_cls = PasswordAuthenticationModel.get_response_cls(
            self.VERSION, index.PASSWD1)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``PasswordAuthenticationInterface.get_max_function_index``
        return PasswordAuthenticationModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class PasswordAuthenticationV0


class LongEmptyPacketDataFormat(PasswordAuthentication):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - EndSessionResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(PasswordAuthentication.FID):
        # See ``PasswordAuthentication.FID``
        PADDING = PasswordAuthentication.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PasswordAuthentication.LEN):
        # See ``PasswordAuthentication.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = PasswordAuthentication.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PasswordAuthentication.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class Session(PasswordAuthentication):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - StartSession
        - EndSession

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Account Name                  128
    ============================  ==========
    """

    class FID(PasswordAuthentication.FID):
        # See ``PasswordAuthentication.FID``
        ACCOUNT_NAME = PasswordAuthentication.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PasswordAuthentication.LEN):
        # See ``PasswordAuthentication.LEN``
        ACCOUNT_NAME = 0x80
        NAME_MAX_SIZE = 0x80
        NAME_MIN_SIZE = 0x08
    # end class LEN

    FIELDS = PasswordAuthentication.FIELDS + (
        BitField(fid=FID.ACCOUNT_NAME, length=LEN.ACCOUNT_NAME,
                 title="AccountName", name="account_name",
                 checks=(CheckHexList(max_length=(LEN.NAME_MAX_SIZE // 8), min_length=(LEN.NAME_MIN_SIZE // 8)),), ),
    )
# end class Session


class Password(PasswordAuthentication):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - Passwd0
        - Passwd1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Passwd                        128
    ============================  ==========
    """

    class FID(PasswordAuthentication.FID):
        # See ``PasswordAuthentication.FID``
        PASSWD = PasswordAuthentication.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PasswordAuthentication.LEN):
        # See ``PasswordAuthentication.LEN``
        PASSWD = 0x80
    # end class LEN

    FIELDS = PasswordAuthentication.FIELDS + (
        BitField(fid=FID.PASSWD, length=LEN.PASSWD,
                 title="Passwd", name="passwd",
                 checks=(CheckHexList(LEN.PASSWD // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PASSWD) - 1),)),
    )
# end class Password


class PasswordResponse(PasswordAuthentication):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - Passwd0Response
        - Passwd1Response

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Status                        8
    Padding                       120
    ============================  ==========
    """

    class FID(PasswordAuthentication.FID):
        # See ``PasswordAuthentication.FID``
        STATUS = PasswordAuthentication.FID.SOFTWARE_ID - 1
        PADDING = STATUS - 1
    # end class FID

    class LEN(PasswordAuthentication.LEN):
        # See ``PasswordAuthentication.LEN``
        STATUS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = PasswordAuthentication.FIELDS + (
        BitField(fid=FID.STATUS, length=LEN.STATUS,
                 title="Status", name="status",
                 checks=(CheckHexList(LEN.STATUS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PasswordAuthentication.DEFAULT.PADDING),
    )
# end class PasswordResponse


class StartSession(Session):
    """
    Define ``StartSession`` implementation class
    """

    def __init__(self, device_index, feature_index, account_name, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param account_name: Account name, expressed as UTF-8 string (except 0)
        :type account_name: ``str | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=StartSessionResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        account_name = HexList.fromString(account_name) if isinstance(account_name, str) else account_name
        account_name_copy = HexList(account_name.copy())
        account_name_copy.addPadding(
            size=self.LEN.ACCOUNT_NAME // 8,
            pattern=self.DEFAULT.PADDING, fromLeft=False)
        self.account_name = account_name_copy
    # end def __init__
# end class StartSession


class EndSession(Session):
    """
    Define ``EndSession`` implementation class
    """

    def __init__(self, device_index, feature_index, account_name, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param account_name: Account name, expressed as UTF-8 string (except 0)
        :type account_name: ``str | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=EndSessionResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        account_name = HexList.fromString(account_name) if isinstance(account_name, str) else account_name
        account_name_copy = HexList(account_name.copy())
        account_name_copy.addPadding(
            size=self.LEN.ACCOUNT_NAME // 8,
            pattern=self.DEFAULT.PADDING, fromLeft=False)
        self.account_name = account_name_copy
    # end def __init__
# end class EndSession


class Passwd0(Password):
    """
    Define ``Passwd0`` implementation class
    """

    def __init__(self, device_index, feature_index, passwd, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param passwd: Password. This parameter shall be a random binary string, except 0.
        :type passwd: ``str | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=Passwd0Response.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        passwd = HexList.fromString(passwd) if isinstance(passwd, str) else passwd
        passwd_copy = HexList(passwd.copy())
        passwd_copy.addPadding(
            size=self.LEN.PASSWD // 8,
            pattern=self.DEFAULT.PADDING, fromLeft=False)
        self.passwd = passwd_copy
    # end def __init__
# end class Passwd0


class Passwd1(Password):
    """
    Define ``Passwd1`` implementation class
    """

    def __init__(self, device_index, feature_index, passwd, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param passwd: Password. This parameter shall be a random binary string, except 0.
        :type passwd: ``str | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=Passwd1Response.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        passwd = HexList.fromString(passwd) if isinstance(passwd, str) else passwd
        passwd_copy = HexList(passwd.copy())
        passwd_copy.addPadding(
            size=self.LEN.PASSWD // 8,
            pattern=self.DEFAULT.PADDING, fromLeft=False)
        self.passwd = passwd_copy
    # end def __init__
# end class Passwd1


class StartSessionResponse(PasswordAuthentication):
    """
    Define ``StartSessionResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      5
    Long Password                 1
    Full Authentication           1
    Constant Credentials          1
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartSession,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(PasswordAuthentication.FID):
        # See ``PasswordAuthentication.FID``
        RESERVED = PasswordAuthentication.FID.SOFTWARE_ID - 1
        LONG_PASSWORD = RESERVED - 1
        FULL_AUTHENTICATION = LONG_PASSWORD - 1
        CONSTANT_CREDENTIALS = FULL_AUTHENTICATION - 1
        PADDING = CONSTANT_CREDENTIALS - 1
    # end class FID

    class LEN(PasswordAuthentication.LEN):
        # See ``PasswordAuthentication.LEN``
        RESERVED = 0x5
        LONG_PASSWORD = 0x1
        FULL_AUTHENTICATION = 0x1
        CONSTANT_CREDENTIALS = 0x1
        PADDING = 0x78
    # end class LEN

    FIELDS = PasswordAuthentication.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=PasswordAuthentication.DEFAULT.PADDING),
        BitField(fid=FID.LONG_PASSWORD, length=LEN.LONG_PASSWORD,
                 title="LongPassword", name="long_password",
                 checks=(CheckInt(0, pow(2, LEN.LONG_PASSWORD) - 1),)),
        BitField(fid=FID.FULL_AUTHENTICATION, length=LEN.FULL_AUTHENTICATION,
                 title="FullAuthentication", name="full_authentication",
                 checks=(CheckInt(0, pow(2, LEN.FULL_AUTHENTICATION) - 1),)),
        BitField(fid=FID.CONSTANT_CREDENTIALS, length=LEN.CONSTANT_CREDENTIALS,
                 title="ConstantCredentials", name="constant_credentials",
                 checks=(CheckInt(0, pow(2, LEN.CONSTANT_CREDENTIALS) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PasswordAuthentication.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, long_password=False, full_authentication=False,
                 constant_credentials=False, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param long_password: Long pass-word. When set to 1, pass-words may be up to 32 bytes long and both functions
                              passwd0 and passwd1 shall be used. When set to 0, pass-words are limited to 16 bytes and
                              only function passwd0 shall be used - OPTIONAL.
        :type long_password: ``bool | HexList``
        :param full_authentication: Full authentication. Always set to 0, as this feature supports only
                                    semi-authentication (external entity authenticated by HID) - OPTIONAL.
        :type full_authentication: ``bool | HexList``
        :param constant_credentials: Constant credentials. When set to 1, the credentials for this account can not be
                                     changed (except by DFU). When set to 0, they may be modified (outside this
                                     feature's scope) - OPTIONAL.
        :type constant_credentials: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.long_password = long_password
        self.full_authentication = full_authentication
        self.constant_credentials = constant_credentials
    # end def __init__
# end class StartSessionResponse


class EndSessionResponse(LongEmptyPacketDataFormat):
    """
    Define ``EndSessionResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EndSession,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class EndSessionResponse


class Passwd0Response(PasswordResponse):
    """
    Define ``Passwd0Response`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Passwd0,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, status, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param status: External-entity authentication status.
        :type status: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.status = status
    # end def __init__
# end class Passwd0Response


class Passwd1Response(PasswordResponse):
    """
    Define ``Passwd1Response`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Passwd1,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, status, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param status: External-entity authentication status.
        :type status: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.status = status
    # end def __init__
# end class Passwd1Response

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
