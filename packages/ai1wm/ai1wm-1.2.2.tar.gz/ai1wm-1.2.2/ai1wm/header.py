""" Parses ai1wm file header. """

import collections
import struct
from .exception import Ai1wmError
from .str_ import b__, s__


class Ai1wmHeader(tuple):
    """ Parses an `All-in-One WP Migration` header. """

    SIZE = 4377
    EOF = b'\x00' * SIZE

    _Location = collections.namedtuple('_Location', ['offset', 'size'])
    _LOC_NAME = _Location(0, 255)       # File name
    _LOC_SIZE = _Location(255, 14)      # File size
    _LOC_TIME = _Location(269, 12)      # Last modified time
    _LOC_PATH = _Location(281, 4096)    # File path

    def __new__(cls, path=None, name=None, size=None, time=None):
        """ Returns a new instance of the object. """

        if path or name or size or time:
            if not isinstance(path, str) or path == '':
                raise ValueError('<path> must be a nonempty string')
            if not isinstance(name, str) or name == '':
                raise ValueError('<name> must be a nonempty string')
            if not isinstance(size, int) or size < 0:
                raise ValueError('<size> must be a non-negative integer')
            if not isinstance(time, int) or time < 0:
                raise ValueError('<time> must be a non-negative integer')

        return super(Ai1wmHeader, cls).__new__(cls, [path, name, size, time])

    @classmethod
    def unpack(cls, header):
        """ Unpacks a binary header. """

        if len(header) != cls.SIZE:
            raise Ai1wmError('invalid header size')

        if header == cls.EOF:
            return cls()

        return cls(
            path=s__(cls.__extract_field(header, cls._LOC_PATH)),
            name=s__(cls.__extract_field(header, cls._LOC_NAME)),
            size=cls.__extract_int(header, cls._LOC_SIZE),
            time=cls.__extract_int(header, cls._LOC_TIME),
        )

    def pack(self):
        """ Packs to a binary header. """

        attributes, formats, locations = [], '', [
            ('name', self._LOC_NAME),
            ('size', self._LOC_SIZE),
            ('time', self._LOC_TIME),
            ('path', self._LOC_PATH),
        ]

        for name, location in locations:
            attribute = b__(getattr(self, name))
            if len(attribute) > location.size:
                raise Ai1wmError('{} is too long to pack: {}'.format(name, getattr(self, name)))
            attributes.append(attribute)
            formats += '{}s'.format(location.size)

        return struct.pack(formats, *attributes)

    @property
    def path(self):
        """ Path of the file. """

        return self[0]

    @property
    def name(self):
        """ Name of the file. """

        return self[1]

    @property
    def size(self):
        """ Size of the file. """

        return self[2]

    @property
    def time(self):
        """ Time of the file. """

        return self[3]

    @property
    def eof(self):
        """ Indicates if this is an EOF header. """

        return not any(self)

    @classmethod
    def __extract_field(cls, header, location):
        """ Extracts a header field. """

        try:
            field = struct.unpack_from('{}s'.format(location.size), header, offset=location.offset)[0]
        except struct.error as e:
            raise Ai1wmError('error extracting a header field, error: {}'.format(e))

        return field.rstrip(b'\x00')

    @classmethod
    def __extract_int(cls, header, location):
        """ Extracts an integral header field. """

        try:
            return int(cls.__extract_field(header, location))
        except ValueError:
            raise Ai1wmError('invalid header field')
