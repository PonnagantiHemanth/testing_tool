#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------

"""
:package: pyhid.test.field
:brief: PyHid Field test module
:author: Christophe Roquebert <croquebert@logitech.com>
:date: 2018/12/18
"""

# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

from unittest import TestCase

from pyhid.field import CheckBitStruct
from pyhid.field import CheckBool
from pyhid.field import CheckByte
from pyhid.field import CheckHexList
from pyhid.field import CheckInt
from pyhid.field import CheckList
from pyhid.field import CheckNone
from pyhid.field import CheckString
from pyhid.field import Field
from pylibrary.tools.bitstruct import BitStruct
from pylibrary.tools.deprecation import ignoredeprecation
from pylibrary.tools.hexlist import HexList
from pylibrary.tools.numeral import Numeral


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

class FieldTestCaseMixin(object):
    """
    Utility class for testing field consistency
    """

    def assert_field_consistency(self, obj_to_check,
                                 name,
                                 fid,
                                 length,
                                 value,
                                 message=None,
                                 constructor=False,
                                 input_values=None,
                                 auto_hex_list=True):
        """
        Tests the content of a field.

        :param obj_to_check: Object builds on field
        :type obj_to_check: ``object``
        :param name: Name of the field
        :type name: ``str``
        :param fid: Field identifier
        :type fid: ``int``
        :param length: Length of the field
        :type length: ``int``
        :param value: Value of the field
        :type value: ``object``
        :param message: Message - OPTIONAL
        :type message: ``str`` or ``None``
        :param constructor: Check constructor consistency - OPTIONAL
        :type constructor: ``bool``
        :param input_values: List of input values to feed to the object.
        :type input_values: ``list[object]`` or ``None``
        :param auto_hex_list:  Auto-generate hexlist test vector. - OPTIONAL
        :type auto_hex_list: ``bool``
        :return:
        :rtype:
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
            self.assertEqual(value, getattr(obj_to_check, name), message)
        # end if

        # Direct access in HexList
        if auto_hex_list:
            if length is None:
                expectedValue1 = HexList()
            else:
                expectedValue1 = HexList(0x51) * length
            # end if
            setattr(obj_to_check, name, expectedValue1)

            value1 = getattr(obj_to_check, name)
            obtainedValue1 = HexList(value1)
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
                expectedValue2 = HexList(0xA1) * length
            # end if
            obj_to_check.setValue(fid, expectedValue2)
            value2 = obj_to_check.getValue(fid)
            obtainedValue2 = HexList(value2)
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
    # end def assert_field_consistency
# end class FieldTestCaseMixin


class CommonFieldTestCase(TestCase, FieldTestCaseMixin):
    """
    Tests of an object which contains field.
    """
# end class CommonFieldTestCase


class FieldTestCase(TestCase):  # pylint:disable=R0904
    """
    Tests of the Field class
    """

    @classmethod
    def _create_field(cls, fid=0x01, length=0x02, has_tag=False, variable=False, finger_print=False, default_value=None,
                      title="Default title", name=None, mode=None, checks=None, conversions=None, aliases=tuple(),
                      **kwargs):
        """
        Create a default Field

        :param fid: Field Identifier value - OPTIONAL
        :type fid: ``int``
        :param length: Field length value - OPTIONAL
        :type length: ``int``
        :param has_tag: Optional field - OPTIONAL
        :type has_tag: ``bool``
        :param variable: Variable field - OPTIONAL
        :type variable: ``bool``
        :param finger_print: Field is used for Rivet/Integra computation - OPTIONAL
        :type finger_print: ``bool``
        :param default_value: Default value of the field - OPTIONAL
        :type default_value: ``object``
        :param title: Field title value - OPTIONAL
        :type title: ``str`` or ``None``
        :param name: Field name value - OPTIONAL
        :type name: ``str`` or ``None``
        :param mode: Mode of management of Field - OPTIONAL
        :type mode: ``int`` or ``None``
        :param checks: List of checks on the value - OPTIONAL
        :type checks: ``list[Check] or ``tuple[Check] or ``None``
        :param conversions: Dict that maps an input type to a conversion routine. - OPTIONAL
        :type conversions: ``dict[sourceType, converter]`` or ``None``
        :param aliases: List of alternative names by which to reference this field. - OPTIONAL
        :type aliases: ``tuple``
        :param kwargs: Optional arguments
        :type kwargs: ``dict``
        :return: Created Field
        :rtype: ``Field``
        """

        if default_value is None:
            default_value = HexList("05060708")
        # end if

        return Field(fid,
                     length,
                     has_tag,
                     variable,
                     finger_print,
                     default_value,
                     title,
                     name,
                     mode=mode,
                     checks=checks,
                     conversions=conversions,
                     aliases=aliases,
                     **kwargs)
    # end def _create_field

    def test_eq(self):
        """
        Tests __eq__ method
        """
        field1 = self._create_field()
        field2 = self._create_field()

        self.assertEqual(field1,
                         field2,
                         "Field instances should be equal")

        field2 = self._create_field(fid=0x02)
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal")

        field2 = self._create_field(length=0x03)
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal")

        field2 = self._create_field(has_tag=True)
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal")

        field2 = self._create_field(variable=True)
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal")

        field2 = self._create_field(default_value=HexList(0x02))
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal")

        field2 = self._create_field(title="New title")
        self.assertNotEqual(field1,
                            field2,
                            "Field instances shouldn't be equal")
    # end def test_eq

    def test_eq_wrong_type(self):
        """
        Tests __eq__ method with wrong type
        """
        field = self._create_field()

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
        field1 = self._create_field()
        field2 = self._create_field()

        self.assertFalse(field1 != field2,
                         "Field instances should be equal")

        field2 = self._create_field(fid=0x02)
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal")

        field2 = self._create_field(length=0x03)
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal")

        field2 = self._create_field(has_tag=True)
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal")

        field2 = self._create_field(variable=True)
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal")

        field2 = self._create_field(default_value=HexList(0x02))
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal")

        field2 = self._create_field(title="New title")
        self.assertTrue(field1 != field2,
                        "Field instances shouldn't be equal")
    # end def test_ne

    def test_get_fid(self):
        """
        Tests the GetFid method
        """
        expectedFid = 0x01
        field = self._create_field(fid=expectedFid)

        self.assertEqual(expectedFid,
                         field.getFid(),
                         "Inconsistent Fid value")
    # end def test_get_fid

    def test_set_fid(self):
        """
        Tests the SetFid method
        """
        fidList = [-2, -1, 0, 128, 255]
        for expectedFid in fidList:
            field = self._create_field(fid=0x02)

            field.setFid(expectedFid)

            self.assertEqual(expectedFid,
                             field.getFid(),
                             "Inconsistent Fid value")
        # end for
    # end def test_set_fid

    def test_set_fid_wrong_type(self):
        """
        Tests the SetFid method with wrong type
        """
        field = self._create_field(fid=0x02)

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
        field = self._create_field(fid=0x02)

        self.assertRaises(ValueError,
                          field.setFid,
                          256)
    # end def test_set_fid_wrong_value

    def test_get_length(self):
        """
        Tests the GetLength method
        """
        expectedLength = 0x01
        field = self._create_field(length=expectedLength)

        self.assertEqual(expectedLength,
                         field.get_length(),
                         "Inconsistent Length length")
    # end def test_get_length

    def test_set_length(self):
        """
        Tests the SetLength method
        """
        expectedLength = 0x01
        field = self._create_field(length=0x02)

        field.set_length(expectedLength)

        self.assertEqual(expectedLength,
                         field.get_length(),
                         "Inconsistent Length length")

        expectedLength = None
        field = self._create_field(length=0x10)

        field.set_length(expectedLength)

        self.assertEqual(expectedLength,
                         field.get_length(),
                         "Inconsistent Length length")
    # end def test_set_length

    def test_set_length_wrong_type(self):
        """
        Tests the SetLength method with wrong type
        """
        field = self._create_field(length=0x02)

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
        field = self._create_field(length=0x02)

        self.assertRaises(ValueError,
                          field.set_length,
                          1024)

        self.assertRaises(ValueError,
                          field.set_length,
                          256)
    # end def test_set_length_wrong_value

    def test_optional(self):
        """
        Tests the get_has_tag method
        """
        expectedOptional = True
        field = self._create_field(optional=expectedOptional)

        self.assertEqual(expectedOptional,
                         field.optional,
                         "Inconsistent Optional value")
    # end def test_optional

    def test_get_conversions(self):
        """
        Tests the get_has_tag method
        """
        expectedConversions = {type(None): lambda x: None}
        field = self._create_field(conversions=expectedConversions)

        obtainedConversions = field.conversions
        self.assertEqual(expectedConversions,
                         obtainedConversions,
                         "Inconsistent conversions value")
    # end def test_get_conversions

    def test_set_conversions(self):
        """
        Tests the set_has_tag method
        """
        expectedConversions = {type(None): lambda x: None}
        field = self._create_field(conversions=None)

        field.conversions = expectedConversions

        self.assertEqual(expectedConversions,
                         field.conversions,
                         "Inconsistent conversions value")
    # end def test_set_conversions

    def test_get_has_tag(self):
        """
        Tests the get_has_tag method
        """
        expected_has_tag = True
        field = self._create_field(has_tag=expected_has_tag)

        self.assertEqual(expected_has_tag,
                         field.get_has_tag(),
                         "Inconsistent Optional value")
    # end def test_get_has_tag

    def test_set_has_tag(self):
        """
        Tests the set_has_tag method
        """
        expected_has_tag = True
        field = self._create_field(has_tag=False)

        field.set_has_tag(expected_has_tag)

        self.assertEqual(expected_has_tag,
                         field.get_has_tag(),
                         "Inconsistent Optional value")
    # end def test_set_has_tag

    def test_set_has_tag_wrong_type(self):
        """
        Tests the set_has_tag method with wrong type
        """
        field = self._create_field(has_tag=False)

        self.assertRaises(TypeError,
                          field.set_has_tag,
                          "01")

        self.assertRaises(TypeError,
                          field.set_has_tag,
                          HexList("01"))
    # end def test_set_has_tag_wrong_type

    def test_set_has_tag_wrong_value(self):
        """
        Tests the set_has_tag method with wrong value
        """
        field = self._create_field(has_tag=False)

        self.assertRaises(ValueError,
                          field.set_has_tag,
                          -1)

        self.assertRaises(ValueError,
                          field.set_has_tag,
                          3)
    # end def test_set_has_tag_wrong_value

    def test_is_variable(self):
        """
        Tests the IsVariable method
        """
        expectedVariable = True
        field = self._create_field(variable=expectedVariable)

        self.assertEqual(expectedVariable,
                         field.variable,
                         "Inconsistent Variable value")
    # end def test_is_variable

    def test_set_variable(self):
        """
        Tests the SetVariable method
        """
        expectedVariable = True
        field = self._create_field(variable=False)

        field.set_variable(expectedVariable)

        self.assertEqual(expectedVariable,
                         field.variable,
                         "Inconsistent Variable value")
    # end def test_set_variable

    def test_set_variable_wrong_type(self):
        """
        Tests the SetVariable method with wrong type
        """
        field = self._create_field(variable=False)

        self.assertRaises(TypeError,
                          field.set_variable,
                          "01")

        self.assertRaises(TypeError,
                          field.set_variable,
                          HexList("01"))
    # end def test_set_variable_wrong_type

    def test_set_variable_wrong_value(self):
        """
        Tests the SetVariable method with wrong value
        """
        field = self._create_field(variable=False)

        self.assertRaises(ValueError,
                          field.set_variable,
                          -1)

        self.assertRaises(ValueError,
                          field.set_variable,
                          3)
    # end def test_set_variable_wrong_value

    def test_is_finger_print(self):
        """
        Tests the IsFingerPrint method
        """
        fingerPrint = True
        field = self._create_field(finger_print=fingerPrint)

        self.assertEqual(fingerPrint,
                         field.finger_print,
                         "Wrong finger_print property result.")

        fingerPrint = False
        field = self._create_field(finger_print=fingerPrint)

        self.assertEqual(fingerPrint,
                         field.finger_print,
                         "Wrong finger_print property result.")
    # end def test_is_finger_print

    def test_set_finger_print(self):
        """
        Tests SetFingerPrint method
        """
        fingerPrint = True
        field = self._create_field(finger_print=False)

        field.set_finger_print(fingerPrint)

        self.assertEqual(fingerPrint,
                         field.finger_print,
                         "Wrong finger_print method result.")
    # end def test_set_finger_print

    def test_set_finger_print_wrong_type(self):
        """
        Tests the SetFingerPrint method with wrong type
        """
        field = self._create_field(finger_print=False)

        self.assertRaises(TypeError,
                          field.set_finger_print,
                          "01")

        self.assertRaises(TypeError,
                          field.set_finger_print,
                          HexList("01"))
    # end def test_set_finger_print_wrong_type

    def test_set_finger_print_wrong_value(self):
        """
        Tests the SetFingerPrint method with wrong value
        """
        field = self._create_field(finger_print=False)

        self.assertRaises(ValueError,
                          field.set_finger_print,
                          -1)

        self.assertRaises(ValueError,
                          field.set_finger_print,
                          3)
    # end def test_set_finger_print_wrong_value

    def test_get_default_value(self):
        """
        Tests the Get_default_value method
        """
        expected_default_value = HexList("0102030405")
        field = self._create_field(default_value=expected_default_value)

        self.assertEqual(expected_default_value,
                         field.get_default_value(),
                         "Inconsistent Value default_value")

        globalContext = {"expected_default_value": expected_default_value}

        def default_value(context):
            """
            Obtain the default value from the context.

            @param context [in] (object) The object from which to obtain the value.
            @return The default value from the context
            """
            return context["expected_default_value"]

        # end def default_value

        field = self._create_field(default_value=default_value)
        self.assertEqual(expected_default_value,
                         field.get_default_value(globalContext),
                         "Inconsistent Value default_value when callable")
    # end def test_get_default_value

    def test_set_default_value(self):
        """
        Tests the Set_default_value method
        """
        expected_default_value = HexList("0102030405")
        field = self._create_field(default_value=HexList("01020304"))

        field.set_default_value(expected_default_value)

        self.assertEqual(expected_default_value,
                         field.get_default_value(),
                         "Inconsistent Value default_value")
    # end def test_set_default_value

    def test_set_default_value_wrong_type(self):
        """
        Tests the Set_default_value method with wrong type
        """
        field = self._create_field(default_value=HexList("0102030405"),
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
        field = self._create_field(title=expectedTitle)

        self.assertEqual(expectedTitle,
                         field.title,
                         "Inconsistent Value title")
    # end def test_get_title

    def test_set_title(self):
        """
        Tests the SetTitle method
        """
        expectedTitle = "Expected title"
        field = self._create_field(title="Default title")

        field.title = expectedTitle

        self.assertEqual(expectedTitle,
                         field.title,
                         "Inconsistent Value title")
    # end def test_set_title

    def test_set_title_wrong_type(self):
        """
        Tests the SetTitle method with wrong type
        """
        field = self._create_field(title="Expected title")

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
        field = self._create_field(name=expectedName)

        field.name = expectedName

        self.assertEqual(expectedName,
                         field.name,
                         "Inconsistent Value name")
    # end def test_get_name

    def test_set_name(self):
        """
        Tests the SetName method
        """
        expectedName = "Expected Name"
        field = self._create_field(name="Expected Name")

        field.name = expectedName

        self.assertEqual(expectedName,
                         field.name,
                         "Inconsistent name value!")
    # end def test_set_name

    def test_set_name_wrong_type(self):
        """
        Tests the SetName method with wrong type
        """
        field = self._create_field(name="Expected Name")

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
        field = self._create_field(fid=fid,
                                   default_value=HexList("02"),
                                   title="Expected Title")

        expectedLog = "Expected Title: (0x02)"
        obtainedLog = field.create_summary()

        self.assertEqual(expectedLog,
                         obtainedLog,
                         "Inconsistent log")
    # end def test_create_summary

    def test_str(self):
        """
        Tests the __str__ method
        """
        fid = 0x02
        field = self._create_field(fid=fid,
                                   default_value=HexList("02"),
                                   title="Expected Title")

        expectedLog = "Expected Title: (0x02)"
        obtainedLog = str(field)

        self.assertEqual(expectedLog,
                         obtainedLog,
                         "Inconsistent log")
    # end def test_str

    def test_check_value(self):
        """
        Test the checkValue method
        """
        fid = 0x02
        field = self._create_field(fid=fid,
                                   default_value=HexList("02"),
                                   title="Expected Title")

        field.set_has_tag(True)
        self.assertTrue(field.check_value(None),
                        "Inconsistent checkValue result")

        field._checks = (CheckByte(),)

        self.assertRaises(TypeError,
                          field.check_value,
                          "01")

        self.assertTrue(field.check_value(0x01),
                        "Inconsistent checkValue result")

        field._checks = None

        self.assertTrue(field.check_value(0x01),
                        "Inconsistent checkValue result")
    # end def test_check_value


# end class FieldTestCase

class CheckTestCase(TestCase):
    """
    Tests of check functions
    """

    def test_check_bool(self):
        """
        Tests the CheckBoolean method
        """
        checker = CheckBool()

        value = True
        self.assertTrue(checker(value),
                        "value should be accepted as boolean")

        value = False
        self.assertTrue(checker(value),
                        "value should be accepted as boolean")

        value = 1
        self.assertFalse(checker(value),
                         "value should not be accepted as boolean")

        value = "True"
        self.assertFalse(checker(value),
                         "value should not be accepted as boolean")
    # end def test_check_bool

    def test_check_int(self):
        """
        Tests the CheckInt method
        """
        # Neither min_value nor max_value defined
        checker = CheckInt()

        value = 10
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = "10"
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as integer")

        value = HexList("10")
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as integer")

        # min_value defined
        checker = CheckInt(10)

        value = 10
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 256
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 9
        self.assertRaises(ValueError,
                          checker,
                          value)

        # maxValue defined
        checker = CheckInt(max_value=9)

        value = 9
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 0
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 10
        self.assertRaises(ValueError,
                          checker,
                          value)

        # min_value and max_value defined
        checker = CheckInt(min_value=9,
                           max_value=10)

        value = 9
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 10
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 8
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = 11
        self.assertRaises(ValueError,
                          checker,
                          value)
    # end def test_check_int

    def test_check_byte(self):
        """
        Tests the CheckByte method
        """
        checker = CheckByte()

        value = 0
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = 255
        self.assertTrue(checker(value),
                        "value should be accepted as integer")

        value = -1
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = 256
        self.assertRaises(ValueError,
                          checker,
                          value)
    # end def test_check_byte

    def test_check_hex_list(self):
        """
        Tests the CheckHexList method
        """
        checker = CheckHexList(1)

        value = HexList(1)
        self.assertTrue(checker(value),
                        "value should be accepted as HexList")

        value = Numeral(1, 1)
        self.assertTrue(checker(value),
                        "value should be accepted as HexList")

        value = 1
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as HexList")

        value = "01"
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as HexList")

        value = HexList("0102")
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = Numeral(1, 2)
        self.assertRaises(ValueError,
                          checker,
                          value)

        checker = CheckHexList((1, 2))

        value = HexList(1)
        self.assertTrue(checker(value),
                        "value should be accepted as HexList")

        value = HexList(0x01, 0x02)
        self.assertTrue(checker(value),
                        "value should be accepted as HexList")

        value = HexList(0x01, 0x02, 0x03)
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = Numeral(1, 3)
        self.assertRaises(ValueError,
                          checker,
                          value)
    # end def test_check_hex_list

    @ignoredeprecation
    def test_check_list(self):
        """
        Tests the CheckList method
        """
        checker = CheckList(2)

        value = (0x01, 0x02)
        self.assertTrue(checker(value),
                        "value should be accepted as Tuple")

        value = [0x01, 0x02]
        self.assertTrue(checker(value),
                        "value should be accepted as List")

        value = 0x0102
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as List/Tuple")

        value = "0102"
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as List/Tuple")

        value = (0x01,)
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = [0x01]
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = (0x01, 0x02, 0x03)
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = [0x01, 0x02, 0x03]
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = (0x01, "02")
        self.assertRaises(TypeError,
                          checker,
                          value)

        value = [0x01, "02"]
        self.assertRaises(TypeError,
                          checker,
                          value)

        value = (0x01, 0x0200)
        self.assertRaises(ValueError,
                          checker,
                          value)

        value = [0x0100, 0x02]
        self.assertRaises(ValueError,
                          checker,
                          value)
    # end def test_check_list

    def test_check_bit_struct(self):
        """
        Tests the CheckBitStruct method
        """
        checker = CheckBitStruct(1)

        value = BitStruct(HexList(1))
        self.assertTrue(checker(value),
                        "value should be accepted as BitStruct")

        value = 1
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as BitStruct")

        value = HexList(1)
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as BitStruct")

        value = Numeral(1, 1)
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as BitStruct")

        value = "01"
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as BitStruct")

        value = BitStruct(HexList(1, 2))
        self.assertRaises(ValueError,
                          checker,
                          value)
    # end def test_check_bit_struct

    def test_check_none(self):
        """
        Tests the CheckNone method
        """
        checker = CheckNone()

        value = None
        self.assertTrue(checker(value),
                        "value should be accepted as None")

        value = 1
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as None")

        value = HexList(1)
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as None")

        value = Numeral(1, 1)
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as None")

        value = "01"
        self.assertFalse(checker(value),
                         "value shouldn't be accepted as None")
    # end def test_check_none

    def test_check_string(self):
        """
        Tests the CheckString method
        """
        checker = CheckString(length=4)

        self.assertRaises(ValueError,
                          checker,
                          "123")
        self.assertTrue(checker("1234"),
                        "value should be accepted")
        self.assertRaises(ValueError,
                          checker,
                          "12345")

        checker = CheckString(min_length=3, max_length=5)

        self.assertRaises(ValueError,
                          checker,
                          "12")
        self.assertTrue(checker("123"),
                        "value should be accepted")
        self.assertTrue(checker("1234"),
                        "value should be accepted")
        self.assertTrue(checker("12345"),
                        "value should be accepted")
        self.assertRaises(ValueError,
                          checker,
                          "123456")
    # end def test_check_string


# end class CheckTestCase

if __name__ == "__main__":
    from unittest import main

    main()
# end if
# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
