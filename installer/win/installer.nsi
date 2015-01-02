!include MUI2.nsh
!include StdUtils.nsh  ; http://nsis.sourceforge.net/StdUtils_plug-in
; Requires AccessControl plugin http://nsis.sourceforge.net/AccessControl_plug-in
!include "LogicLib.nsh"

Name "OH Auto Statistical"
OutFile "..\..\dist\ohautostatistical-win64-latest.exe"
RequestExecutionLevel highest

InstallDir "$PROGRAMFILES64\Open Hydrology\OH Auto Statistical"

; Interface settings
!define MUI_WELCOMEPAGE_TITLE "OH Auto Statistical setup"
!define MUI_WELCOMEPAGE_TEXT "Fully automated flood estimation for UK catchments using the latest revisions to the Flood Estimation Handbook Statistical Method.$\r$\n$\r$\nThis installer requires an internet connection."
!define MUI_FINISHPAGE_LINK "Open Hydrology website"
!define MUI_FINISHPAGE_LINK_LOCATION "http://open-hydrology.org"
!define MUI_FINISHPAGE_SHOWREADME "http://docs.open-hydrology.org/projects/oh-auto-statistical/en/latest/"
!define MUI_FINISHPAGE_SHOWREADME_TEXT "Read the manual"
!define MUI_COMPONENTSPAGE_NODESC
!define MUI_WELCOMEFINISHPAGE_BITMAP "images\OH.portrait.bmp"
!define MUI_HEADERIMAGE
!define MUI_HEADERIMAGE_RIGHT
!define MUI_HEADERIMAGE_BITMAP "images\OH.landscape.bmp"
!define MUI_HEADERIMAGE_BITMAP_STRETCH "AspectFitHeight"

; Installer pages
!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE LICENSE
!insertmacro MUI_PAGE_COMPONENTS
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

; Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

; Language settings
!insertmacro MUI_LANGUAGE "English"


Section "Miniconda package manager" miniconda_installer

  ; Install Miniconda
  SetOutPath "$TEMP\Miniconda"
  File "bin\Miniconda3-3.7.0-Windows-x86_64.exe"

  DetailPrint "Run Miniconda installer"
  ${StdUtils.ExecShellWaitEx} $0 $1 "Miniconda3-3.7.0-Windows-x86_64.exe" "" "/S /D=$PROGRAMFILES64\Miniconda3"
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Miniconda installer finished with exit code: $2"

  ; Clean up
  SetOutPath "$TEMP"
  RMDir /r "$TEMP\Miniconda"

SectionEnd


Section "OH Auto Statistical packages"
  IfFileExists $INSTDIR\*.* 0 +3
    DetailPrint "Existing OH Auto Statistical packages detected"
    DetailPrint "Existing files will be removed"
    RMDir /r $INSTDIR

  ; Update conda first
  DetailPrint "Updating conda"
  ${StdUtils.ExecShellWaitEx} $0 $1 "$PROGRAMFILES64\Miniconda3\Scripts\conda" "" "update conda --yes"
  ${StdUtils.WaitForProcEx} $2 $1

  ; Create virtual environment with conda and install packages
  SetOutPath $INSTDIR
  DetailPrint "Creating virtual environment"
  ${StdUtils.ExecShellWaitEx} $0 $1 "$PROGRAMFILES64\Miniconda3\Scripts\conda" "" 'create -y -p "$INSTDIR\ohvenv" python pip numpy scipy sqlalchemy Jinja2'
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Virtual environment installer finished with exit code: $2"

  ; Install remaining packages with `pip`
  DetailPrint "Installing remaining packages"
  ${StdUtils.ExecShellWaitEx} $0 $1 "$INSTDIR\ohvenv\Scripts\pip" "" "install autostatistical"
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: remaining packages installation finished with exit code: $2"

  ; Uninstaller
  WriteUninstaller $INSTDIR\uninstall.exe
  !define UNINST_KEY "Software\Microsoft\Windows\CurrentVersion\Uninstall\OHAutoStatistical"
  WriteRegStr HKLM "${UNINST_KEY}" "DisplayName" "OH Auto Statistical"
  WriteRegStr HKLM "${UNINST_KEY}" "Publisher" "Open Hydrology"
  WriteRegStr HKLM "${UNINST_KEY}" "UninstallString" "$\"$INSTDIR\uninstall.exe$\""
  WriteRegStr HKLM "${UNINST_KEY}" "QuietUninstallString" "$\"$INSTDIR\uninstall.exe$\" /S"
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoModify" 1
  WriteRegDWORD HKLM "${UNINST_KEY}" "NoRepair" 1
  WriteRegStr HKLM "${UNINST_KEY}" "HelpLink" "http://docs.open-hydrology.org"
  WriteRegStr HKLM "${UNINST_KEY}" "URLInfoAbout" "http://open-hydrology.org"
  WriteRegDWORD HKLM "${UNINST_KEY}" "EstimatedSize" 408964

