#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.0'
:package: pyhid.hidpp.features.common.oobstate
:brief: HID++ 2.0 ``OobState`` command interface definition
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2022/03/24
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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class OobState(HidppMessage):
    """
    | Define OobState interface which is used to force a device in its Out - Of - the - Box state;
    | So depending on the device, the following tasks have to be done:
    | * All custom settings stored in Non-Volatile Memory (persistent) must be erased
    | * The radio set in OOB; in Cala (dual UNY / BLE) for example, the lists of UNY and BLE hosts are cleared
    | * All parameters set to their default values
    """

    FEATURE_ID = 0x1805
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
# end class OobState


class OobStateModel(FeatureModel):
    """
    Define ``OobState`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        SET_OOB_STATE = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``OobState`` feature data model

        :return: data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.SET_OOB_STATE: {
                    "request": SetOobState,
                    "response": SetOobStateResponse
                }
            }
        }

        return {
            "feature_base": OobState,
            "versions": {
                OobStateV0.VERSION: {
                    "main_cls": OobStateV0,
                    "api": function_map_v0
                }
            }
        }
    # end def _get_data_model
# end class OobStateModel


class OobStateFactory(FeatureFactory):
    """
    Get ``OobState`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``OobState`` object from given version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``OobStateInterface``
        """
        return OobStateModel.get_main_cls(version)()
    # end def create
# end class OobStateFactory


class OobStateInterface(FeatureInterface, ABC):
    """
    Define required interfaces for ``OobState``
    """

    def __init__(self):
        # Requests
        self.set_oob_state_cls = None

        # Responses
        self.set_oob_state_response_cls = None
    # end def __init__
# end class OobStateInterface


class OobStateV0(OobStateInterface):
    """
    Define ``OobStateV0`` feature

    This feature provides model and unit specific information for version 0

    [0] setOobState() -> None
    """

    VERSION = 0

    def __init__(self):
        # See ``OobState.__init__``
        super().__init__()
        index = OobStateModel.INDEX

        # Requests
        self.set_oob_state_cls = OobStateModel.get_request_cls(
            self.VERSION, index.SET_OOB_STATE)

        # Responses
        self.set_oob_state_response_cls = OobStateModel.get_response_cls(
            self.VERSION, index.SET_OOB_STATE)
    # end def __init__

    def get_max_function_index(self):
        # See ``OobStateInterface.get_max_function_index``
        return OobStateModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class OobStateV0


class ShortEmptyPacketDataFormat(OobState):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetOobState

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(OobState.FID):
        """
        Define field identifier(s)
        """
        PADDING = OobState.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OobState.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = OobState.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OobState.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(OobState):
    """
    Allow this class is to be used as a base class for several messages in this feature
        - SetOobStateResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(OobState.FID):
        """
        Define field identifier(s)
        """
        PADDING = OobState.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(OobState.LEN):
        """
        Define field length(s)
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = OobState.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=OobState.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class SetOobState(ShortEmptyPacketDataFormat):
    """
    Define ``SetOobState`` implementation class for version 0
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
                         functionIndex=SetOobStateResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class SetOobState


class SetOobStateResponse(LongEmptyPacketDataFormat):
    """
    Define ``SetOobStateResponse`` implementation class for version 0
    """

    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetOobState,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

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
# end class SetOobStateResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
