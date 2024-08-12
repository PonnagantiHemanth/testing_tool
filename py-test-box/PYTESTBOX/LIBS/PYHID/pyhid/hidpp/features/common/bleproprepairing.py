#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.bleproprepairing
    :brief: HID++ 2.0 BLE Pro pairing command interface definition
    :author: Christophe Roquebert
    :date: 2020/05/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pylibrary.tools.hexlist import HexList
from pyhid.field import CheckHexList, CheckByte
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class BleProPrepairing(HidppMessage):
    """
    BleProPrepairing implementation class

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
    FEATURE_ID = 0x1816
    MAX_FUNCTION_INDEX = 7

    class TYPE():
        """
        Pre pairing data type
        """
        LOCAL = 0x00
        REMOTE = 0x01
        RFU = 0x02 # 2 .. 0xFF
    # end class TYPE

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(**kwargs)

        self.deviceIndex = device_index
        self.featureIndex = feature_index
    # end def __init__
# end class BleProPrepairing


class BleProPrepairingModel(FeatureModel):
    """
    Configurable device properties feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        PREPAIRING_DATA_MANAGEMENT = 0
        SET_LTK = 1
        SET_IRK_REMOTE = 2
        SET_IRK_LOCAL = 3
        SET_CSRK_REMOTE = 4
        SET_CSRK_LOCAL = 5
        SET_PREPAIRING_DATA = 6
        GET_PREPAIRING_DATA = 7
    # end class

    @staticmethod
    def _get_data_model():
        """
        Configurable device properties feature data model
        """
        return {
            "feature_base": BleProPrepairing,
            "versions": {
                BleProPrepairingV0.VERSION: {
                    "main_cls": BleProPrepairingV0,
                    "api": {
                        "functions": {
                            0: {"request": PrepairingDataManagement, "response": PrepairingDataManagementResponse},
                            1: {"request": SetLtk, "response": SetLtkResponse},
                            2: {"request": SetIrkRemote, "response": SetIrkRemoteResponse},
                            3: {"request": SetIrkLocal, "response": SetIrkLocalResponse},
                            4: {"request": SetCsrkRemote, "response": SetCsrkRemoteResponse},
                            5: {"request": SetCsrkLocal, "response": SetCsrkLocalResponse},
                            6: {"request": SetPrepairingData, "response": SetPrepairingDataResponse},
                            7: {"request": GetPrepairingData, "response": GetPrepairingDataResponse},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class BleProPrepairingModel


class BleProPrepairingFactory(FeatureFactory):
    """
    Ble Pro Pre-Pairing factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        Ble pro pre-pairing object creation from version number

        :param version: Ble pro pre-pairing feature version
        :type version: ``int``
        :return: Ble pro pre-pairing object
        :rtype: ``BleProPrepairingInterface``
        """
        return BleProPrepairingModel.get_main_cls(version)()
    # end def create
# end class BleProPrepairingFactory


class BleProPrepairingInterface(FeatureInterface, ABC):
    """
    Interface to configurable device properties

    Defines required interfaces for configurable device properties classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.prepairing_data_management_cls = None
        self.set_ltk_cls = None
        self.set_irk_remote_cls = None
        self.set_irk_local_cls = None
        self.set_csrk_remote_cls = None
        self.set_csrk_local_cls = None
        self.set_prepairing_data_cls = None
        self.get_prepairing_data_cls = None

        self.prepairing_data_management_response_cls = None
        self.set_ltk_response_cls = None
        self.set_irk_remote_response_cls = None
        self.set_irk_local_response_cls = None
        self.set_csrk_remote_response_cls = None
        self.set_csrk_local_response_cls = None
        self.set_prepairing_data_response_cls = None
        self.get_prepairing_data_response_cls = None
    # end def __init__
# end class BleProPrepairingInterface


class BleProPrepairingV0(BleProPrepairingInterface):
    """
    BleProPrepairing
    The BLE Pro prepairing feature exposes a set of command in order to set prepairing data useful for BLE Pro.

    [0] prepairing_data_management(prepairing_slot, mode)
    [1] set_LTK(ltk)
    [2] set_IRK_remote(irk_remote)
    [3] set_IRK_local(irk_local)
    [4] set_CSRK_remote(csrk_remote)
    [5] set_CSRK_local(csrk_local)
    [6] set_prepairing_data(data_type)
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`BleProPrepairingInterface.__init__`
        """
        super().__init__()
        self.prepairing_data_management_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.PREPAIRING_DATA_MANAGEMENT)
        self.prepairing_data_management_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.PREPAIRING_DATA_MANAGEMENT)

        self.set_ltk_cls = BleProPrepairingModel.get_request_cls(self.VERSION, BleProPrepairingModel.INDEX.SET_LTK)
        self.set_ltk_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_LTK)

        self.set_irk_remote_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_IRK_REMOTE)
        self.set_irk_remote_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_IRK_REMOTE)

        self.set_irk_local_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_IRK_LOCAL)
        self.set_irk_local_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_IRK_LOCAL)

        self.set_csrk_remote_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_CSRK_REMOTE)
        self.set_csrk_remote_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_CSRK_REMOTE)

        self.set_csrk_local_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_CSRK_LOCAL)
        self.set_csrk_local_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_CSRK_LOCAL)

        self.set_prepairing_data_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_PREPAIRING_DATA)
        self.set_prepairing_data_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.SET_PREPAIRING_DATA)

        self.get_prepairing_data_cls = BleProPrepairingModel.get_request_cls(
            self.VERSION, BleProPrepairingModel.INDEX.GET_PREPAIRING_DATA)
        self.get_prepairing_data_response_cls = BleProPrepairingModel.get_response_cls(
            self.VERSION, BleProPrepairingModel.INDEX.GET_PREPAIRING_DATA)
    # end def init

    def get_max_function_index(self):
        return BleProPrepairingModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class BleProPrepairingV0


class PrepairingDataManagement(BleProPrepairing):
    """
       BleProPrepairing PrepairingDataManagement implementation class for version 0

       Open/close a prepairing sequence or a delete the prepairing data.

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       PrePairingSlot                8
       Mode                          8
       Padding                       8
       ============================  ==========
       """

    class FID(BleProPrepairing.FID):
        """
        Fields identifiers
        """
        PREPAIRING_SLOT = 0xFA
        MODE = 0xF9
        PADDING = 0xF8
    # end class FID

    class LEN(BleProPrepairing.LEN):
        """
        Fields lengths in bits
        """
        PREPAIRING_SLOT = 0x08
        MODE = 0x08
        PADDING = 0x08
    # end class LEN

    class DEFAULT(BleProPrepairing.DEFAULT):
        """
        Fields default values
        """
        PREPAIRING_SLOT = 0x00
    # end class DEFAULT

    class MODE():
        """
        Prepairing data management
        """
        START = 0x00
        STORE = 0x01
        DELETE = 0x02
        RFU = 0x03 # 3 .. 0xFF
    # end class MODE

    FIELDS = BleProPrepairing.FIELDS + (
        BitField(
            fid=FID.PREPAIRING_SLOT,
            length=LEN.PREPAIRING_SLOT,
            default_value=DEFAULT.PREPAIRING_SLOT,
            title='PrePairingSlot',
            name='prepairing_slot',
            checks=(CheckHexList(LEN.PREPAIRING_SLOT // 8), CheckByte(),),
        ),
        BitField(
            fid=FID.MODE,
            length=LEN.MODE,
            title='Mode',
            name='mode',
            checks=(CheckHexList(LEN.MODE // 8), CheckByte(),),
        ),
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, prepairing_slot, mode, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param prepairing_slot: Prepairing slot in case of there is a need of several prepairing. if there is only
        one slot, the value shall be 0
        :type prepairing_slot: ``HexList or int``
        :param mode: Indicates the action to do around the prepairing data (Open/Close, Delete).
                0x00 : Open the prepairing data management
                0x01 : Close the prepairing data management
                0x02 : Delete the prepairing data
                other values: RFU
        :type mode: ``HexList or int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = PrepairingDataManagementResponse.FUNCTION_INDEX
        self.prepairing_slot = prepairing_slot
        self.mode = mode
    # end def __init__
# end class PrepairingDataManagement


class BleProPrepairingResponse(BleProPrepairing):
    """
        BleProPrepairing response generic implementation class

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

    class FID(BleProPrepairing.FID):
        """
        Fields Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(BleProPrepairing.LEN):
        """
        Fields lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = BleProPrepairing.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=BleProPrepairing.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )
# end class BleProPrepairingResponse


class PrepairingDataManagementResponse(BleProPrepairingResponse):
    """
        BleProPrepairing PrepairingDataManagement response implementation class for version 0

        Acknowledge the Open/close/delete action of the prepairing data.
        """
    REQUEST_LIST = (PrepairingDataManagement,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class PrepairingDataManagementResponse


class SetKey(BleProPrepairing):
    """
       BleProPrepairing SetKey generic implementation class for version 0

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       Key                           128
       ============================  ==========
    """

    class FID(BleProPrepairing.FID):
        """
        Fields identifiers
        """
        KEY = 0xFA
    # end class FID

    class LEN(BleProPrepairing.LEN):
        """
        Fields lengths in bits
        """
        KEY = 0x80
    # end class LEN

    FIELDS = BleProPrepairing.FIELDS + (
        BitField(
            fid=FID.KEY,
            length=LEN.KEY,
            title='Key',
            name='key',
            aliases=('ltk', 'irk_remote', 'irk_local', 'csrk_remote', 'csrk_local',),
            checks=(CheckHexList(LEN.KEY // 8), ),
        ),
    )
# end class SetKey


class SetLtk(SetKey):
    """
    Set the Long-Term Key (LTK) for the prepairing.
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetLtkResponse.FUNCTION_INDEX
    # end def __init__
# end class SetLtk


class SetLtkResponse(BleProPrepairingResponse):
    """
        BleProPrepairing PrepairingDataManagement response implementation class for version 0

        Acknowledge the setting of the Long-Term Key (LTK) for the prepairing.
    """
    REQUEST_LIST = (SetLtk,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetLtkResponse


class SetIrkRemote(SetKey):
    """
    Set the Remote Identity Resolving Key (IRK) for the prepairing.
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetIrkRemoteResponse.FUNCTION_INDEX
    # end def __init__
# end class SetIrkRemote


class SetIrkRemoteResponse(BleProPrepairingResponse):
    """
    BleProPrepairing SetIrkRemote response implementation class for version 0

    Acknowledge the setting of the Remote Identity Resolving Key (IRK) for the prepairing.
    """
    REQUEST_LIST = (SetIrkRemote,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetIrkRemoteResponse


class SetIrkLocal(SetKey):
    """
    Set the Local Identity Resolving Key (IRK) for the prepairing.
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetIrkLocalResponse.FUNCTION_INDEX
    # end def __init__
# end class SetIrkLocal


class SetIrkLocalResponse(BleProPrepairingResponse):
    """
    BleProPrepairing SetIrkLocal response implementation class for version 0

    Acknowledge the setting of the Local Identity Resolving Key (IRK) for the prepairing.
    """
    REQUEST_LIST = (SetIrkLocal,)
    VERSION = (0,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetIrkLocalResponse


class SetCsrkRemote(SetKey):
    """
    Set the Remote Connection Signature Resolving Key (CSRK) for the prepairing.
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetCsrkRemoteResponse.FUNCTION_INDEX
    # end def __init__
# end class SetCsrkRemote


class SetCsrkRemoteResponse(BleProPrepairingResponse):
    """
    BleProPrepairing SetCsrkRemote response implementation class for version 0

    Acknowledge the setting of the Remote Connection Signature Resolving Key (CSRK) for the prepairing.
    """
    REQUEST_LIST = (SetCsrkRemote,)
    VERSION = (0,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetIrkLocalResponse


class SetCsrkLocal(SetKey):
    """
    Set the Local Connection Signature Resolving Key (CSRK) for the prepairing.
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetCsrkLocalResponse.FUNCTION_INDEX
    # end def __init__
# end class SetCsrkLocal


class SetCsrkLocalResponse(BleProPrepairingResponse):
    """
    BleProPrepairing SetCsrkLocal response implementation class for version 0

    Acknowledge the setting of the Local Connection Signature Resolving Key (CSRK) for the prepairing.
    """
    REQUEST_LIST = (SetCsrkLocal,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetCsrkLocalResponse


class SetPrepairingData(BleProPrepairing):
    """
       BleProPrepairing SetPrepairingData implementation class for version 0

       Set the preparing data address for the prepairing.

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       DataType                      8
       Address                       48
       Padding                       72
       ============================  ==========
       """

    class FID(BleProPrepairing.FID):
        """
        Fields identifiers
        """
        DATA_TYPE = 0xFA
        ADDRESS = 0xF9
        PADDING = 0xF8
    # end class FID

    class LEN(BleProPrepairing.LEN):
        """
        Fields lengths in bits
        """
        DATA_TYPE = 0x08
        ADDRESS = 0x30
        PADDING = 0x48
    # end class LEN

    FIELDS = BleProPrepairing.FIELDS + (
        BitField(
            fid=FID.DATA_TYPE,
            length=LEN.DATA_TYPE,
            title='DataType',
            name='data_type',
            checks=(CheckHexList(LEN.DATA_TYPE // 8), CheckByte(),),
        ),
        BitField(
            fid=FID.ADDRESS,
            length=LEN.ADDRESS,
            title='Address',
            name='address',
            aliases=('remote_address', 'local_address', ),
            checks=(CheckHexList(LEN.ADDRESS // 8), ),
        ),
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=BleProPrepairing.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, data_type, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param data_type: Select the data that can be set through this command
        :type data_type: ``HexList or int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = SetPrepairingDataResponse.FUNCTION_INDEX
        self.data_type = data_type
    # end def __init__
# end class SetPrepairingData


class SetPrepairingDataResponse(BleProPrepairingResponse):
    """
    BleProPrepairing SetPrepairingData response implementation class for version 0

    Acknowledge the setting of the preparing data address for the prepairing.
    """
    REQUEST_LIST = (SetPrepairingData,)
    VERSION = (0,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetPrepairingDataResponse


class GetPrepairingData(BleProPrepairing):
    """
       BleProPrepairing GetPrepairingData implementation class for version 0

       Get the preparing data address for the prepairing.

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       DataType                      8
       Padding                       120
       ============================  ==========
       """

    class FID(BleProPrepairing.FID):
        """
        Fields identifiers
        """
        DATA_TYPE = 0xFA
        PADDING = 0xF9
    # end class FID

    class LEN(BleProPrepairing.LEN):
        """
        Fields lengths in bits
        """
        DATA_TYPE = 0x08
        PADDING = 0x78
    # end class LEN

    FIELDS = BleProPrepairing.FIELDS + (
        BitField(
            fid=FID.DATA_TYPE,
            length=LEN.DATA_TYPE,
            title='DataType',
            name='data_type',
            checks=(CheckHexList(LEN.DATA_TYPE // 8), CheckByte(),),
        ),
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=BleProPrepairing.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, data_type=0x00, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param data_type: Select the data that can be set through this command
        :type data_type: ``HexList or int``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        # The request is 20 bytes long
        self.reportId = HidppMessage.DEFAULT.REPORT_ID_LONG
        self.functionIndex = GetPrepairingDataResponse.FUNCTION_INDEX
        self.data_type = data_type
    # end def __init__
# end class GetPrepairingData


class GetPrepairingDataResponse(BleProPrepairingResponse):
    """
    BleProPrepairing GetPrepairingData response implementation class for version 0

    Retrieve the preparing data address.

    Format:

    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    DataType                      8
    Address                       48
    Padding                       72
    ============================  ==========
    """
    REQUEST_LIST = (GetPrepairingData,)
    VERSION = (0,)
    FUNCTION_INDEX = 7

    class FID(BleProPrepairing.FID):
        """
        Fields identifiers
        """
        DATA_TYPE = 0xFA
        ADDRESS = 0xF9
        PADDING = 0xF8
    # end class FID

    class LEN(BleProPrepairing.LEN):
        """
        Fields lengths in bits
        """
        DATA_TYPE = 0x08
        ADDRESS = 0x30
        PADDING = 0x48
    # end class LEN

    FIELDS = BleProPrepairing.FIELDS + (
        BitField(
            fid=FID.DATA_TYPE,
            length=LEN.DATA_TYPE,
            title='DataType',
            name='data_type',
            checks=(CheckHexList(LEN.DATA_TYPE // 8), CheckByte(),),
        ),
        BitField(
            fid=FID.ADDRESS,
            length=LEN.ADDRESS,
            title='Address',
            name='address',
            aliases=('local_address', 'remote_address', ),
            checks=(CheckHexList(LEN.ADDRESS // 8), ),
        ),
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=BleProPrepairing.DEFAULT.PADDING,
            title='Padding',
            name='padding',
            checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
        ),
    )

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class GetPrepairingDataResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
