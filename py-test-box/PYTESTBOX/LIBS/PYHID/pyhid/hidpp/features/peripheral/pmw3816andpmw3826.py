#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pyhid.hidpp.features.peripheral.pmw3816andpmw3826
:brief: HID++ 2.0 ``PMW3816andPMW3826`` command interface definition
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from abc import ABC

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


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826(HidppMessage):
    """
    Test interface for the mouse sensor Pixart PMW3816(TOG6) and Pixart PMW3826(TOGX)
    """
    FEATURE_ID = 0x9001
    MAX_FUNCTION_INDEX_V0 = 6
    MAX_FUNCTION_INDEX_V1 = 6

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        # noinspection PyTypeChecker
        super().__init__(device_index=device_index, feature_index=feature_index, **kwargs)
    # end def __init__
# end class PMW3816andPMW3826


# noinspection DuplicatedCode
class PMW3816andPMW3826Model(FeatureModel):
    """
    Define ``PMW3816andPMW3826`` feature model
    """

    class INDEX(object):
        """
        Define Function/Event index
        """
        # Function index
        READ_SENSOR_REGISTER = 0
        WRITE_SENSOR_REGISTER = 1
        RESET_SENSOR = 2
        SHUTDOWN_SENSOR = 3
        TRACKING_TEST = 4
        FRAME_CAPTURE = 5
        GET_STRAP_DATA = 5
        CONTINUOUS_POWER = 6

        # Event index
        TRACKING_REPORT = 0
        FRAME_CAPTURE_REPORT = 1
    # end class INDEX

    @classmethod
    def _get_data_model(cls):
        """
        Get ``PMW3816andPMW3826`` feature data model

        :return: Data model
        :rtype: ``dict``
        """
        function_map_v0 = {
            "functions": {
                cls.INDEX.READ_SENSOR_REGISTER: {
                    "request": ReadSensorRegister,
                    "response": ReadSensorRegisterResponse
                },
                cls.INDEX.WRITE_SENSOR_REGISTER: {
                    "request": WriteSensorRegister,
                    "response": WriteSensorRegisterResponse
                },
                cls.INDEX.RESET_SENSOR: {
                    "request": ResetSensor,
                    "response": ResetSensorResponse
                },
                cls.INDEX.SHUTDOWN_SENSOR: {
                    "request": ShutdownSensor,
                    "response": ShutdownSensorResponse
                },
                cls.INDEX.TRACKING_TEST: {
                    "request": TrackingTest,
                    "response": TrackingTestResponse
                },
                cls.INDEX.FRAME_CAPTURE: {
                    "request": FrameCaptureV0,
                    "response": FrameCaptureResponseV0
                },
                cls.INDEX.CONTINUOUS_POWER: {
                    "request": ContinuousPower,
                    "response": ContinuousPowerResponse
                }
            },
            "events": {
                cls.INDEX.TRACKING_REPORT: {"report": TrackingReportEvent},
                cls.INDEX.FRAME_CAPTURE_REPORT: {"report": FrameCaptureReportEvent}
            }
        }

        function_map_v1 = {
            "functions": {
                cls.INDEX.READ_SENSOR_REGISTER: {
                    "request": ReadSensorRegister,
                    "response": ReadSensorRegisterResponse
                },
                cls.INDEX.WRITE_SENSOR_REGISTER: {
                    "request": WriteSensorRegister,
                    "response": WriteSensorRegisterResponse
                },
                cls.INDEX.RESET_SENSOR: {
                    "request": ResetSensor,
                    "response": ResetSensorResponse
                },
                cls.INDEX.SHUTDOWN_SENSOR: {
                    "request": ShutdownSensor,
                    "response": ShutdownSensorResponse
                },
                cls.INDEX.TRACKING_TEST: {
                    "request": TrackingTest,
                    "response": TrackingTestResponse
                },
                cls.INDEX.GET_STRAP_DATA: {
                    "request": GetStrapDataV1,
                    "response": GetStrapDataResponseV1
                },
                cls.INDEX.CONTINUOUS_POWER: {
                    "request": ContinuousPower,
                    "response": ContinuousPowerResponse
                }
            },
            "events": {
                cls.INDEX.TRACKING_REPORT: {"report": TrackingReportEvent},
                cls.INDEX.FRAME_CAPTURE_REPORT: {"report": FrameCaptureReportEvent}
            }
        }

        return {
            "feature_base": PMW3816andPMW3826,
            "versions": {
                PMW3816andPMW3826V0.VERSION: {
                    "main_cls": PMW3816andPMW3826V0,
                    "api": function_map_v0
                },
                PMW3816andPMW3826V1.VERSION: {
                    "main_cls": PMW3816andPMW3826V1,
                    "api": function_map_v1
                }
            }
        }
    # end def _get_data_model
