"""
:package: method_no_brief
:brief: sample file where methods lack a brief
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""
from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:
    """
    Doc string sample test class
    """

    def __init__(self):
        pass
    # end def __init__

    def method(self):
        """

        """
        raise NotImplementedAbstractMethodError()
    # end def method

    def param_method(self, a, b=1, c=None):
        """
        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def param_method

    def return_method(self):
        """

        :return: a value
        :rtype: ``int``
        """
        raise NotImplementedAbstractMethodError()
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        """

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def return_param_method
# end class TestClassBase


class TestOverrideRepeatDocs(TestClassBase):
    """
    Doc string sample test class repeating the docstring
    """

    def __init__(self):
        super().__init__()
    # end def __init__

    def method(self):
        """
        """
        pass

    # end def method

    def param_method(self, a, b=1, c=None):
        """

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        """
        pass

    # end def param_method

    def return_method(self):
        """

        :return: a value
        :rtype: ``int``
        """

        return id(self)

    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        """

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``

        :return: a value
        :rtype: ``int``
        """

        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideRepeatDocs
