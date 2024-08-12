#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.securedfucontrol
    :brief: HID++ 2.0 Secure DFU Control command interface definition
    :author: Christophe Roquebert
    :date: 2020/05/19
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
from pylibrary.tools.aliasing import aliased


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SecureDfuControlModel(FeatureModel):
    """
    Secure Dfu Control feature model
    """
    class INDEX:
        """
        Define Function/Event index
        """
        # Function index
        GET_DFU_CONTROL = 0
        SET_DFU_CONTROL = 1

        # Event index
        DFU_TIMEOUT_EVENT = 0
        DFU_CANCEL_EVENT = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Device information feature data model
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_DFU_CONTROL: {"request": GetDfuControlV0,
                                            "response": GetDfuControlResponseV0},
                cls.INDEX.SET_DFU_CONTROL: {"request": SetDfuControlV0,
                                            "response": SetDfuControlResponseV0},
            },
            "events": {
               cls.INDEX.DFU_TIMEOUT_EVENT: {"report": DfuTimeoutEventV0}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.GET_DFU_CONTROL: {"request": GetDfuControlV0,
                                            "response": GetDfuControlResponseV1},
                cls.INDEX.SET_DFU_CONTROL: {"request": SetDfuControlV0,
                                            "response": SetDfuControlResponseV0},
            },
            "events": {
               cls.INDEX.DFU_TIMEOUT_EVENT: {"report": DfuTimeoutEventV0},
               cls.INDEX.DFU_CANCEL_EVENT: {"report": DfuCancelEventV1}
            }
        }

        return {
            "feature_base": SecureDfuControl,
            "versions": {
                SecureDfuControlV0.VERSION: {
                    "main_cls": SecureDfuControlV0,
                    "api": function_map_v0
                },
                SecureDfuControlV1.VERSION: {
                    "main_cls": SecureDfuControlV1,
                    "api": function_map_v1
                },
            }
        }
    # end def _get_data_model
# end class SecureDfuControlModel


class SecureDfuControlFactory(FeatureFactory):
    """
    Secure Dfu Control factory creates a Secure Dfu Control object from a given version
    """
    @staticmethod
    def create(version):
        """
        Secure Dfu Control object creation from version number

        :param version: Secure Dfu Control feature version
        :type version: ``int``
        :return: Secure Dfu Control object
        :rtype: ``SecureDfuControlInterface``
        """
        return SecureDfuControlModel.get_main_cls(version)()
    # end def create
# end class SecureDfuControlFactory


class SecureDfuControlInterface(FeatureInterface, ABC):
    """
    Interface to Secure Dfu Control feature

    Defines required interfaces for Secure Dfu Control classes
    """
    def __init__(self):
        """
        Constructor
        """
        # Requests
        self.get_dfu_control_cls = None
        self.set_dfu_control_cls = None

        # Responses
        self.get_dfu_control_response_cls = None
        self.set_dfu_control_response_cls = None

        # Events
        self.dfu_timeout_event_cls = None
        self.dfu_cancel_event_cls = None
    # end def __init__
# end class SecureDfuControlInterface


class SecureDfuControlV0(SecureDfuControlInterface):
    """
    SecureDfuControl
    This feature provides model and unit specific information

    [0] getDfuControl() ? enterDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
    [1] setDfuControl(enterDfu, dfuControlParam, dfuMagicKey)
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`SecureDfuControlInterface.__init__`
        """
        super().__init__()
        self.get_dfu_control_cls = SecureDfuControlModel.get_request_cls(
            self.VERSION, SecureDfuControlModel.INDEX.GET_DFU_CONTROL)
        self.set_dfu_control_cls = SecureDfuControlModel.get_request_cls(
            self.VERSION, SecureDfuControlModel.INDEX.SET_DFU_CONTROL)
        self.get_dfu_control_response_cls = SecureDfuControlModel.get_response_cls(
            self.VERSION, SecureDfuControlModel.INDEX.GET_DFU_CONTROL)
        self.set_dfu_control_response_cls = SecureDfuControlModel.get_response_cls(
            self.VERSION, SecureDfuControlModel.INDEX.SET_DFU_CONTROL)
        self.dfu_timeout_event_cls = SecureDfuControlModel.get_event_cls(
            self.VERSION, SecureDfuControlModel.INDEX.DFU_TIMEOUT_EVENT, "report")
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`SecureDfuControlInterface.get_max_function_index`
        """
        return SecureDfuControlModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class SecureDfuControlV0


class SecureDfuControlV1(SecureDfuControlV0):
    """
    SecureDfuControl
    This feature provides model and unit specific information

    [0] getDfuControl() ? enterDfu, dfuControlParam, dfuControlTimeout, dfuControlActionType, dfuControlActionData
    [1] setDfuControl(enterDfu, dfuControlParam, dfuMagicKey)
    """
    VERSION = 1

    def __init__(self):
        """
        See :any:`SecureDfuControlInterface.__init__`
        """
        super().__init__()
        self.dfu_cancel_event_cls = SecureDfuControlModel.get_event_cls(
            self.VERSION, SecureDfuControlModel.INDEX.DFU_CANCEL_EVENT, "report")
    # end def __init__

    def get_max_function_index(self):
        # See ``SecureDfuControlInterface.get_max_function_index``
        return SecureDfuControlModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class SecureDfuControlV1


class SecureDfuControl(HidppMessage):
    """
    DFU control implementation class

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
    FEATURE_ID = 0x00C3
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(**kwargs)

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class SecureDfuControl


