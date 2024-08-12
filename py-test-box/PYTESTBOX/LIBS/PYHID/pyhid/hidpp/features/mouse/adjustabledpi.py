#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package    pyhid.hidpp.features.mouse.adjustabledpi
    :brief      HID++ 2.0 Adjustable Dpi command interface definition
    :author     fred.chen
    :date       2019/2/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from pyhid.bitfield                  import BitField
from pyhid.hidpp.hidppmessage        import HidppMessage, TYPE
from pyhid.field                     import CheckByte
from pyhid.field                     import CheckHexList
from pyhid.field                     import CheckInt
from pylibrary.tools.hexlist         import HexList
from pylibrary.tools.numeral         import Numeral
from pyhid.hidpp.features.basefeature import FeatureModel
from pyhid.hidpp.features.basefeature import FeatureFactory
from pyhid.hidpp.features.basefeature import FeatureInterface
from pylibrary.tools.docutils import DocUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------

class AdjustableDpi(HidppMessage):
    """
    Adjustable DPI implementation class

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
    FEATURE_ID = 0x2201
    MAX_FUNCTION_INDEX_V0_TO_V1 = 3
    MAX_FUNCTION_INDEX_V2 = 4

    # DPI min and max value according to spec
    # http://goldenpass.logitech.com:8080/gitweb?p=ccp_fw/lfa.git;a=blob_plain;f=doc/hidpp20/x2201_adjustabledpi.ad#setSensorDpi
    MIN_DPI_VALUE = 0x01
    MAX_DPI_VALUE = 0xDFFF  # 57343

    def __init__(self, device_index, feature_index, **kwargs):
        """
        Constructor

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
# end class AdjustableDpi


class AdjustableDpiModel(FeatureModel):
    """
    Adjustable DPI feature model
    """
    class INDEX:
        """
        Functions indexes
        """
        GET_SENSOR_COUNT = 0
        GET_SENSOR_DPI_LIST = 1
        GET_SENSOR_DPI = 2
        SET_SENSOR_DPI = 3
        GET_NUMBER_OF_DPI_LEVELS = 4
    # end class

    @classmethod
    def _get_data_model(cls):
        """
        Adjustable DPI feature data model
        """
        return {
            "feature_base": AdjustableDpi,
            "versions": {
                AdjustableDpiV0.VERSION: {
                    "main_cls": AdjustableDpiV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_SENSOR_COUNT: {"request": GetSensorCount, "response": GetSensorCountResponse},
                            cls.INDEX.GET_SENSOR_DPI_LIST: {"request": GetSensorDpiList,
                                                            "response": GetSensorDpiListResponse},
                            cls.INDEX.GET_SENSOR_DPI: {"request": GetSensorDpi, "response": GetSensorDpiResponseV0},
                            cls.INDEX.SET_SENSOR_DPI: {"request": SetSensorDpiV0ToV1,
                                                       "response": SetSensorDpiResponseV0},
                        },
                    },
                },
                AdjustableDpiV1.VERSION: {
                    "main_cls": AdjustableDpiV1,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_SENSOR_COUNT: {"request": GetSensorCount, "response": GetSensorCountResponse},
                            cls.INDEX.GET_SENSOR_DPI_LIST:
                                {"request": GetSensorDpiList, "response": GetSensorDpiListResponse},
                            cls.INDEX.GET_SENSOR_DPI: {"request": GetSensorDpi, "response": GetSensorDpiResponseV1ToV2},
                            cls.INDEX.SET_SENSOR_DPI: {"request": SetSensorDpiV0ToV1,
                                                       "response": SetSensorDpiResponseV1},
                        },
                    },
                },
                AdjustableDpiV2.VERSION: {
                    "main_cls": AdjustableDpiV2,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_SENSOR_COUNT: {"request": GetSensorCount, "response": GetSensorCountResponse},
                            cls.INDEX.GET_SENSOR_DPI_LIST: {"request": GetSensorDpiList,
                                                            "response": GetSensorDpiListResponse},
                            cls.INDEX.GET_SENSOR_DPI: {"request": GetSensorDpi, "response": GetSensorDpiResponseV1ToV2},
                            cls.INDEX.SET_SENSOR_DPI: {"request": SetSensorDpiV2, "response": SetSensorDpiResponseV2},
                            cls.INDEX.GET_NUMBER_OF_DPI_LEVELS: {"request": GetNumberOfDpiLevelsV2,
                                                                 "response": GetNumberOfDpiLevelsResponseV2},
                        },
                    },
                },
            }
        }
    # end def _get_data_model
