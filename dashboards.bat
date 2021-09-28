"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\getpartners.py"

cd "CommandLineUtility"

rem login to Tableau online
tabcmd login -s tableau_server -u tableau_username -p tableau_password

rem export SOME_DASHBOARD for each district + parameter combo
FOR /F "tokens=1" %%a IN (C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\districts.csv) DO (
	FOR /F "tokens=1" %%b IN (C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\viewbyparams.csv) DO (
		tabcmd export "SOME_DASHBOARD?refresh=yes&District%%20Name=%%a&View%%20by%%20parameter=%%b" --pdf --width 1366 --height 768 --pagelayout landscape -f "C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\SOMEDASHBOARDExports_Script\some_dashboard%%a%%b.pdf"))

rem export SOME_DASHBOARD for each county + parameter combo
FOR /F "tokens=1" %%a IN (C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\counties.csv) DO (
	FOR /F "tokens=1" %%b IN (C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\viewbyparams.csv) DO (
		tabcmd export "SOME_DASHBOARDCounty/DataSharingDashboardCounty?refresh=yes&County=%%a&View%%20by%%20parameter=%%b" --pdf --width 1366 --height 768 --pagelayout landscape -f "C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\SOME_DASHBOARDExports_ScriptCounty\some_dashboard%%a%%b.pdf"))

timeout 10

rem rename all files in the folder of interest to replace %20 with an underscore
SETLOCAL DISABLEDELAYEDEXPANSION

SET rendir=C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\SOME_DASHBOARDExports_Script
FOR /F "USEBACKQ DELIMS=" %%N IN (

`DIR /A-D /B "%rendir%"`

) DO (

    SET "Var=%%~NXN"
    SETLOCAL ENABLEDELAYEDEXPANSION
    SET "Orig=!Var!"
    SET "Var=!Var:%%20=_!"

  IF NOT "!Var!"=="!Orig!" (
    IF NOT EXIST "%%~DPN!Var!" (
      REN "%rendir%\!Orig!" "!Var!"

) ELSE (
    GOTO EOF
)
)
  ENDLOCAL
)

SET rendir=C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\SOME_DASHBOARDExports_ScriptCounty
FOR /F "USEBACKQ DELIMS=" %%N IN (

`DIR /A-D /B "%rendir%"`

) DO (

    SET "Var=%%~NXN"
    SETLOCAL ENABLEDELAYEDEXPANSION
    SET "Orig=!Var!"
    SET "Var=!Var:%%20=_!"

  IF NOT "!Var!"=="!Orig!" (
    IF NOT EXIST "%%~DPN!Var!" (
      REN "%rendir%\!Orig!" "!Var!"

) ELSE (
    GOTO EOF
)
)
  ENDLOCAL
)

rem upload to SF
"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\sf_upload.py"

rem send email notification
"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\emailnotification.py"

rem delete counties & districts csv, delete pdfs
"C:\Users\Administrator\AppData\Local\Programs\Python\Python38\python.exe" "C:\Users\Administrator\CommandLineUtility\DistrictDashboardSharing\delete_files.py"
