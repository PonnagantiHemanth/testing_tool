#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------------
# Python Test Harness
# ------------------------------------------------------------------------------
''' @package pylibrary.tools.binaryfiles

@brief Binary files handling classes

@author christophe.roquebert

@date   2018/02/14
 '''
# ------------------------------------------------------------------------------
# imports
# ------------------------------------------------------------------------------
from pylibrary.tools.hexlist            import HexList
from os                                 import R_OK
from os                                 import access
from os.path                            import abspath
from sys                                import maxsize as MAX_INT

# ------------------------------------------------------------------------------
# implementation
# ------------------------------------------------------------------------------
class BinaryFile(object):                                                                                               # pylint:disable=R0924
    '''
    Defines the interface for binary file handling classes.
    '''

    def __init__(self, filePath     = None,
                       defaultValue = 0,
                       overwrite    = True):
        '''
        Constructor.

        @option filePath     [in] (str)  Path to the file to load.
        @option defaultValue [in] (int)     The default value for non-loaded areas.
        @option overwrite    [in] (bool) Whether to overwrite existing values, or to
                                 throw an exception for duplicate definitions.
        '''
        self.defaultValue = defaultValue
        self._headers     = []

        # memoryBlocks contain a mapping: map<offset, HexList>
        # self.memoryBlocks = {}
        self.image = {}
        if (filePath is not None):
            self.load(filePath, overwrite)
        # end if
    # end def __init__

    def _readBlock(self, offset,
                         length):
        '''
        Reads a memory block starting at the given offset, for length bytes

        @param offset [in] (int) The offset at which to read the block
        @param length [in] (int) The length for which to read the block
        @return The block read at @c offset for @c length bytes
        '''
        result = []
        for newOffset in range(offset, offset+length):
            if (newOffset in self.image):
                result.append(self.image[newOffset])
            elif (self.defaultValue is not None):
                result.append(self.defaultValue)
            else:
                raise ValueError("Reading in an uninitialized area")
            # end if
        # end for
        return result
    # end def _readBlock

    def _readBlocks(self, offset,
                          length):
        '''
        Reads a sequence of memory block starting at the given offset, for length bytes
        Depending on the default value, empty spaces may be filled

        @param  offset [in] (int) The offset at which to read the block
        @param  length [in] (int) The length for which to read the block

        @return The sequence of blocks read at @c offset for @c length bytes
        '''
        if (    (offset is not None)
            and (length is not None)):
            if (self.defaultValue is None):
                existingBlocks = [(_offset, self._readBlock(_offset, _length))
                                    for _offset, _length
                                    # end for
                                    in self.getBlockOffsetsAndLengths()]
                newBlocks = []
                for blockOffset, blockValue in existingBlocks:
                    # compute the intersection of this block and
                    # the requested range
                    minOffset = max(blockOffset,
                                    min(blockOffset + len(blockValue),
                                        offset))
                    maxOffset = min(blockOffset + len(blockValue),
                                    max(blockOffset,
                                         offset+length))

                    # there is an intersection
                    if ((maxOffset - minOffset) > 0):
                        newBlocks.append((minOffset, blockValue[minOffset-blockOffset:maxOffset-blockOffset]))
                    # end if
                # end for
                existingBlocks = newBlocks
            else:
                existingBlocks = ((offset, self._readBlock(offset, length)),)
            # end if
        else:
            existingBlocks = [(offset, self._readBlock(offset, length)) for offset, length
                                                                        in self.getBlockOffsetsAndLengths()]
        # end if

        return existingBlocks
    # end def _readBlocks

    def getBlockOffsetsAndLengths(self):
        '''
        Obtains a list of pairs (offset, length) suitable for describing
        contiguous memory blocks.

        @return tuple(tuple(offset, length), ...)
        '''
        result = []
        lastStartOffset   = None
        lastCurrentOffset = None
        for offset in sorted(self.image.keys()):

            if (lastCurrentOffset != (offset-1)):

                # This is a block break: Save the previous block, except if it
                # is the first block fault
                if (lastStartOffset is not None):
                    result.append((lastStartOffset, (lastCurrentOffset + 1 - lastStartOffset)))
                # end if

                lastStartOffset = offset
            # end if
            lastCurrentOffset = offset
        # end for

        if (lastStartOffset is not None):
            result.append((lastStartOffset, (lastCurrentOffset + 1 - lastStartOffset)))
        # end if

        return result
    # end def getBlockOffsetsAndLengths

    def _writeBlock(self, offset,
                          data,
                          overwrite = True):
        '''
        Writes a memory block starting at the given offset, with data bytes.

        @param  offset    [in] (int)     The offset at which to update data
        @param  data      [in] (tuple)   The new data to update
        @option overwrite [in] (bool) Whether to overwrite existing values or to throw
                              an exception for duplicates.
        '''
        if (not overwrite):
            for newOffset in range(offset, offset+len(data)):
                if (newOffset in self.image):
                    raise ValueError("Overlap at address 0x%08.8X" % (newOffset))
                # end if
            # end for
        # end if
        for byteValue in data:
            if (overwrite):
                assert (byteValue & 0xFF) == byteValue, "Values must be inside [0x00 .. 0xFF]"
                self.image[offset] = byteValue
            # end if
            offset += 1
        # end for
    # end def _writeBlock


    def __getslice__(self, i,
                           j):
        '''
        Obtains part of the binary data

        @param  i [in] (int) The offset at which to start obtaining the item
        @param  j [in] (int) The offset at which to stop obtaining the item

        @return The block from i to j
        '''
        assert (i>=0) and (i<=j)

        return self._readBlock(i, j-i)
    # end def __getslice__

    def __setslice__(self, i,
                           j,
                           value):
        '''
        Sets part of the binary data

        @param  i     [in] (int)   The offset at which to start setting data
        @param  j     [in] (int)   The offset at which to stop setting data
        @param  value [in] (tuple) The value to set from i to j.
        '''
        assert len(value) == (j-i), \
            "Invalid length: obtained %d, expected %d" % (len(value), j-i,)
        self._writeBlock(i, value)
    # end def __setslice__

    def __delslice__(self, i,
                           j):
        '''
        Deletes part of the binary data

        @param  i [in] (int) The offset at which to start deleting data
        @param  j [in] (int) The offset at which to stop deleting data
        '''
        for offset in range(i, j):
            if (offset in self.image):
                del self.image[offset]
            # end if
        # end for
    # end def __delslice__

    def __delitem__(self, i):
        '''
        Deletes a single binary data

        @param  i [in] (int) The offset at which to delete data
        '''
        if (i in self.image):
            del self.image[i]
        # end if
    # end def __delitem__

    def __getitem__(self, i):
        '''
        Obtains one element in the binary data

        @param  i [in] (int) The offset at which to obtain the item

        @return The byte value
        '''
        if (i in self.image):
            return self.image[i]
        # end if

        return self.defaultValue
    # end def __getitem__

    def __setitem__(self, i, value):
        '''
        Sets one element in the binary data

        @param  i     [in] (int) The offset at which to set the value
        @param  value [in] (byte) The value to set
        '''
        assert (value & 0xFF) == value, "Values must be inside [0x00 .. 0xFF]"
        self.image[i] = value
    # end def __setitem__

    def __contains__(self, address):
        '''
        Tests whether an address is contained within the file.

        @param  address [in] (int) The address to test

        @return Whether the address is in the file.
        '''
        return address in self.image
    # end def __contains__

    def __cmp__(self, other):
        '''
        Tests the instances for equality

        @param  other [in] (BinaryFile) The other instance to test

        @return The equality comparison results
        '''
        assert isinstance(other, BinaryFile)

        offsets = list(set(self.image.keys()) | set(other.image.keys()))

        result = 0
        for offset in sorted(offsets):
            result = cmp(self[offset], other[offset])
            if (result != 0):
                return result
            # end if
        # end for

        return result
    # end def __cmp__

    def __str__(self):
        '''
        Converts the current instance to a readable string

        @return a readable string.
        '''
        result = ["%d bytes block starting at 0x%08.8X" % (length, offset)
                  for offset, length in self.getBlockOffsetsAndLengths()]

        return str(result)
    # end def __str__

    def load(self, filePath,
                   overwrite  = True,
                   minAddress = 0,
                   maxAddress = MAX_INT):
        '''
        Loads the file in memory.

        @param  filePath   [in] (str) The file to load.
        @option overwrite  [in] (bool) Whether already loaded memory locations are lost.
        @option minAddress [in] (int) The minimum address to read in the file, included.
        @option maxAddress [in] (int) The maximum address to read in the file, excluded.
        '''
        raise NotImplementedError
    # end def load

    def loadLines(self, lines,
                        overwrite  = True,
                        minAddress = 0,
                        maxAddress = MAX_INT):
        '''
        Loads the contents of a file in memory.

        @param  lines      [in] (tuple) A sequence of lines from a binary file.
        @option overwrite  [in] (bool) Whether already loaded memory locations are lost.
        @option minAddress [in] (int) The minimum address to read in the file, included.
        @option maxAddress [in] (int) The maximum address to read in the file, excluded.
        '''
        raise NotImplementedError
    # end def loadLines

    def save(self, filePath,
                   offset      = None,
                   length      = None,
                   blockLength = None):
        '''
        Saves the memory contents to a file.

        @param  filePath    [in] (str) The path to the file to save.
        @option offset      [in] (int) Offset in memory at which to save. If None, the whole memory will be saved.
        @option length      [in] (int) The length of data to save, starting at offset. If offset or length is None, the whole memory is saved.
        @option blockLength [in] (int) The length of a block in each line of the resulting file.
        '''
        raise NotImplementedError
    # end def save

    def saveLines(self, offset      = None,
                        length      = None,
                        blockLength = None):
        '''
        Saves the memory contents to a list of lines.

        @option offset      [in] (int) The offset at which to start saving.
        @option length      [in] (int) The length for which to save.
        @option blockLength [in] (int) The length of a block in each line of the resulting file.

        If no offset or no length is specified, the whole memory, restricted to actual existing data, is saved.
        '''
        raise NotImplementedError
    # end def saveLines

    def getHeaders(self):
        '''
        Obtains the data contained in the headers, as a HexList.

        Note that headers may not be supported by all file formats.

        It is up to the caller to convert this header to a string if necessary,
        using, for instance:
        @code
        header = ''.join([chr(x) for x in binaryFile.getHeaders()[0]])
        @endcode

        @return (list) The list of headers for this binaryFile.
        '''
        return self._headers
    # end def getHeaders

    def setHeaders(self, headers):
        '''
        Sets the headers for the current file, as HexLists

        @param  headers [in] (list) The headers for this file.
        '''
        self._headers = headers
    # end def setHeaders

    def update(self, binaryFile):
        '''
        Updates the current file contents with the other file contents

        @param  binaryFile [in] (BinaryFile) The file to update with.
        '''
        assert isinstance(binaryFile, BinaryFile)
        self.image.update(binaryFile.image)
    # end def update
# end class BinaryFile

# ------------------------------------------------------------------------------
# END OF FILE
# ------------------------------------------------------------------------------
