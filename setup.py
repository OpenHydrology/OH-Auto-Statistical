from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='autostatistical',
    version='0.2.0',
    packages=['autostatistical'],
    url='https://github.com/OpenHydrology/OH-Auto-Statistical',
    license='GPLv3',
    author='Florenz A. P. Hollebrandse',
    author_email='f.a.p.hollebrandse@protonmail.ch',
    description='Fully automated flood estimation for UK catchments',
    long_description=long_description,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "Environment :: Other Environment",
        "Intended Audience :: Education",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
    install_requires=[
        'Jinja2>=2.7.3',
        'appdirs>=1.4.0',
        'floodestimation>=0.2.0'
    ],
    package_data={
        'autostatistical': ['templates/*.*'],
    },
)
