#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.keepalive
:brief: HID++ 2.0 ``KeepAlive`` command interface definition
:author: Harish Kumar D <hd@logitech.com>
:date: 2024/01/16
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
class KeepAlive(HidppMessage):
    """
    Software-driven keep-alive requests may be used if a device needs to be aware of the state of the software. The use
    case is for supporting an autonomous fallback UX on the device should the software becomes unresponsive.
    """
    FEATURE_ID = 0x0008
    MAX_FUNCTION_INDEX_V0 = 2
    MAX_FUNCTION_INDEX_V1 = 2

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
# end class KeepAlive


# noinspection DuplicatedCode
class KeepAliveModel(FeatureModel):
    """
    Define ``KeepAlive`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_TIMEOUT_RANGE = 0
        KEEP_ALIVE = 1
        TERMINATE = 2

        # Event index
        KEEP_ALIVE_TIMEOUT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``KeepAlive`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_TIMEOUT_RANGE: {
                    "request": GetTimeoutRangeRequest,
                    "response": GetTimeoutRangeResponse
                },
                cls.INDEX.KEEP_ALIVE: {
                    "request": KeepAliveRequest,
                    "response": KeepAliveResponse
                },
                cls.INDEX.TERMINATE: {
                    "request": TerminateRequest,
                    "response": TerminateResponse
                }
            },
            "events": {}
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_TIMEOUT_RANGE: {
                    "request": GetTimeoutRangeRequest,
                    "response": GetTimeoutRangeResponse
                },
                cls.INDEX.KEEP_ALIVE: {
                    "request": KeepAliveRequest,
                    "response": KeepAliveResponse
                },
                cls.INDEX.TERMINATE: {
                    "request": TerminateRequest,
                    "response": TerminateResponse
                }
            },
            "events": {
                cls.INDEX.KEEP_ALIVE_TIMEOUT: {"report": KeepAliveTimeoutEventV1}
            }
        }

        return {
            "feature_base": KeepAlive,
            "versions": {
                KeepAliveV0.VERSION: {
                    "main_cls": KeepAliveV0,
                    "api": function_map_v0
                },
                KeepAliveV1.VERSION: {
                    "main_cls": KeepAliveV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class KeepAliveModel


class KeepAliveFactory(FeatureFactory):
    """
    Get ``KeepAlive`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``KeepAlive`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``KeepAliveInterface``
        """
        return KeepAliveModel.get_main_cls(version)()
    # end def create
# end class KeepAliveFactory


class KeepAliveInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``KeepAlive``
    """

    def __init__(self):
        # Requests
        self.get_timeout_range_cls = None
        self.keep_alive_cls = None
        self.terminate_cls = None

        # Responses
        self.get_timeout_range_response_cls = None
        self.keep_alive_response_cls = None
        self.terminate_response_cls = None

        # Events
        self.keep_alive_timeout_event_cls = None
    # end def __init__
# end class KeepAliveInterface


class KeepAliveV0(KeepAliveInterface):
    """
    Define ``KeepAliveV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getTimeoutRange() -> timeoutMinimum, timeoutMaximum

    [1] keepAlive(requestedTimeout) -> finalTimeout

    [2] terminate() -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``KeepAlive.__init__``
        super().__init__()
        index = KeepAliveModel.INDEX

        # Requests
        self.get_timeout_range_cls = KeepAliveModel.get_request_cls(
            self.VERSION, index.GET_TIMEOUT_RANGE)
        self.keep_alive_cls = KeepAliveModel.get_request_cls(
            self.VERSION, index.KEEP_ALIVE)
        self.terminate_cls = KeepAliveModel.get_request_cls(
            self.VERSION, index.TERMINATE)

        # Responses
        self.get_timeout_range_response_cls = KeepAliveModel.get_response_cls(
            self.VERSION, index.GET_TIMEOUT_RANGE)
        self.keep_alive_response_cls = KeepAliveModel.get_response_cls(
            self.VERSION, index.KEEP_ALIVE)
        self.terminate_response_cls = KeepAliveModel.get_response_cls(
            self.VERSION, index.TERMINATE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``KeepAliveInterface.get_max_function_index``
        return KeepAliveModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class KeepAliveV0


class KeepAliveV1(KeepAliveV0):
    """
    Define ``KeepAliveV1`` feature

    This feature provides model and unit specific information for version 1

    [Event 0] KeepAliveTimeoutEvent -> reserved
    """
    VERSION = 1

    def __init__(self):
        # See ``KeepAlive.__init__``
        super().__init__()
        index = KeepAliveModel.INDEX

        # Events
        self.keep_alive_timeout_event_cls = KeepAliveModel.get_report_cls(self.VERSION, index.KEEP_ALIVE_TIMEOUT)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``KeepAliveInterface.get_max_function_index``
        return KeepAliveModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class KeepAliveV1


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(KeepAlive):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetTimeoutRangeRequest
        - TerminateRequest

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(KeepAlive.FID):
        # See ``KeepAliveFID``
        PADDING = KeepAlive.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(KeepAlive.LEN):
        # See ``KeepAliveLEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = KeepAlive.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeepAlive.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(KeepAlive):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - TerminateResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(KeepAlive.FID):
        # See ``KeepAliveFID``
        PADDING = KeepAlive.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(KeepAlive.LEN):
        # See ``KeepAlive.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = KeepAlive.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeepAlive.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat

class GetTimeoutRangeRequest(ShortEmptyPacketDataFormat):
    """
    Define ``GetTimeoutRangeRequest`` implementation class
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
                         function_index=GetTimeoutRangeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetTimeoutRangeRequest

