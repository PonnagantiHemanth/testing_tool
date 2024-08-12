#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.features.common.equadpairingenc
    :brief: HID++ 2.0 eQuad Pairing Encryption command interface definition
    :author: Christophe Roquebert
    :date: 2020/05/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield import BitField
from pyhid.hidpp.hidppmessage import HidppMessage, TYPE
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyhid.field import CheckHexList, CheckByte
from pyhid.field import CheckInt
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class EquadPairingEnc(HidppMessage):
    """
    eQuad Pairing Enc implementation class

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
    FEATURE_ID = 0x1811
    MAX_FUNCTION_INDEX = 2

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
# end class EquadPairingEnc


class EquadPairingEncModel(FeatureModel):
    """
    Configurable device properties feature model
    """
    @staticmethod
    def _get_data_model():
        """
        Configurable device properties feature data model
        """
        return {
            "feature_base": EquadPairingEnc,
            "versions": {
                EquadPairingEncV0.VERSION: {
                    "main_cls": EquadPairingEncV0,
                    "api": {
                        "functions": {
                            0: {"request": GetPairingInfo, "response": GetPairingInfoResponse},
                            1: {"request": SetPairingInfo, "response": SetPairingInfoResponse},
                            2: {"request": SetEncKey, "response": SetEncKeyResponse},
                        }
                    },
                },
            }
        }
    # end def _get_data_model
# end class EquadPairingEncModel


class EquadPairingEncFactory(FeatureFactory):
    """
    Configurable Device Properties factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        Configurable device properties object creation from version number

        :param version: Configurable device properties feature version
        :type version: ``int``
        :return: Configurable device properties object
        :rtype: ``EquadPairingEncInterface``
        """
        return EquadPairingEncModel.get_main_cls(version)()
    # end def create
# end class EquadPairingEncFactory


class EquadPairingEncInterface(FeatureInterface, ABC):
    """
    Interface to configurable device properties

    Defines required interfaces for configurable device properties classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_pairing_info_cls = None
        self.set_pairing_info_cls = None

        self.get_pairing_info_response_cls = None
        self.set_pairing_info_response_cls = None

        self.set_enc_key_cls = None
        self.set_enc_key_response_cls = None
    # end def __init__
# end class EquadPairingEncInterface


class EquadPairingEncV0(EquadPairingEncInterface):
    """
    EquadPairingEnc
    The BLE Pro prepairing feature exposes a set of command in order to set prepairing data useful for BLE Pro.

    [0] prepairing_data_management(prepairing_slot, mode)
    [1] set_LTK(ltk)
    [2] set_IRK_central(irk_central)
    [3] set_IRK_peripheral(irk_peripheral)
    [4] set_CSRK_central(csrk_central)
    [5] set_CSRK_peripheral(csrk_peripheral)
    [6] set_prepairing_data(data_type)
    """
    VERSION = 0
    GET_PAIRING_INFO = 0
    SET_PAIRING_INFO = 1
    SET_ENC_KEY = 2

    def __init__(self):
        """
        See :any:`EquadPairingEncInterface.__init__`
        """
        super().__init__()
        self.get_pairing_info_cls = EquadPairingEncModel.get_request_cls(
            self.VERSION, self.GET_PAIRING_INFO)
        self.get_pairing_info_response_cls = EquadPairingEncModel.get_response_cls(
            self.VERSION, self.GET_PAIRING_INFO)

        self.set_pairing_info_cls = EquadPairingEncModel.get_request_cls(self.VERSION, self.SET_PAIRING_INFO)
        self.set_pairing_info_response_cls = EquadPairingEncModel.get_response_cls(self.VERSION, self.SET_PAIRING_INFO)

        self.set_enc_key_cls = EquadPairingEncModel.get_request_cls(self.VERSION, self.SET_ENC_KEY)
        self.set_enc_key_response_cls = EquadPairingEncModel.get_response_cls(self.VERSION, self.SET_ENC_KEY)
    # end def init

    def get_max_function_index(self):
        return EquadPairingEncModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class EquadPairingEncV0


class GetPairingInfo(EquadPairingEnc):
    """
       EquadPairingEnc GetPairingInfo implementation class for version 0

       Reads the pairing information from a non-volatile storage on the device being manufactured.

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

    class FID(EquadPairingEnc.FID):
        """
        Fields identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(EquadPairingEnc.LEN):
        """
        Fields lengths in bits
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = EquadPairingEnc.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=EquadPairingEnc.DEFAULT.PADDING,
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
        self.functionIndex = GetPairingInfoResponse.FUNCTION_INDEX
    # end def __init__
# end class GetPairingInfo


class PairingInfoFormat(EquadPairingEnc):
    """
        PairingInfo generic format implementation class

        Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        AddrBase                      32
        AddrDest                      8
        EquadAttrbReserved            1
        EquadAttrbTpadInfo            1
        EquadAttrb16bitMse            1
        EquadAttrbHighRptRate         1
        EquadAttrbOtpDevice           1
        EquadAttrbMultidevice         1
        EquadAttrbOtaDfu              1
        EquadAttrbEncryption          1
        EquadAttrbReservedBytes       40
        Serial                        32
        FlagsReserved                 7
        FlagsUseAttr                  1
        ============================  ==========
        """

    class FID(EquadPairingEnc.FID):
        """
        Fields Identifiers
        """
        ADDR_BASE = 0xFA
        ADDR_DEST = 0xF9
        EQUAD_ATTRB_RESERVED = 0xF8
        EQUAD_ATTRB_TPAD_INFO = 0xF7
        EQUAD_ATTRB_16BIT_MSE = 0xF6
        EQUAD_ATTRB_HIGH_RPT_RATE = 0xF5
        EQUAD_ATTRB_OTP_DEVICE = 0xF4
        EQUAD_ATTRB_MULTIDEVICE = 0xF3
        EQUAD_ATTRB_OTA_DFU = 0xF2
        EQUAD_ATTRB_ENCRYPTION = 0xF1
        EQATTR_01_05 = 0xF0
        SERIAL = 0xEF
        FLAGS_RESERVED = 0xEE
        FLAGS_USE_ATTR = 0xED
    # end class FID

    class LEN(EquadPairingEnc.LEN):
        """
        Fields lengths in bits
        """
        ADDR_BASE = 0x20
        ADDR_DEST = 0x08
        EQUAD_ATTRB_RESERVED = 0x01
        EQUAD_ATTRB_TPAD_INFO = 0x01
        EQUAD_ATTRB_16BIT_MSE = 0x01
        EQUAD_ATTRB_HIGH_RPT_RATE = 0x01
        EQUAD_ATTRB_OTP_DEVICE = 0x01
        EQUAD_ATTRB_MULTIDEVICE = 0x01
        EQUAD_ATTRB_OTA_DFU = 0x01
        EQUAD_ATTRB_ENCRYPTION = 0x01
        EQATTR_01_05 = 0x28
        SERIAL = 0x20
        FLAGS_RESERVED = 0x07
        FLAGS_USE_ATTR = 0x01
    # end class LEN

    FIELDS = EquadPairingEnc.FIELDS + (
        BitField(
            fid=FID.ADDR_BASE,
            length=LEN.ADDR_BASE,
            title='AddrBase',
            name='addr_base',
            checks=(CheckHexList(LEN.ADDR_BASE // 8), ),
        ),
        BitField(
            fid=FID.ADDR_DEST,
            length=LEN.ADDR_DEST,
            title='AddrDest',
            name='addr_dest',
            checks=(CheckHexList(LEN.ADDR_DEST // 8), CheckByte(),),
        ),
        BitField(FID.EQUAD_ATTRB_RESERVED,
               LEN.EQUAD_ATTRB_RESERVED,
               title='EquadAttrbReserved',
               name='equad_attrb_reserved',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_RESERVED) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_TPAD_INFO,
               LEN.EQUAD_ATTRB_TPAD_INFO,
               title='EquadAttrbTpadInfo',
               name='equad_attrb_tpad_info',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_TPAD_INFO) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_16BIT_MSE,
               LEN.EQUAD_ATTRB_16BIT_MSE,
               title='EquadAttrb16bitMse',
               name='equad_attrb_16bit_mse',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_16BIT_MSE) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_HIGH_RPT_RATE,
               LEN.EQUAD_ATTRB_HIGH_RPT_RATE,
               title='EquadAttrbHighRptRate',
               name='equad_attrb_high_rpt_rate',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_HIGH_RPT_RATE) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_OTP_DEVICE,
               LEN.EQUAD_ATTRB_OTP_DEVICE,
               title='EquadAttrbOtpDevice',
               name='equad_attrb_otp_device',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_OTP_DEVICE) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_MULTIDEVICE,
               LEN.EQUAD_ATTRB_MULTIDEVICE,
               title='EquadAttrbMultiDevice',
               name='equad_attrb_multidevice',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_MULTIDEVICE) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_OTA_DFU,
               LEN.EQUAD_ATTRB_OTA_DFU,
               title='EquadAttrbOtaDfu',
               name='equad_attrb_ota_dfu',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_OTA_DFU) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQUAD_ATTRB_ENCRYPTION,
               LEN.EQUAD_ATTRB_ENCRYPTION,
               title='EquadAttrbEncryption',
               name='equad_attrb_encryption',
               checks=(CheckInt(0, pow(2, LEN.EQUAD_ATTRB_ENCRYPTION) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.EQATTR_01_05,
               LEN.EQATTR_01_05,
               title='Eqattr0105',
               name='eqattr_01_05',
            checks=(CheckHexList(LEN.EQATTR_01_05 // 8), ),
        ),
        BitField(
            fid=FID.SERIAL,
            length=LEN.SERIAL,
            title='Serial',
            name='serial',
            checks=(CheckHexList(LEN.SERIAL // 8), ),
        ),
        BitField(FID.FLAGS_RESERVED,
               LEN.FLAGS_RESERVED,
               title='FlagsReserved',
               name='flags_reserved',
               checks=(CheckInt(0, pow(2, LEN.FLAGS_USE_ATTR) - 1),),
               conversions={HexList: Numeral}
        ),
        BitField(FID.FLAGS_USE_ATTR,
               LEN.FLAGS_USE_ATTR,
               title='FlagsUseAttr',
               name='flags_use_attr',
               checks=(CheckInt(0, pow(2, LEN.FLAGS_USE_ATTR) - 1),),
               conversions={HexList: Numeral}
        ),
    )

    def __init__(self, device_index, feature_index, addr_base, addr_dest, equad_attrb_tpad_info=False,
                 equad_attrb_16bit_mse=False, equad_attrb_high_rpt_rate=False, equad_attrb_otp_device=False,
                 equad_attrb_multidevice=False, equad_attrb_ota_dfu=False, equad_attrb_encryption=False,
                 eqattr_01_05=HexList("00"*(LEN.EQATTR_01_05//8)), serial=HexList("00"*(LEN.SERIAL//8)),
                 flags_use_attr=False, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param addr_base: Address Base field
        :type addr_base: ``HexList``
        :param addr_dest: Address Destination field
        :type addr_dest: ``HexList``
        :param equad_attrb_tpad_info: tpad_info Equad attribute field
        :type equad_attrb_tpad_info: ``bool``
        :param equad_attrb_16bit_mse: 16bit_mse Equad attribute field
        :type equad_attrb_16bit_mse: ``bool``
        :param equad_attrb_high_rpt_rate: high_rpt_rate Equad attribute field
        :type equad_attrb_high_rpt_rate: ``bool``
        :param equad_attrb_otp_device: otp_device Equad attribute field
        :type equad_attrb_otp_device: ``bool``
        :param equad_attrb_multidevice: multidevice Equad attribute field
        :type equad_attrb_multidevice: ``bool``
        :param equad_attrb_ota_dfu: ota_dfu Equad attribute field
        :type equad_attrb_ota_dfu: ``bool``
        :param equad_attrb_encryption: encryption Equad attribute field
        :type equad_attrb_encryption: ``bool``
        :param serial: 4 bytes long serial field
        :type serial: ``HexList``
        :param flags_use_attr: (Read only): 1 -> The device will use the attributes written by the test plan.
                          0 -> The device will use its hardcoded equad attributes and will ignore any attributes written
                                via x1811 feature. The device will also ignore the attributes accepted by a receiver
                                after a pairing.
        :type flags_use_attr: ``bool``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index)
        self.addr_base = addr_base
        self.addr_dest = addr_dest
        self.equad_attrb_tpad_info = equad_attrb_tpad_info
        self.equad_attrb_16bit_mse = equad_attrb_16bit_mse
        self.equad_attrb_high_rpt_rate = equad_attrb_high_rpt_rate
        self.equad_attrb_otp_device = equad_attrb_otp_device
        self.equad_attrb_multidevice = equad_attrb_multidevice
        self.equad_attrb_ota_dfu = equad_attrb_ota_dfu
        self.equad_attrb_encryption = equad_attrb_encryption
        self.eqattr_01_05 = eqattr_01_05
        self.serial = serial
        self.flags_use_attr = flags_use_attr
    # end def __init__
# end class PairingInfoFormat


class GetPairingInfoResponse(PairingInfoFormat):
    """
    EquadPairingEnc GetPairingInfo response implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetPairingInfo,)
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
# end class GetPairingInfoResponse


class SetPairingInfo(PairingInfoFormat):
    """
       EquadPairingEnc SetPairingInfo implementation class for version 0

       Writes the pairing information on the non-volatile memory of the device being manufactured.

       Format:

        ============================  ==========
        Name                          Bit count
        ============================  ==========
        ReportID                      8
        DeviceIndex                   8
        FeatureIndex                  8
        FunctionID                    4
        SoftwareID                    4
        AddrBase                      32
        AddrDest                      8
        EquadAttrbReserved            1
        EquadAttrbTpadInfo            1
        EquadAttrb16bitMse            1
        EquadAttrbHighRptRate         1
        EquadAttrbOtpDevice           1
        EquadAttrbMultidevice         1
        EquadAttrbOtaDfu              1
        EquadAttrbEncryption          1
        EquadAttrbReservedBytes       40
        Serial                        32
        FlagsReserved                 7
        FlagsUseAttr                  1
        ============================  ==========
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
        self.functionIndex = SetPairingInfoResponse.FUNCTION_INDEX
    # end def __init__
# end class SetPairingInfo

class SetPairingInfoResponse(EquadPairingEnc):
    """
    EquadPairingEnc SetPairingInfo response implementation class for version 0

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
    REQUEST_LIST = (SetPairingInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(EquadPairingEnc.FID):
        """
        Fields identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(EquadPairingEnc.LEN):
        """
        Fields lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = EquadPairingEnc.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=EquadPairingEnc.DEFAULT.PADDING,
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
# end class SetPairingInfoResponse


class SetEncKey(EquadPairingEnc):
    """
       EquadPairingEnc SetEncKey implementation class for version 0

       Writes the pairing encryption key on the non-volatile memory of the device being manufactured.

       Format:

       ============================  ==========
       Name                          Bit count
       ============================  ==========
       ReportID                      8
       DeviceIndex                   8
       FeatureIndex                  8
       FunctionID                    4
       SoftwareID                    4
       Encryption Key                128
       ============================  ==========
       """

    class FID(EquadPairingEnc.FID):
        """
        Fields identifiers
        """
        ENC_KEY = 0xFA
    # end class FID

    class LEN(EquadPairingEnc.LEN):
        """
        Fields lengths in bits
        """
        ENC_KEY = 0x80
    # end class LEN

    FIELDS = EquadPairingEnc.FIELDS + (
        BitField(
            fid=FID.ENC_KEY,
            length=LEN.ENC_KEY,
            title='EncKey',
            name='enc_key',
            checks=(CheckHexList(LEN.ENC_KEY // 8), ),
        ),
    )

    def __init__(self, device_index, feature_index, enc_key, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int or HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int or HexList``
        :param enc_key: Pairing encryption key
        :type enc_key: ``HexList``
        :param \**kwargs: Potential future parameters
        :type \**kwargs: dict
        """
        super().__init__(device_index, feature_index, **kwargs)
        self.functionIndex = SetEncKeyResponse.FUNCTION_INDEX
        self.enc_key = enc_key
    # end def __init__
# end class SetEncKey


class SetEncKeyResponse(EquadPairingEnc):
    """
    EquadPairingEnc SetEncKey response implementation class for version 0

    Acknowledge the writing of the pairing encryption key on the non-volatile memory of the device being manufactured.
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetEncKey,)
    VERSION = (0,)
    FUNCTION_INDEX = 2

    class FID(EquadPairingEnc.FID):
        """
        Fields identifiers
        """
        PADDING = 0xFA
    # end class FID

    class LEN(EquadPairingEnc.LEN):
        """
        Fields lengths in bits
        """
        PADDING = 0x80
    # end class LEN

    FIELDS = EquadPairingEnc.FIELDS + (
        BitField(
            fid=FID.PADDING,
            length=LEN.PADDING,
            default_value=EquadPairingEnc.DEFAULT.PADDING,
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
# end class SetEncKeyResponse

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
