#!/usr/bin/env python
# encoding: utf-8
"""
Packerizer

Simple Asset versioning and compression for Python and PHP.

MIT License
Copyright Alex Gisby <alex@solution10.com>
"""

import argparse
import packerizer

help_message = '''
Simple Asset versioning and compression.
'''

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=help_message)
    parser.add_argument('--basedir', 
            help="Specify the base location of the config and build files"
        )

    parser.add_argument('--quiet', '-q',
            help="Don't output progress information",
            default=False
        )

    args = parser.parse_args()
    packer = packerizer.Packer(args.basedir)

    if not args.quiet:
        print "Packer loaded, reading config from %s" % packer.config_location
        print "Starting compression run..."

    packer.compress()

    print "Done"
    