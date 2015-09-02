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

; Imports

!include MUI2.nsh
!include StdUtils.nsh  ; http://nsis.sourceforge.net/StdUtils_plug-in
!include "LogicLib.nsh"
!include ".\includes\dumplog.nsi"


; Constants

!define APP_NAME "OH Auto Statistical"
; !define VERSION "0.0.0" ; should be set by `makensis` argument e.g. `/DVERSION=0.0.0`

!define ORG_NAME "Open Hydrology"
!define ORG_URL "http://open-hydrology.org"
!define HELP_URL "http://docs.open-hydrology.org"
!define PACKAGE_NAME "autostatistical"
; !define CONDA_CHANNEL "https://conda.binstar.org/openhydrology"  ; should be set by `makensis` argument
!define CONDA_URL "https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe"

; Interface settings
!define MUI_WELCOMEPAGE_TITLE "${APP_NAME} ${VERSION} setup"
!define MUI_WELCOMEPAGE_TEXT "Fully automated flood estimation for UK catchments using the latest revisions to the Flood Estimation Handbook Statistical Method.$\r$\n$\r$\nThis installer requires an internet connection."
!define MUI_FINISHPAGE_LINK "${ORG_NAME} website"
!define MUI_FINISHPAGE_LINK_LOCATION "${ORG_URL}"
!define MUI_FINISHPAGE_SHOWREADME "http://docs.open-hydrology.org/projects/oh-auto-statistical/"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Read the manual"
!define MUI_COMPONENTSPAGE_NODESC
!define MUI_WELCOMEFINISHPAGE_BITMAP "images\OH.portrait.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_HEADERIMAGE_BITMAP "images\OH.landscape.bmp"
!define MUI_HEADERIMAGE_BITMAP_STRETCH "AspectFitHeight"
!define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\${PACKAGE_NAME}"

Name "${APP_NAME}"
; !define OUTFILENAME "${PACKAGE_NAME}-${VERSION}-win64.exe"  ; Should be set from makensis argument
OutFile "..\..\dist\${OUTFILENAME}"
InstallDir "$LOCALAPPDATA\Continuum\Miniconda3\envs\_app_own_environment_${PACKAGE_NAME}"
RequestExecutionLevel user

; Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE LICENSE
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!include uninstaller.nsi

; Language settings
!insertmacro MUI_LANGUAGE "English"


Section "Conda package manager" miniconda_installer

  ; Install Miniconda
  SetOutPath "$TEMP\Conda"
  DetailPrint "Downloading Conda installer"
  NSISdl::download /TIMEOUT=1800000 ${CONDA_URL} Miniconda3_setup.exe
  Pop $R0
  StrCmp $R0 "success" +4
    MessageBox MB_OK "Conda could not be downloaded."
    DetailPrint "Conda could not be downloaded (exit code $R0)."
    Goto .finally
  DetailPrint "Conda successfully downloaded."

  DetailPrint "Running Conda installer"
  ; Default installation location %LOCALAPPDATA%/Continuum/Miniconda3/
  ${StdUtils.ExecShellWaitEx} $0 $1 "Miniconda3_setup.exe" "" \
    "/InstallationType=JustMe /AddtoPath=1 /RegisterPython=0 /S"
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Conda installer finished with exit code: $2"

  ; Clean up
  SetOutPath "$TEMP"
  RMDir /r "$TEMP\Conda"

SectionEnd


Section "${APP_NAME} program files" application_packages

  ; Remove any existing application files
  IfFileExists "$INSTDIR\*.*" 0 +3
    DetailPrint "Existing ${APP_NAME} program files detected"
    DetailPrint "Existing files in $INSTDIR will be removed"
    RMDir /r "$INSTDIR"

  ; Create python environment with conda and install packages
  !define CONDA "$LOCALAPPDATA\Continuum\Miniconda3\Scripts\conda"

  ; Update miniconda package manager only if we haven't just installed it
  SectionGetFlags ${miniconda_installer} $0
  IntCmp $0 16 0 +3 +3
    DetailPrint "Updating Conda package manager"
    ExecDos::exec /DETAILED '"${CONDA}" update -y conda' "" ""

  DetailPrint "Searching in channel(s) -c ${CONDA_CHANNEL}"
  DetailPrint "Installing application packages (version ${VERSION}-${BUILD})"

  ExecDos::exec /DETAILED '"${CONDA}" create -y -n "_app_own_environment_${PACKAGE_NAME}" \
    -c ${CONDA_CHANNEL} python ${PACKAGE_NAME}=${VERSION}=${BUILD}' "" ""

  Pop $0
  IntCmp $0 0 +4 0 0
    MessageBox MB_OK "Application packages could not be installed."
    DetailPrint "Application packages could not be installed (exit code $0)."
    Goto .finally
  DetailPrint "Application packages installed (exit code $0)"

  ; Uninstaller details
  WriteUninstaller $INSTDIR\uninstall.exe
  WriteRegStr HKCU "${UNINST_KEY}" "DisplayName" "${APP_NAME}"
  WriteRegStr HKCU "${UNINST_KEY}" "Publisher" "${ORG_NAME}"
  WriteRegStr HKCU "${UNINST_KEY}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteRegStr HKCU "${UNINST_KEY}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKCU "${UNINST_KEY}" "NoRepair" 1
  WriteRegStr HKCU "${UNINST_KEY}" "HelpLink" "${HELP_URL}"
  WriteRegStr HKCU "${UNINST_KEY}" "URLInfoAbout" "${ORG_URL}"
  WriteRegDWORD HKCU "${UNINST_KEY}" "EstimatedSize" 408964

SectionEnd


Section "Start menu"

  SetOutPath "$INSTDIR\icons"
  File "images\*.ico"

  ; Start menu: run program
  SetOutPath "$SMPROGRAMS\${ORG_NAME}\${APP_NAME}"
  CreateShortcut "OH Auto Statistical.lnk" "$INSTDIR\pythonw.exe" "-m ${PACKAGE_NAME}" "$INSTDIR\icons\application.ico" 0

  ; Start menu: link to online documentation
  File "..\..\docs\source\*.url"

  ; Start menu: download NRFA data
  CreateShortcut "Download NRFA data.lnk" "$INSTDIR\Scripts\download_nrfa.exe" "" "$INSTDIR\icons\download.ico" 0

SectionEnd


Section "Download NRFA data"

  DetailPrint "Downloading NRFA data"
  ExecDos::exec /DETAILED "$INSTDIR\Scripts\download_nrfa.exe" "" ""
  DetailPrint "Completed: NRFA data downloaded completed."

SectionEnd


Section -Log

.finally:

  StrCpy $0 "$INSTDIR\install.log"
  Push $0
  Call DumpLog
SectionEnd


Function .onInit

  SectionSetFlags ${miniconda_installer} 17 ; Selected and read-only
  SectionSetFlags ${application_packages} 17

  ; Check if Miniconda has already been installed
  IfFileExists "$LOCALAPPDATA\Continuum\Miniconda3\Uninstall-Anaconda.exe" 0 +5
    SectionSetFlags ${miniconda_installer} 16 ; Unselected and read-only
    SectionGetText ${miniconda_installer} $0
    StrCpy $0 "$0 (already installed)"
    SectionSetText ${miniconda_installer} $0

FunctionEnd
