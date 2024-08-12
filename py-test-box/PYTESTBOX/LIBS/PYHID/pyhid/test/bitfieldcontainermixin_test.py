#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
"""
    :package: pyhid.test.bitfieldcontainermixin
    :brief: BitFieldContainerMixin testing module
    :author: Christophe Roquebert
    :date: 2018/12/18
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pylibrary.tools.hexlist import HexList
from pyhid.bitfield import BitField
from pyhid.bitfieldcontainermixin import BitFieldContainerMixin as PyHid_BitFieldContainerMixin
from pyhid.field import Field as PyHid_Field
from pyhid.field import field_length
from unittest import TestCase


# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------
class AbstractFieldContainerMixinTestCase(TestCase):
    """
    Tests of the FieldContainerMixin-derived classes
    """
    FieldContainerMixin = None

    def _createInstance(self, **kwargs):
        """
        Creates a new instance of the class under test.

        @param  kwargs [in] (dict) The keyword arguments

        @return (FieldContainerMixin) The newly created instance
        """
        self.assertTrue(self.FieldContainerMixin is not None,
                        'The %s.%s class must define a FieldContainerMixin class attribute' %
                        (self.__class__.__module__, self.__class__.__name__))

        return self.FieldContainerMixin(**kwargs)                               # pylint:disable=E1102
    # end def _createInstance

    def testConstructor_Default(self):
        """
        Test the class constructor with default values
        """
        if not self.__class__.__name__.startswith('Abstract'):
            instance = self._createInstance()

            self.assertTrue(instance is not None,
                            "Could not create an instance of the class under test")
        # end if
    # end def testConstructor_Default

    def testHexListConsistency(self):
        """
        Tests the consistency between the serialization/deserialization of the object
        """
        if not self.__class__.__name__.startswith('Abstract'):
            expected = self._createInstance()

            raw_value = HexList(expected)
            obtained = expected.__class__.fromHexList(raw_value)

            # Force values resolution for all auto-computed values
            for field in expected.FIELDS:
                value = getattr(expected, field.name)
                setattr(expected, field.name, value)
            # end for

            self.assertEqual(expected,
                             obtained,
                             'Inconsistent %s.%s from instance to HexList to instance:\n expected: %s\n obtained: %s' %
                             (expected.__class__.__module__, expected.__class__.__name__, expected, obtained))
        # end if
    # end def testHexListConsistency

    def testCreateSummary_SmokeTest(self):
        """
        Smoke test of the createSummary for derived types
        """
        if not self.__class__.__name__.startswith('Abstract'):
            instance = self._createInstance()
            obtained = instance.create_summary()

            self.assertNotEqual('', obtained, 'Empty summary')
        # end if
    # end def testCreateSummary_SmokeTest

# end class AbstractFieldContainerMixinTestCase


class TestFieldContainerMixin(PyHid_BitFieldContainerMixin):                 # pylint:disable=W0223
    """
    Class test sub class implementation for FieldContainerMixin class
    """

    # FieldContainerMixin configuration
    VARIABLE = False

    FID_1 = 0x01
    FID_2 = 0x02
    FID_3 = 0x03
    FID_4 = 0x04

    LEN_1 = 0x01 * 8
    LEN_2 = 0x02 * 8
    LEN_3 = 0x03 * 8
    LEN_4 = 0x04 * 8

    class FID(object):
        """
        Field Identifiers
        """
        FIRST = 0x01
        SECOND = 0x02
        THIRD = 0x03
        FOURTH = 0x04
    # end class FID

    class LEN(object):
        """
        Field Lengths
        """
        FIRST = 0x01
        SECOND = 0x02
        THIRD = 0x03
        FOURTH = 0x04
    # end class LEN

    FIELDS = (BitField(FID_1,
                       LEN_1,
                       fid_length=0x00,
                       len_length=0x00,
                       default_value=None,
                       title='Field 1',
                       name='field1'),
              BitField(FID_2,
                       LEN_2,
                       fid_length=0x00,
                       len_length=0x08,
                       default_value=None,
                       title='Field 2',
                       name='field2'),
              BitField(FID_3,
                       LEN_3,
                       fid_length=0x08,
                       len_length=0x00,
                       default_value=field_length(FID_4),
                       title='Field 3',
                       name='field3',
                       optional=True),
              BitField(FID_4,
                       LEN_4,
                       fid_length=0x08,
                       len_length=0x08,
                       default_value=None,
                       title='Field 4',
                       name='field4',
                       optional=True),
              BitField(FID_4,
                       LEN_4,
                       fid_length=0x00,
                       len_length=0x08,
                       default_value=None,
                       title='Field 5',
                       name='field5',
                       optional=True),
              )

# end class TestFieldContainerMixin


class BitFieldContainerMixinTestCase(TestCase):
    """
    BitFieldContainerMixin testing class
    """
    FieldContainerMixin = PyHid_BitFieldContainerMixin
    RefField = BitField

    @classmethod
    def _createInstance(cls, variable=False, mode=None, fields=tuple(), **kwargs):
        """
        Creates an FieldContainerMixin instance.

        This method should be overridden in derived classes, creating relevant
        instances of the class under test

        :param variable: FieldContainerMixin length is variable (optional)
        :type variable: ``int``
        :param mode: The FieldContainerMixin mode (optional)
        :type mode: ``int``
        :param fields: List of fields for the class (optional)
        :type fields: ``tuple``
        :param \**kwargs: The values (optional)
        :type \**kwargs: dict

        :return: Created FieldContainerMixin
        :rtype: ``FieldContainerMixin``
        """
        class BitFieldContainerMixin(cls.FieldContainerMixin):
            """
            Intermediate class that wraps the class method variable
            before construction
            """
            VARIABLE = variable
            MODE = mode

            FIELDS = fields
        # end class BitFieldContainerMixin

        return BitFieldContainerMixin(**kwargs)
    # end def _createInstance

    @classmethod
    def _createField(cls, fid=0x01, length=0x20, fid_length=0x08, len_length=0x08, default_value=None,
                     title='Default title', name=None, aliases=tuple(), optional=None):
        """
        Create a default Field

        :param fid: Field identifier value (optional)
        :type fid: ``int``
        :param length: Field length value (optional)
        :type length: ``int``
        :param fid_length: Field identifier length (optional)
        :type fid_length: ``int``
        :param len_length: Field value length length (optional)
        :type len_length: ``int``
        :param default_value: Default value of the field (optional)
        :type default_value: ``HexList``
        :param title: Field title value (optional)
        :type title: ``str``
        :param name: Field name value (optional)
        :type name: ``str``
        :param aliases: Aliases for this field name (optional)
        :type aliases: ``tuple``
        :param optional: Field is optional or not (optional)
        :type optional: ``bool``

        :return: Created Field
        :rtype: ``Field``
        """
        return cls.RefField(fid=fid,
                            length=length,
                            fid_length=fid_length,
                            len_length=len_length,
                            default_value=default_value,
                            title=title,
                            name=name,
                            aliases=aliases,
                            optional=optional,
                            )
    # end def _createField
#
#     def test1(self):
#         """
#         """
#         instance =  self._createInstance()
#         self.assertEqual(HexList('EE B8 80 00 18 12 82 03'),
#                          HexList(instance))
#     # end def test1

    def testEq(self):
        """
        Tests __eq__ method
        """
        fields1 = (self._createField(fid=0x01),
                   self._createField(fid=0x02))
        expected = self._createInstance(fields=fields1)

        fields2 = (self._createField(fid=0x02),
                   self._createField(fid=0x01))
        obtained = self._createInstance(fields=fields1)

        self.assertEqual(expected,
                         obtained,
                         "Field instances should be equal")

        obtained = self._createInstance(fields=fields2)
        self.assertNotEqual(expected,
                            obtained,
                            "Field instances shouldn't be equal")
    # end def testEq

    def testEq_WrongType(self):
        """
        Tests __eq__ method with wrong type
        """
        field_container_mixin = self._createInstance()

        self.assertRaises(TypeError,
                          field_container_mixin.__eq__,
                          0x01)

        self.assertRaises(TypeError,
                          field_container_mixin.__eq__,
                          "01")

        self.assertRaises(TypeError,
                          field_container_mixin.__eq__,
                          HexList(0x01))
    # end def testEq_WrongType

    def testNe(self):
        """
        Tests the __ne__ method
        """
        # Init field and FieldContainerMixin
        fields1 = (self._createField(fid=0x01),
                   self._createField(fid=0x02))
        fields2 = (self._createField(fid=0x02),
                   self._createField(fid=0x01))

        instance1 = self._createInstance(fields=fields1)
        instance2 = self._createInstance(fields=fields1)

        self.assertFalse(instance1 != instance2,
                         "FieldContainerMixin instances should be equal")

        # Field different
        instance2 = self._createInstance(fields=fields2)
        self.assertTrue(instance1 != instance2,
                        "FieldContainerMixin instances shouldn't be equal (different fields)")

        field = self._createField(fid=0x01,
                                  name="name")

        # Init field and FieldContainerMixin
        instance1 = self._createInstance(fields=(field,))
        instance1.name = HexList("11111111")
        instance2 = self._createInstance(fields=(field,))
        instance2.name = HexList("11111111")

        self.assertFalse(instance1 != instance2,
                         "FieldContainerMixin instances should be equal")

        # Value different
        instance2.name = HexList("22222222")
        self.assertTrue(instance1 != instance2,
                        "FieldContainerMixin instances shouldn't be equal (different values)")
    # end def testNe

    def testAccess_AutomaticGetter(self):
        """
        Tests the __ne__ method
        """
        # Init field and FieldContainerMixin
        fields = (self._createField(fid=0x01, name='field1'),
                  self._createField(fid=0x02, name='field2'))
        instance = self._createInstance(fields=fields)

        # Setter, getter
        expected = HexList('1111')
        obtained = instance.field1
        self.assertNotEqual(expected,
                            obtained,
                            'Invalid default value for field1')
        instance.setField1(expected)
        self.assertEqual(expected,
                         instance.field1,
                         'Invalid value for field1')

        expected = HexList('2222')
        setattr(instance, 'field1', expected)
        self.assertEqual(expected,
                         instance.getField1(),
                         'Invalid value for field1')
    # end def testAccess_AutomaticGetter

    def testAccess_InvalidAttributeAtCreation(self):
        """
        Tests the use of an invalid Key at creation, it should be ignore
        """
        instance = self._createInstance(unDefinedMethod=True)

        self.assertRaises(AttributeError,
                          getattr,
                          instance, 'unDefinedMethod')
    # end def testAccess_InvalidAttribute

    def testAccess_InvalidAttribute(self):
        """
        Tests the use of an invalid Key, by attribute access
        """
        instance = self._createInstance()

        self.assertRaises(AttributeError,
                          getattr,
                          instance, 'unDefinedMethod')
    # end def testAccess_InvalidAttribute

    def _testAccess(self, has_tag, variable, optional):
        """
        Builds a FieldContainerMixin, and tests access to a field that is built
        to have the given specification.

        :param  has_tag: Whether the field has a tag
        :type has_tag: ``bool``
        :param  variable: Whether the field has a length
        :type variable: ``bool``
        :param  optional: Whether the field is optional
        :type optional: ``bool``
        """
        class HexList2(HexList):
            """
            Sub class of HexList to interpret 2-bytes long integers
            """
            @classmethod
            def fromLong(cls, value, **kwargs):                                           # pylint:disable=W0221
                """
                @copydoc pylibrary.tools.hexlist.HexList.fromLong
                """
                return super(HexList2, cls).fromLong(value, 2)
            # end def fromLong
        # end class HexList2

        # Create all fields
        fid = 1
        fields = []
        prefix = {True: '',
                  False: 'No'}
        field_values = {}
        for fieldHasTag in (True, False):
            for fieldVariable in (True, False):
                for fieldOptional in (True, False):
                    field_name = 'field%sTag%sVariable%sOptional' % \
                                (prefix[fieldHasTag], prefix[fieldVariable], prefix[fieldOptional])
                    field = self.RefField(fid,
                                          length=2 * 8,  # Use a fixed length for this test
                                          fid_length=0x08 if fieldHasTag else 0x00,
                                          len_length=0x08 if fieldVariable else 0x00,
                                          name=field_name,
                                          optional=fieldOptional,
                                          conversions={int: HexList2.fromLong})
                    fields.append(field)

                    field_value = HexList(((fid << 4) + fid)) * 2
                    field_values[field_name] = field_value

                    fid += 1
                # end for
            # end for
        # end for

        class TestClass(self.FieldContainerMixin):
            """
            Inner test class, defining the fields.
            """
            TAG = 0xEE
            VARIABLE = False

            FIELDS = tuple(fields)
        # end class TestClass

        field_name = 'field%sTag%sVariable%sOptional' % (prefix[has_tag], prefix[variable], prefix[optional])
        expected = TestClass(**field_values)
        raw_data = HexList(expected)
        obtained = TestClass.fromHexList(raw_data)

        self.assertEqual(expected,
                         obtained,
                         'Inconsistent HexList serialization/deserialization')

        self.assertEqual(field_values[field_name],
                         getattr(obtained, field_name),
                         'Inconsistent field value')
    # end def _testAccess

    def testAccess_TagVariableOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=True,
                         variable=True,
                         optional=True)
    # end def testAccess_TagVariableOptional

    def testAccess_TagVariableNoOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=True,
                         variable=True,
                         optional=False)
    # end def testAccess_TagVariableNoOptional

    def testAccess_TagNoVariableOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=True,
                         variable=False,
                         optional=True)
    # end def testAccess_TagNoVariableOptional

    def testAccess_TagNoVariableNoOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=True,
                         variable=False,
                         optional=False)
    # end def testAccess_TagNoVariableNoOptional

    def testAccess_NoTagVariableOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=False,
                         variable=True,
                         optional=True)
    # end def testAccess_NoTagVariableOptional

    def testAccess_NoTagVariableNoOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=False,
                         variable=True,
                         optional=False)
    # end def testAccess_NoTagVariableNoOptional

    def testAccess_NoTagNoVariableOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=False,
                         variable=False,
                         optional=True)
    # end def testAccess_NoTagNoVariableOptional

    def testAccess_NoTagNoVariableNoOptional(self):
        """
        Tests access consistency
        """
        self._testAccess(has_tag=False,
                         variable=False,
                         optional=False)
    # end def testAccess_NoTagNoVariableNoOptional

    def testGetAttr(self):
        """
        Tests the __getattr__ method
        """

        fid = 0x01
        fields = (self._createField(fid,
                                    name="field1",
                                    aliases=('fieldAlias1', 'fieldAlias2')),)
        instance = self._createInstance(fields=fields)

        instance.setValue(fid, HexList("11111111"))

        self.assertEqual(HexList("11111111"),
                         instance.field1,
                         "Inconsistent value!")

        self.assertEqual(HexList("11111111"),
                         instance.fieldAlias1,
                         "Inconsistent value in alias")

        self.assertEqual(HexList("11111111"),
                         instance.fieldAlias2,
                         "Inconsistent value in alias")
    # end def testGetAttr

    def testSetAttr(self):
        """
        Tests the __setattr__ method
        """
        fid = 0x01
        fields = (self._createField(fid,
                                    name="field1",
                                    aliases=('fieldAlias1', 'fieldAlias2')),)
        instance = self._createInstance(fields=fields)

        setattr(instance, 'field1', HexList("11111111"))

        self.assertEqual(HexList("11111111"),
                         instance.field1,
                         "Inconsistent value between set and get")

        setattr(instance, 'fieldAlias1', HexList("22222222"))
        self.assertEqual(HexList("22222222"),
                         instance.field1,
                         "Inconsistent value when setting alias")

        setattr(instance, 'fieldAlias2', HexList("33333333"))
        self.assertEqual(HexList("33333333"),
                         instance.field1,
                         "Inconsistent value when setting alias")
    # end def testSetAttr

    def testGetValue(self):
        """
        Tests the GetValue method
        """
        # Value exits
        expected = HexList("11111111")

        fid = 0x01
        fields = (self._createField(fid,
                                    default_value=expected,
                                    name="field1"),)
        instance = self._createInstance(fields=fields)

        self.assertEqual(expected,
                         instance.getValue(fid),
                         "Inconsistent value")

        # Value don't exits
        expected = HexList("22222222")

        fields = (self._createField(fid,
                                    default_value=expected,
                                    name="bDateTime"),)
        instance = self._createInstance(fields=fields)

        self.assertEqual(expected,
                         instance.getValue(fid, True),
                         "Inconsistent value")
    # end def testGetValue

    def testSetValue(self):
        """
        Tests the SetValue method
        """
        expected = HexList("11111111")

        fid = 0x01
        fields = (self._createField(fid,
                                    length=0x04,
                                    name="field1",),)
        instance = self._createInstance(fields=fields)

        instance.setValue(fid, expected)

        self.assertEqual(expected,
                         instance.field1,
                         "Inconsistent value!")
    # end def testSetValue

    def testDebug(self):
        """
        Tests the _debug method
        """
        fields = (self._createField(fid=0x01,
                                    name="name1"),
                  self._createField(fid=0x02,
                                    name="name2"))
        instance = self._createInstance(fields=fields,
                                        name1=HexList("11111111"),
                                        name2=HexList("22222222"))

        expected = {'name1': HexList("11111111"),
                    'name2': HexList("22222222")}
        obtained = instance.debug

        self.assertEqual(expected,
                         obtained,
                         "Inconsistent value")
    # end def testDebug

    def testGet_default_value(self):
        """
        Tests get_default_value method
        """
        expected = HexList("11111111")

        fid = 0x01
        fields = (self._createField(fid,
                                    default_value=expected,
                                    name="field1"),)
        instance = self._createInstance(fields=fields)
        obtained = instance.get_default_value(fid)

        self.assertEqual(expected,
                         obtained,
                         "Inconsistent value")
    # end def testGet_default_value

    def testGet_default_value_Dynamic(self):
        """
        Tests get_default_value, when the default value is a callable
        """

        fid1 = 0x01
        fid2 = 0x02
        value = HexList('0102030405')
        fields = (self._createField(fid1,
                                    default_value=field_length(fid2),
                                    name="field1"),
                  self._createField(fid2,
                                    default_value=value,
                                    name="field2"))
        instance = self._createInstance(fields=fields)

        expected = len(value)
        self.assertEqual(expected,
                         instance.get_default_value(fid1),
                         "Inconsistent value")
    # end def testGet_default_value_Dynamic

    def testGetName(self):
        """
        Tests the get_field_name method
        """
        instance = self._createInstance()

        self.assertEqual(self.FieldContainerMixin.__name__,
                         instance.get_field_name(),
                         "Wrong FieldContainerMixin name")
    # end def testGetName

    def testSetName(self):
        """
        Tests the set_field_name method
        """
        instance = self._createInstance()

        expected = "New FieldContainerMixin name"

        instance.set_field_name(expected)

        self.assertEqual(expected,
                         instance.get_field_name(),
                         "Wrong FieldContainerMixin name")
    # end def testSetName

    def testSetName_WrongType(self):
        """
        Tests the set_field_name method with a wrong type
        """
        instance = self._createInstance()

        self.assertRaises(TypeError,
                          instance.set_field_name,
                          0x01)

        self.assertRaises(TypeError,
                          instance.set_field_name,
                          HexList(0x01))
    # end def testSetName_WrongType

    def _testCreateSummary(self, missing=True, extraneous=True, omit_name=False):
        """
        Tests the createSummary method with instance in mode Default

        :param missing: Indicates if we test if elements are missing (optional)
        :type missing: ``bool``
        :param extraneous: Indicates if we test if extra elements are present (optional)
        :type extraneous: ``bool``
        :param omit_name: Indicate if we take into account the name or not (optional)
        :type omit_name: ``bool``
        """
        assert (missing or extraneous), ValueError('At least one check condition is needed')

        # 1st case : 2 defined values
        # ---------------------------
        fields = (self._createField(fid=0x01,
                                    length=0x20,
                                    name="name1"),
                  self._createField(fid=0x02,
                                    length=0x20,
                                    name="name2"))

        instance = self._createInstance(fields=fields,
                                        name1=HexList("11 11 11 11"),
                                        name2=HexList("22 22 22 22"))

        expected_lines = []
        if not omit_name:
            expected_lines.append('%s: 0x%s' % (self.FieldContainerMixin.__name__, HexList(instance)))
        else:
            expected_lines.append('%s' % HexList(instance))
        # end if
        expected_lines.extend(('  - Default title: (0x01) 0x11111111',
                              '  - Default title: (0x02) 0x22222222'))

        expected_log = '\n'.join(expected_lines)
        obtained_log = instance.create_summary()

        expected_table = expected_log.split('\n')
        obtained_table = obtained_log.split('\n')

        if extraneous:
            for elt in obtained_table:
                assert (elt in expected_table), \
                       "Surplus element of log! %s" % elt
            # end for
        # end if

        if missing:
            for elt in expected_table:
                assert (elt in obtained_table), \
                       "Missing element of log! %s" % elt
            # end for
        # end if

        # 2nd case : 1 defined value and 1 value undefined
        # ------------------------------------------------
        fields = (self._createField(fid=0x01,
                                    title='Title1',
                                    name='name1'),
                  self._createField(fid=0x02,
                                    title='Title2',
                                    name='name2',
                                    default_value=HexList("02")))

        instance = self._createInstance(fields=fields,
                                        name1=HexList("01"))

        expected_log = '%s: 0x%s' % (self.FieldContainerMixin.__name__, HexList(instance)) if not omit_name else \
            ('%s\n' % HexList(instance))
        expected_log += '\n  - Title1: (0x01) 0x01'
        expected_log += '\n  - Title2: (0x02) 0x02'
        obtained_log = instance.create_summary()

        expected_table = expected_log.split('\n')
        obtained_table = obtained_log.split('\n')

        if extraneous:
            for elt in obtained_table:
                self.assertTrue((elt in expected_table),
                                "Surplus element of log! %s" % elt)
            # end for
        # end if

        if missing:
            for elt in expected_table:
                self.assertTrue((elt in obtained_table),
                                "Missing element of log! %s" % elt)
            # end for
        # end if
    # end def _testCreateSummary_ModeDefault

    def testCreateSummary_ModeDefault(self):
        """
        Tests the createSummary method with fieldcontainermixin in mode Default
        """
        self._testCreateSummary(missing=True, extraneous=True)
    # end def testCreateSummary_ModeDefault

    def testGetFieldDefinition(self):
        """
        Tests GetFieldDefinition method
        """
        fid = 0x01
        expected = self._createField(fid=fid)

        instance = self._createInstance(fields=(expected,))

        self.assertEqual(expected,
                         instance.getFieldDefinition(fid),
                         "Field of FieldContainerMixin instance should be equal")
    # end def testGetFieldDefinition

    def testGetFieldDefinition_WrongValue(self):
        """
        Tests GetFieldDefinition method with wrong value
        """
        instance = self._createInstance()

        self.assertRaises(ValueError,
                          instance.getFieldDefinition,
                          0x01)

        self.assertRaises(ValueError,
                          instance.getFieldDefinition,
                          0x02)
    # end def testGetFieldDefinition_WrongValue

    def testGetFieldCount(self):
        """
        Tests getFieldCount method
        """
        instance = self._createInstance()

        # Tests empty instance
        initial_field_count = len(self.FieldContainerMixin.FIELDS)
        self.assertEqual(initial_field_count,
                         instance.getFieldCount(),
                         "Incorrect value")

        # Tests 2 fields in the instance
        fields = (self._createField(fid=0x01),
                  self._createField(fid=0x02))

        instance = self._createInstance(fields=fields)

        self.assertEqual(len(fields),
                         instance.getFieldCount(),
                         "Incorrect value")
    # end def testGetFieldCount

    def _testHexList(self):
        """
        Tests the __hexlist__ method
        """
        field_length = 4 * 8                                                     # pylint:disable=W0621

        fid = 1
        fields = []
        prefix = {True: '',
                  False: 'No'}
        field_values = {}

        expected = HexList()
        for fieldHasTag in (True, False):
            for fieldVariable in (True, False):
                for fieldOptional in (True, False):
                    field_name = 'field%sTag%sVariable%sOptional' % (prefix[fieldHasTag],
                                                                     prefix[fieldVariable],
                                                                     prefix[fieldOptional])
                    field = self.RefField(fid,
                                          length=field_length,  # Use a fixed length for this test
                                          fid_length=0x08 if fieldHasTag else 0x00,
                                          len_length=0x08 if fieldVariable else 0x00,
                                          name=field_name,
                                          optional=fieldOptional)
                    fields.append(field)

                    field_value = HexList(((fid << 4) + fid)) * (field_length // 8)
                    field_values[field_name] = field_value

                    # Build the expected value
                    if fieldHasTag:
                        expected.append(fid)
                    # end if

                    if fieldVariable:
                        expected.append(field_length)
                    # end if

                    expected.extend(field_value)

                    fid += 1
                # end for
            # end for
        # end for

        instance = self._createInstance(variable=False,
                                        fields=tuple(fields),
                                        **field_values)

        obtained = HexList(instance)

        self.assertEqual(expected,
                         obtained,
                         "Inconsistent HexList representation of FieldContainerMixin")
    # end def _testHexList

    def testHexList(self):
        """
        Tests the __hexlist__ method
        """
        self._testHexList()
    # end def testHexList

    def testStr(self):
        """
        Tests the __str__ method
        """
        fields = (self._createField(fid=0x01,
                                    name="name1"),
                  self._createField(fid=0x02,
                                    name="name2"))

        instance = self._createInstance(variable=False,
                                        fields=fields,
                                        name1=HexList("11 11 11 11"),
                                        name2=HexList("22 22 22 22"))

        expected_log = '\n'.join(('%s: 0x%s' % (instance.__class__.__name__, HexList(instance)),
                                  '  - Default title: (0x01) 0x11111111',
                                  '  - Default title: (0x02) 0x22222222'))
        obtained_log = str(instance)

        expected_table = expected_log.split('\n')
        obtained_table = obtained_log.split('\n')

        for elt in obtained_table:
            assert (elt in expected_table), \
                   "Surplus element of log! %s" % elt
        # end for

        for elt in expected_table:
            assert (elt in obtained_table), \
                   "Missing element of log! %s" % elt
        # end for
    # end def testStr

    def _testRepr(self, missing=True, extraneous=True):
        """
        Tests the __repr__ method

        :param missing: Indicates if we test if elements are missing (optional)
        :type missing: ``bool``
        :param extraneous: Indicates if we test if extra elements are present (optional)
        :type extraneous: ``bool``
        """

        fields = (self._createField(fid=0x01,
                                    name="name1"),
                  self._createField(fid=0x02,
                                    name="name2"))

        instance = self._createInstance(variable=False,
                                        fields=fields,
                                        name1=HexList("11111111"),
                                        name2=HexList("22222222"))

        expected_elements = []
        expected_elements.extend(("name1=HexList('11111111')",
                                  "name2=HexList('22222222')"))

        obtained = instance.__repr__()
        self.assertEqual(obtained[-1],
                         ')',
                         'Representation does not end with \')\'')

        obtained_string = obtained[obtained.index('(')+1:-1]
        obtained_elements = [e.strip() for e in obtained_string.split(',')]

        if extraneous:
            for elt in obtained_elements:
                assert (elt in expected_elements), \
                       "Surplus element of log: %s" % elt
            # end for
        # end if

        if missing:
            for elt in expected_elements:
                assert (elt in obtained_elements), \
                       "Missing element of log: %s" % elt
            # end for
        # end if
    # end def _testRepr

    def testRepr(self):
        """
        Tests the __repr__ method
        """
        self._testRepr(missing=True, extraneous=True)
    # end def testRepr

    def testFromHexList_AllFields(self):
        """
        Tests the fromHexList method
        """
        data = HexList("1110222203333333042044444444")
        # All fields present
        obtained = TestFieldContainerMixin().fromHexList(data)

        expected = TestFieldContainerMixin()
        expected.field1 = HexList("11")                                          # pylint:disable=W0201
        expected.field2 = HexList("2222")                                        # pylint:disable=W0201
        expected.field3 = HexList("333333")                                      # pylint:disable=W0201
        expected.field4 = HexList("44444444")                                    # pylint:disable=W0201

        self.assertEqual(expected,
                         obtained,
                         "Inconsistent fieldcontainermixin interpretation")

        # All fields present
        obtained = TestFieldContainerMixin().fromHexList(HexList('0000', data, '0000'),
                                                         offset=2 * 8,
                                                         length=len(data) * 8)
        self.assertEqual(expected,
                         obtained,
                         "Inconsistent fieldcontainermixin interpretation")
    # end def testFromHexList_AllFields

    def testFromHexList_MissingOptional_Middle(self):
        """
        Tests the fromHexList method
        """
        # 1 optional field is absent
        fieldcontainermixin = TestFieldContainerMixin().fromHexList(HexList("11102222042044444444"))

        expected_field_container_mixin = TestFieldContainerMixin()
        expected_field_container_mixin.field1 = HexList("11")                       # pylint:disable=W0201
        expected_field_container_mixin.field2 = HexList("2222")                     # pylint:disable=W0201
        expected_field_container_mixin.field4 = HexList("44444444")                 # pylint:disable=W0201

        self.assertEqual(expected_field_container_mixin,
                         fieldcontainermixin,
                         "Inconsistent fieldcontainermixin interpretation")
    # end def testFromHexList_MissingOptional_Middle

    def testFromHexList_MissingOptional_End(self):
        """
        Tests the fromHexList method
        """
        # 1 optional field is absent
        fieldcontainermixin = TestFieldContainerMixin().fromHexList(HexList("1110222203333333"))

        expected_field_container_mixin = TestFieldContainerMixin()
        expected_field_container_mixin.field1 = HexList("11")                       # pylint:disable=W0201
        expected_field_container_mixin.field2 = HexList("2222")                     # pylint:disable=W0201
        expected_field_container_mixin.field3 = HexList("333333")                   # pylint:disable=W0201

        self.assertEqual(expected_field_container_mixin,
                         fieldcontainermixin,
                         "Inconsistent fieldcontainermixin interpretation")
    # end def testFromHexList_MissingOptional_End

    def testFromHexList_MissingOptional_MiddleEnd(self):
        """
        Tests the fromHexList method
        """
        # 2 optional fields are absent
        fieldcontainermixin = TestFieldContainerMixin().fromHexList(HexList("11102222"))

        expected_field_container_mixin = TestFieldContainerMixin()
        expected_field_container_mixin.field1 = HexList("11")                       # pylint:disable=W0201
        expected_field_container_mixin.field2 = HexList("2222")                     # pylint:disable=W0201

        self.assertEqual(expected_field_container_mixin,
                         fieldcontainermixin,
                         "Inconsistent fieldcontainermixin interpretation")
    # end def testFromHexList_MissingOptional_MiddleEnd

    def testFromHexList_WrongValue(self):
        """
        Tests the fromHexList method with a not present mandatory field
        """
        fieldcontainermixin = TestFieldContainerMixin()

        self.assertRaises(ValueError,
                          fieldcontainermixin.fromHexList,
                          HexList("01"))
    # end def testFromHexList_WrongValue

    def _testGetFieldOffset(self, initial_offset=0):
        """
        Tests the getFieldOffset method

        :param  initial_offset: Initial offset to take into account before starting computation (optional)
        :type initial_offset: ``int``
        """
        field1 = self._createField(0x01,
                                   fid_length=0x00,
                                   len_length=0x00,
                                   optional=False,
                                   default_value=None,
                                   name="field1")
        field2 = self._createField(0x02,
                                   fid_length=0x00,
                                   len_length=0x08,
                                   optional=False,
                                   default_value=None,
                                   name="field2")
        field3 = self._createField(0x03,
                                   fid_length=0x08,
                                   len_length=0x00,
                                   optional=True,
                                   default_value=None,
                                   name="field3")
        field4 = self._createField(0x04,
                                   fid_length=0x08,
                                   len_length=0x08,
                                   optional=True,
                                   default_value=None,
                                   name="field4")
        field5 = self._createField(0x05,
                                   fid_length=0x08,
                                   len_length=0x08,
                                   optional=True,
                                   default_value=None,
                                   name="field5")

        instance = self._createInstance(fields=(field1, field2, field3, field4, field5),
                                        field1=HexList(0x11) * field1.length,
                                        field2=HexList(0x22) * field2.length,
                                        field4=HexList(0x44) * field4.length)

        self.assertEqual(initial_offset +
                         field1.length +  # No tag, no length, value (mandatory)
                         8,  # No tag, length, target field
                         instance.getFieldOffset(field2.fid),
                         "Inconsistent field offset!")

        expected = (initial_offset +
                    field1.length +  # No tag, no length, value (mandatory)
                    (8 + field2.length) +  # No tag, length, value (mandatory)
                    0 +  # Omitted tag, omitted length, no value (optional)
                    (8 + 8))              # Tag, length, target field
        obtained = instance.getFieldOffset(field4.fid)
        self.assertEqual(expected,
                         obtained,
                         "Inconsistent field offset!")

        instance.field3 = HexList(0x33) * field3.length                          # pylint:disable=W0201

        self.assertEqual(initial_offset +
                         field1.length +  # No tag, no length, value (mandatory)
                         (8 + field2.length) +  # No tag, length, value (mandatory)
                         (8 + field3.length) +  # Tag, omitted length, value (optional)
                         (0x10 + field4.length) +  # Tag, length, value (optional)
                         0, +  # Nothing (target field, not present)
                         instance.getFieldOffset(field5.fid),
                         "Inconsistent field offset!")

    # end def _testGetFieldOffset

    def testGetFieldOffset(self):
        """
        Tests the getFieldOffset method
        """
        self._testGetFieldOffset(initial_offset=0)
    # end def testGetFieldOffset
#
#     def testArrayFieldAccess_FixedSize(self):
#         """
#         Tests the __getattr__ method
#         """
#         class InnerTestFieldContainerMixin(self.FieldContainerMixin):
#             """
#             Test class
#             """
#             VARIABLE = False
#
#             FIELDS = (self.RefField(fid          = 0x01,
#                                     length       = 0x05 * 8,
#                                     fid_length    = 0x08,
#                                     len_length    = 0x08,
#                                     default_value = HexList('1111111111'),
#                                      title        = 'Field1',
#                                      name         = 'field1'),
# #                       PyHid_ArrayField(fid          = 0x02,
# #                                           length       = 0x04,
# #                                           has_tag       = True,
# #                                           variable     = True,
# #                                           default_value = HexList('22222222'),
# #                                           title        = 'Field2',
# #                                           name         = 'field2',
# #                                           size         = 3),
#                       self.RefField(fid          = 0x03,
#                                     length       = 0x03 * 8,
#                                     fid_length    = 0x08,
#                                     len_length    = 0x08,
#                                     default_value = HexList('333333'),
#                                     title        = 'Field3',
#                                     name         = 'field3'),
#                       )
#         # end class InnerTestFieldContainerMixin
#
#         instance = InnerTestFieldContainerMixin(field1 = HexList('1122334455'),
#                                                 field3 = HexList('112233'))
# #         instance.field2[0]   = HexList('11223344')
# #         instance.field2[1:3] = (HexList('55667788'),
# #                                 HexList('99AABBCC'))
# #
# #         expected = HexList('01051122334455',
# #                           ('020411223344', '020455667788', '020499AABBCC'),
# #                           '0303112233')
# #         obtained = HexList(instance)
# #         self.assertEqual(expected,
# #                          obtained,
# #                          "Inconsistent value for ArrayField HexList conversion")
#
#         expected = instance
#         obtained = instance.fromHexList(HexList(instance))
#         self.assertEqual(expected,
#                          obtained,
#                          "Inconsistent value for ArrayField fromHexList conversion")
#
#         self.assertEqual(3,
#                          len(obtained.field2),
#                          'Inconsistent length of ArrayField value')
#
#         self.assertEqual(HexList('11223344'),
#                          obtained.field2[0],
#                          'Inconsistent length of ArrayField value[0]')
#         self.assertEqual(HexList('55667788'),
#                          obtained.field2[1],
#                          'Inconsistent length of ArrayField value[1]')
#         self.assertEqual(HexList('99AABBCC'),
#                          obtained.field2[2],
#                          'Inconsistent length of ArrayField value[2]')
#     # end def testArrayFieldAccess_FixedSize
#
#     def testArrayFieldAccess_UnsetSize(self):
#         """
#         Tests the __getattr__ method
#         """
#         class InnerTestFieldContainerMixin(self.FieldContainerMixin):
#             """
#             Test class
#             """
#             VARIABLE = False
#
#             FIELDS = (self.RefField(fid          = 0x01,
#                                     length       = 0x05,
#                                     fid_length    = 0x08,
#                                     len_length    = 0x08,
#                                     default_value = HexList('1111111111'),
#                                     title        = 'Field1',
#                                     name         = 'field1'),
# #                       PyHid_ArrayField(fid          = 0x02,
# #                                           length       = 0x04,
# #                                           has_tag       = True,
# #                                           variable     = True,
# #                                           default_value = HexList('22222222'),
# #                                           title        = 'Field2',
# #                                           name         = 'field2',
# #                                           size         = None)
#                       )
#         # end class InnerTestFieldContainerMixin
#
#         instance = InnerTestFieldContainerMixin(field1 = HexList('1122334455'))
# #         instance.field2[0]   = HexList('11223344')
# #         instance.field2[1:3] = (HexList('55667788'),
# #                                 HexList('99AABBCC'))
# #
# #         expected = HexList('01051122334455',
# #                           ('020411223344', '020455667788', '020499AABBCC'),
# #                           )
# #         obtained = HexList(instance)
# #         self.assertEqual(expected,
# #                          obtained,
# #                          "Inconsistent value for ArrayField HexList conversion")
#
#         expected = instance
#         obtained = instance.fromHexList(HexList(instance))
#         self.assertEqual(expected,
#                          obtained,
#                          "Inconsistent value for ArrayField fromHexList conversion")
#
#         self.assertEqual(3,
#                          len(obtained.field2),
#                          'Inconsistent length of ArrayField value')
#
#         self.assertEqual(HexList('11223344'),
#                          obtained.field2[0],
#                          'Inconsistent length of ArrayField value[0]')
#         self.assertEqual(HexList('55667788'),
#                          obtained.field2[1],
#                          'Inconsistent length of ArrayField value[1]')
#         self.assertEqual(HexList('99AABBCC'),
#                          obtained.field2[2],
#                          'Inconsistent length of ArrayField value[2]')
#     # end def testArrayFieldAccess_UnsetSize

    def testCopy(self):
        """
        Tests copy method
        """
        field1 = self._createField(0x01,
                                   fid_length=0x00,
                                   len_length=0x00,
                                   optional=False,
                                   default_value=None,
                                   name="field1")
        field2 = self._createField(0x02,
                                   fid_length=0x00,
                                   len_length=0x08,
                                   optional=False,
                                   default_value=None,
                                   name="field2")
        field3 = self._createField(0x03,
                                   fid_length=0x08,
                                   len_length=0x00,
                                   optional=True,
                                   default_value=None,
                                   name="field3")
        field4 = self._createField(0x04,
                                   fid_length=0x08,
                                   len_length=0x08,
                                   optional=True,
                                   default_value=None,
                                   name="field4")
        field5 = self._createField(0x05,
                                   fid_length=0x08,
                                   len_length=0x08,
                                   optional=True,
                                   default_value=None,
                                   name="field5")

        instance = self._createInstance(fields=(field1, field2, field3, field4, field5),
                                        field1=HexList(0x11) * field1.length,
                                        field2=HexList(0x22) * field2.length,
                                        field4=HexList(0x44) * field4.length)

        instance2 = instance.copy()

        self.assertEqual(instance, instance2)

    # end def testCopy

    def testMixFieldAndBitField(self):
        """
        Tests BitFieldContainerMixin containing Fields and BitFields
        """
        field1 = self._createField(0x01,
                                   fid_length=0x00,
                                   len_length=0x00,
                                   optional=False,
                                   default_value=None,
                                   name="field1")
        field2 = PyHid_Field(0x02,
                             length=0x02,
                             has_tag=False,
                             variable=True,
                             optional=False,
                             default_value=None,
                             name="field2")
        field3 = self._createField(0x03,
                                   fid_length=0x08,
                                   len_length=0x00,
                                   optional=True,
                                   default_value=None,
                                   name="field3")
        field4 = PyHid_Field(0x04,
                             length=0x02,
                             has_tag=True,
                             variable=True,
                             optional=True,
                             default_value=None,
                             name="field4")
        field5 = self._createField(0x05,
                                   fid_length=0x08,
                                   len_length=0x08,
                                   optional=True,
                                   default_value=None,
                                   name="field5")

        instance = self._createInstance(fields=(field1, field2, field3, field4, field5),
                                        field1=HexList(0x11) * (field1.length // 8),
                                        field2=HexList(0x22) * field2.length,
                                        field4=HexList(0x44) * field4.length)

        data = HexList(instance)
        obtained = instance.fromHexList(data)
        self.assertEqual(instance, obtained)

    # end def testMixFieldAndBitField
# end class BitFieldContainerMixinTestCase

# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
