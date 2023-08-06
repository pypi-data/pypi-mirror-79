from setuptools import setup

# read the contents of your README file
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
	  name='gps2space',
	  long_description=long_description,
	  long_description_content_type='text/markdown',
	  packages=['gps2space'],
      version='0.1.3',
      license='MIT',
      description='A Python library for building spatial data and calculating buffer- and Convex hull-based activity space from raw GPS data',
      author='GPS2space',
      author_email='sxz217@psu.edu',
      url='https://gps2space.readthedocs.io/en/latest/',
      keywords = ['GPS', 'activity space', 'buffer', 'convex hull'],
      install_requires=[
                        'pandas',
                        'geopandas',
                        'numpy',
                        'scipy',
                        'shapely'],
	  classifiers=[
	  	           'Development Status :: 4 - Beta',
	  	           'Programming Language :: Python :: 3',
	               'License :: OSI Approved :: MIT License',
				   'Operating System :: OS Independent'],
      )
