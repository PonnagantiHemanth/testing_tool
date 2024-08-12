#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
:package: pyhid.test.bitfield
:brief: PyHid BitField testing module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/18
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from unittest import TestCase

from pylibrary.tools.hexlist import HexList
from pyhid.bitfield import BitField
from pyhid.field import CheckByte
from pyhid.field import CheckHexList

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------


class FieldTestCaseMixin(object):
    """
    Utility class for testing field consistency
    """

    def assert_bit_field_consistency(self, obj_to_check, name, value, fid=None, length=0x00, message=None,
                                     constructor=False, input_values=None, auto_hex_list=True):
        """
        Tests the content of a field.

        :param obj_to_check: Object builds on field.
        :type obj_to_check: ``object``
        :param name: Name of the field.
        :type name: ``str``
        :param value: Value of the field.
        :type value: ``object``
        :param fid: Field identifier. - OPTIONAL
        :type fid: ``int`` or ``None``
        :param length: Length of the field. - OPTIONAL
        :type length: ``int``
        :param message: Message - OPTIONAL
        :type message: ``str``. or ``None``
        :param constructor: Check constructor consistency. - OPTIONAL
        :type constructor: ``bool``
        :param input_values: List of input values to feed to the object. - OPTIONAL
        :type input_values: ``list`` or ``None``
        :param auto_hex_list: Auto-generate HexList test vector. - OPTIONAL
        :type auto_hex_list: ``bool``
        """
        if message is None:
            message = f"Inconsistent {name} field value!"
        # end if

        # No input values uses the value as input
        if input_values is None:
            input_values = (value,)
        # end if

        # Check for default value initialized in object's constructor
        if constructor:
            self.assertEqual(value,
                             getattr(obj_to_check, name),
                             message)
        # end if

        # Direct access in HexList
        if auto_hex_list:
            if length is None:
                expectedValue1 = HexList()
            else:
                if (length % 8) == 0:
                    expectedValue1 = HexList(0x51) * (length / 8)
                else:
                    expectedValue1 = pow(2, length) - 1
                # end if
            # end if
            setattr(obj_to_check, name, expectedValue1)

            value1 = getattr(obj_to_check, name)
            if (length % 8) == 0:
                obtainedValue1 = HexList(value1)
            else:
                obtainedValue1 = value1
            # end if
            self.assertEqual(expectedValue1,
                             obtainedValue1,
                             message)
        # end if

        # Direct access in expected format
        for inputValue in input_values:
            setattr(obj_to_check, name, inputValue)
            obtained = getattr(obj_to_check, name)
            self.assertEqual(value,
                             obtained,
                             message + f"\nExpected: {value}\nObtained: {obtained}")
        # end for

        # Access by setValue/getValue method in HexList
        if auto_hex_list:
            if length is None:
                expectedValue2 = HexList()
            else:
                if (length % 8) == 0:
                    expectedValue2 = HexList(0xA1) * (length / 8)
                else:
                    expectedValue2 = pow(2, length) - 1
                # end if
            # end if
            if fid is None:
                fid = obj_to_check.getFidFromName(name)
            # end if

            obj_to_check.setValue(fid, expectedValue2)
            value2 = obj_to_check.getValue(fid)
            if (length % 8) == 0:
                obtainedValue2 = HexList(value2)
            else:
                obtainedValue2 = value2
            # end if
            self.assertEqual(expectedValue2,
                             obtainedValue2,
                             message + f"\nExpected: {expectedValue2}\nObtained: {obtainedValue2}")
        # end if

        # Access by setValue/getValue method in expected format
        for inputValue in input_values:
            obj_to_check.setValue(fid, inputValue)
            obtainedValue = obj_to_check.getValue(fid)
            self.assertEqual(value,
                             obtainedValue,
                             message)
        # end for
    # end def assert_bit_field_consistency
# end class FieldTestCaseMixin


class CommonFieldTestCase(TestCase, FieldTestCaseMixin):
    """
    Tests of an object which contains field.
    """
