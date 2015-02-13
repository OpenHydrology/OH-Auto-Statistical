# -*- coding: utf-8 -*-

from subprocess import call

full_version = open('VERSION').read().split('-')
version = full_version[0]
if len(full_version) > 1:
    number = full_version[1]
    out_file_name = 'autostatistical-{}-win64_{}.exe'.format(version, number)
else:
    number = 0
    out_file_name = 'autostatistical-{}-win64.exe'.format(version)

nsis_args = [r'c:\Program Files (x86)\NSIS\makensis.exe',
             '/DVERSION=' + version,
             '/DNUMBER=' + number,
             '/DOUTFILENAME=' + out_file_name,
             'installer\win\installer.nsi']
call(nsis_args)