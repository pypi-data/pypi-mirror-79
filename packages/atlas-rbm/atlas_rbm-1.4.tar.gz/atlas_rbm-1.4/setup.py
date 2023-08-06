# -*- coding: utf-8 -*-

# Always prefer setuptools over distutils
#from ez_setup import use_setuptools
#use_setuptools()
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path, walk
import versioneer

def main():
	# additional files
	data_files = []
	for dirpath, dirnames, filenames in walk('atlas_rbm/notebooks'):
		tmp = []
		for filename in filenames:
			tmp.append(path.join(dirpath, filename))
		data_files.append(('atlas', tmp))

	for dirpath, dirnames, filenames in walk('atlas_rbm/templates'):
		tmp = []
		for filename in filenames:
			tmp.append(path.join(dirpath, filename))
		data_files.append(('atlas', tmp))
	#print(data_files)

	# Get the long description from the README file
	here = path.abspath(path.dirname(__file__))
	with open(path.join(here, 'README.md'), encoding='utf-8') as f:
		long_description = f.read()

	setup(
		name='atlas_rbm',
		license='GPLv3+',
		version='1.4',
		#version=versioneer.get_version(),
		description='Atlas: Reconstruction of Rule-Based Models from biological networks',
		long_description=long_description,
		long_description_content_type='text/markdown',
		url='https://github.com/glucksfall/atlas',
		author='Rodrigo Santibáñez',
		author_email='glucksfall@users.noreply.github.com',
		classifiers=[
			#'Development Status :: 1 - Planning',
			#'Development Status :: 2 - Pre-Alpha',
			#'Development Status :: 3 - Alpha',
			#'Development Status :: 4 - Beta',
			'Development Status :: 5 - Production/Stable',
			#'Development Status :: 6 - Mature',
			#'Development Status :: 7 - Inactive',

			# Indicate who your project is intended for
			'Intended Audience :: Science/Research',
			'Topic :: Scientific/Engineering',

			# Pick your license as you wish
			'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',

			# Specify the Python versions you support here. In particular, ensure
			# that you indicate whether you support Python 2, Python 3 or both.
			#'Programming Language :: Python :: 2',
			#'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			'Programming Language :: Python :: 3.4',
			'Programming Language :: Python :: 3.5',
			'Programming Language :: Python :: 3.6',
			'Programming Language :: Python :: 3.7',
			'Programming Language :: Python :: 3.8',

			# other classifiers added by author
			'Environment :: Console',
			'Operating System :: Unix',
			'Operating System :: Microsoft :: Windows',
			'Operating System :: MacOS',
		],

		python_requires='~=3.0',
		keywords=[
			'systems biology',
			'systems modeling',
			'rule-based modeling',
			'ordinary differential equations',
			'stochastic simulation',
			'parameter estimation'
			],
		install_requires=[
			'pysb>=1.11.0',
			'PythonCyc',
			'jupyter',
			'ipykernel',
			'seaborn',
			'importlib-resources',
			'pyvipr'
			],

		# WARNING: seems to be bdist_wheel only
		packages=find_packages(exclude=('contrib', 'docs', 'tests', 'notebooks', 'templates')),
		# using the MANIFEST.in file to exclude same folders from sdist
		include_package_data=False,

		# WARNING: use this way to install in the package folder and
		# to have access to files using importlib_resources or importlib.resources
		# bdist_wheel only
		#package_data = {
			#'atlas_rbm' : [
				#'notebooks/*',
				#]
			#},

		# WARNING: do not use data_files as the installation path is hard to determine
		# e.g.: ubuntu 18.04 install to /usr/local/installation_path or /$USER/.local/installation_path
		#data_files=[('installation_path', ['example/ucrit-twotails-5percent.txt'])],
		#data_files=data_files,

		# others
		project_urls={
			'Manual': 'https://atlas_rbm.readthedocs.io',
			'Bug Reports': 'https://github.com/glucksfall/atlas/issues',
			'Source': 'https://github.com/glucksfall/atlas',
		},
	)

if __name__ == '__main__':
    main()