class KeepAliveRequest(KeepAlive):
    """
    Define ``KeepAlive`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Requested Timeout             16
    Padding                       8
    ============================  ==========
    """

    class FID(KeepAlive.FID):
        # See ``KeepAlive.FID``
        REQUESTED_TIMEOUT = KeepAlive.FID.SOFTWARE_ID - 1
        PADDING = REQUESTED_TIMEOUT - 1
    # end class FID

    class LEN(KeepAlive.LEN):
        # See ``KeepAlive.LEN``
        REQUESTED_TIMEOUT = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = KeepAlive.FIELDS + (
        BitField(fid=FID.REQUESTED_TIMEOUT, length=LEN.REQUESTED_TIMEOUT,
                 title="RequestedTimeout", name="requested_timeout",
                 checks=(CheckHexList(LEN.REQUESTED_TIMEOUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REQUESTED_TIMEOUT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeepAlive.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, requested_timeout, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param requested_timeout: Requested Timeout
        :type requested_timeout: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=KeepAliveResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        requested_timeout_copy = HexList(requested_timeout.copy())
        requested_timeout_copy.addPadding(self.LEN.REQUESTED_TIMEOUT // 8)
        self.requested_timeout = requested_timeout_copy
    # end def __init__
# end class KeepAlive


class TerminateRequest(ShortEmptyPacketDataFormat):
    """
    Define ``TerminateRequest`` implementation class
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
                         function_index=TerminateResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class TerminateRequest


class GetTimeoutRangeResponse(KeepAlive):
    """
    Define ``GetTimeoutRangeResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Timeout Minimum               16
    Timeout Maximum               16
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetTimeoutRangeRequest,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(KeepAlive.FID):
        # See ``KeepAlive.FID``
        TIMEOUT_MINIMUM = KeepAlive.FID.SOFTWARE_ID - 1
        TIMEOUT_MAXIMUM = TIMEOUT_MINIMUM - 1
        PADDING = TIMEOUT_MAXIMUM - 1
    # end class FID

    class LEN(KeepAlive.LEN):
        # See ``KeepAlive.LEN``
        TIMEOUT_MINIMUM = 0x10
        TIMEOUT_MAXIMUM = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = KeepAlive.FIELDS + (
        BitField(fid=FID.TIMEOUT_MINIMUM, length=LEN.TIMEOUT_MINIMUM,
                 title="TimeoutMinimum", name="timeout_minimum",
                 checks=(CheckHexList(LEN.TIMEOUT_MINIMUM // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIMEOUT_MINIMUM) - 1),)),
        BitField(fid=FID.TIMEOUT_MAXIMUM, length=LEN.TIMEOUT_MAXIMUM,
                 title="TimeoutMaximum", name="timeout_maximum",
                 checks=(CheckHexList(LEN.TIMEOUT_MAXIMUM // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.TIMEOUT_MAXIMUM) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeepAlive.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, timeout_minimum, timeout_maximum, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param timeout_minimum: Timeout Minimum
        :type timeout_minimum: ``HexList``
        :param timeout_maximum: Timeout Maximum
        :type timeout_maximum: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        timeout_minimum_copy = HexList(timeout_minimum.copy())
        timeout_minimum_copy.addPadding(self.LEN.TIMEOUT_MINIMUM // 8)
        self.timeout_minimum = timeout_minimum_copy

        timeout_maximum_copy = HexList(timeout_maximum.copy())
        timeout_maximum_copy.addPadding(self.LEN.TIMEOUT_MAXIMUM // 8)
        self.timeout_maximum = timeout_maximum_copy
    # end def __init__
# end class GetTimeoutRangeResponse


class KeepAliveResponse(KeepAlive):
    """
    Define ``KeepAliveResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Final Timeout                 16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (KeepAlive,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    class FID(KeepAlive.FID):
        # See ``KeepAlive.FID``
        FINAL_TIMEOUT = KeepAlive.FID.SOFTWARE_ID - 1
        PADDING = FINAL_TIMEOUT - 1
    # end class FID

    class LEN(KeepAlive.LEN):
        # See ``KeepAlive.LEN``
        FINAL_TIMEOUT = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = KeepAlive.FIELDS + (
        BitField(fid=FID.FINAL_TIMEOUT, length=LEN.FINAL_TIMEOUT,
                 title="FinalTimeout", name="final_timeout",
                 checks=(CheckHexList(LEN.FINAL_TIMEOUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FINAL_TIMEOUT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=KeepAlive.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, final_timeout, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param final_timeout: Final Timeout
        :type final_timeout: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        final_timeout_copy = HexList(final_timeout.copy())
        final_timeout_copy.addPadding(self.LEN.FINAL_TIMEOUT // 8)
        self.final_timeout = final_timeout_copy
    # end def __init__
# end class KeepAliveResponse


class TerminateResponse(LongEmptyPacketDataFormat):
    """
    Define ``TerminateResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (TerminateRequest,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

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
# end class TerminateResponse


class KeepAliveTimeoutEventV1(LongEmptyPacketDataFormat):
    """
    Define ``KeepAliveTimeoutEventV1`` implementation class
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
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
# end class KeepAliveTimeoutEventV1

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
