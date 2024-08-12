#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.quaddeviceconnection
    :brief: HID++ 1.0 Receiver Quad or eQUAD Device Connection and Disconnection registers definition
    :author: Martin Cryonnet
    :date: 2020/05/12
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from enum import IntEnum

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.setgetregister import BaseRegisterModel
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegister
from pyhid.hidpp.hidpp1.setgetregister import SetLongRegisterResponse
from pyhid.hidpp.hidpp1.setgetregister import SetRegister
from pyhid.hidpp.hidpp1.setgetregister import SetRegisterResponse
from pyhid.hidpp.hidppmessage import HidppMessage


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class QuadDeviceConnection:
    """
    Command specific constants
    """
    class ConnectDevices(IntEnum):
        """
        Connect Devices values
        """
        NO_CHANGE = 0
        OPEN_LOCK = 1
        CLOSE_LOCK = 2
        DISCONNECT_UNPLUG = 3
        RESERVED = 4
        DISCONNECT_LINK = 5
        OPEN_LOCK_ALLOW_LAST_OTP = 6
        PROXIMITY_OPEN_LOCK = 7
    # end class ConnectDevices

    class OpenLockTimeout(IntEnum):
        """
        Open Lock timeout values
        """
        USE_DEFAULT = 0
        DEFAULT_VALUE = 30
        MIN = 1
        MAX = 255
    # end class OpenLockTimeout

    class DeviceNumber(IntEnum):
        """
        Define some Device Number parameter specific values
        """
        NOT_APPLICABLE = 0x00
    # end class DeviceNumber
# end class DeviceConnection


class QuadDeviceConnectionModel(BaseRegisterModel):
    """
    Register QUAD or eQUAD Device Connection or Disconnection model
    """
    @classmethod
    def _get_data_model(cls):
        """
        Get model

        :return: Register model
        :rtype: ``dict``
        """
        return {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": SetQuadDeviceConnectionRequest,
                "response": SetQuadDeviceConnectionResponse
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": SetGothardDeviceConnectionRequest,
                "response": SetGothardDeviceConnectionResponse
            },
        }
    # end def _get_data_model
# end class TestModeControlModel


class SetQuadDeviceConnectionRequest(SetRegister):
    """
    Write Device Connection and Disconnection request
    """
    class FID(SetRegister.FID):
        """
        Fields Identifiers
        """
        CONNECT_DEVICES = SetRegister.FID.ADDRESS - 1
        DEVICE_NUMBER = CONNECT_DEVICES - 1
        OPEN_LOCK_TIMEOUT = DEVICE_NUMBER - 1
    # end class FID

    class LEN(SetRegister.LEN):
        """
        Fields Lengths in bits
        """
        CONNECT_DEVICES = 0x08
        DEVICE_NUMBER = 0x08
        OPEN_LOCK_TIMEOUT = 0x08
    # end class LEN

    FIELDS = SetRegister.FIELDS + (
        BitField(FID.CONNECT_DEVICES,
                 LEN.CONNECT_DEVICES,
                 title='ConnectDevices',
                 name='connect_devices',
                 checks=(CheckHexList(LEN.CONNECT_DEVICES // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.CONNECT_DEVICES) - 1),)),
        BitField(FID.DEVICE_NUMBER,
                 LEN.DEVICE_NUMBER,
                 title='DeviceNumber',
                 name='device_number',
                 checks=(CheckHexList(LEN.DEVICE_NUMBER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_NUMBER) - 1),)),
        BitField(FID.OPEN_LOCK_TIMEOUT,
                 LEN.OPEN_LOCK_TIMEOUT,
                 title='OpenLockTimeout',
                 name='open_lock_timeout',
                 checks=(CheckHexList(LEN.OPEN_LOCK_TIMEOUT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.OPEN_LOCK_TIMEOUT) - 1),)),
    )

    def __init__(self, connect_devices, device_number, open_lock_timeout):
        """
        See 0xB2 - Device Connection and Disconnection in HIDPP 1_0 Protocol Specification
        (https://docs.google.com/document/d/11LzttOQP5EgmbbKCIkzBd1qCc5O9c7xiFqyRgHtq15c/edit?usp=sharing)

        :param connect_devices: Connect Devices
        :type connect_devices: ``HexList`` or ``int`` or ``QuadDeviceConnection.ConnectDevices``
        :param device_number: * Device number for Connect Devices = Disconnect (unplug) & Disconnect Link
                              * N/A for Connect Devices = 1, 2 & 6
                              * type of device to accept for Connect Devices = 7 (under discussion)
        :type device_number: ``HexList`` or ``int`` or ``QuadDeviceConnection.DeviceNumber``
        :param open_lock_timeout: Open lock timeout
        :type open_lock_timeout: ``HexList`` or ``int`` or ``QuadDeviceConnection.OpenLockTimeout``
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.QUAD_DEVICE_CONNECTION)
        self.connect_devices = connect_devices
        self.device_number = device_number
        self.open_lock_timeout = open_lock_timeout
    # end def __init__
# end class SetQuadDeviceConnectionRequest


class SetQuadDeviceConnectionResponse(SetRegisterResponse):
    """
    Write QUAD or eQUAD Device Connection and Disconnection response
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.QUAD_DEVICE_CONNECTION)
    # end def __init__
