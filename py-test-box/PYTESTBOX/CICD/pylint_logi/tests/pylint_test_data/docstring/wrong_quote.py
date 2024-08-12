'''
:package: wrong_quote
:brief: sample file without errors
:author: Sylvana Ieri <sieri@logitech.com>
:date: 2024/05/08
'''
from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:
    '''
    Doc string sample test class
    '''

    def __init__(self):
        pass
    # end def __init__

    def method(self):
        '''
        Method to override
        '''
        raise NotImplementedAbstractMethodError()
    # end def method

    def param_method(self, a, b=1, c=None):
        '''
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        '''
        raise NotImplementedAbstractMethodError()
    # end def param_method

    def return_method(self):
        '''
        Method with return

        :return: a value
        :rtype: ``int``
        '''

        raise NotImplementedAbstractMethodError()
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        '''
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        '''
        raise NotImplementedAbstractMethodError()
    # end def return_param_method
# end class TestClassBase


class TestOverrideRepeatDocs(TestClassBase):
    '''
    Doc string sample test class repeating the docstring
    '''

    def __init__(self):
        super().__init__()
    # end def __init__

    def method(self):
        '''
        Method to override
        '''
        pass

    # end def method

    def param_method(self, a, b=1, c=None):
        '''
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``
        '''
        pass

    # end def param_method

    def return_method(self):
        '''
        Method with return

        :return: a value
        :rtype: ``int``
        '''

        return id(self)

    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        '''
        Method with parameters

        :param a: a parameter
        :type a: ``object``
        :param b: another parameter - OPTIONAL
        :type b: ``int``
        :param c: last parameter - OPTIONAL
        :type c: ``int`` or ``None``

        :return: a value
        :rtype: ``int``
        '''

        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverrideRepeatDocs


class TestInitWithParam:
    '''
    Doc string sample class where the init method has parameters
    '''

    def __init__(self, a, b=0, c=None):
        '''
        :param a: first parameter
        :type a: ``object``
        :param b: second parameter - OPTIONAL
        :type b: ``int``
        :param c: third parameter - OPTIONAL
        :type c: ``int``
        '''
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam
