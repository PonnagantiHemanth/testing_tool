#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.2'
:package: pyhid.hidpp.features.common.opticalswitches
:brief: HID++ 2.0 ``OpticalSwitches`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2023/03/08
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
class OpticalSwitches(HidppMessage):
    """
    An optical switch is a component consisting of an optocoupler system, IR LED and photo-transistor. This feature
    handles the mask table of available keys as well as examines the functionality of optical switches
    """
    FEATURE_ID = 0x1876
    MAX_FUNCTION_INDEX = 6

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
# end class OpticalSwitches


class OpticalSwitchesModel(FeatureModel):
    """
    Define ``OpticalSwitches`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_HARDWARE_INFO = 0
        GENERATE_MASK_TABLE = 1
        GET_MASK_TABLE = 2
        INIT_TEST = 3
        GET_KEY_RELEASE_TIMINGS = 4
        CONFIG_EMIT_TIME = 5
        END_TEST = 6
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``OpticalSwitches`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_HARDWARE_INFO: {
                    "request": GetHardwareInfo,
                    "response": GetHardwareInfoResponse
                },
                cls.INDEX.GENERATE_MASK_TABLE: {
                    "request": GenerateMaskTable,
                    "response": GenerateMaskTableResponse
                },
                cls.INDEX.GET_MASK_TABLE: {
                    "request": GetMaskTable,
                    "response": GetMaskTableResponse
                },
                cls.INDEX.INIT_TEST: {
                    "request": InitTest,
                    "response": InitTestResponse
                },
                cls.INDEX.GET_KEY_RELEASE_TIMINGS: {
                    "request": GetKeyReleaseTimings,
                    "response": GetKeyReleaseTimingsResponse
                },
                cls.INDEX.CONFIG_EMIT_TIME: {
                    "request": ConfigEmitTime,
                    "response": ConfigEmitTimeResponse
                },
                cls.INDEX.END_TEST: {
                    "request": EndTest,
                    "response": EndTestResponse
                }
            }
        }

        return {
            "feature_base": OpticalSwitches,
            "versions": {
                OpticalSwitchesV0.VERSION: {
                    "main_cls": OpticalSwitchesV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class OpticalSwitchesModel


class OpticalSwitchesFactory(FeatureFactory):
    """
    Get ``OpticalSwitches`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``OpticalSwitches`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``OpticalSwitchesInterface``
        """
        return OpticalSwitchesModel.get_main_cls(version)()
    # end def create
# end class OpticalSwitchesFactory


class OpticalSwitchesInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``OpticalSwitches``
    """

    def __init__(self):
        # Requests
        self.get_hardware_info_cls = None
        self.generate_mask_table_cls = None
        self.get_mask_table_cls = None
        self.init_test_cls = None
        self.get_key_release_timings_cls = None
        self.config_emit_time_cls = None
        self.end_test_cls = None

        # Responses
        self.get_hardware_info_response_cls = None
        self.generate_mask_table_response_cls = None
        self.get_mask_table_response_cls = None
        self.init_test_response_cls = None
        self.get_key_release_timings_response_cls = None
        self.config_emit_time_response_cls = None
        self.end_test_response_cls = None
    # end def __init__
# end class OpticalSwitchesInterface


class OpticalSwitchesV0(OpticalSwitchesInterface):
    """
    Define ``OpticalSwitchesV0`` feature

    This feature provides model and unit specific information for version 0

    [0] GetHardwareInfo() -> NbColumns, NbRows, TimeoutUs

    [1] GenerateMaskTable() -> NbAvailableKeys

    [2] GetMaskTable(ColumnIdx) -> Port0RowMask, Port1RowMask

    [3] InitTest() -> None

    [4] GetKeyReleaseTimings(ColumnIdx) -> MinDuration, MaxDuration

    [5] ConfigEmitTime(EmitTimeUs) -> None

    [6] EndTest() -> None
    """
    VERSION = 0

    def __init__(self):
        # See ``OpticalSwitches.__init__``
        super().__init__()
        index = OpticalSwitchesModel.INDEX

        # Requests
        self.get_hardware_info_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.GET_HARDWARE_INFO)
        self.generate_mask_table_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.GENERATE_MASK_TABLE)
        self.get_mask_table_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.GET_MASK_TABLE)
        self.init_test_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.INIT_TEST)
        self.get_key_release_timings_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.GET_KEY_RELEASE_TIMINGS)
        self.config_emit_time_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.CONFIG_EMIT_TIME)
        self.end_test_cls = OpticalSwitchesModel.get_request_cls(
            self.VERSION, index.END_TEST)

        # Responses
        self.get_hardware_info_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.GET_HARDWARE_INFO)
        self.generate_mask_table_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.GENERATE_MASK_TABLE)
        self.get_mask_table_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.GET_MASK_TABLE)
        self.init_test_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.INIT_TEST)
        self.get_key_release_timings_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.GET_KEY_RELEASE_TIMINGS)
        self.config_emit_time_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.CONFIG_EMIT_TIME)
        self.end_test_response_cls = OpticalSwitchesModel.get_response_cls(
            self.VERSION, index.END_TEST)
    # end def __init__

    def get_max_function_index(self):
        # See ``OpticalSwitchesInterface.get_max_function_index``
        return OpticalSwitchesModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class OpticalSwitchesV0


class ShortEmptyPacketDataFormat(OpticalSwitches):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - GetHardwareInfo
        - GenerateMaskTable
        - InitTest
        - EndTest

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        PADDING = OpticalSwitches.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(OpticalSwitches):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - InitTestResponse
        - ConfigEmitTimeResponse
        - EndTestResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        PADDING = OpticalSwitches.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class ColumnIndex(OpticalSwitches):
    """
    Define reusable class to be used as a base class for several messages in this feature.
        - GetMaskTable
        - GetKeyReleaseTimings

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Column Idx                    8
    Padding                       16
    ============================  ==========
    """

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        COLUMN_IDX = OpticalSwitches.FID.SOFTWARE_ID - 1
        PADDING = COLUMN_IDX - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        COLUMN_IDX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.COLUMN_IDX, length=LEN.COLUMN_IDX,
                 title="ColumnIdx", name="column_idx",
                 checks=(CheckHexList(LEN.COLUMN_IDX // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),
    )
# end class ColumnIndex


class GetHardwareInfo(ShortEmptyPacketDataFormat):
    """
    Define ``GetHardwareInfo`` implementation class for version 0
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
                         function_index=GetHardwareInfoResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetHardwareInfo


class GetHardwareInfoResponse(OpticalSwitches):
    """
    Define ``GetHardwareInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Nb Columns                    8
    Nb Rows                       8
    Timeout Us                    8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetHardwareInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        NB_COLUMNS = OpticalSwitches.FID.SOFTWARE_ID - 1
        NB_ROWS = NB_COLUMNS - 1
        TIMEOUT_US = NB_ROWS - 1
        PADDING = TIMEOUT_US - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        NB_COLUMNS = 0x8
        NB_ROWS = 0x8
        TIMEOUT_US = 0x8
        PADDING = 0x68
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.NB_COLUMNS, length=LEN.NB_COLUMNS,
                 title="NbColumns", name="nb_columns",
                 checks=(CheckHexList(LEN.NB_COLUMNS // 8),
                         CheckByte(),)),
        BitField(fid=FID.NB_ROWS, length=LEN.NB_ROWS,
                 title="NbRows", name="nb_rows",
                 checks=(CheckHexList(LEN.NB_ROWS // 8),
                         CheckByte(),)),
        BitField(fid=FID.TIMEOUT_US, length=LEN.TIMEOUT_US,
                 title="TimeoutUs", name="timeout_us",
                 checks=(CheckHexList(LEN.TIMEOUT_US // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nb_columns, nb_rows, timeout_us, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param nb_columns: Nb Columns
        :type nb_columns: ``int | HexList``
        :param nb_rows: Nb Rows
        :type nb_rows: ``int | HexList``
        :param timeout_us: Timeout Us
        :type timeout_us: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.nb_columns = nb_columns
        self.nb_rows = nb_rows
        self.timeout_us = timeout_us
    # end def __init__
# end class GetHardwareInfoResponse


class GenerateMaskTable(ShortEmptyPacketDataFormat):
    """
    Define ``GenerateMaskTable`` implementation class for version 0
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
                         function_index=GenerateMaskTableResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GenerateMaskTable


class GenerateMaskTableResponse(OpticalSwitches):
    """
    Define ``GenerateMaskTableResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Nb Available Keys             8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GenerateMaskTable,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        NB_AVAILABLE_KEYS = OpticalSwitches.FID.SOFTWARE_ID - 1
        PADDING = NB_AVAILABLE_KEYS - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        NB_AVAILABLE_KEYS = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.NB_AVAILABLE_KEYS, length=LEN.NB_AVAILABLE_KEYS,
                 title="NbAvailableKeys", name="nb_available_keys",
                 checks=(CheckHexList(LEN.NB_AVAILABLE_KEYS // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, nb_available_keys, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param nb_available_keys: Nb Available Keys
        :type nb_available_keys: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.nb_available_keys = nb_available_keys
    # end def __init__
# end class GenerateMaskTableResponse


class GetMaskTable(ColumnIndex):
    """
    Define ``GetMaskTable`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, column_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param column_idx: Column Idx
        :type column_idx: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetMaskTableResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.column_idx = column_idx
    # end def __init__
