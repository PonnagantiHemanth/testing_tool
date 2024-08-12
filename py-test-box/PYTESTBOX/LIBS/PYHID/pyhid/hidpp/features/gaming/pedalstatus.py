#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.gaming.pedalstatus
:brief: HID++ 2.0 ``PedalStatus`` command interface definition
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE
from pylibrary.tools.hexlist import HexList


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PedalStatus(HidppMessage):
    """
    This feature is used to determine the connected status of the individual parts of a pedal set.
    This was introduced with the Schumacher pedal set that allows a number of pedals to be connected to the pedal brain.

    There is more than one type of pedal and all the ports on the brain that accept pedals are the same.
    The electronics for the ports only support one pedal type.
    Therefore it is possible to insert the wrong pedal type in to the port.

    This feature is designed to query the device and to find out what pedals are connected
    and if those pedals are connected in to the correct port type.

    If the Schumacher pedals are powered and detects a change (a pedal plugged in or unplugged).
    It will reset and re-enumerate. Therefore there is no change event for this feature.
    """

    FEATURE_ID = 0x8135
    MAX_FUNCTION_INDEX = 0

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
# end class PedalStatus


class PedalStatusModel(FeatureModel):
    """
    Define ``PedalStatus`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """

        # Function index
        GET_PEDAL_STATUS = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``PedalStatus`` feature data model
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.GET_PEDAL_STATUS: {"request": GetPedalStatus, "response": GetPedalStatusResponse}
            }
        }

        return {
            "feature_base": PedalStatus,
            "versions": {
                PedalStatusV0.VERSION: {
                    "main_cls": PedalStatusV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class PedalStatusModel


class PedalStatusFactory(FeatureFactory):
    """
    Get ``PedalStatus`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``PedalStatus`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``PedalStatusInterface``
        """
        return PedalStatusModel.get_main_cls(version)()
    # end def create
# end class PedalStatusFactory


class PedalStatusInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``PedalStatus`` classes
    """

    def __init__(self):
        # Requests
        self.get_pedal_status_cls = None

        # Responses
        self.get_pedal_status_response_cls = None
    # end def __init__
# end class PedalStatusInterface


class PedalStatusV0(PedalStatusInterface):
    """
    Define ``PedalStatusV0`` feature

    This feature provides model and unit specific information for version 0

    [0] getPedalStatus() -> entryCount, entry1PortType, entry1PortStatus, entry2PortType, entry2PortStatus,
    entry3PortType, entry3PortStatus
    """

    VERSION = 0

    def __init__(self):
        # See ``PedalStatus.__init__``
        super().__init__()
        index = PedalStatusModel.INDEX

        # Requests
        self.get_pedal_status_cls = PedalStatusModel.get_request_cls(self.VERSION, index.GET_PEDAL_STATUS)

        # Responses
        self.get_pedal_status_response_cls = PedalStatusModel.get_response_cls(self.VERSION, index.GET_PEDAL_STATUS)
    # end def __init__

    def get_max_function_index(self):
        # See ``PedalStatusInterface.get_max_function_index``
        return PedalStatusModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class PedalStatusV0


class ShortEmptyPacketDataFormat(PedalStatus):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - GetPedalStatus

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(PedalStatus.FID):
        """
        Define Field Identifiers
        """

        PADDING = PedalStatus.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PedalStatus.LEN):
        """
        Define Field Lengths
        """

        PADDING = 0x18
    # end class LEN

    FIELDS = PedalStatus.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PedalStatus.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class GetPedalStatus(ShortEmptyPacketDataFormat):
    """
    Define ``GetPedalStatus`` implementation class for version 0
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
                         functionIndex=GetPedalStatusResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetPedalStatus


class GetPedalStatusResponse(PedalStatus):
    """
    Define ``GetPedalStatusResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    EntryCount                    8
    Entry1PortType                8
    Entry1PortStatus              8
    Entry2PortType                8
    Entry2PortStatus              8
    Entry3PortType                8
    Entry3PortStatus              8
    Padding                       72
    ============================  ==========
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPedalStatus,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(PedalStatus.FID):
        """
        Define Field Identifiers
        """

        ENTRY_COUNT = PedalStatus.FID.SOFTWARE_ID - 1
        ENTRY_1_PORT_TYPE = ENTRY_COUNT - 1
        ENTRY_1_PORT_STATUS = ENTRY_1_PORT_TYPE - 1
        ENTRY_2_PORT_TYPE = ENTRY_1_PORT_STATUS - 1
        ENTRY_2_PORT_STATUS = ENTRY_2_PORT_TYPE - 1
        ENTRY_3_PORT_TYPE = ENTRY_2_PORT_STATUS - 1
        ENTRY_3_PORT_STATUS = ENTRY_3_PORT_TYPE - 1
        PADDING = ENTRY_3_PORT_STATUS - 1
    # end class FID

    class LEN(PedalStatus.LEN):
        """
        Define Field Lengths
        """

        ENTRY_COUNT = 0x8
        ENTRY_1_PORT_TYPE = 0x8
        ENTRY_1_PORT_STATUS = 0x8
        ENTRY_2_PORT_TYPE = 0x8
        ENTRY_2_PORT_STATUS = 0x8
        ENTRY_3_PORT_TYPE = 0x8
        ENTRY_3_PORT_STATUS = 0x8
        PADDING = 0x48
    # end class LEN

    FIELDS = PedalStatus.FIELDS + (
        BitField(fid=FID.ENTRY_COUNT, length=LEN.ENTRY_COUNT,
                 title="EntryCount", name="entry_count",
                 checks=(CheckHexList(LEN.ENTRY_COUNT // 8), CheckByte(),)),
        BitField(fid=FID.ENTRY_1_PORT_TYPE, length=LEN.ENTRY_1_PORT_TYPE,
                 title="Entry1PortType", name="entry_1_port_type",
                 checks=(CheckHexList(LEN.ENTRY_1_PORT_TYPE // 8), CheckByte(),)),
        BitField(fid=FID.ENTRY_1_PORT_STATUS, length=LEN.ENTRY_1_PORT_STATUS,
                 title="Entry1PortStatus", name="entry_1_port_status",
                 checks=(CheckHexList(LEN.ENTRY_1_PORT_STATUS // 8), CheckByte(),)),
        BitField(fid=FID.ENTRY_2_PORT_TYPE, length=LEN.ENTRY_2_PORT_TYPE,
                 title="Entry2PortType", name="entry_2_port_type",
                 checks=(CheckHexList(LEN.ENTRY_2_PORT_TYPE // 8), CheckByte(),)),
        BitField(fid=FID.ENTRY_2_PORT_STATUS, length=LEN.ENTRY_2_PORT_STATUS,
                 title="Entry2PortStatus", name="entry_2_port_status",
                 checks=(CheckHexList(LEN.ENTRY_2_PORT_STATUS // 8), CheckByte(),)),
        BitField(fid=FID.ENTRY_3_PORT_TYPE, length=LEN.ENTRY_3_PORT_TYPE,
                 title="Entry3PortType", name="entry_3_port_type",
                 checks=(CheckHexList(LEN.ENTRY_3_PORT_TYPE // 8), CheckByte(),)),
        BitField(fid=FID.ENTRY_3_PORT_STATUS, length=LEN.ENTRY_3_PORT_STATUS,
                 title="Entry3PortStatus", name="entry_3_port_status",
                 checks=(CheckHexList(LEN.ENTRY_3_PORT_STATUS // 8), CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PedalStatus.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, entry_count,
                 entry_1_port_type, entry_1_port_status,
                 entry_2_port_type, entry_2_port_status,
                 entry_3_port_type, entry_3_port_status,
                 **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param entry_count: Entry Count
        :type entry_count: ``int`` or ``HexList``
        :param entry_1_port_type: Entry 1 Port Type
        :type entry_1_port_type: ``int`` or ``HexList``
        :param entry_1_port_status: Entry 1 Port Status
        :type entry_1_port_status: ``int`` or ``HexList``
        :param entry_2_port_type: Entry 2 Port Type
        :type entry_2_port_type: ``int`` or ``HexList``
        :param entry_2_port_status: Entry 2 Port Status
        :type entry_2_port_status: ``int`` or ``HexList``
        :param entry_3_port_type: Entry 3 Port Type
        :type entry_3_port_type: ``int`` or ``HexList``
        :param entry_3_port_status: Entry 3 Port Status
        :type entry_3_port_status: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.entry_count = entry_count
        self.entry_1_port_type = entry_1_port_type
        self.entry_1_port_status = entry_1_port_status
        self.entry_2_port_type = entry_2_port_type
        self.entry_2_port_status = entry_2_port_status
        self.entry_3_port_type = entry_3_port_type
        self.entry_3_port_status = entry_3_port_status
    # end def __init__
# end class GetPedalStatusResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
