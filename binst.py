# -*- coding: utf-8 -*-
#
# Script to build the Windows installer
#
# Requires NSIS including some extensions.

from subprocess import call
import versioneer

full_version = versioneer.get_versions()['version'].split('+')
version = full_version[0]
conda_channel = 'https://conda.anaconda.org/openhydrology'

if len(full_version) == 1:  # Public release version
    number = 0
    out_file_name = 'autostatistical-{}-win64.exe'.format(version)
else:  # Private build version
    number = int(full_version[1].split('.')[0])
    out_file_name = 'autostatistical-{}-win64_{}.exe'.format(version, number)
    conda_channel = conda_channel + '/channel/dev -c ' + conda_channel  # Add dev channel
build = 'py34_' + str(number)

nsis_args = [r'c:\Program Files (x86)\NSIS\makensis.exe',
             '/DVERSION=' + version,
             '/DBUILD=' + build,
             '/DOUTFILENAME=' + out_file_name,
             '/DCONDA_CHANNEL=' + conda_channel,
             'installer\win\installer.nsi']
call(nsis_args)