# end class PMW3816andPMW3826Model


class PMW3816andPMW3826Factory(FeatureFactory):
    """
    Get ``PMW3816andPMW3826`` object from a given version
    """

    @staticmethod
    def create(version):
        """
        Create ``PMW3816andPMW3826`` object from given version number

        :param version: Feature version
        :type version: ``int``

        :return: Feature object
        :rtype: ``PMW3816andPMW3826Interface``
        """
        return PMW3816andPMW3826Model.get_main_cls(version)()
    # end def create
# end class PMW3816andPMW3826Factory


class PMW3816andPMW3826Interface(FeatureInterface, ABC):
    """
    Define required interfaces for ``PMW3816andPMW3826``
    """

    def __init__(self):
        # Requests
        self.read_sensor_register_cls = None
        self.write_sensor_register_cls = None
        self.reset_sensor_cls = None
        self.shutdown_sensor_cls = None
        self.tracking_test_cls = None
        self.frame_capture_cls = None
        self.get_strap_data_cls = None
        self.continuous_power_cls = None

        # Responses
        self.read_sensor_register_response_cls = None
        self.write_sensor_register_response_cls = None
        self.reset_sensor_response_cls = None
        self.shutdown_sensor_response_cls = None
        self.tracking_test_response_cls = None
        self.frame_capture_response_cls = None
        self.get_strap_data_response_cls = None
        self.continuous_power_response_cls = None

        # Events
        self.tracking_report_event_cls = None
        self.frame_capture_report_event_cls = None
    # end def __init__
# end class PMW3816andPMW3826Interface


class PMW3816andPMW3826V0(PMW3816andPMW3826Interface):
    """
    Define ``PMW3816andPMW3826V0`` feature

    This feature provides model and unit specific information for version 0

    [0] readSensorRegister(registerAddress) -> registerValue

    [1] writeSensorRegister(registerAddress, registerValue) -> None

    [2] resetSensor() -> None

    [3] shutdownSensor() -> None

    [4] trackingTest(count) -> None

    [5] frameCapture() -> None

    [6] continuousPower() -> None

    [Event 0] TrackingReportEvent -> deltaX, deltaY, surfaceQualityValue, pixelSum, maximumPixel, minimumPixel,
    shutter, counter, sQUALAverage, shutterAverage

    [Event 1] FrameCaptureReportEvent -> frameData
    """
    VERSION = 0

    def __init__(self):
        # See ``PMW3816andPMW3826.__init__``
        super().__init__()
        index = PMW3816andPMW3826Model.INDEX

        # Requests
        self.read_sensor_register_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.READ_SENSOR_REGISTER)
        self.write_sensor_register_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.WRITE_SENSOR_REGISTER)
        self.reset_sensor_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.SHUTDOWN_SENSOR)
        self.tracking_test_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.TRACKING_TEST)
        self.frame_capture_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.FRAME_CAPTURE)
        self.continuous_power_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.CONTINUOUS_POWER)

        # Responses
        self.read_sensor_register_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.READ_SENSOR_REGISTER)
        self.write_sensor_register_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.WRITE_SENSOR_REGISTER)
        self.reset_sensor_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.RESET_SENSOR)
        self.shutdown_sensor_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.SHUTDOWN_SENSOR)
        self.tracking_test_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.TRACKING_TEST)
        self.frame_capture_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.FRAME_CAPTURE)
        self.continuous_power_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.CONTINUOUS_POWER)

        # Events
        self.tracking_report_event_cls = PMW3816andPMW3826Model.get_report_cls(
            self.VERSION, index.TRACKING_REPORT)
        self.frame_capture_report_event_cls = PMW3816andPMW3826Model.get_report_cls(
            self.VERSION, index.FRAME_CAPTURE_REPORT)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``PMW3816andPMW3826Interface.get_max_function_index``
        return PMW3816andPMW3826Model.get_base_cls().MAX_FUNCTION_INDEX_V0
    # end def get_max_function_index
