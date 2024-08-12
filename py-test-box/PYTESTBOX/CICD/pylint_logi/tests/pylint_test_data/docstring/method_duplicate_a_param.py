"""
:package: method_duplicate_a_param
:brief: sample file without errors
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

        :param a: a parameter
        :type a: ``object``
        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        """
        raise NotImplementedAbstractMethodError()
    # end def param_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``

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

        :param a: a parameter
        :type a: ``object``
        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        """
        pass

    # end def param_method

    def return_param_method(self, a, b=1, c=None):
        """
        Method with parameters

        :param a: a parameter
        :type a: ``object``
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

class TestInitWithParam:
    """
    Doc string sample class where the init method has parameters
    """

    def __init__(self, a, b=0, c=None):
        """
        :param a: first parameter
        :type a: ``object``
        :param a: first parameter
        :type a: ``object``
        :param b: second parameter - OPTIONAL
        :type b: ``int``
        :param c: third parameter - OPTIONAL
        :type c: ``int``
        """
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam

def note_with_link_to_ignore(sample):
    """
    this is a brief with a note, no special processing should happen

    Note: see confluence: https://spaces.logitech.com/display/ptb/Python+docstring+format+and+best+practices

    :param sample: sample parameter
    :type sample: ``object``
    :param sample: sample parameter
    :type sample: ``object``
    """
    pass
# end def note_with_link_to_ignore
