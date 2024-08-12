#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.gaming.onboardprofiles
:brief: HID++ 2.0 ``OnboardProfiles`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/11/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC
from enum import IntEnum
from enum import unique

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
class OnboardProfiles(HidppMessage):
    """
    Manage onboard profile memory for devices.
    """
    FEATURE_ID = 0x8100
    MAX_FUNCTION_INDEX = 12
    MAX_FUNCTION_INDEX_V1 = 13

    @unique
    class Mode(IntEnum):
        """
        Control mode
        """
        NO_CHANGE = 0
        ONBOARD_MODE = 1
        HOST_MODE = 2
    # end class Mode

    @unique
    class SectorId(IntEnum):
        """
        Specific Sector ID
        """
        OOB_PROFILE_DIRECTORY = 0x0100
        OOB_PROFILE_START = 0x0101
        PROFILE_DIRECTORY = 0x0000
        PROFILE_START = 0x0001
    # end class SectorId

    @unique
    class Status(IntEnum):
        """
        Profile Status
        """
        DISABLED = 0
        ENABLED = 1
    # end class Status

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
# end class OnboardProfiles


class OnboardProfilesModel(FeatureModel):
    """
    Define ``OnboardProfiles`` feature model
    """
    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_ONBOARD_PROFILES_INFO = 0
        SET_ONBOARD_MODE = 1
        GET_ONBOARD_MODE = 2
        SET_ACTIVE_PROFILE = 3
        GET_ACTIVE_PROFILE = 4
        READ_DATA = 5
        START_WRITE = 6
        WRITE_DATA = 7
        END_WRITE = 8
        EXECUTE_MACRO = 9
        GET_CRC = 10
        GET_ACTIVE_PROFILE_RESOLUTION = 11
        SET_ACTIVE_PROFILE_RESOLUTION = 12
        GET_PROFILE_FIELDS_LIST = 13

        # Event index
        PROFILE_ACTIVATED = 0
        ACTIVE_PROFILE_RESOLUTION_CHANGED = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``OnboardProfiles`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        return {
            "feature_base": OnboardProfiles,
            "versions": {
                OnboardProfilesV0.VERSION: {
                    "main_cls": OnboardProfilesV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_ONBOARD_PROFILES_INFO: {
                                "request": GetOnboardProfilesInfo,
                                "response": GetOnboardProfilesInfoResponseV0
                            },
                            cls.INDEX.SET_ONBOARD_MODE: {
                                "request": SetOnboardMode,
                                "response": SetOnboardModeResponse
                            },
                            cls.INDEX.GET_ONBOARD_MODE: {
                                "request": GetOnboardMode,
                                "response": GetOnboardModeResponse
                            },
                            cls.INDEX.SET_ACTIVE_PROFILE: {
                                "request": SetActiveProfile,
                                "response": SetActiveProfileResponse
                            },
                            cls.INDEX.GET_ACTIVE_PROFILE: {
                                "request": GetActiveProfile,
                                "response": GetActiveProfileResponse
                            },
                            cls.INDEX.READ_DATA: {
                                "request": ReadData,
                                "response": ReadDataResponse
                            },
                            cls.INDEX.START_WRITE: {
                                "request": StartWrite,
                                "response": StartWriteResponse
                            },
                            cls.INDEX.WRITE_DATA: {
                                "request": WriteData,
                                "response": WriteDataResponse
                            },
                            cls.INDEX.END_WRITE: {
                                "request": EndWrite,
                                "response": EndWriteResponse
                            },
                            cls.INDEX.EXECUTE_MACRO: {
                                "request": ExecuteMacro,
                                "response": ExecuteMacroResponse
                            },
                            cls.INDEX.GET_CRC: {
                                "request": GetCrc,
                                "response": GetCrcResponse
                            },
                            cls.INDEX.GET_ACTIVE_PROFILE_RESOLUTION: {
                                "request": GetActiveProfileResolution,
                                "response": GetActiveProfileResolutionResponse
                            },
                            cls.INDEX.SET_ACTIVE_PROFILE_RESOLUTION: {
                                "request": SetActiveProfileResolution,
                                "response": SetActiveProfileResolutionResponse
                            }
                        },
                        "events": {
                            cls.INDEX.PROFILE_ACTIVATED: {
                                "report": ProfileActivatedEvent
                            },
                            cls.INDEX.ACTIVE_PROFILE_RESOLUTION_CHANGED: {
                                "report": ActiveProfileResolutionChangedEvent
                            }
                        }
                    }
                },
                OnboardProfilesV1.VERSION: {
                    "main_cls": OnboardProfilesV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_ONBOARD_PROFILES_INFO: {
                                "request": GetOnboardProfilesInfo,
                                "response": GetOnboardProfilesInfoResponseV1
                            },
                            cls.INDEX.SET_ONBOARD_MODE: {
                                "request": SetOnboardMode,
                                "response": SetOnboardModeResponse
                            },
                            cls.INDEX.GET_ONBOARD_MODE: {
                                "request": GetOnboardMode,
                                "response": GetOnboardModeResponse
                            },
                            cls.INDEX.SET_ACTIVE_PROFILE: {
                                "request": SetActiveProfile,
                                "response": SetActiveProfileResponse
                            },
                            cls.INDEX.GET_ACTIVE_PROFILE: {
                                "request": GetActiveProfile,
                                "response": GetActiveProfileResponse
                            },
                            cls.INDEX.READ_DATA: {
                                "request": ReadData,
                                "response": ReadDataResponse
                            },
                            cls.INDEX.START_WRITE: {
                                "request": StartWrite,
                                "response": StartWriteResponse
                            },
                            cls.INDEX.WRITE_DATA: {
                                "request": WriteData,
                                "response": WriteDataResponse
                            },
                            cls.INDEX.END_WRITE: {
                                "request": EndWrite,
                                "response": EndWriteResponse
                            },
                            cls.INDEX.EXECUTE_MACRO: {
                                "request": ExecuteMacro,
                                "response": ExecuteMacroResponse
                            },
                            cls.INDEX.GET_CRC: {
                                "request": GetCrc,
                                "response": GetCrcResponse
                            },
                            cls.INDEX.GET_ACTIVE_PROFILE_RESOLUTION: {
                                "request": GetActiveProfileResolution,
                                "response": GetActiveProfileResolutionResponse
                            },
                            cls.INDEX.SET_ACTIVE_PROFILE_RESOLUTION: {
                                "request": SetActiveProfileResolution,
                                "response": SetActiveProfileResolutionResponse
                            },
                            cls.INDEX.GET_PROFILE_FIELDS_LIST: {
                                "request": GetProfileFieldsList,
                                "response": GetProfileFieldsListResponse
                            }
                        },
                        "events": {
                            cls.INDEX.PROFILE_ACTIVATED: {
                                "report": ProfileActivatedEvent
                            },
                            cls.INDEX.ACTIVE_PROFILE_RESOLUTION_CHANGED: {
                                "report": ActiveProfileResolutionChangedEvent
                            }
                        }
                    }
                }
            }
        }
    # end def _get_data_model
