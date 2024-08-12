#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.deviceinformation
:brief: HID++ 2.0 Device Information command interface definition
:author: Stanislas Cottard <scottard@logitech.com>
:date: 2019/11/28
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from warnings import warn

from pyhid.bitfield import BitField
from pyhid.field import CheckBCD
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


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DeviceInformation(HidppMessage):
    """
    DeviceInformation implementation class

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        24
    ============================  ==========
    """
    FEATURE_ID = 0x0003
    MAX_FUNCTION_INDEX_V1_TO_V3 = 1
    MAX_FUNCTION_INDEX_V4_TO_V8 = 2

    class EntityTypeV1(object):
        """
        This is the entity type possible values for version 1
        """
        MAIN_APP = 0      # Main application (provides full functionality to a device)
        BOOTLOADER = 1    # Bootloader (provides DFU functionality)
        HARDWARE = 2      # Hardware
        TOUCHPAD = 3      # Touchpad (used to know touchpad FW version)
        OPT_SENSOR = 4    # Optical sensor (used to know optical sensor FW version)
        SOFTDEVICE = 5    # Softdevice (Nordic's SoftDevice version)
        RF_COMPANION = 6  # RF companion MCU (used to know RF companion MCU FW version)
        RESERVED = list(range(7, 16))     # 7..15 Reserved
    # end class EntityTypeV1

    class EntityTypeV2(EntityTypeV1):
        """
        This is the entity type possible values for version 2
        """
        # Factory application (provides full functionality to a device and handles the DFU
        # process, but is not upgradable)
        FACTORY_APP = 7
        RGB_EFFECT = 8    # RGB Custom Effect (storage for a custom RGB effect)
        RESERVED = list(range(9, 16))     # 9..15 Reserved
    # end class EntityTypeV2

    class EntityTypeV3ToV4(EntityTypeV2):
        """
        This is the entity type possible values for versions 3 & 4
        """
        # Motor drive (provides an HIDPP and DFU capability for a companion MCU chip for motor
        # drive)
        MOTOR_DRIVE = 9
        # 10..15 Reserved
        RESERVED = list(range(10, 16))
    # end class EntityTypeV3ToV4

    class EntityTypeV5ToV6(EntityTypeV3ToV4):
        """
        This is the entity type possible values for versions 5 & 6
        """
        # Main application of Companion MCU (used to know companion MCU FW application version)
        MAIN_APP_COMPANION = 6
        # Bootloader of Companion MCU (used to know companion MCU bootloader version)
        BOOTLOADER_COMPANION = 10
        # 11..15 Reserved
        RESERVED = list(range(11, 16))
    # end class EntityTypeV5ToV6

    class EntityTypeV7ToV8(EntityTypeV5ToV6):
        """
        This is the entity type possible values for version 7 & 8
        """
        # Embedded images: Storage of on-board image and animation resources. Updatable via Bazinga.
        EMBEDDED_IMAGES = 11
        # 12..15 Reserved
        RESERVED = list(range(12, 16))
    # end class EntityTypeV7ToV8

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(**kwargs)

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class DeviceInformation


class DeviceInformationModel(FeatureModel):
    """
    Device information feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_DEVICE_INFO = 0
        GET_FW_INFO = 1
        GET_DEVICE_SERIAL_NUMBER = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Device information feature data model

        :return: Device information feature data model
        :rtype: ``dict``
        """
        function_map_v2_to_v3 = {
            "functions": {
                cls.INDEX.GET_DEVICE_INFO: {"request": GetDeviceInfoV1ToV8,
                                            "response": GetDeviceInfoResponseV2ToV3},
                cls.INDEX.GET_FW_INFO: {"request": GetFwInfoV1ToV8, "response": GetFwInfoResponseV1ToV7},
            }
        }
        function_map_v4_to_v5 = {
            "functions": {
                cls.INDEX.GET_DEVICE_INFO: {"request": GetDeviceInfoV1ToV8,
                                            "response": GetDeviceInfoResponseV4ToV5},
                cls.INDEX.GET_FW_INFO: {"request": GetFwInfoV1ToV8, "response": GetFwInfoResponseV1ToV7},
                cls.INDEX.GET_DEVICE_SERIAL_NUMBER: {"request": GetDeviceSerialNumberV4ToV8,
                                                     "response": GetDeviceSerialNumberResponseV4ToV8},
            }
        }
        function_map_v6_to_v7 = {
            "functions": {
                cls.INDEX.GET_DEVICE_INFO: {"request": GetDeviceInfoV1ToV8,
                                            "response": GetDeviceInfoResponseV6ToV8},
                cls.INDEX.GET_FW_INFO: {"request": GetFwInfoV1ToV8, "response": GetFwInfoResponseV1ToV7},
                cls.INDEX.GET_DEVICE_SERIAL_NUMBER: {"request": GetDeviceSerialNumberV4ToV8,
                                                     "response": GetDeviceSerialNumberResponseV4ToV8},
            }
        }
        function_map_v8 = {
            "functions": {
                cls.INDEX.GET_DEVICE_INFO: {"request": GetDeviceInfoV1ToV8,
                                            "response": GetDeviceInfoResponseV6ToV8},
                cls.INDEX.GET_FW_INFO: {"request": GetFwInfoV1ToV8, "response": GetFwInfoResponseV8},
                cls.INDEX.GET_DEVICE_SERIAL_NUMBER: {"request": GetDeviceSerialNumberV4ToV8,
                                                     "response": GetDeviceSerialNumberResponseV4ToV8},
            }
        }
        return {
            "feature_base": DeviceInformation,
            "versions": {
                DeviceInformationV1.VERSION: {
                    "main_cls": DeviceInformationV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_DEVICE_INFO: {"request": GetDeviceInfoV1ToV8,
                                                        "response": GetDeviceInfoResponseV1},
                            cls.INDEX.GET_FW_INFO: {"request": GetFwInfoV1ToV8, "response": GetFwInfoResponseV1ToV7},
                        }
                    },
                },
                DeviceInformationV2.VERSION: {
                    "main_cls": DeviceInformationV2,
                    "api": function_map_v2_to_v3
                },
                DeviceInformationV3.VERSION: {
                    "main_cls": DeviceInformationV3,
                    "api": function_map_v2_to_v3
                },
                DeviceInformationV4.VERSION: {
                    "main_cls": DeviceInformationV4,
                    "api": function_map_v4_to_v5
                },
                DeviceInformationV5.VERSION: {
                    "main_cls": DeviceInformationV5,
                    "api": function_map_v4_to_v5
                },
                DeviceInformationV6.VERSION: {
                    "main_cls": DeviceInformationV6,
                    "api": function_map_v6_to_v7
                },
                DeviceInformationV7.VERSION: {
                    "main_cls": DeviceInformationV7,
                    "api": function_map_v6_to_v7
                },
                DeviceInformationV8.VERSION: {
                    "main_cls": DeviceInformationV8,
                    "api": function_map_v8
                },
            }
        }
    # end def _get_data_model