SectionEnd


Section "Start menu and context menu items"

  ; Context menu: right-click "Create OH Auto Statistical report"
  WriteRegStr HKCR ".cd3" "" "OH.CD3"
  WriteRegStr HKCR ".cd3" "PerceivedType" "text"
  WriteRegStr HKCR "OH.CD3" "" "Catchment descriptors file"
  ReadRegStr $R0 HKCR "OH.CD3\shell\open\command" ""
  ${If} $R0 == ""
    WriteRegStr HKCR "OH.CD3\shell" "" "open"
    WriteRegStr HKCR "OH.CD3\shell\open\command" "" 'notepad.exe "%1"'
  ${EndIf}
  WriteRegStr HKCR "OH.CD3\shell\run" "" "Create OH Auto Statistical report"
  WriteRegStr HKCR "OH.CD3\shell\run\command" "" '"$INSTDIR\ohvenv\python.exe" -m autostatistical "%1"'

  ; Start menu: link to online documentation
  SetOutPath "$SMPROGRAMS\Open Hydrology\OH Auto Statistical"
  File "..\..\docs\source\*.url"

  ; Start menu: download NRFA data
  SetOutPath "$INSTDIR\icons"
  File "images\download.ico"
  SetOutPath "$SMPROGRAMS\Open Hydrology\OH Auto Statistical"
  CreateShortcut "Reload NRFA data.lnk" "$INSTDIR\ohvenv\python.exe" '"$INSTDIR\ohvenv\Lib\site-packages\autostatistical\download_nrfa.py"' "$INSTDIR\icons\download.ico" 0

SectionEnd


Section "Download NRFA data"

  DetailPrint "Downloading NRFA data"
  ${StdUtils.ExecShellWaitEx} $0 $1 "$INSTDIR\ohvenv\python.exe" "" '"$INSTDIR\ohvenv\Lib\site-packages\autostatistical\download_nrfa.py"'
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: NRFA data downloaded completed with exit code: $2"

SectionEnd


Section Uninstall

  ; Start menu
  RmDir /r "$SMPROGRAMS\Open Hydrology\OH Auto Statistical"
  RmDir "$SMPROGRAMS\Open Hydrology"

  ; Win context menu
  DeleteRegKey HKCR "OH.CD3"
  DeleteRegKey HKCR ".cd3"

  ; OH Auto Statistical program files
  RmDir /r $INSTDIR

  ; Uninstaller registry
  DeleteRegKey HKLM "${UNINST_KEY}"

SectionEnd

Function .onInit

  ; Check if Miniconda has already been installed
  IfFileExists $PROGRAMFILES64\Miniconda3\Uninstall-Anaconda.exe 0 +4
    SectionSetFlags ${miniconda_installer} 16 ; Unselected and read-only
    SectionGetText ${miniconda_installer} $0
    StrCpy $0 "$0 (already installed)"
    SectionSetText ${miniconda_installer} $0

FunctionEnd