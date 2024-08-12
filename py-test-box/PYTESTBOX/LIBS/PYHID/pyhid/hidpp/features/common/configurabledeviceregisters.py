#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.common.configurabledeviceregisters
:brief: HID++ 2.0 ``ConfigurableDeviceRegisters`` command interface definition
:author: Udayathilagan <uelamaran@logitech.com>
:date: 2024/05/08
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import auto
from enum import IntEnum

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
# Constants
# ----------------------------------------------------------------------------------------------------------------------

class REGISTERS(IntEnum):
    """
    Define register names
    """
    READ_PROTECTION_LEVEL = 1
    WRITE_PROTECTION_LEVEL = auto()
    BROWN_OUT_REST_LEVEL = auto()
    USER = auto()
    PROPRIETARY_CODE_READOUT_PROTECTION_CONFIGURATION = auto()
    BOOT_LOCK = auto()
    SEC = auto()
# end class REGISTERS


DEFAULT_REGISTER_SIZE_MAP = {
    REGISTERS.READ_PROTECTION_LEVEL: 1,
    REGISTERS.WRITE_PROTECTION_LEVEL: 1,
    REGISTERS.BROWN_OUT_REST_LEVEL: 1,
    REGISTERS.USER: 1,
    REGISTERS.PROPRIETARY_CODE_READOUT_PROTECTION_CONFIGURATION: 8,
    REGISTERS.BOOT_LOCK: 1,
    REGISTERS.SEC: 1,
}


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class ConfigurableDeviceRegisters(HidppMessage):
    """
    Configurable Device Register implementation class

    This TDE only feature is responsible for setting and getting device specific configuration registers.
    """
    FEATURE_ID = 0x180B
    MAX_FUNCTION_INDEX_V0 = 3

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
# end class ConfigurableDeviceRegisters


# noinspection DuplicatedCode
class ConfigurableDeviceRegistersModel(FeatureModel):
    """
    Define ``ConfigurableDeviceRegisters`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_REGISTER_INFO = 1
        GET_REGISTER_VALUE = 2
        SET_REGISTER_VALUE = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ConfigurableDeviceRegisters`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_REGISTER_INFO: {
                    "request": GetRegisterInfo,
                    "response": GetRegisterInfoResponse
                },
                cls.INDEX.GET_REGISTER_VALUE: {
                    "request": GetRegisterValue,
                    "response": GetRegisterValueResponse
                },
                cls.INDEX.SET_REGISTER_VALUE: {
                    "request": SetRegisterValue,
                    "response": SetRegisterValueResponse
                }
            }
        }

        return {
            "feature_base": ConfigurableDeviceRegisters,
            "versions": {
                ConfigurableDeviceRegistersV0.VERSION: {
                    "main_cls": ConfigurableDeviceRegistersV0,
                    "api": function_map
                }
            }
        }
    # end def _get_data_model
# end class ConfigurableDeviceRegistersModel


class ConfigurableDeviceRegistersFactory(FeatureFactory):
    """
    Get ``ConfigurableDeviceRegisters`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ConfigurableDeviceRegisters`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``ConfigurableDeviceRegistersInterface``
        """
        return ConfigurableDeviceRegistersModel.get_main_cls(version)()
    # end def create
# end class ConfigurableDeviceRegistersFactory


class ConfigurableDeviceRegistersInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ConfigurableDeviceRegisters``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_register_info_cls = None
        self.get_register_value_cls = None
        self.set_register_value_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_register_info_response_cls = None
        self.get_register_value_response_cls = None
        self.set_register_value_response_cls = None
    # end def __init__
# end class ConfigurableDeviceRegistersInterface


class ConfigurableDeviceRegistersV0(ConfigurableDeviceRegistersInterface):
    """
    Define ``ConfigurableDeviceRegistersV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getCapabilities() -> capabilities

    [1] getRegisterInfo(register id) -> configurable, supported, register size

    [2] getRegisterValue(register id) -> register value

    [3] setRegisterValue(register id, register value) -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``ConfigurableDeviceRegisters.__init__``
        super().__init__()
        index = ConfigurableDeviceRegistersModel.INDEX

        # Requests
        self.get_capabilities_cls = ConfigurableDeviceRegistersModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_register_info_cls = ConfigurableDeviceRegistersModel.get_request_cls(
            self.VERSION, index.GET_REGISTER_INFO)
        self.get_register_value_cls = ConfigurableDeviceRegistersModel.get_request_cls(
            self.VERSION, index.GET_REGISTER_VALUE)
        self.set_register_value_cls = ConfigurableDeviceRegistersModel.get_request_cls(
            self.VERSION, index.SET_REGISTER_VALUE)

        # Responses
        self.get_capabilities_response_cls = ConfigurableDeviceRegistersModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_register_info_response_cls = ConfigurableDeviceRegistersModel.get_response_cls(
            self.VERSION, index.GET_REGISTER_INFO)
        self.get_register_value_response_cls = ConfigurableDeviceRegistersModel.get_response_cls(
            self.VERSION, index.GET_REGISTER_VALUE)
        self.set_register_value_response_cls = ConfigurableDeviceRegistersModel.get_response_cls(
            self.VERSION, index.SET_REGISTER_VALUE)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``ConfigurableDeviceRegistersInterface.get_max_function_index``
        return ConfigurableDeviceRegistersModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class ConfigurableDeviceRegistersV0


