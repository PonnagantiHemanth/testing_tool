#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.keyboard.fninversionformultihostdevices
:brief: HID++ 2.0 ``FnInversionForMultiHostDevices`` command interface definition
:author: Fred Chen <fchen7@logitech.com>
:date: 2022/04/26
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
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class FnInversionForMultiHostDevices(HidppMessage):
    """
    Fn Inversion for multi-host devices feature is dedicated to multi-host keyboards to give possibility to SW to
    set Fn Inversion option for each connected host separately.
    """

    FEATURE_ID = 0x40A3
    MAX_FUNCTION_INDEX = 1

    @unique
    class FnInversionState(IntEnum):
        """
        Fn Inversion State
        """
        OFF = 0
        ON = 1
    # end class FnInversionState

    @unique
    class HostIndex(IntEnum):
        """
        Define the hostIndex: Channel / host index. 0xFF = Current Host; 0x00 = Host 1, 0x01 = Host 2, etc.
        """
        HOST1 = 0x0
        HOST2 = 0x1
        HOST3 = 0x2
        CURRENT_HOST = 0xFF
    # end class HostIndex

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class FnInversionForMultiHostDevices


class FnInversionForMultiHostDevicesModel(FeatureModel):
    """
    Define ``FnInversionForMultiHostDevices`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        GET_GLOBAL_FN_INVERSION = 0
        SET_GLOBAL_FN_INVERSION = 1

        # Event index
        F_LOCK_CHANGE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``FnInversionForMultiHostDevices`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_GLOBAL_FN_INVERSION: {
                    "request": GetGlobalFnInversion,
                    "response": GetGlobalFnInversionResponse
                },
                cls.INDEX.SET_GLOBAL_FN_INVERSION: {
                    "request": SetGlobalFnInversion,
                    "response": SetGlobalFnInversionResponse
                }
            },
            "events": {
                cls.INDEX.F_LOCK_CHANGE: {"report": FLockChangeEvent}
            }
        }

        return {
            "feature_base": FnInversionForMultiHostDevices,
            "versions": {
                FnInversionForMultiHostDevicesV0.VERSION: {
                    "main_cls": FnInversionForMultiHostDevicesV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class FnInversionForMultiHostDevicesModel


class FnInversionForMultiHostDevicesFactory(FeatureFactory):
    """
    Get ``FnInversionForMultiHostDevices`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``FnInversionForMultiHostDevices`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``FnInversionForMultiHostDevicesInterface``
        """
        return FnInversionForMultiHostDevicesModel.get_main_cls(version)()
    # end def create
# end class FnInversionForMultiHostDevicesFactory


class FnInversionForMultiHostDevicesInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``FnInversionForMultiHostDevices``
    """

    def __init__(self):
        # Requests
        self.get_global_fn_inversion_cls = None
        self.set_global_fn_inversion_cls = None

        # Responses
        self.get_global_fn_inversion_response_cls = None
        self.set_global_fn_inversion_response_cls = None

        # Events
        self.f_lock_change_event_cls = None
    # end def __init__
# end class FnInversionForMultiHostDevicesInterface


class FnInversionForMultiHostDevicesV0(FnInversionForMultiHostDevicesInterface):
    """
    Define ``FnInversionForMultiHostDevicesV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getGlobalFnInversion(hostIndex) -> hostIndex, fnInversionState, fnInversionDefaultState,
        capabilitiesMaskReservedBits, capabilitiesMaskFnLock

    [1] setGlobalFnInversion(hostIndex, fnInversionState) -> hostIndex, fnInversionState, fnInversionDefaultState,
        capabilitiesMaskReservedBits, capabilitiesMaskFnLock

    [Event 0] fLockChangeEvent -> hostIndex, fnInversionState, fnInversionDefaultState, capabilitiesMaskReservedBits,
              capabilitiesMaskFnLock
    """

    VERSION = 0

    def __init__(self):
        # See ``FnInversionForMultiHostDevices.__init__``
        super().__init__()
        index = FnInversionForMultiHostDevicesModel.INDEX

        # Requests
        self.get_global_fn_inversion_cls = FnInversionForMultiHostDevicesModel.get_request_cls(
            self.VERSION, index.GET_GLOBAL_FN_INVERSION)
        self.set_global_fn_inversion_cls = FnInversionForMultiHostDevicesModel.get_request_cls(
            self.VERSION, index.SET_GLOBAL_FN_INVERSION)

        # Responses
        self.get_global_fn_inversion_response_cls = FnInversionForMultiHostDevicesModel.get_response_cls(
            self.VERSION, index.GET_GLOBAL_FN_INVERSION)
        self.set_global_fn_inversion_response_cls = FnInversionForMultiHostDevicesModel.get_response_cls(
            self.VERSION, index.SET_GLOBAL_FN_INVERSION)

        # Events
        self.f_lock_change_event_cls = FnInversionForMultiHostDevicesModel.get_report_cls(
            self.VERSION, index.F_LOCK_CHANGE)
    # end def __init__

    def get_max_function_index(self):
        # See ``FnInversionForMultiHostDevicesInterface.get_max_function_index``
        return FnInversionForMultiHostDevicesModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class FnInversionForMultiHostDevicesV0