# end class SetQuadDeviceConnectionResponse


class SetGothardDeviceConnectionRequest(SetQuadDeviceConnectionRequest):
    """
    Perform a QUAD or eQUAD device connection setup
    """
    SUB_ID = SetLongRegister.SUB_ID

    class FID(SetQuadDeviceConnectionRequest.FID):
        """
        Fields Identifiers
        """
        RSSI_THRESHOLD = SetQuadDeviceConnectionRequest.FID.OPEN_LOCK_TIMEOUT - 1
        LNA_GAIN = RSSI_THRESHOLD - 1
        AAF_GAIN = LNA_GAIN - 1
        DEVICE_QUAD_ID = AAF_GAIN - 1
        DEVICE_QUAD_ID_MASK = DEVICE_QUAD_ID - 1
        DEBUG_MODE = DEVICE_QUAD_ID_MASK - 1
        CONSECUTIVES_MESSAGES_COUNT = DEBUG_MODE - 1
        OUTPUT_POWER = CONSECUTIVES_MESSAGES_COUNT - 1
        PROTOCOL = OUTPUT_POWER - 1
        PADDING = PROTOCOL - 1
    # end class FID

    class LEN(SetQuadDeviceConnectionRequest.LEN):
        """
        Fields Lengths in bits
        """
        RSSI_THRESHOLD = 0x08
        LNA_GAIN = 0x08
        AAF_GAIN = 0x08
        DEVICE_QUAD_ID = 0x10
        DEVICE_QUAD_ID_MASK = 0x10
        DEBUG_MODE = 0x08
        CONSECUTIVES_MESSAGES_COUNT = 0x08
        OUTPUT_POWER = 0x08
        PROTOCOL = 0x08
        PADDING = 0x10
    # end class LEN

    FIELDS = SetQuadDeviceConnectionRequest.FIELDS + (
        BitField(FID.RSSI_THRESHOLD,
                 LEN.RSSI_THRESHOLD,
                 title='RssiThreshold',
                 name='rssi_threshold',
                 checks=(CheckHexList(LEN.RSSI_THRESHOLD // 8), CheckByte(),),
                 default_value=QuadDeviceConnection.ConnectDevices.PROXIMITY_OPEN_LOCK),
        BitField(FID.LNA_GAIN,
                 LEN.LNA_GAIN,
                 title='LNAGain',
                 name='lna_gain',
                 checks=(CheckHexList(LEN.LNA_GAIN // 8), CheckByte(),),),
        BitField(FID.AAF_GAIN,
                 LEN.AAF_GAIN,
                 title='AAFGain',
                 name='aaf_gain',
                 checks=(CheckHexList(LEN.AAF_GAIN // 8), CheckByte(),),),
        BitField(FID.DEVICE_QUAD_ID,
                 LEN.DEVICE_QUAD_ID,
                 title='DeviceQuadId',
                 name='device_quad_id',
                 checks=(CheckHexList(LEN.DEVICE_QUAD_ID // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_QUAD_ID) - 1),)),
        BitField(FID.DEVICE_QUAD_ID_MASK,
                 LEN.DEVICE_QUAD_ID_MASK,
                 title='DeviceQuadIdMask',
                 name='device_quad_id_mask',
                 checks=(CheckHexList(LEN.DEVICE_QUAD_ID_MASK // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DEVICE_QUAD_ID_MASK) - 1),)),
        BitField(FID.DEBUG_MODE,
                 LEN.DEBUG_MODE,
                 title='DebugMode',
                 name='debug_mode',
                 checks=(CheckHexList(LEN.DEBUG_MODE // 8), CheckByte(),),),
        BitField(FID.CONSECUTIVES_MESSAGES_COUNT,
                 LEN.CONSECUTIVES_MESSAGES_COUNT,
                 title='ConsecutivesMessagesCount',
                 name='consecutives_messages_count',
                 checks=(CheckHexList(LEN.CONSECUTIVES_MESSAGES_COUNT // 8), CheckByte(),),),
        BitField(FID.OUTPUT_POWER,
                 LEN.OUTPUT_POWER,
                 title='OutputPower',
                 name='output_power',
                 checks=(CheckHexList(LEN.OUTPUT_POWER // 8), CheckByte(),),),
        BitField(FID.PROTOCOL,
                 LEN.PROTOCOL,
                 title='Protocol',
                 name='protocol',
                 checks=(CheckHexList(LEN.PROTOCOL // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=SetQuadDeviceConnectionRequest.DEFAULT.PADDING),
    )

    def __init__(self, connect_devices, device_number, open_lock_timeout, rssi_threshold, lna_gain, aaf_gain,
                 device_quad_id, device_quad_id_mask, debug_mode, consecutives_messages_count, output_power, protocol):
        """
        Constructor

        :param connect_devices: Connect Devices options
        :type connect_devices: ``int``
        :param device_number: pairing slot (matches the index returned by 0x41 notification)
        :type device_number: ``int``
        :param open_lock_timeout: timeout in second in range 1 to 255 (0=default timeout is 30s)
        :type open_lock_timeout: ``int``
        :param rssi_threshold: RSSI Threshold
        :type rssi_threshold: ``int``
        :param lna_gain: LNA gain value
        :type lna_gain: ``int``
        :param aaf_gain: AAF gain value
        :type aaf_gain: ``int``
        :param device_quad_id: Device QUAD or eQUAD Identifier (2 Bytes)
        :type device_quad_id: ``HexList``
        :param device_quad_id_mask: Device QUAD or eQUAD Identifier Mask (2 Bytes)
        :type device_quad_id_mask: ``HexList``
        :param debug_mode:  Bit 0 = Allow RDSSI reporting thru 0x49 notification
                            Bit 1 = ACK not sent to the receiver (spy mode)
        :type debug_mode: ``int``
        :param consecutives_messages_count: Pairing acceptance criteria
        :type consecutives_messages_count: ``int``
        :param output_power: Output power (dBm) on 4 bits (i.e. 0xF gives the maximum power)
        :type output_power: ``int``
        :param protocol: 0 for Unifying (eQuad v4)
                         1 for Gaming (eQuad v12)
        :type protocol: ``int``

        """
        super().__init__(connect_devices=connect_devices, device_number=device_number,
                         open_lock_timeout=open_lock_timeout)

        self.report_id = HidppMessage.DEFAULT.REPORT_ID_LONG
        # Parameters initialization
        self.rssi_threshold = rssi_threshold
        self.lna_gain = lna_gain
        self.aaf_gain = aaf_gain
        self.device_quad_id = device_quad_id
        self.device_quad_id_mask = device_quad_id_mask
        self.debug_mode = debug_mode
        self.consecutives_messages_count = consecutives_messages_count
        self.output_power = output_power
        self.protocol = protocol
    # end def __init__
#end class SetGothardDeviceConnectionRequest


class SetGothardDeviceConnectionResponse(SetLongRegisterResponse):
    """
    Acknowledge the QUAD or eQUAD device connection setup
    """
    def __init__(self):
        """
        Constructor
        """
        super().__init__(device_index=Hidpp1Data.DeviceIndex.TRANSCEIVER,
                         address=Hidpp1Data.Hidpp1RegisterAddress.QUAD_DEVICE_CONNECTION)
    # end def __init__
# class SetGothardDeviceConnectionResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