# end class GetMaskTable


class GetMaskTableResponse(OpticalSwitches):
    """
    Define ``GetMaskTableResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Port 0 Row Mask               32
    Port 1 Row Mask               32
    Padding                       64
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetMaskTable,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        PORT_0_ROW_MASK = OpticalSwitches.FID.SOFTWARE_ID - 1
        PORT_1_ROW_MASK = PORT_0_ROW_MASK - 1
        PADDING = PORT_1_ROW_MASK - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        PORT_0_ROW_MASK = 0x20
        PORT_1_ROW_MASK = 0x20
        PADDING = 0x40
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.PORT_0_ROW_MASK, length=LEN.PORT_0_ROW_MASK,
                 title="Port0RowMask", name="port_0_row_mask",
                 checks=(CheckHexList(LEN.PORT_0_ROW_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PORT_0_ROW_MASK) - 1),)),
        BitField(fid=FID.PORT_1_ROW_MASK, length=LEN.PORT_1_ROW_MASK,
                 title="Port1RowMask", name="port_1_row_mask",
                 checks=(CheckHexList(LEN.PORT_1_ROW_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PORT_1_ROW_MASK) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, port_0_row_mask, port_1_row_mask, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param port_0_row_mask: Port 0 Row Mask
        :type port_0_row_mask: ``int | HexList``
        :param port_1_row_mask: Port 1 Row Mask
        :type port_1_row_mask: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.port_0_row_mask = port_0_row_mask
        self.port_1_row_mask = port_1_row_mask
    # end def __init__
# end class GetMaskTableResponse


class InitTest(ShortEmptyPacketDataFormat):
    """
    Define ``InitTest`` implementation class for version 0
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
                         function_index=InitTestResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class InitTest


