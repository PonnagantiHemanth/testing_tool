# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:package: logidevice.example.batterylevelscalibration
:brief:   Example of logidevicehandler to do battery calibration.
:author:  YY Liu  <yliu5@logitech.com>
:date:    2022/07/01
"""
# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
import sys
from os import path
from sys import stdout

FILE_PATH = path.abspath(__file__)
WS_DIR = FILE_PATH[:FILE_PATH.rfind("TESTS")]
TOOLS_DIR = path.join(WS_DIR, "TESTS", "TOOLS")
PYTRANSPORT_DIR = path.join(WS_DIR, "LIBS", "PYTRANSPORT")
if TOOLS_DIR not in sys.path:
    sys.path.insert(0, TOOLS_DIR)
# end if
if PYTRANSPORT_DIR not in sys.path:
    sys.path.insert(0, PYTRANSPORT_DIR)
# end if
from logidevice.logidevicehandler import LogiDeviceHandler
from pytransport.usb.usbconstants import LogitechReceiverProductId
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibration
from pyhid.hidpp.features.common.batterylevelscalibration import BatteryLevelsCalibrationModel
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuth
from pyhid.hidpp.features.common.managedeactivatablefeaturesauth import ManageDeactivatableFeaturesAuthModel
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthentication
from pyhid.hidpp.features.common.passwordauthentication import PasswordAuthenticationModel
from pyhid.hidpp.features.enablehidden import EnableHidden
from pyhid.hidpp.features.enablehidden import EnableHiddenModel
from pylibrary.tools.hexlist import HexList
from pytestbox.device.base.passwordauthenticationutils import DevicePasswordAuthenticationTestUtils


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------
# HERZOG
# PID = 'C52B'
# Herzog
# TID = '4082'
# Zaha
# TID = '4090'

# G502 Hyjal
# PID = 'C07D'
# TID = ('C07D',)

# G705 Garnet
# PID = 'C547'
# TID = ('409D',)

# Artanis
# PID = 'C547'
# TID = ('4099',)

# Bazooka2
PID = 'C54D'
TID = ('40A9',)


def battery_levels_calibration(pid, tid):
    """
    Run battery levels calibration from DUT via logidevicehandler.

    :param pid: The product ID of the device. None for the default PID(HERZOG).
    :type pid: ``str`` or ``None``
    :param tid: The transpose ID of the device. None for the default TID(HERZOG).
    :type tid: ``tuple`` or ``None``
    """
    feature_id_1e00 = EnableHidden.FEATURE_ID
    feature_id_1602 = PasswordAuthentication.FEATURE_ID
    feature_id_1e02 = ManageDeactivatableFeaturesAuth.FEATURE_ID
    feature_id_1861 = BatteryLevelsCalibration.FEATURE_ID

    for i in range(1):
        with LogiDeviceHandler(pid=pid, tid=tid) as handler:
            # Enable Hidden feature
            result = handler.send_message(feature_id=feature_id_1e00,
                                          function_id=EnableHiddenModel.INDEX.SET_ENABLE_HIDDEN_FEATURES,
                                          enable_byte=EnableHidden.ENABLED)
            stdout.write(f'0x1E00 response = {result}\n')

            if int(PID, 16) == LogitechReceiverProductId.SAVITUCK:
                # Start session x1E02_Manuf
                session_name = HexList.fromString(
                    DevicePasswordAuthenticationTestUtils.AccountNames.MANUFACTURING.value)
                result = handler.send_message(feature_id=feature_id_1602,
                                              function_id=PasswordAuthenticationModel.INDEX.START_SESSION,
                                              name=session_name)
                stdout.write(f'x1E02_Manuf response = {result}\n')

                # Send Password 0
                result = handler.send_message(
                    feature_id=feature_id_1602, function_id=PasswordAuthenticationModel.INDEX.PASSWD0,
                    passwd=HexList(handler.framework_adapter.PASSWORD_MANUF))
                stdout.write(f'Password0 response = {result}\n')

                # Manage deactivatable features
                result = handler.send_message(
                    feature_id=feature_id_1e02, function_id=ManageDeactivatableFeaturesAuthModel.INDEX.ENABLE_FEATURES,
                    enable_all_bit="False", enable_gothard="False",
                    enable_compliance="False", enable_manufacturing="True")
                stdout.write(f'Enable manufacturing response = {result}\n')
            # end if

            # Cutoff control - cutoff disabled
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.CUT_OFF_CONTROL,
                                          cutoff_change_state_requested="True", cutoff_desired_state="True")
            stdout.write(f'cutoff control response = {result}\n')

            # Get battery calibration info
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.GET_BATTERY_CALIBRATION_INFO)
            stdout.write(f'get battery calibration info response = {result}\n')

            # Measure battery
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.MEASURE_BATTERY)
            stdout.write(f'measured battery response = {result}\n')

            # Read calibration
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.READ_CALIBRATION)
            stdout.write(f'read calibration response = {result}\n')

            # Store calibration
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.STORE_CALIBRATION,
                                          calibration_points_nb=result['calibration_points_nb'],
                                          calibration_point_0=result['calibration_point_0'],
                                          calibration_point_1=result['calibration_point_1'])
            stdout.write(f'store calibration response = {result}\n')

            # Read calibration
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.READ_CALIBRATION)
            stdout.write(f'read calibration response = {result}\n')

            # Cutoff control - cutoff enabled
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.CUT_OFF_CONTROL,
                                          cutoff_change_state_requested="True", cutoff_desired_state="False")
            stdout.write(f'cutoff control response = {result}\n')

            # Set battery source info
            result = handler.send_message(feature_id=feature_id_1861,
                                          function_id=BatteryLevelsCalibrationModel.INDEX.SET_BATTERY_SOURCE_INFO,
                                          battery_source_index=1)
            stdout.write(f'set battery source info response = {result}\n')
        # end with
    # end for
# end def battery_levels_calibration


if __name__ == '__main__':
    battery_levels_calibration(pid=PID, tid=TID)
# end if

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
