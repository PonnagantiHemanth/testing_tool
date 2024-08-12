#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
""" @package pyhid.hidpp.feature.common.test.dfu_test

@brief  HID++ 2.0 DFU test module

@author Stanislas Cottard

@date   2019/08/16
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral
from pyhid.hidpp.features.common.dfu import DfuModel
from pyhid.hidpp.features.common.dfu import DfuInterface
from pyhid.hidpp.features.common.dfu import DfuFactory
from pyhid.hidpp.features.common.dfu import DfuV0
from pyhid.hidpp.features.common.dfu import DfuV1
from pyhid.hidpp.features.common.dfu import DfuV2
from pyhid.hidpp.features.common.dfu import DfuV3
from pyhid.hidpp.features.common.dfu import Dfu
from pyhid.hidpp.features.common.dfu import Restart
from pyhid.hidpp.features.common.dfu import RestartResponse
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd1or2
from pyhid.hidpp.features.common.dfu import DfuCmdDataXCmd3
from pyhid.hidpp.features.common.dfu import DfuCmdDataXData
from pyhid.hidpp.features.common.dfu import DfuStatusResponse
from pyhid.hidpp.features.common.dfu import DfuStatusEvent
from pyhid.hidpp.features.common.dfu import DfuStartV0
from pyhid.hidpp.features.common.dfu import DfuStartV1
from pyhid.hidpp.features.common.dfu import DfuStartV2
from pyhid.hidpp.features.test.root_test import RootTestCase
from unittest import TestCase

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class DfuTestInstanciationCase(TestCase):
    """
    Dfu testing class
    """

    @staticmethod
    def test_dfu():
        """
        Tests Dfu class instantiation
        """
        my_class = Dfu(device_index=0, feature_index=0)

        RootTestCase._top_level_class_checker(my_class)

        my_class = Dfu(device_index=0xFF, feature_index=0xFF)

        RootTestCase._top_level_class_checker(my_class)
    # end def test_dfu

    @staticmethod
    def test_restart():
        """
        Tests Restart class instantiation
        """
        my_class = Restart(device_index=0, feature_index=0, fw_entity=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = Restart(device_index=0xFF, feature_index=0xFF, fw_entity=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_restart

    @staticmethod
    def test_restart_response():
        """
        Tests RestartResponse class instantiation
        """
        my_class = RestartResponse(device_index=0, feature_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = RestartResponse(device_index=0xFF, feature_index=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_restart_response

    @staticmethod
    def test_dfu_status_response():
        """
        Tests DfuStatus class instantiation
        """
        my_class = DfuStatusResponse(device_index=0, feature_index=0, function_index=0, pkt_nb=0, status=0, params=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuStatusResponse(device_index=0xFF, feature_index=0xFF, function_index=0xF, pkt_nb=0xFFFFFFFF,
                                     status=0xFF, params=HexList(hex(pow(2, DfuStatusEvent.LEN.PARAMS) - 1)[2:]))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_status_response

    @staticmethod
    def test_dfu_status_event():
        """
        Tests DfuStatusEvent class instantiation
        """
        my_class = DfuStatusEvent(device_index=0, feature_index=0, pkt_nb=0, status=0, params=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuStatusEvent(device_index=0xFF, feature_index=0xFF, pkt_nb=0xFFFFFFFF, status=0xFF,
                                  params=HexList(hex(pow(2, DfuStatusEvent.LEN.PARAMS) - 1)[2:]))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_status_event

    @staticmethod
    def test_dfu_cmd_data_x_cmd_1_or_2():
        """
        Tests DfuCmdDataXCmd1or2 class instantiation
        """
        my_class = DfuCmdDataXCmd1or2(device_index=0, feature_index=0, function_index=0, cmd_1_or_2=False, address=0,
                                      size=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuCmdDataXCmd1or2(device_index=0xFF, feature_index=0xFF, function_index=0xF, cmd_1_or_2=True,
                                      address=pow(2, DfuCmdDataXCmd1or2.LEN.ADDRESS) - 1,
                                      size=pow(2, DfuCmdDataXCmd1or2.LEN.SIZE) - 1)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_cmd_data_x_cmd_1_or_2

    @staticmethod
    def test_dfu_cmd_data_x_cmd_3():
        """
        Tests DfuCmdDataXCmd3 class instantiation
        """
        my_class = DfuCmdDataXCmd3(device_index=0, feature_index=0, function_index=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuCmdDataXCmd3(device_index=0xFF, feature_index=0xFF, function_index=0xF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_cmd_data_x_cmd_3

    @staticmethod
    def test_dfu_cmd_data_x_data():
        """
        Tests DfuCmdDataXData class instantiation
        """
        my_class = DfuCmdDataXData(device_index=0, feature_index=0, function_index=0, data=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuCmdDataXData(device_index=0xFF, feature_index=0xFF, function_index=0xF,
                                   data=HexList(hex(pow(2, DfuCmdDataXData.LEN.DATA) - 1)[2:]))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_cmd_data_x_data

    @staticmethod
    def test_dfu_start_v0():
        """
        Tests DfuStartV0 class instantiation
        """
        my_class = DfuStartV0(device_index=0, feature_index=0, fw_entity=0, encrypt=0,
                              magic_str=HexList(Numeral(0, DfuStartV0.LEN.MAGIC_STR // 8)))

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuStartV0(device_index=0xFF, feature_index=0xFF, fw_entity=0xFF, encrypt=0xFF,
                              magic_str=HexList(hex(pow(2, DfuStartV0.LEN.MAGIC_STR) - 1)[2:]))

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_start_v0

    @staticmethod
    def test_dfu_start_v1():
        """
        Tests DfuStartV1 class instantiation
        """
        my_class = DfuStartV1(device_index=0, feature_index=0, fw_entity=0, encrypt=0,
                              magic_str=HexList(Numeral(0, DfuStartV1.LEN.MAGIC_STR // 8)), flag=0)

        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuStartV1(device_index=0xFF, feature_index=0xFF, fw_entity=0xFF, encrypt=0xFF,
                              magic_str=HexList(hex(pow(2, DfuStartV1.LEN.MAGIC_STR) - 1)[2:]), flag=0xFF)

        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_start_v1

    @staticmethod
    def test_dfu_start_v2():
        """
        Tests DfuStartV2 class instantiation
        """
        my_class = DfuStartV2(device_index=0, feature_index=0, fw_entity=0, encrypt=0,
                              magic_str=HexList(Numeral(0, DfuStartV2.LEN.MAGIC_STR // 8)), flag=0,
                              secur_lvl=0)
        RootTestCase._long_function_class_checker(my_class)

        my_class = DfuStartV2(device_index=0xFF, feature_index=0xFF, fw_entity=0xFF, encrypt=0xFF,
                              magic_str=HexList(hex(pow(2, DfuStartV2.LEN.MAGIC_STR) - 1)[2:]), flag=0xFF,
                              secur_lvl=0xFF)
        RootTestCase._long_function_class_checker(my_class)
    # end def test_dfu_start_v2
# end class DfuTestCase


class DfuTestCase(TestCase):
    """
    Dfu factory testing
    """

    @classmethod
    def setUpClass(cls):
        cls.expected = {
            0: {
                "cls": DfuV0,
                "interfaces": {
                    "dfu_cmd_data0_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data1_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data2_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data3_cls": DfuCmdDataXCmd3,
                    "dfu_start_cls": DfuStartV0,
                    "restart_cls": Restart,
                    "dfu_cmd_data0_response_cls": DfuStatusResponse,
                    "dfu_cmd_data1_response_cls": DfuStatusResponse,
                    "dfu_cmd_data2_response_cls": DfuStatusResponse,
                    "dfu_cmd_data3_response_cls": DfuStatusResponse,
                    "dfu_start_response_cls": DfuStatusResponse,
                    "restart_response_cls": RestartResponse,
                },
                "max_function_index": 5
            },
            1: {
                "cls": DfuV1,
                "interfaces": {
                    "dfu_cmd_data0_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data1_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data2_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data3_cls": DfuCmdDataXCmd3,
                    "dfu_start_cls": DfuStartV1,
                    "restart_cls": Restart,
                    "dfu_cmd_data0_response_cls": DfuStatusResponse,
                    "dfu_cmd_data1_response_cls": DfuStatusResponse,
                    "dfu_cmd_data2_response_cls": DfuStatusResponse,
                    "dfu_cmd_data3_response_cls": DfuStatusResponse,
                    "dfu_start_response_cls": DfuStatusResponse,
                    "restart_response_cls": RestartResponse,
                },
                "max_function_index": 5
            },
            2: {
                "cls": DfuV2,
                "interfaces": {
                    "dfu_cmd_data0_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data1_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data2_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data3_cls": DfuCmdDataXCmd3,
                    "dfu_start_cls": DfuStartV2,
                    "restart_cls": Restart,
                    "dfu_cmd_data0_response_cls": DfuStatusResponse,
                    "dfu_cmd_data1_response_cls": DfuStatusResponse,
                    "dfu_cmd_data2_response_cls": DfuStatusResponse,
                    "dfu_cmd_data3_response_cls": DfuStatusResponse,
                    "dfu_start_response_cls": DfuStatusResponse,
                    "restart_response_cls": RestartResponse,
                },
                "max_function_index": 5
            },
            3: {
                "cls": DfuV3,
                "interfaces": {
                    "dfu_cmd_data0_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data1_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data2_cls": DfuCmdDataXCmd1or2,
                    "dfu_cmd_data3_cls": DfuCmdDataXCmd3,
                    "dfu_start_cls": DfuStartV2,
                    "restart_cls": Restart,
                    "dfu_cmd_data0_response_cls": DfuStatusResponse,
                    "dfu_cmd_data1_response_cls": DfuStatusResponse,
                    "dfu_cmd_data2_response_cls": DfuStatusResponse,
                    "dfu_cmd_data3_response_cls": DfuStatusResponse,
                    "dfu_start_response_cls": DfuStatusResponse,
                    "restart_response_cls": RestartResponse,
                },
                "max_function_index": 5
            },
        }
    # end def setUpClass

    def test_dfu_factory(self):
        """
        Tests DFU Factory
        """
        for version, expected in self.expected.items():
            self.assertEqual(type(DfuFactory.create(version)), expected["cls"])
        # end for loop
    # end def test_dfu_factory

    def test_dfu_factory_version_out_of_range(self):
        """
        Tests DFU Factory with out of range versions
        """
        for version in [4, 5]:
            with self.assertRaises(KeyError):
                DfuFactory.create(version)
            # end with
        # end for
    # end def test_dfu_factory_version_out_of_range

    def test_dfu_factory_interfaces(self):
        """
        Check DFU Factory returns expected interfaces
        """
        for version, cls_map in self.expected.items():
            dfu = DfuFactory.create(version)
            for interface, interface_cls in cls_map["interfaces"].items():
                if interface_cls:
                    self.assertEqual(getattr(dfu, interface), interface_cls)
                else:
                    with self.assertRaises(NotImplementedError):
                        getattr(dfu, interface)
                # end if
            # end for loop
        # end for loop
    # end def test_dfu_factory_interfaces

    def test_get_max_function_index(self):
        """
        Check get_max_function_index returns correct value at each version
        """
        for version, expected in self.expected.items():
            dfu = DfuFactory.create(version)
            self.assertEqual(dfu.get_max_function_index(), expected["max_function_index"])
        # end for loop
    # end def test_get_max_function_index
# end class DfuTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
