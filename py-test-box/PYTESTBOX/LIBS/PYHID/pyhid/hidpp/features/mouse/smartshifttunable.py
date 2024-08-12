#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.mouse.smartshifttunable
:brief: HID++ 2.0 SmartShift 3G/EPM wheel with tunable torque command interface definition
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2020/02/17
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
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


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SmartShiftTunable(HidppMessage):
    """
    SmartShift 3G/EPM wheel with tunable torque implementation class

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
    FEATURE_ID = 0x2111
    MAX_FUNCTION_INDEX_V0 = 2

    class WheelModeConst:
        """
        Wheel modes constants
        """
        DO_NOT_CHANGE = 0
        FREESPIN = 1
        RATCHET = 2
    # end class WheelModeConst

    class AutoDisengageConst:
        """
        Auto disengage constants
        """
        DO_NOT_CHANGE = 0
        RANGE = (0x01, 0xFE)
        ALWAYS_ENGAGED = 0xFF
    # end class AutoDisengageConst

    class TunableTorqueConst:
        """
        Current tunable torque constants
        """
        DO_NOT_CHANGE = 0
        RANGE = (0x01, 0x64)
    # end class TunableTorqueConst

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(**kwargs)

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class SmartShiftTunable


class SmartShiftTunableModel(FeatureModel):
    """
    SmartShift 3G/EPM wheel with tunable torque feature model
    """

    class INDEX:
        """
        Functions indexes
        """
        GET_CAPABILITIES = 0
        GET_RATCHET_CONTROL_MODE = 1
        SET_RATCHET_CONTROL_MODE = 2
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        SmartShift 3G/EPM wheel with tunable torque feature data model
        """
        return {
                "feature_base": SmartShiftTunable,
                "versions": {
                    SmartShiftTunableV0.VERSION: {
                        "main_cls": SmartShiftTunableV0,
                        "api": {
                            "functions": {
                                cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilitiesV0,
                                                             "response": GetCapabilitiesResponseV0},
                                cls.INDEX.GET_RATCHET_CONTROL_MODE: {"request": GetRatchetControlModeV0,
                                                                     "response": GetRatchetControlModeResponseV0},
                                cls.INDEX.SET_RATCHET_CONTROL_MODE: {"request": SetRatchetControlModeV0,
                                                                     "response": SetRatchetControlModeResponseV0},
                            }
                        },
                    },
                }
            }
    # end def _get_data_model
# end class SmartShiftTunableModel


class SmartShiftTunableFactory(FeatureFactory):
    """
    SmartShift 3G/EPM wheel with tunable torque factory
    """
    @staticmethod
    def create(version):
        """
        SmartShift tunable object creation from version number

        :param version: SmartShift Tunable feature version
        :type version: ``int``
        :return: Device information object
        :rtype: ``DeviceInformationInterface``
        """
        return SmartShiftTunableModel.get_main_cls(version)()
    # end def create
# end class SmartShiftTunableFactory


class SmartShiftTunableInterface(FeatureInterface, ABC):
    """
    Interface to SmartShift tunable feature
    Defines required interfaces for smartshift tunable classes
    """
    def __init__(self):
        # See class documentation above
        self.get_capabilities_cls = None
        self.get_capabilities_response_cls = None
        self.get_ratchet_control_mode_cls = None
        self.get_ratchet_control_mode_response_cls = None
        self.set_ratchet_control_mode_cls = None
        self.set_ratchet_control_mode_response_cls = None
    # end def __init__
# end class SmartShiftTunableInterface


class SmartShiftTunableV0(SmartShiftTunableInterface):
    """
    x2111 - SmartShift 3G/EPM wheel with tunable torque
    Version 0

    SmartShift
    [0] getCapabilities() -> capabilities, autoDisengageDefault, defaultTunableTorque, maxForce
    [1] getRatchetControlMode() -> wheelMode, autoDisengage, currentTunableTorque
    [2] setRatchetControlMode(wheelMode, autoDisengage, currentTunableTorque) -> wheelMode, autoDisengage,
    currentTunableTorque

    This feature exposes and configures the smart shift enhanced functionality on a 3G/EPM wheel (threshold and
    tunable torque)

    ChangeLog:
        * Version 0: Initial version
    """
    VERSION = 0

    def __init__(self):
        # See SmartShiftTunableInterface
        super().__init__()
        self.get_capabilities_cls = SmartShiftTunableModel.get_request_cls(
            self.VERSION, SmartShiftTunableModel.INDEX.GET_CAPABILITIES)
        self.get_capabilities_response_cls = SmartShiftTunableModel.get_response_cls(
            self.VERSION, SmartShiftTunableModel.INDEX.GET_CAPABILITIES)
        self.get_ratchet_control_mode_cls = SmartShiftTunableModel.get_request_cls(
            self.VERSION, SmartShiftTunableModel.INDEX.GET_RATCHET_CONTROL_MODE)
        self.get_ratchet_control_mode_response_cls = SmartShiftTunableModel.get_response_cls(
            self.VERSION, SmartShiftTunableModel.INDEX.GET_RATCHET_CONTROL_MODE)
        self.set_ratchet_control_mode_cls = SmartShiftTunableModel.get_request_cls(
            self.VERSION, SmartShiftTunableModel.INDEX.SET_RATCHET_CONTROL_MODE)
        self.set_ratchet_control_mode_response_cls = SmartShiftTunableModel.get_response_cls(
            self.VERSION, SmartShiftTunableModel.INDEX.SET_RATCHET_CONTROL_MODE)
    # end def __init__

    def get_max_function_index(self):
        # See ``SmartShiftTunableInterface.get_max_function_index``
        return SmartShiftTunableModel.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end def class SmartShiftTunableV0


