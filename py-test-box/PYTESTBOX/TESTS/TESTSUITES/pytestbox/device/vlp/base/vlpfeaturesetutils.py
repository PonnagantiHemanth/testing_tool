#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:tool: This file has been generated using 'code generator tool version 1.3'
:package: pytestbox.device.base.vlpfeaturesetutils
:brief: Helpers for ``VLPFeatureSet`` feature
:author: Gautham S B <gsb@logitech.com>
:date: 2024/04/23
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.vlp.features.important.vlpfeatureset import GetAllFeatureIDsResponse
from pyhid.vlp.features.important.vlpfeatureset import GetCountResponse
from pyhid.vlp.features.important.vlpfeatureset import GetFeatureIDResponse
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSet
from pyhid.vlp.features.important.vlpfeatureset import VLPFeatureSetFactory
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.vlp.protocol.vlpprotocoltestutils import VlpProtocolTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class VLPFeatureSetTestUtils(DeviceBaseTestUtils):
    """
    Provide helpers for common checks on ``VLPFeatureSet`` feature
    """

    class GetCountResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetCountResponse``
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
            config = test_case.f.PRODUCT.FEATURES.VLP.IMPORTANT.FEATURE_SET
            return {
                "count": (cls.check_count, config.F_FeatureCount)
            }
        # end def get_default_check_map

        @staticmethod
        def check_count(test_case, response, expected):
            """
            Check count field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetCountResponse to check
            :type response: ``GetCountResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert count that raise an exception
            """
            test_case.assertNotNone(expected, msg="The count shall be defined in the DUT settings")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(response.count),
                                  msg="The count parameter differs from the one expected")
        # end def check_count
    # end class GetCountResponseChecker

    class FeatureTypeChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``FeatureType``
        """

        @classmethod
        def get_check_map(cls, feature_hidden):
            """
            Get the default check methods and expected values

            :param feature_hidden: The feature hidden flag (True if hidden, false otherwise)
            :type feature_hidden: ``bool``

            :return: Default check map
            :rtype: ``dict``
            """
            return {
                "reserved_1": (cls.check_reserved_1, 0),
                "feature_hidden": (cls.check_feature_hidden, feature_hidden),
                "reserved_2": (cls.check_reserved_2, 0)
            }
        # end def get_check_map

        @staticmethod
        def check_reserved_1(test_case, bitmap, expected):
            """
            Check reserved_1 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FeatureType to check
            :type bitmap: ``VLPFeatureSet.FeatureType``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved_1 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The reserved_1 shall be passed as an argument")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(bitmap.reserved_1),
                                  msg="The reserved_1 parameter differs from the one expected")
        # end def check_reserved_1

        @staticmethod
        def check_feature_hidden(test_case, bitmap, expected):
            """
            Check feature_hidden field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FeatureType to check
            :type bitmap: ``VLPFeatureSet.FeatureType``
            :param expected: Expected value
            :type expected: ``bool | HexList``

            :raise ``AssertionError``: Assert feature_hidden that raise an exception
            """
            test_case.assertNotNone(
                expected, msg="The feature_hidden shall be (a) defined in the DUT settings (b) passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(bitmap.feature_hidden),
                                  msg="The feature_hidden parameter differs from the one expected")
        # end def check_feature_hidden

        @staticmethod
        def check_reserved_2(test_case, bitmap, expected):
            """
            Check reserved_2 field in bitmap

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param bitmap: FeatureType to check
            :type bitmap: ``VLPFeatureSet.FeatureType``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert reserved_2 that raise an exception
            """
            test_case.assertNotNone(expected, msg="The reserved_2 shall be passed as an argument")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(bitmap.reserved_2),
                                  msg="The reserved_2 parameter differs from the one expected")
        # end def check_reserved_2
    # end class FeatureTypeChecker

    class FeatureRecordChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check FeatureRecord
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
                "feature_idx": (cls.check_feature_idx, None),
                "feature_id": (cls.check_feature_id, None),
                "feature_version": (cls.check_feature_version, None),
                "feature_type": (cls.check_feature_type, None),
                "feature_max_memory": (cls.check_feature_max_memory, None)
            }
        # end def get_default_check_map

        @staticmethod
        def check_feature_idx(test_case, response, expected):
            """
            Check feature_idx field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIDResponse to check
            :type response: ``GetFeatureIDResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert feature_idx that raise an exception
            """
            test_case.assertNotNone(expected, msg="The feature_idx shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(response.feature_idx),
                                  msg="The feature_idx parameter differs from the one expected")
        # end def check_feature_idx

        @staticmethod
        def check_feature_id(test_case, response, expected):
            """
            Check feature_id field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIDResponse to check
            :type response: ``GetFeatureIDResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert feature_id that raise an exception
            """
            test_case.assertNotNone(expected, msg="The feature_id shall be passed as an argument")
            test_case.assertEqual(expected=HexList(expected), obtained=HexList(response.feature_id),
                                  msg="The feature_id parameter differs from the one expected")
        # end def check_feature_id

        @staticmethod
        def check_feature_type(test_case, message, expected):
            """
            Check ``feature_type``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: GetFeatureIDResponse to check
            :type message: ``GetFeatureIDResponse``
            :param expected: Expected value
            :type expected: ``bool``
            """
            check_map = VLPFeatureSetTestUtils.FeatureTypeChecker.get_check_map(feature_hidden=expected)
            VLPFeatureSetTestUtils.FeatureTypeChecker.check_fields(
                test_case, message.feature_type, VLPFeatureSet.FeatureType, check_map)
        # end def check_feature_type

        @staticmethod
        def check_feature_version(test_case, response, expected):
            """
            Check feature_version field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIDResponse to check
            :type response: ``GetFeatureIDResponse``
            :param expected: Expected value
            :type expected: ``int | HexList``

            :raise ``AssertionError``: Assert feature_version that raise an exception
            """
            test_case.assertNotNone(expected, msg="The feature_version shall be passed as an argument")
            test_case.assertEqual(expected=to_int(expected), obtained=to_int(response.feature_version),
                                  msg="The feature_version parameter differs from the one expected")
        # end def check_feature_version

        @staticmethod
        def check_feature_max_memory(test_case, response, expected):
            """
            Check feature_max_memory field in response

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param response: GetFeatureIDResponse to check
            :type response: ``GetFeatureIDResponse``
            :param expected: Expected value
            :type expected: ``HexList``

            :raise ``AssertionError``: Assert feature_max_memory that raise an exception
            """
            test_case.assertNotNone(expected, msg="The feature_max_memory shall be defined in the DUT settings")
            test_case.assertEqual(expected=Numeral(expected), obtained=Numeral(response.feature_max_memory),
                                  msg="The feature_max_memory parameter differs from the one expected")
        # end def check_feature_max_memory
    # end class FeatureRecordChecker

    class GetFeatureIDResponseChecker(FeatureRecordChecker):
        """
        Define Helper to check ``GetFeatureIDResponse``
        """
    # end class GetFeatureIDResponseChecker

    class GetAllFeatureIDsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Define Helper to check ``GetAllFeatureIDsResponse``
        """
    # end class GetAllFeatureIDsResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``

        @classmethod
        def get_vlp_parameters(cls, test_case, feature_id=VLPFeatureSet.FEATURE_ID, factory=VLPFeatureSetFactory,
                               device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_vlp_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_vlp_parameters

        @classmethod
        def get_count(cls, test_case, device_index=None, port_index=None, software_id=None):
            """
            Process ``GetCount``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: GetCountResponse (if not error)
            :rtype: ``GetCountResponse``
            """
            feature_0103_index, feature_0103, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0103.get_count_cls(
                device_index=device_index,
                feature_index=feature_0103_index)

            VlpProtocolTestUtils.VlpHelper.add_padding(report, len(report) + 1)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0103.get_count_response_cls)
        # end def get_count

        @classmethod
        def get_count_and_check_error(
                cls, test_case, error_codes, function_index=None, device_index=None, port_index=None):
            """
            Process ``GetCount``

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
            """
            feature_0103_index, feature_0103, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0103.get_count_cls(
                device_index=device_index,
                feature_index=feature_0103_index)

            VlpProtocolTestUtils.VlpHelper.add_padding(report, len(report) + 1)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_count_and_check_error

        @classmethod
        def get_feature_id(cls, test_case, feature_idx, device_index=None, port_index=None, software_id=None):
            """
            Process ``GetFeatureID``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param feature_idx: Feature Idx
            :type feature_idx: ``HexList``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: GetFeatureIDResponse (if not error)
            :rtype: ``GetFeatureIDResponse``
            """
            feature_0103_index, feature_0103, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0103.get_feature_id_cls(
                device_index=device_index,
                feature_index=feature_0103_index,
                feature_idx=feature_idx)

            VlpProtocolTestUtils.VlpHelper.add_padding(report, len(report) + 1)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0103.get_feature_id_response_cls)
        # end def get_feature_id

        @classmethod
        def get_feature_id_and_check_error(cls, test_case, error_codes, feature_idx, function_index=None,
                                           device_index=None, port_index=None):
            """
            Process ``GetFeatureID``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param error_codes: Error codes
            :type error_codes: ``list[int]``
            :param feature_idx: Feature Idx
            :type feature_idx: ``HexList``
            :param function_index: Function index - OPTIONAL
            :type function_index: ``int | None``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            """
            feature_0103_index, feature_0103, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0103.get_feature_id_cls(
                device_index=device_index,
                feature_index=feature_0103_index,
                feature_idx=feature_idx)

            VlpProtocolTestUtils.VlpHelper.add_padding(report, len(report) + 1)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_feature_id_and_check_error

        @classmethod
        def get_all_feature_ids(cls, test_case, device_index=None, port_index=None, software_id=None):
            """
            Process ``GetAllFeatureIDs``

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int | None``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int | None``
            :param software_id: Software identifier - OPTIONAL
            :type software_id: ``int | None``

            :return: GetAllFeatureIDsResponse (if not error)
            :rtype: ``GetAllFeatureIDsResponse``
            """
            feature_0103_index, feature_0103, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0103.get_all_feature_ids_cls(
                device_index=device_index,
                feature_index=feature_0103_index)

            VlpProtocolTestUtils.VlpHelper.add_padding(report, len(report) + 1)

            if software_id is not None:
                report.software_id = software_id
            # end if

            return ChannelUtils.send(
                test_case=test_case,
                report=report,
                response_queue_name=HIDDispatcher.QueueName.VLP_IMPORTANT,
                response_class_type=feature_0103.get_all_feature_ids_response_cls)
        # end def get_all_feature_ids

        @classmethod
        def get_all_feature_ids_and_check_error(cls, test_case, error_codes, function_index=None, device_index=None,
                                                port_index=None):
            """
            Process ``GetAllFeatureIDs``

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
            """
            feature_0103_index, feature_0103, device_index, _ = cls.get_vlp_parameters(
                test_case, device_index=device_index, port_index=port_index)

            report = feature_0103.get_all_feature_ids_cls(
                device_index=device_index,
                feature_index=feature_0103_index)

            VlpProtocolTestUtils.VlpHelper.add_padding(report, len(report) + 1)

            if function_index is not None:
                report.function_index = function_index
            # end if

            cls.send_report_wait_error(test_case=test_case, report=report, error_codes=error_codes)
        # end def get_all_feature_ids_and_check_error
    # end class HIDppHelper
# end class VLPFeatureSetTestUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