class FnInversionInfo(FnInversionForMultiHostDevices):
    """
    Allow this class is to be used as a base class for several messages in this feature.
        - GetGlobalFnInversionResponse
        - SetGlobalFnInversionResponse
        - FLockChangeEvent

    Format:
    ===============================  ==========
    Name                             Bit count
    ===============================  ==========
    HostIndex                        8
    FnInversionState                 8
    FnInversionDefaultState          8
    CapabilitiesMaskReservedBits     7
    CapabilitiesMaskFnLock           1
    Padding                          96
    ===============================  ==========
    """

    class FID(FnInversionForMultiHostDevices.FID):
        """
        Define field identifier(s)
        """
        HOST_INDEX = FnInversionForMultiHostDevices.FID.SOFTWARE_ID - 1
        FN_INVERSION_STATE = HOST_INDEX - 1
        FN_INVERSION_DEFAULT_STATE = FN_INVERSION_STATE - 1
        CAPABILITIES_MASK_RESERVED_BITS = FN_INVERSION_DEFAULT_STATE - 1
        CAPABILITIES_MASK_FN_LOCK = CAPABILITIES_MASK_RESERVED_BITS - 1
        PADDING = CAPABILITIES_MASK_FN_LOCK - 1
    # end class FID

    class LEN(FnInversionForMultiHostDevices.LEN):
        """
        Define field length(s)
        """
        HOST_INDEX = 0x8
        FN_INVERSION_STATE = 0x8
        FN_INVERSION_DEFAULT_STATE = 0x8
        CAPABILITIES_MASK_RESERVED_BITS = 0x7
        CAPABILITIES_MASK_FN_LOCK = 0x1
        PADDING = 0x60
    # end class LEN

    FIELDS = FnInversionForMultiHostDevices.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),),
                 zero_print=True),
        BitField(fid=FID.FN_INVERSION_STATE, length=LEN.FN_INVERSION_STATE,
                 title="FnInversionState", name="fn_inversion_state",
                 checks=(CheckHexList(LEN.FN_INVERSION_STATE // 8),
                         CheckByte(),),
                 zero_print=True),
        BitField(fid=FID.FN_INVERSION_DEFAULT_STATE, length=LEN.FN_INVERSION_DEFAULT_STATE,
                 title="FnInversionDefaultState", name="fn_inversion_default_state",
                 checks=(CheckHexList(LEN.FN_INVERSION_DEFAULT_STATE // 8),
                         CheckByte(),)),
        BitField(fid=FID.CAPABILITIES_MASK_RESERVED_BITS, length=LEN.CAPABILITIES_MASK_RESERVED_BITS,
                 title="CapabilitiesMaskReservedBits", name="capabilities_mask_reserved_bits",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CAPABILITIES_MASK_RESERVED_BITS) - 1),)),
        BitField(fid=FID.CAPABILITIES_MASK_FN_LOCK, length=LEN.CAPABILITIES_MASK_FN_LOCK,
                 title="CapabilitiesMaskFnLock", name="capabilities_mask_fn_lock",
                 conversions={HexList: Numeral},
                 checks=(CheckInt(0, pow(2, LEN.CAPABILITIES_MASK_FN_LOCK) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FnInversionForMultiHostDevices.DEFAULT.PADDING),
    )
# end class FnInversionInfo


class GetGlobalFnInversion(FnInversionForMultiHostDevices):
    """
    Define ``GetGlobalFnInversion`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    HostIndex                     8
    Padding                       16
    ============================  ==========
    """

    class FID(FnInversionForMultiHostDevices.FID):
        """
        Define field identifier(s)
        """
        HOST_INDEX = FnInversionForMultiHostDevices.FID.SOFTWARE_ID - 1
        PADDING = HOST_INDEX - 1
    # end class FID

    class LEN(FnInversionForMultiHostDevices.LEN):
        """
        Define field length(s)
        """
        HOST_INDEX = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = FnInversionForMultiHostDevices.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),),
                 zero_print=True),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FnInversionForMultiHostDevices.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param host_index: Host Index
        :type host_index: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetGlobalFnInversionResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.host_index = host_index
    # end def __init__
# end class GetGlobalFnInversion


