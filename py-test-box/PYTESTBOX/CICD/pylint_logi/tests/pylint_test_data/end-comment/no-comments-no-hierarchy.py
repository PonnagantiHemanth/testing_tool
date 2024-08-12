# -*- coding: utf-8 -*-

class TestClass1:
    pass

fail_here = 1


class TestClass2(TestClass1):
    pass

fail_here = 1

def test_func():
    pass

fail_here = 1

async def test_async_func():
    pass

fail_here = 1

if True:
    pass

fail_here = 1

for i in range(3):
    pass

fail_here = 1

while True:
    pass

fail_here = 1

with open(".."):
    pass

fail_here = 1