# noinspection DuplicatedCode
class ShortEmptyPacketDataFormat(ConfigurableDeviceRegisters):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        PADDING = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongEmptyPacketDataFormat(ConfigurableDeviceRegisters):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetRegisterValueResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        PADDING = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


# noinspection DuplicatedCode
class LongPayloadDataFormat(ConfigurableDeviceRegisters):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - SetRegisterValueResponse
        - GetRegisterValueResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Payload                       128
    ============================  ==========
    """

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        PAYLOAD = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        PAYLOAD = 0x80
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.PAYLOAD, length=LEN.PAYLOAD,
                 title="Payload", name="payload",
                 checks=(CheckHexList(LEN.PAYLOAD // 8), CheckByte(),),),)
# end class LongPayloadDataFormat


class RegisterPayload(ConfigurableDeviceRegisters):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetRegisterInfo
        - GetRegisterValue

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RegisterId                    16
    Padding                       8
    ============================  ==========
    """

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        REGISTER_ID = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
        PADDING = REGISTER_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        REGISTER_ID = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.REGISTER_ID, length=LEN.REGISTER_ID,
                 title="RegisterId", name="register_id",
                 checks=(CheckHexList(LEN.REGISTER_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REGISTER_ID) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),
    )
# end class RegisterPayload