# end class OnboardProfilesModel


class OnboardProfilesFactory(FeatureFactory):
    """
    Get ``OnboardProfiles`` object from a given version
    """
    @staticmethod
    def create(version):
        """
        Create ``OnboardProfiles`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``OnboardProfilesInterface``
        """
        return OnboardProfilesModel.get_main_cls(version)()
    # end def create
# end class OnboardProfilesFactory


class OnboardProfilesInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``OnboardProfiles`` classes
    """
    def __init__(self):
        # Requests
        self.get_onboard_profiles_info_cls = None
        self.set_onboard_mode_cls = None
        self.get_onboard_mode_cls = None
        self.set_active_profile_cls = None
        self.get_active_profile_cls = None
        self.read_data_cls = None
        self.start_write_cls = None
        self.write_data_cls = None
        self.end_write_cls = None
        self.execute_macro_cls = None
        self.get_crc_cls = None
        self.get_active_profile_resolution_cls = None
        self.set_active_profile_resolution_cls = None
        self.get_profile_fields_list_cls = None

        # Responses
        self.get_onboard_profiles_info_response_cls = None
        self.set_onboard_mode_response_cls = None
        self.get_onboard_mode_response_cls = None
        self.set_active_profile_response_cls = None
        self.get_active_profile_response_cls = None
        self.read_data_response_cls = None
        self.start_write_response_cls = None
        self.write_data_response_cls = None
        self.end_write_response_cls = None
        self.execute_macro_response_cls = None
        self.get_crc_response_cls = None
        self.get_active_profile_resolution_response_cls = None
        self.set_active_profile_resolution_response_cls = None
        self.get_profile_fields_list_response_cls = None

        # Events
        self.profile_activated_event_cls = None
        self.active_profile_resolution_changed_event_cls = None
    # end def __init__
# end class OnboardProfilesInterface


class OnboardProfilesV0(OnboardProfilesInterface):
    """
    Define ``OnboardProfilesV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getOnboardProfilesInfo() -> memoryModelID, profileFormatID, macroFormatID, profileCount, profileCountOOB,
        buttonCount, sectorCount, sectorSize, mechanicalLayout, variousInfo, sectorCountRule

    [1] setOnboardMode(onboardMode) -> None

    [2] getOnboardMode() -> onboardMode

    [3] setActiveProfile(profileID) -> None

    [4] getActiveProfile() -> profileID

    [5] readData(sectorID, subAddress, readCount) -> data

    [6] startWrite(sectorID, subAddress, writeCount) -> None

    [7] writeData(data) -> frameNb

    [8] endWrite() -> None

    [9] executeMacro(sectorID, subAddress) -> None

    [10] getCrc(sectorID) -> cRC1, cRC2, cRC3, cRC4, cRC5, cRC6, cRC7, cRC8

    [11] getActiveProfileResolution() -> resolutionIndex

    [12] setActiveProfileResolution(resolutionIndex) -> None

    [Event 0] profileActivatedEvent -> profileID

    [Event 1] activeProfileResolutionChangedEvent -> resolutionIndex
    """
    VERSION = 0

    def __init__(self):
        # See ``OnboardProfiles.__init__``
        super().__init__()
        index = OnboardProfilesModel.INDEX

        # Requests
        self.get_onboard_profiles_info_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.GET_ONBOARD_PROFILES_INFO)
        self.set_onboard_mode_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.SET_ONBOARD_MODE)
        self.get_onboard_mode_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.GET_ONBOARD_MODE)
        self.set_active_profile_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.SET_ACTIVE_PROFILE)
        self.get_active_profile_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.GET_ACTIVE_PROFILE)
        self.read_data_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.READ_DATA)
        self.start_write_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.START_WRITE)
        self.write_data_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.WRITE_DATA)
        self.end_write_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.END_WRITE)
        self.execute_macro_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.EXECUTE_MACRO)
        self.get_crc_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.GET_CRC)
        self.get_active_profile_resolution_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.GET_ACTIVE_PROFILE_RESOLUTION)
        self.set_active_profile_resolution_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.SET_ACTIVE_PROFILE_RESOLUTION)

        # Responses
        self.get_onboard_profiles_info_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.GET_ONBOARD_PROFILES_INFO)
        self.set_onboard_mode_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.SET_ONBOARD_MODE)
        self.get_onboard_mode_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.GET_ONBOARD_MODE)
        self.set_active_profile_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.SET_ACTIVE_PROFILE)
        self.get_active_profile_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.GET_ACTIVE_PROFILE)
        self.read_data_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.READ_DATA)
        self.start_write_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.START_WRITE)
        self.write_data_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.WRITE_DATA)
        self.end_write_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.END_WRITE)
        self.execute_macro_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.EXECUTE_MACRO)
        self.get_crc_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.GET_CRC)
        self.get_active_profile_resolution_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.GET_ACTIVE_PROFILE_RESOLUTION)
        self.set_active_profile_resolution_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.SET_ACTIVE_PROFILE_RESOLUTION)

        # Events
        self.profile_activated_event_cls = OnboardProfilesModel.get_report_cls(
            self.VERSION, index.PROFILE_ACTIVATED)
        self.active_profile_resolution_changed_event_cls = OnboardProfilesModel.get_report_cls(
            self.VERSION, index.ACTIVE_PROFILE_RESOLUTION_CHANGED)
    # end def __init__

    def get_max_function_index(self):
        # See ``OnboardProfilesInterface.get_max_function_index``
        return OnboardProfilesModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class OnboardProfilesV0


class OnboardProfilesV1(OnboardProfilesV0):
    """
    ``OnboardProfilesV1``

    This feature provides model and unit specific information for version 1

    M [0] getOnboardProfilesInfo() -> memoryModelID, profileFormatID, macroFormatID, profileCount, profileCountOOB,
          buttonCount, sectorCount, sectorSize, mechanicalLayout, variousInfo, sectorCountRule
    + [13] getProfileFieldsList() -> fieldsList
    """
    VERSION = 1

    def __init__(self):
        # See ``OnboardProfiles.__init__``
        super().__init__()
        index = OnboardProfilesModel.INDEX

        # Requests
        self.get_profile_fields_list_cls = OnboardProfilesModel.get_request_cls(
            self.VERSION, index.GET_PROFILE_FIELDS_LIST)

        # Responses
        self.get_profile_fields_list_response_cls = OnboardProfilesModel.get_response_cls(
            self.VERSION, index.GET_PROFILE_FIELDS_LIST)
    # end def __init__

    def get_max_function_index(self):
        # See ``OnboardProfilesInterface.get_max_function_index``
        return OnboardProfilesModel.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class OnboardProfilesV1


class ShortEmptyPacketDataFormat(OnboardProfiles):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetOnboardProfilesInfo
        - GetOnboardMode
        - GetActiveProfile
        - EndWrite
        - GetActiveProfileResolution
        - GetProfileFieldsList

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        PADDING = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(OnboardProfiles):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetOnboardModeResponse
        - SetActiveProfileResponse
        - StartWriteResponse
        - EndWriteResponse
        - ExecuteMacroResponse
        - SetActiveProfileResolutionResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        PADDING = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class OnboardModeHead(OnboardProfiles):
    """
    This class is to be used as a base class for several messages in this feature.
        - SetOnboardMode
        - GetOnboardModeResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    OnboardMode                   8
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        ONBOARD_MODE = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        ONBOARD_MODE = 0x8
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.ONBOARD_MODE, length=LEN.ONBOARD_MODE,
                 title="OnboardMode", name="onboard_mode",
                 checks=(CheckHexList(LEN.ONBOARD_MODE // 8),
                         CheckByte(),)),
    )
# end class OnboardModeHead


class ProfileIdHead(OnboardProfiles):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - GetActiveProfileResponse
        - ProfileActivatedEvent

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ProfileID                     16
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        PROFILE_ID = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        PROFILE_ID = 0x10
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.PROFILE_ID, length=LEN.PROFILE_ID,
                 title="ProfileID", name="profile_id",
                 checks=(CheckHexList(LEN.PROFILE_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PROFILE_ID) - 1),)),
    )
# end class ProfileIdHead


class SectorHead(OnboardProfiles):
    """
    This class is to be used as a base class for several messages in this feature.
        - ReadData
        - StartWrite
        - ExecuteMacro

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SectorID                      16
    SubAddress                    16
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        SECTOR_ID = OnboardProfiles.FID.SOFTWARE_ID - 1
        SUB_ADDRESS = SECTOR_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        SECTOR_ID = 0x10
        SUB_ADDRESS = 0x10
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.SECTOR_ID, length=LEN.SECTOR_ID,
                 title="SectorID", name="sector_id",
                 checks=(CheckHexList(LEN.SECTOR_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SECTOR_ID) - 1),)),
        BitField(fid=FID.SUB_ADDRESS, length=LEN.SUB_ADDRESS,
                 title="SubAddress", name="sub_address",
                 checks=(CheckHexList(LEN.SUB_ADDRESS // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SUB_ADDRESS) - 1),)),
    )
# end class SectorHead


class ReadWriteField(OnboardProfiles):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - ReadDataResponse
        - WriteData

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Data                          128
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        DATA = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        DATA = 0x80
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.DATA, length=LEN.DATA,
                 title="Data", name="data",
                 checks=(CheckHexList(LEN.DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DATA) - 1),)),
    )
# end class ReadWriteField


class ResolutionIndexHead(OnboardProfiles):
    """
    This class is to be used as a base class for several messages in this feature.
        - GetActiveProfileResolutionResponse
        - SetActiveProfileResolution

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ResolutionIndex               8
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        RESOLUTION_INDEX = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        RESOLUTION_INDEX = 0x8
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.RESOLUTION_INDEX, length=LEN.RESOLUTION_INDEX,
                 title="ResolutionIndex", name="resolution_index",
                 checks=(CheckHexList(LEN.RESOLUTION_INDEX // 8),
                         CheckByte(),)),
    )
# end class ResolutionIndexHead


class GetOnboardProfilesInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetOnboardProfilesInfo`` implementation class for versions 0 and 1
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
                         functionIndex=GetOnboardProfilesInfoResponseV0.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetOnboardProfilesInfo


