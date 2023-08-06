import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()
	
setuptools.setup(
	name = "nitrogen",
	version = "0.0.1",
	author = "Bryan Changala",
	author_email = "bryan.changala@gmail.com",
	description = "A scientific computing package for rovibronic molecular spectroscopy.",
	long_description = long_description,
	long_description_content_type = "text/markdown",
	url = "https://www.colorado.edu/nitrogen",
	packages = setuptools.find_packages(),
	classifiers = [
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
	python_requires = '>=3.6',
)