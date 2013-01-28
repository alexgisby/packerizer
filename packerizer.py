#
# Main Packerizer Class
#

import sys
import os
import json

class PackerException(Exception):
	pass

class Packer(object):
	def __init__(self, basedir=None, output=None):
		self.base_dir = basedir if basedir != None else "./"
		self.config_location = os.path.join(self.base_dir, "packerizer.json")
		self.buildfile_location = os.path.join(self.base_dir, "packerizer.buildfile.json")

		# Read in the config:
		if not os.path.exists(self.config_location):
			raise PackerException("Config file does not exist: %s" % self.config_location)

		with open(self.config_location) as config_file:
			self.config = json.load(config_file)

		print self.config