class GetGlobalFnInversionResponse(FnInversionInfo):
    """
    Define ``GetGlobalFnInversionResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetGlobalFnInversion,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, host_index, fn_inversion_state, fn_inversion_default_state,
                 capabilities_mask_reserved_bits, capabilities_mask_fn_lock, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param host_index: Host Index
        :type host_index: ``int|HexList``
        :param fn_inversion_state: Fn Inversion State
        :type fn_inversion_state: ``int|HexList``
        :param fn_inversion_default_state: Fn Inversion Default State
        :type fn_inversion_default_state: ``int|HexList``
        :param capabilities_mask_reserved_bits: Capabilities Mask Reserved Bits
        :type capabilities_mask_reserved_bits: ``int|HexList``
        :param capabilities_mask_fn_lock: Capabilities Mask Fn Lock
        :type capabilities_mask_fn_lock: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.host_index = host_index
        self.fn_inversion_state = fn_inversion_state
        self.fn_inversion_default_state = fn_inversion_default_state
        self.capabilities_mask_reserved_bits = capabilities_mask_reserved_bits
        self.capabilities_mask_fn_lock = capabilities_mask_fn_lock
    # end def __init__
# end class GetGlobalFnInversionResponse


class SetGlobalFnInversion(FnInversionForMultiHostDevices):
    """
    Define ``SetGlobalFnInversion`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    HostIndex                     8
    FnInversionState              8
    Padding                       8
    ============================  ==========
    """

    class FID(FnInversionForMultiHostDevices.FID):
        """
        Define field identifier(s)
        """
        HOST_INDEX = FnInversionForMultiHostDevices.FID.SOFTWARE_ID - 1
        FN_INVERSION_STATE = HOST_INDEX - 1
        PADDING = FN_INVERSION_STATE - 1
    # end class FID

    class LEN(FnInversionForMultiHostDevices.LEN):
        """
        Define field length(s)
        """
        HOST_INDEX = 0x8
        FN_INVERSION_STATE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = FnInversionForMultiHostDevices.FIELDS + (
        BitField(fid=FID.HOST_INDEX, length=LEN.HOST_INDEX,
                 title="HostIndex", name="host_index",
                 checks=(CheckHexList(LEN.HOST_INDEX // 8),
                         CheckByte(),),
                 zero_print=True),
        BitField(fid=FID.FN_INVERSION_STATE, length=LEN.FN_INVERSION_STATE,
                 title="FnInversionState", name="fn_inversion_state",
                 checks=(CheckHexList(LEN.FN_INVERSION_STATE // 8),
                         CheckByte(),),
                 zero_print=True),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=FnInversionForMultiHostDevices.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, host_index, fn_inversion_state, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param host_index: Host Index
        :type host_index: ``int|HexList``
        :param fn_inversion_state: Fn Inversion State
        :type fn_inversion_state: ``int|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=SetGlobalFnInversionResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.host_index = host_index
        self.fn_inversion_state = fn_inversion_state
    # end def __init__
# end class SetGlobalFnInversion


class SetGlobalFnInversionResponse(FnInversionInfo):
    """
    Define ``SetGlobalFnInversionResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetGlobalFnInversion,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, host_index, fn_inversion_state, fn_inversion_default_state,
                 capabilities_mask_reserved_bits, capabilities_mask_fn_lock, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param host_index: Host Index
        :type host_index: ``int|HexList``
        :param fn_inversion_state: Fn Inversion State
        :type fn_inversion_state: ``int|HexList``
        :param fn_inversion_default_state: Fn Inversion Default State
        :type fn_inversion_default_state: ``int|HexList``
        :param capabilities_mask_reserved_bits: Capabilities Mask Reserved Bits
        :type capabilities_mask_reserved_bits: ``int|HexList``
        :param capabilities_mask_fn_lock: Capabilities Mask Fn Lock
        :type capabilities_mask_fn_lock: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.host_index = host_index
        self.fn_inversion_state = fn_inversion_state
        self.fn_inversion_default_state = fn_inversion_default_state
        self.capabilities_mask_reserved_bits = capabilities_mask_reserved_bits
        self.capabilities_mask_fn_lock = capabilities_mask_fn_lock
    # end def __init__
# end class SetGlobalFnInversionResponse


class FLockChangeEvent(FnInversionInfo):
    """
    Define ``FLockChangeEvent`` implementation class for version 0
    """

    MSG_TYPE = TYPE.EVENT
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, host_index, fn_inversion_state, fn_inversion_default_state,
                 capabilities_mask_reserved_bits, capabilities_mask_fn_lock, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int|HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int|HexList``
        :param host_index: Host Index
        :type host_index: ``int|HexList``
        :param fn_inversion_state: Fn Inversion State
        :type fn_inversion_state: ``int|HexList``
        :param fn_inversion_default_state: Fn Inversion Default State
        :type fn_inversion_default_state: ``int|HexList``
        :param capabilities_mask_reserved_bits: Fn Inversion Capabilities Mask Reserved Bits
        :type capabilities_mask_reserved_bits: ``int|HexList``
        :param capabilities_mask_fn_lock: Fn Inversion Capabilities Mask Fn Lock
        :type capabilities_mask_fn_lock: ``bool|HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int|HexList|dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.host_index = host_index
        self.fn_inversion_state = fn_inversion_state
        self.fn_inversion_default_state = fn_inversion_default_state
        self.capabilities_mask_reserved_bits = capabilities_mask_reserved_bits
        self.capabilities_mask_fn_lock = capabilities_mask_fn_lock
    # end def __init__
# end class FLockChangeEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