class GetCapabilitiesV0(SmartShiftTunable):
    """
    SmartShift 3G/EPM wheel with tunable torque getCapabilities request implementation class for version 0

    [0] getCapabilities() -> capabilities, autoDisengageDefault, defaultTunableTorque, maxForce

    Returns the EPM configuration capabilities.

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
    class FID(SmartShiftTunable.FID):
        """
        Fields identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(SmartShiftTunable.LEN):
        """
        Fields lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = SmartShiftTunable.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShiftTunable.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        # See ``SmartShiftTunable.__init__``
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = GetCapabilitiesResponseV0.FUNCTION_INDEX
    # end def __init__
# end class GetCapabilitiesV0


class GetCapabilitiesResponseV0(SmartShiftTunable):
    """
    SmartShift 3G/EPM wheel with tunable torque getCapabilities response implementation class for version 0

    [0] getCapabilities() -> capabilities, autoDisengageDefault, defaultTunableTorque, maxForce

    Returns the EPM configuration capabilities.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    CapabilitiesReserved          7
    TunableTorque                 1
    AutoDisengageDefault          8
    DefaultTunableTorque          8
    MaxForce                      8
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilitiesV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(SmartShiftTunable.FID):
        """
        Fields identifiers
        """
        CAPABILITIES_RESERVED = 0xFA
        TUNABLE_TORQUE = 0xF9
        AUTO_DISENGAGE_DEFAULT = 0xF8
        DEFAULT_TUNABLE_TORQUE = 0xF7
        MAX_FORCE = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(SmartShiftTunable.LEN):
        """
        Fields length
        """
        CAPABILITIES_RESERVED = 0x07
        TUNABLE_TORQUE = 0x01
        AUTO_DISENGAGE_DEFAULT = 0x08
        DEFAULT_TUNABLE_TORQUE = 0x08
        MAX_FORCE = 0x08
        PADDING = 0x60
    # end class LEN

    FIELDS = SmartShiftTunable.FIELDS + (
        BitField(fid=FID.CAPABILITIES_RESERVED,
                 length=LEN.CAPABILITIES_RESERVED,
                 default_value=0x00,
                 title='CapabilitiesReserved',
                 name='capabilities_reserved',
                 checks=(CheckHexList(LEN.CAPABILITIES_RESERVED // 8),
                         CheckInt(0, pow(2, LEN.CAPABILITIES_RESERVED) - 1),)),
        BitField(fid=FID.TUNABLE_TORQUE,
                 length=LEN.TUNABLE_TORQUE,
                 title='TunableTorque',
                 name='tunable_torque',
                 checks=(CheckInt(0, pow(2, LEN.TUNABLE_TORQUE) - 1),),
                 conversions={HexList: Numeral}),
        BitField(fid=FID.AUTO_DISENGAGE_DEFAULT,
                 length=LEN.AUTO_DISENGAGE_DEFAULT,
                 title='AutoDisengageDefault',
                 name='auto_disengage_default',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE_DEFAULT // 8), CheckByte(),)),
        BitField(fid=FID.DEFAULT_TUNABLE_TORQUE,
                 length=LEN.DEFAULT_TUNABLE_TORQUE,
                 title='DefaultTunableTorque',
                 name='default_tunable_torque',
                 checks=(CheckHexList(LEN.DEFAULT_TUNABLE_TORQUE // 8), CheckByte(),)),
        BitField(fid=FID.MAX_FORCE,
                 length=LEN.MAX_FORCE,
                 title='MaxForce',
                 name='max_force',
                 checks=(CheckHexList(LEN.MAX_FORCE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SmartShiftTunable.DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),)),
    )

    def __init__(self, device_index, feature_index, tunable_torque, auto_disengage_default, default_tunable_torque,
                 max_force, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param tunable_torque: Tunable torque capability
        :type tunable_torque: ``int`` or ``bool`` or ``HexList``
        :param auto_disengage_default: Default value of the autoDisengage setting
        :type auto_disengage_default: ``int`` or ``HexList``
        :param default_tunable_torque: Default tunable torque in % of the max force
        :type default_tunable_torque: ``int`` or ``HexList``
        :param max_force: max force value expressed in gram-Force (gF)
        :type max_force: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.tunable_torque = tunable_torque
        self.auto_disengage_default = auto_disengage_default
        self.default_tunable_torque = default_tunable_torque
        self.max_force = max_force
    # end def __init__
# end class GetCapabilitiesResponseV0


class GetRatchetControlModeV0(SmartShiftTunable):
    """
    SmartShift 3G/EPM wheel with tunable torque getRatchetControlMode request implementation class for version 0

    [1] getRatchetControlMode() -> wheelMode, autoDisengage, currentTunableTorque

    Returns the current smart shift configuration.

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
    class FID(SmartShiftTunable.FID):
        """
        Fields identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(SmartShiftTunable.LEN):
        """
        Fields lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = SmartShiftTunable.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShiftTunable.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        # SEe ``SmartShiftTunable.__init__``
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = GetRatchetControlModeResponseV0.FUNCTION_INDEX
    # end def __init__
# end class GetRatchetControlModeV0


class GetRatchetControlModeResponseV0(SmartShiftTunable):
    """
    SmartShift 3G/EPM wheel with tunable torque getRatchetControlMode response implementation class for version 0

    [1] getRatchetControlMode() -> wheelMode, autoDisengage, currentTunableTorque

    Returns the current smart shift configuration.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    WheelMode                     8
    AutoDisengage                 8
    CurrentTunableTorque          8
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetRatchetControlModeV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(SmartShiftTunable.FID):
        """
        Fields identifiers
        """
        WHEEL_MODE = 0xFA
        AUTO_DISENGAGE = 0xF9
        CURRENT_TUNABLE_TORQUE = 0xF8
        PADDING = 0xF7
    # end class FID

    class LEN(SmartShiftTunable.LEN):
        """
        Fields lengths
        """
        WHEEL_MODE = 0x08
        AUTO_DISENGAGE = 0x08
        CURRENT_TUNABLE_TORQUE = 0x08
        PADDING = 0x68
    # end class LEN

    FIELDS = SmartShiftTunable.FIELDS + (
        BitField(fid=FID.WHEEL_MODE,
                 length=LEN.WHEEL_MODE,
                 title='WheelMode',
                 name='wheel_mode',
                 checks=(CheckHexList(LEN.WHEEL_MODE // 8), CheckByte(),)),
        BitField(fid=FID.AUTO_DISENGAGE,
                 length=LEN.AUTO_DISENGAGE,
                 title='AutoDisengage',
                 name='auto_disengage',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE // 8), CheckByte(),)),
        BitField(fid=FID.CURRENT_TUNABLE_TORQUE,
                 length=LEN.CURRENT_TUNABLE_TORQUE,
                 title='CurrentTunableTorque',
                 name='current_tunable_torque',
                 checks=(CheckHexList(LEN.CURRENT_TUNABLE_TORQUE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShiftTunable.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, wheel_mode, auto_disengage, current_tunable_torque, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param wheel_mode: Current wheel mode
        :type wheel_mode: ``int`` or ``HexList``
        :param auto_disengage: Speed at which the ratchet automatically disengages
        :type auto_disengage: ``int`` or ``HexList``
        :param current_tunable_torque: Current tunable torque in % of the max force
        :type current_tunable_torque: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = self.FUNCTION_INDEX
        self.wheel_mode = wheel_mode
        self.auto_disengage = auto_disengage
        self.current_tunable_torque = current_tunable_torque
    # end def __init__
# end class GetRatchetControlModeResponseV0


class SetRatchetControlModeV0(SmartShiftTunable):
    """
    SmartShift 3G/EPM wheel with tunable torque setRatchetControlMode request implementation class for version 0

    [2] setRatchetControlMode(wheelMode, autoDisengage, currentTunableTorque) -> wheelMode, autoDisengage,
    currentTunableTorque

    Sets the wheel mode and configures the automatic disengage setting.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    WheelMode                     8
    AutoDisengage                 8
    CurrentTunableTorque          8
    ============================  ==========
    """
    class FID(SmartShiftTunable.FID):
        """
        Fields identifiers
        """
        WHEEL_MODE = 0xFA
        AUTO_DISENGAGE = 0xF9
        CURRENT_TUNABLE_TORQUE = 0xF8
    # end class FID

    class LEN(SmartShiftTunable.LEN):
        """
        Fields lengths
        """
        WHEEL_MODE = 0x08
        AUTO_DISENGAGE = 0x08
        CURRENT_TUNABLE_TORQUE = 0x08
    # end class LEN

    FIELDS = SmartShiftTunable.FIELDS + (
        BitField(fid=FID.WHEEL_MODE,
                 length=LEN.WHEEL_MODE,
                 title='WheelMode',
                 name='wheel_mode',
                 checks=(CheckHexList(LEN.WHEEL_MODE // 8), CheckByte(),)),
        BitField(fid=FID.AUTO_DISENGAGE,
                 length=LEN.AUTO_DISENGAGE,
                 title='AutoDisengage',
                 name='auto_disengage',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE // 8), CheckByte(),)),
        BitField(fid=FID.CURRENT_TUNABLE_TORQUE,
                 length=LEN.CURRENT_TUNABLE_TORQUE,
                 title='CurrentTunableTorque',
                 name='current_tunable_torque',
                 checks=(CheckHexList(LEN.CURRENT_TUNABLE_TORQUE // 8), CheckByte(),))
    )

    def __init__(self, device_index, feature_index, wheel_mode, auto_disengage, current_tunable_torque, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param wheel_mode: Current wheel mode
        :type wheel_mode: ``int`` or ``HexList``
        :param auto_disengage: Speed at which the ratchet automatically disengages
        :type auto_disengage: ``int`` or ``HexList``
        :param current_tunable_torque: Current tunable torque in % of the max force
        :type current_tunable_torque: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = SetRatchetControlModeResponseV0.FUNCTION_INDEX
        self.wheel_mode = wheel_mode
        self.auto_disengage = auto_disengage
        self.current_tunable_torque = current_tunable_torque
    # end def __init__
# end class SetRatchetControlModeV0


class SetRatchetControlModeResponseV0(SmartShiftTunable):
    """
    SmartShift 3G/EPM wheel with tunable torque setRatchetControlMode response implementation class for version 0

    [2] setRatchetControlMode(wheelMode, autoDisengage, currentTunableTorque) -> wheelMode, autoDisengage,
    currentTunableTorque

    Sets the wheel mode and configures the automatic disengage setting.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    WheelMode                     8
    AutoDisengage                 8
    CurrentTunableTorque          8
    Reserved                      104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetRatchetControlModeV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(SmartShiftTunable.FID):
        """
        Fields identifiers
        """
        WHEEL_MODE = 0xFA
        AUTO_DISENGAGE = 0xF9
        CURRENT_TUNABLE_TORQUE = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(SmartShiftTunable.LEN):
        """
        Fields lengths
        """
        WHEEL_MODE = 0x08
        AUTO_DISENGAGE = 0x08
        CURRENT_TUNABLE_TORQUE = 0x08
        PADDING = 0x68

    # end class LEN

    FIELDS = SmartShiftTunable.FIELDS + (
        BitField(fid=FID.WHEEL_MODE,
                 length=LEN.WHEEL_MODE,
                 title='WheelMode',
                 name='wheel_mode',
                 checks=(CheckHexList(LEN.WHEEL_MODE // 8), CheckByte(),)),
        BitField(fid=FID.AUTO_DISENGAGE,
                 length=LEN.AUTO_DISENGAGE,
                 title='AutoDisengage',
                 name='auto_disengage',
                 checks=(CheckHexList(LEN.AUTO_DISENGAGE // 8), CheckByte(),)),
        BitField(fid=FID.CURRENT_TUNABLE_TORQUE,
                 length=LEN.CURRENT_TUNABLE_TORQUE,
                 title='CurrentTunableTorque',
                 name='current_tunable_torque',
                 checks=(CheckHexList(LEN.CURRENT_TUNABLE_TORQUE // 8), CheckByte(),)),
        BitField(fid=FID.PADDING,
                 length=LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SmartShiftTunable.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, wheel_mode, auto_disengage, current_tunable_torque, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param wheel_mode: Current wheel mode
        :type wheel_mode: ``int`` or ``HexList``
        :param auto_disengage: Speed at which the ratchet automatically disengages
        :type auto_disengage: ``int`` or ``HexList``
        :param current_tunable_torque: Current tunable torque in % of the max force
        :type current_tunable_torque: ``int`` or ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = SetRatchetControlModeResponseV0.FUNCTION_INDEX
        self.wheel_mode = wheel_mode
        self.auto_disengage = auto_disengage
        self.current_tunable_torque = current_tunable_torque
    # end def __init__
# end class SetRatchetControlModeResponseV0

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
