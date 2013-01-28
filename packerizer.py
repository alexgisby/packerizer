#
# Main Packerizer Class
#

import sys
import os
import json

class PackerException(Exception):
	pass

class Packer(object):
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


	def build_info(self):
		"""Returns some information about the build we're about to make. TBD."""
		pass

		
	def compress(self):
		"""Does the actual file sticking together and compression"""
		pass

