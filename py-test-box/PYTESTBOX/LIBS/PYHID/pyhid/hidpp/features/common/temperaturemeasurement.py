#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.features.common.temperaturemeasurement
:brief: HID++ 2.0 ``TemperatureMeasurement`` command interface definition
:author: Sanjib Hazra <shazra@logitech.com>
:date: 2021/07/19
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
class TemperatureMeasurement(HidppMessage):
    """
    Temperature measurement exchange interface, allowing to get temperature values (-128°C to 127°C)
    from a given number of sensors, with 1°C of resolution
    """
    FEATURE_ID = 0x1F30
    MAX_FUNCTION_INDEX = 1

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
# end class TemperatureMeasurement


class TemperatureMeasurementModel(FeatureModel):
    """
    ``TemperatureMeasurement`` feature model
    """
    class INDEX(object):
        """
        Function/Event index
        """
        # Function index
        GET_INFO = 0
        GET_TEMPERATURE = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        ``TemperatureMeasurement`` feature data model
        """
        return {
            "feature_base": TemperatureMeasurement,
            "versions": {
                TemperatureMeasurementV0.VERSION: {
                    "main_cls": TemperatureMeasurementV0,
                    "api": {
                        "functions": {
                            cls.INDEX.GET_INFO: {
                                "request": GetInfo,
                                "response": GetInfoResponse
                            },
                            cls.INDEX.GET_TEMPERATURE: {
                                "request": GetTemperature,
                                "response": GetTemperatureResponse
                            }
                        }
                    }
                }
            }
        }
    # end def _get_data_model
# end class TemperatureMeasurementModel


class TemperatureMeasurementFactory(FeatureFactory):
    """
    Factory which creates a ``TemperatureMeasurement`` object from a given version
    """
    @staticmethod
    def create(version):
        """
        ``TemperatureMeasurement`` object creation from version number

        :param version: Feature Version
        :type version: ``int``

        :return: Feature Object
        :rtype: ``TemperatureMeasurementInterface``
        """
        return TemperatureMeasurementModel.get_main_cls(version)()
    # end def create
# end class TemperatureMeasurementFactory


class TemperatureMeasurementInterface(FeatureInterface, ABC):
    """
    Defines required interfaces for ``TemperatureMeasurement`` classes
    """
    def __init__(self):
        # Requests
        self.get_info_cls = None
        self.get_temperature_cls = None

        # Responses
        self.get_info_response_cls = None
        self.get_temperature_response_cls = None
    # end def __init__
# end class TemperatureMeasurementInterface


class TemperatureMeasurementV0(TemperatureMeasurementInterface):
    """
    ``TemperatureMeasurementV0``

    This feature provides model and unit specific information for version 0

    [0] getInfo() -> sensorCount

    [1] getTemperature(sensorId) -> sensorId, temperature
    """
    VERSION = 0

    def __init__(self):
        # See ``TemperatureMeasurement.__init__``
        super().__init__()
        index = TemperatureMeasurementModel.INDEX

        # Requests
        self.get_info_cls = TemperatureMeasurementModel.get_request_cls(
            self.VERSION, index.GET_INFO)
        self.get_temperature_cls = TemperatureMeasurementModel.get_request_cls(
            self.VERSION, index.GET_TEMPERATURE)

        # Responses
        self.get_info_response_cls = TemperatureMeasurementModel.get_response_cls(
            self.VERSION, index.GET_INFO)
        self.get_temperature_response_cls = TemperatureMeasurementModel.get_response_cls(
            self.VERSION, index.GET_TEMPERATURE)
    # end def __init__

    def get_max_function_index(self):
        # See ``TemperatureMeasurementInterface.get_max_function_index``
        return TemperatureMeasurementModel.get_base_cls().MAX_FUNCTION_INDEX
    # end def get_max_function_index
# end class TemperatureMeasurementV0


class ShortEmptyPacketDataFormat(TemperatureMeasurement):
    """
    This class is to be used as a base class for several messages in this feature
        - GetInfo

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """
    class FID(TemperatureMeasurement.FID):
        """
        Field Identifiers
        """
        PADDING = TemperatureMeasurement.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(TemperatureMeasurement.LEN):
        """
        Field Lengths
        """
        PADDING = 0x18
    # end class LEN

    FIELDS = TemperatureMeasurement.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TemperatureMeasurement.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class GetInfo(ShortEmptyPacketDataFormat):
    """
    ``GetInfo`` implementation class for version 0
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
                         functionIndex=GetInfoResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetInfo


