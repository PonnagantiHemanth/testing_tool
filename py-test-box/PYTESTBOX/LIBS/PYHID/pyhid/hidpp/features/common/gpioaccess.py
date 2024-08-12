#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.gpioaccess
:brief: HID++ 2.0 ``GpioAccess`` command interface definition
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/06/06
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
class GpioAccess(HidppMessage):
    """
    Define the Gpio Access to test the GPIO of all microcontrollers.

    This feature can set the gpio as input or output and can read and write on pins.

    The current version of this feature can support up to four ports.
    """
    FEATURE_ID = 0x1803
    MAX_FUNCTION_INDEX_V0 = 3
    MAX_FUNCTION_INDEX_V1 = 4

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
# end class GpioAccess


# noinspection DuplicatedCode
class GpioAccessModel(FeatureModel):
    """
    Define ``GpioAccess`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        SET_GROUP_IN = 0
        WRITE_GROUP_OUT = 1
        READ_GROUP = 2
        WRITE_GROUP = 3
        READ_GROUP_OUT = 4
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``GpioAccess`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.SET_GROUP_IN: {
                    "request": SetGroupIn,
                    "response": SetGroupInResponse
                },
                cls.INDEX.WRITE_GROUP_OUT: {
                    "request": WriteGroupOut,
                    "response": WriteGroupOutResponse
                },
                cls.INDEX.READ_GROUP: {
                    "request": ReadGroup,
                    "response": ReadGroupResponse
                },
                cls.INDEX.WRITE_GROUP: {
                    "request": WriteGroup,
                    "response": WriteGroupResponse
                }
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.SET_GROUP_IN: {
                    "request": SetGroupIn,
                    "response": SetGroupInResponse
                },
                cls.INDEX.WRITE_GROUP_OUT: {
                    "request": WriteGroupOut,
                    "response": WriteGroupOutResponse
                },
                cls.INDEX.READ_GROUP: {
                    "request": ReadGroup,
                    "response": ReadGroupResponse
                },
                cls.INDEX.WRITE_GROUP: {
                    "request": WriteGroup,
                    "response": WriteGroupResponse
                },
                cls.INDEX.READ_GROUP_OUT: {
                    "request": ReadGroupOutV1,
                    "response": ReadGroupOutResponseV1
                }
            }
        }

        return {
            "feature_base": GpioAccess,
            "versions": {
                GpioAccessV0.VERSION: {
                    "main_cls": GpioAccessV0,
                    "api": function_map_v0
                },
                GpioAccessV1.VERSION: {
                    "main_cls": GpioAccessV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class GpioAccessModel


class GpioAccessFactory(FeatureFactory):
    """
    Get ``GpioAccess`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``GpioAccess`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``GpioAccessInterface``
        """
        return GpioAccessModel.get_main_cls(version)()
    # end def create
# end class GpioAccessFactory


class GpioAccessInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``GpioAccess``
    """

    def __init__(self):
        # Requests
        self.set_group_in_cls = None
        self.write_group_out_cls = None
        self.read_group_cls = None
        self.write_group_cls = None
        self.read_group_out_cls = None

        # Responses
        self.set_group_in_response_cls = None
        self.write_group_out_response_cls = None
        self.read_group_response_cls = None
        self.write_group_response_cls = None
        self.read_group_out_response_cls = None
    # end def __init__
# end class GpioAccessInterface


