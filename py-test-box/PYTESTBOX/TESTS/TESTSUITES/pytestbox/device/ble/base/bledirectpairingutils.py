#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------------------------------------------------
# Python Test Box
# ----------------------------------------------------------------------------------------------------------------------
"""
:package: pytestbox.device.ble.base.bledirectpairingutils
:brief: Helpers for BLE pairings in BLE direct mode
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/04/11
"""

# ----------------------------------------------------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------------------------------------------------
from time import sleep

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.ec import ECDH
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.ciphers.algorithms import AES
from cryptography.hazmat.primitives.ciphers.modes import ECB
from cryptography.hazmat.primitives.hashes import Hash
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.hmac import HMAC
from math import ceil

from pyharness.core import TYPE_ERROR
from pyharness.core import TestException
from pylibrary.emulator.keyid import KEY_ID
from pylibrary.tools.hexlist import HexList
from pyraspi.services.keyboardemulator import NUMBER_TO_KEYBOARD_KEY_ID_MAP
from pytestbox.base.loghelper import LogHelper
from pytestbox.device.base.bleprotocolutils import BleProtocolTestUtils
from pytestbox.device.base.devicebasetestutils import DeviceBaseTestUtils
from pytestbox.shared.base.devicepairingutils import DevicePairingTestUtils
from pytransport.ble.bleconstants import BleSmpKeypress
from pytransport.ble.bleconstants import BleUuidStandardService
from pytransport.ble.bleconstants import GoogleFastPairCharacteristic
from pytransport.ble.bleinterfaceclasses import BleUuid

# ----------------------------------------------------------------------------------------------------------------------
# constants
# ----------------------------------------------------------------------------------------------------------------------
PASSKEY_IN_DIGITS = 6


# ----------------------------------------------------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------------------------------------------------

class FastPairWallet:
    """
    Wallet for all the fast pair related keys
    """
    def __init__(self):
        self.private_key = None
        self.public_key = None
        self.ecdh_shared_key = None
        self.ecdh_shared_key = None
        self.aes_128_anti_spoofing_key = None
    # end def __init__
    
    def reset(self):
        """
        Reset all the keys to the initial None values
        """
        self.private_key = None
        self.public_key = None
        self.ecdh_shared_key = None
        self.ecdh_shared_key = None
        self.aes_128_anti_spoofing_key = None
    # end def reset
# end class FastPairWallet

