#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.spidirectaccess
:brief: HID++ 2.0 ``SPIDirectAccess`` command interface definition
:author: YY Liu <yliu5@logitech.com>
:date: 2022/11/21
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
class SPIDirectAccess(HidppMessage):
    """
    This feature is used to have a direct full duplex communication with SPI peripherals.
    """
    FEATURE_ID = 0x1E22
    MAX_FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    class AccessConfig(BitFieldContainerMixin):
        """
        Define ``AccessConfig`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        Enable Atomic Cs              1
        Disable Fw Access             1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            ENABLE_ATOMIC_CS = RESERVED - 1
            DISABLE_FW_ACCESS = ENABLE_ATOMIC_CS - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            ENABLE_ATOMIC_CS = 0x1
            DISABLE_FW_ACCESS = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            ENABLE_ATOMIC_CS = 0x0
            DISABLE_FW_ACCESS = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.ENABLE_ATOMIC_CS, length=LEN.ENABLE_ATOMIC_CS,
                     title="EnableAtomicCs", name="enable_atomic_cs",
                     checks=(CheckInt(0, pow(2, LEN.ENABLE_ATOMIC_CS) - 1),),
                     default_value=DEFAULT.ENABLE_ATOMIC_CS),
            BitField(fid=FID.DISABLE_FW_ACCESS, length=LEN.DISABLE_FW_ACCESS,
                     title="DisableFwAccess", name="disable_fw_access",
                     checks=(CheckInt(0, pow(2, LEN.DISABLE_FW_ACCESS) - 1),),
                     default_value=DEFAULT.DISABLE_FW_ACCESS),
        )
    # end class AccessConfig
# end class SPIDirectAccess


class SPIDirectAccessModel(FeatureModel):
    """
    Define ``SPIDirectAccess`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_NB_DEVICES = 0
        GET_SELECTED_DEVICE = 1
        SELECT_DEVICE = 2
        SPI_DIRECT_ACCESS = 3
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``SPIDirectAccess`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_NB_DEVICES: {
                    "request": GetNbDevices,
                    "response": GetNbDevicesResponse
                },
                cls.INDEX.GET_SELECTED_DEVICE: {
                    "request": GetSelectedDevice,
                    "response": GetSelectedDeviceResponse
                },
                cls.INDEX.SELECT_DEVICE: {
                    "request": SelectDevice,
                    "response": SelectDeviceResponseV0
                },
                cls.INDEX.SPI_DIRECT_ACCESS: {
                    "request": SpiDirectAccess,
                    "response": SpiDirectAccessResponse
                }
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_NB_DEVICES: {
                    "request": GetNbDevices,
                    "response": GetNbDevicesResponse
                },
                cls.INDEX.GET_SELECTED_DEVICE: {
                    "request": GetSelectedDevice,
                    "response": GetSelectedDeviceResponse
                },
                cls.INDEX.SELECT_DEVICE: {
                    "request": SelectDevice,
                    "response": SelectDeviceResponseV1
                },
                cls.INDEX.SPI_DIRECT_ACCESS: {
                    "request": SpiDirectAccess,
                    "response": SpiDirectAccessResponse
                }
            }
        }

        return {
            "feature_base": SPIDirectAccess,
            "versions": {
                SPIDirectAccessV0.VERSION: {
                    "main_cls": SPIDirectAccessV0,
                    "api": function_map_v0
                },
                SPIDirectAccessV1.VERSION: {
                    "main_cls": SPIDirectAccessV1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class SPIDirectAccessModel


class SPIDirectAccessFactory(FeatureFactory):
    """
    Get ``SPIDirectAccess`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``SPIDirectAccess`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``SPIDirectAccessInterface``
        """
        return SPIDirectAccessModel.get_main_cls(version)()
    # end def create
# end class SPIDirectAccessFactory


class SPIDirectAccessInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``SPIDirectAccess``
    """

    def __init__(self):
        # Requests
        self.get_nb_devices_cls = None
        self.get_selected_device_cls = None
        self.select_device_cls = None
        self.spi_direct_access_cls = None

        # Responses
        self.get_nb_devices_response_cls = None
        self.get_selected_device_response_cls = None
        self.select_device_response_cls = None
        self.spi_direct_access_response_cls = None
    # end def __init__
# end class SPIDirectAccessInterface


class SPIDirectAccessV0(SPIDirectAccessInterface):
    """
    Define ``SPIDirectAccessV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetNbDevices() -> numberOfDevices

    [1] GetSelectedDevice() -> deviceIdx, accessConfig

    [2] SelectDevice(deviceIdx, accessConfig) -> deviceIdx, accessConfig

    [3] SpiDirectAccess(nBytes, dataIn1, dataIn2, dataIn3, dataIn4, dataIn5, dataIn6, dataIn7, dataIn8, dataIn9,
     dataIn10, dataIn11, dataIn12, dataIn13, dataIn14, dataIn15) -> nBytes, dataOut1, dataOut2, dataOut3, dataOut4,
     dataOut5, dataOut6, dataOut7, dataOut8, dataOut9, dataOut10, dataOut11, dataOut12, dataOut13, dataOut14,
     dataOut15
    """
    VERSION = 0

    def __init__(self):
        # See ``SPIDirectAccess.__init__``
        super().__init__()
        index = SPIDirectAccessModel.INDEX

        # Requests
        self.get_nb_devices_cls = SPIDirectAccessModel.get_request_cls(
            self.VERSION, index.GET_NB_DEVICES)
        self.get_selected_device_cls = SPIDirectAccessModel.get_request_cls(
            self.VERSION, index.GET_SELECTED_DEVICE)
        self.select_device_cls = SPIDirectAccessModel.get_request_cls(
            self.VERSION, index.SELECT_DEVICE)
        self.spi_direct_access_cls = SPIDirectAccessModel.get_request_cls(
            self.VERSION, index.SPI_DIRECT_ACCESS)

        # Responses
        self.get_nb_devices_response_cls = SPIDirectAccessModel.get_response_cls(
            self.VERSION, index.GET_NB_DEVICES)
        self.get_selected_device_response_cls = SPIDirectAccessModel.get_response_cls(
            self.VERSION, index.GET_SELECTED_DEVICE)
        self.select_device_response_cls = SPIDirectAccessModel.get_response_cls(
            self.VERSION, index.SELECT_DEVICE)
        self.spi_direct_access_response_cls = SPIDirectAccessModel.get_response_cls(
            self.VERSION, index.SPI_DIRECT_ACCESS)
    # end def __init__

    def get_max_function_index(self):
        # See ``SPIDirectAccessInterface.get_max_function_index``
        return SPIDirectAccessModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class SPIDirectAccessV0


class SPIDirectAccessV1(SPIDirectAccessV0):
    # See ``SPIDirectAccessV0``
    VERSION = 1
# end class SPIDirectAccessV1


class ShortEmptyPacketDataFormat(SPIDirectAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetNbDevices
        - GetSelectedDevice

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        PADDING = SPIDirectAccess.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SPIDirectAccess.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class MixedContainer1(SPIDirectAccess):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetSelectedDeviceResponse
        - SelectDeviceResponseV1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device Idx                    8
    Access Config                 8
    Padding                       112
    ============================  ==========
    """

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        DEVICE_IDX = SPIDirectAccess.FID.SOFTWARE_ID - 1
        ACCESS_CONFIG = DEVICE_IDX - 1
        PADDING = ACCESS_CONFIG - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        DEVICE_IDX = 0x8
        ACCESS_CONFIG = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.DEVICE_IDX, length=LEN.DEVICE_IDX,
                 title="DeviceIdx", name="device_idx",
                 checks=(CheckHexList(LEN.DEVICE_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.ACCESS_CONFIG, length=LEN.ACCESS_CONFIG,
                 title="AccessConfig", name="access_config",
                 checks=(CheckHexList(LEN.ACCESS_CONFIG // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SPIDirectAccess.DEFAULT.PADDING),
    )
# end class MixedContainer1


class GetNbDevices(ShortEmptyPacketDataFormat):
    """
    Define ``GetNbDevices`` implementation class for version 0, 1
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetNbDevicesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetNbDevices


class GetNbDevicesResponse(SPIDirectAccess):
    """
    Define ``GetNbDevicesResponse`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Number Of Devices             8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetNbDevices,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        NUMBER_OF_DEVICES = SPIDirectAccess.FID.SOFTWARE_ID - 1
        PADDING = NUMBER_OF_DEVICES - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        NUMBER_OF_DEVICES = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.NUMBER_OF_DEVICES, length=LEN.NUMBER_OF_DEVICES,
                 title="NumberOfDevices", name="number_of_devices",
                 checks=(CheckHexList(LEN.NUMBER_OF_DEVICES // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SPIDirectAccess.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, number_of_devices, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param number_of_devices: Number Of Devices
        :type number_of_devices: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.number_of_devices = number_of_devices
    # end def __init__
# end class GetNbDevicesResponse


class GetSelectedDevice(ShortEmptyPacketDataFormat):
    """
    Define ``GetSelectedDevice`` implementation class for version 0, 1
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSelectedDeviceResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetSelectedDevice


class GetSelectedDeviceResponse(MixedContainer1):
    """
    Define ``GetSelectedDeviceResponse`` implementation class for version 0, 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSelectedDevice,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, device_idx, enable_atomic_cs, disable_fw_access, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param device_idx: Device Idx
        :type device_idx: ``int|HexList``
        :param enable_atomic_cs: Enable Atomic Cs
        :type enable_atomic_cs: ``bool|HexList``
        :param disable_fw_access: Disable Fw Access
        :type disable_fw_access: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_idx = device_idx
        self.access_config = self.AccessConfig(enable_atomic_cs=enable_atomic_cs,
                                               disable_fw_access=disable_fw_access)
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
        :rtype: ``GetSelectedDeviceResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.access_config = cls.AccessConfig.fromHexList(
            inner_field_container_mixin.access_config)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSelectedDeviceResponse


class SelectDevice(SPIDirectAccess):
    """
    Define ``SelectDevice`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Device Idx                    8
    Access Config                 8
    Padding                       8
    ============================  ==========
    """

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        DEVICE_IDX = SPIDirectAccess.FID.SOFTWARE_ID - 1
        ACCESS_CONFIG = DEVICE_IDX - 1
        PADDING = ACCESS_CONFIG - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        DEVICE_IDX = 0x8
        ACCESS_CONFIG = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.DEVICE_IDX, length=LEN.DEVICE_IDX,
                 title="DeviceIdx", name="device_idx",
                 checks=(CheckHexList(LEN.DEVICE_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.ACCESS_CONFIG, length=LEN.ACCESS_CONFIG,
                 title="AccessConfig", name="access_config",
                 checks=(CheckHexList(LEN.ACCESS_CONFIG // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SPIDirectAccess.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, device_idx, access_config, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param device_idx: Device Idx
        :type device_idx: ``int|HexList``
        :param access_config: Access Config
        :type access_config: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SelectDeviceResponseV0.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.device_idx = device_idx
        self.access_config = access_config
    # end def __init__
# end class SelectDevice


class SelectDeviceResponseV0(SPIDirectAccess):
    """
    Define ``SelectDeviceResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SelectDevice,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        DEVICE_IDX = SPIDirectAccess.FID.SOFTWARE_ID - 1
        PADDING = DEVICE_IDX - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        DEVICE_IDX = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.DEVICE_IDX, length=LEN.DEVICE_IDX,
                 title="DeviceIdx", name="device_idx",
                 checks=(CheckHexList(LEN.DEVICE_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SPIDirectAccess.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, device_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param device_idx: Device Idx
        :type device_idx: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_idx = device_idx
    # end def __init__
# end class SelectDeviceResponseV0


class SelectDeviceResponseV1(MixedContainer1):
    """
    Define ``SelectDeviceResponse`` implementation class for version 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SelectDevice,)
    VERSION = (1,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, device_idx, enable_atomic_cs, disable_fw_access, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param device_idx: Device Idx
        :type device_idx: ``int|HexList``
        :param enable_atomic_cs: Enable Atomic Cs
        :type enable_atomic_cs: ``bool|HexList``
        :param disable_fw_access: Disable Fw Access
        :type disable_fw_access: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.device_idx = device_idx
        self.access_config = self.AccessConfig(enable_atomic_cs=enable_atomic_cs,
                                               disable_fw_access=disable_fw_access)
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
        :rtype: ``SelectDeviceResponseV1``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.access_config = cls.AccessConfig.fromHexList(
            inner_field_container_mixin.access_config)
        return inner_field_container_mixin
    # end def fromHexList
# end class SelectDeviceResponseV1


class SpiDirectAccess(SPIDirectAccess):
    """
    Define ``SpiDirectAccess`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    N Bytes                       8
    Data In 1                     8
    Data In 2                     8
    Data In 3                     8
    Data In 4                     8
    Data In 5                     8
    Data In 6                     8
    Data In 7                     8
    Data In 8                     8
    Data In 9                     8
    Data In 10                    8
    Data In 11                    8
    Data In 12                    8
    Data In 13                    8
    Data In 14                    8
    Data In 15                    8
    ============================  ==========
    """

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        N_BYTES = SPIDirectAccess.FID.SOFTWARE_ID - 1
        DATA_IN_1 = N_BYTES - 1
        DATA_IN_2 = DATA_IN_1 - 1
        DATA_IN_3 = DATA_IN_2 - 1
        DATA_IN_4 = DATA_IN_3 - 1
        DATA_IN_5 = DATA_IN_4 - 1
        DATA_IN_6 = DATA_IN_5 - 1
        DATA_IN_7 = DATA_IN_6 - 1
        DATA_IN_8 = DATA_IN_7 - 1
        DATA_IN_9 = DATA_IN_8 - 1
        DATA_IN_10 = DATA_IN_9 - 1
        DATA_IN_11 = DATA_IN_10 - 1
        DATA_IN_12 = DATA_IN_11 - 1
        DATA_IN_13 = DATA_IN_12 - 1
        DATA_IN_14 = DATA_IN_13 - 1
        DATA_IN_15 = DATA_IN_14 - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        N_BYTES = 0x8
        DATA_IN_1 = 0x8
        DATA_IN_2 = 0x8
        DATA_IN_3 = 0x8
        DATA_IN_4 = 0x8
        DATA_IN_5 = 0x8
        DATA_IN_6 = 0x8
        DATA_IN_7 = 0x8
        DATA_IN_8 = 0x8
        DATA_IN_9 = 0x8
        DATA_IN_10 = 0x8
        DATA_IN_11 = 0x8
        DATA_IN_12 = 0x8
        DATA_IN_13 = 0x8
        DATA_IN_14 = 0x8
        DATA_IN_15 = 0x8
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.N_BYTES, length=LEN.N_BYTES,
                 title="NBytes", name="n_bytes",
                 checks=(CheckHexList(LEN.N_BYTES // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_1, length=LEN.DATA_IN_1,
                 title="DataIn1", name="data_in_1",
                 checks=(CheckHexList(LEN.DATA_IN_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_2, length=LEN.DATA_IN_2,
                 title="DataIn2", name="data_in_2",
                 checks=(CheckHexList(LEN.DATA_IN_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_3, length=LEN.DATA_IN_3,
                 title="DataIn3", name="data_in_3",
                 checks=(CheckHexList(LEN.DATA_IN_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_4, length=LEN.DATA_IN_4,
                 title="DataIn4", name="data_in_4",
                 checks=(CheckHexList(LEN.DATA_IN_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_5, length=LEN.DATA_IN_5,
                 title="DataIn5", name="data_in_5",
                 checks=(CheckHexList(LEN.DATA_IN_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_6, length=LEN.DATA_IN_6,
                 title="DataIn6", name="data_in_6",
                 checks=(CheckHexList(LEN.DATA_IN_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_7, length=LEN.DATA_IN_7,
                 title="DataIn7", name="data_in_7",
                 checks=(CheckHexList(LEN.DATA_IN_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_8, length=LEN.DATA_IN_8,
                 title="DataIn8", name="data_in_8",
                 checks=(CheckHexList(LEN.DATA_IN_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_9, length=LEN.DATA_IN_9,
                 title="DataIn9", name="data_in_9",
                 checks=(CheckHexList(LEN.DATA_IN_9 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_10, length=LEN.DATA_IN_10,
                 title="DataIn10", name="data_in_10",
                 checks=(CheckHexList(LEN.DATA_IN_10 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_11, length=LEN.DATA_IN_11,
                 title="DataIn11", name="data_in_11",
                 checks=(CheckHexList(LEN.DATA_IN_11 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_12, length=LEN.DATA_IN_12,
                 title="DataIn12", name="data_in_12",
                 checks=(CheckHexList(LEN.DATA_IN_12 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_13, length=LEN.DATA_IN_13,
                 title="DataIn13", name="data_in_13",
                 checks=(CheckHexList(LEN.DATA_IN_13 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_14, length=LEN.DATA_IN_14,
                 title="DataIn14", name="data_in_14",
                 checks=(CheckHexList(LEN.DATA_IN_14 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_IN_15, length=LEN.DATA_IN_15,
                 title="DataIn15", name="data_in_15",
                 checks=(CheckHexList(LEN.DATA_IN_15 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, n_bytes, data_in_1, data_in_2, data_in_3, data_in_4, data_in_5,
                 data_in_6, data_in_7, data_in_8, data_in_9, data_in_10, data_in_11, data_in_12, data_in_13, data_in_14,
                 data_in_15, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param n_bytes: N Bytes
        :type n_bytes: ``int|HexList``
        :param data_in_1: Data In 1
        :type data_in_1: ``int|HexList``
        :param data_in_2: Data In 2
        :type data_in_2: ``int|HexList``
        :param data_in_3: Data In 3
        :type data_in_3: ``int|HexList``
        :param data_in_4: Data In 4
        :type data_in_4: ``int|HexList``
        :param data_in_5: Data In 5
        :type data_in_5: ``int|HexList``
        :param data_in_6: Data In 6
        :type data_in_6: ``int|HexList``
        :param data_in_7: Data In 7
        :type data_in_7: ``int|HexList``
        :param data_in_8: Data In 8
        :type data_in_8: ``int|HexList``
        :param data_in_9: Data In 9
        :type data_in_9: ``int|HexList``
        :param data_in_10: Data In 10
        :type data_in_10: ``int|HexList``
        :param data_in_11: Data In 11
        :type data_in_11: ``int|HexList``
        :param data_in_12: Data In 12
        :type data_in_12: ``int|HexList``
        :param data_in_13: Data In 13
        :type data_in_13: ``int|HexList``
        :param data_in_14: Data In 14
        :type data_in_14: ``int|HexList``
        :param data_in_15: Data In 15
        :type data_in_15: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SpiDirectAccessResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.n_bytes = n_bytes
        self.data_in_1 = data_in_1
        self.data_in_2 = data_in_2
        self.data_in_3 = data_in_3
        self.data_in_4 = data_in_4
        self.data_in_5 = data_in_5
        self.data_in_6 = data_in_6
        self.data_in_7 = data_in_7
        self.data_in_8 = data_in_8
        self.data_in_9 = data_in_9
        self.data_in_10 = data_in_10
        self.data_in_11 = data_in_11
        self.data_in_12 = data_in_12
        self.data_in_13 = data_in_13
        self.data_in_14 = data_in_14
        self.data_in_15 = data_in_15
    # end def __init__
# end class SpiDirectAccess


class SpiDirectAccessResponse(SPIDirectAccess):
    """
    Define ``SpiDirectAccessResponse`` implementation class for version 0, 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    N Bytes                       8
    Data Out 1                    8
    Data Out 2                    8
    Data Out 3                    8
    Data Out 4                    8
    Data Out 5                    8
    Data Out 6                    8
    Data Out 7                    8
    Data Out 8                    8
    Data Out 9                    8
    Data Out 10                   8
    Data Out 11                   8
    Data Out 12                   8
    Data Out 13                   8
    Data Out 14                   8
    Data Out 15                   8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SpiDirectAccess,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

    class FID(SPIDirectAccess.FID):
        # See ``SPIDirectAccess.FID``
        N_BYTES = SPIDirectAccess.FID.SOFTWARE_ID - 1
        DATA_OUT_1 = N_BYTES - 1
        DATA_OUT_2 = DATA_OUT_1 - 1
        DATA_OUT_3 = DATA_OUT_2 - 1
        DATA_OUT_4 = DATA_OUT_3 - 1
        DATA_OUT_5 = DATA_OUT_4 - 1
        DATA_OUT_6 = DATA_OUT_5 - 1
        DATA_OUT_7 = DATA_OUT_6 - 1
        DATA_OUT_8 = DATA_OUT_7 - 1
        DATA_OUT_9 = DATA_OUT_8 - 1
        DATA_OUT_10 = DATA_OUT_9 - 1
        DATA_OUT_11 = DATA_OUT_10 - 1
        DATA_OUT_12 = DATA_OUT_11 - 1
        DATA_OUT_13 = DATA_OUT_12 - 1
        DATA_OUT_14 = DATA_OUT_13 - 1
        DATA_OUT_15 = DATA_OUT_14 - 1
    # end class FID

    class LEN(SPIDirectAccess.LEN):
        # See ``SPIDirectAccess.LEN``
        N_BYTES = 0x8
        DATA_OUT_1 = 0x8
        DATA_OUT_2 = 0x8
        DATA_OUT_3 = 0x8
        DATA_OUT_4 = 0x8
        DATA_OUT_5 = 0x8
        DATA_OUT_6 = 0x8
        DATA_OUT_7 = 0x8
        DATA_OUT_8 = 0x8
        DATA_OUT_9 = 0x8
        DATA_OUT_10 = 0x8
        DATA_OUT_11 = 0x8
        DATA_OUT_12 = 0x8
        DATA_OUT_13 = 0x8
        DATA_OUT_14 = 0x8
        DATA_OUT_15 = 0x8
    # end class LEN

    FIELDS = SPIDirectAccess.FIELDS + (
        BitField(fid=FID.N_BYTES, length=LEN.N_BYTES,
                 title="NBytes", name="n_bytes",
                 checks=(CheckHexList(LEN.N_BYTES // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_1, length=LEN.DATA_OUT_1,
                 title="DataOut1", name="data_out_1",
                 checks=(CheckHexList(LEN.DATA_OUT_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_2, length=LEN.DATA_OUT_2,
                 title="DataOut2", name="data_out_2",
                 checks=(CheckHexList(LEN.DATA_OUT_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_3, length=LEN.DATA_OUT_3,
                 title="DataOut3", name="data_out_3",
                 checks=(CheckHexList(LEN.DATA_OUT_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_4, length=LEN.DATA_OUT_4,
                 title="DataOut4", name="data_out_4",
                 checks=(CheckHexList(LEN.DATA_OUT_4 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_5, length=LEN.DATA_OUT_5,
                 title="DataOut5", name="data_out_5",
                 checks=(CheckHexList(LEN.DATA_OUT_5 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_6, length=LEN.DATA_OUT_6,
                 title="DataOut6", name="data_out_6",
                 checks=(CheckHexList(LEN.DATA_OUT_6 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_7, length=LEN.DATA_OUT_7,
                 title="DataOut7", name="data_out_7",
                 checks=(CheckHexList(LEN.DATA_OUT_7 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_8, length=LEN.DATA_OUT_8,
                 title="DataOut8", name="data_out_8",
                 checks=(CheckHexList(LEN.DATA_OUT_8 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_9, length=LEN.DATA_OUT_9,
                 title="DataOut9", name="data_out_9",
                 checks=(CheckHexList(LEN.DATA_OUT_9 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_10, length=LEN.DATA_OUT_10,
                 title="DataOut10", name="data_out_10",
                 checks=(CheckHexList(LEN.DATA_OUT_10 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_11, length=LEN.DATA_OUT_11,
                 title="DataOut11", name="data_out_11",
                 checks=(CheckHexList(LEN.DATA_OUT_11 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_12, length=LEN.DATA_OUT_12,
                 title="DataOut12", name="data_out_12",
                 checks=(CheckHexList(LEN.DATA_OUT_12 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_13, length=LEN.DATA_OUT_13,
                 title="DataOut13", name="data_out_13",
                 checks=(CheckHexList(LEN.DATA_OUT_13 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_14, length=LEN.DATA_OUT_14,
                 title="DataOut14", name="data_out_14",
                 checks=(CheckHexList(LEN.DATA_OUT_14 // 8),
                         CheckByte(),)),
        BitField(fid=FID.DATA_OUT_15, length=LEN.DATA_OUT_15,
                 title="DataOut15", name="data_out_15",
                 checks=(CheckHexList(LEN.DATA_OUT_15 // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, n_bytes, data_out_1, data_out_2, data_out_3, data_out_4, data_out_5,
                 data_out_6, data_out_7, data_out_8, data_out_9, data_out_10, data_out_11, data_out_12, data_out_13,
                 data_out_14, data_out_15, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param n_bytes: N Bytes
        :type n_bytes: ``int|HexList``
        :param data_out_1: Data Out 1
        :type data_out_1: ``int|HexList``
        :param data_out_2: Data Out 2
        :type data_out_2: ``int|HexList``
        :param data_out_3: Data Out 3
        :type data_out_3: ``int|HexList``
        :param data_out_4: Data Out 4
        :type data_out_4: ``int|HexList``
        :param data_out_5: Data Out 5
        :type data_out_5: ``int|HexList``
        :param data_out_6: Data Out 6
        :type data_out_6: ``int|HexList``
        :param data_out_7: Data Out 7
        :type data_out_7: ``int|HexList``
        :param data_out_8: Data Out 8
        :type data_out_8: ``int|HexList``
        :param data_out_9: Data Out 9
        :type data_out_9: ``int|HexList``
        :param data_out_10: Data Out 10
        :type data_out_10: ``int|HexList``
        :param data_out_11: Data Out 11
        :type data_out_11: ``int|HexList``
        :param data_out_12: Data Out 12
        :type data_out_12: ``int|HexList``
        :param data_out_13: Data Out 13
        :type data_out_13: ``int|HexList``
        :param data_out_14: Data Out 14
        :type data_out_14: ``int|HexList``
        :param data_out_15: Data Out 15
        :type data_out_15: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.n_bytes = n_bytes
        self.data_out_1 = data_out_1
        self.data_out_2 = data_out_2
        self.data_out_3 = data_out_3
        self.data_out_4 = data_out_4
        self.data_out_5 = data_out_5
        self.data_out_6 = data_out_6
        self.data_out_7 = data_out_7
        self.data_out_8 = data_out_8
        self.data_out_9 = data_out_9
        self.data_out_10 = data_out_10
        self.data_out_11 = data_out_11
        self.data_out_12 = data_out_12
        self.data_out_13 = data_out_13
        self.data_out_14 = data_out_14
        self.data_out_15 = data_out_15
    # end def __init__
# end class SpiDirectAccessResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