class GpioAccessV0(GpioAccessInterface):
    """
    Define ``GpioAccessV0`` feature

    This feature provides model and unit specific information for version 0

    [0] setGroupIn(portNumber, gpioMask) -> None

    [1] writeGroupOut(portNumber, gpioMask, value) -> None

    [2] readGroup(portNumber, gpioMask) -> portNumber, gpioMask, value

    [3] writeGroup(portNumber, gpioMask, value) -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``GpioAccess.__init__``
        super().__init__()
        index = GpioAccessModel.INDEX

        # Requests
        self.set_group_in_cls = GpioAccessModel.get_request_cls(
            self.VERSION, index.SET_GROUP_IN)
        self.write_group_out_cls = GpioAccessModel.get_request_cls(
            self.VERSION, index.WRITE_GROUP_OUT)
        self.read_group_cls = GpioAccessModel.get_request_cls(
            self.VERSION, index.READ_GROUP)
        self.write_group_cls = GpioAccessModel.get_request_cls(
            self.VERSION, index.WRITE_GROUP)

        # Responses
        self.set_group_in_response_cls = GpioAccessModel.get_response_cls(
            self.VERSION, index.SET_GROUP_IN)
        self.write_group_out_response_cls = GpioAccessModel.get_response_cls(
            self.VERSION, index.WRITE_GROUP_OUT)
        self.read_group_response_cls = GpioAccessModel.get_response_cls(
            self.VERSION, index.READ_GROUP)
        self.write_group_response_cls = GpioAccessModel.get_response_cls(
            self.VERSION, index.WRITE_GROUP)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``GpioAccessInterface.get_max_function_index``
        return GpioAccessModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class GpioAccessV0


class GpioAccessV1(GpioAccessV0):
    """
    Define ``GpioAccessV1`` feature

    This feature provides model and unit specific information for version 1

    [4] readGroupOut(portNumber, gpioMask) -> portNumber, gpioMask, value
    """
    VERSION = 1

    def __init__(self):
        # See ``GpioAccess.__init__``
        super().__init__()
        index = GpioAccessModel.INDEX

        # Requests
        self.read_group_out_cls = GpioAccessModel.get_request_cls(
            self.VERSION, index.READ_GROUP_OUT)

        # Responses
        self.read_group_out_response_cls = GpioAccessModel.get_response_cls(
            self.VERSION, index.READ_GROUP_OUT)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``GpioAccessInterface.get_max_function_index``
        return GpioAccessModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class GpioAccessV1


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(GpioAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetGroupInResponse
        - WriteGroupOutResponse
        - WriteGroupResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(GpioAccess.FID):
        # See ``GpioAccess.FID``
        PADDING = GpioAccess.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(GpioAccess.LEN):
        # See ``GpioAccess.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = GpioAccess.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GpioAccess.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class SetReqReadReqDataFormat(GpioAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ReadGroup
        - ReadGroupOutV1
        - SetGroupIn

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Port Number                   8
    Gpio Mask                     32
    Padding                       88
    ============================  ==========
    """

    class FID(GpioAccess.FID):
        # See ``GpioAccess.FID``
        PORT_NUMBER = GpioAccess.FID.SOFTWARE_ID - 1
        GPIO_MASK = PORT_NUMBER - 1
        PADDING = GPIO_MASK - 1
    # end class FID

    class LEN(GpioAccess.LEN):
        # See ``GpioAccess.LEN``
        PORT_NUMBER = 0x8
        GPIO_MASK = 0x20
        PADDING = 0x58
    # end class LEN

    FIELDS = GpioAccess.FIELDS + (
        BitField(fid=FID.PORT_NUMBER, length=LEN.PORT_NUMBER,
                 title="PortNumber", name="port_number",
                 checks=(CheckHexList(LEN.PORT_NUMBER // 8),
                         CheckByte(),)),
        BitField(fid=FID.GPIO_MASK, length=LEN.GPIO_MASK,
                 title="GpioMask", name="gpio_mask",
                 checks=(CheckHexList(LEN.GPIO_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.GPIO_MASK) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GpioAccess.DEFAULT.PADDING),
    )
# end class SetReqReadReqDataFormat


class WriteReqReadResDataFormat(GpioAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - ReadGroupOutResponseV1
        - ReadGroupResponse
        - WriteGroup
        - WriteGroupOut

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Port Number                   8
    Gpio Mask                     32
    Value                         32
    Padding                       56
    ============================  ==========
    """

    class FID(GpioAccess.FID):
        # See ``GpioAccess.FID``
        PORT_NUMBER = GpioAccess.FID.SOFTWARE_ID - 1
        GPIO_MASK = PORT_NUMBER - 1
        VALUE = GPIO_MASK - 1
        PADDING = VALUE - 1
    # end class FID

    class LEN(GpioAccess.LEN):
        # See ``GpioAccess.LEN``
        PORT_NUMBER = 0x8
        GPIO_MASK = 0x20
        VALUE = 0x20
        PADDING = 0x38
    # end class LEN

    FIELDS = GpioAccess.FIELDS + (
        BitField(fid=FID.PORT_NUMBER, length=LEN.PORT_NUMBER,
                 title="PortNumber", name="port_number",
                 checks=(CheckHexList(LEN.PORT_NUMBER // 8),
                         CheckByte(),)),
        BitField(fid=FID.GPIO_MASK, length=LEN.GPIO_MASK,
                 title="GpioMask", name="gpio_mask",
                 checks=(CheckHexList(LEN.GPIO_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.GPIO_MASK) - 1),)),
        BitField(fid=FID.VALUE, length=LEN.VALUE,
                 title="Value", name="value",
                 checks=(CheckHexList(LEN.VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.VALUE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=GpioAccess.DEFAULT.PADDING),
    )
# end class WriteReqReadResDataFormat


class SetGroupIn(SetReqReadReqDataFormat):
    """
    Define ``SetGroupIn`` implementation class
    """

    def __init__(self, device_index, feature_index, port_number, gpio_mask, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetGroupInResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
    # end def __init__
# end class SetGroupIn


class WriteGroupOut(WriteReqReadResDataFormat):
    """
    Define ``WriteGroupOut`` implementation class
    """

    def __init__(self, device_index, feature_index, port_number, gpio_mask, value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param value: Value
        :type value: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=WriteGroupOutResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
        self.value = HexList(Numeral(value, self.LEN.VALUE // 8))
    # end def __init__
# end class WriteGroupOut


class ReadGroup(SetReqReadReqDataFormat):
    """
    Define ``ReadGroup`` implementation class
    """

    def __init__(self, device_index, feature_index, port_number, gpio_mask, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadGroupResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
    # end def __init__
# end class ReadGroup


class WriteGroup(WriteReqReadResDataFormat):
    """
    Define ``WriteGroup`` implementation class
    """

    def __init__(self, device_index, feature_index, port_number, gpio_mask, value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param value: Value
        :type value: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=WriteGroupResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
        self.value = HexList(Numeral(value, self.LEN.VALUE // 8))
    # end def __init__
# end class WriteGroup


class ReadGroupOutV1(SetReqReadReqDataFormat):
    """
    Define ``ReadGroupOutV1`` implementation class
    """

    def __init__(self, device_index, feature_index, port_number, gpio_mask, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadGroupOutResponseV1.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
    # end def __init__
# end class ReadGroupOutV1


class SetGroupInResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetGroupInResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetGroupIn,)
    VERSION = (0, 1,)
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
# end class SetGroupInResponse


class WriteGroupOutResponse(LongEmptyPacketDataFormat):
    """
    Define ``WriteGroupOutResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteGroupOut,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

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
# end class WriteGroupOutResponse


class ReadGroupResponse(WriteReqReadResDataFormat):
    """
    Define ``ReadGroupResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadGroup,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, port_number, gpio_mask, value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param value: Value
        :type value: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
        self.value = HexList(Numeral(value, self.LEN.VALUE // 8))
    # end def __init__
# end class ReadGroupResponse


class WriteGroupResponse(LongEmptyPacketDataFormat):
    """
    Define ``WriteGroupResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteGroup,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

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
# end class WriteGroupResponse


class ReadGroupOutResponseV1(WriteReqReadResDataFormat):
    """
    Define ``ReadGroupOutResponseV1`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadGroupOutV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, port_number, gpio_mask, value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param port_number: Port Number
        :type port_number: ``int | HexList``
        :param gpio_mask: Gpio Mask
        :type gpio_mask: ``int | HexList``
        :param value: Value
        :type value: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_number = HexList(Numeral(port_number, self.LEN.PORT_NUMBER // 8))
        self.gpio_mask = HexList(Numeral(gpio_mask, self.LEN.GPIO_MASK // 8))
        self.value = HexList(Numeral(value, self.LEN.VALUE // 8))
    # end def __init__
# end class ReadGroupOutResponseV1

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
