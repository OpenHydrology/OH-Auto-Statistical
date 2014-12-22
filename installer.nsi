!include StdUtils.nsh  ; http://nsis.sourceforge.net/StdUtils_plug-in
; Requires AccessControl plugin http://nsis.sourceforge.net/AccessControl_plug-in
!include "LogicLib.nsh"

Name "OH Auto Statistical"
caption "OH Auto Statistical"
OutFile "dist\Setup-Win64.exe"
RequestExecutionLevel highest

InstallDir "$PROGRAMFILES64\Open Hydrology\OH Auto Statistical"

Page components
Page instfiles


Section "Miniconda package manager"

  ; Install Miniconda
  SetOutPath "$TEMP\Miniconda"
  File "Miniconda3-3.7.0-Windows-x86_64.exe"

  DetailPrint "Run Miniconda installer"
  ${StdUtils.ExecShellWaitEx} $0 $1 "Miniconda3-3.7.0-Windows-x86_64.exe" "" '/D="$PROGRAMFILES64\Miniconda3"'
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Miniconda installer finished with exit code: $2"

  ; Clean up
  SetOutPath "$TEMP"
  RMDir /r "$TEMP\Miniconda"

SectionEnd


Section "OH Auto Statistical packages"

  ; Update conda first
  DetailPrint "Updating conda"
  ${StdUtils.ExecShellWaitEx} $0 $1 "conda" "" "update -y conda"
  ${StdUtils.WaitForProcEx} $2 $1

  ; Create virtual environment with conda and install packages
  SetOutPath $INSTDIR
  DetailPrint "Creating virtual environment"
  ${StdUtils.ExecShellWaitEx} $0 $1 "conda" "" 'create -y -p "$INSTDIR\ohvenv" python pip numpy scipy sqlalchemy Jinja2'
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Virtual environment installer finished with exit code: $2"

  ; Install remaining packages with `pip`
  SetOutPath $INSTDIR\ohvenv\Scripts
  DetailPrint "Installing remaining packages"
  ${StdUtils.ExecShellWaitEx} $0 $1 "pip" "" "install autostatistical"
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Virtual environment installer finished with exit code: $2"

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
  File "docs\source\*.url"

SectionEnd
