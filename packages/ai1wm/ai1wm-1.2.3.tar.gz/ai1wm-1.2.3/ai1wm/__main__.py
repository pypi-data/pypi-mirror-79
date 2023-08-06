""" Entry of the ai1wm program. """

import argparse
import os
import sys
from .exception import Ai1wmError
from .package import Ai1wmPackage


if __name__ == '__main__':
    """ Entry of the ai1wm program. """

    parser = argparse.ArgumentParser(prog='ai1wm', description='Pack/Unpack All-in-One WP Migration Packages')
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
        sys.exit(-1)

    sys.exit(0)