# end class DeviceInformationModel


class DeviceInformationFactory(FeatureFactory):
    """
    Device Information factory creates a device information object from a given version
    """
    @staticmethod
    def create(version):
        """
        Device information object creation from version number

        :param version: Device information feature version
        :type version: ``int``
        :return: Device information object
        :rtype: ``DeviceInformationInterface``
        """
        return DeviceInformationModel.get_main_cls(version)()
    # end def create
# end class DeviceInformationFactory


class DeviceInformationInterface(FeatureInterface, ABC):
    """
    Interface to device information feature

    Defines required interfaces for device information classes
    """
    def __init__(self):
        self.entity_types = None
        self.get_device_info_cls = None
        self.get_device_info_response_cls = None
        self.get_fw_info_cls = None
        self.get_fw_info_response_cls = None
        self.get_device_serial_number_cls = None
        self.get_device_serial_number_response_cls = None
    # end def __init__
# end class DeviceInformationInterface


class DeviceInformationV1(DeviceInformationInterface):
    """
    DeviceInformation
    This feature provides model and unit specific information

    [0] getDeviceInfo() -> entityCnt, unitId, transport, modelId
    [1] getFwInfo(entityIdx) -> type, fwName, rev, build, active, trPid, extraVer
    """
    VERSION = 1

    def __init__(self):
        super().__init__()
        self.entity_types = DeviceInformationModel.get_base_cls().EntityTypeV1
        self.get_device_info_cls = DeviceInformationModel.get_request_cls(
            self.VERSION, DeviceInformationModel.INDEX.GET_DEVICE_INFO)
        self.get_device_info_response_cls = DeviceInformationModel.get_response_cls(
            self.VERSION, DeviceInformationModel.INDEX.GET_DEVICE_INFO)
        self.get_fw_info_cls = self.get_fw_info_cls = DeviceInformationModel.get_request_cls(
            self.VERSION, DeviceInformationModel.INDEX.GET_FW_INFO)
        self.get_fw_info_response_cls = DeviceInformationModel.get_response_cls(
            self.VERSION, DeviceInformationModel.INDEX.GET_FW_INFO)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`DeviceInformationInterface.get_max_function_index`

        :return: Maximum function index
        :rtype: ``int``
        """
        return DeviceInformationModel.get_base_cls().MAX_FUNCTION_INDEX_V1_TO_V3
    # end def get_max_function_index
# end class DeviceInformationV1


class DeviceInformationV2(DeviceInformationV1):
    """
    DeviceInformation
    This feature provides model and unit specific information

    [0] getDeviceInfo() -> entityCnt, unitId, transport, modelId, extendedModelId
    [1] getFwInfo(entityIdx) -> type, fwName, rev, build, active, trPid, extraVer
    """
    VERSION = 2

    def __init__(self):
        super().__init__()
        self.entity_types = DeviceInformationModel.get_base_cls().EntityTypeV2
    # end def __init__
# end class DeviceInformationV2


class DeviceInformationV3(DeviceInformationV2):
    """
    DeviceInformation
    This feature provides model and unit specific information

    [0] getDeviceInfo() -> entityCnt, unitId, transport, modelId, extendedModelId
    [1] getFwInfo(entityIdx) -> type, fwName, rev, build, active, trPid, extraVer
    """
    VERSION = 3

    def __init__(self):
        super().__init__()
        self.entity_types = DeviceInformationModel.get_base_cls().EntityTypeV3ToV4
    # end def __init__
# end class DeviceInformationV3


class DeviceInformationV4(DeviceInformationV3):
    """
    DeviceInformation
    This feature provides model and unit specific information

    [0] getDeviceInfo() -> entityCnt, unitId, transport, modelId, extendedModelId, capabilities
    [1] getFwInfo(entityIdx) -> type, fwName, rev, build, active, trPid, extraVer
    [2] getDeviceSerialNumber() -> serialNumber
    """
    VERSION = 4

    def __init__(self):
        super().__init__()
        self.get_device_serial_number_cls = DeviceInformationModel.get_request_cls(
            self.VERSION, DeviceInformationModel.INDEX.GET_DEVICE_SERIAL_NUMBER)
        self.get_device_serial_number_response_cls = DeviceInformationModel.get_response_cls(
            self.VERSION, DeviceInformationModel.INDEX.GET_DEVICE_SERIAL_NUMBER)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`DeviceInformationInterface.get_max_function_index`

        :return: Maximum function index
        :rtype: ``int``
        """
        return DeviceInformationModel.get_base_cls().MAX_FUNCTION_INDEX_V4_TO_V8
    # end def get_max_function_index