class GetDfuControlV0(SecureDfuControl):
    """
    SecureDfuControl GetDfuControl implementation class

    Request the DFU control information.

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

    class FID(SecureDfuControl.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(SecureDfuControl.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = SecureDfuControl.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SecureDfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetDfuControlResponseV0.FUNCTION_INDEX
    # end def __init__
# end class GetDfuControlV0


class GetDfuControlResponseV0(SecureDfuControl):
    """
    SecureDfuControl GetDfuControl response implementation class

    Returns the DFU control information.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ReservedEnableDfu             7
    EnableDfu                     1
    DfuControlParam               8
    DfuControlTimeout             8
    DfuControlActionType          8
    DfuControlActionData          24
    Padding                       72
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetDfuControlV0,)
    VERSION = (0, )
    FUNCTION_INDEX = 0

    class FID(SecureDfuControl.FID):
        """
        Field Identifiers
        """
        RESERVED_ENABLE_DFU = 0xFA
        ENABLE_DFU = 0xF9
        DFU_CONTROL_PARAM = 0xF8
        DFU_CONTROL_TIMEOUT = 0xF7
        DFU_CONTROL_ACTION_TYPE = 0xF6
        DFU_CONTROL_ACTION_DATA = 0xF5
        PADDING = 0xF4
    # end class FID

    class LEN(SecureDfuControl.LEN):
        """
        Field Lengths
        """
        RESERVED_ENABLE_DFU = 0x07
        ENABLE_DFU = 0x01
        DFU_CONTROL_PARAM = 0x08
        DFU_CONTROL_TIMEOUT = 0x08
        DFU_CONTROL_ACTION_TYPE = 0x08
        DFU_CONTROL_ACTION_DATA = 0x18
        PADDING = 0x48
    # end class LEN

    class STATE:
        """
        enterDfu parameter : getDfuControl() bit 0 of byte 0
        """
        DFU_DISABLED = 0  # the device will not enter into DFU mode at next restart.
        DFU_ENABLED = 1  # the device will enter into DFU mode at next restart.
    # end

    class ACTION:
        """
        Control action to perform during the device reset in order to enter in bootloader at the next reset. Zero if
        unused.
        """
        NO_ACTION = 0  # No action required.
        OFF_ON = 1  # Device Off/On required or Receiver/corded device unplug/replug required.
        OFF_ON_KBD_KEYS = 2  # Device Off/On required with up to three simultaneous keys pressed on the keyboard.
        OFF_ON_MSE_CLICKS = 3  # Device Off/On required with up to three simultaneous buttons pressed on the mouse.
        RESERVED = 4  # 4..255 - reserved
    # end class ACTION

    FIELDS = SecureDfuControl.FIELDS + (
        BitField(FID.RESERVED_ENABLE_DFU,
                 LEN.RESERVED_ENABLE_DFU,
                 title='ReservedEnableDfu',
                 name='reserved_enable_dfu',
                 aliases=('reserved_enter_dfu',),  # This alias is added to be compatible with feature 0x00C2
                 checks=(CheckInt(max_value=0x7F),),  # i.e. == 0
                 default_value=HidppMessage.DEFAULT.RESERVED),
        BitField(FID.ENABLE_DFU,
                 LEN.ENABLE_DFU,
                 title='EnableDfu',
                 name='enable_dfu',
                 aliases=('enter_dfu',),  # This alias is added to be compatible with feature 0x00C2
                 checks=(CheckInt(0, pow(2, LEN.ENABLE_DFU) - 1),)),
        BitField(FID.DFU_CONTROL_PARAM,
                 LEN.DFU_CONTROL_PARAM,
                 title='DfuControlParam',
                 name='dfu_control_param',
                 checks=(CheckHexList(LEN.DFU_CONTROL_PARAM // 8), CheckByte(),)),
        BitField(FID.DFU_CONTROL_TIMEOUT,
                 LEN.DFU_CONTROL_TIMEOUT,
                 title='DfuControlTimeout',
                 name='dfu_control_timeout',
                 checks=(CheckHexList(LEN.DFU_CONTROL_TIMEOUT // 8), CheckByte(),)),
        BitField(FID.DFU_CONTROL_ACTION_TYPE,
                 LEN.DFU_CONTROL_ACTION_TYPE,
                 title='DfuControlActionType',
                 name='dfu_control_action_type',
                 checks=(CheckHexList(LEN.DFU_CONTROL_ACTION_TYPE // 8), CheckByte(),)),
        BitField(FID.DFU_CONTROL_ACTION_DATA,
                 LEN.DFU_CONTROL_ACTION_DATA,
                 title='DfuControlActionData',
                 name='dfu_control_action_data',
                 checks=(CheckHexList(LEN.DFU_CONTROL_ACTION_DATA // 8), )),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SecureDfuControl.DEFAULT.PADDING),
    )

    @aliased(enter_dfu='enable_dfu')
    def __init__(self, device_index, feature_index, enable_dfu, dfu_control_param, dfu_control_timeout,
                 dfu_control_action_type, dfu_control_action_data, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param enable_dfu: The device will enter DFU mode on next restart
        :type enable_dfu: ``int``
        :param dfu_control_param: The DFU control parameter
        :type dfu_control_param: ``int``
        :param dfu_control_timeout: Control timeout (in seconds) to perform the reset in order to enter in bootloader
                                    at the next reset. Zero if unused.
        :type dfu_control_timeout: ``int``
        :param dfu_control_action_type: Control action to perform during the device reset in order to enter in
                                        bootloader at the next reset. Zero if unused.
        :type dfu_control_action_type: ``int``
        :param dfu_control_action_data: Additional data, depending on the control action type. Zero if unused
        :type dfu_control_action_data: ``int``or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.reserved_enable_dfu = 0
        self.enable_dfu = enable_dfu
        self.dfu_control_param = dfu_control_param
        self.dfu_control_timeout = dfu_control_timeout
        self.dfu_control_action_type = dfu_control_action_type
        self.dfu_control_action_data = dfu_control_action_data
    # end def __init__
# end class GetDfuControlResponseV0


class GetDfuControlResponseV1(GetDfuControlResponseV0):
    # See ``GetDfuControlResponseV0``
    VERSION = (1,)

    class ACTION(GetDfuControlResponseV0.ACTION):
        """
        Control action to perform during the device reset in order to enter in bootloader.
        """
        ON_SCREEN_CONFIRMATION = 4
        RESERVED = 5  # 5..255 - reserved
    # end class ACTION
# end class GetDfuControlResponseV1


class SetDfuControlV0(SecureDfuControl):
    """
    SecureDfuControl SetDfuControl implementation class

    Requests device to enter into DFU mode (boot-loader).

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ReservedEnableDfu             7
    EnableDfu                     1
    DfuControlParam               8
    Reserved                      16
    DfuMagicKey                   24
    Padding                       72
    ============================  ==========
    """

    class FID(SecureDfuControl.FID):
        """
        Field Identifiers
        """
        RESERVED_ENABLE_DFU = 0xFA
        ENABLE_DFU = 0xF9
        DFU_CONTROL_PARAM = 0xF8
        RESERVED = 0xF7
        DFU_MAGIC_KEY = 0xF6
        PADDING = 0xF5
    # end class FID

    class LEN(SecureDfuControl.LEN):
        """
        Field Lengths
        """
        RESERVED_ENABLE_DFU = 0x07
        ENABLE_DFU = 0x01
        DFU_CONTROL_PARAM = 0x08
        RESERVED = 0x10
        DFU_MAGIC_KEY = 0x18
        PADDING = 0x48
    # end class LEN

    class DEFAULT(SecureDfuControl.DEFAULT):
        DFU_MAGIC_KEY = 0x444655  # ASCII code for 'DFU'
    # end class DEFAULT

    FIELDS = SecureDfuControl.FIELDS + (
        BitField(FID.RESERVED_ENABLE_DFU,
                 LEN.RESERVED_ENABLE_DFU,
                 title='ReservedEnableDfu',
                 name='reserved_enable_dfu',
                 aliases=('reserved_enter_dfu',),  # This alias is added to be compatible with feature 0x00C2
                 checks=(CheckInt(max_value=0x7F),)),
        BitField(FID.ENABLE_DFU,
                 LEN.ENABLE_DFU,
                 title='EnableDfu',
                 name='enable_dfu',
                 aliases=('enter_dfu',),  # This alias is added to be compatible with feature 0x00C2
                 checks=(CheckInt(0, pow(2, LEN.ENABLE_DFU) - 1),)),
        BitField(FID.DFU_CONTROL_PARAM,
                 LEN.DFU_CONTROL_PARAM,
                 title='DfuControlParam',
                 name='dfu_control_param',
                 checks=(CheckByte(),)),
        BitField(FID.RESERVED,
                 LEN.RESERVED,
                 title='Reserved',
                 name='reserved',
                 checks=(CheckInt(max_value=0xFFFF),)),
        BitField(FID.DFU_MAGIC_KEY,
                 LEN.DFU_MAGIC_KEY,
                 title='DfuMagicKey',
                 name='dfu_magic_key',
                 checks=(CheckInt(0, pow(2, LEN.DFU_MAGIC_KEY) - 1),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckByte(),),
                 default_value=SecureDfuControl.DEFAULT.PADDING),
    )

    @aliased(enter_dfu='enable_dfu')
    def __init__(self, device_index, feature_index, enable_dfu, dfu_control_param=0,
                 dfu_magic_key=DEFAULT.DFU_MAGIC_KEY, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param enable_dfu: The device will enter DFU mode on next restart
        :type enable_dfu: ``int`` or ``HexList``
        :param dfu_control_param: The DFU control parameter, for now it is not used. so it is by default 0
        :type dfu_control_param: ``int`` or ``HexList``
        :param dfu_magic_key: DFU Magic Key
        :type dfu_magic_key: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetDfuControlResponseV0.FUNCTION_INDEX
        self.reserved_enable_dfu = 0
        self.enable_dfu = enable_dfu
        self.dfu_control_param = dfu_control_param
        self.reserved = 0
        self.dfu_magic_key = dfu_magic_key
    # end def __init__
# end class SetDfuControlV0


class SetDfuControlResponseV0(SecureDfuControl):
    """
    SecureDfuControl SetDfuControl response implementation class

    This command may not return a response. If it does, the response is empty (all bytes set to zero).

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
    REQUEST_LIST = (SetDfuControlV0,)
    VERSION = (0, 1, )
    FUNCTION_INDEX = 1

    class FID(SecureDfuControl.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(SecureDfuControl.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80

    # end class LEN

    FIELDS = SecureDfuControl.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SecureDfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetDfuControlResponseV0


class DfuTimeoutEventV0(SecureDfuControl):
    """
    SecureDfuControl DfuTimeoutEvent event

    This event is sent when the window for a reset reaches the timeout.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    DfuControlTimeout             8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1, )
    FUNCTION_INDEX = 0

    class FID(SecureDfuControl.FID):
        """
        Field Identifiers
        """
        DFU_CONTROL_TIMEOUT = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(SecureDfuControl.LEN):
        """
        Field Lengths
        """
        DFU_CONTROL_TIMEOUT = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = SecureDfuControl.FIELDS + (
        BitField(FID.DFU_CONTROL_TIMEOUT,
                 LEN.DFU_CONTROL_TIMEOUT,
                 title='DfuControlTimeout',
                 name='dfu_control_timeout',
                 checks=(CheckHexList(LEN.DFU_CONTROL_TIMEOUT // 8), CheckByte(),)),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SecureDfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, dfu_control_timeout, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param dfu_control_timeout: Control timeout (in seconds) to perform the reset in order to enter in bootloader
                                    at the next reset. Zero if unused.
        :type dfu_control_timeout: ``int``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.dfu_control_timeout = dfu_control_timeout
    # end def __init__
# end class DfuTimeoutEventV0


class DfuCancelEventV1(SecureDfuControl):
    """
    SecureDfuControl DfuCancelEvent event

    This event is sent when the cancel control action is performed.

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
    MSG_TYPE = TYPE.EVENT
    VERSION = (1,)
    FUNCTION_INDEX = 1

    class FID(SecureDfuControl.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(SecureDfuControl.LEN):
        """
        Field Lengths
        """
        PADDING = 0x79

    # end class LEN

    FIELDS = SecureDfuControl.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=SecureDfuControl.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int``
        :param feature_index: Desired feature index
        :type feature_index: ``int``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class DfuCancelEventV1
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
