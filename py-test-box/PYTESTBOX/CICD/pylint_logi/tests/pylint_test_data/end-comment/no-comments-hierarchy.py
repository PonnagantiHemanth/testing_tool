# -*- coding: utf-8 -*-

class TestClass1:
    class TestClass2(object):
        def test_func(self):
            if True:
                for i in range(3):
                    pass
            else:
                while True:
                    pass

    async def test_async_func(self):
        with open(".."):
            pass

    @property
    def test_property(self):
        return

    @test_property.setter
    def test_property(self, value):
        match value:
            case "a":
                pass
            case "b":
                pass