# end class PMW3816andPMW3826V0


class PMW3816andPMW3826V1(PMW3816andPMW3826V0):
    """
    Define ``PMW3816andPMW3826V1`` feature

    This feature provides model and unit specific information for version 1

    [5] getStrapData() -> sensor, strapMeasurementX
    """
    VERSION = 1

    def __init__(self):
        # See ``PMW3816andPMW3826.__init__``
        super().__init__()
        index = PMW3816andPMW3826Model.INDEX

        # Requests
        self.get_strap_data_cls = PMW3816andPMW3826Model.get_request_cls(
            self.VERSION, index.GET_STRAP_DATA)

        # Responses
        self.get_strap_data_response_cls = PMW3816andPMW3826Model.get_response_cls(
            self.VERSION, index.GET_STRAP_DATA)
    # end def __init__

    # noinspection PyMethodMayBeStatic
    def get_max_function_index(self):
        # See ``PMW3816andPMW3826Interface.get_max_function_index``
        return PMW3816andPMW3826Model.get_base_cls().MAX_FUNCTION_INDEX_V1
    # end def get_max_function_index
# end class PMW3816andPMW3826V1


class ShortEmptyPacketDataFormat(PMW3816andPMW3826):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - ResetSensor
        - ShutdownSensor
        - FrameCaptureV0
        - GetStrapDataV1
        - ContinuousPower

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       24
    ============================  ==========
    """

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        PADDING = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        PADDING = 0x18
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),)
# end class ShortEmptyPacketDataFormat


class LongEmptyPacketDataFormat(PMW3816andPMW3826):
    """
    Define reusable class to be used as a base class for several messages in this feature
        - WriteSensorRegisterResponse
        - ResetSensorResponse
        - ShutdownSensorResponse
        - TrackingTestResponse
        - FrameCaptureResponseV0
        - ContinuousPowerResponse

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Padding                       128
    ============================  ==========
    """

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        PADDING = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        PADDING = 0x80
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),)
# end class LongEmptyPacketDataFormat


class ReadSensorRegister(PMW3816andPMW3826):
    """
    Define ``ReadSensorRegister`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Register Address              8
    Padding                       16
    ============================  ==========
    """

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        REGISTER_ADDRESS = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
        PADDING = REGISTER_ADDRESS - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        REGISTER_ADDRESS = 0x8
        PADDING = 0x10
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.REGISTER_ADDRESS, length=LEN.REGISTER_ADDRESS,
                 title="RegisterAddress", name="register_address",
                 checks=(CheckHexList(LEN.REGISTER_ADDRESS // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, register_address, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: Register Address
        :type register_address: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ReadSensorRegisterResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.register_address = register_address
    # end def __init__
# end class ReadSensorRegister


class WriteSensorRegister(PMW3816andPMW3826):
    """
    Define ``WriteSensorRegister`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Register Address              8
    Register Value                8
    Padding                       8
    ============================  ==========
    """

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        REGISTER_ADDRESS = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
        REGISTER_VALUE = REGISTER_ADDRESS - 1
        PADDING = REGISTER_VALUE - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        REGISTER_ADDRESS = 0x8
        REGISTER_VALUE = 0x8
        PADDING = 0x8
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.REGISTER_ADDRESS, length=LEN.REGISTER_ADDRESS,
                 title="RegisterAddress", name="register_address",
                 checks=(CheckHexList(LEN.REGISTER_ADDRESS // 8),
                         CheckByte(),)),
        BitField(fid=FID.REGISTER_VALUE, length=LEN.REGISTER_VALUE,
                 title="RegisterValue", name="register_value",
                 checks=(CheckHexList(LEN.REGISTER_VALUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, register_address, register_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_address: Register Address
        :type register_address: ``HexList``
        :param register_value: Register Value
        :type register_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=WriteSensorRegisterResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.register_address = register_address
        self.register_value = register_value
    # end def __init__
# end class WriteSensorRegister


class ResetSensor(ShortEmptyPacketDataFormat):
    """
    Define ``ResetSensor`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ResetSensorResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ResetSensor


class ShutdownSensor(ShortEmptyPacketDataFormat):
    """
    Define ``ShutdownSensor`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ShutdownSensorResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ShutdownSensor