# end class DeviceInformationV4


class DeviceInformationV5(DeviceInformationV4):
    """
    Define ``DeviceInformationV5`` feature

    This feature provides model and unit specific information for version 5
    """
    VERSION = 5

    def __init__(self):
        super().__init__()
        self.entity_types = DeviceInformationModel.get_base_cls().EntityTypeV5ToV6
    # end def __init__
# end class DeviceInformationV5


class DeviceInformationV6(DeviceInformationV5):
    """
    Define ``DeviceInformationV6`` feature

    This feature provides model and unit specific information for version 6
    """
    VERSION = 6
# end class DeviceInformationV6


class DeviceInformationV7(DeviceInformationV6):
    """
    Define ``DeviceInformationV7`` feature

    This feature provides model and unit specific information for version 7
    """
    VERSION = 7

    def __init__(self):
        super().__init__()
        self.entity_types = DeviceInformationModel.get_base_cls().EntityTypeV7ToV8
    # end def __init__
# end class DeviceInformationV7


class DeviceInformationV8(DeviceInformationV7):
    """
    Define ``DeviceInformationV8`` feature

    This feature provides model and unit specific information for version 8
    """
    VERSION = 8

    def __init__(self):
        super().__init__()
        self.entity_types = DeviceInformationModel.get_base_cls().EntityTypeV7ToV8
    # end def __init__
# end class DeviceInformationV8