class InitTestResponse(LongEmptyPacketDataFormat):
    """
    Define ``InitTestResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (InitTest,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

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
# end class InitTestResponse


class GetKeyReleaseTimings(ColumnIndex):
    """
    Define ``GetKeyReleaseTimings`` implementation class for version 0
    """

    def __init__(self, device_index, feature_index, column_idx, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param column_idx: Column Idx
        :type column_idx: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetKeyReleaseTimingsResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.column_idx = column_idx
    # end def __init__
# end class GetKeyReleaseTimings


class GetKeyReleaseTimingsResponse(OpticalSwitches):
    """
    Define ``GetKeyReleaseTimingsResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Min Duration                  16
    Max Duration                  16
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetKeyReleaseTimings,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        MIN_DURATION = OpticalSwitches.FID.SOFTWARE_ID - 1
        MAX_DURATION = MIN_DURATION - 1
        PADDING = MAX_DURATION - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        MIN_DURATION = 0x10
        MAX_DURATION = 0x10
        PADDING = 0x60
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.MIN_DURATION, length=LEN.MIN_DURATION,
                 title="MinDuration", name="min_duration",
                 checks=(CheckHexList(LEN.MIN_DURATION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MIN_DURATION) - 1),)),
        BitField(fid=FID.MAX_DURATION, length=LEN.MAX_DURATION,
                 title="MaxDuration", name="max_duration",
                 checks=(CheckHexList(LEN.MAX_DURATION // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.MAX_DURATION) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, min_duration, max_duration, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param min_duration: Min Duration
        :type min_duration: ``int | HexList``
        :param max_duration: Max Duration
        :type max_duration: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.min_duration = min_duration
        self.max_duration = max_duration
    # end def __init__
# end class GetKeyReleaseTimingsResponse


class ConfigEmitTime(OpticalSwitches):
    """
    Define ``ConfigEmitTime`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Emit Time Us                  8
    Padding                       16
    ============================  ==========
    """

    class FID(OpticalSwitches.FID):
        # See ``OpticalSwitches.FID``
        EMIT_TIME_US = OpticalSwitches.FID.SOFTWARE_ID - 1
        PADDING = EMIT_TIME_US - 1
    # end class FID

    class LEN(OpticalSwitches.LEN):
        # See ``OpticalSwitches.LEN``
        EMIT_TIME_US = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = OpticalSwitches.FIELDS + (
        BitField(fid=FID.EMIT_TIME_US, length=LEN.EMIT_TIME_US,
                 title="EmitTimeUs", name="emit_time_us",
                 checks=(CheckHexList(LEN.EMIT_TIME_US // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OpticalSwitches.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, emit_time_us, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int | HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int | HexList``
        :param emit_time_us: Emit Time Us
        :type emit_time_us: ``int | HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ConfigEmitTimeResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.emit_time_us = emit_time_us
    # end def __init__
# end class ConfigEmitTime


class ConfigEmitTimeResponse(LongEmptyPacketDataFormat):
    """
    Define ``ConfigEmitTimeResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ConfigEmitTime,)
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
# end class ConfigEmitTimeResponse


class EndTest(ShortEmptyPacketDataFormat):
    """
    Define ``EndTest`` implementation class for version 0
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
                         function_index=EndTestResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class EndTest


class EndTestResponse(LongEmptyPacketDataFormat):
    """
    Define ``EndTestResponse`` implementation class for version 0
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (EndTest,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

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
# end class EndTestResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