class GetOnboardProfilesInfoResponseV0(OnboardProfiles):
    """
    Define ``GetOnboardProfilesInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    MemoryModelID                 8
    ProfileFormatID               8
    MacroFormatID                 8
    ProfileCount                  8
    ProfileCountOOB               8
    ButtonCount                   8
    SectorCount                   8
    SectorSize                    16
    MechanicalLayout              8
    VariousInfo                   8
    SectorCountRule               8
    Padding                       32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetOnboardProfilesInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        MEMORY_MODEL_ID = OnboardProfiles.FID.SOFTWARE_ID - 1
        PROFILE_FORMAT_ID = MEMORY_MODEL_ID - 1
        MACRO_FORMAT_ID = PROFILE_FORMAT_ID - 1
        PROFILE_COUNT = MACRO_FORMAT_ID - 1
        PROFILE_COUNT_OOB = PROFILE_COUNT - 1
        BUTTON_COUNT = PROFILE_COUNT_OOB - 1
        SECTOR_COUNT = BUTTON_COUNT - 1
        SECTOR_SIZE = SECTOR_COUNT - 1
        MECHANICAL_LAYOUT = SECTOR_SIZE - 1
        VARIOUS_INFO = MECHANICAL_LAYOUT - 1
        SECTOR_COUNT_RULE = VARIOUS_INFO - 1
        PADDING = SECTOR_COUNT_RULE - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        MEMORY_MODEL_ID = 0x8
        PROFILE_FORMAT_ID = 0x8
        MACRO_FORMAT_ID = 0x8
        PROFILE_COUNT = 0x8
        PROFILE_COUNT_OOB = 0x8
        BUTTON_COUNT = 0x8
        SECTOR_COUNT = 0x8
        SECTOR_SIZE = 0x10
        MECHANICAL_LAYOUT = 0x8
        VARIOUS_INFO = 0x8
        SECTOR_COUNT_RULE = 0x8
        PADDING = 0x20
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.MEMORY_MODEL_ID, length=LEN.MEMORY_MODEL_ID,
                 title="MemoryModelID", name="memory_model_id",
                 checks=(CheckHexList(LEN.MEMORY_MODEL_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_FORMAT_ID, length=LEN.PROFILE_FORMAT_ID,
                 title="ProfileFormatID", name="profile_format_id",
                 checks=(CheckHexList(LEN.PROFILE_FORMAT_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.MACRO_FORMAT_ID, length=LEN.MACRO_FORMAT_ID,
                 title="MacroFormatID", name="macro_format_id",
                 checks=(CheckHexList(LEN.MACRO_FORMAT_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_COUNT, length=LEN.PROFILE_COUNT,
                 title="ProfileCount", name="profile_count",
                 checks=(CheckHexList(LEN.PROFILE_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_COUNT_OOB, length=LEN.PROFILE_COUNT_OOB,
                 title="ProfileCountOOB", name="profile_count_oob",
                 checks=(CheckHexList(LEN.PROFILE_COUNT_OOB // 8),
                         CheckByte(),)),
        BitField(fid=FID.BUTTON_COUNT, length=LEN.BUTTON_COUNT,
                 title="ButtonCount", name="button_count",
                 checks=(CheckHexList(LEN.BUTTON_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.SECTOR_COUNT, length=LEN.SECTOR_COUNT,
                 title="SectorCount", name="sector_count",
                 checks=(CheckHexList(LEN.SECTOR_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.SECTOR_SIZE, length=LEN.SECTOR_SIZE,
                 title="SectorSize", name="sector_size",
                 checks=(CheckHexList(LEN.SECTOR_SIZE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SECTOR_SIZE) - 1),)),
        BitField(fid=FID.MECHANICAL_LAYOUT, length=LEN.MECHANICAL_LAYOUT,
                 title="MechanicalLayout", name="mechanical_layout",
                 checks=(CheckHexList(LEN.MECHANICAL_LAYOUT // 8),
                         CheckByte(),)),
        BitField(fid=FID.VARIOUS_INFO, length=LEN.VARIOUS_INFO,
                 title="VariousInfo", name="various_info",
                 checks=(CheckHexList(LEN.VARIOUS_INFO // 8),
                         CheckByte(),)),
        BitField(fid=FID.SECTOR_COUNT_RULE, length=LEN.SECTOR_COUNT_RULE,
                 title="SectorCountRule", name="sector_count_rule",
                 checks=(CheckHexList(LEN.SECTOR_COUNT_RULE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 memory_model_id, profile_format_id, macro_format_id, profile_count, profile_count_oob, button_count,
                 sector_count, sector_size, mechanical_layout, various_info, sector_count_rule, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param memory_model_id: This field provides the memory organization in the device.
        :type memory_model_id: ``int`` or ``HexList``
        :param profile_format_id: Format of the Profile headers and of the Profile Directory.
        :type profile_format_id: ``int`` or ``HexList``
        :param macro_format_id: Type of Macros supported by the device.
        :type macro_format_id: ``int`` or ``HexList``
        :param profile_count: Number of Profiles.
        :type profile_count: ``int`` or ``HexList``
        :param profile_count_oob: Number of Profiles available OOB in the device.
        :type profile_count_oob: ``int`` or ``HexList``
        :param button_count: Number of customizable buttons or keys
        :type button_count: ``int`` or ``HexList``
        :param sector_count: Number of Sectors writable (by SW)
        :type sector_count: ``int`` or ``HexList``
        :param sector_size: Size of a "Software Sector".
        :type sector_size: ``int`` or ``HexList``
        :param mechanical_layout: Informs whether the button mechanical configuration supports correctly
                                  the listed functionalities
        :type mechanical_layout: ``int`` or ``HexList``
        :param various_info: The types of Device connection.
        :type various_info: ``int`` or ``HexList``
        :param sector_count_rule: Specify where and how many Macros can be set.
        :type sector_count_rule: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.memory_model_id = memory_model_id
        self.profile_format_id = profile_format_id
        self.macro_format_id = macro_format_id
        self.profile_count = profile_count
        self.profile_count_oob = profile_count_oob
        self.button_count = button_count
        self.sector_count = sector_count
        self.sector_size = sector_size
        self.mechanical_layout = mechanical_layout
        self.various_info = various_info
        self.sector_count_rule = sector_count_rule
    # end def __init__
# end class GetOnboardProfilesInfoResponseV0


class GetOnboardProfilesInfoResponseV1(OnboardProfiles):
    """
    Define ``GetOnboardProfilesInfoResponse`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    MemoryModelID                 8
    ProfileFormatID               8
    MacroFormatID                 8
    ProfileCount                  8
    ProfileCountOOB               8
    ButtonCount                   8
    SectorCount                   8
    SectorSize                    8
    MechanicalLayout              8
    VariousInfo                   8
    SectorCountRule               8
    SupportedHostLayer            8
    Padding                       32
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetOnboardProfilesInfo,)
    VERSION = (1,)
    FUNCTION_INDEX = 0

    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        MEMORY_MODEL_ID = OnboardProfiles.FID.SOFTWARE_ID - 1
        PROFILE_FORMAT_ID = MEMORY_MODEL_ID - 1
        MACRO_FORMAT_ID = PROFILE_FORMAT_ID - 1
        PROFILE_COUNT = MACRO_FORMAT_ID - 1
        PROFILE_COUNT_OOB = PROFILE_COUNT - 1
        BUTTON_COUNT = PROFILE_COUNT_OOB - 1
        SECTOR_COUNT = BUTTON_COUNT - 1
        SECTOR_SIZE = SECTOR_COUNT - 1
        MECHANICAL_LAYOUT = SECTOR_SIZE - 1
        VARIOUS_INFO = MECHANICAL_LAYOUT - 1
        SECTOR_COUNT_RULE = VARIOUS_INFO - 1
        SUPPORTED_HOST_LAYER = SECTOR_COUNT_RULE - 1
        PADDING = SUPPORTED_HOST_LAYER - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        MEMORY_MODEL_ID = 0x8
        PROFILE_FORMAT_ID = 0x8
        MACRO_FORMAT_ID = 0x8
        PROFILE_COUNT = 0x8
        PROFILE_COUNT_OOB = 0x8
        BUTTON_COUNT = 0x8
        SECTOR_COUNT = 0x8
        SECTOR_SIZE = 0x8
        MECHANICAL_LAYOUT = 0x8
        VARIOUS_INFO = 0x8
        SECTOR_COUNT_RULE = 0x8
        SUPPORTED_HOST_LAYER = 0x8
        PADDING = 0x20
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.MEMORY_MODEL_ID, length=LEN.MEMORY_MODEL_ID,
                 title="MemoryModelID", name="memory_model_id",
                 checks=(CheckHexList(LEN.MEMORY_MODEL_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_FORMAT_ID, length=LEN.PROFILE_FORMAT_ID,
                 title="ProfileFormatID", name="profile_format_id",
                 checks=(CheckHexList(LEN.PROFILE_FORMAT_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.MACRO_FORMAT_ID, length=LEN.MACRO_FORMAT_ID,
                 title="MacroFormatID", name="macro_format_id",
                 checks=(CheckHexList(LEN.MACRO_FORMAT_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_COUNT, length=LEN.PROFILE_COUNT,
                 title="ProfileCount", name="profile_count",
                 checks=(CheckHexList(LEN.PROFILE_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PROFILE_COUNT_OOB, length=LEN.PROFILE_COUNT_OOB,
                 title="ProfileCountOOB", name="profile_count_oob",
                 checks=(CheckHexList(LEN.PROFILE_COUNT_OOB // 8),
                         CheckByte(),)),
        BitField(fid=FID.BUTTON_COUNT, length=LEN.BUTTON_COUNT,
                 title="ButtonCount", name="button_count",
                 checks=(CheckHexList(LEN.BUTTON_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.SECTOR_COUNT, length=LEN.SECTOR_COUNT,
                 title="SectorCount", name="sector_count",
                 checks=(CheckHexList(LEN.SECTOR_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.SECTOR_SIZE, length=LEN.SECTOR_SIZE,
                 title="SectorSize", name="sector_size",
                 checks=(CheckHexList(LEN.SECTOR_SIZE // 8),
                         CheckByte(),)),
        BitField(fid=FID.MECHANICAL_LAYOUT, length=LEN.MECHANICAL_LAYOUT,
                 title="MechanicalLayout", name="mechanical_layout",
                 checks=(CheckHexList(LEN.MECHANICAL_LAYOUT // 8),
                         CheckByte(),)),
        BitField(fid=FID.VARIOUS_INFO, length=LEN.VARIOUS_INFO,
                 title="VariousInfo", name="various_info",
                 checks=(CheckHexList(LEN.VARIOUS_INFO // 8),
                         CheckByte(),)),
        BitField(fid=FID.SECTOR_COUNT_RULE, length=LEN.SECTOR_COUNT_RULE,
                 title="SectorCountRule", name="sector_count_rule",
                 checks=(CheckHexList(LEN.SECTOR_COUNT_RULE // 8),
                         CheckByte(),)),
        BitField(fid=FID.SUPPORTED_HOST_LAYER, length=LEN.SUPPORTED_HOST_LAYER,
                 title="SupportedHostLayer", name="supported_host_layer",
                 checks=(CheckHexList(LEN.SUPPORTED_HOST_LAYER // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index,
                 memory_model_id, profile_format_id, macro_format_id, profile_count, profile_count_oob, button_count,
                 sector_count, sector_size, mechanical_layout, various_info, sector_count_rule, supported_host_layer,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param memory_model_id: This field provides the memory organization in the device.
        :type memory_model_id: ``int`` or ``HexList``
        :param profile_format_id: Format of the Profile headers and of the Profile Directory.
        :type profile_format_id: ``int`` or ``HexList``
        :param macro_format_id: Type of Macros supported by the device.
        :type macro_format_id: ``int`` or ``HexList``
        :param profile_count: Number of Profiles.
        :type profile_count: ``int`` or ``HexList``
        :param profile_count_oob: Number of Profiles available OOB in the device.
        :type profile_count_oob: ``int`` or ``HexList``
        :param button_count: Number of customizable buttons or keys
        :type button_count: ``int`` or ``HexList``
        :param sector_count: Number of Sectors writable (by SW)
        :type sector_count: ``int`` or ``HexList``
        :param sector_size: Size of a "Software Sector".
        :type sector_size: ``int`` or ``HexList``
        :param mechanical_layout: Informs whether the button mechanical configuration supports correctly
                                  the listed functionalities
        :type mechanical_layout: ``int`` or ``HexList``
        :param various_info: The types of Device connection.
        :type various_info: ``int`` or ``HexList``
        :param sector_count_rule: Specify where and how many Macros can be set.
        :type sector_count_rule: ``int`` or ``HexList``
        :param supported_host_layer: Informs whether host and layer concepts are supported with onboard profiles
        :type supported_host_layer: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.memory_model_id = memory_model_id
        self.profile_format_id = profile_format_id
        self.macro_format_id = macro_format_id
        self.profile_count = profile_count
        self.profile_count_oob = profile_count_oob
        self.button_count = button_count
        self.sector_count = sector_count
        self.sector_size = sector_size
        self.mechanical_layout = mechanical_layout
        self.various_info = various_info
        self.sector_count_rule = sector_count_rule
        self.supported_host_layer = supported_host_layer
    # end def __init__
# end class GetOnboardProfilesInfoResponseV1


class SetOnboardMode(OnboardModeHead):
    """
    Define ``SetOnboardMode`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    OnboardMode                   8
    Padding                       16
    ============================  ==========
    """
    class FID(OnboardModeHead.FID):
        # See ``OnboardModeHead.FID``
        PADDING = OnboardModeHead.FID.ONBOARD_MODE - 1
    # end class FID

    class LEN(OnboardModeHead.LEN):
        # See ``OnboardModeHead.LEN``
        PADDING = 0x10
    # end class LEN

    FIELDS = OnboardModeHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, onboard_mode, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param onboard_mode: Indicates the device onboard mode.
        :type onboard_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetOnboardModeResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.onboard_mode = onboard_mode
    # end def __init__
# end class SetOnboardMode


class SetOnboardModeResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetOnboardModeResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetOnboardMode,)
    VERSION = (0, 1,)
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
# end class SetOnboardModeResponse


class GetOnboardMode(ShortEmptyPacketDataFormat):
    """
    Define ``GetOnboardMode`` implementation class for versions 0 and 1
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
                         functionIndex=GetOnboardModeResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetOnboardMode


