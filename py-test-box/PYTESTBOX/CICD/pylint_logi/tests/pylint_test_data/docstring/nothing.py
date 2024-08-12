from PYTESTBOX.LIBS.PYLIBRARY.pylibrary.tools.util import NotImplementedAbstractMethodError


class TestClassBase:

    def __init__(self):
        pass
    # end def __init__

    def method(self):
        raise NotImplementedAbstractMethodError()
    # end def method

    def param_method(self, a, b=1, c=None):
        raise NotImplementedAbstractMethodError()
    # end def param_method

    def return_method(self):
        raise NotImplementedAbstractMethodError()
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        raise NotImplementedAbstractMethodError()
    # end def return_param_method
# end class TestClassBase


class TestOverride(TestClassBase):

    def __init__(self):
        super().__init__()
    # end def __init__

    def method(self):
        pass
    # end def method

    def param_method(self, a, b=1, c=None):
        pass
    # end def param_method

    def return_method(self):
        return id(self)
    # end def return_method

    def return_param_method(self, a, b=1, c=None):
        temp = c if c else 0

        return id(self) + id(a) + b + temp
    # end def return_param_method
# end class TestOverride

class TestInitWithParam:
    def __init__(self, a, b=0, c=None):
        self.a = a
        self.b = b
        self.c = c
    # end def __init__
# end class TestInitWithParam
