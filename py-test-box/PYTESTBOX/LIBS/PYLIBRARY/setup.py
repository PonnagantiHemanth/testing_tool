#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package setup

@brief  pylibrary setup file

@author christophe.roquebert

@date   2018/06/09
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------

# This is where the version is defined.
# This is used both by setup and PySetup's Config
VERSION = '1.3.1.0'

if (__name__ == '__main__'):
    from setuptools                     import setup
    from setuptools                     import find_packages
    from setuptools                     import findall

    def hackPath(targetImport, pathRelativeToRoot):
        '''
        Hacks sys.path to give access to the target import

        @param  targetImport       [in] (str)   The import to attempt.
        @param  pathRelativeToRoot [in] (tuple) Path elements
        '''
        try:
            __import__(targetImport)
        except ImportError:
            try:
                from os.path            import abspath
                from os.path            import normpath
                from os.path            import join
                key  = '__'
                key += 'file'
                key += '__'
                thisPath = normpath(abspath(globals().get(key, None)))
                devPath  = thisPath[:thisPath.index(normpath('/PYTESTBOX/')) + 4]
                newPath  = join(devPath, *pathRelativeToRoot)
                import sys
                sys.path.insert(0, newPath)
            except ImportError:
                pass
            # end try
        # end try
    # end def hackPath

    # HACK: Fix sys.path to give access to pysetup
    hackPath('pysetup', ('LIBS', 'PYSETUP', 'PYTHON'))

    # HACK: Fix sys.path to give access to pylibrary
    hackPath('pylibrary', ('LIBS', 'PYLIBRARY'))

    setup(# This line left intentionally blank
      name             = 'PyLibrary',
      version          = VERSION,
      packages         = find_packages(),
      package_dir      = {'pylibrary': 'pylibrary'
                         },
      py_modules       = ['setup',],
      author           = 'christophe Roquebert',
      author_email     = 'croquebert@logitech.com',
      maintainer       = 'christophe Roquebert',
      maintainer_email = 'croquebert@logitech.com',
      description      = '\n'.join(('PyLibrary is a collection of python utilities',
                                    'for test, lib and tools development')),
      license = '\n'.join(('Python Utility Library',
                           '  PyLibrary package.',
                           '  ',
                           )),
      keywords = 'device tools threads',
      data_files = [('doc/chm',  [x for x in findall('doc/chm')
                                    if x.endswith('.chm')]),
                    ],
      classifiers = ['Environment :: Console',
                     'Environment :: Gui',
                     'Intended Audience :: Developers',
                     'Operating System :: Microsoft :: Windows',
                     'Operating System :: Linux :: Ubuntu',
                     'Operating System :: Linux :: Scientific Linux',
                     'Operating System :: Apple :: Darwin',
                     'Programming Language :: Python',
                     'Topic :: Software Development :: Testing',
                     ],
      url = 'http://www.hotmail.com',
      test_suite = 'pylibrary.testrunner.PyLibraryTestRunner', install_requires=['pywin32', 'libusb1', 'bitstring',
                                                                                 'pylink-square', 'hidapi', 'intelhex',
                                                                                 'pyelftools', 'pysetup',
                                                                                 'pycryptodome', 'pyserial']
    )
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
