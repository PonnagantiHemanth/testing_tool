#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.dfu
    :brief: HID++ 2.0 DFU command interface definition
    :author: Stanislas Cottard
    :date: 2019/06/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckInt
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pylibrary.tools.hexlist import HexList
from Crypto.Cipher import AES
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuModel(FeatureModel):
    """
    Dfu feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        DFU_CMD_DATA_0 = 0
        DFU_CMD_DATA_1 = 1
        DFU_CMD_DATA_2 = 2
        DFU_CMD_DATA_3 = 3
        DFU_START = 4
        RESTART = 5
    # end class

    @classmethod
    def _get_data_model(cls):
        """
        Device information feature data model
        """
        return {
            "feature_base": Dfu,
            "versions": {
                DfuV0.VERSION: {
                    "main_cls": DfuV0,
                    "api": {
                        "functions": {
                            cls.INDEX.DFU_CMD_DATA_0: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_1: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_2: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_3: {"request": DfuCmdDataXCmd3, "response": DfuStatusResponse},
                            cls.INDEX.DFU_START: {"request": DfuStartV0, "response": DfuStatusResponse},
                            cls.INDEX.RESTART: {"request": Restart, "response": RestartResponse},
                        },
                        "events": {
                           0: {"report": DfuStatusEvent}
                        }
                    },
                },
                DfuV1.VERSION: {
                    "main_cls": DfuV1,
                    "api": {
                        "functions": {
                            cls.INDEX.DFU_CMD_DATA_0: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_1: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_2: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_3: {"request": DfuCmdDataXCmd3, "response": DfuStatusResponse},
                            cls.INDEX.DFU_START: {"request": DfuStartV1, "response": DfuStatusResponse},
                            cls.INDEX.RESTART: {"request": Restart, "response": RestartResponse},
                        },
                        "events": {
                           0: {"report": DfuStatusEvent}
                        }
                    },
                },
                DfuV2.VERSION: {
                    "main_cls": DfuV2,
                    "api": {
                        "functions": {
                            cls.INDEX.DFU_CMD_DATA_0: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_1: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_2: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_3: {"request": DfuCmdDataXCmd3, "response": DfuStatusResponse},
                            cls.INDEX.DFU_START: {"request": DfuStartV2, "response": DfuStatusResponse},
                            cls.INDEX.RESTART: {"request": Restart, "response": RestartResponse},
                        },
                        "events": {
                           0: {"report": DfuStatusEvent}
                        }
                    },
                },
                DfuV3.VERSION: {
                    "main_cls": DfuV3,
                    "api": {
                        "functions": {
                            cls.INDEX.DFU_CMD_DATA_0: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_1: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_2: {"request": DfuCmdDataXCmd1or2, "response": DfuStatusResponse},
                            cls.INDEX.DFU_CMD_DATA_3: {"request": DfuCmdDataXCmd3, "response": DfuStatusResponse},
                            cls.INDEX.DFU_START: {"request": DfuStartV2, "response": DfuStatusResponse},
                            cls.INDEX.RESTART: {"request": Restart, "response": RestartResponse},
                        },
                        "events": {
                           0: {"report": DfuStatusEvent}
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class DfuModel


class DfuFactory(FeatureFactory):
    """
    Dfu factory creates a Dfu object from a given version
    """
    @staticmethod
    def create(version):
        """
        Dfu object creation from version number

        :param version: Dfu feature version
        :type version: ``int``
        :return: Dfu object
        :rtype: ``DfuInterface``
        """
        return DfuModel.get_main_cls(version)()
    # end def create
# end class DfuFactory


class DfuInterface(FeatureInterface, ABC):
    """
    Interface to Dfu feature

    Defines required interfaces for Dfu classes
    """
    def __init__(self):
        """
        Constructor
        """
        # Requests
        self.dfu_cmd_data0_cls = None
        self.dfu_cmd_data1_cls = None
        self.dfu_cmd_data2_cls = None
        self.dfu_cmd_data3_cls = None
        self.dfu_start_cls = None
        self.restart_cls = None

        # Responses
        self.dfu_cmd_data0_response_cls = None
        self.dfu_cmd_data1_response_cls = None
        self.dfu_cmd_data2_response_cls = None
        self.dfu_cmd_data3_response_cls = None
        self.dfu_start_response_cls = None
        self.restart_response_cls = None
    # end def __init__
# end class DfuInterface


class DfuV0(DfuInterface):
    """
    Dfu
    This feature provides model and unit specific information

    [0] dfuCmdData0(cmd, param) ? pktNb, status, param
    [1] dfuCmdData1(cmd, param) ? pktNb, status, param
    [2] dfuCmdData2(cmd, param) ? pktNb, status, param
    [3] dfuCmdData3(cmd, param) ? pktNb, status, param
    [4] dfuStart(fwEntity, encrypt, magicStrg) ? pktNb, status, param
    [5] restart(fwEntity) ? pktNb, status, param

    [event0] dfuStatus() ? pktNb, status, param
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`DfuInterface.__init__`
        """
        super().__init__()
        self.dfu_cmd_data0_cls = DfuModel.get_request_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_0)
        self.dfu_cmd_data1_cls = DfuModel.get_request_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_1)
        self.dfu_cmd_data2_cls = DfuModel.get_request_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_2)
        self.dfu_cmd_data3_cls = DfuModel.get_request_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_3)
        self.dfu_start_cls = DfuModel.get_request_cls(
            self.VERSION, DfuModel.INDEX.DFU_START)
        self.restart_cls = DfuModel.get_request_cls(
            self.VERSION, DfuModel.INDEX.RESTART)

        self.dfu_cmd_data0_response_cls = DfuModel.get_response_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_0)
        self.dfu_cmd_data1_response_cls = DfuModel.get_response_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_1)
        self.dfu_cmd_data2_response_cls = DfuModel.get_response_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_2)
        self.dfu_cmd_data3_response_cls = DfuModel.get_response_cls(
            self.VERSION, DfuModel.INDEX.DFU_CMD_DATA_3)
        self.dfu_start_response_cls = DfuModel.get_response_cls(
            self.VERSION, DfuModel.INDEX.DFU_START)
        self.restart_response_cls = DfuModel.get_response_cls(
            self.VERSION, DfuModel.INDEX.RESTART)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`Dfu.get_max_function_index`
        """
        return DfuModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class DfuV0


