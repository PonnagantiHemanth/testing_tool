#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.forcepairing
:brief: HID++ 2.0 Force Pairing command interface definition
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2021/05/07
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.hidppmessage import HidppMessage
from pyhid.hidpp.hidppmessage import TYPE


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ForcePairing(HidppMessage):
    """
    Force Pairing implementation class

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
    FEATURE_ID = 0x1500
    MAX_FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        super().__init__(deviceIndex=device_index, featureIndex=feature_index, **kwargs)
    # end def __init__
# end class ForcePairing


class ForcePairingModel(FeatureModel):
    """
    ForcePairing feature model.
    """
    class INDEX:
        """
        Functions & Events indexes
        """
        GET_CAPABILITIES = 0
        SET_FORCE_PAIRING = 1
        # Events
        FORCE_PAIRING_TIMEOUT_EVENT = 0
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Force Pairing feature data model.
        """
        return {
            "feature_base": ForcePairing,
            "versions": {
                ForcePairingV0.VERSION: {
                    "main_cls": ForcePairingV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_CAPABILITIES: {"request": GetCapabilities,
                                                         "response": GetCapabilitiesResponse},
                            cls.INDEX.SET_FORCE_PAIRING: {"request": SetForcePairing,
                                                          "response": SetForcePairingResponse},
                        },
                        "events": {
                           cls.INDEX.FORCE_PAIRING_TIMEOUT_EVENT: {"report": ForcePairingTimeoutEvent}
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class ForcePairingModel


class ForcePairingFactory(FeatureFactory):
    """
    Force Pairing factory to create a feature object from a given version.
    """
    @staticmethod
    def create(version):
        """
        Force Pairing object creation from a version number.

        :param version: Force Pairing feature version
        :type version: ``int``

        :return: Force Pairing object
        :rtype: ``ForcePairingInterface``
        """
        return ForcePairingModel.get_main_cls(version)()
    # end def create
# end class ForcePairingFactory


class ForcePairingInterface(FeatureInterface, ABC):
    """
    Interface to the Force Pairing feature.

    Define the required interfaces for Force Pairing classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_capabilities_cls = None
        self.get_capabilities_response_cls = None

        self.set_force_pairing_cls = None
        self.set_force_pairing_response_cls = None

        self.force_pairing_timeout_event_cls = None
    # end def __init__
# end class ForcePairingInterface


class ForcePairingV0(ForcePairingInterface):
    """
    Force Pairing
    This feature is used to force the device to enter a pairing mode.

    [0] getCapabilities(void) ? forcePairingTimeout, forcePairingActionType
    [1] setForcePairing(pairingAddress)
    [event0] forcePairingTimeoutEvent
    """
    VERSION = 0

    def __init__(self):
        # See ``ForcePairingInterface.__init__``
        super().__init__()
        self.get_capabilities_cls = ForcePairingModel.get_request_cls(
            self.VERSION, ForcePairingModel.INDEX.GET_CAPABILITIES)
        self.get_capabilities_response_cls = ForcePairingModel.get_response_cls(
            self.VERSION, ForcePairingModel.INDEX.GET_CAPABILITIES)

        self.set_force_pairing_cls = ForcePairingModel.get_request_cls(
            self.VERSION, ForcePairingModel.INDEX.SET_FORCE_PAIRING)
        self.set_force_pairing_response_cls = ForcePairingModel.get_response_cls(
            self.VERSION, ForcePairingModel.INDEX.SET_FORCE_PAIRING)

        self.force_pairing_timeout_event_cls = ForcePairingModel.get_report_cls(
            self.VERSION, ForcePairingModel.INDEX.FORCE_PAIRING_TIMEOUT_EVENT)
    # end def __init__

    def get_max_function_index(self):
        """
        Get max function index
        """
        return ForcePairingModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class ForcePairingV0


class GetCapabilities(ForcePairing):
    """
    ForcePairing GetCapabilities implementation class

    Return the force pairing information.

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

    class FID(ForcePairing.FID):
        """
        Field Identifiers
        """
        PADDING = ForcePairing.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ForcePairing.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = ForcePairing.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=ForcePairing.DEFAULT.PADDING),
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
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetCapabilitiesResponse.FUNCTION_INDEX, **kwargs)
    # end def __init__
# end class GetCapabilities


class GetCapabilitiesResponse(ForcePairing):
    """
    ForcePairing GetCapabilities response implementation class

    Return the force pairing information.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    ForcePairingTimeout           8
    ForcePairingActionType        8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetCapabilities,)
    FUNCTION_INDEX = 0
    VERSION = (0, )

    class FID(ForcePairing.FID):
        """
        Field Identifiers
        """
        FORCE_PAIRING_TIMEOUT = ForcePairing.FID.SOFTWARE_ID - 1
        FORCE_PAIRING_ACTION_TYPE = FORCE_PAIRING_TIMEOUT - 1
        PADDING = FORCE_PAIRING_ACTION_TYPE - 1
    # end class FID

    class LEN(ForcePairing.LEN):
        """
        Field Lengths
        """
        FORCE_PAIRING_TIMEOUT = 0x08
        FORCE_PAIRING_ACTION_TYPE = 0x08
        PADDING = 0x70
    # end class LEN

    FIELDS = ForcePairing.FIELDS + (
        BitField(FID.FORCE_PAIRING_TIMEOUT,
                 LEN.FORCE_PAIRING_TIMEOUT,
                 title='ForcePairingTimeout',
                 name='force_pairing_timeout',
                 checks=(CheckHexList(LEN.FORCE_PAIRING_TIMEOUT // 8), CheckByte(),),),
        BitField(FID.FORCE_PAIRING_ACTION_TYPE,
                 LEN.FORCE_PAIRING_ACTION_TYPE,
                 title='ForcePairingActionType',
                 name='force_pairing_action_type',
                 checks=(CheckHexList(LEN.FORCE_PAIRING_ACTION_TYPE // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ForcePairing.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, force_pairing_timeout, force_pairing_action_type, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param force_pairing_timeout: Control timeout (in seconds)
        :type force_pairing_timeout: ``int``
        :param force_pairing_action_type: Implementation-defined control action to perform in order to enable the Force
                                          pairing mode.
        :type force_pairing_action_type: ``int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
        self.force_pairing_timeout = force_pairing_timeout
        self.force_pairing_action_type = force_pairing_action_type
    # end def __init__
# end class GetCapabilitiesResponse


class SetForcePairing(ForcePairing):
    """
    ForcePairing SetForcePairing implementation class

    Force the device entering to the pairing mode.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    PairingAddress                32
    Padding                       96
    ============================  ==========
    """
    MSG_TYPE = TYPE.REQUEST

    class FID(ForcePairing.FID):
        """
        Field Identifiers
        """
        PAIRING_ADDRESS = ForcePairing.FID.SOFTWARE_ID - 1
        PADDING = PAIRING_ADDRESS - 1
    # end class FID

    class LEN(ForcePairing.LEN):
        """
        Field Lengths
        """
        PAIRING_ADDRESS = 0x20
        PADDING = 0x60
    # end class LEN

    FIELDS = ForcePairing.FIELDS + (
        BitField(FID.PAIRING_ADDRESS,
                 LEN.PAIRING_ADDRESS,
                 title='PairingAddress',
                 name='pairing_address',
                 checks=(CheckHexList(LEN.PAIRING_ADDRESS // 8), CheckByte(),),),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=ForcePairing.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, pairing_address, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param pairing_address: Pairing address of the destination receiver (4 bytes)
        :type pairing_address: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: ``dict``
        """
        super().__init__(reportId=self.DEFAULT.REPORT_ID_LONG,
                         device_index=device_index, feature_index=feature_index,
                         functionIndex=SetForcePairingResponse.FUNCTION_INDEX, **kwargs)
        self.pairing_address = pairing_address
    # end def __init__
# end class SetForcePairing


class SetForcePairingResponse(ForcePairing):
    """
    ForcePairing SetForcePairing response implementation class

    Acknowledge the device entering to the pairing mode.

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
    REQUEST_LIST = (SetForcePairing,)
    FUNCTION_INDEX = 1
    VERSION = (0, )

    class FID(ForcePairing.FID):
        """
        Field Identifiers
        """
        PADDING = ForcePairing.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(ForcePairing.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = ForcePairing.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 default_value=ForcePairing.DEFAULT.PADDING),
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
        super().__init__(device_index=device_index, feature_index=feature_index, functionIndex=self.FUNCTION_INDEX,
                         **kwargs)
    # end def __init__
# end class SetForcePairingResponse


class ForcePairingTimeoutEvent(SetForcePairingResponse):
    # See ``SetForcePairingResponse``
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, )
    FUNCTION_INDEX = 0
# end class ForcePairingTimeoutEvent

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
