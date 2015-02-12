from setuptools import setup


setup(
    name='autostatistical',
    version='0.4.0',
    packages=['autostatistical'],
    install_requires=[
        'Jinja2>=2.7,<2.8',
        'appdirs>=1.4,<1.5',
        'floodestimation==0.3.1'
    ],
    package_data={
        'autostatistical': ['templates/*.*'],
    },
)
