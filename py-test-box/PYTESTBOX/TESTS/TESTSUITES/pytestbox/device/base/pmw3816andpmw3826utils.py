#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.pmw3816andpmw3826utils
:brief: Helpers for ``PMW3816andPMW3826`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2023/01/09
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pychannel.channelinterfaceclasses import BaseCommunicationChannel
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ContinuousPowerResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import FrameCaptureReportEvent
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import FrameCaptureResponseV0
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import GetStrapDataResponseV1
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import PMW3816andPMW3826Factory
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ReadSensorRegisterResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ResetSensorResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import ShutdownSensorResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import TrackingReportEvent
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import TrackingTestResponse
from pyhid.hidpp.features.peripheral.pmw3816andpmw3826 import WriteSensorRegisterResponse
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int
from pylibrary.tools.util import NotImplementedAbstractMethodError
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.spidirectaccessutils import SPI_PERIPHERAL_REGISTER_DICT


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PMW3816andPMW3826TestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``PMW3816andPMW3826`` feature
    """

    class ReadSensorRegisterResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReadSensorRegisterResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "register_value": (
                    cls.check_register_value,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_register_value(test_case, response, expected):
            """
            Check register_value field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="RegisterValue shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.register_value),
                msg="The register_value parameter differs "
                    f"(expected:{expected}, obtained:{response.register_value})")
        # end def check_register_value
    # end class ReadSensorRegisterResponseChecker

    class GetStrapDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetStrapDataResponse``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``

            :raise ``NotImplementedError``: Version that raise an exception
            """
            config = test_case.f.PRODUCT.FEATURES.PERIPHERAL.PMW3816_AND_PMW3826
            test_case.assertFalse(config.F_Version_0, 'The getStrapData method is not available in version 0')
            return {
                "sensor": (
                    cls.check_sensor,
                    None),
                "strap_measurement_x": (
                    cls.check_strap_measurement_x,
                    None),
                "reserved": (
                    cls.check_reserved,
                    0),
            }
            # end if
        # end def get_default_check_map

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetStrapDataResponse to check
            :type response: ``GetStrapDataResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{response.reserved})")
        # end def check_reserved

        @staticmethod
        def check_sensor(test_case, response, expected):
            """
            Check sensor field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetStrapDataResponse to check
            :type response: ``GetStrapDataResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert sensor that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Sensor shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.sensor),
                msg="The sensor parameter differs "
                    f"(expected:{expected}, obtained:{response.sensor})")
        # end def check_sensor

        @staticmethod
        def check_strap_measurement_x(test_case, response, expected):
            """
            Check strap_measurement_x field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetStrapDataResponse to check
            :type response: ``GetStrapDataResponseV1``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert strap_measurement_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="StrapMeasurementX shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.strap_measurement_x),
                msg="The strap_measurement_x parameter differs "
                    f"(expected:{expected}, obtained:{response.strap_measurement_x})")
        # end def check_strap_measurement_x
    # end class GetStrapDataResponseChecker

    class TrackingReportEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``TrackingReportEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "delta_x": (
                    cls.check_delta_x,
                    0),
                "delta_y": (
                    cls.check_delta_y,
                    0),
                "surface_quality_value": (
                    cls.check_surface_quality_value,
                    0),
                "pixel_sum": (
                    cls.check_pixel_sum,
                    0),
                "maximum_pixel": (
                    cls.check_maximum_pixel,
                    0),
                "minimum_pixel": (
                    cls.check_minimum_pixel,
                    0),
                "shutter": (
                    cls.check_shutter,
                    0),
                "counter": (
                    cls.check_counter,
                    0),
                "reserved": (
                    cls.check_reserved,
                    0),
                "squal_average": (
                    cls.check_squal_average,
                    0),
                "shutter_average": (
                    cls.check_shutter_average,
                    0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_delta_x(test_case, event, expected):
            """
            Check delta_x field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert delta_x that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="DeltaX shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.delta_x),
                msg="The delta_x parameter differs "
                    f"(expected:{expected}, obtained:{event.delta_x})")
        # end def check_delta_x

        @staticmethod
        def check_delta_y(test_case, event, expected):
            """
            Check delta_y field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert delta_y that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="DeltaY shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.delta_y),
                msg="The delta_y parameter differs "
                    f"(expected:{expected}, obtained:{event.delta_y})")
        # end def check_delta_y

        @staticmethod
        def check_surface_quality_value(test_case, event, expected):
            """
            Check surface_quality_value field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert surface_quality_value that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="SurfaceQualityValue shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.surface_quality_value),
                msg="The surface_quality_value parameter differs "
                    f"(expected:{expected}, obtained:{event.surface_quality_value})")
        # end def check_surface_quality_value

        @staticmethod
        def check_pixel_sum(test_case, event, expected):
            """
            Check pixel_sum field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert pixel_sum that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="PixelSum shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.pixel_sum),
                msg="The pixel_sum parameter differs "
                    f"(expected:{expected}, obtained:{event.pixel_sum})")
        # end def check_pixel_sum

        @staticmethod
        def check_maximum_pixel(test_case, event, expected):
            """
            Check maximum_pixel field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert maximum_pixel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="MaximumPixel shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.maximum_pixel),
                msg="The maximum_pixel parameter differs "
                    f"(expected:{expected}, obtained:{event.maximum_pixel})")
        # end def check_maximum_pixel

        @staticmethod
        def check_minimum_pixel(test_case, event, expected):
            """
            Check minimum_pixel field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert minimum_pixel that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="MinimumPixel shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.minimum_pixel),
                msg="The minimum_pixel parameter differs "
                    f"(expected:{expected}, obtained:{event.minimum_pixel})")
        # end def check_minimum_pixel

        @staticmethod
        def check_shutter(test_case, event, expected):
            """
            Check shutter field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert shutter that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Shutter shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.shutter),
                msg="The shutter parameter differs "
                    f"(expected:{expected}, obtained:{event.shutter})")
        # end def check_shutter

        @staticmethod
        def check_counter(test_case, event, expected):
            """
            Check counter field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert counter that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Counter shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.counter),
                msg="The counter parameter differs "
                    f"(expected:{expected}, obtained:{event.counter})")
        # end def check_counter

        @staticmethod
        def check_reserved(test_case, event, expected):
            """
            Check reserved field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="Reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.reserved),
                msg="The reserved parameter differs "
                    f"(expected:{expected}, obtained:{event.reserved})")
        # end def check_reserved

        @staticmethod
        def check_squal_average(test_case, event, expected):
            """
            Check squal_average field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert squal_average that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="SQUALAverage shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.squal_average),
                msg="The squal_average parameter differs "
                    f"(expected:{expected}, obtained:{event.squal_average})")
        # end def check_squal_average

        @staticmethod
        def check_shutter_average(test_case, event, expected):
            """
            Check shutter_average field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: TrackingReportEvent to check
            :type event: ``TrackingReportEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert shutter_average that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="ShutterAverage shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.shutter_average),
                msg="The shutter_average parameter differs "
                    f"(expected:{expected}, obtained:{event.shutter_average})")
        # end def check_shutter_average
    # end class TrackingReportEventChecker

    class FrameCaptureReportEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FrameCaptureReportEvent``
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "frame_data": (
                    cls.check_frame_data,
                    None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_frame_data(test_case, event, expected):
            """
            Check frame_data field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: FrameCaptureReportEvent to check
            :type event: ``FrameCaptureReportEventV0``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert frame_data that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="FrameData shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(event.frame_data),
                msg="The frame_data parameter differs "
                    f"(expected:{expected}, obtained:{event.frame_data})")
        # end def check_frame_data
    # end class FrameCaptureReportEventChecker

    class RegisterValueInRangeChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check register value in expected range
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``

            :raise ``NotImplementedAbstractMethodError``: Throws Not Implemented Abstract Method error
            """
            raise NotImplementedAbstractMethodError()
        # end class get_default_check_map

        @classmethod
        def get_check_map(cls, test_case, register_name):
            """
            Get the check methods and expected values

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_name: The name of the register
            :type register_name: ``str``

            :return: Check map
            :rtype: ``dict``
            """
            sensor_map = SPI_PERIPHERAL_REGISTER_DICT[test_case.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName]
            check_full_range = {"register_value": (cls.check_register_value_in_range, HexList(0xFF))}
            check_map = {
                "product_id": {"register_value": (cls.check_register_value,
                                                  HexList(sensor_map["product_id"]["value"]))},
                "revision_id": {"register_value": (cls.check_register_value,
                                                   HexList(sensor_map["revision_id"]["value"]))},
                "motion": {"register_value": (cls.check_motion_register_value,
                                              PMW3816andPMW3826TestUtils.MotionRegister.VALUES)},
                "delta_x_l": check_full_range,
                "delta_x_h": check_full_range,
                "delta_y_l": check_full_range,
                "delta_y_h": check_full_range,
                "squal": check_full_range,
                "pixel_sum": check_full_range,
                "maximum_pixel": check_full_range,
                "minimum_pixel": check_full_range,
                "shutter_lower": check_full_range,
                "shutter_upper": {"register_value": (cls.check_register_value_in_range,
                                                     PMW3816andPMW3826TestUtils.ShutterUpperRegister.MAX_VALUE)},
                "chip_observation": check_full_range,
                "powerup_reset": {"register_value": (cls.check_register_value,
                                                     HexList(0x00))},
                "shutdown": {"register_value": (cls.check_register_value,
                                                HexList(0x00))},
                "burst_motion_read": check_full_range,
                "performance": check_full_range,
                "dpi": check_full_range,
                "pixel_grab": check_full_range,
                "pixel_grab_status": check_full_range,
                "axis_control": {"register_value": (cls.check_axis_control,
                                                    PMW3816andPMW3826TestUtils.AxisControlRegister.VALUES)},
                "inv_product_id": {"register_value": (cls.check_register_value,
                                                      HexList(sensor_map["inv_product_id"]["value"]))},
                "rest1_period_glass": check_full_range,
                "rest1_downshift_glass": check_full_range,
                "run_downshift": check_full_range,
                "rest1_period_nonglass": check_full_range,
                "rest1_downshift_nonglass": check_full_range,
                "rest2_period": check_full_range,
                "rest2_downshift": check_full_range,
                "rest3_period": check_full_range
            }

            return check_map[register_name]
        # end get_check_map

        @classmethod
        def check_motion_register_value(cls, test_case, response, expected):
            """
            Check motion register value is same as expected value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``list[HexList]``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            x = lambda r, pos: "1" if r.testBit(pos) else "0"
            response = response.register_value
            response = HexList("0" + x(response, 7) + x(response, 1) + x(response, 0))
            test_case.assertIn(
                member=response,
                container=expected,
                msg=f"The register_value_parameter {response} "
                    f"is not in expected range {expected}")
        # end check_motion_register_value

        @classmethod
        def check_axis_control(cls, test_case, response, expected):
            """
            Check axis control register value is same as expected value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``list[HexList]``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            x = lambda r, pos: "1" if r.testBit(pos) else "0"
            response = response.register_value
            response = HexList("0" + x(response, 7) + x(response, 6) + x(response, 5))
            test_case.assertIn(
                member=response,
                container=expected,
                msg=f"The register_value_parameter {response} "
                    f"is not in expected range {expected}")
        # end def check_axis-control

        @classmethod
        def check_register_value_in_range(cls, test_case, response, expected):
            """
            Check register value in valid range

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            test_case.assertTrue(
                expr=(to_int(response.register_value) <= to_int(expected)),
                msg=f"The register_value_parameter {response.register_value} "
                    f"is not in expected range {expected}")
        # end def check_register_value_in_range

        @classmethod
        def check_register_value(cls, test_case, response, expected):
            """
            Check register value is same as expected value

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: ReadSensorRegisterResponse to check
            :type response: ``ReadSensorRegisterResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert register_value that raise an exception
            """
            test_case.assertEqual(
                expected=expected,
                obtained=response.register_value,
                msg="The register_value parameter differs "
                    f"(expected:{expected}, obtained:{response.register_value})")
        # end def check_register_value
    # end class RegisterValueInRangeChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):

        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=PMW3816andPMW3826.FEATURE_ID, factory=PMW3816andPMW3826Factory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def read_sensor_register(cls, test_case, register_address, device_index=None, port_index=None,
                                 software_id=None, padding=None, reserved=None):
            """
            Process ``ReadSensorRegister``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_address: Register Address
            :type register_address: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: ReadSensorRegisterResponse
            :rtype: ``ReadSensorRegisterResponse``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.read_sensor_register_cls(
                device_index=device_index,
                feature_index=feature_9001_index,
                register_address=register_address)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.read_sensor_register_response_cls)
            return response
        # end def read_sensor_register

        @classmethod
        def write_sensor_register(cls, test_case, register_address, register_value, device_index=None,
                                  port_index=None, software_id=None, padding=None, reserved=None):
            """
            Process ``WriteSensorRegister``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param register_address: Register Address
            :type register_address: ``HexList``
            :param register_value: Register Value
            :type register_value: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: WriteSensorRegisterResponse
            :rtype: ``WriteSensorRegisterResponse``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.write_sensor_register_cls(
                device_index=device_index,
                feature_index=feature_9001_index,
                register_address=register_address,
                register_value=register_value)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.write_sensor_register_response_cls)
            return response
        # end def write_sensor_register

        @classmethod
        def reset_sensor(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None,
                         reserved=None):
            """
            Process ``ResetSensor``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: ResetSensorResponse
            :rtype: ``ResetSensorResponse``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.reset_sensor_cls(
                device_index=device_index,
                feature_index=feature_9001_index)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.reset_sensor_response_cls)
            return response
        # end def reset_sensor

        @classmethod
        def shutdown_sensor(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None,
                            reserved=None):
            """
            Process ``ShutdownSensor``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: ShutdownSensorResponse
            :rtype: ``ShutdownSensorResponse``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.shutdown_sensor_cls(
                device_index=device_index,
                feature_index=feature_9001_index)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.shutdown_sensor_response_cls)
            return response
        # end def shutdown_sensor

        @classmethod
        def tracking_test(cls, test_case, count, device_index=None, port_index=None, software_id=None, padding=None,
                          reserved=None):
            """
            Process ``TrackingTest``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param count: Count
            :type count: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: TrackingTestResponse
            :rtype: ``TrackingTestResponse``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.tracking_test_cls(
                device_index=device_index,
                feature_index=feature_9001_index,
                count=count)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.tracking_test_response_cls)
            return response
        # end def tracking_test

        @classmethod
        def frame_capture(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None,
                          reserved=None):
            """
            Process ``FrameCapture``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: FrameCaptureResponse
            :rtype: ``FrameCaptureResponseV0``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.frame_capture_cls(
                device_index=device_index,
                feature_index=feature_9001_index)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.frame_capture_response_cls)
            return response
        # end def frame_capture

        @classmethod
        def get_strap_data(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None,
                           reserved=None):
            """
            Process ``GetStrapData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: GetStrapDataResponse
            :rtype: ``GetStrapDataResponseV1``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.get_strap_data_cls(
                device_index=device_index,
                feature_index=feature_9001_index)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.get_strap_data_response_cls)
            return response
        # end def get_strap_data

        @classmethod
        def continuous_power(cls, test_case, device_index=None, port_index=None, software_id=None, padding=None,
                             reserved=None):
            """
            Process ``ContinuousPower``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``
            :param reserved: Reserved - OPTIONAL
            :type reserved: ``int | None``

            :return: ContinuousPowerResponse
            :rtype: ``ContinuousPowerResponse``
            """
            feature_9001_index, feature_9001, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_9001.continuous_power_cls(
                device_index=device_index,
                feature_index=feature_9001_index)
            if software_id is not None:
                report.software_id = software_id
            # end if
            if padding is not None:
                report.padding = padding
            # end if
            if reserved is not None:
                report.reserved = reserved
            # end if
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.PERIPHERAL,
                response_class_type=feature_9001.continuous_power_response_cls)
            return response
        # end def continuous_power

        @classmethod
        def tracking_report_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                  check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``TrackingReportEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: TrackingReportEvent
            :rtype: ``TrackingReportEvent``
            """
            _, feature_9001, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_9001.tracking_report_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def tracking_report_event

        @classmethod
        def frame_capture_report_event(cls, test_case, timeout=BaseCommunicationChannel.GENERIC_GET_TIMEOUT,
                                       check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``FrameCaptureReportEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param timeout: Time to wait for message before raising exception in seconds (0 disable it) - OPTIONAL
            :type timeout: ``float``
            :param check_first_message: Flag to check on the first received message - OPTIONAL
            :type check_first_message: ``bool``
            :param allow_no_message: Flag to raise exception when the requested message in not received - OPTIONAL
            :type allow_no_message: ``bool``
            :param skip_error_message: Flag to skip error catching mechanism - OPTIONAL
            :type skip_error_message: ``bool``

            :return: FrameCaptureReportEvent
            :rtype: ``FrameCaptureReportEvent``
            """
            _, feature_9001, _, _ = cls.get_parameters(test_case)

            return ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_9001.frame_capture_report_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
        # end def frame_capture_report_event
    # end class HIDppHelper

    class PerformanceMode:
        """
        The different operating modes of sensor
        """
        REST_MODE_1 = 0x20
        REST_MODE_2 = 0x40
        REST_MODE_3 = 0x60
        REST_MODES = [REST_MODE_1, REST_MODE_2, REST_MODE_3]
    # end class PerformanceMode

    class MotionRegister:
        """
        The expected values from motion register
        """
        # each value is from bit 7 + bit 1 + bit 0 of motion register response
        VALUES = [HexList("0001"), HexList("0010"), HexList("0011"), HexList("0100")]
    # end class MotionRegister

    class ShutterUpperRegister:
        """
        The Max value from shutter upper register
        """
        MAX_VALUE = HexList(32)
    # end class ShutterUpperRegister

    class AxisControlRegister:
        """
        The expected values from axis direction of sensor reporting
        """
        # each value is from bit 7 + bit 6 + bit 5 of axis control register response
        VALUES = [HexList("0000"), HexList("0001"), HexList("0010"), HexList("0011"), HexList("0100")]
    # end class AxisControlRegister
# end class PMW3816andPMW3826TestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