class GetCapabilities(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class
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
                         function_index=GetCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetRegisterInfo(RegisterPayload):
    """
    Define ``GetRegisterInfo`` implementation class
    """

    def __init__(self, device_index, feature_index, register_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_id: Register_Id
        :type register_id: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetRegisterInfoResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        register_id_copy = HexList(register_id.copy())
        register_id_copy.addPadding(self.LEN.REGISTER_ID // 8)
        self.register_id = register_id_copy
    # end def __init__
# end class GetRegisterInfo


class GetRegisterValue(RegisterPayload):
    """
    Define ``GetRegisterValue`` implementation class
    """

    def __init__(self, device_index, feature_index, register_id, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_id: Register_Id
        :type register_id: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetRegisterValueResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)

        register_id_copy = HexList(register_id.copy())
        register_id_copy.addPadding(self.LEN.REGISTER_ID // 8)
        self.register_id = register_id_copy
    # end def __init__
# end class GetRegisterValue


class SetRegisterValue(ConfigurableDeviceRegisters):
    """
    Define ``SetRegisterValue`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Register_Id                   16
    Register_Value                 112
    ============================  ==========
    """
    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        REGISTER_ID = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
        REGISTER_VALUE = REGISTER_ID - 1
        PADDING = REGISTER_VALUE - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        REGISTER_ID = 0x10
        REGISTER_VALUE = 0x70
        PADDING = 0x10
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.REGISTER_ID, length=LEN.REGISTER_ID,
                 title="RegisterId", name="register_id",
                 checks=(CheckHexList(LEN.REGISTER_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REGISTER_ID) - 1),)),
        BitField(fid=FID.REGISTER_VALUE, length=LEN.REGISTER_VALUE,
                 title="RegisterValue", name="register_value",
                 checks=(CheckHexList(LEN.REGISTER_VALUE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.REGISTER_VALUE) - 1),)),
    )

    def __init__(self, device_index, feature_index, register_id, register_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_id: RegisterId
        :type register_id: ``HexList``
        :param register_value: RegisterValue
        :type register_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SetRegisterValueResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)

        register_id_copy = HexList(register_id)
        register_id_copy.addPadding(self.LEN.REGISTER_ID // 8)
        self.register_id = register_id_copy

        register_value_copy = HexList(register_value.copy())
        register_value_copy.addPadding(self.LEN.REGISTER_VALUE // 8)
        self.register_value = register_value_copy
    # end def __init__

    @classmethod
    def register_value_based_on_size(cls, report, register_id, register_value, register_size=None):
        """
        Create '' SetRegisterValue'' Adjusts the register value size and padding based on the specified or default
        register size.

        :param report:  set register value request report
        :type report: ``SetRegisterValue``
        :param register_id: register id
        :type register_id: ``int``
        :param register_value: register value
        :type register_value: ``HexList``
        :param register_size: register size - OPTIONAL
        :type register_size: ``int | None``

        :return:  set register value request report
        :rtype: ``SetRegisterValue``
        """
        register_size = register_size \
            if register_size is not None else DEFAULT_REGISTER_SIZE_MAP[register_id]
        # noinspection PyUnresolvedReferences
        total_bits = len(report.register_value) * 8  # Total register value space
        padding_bits = total_bits - (register_size * 8)

        # # Delete the register_value from FIELDS
        report.FIELDS = report.FIELDS[:-1]
        report.FIELDS += (
            BitField(fid=cls.FID.REGISTER_VALUE, length=(register_size*8),
                     title="RegisterValue", name="register_value",
                     checks=(CheckHexList((register_size*8) // 8),
                             CheckInt(min_value=0, max_value=pow(2, (register_size*8)) - 1),)),
        )
        setattr(report, "register_value", register_value)
        report.FIELDS += (
            BitField(fid=cls.FID.PADDING, length=padding_bits,
                     title="Padding", name="padding",
                     checks=(CheckHexList(padding_bits // 8),
                             CheckInt(min_value=0, max_value=pow(2, padding_bits) - 1),)),
        )
        setattr(report, "register_value", register_value)
        setattr(report, "padding", 0)
        return report
    # end def register_value_based_on_size
# end class SetRegisterValue


class GetCapabilitiesResponse(ConfigurableDeviceRegisters):
    """
    Define ``GetCapabilitiesResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      7
    Capabilities                  1
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        RESERVED = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
        CAPABILITIES = RESERVED - 1
        PADDING = CAPABILITIES - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        RESERVED = 0x7
        CAPABILITIES = 0x1
        PADDING = 0x78
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),
        BitField(fid=FID.CAPABILITIES, length=LEN.CAPABILITIES,
                 title="Capabilities", name="capabilities",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CAPABILITIES) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, capabilities, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param capabilities: Capabilities
        :type capabilities: ``bool | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.capabilities = capabilities
    # end def __init__
# end class GetCapabilitiesResponse


class GetRegisterInfoResponse(ConfigurableDeviceRegisters):
    """
    Define ``GetRegisterInfoResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      6
    Configurable                  1
    Supported                     1
    RegisterSize                  8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRegisterInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        RESERVED = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
        CONFIGURABLE = RESERVED - 1
        SUPPORTED = CONFIGURABLE - 1
        REGISTER_SIZE = SUPPORTED - 1
        PADDING = REGISTER_SIZE - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        RESERVED = 0x6
        CONFIGURABLE = 0x1
        SUPPORTED = 0x1
        REGISTER_SIZE = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),
        BitField(fid=FID.CONFIGURABLE, length=LEN.CONFIGURABLE,
                 title="Configurable", name="configurable",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.CONFIGURABLE) - 1),)),
        BitField(fid=FID.SUPPORTED, length=LEN.SUPPORTED,
                 title="Supported", name="supported",
                 checks=(CheckInt(min_value=0, max_value=pow(2, LEN.SUPPORTED) - 1),)),
        BitField(fid=FID.REGISTER_SIZE, length=LEN.REGISTER_SIZE,
                 title="RegisterSize", name="register_size",
                 checks=(CheckHexList(LEN.REGISTER_SIZE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ConfigurableDeviceRegisters.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, configurable, supported, register_size, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param configurable: Configurable
        :type configurable: ``bool | HexList``
        :param supported: Supported
        :type supported: ``bool | HexList``
        :param register_size: Register Size
        :type register_size: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.configurable = configurable
        self.supported = supported

        register_size_copy = HexList(register_size.copy())
        register_size_copy.addPadding(self.LEN.REGISTER_SIZE // 8)
        self.register_size = register_size_copy
    # end def __init__
# end class GetRegisterInfoResponse


class GetRegisterValueResponse(ConfigurableDeviceRegisters):
    """
    Define ``GetRegisterValueResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    RegisterValue                 128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRegisterValue,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(ConfigurableDeviceRegisters.FID):
        # See ``ConfigurableDeviceRegisters.FID``
        PAYLOAD = ConfigurableDeviceRegisters.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ConfigurableDeviceRegisters.LEN):
        # See ``ConfigurableDeviceRegisters.LEN``
        PAYLOAD = 0x80
    # end class LEN

    FIELDS = ConfigurableDeviceRegisters.FIELDS + (
        BitField(fid=FID.PAYLOAD, length=LEN.PAYLOAD,
                 title="Payload", name="payload",
                 checks=(CheckHexList(LEN.PAYLOAD // 8), CheckByte(),),),)

    def __init__(self, device_index, feature_index, payload, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param payload: Payload data
        :type payload: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``object``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.payload = payload
    # end def __init__

    # noinspection PyPep8Naming
    @classmethod
    def from_hex_list(cls, *args, **kwargs):
        """
        Create ``GetRegisterValueResponse``  from raw input

        :param args: List of arguments
        :type args: ``list``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``

        :return: Class instance
        :rtype: ``GetRegisterValueResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        register_id = kwargs["register_id"]
        register_id = register_id if isinstance(register_id, int) else int(register_id)
        register_size = kwargs["register_size"] \
            if kwargs["register_size"] is not None else DEFAULT_REGISTER_SIZE_MAP[register_id]
        payload = inner_field_container_mixin.payload
        register_value = payload[:register_size]
        padding_value = payload[register_size:]
        # Delete the payload from FIELDS
        inner_field_container_mixin.FIELDS = inner_field_container_mixin.FIELDS[:-1]
        inner_field_container_mixin.FIELDS += (
            BitField(fid=cls.FID.PAYLOAD, length=register_size * 8,
                     title="RegisterValue", name="register_value",
                     checks=(CheckHexList(register_size * 8 // 8), CheckByte(),)),
        )
        setattr(inner_field_container_mixin, "register_value", register_value)
        inner_field_container_mixin.FIELDS += (
            BitField(fid=cls.FID.PAYLOAD - 1, length=LongPayloadDataFormat.LEN.PAYLOAD - register_size * 8,
                     title="Padding", name="padding",
                     checks=(CheckHexList((LongPayloadDataFormat.LEN.PAYLOAD - register_size * 8) // 8),
                             CheckByte(),),
                     ),
        )
        setattr(inner_field_container_mixin, "padding", padding_value)
        return inner_field_container_mixin
    # end def from_hex_list
# end class GetRegisterValueResponse


class SetRegisterValueResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetRegisterValueResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRegisterValue,)
    VERSION = (0,)
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
# end class SetRegisterValueResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