# end class CommonFieldTestCase


class BitFieldTestCase(TestCase):
    """
    Tests of the BitField class
    """
    RefClass = BitField

    @classmethod
    def _create_instance(cls, fid=0x01, length=0x02, fid_length=0x08, len_length=0x08, default_value=None,
                         title="Default title", name=None, checks=None, conversions=None, aliases=tuple(),
                         **kwargs):
        """
        Create a default Field

        :param fid: Field Identifier value - OPTIONAL
        :type fid: ``int``
        :param length: Field length value - OPTIONAL
        :type length: ``int``
        :param fid_length: Field identifier length - OPTIONAL
        :type fid_length: ``int``
        :param len_length: Field value length length - OPTIONAL
        :type len_length: ``int``
        :param default_value: Default value of the field - OPTIONAL
        :type default_value: ``HexList`` or ``callable`` or ``None``
        :param title: Field title value - OPTIONAL
        :type title: ``str``
        :param name: Field name value - OPTIONAL
        :type name: ``str`` or ``None``
        :param checks: List of checks on the value - OPTIONAL
        :type checks: ``list[Check]`` or ``tuple[Check]`` or ``None``
        :param conversions: Dict that maps an input type to a conversion routine. - OPTIONAL
        :type conversions: ``dict[sourceType, converter]`` or ``None``
        :param aliases: List of alternative names by which to reference this field. - OPTIONAL
        :type aliases: ``tuple``
        :param kwargs: Optional arguments
        :type kwargs: ``dict``

        :return: Created Field
        :rtype: ``BitField``
        """
        if default_value is None:
            default_value = HexList("05060708")
        # end if

        return cls.RefClass(fid, length, fid_length, len_length, default_value, title, name, checks=checks,
                            conversions=conversions, aliases=aliases, **kwargs)
    # end def _create_instance

    def test_eq(self):
        """
        Tests __eq__ method
        """
        field1 = self._create_instance()
        field2 = self._create_instance()

        self.assertEqual(field1,
                         field2,
                         "Field instances should be equal !")

        field2 = self._create_instance(fid=0x02)
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal !")

        field2 = self._create_instance(length=0x03)
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal !")

        field2 = self._create_instance(default_value=HexList(0x02))
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal !")

        field2 = self._create_instance(title="New title")
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal !")
    # end def test_eq

    def test_eq_wrong_type(self):
        """
        Tests __eq__ method with wrong type
        """
        field = self._create_instance()

        self.assertRaises(TypeError,
                          field.__eq__,
                          0x01)

        self.assertRaises(TypeError,
                          field.__eq__,
                          "01")

        self.assertRaises(TypeError,
                          field.__eq__,
                          HexList(0x01))
    # end def test_eq_wrong_type

    def test_ne(self):
        """
        Tests the __ne__ method
        """
        field1 = self._create_instance()
        field2 = self._create_instance()

        self.assertFalse(field1 != field2,
                         "Field instances should be equal !")

        field2 = self._create_instance(fid=0x02)
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal !")

        field2 = self._create_instance(length=0x03)
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal !")

        field2 = self._create_instance(default_value=HexList(0x02))
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal !")

        field2 = self._create_instance(title="New title")
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal !")
    # end def test_ne

    def test_get_fid(self):
        """
        Tests the GetFid method
        """
        expectedFid = 0x01
        field = self._create_instance(fid=expectedFid)

        self.assertEqual(expectedFid,
                         field.getFid(),
                         "Inconsistent Fid value !")
    # end def test_get_fid

    def test_set_fid(self):
        """
        Tests the SetFid method
        """
        fidList = [-2, -1, 0, 128, 255]
        for expectedFid in fidList:
            field = self._create_instance(fid=0x02)

            field.setFid(expectedFid)

            self.assertEqual(expectedFid,
                             field.getFid(),
                             "Inconsistent Fid value !")
        # end for
    # end def test_set_fid

    def test_set_fid_wrong_type(self):
        """
        Tests the SetFid method with wrong type
        """
        field = self._create_instance(fid=0x02)

        self.assertRaises(TypeError,
                          field.setFid,
                          "01")

        self.assertRaises(TypeError,
                          field.setFid,
                          HexList("01"))
    # end def test_set_fid_wrong_type

    def test_set_fid_wrong_value(self):
        """
        Tests the SetFid method with wrong value
        """
        field = self._create_instance(fid=0x02)

        self.assertRaises(ValueError,
                          field.setFid,
                          256)
    # end def test_set_fid_wrong_value

    def test_get_length(self):
        """
        Tests the GetLength method
        """
        expectedLength = 0x01
        field = self._create_instance(length=expectedLength)

        self.assertEqual(expectedLength,
                         field.get_length(),
                         "Inconsistent Length length !")
    # end def test_get_length

    def test_set_length(self):
        """
        Tests the SetLength method
        """
        expectedLength = 0x01
        field = self._create_instance(length=0x02)

        field.set_length(expectedLength)

        self.assertEqual(expectedLength,
                         field.get_length(),
                         "Inconsistent Length length !")

        expectedLength = None
        field = self._create_instance(length=0x10)

        field.set_length(expectedLength)

        self.assertEqual(expectedLength,
                         field.get_length(),
                         "Inconsistent Length length !")
    # end def test_set_length

    def test_set_length_wrong_type(self):
        """
        Tests the SetLength method with wrong type
        """
        field = self._create_instance(length=0x02)

        self.assertRaises(TypeError,
                          field.set_length,
                          "01")

        self.assertRaises(TypeError,
                          field.set_length,
                          HexList("01"))
    # end def test_set_length_wrong_type

    def test_set_length_wrong_value(self):
        """
        Tests the SetLength method with wrong value
        """
        field = self._create_instance(length=0x02)

        wrongValue = 1 << field._len_length
        self.assertRaises(ValueError,
                          field.set_length,
                          wrongValue)

        wrongValue = 1 << (field._len_length * 0x10)
        self.assertRaises(ValueError,
                          field.set_length,
                          wrongValue)
    # end def test_set_length_wrong_value

    def test_get_conversions(self):
        """
        Tests the getHasTag method
        """
        expectedConversions = {type(None): lambda x: None}
        field = self._create_instance(conversions=expectedConversions)

        obtainedConversions = field.conversions
        self.assertEqual(expectedConversions,
                         obtainedConversions,
                         "Inconsistent conversions value !")
    # end def test_get_conversions

    def test_set_conversions(self):
        """
        Tests the setHasTag method
        """
        expectedConversions = {type(None): lambda x: None}
        field = self._create_instance(conversions=None)

        field.conversions = expectedConversions

        self.assertEqual(expectedConversions,
                         field.conversions,
                         "Inconsistent conversions value !")
    # end def test_set_conversions

    def testGet_default_value(self):
        """
        Tests the Get_default_value method
        """
        expected_default_value = HexList("0102030405")
        field = self._create_instance(default_value=expected_default_value)

        self.assertEqual(expected_default_value,
                         field.get_default_value(),
                         "Inconsistent Value default_value !")

        globalContext = {"expected_default_value": expected_default_value}

        def default_value(context):
            """
            Obtain the default value from the context.

            @param context [in] (object) The object from which to obtain the value.
            @return The default value from the context
            """
            return context["expected_default_value"]
        # end def default_value

        field = self._create_instance(default_value=default_value)
        self.assertEqual(expected_default_value,
                         field.get_default_value(globalContext),
                         "Inconsistent Value default_value when callable !")
    # end def test_get_default_value

    def testSet_default_value(self):
        """
        Tests the Set_default_value method
        """
        expected_default_value = HexList("0102030405")
        field = self._create_instance(default_value=HexList("01020304"))

        field.set_default_value(expected_default_value)

        self.assertEqual(expected_default_value,
                         field.get_default_value(),
                         "Inconsistent Value default_value !")
    # end def test_set_default_value

    def test_set_default_value_wrong_type(self):
        """
        Tests the Set_default_value method with wrong type
        """
        field = self._create_instance(default_value=HexList("0102030405"),
                                      checks=(CheckHexList(),))

        self.assertRaises(TypeError,
                          field.set_default_value,
                          "01")

        self.assertRaises(TypeError,
                          field.set_default_value,
                          0x01)
    # end def test_set_default_value_wrong_type

    def test_get_title(self):
        """
        Tests the GetTitle method
        """
        expectedTitle = "Expected title"
        field = self._create_instance(title=expectedTitle)

        self.assertEqual(expectedTitle,
                         field.title,
                         "Inconsistent Value title !")
    # end def test_get_title

    def test_set_title(self):
        """
        Tests the SetTitle method
        """
        expectedTitle = "Expected title"
        field = self._create_instance(title="Default title")

        field.title = expectedTitle

        self.assertEqual(expectedTitle,
                         field.title,
                         "Inconsistent Value title !")
    # end def test_set_title

    def test_set_title_wrong_type(self):
        """
        Tests the SetTitle method with wrong type
        """
        field = self._create_instance(title="Expected title")

        with self.assertRaises(TypeError):
            field.title = 0x01

        with self.assertRaises(TypeError):
            field.title = HexList(0x01)
    # end def test_set_title_wrong_type

    def test_get_name(self):
        """
        Tests the GetName method
        """
        expectedName = "Expected Name"
        field = self._create_instance(name=expectedName)

        field.name = expectedName

        self.assertEqual(expectedName,
                         field.name,
                         "Inconsistent Value name !")
    # end def test_get_name

    def test_set_name(self):
        """
        Tests the SetName method
        """
        expectedName = "Expected Name"
        field = self._create_instance(name="Expected Name")

        field.name = expectedName

        self.assertEqual(expectedName,
                         field.name,
                         "Inconsistent name value!")
    # end def test_set_name

    def test_set_name_wrong_type(self):
        """
        Tests the SetName method with wrong type
        """
        field = self._create_instance(name="Expected Name")

        with self.assertRaises(TypeError):
            field.name = 0x01

        with self.assertRaises(TypeError):
            field.name = HexList(0x01)
    # end def test_set_name_wrong_type

    def test_create_summary(self):
        """
        Tests the CreateSummary method
        """
        fid = 0x02
        field = self._create_instance(fid=fid,
                                      default_value=HexList("02"),
                                      title="Expected Title")

        expectedLog = "Expected Title: (0x02)"
        obtainedLog = field.create_summary()

        self.assertEqual(expectedLog,
                         obtainedLog,
                         "Inconsistent log !")
    # end def test_create_summary

    def test_str(self):
        """
        Tests the __str__ method
        """
        fid = 0x02
        field = self._create_instance(fid=fid, default_value=HexList("02"), title="Expected Title")

        expectedLog = "Expected Title: (0x02)"
        obtainedLog = str(field)

        self.assertEqual(expectedLog,
                         obtainedLog,
                         "Inconsistent log !")
    # end def test_str

    def test_check_value(self):
        """
        Test the check_value method
        """
        fid = 0x02
        field = self._create_instance(fid=fid, default_value=HexList("02"), title="Expected Title")

        field._checks = (CheckByte(),)

        self.assertRaises(TypeError,
                          field.check_value,
                          "01")

        self.assertTrue(field.check_value(0x01),
                        "Inconsistent check_value result !")

        field._checks = None

        self.assertTrue(field.check_value(0x01),
                        "Inconsistent check_value result !")

        field.set_optional(True)

        field._checks = (CheckByte(),)

        self.assertTrue(field.check_value(None),
                        "Inconsistent check_value result !")
    # end def test_check_value
# end class BitFieldTestCase


if __name__ == "__main__":
    from unittest import main
    main()
# end if
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
