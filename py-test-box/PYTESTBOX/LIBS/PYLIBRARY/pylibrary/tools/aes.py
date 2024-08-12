#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------
"""
    :package: pylibrary
    :brief:  aes encryption class
    :author: Christophe Roquebert
    :date: 2020/06/02
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class Aes:
    """
    AES Algorithm utility class
    """

    @staticmethod
    def aes_cipher(data: HexList, key: HexList, encrypt: bool = True, mode: int = AES.MODE_CFB, iv: HexList = None) -> \
            HexList:
        """
        Cipher the dfu data using the specified AES algorithm.
        Return the encrypted or decrypted buffer.

        :param data: The data buffer to encrypt
        :type data: ``HexList``
        :param key: The project-specific predefined AES DFU encryption key
        :type key: ``HexList``
        :param encrypt: True for encryption, False for decryption
        :type encrypt: ``bool``
        :param mode: AES encryption Mode (MODE_CBC, MODE_CFB and MODE_OFB are supported)
        :type mode: ``int``

        :return: buffer - encrypted or decrypted depending on the'encrypt' parameter value
        :rtype: ``HexList``
        """
        assert(isinstance(data, HexList))
        assert(isinstance(key, HexList))
        key = bytes(key)
        if encrypt:
            if mode == AES.MODE_CBC:
                data = pad(bytes(data), AES.block_size)
            # end if
            if mode == AES.MODE_CFB and iv is not None:
                cipher = AES.new(key, mode, segment_size=AES.block_size * 8, iv=bytes(iv))
            elif mode == AES.MODE_CFB:
                cipher = AES.new(key, mode, segment_size=AES.block_size * 8)
            else:
                # TODO know if the other modes need other paramaters
                cipher = AES.new(key, mode)
            # end if
            ct_bytes = HexList(cipher.encrypt(bytes(data)))
            iv = HexList(cipher.iv)
            buffer = iv + ct_bytes
        else:
            iv = data[:AES.block_size]
            if mode == AES.MODE_CFB:
                cipher = AES.new(key, mode, iv=bytes(iv), segment_size=AES.block_size * 8)
            else:
                # TODO know if the other modes need other paramaters
                cipher = AES.new(key, mode, iv=bytes(iv))
            # end if
            buffer = cipher.decrypt(bytes(data[AES.block_size:]))
            if mode == AES.MODE_CBC:
                buffer = unpad(buffer, AES.block_size)
            # end if
            buffer = HexList(buffer)
        # end if
        assert(isinstance(buffer, HexList))
        return buffer
    # end def aes_cipher
# end class Aes

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
