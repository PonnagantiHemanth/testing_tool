#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package pyhid.tools.test.dfufileparser_test

:brief  PyHid dfu file parser testing module

:author christophe Roquebert

:date   2019/12/05
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList, RandHexList
from pyhid.tools.dfufileparser import DfuFileParser
from Crypto.Cipher import AES
from pylibrary.tools.aes import Aes
from unittest import TestCase

# ------------------------------------------------------------------------------
# constants
# ------------------------------------------------------------------------------
# These modes use a project-specific predefined
# key of a predefined size (128, 192, or 256 bits, as per AES standard)
AES_16_BYTES_LONG_KEY = 16
AES_24_BYTES_LONG_KEY = 24
AES_32_BYTES_LONG_KEY = 32


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class DfuFileParserTestCase(TestCase):                                               # pylint:disable=R0904
    """
    Tests of the DfuFileParser class
    """
    def test_aes_cbc_long_buffer(self):
        """
        Tests aes_cipher method with AES.MODE_CBC and a 128 Bytes buffer
        """
        data = RandHexList(128)
        key = RandHexList(AES_16_BYTES_LONG_KEY)
        cipher_block_cbc = Aes.aes_cipher(data, key, mode=AES.MODE_CBC)
        clear_block_cbc = Aes.aes_cipher(cipher_block_cbc, key, encrypt=False, mode=AES.MODE_CBC)

        self.assertEqual(data,
                         clear_block_cbc,
                         "Inconsistent clear buffer after AES CBC encrypt / decrypt operations !")
    # end def test_aes_cbc_long_buffer

    def test_aes_cbc_not_aligned_buffer(self):
        """
        Tests aes_cipher method with AES.MODE_CBC and an unaligned buffer
        """
        data = RandHexList(129)
        key = RandHexList(AES_16_BYTES_LONG_KEY)
        cipher_block_cbc = Aes.aes_cipher(data, key, mode=AES.MODE_CBC)
        clear_block_cbc = Aes.aes_cipher(cipher_block_cbc, key, encrypt=False, mode=AES.MODE_CBC)

        self.assertEqual(data,
                         clear_block_cbc,
                         "Inconsistent clear buffer after AES CBC encrypt / decrypt operations !")
    # end def test_aes_cbc_not_aligned_buffer

    def test_aes_cbc_very_long_buffer(self):
        """
        Tests aes_cipher method with AES.MODE_CBC and a 75k long buffer
        """
        data = RandHexList(75 * 1024)
        key = RandHexList(AES_16_BYTES_LONG_KEY)
        cipher_block_cbc = Aes.aes_cipher(data, key, mode=AES.MODE_CBC)
        clear_block_cbc = Aes.aes_cipher(cipher_block_cbc, key, encrypt=False, mode=AES.MODE_CBC)

        self.assertEqual(data,
                         clear_block_cbc,
                         "Inconsistent clear buffer after AES CBC encrypt / decrypt operations !")
    # end def test_aes_cbc_very_long_buffer

    def test_aes_cfb_16bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_16_BYTES_LONG_KEY)
        cipher_block = Aes.aes_cipher(data, key)
        clear_block = Aes.aes_cipher(cipher_block, key, encrypt=False)

        self.assertEqual(data,
                         clear_block,
                         "Inconsistent clear buffer after AES CFB encrypt / decrypt operations !")
    # end def test_aes_cfb_16bytes_key

    def test_aes_ofb_16bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_16_BYTES_LONG_KEY)
        cipher_block_ofb = Aes.aes_cipher(data, key, mode=AES.MODE_OFB)
        clear_block_ofb = Aes.aes_cipher(cipher_block_ofb, key, encrypt=False, mode=AES.MODE_OFB)

        self.assertEqual(data,
                         clear_block_ofb,
                         "Inconsistent clear buffer after AES OFB encrypt / decrypt operations !")
    # end def test_aes_ofb_16bytes_key

    def test_aes_cbc_16bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CBC
        """
        data = HexList(b"secret")
        key = RandHexList(AES_16_BYTES_LONG_KEY)
        cipher_block_cbc = Aes.aes_cipher(data, key, mode=AES.MODE_CBC)
        clear_block_cbc = Aes.aes_cipher(cipher_block_cbc, key, encrypt=False, mode=AES.MODE_CBC)

        self.assertEqual(data,
                         clear_block_cbc,
                         "Inconsistent clear buffer after AES CBC encrypt / decrypt operations !")
    # end def test_aes_cbc_16bytes_key

    def test_aes_cfb_24bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_24_BYTES_LONG_KEY)
        cipher_block = Aes.aes_cipher(data, key)
        clear_block = Aes.aes_cipher(cipher_block, key, encrypt=False)

        self.assertEqual(data,
                         clear_block,
                         "Inconsistent clear buffer after AES CFB encrypt / decrypt operations !")
    # end def test_aes_cfb_24bytes_key

    def test_aes_ofb_24bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_24_BYTES_LONG_KEY)
        cipher_block_ofb = Aes.aes_cipher(data, key, mode=AES.MODE_OFB)
        clear_block_ofb = Aes.aes_cipher(cipher_block_ofb, key, encrypt=False, mode=AES.MODE_OFB)

        self.assertEqual(data,
                         clear_block_ofb,
                         "Inconsistent clear buffer after AES OFB encrypt / decrypt operations !")
    # end def test_aes_ofb_24bytes_key

    def test_aes_cbc_24bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_24_BYTES_LONG_KEY)
        cipher_block_cbc = Aes.aes_cipher(data, key, mode=AES.MODE_CBC)
        clear_block_cbc = Aes.aes_cipher(cipher_block_cbc, key, encrypt=False, mode=AES.MODE_CBC)

        self.assertEqual(data,
                         clear_block_cbc,
                         "Inconsistent clear buffer after AES CBC encrypt / decrypt operations !")
    # end def test_aes_cbc_24bytes_key

    def test_aes_cfb_32bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_32_BYTES_LONG_KEY)
        cipher_block = Aes.aes_cipher(data, key)
        clear_block = Aes.aes_cipher(cipher_block, key, encrypt=False)

        self.assertEqual(data,
                         clear_block,
                         "Inconsistent clear buffer after AES CFB encrypt / decrypt operations !")
    # end def test_aes_cfb_32bytes_key

    def test_aes_ofb_32bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_32_BYTES_LONG_KEY)
        cipher_block_ofb = Aes.aes_cipher(data, key, mode=AES.MODE_OFB)
        clear_block_ofb = Aes.aes_cipher(cipher_block_ofb, key, encrypt=False, mode=AES.MODE_OFB)

        self.assertEqual(data,
                         clear_block_ofb,
                         "Inconsistent clear buffer after AES OFB encrypt / decrypt operations !")
    # end def test_aes_ofb_32bytes_key

    def test_aes_cbc_32bytes_key(self):
        """
        Tests aes_cipher method with AES.MODE_CFB
        """
        data = HexList(b"secret")
        key = RandHexList(AES_32_BYTES_LONG_KEY)
        cipher_block_cbc = Aes.aes_cipher(data, key, mode=AES.MODE_CBC)
        clear_block_cbc = Aes.aes_cipher(cipher_block_cbc, key, encrypt=False, mode=AES.MODE_CBC)

        self.assertEqual(data,
                         clear_block_cbc,
                         "Inconsistent clear buffer after AES CBC encrypt / decrypt operations !")
    # end def test_aes_cbc_32bytes_key
# end class DfuFileParserTestCase


if __name__ == '__main__':
    from unittest import main
    main()
# end if


# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
