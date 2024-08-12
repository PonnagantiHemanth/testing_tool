#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pyhid.hidpp.hidpp1.registers.registers_test
:brief: HID++ 1.0 Registers tests
:author: Martin Cryonnet
:date: 2020/03/20
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.hidpp1data import Hidpp1Data
from pyhid.hidpp.hidpp1.hidpp1model import Hidpp1RegisterMap
from pyhid.hidpp.hidpp1.registers.connectionstate import GetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import GetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateRequest
from pyhid.hidpp.hidpp1.registers.connectionstate import SetConnectionStateResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingRequest
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import GetEnableHidppReportingResponse
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import SetEnableHidppReportingRequest
from pyhid.hidpp.hidpp1.registers.enablehidppreporting import SetEnableHidppReportingResponse
from pyhid.hidpp.hidpp1.registers.enterupgrademode import GetEnterUpgradeModeRequest
from pyhid.hidpp.hidpp1.registers.enterupgrademode import GetEnterUpgradeModeResponse
from pyhid.hidpp.hidpp1.registers.enterupgrademode import SetEnterUpgradeModeRequest
from pyhid.hidpp.hidpp1.registers.getrssi import GetRssiRequest
from pyhid.hidpp.hidpp1.registers.getrssi import GetRssiResponse
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesDisableFeaturesRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesDisableFeaturesResponse
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableFeaturesRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesEnableFeaturesResponse
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoRequest
from pyhid.hidpp.hidpp1.registers.managedeactivatablefeatures import ManageDeactivatableFeaturesGetInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import GetNonVolatileMemoryAccessRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import GetNonVolatileMemoryAccessResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import SetNonVolatileMemoryAccessRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryaccess import SetNonVolatileMemoryAccessResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryoperation import SetNonVolatileMemoryOperationRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilememoryoperation import SetNonVolatileMemoryOperationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDeviceDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetBLEProDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceExtendedPairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceExtendedPairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDevicePairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetEQuadDevicePairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetFwVersionResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformation
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetTransceiverEQuadInformationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetUsbSerialNumberRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import GetUsbSerialNumberResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetAesEncryptionKeyRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetAesEncryptionKeyResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDevicePairingInformationRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDevicePairingInformationResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceExtendedPairingInfoRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceExtendedPairingInfoResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceNameRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetEQuadDeviceNameResponse
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetTransceiverEQuadInformationRequest
from pyhid.hidpp.hidpp1.registers.nonvolatilepairinginformation import SetTransceiverEQuadInformationResponse
from pyhid.hidpp.hidpp1.registers.passwd import PasswordRequest
from pyhid.hidpp.hidpp1.registers.passwd import PasswordResponse
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.performdeviceconnection import SetPerformDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import GetPerformDeviceDiscoveryRequest
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import GetPerformDeviceDiscoveryResponse
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryRequest
from pyhid.hidpp.hidpp1.registers.performdevicediscovery import SetPerformDeviceDiscoveryResponse
from pyhid.hidpp.hidpp1.registers.prepairingdata import GetPrepairingDataRequest
from pyhid.hidpp.hidpp1.registers.prepairingdata import GetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingdata import SetPrepairingDataRequest
from pyhid.hidpp.hidpp1.registers.prepairingdata import SetPrepairingDataResponse
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementRequest
from pyhid.hidpp.hidpp1.registers.prepairingmanagement import SetPrepairingManagementResponse
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetGothardDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetGothardDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionRequest
from pyhid.hidpp.hidpp1.registers.quaddeviceconnection import SetQuadDeviceConnectionResponse
from pyhid.hidpp.hidpp1.registers.randomdata import GetRandomDataRequest
from pyhid.hidpp.hidpp1.registers.randomdata import GetRandomDataResponse
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoRequest
from pyhid.hidpp.hidpp1.registers.receiverfwinformation import GetReceiverFwInfoResponse
from pyhid.hidpp.hidpp1.registers.reset import SetResetRequest
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessRequest
from pyhid.hidpp.hidpp1.registers.rfregisteraccess import SetRFRegisterAccessResponse
from pyhid.hidpp.hidpp1.registers.securedfucontrol import GetDfuControlRequest
from pyhid.hidpp.hidpp1.registers.securedfucontrol import GetDfuControlResponse
from pyhid.hidpp.hidpp1.registers.securedfucontrol import SetDfuControlRequest
from pyhid.hidpp.hidpp1.registers.securedfucontrol import SetDfuControlResponse
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralRequest
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyCentralResponse
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralRequest
from pyhid.hidpp.hidpp1.registers.setcsrkkey import SetCSRKKeyPeripheralResponse
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralRequest
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyCentralResponse
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralRequest
from pyhid.hidpp.hidpp1.registers.setirkkey import SetIRKKeyPeripheralResponse
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyRequest
from pyhid.hidpp.hidpp1.registers.setltkkey import SetLTKKeyResponse
from pyhid.hidpp.hidpp1.registers.startsession import StartSessionRequest
from pyhid.hidpp.hidpp1.registers.startsession import StartSessionResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import GetTestModeControlResponse
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlRequest
from pyhid.hidpp.hidpp1.registers.testmodecontrol import SetTestModeControlResponse
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import GetUniqueIdentifierRequest
from pyhid.hidpp.hidpp1.registers.uniqueidentifier import GetUniqueIdentifierResponse
from pyhid.hidpp.hidpp1.test.registerbasetest import RegisterBaseTestCase
from pyhid.hidpp.hidppmessage import HidppMessage
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
class RegistersTestCase(RegisterBaseTestCase):
    """
    Registers test case
    """
    COMMANDS = [
        {
            "name": "Enable HID++ Reporting Register",
            "address": 0x00,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetEnableHidppReportingRequest
            },
            "response": {
                "class": GetEnableHidppReportingResponse,
                "parameters": [
                    {
                        "name": "device_reporting_flag_numpad_numeric_keys",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_f_lock_status",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_roller_h",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_battery_status",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_mouse_extra_buttons",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_roller_v",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_power_keys",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_consumer_vendor_specific_control",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_channel_change_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_attack_detection_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_touchpad_multi_touch_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_software_present",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_quad_link_quality_info",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_ui_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_wireless_notifications",
                        "len": 1
                    },
                    {
                        "name": "device_cont_reporting_flag_configuration_complete",
                        "len": 1
                    },
                    {
                        "name": "device_cont_reporting_flag_vo_ip_telephony",
                        "len": 1
                    },
                    {
                        "name": "device_cont_reporting_flag_3d_gesture",
                        "len": 1
                    }
                ]
            }
        },
        {
            "name": "Enable HID++ Reporting Register",
            "address": 0x00,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetEnableHidppReportingRequest,
                "parameters": [
                    {
                        "name": "device_reporting_flag_numpad_numeric_keys",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_f_lock_status",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_roller_h",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_battery_status",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_mouse_extra_buttons",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_roller_v",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_power_keys",
                        "len": 1
                    },
                    {
                        "name": "device_reporting_flag_consumer_vendor_specific_control",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_channel_change_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_attack_detection_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_touchpad_multi_touch_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_software_present",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_quad_link_quality_info",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_ui_notifications",
                        "len": 1
                    },
                    {
                        "name": "receiver_reporting_flag_wireless_notifications",
                        "len": 1
                    },
                    {
                        "name": "device_cont_reporting_flag_configuration_complete",
                        "len": 1
                    },
                    {
                        "name": "device_cont_reporting_flag_vo_ip_telephony",
                        "len": 1
                    },
                    {
                        "name": "device_cont_reporting_flag_3d_gesture",
                        "len": 1
                    }
                ]
            },
            "response": {
                "class": SetEnableHidppReportingResponse
            }
        },
        {
            "name": "Connection State",
            "address": 0x02,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetConnectionStateRequest,
            },
            "response": {
                "class": GetConnectionStateResponse,
                "parameters": [
                    {
                        "name": "read_number_connected_devices",
                        "len": 8
                    },
                    {
                        "name": "read_number_remaining_pairing_slots",
                        "len": 8
                    }
                ]
            }
        },
        {
            "name": "Connection State",
            "address": 0x02,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetConnectionStateRequest,
                "parameters": [
                    {
                        "name": "write_action_on_connection_fake_ctrl_alt_f12",
                        "len": 1
                    },
                    {
                        "name": "write_action_on_connection_fake_device_arrival",
                        "len": 1
                    },
                    {
                        "name": "write_action_on_connection_fake_connect_button",
                        "len": 1
                    }
                ]
            },
            "response": {
                "class": SetConnectionStateResponse
            }
        },
        {
            "name": "Device Connection and Disconnection (QUAD or eQUAD)",
            "address": 0xB2,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetQuadDeviceConnectionRequest,
                "parameters": [
                    {
                        "name": "connect_devices",
                        "len": 8
                    },
                    {
                        "name": "device_number",
                        "len": 8
                    },
                    {
                        "name": "open_lock_timeout",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": SetQuadDeviceConnectionResponse
            }
        },
        {
            "name": "Device Connection and Disconnection (QUAD or eQUAD)",
            "address": 0xB2,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetGothardDeviceConnectionRequest,
                "parameters": [
                    {
                        "name": "connect_devices",
                        "len": 8
                    },
                    {
                        "name": "device_number",
                        "len": 8
                    },
                    {
                        "name": "open_lock_timeout",
                        "len": 8
                    },
                    {
                        "name": "rssi_threshold",
                        "len": 8
                    },
                    {
                        "name": "lna_gain",
                        "len": 8
                    },
                    {
                        "name": "aaf_gain",
                        "len": 8
                    },
                    {
                        "name": "device_quad_id",
                        "len": 16
                    },
                    {
                        "name": "device_quad_id_mask",
                        "len": 16
                    },
                    {
                        "name": "debug_mode",
                        "len": 8
                    },
                    {
                        "name": "consecutives_messages_count",
                        "len": 8
                    },
                    {
                        "name": "output_power",
                        "len": 8
                    },
                    {
                        "name": "protocol",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": SetGothardDeviceConnectionResponse
            }
        },
        {
            "name": "Get RSSI",
            "address": 0xB4,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetRssiRequest,
                "parameters": [
                    {
                        "name": "index",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": GetRssiResponse,
                "parameters": [
                    {
                        "name": "index",
                        "len": 8
                    },
                    {
                        "name": "device_type",
                        "len": 8
                    },
                    {
                        "name": "signal_strength",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - USB serial number",
            "address": 0xB5,
            "register_0": 0x01,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetUsbSerialNumberRequest,
            },
            "response": {
                "class": GetUsbSerialNumberResponse,
                "parameters": [
                    {
                        "name": "serial_number",
                        "len": 15 * 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - FW Version",
            "address": 0xB5,
            "register_0": 0x02,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetFwVersionRequest,
            },
            "response": {
                "class": GetFwVersionResponse,
                "parameters": [
                    {
                        "name": "fw_name",
                        "len": 8
                    },
                    {
                        "name": "fw_version",
                        "len": 8
                    },
                    {
                        "name": "fw_build_number",
                        "len": 2 * 8
                    },
                    {
                        "name": "protocol_id",
                        "len": 2 * 8
                    },
                    {
                        "name": "r7",
                        "len": 8
                    },
                    {
                        "name": "r8",
                        "len": 8
                    }
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - Get Transceiver EQuad Information",
            "address": 0xB5,
            "register_0": 0x03,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetTransceiverEQuadInformation
            },
            "response": {
                "class": GetTransceiverEQuadInformationResponse,
                "parameters": [
                    {
                        "name": "base_address",
                        "len": 4 * 8
                    },
                    {
                        "name": "rf_channel_index",
                        "len": 8
                    },
                    {
                        "name": "number_of_pairing_slots",
                        "len": 8
                    },
                    {
                        "name": "last_dest_id",
                        "len": 8
                    },
                    {
                        "name": "number_of_remaining_connections",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - Set Transceiver EQuad Information",
            "address": 0xB5,
            "register_0": 0x03,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetTransceiverEQuadInformationRequest,
                "parameters": [
                    {
                        "name": "base_address",
                        "len": 4 * 8
                    },
                    {
                        "name": "rf_channel_index",
                        "len": 8
                    },
                    {
                        "name": "number_of_pairing_slots",
                        "len": 8
                    },
                    {
                        "name": "last_dest_id",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": SetTransceiverEQuadInformationResponse
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - eQuad 'step 4' device - Get pairing information",
            "address": 0xB5,
            "register_0": (0x20, 0x2F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetEQuadDevicePairingInfoRequest
            },
            "response": {
                "class": GetEQuadDevicePairingInfoResponse,
                "parameters": [
                    {
                        "name": "destination_id",
                        "len": 8
                    },
                    {
                        "name": "default_report_interval",
                        "len": 8
                    },
                    {
                        "name": "device_quid",
                        "len": 2 * 8
                    },
                    {
                        "name": "equad_major_version",
                        "len": 8
                    },
                    {
                        "name": "equad_minor_version",
                        "len": 8
                    },
                    {
                        "name": "equad_device_subclass",
                        "len": 8
                    },
                    {
                        "name": "equad_attributes",
                        "len": 6 * 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - eQuad 'step 4' device - Set pairing information",
            "address": 0xB5,
            "register_0": (0x20, 0x2F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetEQuadDevicePairingInformationRequest,
                "parameters": [
                    {
                        "name": "destination_id",
                        "len": 8
                    },
                    {
                        "name": "default_report_interval",
                        "len": 8
                    },
                    {
                        "name": "device_quid",
                        "len": 2 * 8
                    },
                    {
                        "name": "equad_major_version",
                        "len": 8
                    },
                    {
                        "name": "equad_minor_version",
                        "len": 8
                    },
                    {
                        "name": "equad_device_subclass",
                        "len": 8
                    },
                    {
                        "name": "equad_attributes",
                        "len": 6 * 8
                    },
                ]
            },
            "response": {
                "class": SetEQuadDevicePairingInformationResponse
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - eQuad 'step 4' Get Device extended pairing info",
            "address": 0xB5,
            "register_0": (0x30, 0x3F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetEQuadDeviceExtendedPairingInfoRequest
            },
            "response": {
                "class": GetEQuadDeviceExtendedPairingInfoResponse,
                "parameters": [
                    {
                        "name": "serial_number",
                        "len": 4 * 8
                    },
                    {
                        "name": "report_types",
                        "len": 4 * 8
                    },
                    {
                        "name": "usability_info",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - eQuad 'step 4' Set Device extended pairing info",
            "address": 0xB5,
            "register_0": (0x30, 0x3F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetEQuadDeviceExtendedPairingInfoRequest,
                "parameters": [
                    {
                        "name": "serial_number",
                        "len": 4 * 8
                    },
                    {
                        "name": "report_types",
                        "len": 4 * 8
                    },
                    {
                        "name": "usability_info",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": SetEQuadDeviceExtendedPairingInfoResponse
            }
        },
        {
            "name": 'Non-Volatile and Pairing Information - eQuad "step 4" Get Device name',
            "address": 0xB5,
            "register_0": (0x40, 0x4F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetEQuadDeviceNameRequest,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": GetEQuadDeviceNameResponse,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                    {
                        "name": "segment_length",
                        "len": 8
                    },
                    {
                        "name": "name_string",
                        "len": 14 * 8
                    },
                ]
            }
        },
        {
            "name": 'Non-Volatile and Pairing Information - eQuad "step 4" Set Device name',
            "address": 0xB5,
            "register_0": (0x40, 0x4F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetEQuadDeviceNameRequest,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                    {
                        "name": "segment_length",
                        "len": 8
                    },
                    {
                        "name": "name_string",
                        "len": 14 * 8
                    },
                ]
            },
            "response": {
                "class": SetEQuadDeviceNameResponse
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - BLE Pro device - pairing information",
            "address": 0xB5,
            "register_0": (0x51, 0x5F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetBLEProDevicePairingInfoRequest,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": GetBLEProDevicePairingInfoResponse,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                    {
                        "name": "device_type",
                        "len": 4
                    },
                    {
                        "name": "link_status",
                        "len": 1
                    },
                    {
                        "name": "bluetooth_pid",
                        "len": 2 * 8
                    },
                    {
                        "name": "device_unit_id",
                        "len": 2 * 8
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
                        "name": "passkey_auth_method",
                        "len": 1
                    },
                    {
                        "name": "emu_2buttons_auth_method",
                        "len": 1
                    },
                    {
                        "name": "prepairing_auth_method",
                        "len": 1
                    },
                    {
                        "name": "auth_entropy",
                        "len": 8
                    },
                    {
                        "name": "device_state",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - BLE Pro device - device name",
            "address": 0xB5,
            "register_0": (0x61, 0x6F),
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetBLEProDeviceDeviceNameRequest,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                    {
                        "name": "device_name_part",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": GetBLEProDeviceDeviceNameResponse,
                "parameters": [
                    {
                        "name": "r0",
                        "len": 8
                    },
                    {
                        "name": "device_name_part",
                        "len": 8
                    },
                    {
                        "name": "data",
                        "len": 14 * 8,
                        "type": HexList,
                        "dependency": {
                            "on": "device_name_part",
                            "choices": {
                                0x01: {
                                    "class": GetBLEProDeviceDeviceNameResponse.DeviceNamePart1,
                                    "parameters": [
                                        {
                                            "name": "device_name_length",
                                            "len": 8
                                        },
                                        {
                                            "name": "device_name_start",
                                            "len": 13 * 8
                                        }
                                    ]
                                },
                                0x02: {
                                    "class": GetBLEProDeviceDeviceNameResponse.DeviceNamePart2or3,
                                    "parameters": [
                                        {
                                            "name": "device_name_chunk",
                                            "len": 14 * 8
                                        }
                                    ]
                                },
                                0x03: {
                                    "class": GetBLEProDeviceDeviceNameResponse.DeviceNamePart2or3,
                                    "parameters": [
                                        {
                                            "name": "device_name_chunk",
                                            "len": 14 * 8
                                        }
                                    ]
                                },
                            }
                        }
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile and Pairing Information - eQuad 'step 4' Set AES Encryption Key",
            "address": 0xB5,
            "register_0": (0xF0, 0xFF),
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetAesEncryptionKeyRequest,
                "parameters": [
                    {
                        "name": "p0",
                        "len": 8
                    },
                    {
                        "name": "aes_encryption_key_byte_1_to_6",
                        "len": 6 * 8
                    },
                    {
                        "name": "aes_encryption_key_byte_9_to_16",
                        "len": 8 * 8
                    },
                ]
            },
            "response": {
                "class": SetAesEncryptionKeyResponse
            }
        },
        {
            "name": "Perform Device Discovery",
            "address": 0xC0,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetPerformDeviceDiscoveryRequest,
            },
            "response": {
                "class": GetPerformDeviceDiscoveryResponse,
                "parameters": [
                    {
                        "name": "discover_devices_status",
                        "len": 8
                    }
                ]
            }
        },
        {
            "name": "Perform Device Discovery",
            "address": 0xC0,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetPerformDeviceDiscoveryRequest,
                "parameters": [
                    {
                        "name": "discovery_timeout",
                        "len": 8
                    },
                    {
                        "name": "discover_devices",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": SetPerformDeviceDiscoveryResponse
            }
        },
        {
            "name": "Perform device connection and disconnection",
            "address": 0xC1,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetPerformDeviceConnectionRequest,
                "parameters": [
                    {
                        "name": "connect_devices",
                        "len": 8
                    },
                    {
                        "name": "bluetooth_address",
                        "len": 6 * 8
                    },
                    {
                        "name": "passkey_auth_method",
                        "len": 1
                    },
                    {
                        "name": "emu_2buttons_auth_method",
                        "len": 1
                    },
                    {
                        "name": "auth_entropy",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": SetPerformDeviceConnectionResponse
            }
        },
        {
            "name": "Test Mode Control",
            "address": 0xD0,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetTestModeControlRequest,
            },
            "response": {
                "class": GetTestModeControlResponse,
                "parameters": [
                    {
                        "name": "test_mode_enable",
                        "len": 1
                    },
                ]
            }
        },
        {
            "name": "Test Mode Control",
            "address": 0xD0,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetTestModeControlRequest,
                "parameters": [
                    {
                        "name": "test_mode_enable",
                        "len": 1
                    },
                ]
            },
            "response": {
                "class": SetTestModeControlResponse,
            }
        },
        {
            "name": "RF Register Access",
            "address": 0xD1,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetRFRegisterAccessRequest,
                "parameters": [
                    {
                        "name": "rf_page_register",
                        "len": 8
                    },
                    {
                        "name": "address_register",
                        "len": 8
                    },
                    {
                        "name": "data",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": SetRFRegisterAccessResponse,
            }
        },
        {
            "name": "Non-Volatile Memory Access",
            "address": 0xD4,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetNonVolatileMemoryAccessRequest,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                    {
                        "name": "nvm_address_lsb",
                        "len": 8
                    },
                    {
                        "name": "nvm_address_msb",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": GetNonVolatileMemoryAccessResponse,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                    {
                        "name": "nvm_address_lsb",
                        "len": 8
                    },
                    {
                        "name": "nvm_address_msb",
                        "len": 8
                    },
                    {
                        "name": "data",
                        "len": 8
                    }
                ]
            }
        },
        {
            "name": "Non-Volatile Memory Access",
            "address": 0xD4,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetNonVolatileMemoryAccessRequest,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                    {
                        "name": "nvm_address_lsb",
                        "len": 8
                    },
                    {
                        "name": "nvm_address_msb",
                        "len": 8
                    },
                    {
                        "name": "data",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": SetNonVolatileMemoryAccessResponse,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "Non-Volatile Memory Operation",
            "address": 0xD7,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetNonVolatileMemoryOperationRequest,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                    {
                        "name": "target_selection",
                        "len": 2
                    },
                    {
                        "name": "nvm_operation",
                        "len": 4
                    },
                ]
            },
            "response": {
                "class": SetNonVolatileMemoryOperationResponse,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "Prepairing Data Management",
            "address": 0xE7,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetPrepairingManagementRequest,
                "parameters": [
                    {
                        "name": "pairing_slot",
                        "len": 8
                    },
                    {
                        "name": "prepairing_management_control",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": SetPrepairingManagementResponse,
            }
        },
        {
            "name": "Set LTK Key",
            "address": 0xE8,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetLTKKeyRequest,
                "parameters": [
                    {
                        "name": "key_value",
                        "len": 16 * 8
                    }
                ]
            },
            "response": {
                "class": SetLTKKeyResponse,
            }
        },
        {
            "name": "Set IRK Key (Privacy) - Central",
            "address": 0xE9,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetIRKKeyCentralRequest,
                "parameters": [
                    {
                        "name": "key_value",
                        "len": 16 * 8
                    }
                ]
            },
            "response": {
                "class": SetIRKKeyCentralResponse,
            }
        },
        {
            "name": "Set IRK Key (Privacy) - Peripheral",
            "address": 0xEA,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetIRKKeyPeripheralRequest,
                "parameters": [
                    {
                        "name": "key_value",
                        "len": 16 * 8
                    }
                ]
            },
            "response": {
                "class": SetIRKKeyPeripheralResponse,
            }
        },
        {
            "name": "Set CSRK Key (Signature) - Central",
            "address": 0xEB,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetCSRKKeyCentralRequest,
                "parameters": [
                    {
                        "name": "key_value",
                        "len": 16 * 8
                    }
                ]
            },
            "response": {
                "class": SetCSRKKeyCentralResponse,
            }
        },
        {
            "name": "Set CSRK Key (Signature) - Peripheral",
            "address": 0xEC,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetCSRKKeyPeripheralRequest,
                "parameters": [
                    {
                        "name": "key_value",
                        "len": 16 * 8
                    }
                ]
            },
            "response": {
                "class": SetCSRKKeyPeripheralResponse,
            }
        },
        {
            "name": "Set Prepairing Data",
            "address": 0xED,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetPrepairingDataRequest,
                "parameters": [
                    {
                        "name": "data_type",
                        "len": 8
                    },
                    {
                        "name": "ble_address",
                        "len": 6 * 8
                    }
                ]
            },
            "response": {
                "class": SetPrepairingDataResponse,
            }
        },
        {
            "name": "Get Prepairing Data",
            "address": 0xED,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetPrepairingDataRequest,
                "parameters": [
                    {
                        "name": "data_type",
                        "len": 8
                    },
                ]
            },
            "response": {
                "class": GetPrepairingDataResponse,
                "parameters": [
                    {
                        "name": "data_type",
                        "len": 8
                    },
                    {
                        "name": "ble_address",
                        "len": 6 * 8
                    }
                ]
            }
        },
        {
            "name": "Enter USB or OTA firmware upgrade mode",
            "address": 0xF0,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": GetEnterUpgradeModeRequest,
            },
            "response": {
                "class": GetEnterUpgradeModeResponse,
                "parameters": [
                    {
                        "name": "key",
                        "len": 3 * 8
                    }
                ]
            }
        },
        {
            "name": "Enter USB or OTA firmware upgrade mode",
            "address": 0xF0,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetEnterUpgradeModeRequest,
                "parameters": [
                    {
                        "name": "key",
                        "len": 3 * 8
                    }
                ]
            },
        },
        {
            "name": "Reset",
            "address": 0xF2,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": SetResetRequest,
                "parameters": [
                    {
                        "name": "device_index",
                        "len": 8
                    },
                    {
                        "name": "fw_info_item",
                        "len": 8
                    }
                ]
            }
        },
        {
            "name": "Receiver FW information",
            "address": 0xF4,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetReceiverFwInfoRequest,
                "parameters": [
                    {
                        "name": "entity_idx",
                        "len": 8
                    }
                ]
            },
            "response": {
                "class": GetReceiverFwInfoResponse,
                "parameters": [
                    {
                        "name": "entity_type",
                        "len": 8
                    },
                    {
                        "name": "fw_number",
                        "len": 8
                    },
                    {
                        "name": "fw_revision",
                        "len": 8
                    },
                    {
                        "name": "fw_build",
                        "len": 2 * 8
                    },
                    {
                        "name": "extra_ver",
                        "len": 5 * 8
                    },
                ]
            }
        },
        {
            "name": "Dfu Control",
            "address": 0xF5,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetDfuControlRequest,
            },
            "response": {
                "class": GetDfuControlResponse,
                "parameters": [
                    {
                        "name": "enable_dfu",
                        "len": 1
                    },
                    {
                        "name": "dfu_control_timeout",
                        "len": 8
                    },
                    {
                        "name": "dfu_control_action_type",
                        "len": 8
                    }
                ]
            }
        },
        {
            "name": "Dfu Control",
            "address": 0xF5,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": SetDfuControlRequest,
                "parameters": [
                    {
                        "name": "enable_dfu",
                        "len": 1
                    },
                    {
                        "name": "dfu_magic_key",
                        "len": 24
                    },
                ]
            },
            "response": {
                "class": SetDfuControlResponse
            }
        },
        {
            "name": "Random Data",
            "address": 0xF6,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetRandomDataRequest
            },
            "response": {
                "class": GetRandomDataResponse,
                "parameters": [
                    {
                        "name": "random_data",
                        "len": 128
                    },
                ]
            }
        },
        {
            "name": "Start Session",
            "address": 0xF7,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": StartSessionRequest,
                "parameters": [
                    {
                        "name": "account_name",
                        "len": 128,
                        "type": str,
                    },
                ]
            },
            "response": {
                "class": StartSessionResponse,
                "parameters": [
                    {
                        "name": "constant_credentials",
                        "len": 1
                    },
                    {
                        "name": "full_authentication",
                        "len": 1
                    },
                    {
                        "name": "long_password",
                        "len": 1
                    },
                ]
            }
        },
        {
            "name": "Password",
            "address": 0xF8,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER,
            "request": {
                "class": PasswordRequest,
                "parameters": [
                    {
                        "name": "password",
                        "len": 128,
                    },
                ]
            },
            "response": {
                "class": PasswordResponse,
                "parameters": [
                    {
                        "name": "status",
                        "len": 8
                    },
                ]
            }
        },
        {
            "name": "ManageDeactivatableFeatures GetInfo",
            "address": 0xF9,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER,
            "request": {
                "class": ManageDeactivatableFeaturesGetInfoRequest,
            },
            "response": {
                "class": ManageDeactivatableFeaturesGetInfoResponse,
                "parameters": [
                    {
                        "name": "support_all_bit",
                        "len": 1,
                    },
                    {
                        "name": "support_gothard",
                        "len": 1,
                    },
                    {
                        "name": "support_compliance",
                        "len": 1,
                    },
                    {
                        "name": "support_manufacturing",
                        "len": 1,
                    },
                    {
                        "name": "persistent_all_bit_activation",
                        "len": 1,
                    },
                    {
                        "name": "persistent_gothard_activation",
                        "len": 1,
                    },
                    {
                        "name": "persistent_compliance_activation",
                        "len": 1,
                    },
                    {
                        "name": "persistent_manufacturing_activation",
                        "len": 1,
                    },
                    {
                        "name": "state_all_bit_activation",
                        "len": 1,
                    },
                    {
                        "name": "state_gothard_activation",
                        "len": 1,
                    },
                    {
                        "name": "state_compliance_activation",
                        "len": 1,
                    },
                    {
                        "name": "state_manufacturing_activation",
                        "len": 1,
                    },
                ]
            }
        },
        {
            "name": "ManageDeactivatableFeatures DisableFeatures",
            "address": 0xF9,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": ManageDeactivatableFeaturesDisableFeaturesRequest,
                "parameters": [
                    {
                        "name": "disable_all_bit",
                        "len": 1,
                    },
                    {
                        "name": "disable_gothard",
                        "len": 1,
                    },
                    {
                        "name": "disable_compliance",
                        "len": 1,
                    },
                    {
                        "name": "disable_manufacturing",
                        "len": 1,
                    },
                ]
            },
            "response": {
                "class": ManageDeactivatableFeaturesDisableFeaturesResponse,
            }
        },
        {
            "name": "ManageDeactivatableFeatures EnableFeatures",
            "address": 0xFA,
            "type": Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER,
            "request": {
                "class": ManageDeactivatableFeaturesEnableFeaturesRequest,
                "parameters": [
                    {
                        "name": "enable_all_bit",
                        "len": 1,
                    },
                    {
                        "name": "enable_gothard",
                        "len": 1,
                    },
                    {
                        "name": "enable_compliance",
                        "len": 1,
                    },
                    {
                        "name": "enable_manufacturing",
                        "len": 1,
                    },
                ]
            },
            "response": {
                "class": ManageDeactivatableFeaturesEnableFeaturesResponse,
            }
        },
        {
            "name": "Unique Identifier",
            "address": 0xFB,
            "type": Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER,
            "request": {
                "class": GetUniqueIdentifierRequest
            },
            "response": {
                "class": GetUniqueIdentifierResponse,
                "parameters": [
                    {
                        "name": "unique_identifier",
                        "len": 128
                    },
                ]
            }
        },
    ]

    def test_class_match(self):
        """
        Check each class from model is part of the test case commands list and vice versa
        """
        classes_from_model = Hidpp1RegisterMap.get_available_classes()
        classes_from_test_case = []

        for command, message_type in self.command_message_type_gen():
            message_class = command[message_type]["class"]
            self.assertIn(message_class, classes_from_model)
            classes_from_test_case.append(message_class)
        # end for

        for message_class in classes_from_model:
            self.assertIn(message_class, classes_from_test_case)
        # end for
    # end def test_class_match

    def test_commands_instantiation(self):
        """
        Test classes instantiations
        """
        type_to_checker_map = {
            Hidpp1Data.Hidpp1RegisterSubId.SET_REGISTER: {
                "request": self._short_function_class_checker,
                "response": self._short_function_class_checker
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_REGISTER: {
                "request": self._short_function_class_checker,
                "response": self._short_function_class_checker
            },
            Hidpp1Data.Hidpp1RegisterSubId.SET_LONG_REGISTER: {
                "request": self._long_function_class_checker,
                "response": self._short_function_class_checker
            },
            Hidpp1Data.Hidpp1RegisterSubId.GET_LONG_REGISTER: {
                "request": self._short_function_class_checker,
                "response": self._long_function_class_checker
            }
        }
        report_id_to_checker_map = {
            HidppMessage.DEFAULT.REPORT_ID_SHORT: self._short_function_class_checker,
            HidppMessage.DEFAULT.REPORT_ID_LONG: self._long_function_class_checker,
        }

        for command, message_type in self.command_message_type_gen():
            for bits_value in [0, 1]:
                parameters = self.get_parameters(command, message_type, bits_value)
                msg = f'Command "{command["name"]}" failed on {message_type} instantiation for sub id' \
                      f' {repr(command["type"])} ({hex(command["type"])})'
                class_under_test = self.check_class_instantiation(command, message_type, parameters, msg)
                type_to_checker_map[command["type"]][message_type](a_class=class_under_test, msg=msg)
                report_id_to_checker_map[int(Numeral(class_under_test.report_id))](a_class=class_under_test, msg=msg)
                self.assertEqual(class_under_test.SUB_ID, command["type"], msg)
                self.assertEqual(class_under_test.sub_id, HexList(command["type"]), msg)
                self.assertEqual(class_under_test.address, HexList(command["address"]), msg)
                self.check_field_r0(command, class_under_test, msg)
            # end for
        # end for
    # end def test_commands_instantiation

    def test_parameters_with_dependency(self):
        """
        Test parameters with parsing depending on other parameter
        """
        for command, message_type in self.command_message_type_gen():
            if "parameters" in command[message_type] and command[message_type]["parameters"] is not None:
                for parameter in command[message_type]["parameters"]:
                    if "dependency" in parameter:
                        self.check_parameter_choices(command, message_type, parameter)
                    # end if
                # end for
            # end if
        # end for
    # end def test_parameter_with_dependency

    def command_message_type_gen(self):
        """
        Command with message type generator

        :return: Provide a list with the command and its type
        :rtype: ``generator``
        """
        for command in self.COMMANDS:
            for message_type in ["request", "response"]:
                if message_type in command and command[message_type] is not None:
                    yield command, message_type
                # end if
            # end for
        # end for
    # end def command_message_type_gen

    def check_class_instantiation(self, command, message_type, parameters, msg="Class instantiation failed"):
        """
        Check a class can be instantiated
        """
        try:
            return command[message_type]["class"](**parameters)
        except Exception as e:
            self.fail(f'{msg} with error: {type(e).__name__}: {e}')
        # end try
    # end def check_class_instantiation

    def get_parameters(self, command, message_type, bits_value=0):
        """
        Get expected parameters with all bits set to bit_values for each parameter
        """
        parameters = {}
        if "parameters" in command[message_type] and command[message_type]["parameters"] is not None:
            parameters = {parameter["name"]: self.get_parameter_value(parameter, bits_value)
                          for parameter in command[message_type]["parameters"]}
        # end if
        return parameters
    # end def get_parameters

    @staticmethod
    def get_parameter_value(parameter, bits_value=0):
        """
        Get parameter value
        """
        value = int(str(bits_value) * parameter["len"], 2)
        if "type" in parameter and parameter["type"] is not None:
            if parameter["type"] is HexList:
                value = HexList(str(bits_value) * 2 * (parameter["len"] // 8))
            elif parameter["type"] is str:
                value = HexList.fromString(str(bits_value) * (parameter["len"] // 8))
            # end if
        # end if
        return value
    # end def get_parameter_value

    def check_field_r0(self, command, class_under_test, msg=None):
        """
        Check r0 if relevant
        """
        if "register_0" in command and hasattr(class_under_test, 'r0'):
            if type(command["register_0"]) is tuple:
                # r0 is in a range, so r0 should be an attribute of the class
                self._attributes_checker(class_under_test, [("r0", 8)], msg=msg)
            else:
                self.assertEqual(class_under_test.r0, HexList(command["register_0"]), msg)
            # end if
        # end if
    # end def check_field_r0

    def check_parameter_choices(self, command, message_type, parameter):
        """
        Check different possible choices for a parameter
        """
        for choice_value, choice_details in parameter["dependency"]["choices"].items():
            parameters = self.get_parameters(command, message_type)
            parameters[parameter["dependency"]["on"]] = choice_value
            msg = f'Command "{command["name"]}" failed on {message_type} instantiation for sub id' \
                  f' {repr(command["type"])} ({hex(command["type"])}) with ' \
                  f'{parameter["dependency"]["on"]} = {choice_value}'
            class_under_test = self.check_class_instantiation(command, message_type, parameters, msg)
            self.assertIsInstance(class_under_test.__getattr__(parameter["name"]), choice_details["class"])
            self._attributes_checker(class_under_test.__getattr__(parameter["name"]),
                                     [(par["name"], par["len"]) for par in choice_details["parameters"]],
                                     msg=msg)
        # end for
    # end def check_parameter_choices
# end class RegistersTestCase


# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
