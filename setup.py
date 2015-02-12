from setuptools import setup
from os import path

here = path.abspath(path.dirname(__file__))
version = open(path.join(here, 'VERSION')).read()

setup(
    name='autostatistical',
    version=version,
    packages=['autostatistical'],
    install_requires=[
        'Jinja2>=2.7,<2.8',
        'appdirs>=1.4,<1.5',
        'floodestimation==0.3.1'
    ],
    package_data={
        'autostatistical': ['templates/*.*'],
    },
    zip_safe=False
)
