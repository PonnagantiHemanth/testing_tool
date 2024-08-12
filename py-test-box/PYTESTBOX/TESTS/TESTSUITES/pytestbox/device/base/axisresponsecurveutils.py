#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.axisresponsecurveutils
:brief: Helpers for ``AxisResponseCurve`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/03/12
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurve
from pyhid.hidpp.features.gaming.axisresponsecurve import AxisResponseCurveFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
NVS_EVENT_TIMEOUT = 5
# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------


class AxisResponseCurveTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``AxisResponseCurve`` feature
    """

    class MixedInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check common response fields using ``MixedInfoResponseChecker``
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "axis_index": (cls.check_axis_index, None),
            }
        # end def get_default_check_map

        @staticmethod
        def check_axis_index(test_case, response, expected):
            """
            Check axis_index field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.axis_index)),
                msg=f"The axis_index parameter differs "
                    f"(expected:{expected}, obtained:{response.axis_index})")
            # end def check_axis_index
    # end class MixedInfoResponseChecker

    class GetInfoResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetInfo`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            config = test_case.f.PRODUCT.FEATURES.GAMING.AXIS_RESPONSE_CURVE
            version = test_case.config_manager.get_feature_version(config)
            check_map = {
                "axis_count": (
                    cls.check_axis_count, HexList(Numeral(test_case.config.F_AxisCount))),
                "max_get_point_count": (
                    cls.check_max_get_point_count, HexList(Numeral(test_case.config.F_MaxGetPointCount))),
                "max_set_point_count": (
                    cls.check_max_set_point_count, HexList(Numeral(test_case.config.F_MaxSetPointCount)))
            }

            if version >= cls.Version.ONE:
                check_map.update({
                    "reserved": (cls.check_reserved, 0),
                    "capabilities": (cls.check_capabilities, Numeral(test_case.config.F_Capabilities)),
                })
            # end if
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_axis_count(test_case, response, expected):
            """
            Check axis_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.axis_count)),
                msg=f"The axis_count parameter differs "
                    f"(expected:{expected}, obtained:{response.axis_count})")
        # end def check_axis_count

        @staticmethod
        def check_max_get_point_count(test_case, response, expected):
            """
            Check max_get_point_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.max_get_point_count)),
                msg=f"The max_get_point_count parameter differs "
                    f"(expected:{expected}, obtained:{response.max_get_point_count})")
        # end def check_max_get_point_count

        @staticmethod
        def check_max_set_point_count(test_case, response, expected):
            """
            Check max_set_point_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.max_set_point_count)),
                msg=f"The max_set_point_count parameter differs "
                    f"(expected:{expected}, obtained:{response.max_set_point_count})")
        # end def check_max_set_point_count

        @staticmethod
        def check_reserved(test_case, response, expected):
            """
            Check reserved bits value

            :param test_case: The current test case
            :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
            :param response: Obtained message
            :type response: ``BitFieldContainerMixin``
            :param expected: StartSession flags reserved bits value
            :type expected: ``int | HexList``
            """

            test_case.assertEqual(obtained=int(response.reserved),
                                  expected=int(expected),
                                  msg="The reserved bits are not as expected")
        # end def check_reserved

        @staticmethod
        def check_capabilities(test_case, response, expected):
            """
            Check capabilities field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert capabilities that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The capabilities shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.capabilities)),
                msg="The capabilities parameter differs from the one expected")
        # end def check_capabilities

    # end class GetInfoResponseChecker

    class GetAxisInfoResponseChecker(MixedInfoResponseChecker):
        """
        Check ``GetAxisInfo`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetAxisInfoResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            check_map = super().get_default_check_map(test_case)
            check_map.update({
                "hid_usage_page": (cls.check_hid_usage_page, HexList(test_case.config.F_HidUsagePage)),
                "hid_usage": (cls.check_hid_usage, HexList(test_case.config.F_HidUsage[0])),
                "axis_resolution": (cls.check_axis_resolution, HexList(Numeral(test_case.config.F_AxisResolution))),
                "active_point_count": (cls.check_active_point_count,
                                       HexList(Numeral(test_case.config.F_ActivePointCount))),
                "max_point_count": (cls.check_max_point_count, HexList(Numeral(test_case.config.F_MaxPointCount))),
                "properties": (cls.check_properties, HexList(Numeral(test_case.config.F_Properties))),
            })
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_hid_usage_page(test_case, response, expected):
            """
            Check hid_usage_page field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.hid_usage_page)),
                msg=f"The hid_usage_page parameter differs "
                    f"(expected:{expected}, obtained:{response.hid_usage_page})")
        # end def check_hid_usage_page

        @staticmethod
        def check_hid_usage(test_case, response, expected):
            """
            Check hid_usage field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.hid_usage)),
                msg=f"The hid_usage parameter differs "
                    f"(expected:{expected}, obtained:{response.hid_usage})")
        # end def check_hid_usage

        @staticmethod
        def check_axis_resolution(test_case, response, expected):
            """
            Check axis_resolution field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.axis_resolution)),
                msg=f"The axis_resolution parameter differs "
                    f"(expected:{expected}, obtained:{response.axis_resolution})")
        # end def check_axis_resolution

        @staticmethod
        def check_active_point_count(test_case, response, expected):
            """
            Check active_point_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.active_point_count)),
                msg=f"The active_point_count parameter differs "
                    f"(expected:{expected}, obtained:{response.active_point_count})")
        # end def check_active_point_count

        @staticmethod
        def check_max_point_count(test_case, response, expected):
            """
            Check max_point_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.max_point_count)),
                msg=f"The max_point_count parameter differs "
                    f"(expected:{expected}, obtained:{response.max_point_count})")
        # end def check_max_point_count

        @staticmethod
        def check_properties(test_case, response, expected):
            """
            Check properties field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisInfoResponse to check
            :type response: ``GetAxisInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.properties)),
                msg=f"The properties parameter differs "
                    f"(expected:{expected}, obtained:{response.properties})")
        # end def check_properties
    # end class GetAxisInfoResponseChecker

    class GetAxisPointsResponseChecker(MixedInfoResponseChecker):
        """
        Check ``GetAxisPoints`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetAxisPointsResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            check_map = super().get_default_check_map(test_case)
            check_map.update({
                "point_index": (cls.check_point_index, None),
                "point_count": (cls.check_point_count, None),
                "axis_points": (cls.check_axis_points, None)
            })
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_point_index(test_case, response, expected):
            """
            Check point_index field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisPointsResponse to check
            :type response: ``GetAxisPointsResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.point_index)),
                msg=f"The point_index parameter differs "
                    f"(expected:{expected}, obtained:{response.point_index})")
        # end def check_point_index

        @staticmethod
        def check_point_count(test_case, response, expected):
            """
            Check point_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisPointsResponse to check
            :type response: ``GetAxisPointsResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.point_count)),
                msg=f"The point_count parameter differs "
                    f"(expected:{expected}, obtained:{response.point_count})")
        # end def check_point_count

        @staticmethod
        def check_axis_points(test_case, response, expected):
            """
            Check axis_points field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetAxisPointsResponse to check
            :type response: ``GetAxisPointsResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.axis_points)),
                msg=f"The axis_points parameter differs "
                    f"(expected:{expected}, obtained:{response.axis_points})")
        # end def check_axis_points
    # end class GetAxisPointsResponseChecker

    class StopUpdateResponseChecker(MixedInfoResponseChecker):
        """
        Check ``StopUpdate`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``StopUpdateResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            check_map = super().get_default_check_map(test_case)
            check_map.update({
                "status": (cls.check_status, HexList(test_case.config.F_Status)),
                "active_point_count": (cls.check_active_point_count, HexList(test_case.config.F_ActivePointCount)),
            })
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_status(test_case, response, expected):
            """
            Check status field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: StopUpdateResponse to check
            :type response: ``StopUpdateResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.status)),
                msg=f"The status parameter differs "
                    f"(expected:{expected}, obtained:{response.status})")
        # end def check_status

        @staticmethod
        def check_active_point_count(test_case, response, expected):
            """
            Check active_point_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: StopUpdateResponse to check
            :type response: ``StopUpdateResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.active_point_count)),
                msg=f"The active_point_count parameter differs "
                    f"(expected:{expected}, obtained:{response.active_point_count})")
        # end def check_active_point_count
    # end class StopUpdateResponseChecker

    class GetCalculatedValueResponseChecker(MixedInfoResponseChecker):
        """
        Check ``GetCalculatedValue`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCalculatedValueResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            check_map = super().get_default_check_map(test_case)
            check_map.update({
                "input_value": (cls.check_input_value, None),
                "calculated_value": (cls.check_calculated_value, None),
            })
            return check_map
        # end def get_default_check_map

        @staticmethod
        def check_input_value(test_case, response, expected):
            """
            Check input_value field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCalculatedValueResponse to check
            :type response: ``GetCalculatedValueResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.input_value)),
                msg=f"The input_value parameter differs "
                    f"(expected:{expected}, obtained:{response.input_value})")
        # end def check_input_value

        @staticmethod
        def check_calculated_value(test_case, response, expected):
            """
            Check calculated_value field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCalculatedValueResponse to check
            :type response: ``GetCalculatedValueResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.calculated_value)),
                msg=f"The calculated_value parameter differs "
                    f"(expected:{expected}, obtained:{response.calculated_value})")
        # end def check_calculated_value
    # end class GetCalculatedValueResponseChecker

    class SaveCompleteEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``SaveCompleteEvent``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.AXIS_RESPONSE_CURVE
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ONE:
                return {
                    "axis_index": (cls.check_axis_index, None),
                    "status": (cls.check_status, None)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_axis_index(test_case, event, expected):
            """
            Check axis_index field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: SaveCompleteEvent to check
            :type event: ``SaveCompleteEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert axis_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The axis_index shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(event.axis_index)),
                msg="The axis_index parameter differs from the one expected")
        # end def check_axis_index

        @staticmethod
        def check_status(test_case, event, expected):
            """
            Check status field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: SaveCompleteEvent to check
            :type event: ``SaveCompleteEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The status shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(event.status)),
                msg="The status parameter differs from the one expected")
        # end def check_status
    # end class SaveCompleteEventChecker

    class ReloadCompleteEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``ReloadCompleteEvent``
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
            config = test_case.f.PRODUCT.FEATURES.GAMING.AXIS_RESPONSE_CURVE
            version = test_case.config_manager.get_feature_version(config)
            if version == cls.Version.ONE:
                return {
                    "axis_index": (cls.check_axis_index, None),
                    "status": (cls.check_status, None)
                }
            # end if
            raise NotImplementedError(f"Version {version} is not implemented")
        # end def get_default_check_map

        @staticmethod
        def check_axis_index(test_case, event, expected):
            """
            Check axis_index field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: ReloadCompleteEvent to check
            :type event: ``ReloadCompleteEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert axis_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The axis_index shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(event.axis_index)),
                msg="The axis_index parameter differs from the one expected")
        # end def check_axis_index

        @staticmethod
        def check_status(test_case, event, expected):
            """
            Check status field in event

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param event: ReloadCompleteEvent to check
            :type event: ``ReloadCompleteEvent``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert status that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The status shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(event.status)),
                msg="The status parameter differs from the one expected")
        # end def check_status
    # end class ReloadCompleteEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=AxisResponseCurve.FEATURE_ID, factory=AxisResponseCurveFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_info(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetInfo``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetInfoResponse
            :rtype: ``GetInfoResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.get_info_cls(
                device_index, feature_80a4_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.get_info_response_cls)
            return response
        # end def get_info

        @classmethod
        def get_axis_info(cls, test_case, axis_index, device_index=None, port_index=None):
            """
            Process ``GetAxisInfo``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param axis_index: The index of the axis
            :type axis_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetAxisInfoResponse
            :rtype: ``GetAxisInfoResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.get_axis_info_cls(
                device_index, feature_80a4_index,
                axis_index=HexList(axis_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.get_axis_info_response_cls)
            return response
        # end def get_axis_info

        @classmethod
        def get_axis_points(cls, test_case, axis_index, point_index, point_count, device_index=None, port_index=None):
            """
            Process ``GetAxisPoints``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param axis_index: The index of the axis
            :type axis_index: ``int`` or ``HexList``
            :param point_index: The maximum number of points that the firmware supports for getting axis points
            :type point_index: ``int`` or ``HexList``
            :param point_count: The maximum number of points that the firmware supports for setting axis points
            :type point_count: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetAxisPointsResponse
            :rtype: ``GetAxisPointsResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.get_axis_points_cls(
                device_index, feature_80a4_index,
                axis_index=HexList(axis_index),
                point_index=HexList(point_index),
                point_count=HexList(point_count))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.get_axis_points_response_cls)
            return response
        # end def get_axis_points

        @classmethod
        def start_update(cls, test_case, axis_index, device_index=None, port_index=None):
            """
            Process ``StartUpdate``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param axis_index: The index of the axis
            :type axis_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: StartUpdateResponse
            :rtype: ``StartUpdateResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.start_update_cls(
                device_index, feature_80a4_index,
                axis_index=HexList(axis_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.start_update_response_cls)
            return response
        # end def start_update

        @classmethod
        def set_axis_points(cls, test_case, point_count, axis_points, device_index=None, port_index=None):
            """
            Process ``SetAxisPoints``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param point_count: The number of items contained in the packet
            :type point_count: ``int`` or ``HexList``
            :param axis_points: An array of axisPoints to set
            :type axis_points: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetAxisPointsResponse
            :rtype: ``SetAxisPointsResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.set_axis_points_cls(
                device_index, feature_80a4_index,
                point_count=HexList(point_count),
                axis_points=HexList(axis_points))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.set_axis_points_response_cls)
            return response
        # end def set_axis_points

        @classmethod
        def stop_update(cls, test_case, device_index=None, port_index=None):
            """
            Process ``StopUpdate``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: StopUpdateResponse
            :rtype: ``StopUpdateResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.stop_update_cls(
                device_index, feature_80a4_index)
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.stop_update_response_cls)
            return response
        # end def stop_update

        @classmethod
        def reset_axis(cls, test_case, axis_index, device_index=None, port_index=None):
            """
            Process ``ResetAxis``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param axis_index: The index of the axis
            :type axis_index: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: ResetAxisResponse
            :rtype: ``ResetAxisResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.reset_axis_cls(
                device_index, feature_80a4_index,
                axis_index=HexList(axis_index))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.reset_axis_response_cls)
            return response
        # end def reset_axis

        @classmethod
        def get_calculated_value(cls, test_case, axis_index, input_value, device_index=None, port_index=None):
            """
            Process ``GetCalculatedValue``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param axis_index: The index of the axis
            :type axis_index: ``int`` or ``HexList``
            :param input_value: A value representing a value from the ADC to be put through the curve algorithm
            :type input_value: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetCalculatedValueResponse
            :rtype: ``GetCalculatedValueResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.get_calculated_value_cls(
                device_index, feature_80a4_index,
                axis_index=HexList(axis_index),
                input_value=HexList(input_value))
            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=test_case.feature_80a4.get_calculated_value_response_cls)
            return response
        # end def get_calculated_value

        @classmethod
        def save_to_nvs(cls, test_case, axis_index=None, device_index=None, port_index=None, software_id=None,
                        padding=None):
            """
            Process ``SaveToNVS``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param axis_index: The index of the axis that will be saved - OPTIONAL
            :type axis_index: ``int | HexList | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: SaveToNVSResponse (if not error)
            :rtype: ``SaveToNVSResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.save_to_nvs_cls(
                device_index=device_index,
                feature_index=feature_80a4_index,
                axis_index=HexList(axis_index))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_80a4.save_to_nvs_response_cls)
            return response
        # end def save_to_nvs

        @classmethod
        def reload_from_nvs(cls, test_case, axis_index=None, device_index=None, port_index=None, software_id=None,
                            padding=None):
            """
            Process ``ReloadFromNVS``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param axis_index: The index of the axis that will be reloaded - OPTIONAL
            :type axis_index: ``int | HexList | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param padding: Padding - OPTIONAL
            :type padding: ``int | None``

            :return: ReloadFromNVSResponse (if not error)
            :rtype: ``ReloadFromNVSResponse``
            """
            feature_80a4_index, feature_80a4, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80a4.reload_from_nvs_cls(
                device_index=device_index,
                feature_index=feature_80a4_index,
                axis_index=HexList(axis_index))

            if software_id is not None:
                report.software_id = software_id
            # end if

            if padding is not None:
                report.padding = padding
            # end if

            response = ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.GAMING,
                response_class_type=feature_80a4.reload_from_nvs_response_cls)
            return response
        # end def reload_from_nvs

        @classmethod
        def save_complete_event(
                cls, test_case, timeout=NVS_EVENT_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``SaveCompleteEvent``: get notification from event queue

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

            :return: SaveCompleteEvent
            :rtype: ``SaveCompleteEvent``
            """
            _, feature_80a4, _, _ = cls.get_parameters(test_case)

            response = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_80a4.save_complete_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
            return response
        # end def save_complete_event

        @classmethod
        def reload_complete_event(
                cls, test_case, timeout=NVS_EVENT_TIMEOUT,
                check_first_message=True, allow_no_message=False, skip_error_message=False):
            """
            Process ``ReloadCompleteEvent``: get notification from event queue

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

            :return: ReloadCompleteEvent
            :rtype: ``ReloadCompleteEvent``
            """
            _, feature_80a4, _, _ = cls.get_parameters(test_case)

            response = ChannelUtils.get_only(
                test_case=test_case,
                queue_name=HIDDispatcher.QueueName.EVENT,
                class_type=feature_80a4.reload_complete_event_cls,
                timeout=timeout,
                check_first_message=check_first_message,
                allow_no_message=allow_no_message,
                skip_error_message=skip_error_message)
            return response
        # end def reload_complete_event
    # end class HIDppHelper
# end class AxisResponseCurveTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
