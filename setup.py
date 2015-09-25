from setuptools import setup
import versioneer

setup(
    name='autostatistical',
    packages=['autostatistical'],
    package_data={
        'autostatistical': ['application.ico',
                            'config.ini',
                            'templates/*.*']
    },
    zip_safe=False,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass()
)
