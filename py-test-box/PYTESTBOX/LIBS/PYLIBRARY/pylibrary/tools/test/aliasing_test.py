#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
"""
    :package: pylibrary.tools.test.aliasing_test
    :brief: Aliasing tests implementation
    :author: Christophe Roquebert
    :date: 2018/10/08
"""
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.aliasing import aliases
from pylibrary.tools.aliasing import aliased
from pylibrary.tools.deprecation import ignoredeprecation
from unittest import TestCase


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class AliasingTestCase(TestCase):
    """
    Aliasing test implementation.
    """

    @ignoredeprecation
    def test_alias(self):
        """
        Tests simple class method alias
        """
        value = 5

        class MyClass(object, metaclass=aliases({'ALIAS': 'TARGET.VALUE'},
                                                warning_format='%(alias)s is deprecated, use %(target)s instead.')):
            """
            Test class
            """

            class TARGET(object):
                """
                Test subclass
                """
                VALUE = value
            # end class TARGET
        # end class MyClass

        # Test getter
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        value = 7
        MyClass.TARGET.VALUE = value
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test setter
        value = 8
        MyClass.ALIAS = value
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test instance access
        value = 9
        MyClass.ALIAS = value
        instance = MyClass()
        self.assertEqual(instance.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(instance.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')
    # end def test_alias

    @ignoredeprecation
    def test_inheritance(self):
        """
        Tests inheritance behavior
        """
        value = 5

        class ParentClass(object):
            """
            Parent test class
            """

            def __init__(self):
                """
                Constructor
                """
                self.instance_variable = 1
            # end def __init__

            @classmethod
            def class_method(cls):
                """
                Test class method

                :return: 0
                """
                return 0
            # end def class_method

            def instance_method(self):                                   # pylint:disable=R0201
                """
                Test instance method

                :return: 1
                """
                return self.instance_variable
            # end def instance_method
        # end class ParentClass

        class MyClass(ParentClass,
                      metaclass=aliases({'ALIAS': 'TARGET.VALUE'},
                                        warning_format='%(alias)s is deprecated, use %(target)s instead.')):
            """
            Test class
            """

            class TARGET(object):
                """
                Test subclass
                """
                VALUE = value
            # end class TARGET
        # end class MyClass

        # Test getter
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        value = 7
        MyClass.TARGET.VALUE = value
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test setter
        value = 8
        MyClass.ALIAS = value
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test inheritance
        instance = MyClass()
        self.assertTrue(isinstance(instance, MyClass),
                        'Invalid direct inheritance')
        self.assertTrue(isinstance(instance, ParentClass),
                        'Invalid direct inheritance')
        self.assertEqual(0,
                         MyClass.class_method(),
                         'Invalid class method call')
        self.assertEqual(1,
                         instance.instance_method(),
                         'Invalid instance method call')
    # end def test_inheritance

    # This test is unactivated because in python 3 the metaclass is done differently
    @ignoredeprecation
    def _test_complex_inheritance(self):
        """
        Tests inheritance behavior
        """
        value = 5

        class ParentClass(object):
            """
            Parent test class
            """

            def __init__(self):
                """
                Constructor
                """
                self.instance_variable = 1
            # end def __init__

            @classmethod
            def class_method(cls):
                """
                Test class method
                :return: 0
                """
                return 0
            # end def class_method

            def instance_method(self):                               # pylint:disable=R0201
                """
                Test instance method

                :return: 1
                """
                return self.instance_variable
            # end def instance_method
        # end class ParentClass

        class MyClass(ParentClass,
                      metaclass=aliases({'ALIAS': 'TARGET.VALUE'},
                                        warning_format='%(alias)s is deprecated, use %(target)s instead.')):
            """
            Test class
            """

            class TARGET(object):
                """
                Test subclass
                """
                VALUE = value
            # end class TARGET
        # end class MyClass

        class ChildClass(MyClass, metaclass=aliases({'ALIAS2': 'TARGET.VALUE'},
                                                    parents=(MyClass,),
                                                    warning_format='%(alias)s is deprecated, use %(target)s instead.')):
            """
            Test class
            """
        # end class ChildClass

        # Test getter
        self.assertEqual(ChildClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(ChildClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        value = 7
        ChildClass.TARGET.VALUE = value
        self.assertEqual(ChildClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(ChildClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test setter
        value = 8
        ChildClass.ALIAS = value
        self.assertEqual(ChildClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(ChildClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test inheritance
        instance = ChildClass()
        self.assertTrue(isinstance(instance, ChildClass),
                        'Invalid direct inheritance')
        self.assertTrue(isinstance(instance, ParentClass),
                        'Invalid direct inheritance')
        self.assertEqual(0,
                         ChildClass.class_method(),
                         'Invalid classmethod call')
        self.assertEqual(1,
                         instance.instance_method(),
                         'Invalid instancemethod call')

        # Test getter
        self.assertEqual(ChildClass.ALIAS2,                                   # pylint:disable=E1101
                         value,
                         'Unable to obtain aliased property')
    # end def test_complex_inheritance

    def test_aliased_function(self):
        """
        Tests function parameter aliasing
        """

        # Replace source by target
        @aliased(source='target', source1='target', source2='target')
        def function_1(target):
            """
            Target function for the alias

            :param target: The target parameter
            :type target: ``object``

            :return: The target parameter, for checks
            """
            return target
        # end def function_1

        value = 5
        self.assertEqual(value,
                         function_1(value),
                         'Incorrect normal call')

        value = 6
        self.assertEqual(value,
                         function_1(target=value),
                         'Incorrect normal call')

        value = 7
        self.assertEqual(value,
                         function_1(source=value),                           # pylint:disable=E1120,E1123
                         'Incorrect normal call')

        with self.assertRaises(ValueError):
            function_1(source1=value, source2=value)
    # end def test_aliased_function

    @ignoredeprecation
    def test_alias_overridden_getattr(self):
        """
        Tests aliasing, when the aliased class overrides __getattr__
        """
        value = 5

        class MyClass(object, metaclass=aliases({'ALIAS': 'TARGET.VALUE'},
                                                warning_format='%(alias)s is deprecated, use %(target)s instead.')):
            """
            Test class
            """

            class TARGET(object):
                """
                Test subclass
                """
                VALUE = value
            # end class TARGET

            def __getattr__(self, name):
                if name == 'ALIAS_INSTANCE':
                    return self.TARGET.VALUE
                # end if

                raise AttributeError('No attribute: name')
            # end def __getattr__
        # end class MyClass

        # Test getter
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        value = 7
        MyClass.TARGET.VALUE = value
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')

        # Test setter
        value = 8
        MyClass.ALIAS = value
        self.assertEqual(MyClass.ALIAS,
                         value,
                         'Unable to obtain aliased property')
        self.assertEqual(MyClass.TARGET.VALUE,
                         value,
                         'Unable to obtain aliased property')
    # end def test_alias_overridden_getattr
# end class AliasingTestCase

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
