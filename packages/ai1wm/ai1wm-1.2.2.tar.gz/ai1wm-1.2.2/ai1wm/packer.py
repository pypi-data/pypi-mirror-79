""" Packs an `All-in-One WP Migration` package. """

import os
from .exception import Ai1wmError
from .header import Ai1wmHeader
from .str_ import s__


class Ai1wmPacker(object):
    """ Packs an `All-in-One WP Migration` package. """

    @classmethod
    def __archive_file(cls, stream, root_dir, path, name):
        """ Archives a file to the output stream. """

        full_path = os.path.join(path, name)
        header = Ai1wmHeader(
            path=path[len(root_dir) + 1:] or '.',
            name=name,
            size=os.path.getsize(full_path),
            time=int(os.path.getmtime(full_path)),
        )
        stream.write(header.pack())

        with open(full_path, 'rb') as f:
            while True:
                block = f.read(0x4000)
                if len(block) <= 0:
                    break
                stream.write(block)

    @classmethod
    def __pack(cls, stream, source):
        """ Packs a package. """

        for path, _, files in os.walk(source):
            for name in files:
                cls.__archive_file(stream, source, path, name)
        stream.write(Ai1wmHeader.EOF)

    @classmethod
    def pack(cls, source, target):
        """ Packs a package. """

        source, target = s__(os.path.realpath(source)), s__(os.path.realpath(target))
        try:
            with open(target, 'wb') as f:
                cls.__pack(f, source)
        except Exception as ex:
            raise Ai1wmError('error packing a directory: {}, error: {}'.format(source, ex))
        return target
