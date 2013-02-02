import sys
import os
import json
import engines
import shutil
from datetime import datetime

class PackerException(Exception):
    pass

class Packer(object):

    def __init__(self, basedir=None):
        """Loads up an instance of the Packer, with an optional basedir to look for the config in"""
        self.base_dir = basedir if basedir != None else "./"
        self.config_location = os.path.join(self.base_dir, "crushr.json")
        self.buildfile_location = os.path.join(self.base_dir, "crushr.buildfile.json")

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
            with open(self.buildfile_location) as build_file:
                self.buildfile = json.load(build_file)
        else:
            self.buildfile = dict()

        print self.buildfile
    
    def _concat_files(self, file_list, output_filepath, input_basedir = None):
        """
        Concatenates all the files given in file_list into the output_file
        """
        concat_contents = ''
        concatted_files = []
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

                    concatted_files.append(file_fullpath)

        with open(output_filepath, 'w') as output_file:
            output_file.write(concat_contents)

        return concatted_files


    def _load_engine(self, engine_name, language):
        """
        Takes an engine name and returns a full instance
        """
        eng = False
        if engine_name == 'yui':
            eng = engines.YUI()
        elif engine_name == 'google_closure':
            eng = engines.Closure()

        if not eng:
            raise PackerException("No Engine called: %s" % engine_name)

        eng.set_type(language)
        return eng

    def compress(self, force_version=None):
        """Does the actual file sticking together and compression"""
        
        # Calculate the minor and full version filenames if not forcing
        # a version. If you do force it, you're pretty much on your own
        # when it comes to auto-calculating the next version.
        if force_version == None:
            minor_version = 0 if 'minor_version' not in self.buildfile else int(self.buildfile['minor_version']) + 1
            full_version = self.config['base_version'] + '.' + str(minor_version)
        else:
            full_version = force_version
            minor_version = 0 if 'minor_version' not in self.buildfile else int(self.buildfile['minor_version'])

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

        # Start the buildinfo dict ready to whack some data in there.
        version_buildinfo = {
            "minor_version": minor_version,
            "full_version": full_version,
            "packages_built": {}
        }

        for package in self.config['packages']:
            package_items = self.config['packages'][package]

            version_buildinfo['packages_built'][package] = {
                'css': [],
                'js': []
            }

            # Loop through the CSS and JS files, concating them into a single 
            # glorious whole and then running them through the optimisers!
            if 'css' in package_items:
                css_concat_file = os.path.join(workspace_dir, package + ".css")
                files_built = self._concat_files(package_items['css'], css_concat_file, css_basedir)

                # Add the files built into the buildinfo:
                version_buildinfo['packages_built'][package]['css'] = files_built

                # Now work out the optimiser to use! Default to YUI (as we only support YUI...)
                css_optimiser_name = 'yui' if 'css_engine' not in package_items else package_items['css_engine']
                css_options = {} if 'css_options' not in package_items else package_items['css_options']

                # Load the engine, set the options
                css_engine = self._load_engine(css_optimiser_name, 'css')
                css_engine.options(css_options)

                # And now run the compression via the engine!
                css_output_file = os.path.join(full_output_dir, package + ".min.css")
                css_engine.compress(css_concat_file, css_output_file)


            if 'js' in package_items:
                js_concat_file = os.path.join(workspace_dir, package + ".js")
                files_built = self._concat_files(package_items['js'], js_concat_file, js_basedir)

                # Add the files built into the buildinfo:
                version_buildinfo['packages_built'][package]['js'] = files_built

                # Now work out the optimiser to use! Default to Closure
                js_optimiser_name = 'google_closure' if 'js_engine' not in package_items else package_items['js_engine']
                js_options = {} if 'js_options' not in package_items else package_items['js_options']

                # Load the engine, set the options
                js_engine = self._load_engine(js_optimiser_name, 'js')
                js_engine.options(js_options)

                # And now run the compression via the engine!
                js_output_file = os.path.join(full_output_dir, package + ".min.js")
                js_engine.compress(js_concat_file, js_output_file)


        # All done compressing, remove the workspace and write the .buildinfo files
        shutil.rmtree(workspace_dir)

        # Write the version buildinfo into the output directory:
        version_buildinfo['last_built'] = str(datetime.now())
        with open(os.path.join(full_output_dir, "version.buildinfo.json"), 'w') as version_buildinfo_file:
            json.dump(version_buildinfo, version_buildinfo_file, indent=4)

        # And now write the main buildinfo file. This is very small
        # as it just stores the highest minor version.
        buildinfo_minor_version = minor_version
        if force_version == None and 'minor_version' in self.buildfile:
            if int(self.buildfile['minor_version']) > minor_version:
                buildinfo_minor_version = self.buildfile['minor_version']

        buildinfo = {
            "last_build": str(datetime.now()),
            "full_version": full_version,
            "minor_version": buildinfo_minor_version
        }

        with open(self.buildfile_location, 'w') as buildfile_file:
            json.dump(buildinfo, buildfile_file, indent=4)


