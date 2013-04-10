# Crushr

Simple asset minification, with asset grouping, minification with multiple backends and
client libraries for PHP and Python.

## Key Features

- Group your CSS and JS files into "Packages"
- Each Package is combined into a single file and minified using your choice of engine.
- Per-package compression settings.
- Per-package engine decision! Want your homepage assets compressed with YUI, but the About Page Google Closure? Sure we can do that.
- YUI and Google Closure supported out the box.
- Engine interface to write your own backend.
- Compression stats and automatic versioning.

## How to Use

Let's assume you have a project that looks like this:

	/app
	/public_html
	  /css
	  /js
	  /index.html


### Installation:

Clone/copy crushr into your project:

	/app
	/crushr
	/public_html
	  /css
	  /js
	  /index.html


### crushr.json - Basic

All of your packages and options for crushr are defined in crushr.json. This file should probably sit at
the top of your project to keep things flexible:

	/app
	/crushr
	crushr.json
	/public_html
	  /css
	  /js
	  /index.html


The simplest crushr.json file you can have looks like this:

	{
		"base_version": "1.0",
		"basedir_css": "./public_html/css",
		"basedir_js": "./public_html/js"
	}

Basically, this is saying that we're working on version 1.0 of the project, and so all builds will be
a minor version of this (1.0.0 then 1.0.1 etc). We also tell crushr where to find the CSS and JS files
in general, we'll define the packages in a moment.

### Running crushr

In your Terminal, from the top of your project, run the following:

	$ python crushr/compress.py

Awesome! You just ran your first Crushr pass!

### But nothing happened...

Yep, all your CSS and JS files will remain blissfully uncompressed. To get crushr to compress files, you need
to group them together into Packages.

Let's add a new Package into our crushr.json file:


