import setuptools

with open("README.md", "r") as fh:   
	long_description = fh.read()
	#fh = file header

setuptools.setup(
	name="numdatasalva",
	version="0.0.5",
	author="Salvador Gimeno",
	author_email="Salvador.Gimeno@xyz.com",
	description="A simple package calculating values for a simple number",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="",
	keywords="numbers package calculations",
	packages=setuptools.find_packages(),
	classifiers=[
		"Programming Language :: Python :: 2",
		
		# How mature is this project? Common values are
    	#   3 - Alpha
   	 	#   4 - Beta
    	#   5 - Production/Stable
    	'Development Status :: 3 - Alpha',

    	# Indicate who your project is intended for
    	'Intended Audience :: Developers',
    	'Topic :: Software Development :: Build Tools',

    	# Pick your license as you wish (should match "license" above)
     	'License :: OSI Approved :: MIT License',

    	# Specify the Python versions you support here. In particular, ensure
    	# that you indicate whether you support Python 2, Python 3 or both.
    	'Programming Language :: Python :: 2',
    	'Programming Language :: Python :: 2.6',
    	'Programming Language :: Python :: 2.7',
    	'Programming Language :: Python :: 3',
    	'Programming Language :: Python :: 3.2',
    	'Programming Language :: Python :: 3.3',
    	'Programming Language :: Python :: 3.4'
    	# For a full listing, see https://pypi.org/classifiers/
		]
		)