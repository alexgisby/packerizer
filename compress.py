#!/usr/bin/env python
# encoding: utf-8
"""
crushr

Simple Asset versioning and compression for Python and PHP.

MIT License
Copyright Alex Gisby <alex@solution10.com>
"""

import argparse
from crushr.Packer import Packer
import os

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

    parser.add_argument('--force_version', '-fv',
            help="Force crushr to build to a certain version number",
            default=None
        )

    args = parser.parse_args()
    packer = Packer(args.basedir)

    print ""

    if not args.quiet:
        print "Packer loaded, reading config from %s" % packer.config_location
        print "Starting compression run..."

    buildinfo = packer.compress(args.force_version)

    # Output some information about that build:
    if not args.quiet:
        print "Build Complete! Here come the stats:"
        print ""

        print "Version: %s" % buildinfo['full_version']
        print "Packages Built:"
        for package in buildinfo['packages_built']:
            package_items = buildinfo['packages_built'][package]

            print "  %s:" % package

            if len(package_items['css']) > 0:
                css_reduction = 100 - ((package_items['css_output_size'] / float(package_items['css_input_size'])) * 100)
                print "    CSS: %d files, %d" % (len(package_items['css']), css_reduction) + "% size reduction"

            if len(package_items['js']) > 0:
                js_reduction = 100 - ((package_items['js_output_size'] / float(package_items['js_input_size'])) * 100)
                print "    JS: %d files, %d" % (len(package_items['js']), js_reduction) + "% size reduction"

            print ""


        print ""
        print "Build Complete! Have a terrific day"
        print ""


    
