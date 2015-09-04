# -*- coding: utf-8 -*-

# OH Auto Statistical
# Copyright (C) 2014-2015  Florenz A. P. Hollebrandse
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_COMPONENTS
!insertmacro MUI_UNPAGE_INSTFILES


Section "un.${APP_NAME}" uninstall_app_packages
  ; Start menu
  RmDir /r "$SMPROGRAMS\${ORG_NAME}\${APP_NAME}"
  RmDir "$SMPROGRAMS\${ORG_NAME}"

  ; OH Auto Statistical program files
  RmDir /r $INSTDIR

  ; Uninstaller registry
  DeleteRegKey HKLM "${UNINST_KEY}"
SectionEnd


Section "un.NRFA data" uninstall_nrfa
  RmDir /r "$LOCALAPPDATA\${ORG_NAME}\fehdata"
SectionEnd


