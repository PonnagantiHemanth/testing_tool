#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.powermodes
:brief: HID++ 2.0 Power Modes command interface definition
:author: Stanislas Cottard
:date: 2019/05/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pyhid.field import CheckByte
from pyhid.field import CheckHexList


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PowerModes(HidppMessage):
    """
    Power Modes implementation class

    Format:
    || @b Name                || @b Bit count ||
    || ReportID               || 8            ||
    || DeviceIndex            || 8            ||
    || FeatureIndex           || 8            ||
    || FunctionID             || 4            ||
    || softwareID             || 4            ||
    || Params                 || 24           ||
    """
    FEATURE_ID = 0x1830
    MAX_FUNCTION_INDEX = 1

    # Power Mode Number values
    DO_NOTHING = 0
    DEAD_MODE = 1
    FW_CUT_OFF_MODE = 2
    DEEP_SLEEP = 3

    def __init__(self, device_index, feature_index, **kwargs):
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class PowerModes


class PowerModesModel(FeatureModel):
    """
    PowerModes feature model.
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_POWER_MODES_TOTAL_NUMBER = 0
        SET_POWER_MODE = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Power Modes feature data model.
        """
        return {
            "feature_base": PowerModes,
            "versions": {
                PowerModesV0.VERSION: {
                    "main_cls": PowerModesV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_POWER_MODES_TOTAL_NUMBER: {"request": GetPowerModesTotalNumber,
                                                                     "response": GetPowerModesTotalNumberResponse},
                            cls.INDEX.SET_POWER_MODE: {"request": SetPowerMode,
                                                       "response": SetPowerModeResponse},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class PowerModesModel


class PowerModesFactory(FeatureFactory):
    """
    Power Modes factory to create a feature object from a given version.
    """
    @staticmethod
    def create(version):
        """
        Power Modes object creation from a version number.

        :param version: Power Modes feature version
        :type version: ``int``

        :return: Power Modes object
        :rtype: ``PowerModesInterface``
        """
        return PowerModesModel.get_main_cls(version)()
    # end def create
# end class PowerModesFactory


class PowerModesInterface(FeatureInterface, ABC):
    """
    Interface to the Power Modes feature.

    Define the required interfaces for Power Modes classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_power_modes_total_number_cls = None
        self.get_power_modes_total_number_response_cls = None

        self.set_power_mode_cls = None
        self.set_power_mode_response_cls = None
    # end def __init__
# end class PowerModesInterface


class PowerModesV0(PowerModesInterface):
    """
    Power Modes
    This feature allows to set the wanted power mode.

    [0] getPowerModesTotalNumber() -> total_number_of_power_modes
    [1] setPowerMode(powerModeNumber)
    """
    VERSION = 0

    def __init__(self):
        # See ``PowerModesInterface.__init__``
        super().__init__()
        self.get_power_modes_total_number_cls = PowerModesModel.get_request_cls(
            self.VERSION, PowerModesModel.INDEX.GET_POWER_MODES_TOTAL_NUMBER)
        self.get_power_modes_total_number_response_cls = PowerModesModel.get_response_cls(
            self.VERSION, PowerModesModel.INDEX.GET_POWER_MODES_TOTAL_NUMBER)

        self.set_power_mode_cls = PowerModesModel.get_request_cls(
            self.VERSION, PowerModesModel.INDEX.SET_POWER_MODE)
        self.set_power_mode_response_cls = PowerModesModel.get_response_cls(
            self.VERSION, PowerModesModel.INDEX.SET_POWER_MODE)
    # end def __init__

    def get_max_function_index(self):
        """
        Get max function index
        """
        return PowerModesModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class PowerModesV0


class GetPowerModesTotalNumber(PowerModes):
    """
    PowerModes GetPowerModesTotalNumber implementation class

    Request the total number of power modes.

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

    class FID(PowerModes.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(PowerModes.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = PowerModes.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=PowerModes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index,
                         feature_index=feature_index,
                         functionIndex=GetPowerModesTotalNumberResponse.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class GetPowerModesTotalNumber


class GetPowerModesTotalNumberResponse(PowerModes):
    """
    PowerModes GetPowerModesTotalNumber response implementation class

    Return the total number of power modes.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    TotalNumberOfPowerModes       8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPowerModesTotalNumber,)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(PowerModes.FID):
        """
        Field Identifiers
        """
        TOTAL_NUMBER_OF_POWER_MODES = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(PowerModes.LEN):
        """
        Field Lengths
        """
        TOTAL_NUMBER_OF_POWER_MODES = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = PowerModes.FIELDS + (
        BitField(FID.TOTAL_NUMBER_OF_POWER_MODES,
                 LEN.TOTAL_NUMBER_OF_POWER_MODES,
                 title='TotalNumberOfPowerModes',
                 name='total_number_of_power_modes',
                 checks=(CheckHexList(LEN.TOTAL_NUMBER_OF_POWER_MODES // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PowerModes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, total_number_of_power_modes, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param total_number_of_power_modes: The total number of power modes
        :type total_number_of_power_modes: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.total_number_of_power_modes = total_number_of_power_modes
    # end def __init__
# end class GetPowerModesTotalNumberResponse


class SetPowerMode(PowerModes):
    """
    PowerModes SetPowerMode implementation class

    Set the wanted power mode.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    PowerModeNumber               8
    Padding                       16
    ============================  ==========
    """
    MSG_TYPE = TYPE.REQUEST

    class FID(PowerModes.FID):
        """
        Field Identifiers
        """
        POWER_MODE_NUMBER = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(PowerModes.LEN):
        """
        Field Lengths
        """
        POWER_MODE_NUMBER = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = PowerModes.FIELDS + (
        BitField(FID.POWER_MODE_NUMBER,
                 LEN.POWER_MODE_NUMBER,
                 title='PowerModeNumber',
                 name='power_mode_number',
                 checks=(CheckHexList(LEN.POWER_MODE_NUMBER // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PowerModes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, power_mode_number, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param power_mode_number: The power mode device should enter
        :type power_mode_number: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetPowerModeResponse.FUNCTION_INDEX, **kwargs)
        self.power_mode_number = power_mode_number
    # end def __init__
# end class SetPowerMode


class SetPowerModeResponse(PowerModes):
    """
    PowerModes SetPowerMode response implementation class

    Acknowledge the power mode access.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    PowerModeNumber               8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetPowerMode,)
    FUNCTION_INDEX = 1
    VERSION = (0, )

    class FID(PowerModes.FID):
        """
        Field Identifiers
        """
        POWER_MODE_NUMBER = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(PowerModes.LEN):
        """
        Field Lengths
        """
        POWER_MODE_NUMBER = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = PowerModes.FIELDS + (
        BitField(FID.POWER_MODE_NUMBER,
                 LEN.POWER_MODE_NUMBER,
                 title='PowerModeNumber',
                 name='power_mode_number',
                 checks=(CheckHexList(LEN.POWER_MODE_NUMBER // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=PowerModes.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, power_mode_number, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param power_mode_number: The power mode device should enter
        :type power_mode_number: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.power_mode_number = power_mode_number
    # end def __init__
# end class SetPowerModeResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