class DfuV1(DfuV0):
    """
    Differences from the previous version:
    [4] dfuStart(fwEntity, encrypt, magicStrg, flag) ? pktNb, status, param
    """
    VERSION = 1
# class DfuV1


class DfuV2(DfuV1):
    """
    Differences from the previous version:
    [4] dfuStart(fwEntity, encrypt, magicStrg, flag, securLvl) ? pktNb, status, param
    """
    VERSION = 2
# class DfuV2


class DfuV3(DfuV2):
    """
    Differences from the previous version:
    Add pre-requisite error to allow reporting the absence of a required entity.
    """
    VERSION = 3
# class DfuV3


class Dfu(HidppMessage):
    """
    DFU implementation class

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
    FEATURE_ID = 0x00D0
    MAX_FUNCTION_INDEX = 5
    VERSIONS_LIST = (0, 1, 2, 3,)

    class CommandId:
        """
        Command IDs
        """
        SUPPLY_PROGRAM_DATA = 1
        SUPPLY_CHECK_DATA = 2
        CHECK_AND_VALIDATE_FIRMWARE = 3
    # end class COMMAND_ID

    class EncryptionMode:
        """
        Command IDs
        """
        INVALID = 0
        CLEAR_TEXT = 1
        AES_CBC = 2
        AES_CFB = 3
        AES_OFB = 4
        RESERVED = 5  # 5 .. 0xFF are reserved for future encryption modes
    # end class COMMAND_ID

    # This is used to map the AES encryption mode from the EncryptionMode class to those from the standard AES library
    AES_ENCRYPTION_MODE_MAPPING = {
        EncryptionMode.AES_CBC: AES.MODE_CBC,
        EncryptionMode.AES_CFB: AES.MODE_CFB,
        EncryptionMode.AES_OFB: AES.MODE_OFB,
    }

    # This is used to map the AES encryption mode from the EncryptionMode class to those from the standard AES library
    AES_ENCRYPTION_MODE_STR_MAPPING = {
        EncryptionMode.AES_CBC: 'AES-CBC',
        EncryptionMode.AES_CFB: 'AES-CFB',
        EncryptionMode.AES_OFB: 'AES-OFB',
    }

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        # All messages in 0x00D0 are 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class Dfu


class _DfuStatus(Dfu):
    """
    Dfu _DfuStatus

    This object is used for every response (except Restart) and event in 0x00D0.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    PktNb                         32
    Status                        8
    Params                        88
    ============================  ==========
    """

    class StatusValue:
        NO_STATUS = (0x00, 0x80,)
        PACKET_SUCCESS = (0x01, 0x81,)
        DFU_SUCCESS = (0x02, 0x82,)
        ALL_DFU_SUCCESS = (0x02, 0x82, 0x06, 0x86,)
        WAIT_FOR_EVENT = (0x03, 0x83,)
        GENERIC_ERROR = (0x04, 0x84,)
        DFU_SUCCESS_ENTITY_RESTART_REQUIRED = (0x05, 0x85,)
        DFU_SUCCESS_SYSTEM_RESTART_REQUIRED = (0x06, 0x86,)
        UNKNOWN_ERROR = (0x10, 0x90,)
        BAD_POWER = (0x11, 0x91,)
        UNSUPPORTED_FIRMWARE_ENTITY = (0x12, 0x92,)
        UNSUPPORTED_ENCRYPTION_MODE = (0x13, 0x93,)
        BAD_MAGIC_STRING = (0x14, 0x94,)
        INVALIDATION_FAILURE = (0x15, 0x95,)
        DFU_NOT_STARTED = (0x16, 0x96,)
        BAD_SEQUENCE_NUMBER = (0x17, 0x97,)
        UNSUPPORTED_COMMAND = (0x18, 0x98,)
        COMMAND_IN_PROGRESS = (0x19, 0x99,)
        ADDRESS_SIZE_COMBINATION_OUT_OF_RANGE = (0x1A, 0x9A,)
        UNALIGNED_ADDRESS = (0x1B, 0x9B,)
        BAD_SIZE = (0x1C, 0x9C,)
        MISSING_PROGRAM_DATA = (0x1D, 0x9D,)
        MISSING_CHECK_DATA = (0x1E, 0x9E,)
        PROGRAM_CHECK_DATA_WRITE_FAILURE = (0x1F, 0x9F,)
        PROGRAM_CHECK_DATA_VERIFY_FAILURE = (0x20, 0xA0,)
        BAD_FIRMWARE = (0x21, 0xA1,)
        FIRMWARE_CHECK_FAILURE = (0x22, 0xA2,)
        BLOCKED_COMMAND = (0x23, 0xA3,)
        ERASE_ABORT_IN_PROGRESS = (0x24, 0xA4,)
        BAD_INCOMPATIBLE_FLAG_FIELD = (0x25, 0xA5,)
        PROGRAM_CHECK_DATA_DECRYPTION_FAILURE = (0x26, 0xA6,)
        BAD_INCOMPATIBLE_SECURITY_LEVEL = (0x27, 0xA7,)
        MISSING_PRE_REQUISITE = (0x28, 0xA8,)
        # end class StatusValue

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        PKT_NB = 0xFA
        STATUS = 0xF9
        PARAMS = 0xF8
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        PKT_NB = 0x20
        STATUS = 0x08
        PARAMS = 0x58
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.PKT_NB,
                 LEN.PKT_NB,
                 0x00,
                 0x00,
                 title='PktNb',
                 name='pkt_nb',
                 checks=(CheckHexList(LEN.PKT_NB // 8), CheckInt(max_value=pow(2, LEN.PKT_NB) - 1),)),
        BitField(FID.STATUS,
                 LEN.STATUS,
                 0x00,
                 0x00,
                 title='Status',
                 name='status',
                 checks=(CheckHexList(LEN.STATUS // 8), CheckByte(),)),
        BitField(FID.PARAMS,
                 LEN.PARAMS,
                 0x00,
                 0x00,
                 title='Params',
                 name='params',
                 checks=(CheckHexList(LEN.PARAMS // 8), CheckInt(max_value=pow(2, LEN.PARAMS) - 1),)),
    )

    def __init__(self, device_index, feature_index, pkt_nb, status, params, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param pkt_nb: The package number
        :type pkt_nb: ``int``
        :param status: Raw value on y
        :type status: ``int``
        :param params: Status parameters (e.g., debug information). Type int is for the value 0
        :type status: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.pkt_nb = pkt_nb
        self.status = status
        self.params = params
    # end def __init__
# end class _DfuStatus


class _DfuCmdDataXCmd(Dfu):
    """
    Dfu _DfuCmdDataX implementation class

    This can be used as base class for:
    [0] dfuCmdData0(cmd, param) -> pktNb, status, param
    [1] dfuCmdData1(cmd, param) -> pktNb, status, param
    [2] dfuCmdData2(cmd, param) -> pktNb, status, param
    [3] dfuCmdData3(cmd, param) -> pktNb, status, param

    These functions are used to send the stream of command and data packets, which constitutes a DFU. After invoking
    the function "DfuStart", a series of commands shall be sent, each of them followed by a given number (possibly zero)
    of data packets. The software shall stop the stream if the check-and-validate command (3) completes successfully or
    after an error.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Cmd                           8
    Params                        120
    ============================  ==========
    """

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        CMD = 0xFA
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        CMD = 0x08
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.CMD,
                 LEN.CMD,
                 0x00,
                 0x00,
                 title='Cmd',
                 name='cmd',
                 checks=(CheckHexList(LEN.CMD // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, function_index, cmd, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param function_index: Number that represent the function_index:
                                0 -> dfuCmdData0
                                1 -> dfuCmdData1
                                2 -> dfuCmdData2
                                3 -> dfuCmdData3
        :type function_index: ``int``
        :param cmd: The command number
        :type cmd: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = function_index
        self.cmd = cmd
    # end def __init__
# end class _DfuCmdDataXCmd


class DfuCmdDataXCmd1or2(_DfuCmdDataXCmd):
    """
    Dfu DfuCmdDataXCmd1or2 implementation class

    The value 1. Provides firmware update payload data it is followed by "ceil(size/16)" data packets.

    The value 2. This command is used to provide mandatory check data. An insecure DFU may use an error-detection
    code (e.g., CRC) to protect against transmission errors. A secure DFU may use a cryptographic signature.
    The check data is implementation specific, but shall have at least 16 bits. Also, simple sums shall be ruled out.
    In other words, the check data should be at least "as strong as a 16-bit CRC". This command is followed by
    "ceil(size/16)" data packets. As check data is assumed to be small, an implementation may require that the whole
    check data is provided in a single command ("check quantum = check data").

    This can be used as:
    [0] dfuCmdData0(cmd=1 or 2, param) -> pktNb, status, param
    [1] dfuCmdData1(cmd=1 or 2, param) -> pktNb, status, param
    [2] dfuCmdData2(cmd=1 or 2, param) -> pktNb, status, param
    [3] dfuCmdData3(cmd=1 or 2, param) -> pktNb, status, param

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Cmd                           8
    Address                       32
    Size                          32
    Reserved                      56
    ============================  ==========
    """

    class FID(_DfuCmdDataXCmd.FID):
        """
        Field Identifiers
        """
        ADDRESS = 0xF9
        SIZE = 0xF8
        RESERVED = 0xF7
    # end class FID

    class LEN(_DfuCmdDataXCmd.LEN):
        """
        Field Lengths
        """
        ADDRESS = 0x20
        SIZE = 0x20
        RESERVED = 0x38
    # end class LEN

    FIELDS = _DfuCmdDataXCmd.FIELDS + (
        BitField(FID.ADDRESS,
                 LEN.ADDRESS,
                 0x00,
                 0x00,
                 title='Address',
                 name='address',
                 checks=(CheckHexList(LEN.ADDRESS // 8), CheckInt(max_value=pow(2, LEN.ADDRESS) - 1),)),
        BitField(FID.SIZE,
                 LEN.SIZE,
                 0x00,
                 0x00,
                 title='Size',
                 name='size',
                 checks=(CheckHexList(LEN.SIZE // 8), CheckInt(max_value=pow(2, LEN.SIZE) - 1),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, function_index, cmd_1_or_2, address, size, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param function_index: Number that represent the function_index:
                                0 -> dfuCmdData0
                                1 -> dfuCmdData1
                                2 -> dfuCmdData2
                                3 -> dfuCmdData3
        :type function_index: ``int``
        :param cmd_1_or_2: If True command 1, otherwise command 2
        :type cmd_1_or_2: ``bool``
        :param address: Start address (big endian), aligned on a multiple of the program/check quantum.
        :type address: ``int``
        :param size: Size in bytes (big endian), must be a multiple of the program/check quantum.
        :type size: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        if cmd_1_or_2:
            super().__init__(device_index, feature_index, function_index, self.CommandId.SUPPLY_PROGRAM_DATA, **kwargs)
        else:
            super().__init__(device_index, feature_index, function_index, self.CommandId.SUPPLY_CHECK_DATA, **kwargs)
        # end if

        self.address = address
        self.size = size
    # end def __init__
# end class DfuCmdDataXCmd1


class DfuCmdDataXCmd3(_DfuCmdDataXCmd):
    """
    Dfu DfuCmdDataXCmd3 implementation class

    The value 3. This command checks the firmware against the check data and validates it if successful.
    This command shall always be the last one of a DFU stream. It has no parameters and is not followed by
    any data packets.

    This can be used as:
    [0] dfuCmdData0(cmd=3, param) -> pktNb, status, param
    [1] dfuCmdData1(cmd=3, param) -> pktNb, status, param
    [2] dfuCmdData2(cmd=3, param) -> pktNb, status, param
    [3] dfuCmdData3(cmd=3, param) -> pktNb, status, param

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Cmd                           8
    Reserved                      120
    ============================  ==========
    """

    class FID(_DfuCmdDataXCmd.FID):
        """
        Field Identifiers
        """
        RESERVED = 0xF9
    # end class FID

    class LEN(_DfuCmdDataXCmd.LEN):
        """
        Field Lengths
        """
        RESERVED = 0x78
    # end class LEN

    FIELDS = _DfuCmdDataXCmd.FIELDS + (
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, function_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param function_index: Number that represent the function_index:
                                0 -> dfuCmdData0
                                1 -> dfuCmdData1
                                2 -> dfuCmdData2
                                3 -> dfuCmdData3
        :type function_index: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, function_index,self.CommandId.CHECK_AND_VALIDATE_FIRMWARE,
                         **kwargs)
    # end def __init__
# end class DfuCmdDataXCmd3


class DfuCmdDataXData(Dfu):
    """
    Dfu DfuCmdDataXData implementation class

    This can be used as:
    [0] dfuCmdData0(data) -> pktNb, status, param
    [1] dfuCmdData1(data) -> pktNb, status, param
    [2] dfuCmdData2(data) -> pktNb, status, param
    [3] dfuCmdData3(data) -> pktNb, status, param

    These functions are used to send 16 bytes of DFU payload.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Data                          128
    ============================  ==========
    """

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        DATA = 0xFA
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        DATA = 0x80
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.DATA,
                 LEN.DATA,
                 0x00,
                 0x00,
                 title='Data',
                 name='data',
                 checks=(CheckHexList(LEN.DATA // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, function_index, data, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param function_index: Number that represent the function_index:
                                0 -> dfuCmdData0
                                1 -> dfuCmdData1
                                2 -> dfuCmdData2
                                3 -> dfuCmdData3
        :type function_index: ``int``
        :param data: Data to send. Type int is for the value 0
        :type function_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = function_index
        self.data = data
    # end def __init__
# end class _DfuCmdDataXCmd


class DfuStartV0(Dfu):
    """
    DFU DfuStart V0 implementation class

    The host software may invoke this function at any time. Upon receiving it, the firmware shall abort any DFU
    in progress (on the same or a different entity). Then the firmware shall invalidate the corresponding firmware
    entity and prepare it for upgrade (usually, the whole entity is erased). The scheme used to mark an entity as
    invalid is device dependent, but it shall be non-volatile. The entity shall be marked as invalid before or at
    the same times as any part of it is erased. The corresponding peripheral and/or the whole system will not be
    available until a check-and-validate command (3) completes successfully. It is not possible to upgrade two
    entities concurrently.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    FwEntity                      8
    Encrypt                       8
    MagicStr                      80
    Reserved                      32
    ============================  ==========
    """

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        FW_ENTITY = 0xFA
        ENCRYPT = 0xF9
        MAGIC_STR = 0xF8
        RESERVED = 0xF7
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        FW_ENTITY = 0x08
        ENCRYPT = 0x08
        MAGIC_STR = 0x50
        RESERVED = 0x20
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.FW_ENTITY,
                 LEN.FW_ENTITY,
                 0x00,
                 0x00,
                 title='FwEntity',
                 name='fw_entity',
                 checks=(CheckHexList(LEN.FW_ENTITY // 8), CheckByte(),)),
        BitField(FID.ENCRYPT,
                 LEN.ENCRYPT,
                 0x00,
                 0x00,
                 title='Encrypt',
                 name='encrypt',
                 checks=(CheckHexList(LEN.ENCRYPT // 8), CheckByte(),)),
        BitField(FID.MAGIC_STR,
                 LEN.MAGIC_STR,
                 0x00,
                 0x00,
                 title='MagicStr',
                 name='magic_str',
                 checks=(CheckHexList(LEN.MAGIC_STR // 8), CheckByte(),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, fw_entity, encrypt, magic_str, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param fw_entity:Firmware entity to upgrade
        :type fw_entity: ``int``
        :param encrypt: Encryption mode
        :type encrypt: ``int``
        :param magic_str: Magic string (implementation and entity specific)
        :type magic_str: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = DfuStatusResponse.FUNCTION_INDEX[4]
        self.fw_entity = fw_entity
        self.encrypt = encrypt
        self.magic_str = magic_str
    # end def __init__
# end class DfuStartV0


class DfuStartV1(Dfu):
    """
    DFU DfuStart V1 implementation class

    The host software may invoke this function at any time. Upon receiving it, the firmware shall abort any DFU
    in progress (on the same or a different entity). Then the firmware shall invalidate the corresponding firmware
    entity and prepare it for upgrade (usually, the whole entity is erased). The scheme used to mark an entity as
    invalid is device dependent, but it shall be non-volatile. The entity shall be marked as invalid before or at
    the same times as any part of it is erased. The corresponding peripheral and/or the whole system will not be
    available until a check-and-validate command (3) completes successfully. It is not possible to upgrade two
    entities concurrently.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    FwEntity                      8
    Encrypt                       8
    MagicStr                      80
    Flag                          8
    Reserved                      24
    ============================  ==========
    """

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        FW_ENTITY = 0xFA
        ENCRYPT = 0xF9
        MAGIC_STR = 0xF8
        FLAG = 0xF7
        RESERVED = 0xF6
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        FW_ENTITY = 0x08
        ENCRYPT = 0x08
        MAGIC_STR = 0x50
        FLAG = 0x08
        RESERVED = 0x18
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.FW_ENTITY,
                 LEN.FW_ENTITY,
                 0x00,
                 0x00,
                 title='FwEntity',
                 name='fw_entity',
                 checks=(CheckHexList(LEN.FW_ENTITY // 8), CheckByte(),)),
        BitField(FID.ENCRYPT,
                 LEN.ENCRYPT,
                 0x00,
                 0x00,
                 title='Encrypt',
                 name='encrypt',
                 checks=(CheckHexList(LEN.ENCRYPT // 8), CheckByte(),)),
        BitField(FID.MAGIC_STR,
                 LEN.MAGIC_STR,
                 0x00,
                 0x00,
                 title='MagicStr',
                 name='magic_str',
                 checks=(CheckHexList(LEN.MAGIC_STR // 8), CheckByte(),)),
        BitField(FID.FLAG,
                 LEN.FLAG,
                 0x00,
                 0x00,
                 title='Flag',
                 name='flag',
                 checks=(CheckHexList(LEN.FLAG // 8), CheckByte(),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, fw_entity, encrypt, magic_str, flag, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param fw_entity:Firmware entity to upgrade
        :type fw_entity: ``int``
        :param encrypt: Encryption mode
        :type encrypt: ``int``
        :param magic_str: Magic string (implementation and entity specific)
        :type magic_str: ``int or HexList``
        :param flag: Flags (implementation and entity specific, set to zero when unused)
        :type flag: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = DfuStatusResponse.FUNCTION_INDEX[4]
        self.fw_entity = fw_entity
        self.encrypt = encrypt
        self.magic_str = magic_str
        self.flag = flag
    # end def __init__
# end class DfuStartV1


class DfuStartV2(Dfu):
    """
    DFU DfuStart V1 implementation class

    The host software may invoke this function at any time. Upon receiving it, the firmware shall abort any DFU
    in progress (on the same or a different entity). Then the firmware shall invalidate the corresponding firmware
    entity and prepare it for upgrade (usually, the whole entity is erased). The scheme used to mark an entity as
    invalid is device dependent, but it shall be non-volatile. The entity shall be marked as invalid before or at
    the same times as any part of it is erased. The corresponding peripheral and/or the whole system will not be
    available until a check-and-validate command (3) completes successfully. It is not possible to upgrade two
    entities concurrently.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    FwEntity                      8
    Encrypt                       8
    MagicStr                      80
    Flag                          8
    SecurLvl                      8
    Reserved                      16
    ============================  ==========
    """

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        FW_ENTITY = 0xFA
        ENCRYPT = 0xF9
        MAGIC_STR = 0xF8
        FLAG = 0xF7
        SECUR_LVL = 0xF6
        RESERVED = 0xF5
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        FW_ENTITY = 0x08
        ENCRYPT = 0x08
        MAGIC_STR = 0x50
        FLAG = 0x08
        SECUR_LVL = 0x08
        RESERVED = 0x10
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.FW_ENTITY,
                 LEN.FW_ENTITY,
                 0x00,
                 0x00,
                 title='FwEntity',
                 name='fw_entity',
                 checks=(CheckHexList(LEN.FW_ENTITY // 8), CheckByte(),)),
        BitField(FID.ENCRYPT,
                 LEN.ENCRYPT,
                 0x00,
                 0x00,
                 title='Encrypt',
                 name='encrypt',
                 checks=(CheckHexList(LEN.ENCRYPT // 8), CheckByte(),)),
        BitField(FID.MAGIC_STR,
                 LEN.MAGIC_STR,
                 0x00,
                 0x00,
                 title='MagicStr',
                 name='magic_str',
                 checks=(CheckHexList(LEN.MAGIC_STR // 8), CheckByte(),)),
        BitField(FID.FLAG,
                 LEN.FLAG,
                 0x00,
                 0x00,
                 title='Flag',
                 name='flag',
                 checks=(CheckHexList(LEN.FLAG // 8), CheckByte(),)),
        BitField(FID.SECUR_LVL,
                 LEN.SECUR_LVL,
                 0x00,
                 0x00,
                 title='SecurLvl',
                 name='secur_lvl',
                 checks=(CheckHexList(LEN.SECUR_LVL // 8), CheckByte(),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, fw_entity, encrypt, magic_str, flag, secur_lvl, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param fw_entity:Firmware entity to upgrade
        :type fw_entity: ``int``
        :param encrypt: Encryption mode
        :type encrypt: ``int``
        :param magic_str: Magic string (implementation and entity specific)
        :type magic_str: ``int or HexList``
        :param flag: Flags (implementation and entity specific, set to zero when unused)
        :type flag: ``int``
        :param secur_lvl: Security level (implementation and entity specific, set to zero when unused)
        :type secur_lvl: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = DfuStatusResponse.FUNCTION_INDEX[4]
        self.fw_entity = fw_entity
        self.encrypt = encrypt
        self.magic_str = magic_str
        self.flag = flag
        self.secur_lvl = secur_lvl
    # end def __init__
# end class DfuStartV2


class Restart(Dfu):
    """
    Dfu Restart implementation class

    Requests to restart (at least) the given firmware entity.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    FwEntity                      8
    Reserved                      120
    ============================  ==========
    """

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        FW_ENTITY = 0xFA
        RESERVED = 0xF9
    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        FW_ENTITY = 0x08
        RESERVED = 0x78
    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.FW_ENTITY,
                 LEN.FW_ENTITY,
                 0x00,
                 0x00,
                 title='FwEntity',
                 name='fw_entity',
                 checks=(CheckHexList(LEN.FW_ENTITY // 8), CheckByte(),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckHexList(LEN.RESERVED // 8), CheckInt(),),
                 default_value=HidppMessage.DEFAULT.RESERVED),
    )

    def __init__(self, device_index, feature_index, fw_entity, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param fw_entity: Firmware entity to restart. The value 255 may be used to restart all supported entities
        :type fw_entity: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = RestartResponse.FUNCTION_INDEX
        self.fw_entity = fw_entity
    # end def __init__
# end class Restart


class RestartResponse(Dfu):
    """
    Dfu Restart response implementation class

    This command may return an empty response or no response (device reset).

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Padding                       128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Restart,)
    VERSION = (0, 1, 2, 3,)
    FUNCTION_INDEX = 5

    class FID(Dfu.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(Dfu.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80

    # end class LEN

    FIELDS = Dfu.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=Dfu.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super(RestartResponse, self).__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class RestartResponse


class DfuStatusResponse(_DfuStatus):
    """
    Dfu DfuStatus response

    Status for all packets (flow control). The responses to all functions are identical to this structure.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    PktNb                         32
    Status                        8
    Params                        88
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    VERSION = (0, 1, 2, 3, )
    FUNCTION_INDEX = (0, 1, 2, 3, 4,)

    def __init__(self, device_index, feature_index, function_index, pkt_nb, status, params, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param pkt_nb: The package number
        :type pkt_nb: ``int``
        :param status: Status of the requested operation
        :type status: ``int``
        :param params: Status parameters (e.g., debug information). Type int is for the value 0
        :type status: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super(DfuStatusResponse, self).__init__(device_index, feature_index, pkt_nb, status, params, **kwargs)

        self.functionIndex = function_index
    # end def __init__
# end class DfuStatusResponse


class DfuStatusEvent(_DfuStatus):
    """
    Dfu DfuStatus event

    Status for all packets (flow control). An event is only sent when the previous response had a status
    of 3 (wait for event).

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    PktNb                         32
    Status                        8
    Params                        88
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1, 2, 3, )
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, pkt_nb, status, params, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param pkt_nb: The package number
        :type pkt_nb: ``int``
        :param status: Raw value on y
        :type status: ``int``
        :param params: Status parameters (e.g., debug information). Type int is for the value 0
        :type status: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super(DfuStatusEvent, self).__init__(device_index, feature_index, pkt_nb, status, params, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class DfuStatusEvent


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
