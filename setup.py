from setuptools import setup, find_packages
import sys, os
import subprocess
import glob

version_py = os.path.join(os.path.dirname(__file__), 'version.py')
with open(version_py, 'r') as fh:
    version_git = open(version_py).read().strip().split('=')[-1].replace('"','')

try:
    with open("requirements.txt", "r") as f:
        install_requires = [x.strip() for x in f.readlines()]
except IOError:
        install_requires = [
          "flask",
          "pytest"]


setup(name='lims_dashboard',
      version=version_git,
      description="Dashboard wepapp to interact with Genologics LIMS",
      classifiers=[
	"Development Status :: 4 - Beta",
	"Environment :: Web Environment",
	"Intended Audience :: Developers",
	"Intended Audience :: Healthcare Industry",
	"Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
	"Operating System :: POSIX :: Linux",
	"Programming Language :: Python"
	],
      keywords='Genologics lims illumina EPP',
      author='Denis Moreno',
      author_email='milui.galithil@gmail.com',
      maintainer='Denis Moreno',
      maintainer_email='denis.moreno@scilifelab.se',
      url='https://github.com/Galithil/lims_dashboard',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      scripts=glob.glob("scripts/*.py"),
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