# end class AdjustableDpiModel


class AdjustableDpiFactory(FeatureFactory):
    """
    Adjustable DPI factory to create a feature object from a given version
    """
    @staticmethod
    def create(version):
        """
        Adjustable DPI object creation from version number

        :param version: Adjustable DPI feature version
        :type version: ``int``
        :return: Adjustable DPI object
        :rtype: ``AdjustableDpiInterface``
        """
        return AdjustableDpiModel.get_main_cls(version)()
    # end def create
# end class AdjustableDpiFactory


class AdjustableDpiInterface(FeatureInterface, ABC):
    """
    Interface to Adjustable DPI

    Defines required interfaces for Adjustable DPI classes
    """
    def __init__(self):
        """
        Constructor
        """
        self.get_sensor_count_cls = None
        self.get_sensor_count_response_cls = None

        self.get_sensor_dpi_list_cls = None
        self.get_sensor_dpi_list_response_cls = None

        self.get_sensor_dpi_cls = None
        self.get_sensor_dpi_response_cls = None

        self.set_sensor_dpi_cls = None
        self.set_sensor_dpi_response_cls = None

        self.get_number_of_dpi_levels_cls = None
        self.get_number_of_dpi_levels_response_cls = None
    # end def __init__
# end class AdjustableDpiInterface


