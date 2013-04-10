<?php

namespace Crushr;

/**
 * Client Library for reading the location of
 * assets packages.
 *
 * @package 	Crushr
 * @author 		Alex Gisby <alex@solution10.com>
 * @license 	MIT
 */
class Client
{
	/**
	 * @var 	string 	Base dir
	 */
	protected $basedir = '.';

	/**
	 * @var 	string 	Our latest version, read from the buildfile
	 */
	protected $current_version = false;

	/**
	 * @var 	bool 	Whether to serve files compressed or not.
	 */
	protected $serve_compressed = true;

	/**
	 * @var 	object 	Contents of the crushr file
	 */
	protected $crushr_contents;

	/**
	 * @var 	object 	Contents of the buildfile
	 */
	protected $buildfile_contents = false;

	/**
	 * Pass in the basedir if you like, if not, it'll use the current dir.
	 * From there, the constructor will read in the config from the crushr.json file.
	 *
	 * @param 	string 	Basedir (optional)
	 * @return 	this
	 */
	public function __construct($basedir = '.')
	{
		$this->basedir = rtrim($basedir, '/') . DIRECTORY_SEPARATOR;

		// Load the crushr config file:
		$crushr_filepath = $this->basedir . 'crushr.json';
		if(!file_exists($crushr_filepath))
			throw new Exception('crushr.json file not found at: ' . $crushr_filepath);

		$contents = file_get_contents($crushr_filepath);
		$this->crushr_contents = json_decode($contents);

		// Load the buildfile, if it's present.
		$build_filepath = $this->basedir . 'crushr.buildfile.json';
		if(file_exists($build_filepath))
		{
			$contents = file_get_contents($build_filepath);
			$this->buildfile_contents = json_decode($contents);
			$this->current_version = (isset($this->buildfile_contents->full_version))? $this->buildfile_contents->full_version : false;
		}
	}

	/**
	 * Sets whether to serve the compressed version of files or not.
	 * By default, we try and serve compressed (kinda the point in this kit)
	 * but if there's no buildfile, and even if you set this to TRUE, we will
	 * instead serve the uncompressed, just to make sure you actually have some
	 * styles!
	 *
	 * @param 	bool 	true to serve compressed, false to not
	 * @return 	bool|this
	 */
	public function serve_compressed($serve_compressed = null)
	{
		if($serve_compressed === null)
			return $this->serve_compressed;

		$this->serve_compressed = (bool)$serve_compressed;
		return $this;
	}

	/**
	 * Serve the CSS files for a package.
	 * This will fail silently in almost any error condition. Why? Because we want to be
	 * robust and if there's nothing there, do exactly that; nothing.
	 *
	 * @param 	string 	Package name.
	 * @return 	array 	Array of file URLs for the CSS
	 */
	public function css($package_name)
	{
		$css = array();

		// See if we have the buildfile:
		if($this->serve_compressed && $this->buildfile_contents)
		{
			$css_prefix = (isset($this->crushr_contents->webroot))? $this->crushr_contents->webroot : '';
			$css[] = $css_prefix . $this->current_version . DIRECTORY_SEPARATOR . $package_name . '.min.css';
		}
		else
		{
			// We don't have a buildfile, or have specifically asked not to use it.
			// Build up as normal:
			$css_prefix = (isset($this->crushr_contents->webroot_uncompressed))? $this->crushr_contents->webroot_uncompressed : '';
			if(isset($this->crushr_contents->packages->{$package_name}->css))
			{
				$files = $this->crushr_contents->packages->{$package_name}->css;
				foreach($files as $file)
				{
					$css[] = $css_prefix . $file;
				}
			}
		}

		return $css;
	}

	/**
	 * Serve the JS files for a package.
	 * This will fail silently in almost any error condition. Why? Because we want to be
	 * robust and if there's nothing there, do exactly that; nothing.
	 *
	 * @param 	string 	Package name.
	 * @return 	array 	Array of file URLs for the JS
	 */
	public function js($package_name)
	{
		$js = array();

		// See if we have the buildfile:
		if($this->serve_compressed && $this->buildfile_contents)
		{
			$js_prefix = (isset($this->crushr_contents->webroot))? $this->crushr_contents->webroot : '';
			$js[] = $js_prefix . $this->current_version . DIRECTORY_SEPARATOR . $package_name . '.min.js';
		}
		else
		{
			// We don't have a buildfile, or have specifically asked not to use it.
			// Build up as normal:
			$js_prefix = (isset($this->crushr_contents->webroot_uncompressed))? $this->crushr_contents->webroot_uncompressed : '';
			if(isset($this->crushr_contents->packages->{$package_name}->js))
			{
				$files = $this->crushr_contents->packages->{$package_name}->js;
				foreach($files as $file)
				{
					$js[] = $js_prefix . $file;
				}
			}
		}

		return $js;
	}

}
