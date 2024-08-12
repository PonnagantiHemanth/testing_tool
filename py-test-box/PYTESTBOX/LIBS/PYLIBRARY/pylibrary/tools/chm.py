#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.chm

@brief  Compressed HTML (.chm) and Html Help (.hhp, .hhc, .hhk) utils

@author christophe roquebert

@date   2018/06/06
'''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from os.path                            import basename
from os.path                            import dirname
from os.path                            import join
from subprocess                         import Popen
from xml.dom.minidom                    import getDOMImplementation

import re

try:
    from pysetup                        import HHC                                                                      # pylint:disable=E0611
except ImportError:
    from os.path                        import isfile
    HHC = 'C:\\Program Files\\HTML Help Workshop\\hhc.exe'
    if (not isfile(HHC)):
        HHC = 'C:\\Program Files (x86)\\HTML Help Workshop\\hhc.exe'
    # end if
# end try

# ------------------------------------------------------------------------------
# Implementation
# ------------------------------------------------------------------------------
class ChmError(Exception):
    '''
    Exception handle for CHM
    '''
    def __init__(self, msg):
        ''' Constructor

        @param  msg [in] (str) Exception message
        '''
        super(ChmError, self).__init__(msg)
    # end def __init__
# end class ChmError


class AbstractHtmlHelp(object):
    '''
    Abstract Html Help File
    '''

    def __init__(self, filename = 'index.ext'):
        '''
        Constructor

        @option filename [in] (str) ext in hhp, hhc, hhk
        '''
        self._filename = filename
        self._data     = None
    # end def __init__

    @classmethod
    def fromFile(cls, filename):
        '''
        Read Html Help file

        @param  filename [in] (str) input file

        @return (HtmlHelp)
        '''
        try:
            with open(filename, 'r') as fo:
                lines = fo.readlines()
            # end with
        except IOError as ex:
            raise ChmError('%s: %s' % (ex.strerror, ex.filename))
        # end try

        htmlHelp = cls(filename)
        htmlHelp._parse(lines)                                                                                          # pylint:disable=W0212

        return htmlHelp
    # end def fromFile

    def _parse(self, lines):
        '''
        Convert text content into Html Help data

        @param lines [in] (list) of strings
        '''
        raise NotImplementedError()
    # end def _parse

    def toFile(self):
        '''
        Write Html Help file
        '''
        try:
            with open(self._filename, 'w') as fo:
                fo.write(self.__str__())
            # end with
        except IOError as ex:
            raise ChmError('%s: %s' % (ex.strerror, ex.filename))
        # end try
    # end def toFile

    def __str__(self):
        '''
        Convert Html Help data into text

        @return (str)
        '''
        raise NotImplementedError()
    # end def __str__

# end class AbstractHtmlHelp

class HtmlHelpXml(AbstractHtmlHelp):
    '''
    Html Help Xml File

    This class allows to handle html-<i>like</i> files data with
    the <b>D</b>ocument <b>O</b>bject <b>M</b>odel interface.

    @t_start_b0
    @t_rh     hhc/hhk format
    @t_hh     DOM view
    @t_hh_w30 GUI view
    @t_hr

    @t_rd
    @verbatim
    <UL>
      <LI><OBJECT type="text/sitemap">
        <param name="Name" value="Heading">
      </OBJECT>
      <UL>
        <LI><OBJECT type="text/sitemap">
          <param name="Name" value="Page">
          <param name="Local" value="page.html">
        </OBJECT>
      </UL>
    </UL>
    @endverbatim
    @t_dd
    @verbatim
    <Heading>
      <Page Local="page.html"/>
    </Heading>
    @endverbatim
    @t_dd
    @verbatim
    Heading
      Page
    @endverbatim
    @t_dr
    @t_end

    === Usage ===

    @code
    # Create the document
    hhx = HtmlHelpXml()

    # Append the 'Heading' page
    heading = hhx.appendChild(hhx.createPage('Heading'))

    # Append the heading page, parent of next pages
    heading.appendChild(hhx.createPage('Page', 'page.html'))

    # Save the document
    hhx.toFile()
    @endcode
    '''

    def __init__(self, filename = 'index'):
        '''
        Constructor

        @option filename [in] (str) ext in hhc, hhk
        '''
        super(HtmlHelpXml, self).__init__(filename)

        self._doc  = getDOMImplementation().createDocument(None, None, None)
        self._data = self._doc.appendChild(self._doc.createElement('pages'))
    # end def __init__

    pages = property(lambda self: self._data)                                                                           # pylint:disable=W0212

    _RE_TAG   = re.compile(r'<(/?\w+)(.*?)>')
    _RE_ATTR  = re.compile(r'(\w+)="(.+?)"')

    def _parse(self, lines):
        '''
        @copydoc pylibrary.tools.chm.AbstractHtmlHelp._parse
        '''
        node = None

        for line in lines:
            for tag, attributes  in self._RE_TAG.findall(line):

                if (tag == 'UL'):
                    node = self._data if node is None else node.lastChild
                    continue
                # end if

                if node is None:
                    continue
                # end if

                if (tag == 'OBJECT'):
                    params = dict()
                    continue
                # end if

                if (tag == 'param'):
                    for left, right in self._RE_ATTR.findall(attributes):
                        if (left == 'name'):
                            name = right
                            continue
                        # end if

                        if (left == 'value'):
                            value = right
                            continue
                        # end if
                    # end for
                    params[name] = value
                    continue
                # end if

                if (tag == '/OBJECT'):
                    page = self.createPage(params['Name'],
                                           local = params.get('Local', None),
                                           image = params.get('ImageNumber', None))
                    node.appendChild(page)
                    continue
                # end if

                if (tag  == '/UL'):
                    node = node.parentNode
                    continue
                # end if
            # end for
        # end for
    # end def _parse

    def createPage(self, name, local = None, image = None):
        '''
        Create an page node

        @param  name  [in] (str) page
        @option local [in] (str) html[:@#anchor]
        @option image [in] (int) number

        @return (Node) page
        '''
        page = self._doc.createElement(name)

        page.setAttribute('Local',       local)
        page.setAttribute('ImageNumber', str(image) if image is not None else None)

        return page
    # end def createPage

    def __str__(self):
        '''
        @copydoc pylibrary.tools.chm.AbstractHtmlHelp.__str__
        '''
        lines = list()

        def toString(node, depth = 2):
            '''
            Node to String

            @param  node  [in] (Node) to convert
            @option depth [in] (int)  indent

            @warning Recursive function
            '''
            lines.append('%s<LI><OBJECT type="text/sitemap"><param name="Name" value="%s">%s</OBJECT>'
                         % (' ' * depth,
                            node.tagName,
                            ''.join(['<param name="%s" value="%s">'
                                     % (name, value)
                                     for name, value in list(node.attributes.items())
                                     if value is not None])))

            if (node.hasChildNodes()):
                lines.append('%s<UL>' % (' ' * depth,))

                for child in node.childNodes:
                    toString(child, depth + 2)
                # end for

                lines.append('%s</UL>' % (' ' * depth,))
            # end if
        # end def toString

        for node in self._data.childNodes:
            toString(node)
        # end for

        return '''\
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">
<HTML>
<HEAD>
</HEAD><BODY>
<OBJECT type="text/site properties"><param name="FrameName" value="right"></OBJECT>
<UL>
%s
</UL>
</BODY></HTML>
''' % ('\n'.join(lines),)
    # end def __str__

# end class HtmlHelpXml

class HtmlHelpContents(HtmlHelpXml):
    '''
    Html Help Contents file utils

    This class allows to build/update the CHM  <b>T</b>able <b>O</b>f <b>C</b>ontents
    using the DOM interface.

    === Use Case ===

    @t_start_b0

    @t_rh_w20 Input files
    @t_hh_w20 TOC view
    @t_hh     DOM view
    @t_hr
    @t_rd
    @verbatim
    index.html
    heading.html
    overview.html
    details.html
    faq.html
    @endverbatim
    @t_dd
    @verbatim
    ¤ Main
    + Heading
      ¤ Overview
      + Details
        i Item #1
        i Item #2
    ? FAQ
    @endverbatim
    @t_dd
    @verbatim
    <Main  local="index.html"  image="11"/>
    <Heading  local="heading.html"  image="5">
      <Overview  local="overview.html"  image="11"/>
      <Details  local="details.html"  image="5">
        <Item #1  local="details.html#item_1"  image="17"/>
        <Item #2  local="details.html#item_2"  image="17"/>
      </Details>
    </Heading>
    <FAQ  local="faq.html"  image="9"/>
    @endverbatim
    @t_dr
    @t_end

    === Usage ===

    @code
    # Create the document
    hhc = HtmlHelpContents()

    # Select root level
    root = hhc.pages

    # Append pages at root level
    root.appendChild(hhc.createPage('Main', 'index.html', hhc.IN_FILE_TEXT))

    heading = root.appendChild(hhc.createPage('Heading', 'heading.html', hhc.IN_FOLDER))

    # Append pages at Heading level
    heading.appendChild(hhc.createPage('Overview', 'overview.html', hhc.IN_FILE_TEXT))

    details = heading.appendChild(hhc.createPage('Details', 'details.html', hhc.IN_FOLDER))

    # Append pages at Details level
    details.appendChild(hhc.createPage('Item #1', 'details.html#item_1', hhc.IN_FILE_INFO))
    details.appendChild(hhc.createPage('Item #2', 'details.html#item_2', hhc.IN_FILE_INFO))

    # Append the last page at root level
    root.appendChild(hhc.createPage('FAQ', 'faq.html', hhc.IN_FILE_QUERY))

    # Save document
    hhc.toFile()
    @endcode
    '''

    ##@name ImageNumber
    ##@{
    IN_AUTO               = None

    IN_BOOK               = 1
    IN_BOOK_OPEN          = 2
    IN_BOOK_STAR          = 3
    IN_BOOK_STAR_OPEN     = 4

    IN_FOLDER             = 5
    IN_FOLDER_OPEN        = 6
    IN_FOLDER_STAR        = 7
    IN_FOLDER_STAR_OPEN   = 8

    IN_FILE_QUERY         = 9
    IN_FILE_QUERY_STAR    = 10
    IN_FILE_TEXT          = 11
    IN_FILE_TEXT_STAR     = 12

    IN_FILE_INFO          = 17
    IN_FILE_INFO_STAR     = 18
    IN_FILE_SHORTCUT      = 19
    IN_FILE_SHORTCUT_STAR = 20
    IN_FILE_BOOK          = 21
    IN_FILE_BOOK_STAR     = 22
    IN_MAIL               = 23
    IN_MAIL_STAR          = 24
    IN_FILE_MAIL          = 25
    IN_FILE_MAIL_STAR     = 26
    IN_FILE_PERSON        = 27
    IN_FILE_PERSON_STAR   = 28
    IN_FILE_SOUND         = 29
    IN_FILE_SOUND_STAR    = 30
    IN_FILE_DISK          = 31
    IN_FILE_DISK_STAR     = 32
    IN_FILE_CAMERA        = 33
    IN_FILE_CAMERA_STAR   = 34
    IN_FILE_LIST          = 35
    IN_FILE_LIST_STAR     = 36
    IN_FILE_HELP          = 37
    IN_FILE_HELP_STAR     = 38
    IN_FILE_WRITE         = 39
    IN_FILE_WRITE_STAR    = 40
    IN_FILE_CONFIG        = 41
    IN_FILE_CONFIG_STAR   = 42
    ##@}

    def __init__(self, filename = 'index.hhc'):
        '''
        Constructor

        @option filename [in] (str) Table of Contents file
        '''
        super(HtmlHelpContents, self).__init__(filename)
    # end def __init__

# end class HtmlHelpContents

class HtmlHelpIndex(HtmlHelpXml):
    '''
    Html Help Index File
    '''

    def __init__(self, filename = 'index.hhk'):
        '''
        Constructor

        @option filename [in] (str) Index file
        '''
        super(HtmlHelpIndex, self).__init__(filename)
    # end def __init__

# end class HtmlHelpIndex

class HtmlHelpProject(AbstractHtmlHelp):
    '''
    Html Help Project File
    '''

    # Windows Types
    _WIN_TITLE_BAR   = 0  # General - Title Bar Text
    _WIN_TOC         = 1  # File - TOC
    _WIN_INDEX       = 2  # File - Index
    _WIN_DEFAULT     = 3  # File - Default
    _WIN_HOME        = 4  # File - Home
    _WIN_JUMP_1      = 5  # File - Jump 1
    _WIN_JUMP_2      = 6  # File - Jump 2
    _WIN_7           = 7  # ?
    _WIN_8           = 8  # ?
    _WIN_9           = 9  # ?
    _WIN_10          = 10 # ?
    _WIN_BUTTONS     = 11 # Buttons - Button Types
    _WIN_POSITION    = 12 # Position
    _WIN_STYLES      = 13 # Styles - Properties
    _WIN_EXT_STYLES  = 14 # Extended Styles - Properties
    _WIN_15          = 15 # ?
    _WIN_16          = 16 # ?
    _WIN_DEFAULT_TAB = 17 # Navigation Pane - Tabs - Default tab
    _WIN_18          = 18 # ?
    _WIN_19          = 19 # ?

    def __init__(self, filename = 'index.hhp', contents = False, index = False):
        '''
        Constructor

        @option filename [in] (str)  Project file
        @option contents [in] (bool) Include Contents file
        @option index    [in] (bool) Include Index file
        '''
        super(HtmlHelpProject, self).__init__(filename)

        project = basename(filename).rsplit('.', 1)[0]

        self._data = {'OPTIONS'   : {'Compatibility'            : '1.1 or later',
                                     'Compiled file'            : '%s.chm' % (project,),
                                     'Contents file'            : '%s.hhc' % (project,) if contents else None,
                                     'Index file'               : '%s.hhk' % (project,) if index    else None,

                                     'Full-text search'         : None,
                                     'Default Window'           : 'main',
                                     'Default topic'            : 'index.html',

                                     'Display compile notes'    : 'Yes',
                                     'Display compile progress' : 'No',
                                     'Error log file'           : None,

                                     'Language'                 : '0x409 English (United States)',
                                     'Title'                    : 'HTML Help',
                                     },
                      'INFOTYPES' : {},
                      'WINDOWS'   : {'main' : ['HTML Help',
                                               '%s.hhc' % (project,) if contents else None,
                                               '%s.hhk' % (project,) if index    else None,
                                               'index.html',
                                               'index.html',
                                               None, None, None, None,
                                               0x23520,
                                               None,
                                               0x10387e,
                                               None, None, None, None, None, None, None,
                                               0],
                                     },
                      'FILES'     : {},
                      }

        self._hhc = HtmlHelpContents()
        self._hhk = HtmlHelpIndex()
    # end def __init__

    # pylint:disable=W0212
    compileFile     = property(lambda self : self._getOption('Compiled file'),
                               lambda self, value: self._setOption('Compiled file', value))

    contentsFile    = property(lambda self : self._getOption('Contents file'))

    indexFile       = property(lambda self : self._getOption('Index file'))

    displayNotes    = property(lambda self : self._getOption('Display compile notes'),
                               lambda self, value: self._setOption('Display compile notes', value))

    displayProgress = property(lambda self : self._getOption('Display compile progress'),
                               lambda self, value: self._setOption('Display compile progress', value))

    errorLogFile    = property(lambda self : self._getOption('Error log file'),
                               lambda self, value: self._setOption('Error log file', value))

    language        = property(lambda self : self._getOption('Language'),
                               lambda self, value: self._setOption('Language', value))

    title           = property(lambda self : self._getOption('Title'),
                               lambda self, value: self._setOption('Title', value))
    # pylint:enable=W0212


    # pylint:disable=W0212
    hhc = property(lambda self: self._hhc)
    hhk = property(lambda self: self._hhk)
    # pylint:enable=W0212

    def _getOption(self, key):
        '''
        Getter

        @param key [in] (str) option

        @return (str, bool) title
        '''
        value = self._data['OPTIONS'][key]
        return None  if value is None  \
          else True  if value == 'Yes' \
          else False if value == 'No'  \
          else value
    # end def _getOption

    def _setOption(self, key, value):
        '''
        Setter

        @param key   [in] (str)       option
        @param value [in] (str, bool) value
        '''
        self._data['OPTIONS'][key] = 'Yes' if str(value) == True  \
                                else 'No'  if str(value) == False \
                                else value

        if (key == 'Title'):
            self._data['WINDOWS'][self._data['OPTIONS']['Default Window']][self._WIN_TITLE_BAR] = value
        # end if

    # end def _setOption


    _RE_SECTION = re.compile(r'\[([A-Z]+)\]')
    _RE_OPTION  = re.compile(r'([^=]+)=?(.+)?')

    def _parse(self, lines):
        '''
        @copydoc pylibrary.tools.chm.AbstractHtmlHelp._parse
        '''
        for line in lines:

            mo = self._RE_SECTION.match(line)
            if (mo is not None):
                section = mo.group(1)

                if (section not in self._data):
                    self._data[section] = dict()
                # end if

                continue
            # end if

            mo = self._RE_OPTION.match(line)
            if (mo is not None):
                key   = mo.group(1).strip()
                value = str(mo.group(2)).strip() if mo.group(2) is not None else ''

                if (key != ''):
                    self._data[section][key] = value
                # end if

                continue
            # end if
        # end for

        for key, value in self._data['WINDOWS'].items():
            self._data['WINDOWS'][key] = self._splitWindow(value)
        # end for

        if (self.contentsFile is not None):
            self._hhc = HtmlHelpContents.fromFile(join(dirname(self._filename),
                                                       self.contentsFile))
        # end if

        if (self.indexFile is not None):
            self._hhk = HtmlHelpIndex.fromFile(join(dirname(self._filename),
                                                    self.indexFile))
        # end if
    # end def _parse

    @staticmethod
    def _splitWindow(csv):
        '''
        Split WINDOWS data

        @param csv [in] (str) '"file", ... '

        @return (list)
        '''
        data = list()

        sep  = ','
        item = ''

        for char in csv + sep:
            if (char == sep):

                data.append(str(item[1:-1]) if item.startswith('"') else
                            int(item[2:], 16) if item.startswith('0x') else
                            item[1:-1].split(',') if item.startswith('[') else
                            int(item) if item != '' else None)

                item = ''
                continue
            else:
                item += char
            # end if

            if (char in ('["]')):
                sep = ',' if sep is None else None
            # end if
        # end for
        return data
    # end def _splitWindow

    @staticmethod
    def _joinWindow(data):
        '''
        Join WINDOWS data

        @param data [in] (list) ['file', ... ]

        @return (str)
        '''
        return ','.join(['"%s"' % (item,) if isinstance(item, str) else
                         '%d'   % (item,) if isinstance(item, int) else
                         '[%s]' % (','.join(['%d' % (i,) for i in item]),) if isinstance(item, list) else
                         ''
                         for item in data])
    # end def _joinWindow

    def toFile(self):
        '''
        @copydoc pylibrary.tools.chm.AbstractHtmlHelp.toFile
        '''
        super(HtmlHelpProject, self).toFile()

        if (self.contentsFile is not None):
            self.hhc.toFile()
        # end if

        if (self.indexFile is not None):
            self.hhk.toFile()
        # end if

    # end def toFile

    def __str__(self):
        '''
        @copydoc pylibrary.tools.chm.AbstractHtmlHelp.__str__
        '''
        return '\n'.join(['[%s]\n%s\n'
                          % (section,
                             '\n'.join(['%s%s%s' % (key,
                                                    ' = ' if value != '' else '',
                                                    self._joinWindow(value) if section == 'WINDOWS' else value)
                                        for key, value in self._data[section].items()
                                        if value is not None]))
                          for section in ('OPTIONS', 'INFOTYPES', 'WINDOWS', 'FILES')])
    # end def __str__


    def run(self):
        '''
        Compile HTML file

        @return (int) status
        '''
        self.toFile()

        return Popen(['hhc', self._filename], executable = HHC).wait()                                                  # pylint: disable=E1101
    # end def run

# end class HtmlHelpProject

# ------------------------------------------------------------------------------
#  END OF FILE
# ------------------------------------------------------------------------------
