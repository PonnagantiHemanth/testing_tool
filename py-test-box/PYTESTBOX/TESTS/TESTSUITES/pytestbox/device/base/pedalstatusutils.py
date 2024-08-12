#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.base.pedalstatusutils
:brief: Helpers for ``PedalStatus`` feature
:author: Vasudev Mukkamala <vmukkamala@logitech.com>
:date: 2021/02/24
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatus
from pyhid.hidpp.features.gaming.pedalstatus import PedalStatusFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class PedalStatusTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``PedalStatus`` feature
    """

    class GetPedalStatusResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Check ``GetPedalStatus`` response
        """

        @classmethod
        def get_default_check_map(cls, test_case):
            """
            Get the default check methods and expected values for the ``GetPedalStatusResponse`` API

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "entry_count": (cls.check_entry_count,
                                test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_TotalPedalsCount),
                "entry_1_port_type": (cls.check_entry_1_port_type,
                                      test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_PortType[0]),
                "entry_1_port_status": (cls.check_entry_1_port_status,
                                        test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_PortStatus[0]),
                "entry_2_port_type": (cls.check_entry_2_port_type,
                                      test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_PortType[1]),
                "entry_2_port_status": (cls.check_entry_2_port_status,
                                        test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_PortStatus[1]),
                "entry_3_port_type": (cls.check_entry_3_port_type,
                                      test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_PortType[2]),
                "entry_3_port_status": (cls.check_entry_3_port_status,
                                        test_case.f.PRODUCT.FEATURES.GAMING.PEDAL_STATUS.F_PortStatus[2])
            }
        # end def get_default_check_map

        @staticmethod
        def check_entry_count(test_case, response, expected):
            """
            Check entry_count field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_count)),
                msg=f"The entry_count parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_count})")
        # end def check_entry_count

        @staticmethod
        def check_entry_1_port_type(test_case, response, expected):
            """
            Check entry_1_port_type field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_1_port_type)),
                msg=f"The entry_1_port_type parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_1_port_type})")
        # end def check_entry_1_port_type

        @staticmethod
        def check_entry_1_port_status(test_case, response, expected):
            """
            Check entry_1_port_status field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_1_port_status)),
                msg=f"The entry_1_port_status parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_1_port_status})")
        # end def check_entry_1_port_status

        @staticmethod
        def check_entry_2_port_type(test_case, response, expected):
            """
            Check entry_2_port_type field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_2_port_type)),
                msg=f"The entry_2_port_type parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_2_port_type})")
        # end def check_entry_2_port_type

        @staticmethod
        def check_entry_2_port_status(test_case, response, expected):
            """
            Check entry_2_port_status field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_2_port_status)),
                msg=f"The entry_2_port_status parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_2_port_status})")
        # end def check_entry_2_port_status

        @staticmethod
        def check_entry_3_port_type(test_case, response, expected):
            """
            Check entry_3_port_type field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_3_port_type)),
                msg=f"The entry_3_port_type parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_3_port_type})")
        # end def check_entry_3_port_type

        @staticmethod
        def check_entry_3_port_status(test_case, response, expected):
            """
            Check entry_3_port_status field in response

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param response: GetPedalStatusResponse to check
            :type response: ``GetPedalStatusResponse``
            :param expected: Expected value
            :type expected: ``int`` or ``HexList``
            """
            test_case.assertEqual(
                expected=int(Numeral(expected)),
                obtained=int(Numeral(response.entry_3_port_status)),
                msg=f"The entry_3_port_status parameter differs "
                    f"(expected:{expected}, obtained:{response.entry_3_port_status})")
        # end def check_entry_3_port_status
    # end class GetPedalStatusResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_parameters(cls, test_case, feature_id=PedalStatus.FEATURE_ID, factory=PedalStatusFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_pedal_status(cls, test_case, device_index=None, port_index=None):
            """
            Process ``GetPedalStatus``

            :param test_case: Current test case
            :type test_case: ``BaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int`` or ``HexList``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int`` or ``HexList``

            :return: GetPedalStatusResponse
            :rtype: ``GetPedalStatusResponse``
            """
            feature_8135_index, feature_8135, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_8135.get_pedal_status_cls(
                device_index, feature_8135_index)
            response = test_case.send_report_wait_response(
                report=report,
                response_queue=test_case.hidDispatcher.gaming_message_queue,
                response_class_type=test_case.feature_8135.get_pedal_status_response_cls)
            return response
        # end def get_pedal_status
    # end class HIDppHelper
# end class PedalStatusTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
