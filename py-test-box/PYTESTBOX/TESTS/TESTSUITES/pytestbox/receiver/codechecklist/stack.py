#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.receiver.codechecklist.stack
:brief: Device Stack tests
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2022/06/21
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyhid.hidpp.hidpp1.registers.testmodecontrol import TestModeControl
from pylibrary.tools.hexlist import RandHexList
from pytestbox.base.basetest import ReceiverBaseTestCase
from pytestbox.base.loghelper import LogHelper
from pytestbox.receiver.base.receivermanagedeactivatablefeaturesauthutils import \
    ReceiverManageDeactivatableFeaturesAuthTestUtils
from pytestbox.shared.base.bleproreceiverprepairingutils import BleProReceiverPrepairingTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytestbox.shared.base.tdeutils import TDETestUtils
from pytestbox.shared.codechecklist.stack import SharedStackTestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class ReceiverStackTestCase(SharedStackTestCase, ReceiverBaseTestCase):
    """
    Validate Receiver Stack management
    """

    def execute_scenario(self):
        # See ``SharedStackTestCase.execute_scenario``

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Enable Test Mode Control')
        # ---------------------------------------------------------------------------
        TDETestUtils.set_check_test_mode(
            self, test_mode_enable=TestModeControl.TestModeEnable.ENABLE_MANUFACTURING_TEST_MODE)

        # ----------------------------------------------------------------------------
        LogHelper.log_step(self, 'Enable all manufacturing features')
        # ----------------------------------------------------------------------------
        ReceiverManageDeactivatableFeaturesAuthTestUtils.HIDppHelper.enable_features(test_case=self,
                                                                                     manufacturing=True)

        if self.f.RECEIVER.TDE.F_Prepairing:
            self.post_requisite_reload_nvs = True

            self.prepairing_slot = 0x02
            new_device_address = RandHexList(6)
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Generate random keys by the 0xF6 register')
            # ---------------------------------------------------------------------------
            ltk_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
            irk_local_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)
            irk_remote_key = BleProReceiverPrepairingTestUtils.get_randomized_key(self)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, f'Run prepairing sequence')
            # ---------------------------------------------------------------------------
            BleProReceiverPrepairingTestUtils.receiver_prepairing_sequence(
                self, prepairing_slot=self.prepairing_slot, ltk_key=ltk_key,
                irk_local_key=irk_local_key, irk_remote_key=irk_remote_key, device_address=new_device_address)
        # end if

        if self.f.SHARED.PAIRING.F_BLEDevicePairing:
            self.post_requisite_reload_nvs = True

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Run a user pairing sequence')
            # ---------------------------------------------------------------------------
            ble_addr = DiscoveryTestUtils.discover_device(self)
            pairing_slot = DevicePairingTestUtils.pair_device(self, ble_addr)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Unpair the last slot')
            # ---------------------------------------------------------------------------
            DevicePairingTestUtils.unpair_slot(self, pairing_slot=pairing_slot)
        # end if
    # def execute_scenario
# end class ReceiverStackTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