class GetDeviceInfoV1ToV8(DeviceInformation):
    """
    Define ``GetDeviceInfoV1ToV8`` implementation class for versions 1 to 8.
    
    Request information that characterises the whole device (as opposed to a particular firmware entity).
    A device may hold multiple firmware entities, including multiple main applications and bootloader.

    The response to this request 'does not depend' on the transport protocol used to carry the request, this is very
    useful when the host SW wants to identify a device that supports more than one communication protocol.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """

    class FID(DeviceInformation.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(DeviceInformation.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
              BitField(fid=FID.PADDING,
                       length=LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=DeviceInformation.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetDeviceInfoResponseV1.FUNCTION_INDEX
    # end def __init__
# end class GetDeviceInfoV1ToV8


class GetDeviceInfoResponseV1(DeviceInformation):
    """
    DeviceInformation GetDeviceInfo response implementation class for version 1.
    
    Returns information that characterises the whole device (as opposed to a particular firmware
    entity).
    A device may hold multiple firmware entities, including multiple main applications and
    bootloader.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    EntityCount                   8
    UnitId                        32
    TransportReserved             12
    USB                           1
    eQuad                         1
    BTLE                          1
    BT                            1
    ModelId                       48
    Padding                       24
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceInfoV1ToV8,)
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(DeviceInformation.FID):
        """
        Field Identifiers
        """
        ENTITY_COUNT = 0xFA
        UNIT_ID = 0xF9
        TRANSPORT_RESERVED = 0xF8
        USB = 0xF7
        EQUAD = 0xF6
        BTLE = 0xF5
        BT = 0xF4
        MODEL_ID = 0xF3
        PADDING = 0xF2
    # end class FID

    class LEN(DeviceInformation.LEN):
        """
        Field Lengths
        """
        ENTITY_COUNT = 0x08
        UNIT_ID = 0x20
        TRANSPORT_RESERVED = 0x0C
        USB = 0x01
        EQUAD = 0x01
        BTLE = 0x01
        BT = 0x01
        MODEL_ID = 0x30
        PADDING = 0x18
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
              BitField(fid=FID.ENTITY_COUNT,
                       length=LEN.ENTITY_COUNT,
                       title='EntityCount',
                       name='entity_count',
                       checks=(CheckHexList(LEN.ENTITY_COUNT // 8), CheckByte(),)),
              BitField(fid=FID.UNIT_ID,
                       length=LEN.UNIT_ID,
                       title='UnitId',
                       name='unit_id',
                       checks=(CheckHexList(LEN.UNIT_ID // 8),)),
              BitField(fid=FID.TRANSPORT_RESERVED,
                       length=LEN.TRANSPORT_RESERVED,
                       title='TransportReserved',
                       name='transport_reserved',
                       checks=(CheckHexList(LEN.TRANSPORT_RESERVED // 8),
                               CheckInt(0, pow(2, LEN.TRANSPORT_RESERVED) - 1),),
                       default_value=HidppMessage.DEFAULT.RESERVED),
              BitField(fid=FID.USB,
                       length=LEN.USB,
                       title='USB',
                       name='usb',
                       checks=(CheckInt(0, pow(2, LEN.USB) - 1),),
                       conversions={HexList: Numeral}),
              BitField(fid=FID.EQUAD,
                       length=LEN.EQUAD,
                       title='eQuad',
                       name='e_quad',
                       checks=(CheckInt(0, pow(2, LEN.EQUAD) - 1),),
                       conversions={HexList: Numeral}),
              BitField(fid=FID.BTLE,
                       length=LEN.BTLE,
                       title='BTLE',
                       name='btle',
                       checks=(CheckInt(0, pow(2, LEN.BTLE) - 1),),
                       conversions={HexList: Numeral}),
              BitField(fid=FID.BT,
                       length=LEN.BT,
                       title='BT',
                       name='bt',
                       checks=(CheckInt(0, pow(2, LEN.BT) - 1),),
                       conversions={HexList: Numeral}),
              BitField(fid=FID.MODEL_ID,
                       length=LEN.MODEL_ID,
                       title='ModelId',
                       name='model_id',
                       checks=(CheckHexList(LEN.MODEL_ID // 8),)),
              BitField(fid=FID.PADDING,
                       length=LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=DeviceInformation.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, entity_count, unit_id, usb, e_quad, btle, bt,
                 model_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param entity_count: Number of entities present in the device
        :type entity_count: ``int | HexList``
        :param unit_id: Four byte random array unit identifier
        :type unit_id: ``HexList``
        :param usb: USB communication protocol support
        :type usb: ``int | HexList | bool``
        :param e_quad: eQuad communication protocol support
        :type e_quad: ``int | HexList | bool``
        :param btle: Bluetooth low energy communication protocol support
        :type btle: ``int | HexList | bool``
        :param bt: Bluetooth communication protocol support
        :type bt: ``int | HexList | bool``
        :param model_id: Array of the PIDs of the different transports supported by the device
        :type model_id: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.entity_count = entity_count
        self.unit_id = unit_id
        self.usb = usb
        self.e_quad = e_quad
        self.btle = btle
        self.bt = bt
        self.model_id = model_id
    # end def __init__
# end class GetDeviceInfoResponseV1


class GetDeviceInfoResponseV2ToV3(GetDeviceInfoResponseV1):
    """
    DeviceInformation GetDeviceInfo response implementation class for version 2 to 3.

    Returns information that characterises the whole device (as opposed to a particular firmware
    entity).
    A device may hold multiple firmware entities, including multiple main applications and
    bootloader.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    EntityCount                   8
    UnitId                        32
    TransportReserved             12
    USB                           1
    eQuad                         1
    BTLE                          1
    BT                            1
    ModelId                       48
    ExtendedModelId               8
    Padding                       16
    ============================  ==========
    """
    VERSION = (2, 3,)

    class FID(GetDeviceInfoResponseV1.FID):
        """
        Field Identifiers
        """
        EXTENDED_MODEL_ID = 0xF2
        PADDING = 0xF1
    # end class FID

    class LEN(GetDeviceInfoResponseV1.LEN):
        """
        Field Lengths
        """
        EXTENDED_MODEL_ID = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = GetDeviceInfoResponseV1.FIELDS[:-1] + (  # Remove the padding field of the parent class
              BitField(fid=FID.EXTENDED_MODEL_ID,
                       length=LEN.EXTENDED_MODEL_ID,
                       title='ExtendedModelId',
                       name='extended_model_id',
                       checks=(CheckHexList(LEN.EXTENDED_MODEL_ID // 8), CheckByte(),)),
              BitField(fid=FID.PADDING,
                       length=LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=DeviceInformation.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, entity_count, unit_id, usb, e_quad, btle, bt,
                 model_id, extended_model_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param entity_count: Number of entities present in the device
        :type entity_count: ``int | HexList``
        :param unit_id: Four byte random array unit identifier
        :type unit_id: ``HexList``
        :param usb: USB communication protocol support
        :type usb: ``int | HexList | bool``
        :param e_quad: eQuad communication protocol support
        :type e_quad: ``int | HexList | bool``
        :param btle: Bluetooth low energy communication protocol support
        :type btle: ``int | HexList | bool``
        :param bt: Bluetooth communication protocol support
        :type bt: ``int | HexList | bool``
        :param model_id: Array of the PIDs of the different transports supported by the device
        :type model_id: ``HexList``
        :param extended_model_id: A 8 bit value that represents a configurable attribute of the device
        :type extended_model_id: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, entity_count, unit_id, usb, e_quad, btle,
                         bt, model_id, **kwargs)

        self.extended_model_id = extended_model_id
    # end def __init__
# end class GetDeviceInfoResponseV2ToV3


class GetDeviceInfoResponseV4ToV5(GetDeviceInfoResponseV2ToV3):
    """
    DeviceInformation GetDeviceInfo response implementation class for versions 4 to 6

    Returns information that characterises the whole device (as opposed to a particular firmware
    entity).
    A device may hold multiple firmware entities, including multiple main applications and
    bootloader.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    EntityCount                   8
    UnitId                        32
    TransportReserved             12
    USB                           1
    eQuad                         1
    BTLE                          1
    BT                            1
    ModelId                       48
    ExtendedModelId               8
    CapabilitiesReserved          7
    SerialNumber                  1
    Padding                       8
    ============================  ==========
    """
    VERSION = (4, 5,)

    class FID(GetDeviceInfoResponseV2ToV3.FID):
        """
        Field Identifiers
        """
        CAPABILITIES_RESERVED = 0xF1
        SERIAL_NUMBER = 0xF0
        PADDING = 0xEF
    # end class FID

    class LEN(GetDeviceInfoResponseV2ToV3.LEN):
        """
        Field Lengths
        """
        CAPABILITIES_RESERVED = 0x07
        SERIAL_NUMBER = 0x01
        PADDING = 0x08
    # end class LEN

    # Remove the padding field of the parent class and add the new fields
    FIELDS = GetDeviceInfoResponseV2ToV3.FIELDS[:-1] + (
        BitField(fid=FID.CAPABILITIES_RESERVED,
                 length=LEN.CAPABILITIES_RESERVED,
                 title='CapabilitiesReserved',
                 name='capabilities_reserved',
                 checks=(CheckInt(max_value=pow(2, LEN.CAPABILITIES_RESERVED) - 1),)),
        BitField(fid=FID.SERIAL_NUMBER,
                 length=LEN.SERIAL_NUMBER,
                 title='SerialNumber',
                 name='serial_number',
                 checks=(CheckInt(max_value=pow(2, LEN.SERIAL_NUMBER) - 1),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DeviceInformation.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, entity_count, unit_id, usb, e_quad, btle, bt,
                 model_id, extended_model_id, serial_number, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param entity_count: Number of entities present in the device
        :type entity_count: ``int | HexList``
        :param unit_id: Four byte random array unit identifier
        :type unit_id: ``HexList``
        :param usb: USB communication protocol support
        :type usb: ``int | HexList | bool``
        :param e_quad: eQuad communication protocol support
        :type e_quad: ``int | HexList | bool``
        :param btle: Bluetooth low energy communication protocol support
        :type btle: ``int | HexList | bool``
        :param bt: Bluetooth communication protocol support
        :type bt: ``int | HexList | bool``
        :param model_id: Array of the PIDs of the different transports supported by the device
        :type model_id: ``HexList``
        :param extended_model_id: 8 bit value that represents a configurable attribute of the device
        :type extended_model_id: ``int | HexList``
        :param serial_number: Serial number support
        :type serial_number: ``int | HexList | bool``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, entity_count, unit_id, usb, e_quad, btle, bt,
                         model_id, extended_model_id, **kwargs)

        self.serial_number = serial_number
    # end def __init__
# end class GetDeviceInfoResponseV4ToV5


class GetDeviceInfoResponseV6ToV8(GetDeviceInfoResponseV4ToV5):
    """
    Define ``GetDeviceInfoResponseV6ToV8`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    EntityCount                   8
    UnitId                        32
    TransportReserved             11
    Serial                        1
    USB                           1
    eQuad                         1
    BTLE                          1
    BT                            1
    ModelId                       48
    ExtendedModelId               8
    CapabilitiesReserved          7
    SerialNumber                  1
    Padding                       8
    ============================  ==========
    """
    VERSION = (6, 7, 8)

    class FID(GetDeviceInfoResponseV4ToV5.FID):
        """
        Field Identifiers
        """
        SERIAL = 0xF7
        USB = 0xF6
        EQUAD = 0xF5
        BTLE = 0xF4
        BT = 0xF3
        MODEL_ID = 0xF2
        EXTENDED_MODEL_ID = 0xF1
        CAPABILITIES_RESERVED = 0xF0
        SERIAL_NUMBER = 0xEF
        PADDING = 0xEE
    # end class FID

    class LEN(GetDeviceInfoResponseV4ToV5.LEN):
        """
        Field Lengths
        """
        TRANSPORT_RESERVED = 0x0B
        SERIAL = 0x01
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
        BitField(fid=FID.ENTITY_COUNT,
                 length=LEN.ENTITY_COUNT,
                 title='EntityCount',
                 name='entity_count',
                 checks=(CheckHexList(LEN.ENTITY_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.UNIT_ID,
                 length=LEN.UNIT_ID,
                 title='UnitId',
                 name='unit_id',
                 checks=(CheckHexList(LEN.UNIT_ID // 8),)),
        BitField(fid=FID.TRANSPORT_RESERVED,
                 length=LEN.TRANSPORT_RESERVED,
                 title='TransportReserved',
                 name='transport_reserved',
                 checks=(CheckHexList(LEN.TRANSPORT_RESERVED // 8),
                         CheckInt(0, pow(2, LEN.TRANSPORT_RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(fid=FID.SERIAL,
                 length=LEN.SERIAL,
                 title='Serial',
                 name='serial',
                 checks=(CheckInt(0, pow(2, LEN.SERIAL) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.USB,
                 length=LEN.USB,
                 title='USB',
                 name='usb',
                 checks=(CheckInt(0, pow(2, LEN.USB) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.EQUAD,
                 length=LEN.EQUAD,
                 title='eQuad',
                 name='e_quad',
                 checks=(CheckInt(0, pow(2, LEN.EQUAD) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.BTLE,
                 length=LEN.BTLE,
                 title='BTLE',
                 name='btle',
                 checks=(CheckInt(0, pow(2, LEN.BTLE) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.BT,
                 length=LEN.BT,
                 title='BT',
                 name='bt',
                 checks=(CheckInt(0, pow(2, LEN.BT) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.MODEL_ID,
                 length=LEN.MODEL_ID,
                 title='ModelId',
                 name='model_id',
                 checks=(CheckHexList(LEN.MODEL_ID // 8),)),
        BitField(fid=FID.EXTENDED_MODEL_ID,
                 length=LEN.EXTENDED_MODEL_ID,
                 title='ExtendedModelId',
                 name='extended_model_id',
                 checks=(CheckHexList(LEN.EXTENDED_MODEL_ID // 8), CheckByte(),)),
        BitField(fid=FID.CAPABILITIES_RESERVED,
                 length=LEN.CAPABILITIES_RESERVED,
                 title='CapabilitiesReserved',
                 name='capabilities_reserved',
                 checks=(CheckInt(max_value=pow(2, LEN.CAPABILITIES_RESERVED) - 1),)),
        BitField(fid=FID.SERIAL_NUMBER,
                 length=LEN.SERIAL_NUMBER,
                 title='SerialNumber',
                 name='serial_number',
                 checks=(CheckInt(max_value=pow(2, LEN.SERIAL_NUMBER) - 1),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=DeviceInformation.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, entity_count, unit_id, serial, usb, e_quad, btle, bt,
                 model_id, extended_model_id, serial_number, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param entity_count: Number of entities present in the device
        :type entity_count: ``int | HexList``
        :param unit_id: Four byte random array unit identifier
        :type unit_id: ``HexList``
        :param serial: serial communication protocol support (can be UART, SPI, ...)
        :type serial: ``int | HexList | bool``
        :param usb: USB communication protocol support
        :type usb: ``int | HexList | bool``
        :param e_quad: eQuad communication protocol support
        :type e_quad: ``int | HexList | bool``
        :param btle: Bluetooth low energy communication protocol support
        :type btle: ``int | HexList | bool``
        :param bt: Bluetooth communication protocol support
        :type bt: ``int | HexList | bool``
        :param model_id: Array of the PIDs of the different transports supported by the device
        :type model_id: ``HexList``
        :param extended_model_id: 8 bit value that represents a configurable attribute of the device
        :type extended_model_id: ``int | HexList``
        :param serial_number: Serial number support
        :type serial_number: ``int | HexList | bool``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, entity_count, unit_id, usb, e_quad, btle, bt, model_id,
                         extended_model_id, serial_number, **kwargs)

        self.serial = serial
    # end def __init__
# end class GetDeviceInfoResponseV6ToV8


class GetFwInfoV1ToV8(DeviceInformation):
    """
    DeviceInformation GetFwInfo implementation class for version 1 to 8.
    
    Request the firmware version for the given entityIdx.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    EntityIndex                   8
    Padding                       16
    ============================  ==========
    """

    class FID(DeviceInformation.FID):
        """
        Field Identifiers
        """
        ENTITY_INDEX = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(DeviceInformation.LEN):
        """
        Field Lengths
        """
        ENTITY_INDEX = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
              BitField(fid=FID.ENTITY_INDEX,
                       length=LEN.ENTITY_INDEX,
                       title='EntityIndex',
                       name='entity_index',
                       checks=(CheckHexList(LEN.ENTITY_INDEX // 8), CheckByte(),),
                       zero_print=True),
              BitField(fid=FID.PADDING,
                       length=LEN.PADDING,
                       title='Padding',
                       name='padding',
                       default_value=DeviceInformation.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, entity_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param entity_index: The index of the entity for which we want to obtain the version
        information
        :type entity_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetFwInfoResponseV1ToV7.FUNCTION_INDEX
        self.entity_index = entity_index
    # end def __init__
# end class GetFwInfoV1ToV8


class GetFwInfoResponseV1ToV7(DeviceInformation):
    """
    DeviceInformation GetFwInfo response class for version 1 to 7.
    
    Returns the firmware version for the given entityIdx.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    FwType                        8
    FwPrefix                      24
    FwNumber                      8
    FwRevision                    8
    FwBuild                       16
    Reserved                      7
    Active                        1
    TransportId                   16
    ExtraVersionInformation       40
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFwInfoV1ToV8,)
    VERSION = (1, 2, 3, 4, 5, 6, 7,)
    FUNCTION_INDEX = 1

    class FID(DeviceInformation.FID):
        """
        Field Identifiers
        """
        FW_TYPE = 0xFA
        FW_PREFIX = 0xF9
        FW_NUMBER = 0xF8
        FW_REVISION = 0xF7
        FW_BUILD = 0xF6
        RESERVED = 0xF5
        ACTIVE = 0xF4
        TRANSPORT_ID = 0xF3
        EXTRA_VERSION_INFORMATION = 0xF2
    # end class FID

    class LEN(DeviceInformation.LEN):
        """
        Field Lengths
        """
        FW_TYPE = 0x08
        FW_PREFIX = 0x18
        FW_NUMBER = 0x08
        FW_REVISION = 0x08
        FW_BUILD = 0x10
        RESERVED = 0x07
        ACTIVE = 0x01
        TRANSPORT_ID = 0x10
        EXTRA_VERSION_INFORMATION = 0x28
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
              BitField(fid=FID.FW_TYPE,
                       length=LEN.FW_TYPE,
                       title='FwType',
                       name='fw_type',
                       checks=(CheckHexList(LEN.FW_TYPE // 8), CheckByte(),)),
              BitField(fid=FID.FW_PREFIX,
                       length=LEN.FW_PREFIX,
                       title='FwPrefix',
                       name='fw_prefix',
                       checks=(CheckHexList(LEN.FW_PREFIX // 8),)),
              BitField(fid=FID.FW_NUMBER,
                       length=LEN.FW_NUMBER,
                       title='FwNumber',
                       name='fw_number',
                       checks=(CheckBCD(LEN.FW_NUMBER // 8),)),
              BitField(fid=FID.FW_REVISION,
                       length=LEN.FW_REVISION,
                       title='FwRevision',
                       name='fw_revision',
                       # TODO according to spec it should be BCD format but there is a bug in HYJAL HERO bootloader
                       #  product that prevent the usage of the CheckBCD function alone.
                       checks=(CheckBCD(LEN.FW_REVISION // 8), CheckHexList(LEN.FW_REVISION // 8))),
              BitField(fid=FID.FW_BUILD,
                       length=LEN.FW_BUILD,
                       title='FwBuild',
                       name='fw_build',
                       # TODO according to spec it should be BCD format but there is a bug for
                       #  the softdevice where it is not. Until a choice is made on how to take
                       #  care of that both are acceptable.
                       checks=(CheckBCD(LEN.FW_BUILD // 8), CheckHexList(LEN.FW_BUILD // 8))),
              BitField(fid=FID.RESERVED,
                       length=LEN.RESERVED,
                       title='Reserved',
                       name='reserved',
                       checks=(CheckHexList(LEN.RESERVED // 8),
                               CheckInt(max_value=pow(2, LEN.RESERVED) - 1),),
                       default_value=HidppMessage.DEFAULT.RESERVED),
              BitField(fid=FID.ACTIVE,
                       length=LEN.ACTIVE,
                       title='Active',
                       name='active',
                       checks=(CheckHexList(LEN.ACTIVE // 8),
                               CheckInt(max_value=pow(2, LEN.ACTIVE) - 1),),
                       conversions={HexList: Numeral}),
              BitField(fid=FID.TRANSPORT_ID,
                       length=LEN.TRANSPORT_ID,
                       title='TransportId',
                       name='transport_id',
                       checks=(CheckHexList(LEN.TRANSPORT_ID // 8),
                               CheckInt(max_value=pow(2, LEN.TRANSPORT_ID) - 1),)),
              BitField(fid=FID.EXTRA_VERSION_INFORMATION,
                       length=LEN.EXTRA_VERSION_INFORMATION,
                       title='ExtraVersionInformation',
                       name='extra_version_information',
                       checks=(CheckHexList(LEN.EXTRA_VERSION_INFORMATION // 8),),
                       default_value=HexList('00' * (LEN.EXTRA_VERSION_INFORMATION // 8))),
              )

    def __init__(self, device_index, feature_index, fw_type, fw_prefix, fw_number, fw_revision,
                 fw_build, active, transport_id, extra_version_information=None, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param fw_type: The entity type
        :type fw_type: ``int | HexList``
        :param fw_prefix: Prefix characters
        :type fw_prefix: ``HexList``
        :param fw_number: Firmware number (BCD format)
        :type fw_number: ``HexList``
        :param fw_revision: Firmware revision (BCD format)
        :type fw_revision: ``HexList``
        :param fw_build: Firmware build (BCD format)
        :type fw_build: ``HexList``
        :param active: This entity is the active entity responding to this hid++ request
        :type active: ``int | HexList | bool``
        :param transport_id: Transport ID (depends on the protocol, USB PID, BT PID, etc...)
        :type transport_id: ``int | HexList``
        :param extra_version_information: Optional extra versioning information - OPTIONAL
        :type extra_version_information: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.fw_type = fw_type
        self.fw_prefix = fw_prefix
        self.fw_number = fw_number
        self.fw_revision = fw_revision
        self.fw_build = fw_build
        self.active = active
        self.transport_id = transport_id
        # Since the last field is optional, it can be ignored.
        if extra_version_information is not None:
            self.extra_version_information = extra_version_information
        # end if
    # end def __init__
# end class GetFwInfoResponseV1ToV7


class GetFwInfoResponseV8(GetFwInfoResponseV1ToV7):
    """
    DeviceInformation GetFwInfo response class for version 8.

    Returns the firmware version for the given entityIdx.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    FwType                        8
    FwPrefix                      24
    FwNumber                      8
    FwRevision                    8
    FwBuild                       16
    Reserved                      5
    SlotId                        1
    Invalid                       1
    Active                        1
    TransportId                   16
    ExtraVersionInformation       40
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetFwInfoV1ToV8,)
    VERSION = (8,)
    FUNCTION_INDEX = 1

    class FID(GetFwInfoResponseV1ToV7.FID):
        """
        Field Identifiers
        """
        SLOT_ID = 0xF4
        INVALID = 0xF3
        ACTIVE = 0xF2
        TRANSPORT_ID = 0xF1
        EXTRA_VERSION_INFORMATION = 0xF0
    # end class FID

    class LEN(GetFwInfoResponseV1ToV7.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x05
        SLOT_ID = 0x01
        INVALID = 0x01
    # end class LEN

    FIELDS = GetFwInfoResponseV1ToV7.FIELDS[:-4] + (
        BitField(fid=FID.RESERVED,
                 length=LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckInt(max_value=pow(2, LEN.RESERVED) - 1),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(fid=FID.SLOT_ID,
                 length=LEN.SLOT_ID,
                 title='SlotId',
                 name='slot_id',
                 checks=(CheckHexList(LEN.SLOT_ID // 8),
                         CheckInt(max_value=pow(2, LEN.SLOT_ID) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.INVALID,
                 length=LEN.INVALID,
                 title='Invalid',
                 name='invalid',
                 checks=(CheckHexList(LEN.INVALID // 8),
                         CheckInt(max_value=pow(2, LEN.INVALID) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.ACTIVE,
                 length=LEN.ACTIVE,
                 title='Active',
                 name='active',
                 checks=(CheckHexList(LEN.ACTIVE // 8),
                         CheckInt(max_value=pow(2, LEN.ACTIVE) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.TRANSPORT_ID,
                 length=LEN.TRANSPORT_ID,
                 title='TransportId',
                 name='transport_id',
                 checks=(CheckHexList(LEN.TRANSPORT_ID // 8),
                         CheckInt(max_value=pow(2, LEN.TRANSPORT_ID) - 1),)),
        BitField(fid=FID.EXTRA_VERSION_INFORMATION,
                 length=LEN.EXTRA_VERSION_INFORMATION,
                 title='ExtraVersionInformation',
                 name='extra_version_information',
                 checks=(CheckHexList(LEN.EXTRA_VERSION_INFORMATION // 8),),
                 default_value=HexList('00' * (LEN.EXTRA_VERSION_INFORMATION // 8))),
    )

    def __init__(self, device_index, feature_index, fw_type, fw_prefix, fw_number, fw_revision,
                 fw_build, slot_id, invalid, active, transport_id, extra_version_information=None, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param fw_type: The entity type
        :type fw_type: ``int | HexList``
        :param fw_prefix: Prefix characters
        :type fw_prefix: ``HexList``
        :param fw_number: Firmware number (BCD format)
        :type fw_number: ``HexList``
        :param fw_revision: Firmware revision (BCD format)
        :type fw_revision: ``HexList``
        :param fw_build: Firmware build (BCD format)
        :type fw_build: ``HexList``
        :param slot_id: Index of the slot on which this entity is stored for multi-slot devices
        :type slot_id: ``int | HexList | bool``
        :param invalid: This entity had failed sanity checks and is considered invalid
        :type invalid: ``int | HexList | bool``
        :param active: This entity is the active entity responding to this hid++ request
        :type active: ``int | HexList | bool``
        :param transport_id: Transport ID (depends on the protocol, USB PID, BT PID, etc...)
        :type transport_id: ``int | HexList``
        :param extra_version_information: Optional extra versioning information - OPTIONAL
        :type extra_version_information: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, fw_type, fw_prefix, fw_number, fw_revision, fw_build, active,
                         transport_id, extra_version_information, **kwargs)

        self.slot_id = slot_id
        self.invalid = invalid
    # end def __init__
# end class GetFwInfoResponseV8


class GetDeviceSerialNumberV4ToV8(DeviceInformation):
    """
    Define ``GetDeviceSerialNumberV4ToV8`` implementation class for versions 4 to 8.

    Request the serial number of the device.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       24
    ============================  ==========
    """

    class FID(DeviceInformation.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(DeviceInformation.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
              BitField(fid=FID.PADDING,
                       length=LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=DeviceInformation.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetDeviceSerialNumberResponseV4ToV8.FUNCTION_INDEX
    # end def __init__
# end class GetDeviceSerialNumberV4ToV8


class GetDeviceSerialNumberResponseV4ToV8(DeviceInformation):
    """
    DeviceInformation GetDeviceSerialNumber response implementation class for versions 4 to 8

    Returns the serial number of the device

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SerialNumber                  96
    Reserved                      32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDeviceSerialNumberV4ToV8,)
    VERSION = (4, 5, 6, 7, 8)
    FUNCTION_INDEX = 2

    class FID(DeviceInformation.FID):
        """
        Field Identifiers
        """
        SERIAL_NUMBER = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(DeviceInformation.LEN):
        """
        Field Lengths
        """
        SERIAL_NUMBER = 0x60
        PADDING = 0x20
    # end class LEN

    FIELDS = DeviceInformation.FIELDS + (
              BitField(fid=FID.SERIAL_NUMBER,
                       length=LEN.SERIAL_NUMBER,
                       title='SerialNumber',
                       name='serial_number',
                       checks=(CheckHexList(LEN.SERIAL_NUMBER // 8), CheckByte(),)),
              BitField(fid=FID.PADDING,
                       length=LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=DeviceInformation.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, serial_number, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param serial_number: Serial number of the device
        :type serial_number: ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.serial_number = serial_number
    # end def __init__
# end class GetDeviceSerialNumberResponseV4ToV8


def ascii_converter(value):
    """
    DEPRECATED

    Converting HexList byte list into letter representation

    :param value: The list of letter to convert
    :type value: ``HexList``

    :return: The ascii string representation of the input value
    :rtype: ``str``
    """
    warn('This function is deprecated, use HexList.ascii_converter instead', DeprecationWarning)
    result = ''
    data_length = len(value)
    for i in range(data_length):
        if value[i] != 0:
            result += chr(value[i])
        # end if
    # end for
    return result
# end def ascii_converter
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
