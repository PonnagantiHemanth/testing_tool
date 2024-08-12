#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.gaming.profilemanagement
:brief: HID++ 2.0 ``ProfileManagement`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/22
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

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
class ProfileManagement(HidppMessage):
    """
    This feature provides the means to manage on-device profile files and feature-specific configuration files
    in a simple (host managed) file system that lives in persistent storage in the device.
    """
    FEATURE_ID = 0x8101
    MAX_FUNCTION_INDEX = 12

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__

    @unique
    class Mode(IntEnum):
        """
        Onboard mode
        """
        HOST_MODE = 0
        ONBOARD_MODE = 1
    # end class Mode

    @unique
    class ProfileMode(IntEnum):
        """
        Profile control mode
        """
        SW_CONTROL = 0
        HW_SW_CONTROL = 1
    # end class ProfileMode

    @unique
    class SpecialFileId(IntEnum):
        """
        Special File ID
        """
        PROFILE_DIRECTORY = 0
        FILE_ID_START = 1
    # end class SpecialFileId

    class Hash(IntEnum):
        """
        Hashes
        """
        OOB_PROFILE_DIRECTORY = 0xFFFFFFFF
        OOB_PROFILE = 0xFFFFFFFF
    # end class Hash

    @unique
    class Tag(IntEnum):
        """
        Profile Tag definition

        https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1072722811&range=A14
        """
        PROFILE_IDENTIFIER = 0x01
        PROFILE_VERSION = 0x02
        PROFILE_NAME = 0x03
        LIGHTING_FLAG = 0x07
        ACTIVE_CLUSTER_0_EFFECT = 0x0C
        ACTIVE_CLUSTER_1_EFFECT = 0x0D
        PASSIVE_CLUSTER_0_EFFECT = 0x0E
        PASSIVE_CLUSTER_1_EFFECT = 0x0F
        PS_TIMEOUT = 0x12
        PO_TIMEOUT = 0x13
        X4523_CIDX_BITMAP = 0x30
        ANALOG_GENERIC_SETTING = 0x40
        FEATURE_SETTINGS_FILE_1B05_MACRO = 0xE01B05
        FEATURE_SETTINGS_FILE_1B05_BASE = 0xE11B05
        FEATURE_SETTINGS_FILE_1B05_FN = 0xE21B05
        FEATURE_SETTINGS_FILE_1B05_GSHIFT = 0xE31B05
        FEATURE_SETTINGS_FILE_1B08_ACTUATION = 0xE01B08
        FEATURE_SETTINGS_FILE_1B08_RAPID_TRIGGER = 0xE11B08
        FEATURE_SETTINGS_FILE_1B08_MULTI_ACTION = 0xE21B08
        EOF = 0xFF
    # end class Tag

    class Partition:
        """
        Partition definition class.
        """

        @unique
        class SectorId(IntEnum):
            """
            The sectorID is in general a 2-byte value. The Partition.SectorId be used in the sectorID higher byte (MSB).

            https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1017032508&range=B104
            """
            NVS = 0x0000
            OOB = 0x0100
        # end class SectorId

        @unique
        class FileId(IntEnum):
            """
            The fileID is in general a 2-byte value. The Partition.FileId be used in the fileID higher byte (MSB).

            https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1017032508&range=B134
            """
            NVS = 0x0000
            OOB = 0x0100
            RAM = 0x0200
        # end class FileId
    # end class Partition

    class FileTypeId:
        """
        File Type Id definition (Be used in profile directory)
        """

        @unique
        class X8101(IntEnum):
            """
            https://docs.google.com/spreadsheets/d/1Py5a5bWBmDEK2voFczI4x0L5_dkbT9EGM-jmkCCJTao/view#gid=1017032508&range=A87
            """
            HOST_MODE_PROFILE = 0
            ONBOARD_MODE_PROFILE = 1
        # end class X8101

        @unique
        class X1B05(IntEnum):
            """
            https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x1b05_full_key_customization_v0.adoc
            """
            MACRO_DEFINITION_FILE = 0
            BASE_LAYER_SETTINGS_FILE = 1
            FN_LAYER_SETTINGS_FILE = 2
            GSHIFT_LAYER_SETTINGS_FILE = 3
        # end class X1B05

        @unique
        class X1B08(IntEnum):
            """
            https://docs.google.com/spreadsheets/d/1S3Fz3mccpNIoguVkO6hN5ggfgllsojhGkD2j5E9f2A0/view#gid=1017032508
            """
            ACTUATION_CONFIGURATION_FILE = 0
            RAPID_TRIGGER_CONFIGURATION_FILE = 1
            MULTI_ACTION_CONFIGURATION_FILE = 2
        # end class X1B08
    # end class FileTypeId

    @unique
    class FileSystemErrorCode(IntEnum):
        """
        The filesystem error code definition class
        """
        NO_ERROR = 0x00
        MISSING_FILE_REFERENCE_IN_DIRECTORY = 0x01
        INVALID_SECTOR_ID = 0x02
        NVS_ERROR = 0x03
        CRC_CHECK_ERROR = 0x04
        FILE_TOO_BIG = 0x05
        SIZE_EXCEEDS_BUFFER_CAPACITY = 0x06
        FILE_DETAIL_MISMATCH = 0x07
        INVALID_FEATURE_ID_FILETYPE_ID = 0x08
        PROFILE_PARSE_ERROR = 0x09
        FEATURE_CONFIGURATION_ERROR = 0x0A
        RAM_BUFFER_CHECK_ERROR = 0x0B
        INVALID_FILE_ID = 0x0C
        DIRECTORY_ONBOARD_PROFILE_ORDER_ERROR = 0x0D
        MISSING_ONBOARD_PROFILE = 0x0E
        NOT_SUPPORTED = 0xFF
    # end class FileSystemErrorCode

    class CfgErrorCode:
        """
        Error during configuration of feature (each feature defines its own cfg_err_code values)
        """

        @unique
        class X8101(IntEnum):
            """
            cf: Table 9.cfg_err_code value definition in
            https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x8101_profile_management_v0.adoc#getError
            """
            NO_ERROR = 0x00
            GENERIC_CONFIGURATION_ERROR = 0x01
        # end class X8101

        @unique
        class X1B05(IntEnum):
            """
            cf: Table 2.cfg_err_code value definition in
            https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x1b05_full_key_customization_v0.adoc
            """
            NO_ERROR = 0x00
            GENERIC_CONFIGURATION_ERROR = 0x01
        # end class X1B05
    # end class CfgErrorCode

    class EditBufferCapabilities(BitFieldContainerMixin):
        """
        Define ``EditBufferCapabilities`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      5
        Opcode                        3
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            OPCODE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x5
            OPCODE = 0x3
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            OPCODE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.OPCODE, length=LEN.OPCODE,
                     title="Opcode", name="opcode",
                     checks=(CheckInt(0, pow(2, LEN.OPCODE) - 1),),
                     default_value=DEFAULT.OPCODE),
        )
    # end class EditBufferCapabilities

    class EditBufferOperation(BitFieldContainerMixin):
        """
        Define ``EditBufferOperation`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Count                         4
        Reserved                      1
        Opcode                        3
        ============================  ==========
        """

        @unique
        class Opcode(IntEnum):
            """
            Specifies the type of operation to execute

            https://github.com/Logitech/cpg-samarkand-hidpp-docs/blob/master/docs/x8101_profile_management_v0.adoc#editBuffer
            """
            OVERWRITE = 1
            INSERT = 2
            DELETE = 4
        # end class Opcode

        class FID(object):
            """
            Field identifiers
            """
            COUNT = 0xFF
            RESERVED = COUNT - 1
            OPCODE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            COUNT = 0x4
            RESERVED = 0x1
            OPCODE = 0x3
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            COUNT = 0x0
            RESERVED = 0x0
            OPCODE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.COUNT, length=LEN.COUNT,
                     title="Count", name="count",
                     checks=(CheckInt(0, pow(2, LEN.COUNT) - 1),),
                     default_value=DEFAULT.COUNT),
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.OPCODE, length=LEN.OPCODE,
                     title="Opcode", name="opcode",
                     checks=(CheckInt(0, pow(2, LEN.OPCODE) - 1),),
                     default_value=DEFAULT.OPCODE),
        )
    # end class EditBufferOperation

    class OperatingMode(BitFieldContainerMixin):
        """
        Define ``OperatingMode`` information for version 0

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      4
        Profile Mode                  1
        Set Profile Mode              1
        Onboard Mode                  1
        Set Onboard Mode              1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SET_PROFILE_MODE = RESERVED - 1
            PROFILE_MODE = SET_PROFILE_MODE - 1
            ONBOARD_MODE = PROFILE_MODE - 1
            SET_ONBOARD_MODE = ONBOARD_MODE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x4
            SET_PROFILE_MODE = 0x1
            PROFILE_MODE = 0x1
            ONBOARD_MODE = 0x1
            SET_ONBOARD_MODE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            SET_PROFILE_MODE = 0x0
            PROFILE_MODE = 0x0
            ONBOARD_MODE = 0x0
            SET_ONBOARD_MODE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.PROFILE_MODE, length=LEN.PROFILE_MODE,
                     title="ProfileMode", name="profile_mode",
                     checks=(CheckInt(0, pow(2, LEN.PROFILE_MODE) - 1),),
                     default_value=DEFAULT.PROFILE_MODE),
            BitField(fid=FID.SET_PROFILE_MODE, length=LEN.SET_PROFILE_MODE,
                     title="SetProfileMode", name="set_profile_mode",
                     checks=(CheckInt(0, pow(2, LEN.SET_PROFILE_MODE) - 1),),
                     default_value=DEFAULT.SET_PROFILE_MODE),
            BitField(fid=FID.ONBOARD_MODE, length=LEN.ONBOARD_MODE,
                     title="OnboardMode", name="onboard_mode",
                     checks=(CheckInt(0, pow(2, LEN.ONBOARD_MODE) - 1),),
                     default_value=DEFAULT.ONBOARD_MODE),
            BitField(fid=FID.SET_ONBOARD_MODE, length=LEN.SET_ONBOARD_MODE,
                     title="SetOnboardMode", name="set_onboard_mode",
                     checks=(CheckInt(0, pow(2, LEN.SET_ONBOARD_MODE) - 1),),
                     default_value=DEFAULT.SET_ONBOARD_MODE),
        )
    # end class OperatingMode

    class OperatingModeResponse(BitFieldContainerMixin):
        """
        Define ``OperatingModeResponse`` information for version 0

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        Profile Mode                  1
        Onboard Mode                  1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            PROFILE_MODE = RESERVED - 1
            ONBOARD_MODE = PROFILE_MODE - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            PROFILE_MODE = 0x1
            ONBOARD_MODE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            PROFILE_MODE = 0x0
            ONBOARD_MODE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.PROFILE_MODE, length=LEN.PROFILE_MODE,
                     title="ProfileMode", name="profile_mode",
                     checks=(CheckInt(0, pow(2, LEN.PROFILE_MODE) - 1),),
                     default_value=DEFAULT.PROFILE_MODE),
            BitField(fid=FID.ONBOARD_MODE, length=LEN.ONBOARD_MODE,
                     title="OnboardMode", name="onboard_mode",
                     checks=(CheckInt(0, pow(2, LEN.ONBOARD_MODE) - 1),),
                     default_value=DEFAULT.ONBOARD_MODE),
        )
    # end class OperatingModeResponse

    class ConfigureAction(BitFieldContainerMixin):
        """
        Define ``ConfigureAction`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      6
        File Type Id                  2
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            FILE_TYPE_ID = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x6
            FILE_TYPE_ID = 0x2
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            FILE_TYPE_ID = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.FILE_TYPE_ID, length=LEN.FILE_TYPE_ID,
                     title="FileTypeId", name="file_type_id",
                     checks=(CheckInt(0, pow(2, LEN.FILE_TYPE_ID) - 1),),
                     default_value=DEFAULT.FILE_TYPE_ID),
        )
    # end class ConfigureAction

    class PowerOnProfileAction(BitFieldContainerMixin):
        """
        Define ``PowerOnProfileAction`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Set Power On Profile          1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            SET_POWER_ON_PROFILE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            SET_POWER_ON_PROFILE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            SET_POWER_ON_PROFILE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.SET_POWER_ON_PROFILE, length=LEN.SET_POWER_ON_PROFILE,
                     title="SetPowerOnProfile", name="set_power_on_profile",
                     checks=(CheckInt(0, pow(2, LEN.SET_POWER_ON_PROFILE) - 1),),
                     default_value=DEFAULT.SET_POWER_ON_PROFILE),
        )
    # end class PowerOnProfileAction

    class GetHashAction(BitFieldContainerMixin):
        """
        Define ``GetHashAction`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Compute                       1
        ============================  ==========
        """

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            COMPUTE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            COMPUTE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            COMPUTE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.COMPUTE, length=LEN.COMPUTE,
                     title="Compute", name="compute",
                     checks=(CheckInt(0, pow(2, LEN.COMPUTE) - 1),),
                     default_value=DEFAULT.COMPUTE),
        )
    # end class GetHashAction

    class ProfileChangeResult(BitFieldContainerMixin):
        """
        Define ``ProfileChangeResult`` information

        Format:
        ============================  ==========
        Name                          Bit count
        ============================  ==========
        Reserved                      7
        Failure                       1
        ============================  ==========
        """

        @unique
        class Result(IntEnum):
            """
            Profile Change Result
            """
            SUCCESS = 0
            FAILURE = 1
        # end class Result

        class FID(object):
            """
            Field identifiers
            """
            RESERVED = 0xFF
            FAILURE = RESERVED - 1
        # end class FID

        class LEN(object):
            """
            Field lengths in bits
            """
            RESERVED = 0x7
            FAILURE = 0x1
        # end class LEN

        class DEFAULT(object):
            """
            Field default values
            """
            RESERVED = 0x0
            FAILURE = 0x0
        # end class DEFAULT

        FIELDS = (
            BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                     title="Reserved", name="reserved",
                     checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                     default_value=DEFAULT.RESERVED),
            BitField(fid=FID.FAILURE, length=LEN.FAILURE,
                     title="Failure", name="failure",
                     checks=(CheckInt(0, pow(2, LEN.FAILURE) - 1),),
                     default_value=DEFAULT.FAILURE),
        )
    # end class ProfileChangeResult
# end class ProfileManagement


class ProfileManagementModel(FeatureModel):
    """
    Define ``ProfileManagement`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_CAPABILITIES = 0
        GET_PROFILE_TAG_LIST = 1
        START_WRITE_BUFFER = 2
        WRITE_BUFFER = 3
        GET_ERROR = 4
        EDIT_BUFFER = 5
        GET_SET_MODE = 6
        SAVE = 7
        LOAD = 8
        CONFIGURE = 9
        GET_SET_POWER_ON_PARAMS = 10
        GET_HASHES = 11
        READ_BUFFER = 12

        # Event index
        PROFILE_CHANGE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``ProfileManagement`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_CAPABILITIES: {
                    "request": GetCapabilities,
                    "response": GetCapabilitiesResponse
                },
                cls.INDEX.GET_PROFILE_TAG_LIST: {
                    "request": GetProfileTagList,
                    "response": GetProfileTagListResponse
                },
                cls.INDEX.START_WRITE_BUFFER: {
                    "request": StartWriteBuffer,
                    "response": StartWriteBufferResponse
                },
                cls.INDEX.WRITE_BUFFER: {
                    "request": WriteBuffer,
                    "response": WriteBufferResponse
                },
                cls.INDEX.GET_ERROR: {
                    "request": GetError,
                    "response": GetErrorResponse
                },
                cls.INDEX.EDIT_BUFFER: {
                    "request": EditBuffer,
                    "response": EditBufferResponse
                },
                cls.INDEX.GET_SET_MODE: {
                    "request": GetSetMode,
                    "response": GetSetModeResponse
                },
                cls.INDEX.SAVE: {
                    "request": Save,
                    "response": SaveResponse
                },
                cls.INDEX.LOAD: {
                    "request": Load,
                    "response": LoadResponse
                },
                cls.INDEX.CONFIGURE: {
                    "request": Configure,
                    "response": ConfigureResponse
                },
                cls.INDEX.GET_SET_POWER_ON_PARAMS: {
                    "request": GetSetPowerOnParams,
                    "response": GetSetPowerOnParamsResponse
                },
                cls.INDEX.GET_HASHES: {
                    "request": GetHashes,
                    "response": GetHashesResponse
                },
                cls.INDEX.READ_BUFFER: {
                    "request": ReadBuffer,
                    "response": ReadBufferResponse
                }
            },
            "events": {
                cls.INDEX.PROFILE_CHANGE: {"report": ProfileChangeEvent}
            }
        }

        return {
            "feature_base": ProfileManagement,
            "versions": {
                ProfileManagementV0.VERSION: {
                    "main_cls": ProfileManagementV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class ProfileManagementModel


class ProfileManagementFactory(FeatureFactory):
    """
    Get ``ProfileManagement`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``ProfileManagement`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``ProfileManagementInterface``
        """
        return ProfileManagementModel.get_main_cls(version)()
    # end def create
# end class ProfileManagementFactory


class ProfileManagementInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``ProfileManagement``
    """

    def __init__(self):
        # Requests
        self.get_capabilities_cls = None
        self.get_profile_tag_list_cls = None
        self.start_write_buffer_cls = None
        self.write_buffer_cls = None
        self.get_error_cls = None
        self.edit_buffer_cls = None
        self.get_set_mode_cls = None
        self.save_cls = None
        self.load_cls = None
        self.configure_cls = None
        self.get_set_power_on_params_cls = None
        self.get_hashes_cls = None
        self.read_buffer_cls = None

        # Responses
        self.get_capabilities_response_cls = None
        self.get_profile_tag_list_response_cls = None
        self.start_write_buffer_response_cls = None
        self.write_buffer_response_cls = None
        self.get_error_response_cls = None
        self.edit_buffer_response_cls = None
        self.get_set_mode_response_cls = None
        self.save_response_cls = None
        self.load_response_cls = None
        self.configure_response_cls = None
        self.get_set_power_on_params_response_cls = None
        self.get_hashes_response_cls = None
        self.read_buffer_response_cls = None

        # Events
        self.profile_change_event_cls = None
    # end def __init__
# end class ProfileManagementInterface


class ProfileManagementV0(ProfileManagementInterface):
    """
    Define ``ProfileManagementV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetCapabilities() -> FileSystemVer, ProfileTagVer, MaxSectorSize, RamBufferSize, MaxSectorId, MaxFileId,
     MaxDirectorySectorId, TotalFlashSizeKb, FlashEraseCounter, FlashLifeExpect, NumOnboardProfiles,
     EditBufferCapabilities

    [1] GetProfileTagList(OffsetBytes) -> PartialTagList

    [2] StartWriteBuffer(Count) -> None

    [3] WriteBuffer(Data) -> FrameNum

    [4] GetError() -> FsErrorCode, FsErrorParam1, FsErrorParam2

    [5] EditBuffer(EditBufferOperation, Address, Data) -> None

    [6] GetSetMode(OperatingMode) -> OperatingModeResponse, CurrProfileFileId

    [7] Save(FirstSectorId, Count, Hash32) -> None

    [8] Load(FirstSectorId, Count) -> None

    [9] Configure(FeatureId, ConfigureAction, FileId, Count, Hash) -> None

    [10] GetSetPowerOnParams(PowerOnProfileAction, PowerOnProfile) -> PowerOnProfile

    [11] GetHashes(GetHashAction, FileId0, FileId1, FileId2, FileId3) -> Hash0, Hash1, Hash2, Hash3

    [12] ReadBuffer(OffsetBytes) -> Data

    [Event 0] ProfileChangeEvent -> NewProfile, ProfileChangeResult
    """
    VERSION = 0

    def __init__(self):
        # See ``ProfileManagement.__init__``
        super().__init__()
        index = ProfileManagementModel.INDEX

        # Requests
        self.get_capabilities_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_profile_tag_list_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.GET_PROFILE_TAG_LIST)
        self.start_write_buffer_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.START_WRITE_BUFFER)
        self.write_buffer_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.WRITE_BUFFER)
        self.get_error_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.GET_ERROR)
        self.edit_buffer_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.EDIT_BUFFER)
        self.get_set_mode_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.GET_SET_MODE)
        self.save_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.SAVE)
        self.load_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.LOAD)
        self.configure_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.CONFIGURE)
        self.get_set_power_on_params_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.GET_SET_POWER_ON_PARAMS)
        self.get_hashes_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.GET_HASHES)
        self.read_buffer_cls = ProfileManagementModel.get_request_cls(
            self.VERSION, index.READ_BUFFER)

        # Responses
        self.get_capabilities_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.GET_CAPABILITIES)
        self.get_profile_tag_list_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.GET_PROFILE_TAG_LIST)
        self.start_write_buffer_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.START_WRITE_BUFFER)
        self.write_buffer_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.WRITE_BUFFER)
        self.get_error_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.GET_ERROR)
        self.edit_buffer_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.EDIT_BUFFER)
        self.get_set_mode_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.GET_SET_MODE)
        self.save_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.SAVE)
        self.load_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.LOAD)
        self.configure_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.CONFIGURE)
        self.get_set_power_on_params_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.GET_SET_POWER_ON_PARAMS)
        self.get_hashes_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.GET_HASHES)
        self.read_buffer_response_cls = ProfileManagementModel.get_response_cls(
            self.VERSION, index.READ_BUFFER)

        # Events
        self.profile_change_event_cls = ProfileManagementModel.get_report_cls(
            self.VERSION, index.PROFILE_CHANGE)
    # end def __init__

    def get_max_function_index(self):
        # See ``ProfileManagementInterface.get_max_function_index``
        return ProfileManagementModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ProfileManagementV0


class ShortEmptyPacketDataFormat(ProfileManagement):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetCapabilities
        - GetError

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        PADDING = ProfileManagement.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(ProfileManagement):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - StartWriteBufferResponse
        - EditBufferResponse
        - SaveResponse
        - LoadResponse
        - ConfigureResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        PADDING = ProfileManagement.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class BufferOffset(ProfileManagement):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetProfileTagList
        - ReadBuffer

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Offset Bytes                  16
    Padding                       8
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        OFFSET_BYTES = ProfileManagement.FID.SOFTWARE_ID - 1
        PADDING = OFFSET_BYTES - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        OFFSET_BYTES = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.OFFSET_BYTES, length=LEN.OFFSET_BYTES,
                 title="OffsetBytes", name="offset_bytes",
                 checks=(CheckHexList(LEN.OFFSET_BYTES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OFFSET_BYTES) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )
# end class BufferOffset


class BufferData(ProfileManagement):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - WriteBuffer
        - ReadBufferResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Data                          128
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        DATA = ProfileManagement.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        DATA = 0x80
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )
# end class BufferData


class GetCapabilities(ShortEmptyPacketDataFormat):
    """
    Define ``GetCapabilities`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetCapabilitiesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetCapabilities


class GetCapabilitiesResponse(ProfileManagement):
    """
    Define ``GetCapabilitiesResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    File System Ver               8
    Profile Tag Ver               8
    Max Sector Size               16
    Ram Buffer Size               16
    Max Sector Id                 8
    Max File Id                   8
    Max Directory Sector Id       8
    Total Flash Size Kb           8
    Flash Erase Counter           24
    Flash Life Expect             8
    Num Onboard Profiles          8
    Edit Buffer Capabilities      8
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        FILE_SYSTEM_VER = ProfileManagement.FID.SOFTWARE_ID - 1
        PROFILE_TAG_VER = FILE_SYSTEM_VER - 1
        MAX_SECTOR_SIZE = PROFILE_TAG_VER - 1
        RAM_BUFFER_SIZE = MAX_SECTOR_SIZE - 1
        MAX_SECTOR_ID = RAM_BUFFER_SIZE - 1
        MAX_FILE_ID = MAX_SECTOR_ID - 1
        MAX_DIRECTORY_SECTOR_ID = MAX_FILE_ID - 1
        TOTAL_FLASH_SIZE_KB = MAX_DIRECTORY_SECTOR_ID - 1
        FLASH_ERASE_COUNTER = TOTAL_FLASH_SIZE_KB - 1
        FLASH_LIFE_EXPECT = FLASH_ERASE_COUNTER - 1
        NUM_ONBOARD_PROFILES = FLASH_LIFE_EXPECT - 1
        EDIT_BUFFER_CAPABILITIES = NUM_ONBOARD_PROFILES - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        FILE_SYSTEM_VER = 0x8
        PROFILE_TAG_VER = 0x8
        MAX_SECTOR_SIZE = 0x10
        RAM_BUFFER_SIZE = 0x10
        MAX_SECTOR_ID = 0x8
        MAX_FILE_ID = 0x8
        MAX_DIRECTORY_SECTOR_ID = 0x8
        TOTAL_FLASH_SIZE_KB = 0x8
        FLASH_ERASE_COUNTER = 0x18
        FLASH_LIFE_EXPECT = 0x8
        NUM_ONBOARD_PROFILES = 0x8
        EDIT_BUFFER_CAPABILITIES = 0x8
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.FILE_SYSTEM_VER, length=LEN.FILE_SYSTEM_VER,
                 title="FileSystemVer", name="file_system_ver",
                 checks=(CheckHexList(LEN.FILE_SYSTEM_VER // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_TAG_VER, length=LEN.PROFILE_TAG_VER,
                 title="ProfileTagVer", name="profile_tag_ver",
                 checks=(CheckHexList(LEN.PROFILE_TAG_VER // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAX_SECTOR_SIZE, length=LEN.MAX_SECTOR_SIZE,
                 title="MaxSectorSize", name="max_sector_size",
                 checks=(CheckHexList(LEN.MAX_SECTOR_SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_SECTOR_SIZE) - 1),)),
        BitField(fid=FID.RAM_BUFFER_SIZE, length=LEN.RAM_BUFFER_SIZE,
                 title="RamBufferSize", name="ram_buffer_size",
                 checks=(CheckHexList(LEN.RAM_BUFFER_SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RAM_BUFFER_SIZE) - 1),)),
        BitField(fid=FID.MAX_SECTOR_ID, length=LEN.MAX_SECTOR_ID,
                 title="MaxSectorId", name="max_sector_id",
                 checks=(CheckHexList(LEN.MAX_SECTOR_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAX_FILE_ID, length=LEN.MAX_FILE_ID,
                 title="MaxFileId", name="max_file_id",
                 checks=(CheckHexList(LEN.MAX_FILE_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAX_DIRECTORY_SECTOR_ID, length=LEN.MAX_DIRECTORY_SECTOR_ID,
                 title="MaxDirectorySectorId", name="max_directory_sector_id",
                 checks=(CheckHexList(LEN.MAX_DIRECTORY_SECTOR_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.TOTAL_FLASH_SIZE_KB, length=LEN.TOTAL_FLASH_SIZE_KB,
                 title="TotalFlashSizeKb", name="total_flash_size_kb",
                 checks=(CheckHexList(LEN.TOTAL_FLASH_SIZE_KB // 8),
                         CheckByte(),)),
        BitField(fid=FID.FLASH_ERASE_COUNTER, length=LEN.FLASH_ERASE_COUNTER,
                 title="FlashEraseCounter", name="flash_erase_counter",
                 checks=(CheckHexList(LEN.FLASH_ERASE_COUNTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FLASH_ERASE_COUNTER) - 1),)),
        BitField(fid=FID.FLASH_LIFE_EXPECT, length=LEN.FLASH_LIFE_EXPECT,
                 title="FlashLifeExpect", name="flash_life_expect",
                 checks=(CheckHexList(LEN.FLASH_LIFE_EXPECT // 8),
                         CheckByte(),)),
        BitField(fid=FID.NUM_ONBOARD_PROFILES, length=LEN.NUM_ONBOARD_PROFILES,
                 title="NumOnboardProfiles", name="num_onboard_profiles",
                 checks=(CheckHexList(LEN.NUM_ONBOARD_PROFILES // 8),
                         CheckByte(),)),
        BitField(fid=FID.EDIT_BUFFER_CAPABILITIES, length=LEN.EDIT_BUFFER_CAPABILITIES,
                 title="EditBufferCapabilities", name="edit_buffer_capabilities",
                 checks=(CheckHexList(LEN.EDIT_BUFFER_CAPABILITIES // 8),
                         CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, file_system_ver, profile_tag_ver, max_sector_size, ram_buffer_size,
                 max_sector_id, max_file_id, max_directory_sector_id, total_flash_size_kb, flash_erase_counter,
                 flash_life_expect, num_onboard_profiles, opcode, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param file_system_ver: File System Ver
        :type file_system_ver: ``int | HexList``
        :param profile_tag_ver: Profile Tag Ver
        :type profile_tag_ver: ``int | HexList``
        :param max_sector_size: Max Sector Size
        :type max_sector_size: ``int | HexList``
        :param ram_buffer_size: Ram Buffer Size
        :type ram_buffer_size: ``int | HexList``
        :param max_sector_id: Max Sector Id
        :type max_sector_id: ``int | HexList``
        :param max_file_id: Max File Id
        :type max_file_id: ``int | HexList``
        :param max_directory_sector_id: Max Directory Sector Id
        :type max_directory_sector_id: ``int | HexList``
        :param total_flash_size_kb: Total Flash Size Kb
        :type total_flash_size_kb: ``int | HexList``
        :param flash_erase_counter: Flash Erase Counter
        :type flash_erase_counter: ``int | HexList``
        :param flash_life_expect: Flash Life Expect
        :type flash_life_expect: ``int | HexList``
        :param num_onboard_profiles: Num Onboard Profiles
        :type num_onboard_profiles: ``int | HexList``
        :param opcode: Opcode
        :type opcode: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.file_system_ver = file_system_ver
        self.profile_tag_ver = profile_tag_ver
        self.max_sector_size = max_sector_size
        self.ram_buffer_size = ram_buffer_size
        self.max_sector_id = max_sector_id
        self.max_file_id = max_file_id
        self.max_directory_sector_id = max_directory_sector_id
        self.total_flash_size_kb = total_flash_size_kb
        self.flash_erase_counter = flash_erase_counter
        self.flash_life_expect = flash_life_expect
        self.num_onboard_profiles = num_onboard_profiles
        self.edit_buffer_capabilities = self.EditBufferCapabilities(opcode=opcode)
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
        :rtype: ``GetCapabilitiesResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.edit_buffer_capabilities = cls.EditBufferCapabilities.fromHexList(
            inner_field_container_mixin.edit_buffer_capabilities)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetCapabilitiesResponse


class GetProfileTagList(BufferOffset):
    """
    Define ``GetProfileTagList`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, offset_bytes, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param offset_bytes: Offset Bytes
        :type offset_bytes: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetProfileTagListResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.offset_bytes = offset_bytes
    # end def __init__
# end class GetProfileTagList


class GetProfileTagListResponse(ProfileManagement):
    """
    Define ``GetProfileTagListResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Partial Tag List              128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetProfileTagList,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        PARTIAL_TAG_LIST = ProfileManagement.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        PARTIAL_TAG_LIST = 0x80
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.PARTIAL_TAG_LIST, length=LEN.PARTIAL_TAG_LIST,
                 title="PartialTagList", name="partial_tag_list",
                 checks=(CheckHexList(LEN.PARTIAL_TAG_LIST // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PARTIAL_TAG_LIST) - 1),)),
    )

    def __init__(self, device_index, feature_index, partial_tag_list, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param partial_tag_list: Partial Tag List
        :type partial_tag_list: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.partial_tag_list = partial_tag_list
    # end def __init__
# end class GetProfileTagListResponse


class StartWriteBuffer(ProfileManagement):
    """
    Define ``StartWriteBuffer`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Count                         16
    Padding                       8
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        COUNT = ProfileManagement.FID.SOFTWARE_ID - 1
        PADDING = COUNT - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        COUNT = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=StartWriteBufferResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.count = count
    # end def __init__
# end class StartWriteBuffer


class StartWriteBufferResponse(LongEmptyPacketDataFormat):
    """
    Define ``StartWriteBufferResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartWriteBuffer,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class StartWriteBufferResponse


class WriteBuffer(BufferData):
    """
    Define ``WriteBuffer`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param data: Data
        :type data: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=WriteBufferResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data = data
    # end def __init__
# end class WriteBuffer


class WriteBufferResponse(ProfileManagement):
    """
    Define ``WriteBufferResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Frame Num                     16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteBuffer,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        FRAME_NUM = ProfileManagement.FID.SOFTWARE_ID - 1
        PADDING = FRAME_NUM - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        FRAME_NUM = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.FRAME_NUM, length=LEN.FRAME_NUM,
                 title="FrameNum", name="frame_num",
                 checks=(CheckHexList(LEN.FRAME_NUM // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FRAME_NUM) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, frame_num, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param frame_num: Frame Num
        :type frame_num: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.frame_num = frame_num
    # end def __init__
# end class WriteBufferResponse


class GetError(ShortEmptyPacketDataFormat):
    """
    Define ``GetError`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetErrorResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetError


class GetErrorResponse(ProfileManagement):
    """
    Define ``GetErrorResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Fs Error Code                 8
    Fs Error Param 1              16
    Fs Error Param 2              8
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetError,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        FS_ERROR_CODE = ProfileManagement.FID.SOFTWARE_ID - 1
        FS_ERROR_PARAM_1 = FS_ERROR_CODE - 1
        FS_ERROR_PARAM_2 = FS_ERROR_PARAM_1 - 1
        PADDING = FS_ERROR_PARAM_2 - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        FS_ERROR_CODE = 0x8
        FS_ERROR_PARAM_1 = 0x10
        FS_ERROR_PARAM_2 = 0x8
        PADDING = 0x60
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.FS_ERROR_CODE, length=LEN.FS_ERROR_CODE,
                 title="FsErrorCode", name="fs_error_code",
                 checks=(CheckHexList(LEN.FS_ERROR_CODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.FS_ERROR_PARAM_1, length=LEN.FS_ERROR_PARAM_1,
                 title="FsErrorParam1", name="fs_error_param_1",
                 checks=(CheckHexList(LEN.FS_ERROR_PARAM_1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FS_ERROR_PARAM_1) - 1),)),
        BitField(fid=FID.FS_ERROR_PARAM_2, length=LEN.FS_ERROR_PARAM_2,
                 title="FsErrorParam2", name="fs_error_param_2",
                 checks=(CheckHexList(LEN.FS_ERROR_PARAM_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, fs_error_code, fs_error_param_1, fs_error_param_2, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param fs_error_code: Fs Error Code
        :type fs_error_code: ``int | HexList``
        :param fs_error_param_1: Fs Error Param 1
        :type fs_error_param_1: ``int | HexList``
        :param fs_error_param_2: Fs Error Param 2
        :type fs_error_param_2: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.fs_error_code = fs_error_code
        self.fs_error_param_1 = fs_error_param_1
        self.fs_error_param_2 = fs_error_param_2
    # end def __init__
# end class GetErrorResponse


class EditBuffer(ProfileManagement):
    """
    Define ``EditBuffer`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Edit Buffer Operation         8
    Address                       16
    Data                          104
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        EDIT_BUFFER_OPERATION = ProfileManagement.FID.SOFTWARE_ID - 1
        ADDRESS = EDIT_BUFFER_OPERATION - 1
        DATA = ADDRESS - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        EDIT_BUFFER_OPERATION = 0x8
        ADDRESS = 0x10
        DATA = 0x68
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.EDIT_BUFFER_OPERATION, length=LEN.EDIT_BUFFER_OPERATION,
                 title="EditBufferOperation", name="edit_buffer_operation",
                 checks=(CheckHexList(LEN.EDIT_BUFFER_OPERATION // 8),
                         CheckByte(),)),
        BitField(fid=FID.ADDRESS, length=LEN.ADDRESS,
                 title="Address", name="address",
                 checks=(CheckHexList(LEN.ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.ADDRESS) - 1),)),
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )

    def __init__(self, device_index, feature_index, count, opcode, address, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param opcode: Opcode
        :type opcode: ``int | HexList``
        :param address: Address
        :type address: ``int | HexList``
        :param data: Data
        :type data: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=EditBufferResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.edit_buffer_operation = self.EditBufferOperation(count=count, opcode=opcode)
        self.address = address
        self.data = data
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
        :rtype: ``EditBuffer``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.edit_buffer_operation = cls.EditBufferOperation.fromHexList(
            inner_field_container_mixin.edit_buffer_operation)
        return inner_field_container_mixin
    # end def fromHexList
# end class EditBuffer


class EditBufferResponse(LongEmptyPacketDataFormat):
    """
    Define ``EditBufferResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EditBuffer,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class EditBufferResponse


class GetSetMode(ProfileManagement):
    """
    Define ``GetSetMode`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Operating Mode                8
    Padding                       16
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        OPERATING_MODE = ProfileManagement.FID.SOFTWARE_ID - 1
        PADDING = OPERATING_MODE - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        OPERATING_MODE = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.OPERATING_MODE, length=LEN.OPERATING_MODE,
                 title="OperatingMode", name="operating_mode",
                 checks=(CheckHexList(LEN.OPERATING_MODE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, onboard_mode, set_onboard_mode, profile_mode, set_profile_mode,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param onboard_mode: Onboard Mode
        :type onboard_mode: ``int | HexList``
        :param set_onboard_mode: Set Onboard Mode
        :type set_onboard_mode: ``int | HexList``
        :param profile_mode: Profile Mode
        :type profile_mode: ``int | HexList``
        :param set_profile_mode: Set Profile Mode
        :type set_profile_mode: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSetModeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.operating_mode = self.OperatingMode(onboard_mode=onboard_mode, set_onboard_mode=set_onboard_mode,
                                                 profile_mode=profile_mode, set_profile_mode=set_profile_mode)
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
        :rtype: ``GetSetMode``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.operating_mode = cls.OperatingMode.fromHexList(
            inner_field_container_mixin.operating_mode)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetMode


class GetSetModeResponse(ProfileManagement):
    """
    Define ``GetSetModeResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Operating Mode Response       8
    Curr Profile File Id          16
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSetMode,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        OPERATING_MODE_RESPONSE = ProfileManagement.FID.SOFTWARE_ID - 1
        CURR_PROFILE_FILE_ID = OPERATING_MODE_RESPONSE - 1
        PADDING = CURR_PROFILE_FILE_ID - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        OPERATING_MODE_RESPONSE = 0x8
        CURR_PROFILE_FILE_ID = 0x10
        PADDING = 0x68
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.OPERATING_MODE_RESPONSE, length=LEN.OPERATING_MODE_RESPONSE,
                 title="OperatingModeResponse", name="operating_mode_response",
                 checks=(CheckHexList(LEN.OPERATING_MODE_RESPONSE // 8),
                         CheckByte(),)),
        BitField(fid=FID.CURR_PROFILE_FILE_ID, length=LEN.CURR_PROFILE_FILE_ID,
                 title="CurrProfileFileId", name="curr_profile_file_id",
                 checks=(CheckHexList(LEN.CURR_PROFILE_FILE_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CURR_PROFILE_FILE_ID) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, onboard_mode, profile_mode, curr_profile_file_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param onboard_mode: Onboard Mode
        :type onboard_mode: ``int | HexList``
        :param profile_mode: Profile Mode
        :type profile_mode: ``int | HexList``
        :param curr_profile_file_id: Curr Profile File Id
        :type curr_profile_file_id: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.operating_mode_response = self.OperatingModeResponse(onboard_mode=onboard_mode,
                                                                  profile_mode=profile_mode)
        self.curr_profile_file_id = curr_profile_file_id
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
        :rtype: ``GetSetModeResponse``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.operating_mode_response = cls.OperatingModeResponse.fromHexList(
            inner_field_container_mixin.operating_mode_response)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetModeResponse


class Save(ProfileManagement):
    """
    Define ``Save`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    First Sector Id               16
    Count                         16
    Hash32                        32
    Padding                       64
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        FIRST_SECTOR_ID = ProfileManagement.FID.SOFTWARE_ID - 1
        COUNT = FIRST_SECTOR_ID - 1
        HASH32 = COUNT - 1
        PADDING = HASH32 - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        FIRST_SECTOR_ID = 0x10
        COUNT = 0x10
        HASH32 = 0x20
        PADDING = 0x40
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.FIRST_SECTOR_ID, length=LEN.FIRST_SECTOR_ID,
                 title="FirstSectorId", name="first_sector_id",
                 checks=(CheckHexList(LEN.FIRST_SECTOR_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FIRST_SECTOR_ID) - 1),)),
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.HASH32, length=LEN.HASH32,
                 title="Hash32", name="hash32",
                 checks=(CheckHexList(LEN.HASH32 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HASH32) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, first_sector_id, count, hash32, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param first_sector_id: First Sector Id
        :type first_sector_id: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param hash32: Hash32
        :type hash32: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=SaveResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.first_sector_id = first_sector_id
        self.count = count
        self.hash32 = hash32
    # end def __init__
# end class Save


class SaveResponse(LongEmptyPacketDataFormat):
    """
    Define ``SaveResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Save,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class SaveResponse


class Load(ProfileManagement):
    """
    Define ``Load`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    First Sector Id               16
    Count                         16
    Padding                       96
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        FIRST_SECTOR_ID = ProfileManagement.FID.SOFTWARE_ID - 1
        COUNT = FIRST_SECTOR_ID - 1
        PADDING = COUNT - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        FIRST_SECTOR_ID = 0x10
        COUNT = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.FIRST_SECTOR_ID, length=LEN.FIRST_SECTOR_ID,
                 title="FirstSectorId", name="first_sector_id",
                 checks=(CheckHexList(LEN.FIRST_SECTOR_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FIRST_SECTOR_ID) - 1),)),
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, first_sector_id, count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param first_sector_id: First Sector Id
        :type first_sector_id: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=LoadResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.first_sector_id = first_sector_id
        self.count = count
    # end def __init__
# end class Load


class LoadResponse(LongEmptyPacketDataFormat):
    """
    Define ``LoadResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Load,)
    VERSION = (0,)
    FUNCTION_INDEX = 8

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class LoadResponse


class Configure(ProfileManagement):
    """
    Define ``Configure`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Feature Id                    16
    Configure Action              8
    File Id                       16
    Count                         16
    Hash Key                      32
    Padding                       40
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        FEATURE_ID = ProfileManagement.FID.SOFTWARE_ID - 1
        CONFIGURE_ACTION = FEATURE_ID - 1
        FILE_ID = CONFIGURE_ACTION - 1
        COUNT = FILE_ID - 1
        HASH_KEY = COUNT - 1
        PADDING = HASH_KEY - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        FEATURE_ID = 0x10
        CONFIGURE_ACTION = 0x8
        FILE_ID = 0x10
        COUNT = 0x10
        HASH_KEY = 0x20
        PADDING = 0x28
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.FEATURE_ID, length=LEN.FEATURE_ID,
                 title="FeatureId", name="feature_id",
                 checks=(CheckHexList(LEN.FEATURE_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FEATURE_ID) - 1),)),
        BitField(fid=FID.CONFIGURE_ACTION, length=LEN.CONFIGURE_ACTION,
                 title="ConfigureAction", name="configure_action",
                 checks=(CheckHexList(LEN.CONFIGURE_ACTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.FILE_ID, length=LEN.FILE_ID,
                 title="FileId", name="file_id",
                 checks=(CheckHexList(LEN.FILE_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FILE_ID) - 1),)),
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.HASH_KEY, length=LEN.HASH_KEY,
                 title="HashKey", name="hash_key",
                 aliases=('hash',),
                 checks=(CheckHexList(LEN.HASH_KEY // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HASH_KEY) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, feature_id, file_type_id, file_id, count, hash_key, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param feature_id: Feature Id
        :type feature_id: ``int | HexList``
        :param file_type_id: File Type Id
        :type file_type_id: ``int | HexList``
        :param file_id: File Id
        :type file_id: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param hash_key: Hash key
        :type hash_key: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ConfigureResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.feature_id = feature_id
        self.configure_action = self.ConfigureAction(file_type_id=file_type_id)
        self.file_id = file_id
        self.count = count
        self.hash_key = hash_key
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
        :rtype: ``Configure``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.configure_action = cls.ConfigureAction.fromHexList(
            inner_field_container_mixin.configure_action)
        return inner_field_container_mixin
    # end def fromHexList
# end class Configure


class ConfigureResponse(LongEmptyPacketDataFormat):
    """
    Define ``ConfigureResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (Configure,)
    VERSION = (0,)
    FUNCTION_INDEX = 9

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ConfigureResponse


class GetSetPowerOnParams(ProfileManagement):
    """
    Define ``GetSetPowerOnParams`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Power On Profile Action       8
    Power On Profile              16
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        POWER_ON_PROFILE_ACTION = ProfileManagement.FID.SOFTWARE_ID - 1
        POWER_ON_PROFILE = POWER_ON_PROFILE_ACTION - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        POWER_ON_PROFILE_ACTION = 0x8
        POWER_ON_PROFILE = 0x10
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.POWER_ON_PROFILE_ACTION, length=LEN.POWER_ON_PROFILE_ACTION,
                 title="PowerOnProfileAction", name="power_on_profile_action",
                 checks=(CheckHexList(LEN.POWER_ON_PROFILE_ACTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.POWER_ON_PROFILE, length=LEN.POWER_ON_PROFILE,
                 title="PowerOnProfile", name="power_on_profile",
                 checks=(CheckHexList(LEN.POWER_ON_PROFILE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.POWER_ON_PROFILE) - 1),)),
    )

    def __init__(self, device_index, feature_index, set_power_on_profile, power_on_profile, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param set_power_on_profile: Set Power On Profile
        :type set_power_on_profile: ``int | HexList``
        :param power_on_profile: Power On Profile
        :type power_on_profile: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetSetPowerOnParamsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.power_on_profile_action = self.PowerOnProfileAction(set_power_on_profile=set_power_on_profile)
        self.power_on_profile = power_on_profile
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
        :rtype: ``GetSetPowerOnParams``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.power_on_profile_action = cls.PowerOnProfileAction.fromHexList(
            inner_field_container_mixin.power_on_profile_action)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetSetPowerOnParams


class GetSetPowerOnParamsResponse(ProfileManagement):
    """
    Define ``GetSetPowerOnParamsResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Power On Profile              16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSetPowerOnParams,)
    VERSION = (0,)
    FUNCTION_INDEX = 10

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        POWER_ON_PROFILE = ProfileManagement.FID.SOFTWARE_ID - 1
        PADDING = POWER_ON_PROFILE - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        POWER_ON_PROFILE = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.POWER_ON_PROFILE, length=LEN.POWER_ON_PROFILE,
                 title="PowerOnProfile", name="power_on_profile",
                 checks=(CheckHexList(LEN.POWER_ON_PROFILE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.POWER_ON_PROFILE) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, power_on_profile, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param power_on_profile: Power On Profile
        :type power_on_profile: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.power_on_profile = power_on_profile
    # end def __init__
# end class GetSetPowerOnParamsResponse


class GetHashes(ProfileManagement):
    """
    Define ``GetHashes`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Get Hash Action               8
    File Id 0                     8
    File Id 1                     8
    File Id 2                     8
    File Id 3                     8
    Padding                       88
    ============================  ==========
    """

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        GET_HASH_ACTION = ProfileManagement.FID.SOFTWARE_ID - 1
        FILE_ID_0 = GET_HASH_ACTION - 1
        FILE_ID_1 = FILE_ID_0 - 1
        FILE_ID_2 = FILE_ID_1 - 1
        FILE_ID_3 = FILE_ID_2 - 1
        PADDING = FILE_ID_3 - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        GET_HASH_ACTION = 0x8
        FILE_ID_0 = 0x8
        FILE_ID_1 = 0x8
        FILE_ID_2 = 0x8
        FILE_ID_3 = 0x8
        PADDING = 0x58
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.GET_HASH_ACTION, length=LEN.GET_HASH_ACTION,
                 title="GetHashAction", name="get_hash_action",
                 checks=(CheckHexList(LEN.GET_HASH_ACTION // 8),
                         CheckByte(),)),
        BitField(fid=FID.FILE_ID_0, length=LEN.FILE_ID_0,
                 title="FileId0", name="file_id_0",
                 checks=(CheckHexList(LEN.FILE_ID_0 // 8),
                         CheckByte(),)),
        BitField(fid=FID.FILE_ID_1, length=LEN.FILE_ID_1,
                 title="FileId1", name="file_id_1",
                 checks=(CheckHexList(LEN.FILE_ID_1 // 8),
                         CheckByte(),)),
        BitField(fid=FID.FILE_ID_2, length=LEN.FILE_ID_2,
                 title="FileId2", name="file_id_2",
                 checks=(CheckHexList(LEN.FILE_ID_2 // 8),
                         CheckByte(),)),
        BitField(fid=FID.FILE_ID_3, length=LEN.FILE_ID_3,
                 title="FileId3", name="file_id_3",
                 checks=(CheckHexList(LEN.FILE_ID_3 // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, compute, file_id_0, file_id_1, file_id_2, file_id_3, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param compute: Compute
        :type compute: ``int | HexList``
        :param file_id_0: File Id 0
        :type file_id_0: ``int | HexList``
        :param file_id_1: File Id 1
        :type file_id_1: ``int | HexList``
        :param file_id_2: File Id 2
        :type file_id_2: ``int | HexList``
        :param file_id_3: File Id 3
        :type file_id_3: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetHashesResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.get_hash_action = self.GetHashAction(compute=compute)
        self.file_id_0 = file_id_0
        self.file_id_1 = file_id_1
        self.file_id_2 = file_id_2
        self.file_id_3 = file_id_3
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
        :rtype: ``GetHashes``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.get_hash_action = cls.GetHashAction.fromHexList(
            inner_field_container_mixin.get_hash_action)
        return inner_field_container_mixin
    # end def fromHexList
# end class GetHashes


class GetHashesResponse(ProfileManagement):
    """
    Define ``GetHashesResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Hash 0                        32
    Hash 1                        32
    Hash 2                        32
    Hash 3                        32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetHashes,)
    VERSION = (0,)
    FUNCTION_INDEX = 11

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        HASH_0 = ProfileManagement.FID.SOFTWARE_ID - 1
        HASH_1 = HASH_0 - 1
        HASH_2 = HASH_1 - 1
        HASH_3 = HASH_2 - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        HASH_0 = 0x20
        HASH_1 = 0x20
        HASH_2 = 0x20
        HASH_3 = 0x20
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.HASH_0, length=LEN.HASH_0,
                 title="Hash0", name="hash_0",
                 checks=(CheckHexList(LEN.HASH_0 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HASH_0) - 1),)),
        BitField(fid=FID.HASH_1, length=LEN.HASH_1,
                 title="Hash1", name="hash_1",
                 checks=(CheckHexList(LEN.HASH_1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HASH_1) - 1),)),
        BitField(fid=FID.HASH_2, length=LEN.HASH_2,
                 title="Hash2", name="hash_2",
                 checks=(CheckHexList(LEN.HASH_2 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HASH_2) - 1),)),
        BitField(fid=FID.HASH_3, length=LEN.HASH_3,
                 title="Hash3", name="hash_3",
                 checks=(CheckHexList(LEN.HASH_3 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.HASH_3) - 1),)),
    )

    def __init__(self, device_index, feature_index, hash_0, hash_1, hash_2, hash_3, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param hash_0: Hash 0
        :type hash_0: ``int | HexList``
        :param hash_1: Hash 1
        :type hash_1: ``int | HexList``
        :param hash_2: Hash 2
        :type hash_2: ``int | HexList``
        :param hash_3: Hash 3
        :type hash_3: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.hash_0 = hash_0
        self.hash_1 = hash_1
        self.hash_2 = hash_2
        self.hash_3 = hash_3
    # end def __init__
# end class GetHashesResponse


class ReadBuffer(BufferOffset):
    """
    Define ``ReadBuffer`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, offset_bytes, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param offset_bytes: Offset Bytes
        :type offset_bytes: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadBufferResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.offset_bytes = offset_bytes
    # end def __init__
# end class ReadBuffer


class ReadBufferResponse(BufferData):
    """
    Define ``ReadBufferResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadBuffer,)
    VERSION = (0,)
    FUNCTION_INDEX = 12

    def __init__(self, device_index, feature_index, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param data: Data
        :type data: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data = data
    # end def __init__
# end class ReadBufferResponse


class ProfileChangeEvent(ProfileManagement):
    """
    Define ``ProfileChangeEvent`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    New Profile                   16
    Profile Change Result         8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(ProfileManagement.FID):
        # See ``ProfileManagement.FID``
        NEW_PROFILE = ProfileManagement.FID.SOFTWARE_ID - 1
        PROFILE_CHANGE_RESULT = NEW_PROFILE - 1
        PADDING = PROFILE_CHANGE_RESULT - 1
    # end class FID

    class LEN(ProfileManagement.LEN):
        # See ``ProfileManagement.LEN``
        NEW_PROFILE = 0x10
        PROFILE_CHANGE_RESULT = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = ProfileManagement.FIELDS + (
        BitField(fid=FID.NEW_PROFILE, length=LEN.NEW_PROFILE,
                 title="NewProfile", name="new_profile",
                 checks=(CheckHexList(LEN.NEW_PROFILE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.NEW_PROFILE) - 1),)),
        BitField(fid=FID.PROFILE_CHANGE_RESULT, length=LEN.PROFILE_CHANGE_RESULT,
                 title="ProfileChangeResult", name="profile_change_result",
                 checks=(CheckHexList(LEN.PROFILE_CHANGE_RESULT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ProfileManagement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, new_profile, failure, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param new_profile: New Profile
        :type new_profile: ``int | HexList``
        :param failure: Failure
        :type failure: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.new_profile = new_profile
        self.profile_change_result = self.ProfileChangeResult(failure=failure)
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
        :rtype: ``ProfileChangeEvent``
        """
        inner_field_container_mixin = super().fromHexList(*args, **kwargs)
        inner_field_container_mixin.profile_change_result = cls.ProfileChangeResult.fromHexList(
            inner_field_container_mixin.profile_change_result)
        return inner_field_container_mixin
    # end def fromHexList
# end class ProfileChangeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
