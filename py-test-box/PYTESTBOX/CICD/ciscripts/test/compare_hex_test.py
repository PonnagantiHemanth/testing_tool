import unittest
from compare_hex import HexCompare
from compare_hex import ElfHelper
import os

class MyTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.curr_dir = os.curdir;
        os.chdir(os.path.dirname(__file__))
        cls.hex_compare = HexCompare('reference.hex')
        cls.elfhelper = ElfHelper('reference.elf')

    @classmethod
    def tearDownClass(cls) -> None:
        os.chdir(cls.curr_dir)

    def test_same_file(self):
        self.assertTrue(self.hex_compare.is_same_hex('reference.hex'))

    def test_missing_data(self):
        self.assertFalse(self.hex_compare.is_same_hex('reference_with_less_data.hex'))

    def test_extra_data(self):
        self.assertFalse(self.hex_compare.is_same_hex('reference_with_more_data.hex'))

    def test_same_file_allow_one_diff(self):
        self.assertTrue(self.hex_compare.is_same_hex('reference.hex',
                                                     addresses_allowed_to_differ={0x10001208}))

    def test_unexpected_diff_in_file(self):
        self.assertFalse(self.hex_compare.is_same_hex('reference_with_extra_diff.hex'))

    def test_diff_in_approtect_only(self):
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_in_approtect.hex',
                                                     addresses_allowed_to_differ={0x10001208}))

    def test_duplicated_addresses(self):
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_in_approtect.hex',
                                                     addresses_allowed_to_differ={0x10001208,
                                                                                  0x10001208}))

    def test_unknown_symbols(self):
        addresses_allowed_to_differ = self.elfhelper.get_symbols_address_range(['rsa_keyMod',
                                                                                'unknown_symbol'])
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_key.hex',
                                                     addresses_allowed_to_differ))

    def test_diff_in_approtect_and_approtect_expected_value(self):
        addresses_allowed_to_differ = {0x10001208}
        addresses_allowed_to_differ |= self.elfhelper.get_symbols_address_range(['uicr_approtectExpectedValue'])
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_approtect_and_expected_approtect.hex',
                                                     addresses_allowed_to_differ))

    def test_diff_in_public_keys(self):
        addresses_allowed_to_differ = self.elfhelper.get_symbols_address_range(['rsa_keyMod'])
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_key.hex',
                                                     addresses_allowed_to_differ))

    def test_diff_in_public_keys_and_approtect_values(self):
        addresses_allowed_to_differ = {0x10001208}
        addresses_allowed_to_differ |= self.elfhelper.get_symbols_address_range(['rsa_keyMod', 'uicr_approtectExpectedValue'])
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_in_key_and_approtect_values.hex',
                                                     addresses_allowed_to_differ))

    def test_diff_in_public_keys_approtect_and_ci_bit_values(self):
        addresses_allowed_to_differ = {0x10001208}
        addresses_allowed_to_differ |= self.elfhelper.get_symbols_address_range(['rsa_keyMod', 'uicr_approtectExpectedValue'])
        addresses_allowed_to_differ |= {(self.elfhelper.get_symbol_address('fwd_currentFwData') + 19)}
        elfhelper_app = ElfHelper('reference_app.elf')
        addresses_allowed_to_differ |= {(elfhelper_app.get_symbol_address('fwd_currentFwData') + 19)}
        self.assertTrue(self.hex_compare.is_same_hex('reference_with_diff_in_key_cibit_and_approtect_values.hex',
                                                     addresses_allowed_to_differ))

if __name__ == '__main__':
    unittest.main()
