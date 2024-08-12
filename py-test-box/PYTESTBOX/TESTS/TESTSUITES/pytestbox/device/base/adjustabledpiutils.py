#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
:package: pytestbox.device.base.adjustabledpiutils
:brief: Helpers for Adjustable DPI feature
:author: Fred Chen <fchen7@logitech.com>
:date: 2021/06/16
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from math import ceil

from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpi
from pyhid.hidpp.features.mouse.adjustabledpi import AdjustableDpiFactory
from pyhid.hidpp.features.mouse.adjustabledpi import GetNumberOfDpiLevelsResponseV2
from pylibrary.tools.numeral import Numeral
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.device.base.spidirectaccessutils import HERO_SENSOR_HIGH_SPEED_THRESHOLD
from pytestbox.device.base.spidirectaccessutils import OpticalSensorName


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AdjustableDpiTestUtils(DeviceBaseTestUtils):
    """
    Test utils for x2201 Adjustable DPI feature
    """

    DPI_LEVEL_COLORS = ['WHITE', 'ORANGE', 'TEAL', 'YELLOW', 'MAGENTA']

    class GetSensorCountResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Helper to check GetSensorCount response
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
            config = test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
            return {
                "sensor_count": (cls.check_sensor_count, config.F_SensorCount),
            }
        # end def get_default_check_map

        @classmethod
        def check_sensor_count(cls, test_case, message, expected):
            """
            Check sensor count

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetSensorCountResponse``
            :param expected: sensor_count field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.sensor_count)), expected=int(Numeral(expected)),
                                  msg="sensor_count value is not as expected")
        # end def check_sensor_count
    # end class GetSensorCountResponseChecker

    class GetSensorDpiListResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check GetSensorDpiList response
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
            config = test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "dpi_list": (cls.check_dpi_list, config),
            }
        # end def get_default_check_map

        @classmethod
        def check_sensor_idx(cls, test_case, message, expected):
            """
            Check sensor index

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetSensorDpiListResponse``
            :param expected: sensor_idx field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.sensor_idx)), expected=int(Numeral(expected)),
                                  msg="sensor_index value is not as expected")
        # end def check_sensor_idx

        @classmethod
        def check_dpi_list(cls, test_case, message, expected):
            """
            Check Dpi List

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetSensorDpiListResponse``
            :param expected: dpi_list field expected value
            :type expected: ``AdjDPISubSystem``
            """
            adj_dpi = expected
            is_range, range_list, list_list = AdjustableDpiTestUtils.parse_raw_dpi_list(message.dpi_list)
            test_case.assertEqual(expected=adj_dpi.F_DpiListReportList,
                                  obtained=not is_range,
                                  msg='The DpiListReportList parameter differs from the one expected')
            test_case.assertEqual(expected=adj_dpi.F_DpiListReportRange,
                                  obtained=is_range,
                                  msg='The DpiListReportRange parameter differs from the one expected')

            if adj_dpi.F_DpiListReportRange is True:
                test_case.assertEqual(expected=adj_dpi.F_DpiMin,
                                      obtained=range_list['min'],
                                      msg=f'The rangeList["min"] {range_list["min"]} differs from '
                                          f'the one expected {adj_dpi.F_DpiMin}')
                test_case.assertEqual(expected=adj_dpi.F_DpiStep,
                                      obtained=range_list['step'],
                                      msg=f'The rangeList["step"] {range_list["step"]} differs from '
                                          f'the one expected {adj_dpi.F_DpiStep}')
                test_case.assertEqual(expected=adj_dpi.F_DpiMax,
                                      obtained=range_list['max'],
                                      msg=f'The rangeList["max"] {range_list["max"]} differs from '
                                          f'the one expected {adj_dpi.F_DpiMax}')
            # end if

            if adj_dpi.F_DpiListReportList is True:
                for dpi in list_list:
                    dpi_list = AdjustableDpiTestUtils.get_dpi_from_list_report(adj_dpi)
                    test_case.assertTrue(dpi in dpi_list, msg=f'The dpi {dpi} differs from the one expected')
                # end for
            # end if
        # end def check_dpi_list
    # end class GetSensorDpiListResponseChecker

    class GetSensorDpiResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check GetSensorDpi response
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
            config = test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "dpi": (cls.check_dpi, config.F_DpiDefault),
                "default_dpi": (cls.check_default_dpi, config.F_DpiDefault),
            }
        # end def get_default_check_map

        @classmethod
        def check_sensor_idx(cls, test_case, message, expected):
            """
            Check sensor index

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetSensorDpiResponseV0``
            :param expected: sensor_idx field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.sensor_idx)), expected=int(Numeral(expected)),
                                  msg="sensor_index value is not as expected")
        # end def check_sensor_idx

        @classmethod
        def check_dpi(cls, test_case, message, expected):
            """
            Check sensor Dpi

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetSensorDpiResponseV0``
            :param expected: dpi field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.dpi)), expected=int(Numeral(expected)),
                                  msg="dpi value is not as expected")
        # end def check_dpi

        @classmethod
        def check_default_dpi(cls, test_case, message, expected):
            """
            Check sensor default Dpi

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetSensorDpiResponseV1ToV2``
            :param expected: default_dpi field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.default_dpi)), expected=int(Numeral(expected)),
                                  msg="default_dpi value is not as expected")
        # end def check_default_dpi
    # end class GetSensorDpiResponseChecker

    class SetSensorDpiResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check SetSensorDpi response
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
            config = test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
            return {
                "sensor_idx": (cls.check_sensor_idx, 0),
                "dpi": (cls.check_dpi, config.F_DpiDefault),
                "default_dpi": (cls.check_default_dpi, config.F_DpiDefault),
                "dpi_level": (cls.check_dpi_level, 0),
            }
        # end def get_default_check_map

        @classmethod
        def check_sensor_idx(cls, test_case, message, expected):
            """
            Check sensor index

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``SetSensorDpiResponseV0ToV1``
            :param expected: sensor_idx field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.sensor_idx)), expected=int(Numeral(expected)),
                                  msg="sensor_idx value is not as expected")
        # end def check_sensor_idx

        @classmethod
        def check_dpi(cls, test_case, message, expected):
            """
            Check sensor Dpi

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``SetSensorDpiResponseV0ToV1``
            :param expected: dpi field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.dpi)), expected=int(Numeral(expected)),
                                  msg="Dpi value is not as expected")
        # end def check_dpi

        @classmethod
        def check_default_dpi(cls, test_case, message, expected):
            """
            Check sensor default Dpi

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``SetSensorDpiResponseV0ToV1``
            :param expected: default_dpi field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.default_dpi)), expected=int(Numeral(expected)),
                                  msg="default_dpi value is not as expected")
        # end def check_default_dpi

        @classmethod
        def check_dpi_level(cls, test_case, message, expected):
            """
            Check sensor Dpi levels

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``SetSensorDpiResponseV2``
            :param expected: dpi_level field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.dpi_level)), expected=int(Numeral(expected)),
                                  msg="dpi_level value is not as expected")
        # end def check_dpi_level
    # end class SetSensorDpiResponseChecker

    class GetNumberOfDpiLevelsResponseChecker(DeviceBaseTestUtils.MessageChecker):
        """
        Test utils to check GetNumberOfDpiLevels response
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
                "dpi_levels": (cls.check_dpi_levels, test_case.max_supported_dpi_levels),
            }
        # end def get_default_check_map

        @classmethod
        def check_dpi_levels(cls, test_case, message, expected):
            """
            Check Dpi levels

            :param test_case: Current test case
            :type test_case: ``CommonBaseTestCase``
            :param message: Obtained message
            :type message: ``GetNumberOfDpiLevelsResponseV2``
            :param expected: dpi_levels field expected value
            :type expected: ``int``
            """
            test_case.assertEqual(obtained=int(Numeral(message.dpi_levels)), expected=int(Numeral(expected)),
                                  msg="dpi_levels value is not as expected")
        # end def check_dpi_levels
    # end class GetNumberOfDpiLevelsResponseChecker

    class HIDppHelper(DeviceBaseTestUtils.HIDppHelper):
        # See ``DeviceBaseTestUtils.HIDppHelper``
        @classmethod
        def get_parameters(cls, test_case, feature_id=AdjustableDpi.FEATURE_ID, factory=AdjustableDpiFactory,
                           device_index=None, port_index=None, update_test_case=None, skip_not_found=False):
            # See ``DeviceBaseTestUtils.HIDppHelper.get_parameters``
            return super().get_parameters(
                test_case, feature_id, factory, device_index, port_index, update_test_case, skip_not_found)
        # end def get_parameters

        @classmethod
        def get_sensor_count(cls, test_case, device_index=None, port_index=None):
            """
            HID++ request to get sensor count

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetSensorCount response
            :rtype: ``GetSensorCountResponse``
            """
            feature_2201_index, feature_2201, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_sensor_count_req = feature_2201.get_sensor_count_cls(device_index, feature_2201_index)
            get_sensor_count_resp = test_case.send_report_wait_response(
                report=get_sensor_count_req,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2201.get_sensor_count_response_cls)
            return get_sensor_count_resp
        # end def get_sensor_count

        @classmethod
        def get_sensor_dpi_list(cls, test_case, sensor_idx=0, device_index=None, port_index=None):
            """
            HID++ request to get sensor dpi list

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param sensor_idx: The index of optical sensor - OPTIONAL
            :type sensor_idx: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetSensorDpiList response
            :rtype: ``GetSensorDpiListResponse``
            """
            feature_2201_index, feature_2201, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_sensor_dpi_list_req = feature_2201.get_sensor_dpi_list_cls(
                device_index, feature_2201_index, sensor_idx=sensor_idx)
            get_sensor_dpi_list_resp = test_case.send_report_wait_response(
                report=get_sensor_dpi_list_req,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2201.get_sensor_dpi_list_response_cls)
            return get_sensor_dpi_list_resp
        # end def get_sensor_dpi_list

        @classmethod
        def get_sensor_dpi(cls, test_case, sensor_idx=0, device_index=None, port_index=None):
            """
            HID++ request to get sensor dpi

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param sensor_idx: The index of optical sensor - OPTIONAL
            :type sensor_idx: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return:  GetSensorDpi response
            :rtype: ``GetSensorDpiResponseV0`` or ``GetSensorDpiResponseV1ToV2``
            """
            feature_2201_index, feature_2201, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_sensor_dpi_req = feature_2201.get_sensor_dpi_cls(
                device_index, feature_2201_index, sensor_idx=sensor_idx)
            get_sensor_dpi_resp = test_case.send_report_wait_response(
                report=get_sensor_dpi_req,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2201.get_sensor_dpi_response_cls)
            return get_sensor_dpi_resp
        # end def get_sensor_dpi

        @classmethod
        def set_sensor_dpi(cls, test_case, sensor_idx, dpi, device_index=None, port_index=None, **kwargs):
            """
            HID++ request to set sensor dpi

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param sensor_idx: The index of optical sensor
            :type sensor_idx: ``int``
            :param dpi: The Dpi value will be set to optical sensor
            :type dpi: ``int``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``
            :param kwargs: Potential future parameters
            :type kwargs: ``dict or int``

            :kwargs:
                * **dpi_level** (``int``): Set DPI Level to display the predefined DPI color - OPTIONAL

            :return: SetSensorDpi response
            :rtype: ``SetSensorDpiResponseV0ToV1`` or ``SetSensorDpiResponseV2``
            """
            feature_2201_index, feature_2201, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            if feature_2201.VERSION < 2:
                set_sensor_dpi_req = feature_2201.set_sensor_dpi_cls(
                    device_index, feature_2201_index, sensor_idx=sensor_idx, dpi=dpi)
            else:
                dpi_level = kwargs['dpi_level']
                set_sensor_dpi_req = feature_2201.set_sensor_dpi_cls(
                    device_index, feature_2201_index, sensor_idx=sensor_idx, dpi=dpi, dpi_level=dpi_level)
            # end if

            set_sensor_dpi_resp = test_case.send_report_wait_response(
                report=set_sensor_dpi_req,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2201.set_sensor_dpi_response_cls)
            return set_sensor_dpi_resp
        # end def set_sensor_dpi

        @classmethod
        def get_number_of_dpi_levels(cls, test_case, device_index=None, port_index=None):
            """
            HID++ request to get the number of Dpi levels

            :param test_case: The current test case
            :type test_case: ``CommonBaseTestCase``
            :param device_index: Device index - OPTIONAL
            :type device_index: ``int``
            :param port_index: Port index - OPTIONAL
            :type port_index: ``int``

            :return: GetSensorCount response
            :rtype: ``GetNumberOfDpiLevelsResponseV2``
            """
            feature_2201_index, feature_2201, device_index, _ = cls.get_parameters(
                test_case, device_index=device_index, port_index=port_index)

            get_number_of_dpi_levels_req = feature_2201.get_number_of_dpi_levels_cls(device_index, feature_2201_index)
            get_number_of_dpi_levels_resp = test_case.send_report_wait_response(
                report=get_number_of_dpi_levels_req,
                response_queue=test_case.hidDispatcher.mouse_message_queue,
                response_class_type=feature_2201.get_number_of_dpi_levels_response_cls)
            return get_number_of_dpi_levels_resp
        # end def get_number_of_dpi_levels
    # end class HIDppHelper

    @classmethod
    def parse_raw_dpi_list(cls, raw_data):
        """
        To parse RAW DPI list data from FW report into range or list type format

        :param raw_data: DPI list raw data
        :type raw_data: ``list``

        :return: The report type is range or not and the data list
        :rtype: ``list``
        """
        is_range = False
        result_list = []
        high_bytes = raw_data[0::2]
        low_bytes = raw_data[1::2]
        range_report_threshold = 0xe0
        for h, l in zip(high_bytes, low_bytes):
            if h >= range_report_threshold:
                result_list.append(((h - range_report_threshold) << 8) + l)
                is_range = True
            else:
                result_list.append((h << 8) + l)
            # end if
        # end for

        range_list = dict(min=0, step=0, max=0)
        list_list = None
        if is_range is True:
            range_list['min'] = result_list[0]
            range_list['step'] = result_list[1]
            range_list['max'] = result_list[2]
        else:
            list_list = result_list
        # end if

        return is_range, range_list, list_list
    # end def parse_raw_dpi_list

    @classmethod
    def is_the_dpi_in_the_list_report(cls, dpi, adj_dpi):
        """
        Check the DPi is in the list report or not

        :param dpi: The Dpi value for checking
        :type dpi: ``int``
        :param adj_dpi: The user settings of ADJUSTABLE_DPI
        :type adj_dpi: ``AdjDPISubSystem``

        :return: True if the dpi value is found in the feature configuration, False otherwise
        :rtype: ``bool``
        """
        dpi_in_list_report = cls.get_dpi_from_list_report(adj_dpi)
        return dpi in dpi_in_list_report
    # end def is_the_dpi_in_the_list_report

    @classmethod
    def get_dpi_from_list_report(cls, adj_dpi):
        """
        Get DPI from list report

        :param adj_dpi: The user settings of ADJUSTABLE_DPI
        :type adj_dpi: ``AdjDPISubSystem``

        :return: The DPI values from DPI List report
        :rtype: ``list``
        """
        return [adj_dpi.F_DPI_1, adj_dpi.F_DPI_2, adj_dpi.F_DPI_3, adj_dpi.F_DPI_4, adj_dpi.F_DPI_5, adj_dpi.F_DPI_6]
    # end def get_dpi_from_list_report

    @classmethod
    def generate_valid_dpi_list(cls, test_case):
        """
        Generate a valid DPI list whatever the DpiList type

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: A valid Dpi list
        :rtype: ``list``
        """
        adj_dpi = test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI
        valid_dpi_list = None
        if adj_dpi.F_DpiListReportRange:
            if adj_dpi.F_DpiMin == adj_dpi.F_DpiMax and adj_dpi.F_DpiStep == 0:
                valid_dpi_list = [adj_dpi.F_DpiMin]
            else:
                valid_dpi_list = list(range(adj_dpi.F_DpiMin, adj_dpi.F_DpiMax, adj_dpi.F_DpiStep))
            # end if
        elif adj_dpi.F_DpiListReportList:
            valid_dpi_list = cls.get_dpi_from_list_report(adj_dpi)
        # end if
        test_case.assertNotNone(obtained=valid_dpi_list)
        return valid_dpi_list
    # end def generate_valid_dpi_list

    @classmethod
    def update_invalid_dpi_list(cls, adj_dpi, invalid_dpi_list, start_dpi):
        """
        Update the invalid DPI list

        :param adj_dpi: The user settings of ADJUSTABLE_DPI
        :type adj_dpi: ``AdjDPISubSystem``
        :param invalid_dpi_list: The list to update
        :type invalid_dpi_list: ``list``
        :param start_dpi: Start DPI Value
        :type start_dpi: ``int``
        """
        if adj_dpi.F_DpiListReportRange:
            if start_dpi < adj_dpi.F_DpiMin or start_dpi > adj_dpi.F_DpiMax:
                invalid_dpi_list.append(start_dpi)
            # end if
        elif adj_dpi.F_DpiListReportList:
            dpi_list = cls.get_dpi_from_list_report(adj_dpi)
            if start_dpi not in dpi_list:
                invalid_dpi_list.append(start_dpi)
            # end if
        # end if
    # end def update_invalid_dpi_list

    @classmethod
    def generate_invalid_dpi_list(cls, adj_dpi):
        """
        Generate an invalid DPI list whatever the DpiList type

        :param adj_dpi: The user settings of ADJUSTABLE_DPI
        :type adj_dpi: ``AdjDPISubSystem``

        :return: The invalid DPI list
        :rtype: ``list``
        """
        invalid_dpi_list = []
        start_dpi = 1
        shift_count = 16
        unused_dpi = 0xE000
        while shift_count > 0:
            cls.update_invalid_dpi_list(adj_dpi, invalid_dpi_list, start_dpi)
            start_dpi <<= 1
            shift_count -= 1
        # end while
        invalid_dpi_list.append(unused_dpi)
        start_dpi = 0xFFFE
        shift_count = 16
        while shift_count > 0:
            cls.update_invalid_dpi_list(adj_dpi, invalid_dpi_list, start_dpi)
            start_dpi = ((start_dpi << 1) + 1) & 0xFFFF
            shift_count -= 1
        # end while
        return invalid_dpi_list
    # end def generate_invalid_dpi_list

    @classmethod
    def get_dpi_at_next_dpi_level(cls, test_case, dpi):
        """
        Get the Dpi at next dpi level for DPI cycling button

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param dpi: The Dpi value for finding its next value
        :type dpi: ``int``

        :return: The Dpi value at the next level
        :rtype: ``int``
        """
        predefined_dpi_levels = AdjustableDpiTestUtils.get_predefined_dpi_levels(test_case)
        for idx, d in enumerate(predefined_dpi_levels):
            if dpi == int(d):
                if idx == len(predefined_dpi_levels) - 1:
                    return int(predefined_dpi_levels[0])
                else:
                    return int(predefined_dpi_levels[idx + 1])
                # end if
            # end if
        # end for
    # end def get_dpi_at_next_dpi_level

    @classmethod
    def get_predefined_dpi_levels(cls, test_case):
        """
        Get the predefined DPI level list

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: The predefined DPI level list
        :rtype: ``list``
        """
        predefined_dpi_levels = list(test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_PredefinedDpiValueList)
        if predefined_dpi_levels[-1] == '':
            predefined_dpi_levels.pop(-1)
        # end if
        return predefined_dpi_levels
        # end if
    # end def get_predefined_dpi_levels

    @classmethod
    def adjust_dpi_by_high_speed_threshold(cls, test_case, dpi):
        """
        Gaming mice usually have high speed mode that increasing DPI in double step

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``
        :param dpi: The DPI value
        :type dpi: ``int``

        :return: The adjusted DPI
        :rtype: ``int``
        """
        if test_case.f.PRODUCT.FEATURES.MOUSE.F_OpticalSensorName != OpticalSensorName.HERO:
            return dpi
        else:
            adjusted_dpi = dpi
            if dpi > HERO_SENSOR_HIGH_SPEED_THRESHOLD:
                adjusted_dpi = ceil(dpi / 100) * 100
            # end if
            return adjusted_dpi
        # end if
    # end def adjust_dpi_by_high_speed_threshold

    @classmethod
    def get_default_dpi_level_index(cls, test_case):
        """
        Get the default Dpi level index

        :param test_case: The current test case
        :type test_case: ``CommonBaseTestCase``

        :return: The default Dpi level index
        :rtype: ``int``
        """
        default_dpi = test_case.f.PRODUCT.FEATURES.MOUSE.ADJUSTABLE_DPI.F_DpiDefault
        predefined_dpi_level_list = AdjustableDpiTestUtils.get_predefined_dpi_levels(test_case)
        default_dpi_index = None
        if predefined_dpi_level_list:
            default_dpi_index = predefined_dpi_level_list.index(f'{default_dpi}')
        # end if
        return default_dpi_index
    # end def get_default_dpi_level_index
# end class AdjustableDpiTestUtils
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
