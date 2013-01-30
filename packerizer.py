#
# Main Packerizer Class
#

import sys
import os
import json

class PackerException(Exception):
    pass

class Packer(object):

    ENGINES = {
        'yui': 'vendor/yui/build/yuicompressor-2.4.7.jar',
        'google_closure': 'vendor/google_closure/compiler.jar'
    }

    def __init__(self, basedir=None):
        """Loads up an instance of the Packer, with an optional basedir to look for the config in"""
        self.base_dir = basedir if basedir != None else "./"
        self.config_location = os.path.join(self.base_dir, "packerizer.json")
        self.buildfile_location = os.path.join(self.base_dir, "packerizer.buildfile.json")

        # Read in the config:
        if not os.path.exists(self.config_location):
            raise PackerException("Config file does not exist: %s" % self.config_location)

        with open(self.config_location) as config_file:
            self.config = json.load(config_file)

        # Sanity check the config file:
        if 'base_version' not in self.config:
            # Don't worry, guess at 0.0
            self.config['base_version'] = u'0.0'

        if 'output_dir' not in self.config:
            self.config['output_dir'] = os.path.join(self.base_dir, 'output')

        # Check that output exists, if not create.
        if not os.path.exists(self.config['output_dir']):
            os.makedirs(self.config['output_dir'])

        # Read the buildinfo file:
        if os.path.exists(self.buildfile_location):
            with open(self.config_location) as build_file:
                self.buildfile = json.load(build_file)
        else:
            self.buildfile = dict()


    def build_info(self):
        """Returns some information about the build we're about to make. TBD."""
        pass

    
    def _concat_files(self, file_list, output_filepath, input_basedir = None):
        """
        Concatenates all the files given in file_list into the output_file
        """
        concat_contents = ''
        for filename in file_list:
            if not input_basedir == None:
                file_fullpath = os.path.join(input_basedir, filename)
            else:
                file_fullpath = filename
            
            if os.path.exists(file_fullpath):
                with open(file_fullpath) as file_contents:
                    concat_contents += "/* File: " + file_fullpath + " */\n"
                    concat_contents += file_contents.read()
                    concat_contents += "\n\n"

        with open(output_filepath, 'w') as output_file:
            output_file.write(concat_contents)


    def compress(self):
        """Does the actual file sticking together and compression"""
        
        # Calculate the minor and full version filenames:
        minor_version = "0" if 'minor_version' not in self.buildfile else self.buildfile['minor_version']
        full_version = self.config['base_version'] + '.' + minor_version

        # Make the output directory
        full_output_dir = os.path.join(self.config['output_dir'], full_version)
        if not os.path.exists(full_output_dir):
            os.makedirs(full_output_dir)

        # Create the necessary dirs in the output folder:
        workspace_dir = os.path.join(full_output_dir, "workspace")
        if not os.path.exists(workspace_dir):
            os.makedirs(workspace_dir)

        # Housekeeping done, let's start making some sweet concatenated files!
        if 'packages' not in self.config:
            return

        # Work out the base dirs:
        css_basedir = self.base_dir if 'basedir_css' not in self.config else self.config['basedir_css']
        js_basedir = self.base_dir if 'basedir_js' not in self.config else self.config['basedir_js']

        for package in self.config['packages']:
            package_items = self.config['packages'][package]

            # Loop through the CSS and JS files, concating them into a single 
            # glorious whole and then running them through the optimisers!
            if 'css' in package_items:
                css_output_file = os.path.join(workspace_dir, package + ".css")
                self._concat_files(package_items['css'], css_output_file, css_basedir)

                # Now work out the optimiser to use!
                css_optimiser = 'yui' if 'css_engine' not in package_items else package_items['css_engine']
                css_params.append(self.ENGINES[css_optimiser])
                css_params.extend(['--type', 'css', ])
                

            if 'js' in package_items:
                js_output_file = os.path.join(workspace_dir, package + ".js")
                self._concat_files(package_items['js'], js_output_file, js_basedir)