class GetOnboardModeResponse(OnboardModeHead):
    """
    Define ``GetOnboardModeResponse`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    OnboardMode                   8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetOnboardMode,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    class FID(OnboardModeHead.FID):
        # See ``OnboardModeHead.FID``
        PADDING = OnboardModeHead.FID.ONBOARD_MODE - 1
    # end class FID

    class LEN(OnboardModeHead.LEN):
        # See ``OnboardModeHead.LEN``
        PADDING = 0x78
    # end class LEN

    FIELDS = OnboardModeHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, onboard_mode, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param onboard_mode: Retrieve the device mode.
        :type onboard_mode: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.onboard_mode = onboard_mode
    # end def __init__
# end class GetOnboardModeResponse


class SetActiveProfile(ProfileIdHead):
    """
    Define ``SetActiveProfile`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ProfileID                     16
    Padding                       8
    ============================  ==========
    """
    class FID(ProfileIdHead.FID):
        # See ``ProfileIdHead.FID``
        PADDING = ProfileIdHead.FID.PROFILE_ID - 1
    # end class FID

    class LEN(ProfileIdHead.LEN):
        # See ``ProfileIdHead.LEN``
        PADDING = 0x8
    # end class LEN

    FIELDS = ProfileIdHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, profile_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param profile_id: Indicates the onboard profile to activate.
        :type profile_id: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetActiveProfileResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.profile_id = profile_id
    # end def __init__
# end class SetActiveProfile


class SetActiveProfileResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetActiveProfileResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetActiveProfile,)
    VERSION = (0, 1,)
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
# end class SetActiveProfileResponse


class GetActiveProfile(ShortEmptyPacketDataFormat):
    """
    Define ``GetActiveProfile`` implementation class for versions 0 and 1
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
                         functionIndex=GetActiveProfileResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetActiveProfile


class GetActiveProfileResponse(ProfileIdHead):
    """
    Define ``GetActiveProfileResponse`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ProfileID                     16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetActiveProfile,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 4

    class FID(ProfileIdHead.FID):
        # See ``ProfileIdHead.FID``
        PADDING = ProfileIdHead.FID.PROFILE_ID - 1
    # end class FID

    class LEN(ProfileIdHead.LEN):
        # See ``ProfileIdHead.LEN``
        PADDING = 0x70
    # end class LEN

    FIELDS = ProfileIdHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, profile_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param profile_id: The current Profile.
        :type profile_id: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.profile_id = profile_id
    # end def __init__