class GetInfoResponse(TemperatureMeasurement):
    """
    ``GetInfoResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorCount                   8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetInfo,)
    VERSION = (0,)
    FUNCTION_INDEX = 0

    class FID(TemperatureMeasurement.FID):
        """
        Field Identifiers
        """
        SENSOR_COUNT = TemperatureMeasurement.FID.SOFTWARE_ID - 1
        PADDING = SENSOR_COUNT - 1
    # end class FID

    class LEN(TemperatureMeasurement.LEN):
        """
        Field Lengths
        """
        SENSOR_COUNT = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = TemperatureMeasurement.FIELDS + (
        BitField(fid=FID.SENSOR_COUNT, length=LEN.SENSOR_COUNT,
                 title="SensorCount", name="sensor_count",
                 checks=(CheckHexList(LEN.SENSOR_COUNT // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TemperatureMeasurement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_count, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_count: Number of available sensors
        :type sensor_count: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_count = sensor_count
    # end def __init__
# end class GetInfoResponse


class GetTemperature(TemperatureMeasurement):
    """
    ``GetTemperature`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    Padding                       16
    ============================  ==========
    """
    class FID(TemperatureMeasurement.FID):
        """
        Field Identifiers
        """
        SENSOR_ID = TemperatureMeasurement.FID.SOFTWARE_ID - 1
        PADDING = SENSOR_ID - 1
    # end class FID

    class LEN(TemperatureMeasurement.LEN):
        """
        Field Lengths
        """
        SENSOR_ID = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = TemperatureMeasurement.FIELDS + (
        BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                 title="SensorId", name="sensor_id",
                 checks=(CheckHexList(LEN.SENSOR_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TemperatureMeasurement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_id, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=GetTemperatureResponse.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.sensor_id = sensor_id
    # end def __init__
# end class GetTemperature


class GetTemperatureResponse(TemperatureMeasurement):
    """
    ``GetTemperatureResponse`` implementation class for version 0

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    SensorId                      8
    Temperature                   8
    Padding                       112
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetTemperature,)
    VERSION = (0,)
    FUNCTION_INDEX = 1

    class FID(TemperatureMeasurement.FID):
        """
        Field Identifiers
        """
        SENSOR_ID = TemperatureMeasurement.FID.SOFTWARE_ID - 1
        TEMPERATURE = SENSOR_ID - 1
        PADDING = TEMPERATURE - 1
    # end class FID

    class LEN(TemperatureMeasurement.LEN):
        """
        Field Lengths
        """
        SENSOR_ID = 0x8
        TEMPERATURE = 0x8
        PADDING = 0x70
    # end class LEN

    FIELDS = TemperatureMeasurement.FIELDS + (
        BitField(fid=FID.SENSOR_ID, length=LEN.SENSOR_ID,
                 title="SensorId", name="sensor_id",
                 checks=(CheckHexList(LEN.SENSOR_ID // 8),
                         CheckByte(),)),
        BitField(fid=FID.TEMPERATURE, length=LEN.TEMPERATURE,
                 title="Temperature", name="temperature",
                 checks=(CheckHexList(LEN.TEMPERATURE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=TemperatureMeasurement.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, sensor_id, temperature, **kwargs):
        """
        :param device_index: Device Index
        :type device_index: ``int`` or ``HexList``
        :param feature_index: Feature Index
        :type feature_index: ``int`` or ``HexList``
        :param sensor_id: Sensor Index
        :type sensor_id: ``int`` or ``HexList``
        :param temperature: Temperature value from the sensor
        :type temperature: ``int`` or ``HexList``
        :param kwargs: Potential Future Parameters
        :type kwargs: ``int`` or ``HexList`` or ``dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         functionIndex=self.FUNCTION_INDEX,
                         reportId=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor_id = sensor_id
        self.temperature = temperature
    # end def __init__
# end class GetTemperatureResponse

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
