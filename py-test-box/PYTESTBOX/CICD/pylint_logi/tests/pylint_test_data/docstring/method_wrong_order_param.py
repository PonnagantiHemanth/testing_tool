"""
:package: method_wrong_order_param
:brief: sample file where parameters are in the reversed order
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""
from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:
    """
    Doc string sample test class
    """

    def param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param a: a parameter
        :type a: ``object``
        """
        raise NotImplementedAbstractMethodError()
    # end def param_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param a: a parameter
        :type a: ``object``

        :return: a value
        :rtype: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def return_param_method
# end class TestClassBase


class TestOverrideRepeatDocs(TestClassBase):
    """
    Doc string sample test class repeating the docstring
    """

    def param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param a: a parameter
        :type a: ``object``
        """
        pass

    # end def param_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param a: a parameter
        :type a: ``object``

        :return: a value
        :rtype: ``int``
        """

        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideRepeatDocs


class TestInitWithParam:
    """
    Doc string sample class where the init method has parameters
    """

    def __init__(self, a, b=0, c=None):
        """
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param a: a parameter
        :type a: ``object``
        """
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam
