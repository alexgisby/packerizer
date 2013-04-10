#
# Contains the Engines for Crushr to use
#

import os
import subprocess
import pipes

class Engine(object):
    """
    Generic Engine class for all engines to extend from, overloading
    wherever they need to
    """

    # The path of the engine 
    ENGINE_PATH = None

    def __init__(self):
        self.opts = {}
        self.type = False

        self._set_base_options()

    def set_type(self, type):
        """
        Sets the type of file to compress.
        """
        self.type = type

    def _set_base_options(self):
        """
        Overload point for engines to set their basic options before doing
        anything else.
        """
        pass

    def options(self, opts):
        """
        Merges the given options into the options array to be used for compression.
        Pass options in as key: value pairs in a dict.

        Other engines will specify their own options, so see their docstrings for usage.
        """
        self.opts = dict(self.opts.items() + opts.items())

    def _flatten_options(self):
        """
        Turns the key-value dict into a flattened list appropriate for the subprocess module
        """
        flat = []
        for key in self.opts:
            flat.append(key)
            flat.append(self.opts[key])

        return flat

    def compress(self, input_file, output_file):
        """
        Runs the actual compression and stores the result in the output file
        """
        pass


#
# YUI Compressor
#
class YUI(Engine):
    """
    Options:
        type: css or js
    """

    def __init__(self):
        jarpath = os.path.dirname(os.path.realpath(__file__)) + '/../'
        self.ENGINE_PATH = 'java -jar ' + pipes.quote(jarpath) + 'vendor/yui/build/yuicompressor-2.4.7.jar'
        Engine.__init__(self);

    def compress(self, input_file, output_file):
        self.options({
                '--type': self.type,
                '-o': output_file
            })
        opts = self._flatten_options()
        cmd = [self.ENGINE_PATH]
        cmd.extend(opts)
        cmd.extend([input_file])

        # Fairly sure this isn't the way to do it, but I can't get subprocess working
        # nicely with cmd as a list. Probably showing my noobishness again :D
        cmd = " ".join(cmd)
        subprocess.call(cmd, shell=True)


#
# Google Closure
#
class Closure(Engine):

    def __init__(self):
        jarpath = os.path.dirname(os.path.realpath(__file__)) + '/../'
        self.ENGINE_PATH = 'java -jar ' + pipes.quote(jarpath) + 'vendor/google_closure/compiler.jar'
        Engine.__init__(self);

    def _set_base_options(self):
        """
        By default, in Closure we use SIMPLE_OPTIMIZATIONS. You can overload this in your
        crushr.json file using the js_options: parameter.
        """
        self.options({
                '--compilation_level': 'SIMPLE_OPTIMIZATIONS'
            })

    def compress(self, input_file, output_file):
        self.options({
                '--js': input_file,
                '--js_output_file': output_file
            })

        opts = self._flatten_options()
        cmd = [self.ENGINE_PATH]
        cmd.extend(opts)

        # Again, not sure this is the correct way, but it works
        cmd = " ".join(cmd)
        subprocess.call(cmd, shell=True)
