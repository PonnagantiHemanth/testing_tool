#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Box
# ------------------------------------------------------------------------------
"""
    :package: pyhid.mcu.nrf52.test.blenvschunks_test
    :brief:  NVS BLE chunk test module
    :author: Christophe Roquebert
    :date: 2020/06/15
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.mcu.nrf52.bleproprepairingchunk import BleProPrePairingNvsChunk
from pylibrary.tools.hexlist import HexList, RandHexList
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BleProPrePairingNvsChunkTestCase(TestCase):
    """
    Ble Pro Pre-Pairing Nvs Chunk testing class
    """

    def test_ble_pro_prepairing_irk_and_csrk_nvs_chunk(self):
        """
        Tests BleProPrePairingNvsChunk class instantiation
        """
        my_class = BleProPrePairingNvsChunk.fromHexList(HexList(
            "EF"
            "11111111111111111111111111111111"
            "222222222222"
            "33333333333333333333333333333333"
            "44444444444444444444444444444444"
            "555555555555"
            "66666666666666666666666666666666"
            "77777777777777777777777777777777"))
        assert(my_class.key_map == HexList("EF"))
        assert(my_class.long_term_key == HexList("11111111111111111111111111111111"))
        assert(my_class.keys.local_address == HexList("222222222222"))
        assert(my_class.keys.local_identity_resolving_key == HexList("33333333333333333333333333333333"))
        assert(my_class.keys.local_connection_signature_resolving_key == HexList("44444444444444444444444444444444"))
        assert(my_class.keys.remote_address == HexList("555555555555"))
        assert(my_class.keys.remote_identity_resolving_key == HexList("66666666666666666666666666666666"))
        assert(my_class.keys.remote_connection_signature_resolving_key == HexList("77777777777777777777777777777777"))
    # end def test_ble_pro_prepairing_irk_and_csrk_nvs_chunk


    def test_ble_pro_prepairing_irk_nvs_chunk(self):
        """
        Tests BleProPrePairingNvsChunk class instantiation
        """
        my_class = BleProPrePairingNvsChunk.fromHexList(HexList(
            "67"
            "11111111111111111111111111111111"
            "222222222222"
            "33333333333333333333333333333333"
            "555555555555"
            "66666666666666666666666666666666"))
        assert(my_class.key_map == HexList("67"))
        assert(my_class.long_term_key == HexList("11111111111111111111111111111111"))
        assert(my_class.keys.local_address == HexList("222222222222"))
        assert(my_class.keys.local_identity_resolving_key == HexList("33333333333333333333333333333333"))
        assert(my_class.keys.remote_address == HexList("555555555555"))
        assert(my_class.keys.remote_identity_resolving_key == HexList("66666666666666666666666666666666"))
    # end def test_ble_pro_prepairing_irk_nvs_chunk

# end class BleProPrePairingNvsChunkTestCase
