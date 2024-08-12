#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
""" @package    pyhid.hidpp.features.common.dfucontrol

@brief  HID++ 2.0 DFU Control command interface definition

@author Stanislas Cottard

@date   2019/06/25
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class DfuControlModel(FeatureModel):
    """
    Dfu Control feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_DFU_STATUS = 0
        START_DFU = 1
    # end class

    @classmethod
    def _get_data_model(cls):
        """
        Device information feature data model
        """
        return {
            "feature_base": DfuControl,
            "versions": {
                0: {
                    "main_cls": DfuControlV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_DFU_STATUS: {"request": GetDfuStatus, "response": GetDfuStatusResponse},
                            cls.INDEX.START_DFU: {"request": StartDfu, "response": StartDfuResponse},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class DfuControlModel


class DfuControlFactory(FeatureFactory):
    """
    Dfu Control factory creates a Dfu Control object from a given version
    """
    @staticmethod
    def create(version):
        """
        Dfu Control object creation from version number

        :param version: Dfu Control feature version
        :type version: ``int``
        :return: Dfu Control object
        :rtype: ``DfuControlInterface``
        """
        return DfuControlModel.get_main_cls(version)()
    # end def create
# end class DfuControlFactory


class DfuControlInterface(FeatureInterface, ABC):
    """
    Interface to Dfu Control feature

    Defines required interfaces for Dfu Control classes
    """
    def __init__(self):
        """
        Constructor
        """
        # Requests
        self.get_dfu_status_cls = None
        self.start_dfu_cls = None

        # Responses
        self.get_dfu_status_response_cls = None
        self.start_dfu_response_cls = None
    # end def __init__
# end class DfuControlInterface


class DfuControlV0(DfuControlInterface):
    """
    DfuControl
    This feature provides model and unit specific information

    [0] getDfuStatus() ? 0, 0, notAvail
    [1] startDfu(enterDfu, dfuControlParam, dfuMagicKey)
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`DfuControlInterface.__init__`
        """
        super().__init__()
        self.get_dfu_status_cls = DfuControlModel.get_request_cls(
            self.VERSION, DfuControlModel.INDEX.GET_DFU_STATUS)
        self.start_dfu_cls = DfuControlModel.get_request_cls(
            self.VERSION, DfuControlModel.INDEX.START_DFU)
        self.get_dfu_status_response_cls = DfuControlModel.get_response_cls(
            self.VERSION, DfuControlModel.INDEX.GET_DFU_STATUS)
        self.start_dfu_response_cls = DfuControlModel.get_response_cls(
            self.VERSION, DfuControlModel.INDEX.START_DFU)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`DeviceInformationInterface.get_max_function_index`
        """
        return DfuControlModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class DfuControlV0


class DfuControl(HidppMessage):
    """
    DFU control implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x00C2
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index           [in] (int)  feature Index
        """
        super(DfuControl, self).__init__()

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class DfuControl


class GetDfuStatus(DfuControl):
    """
    DfuControl GetDfuStatus implementation class

    Request the DFU-mode status.

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 24           ||
    """

    class FID(DfuControl.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(DfuControl.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = DfuControl.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=DfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index              [in] (int)  desired feature Id
        """
        super(GetDfuStatus, self).__init__(device_index, feature_index)

        self.functionIndex = GetDfuStatusResponse.FUNCTION_INDEX
    # end def __init__
# end class GetDfuStatus


class GetDfuStatusResponse(DfuControl):
    """
    DfuControl GetDfuStatus response implementation class

    Returns the the DFU-mode status.

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || ReservedEnterDfu        || 7            ||
    || EnterDfu                || 1            ||
    || DfuControlParam         || 8            ||
    || ReservedNotAvail        || 7            ||
    || NotAvail                || 1            ||
    || Padding                 || 104          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDfuStatus,)
    VERSION = (0, )
    FUNCTION_INDEX = 0

    class FID(DfuControl.FID):
        """
        Field Identifiers
        """
        RESERVED_ENTER_DFU = 0xFA
        ENTER_DFU = 0xF9
        DFU_CONTROL_PARAM = 0xF8
        RESERVED_NOT_AVAILABLE = 0xF7
        NOT_AVAIL = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(DfuControl.LEN):
        """
        Field Lengths
        """
        RESERVED_ENTER_DFU = 0x07
        ENTER_DFU = 0x01
        DFU_CONTROL_PARAM = 0x08
        RESERVED_NOT_AVAILABLE = 0x07
        NOT_AVAIL = 0x01
        PADDING = 0x68
    # end class LEN

    FIELDS = DfuControl.FIELDS + (
        BitField(FID.RESERVED_ENTER_DFU,
                 LEN.RESERVED_ENTER_DFU,
                 0x00,
                 0x00,
                 title='ReservedEnterDfu',
                 name='reserved_enter_dfu',
                 checks=(CheckInt(max_value=0),)),  # i.e. == 0
        BitField(FID.ENTER_DFU,
                 LEN.ENTER_DFU,
                 0x00,
                 0x00,
                 title='EnterDfu',
                 name='enter_dfu',
                 checks=(CheckInt(0, pow(2, LEN.ENTER_DFU) - 1),)),
        BitField(FID.DFU_CONTROL_PARAM,
                 LEN.DFU_CONTROL_PARAM,
                 0x00,
                 0x00,
                 title='DfuControlParam',
                 name='dfu_control_param',
                 checks=(CheckHexList(LEN.DFU_CONTROL_PARAM // 8), CheckByte(),)),
        BitField(FID.RESERVED_NOT_AVAILABLE,
                 LEN.RESERVED_NOT_AVAILABLE,
                 0x00,
                 0x00,
                 title='ReservedNotAvail',
                 name='reserved_not_avail',
                 checks=(CheckInt(max_value=0),)),  # i.e. == 0
        BitField(FID.NOT_AVAIL,
                 LEN.NOT_AVAIL,
                 0x00,
                 0x00,
                 title='NotAvail',
                 name='not_avail',
                 checks=(CheckInt(0, pow(2, LEN.NOT_AVAIL) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=DfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enter_dfu, dfu_control_param, not_avail):
        """
        Constructor

        @param  device_index                    [in] (int)  Device Index
        @param  feature_index                      [in] (int)  Desired feature Id
        @param  enter_dfu                       [in] (int)  The device will enter DFU mode on next restart
        @param  dfu_control_param               [in] (int)  The DFU control parameter
        @param  not_avail                       [in] (int)  The DFU mode is not available or not
        """
        super(GetDfuStatusResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved_enter_dfu = 0
        self.enter_dfu = enter_dfu
        self.dfu_control_param = dfu_control_param
        self.reserved_not_avail = 0
        self.not_avail = not_avail
    # end def __init__
# end class GetDfuStatusResponse


class StartDfu(DfuControl):
    """
    DfuControl StartDfu implementation class

    Requests device to enter into DFU mode (boot-loader).

    Format:
    || @b Name                 || @b Bit count ||
    || ReportID                || 8            ||
    || DeviceIndex             || 8            ||
    || FeatureIndex            || 8            ||
    || FunctionID              || 4            ||
    || SoftwareID              || 4            ||
    || ReservedEnterDfu        || 7            ||
    || EnterDfu                || 1            ||
    || DfuControlParam         || 8            ||
    || Reserved                || 16           ||
    || DfuMagicKey             || 24           ||
    || Padding                 || 72           ||
    """

    class FID(DfuControl.FID):
        """
        Field Identifiers
        """
        RESERVED_ENTER_DFU = 0xFA
        ENTER_DFU = 0xF9
        DFU_CONTROL_PARAM = 0xF8
        RESERVED = 0xF7
        DFU_MAGIC_KEY = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(DfuControl.LEN):
        """
        Field Lengths
        """
        RESERVED_ENTER_DFU = 0x07
        ENTER_DFU = 0x01
        DFU_CONTROL_PARAM = 0x08
        RESERVED = 0x10
        DFU_MAGIC_KEY = 0x18
        PADDING = 0x48
    # end class LEN

    class DEFAULT(DfuControl.DEFAULT):
        DFU_MAGIC_KEY = 0x444655  # ASCII code for 'DFU'
    # end class DEFAULT

    FIELDS = DfuControl.FIELDS + (
        BitField(FID.RESERVED_ENTER_DFU,
                 LEN.RESERVED_ENTER_DFU,
                 0x00,
                 0x00,
                 title='ReservedEnterDfu',
                 name='reserved_enter_dfu',
                 checks=(CheckInt(max_value=0x7F),)),
        BitField(FID.ENTER_DFU,
                 LEN.ENTER_DFU,
                 0x00,
                 0x00,
                 title='EnterDfu',
                 name='enter_dfu',
                 checks=(CheckInt(0, pow(2, LEN.ENTER_DFU) - 1),)),
        BitField(FID.DFU_CONTROL_PARAM,
                 LEN.DFU_CONTROL_PARAM,
                 0x00,
                 0x00,
                 title='DfuControlParam',
                 name='dfu_control_param',
                 checks=(CheckByte(),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 0x00,
                 0x00,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(max_value=0xFFFF),)),
        BitField(FID.DFU_MAGIC_KEY,
                 LEN.DFU_MAGIC_KEY,
                 0x00,
                 0x00,
                 title='DfuMagicKey',
                 name='dfu_magic_key',
                 checks=(CheckInt(0, pow(2, LEN.DFU_MAGIC_KEY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=DfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, enter_dfu, dfu_control_param, dfu_magic_key):
        """
        Constructor

        @param  device_index                    [in] (int)  Device Index
        @param  feature_index                      [in] (int)  Desired feature Id
        @param  enter_dfu                       [in] (int)  The device will enter DFU mode on next restart
        @param  dfu_control_param               [in] (int)  The DFU control parameter
        @param  dfu_magic_key                   [in] (int)  The DFU mode is not available or not
        """
        super(StartDfu, self).__init__(device_index, feature_index)

        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = StartDfuResponse.FUNCTION_INDEX
        self.reserved_enter_dfu = 0
        self.enter_dfu = enter_dfu
        self.dfu_control_param = dfu_control_param
        self.reserved = 0
        self.dfu_magic_key = dfu_magic_key
    # end def __init__
# end class StartDfu


class StartDfuResponse(DfuControl):
    """
    DfuControl StartDfu response implementation class

    This command may not return a response. If it does, the response is empty (all bytes set to zero).

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || SoftwareID             || 4            ||
    || Padding                || 128          ||
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (StartDfu,)
    VERSION = (0, )
    FUNCTION_INDEX = 1

    class FID(DfuControl.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(DfuControl.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80

    # end class LEN

    FIELDS = DfuControl.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 0x00,
                 0x00,
                 title='Padding',
                 name='padding',
                 default_value=DfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index):
        """
        Constructor

        @param  device_index            [in] (int)  Device Index
        @param  feature_index              [in] (int)  desired feature Id
        """
        super(StartDfuResponse, self).__init__(device_index, feature_index)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class StartDfuResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
