"""
:package: no_error
:brief: sample file without errors
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

    def __repr__(self):
        return 'TestClassBase'
    # end def __repr__

    def method(self):
        """
        Method to override
        """
        raise NotImplementedAbstractMethodError()
    # end def method

    def param_method(self, a, b=1, c=None):
        """
        Method with parameters

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
        Method with return

        :return: a value
        :rtype: ``int``
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

    def __init__(self):
        super().__init__()
    # end def __init__

    def method(self):
        """
        Method to override
        """
        pass
    # end def method

    def param_method(self, a, b=1, c=None):
        """
        Method with parameters

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
        Method with return

        :return: a value
        :rtype: ``int``
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

        :return: a value
        :rtype: ``int``
        """
        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideRepeatDocs


class TestOverrideReferenceDocs(TestClassBase):
    # See ``TestClassBase``

    def __init__(self):
        super().__init__()
    # end def __init__

    def method(self):
        # See ``TestClassBase.method``

        pass
    # end def method

    def param_method(self, a, b=1, c=None):
        # See ``TestClassBase.param_method``

        pass
    # end def param_method

    def return_method(self):
        # See ``TestClassBase.return_method``

        return id(self)
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        # See ``TestClassBase.return_param_method``
        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideReferenceDocs

class TestInitWithParam:
    """
    Doc string sample class where the init method has parameters
    """

    def __init__(self, a, b=0, c=None):
        """
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
    This is a brief with a note, no special processing should happen

    Note: see confluence: https://spaces.logitech.com/display/ptb/Python+docstring+format+and+best+practices

    :param sample: sample parameter
    :type sample: ``object``
    """
    pass
# end def note_with_link_to_ignore

def return_as_flow_control_only(on):
    """
    method where the return does not have a value and is purely for flow control

    :param on: an example parameter
    :type on: ``bool``
    """
    if on:
        return
    # end if
    pass
# end def return_as_flow_control_only


def type_hint_complex(list_parameter, tuple_parameter):
    """
    function where with harder to parse type hint

    :param list_parameter: list of a single type
    :type list_parameter: ``list[str]``
    :param tuple_parameter: tuple of a few set of parameters with an option
    :type tuple_parameter: ``tuple[str, int|float]``
    """
    pass
# end def type_hint_complex

def raise_function(on):
    """
    function that raises an exception

    :param on: an example parameter
    :type on: ``bool``

    :raise ``ValueError``: if on is True
    """
    if on:
        raise ValueError('on is True')
    # end if
    pass
# end def raise_function

def args_kwargs_function(a, *args, **kwargs):
    """
    function that takes in args and kwargs

    :param a: a parameter
    :type a: ``int``
    :param args: optional positional arguments
    :type args: ``tuple``
    :param kwargs: optional keyword arguments
    :type kwargs: ``dict`` or ``None``

    :kwargs:
        * **random_param** (``float``): Third random parameter - OPTIONAL
    """
    pass
# end def args_kwargs_function

def yield_as_flow_control_only(on):
    """
    function that yields but does not return a value, is as used by contextmanager

    :param on: an example parameter
    :type on: ``bool``
    """
    if on:
        yield
    # end if
    pass
# end def yield_as_flow_control_only