class AdjustableDpiV0(AdjustableDpiInterface):
    """
    AdjustableDpi
    This feature provides model and unit specific information

    [0] getSensorCount() -> sensorCount
    [1] getSensorDpiList(sensorIdx) -> sensorIdx, dpiList
    [2] getSensorDpi(sensorIdx) -> sensorIdx, dpi
    [3] setSensorDpi(sensorIdx, dpi)
    """
    VERSION = 0

    def __init__(self):
        """
        See :any:`AdjustableDpiInterface.__init__`
        """
        super().__init__()
        self.get_sensor_count_cls = AdjustableDpiModel.get_request_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_SENSOR_COUNT)
        self.get_sensor_count_response_cls = AdjustableDpiModel.get_response_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_SENSOR_COUNT)

        self.get_sensor_dpi_list_cls = AdjustableDpiModel.get_request_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_SENSOR_DPI_LIST)
        self.get_sensor_dpi_list_response_cls = AdjustableDpiModel.get_response_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_SENSOR_DPI_LIST)

        self.get_sensor_dpi_cls = AdjustableDpiModel.get_request_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_SENSOR_DPI)
        self.get_sensor_dpi_response_cls = AdjustableDpiModel.get_response_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_SENSOR_DPI)

        self.set_sensor_dpi_cls = AdjustableDpiModel.get_request_cls(
            self.VERSION, AdjustableDpiModel.INDEX.SET_SENSOR_DPI)
        self.set_sensor_dpi_response_cls = AdjustableDpiModel.get_response_cls(
            self.VERSION, AdjustableDpiModel.INDEX.SET_SENSOR_DPI)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`AdjustableDpiInterface.get_max_function_index`
        """
        return AdjustableDpiModel.get_base_cls().MAX_FUNCTION_INDEX_V0_TO_V1
    # end def get_max_function_index
# end class AdjustableDpiV0


class AdjustableDpiV1(AdjustableDpiV0):
    """
    AdjustableDpi
    This feature provides model and unit specific information

    M [2] getSensorDpi(sensorIdx) -> sensorIdx, dpi, defaultDpi
    M [3] setSensorDpi(sensorIdx, dpi) -> sensorIdx, dpi
    """
    VERSION = 1
# end class AdjustableDpiV1

class AdjustableDpiV2(AdjustableDpiV1):
    """
    AdjustableDpi
    This feature provides model and unit specific information

    M [3] setSensorDpi(sensorIdx, dpi, dpiLevel) -> sensorIdx, dpi, dpiLevel
    + [4] getNumberofDpiLevels() -> dpiLevels
    """
    VERSION = 2

    def __init__(self):
        """
        See :any:`AdjustableDpiInterface.__init__`
        """
        super().__init__()
        self.get_number_of_dpi_levels_cls = AdjustableDpiModel.get_request_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_NUMBER_OF_DPI_LEVELS)
        self.get_number_of_dpi_levels_response_cls = AdjustableDpiModel.get_response_cls(
            self.VERSION, AdjustableDpiModel.INDEX.GET_NUMBER_OF_DPI_LEVELS)
    # end def __init__

    def get_max_function_index(self):
        """
        See :any:`DeviceInformationInterface.get_max_function_index`
        """
        return AdjustableDpiModel.get_base_cls().MAX_FUNCTION_INDEX_V2
    # end def get_max_function_index
# end class AdjustableDpiV1


class GetSensorCount(AdjustableDpi):
    """
    AdjustableDpi GetSensorCount implementation class

    Returns the number of optical sensors in the device.

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

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
              BitField(FID.PADDING,
                       LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=AdjustableDpi.DEFAULT.PADDING),
              )

    @DocUtils.copy_doc(AdjustableDpi.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        """
        See ``AdjustableDpi.__init__``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetSensorCountResponse.FUNCTION_INDEX
    # end def __init__
# end class GetSensorCount


class GetSensorCountResponse(AdjustableDpi):
    """
    AdjustableDpi GetSensorCount response implementation class

    Returns the number of optical sensors in the device.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorCount                   8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorCount)
    FUNCTION_INDEX = 0
    VERSION = (0, 1, 2,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_COUNT = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_COUNT = 0x08
        PADDING = 0x78

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_COUNT,
                 LEN.SENSOR_COUNT,
                 title='Sensor Count',
                 name='sensor_count',
                 checks=(CheckHexList(LEN.SENSOR_COUNT // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_count, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_count: The received sensor count
        :type sensor_count: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.sensor_count = sensor_count
    # end def __init__
# end class GetSensorCountResponse


class GetSensorDpiList(AdjustableDpi):
    """
    AdjustableDpi GetSensorDpiList implementation class

    Returns the DPI List of optical sensor.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    Padding                       16
    ============================  ==========
    """

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        PADDING = 0x10

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_IDX,
                 LEN.SENSOR_IDX,
                 title='Sensor Index',
                 name='sensor_idx',
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8),
                         CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetSensorDpiListResponse.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
    # end def __init__
# end class GetSensorCount


class GetSensorDpiListResponse(AdjustableDpi):
    """
    AdjustableDpi GetSensorDpiList response implementation class

    Returns the DPI List of specific optical sensor.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DpiList                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorDpiList,)
    FUNCTION_INDEX = 1
    VERSION = (0, 1, 2,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        DPI_LIST = 0xF9

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        DPI_LIST = 0x78

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_IDX,
                 LEN.SENSOR_IDX,
                 title='Sensor Index',
                 name='sensor_idx',
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DPI_LIST,
                 LEN.DPI_LIST,
                 title='DPI List',
                 name='dpi_list',
                 checks=(CheckHexList(LEN.DPI_LIST // 8), CheckByte(),), )
    )

    @DocUtils.copy_doc(AdjustableDpi.__init__)
    def __init__(self, device_index, feature_index, sensor_idx, dpi_list, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi_list: The returned DPI list
        :type dpi_list: ``list`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi_list = dpi_list
    # end def __init__
# end class GetSensorDpiListResponse


class GetSensorDpi(AdjustableDpi):
    """
    AdjustableDpi GetSensorDpi implementation class

    Returns the DPI of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    Padding                       16
    ============================  ==========
    """

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        PADDING = 0x10

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
              BitField(FID.SENSOR_IDX,
                       LEN.SENSOR_IDX,
                       title='Sensor Index',
                       name='sensor_idx',
                       checks=(CheckHexList(LEN.SENSOR_IDX // 8), CheckByte(),),
                       conversions={HexList: Numeral}, ),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=AdjustableDpi.DEFAULT.PADDING)
              )

    def __init__(self, device_index, feature_index, sensor_idx, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetSensorDpiResponseV0.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
    # end def __init__
# end class GetSensorDpi


class GetSensorDpiResponseV0(AdjustableDpi):
    """
    AdjustableDpi GetSensorDpi v0 response implementation class

    Returns the DPI of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DPI                           16
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorDpi,)
    FUNCTION_INDEX = 2
    VERSION = (0,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        DPI = 0xF9
        PADDING = 0xF8

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        DPI = 0x10
        PADDING = 0x68

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_IDX,
                 LEN.SENSOR_IDX,
                 title='Sensor Index',
                 name='sensor_idx',
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DPI,
                 LEN.DPI,
                 title='DPI',
                 name='dpi',
                 checks=(CheckHexList(LEN.DPI // 8), CheckInt(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi: The returned DPI
        :type dpi: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi = dpi
    # end def __init__
# end class GetSensorDpiResponseV0


class GetSensorDpiResponseV1ToV2(AdjustableDpi):
    """
    AdjustableDpi GetSensorDpi v1 ~ v2 response implementation class

    Returns the DPI of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DPI                           16
    DefaultDPI                    16
    Padding                       88
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetSensorDpi,)
    FUNCTION_INDEX = 2
    VERSION = (1, 2,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        DPI = 0xF9
        DEFAULT_DPI = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        DPI = 0x10
        DEFAULT_DPI = 0x10
        PADDING = 0x58

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_IDX,
                 LEN.SENSOR_IDX,
                 title='Sensor Index',
                 name='sensor_idx',
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DPI,
                 LEN.DPI,
                 title='DPI',
                 name='dpi',
                 checks=(CheckHexList(LEN.DPI // 8), CheckInt(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DEFAULT_DPI,
                 LEN.DEFAULT_DPI,
                 title='DEFAULT_DPI',
                 name='default_dpi',
                 checks=(CheckHexList(LEN.DEFAULT_DPI // 8), CheckInt(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi, default_dpi, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi: The returned DPI
        :type dpi: ``int`` or ``HexList``
        :param default_dpi: The returned default DPI
        :type default_dpi: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi = dpi
        self.default_dpi = default_dpi
    # end def __init__
# end class GetSensorDpiResponseV1ToV2


class SetSensorDpiV0ToV1(AdjustableDpi):
    """
    AdjustableDpi SetSensorDpi implementation class

    Set DPI to the specific optical sensor
    Returns the DPI setting result of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DPI                           16
    ============================  ==========
    """

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        DPI = 0xF9

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        DPI = 0x10

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
              BitField(FID.SENSOR_IDX,
                       LEN.SENSOR_IDX,
                       title='Sensor Index',
                       name='sensor_idx',
                       checks=(CheckHexList(LEN.SENSOR_IDX // 8),CheckByte(),),
                       conversions={HexList: Numeral}, ),
              BitField(FID.DPI,
                       LEN.DPI,
                       title='DPI',
                       name='dpi',
                       checks=(CheckHexList(LEN.DPI // 8), CheckInt(),),
                       conversions={HexList: Numeral}, )
              )

    def __init__(self, device_index, feature_index, sensor_idx, dpi, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi: The new DPI setting of the specific optical sensor
        :type dpi: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = SetSensorDpiResponseV0.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi = dpi
    # end def __init__
# end class SetSensorDpiV0ToV1


class SetSensorDpiV2(SetSensorDpiV0ToV1):
    """
    AdjustableDpi SetSensorDpi v2 implementation class

    Set DPI to the specific optical sensor
    Returns the DPI setting result of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DPI                           16
    DPI Level                     8
    Params                        96
    ============================  ==========
    """

    class FID(SetSensorDpiV0ToV1.FID):
        """
        Field Identifiers
        """
        DPI_LEVEL = 0xF8
        PADDING = 0XF7

    # end class FID

    class LEN(SetSensorDpiV0ToV1.LEN):
        """
        Field Lengths
        """
        DPI_LEVEL = 0x08
        PADDING = 0x60

    # end class LEN

    FIELDS = SetSensorDpiV0ToV1.FIELDS + (
              BitField(FID.DPI_LEVEL,
                       LEN.DPI_LEVEL,
                       title='DPI Level',
                       name='dpi_level',
                       checks=(CheckHexList(LEN.DPI_LEVEL // 8), CheckByte(),),
                       conversions={HexList: Numeral}, ),
              BitField(FID.PADDING,
                       LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckInt(),),
                       conversions={HexList: Numeral},
                       default_value=AdjustableDpi.DEFAULT.PADDING),
              )

    def __init__(self, device_index, feature_index, sensor_idx, dpi, dpi_level, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi: The new DPI setting of the specific optical sensor
        :type dpi: ``int`` or ``HexList``
        :param dpi_level: The new DPI level setting of the specific optical sensor
        :type dpi_level: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, sensor_idx, dpi, **kwargs)

        self.functionIndex = SetSensorDpiResponseV0.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi = dpi
        self.dpi_level = dpi_level
        self.reportId = AdjustableDpi.DEFAULT.REPORT_ID_LONG
    # end def __init__
# end class SetSensorDpiV2


class SetSensorDpiResponseV0(AdjustableDpi):
    """
    AdjustableDpi SetSensorDpi response implementation class

    Set DPI to the specific optical sensor
    Returns the DPI setting result of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    Params                        128
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetSensorDpiV0ToV1,)
    FUNCTION_INDEX = 3
    VERSION = (0,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        PADDING = 0x80

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    @DocUtils.copy_doc(AdjustableDpi.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        """
        See ``AdjustableDpi.__init__``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
    # end def __init__
# end class SetSensorDpiResponseV0


class SetSensorDpiResponseV1(AdjustableDpi):
    """
    AdjustableDpi SetSensorDpi v1 response implementation class

    Set DPI to the specific optical sensor
    Returns the DPI setting result of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DPI                           16
    Padding                       104
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetSensorDpiV0ToV1,)
    FUNCTION_INDEX = 3
    VERSION = (1,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        DPI = 0xF9
        PADDING = 0xF7

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        DPI = 0x10
        PADDING = 0x68

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_IDX,
                 LEN.SENSOR_IDX,
                 title='Sensor Index',
                 name='sensor_idx',
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DPI,
                 LEN.DPI,
                 title='DPI',
                 name='dpi',
                 checks=(CheckHexList(LEN.DPI // 8), CheckInt(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi: The returned DPI
        :type dpi: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi = dpi
    # end def __init__
# end class SetSensorDpiResponseV1


class SetSensorDpiResponseV2(AdjustableDpi):
    """
    AdjustableDpi SetSensorDpi v2 response implementation class

    Set DPI to the specific optical sensor
    Returns the DPI setting result of the specific sensor

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    SensorIdx                     8
    DPI                           16
    DPI Level                     8
    Params                        96
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (SetSensorDpiV2,)
    FUNCTION_INDEX = 3
    VERSION = (2,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        SENSOR_IDX = 0xFA
        DPI = 0xF9
        DPI_LEVEL = 0xF8
        PADDING = 0xF7

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        SENSOR_IDX = 0x08
        DPI = 0x10
        DPI_LEVEL = 0x08
        PADDING = 0x60

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.SENSOR_IDX,
                 LEN.SENSOR_IDX,
                 title='Sensor Index',
                 name='sensor_idx',
                 checks=(CheckHexList(LEN.SENSOR_IDX // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DPI,
                 LEN.DPI,
                 title='DPI',
                 name='dpi',
                 checks=(CheckHexList(LEN.DPI // 8), CheckInt(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.DPI_LEVEL,
                 LEN.DPI_LEVEL,
                 title='DPI Level',
                 name='dpi_level',
                 checks=(CheckHexList(LEN.DPI_LEVEL // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_idx, dpi, dpi_level, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_idx: The specific sensor index
        :type sensor_idx: ``int`` or ``HexList``
        :param dpi: The returned DPI
        :type dpi: ``int`` or ``HexList``
        :param dpi_level: The returned DPI level
        :type dpi_level: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.sensor_idx = sensor_idx
        self.dpi = dpi
        self.dpi_level = dpi_level
    # end def __init__
# end class SetSensorDpiResponseV2


class GetNumberOfDpiLevelsV2(AdjustableDpi):
    """
    AdjustableDpi GetNumberofDpiLevels implementation class

    Returns the number of "motion" sensors in the device.

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

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        PADDING = 0xFA

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
              BitField(FID.PADDING,
                       LEN.PADDING,
                       title='Padding',
                       name='padding',
                       checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                       default_value=AdjustableDpi.DEFAULT.PADDING),
              )

    @DocUtils.copy_doc(AdjustableDpi.__init__)
    def __init__(self, device_index, feature_index, **kwargs):
        """
        See ``AdjustableDpi.__init__``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = GetNumberOfDpiLevelsResponseV2.FUNCTION_INDEX
    # end def __init__
# end class GetNumberOfDpiLevelsV2


class GetNumberOfDpiLevelsResponseV2(AdjustableDpi):
    """
    AdjustableDpi GetSensorCount response implementation class

    Returns the number of "motion" sensors in the device.

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    ReportID                      8
    DeviceIndex                   8
    FeatureIndex                  8
    FunctionID                    4
    SoftwareID                    4
    DpiLevels                     8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetNumberOfDpiLevelsV2,)
    FUNCTION_INDEX = 4
    VERSION = (2,)

    class FID(AdjustableDpi.FID):
        """
        Field Identifiers
        """
        DPI_LEVELS = 0xFA
        PADDING = 0xF9

    # end class FID

    class LEN(AdjustableDpi.LEN):
        """
        Field Lengths
        """
        DPI_LEVELS = 0x08
        PADDING = 0x78

    # end class LEN

    FIELDS = AdjustableDpi.FIELDS + (
        BitField(FID.DPI_LEVELS,
                 LEN.DPI_LEVELS,
                 title='DPI Levels',
                 name='dpi_levels',
                 checks=(CheckHexList(LEN.DPI_LEVELS // 8), CheckByte(),),
                 conversions={HexList: Numeral}, ),
        BitField(FID.PADDING,
                 LEN.PADDING,
                 title='Padding',
                 name='padding',
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=AdjustableDpi.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, dpi_levels, **kwargs):
        """
        Constructor

        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param dpi_levels: The received DPI Levels
        :type dpi_levels: ``int`` or ``HexList``
        :param **kwargs: Potential future parameters
        :type **kwargs: ``dict``
        """
        super().__init__(device_index, feature_index, **kwargs)

        self.functionIndex = self.FUNCTION_INDEX
        self.dpi_levels = dpi_levels
    # end def __init__
# end class GetNumberOfDpiLevelsResponseV2

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
