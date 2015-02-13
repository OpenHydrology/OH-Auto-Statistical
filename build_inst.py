# -*- coding: utf-8 -*-

from subprocess import call
import version

# Update version from GIT tags if possible
version.update()

# Parse version and build number from VERSION file
full_version = open('VERSION').read().split('-')
version = full_version[0]
conda_channel = 'https://conda.binstar.org/openhydrology'

if len(full_version) == 1:  # Public release version
    number = 0
    out_file_name = 'autostatistical-{}-win64.exe'.format(version)
else:  # Private build version
    number = full_version[1]
    out_file_name = 'autostatistical-{}-win64_{}.exe'.format(version, number)
    conda_channel = conda_channel + '/channel/dev -c ' + conda_channel  # Add dev channel

nsis_args = [r'c:\Program Files (x86)\NSIS\makensis.exe',
             '/DVERSION=' + version,
             '/DNUMBER=' + number,
             '/DOUTFILENAME=' + out_file_name,
             '/DCONDA_CHANNEL=' + conda_channel,
             'installer\win\installer.nsi']
call(nsis_args)