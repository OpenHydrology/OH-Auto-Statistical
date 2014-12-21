Name "OH Auto Statistical"
caption "OH Auto Statistical"
OutFile "Setup-64bit.exe"
RequestExecutionLevel user

InstallDir "$PROGRAMFILES64\Open Hydrology\OH Auto Statistical"

Page components
Page instfiles

Section "Python"
  SetOutPath $INSTDIR
  File /r "venv\*.*"
SectionEnd
