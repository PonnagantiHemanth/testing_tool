#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.performdevicediscovery
    :brief: HID++ 1.0 Perform Device Discovery registers definition
    :author: Martin Cryonnet
    :date: 2020/03/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum, Enum
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckInt
from pyhid.field import CheckHexList
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import GetRegister, GetRegisterRequest
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterRequest, SetRegisterResponse


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class PerformDeviceDiscovery:
    """
    Command specific constants
    """
    class DeviceDiscoveryStatus(IntEnum):
        """
        Device Discovery Status valurs
        """
        NOTHING_ONGOING = 0
        DISCOVER_HID_DEVICES_ONGOING = 1

        @classmethod
        def range(cls):
            return tuple([cls.NOTHING_ONGOING, cls.DISCOVER_HID_DEVICES_ONGOING])
        # end def range
    # end class DeviceDiscoveryStatus

    class DiscoveryTimeout(IntEnum):
        """
        Discovery timeout values
        """
        USE_DEFAULT = 0
        DEFAULT_VALUE = 30
        MIN = 1
        TESTABLE_MIN = 5
        MAX = 60

        @classmethod
        def range(cls):
            return tuple([cls.MIN, cls.MAX])
        # end def range
    # end class DiscoveryTimeout

    class DiscoverDevices(IntEnum):
        """
        Discover Devices Values
        """
        NO_CHANGE = 0x00
        DISCOVER_HID_DEVICES = 0x01
        CANCEL_DISCOVERY = 0x02
    # end class DiscoverDevices
# end class PerformDeviceDiscovery


class PerformDeviceDiscoveryModel(BaseRegisterModel):
    """
    Register Perform Device Discovery model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": GetPerformDeviceDiscoveryRequest,
                "response": GetPerformDeviceDiscoveryResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetPerformDeviceDiscoveryRequest,
                "response": SetPerformDeviceDiscoveryResponse
            }
        }
    # end def _get_data_model
# end class PerformDeviceDiscoveryModel


class GetPerformDeviceDiscoveryRequest(GetRegisterRequest):
    """
    Read Perform Device Discovery request
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_DISCOVERY)
    # end def __init__
# end class GetPerformDeviceDiscoveryRequest


class GetPerformDeviceDiscoveryResponse(GetRegister):
    """
    Read Perform Device Discovery response
    """
    class FID(GetRegister.FID):
        """
        Fields identifiers
        """
        R0 = 0xFB
        PADDING = R0 - 1
    # end class FID

    class LEN(GetRegister.LEN):
        """
        Fields length
        """
        R0 = 0x08
        PADDING = 0x10
    # end class LEN

    class OFFSET(GetRegister.OFFSET):
        """
        Fields offset
        """
        R0 = GetRegister.OFFSET.ADDRESS + 0x01
        PADDING = R0 + 0x01
    # end class OFFSET

    class DEFAULT(GetRegister.DEFAULT):
        """
        Fields default values
        """
    # end class DEFAULT

    FIELDS = GetRegister.FIELDS + (
        BitField(FID.R0,
                 LEN.R0,
                 title='R0',
                 name='r0',
                 aliases=('discover_devices_status',),
                 checks=(CheckHexList(LEN.R0 // 8), CheckByte())),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=DEFAULT.PADDING,
                 checks=(CheckHexList(LEN.PADDING // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.PADDING) - 1),)),
    )

    def __init__(self, discover_devices_status):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_DISCOVERY)
        self.discover_devices_status = discover_devices_status
    # end def __init__
# end class GetPerformDeviceDiscoveryResponse


class SetPerformDeviceDiscoveryRequest(SetRegisterRequest):
    """
    Write Perform Device Discovery request
    """

    def __init__(self, discovery_timeout, discover_devices):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_DISCOVERY)
        self.get_field_from_name("p0").add_alias("discovery_timeout")
        self.get_field_from_name("p1").add_alias("discover_devices")
        self.discovery_timeout = discovery_timeout
        self.discover_devices = discover_devices
    # end def __init__
# end class SetPerformDeviceDiscoveryRequest


class SetPerformDeviceDiscoveryResponse(SetRegisterResponse):
    """
    Write Perform Device Discovery response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.PERFORM_DEVICE_DISCOVERY)
    # end def __init__
# end class SetPerformDeviceDiscoveryResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
