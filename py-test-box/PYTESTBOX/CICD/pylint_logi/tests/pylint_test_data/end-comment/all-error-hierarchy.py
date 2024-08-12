# -*- coding: utf-8 -*-

class TestClass1:
    class TestClass2(object):
        def test_func(self):
            if True:
                for i in range(3):
                    pass
                # end if
            else:
                while True:
                    pass
                # end if
            # end while
        # end class TestClass2
    # end def test_func

    async def test_async_func(self):
        with open(".."):
            pass
        # end def test_async_func
    # end with

    @property
    def test_property(self):
        return
    # end with

    @test_property.setter
    def test_property(self, value):
        match value:
            case "a":
                pass
            case "b":
                pass
        # end if
    # end with
# end def test_func
