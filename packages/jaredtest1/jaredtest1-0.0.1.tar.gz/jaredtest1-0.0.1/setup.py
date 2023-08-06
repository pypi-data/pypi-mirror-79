from setuptools import setup

with open("C:/Users/jared/pythoncode/jaredtest1/README.txt", "r") as fh:
	long_description = fh.read()

setup(
	name = 'jaredtest1',
	version = '0.0.1',
	description = 'Say hello!',
	py_modules = ["jaredtest1"],
	package_dir = {'': 'src'},
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
		"Operating System :: OS Independent",
	],
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://github.com/danielwilczak101/EasyGA",
	author = "Jared Curtis",
	author_email = "curtij18@my.erau.edu",
)