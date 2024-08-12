#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.brakeforceutils
:brief: Helpers for ``BrakeForce`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/26
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.gaming.brakeforce import BrakeForce
from pyhid.hidpp.features.gaming.brakeforce import BrakeForceFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class BrakeForceTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``BrakeForce`` feature
    """

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
            maximum_kg_load = test_case.config.F_MaximumKgLoad
            return {
                "maximum_kg_load": (cls.check_maximum_kg_load, maximum_kg_load)
            }
        # end def get_default_check_map

        @staticmethod
        def check_maximum_kg_load(test_case, response, expected):
            """
            Check maximum_kg_load field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetInfoResponse to check
            :type response: ``GetInfoResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            value = int(Numeral(response.maximum_kg_load))
            maximum_kg_load = int(Numeral(expected))
            test_case.assertTrue(expr=(1 <= value <= maximum_kg_load),
                                 msg=f"The maximum_kg_load:{value} is not in range(1, {maximum_kg_load})")
        # end def check_maximum_kg_load
    # end class GetInfoResponseChecker

    class GetMaxLoadPointResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetMaxLoadPoint`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetMaxLoadPointResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "maximum_load_point": (cls.check_maximum_load_point, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_maximum_load_point(test_case, response, expected):
            """
            Check maximum_load_point field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetMaxLoadPointResponse to check
            :type response: ``GetMaxLoadPointResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.maximum_load_point)),
                msg=f"The maximum_load_point parameter differs "
                    f"(expected:{expected}, obtained:{response.maximum_load_point})")
        # end def check_maximum_load_point
    # end class GetMaxLoadPointResponseChecker

    class MaxLoadPointChangedEventChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``MaxLoadPointChangedEvent`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``MaxLoadPointChanged`` Event

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "maximum_load_point": (cls.check_maximum_load_point, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_maximum_load_point(test_case, response, expected):
            """
            Check maximum_load_point field in event

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: MaxLoadPointChangedEventResponse to check
            :type response: ``MaxLoadPointChangedEvent``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.maximum_load_point)),
                msg=f"The maximum_load_point parameter differs "
                    f"(expected:{expected}, obtained:{response.maximum_load_point})")
        # end def check_maximum_load_point
    # end class MaxLoadPointChangedEventChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=BrakeForce.FEATURE_ID, factory=BrakeForceFactory,
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
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetInfoResponse
            :rtype: ``GetInfoResponse``
            """
            feature_8134_index, feature_8134, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8134.get_info_cls(
                device_index, feature_8134_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8134.get_info_response_cls)
            return response
        # end def get_info

        @classmethod
        def get_max_load_point(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetMaxLoadPoint``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: GetMaxLoadPointResponse
            :rtype: ``GetMaxLoadPointResponse``
            """
            feature_8134_index, feature_8134, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8134.get_max_load_point_cls(
                device_index, feature_8134_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8134.get_max_load_point_response_cls)
            return response
        # end def get_max_load_point

        @classmethod
        def set_max_load_point(cls, test_case, maximum_load_point, device_index=None, port_index=None):
            """
            Process ``SetMaxLoadPoint``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param maximum_load_point: Maximum load point value of the loadcell
            :type maximum_load_point: ``int`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``None``

            :return: SetMaxLoadPointResponse
            :rtype: ``SetMaxLoadPointResponse``
            """
            feature_8134_index, feature_8134, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8134.set_max_load_point_cls(
                device_index, feature_8134_index,
                maximum_load_point=HexList(maximum_load_point))
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8134.set_max_load_point_response_cls)
            return response
        # end def set_max_load_point

        @classmethod
        def max_load_point_changed_event(cls, test_case):
            """
            Process ``MaxLoadPointChangedEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: MaxLoadPointChangedEvent
            :rtype: ``MaxLoadPointChangedEvent``
            """
            return test_case.getMessage(queue=test_case.hidDispatcher.event_message_queue,
                                        class_type=test_case.feature_8134.max_load_point_changed_event_cls)
        # end def max_load_point_changed_event
    # end class HIDppHelper
# end class BrakeForceTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
