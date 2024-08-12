#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Python Test Harness
# ----------------------------------------------------------------------------
""" @package autotests.newfeatures.generator

@brief Auto Test of asynchronous generators

@author christophe.roquebert

@date   2018/11/02
"""
# ----------------------------------------------------------------------------
# imports
# ----------------------------------------------------------------------------
from pyharness.core             import TestCase
from datetime                   import datetime
import asyncio 

# ----------------------------------------------------------------------------
# implementation
# ----------------------------------------------------------------------------


class TestGeneratorsMethods(TestCase):
    """ PEP 492 introduced support for native coroutines 
        and async / await syntax to Python 3.5.. """
    
    @staticmethod
    async def ticker(delay, to):
        """Yield numbers from 0 to *to* every *delay* seconds."""
        for i in range(to):
            yield i
            await asyncio.sleep(delay)
    
    @staticmethod        
    async def execute():
        async for i in TestGeneratorsMethods.ticker(1, 3):
            #print(i)
            pass
    
    # PEP 492 introduced support for native coroutines 
    # and async / await syntax to Python 3.5
    def test_asynchronousGenerators(self):
        """ A notable limitation of the Python 3.5 implementation is that 
            it was not possible to use await and yield in the same function body. 
            In Python 3.6 this restriction has been lifted, making it possible 
            to define asynchronous generators. """
        t1 = datetime.now()
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self.execute())
        finally:
            loop.close()
        t2 = datetime.now()
        result = t2 -t1
        self.assertEqual(3, result.seconds)
    # end def test_asynchronousGenerators
    
# end class TestGeneratorsMethods  
         
# ----------------------------------------------------------------------------
# END OF FILE
# ----------------------------------------------------------------------------
