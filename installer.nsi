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


Section "Miniconda Python package manager"
  SetOutPath "$TEMP\Miniconda"
  File "Miniconda3-3.7.0-Windows-x86_64.exe"

  DetailPrint "Execute: $TEMP\MiniConda\Miniconda3-3.7.0-Windows-x86_64.exe"
  ${StdUtils.ExecShellWaitEx} $0 $1 "Miniconda3-3.7.0-Windows-x86_64.exe" "" ""

  StrCmp $0 "error" ExecFailed
  StrCmp $0 "no_wait" WaitNotPossible
  StrCmp $0 "ok" WaitForProc
  Abort

  WaitForProc:
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Miniconda installer finished with exit code: $2"
  Goto WaitDone

  ExecFailed:
  DetailPrint "Could not start Miniconda installer (error code: $1)"
  Goto WaitDone

  WaitNotPossible:
  DetailPrint "Could not start Miniconda installer."
  Goto WaitDone

  WaitDone:
  ; Clean up
  SetOutPath "$TEMP"
  RMDir /r "$TEMP\Miniconda"
SectionEnd


Section "Python virtual environment"

  ; Create virtual environment with conda and install packages
  SetOutPath $INSTDIR
  DetailPrint 'Execute: conda create -y -p "$INSTDIR\ohvenv" python pip numpy scipy sqlalchemy Jinja2'
  ${StdUtils.ExecShellWaitEx} $0 $1 "conda" "" 'create -y -p "$INSTDIR\ohvenv" python pip numpy scipy sqlalchemy Jinja2'

  StrCmp $0 "error" ExecFailed1
  StrCmp $0 "no_wait" WaitNotPossible1
  StrCmp $0 "ok" WaitForProc1
  Abort

  WaitForProc1:
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Virtual environment installer finished with exit code: $2"
  Goto WaitDone1

  ExecFailed1:
  DetailPrint "Could not start Virtual environment installer (error code: $1)"
  Goto WaitDone1

  WaitNotPossible1:
  DetailPrint "Could not start Virtual environment installer."
  Goto WaitDone1

  WaitDone1:

  ; Install remaining packages with `pip`
  SetOutPath $INSTDIR\ohvenv\Scripts
  DetailPrint "Execute: pip install autostatistical"
  ${StdUtils.ExecShellWaitEx} $0 $1 "pip" "" "install autostatistical"

  StrCmp $0 "error" ExecFailed2
  StrCmp $0 "no_wait" WaitNotPossible2
  StrCmp $0 "ok" WaitForProc2
  Abort

  WaitForProc2:
  ${StdUtils.WaitForProcEx} $2 $1
  DetailPrint "Completed: Virtual environment installer finished with exit code: $2"
  Goto WaitDone2

  ExecFailed2:
  DetailPrint "Could not start Virtual environment installer (error code: $1)"
  Goto WaitDone2

  WaitNotPossible2:
  DetailPrint "Could not start Virtual environment installer."
  Goto WaitDone2

  WaitDone2:

SectionEnd

Section "Start and context menu items"
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