class TrackingTest(PMW3816andPMW3826):
    """
    Define ``TrackingTest`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Count                         16
    Padding                       8
    ============================  ==========
    """

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        COUNT = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
        PADDING = COUNT - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        COUNT = 0x10
        PADDING = 0x8
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.COUNT, length=LEN.COUNT,
                 title="Count", name="count",
                 checks=(CheckHexList(LEN.COUNT // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNT) - 1),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, count, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param count: Count
        :type count: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=TrackingTestResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
        self.count = count
    # end def __init__
# end class TrackingTest


class FrameCaptureV0(ShortEmptyPacketDataFormat):
    """
    Define ``FrameCaptureV0`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=FrameCaptureResponseV0.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class FrameCaptureV0


class GetStrapDataV1(ShortEmptyPacketDataFormat):
    """
    Define ``GetStrapDataV1`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=GetStrapDataResponseV1.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class GetStrapDataV1


class ContinuousPower(ShortEmptyPacketDataFormat):
    """
    Define ``ContinuousPower`` implementation class
    """

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=ContinuousPowerResponse.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_SHORT,
                         **kwargs)
    # end def __init__
# end class ContinuousPower


class ReadSensorRegisterResponse(PMW3816andPMW3826):
    """
    Define ``ReadSensorRegisterResponse`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Register Value                8
    Padding                       120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ReadSensorRegister,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        REGISTER_VALUE = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
        PADDING = REGISTER_VALUE - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        REGISTER_VALUE = 0x8
        PADDING = 0x78
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.REGISTER_VALUE, length=LEN.REGISTER_VALUE,
                 title="RegisterValue", name="register_value",
                 checks=(CheckHexList(LEN.REGISTER_VALUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PADDING, length=LEN.PADDING,
                 title="Padding", name="padding",
                 checks=(CheckHexList(LEN.PADDING // 8), CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),
    )

    def __init__(self, device_index, feature_index, register_value, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param register_value: Register Value
        :type register_value: ``HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.register_value = register_value
    # end def __init__
# end class ReadSensorRegisterResponse


class WriteSensorRegisterResponse(LongEmptyPacketDataFormat):
    """
    Define ``WriteSensorRegisterResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (WriteSensorRegister,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class WriteSensorRegisterResponse


class ResetSensorResponse(LongEmptyPacketDataFormat):
    """
    Define ``ResetSensorResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ResetSensor,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 2

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ResetSensorResponse


class ShutdownSensorResponse(LongEmptyPacketDataFormat):
    """
    Define ``ShutdownSensorResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ShutdownSensor,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 3

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ShutdownSensorResponse


class TrackingTestResponse(LongEmptyPacketDataFormat):
    """
    Define ``TrackingTestResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (TrackingTest,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 4

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class TrackingTestResponse


class FrameCaptureResponseV0(LongEmptyPacketDataFormat):
    """
    Define ``FrameCaptureResponseV0`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (FrameCaptureV0,)
    VERSION = (0,)
    FUNCTION_INDEX = 5

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class FrameCaptureResponseV0


class GetStrapDataResponseV1(PMW3816andPMW3826):
    """
    Define ``GetStrapDataResponseV1`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Reserved                      6
    Sensor                        2
    Strap Measurement X           120
    ============================  ==========
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (GetStrapDataV1,)
    VERSION = (1,)
    FUNCTION_INDEX = 5

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        RESERVED = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
        SENSOR = RESERVED - 1
        STRAP_MEASUREMENT_X = SENSOR - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        RESERVED = 0x6
        SENSOR = 0x2
        STRAP_MEASUREMENT_X = 0x78
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckInt(0, pow(2, LEN.RESERVED) - 1),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),
        BitField(fid=FID.SENSOR, length=LEN.SENSOR,
                 title="Sensor", name="sensor",
                 checks=(CheckInt(0, pow(2, LEN.SENSOR) - 1),)),
        BitField(fid=FID.STRAP_MEASUREMENT_X, length=LEN.STRAP_MEASUREMENT_X,
                 title="StrapMeasurementX", name="strap_measurement_x",
                 checks=(CheckHexList(LEN.STRAP_MEASUREMENT_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.STRAP_MEASUREMENT_X) - 1),)),
    )

    def __init__(self, device_index, feature_index, sensor, strap_measurement_x, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param sensor: Sensor
        :type sensor: ``int | HexList``
        :param strap_measurement_x: Strap Measurement X
        :type strap_measurement_x: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.sensor = sensor
        self.strap_measurement_x = strap_measurement_x
    # end def __init__
# end class GetStrapDataResponseV1


class ContinuousPowerResponse(LongEmptyPacketDataFormat):
    """
    Define ``ContinuousPowerResponse`` implementation class
    """
    MSG_TYPE = TYPE.RESPONSE
    REQUEST_LIST = (ContinuousPower,)
    VERSION = (0, 1,)
    FUNCTION_INDEX = 6

    def __init__(self, device_index, feature_index, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
    # end def __init__
# end class ContinuousPowerResponse


class TrackingReportEvent(PMW3816andPMW3826):
    """
    Define ``TrackingReportEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Delta X                       16
    Delta Y                       16
    Surface Quality Value         8
    Pixel Sum                     8
    Maximum Pixel                 8
    Minimum Pixel                 8
    Shutter                       16
    Counter                       16
    Reserved                      8
    SQUAL Average                 8
    Shutter Average               16
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 0

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        DELTA_X = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
        DELTA_Y = DELTA_X - 1
        SURFACE_QUALITY_VALUE = DELTA_Y - 1
        PIXEL_SUM = SURFACE_QUALITY_VALUE - 1
        MAXIMUM_PIXEL = PIXEL_SUM - 1
        MINIMUM_PIXEL = MAXIMUM_PIXEL - 1
        SHUTTER = MINIMUM_PIXEL - 1
        COUNTER = SHUTTER - 1
        RESERVED = COUNTER - 1
        SQUAL_AVERAGE = RESERVED - 1
        SHUTTER_AVERAGE = SQUAL_AVERAGE - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        DELTA_X = 0x10
        DELTA_Y = 0x10
        SURFACE_QUALITY_VALUE = 0x8
        PIXEL_SUM = 0x8
        MAXIMUM_PIXEL = 0x8
        MINIMUM_PIXEL = 0x8
        SHUTTER = 0x10
        COUNTER = 0x10
        RESERVED = 0x8
        SQUAL_AVERAGE = 0x8
        SHUTTER_AVERAGE = 0x10
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.DELTA_X, length=LEN.DELTA_X,
                 title="DeltaX", name="delta_x",
                 checks=(CheckHexList(LEN.DELTA_X // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DELTA_X) - 1),)),
        BitField(fid=FID.DELTA_Y, length=LEN.DELTA_Y,
                 title="DeltaY", name="delta_y",
                 checks=(CheckHexList(LEN.DELTA_Y // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.DELTA_Y) - 1),)),
        BitField(fid=FID.SURFACE_QUALITY_VALUE, length=LEN.SURFACE_QUALITY_VALUE,
                 title="SurfaceQualityValue", name="surface_quality_value",
                 checks=(CheckHexList(LEN.SURFACE_QUALITY_VALUE // 8),
                         CheckByte(),)),
        BitField(fid=FID.PIXEL_SUM, length=LEN.PIXEL_SUM,
                 title="PixelSum", name="pixel_sum",
                 checks=(CheckHexList(LEN.PIXEL_SUM // 8),
                         CheckByte(),)),
        BitField(fid=FID.MAXIMUM_PIXEL, length=LEN.MAXIMUM_PIXEL,
                 title="MaximumPixel", name="maximum_pixel",
                 checks=(CheckHexList(LEN.MAXIMUM_PIXEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.MINIMUM_PIXEL, length=LEN.MINIMUM_PIXEL,
                 title="MinimumPixel", name="minimum_pixel",
                 checks=(CheckHexList(LEN.MINIMUM_PIXEL // 8),
                         CheckByte(),)),
        BitField(fid=FID.SHUTTER, length=LEN.SHUTTER,
                 title="Shutter", name="shutter",
                 checks=(CheckHexList(LEN.SHUTTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SHUTTER) - 1),)),
        BitField(fid=FID.COUNTER, length=LEN.COUNTER,
                 title="Counter", name="counter",
                 checks=(CheckHexList(LEN.COUNTER // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.COUNTER) - 1),)),
        BitField(fid=FID.RESERVED, length=LEN.RESERVED,
                 title="Reserved", name="reserved",
                 checks=(CheckHexList(LEN.RESERVED // 8),
                         CheckByte(),),
                 default_value=PMW3816andPMW3826.DEFAULT.PADDING),
        BitField(fid=FID.SQUAL_AVERAGE, length=LEN.SQUAL_AVERAGE,
                 title="SqualAverage", name="squal_average",
                 checks=(CheckHexList(LEN.SQUAL_AVERAGE // 8),
                         CheckByte(),)),
        BitField(fid=FID.SHUTTER_AVERAGE, length=LEN.SHUTTER_AVERAGE,
                 title="ShutterAverage", name="shutter_average",
                 checks=(CheckHexList(LEN.SHUTTER_AVERAGE // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.SHUTTER_AVERAGE) - 1),)),
    )

    def __init__(self, device_index, feature_index, delta_x, delta_y, surface_quality_value, pixel_sum, maximum_pixel,
                 minimum_pixel, shutter, counter, squal_average, shutter_average, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param delta_x: Delta X
        :type delta_x: ``int | HexList``
        :param delta_y: Delta Y
        :type delta_y: ``int | HexList``
        :param surface_quality_value: Surface Quality Value
        :type surface_quality_value: ``int | HexList``
        :param pixel_sum: Pixel Sum
        :type pixel_sum: ``int | HexList``
        :param maximum_pixel: Maximum Pixel
        :type maximum_pixel: ``int | HexList``
        :param minimum_pixel: Minimum Pixel
        :type minimum_pixel: ``int | HexList``
        :param shutter: Shutter
        :type shutter: ``int | HexList``
        :param counter: Counter
        :type counter: ``int | HexList``
        :param squal_average: SQUAL Average
        :type squal_average: ``int | HexList``
        :param shutter_average: Shutter Average
        :type shutter_average: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.delta_x = delta_x
        self.delta_y = delta_y
        self.surface_quality_value = surface_quality_value
        self.pixel_sum = pixel_sum
        self.maximum_pixel = maximum_pixel
        self.minimum_pixel = minimum_pixel
        self.shutter = shutter
        self.counter = counter
        self.squal_average = squal_average
        self.shutter_average = shutter_average
    # end def __init__
# end class TrackingReportEvent


class FrameCaptureReportEvent(PMW3816andPMW3826):
    """
    Define ``FrameCaptureReportEvent`` implementation class

    Format:
    ============================  ==========
    Name                          Bit count
    ============================  ==========
    Frame Data                    128
    ============================  ==========
    """
    MSG_TYPE = TYPE.EVENT
    VERSION = (0, 1,)
    FUNCTION_INDEX = 1

    class FID(PMW3816andPMW3826.FID):
        # See ``PMW3816andPMW3826.FID``
        FRAME_DATA = PMW3816andPMW3826.FID.SOFTWARE_ID - 1
    # end class FID

    class LEN(PMW3816andPMW3826.LEN):
        # See ``PMW3816andPMW3826.LEN``
        FRAME_DATA = 0x80
    # end class LEN

    FIELDS = PMW3816andPMW3826.FIELDS + (
        BitField(fid=FID.FRAME_DATA, length=LEN.FRAME_DATA,
                 title="FrameData", name="frame_data",
                 checks=(CheckHexList(LEN.FRAME_DATA // 8),
                         CheckInt(min_value=0, max_value=pow(2, LEN.FRAME_DATA) - 1),)),
    )

    def __init__(self, device_index, feature_index, frame_data, **kwargs):
        """
        :param device_index: Device index
        :type device_index: ``int | HexList``
        :param feature_index: Feature index
        :type feature_index: ``int | HexList``
        :param frame_data: Frame Data
        :type frame_data: ``int | HexList``
        :param kwargs: Potential future parameters
        :type kwargs: ``int | HexList | dict``
        """
        super().__init__(device_index=device_index, feature_index=feature_index,
                         function_index=self.FUNCTION_INDEX,
                         report_id=self.DEFAULT.REPORT_ID_LONG,
                         **kwargs)
        self.frame_data = frame_data
    # end def __init__
# end class FrameCaptureReportEvent

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
