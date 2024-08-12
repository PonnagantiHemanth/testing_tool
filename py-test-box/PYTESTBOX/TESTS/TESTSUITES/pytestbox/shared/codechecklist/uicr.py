#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
:package: pytestbox.shared.codechecklist.uicr
:brief: Shared Memory tests
:author: Martin Cryonnet <mcryonnet@logitech.com>
:date: 2021/08/24
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from abc import ABC
from os.path import join
from time import perf_counter

from intelhex import IntelHex

from pyharness.extensions import level
from pyharness.selector import features
from pyharness.selector import services
from pyhid.hiddispatcher import HIDDispatcher
from pyhid.hidpp.features.common.wirelessdevicestatus import WirelessDeviceStatusBroadcastEvent
from pylibrary.tools.numeral import Numeral
from pylibrary.tools.numeral import to_int
# noinspection PyUnresolvedReferences
from pysetup import TESTS_PATH
from pytestbox.base.basetest import CommonBaseTestCase
from pytestbox.base.basetestutils import CommonBaseTestUtils
from pytestbox.base.channelutils import ChannelUtils
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.connectionschemeutils import BleProConnectionSchemeTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.devicediscoveryutils import DiscoveryTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class SharedUICRTestCase(CommonBaseTestCase, ABC):
    """
    Validate UICR registers handling
    """
    def setUp(self):
        # See ``CommonBaseTestCase.setUp``
        self.post_requisite_flash_cache = False
        self.post_requisite_reload_uicr_and_nvs = False
        self.post_requisite_reload_device_nvs = False

        # Start with super setUp()
        super().setUp()

        # Stop Task executor
        ChannelUtils.close_channel(test_case=self)

        self.device_firmware_hex_file = join(TESTS_PATH, "DFU_FILES", self.f.PRODUCT.FEATURES.COMMON.DFU.F_HexFileName)

        # ------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup DUT initial NVS")
        # ------------------------------------------------------------------------
        CommonBaseTestUtils.NvsHelper.backup_nvs(self)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, 'Get DUT initial AES Encryption key')
        # ---------------------------------------------------------------------------
        self.initial_aes_local_key = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY, self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
    # end def setUp

    def tearDown(self):
        # See ``CommonBaseTestCase.tearDown``
        with self.manage_post_requisite():
            # Stop Task executor
            ChannelUtils.close_channel(test_case=self)
            
            if self.post_requisite_reload_uicr_and_nvs:
                # ---------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload DUT initial NVS and UICR')
                # ---------------------------------------------------------------------------
                nvs_intel_hex = self.memory_manager.backup_nvs_parser.to_hex_file()
                aes_key_addresses = range(
                    self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY,
                    self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY + self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
                aes_key_intel_hex = IntelHex(dict(zip(aes_key_addresses, self.initial_aes_local_key)))
                firmware_intel_hex = IntelHex(self.device_firmware_hex_file)
                firmware_intel_hex.merge(nvs_intel_hex, overlap='replace')
                firmware_intel_hex.merge(aes_key_intel_hex, overlap='replace')
                self.memory_manager.debugger.erase_and_flash_firmware(firmware_intel_hex)
            elif self.post_requisite_reload_device_nvs and self.device_memory_manager is not None:
                # ---------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Reload Device initial NVS')
                # ---------------------------------------------------------------------------
                self.device_memory_manager.load_nvs(backup=True)
            # end if

            if self.post_requisite_flash_cache:
                # ---------------------------------------------------------------------------
                LogHelper.log_post_requisite(self, 'Restore debugger cache configuration')
                # ---------------------------------------------------------------------------
                self.memory_manager.debugger.stop()
                self.memory_manager.debugger.exclude_flash_cache_range(
                    self.memory_manager.debugger.NVS_START_ADDRESS,
                    self.memory_manager.debugger.NVS_START_ADDRESS + self.memory_manager.debugger.NVS_SIZE)
                self.memory_manager.debugger.reset()
            # end if

            ChannelUtils.wait_for_channel_device_to_be_connected(test_case=self)
            ChannelUtils.clean_messages(test_case=self, queue_name=HIDDispatcher.QueueName.EVENT,
                                        class_type=WirelessDeviceStatusBroadcastEvent)
        # end with
        super().tearDown()
    # end def tearDown

    @features('NVSEncryption')
    @level('Functionality')
    @services('Debugger')
    def test_random_aes_encryption_key(self):
        """
        Check AES Encryption key is random
        """
        samples_count = 17
        aes_keys = []
        self.post_requisite_reload_uicr_and_nvs = True
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude Encryption key from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY,
            self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY + self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
        self.memory_manager.debugger.run()

        LogHelper.log_info(self, f'Loop over {samples_count} samples')
        start_time = perf_counter()
        for _ in range(samples_count):
            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Read AES Encryption Key')
            # ---------------------------------------------------------------------------
            aes_local_key = self.memory_manager.debugger.readMemory(
                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY, self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)

            # ---------------------------------------------------------------------------
            LogHelper.log_check(self, 'Check each key is unique')
            # ---------------------------------------------------------------------------
            self.assertNotIn(aes_local_key, aes_keys, "New key should not be equal to one of the previous one")
            aes_keys.append(aes_local_key)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Reload default firmware')
            # ---------------------------------------------------------------------------
            self.memory_manager.debugger.erase_and_flash_firmware(self.device_firmware_hex_file)
            self.memory_manager.debugger.exclude_flash_cache_range(
                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY,
                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY + self.memory_manager.SIZE.NVS_ENCRYPTION_KEY)
            self.memory_manager.debugger.reset(soft_reset=False)
        # end for
        end_time = perf_counter()
        LogHelper.log_info(
            self, f'End Test Loop : {samples_count} loops in {end_time - start_time}s')

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check each bit changes at least once')
        # ---------------------------------------------------------------------------
        all_ones = int('FF' * self.memory_manager.SIZE.NVS_ENCRYPTION_KEY, 16)
        key_index = 0
        result_and = int(Numeral(aes_keys[key_index]))
        result_or = int(Numeral(aes_keys[key_index]))
        while (result_and != 0 or result_or != all_ones) and key_index < len(aes_keys) - 1:
            key_index += 1
            result_and &= int(Numeral(aes_keys[key_index]))
            result_or |= int(Numeral(aes_keys[key_index]))
        # end while
        LogHelper.log_info(self, f'Loop exits after {key_index} keys')
        self.assertEqual(0, result_and, "And result should be 0 because each bit should be 0 at least once")
        self.assertEqual(
            all_ones, result_or, f'Or result should be {all_ones} because each bit should be 1 at least once')

        self.testCaseChecked("FUN_UICR_0001")
    # end def test_random_aes_encryption_key

    @features('UICR')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_bootloader_address(self):
        """
        Check Bootloader Address in UICR
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude Bootloader address from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.BOOTLOADER_ADDRESS,
            self.memory_manager.ADDRESS.BOOTLOADER_ADDRESS + self.memory_manager.SIZE.BOOTLOADER_ADDRESS)
        self.memory_manager.debugger.run()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read Bootloader Address')
        # ---------------------------------------------------------------------------
        bootloader_address = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.BOOTLOADER_ADDRESS, self.memory_manager.SIZE.BOOTLOADER_ADDRESS)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check Bootloader address')
        # ---------------------------------------------------------------------------
        self.assertEqual(Numeral(self.config_manager.get_feature(self.config_manager.ID.BOOTLOADER_ADDRESS)),
                         Numeral(bootloader_address, littleEndian=True),
                         "Bootloader Address should be as expected")

        self.testCaseChecked("FUN_UICR_0002")
    # end def test_uicr_bootloader_address

    @features('UICR')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_pselreset(self):
        """
        Check PSELRESET[0] and PSELRESET[1] registers in UICR
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude PSELRESET from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.PSELRESET_0,
            self.memory_manager.ADDRESS.PSELRESET_1 + self.memory_manager.SIZE.UICR_REGISTER)
        self.memory_manager.debugger.run()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read PSELRESET[0]')
        # ---------------------------------------------------------------------------
        pselreset_0 = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.PSELRESET_0, self.memory_manager.SIZE.UICR_REGISTER)

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read PSELRESET[1]')
        # ---------------------------------------------------------------------------
        pselreset_1 = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.PSELRESET_1, self.memory_manager.SIZE.UICR_REGISTER)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check all PSELRESET registers contain the same value')
        # ---------------------------------------------------------------------------
        self.assertEqual(
            pselreset_0,
            pselreset_1,
            "All PSELRESET registers have to contain the same value for a pin mapping to be valid.")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check PSELRESET[0] value')
        # ---------------------------------------------------------------------------
        self.assertEqual(
            Numeral(self.f.PRODUCT.NVS_UICR.F_PSELRESET),
            Numeral(pselreset_0, littleEndian=True),
            "PSELRESET[0] should be as expected")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check PSELRESET[1] value')
        # ---------------------------------------------------------------------------
        self.assertEqual(
            Numeral(self.f.PRODUCT.NVS_UICR.F_PSELRESET),
            Numeral(pselreset_1, littleEndian=True),
            "PSELRESET[1] should be as expected")

        self.testCaseChecked("FUN_UICR_0003")
    # end def test_uicr_pselreset

    @features('UICR')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_customer(self):
        """
        Check Customer registers in UICR
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude Customer registers from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.CUSTOMER_0,
            self.memory_manager.ADDRESS.CUSTOMER_0 + self.memory_manager.SIZE.UICR_REGISTER *
            self.memory_manager.ADDRESS.N_CUSTOMER_REGISTERS)
        self.memory_manager.debugger.run()

        used_registers = []
        if self.f.PRODUCT.NVS_UICR.F_NVSEncryption:
            used_registers.extend([
                self.memory_manager.ADDRESS.NVS_ENCRYPTION_KEY + i * self.memory_manager.SIZE.UICR_REGISTER
                for i in range(self.memory_manager.SIZE.NVS_ENCRYPTION_KEY // self.memory_manager.SIZE.UICR_REGISTER)])
        # end if
        if self.f.PRODUCT.NVS_UICR.F_MagicNumber:
            # Exclude Customer[31] register from the following check procedure
            used_registers.extend([self.memory_manager.ADDRESS.MAGIC_NUMBER])
        # end if

        customer = [None] * self.memory_manager.ADDRESS.N_CUSTOMER_REGISTERS
        for i in range(self.memory_manager.ADDRESS.N_CUSTOMER_REGISTERS):
            address = self.memory_manager.ADDRESS.CUSTOMER_0 + i * self.memory_manager.SIZE.UICR_REGISTER
            if address not in used_registers:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, f'Read Customer[{i}] register')
                # ---------------------------------------------------------------------------
                customer[i] = self.memory_manager.debugger.readMemory(address, self.memory_manager.SIZE.UICR_REGISTER)

                # ---------------------------------------------------------------------------
                LogHelper.log_check(self, f'Check CUSTOMER[{i}] value')
                # ---------------------------------------------------------------------------
                self.assertEqual(Numeral(self.memory_manager.UICR_REGISTER_RESET_VALUE),
                                 Numeral(customer[i], littleEndian=True),
                                 f"Customer[{i}] should be as expected")
            else:
                LogHelper.log_info(self, f'Customer[{i}] register is used')
            # end if
        # end for

        self.testCaseChecked("FUN_UICR_0004")
    # end def test_uicr_customer

    @features('UICR')
    @features('UicrMagicNumber')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_magic_number(self):
        """
        Check Customer[31] register in UICR which stores a magic number used to ensure UICR programming
        cf https://goldenpass.logitech.com:8443/c/ccp_fw/quark/+/9153
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude Customer registers from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        magic_number_address = self.memory_manager.ADDRESS.MAGIC_NUMBER
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            magic_number_address, magic_number_address + self.memory_manager.SIZE.UICR_REGISTER)
        self.memory_manager.debugger.run()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read Customer[31] (Magic Number) register')
        # ---------------------------------------------------------------------------
        magic_number = self.memory_manager.debugger.readMemory(
            magic_number_address, self.memory_manager.SIZE.UICR_REGISTER)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, f'Check UICR Magic Number (i.e. CUSTOMER[31] register) value')
        # ---------------------------------------------------------------------------
        self.assertEqual(Numeral(self.memory_manager.UICR_REGISTER_MAGIC_NUMBER),
                         Numeral(magic_number, littleEndian=True),
                         "UICR Magic Number (i.e. CUSTOMER[31] register) should be as expected")

        self.testCaseChecked("FUN_UICR_0009")
    # end def test_uicr_magic_number

    @features('UicrNfcPins')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_nfcpins(self):
        """
        Check NFCPINS register in UICR
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude NFCPINS from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.NFCPINS,
            self.memory_manager.ADDRESS.NFCPINS + self.memory_manager.SIZE.UICR_REGISTER)
        self.memory_manager.debugger.run()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read NFCPINS')
        # ---------------------------------------------------------------------------
        nfcpins = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.NFCPINS, self.memory_manager.SIZE.UICR_REGISTER)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check NFCPINS')
        # ---------------------------------------------------------------------------
        self.assertEqual(Numeral(self.f.PRODUCT.NVS_UICR.F_NFCPINS),
                         Numeral(nfcpins, littleEndian=True),
                         "NFCPINS register should be as expected")

        self.testCaseChecked("FUN_UICR_0005")
    # end def test_uicr_nfcpins

    @features('UicrRegout0')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_regout0(self):
        """
        Check REGOUT0 register in UICR
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude REGOUT0 from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.REGOUT0,
            self.memory_manager.ADDRESS.REGOUT0 + self.memory_manager.SIZE.UICR_REGISTER)
        self.memory_manager.debugger.run()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read REGOUT0')
        # ---------------------------------------------------------------------------
        regout0 = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.REGOUT0, self.memory_manager.SIZE.UICR_REGISTER)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check REGOUT0')
        # ---------------------------------------------------------------------------
        self.assertEqual(Numeral(self.f.PRODUCT.NVS_UICR.F_REGOUT0),
                         Numeral(regout0, littleEndian=True),
                         "REGOUT0 register should be as expected")

        self.testCaseChecked("FUN_UICR_0006")
    # end def test_uicr_regout0

    @features('UicrDebugCtrl')
    @level('Functionality')
    @services('Debugger')
    def test_uicr_debugctrl(self):
        """
        Check DEBUGCTRL register in UICR
        """
        self.post_requisite_flash_cache = True

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(
            self, 'Exclude DEBUGCTRL from debugger cache, to force new memory read from device each time')
        # ---------------------------------------------------------------------------
        self.memory_manager.debugger.stop()
        self.memory_manager.debugger.exclude_flash_cache_range(
            self.memory_manager.ADDRESS.DEBUGCTRL,
            self.memory_manager.ADDRESS.DEBUGCTRL + self.memory_manager.SIZE.UICR_REGISTER)
        self.memory_manager.debugger.run()

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, 'Read DEBUGCTRL')
        # ---------------------------------------------------------------------------
        debugctrl = self.memory_manager.debugger.readMemory(
            self.memory_manager.ADDRESS.DEBUGCTRL, self.memory_manager.SIZE.UICR_REGISTER)

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check DEBUGCTRL')
        # ---------------------------------------------------------------------------
        self.assertEqual(Numeral(self.f.PRODUCT.NVS_UICR.F_DEBUGCTRL),
                         Numeral(debugctrl, littleEndian=True),
                         "DEBUGCTRL register should be as expected")

        self.testCaseChecked("FUN_UICR_0007")
    # end def test_uicr_debugctrl

    @features('NVSEncryption')
    @features('BLEDevicePairing')
    @level('Functionality')
    @services('Debugger')
    def test_chunk_iv_randomness(self):
        """
        Check Initialisation Vector is unique for each chunk
        """
        samples_count = 16

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Initialize the authentication method parameter")
        # ---------------------------------------------------------------------------
        DevicePairingTestUtils.set_authentication_method(self, self.config_manager)

        # ---------------------------------------------------------------------------
        LogHelper.log_prerequisite(self, "Backup DUT initial NVS")
        # ---------------------------------------------------------------------------
        self.device_memory_manager.read_nvs(backup=True)
        self.last_ble_address = DeviceBaseTestUtils.NvsHelper.get_last_gap_address(
            test_case=self, memory_manager=self.device_memory_manager)
        self.post_requisite_reload_device_nvs = True

        # ---------------------------------------------------------------------------
        LogHelper.log_step(self, "Get BLE Bond Id chunks")
        # ---------------------------------------------------------------------------
        chunks_list = self.memory_manager.get_ble_bond_id_chunks()

        # Cleanup all pairing slots except the first one
        CommonBaseTestUtils.NvsHelper.clean_pairing_data(self)
        # Cleanup all receiver pairing slots except the first one
        DevicePairingTestUtils.NvsManager.clean_pairing_data(self)

        loop_count = samples_count
        device_index = None
        while len(chunks_list) < samples_count and loop_count > 0:
            loop_count -= 1

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Force the device first pairing channel in unpaired state')
            # ---------------------------------------------------------------------------
            BleProConnectionSchemeTestUtils.NvsHelper.unpair_host(self, host_index=0)

            ChannelUtils.open_channel(test_case=self)
            ChannelUtils.set_hidpp_reporting(test_case=self, enable=True)

            if device_index is not None:
                # ---------------------------------------------------------------------------
                LogHelper.log_step(self, "Unpair slot in receiver")
                # ---------------------------------------------------------------------------
                DevicePairingTestUtils.unpair_slot(self, to_int(device_index))
            # end if

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, 'Pair device to add pairing chunks')
            # ---------------------------------------------------------------------------
            ble_addr = DiscoveryTestUtils.discover_device(self, trigger_user_action=False)
            device_index = DevicePairingTestUtils.pair_device(self, ble_addr)

            # Stop Task executor
            ChannelUtils.close_channel(test_case=self)

            # ---------------------------------------------------------------------------
            LogHelper.log_step(self, "Get new BLE Bond Id chunks")
            # ---------------------------------------------------------------------------
            self.memory_manager.read_nvs()
            chunks_list.extend(self.memory_manager.get_ble_bond_id_chunks(pairing_slot=None,
                                                                          bluetooth_address=ble_addr))
        # end while

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, "Check each IV is unique")
        # ---------------------------------------------------------------------------
        chunks_ivs = [int.from_bytes(chunk.ref.iv, byteorder='big') for chunk in chunks_list]
        self.assertEqual(len(chunks_list),
                         len(set(chunks_ivs)),
                         "Each chunk should have a unique Initialisation Vector for AES encryption")

        # ---------------------------------------------------------------------------
        LogHelper.log_check(self, 'Check each bit changes at least once')
        # ---------------------------------------------------------------------------
        all_ones = int('FF' * len(chunks_list[0].ref.iv), 16)
        chunk_index = 0
        result_and = int(Numeral(chunks_ivs[chunk_index]))
        result_or = int(Numeral(chunks_ivs[chunk_index]))
        while (result_and != 0 or result_or != all_ones) and chunk_index < len(chunks_ivs) - 1:
            chunk_index += 1
            result_and &= int(Numeral(chunks_ivs[chunk_index]))
            result_or |= int(Numeral(chunks_ivs[chunk_index]))
        # end while
        LogHelper.log_info(self, f'Loop exits after {chunk_index} chunks')
        self.assertEqual(0, result_and, "And result should be 0 because each bit should be 0 at least once")
        self.assertEqual(
            all_ones, result_or, f'Or result should be {all_ones} because each bit should be 1 at least once')

        self.testCaseChecked("FUN_UICR_0008")
    # end def test_chunk_iv_randomness
# end class SharedUICRTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
