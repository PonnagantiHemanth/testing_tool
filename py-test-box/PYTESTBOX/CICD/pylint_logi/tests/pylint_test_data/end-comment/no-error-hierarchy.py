# -*- coding: utf-8 -*-

class TestClass1:
    class TestClass2(object):
        def test_func(self):
            if True:
                for i in range(3):
                    pass
                # end for
            else:
                while True:
                    pass
                # end while
            # end if
        # end def test_func
    # end class TestClass2

    async def test_async_func(self):
        with open(".."):
            pass
        # end with
    # end def test_async_func

    @property
    def test_property(self):
        return
    # end def property getter test_property

    @test_property.setter
    def test_property(self, value):
        match value:
            case "a":
                pass
            case "b":
                pass
        # end match
    # end def property setter test_property
# end class TestClass1
