#
# Contains the Engines for Crushr to use
#

import os

class Engine(object):
	"""
	Generic Engine class for all engines to extend from, overloading
	wherever they need to
	"""

	# The path of the engine 
	ENGINE_PATH = None

	def __init__(self, file_to_compress):
		self.file_to_compress = file_to_compress
		self.options = []

	def options(self, options):
		"""
		Merges the given options into the options array to be used for compression
		"""
		pass



	def compress(self, output_file):
		"""
		Runs the actual compression and stores the result in a file
		"""
		pass