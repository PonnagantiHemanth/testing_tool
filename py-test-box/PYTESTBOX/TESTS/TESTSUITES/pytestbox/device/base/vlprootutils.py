#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.vlprootutils
:brief: Helpers for ``VLPRoot`` feature
:author: Vinodh Selvaraj <vselvaraj2@logitech.com>
:date: 2023/09/19
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.features.important.vlproot import GetFeatureIndexResponse
from pyhid.vlp.features.important.vlproot import GetPingDataResponse
from pyhid.vlp.features.important.vlproot import GetProtocolCapabilitiesResponse
from pyhid.vlp.features.important.vlproot import VLPRoot
from pyhid.vlp.features.important.vlproot import VLPRootFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import to_int, Numeral
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils

# ----------------------------------------------------------------------------
# Constants
# ----------------------------------------------------------------------------
NOT_HIDDEN = 0
HIDDEN = 1

# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class VLPRootTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``VLPRoot`` feature
    """

    class GetFeatureIndexResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetFeatureIndexResponse``
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
                "vlp_reserved": (cls.check_vlp_reserved, 0),
                "feature_id": (cls.check_feature_id, 0),
                "feature_idx": (cls.check_feature_index, 0),
                "reserved_0": (cls.check_reserved_0, 0),
                "hidden": (cls.check_hidden, 0),
                "reserved_1": (cls.check_reserved_1, 0),
                "feature_version": (cls.check_feature_version, 0),
                "feature_max_memory": (cls.check_feature_max_memory, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_vlp_reserved(test_case, response, expected):
            """
            Check vlp_reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert feature_id that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The vlp_reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(expected),
                obtained=Numeral(response.vlp_reserved),
                msg="The vlp_reserved parameter differs from the one expected")
        # end def check_vlp_reserved

        @staticmethod
        def check_feature_id(test_case, response, expected):
            """
            Check feature_id field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert feature_id that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The feature_id shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(expected),
                obtained=Numeral(response.feature_id),
                msg="The feature_id parameter differs from the one expected")
        # end def check_feature_id

        @staticmethod
        def check_feature_idx(test_case, response, expected):
            """
            Check feature_index field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert feature_index that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The feature_index shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.feature_idx),
                msg="The feature_idx parameter differs from the one expected")
        # end def check_feature_idx

        @staticmethod
        def check_hidden(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(expected,
                msg="The hidden shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(expected=Numeral(expected),
                             obtained=Numeral(response.hidden),
                             msg="The hidden parameter does not match the expected one")
        # end def check_hidden

        @staticmethod
        def check_reserved_0(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_0),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved_0

        @staticmethod
        def check_reserved_1(test_case, response, expected):
            """
            Check reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=to_int(expected),
                obtained=to_int(response.reserved_1),
                msg="The reserved parameter differs from the one expected")
        # end def check_reserved_1

        @staticmethod
        def check_feature_version(test_case, response, expected):
            """
            Check feature_version field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert feature_version that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The feature_version shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.feature_version),
                msg="The feature_version parameter differs from the one expected")
        # end def check_feature_version

        @staticmethod
        def check_feature_max_memory(test_case, response, expected):
            """
            Check feature_max_memory field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIndexResponse to check
            :type response: ``GetFeatureIndexResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert feature_max_memory that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The feature_max_memory shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.feature_max_memory),
                msg="The feature_max_memory parameter differs from the one expected")
        # end def check_feature_max_memory
    # end class GetFeatureIndexResponseChecker

    class GetProtocolCapabilitiesResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetProtocolCapabilitiesResponse``
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
            config = test_case.f.PRODUCT.FEATURES.VLP.IMPORTANT.ROOT
            return {
                "vlp_reserved": (cls.check_vlp_reserved, 0),
                "protocol_major": (cls.check_protocol_major, config.F_ProtocolNumMajor),
                "protocol_minor": (cls.check_protocol_minor, config.F_ProtocolNumMinor),
                "available_total_memory": (cls.check_available_total_memory, config.F_TotalMemory)
            }
        # end def get_default_check_map

        @staticmethod
        def check_vlp_reserved(test_case, response, expected):
            """
            Check vlp_reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetProtocolCapabilitiesResponse to check
            :type response: ``GetProtocolCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert feature_id that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The vlp_reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(expected),
                obtained=Numeral(response.vlp_reserved),
                msg="The vlp_reserved parameter differs from the one expected")
        # end def check_vlp_reserved

        @staticmethod
        def check_protocol_major(test_case, response, expected):
            """
            Check protocol_major field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetProtocolCapabilitiesResponse to check
            :type response: ``GetProtocolCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert protocol_major that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The protocol_major shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.protocol_major),
                msg="The protocol_major parameter differs from the one expected")
        # end def check_protocol_major

        @staticmethod
        def check_protocol_minor(test_case, response, expected):
            """
            Check protocol_minor field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetProtocolCapabilitiesResponse to check
            :type response: ``GetProtocolCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert protocol_minor that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The protocol_minor shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.protocol_minor),
                msg="The protocol_minor parameter differs from the one expected")
        # end def check_protocol_minor

        @staticmethod
        def check_available_total_memory(test_case, response, expected):
            """
            Check available_total_memory field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetProtocolCapabilitiesResponse to check
            :type response: ``GetProtocolCapabilitiesResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert available_total_memory that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The available_total_memory shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.available_total_memory),
                msg="The available_total_memory parameter differs from the one expected")
        # end def check_available_total_memory
    # end class GetProtocolCapabilitiesResponseChecker

    class GetPingDataResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetPingDataResponse``
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
                "vlp_reserved": (cls.check_vlp_reserved, 0),
                "ping_data": (cls.check_ping_data, 0)
            }
        # end def get_default_check_map

        @staticmethod
        def check_vlp_reserved(test_case, response, expected):
            """
            Check vlp_reserved field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetPingDataResponse to check
            :type response: ``GetPingDataResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert feature_id that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The vlp_reserved shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=int(expected),
                obtained=Numeral(response.vlp_reserved),
                msg="The vlp_reserved parameter differs from the one expected")
        # end def check_vlp_reserved

        @staticmethod
        def check_ping_data(test_case, response, expected):
            """
            Check ping_data field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetPingDataResponse to check
            :type response: ``GetPingDataResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert ping_data that raise an exception
            """
            test_case.assertNotNone(
                expected,
                msg="The ping_data shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(
                expected=Numeral(expected),
                obtained=Numeral(response.ping_data),
                msg="The ping_data parameter differs from the one expected")
        # end def check_ping_data
    # end class GetPingDataResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_vlp_parameters(cls, test_case,
                           feature_id=VLPRoot.FEATURE_ID,
                           factory=VLPRootFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_vlp_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_feature_index(cls, test_case, feature_id, device_index=None, port_index=None, software_id=None,
                              vlp_reserved=0, vlp_begin=0, vlp_end=0, vlp_ack=0, vlp_sequence_number=0, report_id=None):
            """
            Process ``GetFeatureIndex``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param feature_id: Feature ID
            :type feature_id: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetProtocolCapabilitiesResponse (if not error)
            :rtype: ``GetProtocolCapabilitiesResponse``
            """
            # noinspection DuplicatedCode
            feature_0102_index, feature_0102, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0102.get_feature_index_cls(
                device_index=device_index,
                feature_index=feature_0102_index,
                feature_id=feature_id,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0102.get_feature_index_response_cls)
        # end def get_feature_index


        @classmethod
        def get_feature_index_and_check_error(
                cls, test_case, error_codes, feature_id, function_index=None, device_index=None,
                port_index=None, vlp_begin=0, vlp_end=0, vlp_ack=0, vlp_sequence_number=0):
            """
            Process ``GetFeatureIndex``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param feature_id: Feature ID
            :type feature_id: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment
            :type vlp_sequence_number: ``int``
            """
            # noinspection DuplicatedCode
            feature_0102_index, feature_0102, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0102.get_feature_index_cls(
                device_index=device_index,
                feature_index=feature_0102_index,
                feature_id=feature_id,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_feature_index_and_check_error

        @classmethod
        def get_protocol_capabilities(cls, test_case, device_index=None, port_index=None, software_id=None,
                                      vlp_reserved=0, vlp_begin=0, vlp_end=0, vlp_ack=0, vlp_sequence_number=0,
                                      report_id=None):
            """
            Process ``GetProtocolCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: VLP Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin - OPTIONAL
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End - OPTIONAL
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment - OPTIONAL
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment - OPTIONAL
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetProtocolCapabilitiesResponse (if not error)
            :rtype: ``GetProtocolCapabilitiesResponse``
            """
            feature_0102_index, feature_0102, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0102.get_protocol_capabilities_cls(
                device_index=device_index,
                feature_index=feature_0102_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0102.get_protocol_capabilities_response_cls)
        # end def get_protocol_capabilities

        @classmethod
        def get_protocol_capabilities_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None,
                vlp_begin=0, vlp_end=0, vlp_ack=0, vlp_sequence_number=0):
            """
            Process ``GetProtocolCapabilities``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment
            :type vlp_sequence_number: ``int``
            """
            feature_0102_index, feature_0102, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0102.get_protocol_capabilities_cls(
                device_index=device_index,
                feature_index=feature_0102_index,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_protocol_capabilities_and_check_error

        @classmethod
        def get_ping_data(cls, test_case, ping_data, device_index=None, port_index=None, software_id=None,
                          vlp_reserved=0, vlp_begin=0, vlp_end=0, vlp_ack=0, vlp_sequence_number=0, report_id=None):
            """
            Process ``GetPingData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param ping_data: Ping Data
            :type ping_data: ``int | HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``
            :param vlp_reserved: VLP Reserved - OPTIONAL
            :type vlp_reserved: ``int | None``
            :param vlp_begin: VLP Begin
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment
            :type vlp_sequence_number: ``int``
            :param report_id: Report ID - OPTIONAL
            :type report_id: ``int | None``

            :return: GetPingDataResponse (if not error)
            :rtype: ``GetPingDataResponse``
            """
            # noinspection DuplicatedCode
            feature_0102_index, feature_0102, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0102.get_ping_data_cls(
                device_index=device_index,
                feature_index=feature_0102_index,
                ping_data=ping_data,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if software_id is not None:
                report.software_id = software_id
            # end if

            if vlp_reserved is not None:
                report.vlp_reserved = vlp_reserved
            # end if

            if report_id is not None:
                report.report_id = report_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0102.get_ping_data_response_cls)
        # end def get_ping_data

        @classmethod
        def get_ping_data_and_check_error(
                cls, test_case, error_codes, ping_data, function_index=None, device_index=None,
                port_index=None, vlp_begin=0, vlp_end=0, vlp_ack=0, vlp_sequence_number=0):
            """
            Process ``GetPingData``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param ping_data: Ping Data
            :type ping_data: ``int | HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param vlp_begin: VLP Begin
            :type vlp_begin: ``int | bool``
            :param vlp_end: VLP End
            :type vlp_end: ``int | bool``
            :param vlp_ack: VLP Acknowledgment
            :type vlp_ack: ``int | bool``
            :param vlp_sequence_number: VLP Acknowledgment
            :type vlp_sequence_number: ``int``
            """
            # noinspection DuplicatedCode
            feature_0102_index, feature_0102, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0102.get_ping_data_cls(
                device_index=device_index,
                feature_index=feature_0102_index,
                ping_data=ping_data,
                vlp_begin=vlp_begin,
                vlp_end=vlp_end,
                vlp_ack=vlp_ack,
                vlp_sequence_number=vlp_sequence_number)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_ping_data_and_check_error
    # end class HIDppHelper
# end class VLPRootTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
