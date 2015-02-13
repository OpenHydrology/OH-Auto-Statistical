# -*- coding: utf-8 -*-

from subprocess import call

version = open('VERSION').read()
nsis_args = [r'c:\Program Files (x86)\NSIS\makensis.exe',
             '/DVERSION=' + version,
             'installer\win\installer.nsi']
call(nsis_args)