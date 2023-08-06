#!/usr/bin/python
"""
Packs/Unpacks `All-in-One WP Migration` packages. For more information:
https://wordpress.org/plugins/all-in-one-wp-migration/
"""

import json
import os
from .exception import Ai1wmError
from .packer import Ai1wmPacker
from .unpacker import Ai1wmUnpacker


class Ai1wmPackage(object):
    """ An unpacked All-in-One WP Migration package. """

    DATABASE_FILE = 'database.sql'
    INFO_FILE = 'package.json'
    LOG_FILE = 'migration.log'

    def __init__(self, base_dir):
        """ Constructor. """

        self.base_dir = base_dir
        self._details = None
        self._plugins = None

    @property
    def info_file(self):
        """ Path to the migration information file. """

        return os.path.join(self.base_dir, self.INFO_FILE)

    @property
    def database_file(self):
        """ Path to the database dump file. """

        return os.path.join(self.base_dir, self.DATABASE_FILE)

    @property
    def log_file(self):
        """ Path to the migration log file. """

        return os.path.join(self.base_dir, self.LOG_FILE)

    @property
    def details(self):
        """ Details of the package. """

        if self._details is None:
            try:
                with open(self.info_file, 'r') as fp:
                    self._details = json.load(fp)
            except IOError:
                raise Ai1wmError('error reading package information file: {}'.format(self.info_file))
        return self._details

    @property
    def plugins(self):
        """ A list of active plugins. """

        if self._plugins is None:
            try:
                self._plugins = [i.split('/', 1)[0] for i in self.details['Plugins']]
            except (KeyError, TypeError, ValueError):
                raise Ai1wmError('error retrieving plugin list from package information: {}'.format(self.details))
        return self._plugins

    @property
    def stylesheet(self):
        """ The active style sheet. """

        return self.details.get('Stylesheet', None)

    @property
    def template(self):
        """ The active template. """

        return self.details.get('Template', None)

    def validate(self):
        """ Validates the package. """

        if not os.path.isfile(self.info_file):
            raise Ai1wmError('package information file is missing: {}'.format(self.info_file))
        if not os.path.isfile(self.database_file):
            raise Ai1wmError('database dump file is missing: {}'.format(self.database_file))
        return self

    def unpack_from(self, source_file):
        """ Unpacks a package. """

        if not os.path.isfile(source_file):
            raise Ai1wmError('not a file: {}'.format(source_file))
        Ai1wmUnpacker.unpack(source_file, self.base_dir)

        return self.validate()

    def pack_to(self, target_file):
        """ Packs a package. """

        return Ai1wmPacker.pack(self.validate().base_dir, target_file)


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Pack/Unpack All-in-One WP Migration Packages')
    parser.add_argument('source', help='source path')
    parser.add_argument('target', help='target path')
    args = parser.parse_args()

    try:
        if os.path.isfile(args.source):
            Ai1wmPackage(args.target).unpack_from(args.source)
        elif os.path.isdir(args.source):
            Ai1wmPackage(args.source).pack_to(args.target)
    except Ai1wmError as e:
        print(e)
