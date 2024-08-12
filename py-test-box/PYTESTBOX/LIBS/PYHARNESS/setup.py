#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package setup

@brief  PyHarness setup file

@author christophe.roquebert

@date   2018/06/13
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
# This is where the version is defined.
# This is used both by setup and PySetup's Config
VERSION = '1.1.2.0'

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
                key = '__'
                key += 'file'
                key += '__'
                thisPath = normpath(abspath(globals().get(key, None)))
                devPath  = thisPath[:thisPath.index(normpath('/PYTESTBOX/')) + 4]
                newPath  = join(devPath, *pathRelativeToRoot)

                import sys                                                                                              # pylint:disable=W0404,W0621
                sys.path.insert(0, newPath)

                # Fix PySetup to use the path as part of its original pythonpath

            except ImportError:
                pass
            # end try
        # end try
    # end def hackPath

    # HACK: Fix sys.path to give access to pysetup
    hackPath('pysetup', ('LIBS', 'PYSETUP', 'PYTHON'))

    # HACK: Fix sys.path to give access to pylibrary
    hackPath('pylibrary', ('LIBS', 'PYLIBRARY'))

    # HACK: Fix sys.path to give access to pylibrary
    hackPath('pyharness', ('LIBS', 'PYHARNESS'))

    import sys
    print(('System path: \n  %s' % ('\n  '.join(sys.path))))

    setup(# This line left intentionally blank
      name             = 'pyHarness',
      version          = VERSION,
      packages         = find_packages(),
      package_dir      = {'pyharness': 'pyharness',
                        },
      py_modules       = ['setup',],
      author           = 'Christophe Roquebert',
      author_email     = 'croquebert@logitech.com',
      maintainer       = 'Christophe Roquebert',
      maintainer_email = 'croquebert@logitech.com',
      description      = '\n'.join(('pyHarness is a generic testing framework written in Python',
                             '  It is able to address various targets, such as usb boards, devices...')),
      license = '\n'.join(('Python Validation Framework',
                           '  PyHarness package.',
                           '  ',
                           )),
      keywords = 'test',
      package_data = {'pyharness.ui.aui.media': ['*.png'],
                      },
      data_files = [('doc/chm',  [x for x in findall('doc/chm')
                                    if x.endswith('.chm')]),
                    ],
      requires = ['PyLibrary (>= 0.24)'],
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
      test_suite = 'pyharness.testrunner.PyHarnessTestRunner',
      )
# end if

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
