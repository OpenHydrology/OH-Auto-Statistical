from setuptools import setup
from os import path
import version

# Update version from GIT tags if possible and create version file
version.update()

here = path.abspath(path.dirname(__file__))
version = open(path.join(here, 'VERSION')).read().split('-')[0]

setup(
    name='autostatistical',
    version=version,
    packages=['autostatistical'],
    package_data={
        'autostatistical': ['templates/*.*']
    },
    zip_safe=False
)