class BleDirectPairingUtils(DeviceBaseTestUtils):
    """
    Test utils for BLE Direct pairing (applicable to device targets only)
    """

    @classmethod
    def clean_pairing_events(cls, test_case, ble_context_device=None):
        """
        Clean the pairing event queue of the selected device

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Device to clean the queue from - OPTIONAL
        :type ble_context_device: ``BleContextDevice`` or ``None``
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case)
        ble_context_device = test_case.current_device if ble_context_device is None else ble_context_device

        while ble_context.get_pairing_event(ble_context_device, block=False) is not None:
            pass
        # end while
    # end def clean_pairing_events

    @classmethod
    def fail_pairing(cls, test_case, ble_context_device):
        """
        Fail a pairing in ble.

        procedure: start a keypass pairing and immediately confirm it without a passkey

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param ble_context_device: Device to fail pairing
        :type ble_context_device: ``BleContextDevice``
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case)

        ble_context.authenticate_keypress_start(ble_context_device=ble_context_device)

        assert KEY_ID.KEYBOARD_RETURN_ENTER in test_case.button_stimuli_emulator.get_key_id_list()
        
        test_case.button_stimuli_emulator.keystroke(KEY_ID.KEYBOARD_RETURN_ENTER)
    # end def fail_pairing

    @classmethod
    def generate_keystrokes(cls, test_case, passkey_digits, end=-1, start=None, log_check=False,
                            digit_to_ignore_display_key_check=None):
        """
        Emulate a series of keystrokes depending on a provided passkey digits

        :param test_case: The current test case
        :type test_case: ``pytestbox.base.basetest.CommonBaseTestCase``
        :param passkey_digits: sequence of six digits
        :type passkey_digits: ``int``
        :param start: first digit to consider in the keystroke sequence in [5..0] (default is 5) - OPTIONAL
        :type start: ``int``
        :param end: last digit to consider in the keystroke sequence in [4..-1] (default is -1) - OPTIONAL
        :type end: ``int``
        :param log_check: Flag indicating if a log for the check should be added - OPTIONAL
        :type log_check: ``bool``
        :param digit_to_ignore_display_key_check: The digit starts to ignore DisplayKey Key notification
                                                  checking - OPTIONAL
        :type digit_to_ignore_display_key_check: ``int``
        """
        ble_context = BleProtocolTestUtils.get_ble_context(test_case)
        start_max = PASSKEY_IN_DIGITS - 1
        start = start_max if start is None else start 
        assert (0 <= start <= start_max)
        assert (-1 <= end < start_max)
        assert (end < start)
        cls.clean_pairing_events(test_case)

        # --------------------------------------------------------------------------------------------------------------
        LogHelper.log_info(test_case=test_case, msg="Generate keystrokes "
                                                    f"{f'{passkey_digits:06d}'[start-PASSKEY_IN_DIGITS:end]}")
        # --------------------------------------------------------------------------------------------------------------
        for index in range(start, end, -1):
            digit_value = (passkey_digits // (10 ** index)) % 10
            test_case.button_stimuli_emulator.keystroke(
                key_id=NUMBER_TO_KEYBOARD_KEY_ID_MAP[digit_value])

            if log_check:
                # ------------------------------------------------------------------------------------------------------
                LogHelper.log_check(test_case=test_case, text="Wait for a 'Digit In' passkey notification")
                # ------------------------------------------------------------------------------------------------------
            # end if

            if digit_to_ignore_display_key_check is None or index > digit_to_ignore_display_key_check:
                event = ble_context.get_pairing_event(test_case.current_device)

                test_case.assertEqual(expected=BleSmpKeypress.PASSKEY_DIGIT_ENTERED,
                                      obtained=event,
                                      msg=f"No digit entered notification received. Received {repr(event)}")
            # end if
            # Add a delay between 2 keystrokes
            sleep(DevicePairingTestUtils.KEYSTROKE_INTERVAL)
        # end for
    # end def generate_keystrokes

    @classmethod
    def get_fast_pair_test_keys(cls, test_case):
        """
        Get keys for fast pair decoding, store them in the test case object

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        """
        if not hasattr(test_case, "fast_pair_wallet"):
            setattr(test_case, "fast_pair_wallet", FastPairWallet())
        # end if
        
        if test_case.fast_pair_wallet.private_key is None:
            test_case.fast_pair_wallet.reset()
            key = cls.FastPairCryptographyHelper.generate_seeker_test_private_key()
            test_case.fast_pair_wallet.private_key = key
            test_case.fast_pair_wallet.public_key = key.public_key()
        # end if

        if test_case.fast_pair_wallet.ecdh_shared_key is None:
            key = cls.FastPairCryptographyHelper.key_exchange(test_case.private_key,
                                                              test_case.dut_fast_pair_public_key)
            test_case.fast_pair_wallet.ecdh_shared_key = key
        # end if

        if test_case.fast_pair_wallet.aes_128_anti_spoofing_key is None:
            key = cls.FastPairCryptographyHelper.generate_aes_128_anti_spoofing_key(test_case.ecdh_shared_key)
            test_case.fast_pair_wallet.aes_128_anti_spoofing_key = key
        # end if
    # end def get_fast_pair_test_keys

    @classmethod
    def fast_pair_write_key_pairing_characteristic(cls, test_case, message, append_public_key, shared_key=None):
        """
        Write encrypted message on the Google fast pair pairing characteristic

        :param test_case: Test case object
        :type test_case: ``DeviceBaseTestCase``
        :param message: message to send, in plain text
        :type message: ``HexList``
        :param append_public_key: flag indicating if the public key is to be appended to the sent message
        :type append_public_key: ``bool``
        :param shared_key: Shared key to encrypt the message with, by default use the one stored in the test case object
        :type shared_key: ``bytes``
        """
        try:
            aes_key = shared_key if shared_key is not None else test_case.fast_pair_wallet.aes_128_anti_spoofing_key
            public_key = test_case.fast_pair_wallet.public_key
        except AttributeError:
            raise TestException(TYPE_ERROR, "Fast pair keys not found. use the ``get_fast_pair_test_keys`` "
                                            "method before calling this one")
        # end try

        cipher_text = BleDirectPairingUtils.FastPairCryptographyHelper.encrypt_single_block_aes(
            aes_key, bytes(message))

        public_key_bytes = BleDirectPairingUtils.FastPairCryptographyHelper.encode_public_key_for_key_based_paring(
            public_key)

        if append_public_key:
            payload = HexList(cipher_text) + public_key_bytes
        else:
            payload = HexList(cipher_text)
        # end if
        BleProtocolTestUtils.write_characteristic(test_case, test_case.current_device,
                                                  service_uuid=BleUuid(BleUuidStandardService.GOOGLE_FAST_PAIR),
                                                  characteristic_uuid=BleProtocolTestUtils.build_128_bits_uuid(
                                                      GoogleFastPairCharacteristic.KEY_BASED_PAIRING),
                                                  value=payload)
    # end def fast_pair_write_key_pairing_characteristic

    class FastPairCryptographyHelper:
        """
        Helper class for fast pair cryptographic needs
        """

        @staticmethod
        def generate_seeker_test_private_key():
            """
            Generate a private key for the fast pair seeker role, uses the SECP256R1 elliptic curve

            :return: private key object
            :rtype: ``ec.EllipticCurvePrivateKey``
            """

            return ec.generate_private_key(ec.SECP256R1())
        # end def generate_seeker_test_private_key

        @staticmethod
        def key_exchange(private_key, peer_public_key):
            """
            Get the shared key from a private key and a peer public key

            :param private_key: private key part of the exchange
            :type private_key: ``ec.EllipticCurvePrivateKey``
            :param peer_public_key: public key part of the exchange
            :type peer_public_key: ``ec.EllipticCurvePublicKey``
            
            :return: private key value
            :rtype: ``bytes``
            """
            return private_key.exchange(ECDH(), peer_public_key=peer_public_key)
        # end def key_exchange

        @staticmethod
        def generate_aes_128_anti_spoofing_key(shared_key):
            """
            Generate an AES anti spoofing key from a shared key.

            1. Make a SHA256 hash of the shared key
            2. Take the first 128 bits

            source: https://developers.google.com/nearby/fast-pair/specifications/service/gatt
            Procedure step 1.b.ii-iii

            :param shared_key: Shared key generate through ECDH
            :type shared_key: ``bytes``

            :return: AES-128 key
            :rtype: ``bytes``
            """
            hasher = Hash(SHA256())
            hasher.update(shared_key)
            full_digest = hasher.finalize()

            return full_digest[:128 // 8]
        # end def generate_aes_128_anti_spoofing_key

        @staticmethod
        def encrypt_single_block_aes(aes_key, plain_text):
            """
            Encrypt a single block AES with a given key

            :param aes_key: AES key
            :type aes_key: ``bytes``
            :param plain_text: plain text to encrypt
            :type plain_text: ``bytes``

            :return: encrypted block
            :rtype: ``bytes``
            """
            cipher = Cipher(AES(key=aes_key), ECB()).encryptor()

            return cipher.update(plain_text) + cipher.finalize()
        # end def encrypt_single_block_aes

        @classmethod
        def decrypt_single_block_aes(cls, aes_key, cypher_text):
            """
            Encrypt a single block AES with a given key

            :param aes_key: AES key
            :type aes_key: ``bytes``
            :param cypher_text: plain text to encrypt
            :type cypher_text: ``bytes``

            :return: decrypted block
            :rtype: ``bytes``
            """
            return cls.encrypt_single_block_aes(aes_key, cypher_text)
        # end def decrypt_single_block_aes

        @staticmethod
        def encode_public_key_for_key_based_paring(public_key):
            """
            Encode the public key of the fast pair seeker to send to the fast pair provider
            in the key pairing characteristic

            consist of the points on the elliptical curve as a 64 byte number.

            source: reverse engineering
            :param public_key: public key to encode
            :type public_key: ``ec.ECPublicKey``

            :return: encoded public key
            :rtype: ``HexList``
            """
            # Serialize the public key to DER format
            public_key_der = public_key.public_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )

            # Extract the raw bytes of the public key

            raw_public_key_bytes = public_key_der[-64:]

            return HexList(raw_public_key_bytes)
        # end def encode_public_key_for_key_based_paring

        @staticmethod
        def encrypt_aes_ctr(input_data, nonce, secret_key):
            """
            Encrypt aes ctr data, due to the properties of AES, can be used for decryption also

            :param input_data: data to encrypt
            :type input_data: ``bytes``
            :param nonce: nonce used for encryption
            :type nonce: ``bytes``
            :param secret_key: secret key used for encryption
            :type secret_key: ``bytes``
            
            :return: encrypted data
            :rtype: ``bytes``
            """
            block_count = ceil(len(input_data) / 16)
            cipher = Cipher(AES(key=secret_key), ECB()).encryptor()

            encrypted = []
            for i in range(block_count):
                input_value = [i, 0, 0, 0, 0, 0, 0, 0] + list(nonce)
                block = cipher.update(bytes(input_value))

                for a, b in zip(input_data[i * 16:(i + 1) * 16], block):
                    encrypted.append(a ^ b)
                # end for
            # end for
            return encrypted
        # end def encrypt_aes_ctr

        @staticmethod
        def first_8bytes_hmac(secret_key, data):
            """
            Get the first 8 bytes of an hmac-sha256 signature

            :param secret_key: Key used for signing
            :type secret_key: ``bytes``
            :param data: data to sign
            :type data: ``Hexlist``

            :return: first 8 bytes of the digest
            :rtype: ``bytes``
            """
            h = HMAC(secret_key, SHA256())
            h.update(bytes(data[8:]))
            digest = HexList(h.finalize())
            return digest[:8]
        # end def first_8bytes_hmac
    # end class FastPairCryptographyHelper
# end class BleDirectPairingUtils

# ----------------------------------------------------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------------------------------------------------