# end class GetActiveProfileResponse


class ReadData(SectorHead):
    """
    Define ``ReadData`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SectorID                      16
    SubAddress                    16
    ReadCount                     8
    Padding                       88
    ============================  ==========
    """
    class FID(SectorHead.FID):
        # See ``SectorHead.FID``
        READ_COUNT = SectorHead.FID.SUB_ADDRESS - 1
        PADDING = READ_COUNT - 1
    # end class FID

    class LEN(SectorHead.LEN):
        # See ``SectorHead.LEN``
        READ_COUNT = 0x8
        PADDING = 0x58
    # end class LEN

    FIELDS = SectorHead.FIELDS + (
        BitField(fid=FID.READ_COUNT, length=LEN.READ_COUNT,
                 title="ReadCount", name="read_count",
                 checks=(CheckHexList(LEN.READ_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sector_id, sub_address, read_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sector_id: Sector to read from
        :type sector_id: ``int`` or ``HexList``
        :param sub_address: Sub address to read from
        :type sub_address: ``int`` or ``HexList``
        :param read_count: Number of bytes to read
        :type read_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ReadDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sector_id = sector_id
        self.sub_address = sub_address
        self.read_count = read_count
    # end def __init__
# end class ReadData


class ReadDataResponse(ReadWriteField):
    """
    Define ``ReadDataResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadData,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data: Bytes of data
        :type data: ``list`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data = data
    # end def __init__
# end class ReadDataResponse


class StartWrite(SectorHead):
    """
    Define ``StartWrite`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SectorID                      16
    SubAddress                    16
    WriteCount                    16
    Padding                       80
    ============================  ==========
    """
    class FID(SectorHead.FID):
        # See ``SectorHead.FID``
        WRITE_COUNT = SectorHead.FID.SUB_ADDRESS - 1
        PADDING = WRITE_COUNT - 1
    # end class FID

    class LEN(SectorHead.LEN):
        # See ``SectorHead.LEN``
        WRITE_COUNT = 0x10
        PADDING = 0x50
    # end class LEN

    FIELDS = SectorHead.FIELDS + (
        BitField(fid=FID.WRITE_COUNT, length=LEN.WRITE_COUNT,
                 title="WriteCount", name="write_count",
                 checks=(CheckHexList(LEN.WRITE_COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.WRITE_COUNT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sector_id, sub_address, write_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sector_id: Sector to write to (final destination)
        :type sector_id: ``int`` or ``HexList``
        :param sub_address: Sub address to write to (final destination)
        :type sub_address: ``int`` or ``HexList``
        :param write_count: Number of bytes to write
        :type write_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=StartWriteResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sector_id = sector_id
        self.sub_address = sub_address
        self.write_count = write_count
    # end def __init__
# end class StartWrite


class StartWriteResponse(LongEmptyPacketDataFormat):
    """
    Define ``StartWriteResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartWrite,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 6

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
# end class StartWriteResponse


class WriteData(ReadWriteField):
    """
    Define ``WriteData`` implementation class for versions 0 and 1
    """
    def __init__(self, device_index, feature_index, data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param data: Data to write
        :type data: ``list`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=WriteDataResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.data = data
    # end def __init__
# end class WriteData


class WriteDataResponse(OnboardProfiles):
    """
    Define ``WriteDataResponse`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    FrameNb                       16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteData,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 7

    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        FRAME_NB = OnboardProfiles.FID.SOFTWARE_ID - 1
        PADDING = FRAME_NB - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        FRAME_NB = 0x10
        PADDING = 0x70
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.FRAME_NB, length=LEN.FRAME_NB,
                 title="FrameNb", name="frame_nb",
                 checks=(CheckHexList(LEN.FRAME_NB // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FRAME_NB) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, frame_nb, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param frame_nb: Incremented at each writeData(), reset during startWrite()
        :type frame_nb: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.frame_nb = frame_nb
    # end def __init__
# end class WriteDataResponse


class EndWrite(ShortEmptyPacketDataFormat):
    """
    Define ``EndWrite`` implementation class for versions 0 and 1
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
                         functionIndex=EndWriteResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class EndWrite


class EndWriteResponse(LongEmptyPacketDataFormat):
    """
    Define``EndWriteResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EndWrite,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 8

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
# end class EndWriteResponse


class ExecuteMacro(SectorHead):
    """
    Define ``ExecuteMacro`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SectorID                      16
    SubAddress                    16
    Padding                       96
    ============================  ==========
    """
    class FID(SectorHead.FID):
        # See ``SectorHead.FID``
        PADDING = SectorHead.FID.SUB_ADDRESS - 1
    # end class FID

    class LEN(SectorHead.LEN):
        # See ``SectorHead.LEN``
        PADDING = 0x60
    # end class LEN

    FIELDS = SectorHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sector_id, sub_address, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sector_id: Sector to execute
        :type sector_id: ``int`` or ``HexList``
        :param sub_address: Sub address to execute
        :type sub_address: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=ExecuteMacroResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sector_id = sector_id
        self.sub_address = sub_address
    # end def __init__
# end class ExecuteMacro


class ExecuteMacroResponse(LongEmptyPacketDataFormat):
    """
    Define ``ExecuteMacroResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ExecuteMacro,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 9

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
# end class ExecuteMacroResponse


class GetCrc(OnboardProfiles):
    """
    Define ``GetCrc`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SectorID                      16
    Padding                       8
    ============================  ==========
    """
    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        SECTOR_ID = OnboardProfiles.FID.SOFTWARE_ID - 1
        PADDING = SECTOR_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        SECTOR_ID = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.SECTOR_ID, length=LEN.SECTOR_ID,
                 title="SectorID", name="sector_id",
                 checks=(CheckHexList(LEN.SECTOR_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SECTOR_ID) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sector_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sector_id: Sector to start
        :type sector_id: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetCrcResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sector_id = sector_id
    # end def __init__
# end class GetCrc


class GetCrcResponse(OnboardProfiles):
    """
    Define ``GetCrcResponse`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    CRC1                          16
    CRC2                          16
    CRC3                          16
    CRC4                          16
    CRC5                          16
    CRC6                          16
    CRC7                          16
    CRC8                          16
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCrc,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 10

    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        CRC_1 = OnboardProfiles.FID.SOFTWARE_ID - 1
        CRC_2 = CRC_1 - 1
        CRC_3 = CRC_2 - 1
        CRC_4 = CRC_3 - 1
        CRC_5 = CRC_4 - 1
        CRC_6 = CRC_5 - 1
        CRC_7 = CRC_6 - 1
        CRC_8 = CRC_7 - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        CRC_1 = 0x10
        CRC_2 = 0x10
        CRC_3 = 0x10
        CRC_4 = 0x10
        CRC_5 = 0x10
        CRC_6 = 0x10
        CRC_7 = 0x10
        CRC_8 = 0x10
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.CRC_1, length=LEN.CRC_1,
                 title="CRC1", name="crc_1",
                 checks=(CheckHexList(LEN.CRC_1 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_1) - 1),)),
        BitField(fid=FID.CRC_2, length=LEN.CRC_2,
                 title="CRC2", name="crc_2",
                 checks=(CheckHexList(LEN.CRC_2 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_2) - 1),)),
        BitField(fid=FID.CRC_3, length=LEN.CRC_3,
                 title="CRC3", name="crc_3",
                 checks=(CheckHexList(LEN.CRC_3 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_3) - 1),)),
        BitField(fid=FID.CRC_4, length=LEN.CRC_4,
                 title="CRC4", name="crc_4",
                 checks=(CheckHexList(LEN.CRC_4 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_4) - 1),)),
        BitField(fid=FID.CRC_5, length=LEN.CRC_5,
                 title="CRC5", name="crc_5",
                 checks=(CheckHexList(LEN.CRC_5 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_5) - 1),)),
        BitField(fid=FID.CRC_6, length=LEN.CRC_6,
                 title="CRC6", name="crc_6",
                 checks=(CheckHexList(LEN.CRC_6 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_6) - 1),)),
        BitField(fid=FID.CRC_7, length=LEN.CRC_7,
                 title="CRC7", name="crc_7",
                 checks=(CheckHexList(LEN.CRC_7 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_7) - 1),)),
        BitField(fid=FID.CRC_8, length=LEN.CRC_8,
                 title="CRC8", name="crc_8",
                 checks=(CheckHexList(LEN.CRC_8 // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CRC_8) - 1),)),
    )

    def __init__(self, device_index, feature_index, crc_1, crc_2, crc_3, crc_4, crc_5, crc_6, crc_7, crc_8, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param crc_1: The CRC-16 CCITT result.
        :type crc_1: ``int`` or ``HexList``
        :param crc_2: The CRC-16 CCITT result.
        :type crc_2: ``int`` or ``HexList``
        :param crc_3: The CRC-16 CCITT result.
        :type crc_3: ``int`` or ``HexList``
        :param crc_4: The CRC-16 CCITT result.
        :type crc_4: ``int`` or ``HexList``
        :param crc_5: The CRC-16 CCITT result.
        :type crc_5: ``int`` or ``HexList``
        :param crc_6: The CRC-16 CCITT result.
        :type crc_6: ``int`` or ``HexList``
        :param crc_7: The CRC-16 CCITT result.
        :type crc_7: ``int`` or ``HexList``
        :param crc_8: The CRC-16 CCITT result.
        :type crc_8: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.crc_1 = crc_1
        self.crc_2 = crc_2
        self.crc_3 = crc_3
        self.crc_4 = crc_4
        self.crc_5 = crc_5
        self.crc_6 = crc_6
        self.crc_7 = crc_7
        self.crc_8 = crc_8
    # end def __init__
# end class GetCrcResponse


class GetActiveProfileResolution(ShortEmptyPacketDataFormat):
    """
    Define ``GetActiveProfileResolution`` implementation class for versions 0 and 1
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
                         functionIndex=GetActiveProfileResolutionResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetActiveProfileResolution


class GetActiveProfileResolutionResponse(ResolutionIndexHead):
    """
    Define ``GetActiveProfileResolutionResponse`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ResolutionIndex               8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetActiveProfileResolution,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 11

    class FID(ResolutionIndexHead.FID):
        # See ``ResolutionIndexHead.FID``
        PADDING = ResolutionIndexHead.FID.RESOLUTION_INDEX - 1
    # end class FID

    class LEN(ResolutionIndexHead.LEN):
        # See ``ResolutionIndexHead.LEN``
        PADDING = 0x78
    # end class LEN

    FIELDS = ResolutionIndexHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, resolution_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param resolution_index: The Resolution index in range [0..4]
        :type resolution_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.resolution_index = resolution_index
    # end def __init__
# end class GetActiveProfileResolutionResponse


class SetActiveProfileResolution(ResolutionIndexHead):
    """
   Define  ``SetActiveProfileResolution`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ResolutionIndex               8
    Padding                       16
    ============================  ==========
    """
    class FID(ResolutionIndexHead.FID):
        # See ``ResolutionIndexHead.FID``
        PADDING = ResolutionIndexHead.FID.RESOLUTION_INDEX - 1
    # end class FID

    class LEN(ResolutionIndexHead.LEN):
        # See ``ResolutionIndexHead.LEN``
        PADDING = 0x10
    # end class LEN

    FIELDS = ResolutionIndexHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, resolution_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param resolution_index: The Resolution index in range [0..4]
        :type resolution_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetActiveProfileResolutionResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.resolution_index = resolution_index
    # end def __init__
# end class SetActiveProfileResolution


class SetActiveProfileResolutionResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetActiveProfileResolutionResponse`` implementation class for versions 0 and 1
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetActiveProfileResolution,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 12

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
# end class SetActiveProfileResolutionResponse


class GetProfileFieldsList(ShortEmptyPacketDataFormat):
    """
    Define ``GetProfileFieldsList`` implementation class for version 1
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
                         functionIndex=GetProfileFieldsListResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetProfileFieldsList


class GetProfileFieldsListResponse(OnboardProfiles):
    """
    Define ``GetProfileFieldsListResponse`` implementation class for version 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    FieldsList                    128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetProfileFieldsList,)
    VERSION = (1,)
    FUNCTION_INDEX = 13

    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        FIELDS_LIST = OnboardProfiles.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        FIELDS_LIST = 0x80
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.FIELDS_LIST, length=LEN.FIELDS_LIST,
                 title="FieldsList", name="fields_list",
                 checks=(CheckHexList(LEN.FIELDS_LIST // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FIELDS_LIST) - 1),)),
    )

    def __init__(self, device_index, feature_index, fields_list, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param fields_list: Fields list in a Tag-Length format
        :type fields_list: ``list`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.fields_list = fields_list
    # end def __init__
# end class GetProfileFieldsListResponse


class ProfileActivatedEvent(ProfileIdHead):
    """
    Define ``ProfileActivatedEvent`` implementation class for versions 0 and 1

        Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ProfileID                     16
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(ProfileIdHead.FID):
        # See ``ProfileIdHead.FID``
        PADDING = ProfileIdHead.FID.PROFILE_ID - 1
    # end class FID

    class LEN(ProfileIdHead.LEN):
        # See ``ProfileIdHead.LEN``
        PADDING = 0x70
    # end class LEN

    FIELDS = ProfileIdHead.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, profile_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param profile_id: The activated profile ID.
        :type profile_id: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.profile_id = profile_id
    # end def __init__
# end class ProfileActivatedEvent


class ActiveProfileResolutionChangedEvent(OnboardProfiles):
    """
    Define ``ActiveProfileResolutionChangedEvent`` implementation class for versions 0 and 1

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ResolutionIndex               8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    class FID(OnboardProfiles.FID):
        # See ``OnboardProfiles.FID``
        RESOLUTION_INDEX = OnboardProfiles.FID.SOFTWARE_ID - 1
        PADDING = RESOLUTION_INDEX - 1
    # end class FID

    class LEN(OnboardProfiles.LEN):
        # See ``OnboardProfiles.LEN``
        RESOLUTION_INDEX = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = OnboardProfiles.FIELDS + (
        BitField(fid=FID.RESOLUTION_INDEX, length=LEN.RESOLUTION_INDEX,
                 title="ResolutionIndex", name="resolution_index",
                 checks=(CheckHexList(LEN.RESOLUTION_INDEX // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.RESOLUTION_INDEX) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OnboardProfiles.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, resolution_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param resolution_index: The Resolution index in range [0..4].
        :type resolution_index: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.resolution_index = resolution_index
    # end def __init__
# end class ActiveProfileResolutionChangedEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
