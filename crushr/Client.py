import os

class Exception(Exception):
	pass

class Client(object):
	"""
	Client library for reading the buildfiles for your frontend code
	"""

	def __init__(self, basedir="."):
		"""
		Pass in the basedir if you like, if not, it'll use the current dir.
	 	From there, the constructor will read in the config from the crushr.json file.
		"""
		self.basedir = basedir
		self.current_version = False
		self.buildfile_contents = False

		crushr_filepath = os.path.join(self.basedir, 'crushr.json')
		if not os.path.exists(crushr_filepath):
			raise Exception('crushr.json file not found at: %s' % crushr_filepath)

		with open(crushr_filepath, 'r') as f:
			self.crushr_contents = json.load(f)

		# Load the buildfile, if we have one.
		build_filepath = os.path.join(self.basedir, 'crushr.buildfile.json')
		if os.path.exists(build_filepath):
			with open(build_filepath, 'r') as f:
				self.buildfile_contents = json.load(f)
				self.current_version = False if 'full_version' not in self.buildfile_contents else self.buildfile_contents['full_version']

	def serve_compressed(self, serve_compressed=None):
		"""
		Sets whether to serve the compressed version of files or not.
	 	By default, we try and serve compressed (kinda the point in this kit)
		but if there's no buildfile, and even if you set this to TRUE, we will
	 	instead serve the uncompressed, just to make sure you actually have some
	 	styles!
		"""
		if serve_compressed == None:
			return self.serve_compressed

		self.serve_compressed = serve_compressed
		return self

	def css(self, package_name):
		"""
		Serve the CSS files for a package.
	 	This will fail silently in almost any error condition. Why? Because we want to be
	 	robust and if there's nothing there, do exactly that; nothing.
		"""
		css = []

		if self.serve_compressed and self.buildfile_contents:
			css_prefix = '' if 'webroot' not in self.crushr_contents else self.crushr_contents['webroot']
			css.append(
				[css_prefix, self.current_version, package_name + '.min.css'].join('/')
			)
		else:
			# css_prefix = 


			$css_prefix = (isset($this->crushr_contents->webroot_uncompressed))? $this->crushr_contents->webroot_uncompressed : '';
			if(isset($this->crushr_contents->packages->{$package_name}->css))
			{
				$files = $this->crushr_contents->packages->{$package_name}->css;
				foreach($files as $file)
				{
					$css[] = $css_prefix . $file;
				}
			}

