#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.combinedpedalsutils
:brief: Helpers for ``CombinedPedals`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/25
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedals
from pyhid.hidpp.features.gaming.combinedpedals import CombinedPedalsFactory
from pylibrary.tools.hexlist import HexList
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class CombinedPedalsTestUtils(DeviceBaseTestUtils):
    """
    This class provides helpers for common checks on ``CombinedPedals`` feature
    """
    class CombinedPedalsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check ``GetCombinedPedals`` & ``SetCombinedPedals`` response
        """
        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetCombinedPedalsResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "combined_pedals_enabled": (cls.check_combined_pedals_enabled, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_combined_pedals_enabled(test_case, response, expected):
            """
            Check combined_pedals_enabled field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetCombinedPedalsResponse to check
            :type response: ``GetCombinedPedalsResponse``
            :param expected: Expected value
            :type expected: ``bool`` or ``HexList``
            """
            test_case.assertEqual(
                expected=HexList(expected),
                obtained=HexList(response.combined_pedals_enabled),
                msg=f"The combined_pedals_enabled parameter differs "
                    f"(expected:{expected}, obtained:{response.combined_pedals_enabled})")
        # end def check_combined_pedals_enabled
    # end class CombinedPedalsResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=CombinedPedals.FEATURE_ID, factory=CombinedPedalsFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_combined_pedals(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetCombinedPedals``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetCombinedPedalsResponse
            :rtype: ``GetCombinedPedalsResponse``
            """
            feature_80d0_index, feature_80d0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80d0.get_combined_pedals_cls(
                device_index, feature_80d0_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_80d0.get_combined_pedals_response_cls)
            return response
        # end def get_combined_pedals

        @classmethod
        def set_combined_pedals(cls, test_case, enable_combined_pedals, device_index=None, port_index=None):
            """
            Process ``SetCombinedPedals``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param enable_combined_pedals: If set, then the device starts reporting combined pedals.
                                           If reset, then the device starts reporting separate pedals
            :type enable_combined_pedals: ``bool`` or ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: SetCombinedPedalsResponse
            :rtype: ``SetCombinedPedalsResponse``
            """
            feature_80d0_index, feature_80d0, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_80d0.set_combined_pedals_cls(
                device_index, feature_80d0_index,
                enable_combined_pedals=enable_combined_pedals)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_80d0.set_combined_pedals_response_cls)
            return response
        # end def set_combined_pedals

        @classmethod
        def combined_pedals_changed_event(cls, test_case):
            """
            Process ``CombinedPedalsChangedEvent``: get notification from event queue

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: CombinedPedalsChangedEvent
            :rtype: ``CombinedPedalsChangedEvent``
            """
            return test_case.getMessage(queue=test_case.hidDispatcher.event_message_queue,
                                        class_type=test_case.feature_80d0.combined_pedals_changed_event_cls)
        # end def combined_pedals_changed_event
    # end class HIDppHelper
# end class CombinedPedalsTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
