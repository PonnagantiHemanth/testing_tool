#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.newmodules.secrets

@brief Auto Test of 'secrets' module

@author christophe.roquebert

@date   2018/11/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.core             import TestCase
from secrets                    import token_bytes
from secrets                    import token_hex
from secrets                    import token_urlsafe
from secrets                    import choice
from secrets                    import compare_digest
from pylibrary.tools.hexlist    import HexList
from string                     import ascii_letters
from string                     import digits

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class TestSecretsMethods(TestCase):
    """ The main purpose of the new secrets module is to provide 
        an obvious way to reliably generate cryptographically strong 
        pseudo-random values suitable for managing secrets, such as 
        account authentication, tokens, and similar.. """
        
    DEFAULT_ENTROPY = 32  # bytes

    # PEP 506 - Adding A Secrets Module To The Standard Library
    def test_token_bytes(self):
        """ Check the function generating tokens suitable for use 
            in (e.g.) password recovery, as session keys, etc.,
            as bytes. """

        nbytes = self.DEFAULT_ENTROPY
        result = token_bytes(nbytes)
        self.assertEqual(self.DEFAULT_ENTROPY, len(result))
        hexlist = HexList(result)
        self.assertEqual(self.DEFAULT_ENTROPY, len(hexlist))
        
        # Check randomness
        hexlist2 = HexList(token_bytes(nbytes))
        self.assertNotEqual(hexlist2, hexlist)
    # end def test_token_bytes
    
    # PEP 506 - Adding A Secrets Module To The Standard Library
    def test_token_hex(self):
        """ Check the function generating tokens suitable for use 
            in (e.g.) password recovery, as session keys, etc.,
            as text, using hexadecimal digits. """
        nbytes = self.DEFAULT_ENTROPY
        result = token_hex(nbytes)
        self.assertEqual(self.DEFAULT_ENTROPY*2, len(result))
        # Check randomness
        result2 = token_hex(nbytes)
        self.assertNotEqual(result2, result)
    # def test_token_hex

    # PEP 506 - Adding A Secrets Module To The Standard Library
    def test_token_urlsafe(self):
        """ Check the function generating tokens suitable for use 
            in (e.g.) password recovery, as session keys, etc.,
            as text, using URL-safe base-64 encoding. """
        nbytes = self.DEFAULT_ENTROPY
        result = token_urlsafe(nbytes)
        # Check randomness
        result2 = token_urlsafe(nbytes)
        self.assertNotEqual(result2, result)
    # end def test_token_urlsafe
    
    # PEP 506 - Adding A Secrets Module To The Standard Library
    def test_passwordGeneration(self):
        """ Check the generation an eight-character alphanumeric password."""
        alphabet = ascii_letters + digits
        password = ''.join(choice(alphabet) for i in range(8))
        password2 = ''.join(choice(alphabet) for i in range(8))
        self.assertFalse(compare_digest(password, password2))
    # end def test_passwordGeneration
    
    # PEP 506 - Adding A Secrets Module To The Standard Library
    def test_strongPasswordGeneration(self):
        """ Check the generation of a ten-character alphanumeric password 
            with at least one lowercase character, at least one uppercase 
            character, and at least three digits."""
        alphabet = ascii_letters + digits
        while True:
            password = ''.join(choice(alphabet) for i in range(10))
            if (any(c.islower() for c in password)
                    and any(c.isupper() for c in password)
                    and sum(c.isdigit() for c in password) >= 3):
                break
            # end if
        self.assertTrue(any(c.islower() for c in password), 
            'Password do not contain at least one lowercase character !')
        self.assertTrue(any(c.isupper() for c in password), 
            'Password do not contain at least one uppercase character !')
        self.assertGreaterEqual(sum(c.isdigit() for c in password), 3, 
            'Password do not contain at least three digits !')
        # end while
    # end def test_strongPasswordGeneration
    
# end class TestSecretsMethods  
         
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
