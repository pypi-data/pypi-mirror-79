""" Unpacks an `All-in-One WP Migration` package. """

import errno
import os
from .exception import Ai1wmError
from .header import Ai1wmHeader
from .str_ import s__


class Ai1wmUnpacker(object):
    """ Unpacks an `All-in-One WP Migration` package. """

    @staticmethod
    def __make_dirs(path, mode=0o777):
        """ A simple wrapper of os.makedirs(), which does not raise exception if the leaf directory already exists. """

        try:
            os.makedirs(path, mode=mode)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise Ai1wmError('error creating a directory: {}, error: {}'.format(path, e))
        return path

    @classmethod
    def __extract_file(cls, stream, path, size):
        """ Extracts a file from the input stream. """

        block_size = 0x4000

        with open(path, 'wb') as f:
            while size > 0:
                if block_size > size:
                    block_size = size
                block = stream.read(block_size)
                if len(block) != block_size:
                    raise Ai1wmError('error extracting a file: {}, error: bad file size'.format(path))
                f.write(block)
                size -= len(block)

    @classmethod
    def __unpack(cls, stream, target):
        """ Unpacks a package. """

        while True:
            header = Ai1wmHeader.unpack(stream.read(Ai1wmHeader.SIZE))
            if header.eof:
                break

            path = os.path.join(target, header.path)
            cls.__make_dirs(path)

            path = os.path.join(path, header.name)
            cls.__extract_file(stream, path, header.size)

    @classmethod
    def unpack(cls, source, target):
        """ Unpacks a package. """

        source, target = s__(os.path.realpath(source)), s__(os.path.realpath(target))
        try:
            with open(source, 'rb') as f:
                cls.__unpack(f, target)
        except Exception as ex:
            raise Ai1wmError('error unpacking a file: {}, error: {}'.format(source, ex))
        return target
