#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pyhid.hidpp.hidpp1.registers.registers_test
    :brief: HID++ 1.0 Registers tests
    :author: Martin Cryonnet
    :date: 2020/03/20
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.notifications.bleservicechanged import BleServiceChanged
from pylibrary.tools.hexlist import HexList
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1NotificationMap
from pyhid.hidpp.hidpp1.hidpp1message import Hidpp1Message
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase
from pyhid.hidpp.hidpp1.notifications.devicedisconnection import DeviceDisconnection
from pyhid.hidpp.hidpp1.notifications.deviceconnection import DeviceConnection
from pyhid.hidpp.hidpp1.notifications.linkqualityinfo import LinkQualityInfoShort
from pyhid.hidpp.hidpp1.notifications.linkqualityinfo import LinkQualityInfoLong
from pyhid.hidpp.hidpp1.notifications.requestdisplaypasskey import RequestDisplayPassKey
from pyhid.hidpp.hidpp1.notifications.displaypasskeykey import DisplayPassKeyKey
from pyhid.hidpp.hidpp1.notifications.devicediscovery import DeviceDiscovery
from pyhid.hidpp.hidpp1.notifications.devicerecovery import DeviceRecovery
from pyhid.hidpp.hidpp1.notifications.discoverystatus import DiscoveryStatus
from pyhid.hidpp.hidpp1.notifications.pairingstatus import PairingStatus
from pyhid.hidpp.hidpp1.notifications.dfutimeout import DfuTimeout


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class NotificationsTestCase(RegisterBaseTestCase):
    """
    Registers test case
    """

    NOTIFICATIONS = [
        # TODO : device connection and disconnection
        #  {
        #      "name": "Device Disconnection",
        #      "sub_id": 0x40,
        #      "report_id": Hidpp1Message.DEFAULT.REPORT_ID_SHORT,
        #      "class": DeviceDisconnection,
        #      "parameters": [
        #          {
        #              "name": "device_index",
        #              "len": 8
        #          },
        #          {
        #              "name": "disconnection_type",
        #              "len": 8
        #          }
        #      ]
        #  },
        {
            "name": "Link Quality Information (eQUAD only) (long)",
            "sub_id": 0x48,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_LONG,
            "class": LinkQualityInfoLong,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "number_of_records",
                    "len": 8
                },
                {
                    "name": "record_device_index_1",
                    "len": 8
                },
                {
                    "name": "event_type_1",
                    "len": 8
                },
                {
                    "name": "channel_1",
                    "len": 6
                },
                {
                    "name": "counter_1",
                    "len": 2
                },
                {
                    "name": "last_link_loss_duration_1",
                    "len": 8
                },
                {
                    "name": "agility_hops_1",
                    "len": 4
                },
                {
                    "name": "repetitions_1",
                    "len": 4
                },
                {
                    "name": "record_device_index_2",
                    "len": 8
                },
                {
                    "name": "event_type_2",
                    "len": 8
                },
                {
                    "name": "channel_2",
                    "len": 6
                },
                {
                    "name": "counter_2",
                    "len": 2
                },
                {
                    "name": "last_link_loss_duration_2",
                    "len": 8
                },
                {
                    "name": "agility_hops_2",
                    "len": 4
                },
                {
                    "name": "repetitions_2",
                    "len": 4
                },
                {
                    "name": "record_device_index_3",
                    "len": 8
                },
                {
                    "name": "event_type_3",
                    "len": 8
                },
                {
                    "name": "channel_3",
                    "len": 6
                },
                {
                    "name": "counter_3",
                    "len": 2
                },
                {
                    "name": "last_link_loss_duration_3",
                    "len": 8
                },
                {
                    "name": "agility_hops_3",
                    "len": 4
                },
                {
                    "name": "repetitions_3",
                    "len": 4
                },
            ]
        },
        {
            "name": "Link Quality Information (eQUAD only) (short)",
            "sub_id": 0x49,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_SHORT,
            "class": LinkQualityInfoShort,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "event_type",
                    "len": 8
                },
                {
                    "name": "channel",
                    "len": 6
                },
                {
                    "name": "counter",
                    "len": 2
                },
                {
                    "name": "last_link_loss_duration",
                    "len": 8
                },
                {
                    "name": "agility_hops",
                    "len": 4
                },
                {
                    "name": "repetitions",
                    "len": 4
                },
            ]
        },
        {
            "name": "Request to display a passkey",
            "sub_id": 0x4D,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_LONG,
            "class": RequestDisplayPassKey,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "passkey_length",
                    "len": 8
                },
                {
                    "name": "passkey_digits",
                    "len": 6 * 8
                },
                {
                    "name": "bluetooth_address",
                    "len": 6 * 8
                }
            ]
        },
        {
            "name": "Display passkey key",
            "sub_id": 0x4E,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_LONG,
            "class": DisplayPassKeyKey,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "key_code",
                    "len": 8
                },
                {
                    "name": "bluetooth_address",
                    "len": 6 * 8
                }
            ]
        },
        {
            "name": "Device Discovery",
            "sub_id": 0x4F,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_LONG,
            "class": DeviceDiscovery,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "notification_counter",
                    "len": 8
                },
                {
                    "name": "notification_part",
                    "len": 2
                },
                {
                    "name": "data",
                    "len": 14 * 8,
                    "type": HexList,
                    "dependency": {
                        "on": "notification_part",
                        "choices": {
                            0x00: {
                                "class": DeviceDiscovery.DeviceDiscoveryPart0,
                                "parameters": [
                                    {
                                        "name": "protocol_type",
                                        "len": 8
                                    },
                                    {
                                        "name": "device_type",
                                        "len": 4
                                    },
                                    {
                                        "name": "bluetooth_pid",
                                        "len": 2 * 8
                                    },
                                    {
                                        "name": "bluetooth_address",
                                        "len": 6 * 8
                                    },
                                    {
                                        "name": "ble_pro_service_version",
                                        "len": 8
                                    },
                                    {
                                        "name": "product_specific_data",
                                        "len": 8
                                    },
                                    {
                                        "name": "prepairing_auth_method",
                                        "len": 1
                                    },
                                    {
                                        "name": "reserved_auth_method",
                                        "len": 5
                                    },
                                    {
                                        "name": "emu_2buttons_auth_method",
                                        "len": 1
                                    },
                                    {
                                        "name": "passkey_auth_method",
                                        "len": 1
                                    },
                                ]
                            },
                            0x01: {
                                "class": DeviceDiscovery.DeviceDiscoveryPart1,
                                "parameters": [
                                    {
                                        "name": "device_name_length",
                                        "len": 8
                                    },
                                    {
                                        "name": "device_name_start",
                                        "len": 13 * 8
                                    },
                                ]
                            },
                            0x02: {
                                "class": DeviceDiscovery.DeviceDiscoveryPart2,
                                "parameters": [
                                    {
                                        "name": "device_name_chunk",
                                        "len": 14 * 8
                                    },
                                ]
                            },
                            0x03: {
                                "class": DeviceDiscovery.DeviceDiscoveryPart3,
                                "parameters": [
                                    {
                                        "name": "device_name_chunk",
                                        "len": 14 * 8
                                    },
                                ]
                            },
                        }
                    }
                }
            ]
        },
        {
            "name": "Device Recovery",
            "sub_id": 0x52,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_LONG,
            "class": DeviceRecovery,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "notification_counter",
                    "len": 8
                },
                {
                    "name": "notification_part",
                    "len": 2
                },
                {
                    "name": "data",
                    "len": 14 * 8,
                    "type": HexList,
                    "dependency": {
                        "on": "notification_part",
                        "choices": {
                            0x00: {
                                "class": DeviceRecovery.DeviceRecoveryPart0,
                                "parameters": [
                                    {
                                        "name": "protocol_type",
                                        "len": 8
                                    },
                                    {
                                        "name": "bluetooth_pid",
                                        "len": 2 * 8
                                    },
                                    {
                                        "name": "bluetooth_address",
                                        "len": 6 * 8
                                    },
                                    {
                                        "name": "ble_pro_service_version",
                                        "len": 8
                                    },
                                    {
                                        "name": "unit_id",
                                        "len": 4 * 8
                                    },
                                ]
                            },
                            0x01: {
                                "class": DeviceRecovery.DeviceRecoveryPart1,
                                "parameters": [
                                    {
                                        "name": "device_name_length",
                                        "len": 8
                                    },
                                    {
                                        "name": "device_name_start",
                                        "len": 13 * 8
                                    },
                                ]
                            },
                            0x02: {
                                "class": DeviceRecovery.DeviceRecoveryPart2,
                                "parameters": [
                                    {
                                        "name": "device_name_chunk",
                                        "len": 14 * 8
                                    },
                                ]
                            },
                            0x03: {
                                "class": DeviceRecovery.DeviceRecoveryPart3,
                                "parameters": [
                                    {
                                        "name": "device_name_chunk",
                                        "len": 14 * 8
                                    },
                                ]
                            },
                        }
                    }
                }
            ]
        },
        {
            "name": "Discovery Status Notification",
            "sub_id": 0x53,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_SHORT,
            "class": DiscoveryStatus,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "device_discovery_status",
                    "len": 8
                },
                {
                    "name": "error_type",
                    "len": 8
                }
            ]
        },
        {
            "name": "Pairing Status Notification",
            "sub_id": 0x54,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_LONG,
            "class": PairingStatus,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "device_pairing_status",
                    "len": 8
                },
                {
                    "name": "error_type",
                    "len": 8
                },
                {
                    "name": "bluetooth_address",
                    "len": 6 * 8,
                    "type": HexList
                },
                {
                    "name": "pairing_slot",
                    "len": 8
                }
            ]
        },
        {
            "name": "BLE Service Changed",
            "sub_id": 0x55,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_SHORT,
            "class": BleServiceChanged,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
                {
                    "name": "pairing_slot",
                    "len": 8
                },
                {
                    "name": "service_changed_status",
                    "len": 8
                },
            ]
        },
        {
            "name": "DFU Timeout",
            "sub_id": 0x56,
            "report_id": Hidpp1Message.DEFAULT.REPORT_ID_SHORT,
            "class": DfuTimeout,
            "parameters": [
                {
                    "name": "device_index",
                    "len": 8
                },
            ]
        }
    ]

    def test_class_match(self):
        """
        Check each class from model is part of the test case commands list and vice versa
        """
        classes_from_model = Hidpp1NotificationMap.get_available_events_classes()
        # TODO :
        #  classes_from_model += Hidpp1NotificationMap.get_connection_events_classes()

        classes_from_test_case = []

        for notification in self.NOTIFICATIONS:
            message_class = notification["class"]
            self.assertIn(message_class, classes_from_model)
            classes_from_test_case.append(message_class)
        # end for

        for message_class in classes_from_model:
            self.assertIn(message_class, classes_from_test_case)
        # end for
    # end def test_class_match

    def test_class_instantiation(self):
        """
        Test classes instantiations
        """
        report_id_to_checker_map = {
            Hidpp1Message.DEFAULT.REPORT_ID_SHORT: self._short_function_class_checker,
            Hidpp1Message.DEFAULT.REPORT_ID_LONG: self._long_function_class_checker
        }

        for notification in self.NOTIFICATIONS:
            for bits_value in ["0", "1"]:
                parameters = self.get_parameters(notification, bits_value)
                msg = f'Notification "{notification["name"]}" instantiation failed'
                class_under_test = self.check_class_instantiation(notification, parameters, msg)
                report_id_to_checker_map[notification["report_id"]](class_under_test, msg)
                # self.assertEqual(class_under_test.report_id, notification["report_id"], msg)
                self.assertEqual(class_under_test.SUB_ID, notification["sub_id"], msg)
                self.assertEqual(class_under_test.sub_id, HexList(notification["sub_id"]), msg)
            # end for
        # end for
    # end def test_class_instantiation

    def test_parameters_with_dependency(self):
        """
        Test parameters with parsing depending on other parameter
        """
        for notification in self.NOTIFICATIONS:
            if "parameters" in notification and notification["parameters"] is not None:
                for parameter in notification["parameters"]:
                    if "dependency" in parameter:
                        self.check_parameter_choices(notification, parameter)
                    # end if
                # end for
            # end if
        # end for
    # end def test_parameter_with_dependency

    def check_class_instantiation(self, notification, parameters, msg="Class instantiation failed"):
        """
        Check a class can be instantiated
        """
        try:
            return notification["class"](**parameters)
        except Exception as e:
            self.fail(f'{msg} with error: {type(e).__name__}: {e}')
        # end try
    # end def check_class_instantiation

    def get_parameters(self, notification, bits_value=0):
        """
        Get expected parameters with all bits set to bit_values for each parameter
        """
        parameters = {}

        if "parameters" in notification and notification["parameters"] is not None:
            parameters = {parameter["name"]: self.get_parameter_value(parameter, bits_value)
                          for parameter in notification["parameters"]}
        # end if
        return parameters
    # end def get_parameters

    @staticmethod
    def get_parameter_value(parameter, bits_value=0):
        """
        Get parameter value
        """
        value = int(str(bits_value) * parameter["len"], 2)
        if "type" in parameter and parameter["type"] is not None and parameter["type"] is HexList:
            value = HexList(str(bits_value) * 2 * (parameter["len"] // 8))
        # end if
        return value
    # end def get_parameter_value

    def check_parameter_choices(self, notification, parameter):
        """
        Check different possible choices for a parameter
        """
        for choice_value, choice_details in parameter["dependency"]["choices"].items():
            parameters = self.get_parameters(notification)
            parameters[parameter["dependency"]["on"]] = choice_value
            msg = f'Command "{notification["name"]}" instantiation failed with ' \
                  f'{parameter["dependency"]["on"]} = {choice_value}'
            class_under_test = self.check_class_instantiation(notification, parameters, msg)
            self.assertIsInstance(class_under_test.__getattr__(parameter["name"]), choice_details["class"])
            self._attributes_checker(class_under_test.__getattr__(parameter["name"]),
                                     [(par["name"], par["len"]) for par in choice_details["parameters"]],
                                     msg=msg)
        # end for
    # end def check_parameter_choices

# end class NotificationsTestCase


# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
