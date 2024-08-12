"""
:package: method_missing_return_briefs
:brief: sample file with missing returns description and type hints
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
"""
from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:
    """
    Doc string sample test class
    """

    def return_method(self):
        """
        Method with return

        :return:
        :rtype:
        """
        raise NotImplementedAbstractMethodError()
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``

        :return:
        :rtype:
        """
        raise NotImplementedAbstractMethodError()
    # end def return_param_method
# end class TestClassBase


class TestOverrideRepeatDocs(TestClassBase):
    """
    Doc string sample test class repeating the docstring
    """

    def return_method(self):
        """
        Method with return

        :return:
        :rtype:
        """
        return id(self)
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``

        :return:
        :rtype:
        """
        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideRepeatDocs
